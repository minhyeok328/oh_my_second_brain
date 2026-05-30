---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'devops'
  - 'django'
source:
  - 'C:\lecture'
---

# Procfile

태그: #devops #django #llm_wiki

## 한 줄 정의

플랫폼이 애플리케이션 프로세스를 어떤 명령으로 실행할지 정의하는 파일이다.

## 왜 중요한가

Elastic Beanstalk나 Heroku 같은 플랫폼은 Procfile을 보고 웹 프로세스 시작 명령을 결정한다.

## 핵심 개념

- `web:` 프로세스가 HTTP 요청을 담당한다.
- Django는 보통 Gunicorn WSGI 실행 명령을 둔다.
- 파일은 배포 패키지 루트에 있어야 한다.

## 예제

```text
web: gunicorn config.wsgi:application
```

## 실무 활용

Django 운영 배포, EB zip 패키징, GitHub Actions 배포 산출물 구성에 사용한다.

## 관련 개념

- [[WSGI]]
- [[Gunicorn과 Uvicorn]]
- [[AWS Elastic Beanstalk]]

자료 힌트: 13_react-cicd_workspace/03_gha_cicd/sample_app/Procfile

## 내 말로 다시 설명

Procfile은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[WSGI]], [[Gunicorn과 Uvicorn]], [[AWS Elastic Beanstalk]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- Procfile을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
