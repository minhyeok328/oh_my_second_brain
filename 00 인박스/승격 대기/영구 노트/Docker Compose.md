---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'docker'
  - 'devops'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project'
external:
  - 'https://docs.docker.com/compose/'
source_quality: 'mixed'
verified: false
id: '20260530000000-6aaa'
---

# Docker Compose

태그: #llm_wiki #docker #devops

## 한 줄 정의

Docker Compose는 여러 컨테이너 서비스, 네트워크, 볼륨, 환경변수를 하나의 설정으로 함께 실행하는 도구다.

## 내 말로 다시 설명

ML 프로젝트는 Streamlit, MLflow, DB, pipeline API처럼 여러 프로세스가 동시에 필요하다. Docker Compose는 "내 PC에서 순서대로 띄우기"를 "한 명령으로 같은 조합 실행하기"로 바꿔준다.

## 언제 쓰는가

- API 서버, dashboard, DB, MLflow를 함께 띄워야 할 때
- 팀원이 같은 포트와 환경변수로 프로젝트를 실행해야 할 때
- 데이터 볼륨과 서비스 네트워크를 명시해야 할 때

## 언제 쓰면 안 되는가

- 단일 Python script나 notebook으로 충분한 경우
- readiness check 없이 `depends_on`만 믿고 DB 준비 전에 API가 실행되는 경우
- secret을 compose 파일에 직접 적는 경우

## 프로젝트 예시

[[SKN26 2차 신용카드 고객 이탈 분석]]은 Docker Compose로 Streamlit dashboard, MLflow, pipeline API, DB를 함께 실행하도록 README에 안내한다. 서비스 접속 포트는 Streamlit, MLflow, Pipeline API가 분리되어 있다.

## 실패 조건

- `depends_on`은 컨테이너 시작 순서를 보장할 뿐, DB가 query 가능해졌다는 뜻은 아니다.
- volume 경로를 정리하지 않으면 MLflow artifact나 DB 데이터가 재실행 때 사라진다.
- host port 충돌을 확인하지 않으면 팀원마다 실행 결과가 달라진다.

## 관련 개념

- [[Docker Container]]
- [[Docker Volume]]
- [[FastAPI]]
- [[MLflow]]
- [[Streamlit 기본 UI]]

## 먼저 확인할 질문

- 각 서비스가 준비되었는지 확인하는 health/readiness 기준이 있는가?
- `.env`와 volume이 재현 가능한 실행을 보장하는가?

## 외부 참조

- https://docs.docker.com/compose/
