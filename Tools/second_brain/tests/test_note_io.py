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
        self.assertTrue(note.body.startswith("\n# 검색의 핵심"))

    def test_render_round_trip(self):
        parsed = parse_markdown(SAMPLE)
        reparsed = parse_markdown(render_markdown(parsed))
        self.assertEqual(reparsed, parsed)

    def test_parse_preserves_body_whitespace_without_frontmatter(self):
        body = "  indented text\r\nhard break  \r\n"
        self.assertEqual(parse_markdown(body).body, "  indented text\nhard break  \n")

    def test_render_preserves_body_whitespace_after_frontmatter(self):
        note = NoteDocument({"type": "permanent"}, "\n  indented text\nHard break  \n")
        self.assertEqual(
            render_markdown(note),
            "---\ntype: 'permanent'\n---\n\n  indented text\nHard break  \n",
        )
        self.assertEqual(parse_markdown(render_markdown(note)), note)

    def test_extract_link_targets_without_heading_or_alias(self):
        body = "[[RAG#검색 단계]] [[Embedding]] ![[diagram.png]]"
        self.assertEqual(extract_wikilinks(body), ["RAG", "Embedding"])

    def test_rewrite_preserves_heading_and_alias_without_rewriting_embeds(self):
        body = "[[RAG#검색 단계|표시]]와 [[Embedding]] ![[RAG#검색 단계|표시]]"
        rewritten = rewrite_wikilinks(
            body,
            {
                "RAG": "RAG의 성능은 검색 단계의 설계에서 시작된다",
                "Embedding": "임베딩은 하나의 기준으로 비교를 위한 좌표를 표현한다",
            },
        )
        self.assertEqual(
            rewritten,
            "[[RAG의 성능은 검색 단계의 설계에서 시작된다#검색 단계|표시]]와 "
            "[[임베딩은 하나의 기준으로 비교를 위한 좌표를 표현한다]] "
            "![[RAG#검색 단계|표시]]",
        )

    def test_reject_nested_yaml_mapping(self):
        with self.assertRaisesRegex(ValueError, "nested mappings are unsupported"):
            parse_markdown("---\nsource:\n  title: nested\n---\nbody")

    def test_reject_non_empty_inline_list(self):
        with self.assertRaisesRegex(ValueError, "non-empty inline lists are unsupported"):
            parse_markdown("---\ntags: [rag, retrieval]\n---\nbody")

    def test_reject_flow_mappings(self):
        for frontmatter in (
            "source: {title: nested}",
            "source: {title: nested, url: example.com}",
            "tags:\n  - {name: rag}",
        ):
            with self.subTest(frontmatter=frontmatter):
                with self.assertRaisesRegex(ValueError, "unsupported YAML collection syntax"):
                    parse_markdown(f"---\n{frontmatter}\n---\nbody")

    def test_reject_flow_sequences_inside_lists(self):
        with self.assertRaisesRegex(ValueError, "non-empty inline lists are unsupported"):
            parse_markdown("---\ntags:\n  - [rag, retrieval]\n---\nbody")


if __name__ == "__main__":
    unittest.main()
