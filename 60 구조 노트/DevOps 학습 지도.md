---
id: '20260811140012-a00c'
type: 'structure'
status: 'growing'
created: '2026-08-11'
updated: '2026-08-11'
tags:
  - 'learning_map'
  - 'devops'
aliases: []
sources:
  - '[[20 소스 노트/강의/DevOps와 배포 강의|DevOps와 배포 강의]]'
  - '[[20 소스 노트/강의/Git 기초 강의|Git 기초 강의]]'
source_quality: 'mixed'
verified: false
---

# DevOps 학습 지도

## 출발점

- [[20 소스 노트/강의/DevOps와 배포 강의|DevOps와 배포 강의]]: EC2, Nginx, Docker·Compose와 WSGI·ASGI를 배포 경계의 조합으로 따라간다.
- [[20 소스 노트/강의/Git 기초 강의|Git 기초 강의]]: 승인 경로에 독립 Git 강의가 없다는 근거 공백을 확인하고 Git 지식을 이 강의에서 파생하지 않는다.

## 핵심 연결

1. [[Docker Compose는 여러 컨테이너의 실행 계약을 한곳에 모은다]] — 서비스, 포트, 환경 변수와 네트워크 구성을 한 실행 계약으로 본다.
2. [[50 영역/개발 레퍼런스/Docker CLI|Docker CLI]] → [[50 영역/개발 레퍼런스/Docker Compose|Docker Compose 명령 참조]] — 컨테이너 단위 확인에서 여러 서비스 실행으로 확장한다.
3. [[50 영역/개발 레퍼런스/WSGI ASGI 배포 명령어|WSGI ASGI 배포 명령어]] — 애플리케이션 서버의 실행 모델을 비교한다.
4. [[50 영역/개발 레퍼런스/Git 명령어 모음|Git 명령어 모음]] — Git 명령은 강의 근거가 아니라 별도 공식 자료 기반 참조로 확인한다.

## 프로젝트에서의 적용

- [[SKN26 2차 신용카드 고객 이탈 분석]]: MySQL·FastAPI·MLflow·Streamlit을 Docker Compose 실행 구성으로 묶었다.
- [[SKN26 Final HumouR AI HR 채용 보조]]: 팀 시스템이 React·Django·Celery와 AWS 배포 구조를 사용했다.

## 다음 질문

- [[질문 인박스#Compose 시작 순서와 readiness]]에서 컨테이너 시작과 애플리케이션 준비 완료를 어떤 healthcheck로 구분할 것인가?
