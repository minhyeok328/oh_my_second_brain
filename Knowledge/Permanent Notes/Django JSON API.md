---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'api'
source:
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project_change_react'
---

# Django JSON API

태그: #llm_wiki #django #api

## 한 줄 정의

Django JSON API는 Django view가 HTML template 대신 JSON 응답을 반환해, JavaScript, React, 외부 클라이언트가 데이터를 사용하게 하는 인터페이스다.

## 내 말로 다시 설명

Django는 서버 렌더링도 잘하지만, 필요한 순간에는 `JsonResponse`로 작은 API를 제공할 수 있다. 채팅 전송, 찜 토글, 검색 결과 조회처럼 화면 일부만 바꾸는 기능은 JSON API로 분리하면 프론트 코드가 다루기 쉽다.

## 언제 쓰는가

- Django SSR 화면에서 AJAX로 일부 기능만 갱신할 때
- React SPA가 Django backend에서 데이터를 받아 렌더링할 때
- 챗봇처럼 요청-응답이 페이지 새로고침 없이 이어져야 할 때

## 언제 쓰면 안 되는가

- HTML template context로 충분한 단순 페이지를 불필요하게 API화하는 경우
- 인증 실패, validation 실패, 서버 오류의 JSON shape이 정해지지 않은 경우
- view마다 응답 키와 에러 처리가 제각각인 경우

## 프로젝트 예시

[[SKN26 4차 프로젝트 - LG Home]]의 공식 프로젝트에서는 `api\views.py`의 `send_chat`, `favorite`, `check_favorite`가 JSON 응답을 반환한다. 개인 확장 `4th_project_change_react`에서는 검색, 상품 상세, 채팅, 계정 기능을 SPA용 JSON API로 더 넓게 분리했다.

React SPA로 재공학하면서 Django의 책임은 template 렌더링보다 DB, 인증, LLM 호출 결과를 프론트엔드가 소비할 수 있는 JSON 형태로 이어주는 쪽에 가깝다고 정리했다.

## 자주 헷갈리는 점

- JSON API를 만든다고 반드시 Django REST Framework가 필요한 것은 아니다.
- 로그인 실패는 HTML redirect와 JSON 401 중 어느 방식을 쓸지 화면 구조에 맞춰 정해야 한다.
- API 응답 shape이 안정적이어야 프론트 타입과 에러 처리가 단순해진다.

## 관련 개념

- [[Django View]]
- [[Django CSRF]]
- [[React API Fetch]]
- [[React SPA]]

## 먼저 확인할 질문

- 이 endpoint의 성공/실패 응답 JSON shape이 문서화되어 있는가?
- 프론트가 redirect, 401, parse error, network error를 구분해서 처리하는가?
- 이 API는 화면 렌더링 책임까지 가지는가, 아니면 프론트가 렌더링할 데이터를 넘기는 데 집중하는가?
