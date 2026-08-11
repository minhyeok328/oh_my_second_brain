---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'django'
  - 'api'
  - 'json'
aliases:
  - 'Django JSON API'
sources:
  - 'https://docs.djangoproject.com/en/6.0/ref/request-response/#jsonresponse-objects'
  - 'C:\MinHyeok\skn26_projects\4th_project\api\views.py'
source_quality: 'mixed'
verified: true
id: '20260530000000-f530'
---

# Django JSON API는 화면과 서버 책임을 분리한다

## 주장

Django view가 템플릿 대신 `JsonResponse`로 직렬화 가능한 데이터를 반환하면, 서버는 인증·조회·상태 변경 결과를 전달하고 브라우저는 그 결과를 화면으로 표현하는 경계를 만들 수 있다. 이는 `JsonResponse` 자체의 필수 구조가 아니라, [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]]와 서버 사이의 책임을 명시하기 위한 내 설계 해석이다.

## 연결

클라이언트 쪽 [[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]]는 상태 코드와 JSON 형태를 UI 상태로 번역한다. 세션 쿠키를 사용하는 변경 요청에는 [[CSRF 방어는 브라우저 세션 요청의 출처를 검증한다]]의 계약도 적용된다. 프로젝트 코드에서 확인한 적용을 내 관점으로 정리하면, [[SKN26 4차 LG Home AI 가전 상담]]의 `api/views.py`는 인증·입력 검사를 마친 뒤 채팅 결과와 상태 코드를 JSON으로 반환한다.

## 한계와 반례

`JsonResponse`를 쓴다고 안정적인 API 계약이 자동으로 생기지는 않는다. 성공·검증 실패·인증 실패의 상태 코드와 응답 형태를 따로 정해야 하며, 상호작용이 적은 페이지는 서버 템플릿이 더 단순할 수 있다.

## 확인한 근거

- 2026-08-11: Django 공식 request/response 참조에서 `JsonResponse`가 JSON 인코딩과 `application/json` 응답을 제공하는 범위를 확인했다.
- 프로젝트 코드 확인(개인 해석): 승인된 `4th_project/api/views.py`에서 요청 검증, HTTP 상태 코드, JSON 응답을 한 endpoint 경계에 둔 사례를 확인했다.
