---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'langgraph'
  - 'llm'
source:
  - 'C:\lecture'
---

# LangGraph Node와 Edge

태그: #langgraph #llm #llm_wiki

## 한 줄 정의

Node는 상태를 받아 작업을 수행하는 함수이고, Edge는 노드 사이의 실행 흐름이다.

## 왜 중요한가

그래프의 각 단계를 작게 나누면 검색, 생성, 검증, 도구 호출을 독립적으로 테스트할 수 있다.

## 핵심 개념

- 노드는 상태 일부를 반환해 업데이트한다.
- 일반 edge는 고정 경로를 연결한다.
- 조건부 edge는 상태에 따라 다음 노드를 고른다.

## 예제

```python
# graph.add_node("retrieve", retrieve)
# graph.add_edge("retrieve", "generate")
```

## 실무 활용

복잡한 챗봇, 재시도 루프, 사람 검토 포함 워크플로우에 적용한다.

## 관련 개념

- [[LangGraph State]]
- [[LangGraph Conditional Edge]]
- [[Function Calling]]

자료 힌트: 08_llm_workspace/08_langgraph

## 내 말로 다시 설명

LangGraph Node와 Edge은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[LangGraph State]], [[LangGraph Conditional Edge]], [[Function Calling]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- LangGraph Node와 Edge을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
