---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'llm'
  - 'rag'
  - 'vectorstore'
source:
  - 'C:\lecture'
external:
  - 'https://docs.langchain.com/oss/python/integrations/vectorstores/'
  - 'https://docs.langchain.com/oss/python/integrations/retrievers/index'
---

# Vector Store

태그: #llm_wiki #llm #rag #vectorstore

## 한 줄 정의

Vector Store는 embedding 벡터와 원문 metadata를 저장하고, 유사도 검색으로 관련 문서를 찾아주는 저장 계층이다.

## 내 말로 다시 설명

Vector Store는 RAG의 검색 엔진 역할을 한다. 문서 chunk의 embedding을 저장해 두었다가 질문 embedding이 들어오면 가까운 벡터를 찾아 원문과 metadata를 돌려준다. 단순 저장소가 아니라 검색 기준, 필터, 업데이트 전략이 함께 설계되어야 한다.

## 핵심 개념

- index: vector similarity search를 빠르게 하기 위한 구조다.
- document id: chunk와 원본 파일/섹션을 다시 연결하는 키다.
- metadata filter: 강의, 주차, 권한, 파일 타입으로 검색 범위를 줄인다.
- top-k: 가져올 후보 개수다.
- refresh strategy: 원문이 바뀔 때 embedding과 index를 갱신하는 방식이다.

## 언제 쓰는가

- [[Embedding]] 기반 semantic search가 필요할 때
- 강의 자료, 문서 저장소, FAQ를 [[RAG]]에 연결할 때
- 검색 결과에 source path와 metadata를 함께 남겨야 할 때

## 언제 쓰면 안 되는가

- 데이터가 작아서 일반 full-text search나 dictionary lookup이면 충분한 경우
- 수치 범위, 정렬, join이 핵심인 구조화 데이터 조회
- 원문 업데이트가 잦은데 index 갱신 정책이 없는 경우

## 자주 헷갈리는 점

- Vector Store는 DB 전체를 대체하지 않는다. 원문 저장소와 권한 시스템은 따로 필요할 수 있다.
- top-k를 늘리면 recall은 오를 수 있지만 prompt noise도 늘어난다.
- metadata가 부실하면 비슷하지만 엉뚱한 문서가 섞인다.

## 관련 개념

- [[Embedding]]
- [[Retriever]]
- [[Text Splitter]]
- [[Reranking]]
- [[RAG]]

## 확인 질문

- 검색 결과가 틀렸을 때 embedding, metadata, chunking 중 어디를 먼저 조정할 것인가?
- 원문 삭제/수정 시 vector index도 함께 갱신되는가?

## 외부 참조

- https://docs.langchain.com/oss/python/integrations/vectorstores/
- https://docs.langchain.com/oss/python/integrations/retrievers/index
