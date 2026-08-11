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


def _validate_actions(vault: Path, actions: list[MigrationAction]) -> list[tuple[MigrationAction, Path, Path]]:
    root = vault.resolve()
    validated = []
    targets: set[Path] = set()
    sources: set[Path] = set()
    for action in actions:
        source, target = (root / action.source).resolve(), (root / action.target).resolve()
        if not _inside(root, source) or not _inside(root, target):
            raise ValueError("source or target is outside vault")
        if source.relative_to(root).as_posix() in PROTECTED_PATHS or target.relative_to(root).as_posix() in PROTECTED_PATHS:
            raise ValueError("protected Obsidian file")
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
    archive = (root / archive_root).resolve() if archive_root else None
    for path in sorted(root.rglob("*.md"), key=lambda item: item.relative_to(root).as_posix()):
        if archive is not None and _inside(archive, path.resolve()):
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


def _resolve_output(vault: Path, output: Path) -> Path:
    root = vault.resolve()
    resolved = output.resolve() if output.is_absolute() else (root / output).resolve()
    if not _inside(root, resolved):
        raise ValueError("output is outside vault")
    if resolved.relative_to(root).as_posix() in PROTECTED_PATHS:
        raise ValueError("protected Obsidian file")
    return resolved


def main() -> int:
    parser = argparse.ArgumentParser(description="Plan and safely apply a Second Brain migration.")
    commands = parser.add_subparsers(dest="command", required=True)
    for command in ("plan", "apply"):
        subparser = commands.add_parser(command)
        subparser.add_argument("--vault", type=Path, required=True)
        subparser.add_argument("--policy", type=Path, default=Path(__file__).with_name("migration-policy.json"))
        subparser.add_argument("--output", type=Path)
        if command == "apply": subparser.add_argument("--apply", action="store_true")
    rename = commands.add_parser("rename")
    rename.add_argument("--vault", type=Path, required=True); rename.add_argument("--source", required=True); rename.add_argument("--target", required=True); rename.add_argument("--alias", required=True); rename.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if args.command in {"plan", "apply"}:
        policy = MigrationPolicy.load(args.policy)
        actions = build_actions(scan_notes(args.vault), policy)
        if args.command == "apply" and not args.apply:
            parser.error("apply requires --apply")
        _validate_actions(args.vault, actions)
        rendered_plan = _plan_json(actions)
        if args.output is None:
            print(rendered_plan, end="")
        else:
            output = _resolve_output(args.vault, args.output)
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered_plan, encoding="utf-8")
        if args.command == "apply":
            apply_actions(args.vault, actions, {Path(action.source).stem: Path(action.target).stem for action in actions}, policy.archive_root)
        return 0
    if not args.apply: parser.error("rename requires --apply")
    action = MigrationAction(args.source, args.target, "move", {"aliases": [args.alias]})
    apply_actions(args.vault, [action], {Path(args.source).stem: Path(args.target).stem})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
