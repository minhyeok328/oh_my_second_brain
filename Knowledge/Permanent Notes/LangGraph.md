---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'llm'
  - 'langgraph'
  - 'agent'
source:
  - 'C:\lecture'
external:
  - 'https://docs.langchain.com/oss/python/langgraph/graph-api'
---

# LangGraph

태그: #llm_wiki #llm #langgraph #agent

## 한 줄 정의

LangGraph는 LLM 애플리케이션을 상태, 노드, 엣지로 표현해 반복, 분기, 도구 호출, human-in-the-loop 흐름을 제어하는 그래프 실행 프레임워크다.

## 내 말로 다시 설명

단순 chain은 "A 다음 B"처럼 직선 흐름에 강하다. LangGraph는 상태를 들고 여러 노드를 오가며 조건에 따라 다음 행동을 고를 수 있다. 그래서 RAG 검색, 도구 호출, 검증, 재시도, 사용자 확인이 섞인 에이전트 흐름을 설명하기 좋다.

## 핵심 구성

- [[LangGraph State]]: 노드들이 공유하는 데이터 구조다.
- [[LangGraph Node와 Edge]]: 작업 단위와 이동 경로다.
- [[LangGraph Conditional Edge]]: 상태에 따라 다음 노드를 고르는 분기다.
- compile: 그래프 정의를 실행 가능한 객체로 만든다.

## 언제 쓰는가

- 검색, 생성, 검증, 재검색처럼 반복 흐름이 필요할 때
- LLM이 도구를 호출한 뒤 결과에 따라 다음 행동을 바꿔야 할 때
- 실패 시 재시도나 사람 확인 단계를 넣어야 할 때

## 언제 쓰면 안 되는가

- 한 번의 prompt와 한 번의 모델 호출로 충분한 경우
- 상태 설계 없이 노드만 늘려 흐름이 더 불투명해지는 경우
- 로그와 관찰 가능성 없이 복잡한 agent를 먼저 만들려는 경우

## 자주 헷갈리는 점

- LangGraph는 LLM 자체가 아니라 LLM 호출, 도구, 분기, 상태를 묶는 실행 구조다.
- node를 많이 만든다고 좋은 agent가 되지는 않는다. 상태와 종료 조건이 더 중요하다.
- graph가 복잡해질수록 각 node의 입력과 출력 로그가 없으면 디버깅이 어려워진다.

## 설계 체크리스트

- State에 꼭 필요한 값만 들어 있는가?
- 각 node가 한 가지 책임만 갖는가?
- 조건 분기가 테스트 가능한 기준으로 작성됐는가?
- 종료 조건과 실패 조건이 명확한가?
- 각 실행 단계의 입력/출력을 기록하는가?

## 관련 개념

- [[LangChain]]
- [[Runnable]]
- [[RAG]]
- [[Multi-Agent]]
- [[Function Calling]]

## 확인 질문

- 이 흐름은 chain으로 충분한가, 상태 기반 graph가 필요한가?
- 재시도와 종료 조건이 코드로 설명되는가?

## 외부 참조

- https://docs.langchain.com/oss/python/langgraph/graph-api
