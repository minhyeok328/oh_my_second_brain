---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'llm'
  - 'langgraph'
  - 'state'
aliases:
  - 'LangGraph State'
sources:
  - 'https://docs.langchain.com/oss/python/langgraph/graph-api'
source_quality: 'primary'
verified: true
id: '20260530000000-8fe5'
---

# LangGraph 상태는 노드 사이의 데이터 계약이다

LangGraph 상태는 단순한 작업 메모리가 아니라 모든 노드와 엣지가 읽고 갱신하는 데이터 계약이다. 공식 Graph API에서 상태 스키마가 노드와 엣지의 입력이 되고 노드가 상태 업데이트를 반환하는 구조이므로, 각 필드는 생산자·소비자·병합 규칙을 함께 가져야 한다.

질문, route, 검색 후보, 실제 전달 후보, 답변을 구분하면 [[LangGraph는 상태 전이를 명시해 LLM 흐름을 제어한다]]가 어느 단계에서 값이 바뀌었는지 기록할 수 있다. route처럼 다음 경로에 쓰이는 값은 [[조건부 엣지는 상태에 따라 다음 실행 경로를 선택한다]]의 허용 값과 맞아야 하고, 검색 관련 필드는 [[RAG 평가는 검색과 생성을 분리해서 측정해야 한다]]의 관측 자료가 된다.

상태에 모든 지역 변수를 넣는 것은 반례다. 필드가 많아질수록 직렬화, 체크포인트 호환성, 개인정보 보존 비용이 커지고 오래된 세션 값이 새 요청에 섞일 위험도 생긴다. 기본값과 reducer가 불분명한 공유 필드보다 노드 내부에서 끝나는 지역 값이 낫고, 세션 지속 상태와 요청 1회용 상태는 분리해야 한다.

## 확인한 근거

- 2026-08-11: LangGraph 공식 Graph API — 상태 스키마, 노드 업데이트, reducer와 입출력 스키마의 현재 계약을 확인했다.
- 강의 맥락: [[LLM과 RAG 강의]]의 대화 상태와 프로젝트별 GraphState 경험을 필드 책임의 관점으로 재작성했다.
