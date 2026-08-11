import unittest
from pathlib import Path

from Tools.second_brain.policy import MigrationPolicy


class MigrationPolicyTests(unittest.TestCase):
    def setUp(self):
        self.policy = MigrationPolicy.load(
            Path(__file__).parents[1] / "migration-policy.json"
        )

    def test_path_routes_take_precedence_over_status_routes(self):
        """Ignoring an explicit route would move personal context into a generic folder."""
        route = self.policy.route("Knowledge/Thinking/媛쒖씤 Dev Rules.md", "personal-context")

        self.assertEqual(route.target, "50 ?곸뿭/媛쒕컻 ?먯튃/媛쒖씤 Dev Rules.md")
        self.assertEqual(route.action, "move")

    def test_status_routes_promote_notes_to_the_configured_target(self):
        """A wrong status route would lose the lecture note's normalized destination."""
        self.assertEqual(
            self.policy.route("Knowledge/Literature Notes/[Lecture] LLM怨?RAG.md", "source-expanded").target,
            "20 ?뚯뒪 ?명듃/媛뺤쓽/LLM怨?RAG 媛뺤쓽.md",
        )
        self.assertEqual(
            self.policy.route("Knowledge/Permanent Notes/RAG.md", "wiki-expanded").target,
            "00 ?몃컯???밴꺽 ?湲??곴뎄 ?명듃/RAG.md",
        )
        self.assertEqual(
            self.policy.route("Knowledge/Reference Notes/Python 移섑듃?쒗듃.md", "reference").target,
            "50 ?곸뿭/媛쒕컻 ?덊띁?곗뒪/Python 移섑듃?쒗듃.md",
        )

    def test_unrouted_notes_are_archived(self):
        """Treating unknown wiki material as active would keep obsolete notes live."""
        route = self.policy.route("Knowledge/Permanent Notes/?뺤? ?명듃.md", "wiki-standardized")

        self.assertEqual(route.action, "archive")
        self.assertEqual(route.target, "90 蹂닿????댁쟾 LLM Wiki/Knowledge/Permanent Notes/?뺤? ?명듃.md")


if __name__ == "__main__":
    unittest.main()
