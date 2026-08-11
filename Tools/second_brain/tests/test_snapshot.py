import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from Tools.second_brain.snapshot import hash_files, snapshot_tree


class SnapshotTests(unittest.TestCase):
    def test_snapshot_tree_changes_when_a_tracked_file_changes(self):
        """Ignoring size or modification time would miss a source-file mutation."""
        with TemporaryDirectory() as temporary_directory:
            source_root = Path(temporary_directory)
            note = source_root / "note.txt"
            note.write_text("original", encoding="utf-8")
            before = snapshot_tree(source_root)

            note.write_text("changed content", encoding="utf-8")
            after = snapshot_tree(source_root)

            self.assertNotEqual(before, after)

    def test_snapshot_tree_uses_relative_posix_paths_and_excludes_generated_directories(self):
        """Including cache/build files would produce noisy and platform-dependent baselines."""
        with TemporaryDirectory() as temporary_directory:
            source_root = Path(temporary_directory)
            (source_root / "nested").mkdir()
            (source_root / "nested" / "note.txt").write_text("note", encoding="utf-8")
            (source_root / "node_modules").mkdir()
            (source_root / "node_modules" / "cache.js").write_text("cache", encoding="utf-8")
            (source_root / "build").mkdir()
            (source_root / "build" / "output.txt").write_text("output", encoding="utf-8")

            snapshot = snapshot_tree(source_root)

            self.assertEqual([entry["path"] for entry in snapshot], ["nested/note.txt"])
            self.assertEqual(set(snapshot[0]), {"path", "size", "st_mtime_ns"})

    def test_hash_files_returns_sha256_for_each_requested_path(self):
        """A non-content hash would fail to protect existing Obsidian settings."""
        with TemporaryDirectory() as temporary_directory:
            settings_file = Path(temporary_directory) / "settings.json"
            settings_file.write_bytes(b"{}\n")

            hashes = hash_files([settings_file])

            self.assertEqual(
                hashes[str(settings_file)], hashlib.sha256(b"{}\n").hexdigest()
            )


if __name__ == "__main__":
    unittest.main()
