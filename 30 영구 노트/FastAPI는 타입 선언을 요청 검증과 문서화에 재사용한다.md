---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'fastapi'
  - 'api'
  - 'validation'
aliases:
  - 'FastAPI'
sources:
  - 'https://fastapi.tiangolo.com/tutorial/body/'
  - 'https://fastapi.tiangolo.com/features/'
  - 'C:\MinHyeok\skn26_projects\2nd_project\pipeline\main.py'
  - 'C:\MinHyeok\skn26_projects\2nd_project\pipeline\schemas\health.py'
source_quality: 'mixed'
verified: true
id: '20260530000000-46e8'
---

# FastAPI는 타입 선언을 요청 검증과 문서화에 재사용한다

## 주장

FastAPI는 경로 함수의 Python 타입과 Pydantic 모델을 요청 데이터의 요구 조건으로 읽고, 같은 선언으로 변환·검증과 OpenAPI 스키마를 만든다. 입력 계약을 코드와 문서에 따로 중복하지 않는 것이 핵심이며, [[Django JSON API는 화면과 서버 책임을 분리한다]]와 비교하면 프레임워크가 요청 스키마 문서화를 더 직접 맡는 선택이다.

## 연결

외부 서비스가 이 API를 호출할 때는 [[HTTP 요청은 타임아웃과 실패 처리를 기본값으로 가져야 한다]]의 클라이언트 경계가 필요하다. 프로젝트 코드에서 확인한 적용을 내 관점으로 정리하면, [[SKN26 2차 신용카드 고객 이탈 분석]]은 `HealthResponse` 타입을 응답 모델로 지정하고 데이터 조회의 불리언 쿼리 파라미터를 선언했다.

## 한계와 반례

타입 검증은 사용자 권한, 데이터 간 일관성, 호출 가능 시점 같은 비즈니스 규칙을 대신하지 않는다. 또한 원시 `Request`를 직접 읽는 값은 자동 검증·변환·OpenAPI 문서화의 대상이 아니므로 같은 이점을 얻지 못한다.

## 확인한 근거

- 2026-08-11: FastAPI 공식 Request Body 문서에서 Pydantic 모델 하나가 JSON 읽기, 변환, 검증, JSON Schema와 자동 문서에 재사용되는 범위를 확인했다.
- 2026-08-11: FastAPI 공식 Features 문서에서 Python 타입 선언, OpenAPI, JSON Schema와 자동 문서의 관계를 확인했다.
- 프로젝트 코드 확인(개인 해석): 승인된 `2nd_project/pipeline`에서 타입 선언, Pydantic 응답 모델과 라우터 등록 사례를 확인했다.
