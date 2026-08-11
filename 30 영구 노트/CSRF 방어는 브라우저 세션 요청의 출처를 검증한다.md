---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'django'
  - 'security'
  - 'csrf'
aliases:
  - 'Django CSRF'
sources:
  - 'https://docs.djangoproject.com/en/6.0/ref/csrf/'
  - 'https://docs.djangoproject.com/en/6.0/howto/csrf/#using-csrf-protection-with-ajax'
  - 'C:\MinHyeok\skn26_projects\4th_project\static\js\api-response.js'
source_quality: 'mixed'
verified: true
id: '20260530000000-e926'
---

# CSRF 방어는 브라우저 세션 요청의 출처를 검증한다

## 주장

브라우저가 세션 쿠키를 자동으로 보내는 환경에서는 상태를 바꾸는 요청이 사용자가 의도한 사이트에서 시작됐는지 별도로 확인해야 한다. Django의 CSRF 미들웨어는 토큰을 검사하고, 가능한 경우 `Origin` 또는 HTTPS `Referer`도 신뢰할 출처와 비교한다. 따라서 [[Django JSON API는 화면과 서버 책임을 분리한다]]에 AJAX POST를 붙일 때는 토큰을 `X-CSRFToken` 헤더로 전달하는 규칙까지 요청 계약에 포함해야 한다.

## 연결

[[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]]가 세션 기반 Django API에 상태 변경 요청을 보낼 때도 같은 계약이 필요하다. 프로젝트 코드에서 확인한 적용을 내 관점으로 정리하면, [[SKN26 4차 LG Home AI 가전 상담]]의 공통 요청 모듈은 `credentials: same-origin`과 `X-CSRFToken`을 함께 구성한다.

## 한계와 반례

CSRF 검사는 인증이나 권한 검사를 대신하지 않으며 XSS가 있으면 방어가 무력화될 수 있다. 쿠키를 자동 전송하지 않는 별도 토큰 인증 API는 위협 모델이 다를 수 있고, Django 문서가 밝히듯 중간자 공격 방어에는 HTTPS와 HSTS도 필요하다.

## 확인한 근거

- 2026-08-11: Django 공식 CSRF 참조에서 토큰, `Origin`, HTTPS `Referer` 검증 범위와 안전한 메서드 예외를 확인했다.
- 2026-08-11: Django 공식 AJAX 지침에서 `X-CSRFToken` 헤더와 same-origin 요청 예시를 확인했다.
- 프로젝트 코드 확인(개인 해석): 승인된 `4th_project/static/js/api-response.js`에서 같은 출처 자격 증명과 CSRF 헤더를 공통화한 구현을 확인했다.
