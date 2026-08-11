from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path

from Tools.second_brain.note_io import extract_wikilinks, parse_markdown


@dataclass(frozen=True)
class NoteRecord:
    path: str
    title: str
    metadata: dict[str, object]
    wikilinks: list[str]


def scan_notes(source: Path) -> list[NoteRecord]:
    """Return Markdown notes under *source* in stable relative-path order."""
    paths = sorted(source.rglob("*.md"), key=lambda path: path.relative_to(source).as_posix())
    records = []
    for path in paths:
        note = parse_markdown(path.read_text(encoding="utf-8"))
        records.append(
            NoteRecord(
                path=path.relative_to(source).as_posix(),
                title=path.stem,
                metadata=note.metadata,
                wikilinks=extract_wikilinks(note.body),
            )
        )
    return records


def to_json(records: list[NoteRecord]) -> str:
    """Serialize an inventory reproducibly for use as a migration baseline."""
    return json.dumps([asdict(record) for record in records], ensure_ascii=False, indent=2) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a deterministic Markdown inventory.")
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(to_json(scan_notes(args.source)), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
