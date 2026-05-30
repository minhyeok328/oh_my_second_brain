---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'react'
  - 'hook'
source:
  - 'C:\lecture'
external:
  - 'https://react.dev/reference/react/useEffect'
  - 'https://react.dev/learn/you-might-not-need-an-effect'
---

# useEffect

태그: #llm_wiki #react #hook

## 한 줄 정의

useEffect는 React 컴포넌트가 렌더링된 뒤 외부 시스템과 동기화해야 할 작업을 수행하게 해주는 Hook이다.

## 내 말로 다시 설명

useEffect는 "렌더링 결과를 바깥 세계와 맞추는 장치"다. DOM 제목 변경, 구독 연결, 네트워크 요청, 타이머처럼 React 렌더링만으로 끝나지 않는 일이 있을 때 쓴다. 상태 계산을 effect에 넣으면 불필요한 렌더링과 버그가 늘어난다.

## 언제 쓰는가

- 브라우저 API, timer, event listener, 외부 라이브러리와 동기화할 때
- 서버/API에서 데이터를 가져와 컴포넌트 상태에 반영할 때
- 컴포넌트 mount/unmount에 맞춰 연결과 정리를 해야 할 때

## 언제 쓰면 안 되는가

- props나 state에서 계산 가능한 값을 다시 state로 저장할 때
- 사용자 이벤트 처리로 충분한 로직을 렌더링 후 effect로 미룰 때
- 단순 데이터 fetching을 라우터/쿼리 라이브러리가 더 잘 처리하는 구조일 때

## 의존성 배열 기준

- effect 안에서 읽는 reactive 값은 의존성에 포함한다.
- 의존성을 줄이려고 lint를 끄기보다 함수 위치와 상태 구조를 다시 본다.
- cleanup은 이전 effect의 연결을 정리한다.

## 자주 헷갈리는 점

- 빈 배열은 "한 번만"이 아니라 "이 effect가 reactive 값을 읽지 않는다"는 선언에 가깝다.
- Strict Mode 개발 환경에서는 effect가 두 번 실행되어 cleanup 문제를 드러낼 수 있다.
- fetch effect는 race condition과 abort 처리를 신경 써야 한다.

## 관련 개념

- [[React]]
- [[React Lifecycle]]
- [[React State]]
- [[React API Fetch]]
- [[Custom Hook]]

## 확인 질문

- 이 코드는 외부 시스템 동기화인가, 렌더링 중 계산 가능한 값인가?
- cleanup이 필요한 연결을 만들고 있지는 않은가?

## 외부 참조

- https://react.dev/reference/react/useEffect
- https://react.dev/learn/you-might-not-need-an-effect
