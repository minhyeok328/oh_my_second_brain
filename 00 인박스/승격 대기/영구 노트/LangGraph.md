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
  - 'agent'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
external:
  - 'https://docs.langchain.com/oss/python/langgraph/graph-api'
source_quality: 'mixed'
verified: false
id: '20260530000000-90c5'
---

# LangGraph

태그: #llm_wiki #llm #langgraph #agent

## 한 줄 정의

LangGraph는 LLM 애플리케이션을 상태, 노드, 엣지, 조건 분기로 표현해 검색, 추출, 생성, 재시도, 후속 질문 흐름을 제어하는 그래프 실행 프레임워크다.

## 내 말로 다시 설명

단순 chain은 직선 흐름에 강하다. LangGraph는 "지금 상태가 무엇인가"에 따라 다음 노드를 바꿀 수 있어, route, slot extraction, DB 검색, RAG 생성처럼 단계가 갈라지는 챗봇에 맞다.

## 언제 쓰는가

- 질문을 분류한 뒤 서로 다른 검색 경로로 보내야 할 때
- 대화 state를 유지하면서 후속 질문을 처리해야 할 때
- 검색 결과 수, 실패 여부, 사용자 맥락에 따라 다른 답변 전략을 써야 할 때

## 언제 쓰면 안 되는가

- 한 번의 LLM 호출과 한 번의 DB 조회로 충분한 경우
- state schema 없이 node만 늘려 디버깅이 어려워지는 경우
- 평가와 로그 없이 agent 흐름을 복잡하게 만드는 경우

## 프로젝트 예시

- [[SKN26 3차 PICKLE 맛집 추천 챗봇]]은 `route_node -> slot_node -> connector_search_node -> generate_node` 흐름으로 fixed/embedding RAG를 구성했다.
- [[SKN26 4차 LG Home AI 가전 상담]]은 fall case, 후속 질문, 제품군 분류, intent router, DB 검색, 매뉴얼 RAG 답변을 상태 그래프로 묶었다.

## 실패 조건

- state key 이름이 node마다 다르면 조용히 빈 값이 흘러간다.
- 조건 분기가 문자열 비교에 의존하면 route 값 표준화가 중요하다.
- node 입력/출력 로그가 없으면 route 실패와 retrieval 실패를 구분하기 어렵다.

## 관련 개념

- [[LangGraph State]]
- [[LangGraph Node와 Edge]]
- [[LangGraph Conditional Edge]]
- [[RAG]]
- [[Function Calling]]

## 먼저 확인할 질문

- 이 흐름은 분기와 상태 유지가 실제로 필요한가?
- 각 node는 자기 책임의 필드만 만들고 있는가?

## 외부 참조

- https://docs.langchain.com/oss/python/langgraph/graph-api
