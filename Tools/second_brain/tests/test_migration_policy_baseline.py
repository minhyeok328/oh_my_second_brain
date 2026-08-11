import json
from collections import Counter
from pathlib import Path
import unittest
import unicodedata

from Tools.second_brain.inventory import NoteRecord
from Tools.second_brain.migration import build_actions
from Tools.second_brain.policy import MigrationPolicy


ROOT = Path(__file__).resolve().parents[3]
INVENTORY_PATH = (
    ROOT / "docs" / "superpowers" / "migrations" / "2026-08-11-legacy-inventory.json"
)
POLICY_PATH = ROOT / "Tools" / "second_brain" / "migration-policy.json"

APPROVED_ROUTES = {
    "Knowledge/Thinking/개인 Dev Rules.md": "50 영역/개발 원칙/개인 Dev Rules.md",
    "Knowledge/Thinking/생각과 회고 MOC.md": "60 구조 노트/생각과 회고 지도.md",
    "Knowledge/Thinking/프로젝트 기반 개발자 정체성.md": "50 영역/커리어/프로젝트 기반 개발자 정체성.md",
    "Knowledge/Thinking/프로젝트 회고 질문 세트.md": "50 영역/회고/프로젝트 회고 질문 세트.md",
    "Knowledge/Projects/프로젝트 경험 MOC.md": "40 프로젝트/프로젝트 경험 지도.md",
    "Knowledge/Projects/프로젝트 적용 로그.md": "40 프로젝트/공통/프로젝트 적용 로그.md",
    "Knowledge/Projects/프로젝트 의사결정 로그.md": "40 프로젝트/공통/프로젝트 의사결정 로그.md",
    "Knowledge/Projects/프로젝트 실패와 디버깅 로그.md": "40 프로젝트/공통/프로젝트 실패와 디버깅 로그.md",
    "Knowledge/Questions/질문 인박스.md": "00 인박스/질문 인박스.md",
    "Knowledge/Questions/RAG 검색 실패 사례.md": "00 인박스/RAG 검색 실패 사례.md",
    "Knowledge/Questions/RAG 평가 질문 세트.md": "00 인박스/RAG 평가 질문 세트.md",
    "Knowledge/Projects/SKN26 1차 프로젝트 - 차량 TCO.md": "40 프로젝트/SKN26 1차 차량 운영비 프로젝트.md",
    "Knowledge/Projects/SKN26 2차 프로젝트 - 카드 이탈 예측.md": "40 프로젝트/SKN26 2차 신용카드 고객 이탈 분석.md",
    "Knowledge/Projects/SKN26 3차 프로젝트 - PICKLE RAG 챗봇.md": "40 프로젝트/SKN26 3차 PICKLE 맛집 추천 챗봇.md",
    "Knowledge/Projects/SKN26 4차 프로젝트 - LG Home.md": "40 프로젝트/SKN26 4차 LG Home AI 가전 상담.md",
}


class MigrationPolicyBaselineContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        inventory = json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
        records = [
            NoteRecord(
                path=f"Knowledge/{item['path']}",
                title=item["title"],
                metadata=item["metadata"],
                wikilinks=item["wikilinks"],
            )
            for item in inventory
        ]
        cls.policy_document = json.loads(POLICY_PATH.read_text(encoding="utf-8"))
        cls.policy = MigrationPolicy.load(POLICY_PATH)
        cls.actions = build_actions(records, cls.policy)
        cls.actions_by_source = {action.source: action for action in cls.actions}

    def test_committed_inventory_reconciles_to_the_approved_action_counts(self):
        """A corrupt or incomplete policy would archive notes selected for the active vault."""
        action_counts = Counter(action.action for action in self.actions)

        self.assertEqual(len(self.actions), 312)
        self.assertEqual(action_counts["move"], 84)
        self.assertEqual(action_counts["archive"], 228)
        self.assertEqual(action_counts["delete"], 0)
        self.assertEqual(len({action.target for action in self.actions}), 312)

    def test_active_actions_reconcile_to_the_seven_approved_categories(self):
        """Wrong status or path routing would change the reviewed 84-note migration scope."""
        explicit_sources = set(APPROVED_ROUTES)
        personal_sources = {
            source for source in explicit_sources if source.startswith("Knowledge/Thinking/")
        }
        question_sources = {
            source for source in explicit_sources if source.startswith("Knowledge/Questions/")
        }
        project_sources = explicit_sources - personal_sources - question_sources
        project_hub_sources = {
            source for source in project_sources if "/SKN26 " in source
        }
        cross_project_sources = project_sources - project_hub_sources
        categories = {
            "lecture source": {
                action.source
                for action in self.actions
                if action.target.startswith("20 소스 노트/강의/")
            },
            "permanent drafts": {
                action.source
                for action in self.actions
                if action.target.startswith("00 인박스/승격 대기/영구 노트/")
            },
            "references": {
                action.source
                for action in self.actions
                if action.target.startswith("50 영역/개발 레퍼런스/")
            },
            "project hubs": project_hub_sources,
            "personal": personal_sources,
            "cross-project": cross_project_sources,
            "questions": question_sources,
        }

        self.assertEqual(
            {name: len(sources) for name, sources in categories.items()},
            {
                "lecture source": 14,
                "permanent drafts": 34,
                "references": 21,
                "project hubs": 4,
                "personal": 4,
                "cross-project": 4,
                "questions": 3,
            },
        )
        category_sources = set().union(*categories.values())
        active_sources = {
            action.source for action in self.actions if action.action == "move"
        }
        self.assertEqual(category_sources, active_sources)
        self.assertEqual(sum(map(len, categories.values())), len(category_sources))

    def test_all_targets_use_the_approved_korean_roots_without_corruption_markers(self):
        """Mojibake or control characters in a target would move notes to unintended paths."""
        self.assertEqual(self.policy.archive_root, "90 보관함/이전 LLM Wiki")
        self.assertEqual(self.policy_document["staging_root"], "00 인박스/승격 대기")
        approved_active_roots = {
            "00 인박스",
            "20 소스 노트",
            "40 프로젝트",
            "50 영역",
            "60 구조 노트",
        }
        known_mojibake_markers = (
            "?",
            "\ufffd",
            "蹂닿",
            "몃컯",
            "곸뿭",
            "꾨줈",
            "媛쒖씤",
            "吏덈Ц",
        )

        for action in self.actions:
            with self.subTest(source=action.source):
                if action.action == "archive":
                    self.assertTrue(
                        action.target.startswith("90 보관함/이전 LLM Wiki/Knowledge/")
                    )
                else:
                    self.assertIn(action.target.split("/", 1)[0], approved_active_roots)
                self.assertFalse(
                    any(marker in action.target for marker in known_mojibake_markers)
                )
                self.assertFalse(
                    any(unicodedata.category(character).startswith("C") for character in action.target)
                )

    def test_all_fifteen_explicit_routes_match_the_approved_targets(self):
        """Losing an exact override would archive or flatten curated personal and project notes."""
        self.assertEqual(set(self.policy.path_routes), set(APPROVED_ROUTES))
        self.assertEqual(
            {
                source: self.actions_by_source[source].target
                for source in APPROVED_ROUTES
            },
            APPROVED_ROUTES,
        )
        self.assertTrue(
            all(
                self.actions_by_source[source].action == "move"
                for source in APPROVED_ROUTES
            )
        )


if __name__ == "__main__":
    unittest.main()
