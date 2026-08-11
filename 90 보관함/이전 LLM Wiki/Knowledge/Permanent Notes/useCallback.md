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
  - 'performance'
source:
  - 'C:\lecture'
---

# useCallback

태그: #react #hook #performance #llm_wiki

## 한 줄 정의

함수 참조를 의존성이 바뀔 때만 새로 만들도록 메모이제이션하는 Hook이다.

## 왜 중요한가

하위 컴포넌트가 함수 props 변경 때문에 불필요하게 렌더링되는 상황을 줄일 수 있다.

## 핵심 개념

- 반환값은 메모이제이션된 함수다.
- 의존성 배열을 정확히 관리해야 한다.
- React.memo와 함께 쓰이는 경우가 많다.

## 예제

```jsx
const onClick = useCallback(() => save(id), [id]);
```

## 실무 활용

컴포넌트 합성, 이벤트 핸들러 전달, 최적화가 필요한 큰 UI 트리에 사용한다.

## 관련 개념

- [[useMemo]]
- [[React Event Handling]]
- [[Component Composition]]

자료 힌트: 13_react-cicd_workspace/01_react/03_hooks/04_useCallBack

## 내 말로 다시 설명

useCallback은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[useMemo]], [[React Event Handling]], [[Component Composition]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- useCallback을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
