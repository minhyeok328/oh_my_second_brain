import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from Tools.second_brain.inventory import scan_notes, to_json


class InventoryTests(unittest.TestCase):
    def test_scan_notes_returns_relative_posix_records_in_sorted_order(self):
        """A path-ordering regression would make migration baselines unstable."""
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "nested").mkdir()
            (root / "nested" / "B.md").write_text("See [[A]]", encoding="utf-8")
            (root / "A.md").write_text(
                "---\nstatus: growing\n---\n# A", encoding="utf-8"
            )

            records = scan_notes(root)

            self.assertEqual([record.path for record in records], ["A.md", "nested/B.md"])
            self.assertEqual(records[0].title, "A")
            self.assertEqual(records[0].metadata["status"], "growing")
            self.assertEqual(records[1].wikilinks, ["A"])

    def test_to_json_serializes_note_records_as_json_objects(self):
        """Dropping record fields would make the inventory unusable as an audit baseline."""
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            (root / "A.md").write_text("# A", encoding="utf-8")

            inventory = json.loads(to_json(scan_notes(root)))

            self.assertEqual(inventory[0]["path"], "A.md")
            self.assertEqual(inventory[0]["title"], "A")
            self.assertEqual(inventory[0]["metadata"], {})
            self.assertEqual(inventory[0]["wikilinks"], [])


if __name__ == "__main__":
    unittest.main()
