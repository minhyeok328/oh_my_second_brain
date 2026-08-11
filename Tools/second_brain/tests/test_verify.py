import errno
from contextlib import redirect_stderr
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from Tools.second_brain.verify import (
    ARCHIVE_GUIDE,
    ARCHIVE_ROOT,
    REQUIRED_LECTURE_MAPS,
    REQUIRED_PROJECT_HUBS,
    TEMPLATE_FILES,
    TEMPLATE_ROOT,
    VerificationIssue,
    _json_output_path,
    _open_json_temp,
    _write_json_temp,
    main as verify_main,
    verify_vault,
)


def write_note(path: Path, metadata: str, body: str = "[[Target]]") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{metadata}\n---\n{body}\n", encoding="utf-8")


def create_symlink_or_skip(link: Path, target: Path, *, target_is_directory: bool = False) -> None:
    try:
        link.symlink_to(target, target_is_directory=target_is_directory)
    except OSError as error:
        if getattr(error, "winerror", None) == 1314 or error.errno in {errno.EACCES, errno.EPERM}:
            raise unittest.SkipTest(f"symbolic-link creation is unavailable on this host: {error}") from error
        raise


VALID = """id: '20260811000000-abcd'
type: permanent
status: growing
created: 2026-08-11
updated: 2026-08-11
source_quality: primary
verified: true
sources:
  - source"""

APPROVED_PROJECT_HUBS = {
    "SKN26 1차 차량 운영비 프로젝트",
    "SKN26 2차 신용카드 고객 이탈 분석",
    "SKN26 3차 PICKLE 맛집 추천 챗봇",
    "SKN26 4차 LG Home AI 가전 상담",
    "SKN26 Final HumouR AI HR 채용 보조",
}
APPROVED_LECTURE_MAPS = {
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


class VerifyTests(unittest.TestCase):
    def issues_for(self, metadata: str, body: str = "[[Target]]") -> set[str]:
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "Notes" / "Target.md", VALID, "target")
            write_note(vault / "Notes" / "Example.md", metadata, body)
            return {issue.code for issue in verify_vault(vault, final=False)}

    def test_reports_frontmatter_and_required_metadata_errors(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / "note.md").write_text("body", encoding="utf-8")
            self.assertIn("missing-frontmatter", {x.code for x in verify_vault(vault, final=False)})
        self.assertIn("missing-required-field", self.issues_for("id: x"))

    def test_reports_invalid_and_duplicate_ids(self):
        self.assertIn("invalid-id", self.issues_for(VALID.replace("20260811000000-abcd", "bad")))
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "One.md", VALID, "one")
            write_note(vault / "Two.md", VALID, "two")
            self.assertIn("duplicate-id", {x.code for x in verify_vault(vault, final=False)})

    def test_reports_invalid_taxonomy_and_promotion_errors(self):
        self.assertIn("invalid-type", self.issues_for(VALID.replace("type: permanent", "type: nope")))
        self.assertIn("invalid-status", self.issues_for(VALID.replace("status: growing", "status: nope")))
        self.assertIn("invalid-source-quality", self.issues_for(VALID.replace("source_quality: primary", "source_quality: nope")))
        self.assertIn("discovery-only-permanent", self.issues_for(VALID.replace("source_quality: primary", "source_quality: discovery")))
        self.assertIn("unverified-evergreen", self.issues_for(VALID.replace("status: growing", "status: evergreen").replace("verified: true", "verified: false")))
        personal = VALID.replace("source_quality: primary", "source_quality: personal")
        self.assertNotIn("invalid-source-quality", self.issues_for(personal, "개인 해석 [[Target]]"))
        self.assertIn("missing-required-field", self.issues_for(personal, "[[Target]]"))

    def test_unverified_permanent_note_accepts_secondary_source_quality(self):
        secondary = VALID.replace("source_quality: primary", "source_quality: secondary").replace(
            "verified: true", "verified: false"
        )

        self.assertNotIn("invalid-source-quality", self.issues_for(secondary))

    def test_verified_permanent_note_still_rejects_secondary_only_sources(self):
        secondary = VALID.replace("source_quality: primary", "source_quality: secondary")

        self.assertIn("invalid-source-quality", self.issues_for(secondary))

    def test_reports_links_markers_and_stale_sources(self):
        self.assertIn("unresolved-link", self.issues_for(VALID, "[[Missing]]"))
        self.assertIn("legacy-llm-marker", self.issues_for(VALID, "llm_wiki"))
        self.assertIn("stale-source-path", self.issues_for(VALID + "\nsource_path: missing", "[[Target]]"))

    def test_archive_legacy_markers_and_links_do_not_fail(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / ARCHIVE_ROOT / "old.md", "", "llm_wiki [[Missing]]")
            codes = {issue.code for issue in verify_vault(vault, final=False)}
            self.assertNotIn("legacy-llm-marker", codes)
            self.assertNotIn("unresolved-link", codes)

    def test_reports_required_hubs_and_snapshot_drift(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            settings = vault / ".obsidian" / "graph.json"
            settings.parent.mkdir(); settings.write_text("{}", encoding="utf-8")
            obsidian = vault / "obsidian.json"; obsidian.write_text(json.dumps({str(settings): "wrong"}), encoding="utf-8")
            source = vault / "source.json"; source.write_text(json.dumps({str(vault): []}), encoding="utf-8")
            codes = {x.code for x in verify_vault(vault, final=True, obsidian_snapshot=obsidian, source_snapshot=source)}
            self.assertTrue({"missing-project-hub", "missing-lecture-map", "protected-settings-changed", "source-tree-changed"}.issubset(codes))

    def test_required_project_and_lecture_map_names_match_the_approved_contract(self):
        self.assertEqual(APPROVED_PROJECT_HUBS, REQUIRED_PROJECT_HUBS)
        self.assertEqual(APPROVED_LECTURE_MAPS, REQUIRED_LECTURE_MAPS)

    def test_final_verifier_accepts_exact_approved_project_and_lecture_map_names(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            approved_names = sorted(APPROVED_PROJECT_HUBS | APPROVED_LECTURE_MAPS)
            for index, name in enumerate(approved_names):
                metadata = VALID.replace("20260811000000-abcd", f"202608110000{index:02d}-a{index:03x}")
                write_note(vault / f"{name}.md", metadata, "approved contract note")

            completeness_issues = {
                issue.code
                for issue in verify_vault(vault, final=True)
                if issue.code in {"missing-project-hub", "missing-lecture-map"}
            }

            self.assertEqual(set(), completeness_issues)

    def test_stale_project_and_lecture_map_substitutes_do_not_satisfy_contract(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            names = (
                APPROVED_PROJECT_HUBS
                - {"SKN26 1차 차량 운영비 프로젝트"}
                | {"SKN26 1차 차량 운행비 프로젝트"}
            )
            names |= (
                APPROVED_LECTURE_MAPS
                - {"웹 클라이언트 학습 지도", "웹 서버 학습 지도"}
                | {"파이프라인 학습 지도", "서버 학습 지도"}
            )
            for index, name in enumerate(sorted(names)):
                metadata = VALID.replace("20260811000000-abcd", f"202608110000{index:02d}-b{index:03x}")
                write_note(vault / f"{name}.md", metadata, "stale contract note")

            missing = {
                (issue.code, issue.path)
                for issue in verify_vault(vault, final=True)
                if issue.code in {"missing-project-hub", "missing-lecture-map"}
            }

            self.assertEqual(
                {
                    ("missing-project-hub", "SKN26 1차 차량 운영비 프로젝트"),
                    ("missing-lecture-map", "웹 클라이언트 학습 지도"),
                    ("missing-lecture-map", "웹 서버 학습 지도"),
                },
                missing,
            )

    def test_json_output_is_machine_readable(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / "note.md").write_text("body", encoding="utf-8")
            issues = verify_vault(vault, final=False)
            self.assertIn("missing-frontmatter", {issue.code for issue in issues})

    def test_embeds_resolve_active_notes_and_vault_attachments(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "Folder" / "Target.md", VALID, "target")
            (vault / "assets").mkdir(); (vault / "assets" / "image.png").write_bytes(b"png")
            write_note(vault / "Example.md", VALID, "![[Folder/Target#part|label]] ![[assets/image.png]]")
            self.assertNotIn("unresolved-link", {x.code for x in verify_vault(vault, final=False) if x.path == "Example.md"})
            write_note(vault / "Broken.md", VALID, "![[Missing]] ![[assets/lost.png]]")
            self.assertIn("unresolved-link", {x.code for x in verify_vault(vault, final=False) if x.path == "Broken.md"})

    def test_permanent_note_embed_to_an_active_note_satisfies_internal_link_rule(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "Other Note.md", VALID.replace("abcd", "1111"), "target")
            write_note(vault / "Embedded.md", VALID.replace("abcd", "2222"), "![[Other Note]]")
            issues = [x for x in verify_vault(vault, final=False) if x.path == "Embedded.md"]
            self.assertNotIn("missing-required-field", {x.code for x in issues})

    def test_staged_drafts_keep_taxonomy_integrity_errors(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "00 인박스" / "승격 대기" / "draft.md", "type: nope\nstatus: nope\nsource_quality: nope", "draft")
            codes = {x.code for x in verify_vault(vault, final=True, allow_staged_drafts=True)}
            self.assertTrue({"invalid-type", "invalid-status", "invalid-source-quality"}.issubset(codes))

    def test_archive_guide_accepts_bare_and_path_qualified_links(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            guide = vault / ARCHIVE_GUIDE; write_note(guide, "", "guide")
            guide_path = guide.relative_to(vault).with_suffix("").as_posix()
            write_note(vault / "Active.md", VALID, f"[[{guide.stem}#section|label]] [[{guide_path}#section|label]]")
            self.assertNotIn("unresolved-link", {x.code for x in verify_vault(vault, final=False) if x.path == "Active.md"})

    def test_attachment_embeds_resolve_unique_basenames_and_reject_duplicates(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / "assets" / "one").mkdir(parents=True)
            (vault / "assets" / "one" / "image.png").write_bytes(b"png")
            write_note(vault / "Active.md", VALID, "![[image.png]]")
            self.assertNotIn("unresolved-link", {x.code for x in verify_vault(vault, final=False) if x.path == "Active.md"})
            (vault / "assets" / "two").mkdir(); (vault / "assets" / "two" / "image.png").write_bytes(b"png")
            messages = [x.message for x in verify_vault(vault, final=False) if x.path == "Active.md" and x.code == "unresolved-link"]
            self.assertEqual(1, len(messages)); self.assertIn("ambiguous", messages[0])

    def test_templates_are_required_even_when_directory_is_missing(self):
        with TemporaryDirectory() as temporary_directory:
            issues = verify_vault(Path(temporary_directory), final=False)
            missing = [issue for issue in issues if issue.code == "missing-template"]
            self.assertEqual({f"{TEMPLATE_ROOT}/{name}" for name in TEMPLATE_FILES}, {issue.path for issue in missing})

    def test_daily_template_uses_date_without_requiring_a_time_variable(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            for filename in TEMPLATE_FILES:
                variables = "{{date:YYYY-MM-DD}}" if filename == TEMPLATE_FILES[0] else "{{date:YYYY-MM-DD}} {{time:HHmmss}}"
                (vault / TEMPLATE_ROOT / filename).parent.mkdir(parents=True, exist_ok=True)
                (vault / TEMPLATE_ROOT / filename).write_text(variables, encoding="utf-8")
            self.assertEqual([], [x for x in verify_vault(vault, final=False) if x.code == "missing-template"])

    def test_only_uses_global_indexes_and_preserves_cross_folder_links(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "A" / "Selected.md", VALID.replace("abcd", "1111"), "[[B/Target]]")
            write_note(vault / "B" / "Target.md", VALID.replace("abcd", "1111"), "target")
            issues = verify_vault(vault, final=False, only="A")
            self.assertNotIn("unresolved-link", {x.code for x in issues})
            self.assertEqual(2, sum(x.code == "duplicate-id" for x in issues))

    def test_duplicate_alias_is_ambiguous_and_path_links_resolve(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "One" / "Same.md", VALID.replace("abcd", "1111") + "\naliases:\n  - shared", "one")
            write_note(vault / "Two" / "Same.md", VALID.replace("abcd", "2222") + "\naliases:\n  - shared", "two")
            write_note(vault / "Use.md", VALID.replace("abcd", "3333"), "[[One/Same]] [[shared]]")
            messages = [x.message for x in verify_vault(vault, final=False) if x.path == "Use.md" and x.code == "unresolved-link"]
            self.assertEqual(1, len(messages)); self.assertIn("ambiguous", messages[0])

    def test_staged_drafts_defer_only_inbox_promotion_and_final_completeness(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "00 인박스" / "승격 대기" / "draft.md", "type: permanent\nstatus: seed", "draft")
            strict = {x.code for x in verify_vault(vault, final=True)}
            staged = {x.code for x in verify_vault(vault, final=True, allow_staged_drafts=True)}
            self.assertIn("missing-project-hub", strict); self.assertNotIn("missing-project-hub", staged)
            self.assertIn("missing-required-field", strict); self.assertNotIn("missing-required-field", staged)

    def test_full_transition_staged_drafts_keep_invalid_ids_but_defer_content_debt(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "00 인박스" / "승격 대기" / "draft.md", "id: bad\ntype: permanent\nstatus: seed", "llm_wiki [[Missing]]")
            codes = {x.code for x in verify_vault(vault, final=True, allow_staged_drafts=True)}
            self.assertIn("invalid-id", codes)
            self.assertNotIn("legacy-llm-marker", codes)
            self.assertNotIn("unresolved-link", codes)

    def test_repository_roots_are_excluded_from_note_discovery(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            for root_name in (".superpowers", "docs", "Tools", ".codex_recovery", ".obsidian", ".worktrees"):
                path = vault / root_name / "orchestration.md"
                path.parent.mkdir(parents=True)
                path.write_text("not a vault note", encoding="utf-8")
            issues = verify_vault(vault, final=False, only="orchestration.md")
            self.assertNotIn("missing-frontmatter", {issue.code for issue in issues})

    def test_full_transition_defers_only_known_content_debt(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "Notes" / "Debt.md", VALID, "llm_wiki [[Missing]]")
            codes = {issue.code for issue in verify_vault(vault, final=False, allow_staged_drafts=True)}
            self.assertNotIn("legacy-llm-marker", codes)
            self.assertNotIn("unresolved-link", codes)

    def test_scoped_transition_keeps_known_content_debt_strict(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "Notes" / "Debt.md", VALID, "llm_wiki [[Missing]]")
            codes = {
                issue.code
                for issue in verify_vault(vault, final=False, allow_staged_drafts=True, only="Notes")
            }
            self.assertTrue({"legacy-llm-marker", "unresolved-link"}.issubset(codes))

    def test_full_transition_keeps_structural_taxonomy_and_snapshot_errors(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(
                vault / "Notes" / "Unsafe.md",
                VALID.replace("20260811000000-abcd", "bad")
                .replace("type: permanent", "type: nope")
                .replace("status: growing", "status: nope")
                .replace("source_quality: primary", "source_quality: nope")
                + "\nsource_path: missing",
                "body",
            )
            snapshot = vault / "invalid-snapshot.json"
            snapshot.write_text("{", encoding="utf-8")
            codes = {
                issue.code
                for issue in verify_vault(
                    vault,
                    final=False,
                    allow_staged_drafts=True,
                    obsidian_snapshot=snapshot,
                    source_snapshot=snapshot,
                )
            }
            self.assertTrue(
                {
                    "invalid-id",
                    "invalid-type",
                    "invalid-status",
                    "invalid-source-quality",
                    "stale-source-path",
                    "protected-settings-changed",
                    "source-tree-changed",
                }.issubset(codes)
            )

    def test_full_transition_keeps_malformed_approved_note_strict(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            path = vault / "20 소스 노트" / "Broken.md"
            path.parent.mkdir(parents=True)
            path.write_text("missing frontmatter", encoding="utf-8")
            issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            self.assertIn(
                VerificationIssue("missing-frontmatter", "20 소스 노트/Broken.md", "note has no frontmatter"),
                issues,
            )

    def test_full_transition_keeps_malformed_root_home_strict(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / "Second Brain 홈.md").write_text("missing frontmatter", encoding="utf-8")
            issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            self.assertIn(
                VerificationIssue("missing-frontmatter", "Second Brain 홈.md", "note has no frontmatter"),
                issues,
            )

    def test_full_transition_keeps_duplicate_ids_strict(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            metadata = VALID.replace("type: permanent", "type: source")
            write_note(vault / "Notes" / "One.md", metadata, "one")
            write_note(vault / "Notes" / "Two.md", metadata, "two")
            duplicate_paths = {
                issue.path
                for issue in verify_vault(vault, final=False, allow_staged_drafts=True)
                if issue.code == "duplicate-id"
            }
            self.assertEqual({"Notes/One.md", "Notes/Two.md"}, duplicate_paths)

    def test_full_transition_keeps_missing_templates_strict(self):
        with TemporaryDirectory() as temporary_directory:
            issues = verify_vault(Path(temporary_directory), final=False, allow_staged_drafts=True)
            missing_paths = {issue.path for issue in issues if issue.code == "missing-template"}
            self.assertEqual({f"{TEMPLATE_ROOT}/{filename}" for filename in TEMPLATE_FILES}, missing_paths)

    def test_full_transition_keeps_invalid_templates_strict(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            for filename in TEMPLATE_FILES:
                variables = "{{date:YYYY-MM-DD}}" if filename == TEMPLATE_FILES[0] else "{{date:YYYY-MM-DD}} {{time:HHmmss}}"
                write_note(vault / TEMPLATE_ROOT / filename, "template: true", variables)
            invalid = vault / TEMPLATE_ROOT / TEMPLATE_FILES[0]
            write_note(invalid, "template: true", "missing approved date variable")
            invalid_paths = {
                issue.path
                for issue in verify_vault(vault, final=False, allow_staged_drafts=True)
                if issue.code == "missing-template"
            }
            self.assertEqual({f"{TEMPLATE_ROOT}/{TEMPLATE_FILES[0]}"}, invalid_paths)

    def test_full_transition_rejects_simulated_symlink_before_reading_it(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            unsafe = vault / "Notes" / "Unsafe.md"
            write_note(unsafe, VALID, "body")
            original_read_text = Path.read_text
            reads: list[Path] = []

            def tracked_read_text(candidate: Path, *args, **kwargs):
                if candidate == unsafe:
                    reads.append(candidate)
                return original_read_text(candidate, *args, **kwargs)

            with patch.object(Path, "is_symlink", new=lambda candidate: candidate == unsafe):
                with patch.object(Path, "read_text", new=tracked_read_text):
                    issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            self.assertIn(
                VerificationIssue("unsafe-path", "Notes/Unsafe.md", "path contains a symbolic-link component"),
                issues,
            )
            self.assertEqual([], reads)

    def test_full_transition_rejects_non_regular_markdown_path(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / "Notes" / "Directory.md").mkdir(parents=True)
            issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            self.assertIn(
                VerificationIssue("unsafe-path", "Notes/Directory.md", "resolved path is not a regular file"),
                issues,
            )

    def test_full_transition_rejects_simulated_resolved_path_outside_vault(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory) / "vault"
            outside = Path(temporary_directory) / "outside.txt"
            unsafe = vault / "Notes" / "Unsafe.md"
            write_note(unsafe, VALID, "body")
            outside.write_text("outside", encoding="utf-8")
            original_resolve = Path.resolve

            def resolve(candidate: Path, strict: bool = False):
                if candidate == unsafe:
                    return outside
                return original_resolve(candidate, strict=strict)

            with patch.object(Path, "resolve", new=resolve):
                issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            self.assertIn(
                VerificationIssue("unsafe-path", "Notes/Unsafe.md", "resolved path escapes vault"),
                issues,
            )

    def test_full_transition_rejects_simulated_non_markdown_resolution(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            unsafe = vault / "Notes" / "Unsafe.md"
            resolved = vault / "Notes" / "Unsafe.txt"
            write_note(unsafe, VALID, "body")
            resolved.write_text("not Markdown", encoding="utf-8")
            original_resolve = Path.resolve

            def resolve(candidate: Path, strict: bool = False):
                if candidate == unsafe:
                    return resolved
                return original_resolve(candidate, strict=strict)

            with patch.object(Path, "resolve", new=resolve):
                issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            self.assertIn(
                VerificationIssue("unsafe-path", "Notes/Unsafe.md", "resolved path is not Markdown"),
                issues,
            )

    def test_full_transition_rejects_real_symlink_without_reading_target(self):
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "vault"
            alias = vault / "Notes" / "Alias.md"
            target = root / "outside.txt"
            alias.parent.mkdir(parents=True)
            target.write_text("outside bytes", encoding="utf-8")
            create_symlink_or_skip(alias, target)
            before = target.read_bytes()
            issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            self.assertIn(
                VerificationIssue("unsafe-path", "Notes/Alias.md", "path contains a symbolic-link component"),
                issues,
            )
            self.assertEqual(before, target.read_bytes())
            self.assertTrue(alias.is_symlink())

    def test_full_transition_reports_unsafe_template_once_without_reading_it(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            unsafe = vault / TEMPLATE_ROOT / TEMPLATE_FILES[0]
            write_note(unsafe, "template: true", "{{date:YYYY-MM-DD}}")
            original_read_text = Path.read_text
            reads: list[Path] = []

            def tracked_read_text(candidate: Path, *args, **kwargs):
                if candidate == unsafe:
                    reads.append(candidate)
                return original_read_text(candidate, *args, **kwargs)

            with patch.object(Path, "is_symlink", new=lambda candidate: candidate == unsafe):
                with patch.object(Path, "read_text", new=tracked_read_text):
                    issues = verify_vault(vault, final=False, allow_staged_drafts=True)
            unsafe_issues = [issue for issue in issues if issue.path == f"{TEMPLATE_ROOT}/{TEMPLATE_FILES[0]}" and issue.code == "unsafe-path"]
            self.assertEqual(
                [VerificationIssue("unsafe-path", f"{TEMPLATE_ROOT}/{TEMPLATE_FILES[0]}", "path contains a symbolic-link component")],
                unsafe_issues,
            )
            self.assertEqual([], reads)

    def test_cli_full_transition_succeeds_while_scoped_content_debt_fails(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(
                vault / "Notes" / "Debt.md",
                VALID.replace("type: permanent", "type: source"),
                "llm_wiki [[Missing]]",
            )
            for filename in TEMPLATE_FILES:
                variables = "{{date:YYYY-MM-DD}}" if filename == TEMPLATE_FILES[0] else "{{date:YYYY-MM-DD}} {{time:HHmmss}}"
                path = vault / TEMPLATE_ROOT / filename
                write_note(path, "template: true", variables)
            full = subprocess.run(
                [sys.executable, "-m", "Tools.second_brain.verify", "--vault", str(vault), "--allow-staged-drafts", "--json"],
                text=True,
                capture_output=True,
                check=False,
            )
            scoped = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "Tools.second_brain.verify",
                    "--vault",
                    str(vault),
                    "--allow-staged-drafts",
                    "--only",
                    "Notes",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual((0, []), (full.returncode, json.loads(full.stdout)))
            self.assertEqual(1, scoped.returncode)
            self.assertEqual({"legacy-llm-marker", "unresolved-link"}, {issue["code"] for issue in json.loads(scoped.stdout)})

    def test_cli_json_supports_stdout_and_safe_vault_relative_report_files(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(
                vault / "Notes" / "Valid.md",
                VALID.replace("type: permanent", "type: source"),
                "valid",
            )
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)

            stdout_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "Tools.second_brain.verify",
                    "--vault",
                    str(vault),
                    "--only",
                    "Notes",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, stdout_result.returncode)
            self.assertEqual([], json.loads(stdout_result.stdout))

            success_path = "docs/superpowers/migrations/success.json"
            success_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "Tools.second_brain.verify",
                    "--vault",
                    str(vault),
                    "--only",
                    "Notes",
                    "--json",
                    success_path,
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(0, success_result.returncode)
            self.assertEqual("", success_result.stdout)
            self.assertEqual("[]\n", (vault / success_path).read_text(encoding="utf-8"))

            (vault / "Notes" / "Broken.md").write_text("missing frontmatter", encoding="utf-8")
            failure_path = "docs/superpowers/migrations/failure.json"
            failure_result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "Tools.second_brain.verify",
                    "--vault",
                    str(vault),
                    "--only",
                    "Notes",
                    "--json",
                    failure_path,
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            failure_text = (vault / failure_path).read_text(encoding="utf-8")
            self.assertEqual(1, failure_result.returncode)
            self.assertEqual("", failure_result.stdout)
            self.assertTrue(failure_text.endswith("\n"))
            self.assertEqual(
                [{"code": "missing-frontmatter", "message": "note has no frontmatter", "path": "Notes/Broken.md"}],
                json.loads(failure_text),
            )

    def test_cli_json_rejects_unsafe_or_unapproved_report_paths_without_mutation(self):
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "vault"
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            cases = {
                str(root / "absolute.json"): root / "absolute.json",
                "../traversal.json": root / "traversal.json",
                "docs/superpowers/migrations/report.txt": reports / "report.txt",
                "outside-approved-directory.json": vault / "outside-approved-directory.json",
            }
            for argument, target in cases.items():
                with self.subTest(argument=argument):
                    target.write_text("sentinel", encoding="utf-8")
                    result = subprocess.run(
                        [
                            sys.executable,
                            "-m",
                            "Tools.second_brain.verify",
                            "--vault",
                            str(vault),
                            "--json",
                            argument,
                        ],
                        text=True,
                        capture_output=True,
                        check=False,
                    )
                    self.assertEqual(2, result.returncode)
                    self.assertEqual("sentinel", target.read_text(encoding="utf-8"))

    def test_json_output_path_rejects_ads_reserved_illegal_and_trailing_components(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            for filename in (
                "base:stream.json",
                "CON.json",
                "aux.notes.json",
                "COM¹.json",
                "LPT².json",
                "CONIN$.json",
                "CONOUT$.json",
                "CON .json",
                "COM1 .json",
                "report<copy>.json",
                "control\x01.json",
                "report.json ",
                "report.json.",
            ):
                with self.subTest(filename=filename):
                    with self.assertRaises(ValueError):
                        _json_output_path(vault, f"docs/superpowers/migrations/{filename}")
            self.assertEqual(
                reports / "유효한 보고서.json",
                _json_output_path(vault, "docs/superpowers/migrations/유효한 보고서.json"),
            )

    def test_json_output_path_rejects_a_simulated_junction_component(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            with patch.object(Path, "is_junction", return_value=True, create=True):
                with self.assertRaises(ValueError):
                    _json_output_path(vault, "docs/superpowers/migrations/report.json")

    def test_cli_json_does_not_write_a_replaced_report_destination(self):
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "vault"
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            original_report = reports / "report.json"
            original_report.write_text("original sentinel", encoding="utf-8")
            replacement = root / "outside-migrations"
            replacement.mkdir()
            outside_report = replacement / "report.json"
            outside_report.write_text("outside sentinel", encoding="utf-8")
            displaced = root / "approved-migrations"
            swap_succeeded = False

            def replace_report_parent(*args, **kwargs):
                nonlocal swap_succeeded
                try:
                    reports.rename(displaced)
                    replacement.rename(reports)
                except PermissionError:
                    return []
                swap_succeeded = True
                return []

            argv = [
                "verify",
                "--vault",
                str(vault),
                "--only",
                "Notes",
                "--json",
                "docs/superpowers/migrations/report.json",
            ]
            with patch.object(sys, "argv", argv):
                with patch("Tools.second_brain.verify.verify_vault", side_effect=replace_report_parent):
                    with redirect_stderr(StringIO()):
                        try:
                            return_code = verify_main()
                        except SystemExit as error:
                            return_code = error.code

            if swap_succeeded:
                self.assertEqual(2, return_code)
                self.assertEqual("original sentinel", (displaced / "report.json").read_text(encoding="utf-8"))
                self.assertEqual("outside sentinel", (reports / "report.json").read_text(encoding="utf-8"))
            else:
                self.assertIn(return_code, {0, 1})
                self.assertEqual("outside sentinel", outside_report.read_text(encoding="utf-8"))

    def test_cli_json_rechecks_open_file_identity_before_truncating(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            report = reports / "report.json"
            report.write_text("sentinel", encoding="utf-8")
            argv = [
                "verify",
                "--vault",
                str(vault),
                "--only",
                "Notes",
                "--json",
                "docs/superpowers/migrations/report.json",
            ]

            with patch.object(sys, "argv", argv):
                with patch("Tools.second_brain.verify.verify_vault", return_value=[]):
                    with patch("Tools.second_brain.verify._same_open_file", side_effect=[True, False]):
                        with redirect_stderr(StringIO()):
                            with self.assertRaises(SystemExit) as raised:
                                verify_main()

            self.assertEqual(2, raised.exception.code)
            self.assertEqual("sentinel", report.read_text(encoding="utf-8"))

    def test_cli_json_revalidates_transaction_before_writing_temp(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            report = reports / "report.json"
            report.write_bytes(b"existing final sentinel\n")
            captured = {}

            def capture_transaction(vault_path, value):
                transaction = _open_json_temp(vault_path, value)
                captured["transaction"] = transaction
                return transaction

            def simulate_external_move(*args, **kwargs):
                transaction = captured["transaction"]
                transaction.handle.write(b"moved external temp sentinel\n")
                transaction.handle.flush()
                transaction.parent_identity = (-1, -1)
                return []

            argv = [
                "verify",
                "--vault",
                str(vault),
                "--only",
                "Notes",
                "--json",
                "docs/superpowers/migrations/report.json",
            ]
            with patch.object(sys, "argv", argv):
                with patch("Tools.second_brain.verify._open_json_temp", side_effect=capture_transaction):
                    with patch("Tools.second_brain.verify.verify_vault", side_effect=simulate_external_move):
                        with patch("Tools.second_brain.verify._write_json_temp", wraps=_write_json_temp) as write_temp:
                            with redirect_stderr(StringIO()):
                                with self.assertRaises(SystemExit) as raised:
                                    verify_main()

            transaction = captured["transaction"]
            self.assertEqual(2, raised.exception.code)
            write_temp.assert_not_called()
            self.assertEqual(b"existing final sentinel\n", report.read_bytes())
            self.assertEqual(b"moved external temp sentinel\n", transaction.temporary.read_bytes())

    def test_cli_json_verify_exception_preserves_existing_and_absent_reports(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                with TemporaryDirectory() as temporary_directory:
                    vault = Path(temporary_directory)
                    reports = vault / "docs" / "superpowers" / "migrations"
                    reports.mkdir(parents=True)
                    report = reports / "report.json"
                    if existing:
                        report.write_bytes(b"existing sentinel\r\n")
                    argv = [
                        "verify",
                        "--vault",
                        str(vault),
                        "--only",
                        "Notes",
                        "--json",
                        "docs/superpowers/migrations/report.json",
                    ]

                    with patch.object(sys, "argv", argv):
                        with patch("Tools.second_brain.verify.verify_vault", side_effect=RuntimeError("verification failed")):
                            with self.assertRaisesRegex(RuntimeError, "verification failed"):
                                verify_main()

                    if existing:
                        self.assertEqual(b"existing sentinel\r\n", report.read_bytes())
                    else:
                        self.assertFalse(report.exists())
                    self.assertEqual([], list(reports.glob("*.tmp")))

    def test_cli_json_partial_write_failure_preserves_existing_report(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            report = reports / "report.json"
            report.write_bytes(b"existing sentinel\n")
            argv = [
                "verify",
                "--vault",
                str(vault),
                "--only",
                "Notes",
                "--json",
                "docs/superpowers/migrations/report.json",
            ]

            def partial_then_fail(handle, payload):
                handle.write(b"{\"partial\":")
                raise OSError("simulated short write")

            with patch.object(sys, "argv", argv):
                with patch("Tools.second_brain.verify.verify_vault", return_value=[]):
                    with patch(
                        "Tools.second_brain.verify._write_json_temp",
                        side_effect=partial_then_fail,
                        create=True,
                    ):
                        with redirect_stderr(StringIO()):
                            with self.assertRaises(SystemExit) as raised:
                                verify_main()

            self.assertEqual(2, raised.exception.code)
            self.assertEqual(b"existing sentinel\n", report.read_bytes())
            self.assertEqual([], list(reports.glob("*.tmp")))

    def test_cli_json_serialization_and_fsync_failures_preserve_existing_report(self):
        for failure in ("serialization", "fsync"):
            with self.subTest(failure=failure):
                with TemporaryDirectory() as temporary_directory:
                    vault = Path(temporary_directory)
                    reports = vault / "docs" / "superpowers" / "migrations"
                    reports.mkdir(parents=True)
                    report = reports / "report.json"
                    report.write_bytes(b"existing sentinel\n")
                    argv = [
                        "verify",
                        "--vault",
                        str(vault),
                        "--only",
                        "Notes",
                        "--json",
                        "docs/superpowers/migrations/report.json",
                    ]
                    failure_patch = (
                        patch("Tools.second_brain.verify.json.dumps", side_effect=TypeError("serialization failed"))
                        if failure == "serialization"
                        else patch("Tools.second_brain.verify.os.fsync", side_effect=OSError("fsync failed"))
                    )

                    with patch.object(sys, "argv", argv):
                        with patch("Tools.second_brain.verify.verify_vault", return_value=[]):
                            with failure_patch:
                                with redirect_stderr(StringIO()):
                                    if failure == "serialization":
                                        with self.assertRaisesRegex(TypeError, "serialization failed"):
                                            verify_main()
                                    else:
                                        with self.assertRaises(SystemExit) as raised:
                                            verify_main()
                                        self.assertEqual(2, raised.exception.code)

                    self.assertEqual(b"existing sentinel\n", report.read_bytes())
                    self.assertEqual([], list(reports.glob("*.tmp")))

    def test_cli_json_replace_failure_preserves_existing_and_absent_reports(self):
        for existing in (False, True):
            with self.subTest(existing=existing):
                with TemporaryDirectory() as temporary_directory:
                    vault = Path(temporary_directory)
                    reports = vault / "docs" / "superpowers" / "migrations"
                    reports.mkdir(parents=True)
                    report = reports / "report.json"
                    if existing:
                        report.write_bytes(b"existing sentinel\n")
                    argv = [
                        "verify",
                        "--vault",
                        str(vault),
                        "--only",
                        "Notes",
                        "--json",
                        "docs/superpowers/migrations/report.json",
                    ]

                    with patch.object(sys, "argv", argv):
                        with patch("Tools.second_brain.verify.verify_vault", return_value=[]):
                            with patch("Tools.second_brain.verify.os.replace", side_effect=OSError("replace failed")):
                                with redirect_stderr(StringIO()):
                                    with self.assertRaises(SystemExit) as raised:
                                        verify_main()

                    self.assertEqual(2, raised.exception.code)
                    if existing:
                        self.assertEqual(b"existing sentinel\n", report.read_bytes())
                    else:
                        self.assertFalse(report.exists())
                    self.assertEqual([], list(reports.glob("*.tmp")))

    def test_cli_json_atomically_replaces_an_existing_report(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            report = reports / "report.json"
            report.write_text("existing sentinel", encoding="utf-8")
            argv = [
                "verify",
                "--vault",
                str(vault),
                "--only",
                "Notes",
                "--json",
                "docs/superpowers/migrations/report.json",
            ]

            with patch.object(sys, "argv", argv):
                with patch("Tools.second_brain.verify.verify_vault", return_value=[]):
                    with patch("Tools.second_brain.verify.os.replace", wraps=os.replace) as replace:
                        return_code = verify_main()

            self.assertEqual(0, return_code)
            replace.assert_called_once()
            self.assertEqual("[]\n", report.read_text(encoding="utf-8"))
            self.assertEqual([], list(reports.glob("*.tmp")))

    def test_cli_json_rejects_symlinked_report_file_without_mutating_target(self):
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "vault"
            reports = vault / "docs" / "superpowers" / "migrations"
            reports.mkdir(parents=True)
            target = root / "outside.json"
            target.write_text("sentinel", encoding="utf-8")
            create_symlink_or_skip(reports / "report.json", target)

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "Tools.second_brain.verify",
                    "--vault",
                    str(vault),
                    "--json",
                    "docs/superpowers/migrations/report.json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(2, result.returncode)
            self.assertEqual("sentinel", target.read_text(encoding="utf-8"))

    def test_cli_json_rejects_symlinked_report_parent_without_mutating_target(self):
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "vault"
            (vault / "docs").mkdir(parents=True)
            outside_parent = root / "outside-superpowers"
            reports = outside_parent / "migrations"
            reports.mkdir(parents=True)
            target = reports / "report.json"
            target.write_text("sentinel", encoding="utf-8")
            create_symlink_or_skip(
                vault / "docs" / "superpowers",
                outside_parent,
                target_is_directory=True,
            )

            result = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "Tools.second_brain.verify",
                    "--vault",
                    str(vault),
                    "--json",
                    "docs/superpowers/migrations/report.json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(2, result.returncode)
            self.assertEqual("sentinel", target.read_text(encoding="utf-8"))

    def test_only_does_not_emit_unselected_note_parse_errors(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / "Other" / "bad.md").parent.mkdir(parents=True)
            (vault / "Other" / "bad.md").write_text("---\nbroken", encoding="utf-8")
            self.assertNotIn("missing-frontmatter", {x.code for x in verify_vault(vault, final=False, only="Selected")})

    def test_invalid_snapshot_is_reported_and_cli_json_has_exit_status(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            snapshot = vault / "bad.json"; snapshot.write_text("{", encoding="utf-8")
            self.assertIn("protected-settings-changed", {x.code for x in verify_vault(vault, final=False, obsidian_snapshot=snapshot)})
            result = subprocess.run([sys.executable, "-m", "Tools.second_brain.verify", "--vault", str(vault), "--json"], text=True, capture_output=True, check=False)
            self.assertEqual(1, result.returncode); self.assertIsInstance(json.loads(result.stdout), list)

    def test_cli_only_and_allow_staged_drafts_exit_zero(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            metadata = "id: '20260811000000-abcd'\ntype: source\nstatus: growing\ncreated: 2026-08-11\nupdated: 2026-08-11"
            write_note(vault / "Notes" / "한국어.md", metadata, "body")
            only = subprocess.run([sys.executable, "-m", "Tools.second_brain.verify", "--vault", str(vault), "--only", "Notes", "--json"], text=True, capture_output=True, check=False)
            self.assertEqual(0, only.returncode); self.assertEqual([], json.loads(only.stdout))
            write_note(vault / "00 인박스" / "승격 대기" / "draft.md", "type: permanent\nstatus: seed", "draft")
            staged = subprocess.run([sys.executable, "-m", "Tools.second_brain.verify", "--vault", str(vault), "--final", "--allow-staged-drafts", "--only", "00 인박스", "--json"], text=True, capture_output=True, check=False)
            self.assertEqual(0, staged.returncode); self.assertEqual([], json.loads(staged.stdout))

    def test_archive_guide_is_the_only_allowed_active_archive_link(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            guide = vault / ARCHIVE_GUIDE; write_note(guide, "", "guide")
            write_note(vault / "Active.md", VALID, f"[[{guide.stem}]]")
            self.assertNotIn("unresolved-link", {x.code for x in verify_vault(vault, final=False) if x.path == "Active.md"})


if __name__ == "__main__":
    unittest.main()
