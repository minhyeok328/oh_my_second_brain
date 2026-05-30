---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'security'
source:
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project_change_react'
---

# Django CSRF

태그: #llm_wiki #django #security

## 한 줄 정의

Django CSRF는 사용자의 세션을 악용한 위조 POST 요청을 막기 위해, 안전하지 않은 요청에 CSRF token 검증을 요구하는 보호 장치다.

## 내 말로 다시 설명

Django에서 로그인 세션 쿠키는 브라우저가 자동으로 보낸다. 그래서 POST, PATCH, DELETE 같은 요청은 "정말 우리 페이지에서 보낸 요청인지"를 확인해야 한다. AJAX나 SPA에서는 `X-CSRFToken` header와 credentials 정책을 함께 맞춰야 한다.

## 언제 쓰는가

- Django session 인증을 사용하는 POST 요청을 만들 때
- 찜 토글, 채팅 전송, 프로필 수정처럼 사용자 상태를 바꾸는 요청을 보낼 때
- React SPA나 vanilla JS fetch에서 Django view로 JSON 요청을 보낼 때

## 언제 쓰면 안 되는가

- token 검증을 귀찮다는 이유로 view 전체에서 끄는 경우
- GET 요청으로 상태를 변경하려는 경우
- 쿠키 기반 인증이 아닌 별도 token 인증 정책을 쓰면서 Django CSRF와 혼동하는 경우

## 프로젝트 예시

[[SKN26 4차 프로젝트 - LG Home]]의 `static\js\api-response.js`는 FormData/JSON POST용 fetch init을 만들 때 `X-CSRFToken`과 `credentials: same-origin`을 함께 붙이는 공통 함수를 둔다.

프론트 QA 평가서에서는 `ApiResponse`와 `fetchJson` 공통화로 챗봇, 찜, 필터 옵션의 실패 UX가 개선됐다고 보되, 세션 만료 401과 모바일 실기기 동작은 별도 확인이 필요하다고 정리했다.

## 자주 헷갈리는 점

- CSRF token은 인증 token이 아니다. 사용자가 누구인지는 session이 판단하고, CSRF는 요청 출처를 방어한다.
- JSON POST도 안전하지 않은 요청이므로 CSRF 대상이다.
- SPA에서 `credentials`를 빼면 session cookie가 안 가서 인증이 풀린 것처럼 보일 수 있다.

## 관련 개념

- [[Django JSON API]]
- [[React API Fetch]]
- [[Django Session과 Auth]]
- [[Django View]]

## 먼저 확인할 질문

- 이 요청은 상태를 바꾸는가?
- 브라우저 요청에 session cookie와 CSRF header가 함께 전달되는가?
- CSRF 실패, 비로그인 401, HTML redirect, JSON parse 실패를 같은 화면 정책으로 구분하고 있는가?
