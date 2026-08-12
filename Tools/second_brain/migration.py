from __future__ import annotations

import argparse
import ctypes
from dataclasses import asdict, dataclass
import errno
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import sys

from Tools.second_brain.inventory import NoteRecord, scan_notes
from Tools.second_brain.note_io import parse_markdown, render_markdown, rewrite_wikilinks
from Tools.second_brain.policy import MigrationPolicy


PROTECTED_PATHS = {".obsidian/core-plugins.json", ".obsidian/graph.json", ".obsidian/workspace.json"}
AUDIT_OUTPUT_ROOT = Path("docs/superpowers/migrations")
CANONICAL_ARCHIVE_ROOT = Path("90 보관함/이전 LLM Wiki")
SUPPORTED_ACTIONS = frozenset({"archive", "move"})
ACTION_FIELDS = frozenset({"action", "metadata", "source", "target"})
REWRITE_EXCLUDED_ROOTS = frozenset(
    root.casefold()
    for root in (".superpowers", "docs", "Tools", ".codex_recovery", ".obsidian", ".worktrees")
)
EMBED_WIKILINK_RE = re.compile(r"!\[\[([^\]|#^]+)([#^][^\]|]*)?(\|[^\]]+)?\]\]")
WINDOWS_ILLEGAL_PATH_CHARACTERS = frozenset('<>:"|?*')


@dataclass(frozen=True)
class MigrationAction:
    source: str
    target: str
    action: str
    metadata: dict[str, object]


@dataclass(frozen=True)
class _FileState:
    identity: tuple[int, int]
    value: bytes
    mode: int
    atime_ns: int
    mtime_ns: int


@dataclass
class _MoveAttempt:
    source: Path
    target: Path
    identity: tuple[int, int]
    source_parent_identity: tuple[int, int]
    target_parent_identity: tuple[int, int]
    state: str = "attempted"


def make_id(old_relative_path: str, created: str) -> str:
    day = created.replace("-", "") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", created) else "20260811"
    suffix = hashlib.sha256(old_relative_path.encode("utf-8")).hexdigest()[:4]
    return f"{day}000000-{suffix}"


def build_actions(records: list[NoteRecord], policy: MigrationPolicy) -> list[MigrationAction]:
    actions = []
    for record in sorted(records, key=lambda item: item.path):
        route = policy.route(record.path, str(record.metadata.get("status", "")))
        actions.append(MigrationAction(record.path, route.target, route.action, route.metadata))
    return actions


def _inside(root: Path, candidate: Path) -> bool:
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        return False


def _unsafe_windows_path_component(component: str) -> bool:
    if component in (".", ".."):
        return False
    if not component or component.endswith((" ", ".")):
        return True
    if any(
        ord(character) < 32 or character in WINDOWS_ILLEGAL_PATH_CHARACTERS
        for character in component
    ):
        return True
    return PureWindowsPath(component).is_reserved()


def _is_link_or_reparse_point(path: Path) -> bool:
    try:
        if path.is_symlink():
            return True
        is_junction = getattr(path, "is_junction", None)
        if is_junction is not None and is_junction():
            return True
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    except (OSError, RuntimeError) as error:
        raise ValueError("migration path cannot be inspected safely") from error
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _has_link_or_reparse_component(root: Path, relative_path: Path) -> bool:
    candidate = root
    for part in relative_path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            candidate = candidate.parent
            continue
        candidate = candidate / part
        if (
            candidate != root
            and _inside(root, candidate)
            and _is_link_or_reparse_point(candidate)
        ):
            return True
    return False


def _identity(status: os.stat_result) -> tuple[int, int]:
    return status.st_dev, status.st_ino


def _lstat_without_links(path: Path) -> os.stat_result:
    status = path.lstat()
    attributes = getattr(status, "st_file_attributes", 0)
    if stat.S_ISLNK(status.st_mode) or attributes & getattr(
        stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0
    ):
        raise ValueError(f"migration path is a symbolic link or reparse point: {path}")
    return status


def _validate_contained_path(root: Path, path: Path) -> Path:
    try:
        relative = path.relative_to(root)
    except ValueError as error:
        raise ValueError(f"migration path is outside vault: {path}") from error
    if _has_link_or_reparse_component(root, relative):
        raise ValueError(f"migration path contains a symbolic link or reparse point: {path}")
    try:
        resolved = path.resolve(strict=True)
    except (OSError, RuntimeError) as error:
        raise ValueError(f"migration path cannot be resolved safely: {path}") from error
    if not _inside(root, resolved):
        raise ValueError(f"migration path resolves outside vault: {path}")
    return resolved


def _validate_directory(
    root: Path,
    path: Path,
    expected_identity: tuple[int, int] | None = None,
) -> os.stat_result:
    _validate_contained_path(root, path)
    status = _lstat_without_links(path)
    if not stat.S_ISDIR(status.st_mode):
        raise ValueError(f"migration directory changed: {path}")
    if expected_identity is not None and _identity(status) != expected_identity:
        raise ValueError(f"migration directory identity changed: {path}")
    return status


def _validate_regular_file(
    root: Path,
    path: Path,
    expected_identity: tuple[int, int] | None = None,
) -> os.stat_result:
    _validate_contained_path(root, path)
    status = _lstat_without_links(path)
    if not stat.S_ISREG(status.st_mode):
        raise ValueError(f"migration file changed: {path}")
    if expected_identity is not None and _identity(status) != expected_identity:
        raise ValueError(f"migration file identity changed: {path}")
    return status


def _path_identity_without_links(path: Path) -> tuple[int, int] | None:
    try:
        return _identity(_lstat_without_links(path))
    except FileNotFoundError:
        return None


def _open_verified_file(
    root: Path,
    path: Path,
    expected_identity: tuple[int, int],
    *,
    writable: bool,
) -> int:
    _validate_regular_file(root, path, expected_identity)
    flags = os.O_RDWR if writable else os.O_RDONLY
    flags |= getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        status = os.fstat(descriptor)
        if not stat.S_ISREG(status.st_mode) or _identity(status) != expected_identity:
            raise ValueError(f"migration file identity changed while opening: {path}")
        return descriptor
    except Exception:
        os.close(descriptor)
        raise


def _read_descriptor(descriptor: int) -> bytes:
    os.lseek(descriptor, 0, os.SEEK_SET)
    chunks = []
    while True:
        chunk = os.read(descriptor, 1024 * 1024)
        if not chunk:
            return b"".join(chunks)
        chunks.append(chunk)


def _capture_file_state(
    root: Path,
    path: Path,
    expected_identity: tuple[int, int] | None = None,
) -> _FileState:
    status = _validate_regular_file(root, path, expected_identity)
    file_identity = _identity(status)
    descriptor = _open_verified_file(root, path, file_identity, writable=False)
    try:
        value = _read_descriptor(descriptor)
    finally:
        os.close(descriptor)
    return _FileState(
        identity=file_identity,
        value=value,
        mode=stat.S_IMODE(status.st_mode),
        atime_ns=status.st_atime_ns,
        mtime_ns=status.st_mtime_ns,
    )


def _write_all(descriptor: int, value: bytes) -> None:
    view = memoryview(value)
    written = 0
    while written < len(view):
        count = os.write(descriptor, view[written:])
        if count <= 0:
            raise OSError("migration write made no progress")
        written += count


def _write_file_bytes(
    root: Path,
    path: Path,
    expected_identity: tuple[int, int],
    value: bytes,
) -> None:
    descriptor = _open_verified_file(root, path, expected_identity, writable=True)
    try:
        os.lseek(descriptor, 0, os.SEEK_SET)
        os.ftruncate(descriptor, 0)
        _write_all(descriptor, value)
    finally:
        os.close(descriptor)


def _set_descriptor_times(descriptor: int, atime_ns: int, mtime_ns: int) -> None:
    if os.name != "nt":
        os.utime(descriptor, ns=(atime_ns, mtime_ns))
        return
    import msvcrt

    class FileTime(ctypes.Structure):
        _fields_ = [("low", ctypes.c_uint32), ("high", ctypes.c_uint32)]

    def file_time(value_ns: int) -> FileTime:
        ticks = value_ns // 100 + 116_444_736_000_000_000
        return FileTime(ticks & 0xFFFFFFFF, ticks >> 32)

    access = file_time(atime_ns)
    modified = file_time(mtime_ns)
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    set_file_time = kernel32.SetFileTime
    set_file_time.argtypes = [
        ctypes.c_void_p,
        ctypes.c_void_p,
        ctypes.POINTER(FileTime),
        ctypes.POINTER(FileTime),
    ]
    set_file_time.restype = ctypes.c_int
    handle = msvcrt.get_osfhandle(descriptor)
    if not set_file_time(handle, None, ctypes.byref(access), ctypes.byref(modified)):
        error_number = ctypes.get_last_error()
        raise OSError(error_number, ctypes.FormatError(error_number))


def _restore_file_state(root: Path, path: Path, state: _FileState) -> None:
    _write_file_bytes(root, path, state.identity, state.value)
    descriptor = _open_verified_file(root, path, state.identity, writable=True)
    try:
        if hasattr(os, "fchmod"):
            os.fchmod(descriptor, state.mode)
        elif stat.S_IMODE(os.fstat(descriptor).st_mode) != state.mode:
            raise NotImplementedError("identity-safe mode restoration is unavailable")
        _set_descriptor_times(descriptor, state.atime_ns, state.mtime_ns)
    finally:
        os.close(descriptor)


def _atomic_rename_noreplace(source: Path, target: Path) -> None:
    """Rename on one volume without replacing an entry created at the destination."""
    if os.name == "nt":
        os.rename(source, target)
        return
    if sys.platform.startswith("linux"):
        libc = ctypes.CDLL(None, use_errno=True)
        renameat2 = getattr(libc, "renameat2", None)
        if renameat2 is None:
            raise OSError(errno.ENOTSUP, "atomic no-replace rename is unavailable")
        renameat2.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint]
        renameat2.restype = ctypes.c_int
        result = renameat2(
            -100,
            os.fsencode(source),
            -100,
            os.fsencode(target),
            1,
        )
        if result != 0:
            error_number = ctypes.get_errno()
            raise OSError(error_number, os.strerror(error_number), str(source), str(target))
        return
    raise OSError(errno.ENOTSUP, "atomic no-replace rename is unavailable")


def _rename_same_volume(
    root: Path,
    source: Path,
    target: Path,
    source_identity: tuple[int, int],
    source_parent_identity: tuple[int, int],
    target_parent_identity: tuple[int, int],
) -> None:
    source_status = _validate_regular_file(root, source, source_identity)
    _validate_directory(root, source.parent, source_parent_identity)
    target_parent_status = _validate_directory(root, target.parent, target_parent_identity)
    try:
        _lstat_without_links(target)
    except FileNotFoundError:
        pass
    else:
        raise FileExistsError(f"migration target appeared concurrently: {target}")
    if source_status.st_dev != target_parent_status.st_dev:
        raise ValueError("migration move requires source and target on the same filesystem volume")
    try:
        _atomic_rename_noreplace(source, target)
    except OSError as error:
        if error.errno == errno.EXDEV:
            raise ValueError(
                "migration move requires source and target on the same filesystem volume"
            ) from error
        raise


def _resolve_source(vault: Path, source: Path) -> tuple[Path, Path]:
    root = vault.resolve()
    if source.is_absolute():
        raise ValueError("source must be vault-relative")
    resolved = (root / source).resolve()
    if not _inside(root, resolved):
        raise ValueError("source is outside vault")
    obsidian_root = (root / ".obsidian").resolve()
    if resolved == obsidian_root or _inside(obsidian_root, resolved):
        raise ValueError("source is protected")
    if not resolved.exists():
        raise ValueError("source does not exist")
    if not resolved.is_dir():
        raise ValueError("source is not a directory")
    return root, resolved


def _scan_source(vault: Path, source: Path) -> list[NoteRecord]:
    root, source_root = _resolve_source(vault, source)
    for candidate in source_root.rglob("*.md"):
        if not _inside(source_root, candidate.resolve()):
            raise ValueError("source contains a Markdown path outside its subtree")
    prefix = source_root.relative_to(root)
    records = []
    for record in scan_notes(source_root):
        records.append(
            NoteRecord(
                path=(prefix / Path(record.path)).as_posix(),
                title=record.title,
                metadata=record.metadata,
                wikilinks=record.wikilinks,
            )
        )
    return records


def _archive_root_for_action(root: Path, source: Path, target: Path) -> Path:
    source_parts = source.relative_to(root).parts
    target_parts = target.relative_to(root).parts
    if (
        not source_parts
        or len(target_parts) <= len(source_parts)
        or target_parts[-len(source_parts) :] != source_parts
    ):
        raise ValueError(
            "archive target must preserve source relative path beneath an archive root"
        )
    archive_root = root.joinpath(*target_parts[: -len(source_parts)]).resolve()
    if archive_root == root or not _inside(root, archive_root):
        raise ValueError("archive target must use an archive root inside the vault")
    return archive_root


def _validate_actions(vault: Path, actions: list[MigrationAction]) -> list[tuple[MigrationAction, Path, Path]]:
    root = vault.resolve()
    validated = []
    targets: set[Path] = set()
    sources: set[Path] = set()
    for action in actions:
        if action.action not in SUPPORTED_ACTIONS:
            raise ValueError(f"unsupported action type: {action.action}")
        source_path, target_path = Path(action.source), Path(action.target)
        if source_path.is_absolute() or target_path.is_absolute():
            raise ValueError("source or target must be vault-relative")
        if any(_unsafe_windows_path_component(part) for part in source_path.parts):
            raise ValueError("source path contains an unsafe Windows path component")
        if any(_unsafe_windows_path_component(part) for part in target_path.parts):
            raise ValueError("target path contains an unsafe Windows path component")
        if _has_link_or_reparse_component(root, source_path):
            raise ValueError(
                "source path contains a symbolic link, junction, or reparse point"
            )
        if _has_link_or_reparse_component(root, target_path):
            raise ValueError(
                "target path contains a symbolic link, junction, or reparse point"
            )
        source, target = (root / source_path).resolve(), (root / target_path).resolve()
        if not _inside(root, source) or not _inside(root, target):
            raise ValueError("source or target is outside vault")
        obsidian_root = (root / ".obsidian").resolve()
        if _inside(obsidian_root, source) or _inside(obsidian_root, target):
            raise ValueError("protected Obsidian file")
        if source_path.suffix.lower() != ".md":
            raise ValueError("source must be a Markdown path")
        if target_path.suffix.lower() != ".md":
            raise ValueError("target must be a Markdown path")
        if source.suffix.lower() != ".md":
            raise ValueError("resolved source must be a Markdown file")
        if action.action == "archive":
            _archive_root_for_action(root, source, target)
        if target in targets:
            raise ValueError("duplicate target")
        if source in sources:
            raise ValueError("duplicate source")
        if not source.is_file():
            raise ValueError(f"source does not exist: {action.source}")
        targets.add(target)
        sources.add(source)
        validated.append((action, source, target))
    for _, source, target in validated:
        if target.exists() and target != source:
            raise ValueError(f"target already exists: {target.relative_to(root)}")
        parent = target.parent
        while parent != root:
            if parent.exists() or parent.is_symlink():
                if not parent.is_dir():
                    raise ValueError(
                        f"target parent is not a directory: {parent.relative_to(root)}"
                    )
                break
            parent = parent.parent
    ordered_targets = [target for _, _, target in validated]
    for index, target in enumerate(ordered_targets):
        for other in ordered_targets[index + 1 :]:
            if _inside(target, other) or _inside(other, target):
                raise ValueError("target conflicts with another target parent")
    return validated


def _normalized_note_bytes(value: bytes, metadata: dict[str, object], old_path: str) -> bytes:
    if not metadata:
        return value
    note = parse_markdown(value.decode("utf-8"))
    note.metadata.update(metadata)
    if not note.metadata.get("id"):
        note.metadata["id"] = make_id(old_path, str(note.metadata.get("created", "")))
    return render_markdown(note).encode("utf-8")


def _rewrite_embedded_note_links(body: str, title_map: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        title = match.group(1).strip()
        suffix = match.group(2) or ""
        alias = match.group(3) or ""
        return f"![[{title_map.get(title, title)}{suffix}{alias}]]"

    return EMBED_WIKILINK_RE.sub(replace, body)


def _resolve_rewrite_candidate(root: Path, path: Path) -> Path | None:
    relative = path.relative_to(root)
    if relative.parts[0].casefold() in REWRITE_EXCLUDED_ROOTS:
        return None
    try:
        if _has_link_or_reparse_component(root, relative):
            return None
        resolved = path.resolve()
        if not _inside(root, resolved) or not resolved.is_file():
            return None
        if resolved.suffix.casefold() != ".md":
            return None
        if resolved.relative_to(root).parts[0].casefold() in REWRITE_EXCLUDED_ROOTS:
            return None
    except OSError:
        return None
    return resolved


def _create_parent_directories(
    root: Path,
    parent: Path,
    created_directories: list[tuple[Path, tuple[int, int] | None]],
) -> None:
    missing = []
    candidate = parent
    while candidate != root:
        try:
            _lstat_without_links(candidate)
        except FileNotFoundError:
            missing.append(candidate)
            candidate = candidate.parent
            continue
        _validate_directory(root, candidate)
        break
    if candidate == root:
        _validate_directory(root, root)
    for directory in reversed(missing):
        _validate_directory(root, directory.parent)
        try:
            directory.mkdir()
        except FileExistsError:
            _validate_directory(root, directory)
        else:
            created_directories.append((directory, None))
            status = _validate_directory(root, directory)
            created_directories[-1] = (
                directory,
                _identity(status),
            )


def _reconcile_move(attempt: _MoveAttempt) -> str:
    try:
        source_identity = _path_identity_without_links(attempt.source)
    except (OSError, ValueError):
        return "ambiguous"
    try:
        target_identity = _path_identity_without_links(attempt.target)
    except (OSError, ValueError):
        return "ambiguous"
    if source_identity == attempt.identity and target_identity is None:
        return "not-moved"
    if source_identity is None and target_identity == attempt.identity:
        return "moved"
    return "ambiguous"


def _rollback_actions(
    root: Path,
    attempts: list[_MoveAttempt],
    original_states: dict[Path, _FileState],
    created_directories: list[tuple[Path, tuple[int, int] | None]],
) -> list[str]:
    failures = []
    for path, state in reversed(tuple(original_states.items())):
        try:
            _restore_file_state(root, path, state)
        except Exception as error:
            failures.append(
                f"restore {path}: {type(error).__name__}: {error}"
            )
    for attempt in reversed(attempts):
        try:
            state = _reconcile_move(attempt)
            attempt.state = state
            if state == "not-moved":
                continue
            if state != "moved":
                raise RuntimeError("attempted move state is ambiguous")
            _rename_same_volume(
                root,
                attempt.target,
                attempt.source,
                attempt.identity,
                attempt.target_parent_identity,
                attempt.source_parent_identity,
            )
            if _reconcile_move(attempt) != "not-moved":
                raise RuntimeError("rollback rename result is ambiguous")
        except Exception as error:
            failures.append(
                f"move {attempt.target} back to {attempt.source}: "
                f"{type(error).__name__}: {error}"
            )
    for directory, expected_identity in reversed(created_directories):
        try:
            if expected_identity is None:
                raise RuntimeError("created directory identity is unavailable")
            status = _validate_directory(root, directory, expected_identity)
            actual_identity = _identity(status)
            if actual_identity != expected_identity:
                raise RuntimeError("created directory identity changed")
            directory.rmdir()
        except FileNotFoundError:
            continue
        except Exception as error:
            failures.append(
                f"remove created directory {directory}: {type(error).__name__}: {error}"
            )
    return failures


def apply_actions(
    vault: Path,
    actions: list[MigrationAction],
    title_map: dict[str, str],
    archive_root: str | None = None,
    archive_roots: list[str] | None = None,
) -> None:
    """Validate every move, then relocate notes and rewrite active note links."""
    validated = _validate_actions(vault, actions)
    root = vault.resolve()
    _validate_directory(root, root)
    source_identities = {
        source: _identity(_validate_regular_file(root, source))
        for _, source, _ in validated
    }
    source_parent_identities = {
        source.parent: _identity(_validate_directory(root, source.parent))
        for _, source, _ in validated
    }
    attempts: list[_MoveAttempt] = []
    original_states: dict[Path, _FileState] = {}
    created_directories: list[tuple[Path, tuple[int, int] | None]] = []

    def remember_file(path: Path, expected_identity: tuple[int, int]) -> _FileState:
        if path not in original_states:
            original_states[path] = _capture_file_state(root, path, expected_identity)
        return original_states[path]

    try:
        for _, source, target in validated:
            if source == target:
                continue
            _create_parent_directories(root, target.parent, created_directories)
            source_identity = source_identities[source]
            source_parent_identity = source_parent_identities[source.parent]
            target_parent_identity = _identity(_validate_directory(root, target.parent))
            attempt = _MoveAttempt(
                source=source,
                target=target,
                identity=source_identity,
                source_parent_identity=source_parent_identity,
                target_parent_identity=target_parent_identity,
            )
            attempts.append(attempt)
            try:
                _rename_same_volume(
                    root,
                    source,
                    target,
                    source_identity,
                    source_parent_identity,
                    target_parent_identity,
                )
            except Exception:
                attempt.state = _reconcile_move(attempt)
                raise
            attempt.state = _reconcile_move(attempt)
            if attempt.state != "moved":
                raise RuntimeError("migration rename result is ambiguous")
        for action, _, target in validated:
            if action.action != "archive":
                if action.metadata:
                    target_identity = _path_identity_without_links(target)
                    if target_identity is None:
                        raise ValueError(f"migration target disappeared: {target}")
                    state = remember_file(target, target_identity)
                    normalized = _normalized_note_bytes(
                        state.value,
                        action.metadata,
                        action.source,
                    )
                    _write_file_bytes(root, target, state.identity, normalized)
        archives = [(root / CANONICAL_ARCHIVE_ROOT).resolve()]
        if archive_root:
            archives.append((root / archive_root).resolve())
        for configured_archive in archive_roots or []:
            resolved_archive = (root / configured_archive).resolve()
            if resolved_archive not in archives:
                archives.append(resolved_archive)
        for path in sorted(
            root.rglob("*.md"),
            key=lambda item: item.relative_to(root).as_posix(),
        ):
            rewrite_path = _resolve_rewrite_candidate(root, path)
            if rewrite_path is None:
                continue
            if any(_inside(archive, rewrite_path) for archive in archives):
                continue
            rewrite_identity = _path_identity_without_links(rewrite_path)
            if rewrite_identity is None:
                continue
            current_state = _capture_file_state(root, rewrite_path, rewrite_identity)
            note = parse_markdown(current_state.value.decode("utf-8"))
            rewritten_body = _rewrite_embedded_note_links(
                rewrite_wikilinks(note.body, title_map),
                title_map,
            )
            sources = note.metadata.get("sources")
            rewritten_sources = (
                [rewrite_wikilinks(str(value), title_map) for value in sources]
                if isinstance(sources, list)
                else sources
            )
            if rewritten_body != note.body or rewritten_sources != sources:
                state = remember_file(rewrite_path, rewrite_identity)
                if not note.metadata:
                    _write_file_bytes(
                        root,
                        rewrite_path,
                        state.identity,
                        rewritten_body.encode("utf-8"),
                    )
                    continue
                note.body = rewritten_body
                if isinstance(sources, list):
                    note.metadata["sources"] = rewritten_sources
                _write_file_bytes(
                    root,
                    rewrite_path,
                    state.identity,
                    render_markdown(note).encode("utf-8"),
                )
    except Exception as original_error:
        rollback_failures = _rollback_actions(
            root,
            attempts,
            original_states,
            created_directories,
        )
        if rollback_failures:
            details = "; ".join(rollback_failures)
            raise RuntimeError(
                f"migration failed ({type(original_error).__name__}: {original_error}); "
                f"rollback was incomplete ({details})"
            ) from original_error
        raise


def _plan_json(actions: list[MigrationAction]) -> str:
    return json.dumps([asdict(action) for action in actions], ensure_ascii=False, indent=2) + "\n"


def _plan_summary(actions: list[MigrationAction]) -> str:
    counts = {
        "promote_or_stage": sum(action.action == "move" for action in actions),
        "archive": sum(action.action == "archive" for action in actions),
        "delete": sum(action.action == "delete" for action in actions),
    }
    return (
        f"total={len(actions)}\n"
        f"promote_or_stage={counts['promote_or_stage']}\n"
        f"archive={counts['archive']}\n"
        f"delete={counts['delete']}\n"
        "duplicate_targets=0\n"
        "outside_vault_targets=0\n"
    )


def _reject_duplicate_fields(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object field: {key}")
        result[key] = value
    return result


def _reject_nonstandard_json_constant(value: str) -> object:
    raise ValueError(f"non-standard JSON constant: {value}")


def _load_plan(path: Path) -> list[MigrationAction]:
    try:
        document = json.loads(
            path.read_text(encoding="utf-8"),
            object_pairs_hook=_reject_duplicate_fields,
            parse_constant=_reject_nonstandard_json_constant,
        )
    except (OSError, ValueError) as error:
        raise ValueError(f"invalid plan JSON: {error}") from error
    if not isinstance(document, list):
        raise ValueError("plan must contain a JSON list")
    actions = []
    for index, item in enumerate(document):
        if not isinstance(item, dict):
            raise ValueError(f"plan action {index} must be an object")
        fields = set(item)
        missing = sorted(ACTION_FIELDS - fields)
        unknown = sorted(fields - ACTION_FIELDS)
        field_errors = []
        if missing:
            field_errors.append(f"missing fields: {', '.join(missing)}")
        if unknown:
            field_errors.append(f"unknown fields: {', '.join(unknown)}")
        if field_errors:
            raise ValueError(f"plan action {index} has {'; '.join(field_errors)}")
        source = item["source"]
        target = item["target"]
        action = item["action"]
        metadata = item["metadata"]
        if not isinstance(source, str) or not source.strip():
            raise ValueError(f"plan action {index} source must be a non-empty string")
        if not isinstance(target, str) or not target.strip():
            raise ValueError(f"plan action {index} target must be a non-empty string")
        if not isinstance(action, str):
            raise ValueError(f"plan action {index} action must be a string")
        if action not in SUPPORTED_ACTIONS:
            raise ValueError(f"unsupported action type: {action}")
        if not isinstance(metadata, dict):
            raise ValueError(f"plan action {index} metadata must be an object")
        actions.append(MigrationAction(source, target, action, metadata))
    return actions


def _archive_roots_from_actions(vault: Path, actions: list[MigrationAction]) -> list[str]:
    root = vault.resolve()
    archive_roots = set()
    for action in actions:
        if action.action != "archive":
            continue
        source = (root / action.source).resolve()
        target = (root / action.target).resolve()
        archive_root = _archive_root_for_action(root, source, target)
        archive_roots.add(archive_root.relative_to(root).as_posix())
    return sorted(archive_roots)


def _resolve_output(
    vault: Path,
    output: Path,
    validated: list[tuple[MigrationAction, Path, Path]],
) -> Path:
    root = vault.resolve()
    resolved = output.resolve() if output.is_absolute() else (root / output).resolve()
    if not _inside(root, resolved):
        raise ValueError("output is outside vault")
    audit_root = (root / AUDIT_OUTPUT_ROOT).resolve()
    if resolved == audit_root or not _inside(audit_root, resolved):
        raise ValueError("output must be under docs/superpowers/migrations")
    if resolved.suffix.lower() != ".json":
        raise ValueError("output must be a JSON file")
    if resolved.relative_to(root).as_posix() in PROTECTED_PATHS:
        raise ValueError("protected Obsidian file")
    for _, source, target in validated:
        if resolved == source or resolved == target:
            raise ValueError("output collides with an action source or target")
    if resolved.exists():
        raise ValueError("output already exists")
    return resolved


def _resolve_plan(vault: Path, plan: Path) -> Path:
    root = vault.resolve()
    candidate = plan if plan.is_absolute() else root / plan
    resolved = candidate.resolve()
    audit_root = (root / AUDIT_OUTPUT_ROOT).resolve()
    if resolved == audit_root or not _inside(audit_root, resolved):
        raise ValueError("plan must be under docs/superpowers/migrations")
    if resolved.suffix.lower() != ".json":
        raise ValueError("plan must be a JSON file")
    if not resolved.exists():
        raise ValueError("plan does not exist")
    if candidate.is_symlink() or not resolved.is_file():
        raise ValueError("plan is not a regular file")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan and safely apply a Second Brain migration.")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--vault", type=Path, required=True)
    plan.add_argument("--source", type=Path, required=True)
    plan.add_argument(
        "--policy",
        type=Path,
        default=Path(__file__).with_name("migration-policy.json"),
    )
    plan.add_argument("--output", type=Path)
    apply = commands.add_parser("apply")
    apply.add_argument("--vault", type=Path, required=True)
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--apply", action="store_true")
    rename = commands.add_parser("rename")
    rename.add_argument("--vault", type=Path, required=True)
    rename.add_argument("--source", required=True)
    rename.add_argument("--target", required=True)
    rename.add_argument("--alias", required=True)
    rename.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        if args.command == "plan":
            policy = MigrationPolicy.load(args.policy)
            actions = build_actions(_scan_source(args.vault, args.source), policy)
            validated = _validate_actions(args.vault, actions)
            rendered_plan = _plan_json(actions)
            if args.output is None:
                print(rendered_plan, end="")
            else:
                output = _resolve_output(args.vault, args.output, validated)
                output.parent.mkdir(parents=True, exist_ok=True)
                output.write_text(rendered_plan, encoding="utf-8")
                print(_plan_summary(actions), end="")
            return 0
        if args.command == "apply":
            if not args.apply:
                parser.error("apply requires --apply")
            plan_path = _resolve_plan(args.vault, args.plan)
            actions = _load_plan(plan_path)
            validated = _validate_actions(args.vault, actions)
            if any(source == plan_path for _, source, _ in validated):
                raise ValueError("plan cannot be an action source")
            title_map = {
                Path(action.source).stem: Path(action.target).stem
                for action in actions
            }
            apply_actions(
                args.vault,
                actions,
                title_map,
                archive_roots=_archive_roots_from_actions(args.vault, actions),
            )
            return 0
        if not args.apply:
            parser.error("rename requires --apply")
        action = MigrationAction(args.source, args.target, "move", {"aliases": [args.alias]})
        apply_actions(args.vault, [action], {Path(args.source).stem: Path(args.target).stem})
        return 0
    except (OSError, ValueError) as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
