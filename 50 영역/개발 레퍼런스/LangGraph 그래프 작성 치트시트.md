---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'langgraph'
  - 'llm'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.langchain.com/oss/python/langgraph/graph-api'
  - '[[20 소스 노트/강의/LLM과 RAG 강의|LLM과 RAG 강의]]'
source_quality: 'mixed'
verified: false
id: '20260530000000-cc9b'
---

# LangGraph 그래프 작성 치트시트

## 용도

상태 그래프의 최소 구성 순서를 빠르게 확인한다.

## 빠른 참조

1. `TypedDict`, dataclass 또는 지원되는 모델로 공유 상태 스키마를 정의한다.
2. `StateGraph(State)`로 그래프 빌더를 만든다.
3. `add_node(name, fn)`으로 상태를 읽고 부분 업데이트를 반환하는 노드를 추가한다.
4. `add_edge(a, b)` 또는 `add_conditional_edges(...)`로 다음 실행 경로를 연결한다.
5. 시작·종료 경로를 확인한 뒤 `compile()`로 실행 가능한 그래프를 만든다.
6. 실행 전 reducer가 누적과 덮어쓰기 중 어느 의미인지 확인한다.

## 검증 범위

- 2026-08-11: LangGraph 공식 Graph API에서 State, Nodes, Edges, reducer와 compile 순서를 확인했다.
- import 경로, 체크포인터, 스트리밍, 비동기 호출, 사전 구축 에이전트 API는 설치 버전에 따라 달라질 수 있어 확인하지 않았다.
- 구체 코드는 설치된 LangGraph 버전의 공식 레퍼런스를 다시 확인한다.

## 관련 노트

- [[LangGraph는 상태 전이를 명시해 LLM 흐름을 제어한다]]
- [[LangGraph 상태는 노드 사이의 데이터 계약이다]]
- [[조건부 엣지는 상태에 따라 다음 실행 경로를 선택한다]]
- [[20 소스 노트/강의/LLM과 RAG 강의|LLM과 RAG 강의]]
