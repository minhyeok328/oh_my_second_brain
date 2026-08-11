---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'react'
  - 'javascript'
  - 'state'
aliases:
  - 'useEffect'
sources:
  - 'https://react.dev/reference/react/useEffect'
  - 'https://react.dev/learn/you-might-not-need-an-effect'
source_quality: 'primary'
verified: true
id: '20260530000000-d0a4'
---

# useEffect는 외부 시스템과 React 상태를 동기화한다

## 주장

`useEffect`는 렌더링 결과에 맞춰 네트워크 연결, 브라우저 API, 타이머나 비 React 위젯 같은 외부 시스템을 설정하고 정리하는 동기화 경계다. [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]]에서 외부 자원을 구독할 때 setup과 cleanup을 한 과정으로 보고, 데이터 요청이라면 [[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]]의 중복·취소 조건도 함께 설계해야 한다.

## 연결

[[웹 클라이언트 강의]]에는 DOM·이벤트·Fetch 예제가 있지만 React 파일은 확인되지 않았다. 따라서 이 노트의 React 동작 주장은 공식 React 문서에만 근거하며, 강의 링크는 선행 브라우저 개념을 찾기 위한 연결이다.

## 한계와 반례

렌더링만으로 계산할 수 있는 파생 값이나 사용자 이벤트 처리는 Effect가 필요하지 않다. 반응형 의존성을 빠뜨리면 이전 값을 참조하고, 매 렌더마다 새 객체·함수를 의존성으로 만들면 불필요한 재동기화가 생길 수 있다. Effect는 서버 렌더링 중 실행되지 않는다.

## 확인한 근거

- 2026-08-11: React 공식 `useEffect` 참조에서 Effect가 컴포넌트를 외부 시스템과 동기화하고, 의존성 변경 전 cleanup 뒤 setup을 실행하는 범위를 확인했다.
- 2026-08-11: React 공식 ‘You Might Not Need an Effect’ 문서에서 외부 시스템과 동기화하지 않는 파생 계산과 이벤트 로직은 Effect를 피해야 한다는 경계를 확인했다.
