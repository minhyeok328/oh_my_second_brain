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
  - 'evaluation'
source:
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project\src_test3'
source_quality: 'mixed'
verified: false
id: '20260530000000-2179'
---

# RAG 평가 질문 세트

태그: #llm_wiki #questions #rag #evaluation

## 목적

[[SKN26 3차 PICKLE 맛집 추천 챗봇]]의 RAG 품질을 질문 단위로 반복 검증하기 위한 goldset 구조를 wiki에 요약한다.

## 기준 데이터

- 기준 DB: `database\sql\restaurant.db`
- 생성 스크립트: `src_test3\build_llm_goldset.py`
- 평가 스크립트: `src_test3\evaluate_llm.py`
- 구성: fixed 20개 + embedding 30개, 총 50개 케이스

## fixed 질문 유형

특정 식당명, 메뉴명, 유저명처럼 DB entity가 직접 들어간 질문이다.

- 영업시간 질문: `유태우스시 영업시간 알려줘`
- 메뉴 보유 질문: `유태우스시에 회전초밥 있어?`
- 기대 route: `fixed`
- payload check: `restaurant`, `menu`, `user` 중 필요한 key에 기대 문자열이 들어가야 한다.
- target check: 기대 `restaurant_code` 또는 `restaurant_name`이 검색 결과에 포함되어야 한다.

## embedding 질문 유형

분위기, 상황, 태그, 카테고리처럼 유사도 검색이 필요한 질문이다.

- 태그 기반 질문: `혼밥하기 좋은 초밥 맛집 추천해줘`
- 상황 기반 질문: `데이트하기 좋은 파스타 맛집 추천해줘`
- 기대 route: `embedding`
- payload check: `category`, `tag`, `menu`, `food`, `review` 중 적절한 슬롯에 조건이 들어가야 한다.
- retrieval check: 최소 후보 수 이상이 `used_restaurant_list`에 남아야 한다.

## 평가 항목

- route: 질문이 fixed/embedding 중 올바른 경로로 갔는가?
- payload: 슬롯 추출 결과가 기대 key와 값을 포함하는가?
- target: 기대 식당이 후보나 최종 사용 리스트에 포함되는가?
- answer: 답변이 필수 키워드를 포함하고 금지 키워드를 피하는가?
- retrieval: 최소 후보 수를 만족하는가?

## 점수 가중치

- route: 30%
- payload: 25%
- target: 25%
- answer: 10%
- retrieval: 10%

## 운영 규칙

- DB가 바뀌면 goldset도 다시 생성한다.
- 실패 케이스는 [[RAG 검색 실패 사례]]에 route/payload/target/answer/retrieval 중 어느 유형인지 분류한다.
- 답변 문장만 보지 말고 검색 후보와 실제 사용 후보를 함께 확인한다.

## 관련 개념

- [[RAG 평가는 검색과 생성을 분리해서 측정해야 한다]]
- [[RAG의 성능은 검색 단계의 품질에서 시작된다]]
- [[검색기는 질문과 관련된 근거 후보를 좁힌다]]
- [[LangGraph는 상태 전이를 명시해 LLM 흐름을 제어한다]]
- [[SKN26 3차 PICKLE 맛집 추천 챗봇]]
