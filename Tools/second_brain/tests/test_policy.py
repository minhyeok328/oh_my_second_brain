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
        route = self.policy.route(
            "Knowledge/Thinking/개인 Dev Rules.md", "personal-context"
        )

        self.assertEqual(route.target, "50 영역/개발 원칙/개인 Dev Rules.md")
        self.assertEqual(route.action, "move")

    def test_status_routes_promote_notes_to_the_configured_target(self):
        """A wrong status route would lose the lecture note's normalized destination."""
        self.assertEqual(
            self.policy.route(
                "Knowledge/Literature Notes/[Lecture] LLM과 RAG.md",
                "source-expanded",
            ).target,
            "20 소스 노트/강의/LLM과 RAG 강의.md",
        )
        self.assertEqual(
            self.policy.route(
                "Knowledge/Permanent Notes/RAG.md", "wiki-expanded"
            ).target,
            "00 인박스/승격 대기/영구 노트/RAG.md",
        )
        self.assertEqual(
            self.policy.route(
                "Knowledge/Reference Notes/Python 치트시트.md", "reference"
            ).target,
            "50 영역/개발 레퍼런스/Python 치트시트.md",
        )

    def test_unrouted_notes_are_archived(self):
        """Treating unknown wiki material as active would keep obsolete notes live."""
        route = self.policy.route(
            "Knowledge/Permanent Notes/얕은 노트.md", "wiki-standardized"
        )

        self.assertEqual(route.action, "archive")
        self.assertEqual(
            route.target,
            "90 보관함/이전 LLM Wiki/Knowledge/Permanent Notes/얕은 노트.md",
        )


if __name__ == "__main__":
    unittest.main()
