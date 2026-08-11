---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'react'
  - 'api'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project_change_react'
source_quality: 'mixed'
verified: false
id: '20260530000000-b93a'
---

# React API Fetch

태그: #llm_wiki #react #api

## 한 줄 정의

React API Fetch는 React 화면에서 서버 JSON API를 호출하고, 로딩·성공·실패·인증 상태를 UI 상태로 반영하는 패턴이다.

## 내 말로 다시 설명

fetch는 단순히 URL을 부르는 함수가 아니다. session cookie, CSRF token, content-type, 401 redirect, JSON parse 실패, network error를 화면 정책으로 정해야 한다. 이 규칙을 페이지마다 흩뿌리면 API 실패 UX가 깨진다.

## 언제 쓰는가

- React SPA가 Django backend에서 검색 결과, 상품 상세, 채팅, 계정 정보를 받아올 때
- POST 요청에 CSRF와 credentials가 필요한 경우
- API 실패를 alert, inline message, redirect 중 하나로 일관되게 처리해야 할 때

## 언제 쓰면 안 되는가

- 서버 렌더링 template context로 충분한 정적 화면인 경우
- API 응답 shape과 에러 shape이 정해지지 않은 상태에서 화면부터 만드는 경우
- 인증 실패를 HTML redirect와 JSON 401로 섞어 처리하는 경우

## 프로젝트 예시

[[SKN26 4차 LG Home AI 가전 상담]]의 공식 프로젝트는 vanilla JS `api-response.js`로 fetch JSON 응답과 CSRF POST init을 공통화했다. 개인 확장 `4th_project_change_react`는 `frontend\src\api\client.ts`에서 `fetchJson`, `jsonPost`, `formPost`, `ApiError`로 React SPA fetch 계층을 분리했다.

프론트 QA 평가서 기준으로 `fetchJson` 통합, 필터 에러 배너, 찜 in-flight 처리는 개선됐지만, 챗봇 세션 만료 401에서 로그인 유도 경로가 명확하지 않은 점은 잔여 리스크로 남았다.

## 실패 조건

- `credentials`를 빼면 session 인증이 유지되지 않는다.
- JSON이 아닌 HTML redirect를 JSON으로 parse하려 하면 화면이 조용히 실패할 수 있다.
- POST인데 `X-CSRFToken`이 없으면 Django에서 거절된다.

## 관련 개념

- [[React SPA]]
- [[Django JSON API]]
- [[Django CSRF]]
- [[useEffect]]

## 먼저 확인할 질문

- 이 API 호출은 GET인가, 상태 변경 POST인가?
- 실패 응답을 사용자가 이해할 수 있는 UI 상태로 바꾸고 있는가?
- 401 또는 세션 만료가 발생했을 때 로그인으로 이동할지, 현재 화면에서 안내할지 정했는가?
