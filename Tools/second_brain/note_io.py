from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any


FRONTMATTER_BOUNDARY = "---"
WIKILINK_RE = re.compile(r"(?<!!)\[\[([^\]|#^]+)([#^][^\]|]*)?(\|[^\]]+)?\]\]")


@dataclass(eq=True)
class NoteDocument:
    metadata: dict[str, Any]
    body: str


def _parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value == "[]":
        return []
    if value.startswith("[") or value.endswith("]"):
        raise ValueError("non-empty inline lists are unsupported")
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return value[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    return value


def parse_markdown(text: str) -> NoteDocument:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return NoteDocument({}, normalized.strip() + "\n")
    end = normalized.find("\n---\n", 4)
    if end < 0:
        raise ValueError("frontmatter closing boundary is missing")
    lines = normalized[4:end].splitlines()
    metadata: dict[str, Any] = {}
    current_list: str | None = None
    for line in lines:
        if line.startswith("  - "):
            if current_list is None:
                raise ValueError("list item has no key")
            metadata[current_list].append(_parse_scalar(line[4:]))
            continue
        if line.startswith("  "):
            raise ValueError("nested mappings are unsupported")
        key, separator, raw = line.partition(":")
        if not separator:
            raise ValueError(f"invalid frontmatter line: {line}")
        current_list = None
        if raw.strip() == "":
            metadata[key] = []
            current_list = key
        else:
            metadata[key] = _parse_scalar(raw)
    body = normalized[end + 5 :].lstrip("\n").rstrip() + "\n"
    return NoteDocument(metadata, body)


def _render_scalar(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    text = str(value)
    return "'" + text.replace("'", "''") + "'"


def render_markdown(note: NoteDocument) -> str:
    lines = [FRONTMATTER_BOUNDARY]
    for key, value in note.metadata.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                lines.extend(f"  - {_render_scalar(item)}" for item in value)
        else:
            lines.append(f"{key}: {_render_scalar(value)}")
    lines.extend([FRONTMATTER_BOUNDARY, "", note.body.rstrip(), ""])
    return "\n".join(lines)


def extract_wikilinks(body: str) -> list[str]:
    return [match.group(1).strip() for match in WIKILINK_RE.finditer(body)]


def rewrite_wikilinks(body: str, title_map: dict[str, str]) -> str:
    def replace(match: re.Match[str]) -> str:
        title = match.group(1).strip()
        suffix = match.group(2) or ""
        alias = match.group(3) or ""
        return f"[[{title_map.get(title, title)}{suffix}{alias}]]"

    return WIKILINK_RE.sub(replace, body)
