from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
import os
from pathlib import Path, PureWindowsPath
import re
import stat
import tempfile
from typing import BinaryIO

from Tools.second_brain.note_io import extract_wikilinks, parse_markdown
from Tools.second_brain.snapshot import hash_files, snapshot_tree


ARCHIVE_ROOT = "90 보관함"
TEMPLATE_ROOT = "99 템플릿"
ARCHIVE_GUIDE = "90 보관함/보관함 안내.md"
REQUIRED_FIELDS = ("id", "type", "status", "created", "updated")
VALID_TYPES = {"inbox", "daily", "source", "permanent", "project", "area", "structure", "reflection"}
VALID_STATUSES = {"seed", "growing", "evergreen", "archived"}
VALID_SOURCE_QUALITIES = {"discovery", "primary", "mixed", "personal"}
LEGACY_MARKERS = ("llm_wiki", "wiki-standardized", "wiki-expanded", "LLM Wiki 검색")
REPOSITORY_ROOTS = {".superpowers", "docs", "Tools", ".codex_recovery", ".obsidian", ".worktrees"}
TEMPLATE_FILES = (
    "데일리 노트 템플릿.md", "소스 노트 템플릿.md", "영구 노트 템플릿.md",
    "프로젝트 노트 템플릿.md", "회고 노트 템플릿.md",
)
REQUIRED_PROJECT_HUBS = {
    "SKN26 1차 차량 운영비 프로젝트", "SKN26 2차 신용카드 고객 이탈 분석",
    "SKN26 3차 PICKLE 맛집 추천 챗봇", "SKN26 4차 LG Home AI 가전 상담",
    "SKN26 Final HumouR AI HR 채용 보조",
}
REQUIRED_LECTURE_MAPS = {
    "Python 학습 지도", "MySQL 학습 지도", "데이터 수집 학습 지도", "데이터 분석 학습 지도",
    "머신러닝 학습 지도", "딥러닝 기초 학습 지도", "NLP 딥러닝 학습 지도", "LLM과 RAG 학습 지도",
    "멀티모달 딥러닝 학습 지도", "웹 클라이언트 학습 지도", "웹 서버 학습 지도", "DevOps 학습 지도",
}
JSON_REPORT_ROOT = Path("docs/superpowers/migrations")
WINDOWS_ILLEGAL_PATH_CHARACTERS = frozenset('<>:"|?*')
ID_RE = re.compile(r"^\d{14}-[a-z0-9]{4}$")
EMBED_RE = re.compile(r"!\[\[([^\]|#^]+)(?:[#^][^\]|]*)?(?:\|[^\]]+)?\]\]")


@dataclass(frozen=True)
class VerificationIssue:
    code: str
    path: str
    message: str


@dataclass
class _JsonReportTransaction:
    vault: Path
    value: str
    destination: Path
    temporary: Path
    handle: BinaryIO
    parent_identity: tuple[int, int]
    destination_identity: tuple[int, int] | None
    temporary_identity: tuple[int, int]
    committed: bool = False


def _issue(issues: list[VerificationIssue], code: str, path: str, message: str) -> None:
    issues.append(VerificationIssue(code, path, message))


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_archive(relative: str) -> bool:
    return relative == ARCHIVE_ROOT or relative.startswith(ARCHIVE_ROOT + "/")


def _is_template(relative: str) -> bool:
    return relative == TEMPLATE_ROOT or relative.startswith(TEMPLATE_ROOT + "/")


def _is_repository_root(relative: str) -> bool:
    return relative.split("/", 1)[0] in REPOSITORY_ROOTS


def _unsafe_markdown_reason(root: Path, path: Path, *, missing_ok: bool = False) -> str | None:
    try:
        relative_path = path.relative_to(root)
    except ValueError:
        return "lexical path escapes vault"
    candidate = root
    try:
        for part in relative_path.parts:
            candidate /= part
            if candidate.is_symlink():
                return "path contains a symbolic-link component"
        resolved = path.resolve(strict=True)
    except FileNotFoundError:
        return None if missing_ok else "path cannot be resolved safely"
    except (OSError, RuntimeError):
        return "path cannot be resolved safely"
    try:
        resolved.relative_to(root)
    except ValueError:
        return "resolved path escapes vault"
    if not resolved.is_file():
        return "resolved path is not a regular file"
    if resolved.suffix.lower() != ".md":
        return "resolved path is not Markdown"
    return None


def _selected(relative: str, only: str | None) -> bool:
    if not only:
        return True
    normalized = only.replace("\\", "/").strip("/")
    return relative == normalized or relative.startswith(normalized + "/") or Path(relative).name == normalized


def _link_key(value: str) -> str:
    return value.replace("\\", "/").strip().removesuffix(".md")


def _add_index(index: dict[str, set[str]], key: str, relative: str) -> None:
    index.setdefault(_link_key(key), set()).add(relative)


def _read_snapshot(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _unsafe_windows_path_component(component: str) -> bool:
    if not component or component.endswith((" ", ".")):
        return True
    if any(ord(character) < 32 or character in WINDOWS_ILLEGAL_PATH_CHARACTERS for character in component):
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
        raise ValueError("JSON report path cannot be inspected safely") from error
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0))


def _json_output_path(vault: Path, value: str) -> Path:
    relative = Path(value)
    if relative.is_absolute() or relative.anchor or relative.drive:
        raise ValueError("JSON report path must be vault-relative")
    if any(_unsafe_windows_path_component(part) for part in relative.parts):
        raise ValueError("JSON report path contains an unsafe Windows path component")
    if relative.suffix.lower() != ".json":
        raise ValueError("JSON report path must end in .json")
    if relative.parent != JSON_REPORT_ROOT:
        raise ValueError(f"JSON report path must be directly under {JSON_REPORT_ROOT.as_posix()}")
    candidate = vault.resolve()
    for part in relative.parts:
        candidate /= part
        if _is_link_or_reparse_point(candidate):
            raise ValueError("JSON report path must not contain symbolic links or reparse points")
    try:
        candidate.resolve(strict=False).relative_to(vault.resolve())
    except (OSError, RuntimeError, ValueError) as error:
        raise ValueError("JSON report path escapes the vault") from error
    if not candidate.parent.is_dir():
        raise ValueError("JSON report directory does not exist")
    if candidate.exists() and not candidate.is_file():
        raise ValueError("JSON report path is not a regular file")
    return candidate


def _same_open_file(handle: BinaryIO, path: Path) -> bool:
    try:
        return os.path.samefile(path, handle.fileno())
    except (FileNotFoundError, OSError, TypeError, ValueError):
        return False


def _path_identity(path: Path) -> tuple[int, int]:
    status = path.stat()
    return status.st_dev, status.st_ino


def _optional_path_identity(path: Path) -> tuple[int, int] | None:
    try:
        return _path_identity(path)
    except FileNotFoundError:
        return None


def _handle_identity(handle: BinaryIO) -> tuple[int, int]:
    status = os.fstat(handle.fileno())
    return status.st_dev, status.st_ino


def _validate_json_transaction(transaction: _JsonReportTransaction, *, require_open_handle: bool) -> None:
    destination = _json_output_path(transaction.vault, transaction.value)
    if destination != transaction.destination:
        raise ValueError("JSON report destination changed during verification")
    if _path_identity(destination.parent) != transaction.parent_identity:
        raise ValueError("JSON report directory changed during verification")
    if _optional_path_identity(destination) != transaction.destination_identity:
        raise ValueError("JSON report destination changed during verification")
    if transaction.temporary.parent != destination.parent:
        raise ValueError("JSON report temporary path left the approved directory")
    if _is_link_or_reparse_point(transaction.temporary):
        raise ValueError("JSON report temporary path became a link or reparse point")
    try:
        transaction.temporary.resolve(strict=True).relative_to(destination.parent.resolve(strict=True))
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as error:
        raise ValueError("JSON report temporary path cannot be resolved safely") from error
    if not transaction.temporary.is_file():
        raise ValueError("JSON report temporary path is not a regular file")
    if _path_identity(transaction.temporary) != transaction.temporary_identity:
        raise ValueError("JSON report temporary file changed during verification")
    if require_open_handle and not _same_open_file(transaction.handle, transaction.temporary):
        raise ValueError("JSON report temporary handle no longer matches its path")


def _safe_cleanup_json_temp(transaction: _JsonReportTransaction) -> None:
    if not transaction.handle.closed:
        transaction.handle.close()
    if transaction.committed:
        return
    _safe_unlink_json_temp(
        transaction.vault,
        transaction.value,
        transaction.destination,
        transaction.temporary,
        transaction.parent_identity,
        transaction.temporary_identity,
    )


def _safe_unlink_json_temp(
    vault: Path,
    value: str,
    destination: Path,
    temporary: Path,
    parent_identity: tuple[int, int],
    temporary_identity: tuple[int, int],
) -> None:
    try:
        revalidated = _json_output_path(vault, value)
        if revalidated != destination:
            return
        if _path_identity(destination.parent) != parent_identity:
            return
        if _is_link_or_reparse_point(temporary):
            return
        if _path_identity(temporary) != temporary_identity:
            return
        temporary.resolve(strict=True).relative_to(destination.parent.resolve(strict=True))
        temporary.unlink()
    except (FileNotFoundError, OSError, RuntimeError, ValueError):
        return


def _open_json_temp(vault: Path, value: str) -> _JsonReportTransaction:
    destination = _json_output_path(vault, value)
    parent_identity = _path_identity(destination.parent)
    destination_identity = _optional_path_identity(destination)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=".second-brain-report-",
        suffix=".tmp",
        dir=destination.parent,
    )
    temporary = Path(temporary_name)
    status = os.fstat(descriptor)
    temporary_identity = (status.st_dev, status.st_ino)
    try:
        handle = os.fdopen(descriptor, "r+b")
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        _safe_unlink_json_temp(
            vault,
            value,
            destination,
            temporary,
            parent_identity,
            temporary_identity,
        )
        raise
    transaction = _JsonReportTransaction(
        vault=vault,
        value=value,
        destination=destination,
        temporary=temporary,
        handle=handle,
        parent_identity=parent_identity,
        destination_identity=destination_identity,
        temporary_identity=temporary_identity,
    )
    try:
        _validate_json_transaction(transaction, require_open_handle=True)
    except BaseException:
        _safe_cleanup_json_temp(transaction)
        raise
    return transaction


def _write_json_temp(handle: BinaryIO, payload: str) -> None:
    remaining = memoryview((payload + "\n").encode("utf-8"))
    while remaining:
        written = handle.write(remaining)
        if written is None or written <= 0:
            raise OSError("short write while creating JSON report")
        remaining = remaining[written:]
    handle.flush()
    os.fsync(handle.fileno())


def _commit_json_output(transaction: _JsonReportTransaction, payload: str) -> None:
    _write_json_temp(transaction.handle, payload)
    _validate_json_transaction(transaction, require_open_handle=True)
    transaction.handle.close()
    _validate_json_transaction(transaction, require_open_handle=False)
    os.replace(transaction.temporary, transaction.destination)
    transaction.committed = True


def _verify_snapshots(vault: Path, obsidian_snapshot: Path | None, source_snapshot: Path | None, issues: list[VerificationIssue]) -> None:
    if obsidian_snapshot:
        try:
            expected = _read_snapshot(obsidian_snapshot)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            expected = None
        if not isinstance(expected, dict) or not all(isinstance(v, str) for v in expected.values()):
            _issue(issues, "protected-settings-changed", str(obsidian_snapshot), "invalid protected settings snapshot")
        else:
            try:
                actual = hash_files([Path(path) for path in expected])
            except OSError:
                actual = {}
            if actual != expected:
                _issue(issues, "protected-settings-changed", str(obsidian_snapshot), "protected Obsidian settings differ from snapshot")
    if source_snapshot:
        try:
            expected = _read_snapshot(source_snapshot)
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            expected = None
        if not isinstance(expected, dict):
            _issue(issues, "source-tree-changed", str(source_snapshot), "invalid source tree snapshot")
        else:
            try:
                actual = {root: snapshot_tree(Path(root)) for root in expected}
            except OSError:
                actual = {}
            if actual != expected:
                _issue(issues, "source-tree-changed", str(source_snapshot), "external source tree differs from snapshot")


def _template_issues(vault: Path, issues: list[VerificationIssue]) -> None:
    template_root = vault / TEMPLATE_ROOT
    for filename in TEMPLATE_FILES:
        path = template_root / filename
        relative = _relative(vault, path)
        unsafe_reason = _unsafe_markdown_reason(vault, path, missing_ok=True)
        if unsafe_reason:
            unsafe_issue = VerificationIssue("unsafe-path", relative, unsafe_reason)
            if unsafe_issue not in issues:
                issues.append(unsafe_issue)
            continue
        if not path.is_file():
            _issue(issues, "missing-template", relative, "required template is missing")
            continue
        text = path.read_text(encoding="utf-8")
        needs_time = filename != TEMPLATE_FILES[0]
        if "{{date:" not in text or (needs_time and "{{time:" not in text):
            _issue(issues, "missing-template", relative, "template lacks approved Obsidian date/time variables")


def verify_vault(vault: Path, *, final: bool, allow_staged_drafts: bool = False, only: str | None = None, obsidian_snapshot: Path | None = None, source_snapshot: Path | None = None) -> list[VerificationIssue]:
    """Return deterministic, read-only integrity issues for a Second Brain vault."""
    root = vault.resolve()
    full_transition = allow_staged_drafts and only is None
    issues: list[VerificationIssue] = []
    notes: list[tuple[Path, str, object]] = []
    links: dict[str, set[str]] = {}
    attachments: dict[str, set[str]] = {}
    ids: dict[str, list[str]] = {}
    for path in sorted(root.rglob("*.md"), key=lambda item: _relative(root, item)):
        relative = _relative(root, path)
        if _is_archive(relative) or _is_repository_root(relative):
            continue
        selected = _selected(relative, only)
        unsafe_reason = _unsafe_markdown_reason(root, path)
        if unsafe_reason:
            if selected:
                _issue(issues, "unsafe-path", relative, unsafe_reason)
            continue
        try:
            note = parse_markdown(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as error:
            if selected: _issue(issues, "missing-frontmatter", relative, str(error))
            continue
        if not note.metadata:
            if selected: _issue(issues, "missing-frontmatter", relative, "note has no frontmatter")
            continue
        if _is_template(relative):
            continue
        notes.append((path, relative, note))
        note_aliases = note.metadata.get("aliases", [])
        if not isinstance(note_aliases, list):
            note_aliases = []
        _add_index(links, path.with_suffix("").relative_to(root).as_posix(), relative)
        _add_index(links, path.stem, relative)
        for name in note_aliases:
            _add_index(links, str(name), relative)
        identifier = str(note.metadata.get("id", ""))
        if identifier:
            ids.setdefault(identifier, []).append(relative)
        if not selected:
            continue
        if identifier and not ID_RE.fullmatch(identifier):
            _issue(issues, "invalid-id", relative, "id must be YYYYMMDDHHMMSS-xxxx")
        source_path = note.metadata.get("source_path")
        if source_path and not Path(str(source_path)).exists():
            _issue(issues, "stale-source-path", relative, f"source_path does not exist: {source_path}")
        if any(marker in note.body for marker in LEGACY_MARKERS):
            _issue(issues, "legacy-llm-marker", relative, "legacy LLM marker is allowed only in archive")
        note_type, status = str(note.metadata.get("type", "")), str(note.metadata.get("status", ""))
        quality = str(note.metadata.get("source_quality", ""))
        if note_type and note_type not in VALID_TYPES: _issue(issues, "invalid-type", relative, f"unsupported type: {note_type}")
        if status and status not in VALID_STATUSES: _issue(issues, "invalid-status", relative, f"unsupported status: {status}")
        if quality and quality not in VALID_SOURCE_QUALITIES: _issue(issues, "invalid-source-quality", relative, f"unsupported source_quality: {quality}")
        staged_draft = allow_staged_drafts and relative.startswith("00 인박스/승격 대기/")
        if staged_draft:
            continue
        for field in REQUIRED_FIELDS:
            if not str(note.metadata.get(field, "")).strip():
                _issue(issues, "missing-required-field", relative, f"missing required field: {field}")
        if note_type == "permanent":
            sources = note.metadata.get("sources")
            if not isinstance(sources, list) or not sources:
                _issue(issues, "missing-required-field", relative, "permanent note needs sources")
            if status not in {"growing", "evergreen"}: _issue(issues, "invalid-status", relative, "permanent note must be growing or evergreen")
            if quality == "discovery": _issue(issues, "discovery-only-permanent", relative, "permanent note cannot use discovery sources only")
            if status == "evergreen" and note.metadata.get("verified") is not True:
                _issue(issues, "unverified-evergreen", relative, "evergreen permanent note must be verified")
            if quality != "personal" and note.metadata.get("verified") is True and quality not in {"primary", "mixed"}:
                _issue(issues, "invalid-source-quality", relative, "verified factual permanent note needs primary or mixed quality")
            if quality == "personal" and not any(marker in note.body for marker in ("개인 해석", "프로젝트 경험")):
                _issue(issues, "missing-required-field", relative, "personal permanent note needs personal interpretation or project experience")
    for identifier, paths in sorted(ids.items()):
        if len(paths) > 1:
            for relative in paths: _issue(issues, "duplicate-id", relative, f"duplicate id: {identifier}")
    for path in sorted(root.rglob("*"), key=lambda item: _relative(root, item)):
        if path.is_file() and path.suffix.lower() != ".md":
            relative = _relative(root, path)
            attachments.setdefault(path.name, set()).add(relative)
    for _, relative, note in notes:
        if not _selected(relative, only):
            continue
        for link in extract_wikilinks(note.body):
            targets = links.get(_link_key(link), set())
            if len(targets) > 1:
                _issue(issues, "unresolved-link", relative, f"ambiguous internal link: {link}")
            elif not targets:
                guide = root / ARCHIVE_GUIDE
                if _link_key(link) in {_link_key(guide.stem), _link_key(_relative(root, guide))} and guide.exists():
                    continue
                archive_candidate = root / ARCHIVE_ROOT / f"{_link_key(link)}.md"
                if archive_candidate.exists():
                    _issue(issues, "unresolved-link", relative, f"active note links to archived note: {link}")
                else:
                    _issue(issues, "unresolved-link", relative, f"unresolved internal link: {link}")
        for embed in EMBED_RE.findall(note.body):
            key = _link_key(embed)
            targets = links.get(key, set())
            if len(targets) > 1:
                _issue(issues, "unresolved-link", relative, f"ambiguous embedded note: {embed}")
            elif targets:
                continue
            attachment = (root / key).resolve()
            try:
                attachment.relative_to(root)
                exists = attachment.is_file()
            except ValueError:
                exists = False
            if exists:
                continue
            matching_attachments = attachments.get(Path(key).name, set()) if "/" not in key else set()
            if len(matching_attachments) == 1:
                continue
            if len(matching_attachments) > 1:
                _issue(issues, "unresolved-link", relative, f"ambiguous attachment embed: {embed}")
            else:
                _issue(issues, "unresolved-link", relative, f"unresolved embed: {embed}")
        staged_draft = allow_staged_drafts and relative.startswith("00 인박스/승격 대기/")
        if str(note.metadata.get("type", "")) == "permanent" and not staged_draft:
            note_embeds = [embed for embed in EMBED_RE.findall(note.body) if len(links.get(_link_key(embed), set())) == 1]
            if not extract_wikilinks(note.body) and not note_embeds:
                _issue(issues, "missing-required-field", relative, "permanent note needs an internal link")
    if only is None:
        _template_issues(root, issues)
        if final and not allow_staged_drafts:
            active_stems = {path.stem for path, _, _ in notes}
            for name in sorted(REQUIRED_PROJECT_HUBS - active_stems): _issue(issues, "missing-project-hub", name, "required project hub is missing")
            for name in sorted(REQUIRED_LECTURE_MAPS - active_stems): _issue(issues, "missing-lecture-map", name, "required lecture map is missing")
        _verify_snapshots(root, obsidian_snapshot, source_snapshot, issues)
    if full_transition:
        issues = [issue for issue in issues if issue.code not in {"legacy-llm-marker", "unresolved-link"}]
    return sorted(issues, key=lambda issue: (issue.path, issue.code, issue.message))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Second Brain vault without modifying it.")
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--allow-staged-drafts", action="store_true")
    parser.add_argument("--only")
    parser.add_argument("--obsidian-snapshot", type=Path)
    parser.add_argument("--source-snapshot", type=Path)
    parser.add_argument("--json", nargs="?", const="-", metavar="VAULT_RELATIVE_PATH")
    args = parser.parse_args()
    json_transaction = None
    if args.json not in {None, "-"}:
        try:
            json_transaction = _open_json_temp(args.vault, args.json)
        except (OSError, ValueError) as error:
            parser.error(str(error))
    try:
        issues = verify_vault(args.vault, final=args.final, allow_staged_drafts=args.allow_staged_drafts, only=args.only, obsidian_snapshot=args.obsidian_snapshot, source_snapshot=args.source_snapshot)
        if args.json:
            payload = json.dumps([asdict(issue) for issue in issues], ensure_ascii=False, sort_keys=True)
            if json_transaction is None:
                print(payload)
            else:
                try:
                    _commit_json_output(json_transaction, payload)
                except (OSError, ValueError) as error:
                    parser.error(f"cannot write JSON report: {error}")
        else:
            for issue in issues: print(f"{issue.code}: {issue.path}: {issue.message}")
    finally:
        if json_transaction is not None:
            _safe_cleanup_json_temp(json_transaction)
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
