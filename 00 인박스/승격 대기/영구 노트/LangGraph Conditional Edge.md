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
id: '20260530000000-489c'
---

# LangGraph Conditional Edge

태그: #llm_wiki #llm #langgraph

## 한 줄 정의

LangGraph Conditional Edge는 현재 state 값을 보고 다음에 실행할 node를 고르는 조건부 연결이다.

## 내 말로 다시 설명

챗봇은 모든 질문을 같은 방식으로 처리하면 안 된다. 특정 식당명 질문은 fixed 검색, 분위기 질문은 embedding 검색, 상담 범위 밖 질문은 종료처럼 state의 route 값에 따라 다음 길을 바꿔야 한다.

## 언제 쓰는가

- route 결과에 따라 fixed/embedding 검색 경로를 나눌 때
- 검색 결과가 0건인지, 너무 많은지, 적당한지에 따라 답변 방식을 바꿀 때
- 후속 질문인지 새 질문인지에 따라 제품군 분류 단계를 건너뛰거나 유지할 때

## 언제 쓰면 안 되는가

- 조건 함수가 LLM 자유문장을 그대로 비교하는 경우
- fallback 경로가 없어 예외 값에서 그래프가 멈추는 경우
- 조건이 많아졌는데 평가 케이스가 없는 경우

## 프로젝트 예시

[[SKN26 3차 PICKLE 맛집 추천 챗봇]]은 `route`가 `embedding`이면 embedding slot node로, `fixed`이면 fixed slot node로 보낸다. [[SKN26 4차 LG Home AI 가전 상담]]은 fall case, 후속 질문, 제품군 분류, 검색 결과 수에 따라 여러 조건 분기를 둔다.

## 실패 조건

- route 값 표준화가 없으면 `"fixed."`, `"Fixed"` 같은 출력에 취약하다.
- 조건 분기가 많아질수록 각 분기에 대한 최소 테스트 질문이 필요하다.
- 조건 node가 너무 많은 책임을 가지면 실제 실패 지점이 숨겨진다.

## 관련 개념

- [[LangGraph]]
- [[LangGraph State]]
- [[RAG 평가]]
- [[Function Calling]]

## 먼저 확인할 질문

- 가능한 route 값이 코드와 prompt 양쪽에서 같은 이름으로 정의되어 있는가?
- 알 수 없는 route가 나오면 어디로 fallback되는가?
