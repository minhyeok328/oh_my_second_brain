---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'react'
  - 'frontend'
source:
  - 'C:\MinHyeok\skn26_4th_1st\4th_project_change_react'
---

# React SPA

태그: #llm_wiki #react #frontend

## 한 줄 정의

React SPA는 서버가 HTML 페이지를 매번 렌더링하는 대신, 브라우저에서 React가 라우팅과 화면 상태를 관리하고 서버는 주로 JSON API를 제공하는 구조다.

## 내 말로 다시 설명

SSR Django 템플릿은 서버가 화면을 조립한다. React SPA는 첫 HTML 이후 화면 전환, fetch, 상태 관리를 프론트가 맡는다. 대신 API 계약, 인증 상태, CSRF, fallback 라우팅이 명확해야 한다.

## 언제 쓰는가

- 화면 전환과 상호작용이 많아 프론트 상태 관리가 중요할 때
- Django를 API 서버로 두고 UI를 React/TypeScript로 분리하고 싶을 때
- 검색, 상세, 채팅, 계정 페이지가 같은 API client와 라우팅 정책을 공유해야 할 때

## 언제 쓰면 안 되는가

- 서버 템플릿 몇 개로 충분하고 프론트 상태가 단순한 경우
- JSON API 계약을 정리하지 않은 상태에서 화면만 React로 옮기려는 경우
- 인증/CSRF/session 처리를 브라우저 fetch 정책으로 검증하지 않은 경우

## 프로젝트 예시

[[SKN26 4차 프로젝트 - LG Home]]의 공식 산출물은 Django SSR이다. 이후 개인 확장 `4th_project_change_react`에서 React + TypeScript + Tailwind SPA와 Django JSON API 구조로 분리했다.

이 전환을 해보며 Django는 화면 전체를 직접 조립하기보다 DB와 프론트엔드 사이에서 JSON API를 제공하는 징검다리 역할에 집중할 때 책임이 더 명확해진다고 느꼈다.

## 자주 헷갈리는 점

- SPA 전환은 "HTML을 React로 바꾸기"가 아니라 렌더링 책임과 API 책임을 재분배하는 일이다.
- Django session 인증을 계속 쓰면 `credentials`, CSRF token, 401 처리 규칙이 필요하다.
- 기존 URL을 유지하려면 SPA fallback과 API/static/media 경로 예외가 필요하다.

## 관련 개념

- [[React API Fetch]]
- [[React Router]]
- [[Django JSON API]]
- [[Django CSRF]]

## 먼저 확인할 질문

- 이 화면의 데이터는 어떤 JSON API에서 오며, 실패 응답은 어떻게 표시되는가?
- 기존 사용자 URL과 로그인 흐름을 유지할 것인가?
- Django가 계속 맡아야 할 책임은 DB 조회, 인증, 권한, 파일 제공, LLM 호출 중 어디까지인가?
