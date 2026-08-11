---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'langchain'
  - 'rag'
  - 'reference'
source:
  - 'C:\lecture'
source_quality: 'mixed'
verified: false
id: '20260530000000-4d3c'
---

# LangChain RAG 치트시트

태그: #langchain #rag #reference #llm_wiki

## 용도

문서 기반 QA 체인을 빠르게 구성할 때의 단계다.

## 빠른 참조

- `loader.load()`: 문서 로딩
- `splitter.split_documents(docs)`: 청킹
- `embedding.embed_documents(chunks)`: 임베딩
- `vectorstore.as_retriever()`: 검색기 생성
- `prompt | model | parser`: 생성 체인 구성

## 관련 노트

- [[Document Loader]]
- [[Text Splitter]]
- [[RAG]]
