# Zettelkasten Second Brain Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Convert the existing LLM Wiki vault into a Korean-titled, source-backed Zettelkasten Second Brain while preserving user-owned Obsidian settings and read-only source repositories.

**Architecture:** Build small Python standard-library tools for frontmatter parsing, inventory, safe moves, link rewrites, source snapshots, and final validation. Use those tools to stage selected legacy notes, archive everything else without deletion, then curate source notes, permanent notes, project experience, personal areas, and navigation in independently reviewable commits.

**Tech Stack:** Obsidian Markdown and YAML frontmatter, Python 3 standard library, `unittest`, PowerShell, Git.

**First Migration Scope:** Classify all 312 legacy notes, curate 14 lecture source notes and 34 permanent notes, create 12개 강의 학습 지도 and 5개 프로젝트 허브, preserve 21 practical reference notes, and archive every unmatched legacy asset without deletion.

## Global Constraints

- The approved design is `docs/superpowers/specs/2026-08-11-zettelkasten-second-brain-design.md`.
- Work in `C:\MinHyeok\oh_my_second_brain`; treat `C:\MinHyeok\lecture` and `C:\MinHyeok\skn26_projects` as read-only.
- Preserve the user's unstaged changes to `.obsidian/core-plugins.json`, `.obsidian/graph.json`, and `.obsidian/workspace.json`; never stage or overwrite them.
- Keep raw notebooks, code, datasets, and project assets in their original source folders.
- Use readable Korean filenames; keep product and technology names such as `RAG`, `LangGraph`, `React`, and `HumouR` in their original form.
- Use note IDs matching `^[0-9]{14}-[a-z0-9]{4}$` and reject duplicates.
- Active note types are `inbox`, `daily`, `source`, `permanent`, `project`, `area`, `structure`, `reflection`, `template`; `archive` is allowed only under `90 보관함`.
- Note statuses are `seed`, `growing`, `evergreen`, and `archived`.
- Source qualities are `primary`, `secondary`, `discovery`, `personal`, and `mixed`.
- 나무위키(Namuwiki), community posts, and AI answers are discovery sources only; a factual permanent note requires an official or primary source.
- Personal reflection may use `source_quality: personal`, but it must not be presented as an independently verified fact.
- Do not permanently delete legacy files during the first migration.
- 초기 전환에서는 레거시 파일을 영구 삭제하지 않고 `90 보관함`으로 이동한다.
- Use only Python's standard library; do not add PyYAML, Dataview, Templater, or another required dependency.
- Use `apply_patch` for hand-authored file edits. The migration tool may perform only manifest-resolved moves inside the vault after its dry-run report passes review.
- Each commit must stage only the task's paths. Never use an unscoped `git add -A`.

---

## Planned File Structure

### Migration tooling

- `Tools/__init__.py`: marks the existing `Tools` directory as a Python package.
- `Tools/second_brain/__init__.py`: exports the package version.
- `Tools/second_brain/note_io.py`: parses and renders the supported frontmatter subset; extracts and rewrites wikilinks in bodies and list-valued metadata.
- `Tools/second_brain/inventory.py`: inventories Markdown notes and writes deterministic JSON.
- `Tools/second_brain/snapshot.py`: records source-folder metadata and protected Obsidian file hashes.
- `Tools/second_brain/policy.py`: loads and validates the migration policy.
- `Tools/second_brain/migration.py`: produces dry-run actions, applies safe moves, normalizes metadata, and rewrites links.
- `Tools/second_brain/verify.py`: validates active notes, IDs, metadata, source policy, required hubs, stale paths, and unresolved links.
- `Tools/second_brain/migration-policy.json`: status routes and explicit path overrides.
- `Tools/second_brain/tests/`: unit tests and temporary-vault fixtures for every tool.

### Audit records

- `docs/superpowers/migrations/2026-08-11-legacy-inventory.json`: pre-migration inventory of the 312 legacy notes.
- `docs/superpowers/migrations/2026-08-11-source-snapshot.json`: size and modification-time snapshot of the two read-only source roots.
- `docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json`: hashes of the three protected Obsidian settings.
- `docs/superpowers/migrations/2026-08-11-dry-run.json`: resolved promote/archive/move actions before applying them.
- `docs/superpowers/migrations/2026-08-11-final-report.json`: machine-readable final verification report.
- `docs/superpowers/migrations/2026-08-11-final-report.md`: concise human-readable verification summary outside the active vault.

### Active vault

- `Second Brain 홈.md`
- `00 인박스/가져오기 검토 목록.md`
- `00 인박스/질문 인박스.md`
- `10 데일리/`
- `20 소스 노트/강의/`
- `20 소스 노트/프로젝트/`
- `20 소스 노트/공식 문서와 문헌/`
- `30 영구 노트/`
- `40 프로젝트/공통/`
- `50 영역/개발 레퍼런스/`
- `50 영역/회고/`
- `60 구조 노트/`
- `70 첨부 파일/`
- `90 보관함/이전 LLM Wiki/`
- `90 보관함/보관함 안내.md`
- `99 템플릿/`
- `.obsidian/templates.json`
- `.obsidian/daily-notes.json`

---

### Task 1: Markdown note model and wikilink utilities

**Files:**

- Create: `Tools/__init__.py`
- Create: `Tools/second_brain/__init__.py`
- Create: `Tools/second_brain/note_io.py`
- Create: `Tools/second_brain/tests/__init__.py`
- Create: `Tools/second_brain/tests/test_note_io.py`
- Track: `docs/superpowers/plans/2026-08-11-zettelkasten-second-brain.md`

**Interfaces:**

- Produces: `NoteDocument(metadata: dict[str, object], body: str)`
- Produces: `parse_markdown(text: str) -> NoteDocument`
- Produces: `render_markdown(note: NoteDocument) -> str`
- Produces: `extract_wikilinks(body: str) -> list[str]`
- Produces: `rewrite_wikilinks(body: str, title_map: dict[str, str]) -> str`

- [ ] **Step 1: Write parsing and link-rewrite tests**

```python
# Tools/second_brain/tests/test_note_io.py
import unittest

from Tools.second_brain.note_io import (
    NoteDocument,
    extract_wikilinks,
    parse_markdown,
    render_markdown,
    rewrite_wikilinks,
)


SAMPLE = r'''---
type: "permanent"
status: "growing"
verified: true
tags:
  - rag
  - retrieval
sources:
  - "[[LangChain 공식 RAG 문서]]"
source_path: 'C:\MinHyeok\lecture'
aliases: []
---

# 검색 품질

본문 [[RAG#검색|검색 단계]]와 [[Embedding]]을 연결한다.
'''


class NoteIoTests(unittest.TestCase):
    def test_parse_supported_frontmatter(self):
        note = parse_markdown(SAMPLE)
        self.assertEqual(note.metadata["type"], "permanent")
        self.assertTrue(note.metadata["verified"])
        self.assertEqual(note.metadata["tags"], ["rag", "retrieval"])
        self.assertEqual(note.metadata["sources"], ["[[LangChain 공식 RAG 문서]]"])
        self.assertEqual(note.metadata["source_path"], r"C:\MinHyeok\lecture")
        self.assertTrue(note.body.startswith("# 검색 품질"))

    def test_render_round_trip(self):
        parsed = parse_markdown(SAMPLE)
        reparsed = parse_markdown(render_markdown(parsed))
        self.assertEqual(reparsed, parsed)

    def test_extract_link_targets_without_heading_or_alias(self):
        body = "[[RAG#검색|검색 단계]] [[Embedding]] ![[diagram.png]]"
        self.assertEqual(extract_wikilinks(body), ["RAG", "Embedding"])

    def test_rewrite_preserves_heading_and_alias(self):
        body = "[[RAG#검색|검색 단계]]와 [[Embedding]]"
        rewritten = rewrite_wikilinks(
            body,
            {
                "RAG": "RAG의 성능은 검색 단계의 품질에서 시작된다",
                "Embedding": "임베딩은 의미 기반 비교를 위한 좌표 표현이다",
            },
        )
        self.assertEqual(
            rewritten,
            "[[RAG의 성능은 검색 단계의 품질에서 시작된다#검색|검색 단계]]와 "
            "[[임베딩은 의미 기반 비교를 위한 좌표 표현이다]]",
        )

    def test_reject_nested_yaml_mapping(self):
        with self.assertRaisesRegex(ValueError, "nested mappings are unsupported"):
            parse_markdown("---\nsource:\n  title: nested\n---\nbody")

    def test_reject_non_empty_inline_list(self):
        with self.assertRaisesRegex(ValueError, "non-empty inline lists are unsupported"):
            parse_markdown("---\ntags: [rag, retrieval]\n---\nbody")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused tests and confirm they fail**

Run:

```powershell
python -m unittest Tools.second_brain.tests.test_note_io -v
```

Expected: import failure because `Tools.second_brain.note_io` does not exist.

- [ ] **Step 3: Implement the supported YAML subset and wikilink functions**

Implement only flat scalars, block scalar lists, and the empty inline list `[]`. Reject non-empty inline lists and nested mappings so the migration never silently corrupts unsupported frontmatter.

```python
# Tools/second_brain/note_io.py
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
        return value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
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
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run:

```powershell
python -m unittest Tools.second_brain.tests.test_note_io -v
```

Expected: six passing tests.

- [ ] **Step 5: Commit the parser**

```powershell
git add -- Tools/__init__.py Tools/second_brain/__init__.py Tools/second_brain/note_io.py Tools/second_brain/tests/__init__.py Tools/second_brain/tests/test_note_io.py docs/superpowers/plans/2026-08-11-zettelkasten-second-brain.md
git commit -m "feat(tools): add Second Brain note parser"
```

---

### Task 2: Deterministic inventory and protected-source snapshots

**Files:**

- Create: `Tools/second_brain/inventory.py`
- Create: `Tools/second_brain/snapshot.py`
- Create: `Tools/second_brain/tests/test_inventory.py`
- Create: `Tools/second_brain/tests/test_snapshot.py`
- Create at execution time: `docs/superpowers/migrations/2026-08-11-legacy-inventory.json`
- Create at execution time: `docs/superpowers/migrations/2026-08-11-source-snapshot.json`
- Create at execution time: `docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json`

**Interfaces:**

- Consumes: `parse_markdown()` and `extract_wikilinks()` from Task 1.
- Produces: `NoteRecord(path: str, title: str, metadata: dict, wikilinks: list[str])`
- Produces: `scan_notes(source: Path) -> list[NoteRecord]`
- Produces: `to_json(records: list[NoteRecord]) -> str`
- Produces: `snapshot_tree(root: Path) -> list[dict[str, object]]`
- Produces: `hash_files(paths: list[Path]) -> dict[str, str]`
- Produces snapshot CLI modes `--tree`, `--hash`, `--verify-tree`, and `--verify-hashes`.

- [ ] **Step 1: Write inventory and snapshot tests using temporary directories**

```python
# Core assertions for Tools/second_brain/tests/test_inventory.py
records = scan_notes(fixture_root)
self.assertEqual([record.path for record in records], ["A.md", "nested/B.md"])
self.assertEqual(records[0].metadata["status"], "growing")
self.assertEqual(records[1].wikilinks, ["A"])
self.assertEqual(json.loads(to_json(records))[0]["path"], "A.md")
```

```python
# Core assertions for Tools/second_brain/tests/test_snapshot.py
before = snapshot_tree(source_root)
(source_root / "note.txt").write_text("changed", encoding="utf-8")
after = snapshot_tree(source_root)
self.assertNotEqual(before, after)
self.assertEqual(hash_files([settings_file])[str(settings_file)], hashlib.sha256(b"{}\n").hexdigest())
```

- [ ] **Step 2: Run the new tests and confirm they fail**

```powershell
python -m unittest Tools.second_brain.tests.test_inventory Tools.second_brain.tests.test_snapshot -v
```

Expected: imports fail because both modules are missing.

- [ ] **Step 3: Implement deterministic scans**

Use `Path.rglob()` with sorted relative POSIX paths. Exclude `.git`, `node_modules`, `.venv`, `venv`, `__pycache__`, `.next`, `dist`, and `build` from source snapshots. Record only relative path, byte size, and `st_mtime_ns`; do not hash large lecture/project binaries.

```python
@dataclass(frozen=True)
class NoteRecord:
    path: str
    title: str
    metadata: dict[str, object]
    wikilinks: list[str]


def scan_notes(source: Path) -> list[NoteRecord]:
    records = []
    for path in sorted(source.rglob("*.md")):
        note = parse_markdown(path.read_text(encoding="utf-8"))
        records.append(
            NoteRecord(
                path.as_posix().removeprefix(source.as_posix() + "/"),
                path.stem,
                note.metadata,
                extract_wikilinks(note.body),
            )
        )
    return records
```

- [ ] **Step 4: Run the tests and confirm they pass**

```powershell
python -m unittest Tools.second_brain.tests.test_inventory Tools.second_brain.tests.test_snapshot -v
```

Expected: all inventory and snapshot tests pass.

- [ ] **Step 5: Generate the three baselines before any vault move**

```powershell
python -m Tools.second_brain.inventory --source Knowledge --output docs/superpowers/migrations/2026-08-11-legacy-inventory.json
python -m Tools.second_brain.snapshot --tree 'C:\MinHyeok\lecture' --tree 'C:\MinHyeok\skn26_projects' --output docs/superpowers/migrations/2026-08-11-source-snapshot.json
python -m Tools.second_brain.snapshot --hash '.obsidian\core-plugins.json' --hash '.obsidian\graph.json' --hash '.obsidian\workspace.json' --output docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json
```

Expected:

- legacy inventory reports exactly 312 Markdown files;
- source snapshot contains 891 lecture files and 996 project files after the documented exclusions, with both requested roots and no excluded cache/build paths;
- Obsidian snapshot contains exactly the three protected files.

- [ ] **Step 6: Commit tooling and audit baselines**

```powershell
git add -- Tools/second_brain/inventory.py Tools/second_brain/snapshot.py Tools/second_brain/tests/test_inventory.py Tools/second_brain/tests/test_snapshot.py docs/superpowers/migrations/2026-08-11-legacy-inventory.json docs/superpowers/migrations/2026-08-11-source-snapshot.json docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json
git commit -m "chore(vault): record Second Brain migration baselines"
```

---

### Task 3: Migration policy and safe move engine

**Files:**

- Create: `Tools/second_brain/policy.py`
- Create: `Tools/second_brain/migration.py`
- Create: `Tools/second_brain/migration-policy.json`
- Create: `Tools/second_brain/tests/test_policy.py`
- Create: `Tools/second_brain/tests/test_migration.py`

**Interfaces:**

- Consumes: `NoteRecord`, `parse_markdown()`, `render_markdown()`, and `rewrite_wikilinks()`.
- Produces: `MigrationPolicy.load(path: Path) -> MigrationPolicy`
- Produces: `Route(action: str, target: str, metadata: dict[str, object])`
- Produces: `MigrationPolicy.route(path: str, status: str) -> Route`
- Produces: `MigrationAction(source: str, target: str, action: str, metadata: dict[str, object])`
- Produces: `build_actions(records, policy) -> list[MigrationAction]`
- Produces: `apply_actions(vault: Path, actions: list[MigrationAction], title_map: dict[str, str]) -> None`
- Produces CLI commands `plan`, `apply`, and `rename`.
- The `rename` CLI accepts exact `--vault`, `--source`, `--target`, `--alias`, and `--apply` arguments; for example:

```powershell
python -m Tools.second_brain.migration rename --vault . --source '00 인박스/승격 대기/영구 노트/RAG.md' --target '30 영구 노트/RAG의 성능은 검색 단계의 품질에서 시작된다.md' --alias 'RAG' --apply
```

- [ ] **Step 1: Write policy precedence and safe-move tests**

Test these exact behaviors:

```python
self.assertEqual(policy.route("Knowledge/Literature Notes/[Lecture] LLM과 RAG.md", "source-expanded").target, "20 소스 노트/강의/LLM과 RAG 강의.md")
self.assertEqual(policy.route("Knowledge/Permanent Notes/RAG.md", "wiki-expanded").target, "00 인박스/승격 대기/영구 노트/RAG.md")
self.assertEqual(policy.route("Knowledge/Reference Notes/Python 치트시트.md", "reference").target, "50 영역/개발 레퍼런스/Python 치트시트.md")
self.assertEqual(policy.route("Knowledge/Permanent Notes/얕은 노트.md", "wiki-standardized").action, "archive")
self.assertEqual(policy.route("Knowledge/Thinking/개인 Dev Rules.md", "personal-context").target, "50 영역/개발 원칙/개인 Dev Rules.md")
```

The migration test must also prove that dry-run performs no writes, apply refuses a target outside the vault, no source is deleted, and `rename` updates `[[Old#Heading|Alias]]` across active notes.

- [ ] **Step 2: Run the tests and confirm they fail**

```powershell
python -m unittest Tools.second_brain.tests.test_policy Tools.second_brain.tests.test_migration -v
```

Expected: missing-module failures.

- [ ] **Step 3: Add the policy document**

Use this routing precedence: explicit `path_routes`, then `status_routes`, then archive fallback.

```json
{
  "archive_root": "90 보관함/이전 LLM Wiki",
  "staging_root": "00 인박스/승격 대기",
  "status_routes": {
    "source-expanded": {"target": "20 소스 노트/강의", "type": "source", "status": "growing", "source_quality": "primary", "verified": true, "strip_prefix": "[Lecture] ", "append_suffix": " 강의"},
    "reference": {"target": "50 영역/개발 레퍼런스", "type": "source", "status": "growing", "source_quality": "mixed", "verified": false},
    "wiki-expanded": {"target": "00 인박스/승격 대기/영구 노트", "type": "inbox", "status": "seed", "source_quality": "mixed", "verified": false},
    "project-expanded": {"target": "40 프로젝트", "type": "project", "status": "growing", "source_quality": "mixed", "verified": true}
  },
  "path_routes": {
    "Knowledge/Thinking/개인 Dev Rules.md": {"target": "50 영역/개발 원칙/개인 Dev Rules.md", "type": "area", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Thinking/생각과 회고 MOC.md": {"target": "60 구조 노트/생각과 회고 지도.md", "type": "structure", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Thinking/프로젝트 기반 개발자 정체성.md": {"target": "50 영역/커리어/프로젝트 기반 개발자 정체성.md", "type": "reflection", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Thinking/프로젝트 회고 질문 세트.md": {"target": "50 영역/회고/프로젝트 회고 질문 세트.md", "type": "area", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Projects/프로젝트 경험 MOC.md": {"target": "40 프로젝트/프로젝트 경험 지도.md", "type": "structure", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Projects/프로젝트 적용 로그.md": {"target": "40 프로젝트/공통/프로젝트 적용 로그.md", "type": "project", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Projects/프로젝트 의사결정 로그.md": {"target": "40 프로젝트/공통/프로젝트 의사결정 로그.md", "type": "project", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Projects/프로젝트 실패와 디버깅 로그.md": {"target": "40 프로젝트/공통/프로젝트 실패와 디버깅 로그.md", "type": "project", "status": "growing", "source_quality": "personal", "verified": false},
    "Knowledge/Questions/질문 인박스.md": {"target": "00 인박스/질문 인박스.md", "type": "inbox", "status": "seed", "source_quality": "personal", "verified": false},
    "Knowledge/Questions/RAG 검색 실패 사례.md": {"target": "00 인박스/RAG 검색 실패 사례.md", "type": "inbox", "status": "seed", "source_quality": "mixed", "verified": false},
    "Knowledge/Questions/RAG 평가 질문 세트.md": {"target": "00 인박스/RAG 평가 질문 세트.md", "type": "inbox", "status": "seed", "source_quality": "mixed", "verified": false},
    "Knowledge/Projects/SKN26 1차 프로젝트 - 차량 TCO.md": {"target": "40 프로젝트/SKN26 1차 차량 운영비 프로젝트.md", "type": "project", "status": "growing", "source_quality": "mixed", "verified": true},
    "Knowledge/Projects/SKN26 2차 프로젝트 - 카드 이탈 예측.md": {"target": "40 프로젝트/SKN26 2차 신용카드 고객 이탈 분석.md", "type": "project", "status": "growing", "source_quality": "mixed", "verified": true},
    "Knowledge/Projects/SKN26 3차 프로젝트 - PICKLE RAG 챗봇.md": {"target": "40 프로젝트/SKN26 3차 PICKLE 맛집 추천 챗봇.md", "type": "project", "status": "growing", "source_quality": "mixed", "verified": true},
    "Knowledge/Projects/SKN26 4차 프로젝트 - LG Home.md": {"target": "40 프로젝트/SKN26 4차 LG Home AI 가전 상담.md", "type": "project", "status": "growing", "source_quality": "mixed", "verified": true}
  },
  "archive_fallback": true
}
```

The four explicit project entries above override the generic `project-expanded` route and land at these targets:

- `40 프로젝트/SKN26 1차 차량 운영비 프로젝트.md`
- `40 프로젝트/SKN26 2차 신용카드 고객 이탈 분석.md`
- `40 프로젝트/SKN26 3차 PICKLE 맛집 추천 챗봇.md`
- `40 프로젝트/SKN26 4차 LG Home AI 가전 상담.md`

- [ ] **Step 4: Implement dry-run-first migration**

The engine must:

1. resolve both source and target with `Path.resolve()`;
2. assert they remain under the resolved vault root;
3. reject duplicate targets before writing;
4. write a deterministic JSON plan by default;
5. require `--apply` for moves;
6. move, never delete, source files;
7. preserve archived relative paths under `90 보관함/이전 LLM Wiki`;
8. normalize metadata only for promoted notes;
9. add missing stable IDs with timestamp plus the first four hexadecimal characters of SHA-256 over the old relative path;
10. rewrite wikilinks in note bodies and `sources` metadata lists only after every move succeeds.

```python
def make_id(old_relative_path: str, created: str) -> str:
    day = created.replace("-", "") if re.fullmatch(r"\d{4}-\d{2}-\d{2}", created) else "20260811"
    suffix = hashlib.sha256(old_relative_path.encode("utf-8")).hexdigest()[:4]
    return f"{day}000000-{suffix}"
```

- [ ] **Step 5: Run the migration tests and confirm they pass**

```powershell
python -m unittest Tools.second_brain.tests.test_policy Tools.second_brain.tests.test_migration -v
```

Expected: all policy, safety, move, archive, ID, and link tests pass.

- [ ] **Step 6: Commit the migration engine**

```powershell
git add -- Tools/second_brain/policy.py Tools/second_brain/migration.py Tools/second_brain/migration-policy.json Tools/second_brain/tests/test_policy.py Tools/second_brain/tests/test_migration.py
git commit -m "feat(tools): add safe Second Brain migration engine"
```

---

### Task 4: Vault verifier

**Files:**

- Create: `Tools/second_brain/verify.py`
- Create: `Tools/second_brain/tests/test_verify.py`

**Interfaces:**

- Consumes: Task 1 note parser and Task 2 snapshots.
- Produces: `VerificationIssue(code: str, path: str, message: str)`
- Produces: `verify_vault(vault: Path, *, final: bool, allow_staged_drafts: bool = False, only: str | None = None, obsidian_snapshot: Path | None = None, source_snapshot: Path | None = None) -> list[VerificationIssue]`
- Produces CLI flags `--allow-staged-drafts`, `--only`, `--obsidian-snapshot`, `--source-snapshot`, and `--json`.
- Produces CLI exit code `0` on success and `1` when any error exists.

- [ ] **Step 1: Write failing validation tests**

Create temporary active and archive folders and assert these exact error codes:

- `missing-frontmatter`
- `missing-required-field`
- `invalid-id`
- `duplicate-id`
- `invalid-type`
- `invalid-status`
- `invalid-source-quality`
- `discovery-only-permanent`
- `unverified-evergreen`
- `unresolved-link`
- `legacy-llm-marker`
- `stale-source-path`
- `missing-project-hub`
- `missing-lecture-map`
- `protected-settings-changed`
- `source-tree-changed`

Also assert that these markers are allowed under `90 보관함` and forbidden elsewhere: `llm_wiki`, `wiki-standardized`, `wiki-expanded`, `LLM Wiki 검색`.

- [ ] **Step 2: Run the verifier test and confirm it fails**

```powershell
python -m unittest Tools.second_brain.tests.test_verify -v
```

Expected: import failure for `Tools.second_brain.verify`.

- [ ] **Step 3: Implement active-vault and baseline checks**

Required active fields are `id`, `type`, `status`, `created`, and `updated`. A `permanent` note must have at least one `sources` entry, one internal wikilink, `status` in `growing|evergreen`, and `source_quality` not equal to `discovery`. A factual permanent note with `verified: true` must use `primary` or `mixed`; a personal permanent note must state `개인 해석` or `프로젝트 경험` in its body.

Resolve internal links against active filenames and their `aliases`. Report an active-to-archive link unless it targets `90 보관함/보관함 안내.md`; archived legacy notes may retain unresolved or old links without failing final verification.

Treat `99 템플릿` as template definitions: validate that all five files exist and contain the approved Obsidian date/time variables, but do not apply concrete ID, date, source, or permanent-note promotion rules to the template files themselves.

Required project hubs:

```python
REQUIRED_PROJECT_HUBS = {
    "SKN26 1차 차량 운영비 프로젝트",
    "SKN26 2차 신용카드 고객 이탈 분석",
    "SKN26 3차 PICKLE 맛집 추천 챗봇",
    "SKN26 4차 LG Home AI 가전 상담",
    "SKN26 Final HumouR AI HR 채용 보조",
}
```

Required lecture maps:

```python
REQUIRED_LECTURE_MAPS = {
    "Python 학습 지도",
    "MySQL 학습 지도",
    "데이터 수집 학습 지도",
    "데이터 분석 학습 지도",
    "머신러닝 학습 지도",
    "딥러닝 기초 학습 지도",
    "NLP 딥러닝 학습 지도",
    "LLM과 RAG 학습 지도",
    "멀티모달 딥러닝 학습 지도",
    "웹 클라이언트 학습 지도",
    "웹 서버 학습 지도",
    "DevOps 학습 지도",
}
```

- [ ] **Step 4: Run the complete tool test suite**

```powershell
python -m unittest discover -s Tools/second_brain/tests -v
```

Expected: all tests pass.

- [ ] **Step 5: Commit the verifier**

```powershell
git add -- Tools/second_brain/verify.py Tools/second_brain/tests/test_verify.py
git commit -m "test(vault): add Second Brain integrity checks"
```

---

### Task 5: Second Brain skeleton, templates, and Obsidian routing

**Files:**

- Create: `Second Brain 홈.md`
- Create: `00 인박스/가져오기 검토 목록.md`
- Create: `10 데일리/.gitkeep`
- Create: `20 소스 노트/강의/.gitkeep`
- Create: `20 소스 노트/프로젝트/.gitkeep`
- Create: `20 소스 노트/공식 문서와 문헌/.gitkeep`
- Create: `30 영구 노트/.gitkeep`
- Create: `40 프로젝트/공통/.gitkeep`
- Create: `50 영역/개발 레퍼런스/.gitkeep`
- Create: `50 영역/회고/.gitkeep`
- Create: `60 구조 노트/.gitkeep`
- Create: `70 첨부 파일/.gitkeep`
- Create: `90 보관함/이전 LLM Wiki/.gitkeep`
- Create: `90 보관함/보관함 안내.md`
- Create: `99 템플릿/데일리 노트 템플릿.md`
- Create: `99 템플릿/소스 노트 템플릿.md`
- Create: `99 템플릿/영구 노트 템플릿.md`
- Create: `99 템플릿/프로젝트 노트 템플릿.md`
- Create: `99 템플릿/회고 노트 템플릿.md`
- Create: `.obsidian/templates.json`
- Create: `.obsidian/daily-notes.json`

**Interfaces:**

- Produces the final folder contract consumed by Tasks 6-14.
- Does not modify the three protected Obsidian files.

- [ ] **Step 1: Create the folder skeleton and home note**

Give `Second Brain 홈.md` complete frontmatter using `type: structure`, `status: growing`, and a stable ID. Its body must contain these sections and links:

```markdown
# Second Brain 홈

## 빠른 기록

- [[질문 인박스]]
- [[가져오기 검토 목록]]

## 프로젝트

- [[프로젝트 경험 지도]]

## 학습 지도

- [[Python 학습 지도]]
- [[MySQL 학습 지도]]
- [[데이터 수집 학습 지도]]
- [[데이터 분석 학습 지도]]
- [[머신러닝 학습 지도]]
- [[딥러닝 기초 학습 지도]]
- [[NLP 딥러닝 학습 지도]]
- [[LLM과 RAG 학습 지도]]
- [[멀티모달 딥러닝 학습 지도]]
- [[웹 클라이언트 학습 지도]]
- [[웹 서버 학습 지도]]
- [[DevOps 학습 지도]]

## 삶과 성장

- [[기술 학습]]
- [[커리어]]
- [[개인 목표]]
- [[개발 원칙]]
- [[생각과 회고 지도]]
```

Create `90 보관함/보관함 안내.md` with `type: archive`, `status: archived`, and a short explanation that the folder preserves pre-migration material and is not an active knowledge source.

- [ ] **Step 2: Create the five exact templates**

Use type-specific static four-character ID suffixes to keep core Obsidian Templates dependency-free:

- daily: `{{date:YYYYMMDD}}000000-day0`
- source: `{{date:YYYYMMDD}}{{time:HHmmss}}-src0`
- permanent: `{{date:YYYYMMDD}}{{time:HHmmss}}-perm`
- project: `{{date:YYYYMMDD}}{{time:HHmmss}}-proj`
- reflection: `{{date:YYYYMMDD}}{{time:HHmmss}}-refl`

Use these complete template bodies; do not restore the old definition/checklist boilerplate.

`99 템플릿/데일리 노트 템플릿.md`:

```markdown
---
id: '{{date:YYYYMMDD}}000000-day0'
type: 'daily'
status: 'seed'
created: '{{date:YYYY-MM-DD}}'
updated: '{{date:YYYY-MM-DD}}'
tags: []
aliases: []
sources: []
source_quality: 'personal'
verified: false
---

# {{date:YYYY-MM-DD}}

## 오늘의 맥락

## 기록

## 연결

## 다음 행동
```

`99 템플릿/소스 노트 템플릿.md`:

```markdown
---
id: '{{date:YYYYMMDD}}{{time:HHmmss}}-src0'
type: 'source'
status: 'seed'
created: '{{date:YYYY-MM-DD}}'
updated: '{{date:YYYY-MM-DD}}'
tags: []
aliases: []
sources: []
source_quality: 'discovery'
verified: false
---

# {{title}}

## 출처

- 제목:
- 위치:
- 확인일: {{date:YYYY-MM-DD}}

## 핵심 내용

## 내 해석과 의문

## 분리할 영구 노트
```

`99 템플릿/영구 노트 템플릿.md`:

```markdown
---
id: '{{date:YYYYMMDD}}{{time:HHmmss}}-perm'
type: 'permanent'
status: 'seed'
created: '{{date:YYYY-MM-DD}}'
updated: '{{date:YYYY-MM-DD}}'
tags: []
aliases: []
sources: []
source_quality: 'discovery'
verified: false
---

# {{title}}

## 주장

## 근거

## 연결

## 한계와 반례

## 다음 질문
```

`99 템플릿/프로젝트 노트 템플릿.md`:

```markdown
---
id: '{{date:YYYYMMDD}}{{time:HHmmss}}-proj'
type: 'project'
status: 'seed'
created: '{{date:YYYY-MM-DD}}'
updated: '{{date:YYYY-MM-DD}}'
tags: []
aliases: []
sources: []
source_quality: 'mixed'
verified: false
---

# {{title}}

## 프로젝트 개요

## 팀 산출물

## 직접 기여

## 기술적 의사결정

## 실패와 해결 과정

## 개인 회고와 성장

## 관련 영구 노트

## 출처
```

`99 템플릿/회고 노트 템플릿.md`:

```markdown
---
id: '{{date:YYYYMMDD}}{{time:HHmmss}}-refl'
type: 'reflection'
status: 'seed'
created: '{{date:YYYY-MM-DD}}'
updated: '{{date:YYYY-MM-DD}}'
tags: []
aliases: []
sources: []
source_quality: 'personal'
verified: false
---

# {{title}}

## 무슨 일이 있었는가

## 무엇을 배웠는가

## 생각이나 행동이 어떻게 바뀌었는가

## 연결할 노트

## 다음 행동
```

- [ ] **Step 3: Configure only new Obsidian settings files**

`.obsidian/templates.json`:

```json
{
  "folder": "99 템플릿",
  "dateFormat": "YYYY-MM-DD",
  "timeFormat": "HH:mm"
}
```

`.obsidian/daily-notes.json`:

```json
{
  "folder": "10 데일리",
  "format": "YYYY-MM-DD",
  "template": "99 템플릿/데일리 노트 템플릿"
}
```

- [ ] **Step 4: Verify protected settings are unchanged**

```powershell
python -m Tools.second_brain.snapshot --verify-hashes docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json
git diff -- .obsidian/core-plugins.json .obsidian/graph.json .obsidian/workspace.json
```

Expected: the hash check passes and the diff remains exactly the user's pre-migration diff.

- [ ] **Step 5: Commit the skeleton without staging protected settings**

```powershell
git add -- 'Second Brain 홈.md' '00 인박스' '10 데일리' '20 소스 노트' '30 영구 노트' '40 프로젝트' '50 영역' '60 구조 노트' '70 첨부 파일' '90 보관함' '99 템플릿' .obsidian/templates.json .obsidian/daily-notes.json
git commit -m "feat(vault): add Second Brain structure and templates"
```

---

### Task 6: Dry-run and apply the legacy-note staging migration

**Files:**

- Create: `docs/superpowers/migrations/2026-08-11-dry-run.json`
- Move: selected files from `Knowledge/` into active/staging destinations defined by the policy.
- Move: all unmatched `Knowledge/` content to `90 보관함/이전 LLM Wiki/Knowledge/`.

**Interfaces:**

- Consumes: policy and migration engine from Task 3.
- Produces exactly 84 promoted/staged actions and 228 archive actions from the 312-note baseline.
- Produces normalized metadata without promoting the 34 factual concept drafts prematurely.

- [ ] **Step 1: Generate a dry-run plan**

```powershell
python -m Tools.second_brain.migration plan --vault . --source Knowledge --policy Tools/second_brain/migration-policy.json --output docs/superpowers/migrations/2026-08-11-dry-run.json
```

Expected summary:

```text
total=312
promote_or_stage=84
archive=228
delete=0
duplicate_targets=0
outside_vault_targets=0
```

- [ ] **Step 2: Inspect every non-archive action before applying**

```powershell
Get-Content -Encoding utf8 -Raw docs/superpowers/migrations/2026-08-11-dry-run.json
```

Confirm the plan contains 14 lecture source notes, 34 permanent-note drafts under `00 인박스/승격 대기/영구 노트`, 21 reference notes, four existing project hubs, four personal notes, four cross-project notes, and three question notes.

- [ ] **Step 3: Apply only the reviewed plan**

```powershell
python -m Tools.second_brain.migration apply --vault . --plan docs/superpowers/migrations/2026-08-11-dry-run.json --apply
```

Expected: all 312 source paths are moved, no file is deleted, and no content outside the vault is touched.

- [ ] **Step 4: Run transition-mode verification**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --obsidian-snapshot docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json --source-snapshot docs/superpowers/migrations/2026-08-11-source-snapshot.json
```

Expected: no safety, path, ID, or broken-link errors. Missing final hubs/maps and staged permanent drafts are warnings only in this mode.

- [ ] **Step 5: Commit the mechanical move separately from content rewriting**

```powershell
git add -A -- Knowledge '00 인박스' '20 소스 노트' '40 프로젝트' '50 영역' '60 구조 노트' '90 보관함' docs/superpowers/migrations/2026-08-11-dry-run.json
git commit -m "refactor(vault): stage legacy notes for Second Brain migration"
```

---

### Task 7: Curate the 14 lecture source notes

**Files:**

- Modify: all files in `20 소스 노트/강의/`
- Read only: matching modules under `C:\MinHyeok\lecture`
- Read as needed: current official documentation for facts that may have changed.

**Interfaces:**

- Produces 14 `type: source`, `status: growing`, `source_quality: primary` notes.
- Produces source notes that Tasks 8-10 can cite from permanent notes.

- [ ] **Step 1: Confirm the exact 14 source-note filenames**

```text
DevOps와 배포 강의.md
Django 웹 서버 강의.md
Git 기초 강의.md
LLM과 RAG 강의.md
MySQL과 관계형 데이터베이스 강의.md
NLP 딥러닝 강의.md
Python 기초와 Streamlit 강의.md
React와 CI CD 강의.md
데이터 분석 강의.md
데이터 수집 강의.md
딥러닝 기초 강의.md
머신러닝 강의.md
멀티모달 딥러닝 강의.md
웹 클라이언트 강의.md
```

- [ ] **Step 2: Normalize each source note**

For each file, replace LLM Wiki fields and boilerplate with this structure, using the exact path mapping below:

```markdown
## 출처

- 원본 경로: `C:\MinHyeok\lecture`
- 확인일: 2026-08-11

## 핵심 내용

## 내 해석과 의문

## 분리한 영구 노트
```

Use these exact source roots instead of leaving the generic lecture root in the finished note:

```text
Python 기초와 Streamlit 강의 -> C:\MinHyeok\lecture\01_python_workspace
MySQL과 관계형 데이터베이스 강의 -> C:\MinHyeok\lecture\02_mysql_workspace
데이터 수집 강의 -> C:\MinHyeok\lecture\03_data_collection_workspace
데이터 분석 강의 -> C:\MinHyeok\lecture\04_data_analysis_workspace
머신러닝 강의 -> C:\MinHyeok\lecture\05_machine_learning_workspace
딥러닝 기초 강의 -> C:\MinHyeok\lecture\06_deep_learning_basic_workspace
NLP 딥러닝 강의 -> C:\MinHyeok\lecture\07_deep_learning_nlp_workspace
LLM과 RAG 강의 -> C:\MinHyeok\lecture\08_llm_workspace
멀티모달 딥러닝 강의 -> C:\MinHyeok\lecture\09_deep_learning_multimodal_workspace
웹 클라이언트 강의 -> C:\MinHyeok\lecture\10_web_client_workspace
Django 웹 서버 강의 -> C:\MinHyeok\lecture\11_web_server_workspace
DevOps와 배포 강의 -> C:\MinHyeok\lecture\12_devops_workspace
Git 기초 강의 -> C:\MinHyeok\lecture\12_devops_workspace
React와 CI CD 강의 -> C:\MinHyeok\lecture\10_web_client_workspace and C:\MinHyeok\lecture\12_devops_workspace
```

Keep statements that are traceable to the local lecture material. Move unsupported claims into `내 해석과 의문` or `00 인박스/가져오기 검토 목록.md`.

- [ ] **Step 3: Remove active LLM Wiki markers and stale paths**

```powershell
rg -n 'llm_wiki|wiki-expanded|source-expanded|C:\\lecture' '20 소스 노트\강의'
```

Expected: no matches.

- [ ] **Step 4: Run source-note verification**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '20 소스 노트/강의'
```

Expected: all 14 source notes pass metadata, ID, path, and active-marker checks.

- [ ] **Step 5: Commit the source-note layer**

```powershell
git add -- '20 소스 노트/강의' '00 인박스/가져오기 검토 목록.md'
git commit -m "docs(sources): curate lecture source notes"
```

---

### Task 8: Promote LLM and RAG permanent notes

**Files:**

- Move/modify: 12 files from `00 인박스/승격 대기/영구 노트/` to `30 영구 노트/`.
- Modify through link rewriting: active Markdown files that reference the old titles.

**Interfaces:**

- Consumes: lecture source notes from Task 7 and official OpenAI/LangChain/LangGraph documentation where current behavior matters.
- Produces: 12 verified, connected permanent notes with old titles in `aliases`.

- [ ] **Step 1: Apply these exact title mappings one note at a time**

```text
RAG -> RAG의 성능은 검색 단계의 품질에서 시작된다
Embedding -> 임베딩은 의미 기반 비교를 위한 좌표 표현이다
Retriever -> 검색기는 질문과 관련된 근거 후보를 좁힌다
Vector Store -> 벡터 저장소는 임베딩과 메타데이터를 함께 관리해야 한다
RAG 평가 -> RAG 평가는 검색과 생성을 분리해서 측정해야 한다
LLM -> LLM은 다음 토큰 확률로 문맥에 맞는 출력을 만든다
LangGraph -> LangGraph는 상태 전이를 명시해 LLM 흐름을 제어한다
LangGraph State -> LangGraph 상태는 노드 사이의 데이터 계약이다
LangGraph Conditional Edge -> 조건부 엣지는 상태에 따라 다음 실행 경로를 선택한다
Function Calling -> 함수 호출은 자연어 요청을 구조화된 도구 입력으로 바꾼다
Prompt Engineering -> 프롬프트는 모델에 전달하는 작업 계약이다
OpenAI API -> OpenAI API 호출은 입력 출력 오류 경계를 함께 설계해야 한다
```

For each note: read the staged content and linked source; rewrite it into one claim; record official/primary sources and access date; add at least two meaningful internal links; add a limitation or counterexample; set `type: permanent`, `status: growing`, `source_quality: primary|mixed`, and `verified: true`; then run the `migration rename` command so all incoming links update.

- [ ] **Step 2: Verify the domain group**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '30 영구 노트'
rg -n 'llm_wiki|wiki-standardized|한 줄 정의|먼저 확인할 질문' '30 영구 노트'
```

Expected: no verifier errors and no old boilerplate markers in the 12 promoted notes.

- [ ] **Step 3: Commit the LLM/RAG knowledge cluster**

```powershell
git add -A -- 'Second Brain 홈.md' '00 인박스' '20 소스 노트' '30 영구 노트' '40 프로젝트' '50 영역' '60 구조 노트'
git commit -m "docs(notes): promote LLM and RAG zettels"
```

---

### Task 9: Promote web application permanent notes

**Files:**

- Move/modify: 10 staged permanent-note drafts.
- Modify through link rewriting: active notes that reference the old titles.

**Interfaces:**

- Consumes: Django, React, FastAPI, Requests, and SQLite official documentation plus project evidence.
- Produces: 10 verified permanent notes.

- [ ] **Step 1: Apply these exact mappings and curation rules**

```text
Django ORM Model -> Django ORM 모델은 데이터 구조와 제약을 코드로 표현한다
Django QuerySet -> QuerySet은 평가 시점을 늦춰 쿼리 조합을 가능하게 한다
Django CSRF -> CSRF 방어는 브라우저 세션 요청의 출처를 검증한다
Django JSON API -> Django JSON API는 화면과 서버 책임을 분리한다
Django Chatbot -> Django 챗봇은 대화 상태와 요청 경계를 함께 관리해야 한다
FastAPI -> FastAPI는 타입 선언을 요청 검증과 문서화에 재사용한다
React SPA -> React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다
React API Fetch -> React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다
Requests -> HTTP 요청은 타임아웃과 실패 처리를 기본값으로 가져야 한다
SQLite -> SQLite는 단일 파일로 작은 애플리케이션의 영속성을 단순화한다
```

Use the same per-note promotion sequence as Task 8. Project examples belong under `근거` or `연결`; they do not replace the official technical source.

- [ ] **Step 2: Verify and inspect rewritten links**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '30 영구 노트'
rg -n '\[\[(Django ORM Model|Django QuerySet|Django CSRF|Django JSON API|Django Chatbot|FastAPI|React SPA|React API Fetch|Requests|SQLite)([#|\]])' --glob '*.md' --glob '!90 보관함/**'
```

Expected: verifier passes and no active incoming link uses an old title.

- [ ] **Step 3: Commit the web cluster**

```powershell
git add -A -- 'Second Brain 홈.md' '00 인박스' '20 소스 노트' '30 영구 노트' '40 프로젝트' '50 영역' '60 구조 노트'
git commit -m "docs(notes): promote web application zettels"
```

---

### Task 10: Promote data, ML, and operations permanent notes

**Files:**

- Move/modify: the remaining 12 staged permanent-note drafts.
- Modify through link rewriting: active notes that reference the old titles.

**Interfaces:**

- Consumes: official Docker, MLflow, MySQL, pandas, Streamlit, React, scikit-learn, and XGBoost documentation plus lecture source notes.
- Produces: 12 verified permanent notes and an empty `00 인박스/승격 대기/영구 노트/` directory.

- [ ] **Step 1: Apply these exact mappings and curation rules**

```text
Docker Compose -> Docker Compose는 여러 컨테이너의 실행 계약을 한곳에 모은다
Feature Engineering -> 특성 공학은 모델보다 먼저 데이터 표현을 개선한다
MLflow -> MLflow는 실험 조건과 결과를 함께 추적한다
MySQL Connector Python -> MySQL Connector는 SQL 실행과 트랜잭션 경계를 명시해야 한다
Pandas DataFrame -> DataFrame은 열 단위 데이터 변환을 구조화한다
SQL SELECT와 WHERE -> SELECT와 WHERE는 조회 범위와 조건을 분리한다
Streamlit Session State -> Streamlit 세션 상태는 재실행 사이의 값을 보존한다
Streamlit 기본 UI -> Streamlit UI는 위에서 아래로 재실행되는 흐름을 따른다
Train Test Split -> 학습 데이터와 평가 데이터는 모델 선택 전에 분리해야 한다
useEffect -> useEffect는 외부 시스템과 React 상태를 동기화한다
XGBoost -> XGBoost는 약한 트리를 순차적으로 보완한다
분류 평가 지표 -> 분류 평가는 클래스 불균형에 맞는 지표를 선택해야 한다
```

- [ ] **Step 2: Confirm all 34 staged concept notes were promoted**

```powershell
Get-ChildItem -LiteralPath '00 인박스\승격 대기\영구 노트' -File -ErrorAction SilentlyContinue
```

Expected: no files.

- [ ] **Step 3: Verify the complete 34-note permanent layer**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '30 영구 노트'
```

Expected: all 34 permanent notes have valid IDs, verified primary/mixed sources, at least one internal connection, and no discovery-only evidence.

- [ ] **Step 4: Commit the data and operations cluster**

```powershell
git add -A -- 'Second Brain 홈.md' '00 인박스' '20 소스 노트' '30 영구 노트' '40 프로젝트' '50 영역' '60 구조 노트'
git commit -m "docs(notes): promote data and operations zettels"
```

---

### Task 11: Curate reference, personal-area, and cross-project notes

**Files:**

- Modify: 21 files in `50 영역/개발 레퍼런스/`.
- Modify: `50 영역/개발 원칙/개인 Dev Rules.md`
- Modify: `50 영역/커리어/프로젝트 기반 개발자 정체성.md`
- Modify: `50 영역/회고/프로젝트 회고 질문 세트.md`
- Modify: `60 구조 노트/생각과 회고 지도.md`
- Modify: `40 프로젝트/공통/프로젝트 적용 로그.md`
- Modify: `40 프로젝트/공통/프로젝트 의사결정 로그.md`
- Modify: `40 프로젝트/공통/프로젝트 실패와 디버깅 로그.md`
- Modify: `40 프로젝트/프로젝트 경험 지도.md`
- Modify: `00 인박스/질문 인박스.md`
- Modify: `00 인박스/RAG 검색 실패 사례.md`
- Modify: `00 인박스/RAG 평가 질문 세트.md`

**Interfaces:**

- Produces a practical-reference layer without pretending cheat sheets are permanent claims.
- Produces personal notes explicitly marked as personal interpretation.

- [ ] **Step 1: Normalize the 21 reference notes**

Keep their filenames. Set `type: source`, `status: growing`, `source_quality: mixed`, and keep `verified: false` unless the commands/API calls are checked against current official documentation. Replace old tags and remove all `llm_wiki`, `reference` status, and old source paths. Add a visible `검증 범위` section to version-sensitive cheat sheets.

- [ ] **Step 2: Normalize personal and reflection notes**

Set personal notes to `source_quality: personal`, `verified: false`, and include `개인 해석` or `프로젝트 경험` in the body. Preserve the user's existing voice; do not invent motivations, feelings, or goals.

- [ ] **Step 3: Normalize project logs and questions**

For decision and debugging logs, use `상황`, `선택 또는 원인`, `근거`, `결과`, and `다음에 적용할 원칙`. Keep unanswered questions as `type: inbox`, `status: seed`; do not promote them merely to satisfy counts.

- [ ] **Step 4: Verify the curated operational layer**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '50 영역'
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '40 프로젝트/공통'
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '00 인박스'
```

Expected: no metadata, marker, or stale-path errors. Seed questions may remain warnings.

- [ ] **Step 5: Commit reference and personal context**

```powershell
git add -- '00 인박스' '40 프로젝트/공통' '40 프로젝트/프로젝트 경험 지도.md' '50 영역' '60 구조 노트/생각과 회고 지도.md'
git commit -m "docs(vault): curate reference and personal knowledge"
```

---

### Task 12: Rewrite the four existing project hubs

**Files:**

- Modify: `40 프로젝트/SKN26 1차 차량 운영비 프로젝트.md`
- Modify: `40 프로젝트/SKN26 2차 신용카드 고객 이탈 분석.md`
- Modify: `40 프로젝트/SKN26 3차 PICKLE 맛집 추천 챗봇.md`
- Modify: `40 프로젝트/SKN26 4차 LG Home AI 가전 상담.md`
- Read only: corresponding root README and code under `C:\MinHyeok\skn26_projects`.
- Read only: `https://minhyeok328.github.io/` for personal contribution and reflection.

**Interfaces:**

- Produces four project hubs with facts, team output, direct contribution, decisions, failures, reflection, and source paths explicitly separated.
- Produces project source notes in `20 소스 노트/프로젝트/` when a README or portfolio page needs a reusable summary.

- [ ] **Step 1: Verify current source paths before editing**

```powershell
@(
  'C:\MinHyeok\skn26_projects\1st_project\README.md',
  'C:\MinHyeok\skn26_projects\2nd_project\README.md',
  'C:\MinHyeok\skn26_projects\3rd_project\README.md',
  'C:\MinHyeok\skn26_projects\4th_project\README.md'
) | ForEach-Object { if(-not (Test-Path -LiteralPath $_)){ throw "Missing source: $_" } }
```

- [ ] **Step 2: Rewrite each project hub using the approved body contract**

Each hub must contain:

```markdown
## 프로젝트 개요
## 팀 산출물
## 직접 기여
## 기술적 의사결정
## 실패와 해결 과정
## 개인 회고와 성장
## 관련 영구 노트
## 출처
```

Use root README/code for factual implementation and the portfolio for personal contribution/reflection. When the sources disagree, the latest code and README win for technical facts; record the discrepancy rather than blending both accounts.

- [ ] **Step 3: Update old aliases and stale source paths**

Keep aliases for the four old project titles. Replace every old `C:\MinHyeok\skn26_*` source with one of these exact roots: `C:\MinHyeok\skn26_projects\1st_project`, `C:\MinHyeok\skn26_projects\2nd_project`, `C:\MinHyeok\skn26_projects\3rd_project`, or `C:\MinHyeok\skn26_projects\4th_project`.

- [ ] **Step 4: Verify the four hubs**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '40 프로젝트'
rg -n 'C:\\MinHyeok\\skn26_(1st|2nd|3rd|4th)' '40 프로젝트'
```

Expected: hub validation passes and stale-path search returns no matches.

- [ ] **Step 5: Commit the four project histories**

```powershell
git add -- '40 프로젝트/SKN26 1차 차량 운영비 프로젝트.md' '40 프로젝트/SKN26 2차 신용카드 고객 이탈 분석.md' '40 프로젝트/SKN26 3차 PICKLE 맛집 추천 챗봇.md' '40 프로젝트/SKN26 4차 LG Home AI 가전 상담.md' '20 소스 노트/프로젝트'
git commit -m "docs(projects): rewrite SKN26 project experience hubs"
```

---

### Task 13: Add the Final project and derived experience zettels

**Files:**

- Create: `40 프로젝트/SKN26 Final HumouR AI HR 채용 보조.md`
- Create: `20 소스 노트/프로젝트/HumouR README와 포트폴리오.md`
- Create: `30 영구 노트/인증 만료는 오류가 아니라 사용자 흐름의 일부다.md`
- Create: `30 영구 노트/오래된 비동기 응답은 최신 상태를 덮지 못하게 해야 한다.md`
- Create: `30 영구 노트/프론트엔드 상태는 권한 경계와 함께 정리해야 한다.md`
- Modify: `40 프로젝트/프로젝트 경험 지도.md`
- Read only: `C:\MinHyeok\skn26_projects\Final_project\README.md`
- Read only: `C:\MinHyeok\skn26_projects\Final_project\docs\00-overview\project-overview.md`
- Read only: `https://minhyeok328.github.io/`

**Interfaces:**

- Produces the fifth required project hub.
- Produces three `source_quality: mixed` permanent notes grounded in project code/README and explicitly labeled personal experience.

- [ ] **Step 1: Create the project source note**

Separate team-level facts from personal contribution. Record access date `2026-08-11`, local paths, the portfolio URL, and discrepancies if any.

- [ ] **Step 2: Create the HumouR hub**

Include these evidenced personal contribution areas from the portfolio and validate them against the repository before stating them as direct contribution:

- Axios/CSRF request layer, domain API client, Zod validation, adapters, and TanStack Query flow;
- login and external API-key authentication/session/query-cache boundaries;
- request cancellation, stale-response protection, authentication expiry, error normalization, and cache cleanup;
- JD, application, analysis report, interview question, external sharing, and document-chat integration;
- frontend test, QA, and interface documentation.

- [ ] **Step 3: Create three derived permanent notes**

Each derived note must link to the HumouR hub, one relevant official source note or reference, and at least one existing web permanent note. Mark the project experience portion explicitly and include a limitation showing when the principle does not apply.

- [ ] **Step 4: Update the project experience map**

Order all five projects chronologically and add a separate `프로젝트를 지나며 바뀐 개발 관점` section linking the three new zettels and existing personal identity note.

- [ ] **Step 5: Verify and commit**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '40 프로젝트'
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '30 영구 노트'
git add -- '20 소스 노트/프로젝트/HumouR README와 포트폴리오.md' '30 영구 노트' '40 프로젝트/SKN26 Final HumouR AI HR 채용 보조.md' '40 프로젝트/프로젝트 경험 지도.md'
git commit -m "docs(projects): add HumouR experience and derived zettels"
```

---

### Task 14: Build lecture maps, areas, and final navigation

**Files:**

- Create: 12 required files in `60 구조 노트/`.
- Create: `50 영역/기술 학습.md`
- Create: `50 영역/커리어.md`
- Create: `50 영역/개인 목표.md`
- Create: `50 영역/개발 원칙.md`
- Modify: `Second Brain 홈.md`

**Interfaces:**

- Consumes: all curated source, permanent, project, reference, and personal notes.
- Produces navigable maps rather than flat link dumps.

- [ ] **Step 1: Create the 12 lecture maps**

Create exactly:

```text
Python 학습 지도.md
MySQL 학습 지도.md
데이터 수집 학습 지도.md
데이터 분석 학습 지도.md
머신러닝 학습 지도.md
딥러닝 기초 학습 지도.md
NLP 딥러닝 학습 지도.md
LLM과 RAG 학습 지도.md
멀티모달 딥러닝 학습 지도.md
웹 클라이언트 학습 지도.md
웹 서버 학습 지도.md
DevOps 학습 지도.md
```

Each map must have `출발점`, `핵심 연결`, `프로젝트에서의 적용`, and `다음 질문`. Link the matching lecture source note and only relevant permanent/project notes. Do not reproduce the legacy MOC as an alphabetical inventory.

- [ ] **Step 2: Create four long-lived area notes**

- `기술 학습`: links the 12 lecture maps and current learning questions.
- `커리어`: links developer identity, project experience map, and evidence-backed growth goals.
- `개인 목표`: contains only existing or user-authored goals; if none are available, state that the area is intentionally empty and link the daily-note workflow instead of inventing goals.
- `개발 원칙`: links Personal Dev Rules, decision/debugging logs, and generalized permanent notes.

- [ ] **Step 3: Finalize the home note**

Confirm every home link resolves and the home contains only active Second Brain concepts. Do not link legacy LLM Wiki reports or the archive from the main learning navigation; provide one low-emphasis `보관함` link at the bottom for recovery.

- [ ] **Step 4: Verify maps and navigation**

```powershell
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only '60 구조 노트'
python -m Tools.second_brain.verify --vault . --allow-staged-drafts --only 'Second Brain 홈.md'
```

Expected: all 12 required maps exist and all home/map links resolve.

- [ ] **Step 5: Commit the navigation layer**

```powershell
git add -- 'Second Brain 홈.md' '50 영역/기술 학습.md' '50 영역/커리어.md' '50 영역/개인 목표.md' '50 영역/개발 원칙.md' '60 구조 노트'
git commit -m "docs(vault): add learning maps and Second Brain navigation"
```

---

### Task 15: Final verification, manual review, and migration report

**Files:**

- Create: `docs/superpowers/migrations/2026-08-11-final-report.json`
- Create: `docs/superpowers/migrations/2026-08-11-final-report.md`
- Modify only if verification reveals defects: affected active notes or migration tools/tests.

**Interfaces:**

- Consumes: all migration outputs and both baselines.
- Produces final proof that the migration satisfies the approved design.

- [ ] **Step 1: Run the complete unit test suite**

```powershell
python -m unittest discover -s Tools/second_brain/tests -v
```

Expected: all tests pass with zero failures and zero errors.

- [ ] **Step 2: Run final strict vault verification**

```powershell
python -m Tools.second_brain.verify --vault . --final --obsidian-snapshot docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json --source-snapshot docs/superpowers/migrations/2026-08-11-source-snapshot.json --json docs/superpowers/migrations/2026-08-11-final-report.json
```

Expected: zero errors. Warnings are allowed only for intentionally unanswered inbox questions and unverified version-sensitive reference notes; list each warning in the Markdown report.

- [ ] **Step 3: Run explicit regression searches**

```powershell
rg -n 'llm_wiki|wiki-standardized|wiki-expanded|source-expanded|project-expanded|LLM Wiki 검색' --glob '*.md' --glob '!90 보관함/**' --glob '!docs/**'
rg -n 'C:\\lecture|C:\\MinHyeok\\skn26_(1st|2nd|3rd|4th)' --glob '*.md' --glob '!90 보관함/**'
```

Expected: no active-vault matches.

- [ ] **Step 4: Confirm exact required deliverables**

```powershell
(Get-ChildItem -LiteralPath '40 프로젝트' -File | Where-Object Name -Match '^SKN26').Count
(Get-ChildItem -LiteralPath '60 구조 노트' -File | Where-Object Name -Match '학습 지도\.md$').Count
(Get-ChildItem -LiteralPath '99 템플릿' -File).Count
```

Expected: `5`, `12`, and `5` respectively.

- [ ] **Step 5: Manually review representative notes**

Review at least:

- all five project hubs;
- one source note from each of the 12 lecture areas;
- `RAG의 성능은 검색 단계의 품질에서 시작된다.md`;
- `React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다.md`;
- `학습 데이터와 평가 데이터는 모델 선택 전에 분리해야 한다.md`;
- one practical reference note;
- one personal reflection note;
- `Second Brain 홈.md` and all 12 map notes.

Confirm the voice is natural Korean, facts and personal interpretation are visibly separated, no note uses the repeated LLM Wiki template, and links provide meaningful context rather than an unexplained list.

- [ ] **Step 6: Verify protected settings and source roots one final time**

```powershell
python -m Tools.second_brain.snapshot --verify-hashes docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json
python -m Tools.second_brain.snapshot --verify-tree docs/superpowers/migrations/2026-08-11-source-snapshot.json
git diff -- .obsidian/core-plugins.json .obsidian/graph.json .obsidian/workspace.json
```

Expected: snapshots pass and the three-file diff still matches the user's baseline.

If a source snapshot differs, do not restore or overwrite the external file. Inspect the changed paths and timestamps, report them as possible concurrent user changes, and request confirmation before declaring the migration complete.

- [ ] **Step 7: Write the concise final report**

The Markdown report must include:

- active note counts by `type` and `status`;
- archived legacy note count;
- five project hub names;
- twelve lecture map names;
- unit-test and verifier command results;
- unresolved warnings with exact paths;
- confirmation that source roots and protected Obsidian settings were unchanged.

- [ ] **Step 8: Commit verification artifacts and any necessary fixes**

If verification finds a defect, return to the task that introduced it, fix and commit only those affected paths, and rerun Steps 1-7. Do not hide content fixes inside the final-report commit.

```powershell
git add -- docs/superpowers/migrations/2026-08-11-final-report.json docs/superpowers/migrations/2026-08-11-final-report.md
git commit -m "chore(vault): verify Second Brain migration"
```

- [ ] **Step 9: Inspect final repository state**

```powershell
git status --short
git log --oneline -15
```

Expected: only the user's pre-existing `.obsidian/core-plugins.json`, `.obsidian/graph.json`, and `.obsidian/workspace.json` changes remain unstaged; all migration work is committed in reviewable task commits.
