import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from Tools.second_brain.verify import verify_vault


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
        self.assertIn("invalid-source-quality", self.issues_for(VALID.replace("source_quality: primary", "source_quality: personal")))

    def test_reports_links_markers_and_stale_sources(self):
        self.assertIn("unresolved-link", self.issues_for(VALID, "[[Missing]]"))
        self.assertIn("legacy-llm-marker", self.issues_for(VALID, "llm_wiki"))
        self.assertIn("stale-source-path", self.issues_for(VALID + "\nsource_path: missing", "[[Target]]"))

    def test_archive_legacy_markers_and_links_do_not_fail(self):
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            write_note(vault / "90 보관함" / "old.md", "", "llm_wiki [[Missing]]")
            self.assertEqual([], verify_vault(vault, final=False))

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
            self.assertEqual("missing-frontmatter", issues[0].code)


if __name__ == "__main__":
    unittest.main()
