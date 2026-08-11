---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'questions'
  - 'rag'
  - 'debugging'
source:
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project\src_test3'
source_quality: 'mixed'
verified: false
id: '20260530000000-0f1a'
---

# RAG 검색 실패 사례

태그: #llm_wiki #questions #rag #debugging

## 목적

RAG 답변이 틀렸을 때 "모델이 멍청했다"로 뭉개지 않고, 검색 전 단계부터 생성 후 단계까지 실패 위치를 분리한다.

## 실패 유형

### route 실패

증상: 특정 식당명 질문이 `embedding`으로 가거나, 분위기 기반 질문이 `fixed`로 간다.

먼저 볼 것:

- [[LangGraph Conditional Edge]]
- router prompt
- expected_route와 실제 route

대응:

- fixed entity 예시와 embedding 조건 예시를 라우터 프롬프트에 더 명확히 넣는다.
- 애매한 질문의 기본 경로를 의도적으로 정한다.

### payload 실패

증상: route는 맞지만 `restaurant`, `menu`, `category`, `tag`, `review` 슬롯이 비거나 엉뚱한 key에 들어간다.

먼저 볼 것:

- [[Function Calling]]
- slot schema
- payload_checks

대응:

- 슬롯 이름과 설명을 실제 DB 컬럼/테이블 의미에 맞춘다.
- 사용자 표현과 DB 태그 표현 사이의 alias를 보강한다.

### target 실패

증상: 슬롯은 맞지만 기대 식당이 후보에 없다.

먼저 볼 것:

- [[Retriever]]
- [[Embedding]]
- [[SQLite]]
- 관계 테이블 조인

대응:

- category/tag/menu/review 중 어떤 검색 경로가 후보를 탈락시켰는지 분리한다.
- 교집합이 너무 강하면 fallback 후보 확장이나 reranking을 검토한다.

### answer 실패

증상: 후보에는 정답이 있는데 답변이 엉뚱하거나 필수 정보를 빠뜨린다.

먼저 볼 것:

- [[Prompt Engineering]]
- [[RAG]]
- system prompt
- answer_checks

대응:

- 후보 리스트 밖 정보 생성 금지 규칙을 강화한다.
- 답변 형식과 필수 포함 항목을 prompt에 명시한다.

### retrieval 실패

증상: `used_restaurant_list`가 비거나 최소 후보 수를 만족하지 못한다.

먼저 볼 것:

- `restaurant_list_count`
- `used_restaurant_count`
- reranking 기준

대응:

- top-k, 유사도 임계값, 후보 병합 방식을 조정한다.
- goldset 질문이 실제 DB 상태와 맞는지 확인한다.

## 기록 형식

- 질문:
- 기대 route:
- 실제 route:
- 실패 유형:
- 원인 후보:
- 수정한 노트:
- 재평가 결과:

## 관련 개념

- [[RAG 평가]]
- [[RAG 평가 질문 세트]]
- [[LangGraph]]
- [[Retriever]]
- [[Prompt Engineering]]
