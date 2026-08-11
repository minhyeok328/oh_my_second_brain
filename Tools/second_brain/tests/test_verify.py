import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from Tools.second_brain.verify import ARCHIVE_GUIDE, ARCHIVE_ROOT, TEMPLATE_FILES, TEMPLATE_ROOT, verify_vault


def write_note(path: Path, metadata: str, body: str = "[[Target]]") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"---\n{metadata}\n---\n{body}\n", encoding="utf-8")


VALID = """id: '20260811000000-abcd'
type: permanent
status: growing
created: 2026-08-11
updated: 2026-08-11
source_quality: primary
verified: true
sources:
  - source"""


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
