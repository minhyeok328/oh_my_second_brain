---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'llm'
  - 'retriever'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-8f03'
---

# Retriever

태그: #llm_wiki #llm #retriever

## 한 줄 정의

Retriever는 사용자 질문을 받아 RAG 답변에 넣을 후보 문서, DB row, 식당, 매뉴얼 chunk를 가져오는 검색 컴포넌트다.

## 내 말로 다시 설명

Retriever는 LLM에게 넘길 "재료"를 고르는 단계다. 이 단계가 틀리면 generator가 아무리 좋아도 정답을 만들기 어렵다. 그래서 어떤 후보를 가져왔고, 어떤 후보를 최종 사용했는지 기록해야 한다.

## 언제 쓰는가

- 질문에 맞는 문서 chunk나 DB entity를 top-k로 가져와야 할 때
- keyword, SQL, embedding, metadata filter를 조합해야 할 때
- 검색 후보를 reranking하거나 교집합으로 좁혀야 할 때

## 언제 쓰면 안 되는가

- 사용자가 이미 정확한 primary key를 제공해 단일 row 조회면 충분한 경우
- 검색 품질 평가 없이 top-k 숫자만 늘리는 경우
- 후보가 없을 때 fallback이나 "모른다" 처리가 없는 경우

## 프로젝트 예시

[[SKN26 3차 PICKLE 맛집 추천 챗봇]]은 slot별 검색 결과를 restaurant_code 기준으로 교차시키고, 최종 후보를 LLM에 넘긴다. [[SKN26 4차 LG Home AI 가전 상담]]은 ORM 상품 검색과 Pinecone 매뉴얼 검색을 분리해 제품 추천과 사용설명서 Q&A에 각각 사용한다.

## 실패 조건

- 검색 후보 수가 0인데 generator가 임의 답변을 만들면 hallucination이 된다.
- 정확 검색과 의미 검색을 같은 기준으로 섞으면 route 실패를 찾기 어렵다.
- 재랭킹 후 최종 후보를 기록하지 않으면 평가와 디버깅이 어렵다.

## 관련 개념

- [[RAG]]
- [[Embedding]]
- [[Vector Store]]
- [[Reranking]]
- [[RAG 평가]]

## 먼저 확인할 질문

- 후보를 넓히는 단계와 좁히는 단계가 분리되어 있는가?
- 검색 결과가 틀렸을 때 route, slot, vector, SQL 중 어디를 먼저 볼 것인가?
