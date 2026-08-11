from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import hashlib
import json
from pathlib import Path
import re
import shutil

from Tools.second_brain.inventory import NoteRecord, scan_notes
from Tools.second_brain.note_io import parse_markdown, render_markdown, rewrite_wikilinks
from Tools.second_brain.policy import MigrationPolicy


PROTECTED_PATHS = {".obsidian/core-plugins.json", ".obsidian/graph.json", ".obsidian/workspace.json"}
AUDIT_OUTPUT_ROOT = Path("docs/superpowers/migrations")
CANONICAL_ARCHIVE_ROOT = Path("90 보관함/이전 LLM Wiki")
SUPPORTED_ACTIONS = frozenset({"archive", "move"})
ACTION_FIELDS = frozenset({"action", "metadata", "source", "target"})
EMBED_WIKILINK_RE = re.compile(r"!\[\[([^\]|#^]+)([#^][^\]|]*)?(\|[^\]]+)?\]\]")


@dataclass(frozen=True)
class MigrationAction:
    source: str
    target: str
    action: str
    metadata: dict[str, object]


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


def _normalize_note(path: Path, metadata: dict[str, object], old_path: str) -> None:
    if not metadata:
        return
    note = parse_markdown(path.read_text(encoding="utf-8"))
    note.metadata.update(metadata)
    if not note.metadata.get("id"):
        note.metadata["id"] = make_id(old_path, str(note.metadata.get("created", "")))
    path.write_text(render_markdown(note), encoding="utf-8")


def _rewrite_embedded_note_links(body: str, title_map: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        title = match.group(1).strip()
        suffix = match.group(2) or ""
        alias = match.group(3) or ""
        return f"![[{title_map.get(title, title)}{suffix}{alias}]]"

    return EMBED_WIKILINK_RE.sub(replace, body)


def apply_actions(
    vault: Path,
    actions: list[MigrationAction],
    title_map: dict[str, str],
    archive_root: str | None = None,
    archive_roots: list[str] | None = None,
) -> None:
    """Validate every move, then relocate notes and rewrite active note links."""
    validated = _validate_actions(vault, actions)
    for _, source, target in validated:
        if source == target:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(source), str(target))
    for action, _, target in validated:
        if action.action != "archive":
            _normalize_note(target, action.metadata, action.source)
    root = vault.resolve()
    archives = [(root / CANONICAL_ARCHIVE_ROOT).resolve()]
    if archive_root:
        archives.append((root / archive_root).resolve())
    for configured_archive in archive_roots or []:
        resolved_archive = (root / configured_archive).resolve()
        if resolved_archive not in archives:
            archives.append(resolved_archive)
    for path in sorted(root.rglob("*.md"), key=lambda item: item.relative_to(root).as_posix()):
        if any(_inside(archive, path.resolve()) for archive in archives):
            continue
        note = parse_markdown(path.read_text(encoding="utf-8"))
        rewritten_body = _rewrite_embedded_note_links(rewrite_wikilinks(note.body, title_map), title_map)
        sources = note.metadata.get("sources")
        rewritten_sources = [rewrite_wikilinks(str(value), title_map) for value in sources] if isinstance(sources, list) else sources
        if rewritten_body != note.body or rewritten_sources != sources:
            if not note.metadata:
                path.write_text(rewritten_body, encoding="utf-8")
                continue
            note.body = rewritten_body
            if isinstance(sources, list):
                note.metadata["sources"] = rewritten_sources
            path.write_text(render_markdown(note), encoding="utf-8")


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
