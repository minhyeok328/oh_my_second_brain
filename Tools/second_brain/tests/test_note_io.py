import unittest

from Tools.second_brain.note_io import (
    NoteDocument,
    extract_wikilinks,
    parse_markdown,
    render_markdown,
    rewrite_wikilinks,
)


SAMPLE = r'''---
type: "permanent"
status: "growing"
verified: true
tags:
  - rag
  - retrieval
sources:
  - "[[LangChain 공식 RAG 문서]]"
source_path: 'C:\MinHyeok\lecture'
aliases: []
---

# 검색의 핵심

본문 [[RAG#검색 단계]]와 [[Embedding]]을 연결한다.
'''


class NoteIoTests(unittest.TestCase):
    def test_parse_supported_frontmatter(self):
        note = parse_markdown(SAMPLE)
        self.assertEqual(note.metadata["type"], "permanent")
        self.assertTrue(note.metadata["verified"])
        self.assertEqual(note.metadata["tags"], ["rag", "retrieval"])
        self.assertEqual(note.metadata["sources"], ["[[LangChain 공식 RAG 문서]]"])
        self.assertEqual(note.metadata["source_path"], r"C:\MinHyeok\lecture")
        self.assertTrue(note.body.startswith("# 검색의 핵심"))

    def test_render_round_trip(self):
        parsed = parse_markdown(SAMPLE)
        reparsed = parse_markdown(render_markdown(parsed))
        self.assertEqual(reparsed, parsed)

    def test_extract_link_targets_without_heading_or_alias(self):
        body = "[[RAG#검색 단계]] [[Embedding]] ![[diagram.png]]"
        self.assertEqual(extract_wikilinks(body), ["RAG", "Embedding"])

    def test_rewrite_preserves_heading_and_alias(self):
        body = "[[RAG#검색 단계]]와 [[Embedding]]"
        rewritten = rewrite_wikilinks(
            body,
            {
                "RAG": "RAG의 성능은 검색 단계의 설계에서 시작된다",
                "Embedding": "임베딩은 하나의 기준으로 비교를 위한 좌표를 표현한다",
            },
        )
        self.assertEqual(
            rewritten,
            "[[RAG의 성능은 검색 단계의 설계에서 시작된다#검색 단계]]와 "
            "[[임베딩은 하나의 기준으로 비교를 위한 좌표를 표현한다]]",
        )

    def test_reject_nested_yaml_mapping(self):
        with self.assertRaisesRegex(ValueError, "nested mappings are unsupported"):
            parse_markdown("---\nsource:\n  title: nested\n---\nbody")

    def test_reject_non_empty_inline_list(self):
        with self.assertRaisesRegex(ValueError, "non-empty inline lists are unsupported"):
            parse_markdown("---\ntags: [rag, retrieval]\n---\nbody")


if __name__ == "__main__":
    unittest.main()
