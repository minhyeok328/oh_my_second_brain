---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'react'
  - 'hook'
source:
  - 'C:\lecture'
---

# useReducer

태그: #react #hook #llm_wiki

## 한 줄 정의

복잡한 state 변경을 reducer 함수와 action으로 관리하는 React Hook이다.

## 왜 중요한가

여러 이벤트가 같은 상태를 바꾸거나 상태 전이가 명확해야 할 때 useState보다 구조적이다.

## 핵심 개념

- reducer는 이전 state와 action을 받아 다음 state를 반환한다.
- dispatch로 action을 보낸다.
- 상태 머신처럼 전이를 추적할 수 있다.

## 예제

```jsx
const [state, dispatch] = useReducer(reducer, initialState);
```

## 실무 활용

폼 상태, 장바구니, 필터 조합, 챗봇 대화 상태 관리에 사용한다.

## 관련 개념

- [[React State]]
- [[State Pattern]]
- [[useContext]]

자료 힌트: 13_react-cicd_workspace/01_react/03_hooks/02_useReducer

## 내 말로 다시 설명

useReducer은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[React State]], [[State Pattern]], [[useContext]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- useReducer을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
