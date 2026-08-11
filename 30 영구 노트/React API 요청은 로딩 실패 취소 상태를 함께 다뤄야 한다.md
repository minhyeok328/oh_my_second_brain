---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'react'
  - 'fetch'
  - 'async-state'
aliases:
  - 'React API Fetch'
sources:
  - 'https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch'
  - 'https://react.dev/learn/synchronizing-with-effects'
source_quality: 'primary'
verified: true
id: '20260530000000-b93a'
---

# React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다

## 주장

React 화면의 API 요청은 성공 데이터만 저장해서는 수명을 표현할 수 없다. 요청 시작의 로딩, 네트워크 오류와 HTTP 실패, 취소 또는 뒤늦게 도착한 응답을 구분해야 [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]]는 경계가 실제 사용자 경험으로 이어진다. `fetch()`는 404 같은 HTTP 오류에서 자동으로 reject하지 않으므로 `Response.ok`를 확인하고, Effect cleanup에서는 요청을 중단하거나 오래된 결과를 무시해야 한다.

## 연결

세션 기반 Django에 상태 변경 요청을 보낸다면 [[CSRF 방어는 브라우저 세션 요청의 출처를 검증한다]]의 헤더 규칙도 요청 상태와 함께 관리해야 한다. [[웹 클라이언트 강의]]의 Fetch 예제는 브라우저 API의 출발점이지만, 실패·취소와 React 수명은 공식 MDN·React 자료로 보완했다.

## 한계와 반례

모든 요청을 컴포넌트 Effect에서 직접 관리할 필요는 없다. React 공식 문서가 지적하듯 프레임워크 데이터 로더나 캐시 계층이 중복 제거, 선로딩과 서버 렌더링을 제공한다면 수명 관리를 그 계층에 맡기는 편이 낫다. 취소는 이미 서버에서 시작된 부수 효과를 되돌리는 트랜잭션도 아니다.

## 확인한 근거

- 2026-08-11: MDN Fetch API 문서에서 HTTP 오류 시 fulfilled 응답이 올 수 있어 `Response.ok` 검사가 필요하고 `AbortController`로 요청을 취소할 수 있음을 확인했다.
- 2026-08-11: React 공식 Synchronizing with Effects 문서에서 fetch cleanup이 요청을 중단하거나 오래된 결과를 무시해야 하며 수동 Effect fetch에는 캐시·waterfall 한계가 있음을 확인했다.
