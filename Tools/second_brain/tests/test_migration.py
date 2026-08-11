import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from Tools.second_brain.inventory import NoteRecord
from Tools.second_brain.migration import MigrationAction, apply_actions, build_actions, make_id
from Tools.second_brain.policy import MigrationPolicy


class MigrationTests(unittest.TestCase):
    def test_plan_command_is_a_dry_run_without_an_output_path(self):
        """A default plan write would violate dry-run safety and alter a vault unexpectedly."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("# old", encoding="utf-8")

            completed = subprocess.run(
                [sys.executable, "-m", "Tools.second_brain.migration", "plan", "--vault", str(vault)],
                capture_output=True, text=True, check=True,
            )

            self.assertIn('"source": "Old.md"', completed.stdout)
            self.assertTrue((vault / "Old.md").exists())
            self.assertFalse((vault / "migration-plan.json").exists())

    def test_plan_and_unconfirmed_apply_reject_unsafe_output_before_writing(self):
        """Validating output after writing could overwrite protected files without consent."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("# old", encoding="utf-8")
            protected = [".obsidian/core-plugins.json", ".obsidian/graph.json", ".obsidian/workspace.json"]
            for command in ("plan", "apply"):
                for output in protected:
                    with self.subTest(command=command, output=output):
                        completed = subprocess.run(
                            [sys.executable, "-m", "Tools.second_brain.migration", command, "--vault", str(vault), "--output", output],
                            capture_output=True, text=True,
                        )
                        self.assertNotEqual(completed.returncode, 0)
                        self.assertFalse((vault / output).exists())
            outside = vault.parent / f"{vault.name}-outside-plan.json"
            completed = subprocess.run(
                [sys.executable, "-m", "Tools.second_brain.migration", "plan", "--vault", str(vault), "--output", str(outside)],
                capture_output=True, text=True,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(outside.exists())

    def test_plan_preflights_actions_before_writing_an_explicit_output(self):
        """Writing a plan before collision detection would leave a partial dry-run mutation."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            source = vault / "Knowledge" / "Old.md"
            source.parent.mkdir()
            source.write_text("old", encoding="utf-8")
            policy = vault / "policy.json"
            policy.write_text(json.dumps({"archive_root": "Archive", "status_routes": {}, "path_routes": {}, "archive_fallback": True}), encoding="utf-8")
            archive = vault / "Archive" / "Knowledge" / "Old.md"
            archive.parent.mkdir(parents=True)
            archive.write_text("legacy", encoding="utf-8")
            output = vault / "plan.json"

            completed = subprocess.run(
                [sys.executable, "-m", "Tools.second_brain.migration", "plan", "--vault", str(vault), "--policy", str(policy), "--output", "plan.json"],
                capture_output=True, text=True,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())

    def test_plan_output_allows_only_a_new_audit_artifact(self):
        """Allowing arbitrary or existing output paths would let a dry run overwrite vault content."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            output = vault / "docs" / "superpowers" / "migrations" / "dry-run.json"
            command = [sys.executable, "-m", "Tools.second_brain.migration", "plan", "--vault", str(vault), "--output", "docs/superpowers/migrations/dry-run.json"]

            first = subprocess.run(command, capture_output=True, text=True)
            first_content = output.read_text(encoding="utf-8") if output.exists() else ""
            second = subprocess.run(command, capture_output=True, text=True)

            self.assertEqual(first.returncode, 0)
            self.assertIn('"source": "Old.md"', first_content)
            self.assertTrue((vault / "Old.md").exists())
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), first_content)

    def test_plan_output_rejects_the_audit_directory_root(self):
        """Writing a file at the audit directory root would block future migration evidence."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            audit_root = vault / "docs" / "superpowers" / "migrations"

            completed = subprocess.run(
                [sys.executable, "-m", "Tools.second_brain.migration", "plan", "--vault", str(vault), "--output", "docs/superpowers/migrations"],
                capture_output=True, text=True,
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(audit_root.exists())

    def test_plan_output_rejects_ordinary_existing_and_action_collision_paths(self):
        """An audit plan must never use a note, an existing artifact, or an action path as output."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            audit = vault / "docs" / "superpowers" / "migrations"
            audit.mkdir(parents=True)
            existing = audit / "existing.json"
            existing.write_text("evidence", encoding="utf-8")
            base = [sys.executable, "-m", "Tools.second_brain.migration", "plan", "--vault", str(vault), "--output"]

            ordinary = subprocess.run(base + ["Old.md"], capture_output=True, text=True)
            existing_run = subprocess.run(base + ["docs/superpowers/migrations/existing.json"], capture_output=True, text=True)
            target_policy = vault / "target-policy.json"
            target_policy.write_text(json.dumps({"archive_root": "Archive", "status_routes": {}, "path_routes": {"Old.md": {"target": "docs/superpowers/migrations/target.json"}}, "archive_fallback": True}), encoding="utf-8")
            target = subprocess.run(base + ["docs/superpowers/migrations/target.json", "--policy", str(target_policy)], capture_output=True, text=True)

            self.assertNotEqual(ordinary.returncode, 0)
            self.assertEqual((vault / "Old.md").read_text(encoding="utf-8"), "old")
            self.assertNotEqual(existing_run.returncode, 0)
            self.assertEqual(existing.read_text(encoding="utf-8"), "evidence")
            self.assertNotEqual(target.returncode, 0)
            self.assertFalse((audit / "target.json").exists())

    def test_rename_preserves_the_canonical_archive_while_updating_active_links(self):
        """Default rename traversal must not rewrite legacy Markdown under the canonical archive."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            (vault / "Active.md").write_text("[[Old]]", encoding="utf-8")
            archived = vault / "90 보관함" / "이전 LLM Wiki" / "Legacy.md"
            archived.parent.mkdir(parents=True)
            legacy = "Legacy [[Old]]\r\n"
            archived.write_bytes(legacy.encode("utf-8"))

            subprocess.run([sys.executable, "-m", "Tools.second_brain.migration", "rename", "--vault", str(vault), "--source", "Old.md", "--target", "New.md", "--alias", "Old", "--apply"], capture_output=True, text=True, check=True)

            self.assertEqual((vault / "Active.md").read_text(encoding="utf-8"), "[[New]]")
            self.assertEqual(archived.read_bytes(), legacy.encode("utf-8"))

    def test_rename_command_requires_apply_then_preserves_link_heading_and_alias(self):
        """A rename without consent or one that loses link suffixes would corrupt active notes."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("# old", encoding="utf-8")
            (vault / "Active.md").write_text("See [[Old#Heading|Alias]]", encoding="utf-8")
            base = [sys.executable, "-m", "Tools.second_brain.migration", "rename", "--vault", str(vault), "--source", "Old.md", "--target", "New.md", "--alias", "Old"]

            denied = subprocess.run(base, capture_output=True, text=True)
            self.assertNotEqual(denied.returncode, 0)
            self.assertTrue((vault / "Old.md").exists())
            subprocess.run(base + ["--apply"], capture_output=True, text=True, check=True)

            self.assertEqual((vault / "Active.md").read_text(encoding="utf-8"), "See [[New#Heading|Alias]]")

    def test_build_actions_archives_by_preserving_the_old_relative_path(self):
        """Flattening archives would make original paths and attachments impossible to recover."""
        policy = MigrationPolicy.load(Path(__file__).parents[1] / "migration-policy.json")
        actions = build_actions([NoteRecord("Knowledge/Old.md", "Old", {}, [])], policy)

        self.assertEqual(actions[0].action, "archive")
        self.assertEqual(actions[0].target, "90 蹂닿????댁쟾 LLM Wiki/Knowledge/Old.md")

    def test_apply_refuses_target_outside_vault_without_moving_source(self):
        """Skipping containment validation could overwrite files outside the user's vault."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "outside vault"):
                apply_actions(vault, [MigrationAction("Old.md", "../escape.md", "move", {})], {})

            self.assertTrue((vault / "Old.md").exists())

    def test_apply_never_allows_protected_obsidian_files_through_path_normalization(self):
        """A traversal-normalized protected target would silently alter user graph settings."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "protected Obsidian file"):
                apply_actions(vault, [MigrationAction("Old.md", "tmp/../.obsidian/graph.json", "move", {})], {})

            self.assertTrue((vault / "Old.md").exists())

    def test_apply_moves_sources_and_rewrites_active_note_links_after_success(self):
        """Deleting sources or dropping headings and aliases would make a migration irreversible."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("# old", encoding="utf-8")
            (vault / "Active.md").write_text("See [[Old#Heading|Alias]]", encoding="utf-8")

            apply_actions(vault, [MigrationAction("Old.md", "New.md", "move", {})], {"Old": "New"})

            self.assertFalse((vault / "Old.md").exists())
            self.assertEqual((vault / "New.md").read_text(encoding="utf-8"), "# old")
            self.assertEqual((vault / "Active.md").read_text(encoding="utf-8"), "See [[New#Heading|Alias]]")

    def test_apply_rejects_duplicate_targets_before_writing(self):
        """Late collision detection could partially move a vault."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "A.md").write_text("A", encoding="utf-8")
            (vault / "B.md").write_text("B", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "duplicate target"):
                apply_actions(vault, [
                    MigrationAction("A.md", "New.md", "move", {}),
                    MigrationAction("B.md", "New.md", "move", {}),
                ], {})

            self.assertTrue((vault / "A.md").exists())
            self.assertTrue((vault / "B.md").exists())

    def test_apply_rejects_duplicate_resolved_sources_before_writing(self):
        """Moving the same resolved source twice would leave a partial migration behind."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "duplicate source"):
                apply_actions(vault, [
                    MigrationAction("Old.md", "First.md", "move", {}),
                    MigrationAction("nested/../Old.md", "Second.md", "move", {}),
                ], {})

            self.assertTrue((vault / "Old.md").exists())
            self.assertFalse((vault / "First.md").exists())

    def test_apply_rewrites_mapped_note_embeds_but_keeps_attachment_embeds(self):
        """Treating embeds as ordinary links would either miss note renames or alter attachments."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            (vault / "Active.md").write_text("![[Old#Heading|Alias]] ![[diagram.png]]", encoding="utf-8")

            apply_actions(vault, [MigrationAction("Old.md", "New.md", "move", {})], {"Old": "New"})

            self.assertEqual((vault / "Active.md").read_text(encoding="utf-8"), "![[New#Heading|Alias]] ![[diagram.png]]")

    def test_apply_leaves_preexisting_archived_markdown_byte_preserved(self):
        """Rewriting legacy archive links would destroy the archive's preservation guarantee."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            archived = vault / "Archive" / "Legacy.md"
            archived.parent.mkdir()
            legacy = "Legacy [[Old]] ![[Old#Heading|Alias]]\r\n"
            archived.write_bytes(legacy.encode("utf-8"))

            apply_actions(vault, [MigrationAction("Old.md", "New.md", "move", {})], {"Old": "New"}, archive_root="Archive")

            self.assertEqual(archived.read_bytes(), legacy.encode("utf-8"))

    def test_make_id_uses_created_day_and_old_path_hash(self):
        """An unstable identifier would break reversible migration evidence."""
        self.assertEqual(make_id("Knowledge/Old.md", "2026-08-11"), "20260811000000-8ec1")


if __name__ == "__main__":
    unittest.main()
