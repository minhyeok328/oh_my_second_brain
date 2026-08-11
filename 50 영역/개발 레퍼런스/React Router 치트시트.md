---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'react'
  - 'routing'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://reactrouter.com/start/declarative/routing'
source_quality: 'mixed'
verified: false
id: '20260530000000-a62a'
---

# React Router 치트시트

## 용도

React Router의 선언형 라우팅에서 URL과 화면, 중첩 경로와 이동을 연결하는 요소를 구분한다.

## 빠른 참조

- `<BrowserRouter>`: 브라우저 history를 사용하는 라우터 컨텍스트 제공
- `<Routes>`와 `<Route path="..." element={<Page />}>`: URL segment와 UI 연결
- `<Outlet />`: 일치한 자식 route를 부모 layout 안에 렌더링
- `useParams()`: 동적 segment 값 읽기
- `useNavigate()`: 이벤트 처리 중 프로그래밍 방식 이동
- `<Link to="...">`: 문서 전체 새로고침 없이 route 링크 제공

## 검증 범위

- 2026-08-11: React Router 공식 최신 Declarative Routing 문서에서 위 구성요소를 확인했다.
- 설치된 major 버전, `react-router`와 `react-router-dom`의 import 경로, Data/Framework mode API는 확인하지 않았다. 프로젝트의 `package.json`과 해당 버전 문서를 먼저 확인한다.

## 관련 노트

- [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]]
- [[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]]
- [[20 소스 노트/강의/React와 CI CD 강의|React와 CI CD 강의]]
