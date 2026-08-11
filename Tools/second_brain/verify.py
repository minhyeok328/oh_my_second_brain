from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
from typing import Iterable

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
TEMPLATE_FILES = (
    "데일리 노트 템플릿.md", "소스 노트 템플릿.md", "영구 노트 템플릿.md",
    "프로젝트 노트 템플릿.md", "회고 노트 템플릿.md",
)
REQUIRED_PROJECT_HUBS = {
    "SKN26 1차 차량 운행비 프로젝트", "SKN26 2차 신용카드 고객 이탈 분석",
    "SKN26 3차 PICKLE 맛집 추천 챗봇", "SKN26 4차 LG Home AI 가전 상담",
    "SKN26 Final HumouR AI HR 채용 보조",
}
REQUIRED_LECTURE_MAPS = {
    "Python 학습 지도", "MySQL 학습 지도", "데이터 수집 학습 지도", "데이터 분석 학습 지도",
    "머신러닝 학습 지도", "딥러닝 기초 학습 지도", "NLP 딥러닝 학습 지도", "LLM과 RAG 학습 지도",
    "멀티모달 딥러닝 학습 지도", "파이프라인 학습 지도", "서버 학습 지도", "DevOps 학습 지도",
}
ID_RE = re.compile(r"^\d{14}-[a-z0-9]{4}$")


@dataclass(frozen=True)
class VerificationIssue:
    code: str
    path: str
    message: str


def _issue(issues: list[VerificationIssue], code: str, path: str, message: str) -> None:
    issues.append(VerificationIssue(code, path, message))


def _relative(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def _is_archive(relative: str) -> bool:
    return relative == ARCHIVE_ROOT or relative.startswith(ARCHIVE_ROOT + "/")


def _is_template(relative: str) -> bool:
    return relative == TEMPLATE_ROOT or relative.startswith(TEMPLATE_ROOT + "/")


def _selected(relative: str, only: str | None) -> bool:
    if not only:
        return True
    normalized = only.replace("\\", "/").strip("/")
    return relative == normalized or relative.startswith(normalized + "/") or Path(relative).name == normalized


def _read_snapshot(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _verify_snapshots(vault: Path, obsidian_snapshot: Path | None, source_snapshot: Path | None, issues: list[VerificationIssue]) -> None:
    if obsidian_snapshot:
        expected = _read_snapshot(obsidian_snapshot)
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
        expected = _read_snapshot(source_snapshot)
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
    if not template_root.exists():
        return
    for filename in TEMPLATE_FILES:
        path = template_root / filename
        relative = _relative(vault, path)
        if not path.is_file():
            _issue(issues, "missing-required-field", relative, "required template is missing")
            continue
        text = path.read_text(encoding="utf-8")
        if "{{date:" not in text or "{{time:" not in text:
            _issue(issues, "missing-required-field", relative, "template lacks approved Obsidian date/time variables")


def verify_vault(vault: Path, *, final: bool, allow_staged_drafts: bool = False, only: str | None = None, obsidian_snapshot: Path | None = None, source_snapshot: Path | None = None) -> list[VerificationIssue]:
    """Return deterministic, read-only integrity issues for a Second Brain vault."""
    root = vault.resolve()
    issues: list[VerificationIssue] = []
    notes: list[tuple[Path, str, object]] = []
    aliases: dict[str, str] = {}
    ids: dict[str, list[str]] = {}
    for path in sorted(root.rglob("*.md"), key=lambda item: _relative(root, item)):
        relative = _relative(root, path)
        if _is_archive(relative) or not _selected(relative, only):
            continue
        try:
            note = parse_markdown(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, ValueError) as error:
            _issue(issues, "missing-frontmatter", relative, str(error))
            continue
        if not note.metadata:
            _issue(issues, "missing-frontmatter", relative, "note has no frontmatter")
            continue
        if _is_template(relative):
            continue
        notes.append((path, relative, note))
        note_aliases = note.metadata.get("aliases", [])
        if not isinstance(note_aliases, list):
            note_aliases = []
        for name in [path.stem, *note_aliases]:
            aliases[str(name)] = relative
        for field in REQUIRED_FIELDS:
            if not str(note.metadata.get(field, "")).strip():
                _issue(issues, "missing-required-field", relative, f"missing required field: {field}")
        identifier = str(note.metadata.get("id", ""))
        if identifier and not ID_RE.fullmatch(identifier):
            _issue(issues, "invalid-id", relative, "id must be YYYYMMDDHHMMSS-xxxx")
        if identifier:
            ids.setdefault(identifier, []).append(relative)
        note_type, status = str(note.metadata.get("type", "")), str(note.metadata.get("status", ""))
        quality = str(note.metadata.get("source_quality", ""))
        if note_type and note_type not in VALID_TYPES: _issue(issues, "invalid-type", relative, f"unsupported type: {note_type}")
        if status and status not in VALID_STATUSES: _issue(issues, "invalid-status", relative, f"unsupported status: {status}")
        if quality and quality not in VALID_SOURCE_QUALITIES: _issue(issues, "invalid-source-quality", relative, f"unsupported source_quality: {quality}")
        if note_type == "permanent":
            sources = note.metadata.get("sources")
            if not isinstance(sources, list) or not sources:
                _issue(issues, "missing-required-field", relative, "permanent note needs sources")
            if not extract_wikilinks(note.body): _issue(issues, "missing-required-field", relative, "permanent note needs an internal link")
            if status not in {"growing", "evergreen"}: _issue(issues, "invalid-status", relative, "permanent note must be growing or evergreen")
            if quality == "discovery": _issue(issues, "discovery-only-permanent", relative, "permanent note cannot use discovery sources only")
            if status == "evergreen" and note.metadata.get("verified") is not True:
                _issue(issues, "unverified-evergreen", relative, "evergreen permanent note must be verified")
            if note.metadata.get("verified") is True and quality not in {"primary", "mixed"}:
                _issue(issues, "invalid-source-quality", relative, "verified factual permanent note needs primary or mixed quality")
            if quality == "personal" and not any(marker in note.body for marker in ("개인 해석", "프로젝트 경험")):
                _issue(issues, "missing-required-field", relative, "personal permanent note needs personal interpretation or project experience")
        source_path = note.metadata.get("source_path")
        if source_path and not Path(str(source_path)).exists():
            _issue(issues, "stale-source-path", relative, f"source_path does not exist: {source_path}")
        if any(marker in note.body for marker in LEGACY_MARKERS):
            _issue(issues, "legacy-llm-marker", relative, "legacy LLM marker is allowed only in archive")
    for identifier, paths in sorted(ids.items()):
        if len(paths) > 1:
            for relative in paths: _issue(issues, "duplicate-id", relative, f"duplicate id: {identifier}")
    for _, relative, note in notes:
        for link in extract_wikilinks(note.body):
            target = aliases.get(link)
            if target is None:
                archive_candidate = root / ARCHIVE_ROOT / f"{link}.md"
                if archive_candidate.exists() and _relative(root, archive_candidate) != ARCHIVE_GUIDE:
                    _issue(issues, "unresolved-link", relative, f"active note links to archived note: {link}")
                else:
                    _issue(issues, "unresolved-link", relative, f"unresolved internal link: {link}")
    if only is None:
        _template_issues(root, issues)
        if final:
            active_stems = {path.stem for path, _, _ in notes}
            for name in sorted(REQUIRED_PROJECT_HUBS - active_stems): _issue(issues, "missing-project-hub", name, "required project hub is missing")
            for name in sorted(REQUIRED_LECTURE_MAPS - active_stems): _issue(issues, "missing-lecture-map", name, "required lecture map is missing")
        _verify_snapshots(root, obsidian_snapshot, source_snapshot, issues)
    return sorted(issues, key=lambda issue: (issue.path, issue.code, issue.message))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify a Second Brain vault without modifying it.")
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--final", action="store_true")
    parser.add_argument("--allow-staged-drafts", action="store_true")
    parser.add_argument("--only")
    parser.add_argument("--obsidian-snapshot", type=Path)
    parser.add_argument("--source-snapshot", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    issues = verify_vault(args.vault, final=args.final, allow_staged_drafts=args.allow_staged_drafts, only=args.only, obsidian_snapshot=args.obsidian_snapshot, source_snapshot=args.source_snapshot)
    if args.json: print(json.dumps([asdict(issue) for issue in issues], ensure_ascii=False, sort_keys=True))
    else:
        for issue in issues: print(f"{issue.code}: {issue.path}: {issue.message}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
