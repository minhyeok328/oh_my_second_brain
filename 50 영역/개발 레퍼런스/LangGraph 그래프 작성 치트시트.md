---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'langgraph'
  - 'reference'
source:
  - 'C:\lecture'
source_quality: 'mixed'
verified: false
id: '20260530000000-cc9b'
---

# LangGraph 그래프 작성 치트시트

태그: #langgraph #reference #llm_wiki

## 용도

상태 그래프 워크플로우 작성 절차를 요약한다.

## 빠른 참조

- `define State`: 공유 상태 구조 정의
- `add_node(name, fn)`: 작업 노드 추가
- `add_edge(a, b)`: 고정 경로 연결
- `add_conditional_edges(...)`: 조건 분기 연결
- `compile()`: 실행 가능한 그래프 생성

## 관련 노트

- [[LangGraph]]
- [[LangGraph State]]
- [[LangGraph Conditional Edge]]
