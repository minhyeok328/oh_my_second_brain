---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'react'
  - 'hooks'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://react.dev/reference/react/hooks'
  - 'https://react.dev/reference/react/useEffect'
source_quality: 'mixed'
verified: false
id: '20260530000000-67f9'
---

# React Hooks 치트시트

## 용도

React 컴포넌트에서 상태, 외부 동기화, 참조와 공유 값을 다룰 때 Hook의 역할을 구분한다.

## 빠른 참조

- `useState`: 렌더링에 쓰이는 지역 상태 보관
- `useReducer`: 여러 상태 전이를 reducer로 모아 관리
- `useEffect`: React 밖의 시스템과 동기화하고 필요하면 cleanup 반환
- `useRef`: 렌더링을 유발하지 않는 참조나 DOM 참조 보관
- `useContext`: 가까운 provider가 제공한 context 값 읽기
- `useMemo`, `useCallback`: 필요한 경우 계산 결과나 함수 정의를 재사용하는 성능 최적화 도구

## 사용 전 확인

- Hook은 컴포넌트 또는 사용자 정의 Hook의 최상위에서 호출한다.
- `useEffect`는 파생 상태 계산이 아니라 외부 시스템 동기화가 필요한지 먼저 확인한다.
- memoization은 동작 보장이 아니라 최적화이므로 실제 병목을 측정한 뒤 적용한다.

## 검증 범위

- 2026-08-11: React 공식 Hooks와 `useEffect` 레퍼런스에서 위 역할과 호출 규칙을 확인했다.
- React 버전, 컴파일러 설정, Server Components와 프레임워크별 데이터 로딩 방식은 확인하지 않았다.

## 관련 노트

- [[useEffect는 외부 시스템과 React 상태를 동기화한다]]
- [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]]
- [[20 소스 노트/강의/React와 CI CD 강의|React와 CI CD 강의]]
