import errno
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from Tools.second_brain.inventory import NoteRecord
from Tools.second_brain.migration import MigrationAction, apply_actions, build_actions, make_id
from Tools.second_brain.policy import MigrationPolicy


def _run_migration(vault: Path, *arguments: str, **options):
    environment = os.environ.copy()
    repository_root = str(Path(__file__).resolve().parents[3])
    existing_pythonpath = environment.get("PYTHONPATH")
    environment["PYTHONPATH"] = (
        os.pathsep.join((repository_root, existing_pythonpath))
        if existing_pythonpath
        else repository_root
    )
    return subprocess.run(
        [sys.executable, "-m", "Tools.second_brain.migration", *arguments],
        cwd=vault,
        env=environment,
        capture_output=True,
        text=True,
        **options,
    )


def _create_symlink_or_skip(link: Path, target: Path) -> None:
    try:
        link.symlink_to(target)
    except OSError as error:
        if getattr(error, "winerror", None) == 1314 or error.errno in {
            errno.EACCES,
            errno.EPERM,
        }:
            raise unittest.SkipTest(
                f"symbolic-link creation is unavailable on this host: {error}"
            ) from error
        raise


def _write_policy(
    vault: Path,
    *,
    path_routes: dict[str, dict[str, object]] | None = None,
    archive_root: str = "Archive",
) -> Path:
    policy = vault / "policy.json"
    policy.write_text(
        json.dumps(
            {
                "archive_root": archive_root,
                "status_routes": {},
                "path_routes": path_routes or {},
                "archive_fallback": True,
            }
        ),
        encoding="utf-8",
    )
    return policy


def _write_plan(vault: Path, actions: object, name: str = "reviewed.json") -> Path:
    plan = vault / "docs" / "superpowers" / "migrations" / name
    plan.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(actions, str):
        plan.write_text(actions, encoding="utf-8")
    else:
        plan.write_text(json.dumps(actions), encoding="utf-8")
    return plan


class MigrationTests(unittest.TestCase):
    def test_migration_cli_helper_isolates_cwd_and_preserves_pythonpath(self):
        """Repository-CWD execution or a replaced environment could corrupt files or break imports."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            helper = globals().get("_run_migration")
            self.assertTrue(callable(helper), "migration CLI helper is missing")

            with patch.dict(os.environ, {"PYTHONPATH": "existing-path", "PRESERVED": "yes"}, clear=True):
                with patch.object(subprocess, "run", return_value=subprocess.CompletedProcess([], 0)) as run:
                    helper(vault, "plan", "--vault", str(vault), "--source", ".")

            command = run.call_args.args[0]
            options = run.call_args.kwargs
            repository_root = str(Path(__file__).resolve().parents[3])
            self.assertEqual(
                command,
                [
                    sys.executable,
                    "-m",
                    "Tools.second_brain.migration",
                    "plan",
                    "--vault",
                    str(vault),
                    "--source",
                    ".",
                ],
            )
            self.assertEqual(options["cwd"], vault)
            self.assertEqual(options["env"]["PRESERVED"], "yes")
            self.assertEqual(options["env"]["PYTHONPATH"], os.pathsep.join((repository_root, "existing-path")))

    def test_symlink_creation_helper_reraises_unrelated_errors(self):
        """Skipping unrelated creation failures would hide a broken real-symlink regression."""
        helper = globals().get("_create_symlink_or_skip")
        self.assertTrue(callable(helper), "symlink creation helper is missing")
        errors = (
            OSError(errno.ENOSPC, "disk full"),
            NotImplementedError("unexpected unsupported operation"),
        )
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            for error in errors:
                with self.subTest(error=type(error).__name__):
                    with patch.object(Path, "symlink_to", side_effect=error):
                        with self.assertRaises(type(error)) as raised:
                            helper(vault / "Alias.md", Path("policy.json"))

                    self.assertIs(raised.exception, error)

    def test_symlink_creation_helper_skips_only_recognized_privilege_errors(self):
        """Known link privilege failures should be the only errors converted to a skip."""
        helper = globals().get("_create_symlink_or_skip")
        self.assertTrue(callable(helper), "symlink creation helper is missing")
        windows_privilege_error = OSError(errno.EIO, "symbolic-link privilege unavailable")
        windows_privilege_error.winerror = 1314
        errors = (
            windows_privilege_error,
            PermissionError(errno.EACCES, "permission denied"),
            PermissionError(errno.EPERM, "operation not permitted"),
        )
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            for error in errors:
                with self.subTest(error=str(error)):
                    with patch.object(Path, "symlink_to", side_effect=error):
                        with self.assertRaisesRegex(
                            unittest.SkipTest,
                            "symbolic-link creation is unavailable on this host",
                        ):
                            helper(vault / "Alias.md", Path("policy.json"))

    def test_plan_command_is_a_dry_run_without_an_output_path(self):
        """A default plan write would violate dry-run safety and alter a vault unexpectedly."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("# old", encoding="utf-8")

            completed = _run_migration(
                vault, "plan", "--vault", str(vault), "--source", ".", check=True
            )

            self.assertIn('"source": "Old.md"', completed.stdout)
            self.assertTrue((vault / "Old.md").exists())
            self.assertFalse((vault / "migration-plan.json").exists())

    def test_plan_rejects_unsafe_output_before_writing(self):
        """Validating output after writing could overwrite protected files without consent."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("# old", encoding="utf-8")
            protected = [".obsidian/core-plugins.json", ".obsidian/graph.json", ".obsidian/workspace.json"]
            for output in protected:
                with self.subTest(output=output):
                    completed = _run_migration(
                        vault,
                        "plan",
                        "--vault",
                        str(vault),
                        "--source",
                        ".",
                        "--output",
                        output,
                    )
                    self.assertNotEqual(completed.returncode, 0)
                    self.assertFalse((vault / output).exists())
            outside = vault.parent / f"{vault.name}-outside-plan.json"
            completed = _run_migration(
                vault,
                "plan",
                "--vault",
                str(vault),
                "--source",
                ".",
                "--output",
                str(outside),
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
            output = vault / "docs" / "superpowers" / "migrations" / "plan.json"

            completed = _run_migration(
                vault,
                "plan",
                "--vault",
                str(vault),
                "--source",
                "Knowledge",
                "--policy",
                str(policy),
                "--output",
                output.relative_to(vault).as_posix(),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertFalse(output.exists())

    def test_plan_output_allows_only_a_new_audit_artifact(self):
        """Allowing arbitrary or existing output paths would let a dry run overwrite vault content."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            output = vault / "docs" / "superpowers" / "migrations" / "dry-run.json"
            command = [
                "plan",
                "--vault",
                str(vault),
                "--source",
                ".",
                "--output",
                "docs/superpowers/migrations/dry-run.json",
            ]

            first = _run_migration(vault, *command)
            first_content = output.read_text(encoding="utf-8") if output.exists() else ""
            second = _run_migration(vault, *command)

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

            completed = _run_migration(
                vault,
                "plan",
                "--vault",
                str(vault),
                "--source",
                ".",
                "--output",
                "docs/superpowers/migrations",
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
            base = ["plan", "--vault", str(vault), "--source", ".", "--output"]

            ordinary = _run_migration(vault, *(base + ["Old.md"]))
            existing_run = _run_migration(vault, *(base + ["docs/superpowers/migrations/existing.json"]))
            target_policy = vault / "target-policy.json"
            target_policy.write_text(json.dumps({"archive_root": "Archive", "status_routes": {}, "path_routes": {"Old.md": {"target": "docs/superpowers/migrations/target.json"}}, "archive_fallback": True}), encoding="utf-8")
            target = _run_migration(
                vault, *(base + ["docs/superpowers/migrations/target.json", "--policy", str(target_policy)])
            )

            self.assertNotEqual(ordinary.returncode, 0)
            self.assertEqual((vault / "Old.md").read_text(encoding="utf-8"), "old")
            self.assertNotEqual(existing_run.returncode, 0)
            self.assertEqual(existing.read_text(encoding="utf-8"), "evidence")
            self.assertNotEqual(target.returncode, 0)
            self.assertFalse((audit / "target.json").exists())

    def test_plan_exact_interface_scopes_source_preserves_prefix_and_summarizes_deterministically(self):
        """Scanning the whole vault or stripping the source prefix would produce an unreviewable plan."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            knowledge = vault / "Knowledge"
            knowledge.mkdir()
            (knowledge / "Archive.md").write_text("archive", encoding="utf-8")
            (knowledge / "Move.md").write_text("move", encoding="utf-8")
            (knowledge / "ignore.txt").write_text("not a note", encoding="utf-8")
            (vault / "Outside.md").write_text("outside", encoding="utf-8")
            policy = _write_policy(
                vault,
                path_routes={
                    "Knowledge/Move.md": {
                        "target": "Active/Moved.md",
                        "type": "source",
                    }
                },
            )
            first_output = "docs/superpowers/migrations/first.json"
            second_output = "docs/superpowers/migrations/second.json"
            base = [
                "plan",
                "--vault",
                ".",
                "--source",
                "Knowledge",
                "--policy",
                str(policy),
                "--output",
            ]

            first = _run_migration(vault, *(base + [first_output]))
            second = _run_migration(vault, *(base + [second_output]))

            expected_summary = (
                "total=2\n"
                "promote_or_stage=1\n"
                "archive=1\n"
                "delete=0\n"
                "duplicate_targets=0\n"
                "outside_vault_targets=0\n"
            )
            expected_actions = [
                {
                    "source": "Knowledge/Archive.md",
                    "target": "Archive/Knowledge/Archive.md",
                    "action": "archive",
                    "metadata": {},
                },
                {
                    "source": "Knowledge/Move.md",
                    "target": "Active/Moved.md",
                    "action": "move",
                    "metadata": {"type": "source"},
                },
            ]
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first.stdout, expected_summary)
            self.assertEqual(second.stdout, expected_summary)
            first_plan = (vault / first_output).read_text(encoding="utf-8")
            second_plan = (vault / second_output).read_text(encoding="utf-8")
            self.assertEqual(first_plan, second_plan)
            self.assertEqual(json.loads(first_plan), expected_actions)
            self.assertTrue((knowledge / "Archive.md").exists())
            self.assertTrue((knowledge / "Move.md").exists())
            self.assertTrue((vault / "Outside.md").exists())

    def test_plan_rejects_non_relative_outside_protected_missing_and_non_directory_sources(self):
        """Accepting an unsafe source could inventory content outside the reviewed vault subtree."""
        cases = (
            ("absolute", "source must be vault-relative"),
            ("../outside", "source is outside vault"),
            (".obsidian", "source is protected"),
            ("Missing", "source does not exist"),
            ("Knowledge/Old.md", "source is not a directory"),
        )
        for source_case, expected_error in cases:
            with self.subTest(source=source_case), TemporaryDirectory() as directory:
                workspace = Path(directory)
                vault = workspace / "vault"
                knowledge = vault / "Knowledge"
                knowledge.mkdir(parents=True)
                (knowledge / "Old.md").write_text("old", encoding="utf-8")
                outside = workspace / "outside"
                outside.mkdir()
                (outside / "Outside.md").write_text("outside", encoding="utf-8")
                obsidian = vault / ".obsidian"
                obsidian.mkdir()
                (obsidian / "Private.md").write_text("private", encoding="utf-8")
                policy = _write_policy(vault)
                source = str(knowledge.resolve()) if source_case == "absolute" else source_case
                output = vault / "docs" / "superpowers" / "migrations" / "plan.json"

                completed = _run_migration(
                    vault,
                    "plan",
                    "--vault",
                    ".",
                    "--source",
                    source,
                    "--policy",
                    str(policy),
                    "--output",
                    output.relative_to(vault).as_posix(),
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)
                self.assertFalse(output.exists())

    def test_apply_exact_interface_uses_reviewed_plan_without_rescanning_or_mutating_it(self):
        """Rebuilding at apply time could move unreviewed notes or ignore reviewed targets."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            knowledge = vault / "Knowledge"
            knowledge.mkdir()
            (knowledge / "Old.md").write_text("old", encoding="utf-8")
            legacy = b"Legacy [[Old]]\r\n"
            (knowledge / "Legacy.md").write_bytes(legacy)
            (vault / "Active.md").write_text("See [[Old]]", encoding="utf-8")
            policy = _write_policy(
                vault,
                path_routes={"Knowledge/Old.md": {"target": "Active/New.md"}},
            )
            plan_argument = "docs/superpowers/migrations/reviewed.json"
            planned = _run_migration(
                vault,
                "plan",
                "--vault",
                ".",
                "--source",
                "Knowledge",
                "--policy",
                str(policy),
                "--output",
                plan_argument,
            )
            self.assertEqual(planned.returncode, 0, planned.stderr)
            plan = vault / plan_argument
            reviewed_bytes = plan.read_bytes()
            _write_policy(
                vault,
                path_routes={"Knowledge/Old.md": {"target": "Hijacked.md"}},
            )
            (knowledge / "Later.md").write_text("later", encoding="utf-8")

            applied = _run_migration(
                vault,
                "apply",
                "--vault",
                ".",
                "--plan",
                plan_argument,
                "--apply",
            )

            self.assertEqual(applied.returncode, 0, applied.stderr)
            self.assertFalse((knowledge / "Old.md").exists())
            self.assertEqual((vault / "Active" / "New.md").read_text(encoding="utf-8"), "old")
            self.assertFalse((knowledge / "Legacy.md").exists())
            self.assertEqual(
                (vault / "Archive" / "Knowledge" / "Legacy.md").read_bytes(),
                legacy,
            )
            self.assertFalse((vault / "Hijacked.md").exists())
            self.assertEqual((knowledge / "Later.md").read_text(encoding="utf-8"), "later")
            self.assertFalse((vault / "Archive" / "Knowledge" / "Later.md").exists())
            self.assertEqual((vault / "Active.md").read_text(encoding="utf-8"), "See [[New]]")
            self.assertEqual(plan.read_bytes(), reviewed_bytes)

    def test_apply_rejects_archive_targets_that_do_not_preserve_the_source_path(self):
        """A tampered archive action must not flatten a note or derive a vault-wide exclusion."""
        for target_case in ("flattened", "normalized_source"):
            with self.subTest(target=target_case), TemporaryDirectory() as directory:
                vault = Path(directory)
                (vault / "A.md").write_text("A", encoding="utf-8")
                legacy = b"B [[A]]\r\n"
                (vault / "B.md").write_bytes(legacy)
                (vault / "Active.md").write_text("[[A]]", encoding="utf-8")
                target = (
                    "Active/Flattened.md"
                    if target_case == "flattened"
                    else f"../{vault.name}/B.md"
                )
                plan = _write_plan(
                    vault,
                    [
                        {"source": "A.md", "target": "New.md", "action": "move", "metadata": {}},
                        {"source": "B.md", "target": target, "action": "archive", "metadata": {}},
                    ],
                )

                completed = _run_migration(
                    vault,
                    "apply",
                    "--vault",
                    ".",
                    "--plan",
                    plan.relative_to(vault).as_posix(),
                    "--apply",
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn("archive target must preserve source relative path", completed.stderr)
                self.assertEqual((vault / "A.md").read_text(encoding="utf-8"), "A")
                self.assertFalse((vault / "New.md").exists())
                self.assertEqual((vault / "B.md").read_bytes(), legacy)
                self.assertEqual((vault / "Active.md").read_text(encoding="utf-8"), "[[A]]")

    def test_apply_requires_confirmation_before_loading_or_moving_a_reviewed_plan(self):
        """An apply command without explicit confirmation must never mutate the vault."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("old", encoding="utf-8")
            plan = _write_plan(
                vault,
                [{"source": "Old.md", "target": "New.md", "action": "move", "metadata": {}}],
            )
            reviewed_bytes = plan.read_bytes()

            completed = _run_migration(
                vault,
                "apply",
                "--vault",
                ".",
                "--plan",
                plan.relative_to(vault).as_posix(),
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("apply requires --apply", completed.stderr)
            self.assertEqual((vault / "Old.md").read_text(encoding="utf-8"), "old")
            self.assertFalse((vault / "New.md").exists())
            self.assertEqual(plan.read_bytes(), reviewed_bytes)

    def test_apply_restricts_plan_input_to_an_existing_regular_json_audit_file(self):
        """Loading a plan from an unreviewed location or non-file path would bypass audit safety."""
        cases = (
            ("outside", "plan must be under docs/superpowers/migrations"),
            ("non_json", "plan must be a JSON file"),
            ("directory", "plan is not a regular file"),
            ("missing", "plan does not exist"),
        )
        for plan_case, expected_error in cases:
            with self.subTest(plan=plan_case), TemporaryDirectory() as directory:
                workspace = Path(directory)
                vault = workspace / "vault"
                vault.mkdir()
                (vault / "Old.md").write_text("old", encoding="utf-8")
                action = [{"source": "Old.md", "target": "New.md", "action": "move", "metadata": {}}]
                if plan_case == "outside":
                    plan = workspace / "outside.json"
                    plan.write_text(json.dumps(action), encoding="utf-8")
                elif plan_case == "non_json":
                    plan = _write_plan(vault, action, "reviewed.txt")
                elif plan_case == "directory":
                    plan = vault / "docs" / "superpowers" / "migrations" / "directory.json"
                    plan.mkdir(parents=True)
                else:
                    plan = vault / "docs" / "superpowers" / "migrations" / "missing.json"

                completed = _run_migration(
                    vault,
                    "apply",
                    "--vault",
                    ".",
                    "--plan",
                    str(plan),
                    "--apply",
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)
                self.assertEqual((vault / "Old.md").read_text(encoding="utf-8"), "old")
                self.assertFalse((vault / "New.md").exists())

    def test_apply_rejects_malformed_or_non_list_plan_json_without_mutation(self):
        """Lenient JSON parsing could execute a plan that was not the reviewed action list."""
        cases = (
            ("{", "invalid plan JSON"),
            ("{}", "plan must contain a JSON list"),
            ("[NaN]", "invalid plan JSON"),
        )
        for plan_text, expected_error in cases:
            with self.subTest(plan=plan_text), TemporaryDirectory() as directory:
                vault = Path(directory)
                (vault / "Old.md").write_text("old", encoding="utf-8")
                plan = _write_plan(vault, plan_text)

                completed = _run_migration(
                    vault,
                    "apply",
                    "--vault",
                    ".",
                    "--plan",
                    plan.relative_to(vault).as_posix(),
                    "--apply",
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)
                self.assertEqual((vault / "Old.md").read_text(encoding="utf-8"), "old")
                self.assertFalse((vault / "New.md").exists())

    def test_apply_rejects_unknown_missing_duplicate_or_invalid_action_fields_without_mutation(self):
        """A plan action whose schema differs from MigrationAction must never be executed."""
        valid = {"source": "Old.md", "target": "New.md", "action": "move", "metadata": {}}
        cases = (
            (json.dumps([{key: value for key, value in valid.items() if key != "metadata"}]), "missing fields: metadata"),
            (json.dumps([{**valid, "unexpected": True}]), "unknown fields: unexpected"),
            ('[{"source":"Old.md","source":"Other.md","target":"New.md","action":"move","metadata":{}}]', "duplicate JSON object field: source"),
            (json.dumps([{**valid, "source": 1}]), "source must be a non-empty string"),
            (json.dumps([{**valid, "target": ""}]), "target must be a non-empty string"),
            (json.dumps([{**valid, "metadata": []}]), "metadata must be an object"),
            (json.dumps([{**valid, "action": "delete"}]), "unsupported action type: delete"),
        )
        for plan_text, expected_error in cases:
            with self.subTest(error=expected_error), TemporaryDirectory() as directory:
                vault = Path(directory)
                (vault / "Old.md").write_text("old", encoding="utf-8")
                plan = _write_plan(vault, plan_text)

                completed = _run_migration(
                    vault,
                    "apply",
                    "--vault",
                    ".",
                    "--plan",
                    plan.relative_to(vault).as_posix(),
                    "--apply",
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)
                self.assertEqual((vault / "Old.md").read_text(encoding="utf-8"), "old")
                self.assertFalse((vault / "New.md").exists())

    def test_apply_rejects_tampered_non_markdown_action_paths_without_mutation(self):
        """A reviewed note plan must not be repurposed to move arbitrary vault files."""
        cases = (
            ("policy.json", "Moved.json", "source must be a Markdown path"),
            ("Old.md", "Moved.json", "target must be a Markdown path"),
        )
        for source, target, expected_error in cases:
            with self.subTest(source=source, target=target), TemporaryDirectory() as directory:
                vault = Path(directory)
                source_path = vault / source
                source_path.write_text("source", encoding="utf-8")
                plan = _write_plan(
                    vault,
                    [{"source": source, "target": target, "action": "move", "metadata": {}}],
                )

                completed = _run_migration(
                    vault,
                    "apply",
                    "--vault",
                    ".",
                    "--plan",
                    plan.relative_to(vault).as_posix(),
                    "--apply",
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)
                self.assertEqual(source_path.read_text(encoding="utf-8"), "source")
                self.assertFalse((vault / target).exists())

    def test_apply_rejects_each_lexical_symlink_component_before_any_move(self):
        """Missing any source or target component check could execute an aliased reviewed path."""
        cases = (
            ("source leaf", "B.md", "Second.md", "source", "B.md"),
            ("source parent", "Source/B.md", "Second.md", "source", "Source"),
            ("target leaf", "B.md", "Target.md", "target", "Target.md"),
            ("target parent", "B.md", "Target/B.md", "target", "Target"),
        )
        for name, source, target, role, reported_component in cases:
            with self.subTest(component=name), TemporaryDirectory() as directory:
                vault = Path(directory)
                (vault / "A.md").write_text("A", encoding="utf-8")
                source_path = vault / source
                source_path.parent.mkdir(parents=True, exist_ok=True)
                source_path.write_text("B", encoding="utf-8")
                target_path = vault / target
                if name == "target parent":
                    target_path.parent.mkdir(parents=True)
                symlink_component = vault / reported_component

                with patch.object(
                    Path,
                    "is_symlink",
                    new=lambda candidate: candidate == symlink_component,
                ):
                    with self.assertRaisesRegex(
                        ValueError,
                        f"{role} path contains a symbolic link",
                    ):
                        apply_actions(
                            vault,
                            [
                                MigrationAction("A.md", "First.md", "move", {}),
                                MigrationAction(source, target, "move", {}),
                            ],
                            {},
                        )

                self.assertEqual((vault / "A.md").read_text(encoding="utf-8"), "A")
                self.assertEqual(source_path.read_text(encoding="utf-8"), "B")
                self.assertFalse((vault / "First.md").exists())
                self.assertFalse(target_path.exists())

    def test_apply_rejects_a_non_markdown_resolved_source_before_any_move(self):
        """Checking only the reviewed suffix could move a non-Markdown canonical source."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            policy = vault / "policy.json"
            policy_bytes = b'{"protected": true}\n'
            policy.write_bytes(policy_bytes)
            real_resolve = Path.resolve

            def resolve_alias(candidate: Path, *args, **kwargs) -> Path:
                if candidate == vault / "Alias.md":
                    return policy
                return real_resolve(candidate, *args, **kwargs)

            with patch.object(Path, "resolve", new=resolve_alias):
                with self.assertRaisesRegex(
                    ValueError,
                    "resolved source must be a Markdown file",
                ):
                    apply_actions(
                        vault,
                        [MigrationAction("Alias.md", "Moved.md", "move", {})],
                        {},
                    )

            self.assertEqual(policy.read_bytes(), policy_bytes)
            self.assertFalse((vault / "Moved.md").exists())

    def test_apply_cli_rejects_a_real_source_symlink_without_touching_link_or_target(self):
        """Resolving a reviewed .md symlink could move its non-Markdown target and earlier actions."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "A.md").write_text("A", encoding="utf-8")
            policy = vault / "policy.json"
            policy_bytes = b'{"protected": true}\n'
            policy.write_bytes(policy_bytes)
            alias = vault / "Alias.md"
            _create_symlink_or_skip(alias, Path("policy.json"))
            plan = _write_plan(
                vault,
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "Alias.md", "target": "Moved.md", "action": "move", "metadata": {}},
                ],
            )

            completed = _run_migration(
                vault,
                "apply",
                "--vault",
                ".",
                "--plan",
                plan.relative_to(vault).as_posix(),
                "--apply",
            )

            self.assertNotEqual(completed.returncode, 0)
            self.assertIn("source path contains a symbolic link", completed.stderr)
            self.assertEqual((vault / "A.md").read_text(encoding="utf-8"), "A")
            self.assertFalse((vault / "First.md").exists())
            self.assertTrue(alias.is_symlink())
            self.assertEqual(alias.readlink(), Path("policy.json"))
            self.assertEqual(policy.read_bytes(), policy_bytes)
            self.assertFalse((vault / "Moved.md").exists())

    def test_apply_preflights_all_loaded_actions_before_any_move(self):
        """A late duplicate, missing file, collision, or unsafe path must not allow a partial migration."""
        cases = (
            (
                "duplicate target",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "B.md", "target": "nested/../First.md", "action": "move", "metadata": {}},
                ],
            ),
            (
                "duplicate source",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "nested/../A.md", "target": "Second.md", "action": "move", "metadata": {}},
                ],
            ),
            (
                "source does not exist",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "Missing.md", "target": "Second.md", "action": "move", "metadata": {}},
                ],
            ),
            (
                "target already exists",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "B.md", "target": "Existing.md", "action": "move", "metadata": {}},
                ],
            ),
            (
                "target parent is not a directory",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "B.md", "target": "Blocker/Second.md", "action": "move", "metadata": {}},
                ],
            ),
            (
                "target conflicts with another target parent",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "B.md", "target": "First.md/Second.md", "action": "move", "metadata": {}},
                ],
            ),
            (
                "outside vault",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "B.md", "target": "../Escape.md", "action": "move", "metadata": {}},
                ],
            ),
            (
                "protected Obsidian file",
                [
                    {"source": "A.md", "target": "First.md", "action": "move", "metadata": {}},
                    {"source": "B.md", "target": "tmp/../.obsidian/graph.json", "action": "move", "metadata": {}},
                ],
            ),
        )
        for expected_error, actions in cases:
            with self.subTest(error=expected_error), TemporaryDirectory() as directory:
                vault = Path(directory)
                (vault / "A.md").write_text("A", encoding="utf-8")
                (vault / "B.md").write_text("B", encoding="utf-8")
                (vault / "Existing.md").write_text("existing", encoding="utf-8")
                (vault / "Blocker").write_text("blocker", encoding="utf-8")
                plan = _write_plan(vault, actions)

                completed = _run_migration(
                    vault,
                    "apply",
                    "--vault",
                    ".",
                    "--plan",
                    plan.relative_to(vault).as_posix(),
                    "--apply",
                )

                self.assertNotEqual(completed.returncode, 0)
                self.assertIn(expected_error, completed.stderr)
                self.assertEqual((vault / "A.md").read_text(encoding="utf-8"), "A")
                self.assertEqual((vault / "B.md").read_text(encoding="utf-8"), "B")
                self.assertFalse((vault / "First.md").exists())
                self.assertFalse((vault / "Second.md").exists())

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

            _run_migration(
                vault,
                "rename",
                "--vault",
                str(vault),
                "--source",
                "Old.md",
                "--target",
                "New.md",
                "--alias",
                "Old",
                "--apply",
                check=True,
            )

            self.assertEqual((vault / "Active.md").read_text(encoding="utf-8"), "[[New]]")
            self.assertEqual(archived.read_bytes(), legacy.encode("utf-8"))

    def test_rename_command_requires_apply_then_preserves_link_heading_and_alias(self):
        """A rename without consent or one that loses link suffixes would corrupt active notes."""
        with TemporaryDirectory() as directory:
            vault = Path(directory)
            (vault / "Old.md").write_text("# old", encoding="utf-8")
            (vault / "Active.md").write_text("See [[Old#Heading|Alias]]", encoding="utf-8")
            base = ["rename", "--vault", str(vault), "--source", "Old.md", "--target", "New.md", "--alias", "Old"]

            denied = _run_migration(vault, *base)
            self.assertNotEqual(denied.returncode, 0)
            self.assertTrue((vault / "Old.md").exists())
            _run_migration(vault, *(base + ["--apply"]), check=True)

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
