---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'web'
  - 'api'
source:
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-46e8'
---

# FastAPI

태그: #llm_wiki #web #api

## 한 줄 정의

FastAPI는 Python 타입 힌트를 기반으로 HTTP API, 요청/응답 스키마, 자동 문서를 빠르게 만들 수 있는 웹 프레임워크다.

## 내 말로 다시 설명

FastAPI는 데이터 파이프라인이나 ML 모델을 "함수"에서 "서비스"로 꺼내는 경량 API 레이어로 쓰기 좋다. Django처럼 전체 웹 서비스 틀을 만들기보다, health check, dataset 조회, prediction endpoint처럼 독립 API를 빠르게 노출하는 데 잘 맞는다.

## 언제 쓰는가

- ML pipeline, ETL, 모델 추론을 API로 감싸야 할 때
- `/docs`에서 API 동작을 확인하고 팀원과 공유해야 할 때
- Docker Compose 안에서 별도 pipeline service를 띄워야 할 때

## 언제 쓰면 안 되는가

- 복잡한 사용자 인증, 관리자, 템플릿, ORM 중심 서비스가 이미 Django로 잡혀 있는 경우
- API 스키마와 에러 응답 정책이 없이 endpoint만 빠르게 늘리는 경우
- batch로 충분한 ETL을 굳이 HTTP API로 감싸는 경우

## 프로젝트 예시

[[SKN26 2차 신용카드 고객 이탈 분석]]의 `pipeline\main.py`는 FastAPI 앱을 만들고 health router와 creditcard dataset router를 등록해 pipeline 상태와 데이터를 확인하게 한다.

## 자주 헷갈리는 점

- FastAPI는 데이터 검증을 자동으로 해주지만, 비즈니스 검증을 대신하지는 않는다.
- API 서버와 ETL 실행 프로세스는 같은 코드베이스에 있어도 실행 책임이 다르다.
- Docker Compose에서 포트, 환경변수, DB 연결 준비 순서를 확인해야 한다.

## 관련 개념

- [[OpenAPI]]
- [[Docker Compose]]
- [[MLflow]]
- [[Streamlit 기본 UI]]

## 먼저 확인할 질문

- 이 기능은 notebook 함수로 충분한가, 외부에서 호출할 API가 필요한가?
- API 응답은 dashboard가 바로 쓰기 좋은 구조인가?
