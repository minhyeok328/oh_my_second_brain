---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'llm'
  - 'langgraph'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-8fe5'
---

# LangGraph State

태그: #llm_wiki #llm #langgraph

## 한 줄 정의

LangGraph State는 그래프의 node들이 공유하고 갱신하는 데이터 구조다.

## 내 말로 다시 설명

State는 agent의 작업 메모리다. 사용자 질문, route, slot payload, 검색 후보, 답변, 대화 상태처럼 각 node가 다음 node에 넘길 값을 담는다. State가 흐릿하면 agent 전체가 흐릿해진다.

## 언제 쓰는가

- node 사이에 질문, route, 검색 결과, 답변을 넘겨야 할 때
- 후속 질문을 위해 대화방별 agent state를 보존해야 할 때
- 평가에서 route_payload, restaurant_list, used_restaurant_list를 확인해야 할 때

## 언제 쓰면 안 되는가

- node 내부 지역 변수로 충분한 값을 state에 계속 쌓는 경우
- 타입과 기본값 없이 dict key를 임의로 추가하는 경우
- 사용자별/세션별로 분리해야 할 값을 전역 변수로 두는 경우

## 프로젝트 예시

[[SKN26 3차 PICKLE 맛집 추천 챗봇]]의 `GraphState`는 `question`, `session_id`, `route`, `route_payload`, `restaurant_list`, `used_restaurant_list`, `answer`를 가진다. [[SKN26 4차 LG Home AI 가전 상담]]은 `ConversationState`, `product_type`, `slots`, `intent`, `manual_results`, `response_tail`까지 포함한다.

## 실패 조건

- `total=False` state에서 필드 누락을 기본값으로 처리하지 않으면 runtime error가 난다.
- 오래된 agent_state를 새 질문에 잘못 병합하면 후속 질문이 틀어진다.
- 검색 후보 전체와 LLM에 실제 전달한 후보를 구분하지 않으면 평가가 어려워진다.

## 관련 개념

- [[LangGraph]]
- [[LangGraph Node와 Edge]]
- [[RAG 평가]]
- [[Django Chatbot]]

## 먼저 확인할 질문

- 이 필드는 어느 node가 만들고 어느 node가 소비하는가?
- 세션별로 저장해야 하는 state와 요청 1회용 state가 분리되어 있는가?
