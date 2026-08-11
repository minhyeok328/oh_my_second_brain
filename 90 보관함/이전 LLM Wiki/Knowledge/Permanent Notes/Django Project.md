---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'web_server'
source:
  - 'C:\lecture'
---

# Django Project

태그: #django #web_server #llm_wiki

## 한 줄 정의

Django 설정과 URL 루트를 포함하는 웹 애플리케이션의 최상위 구성이다.

## 왜 중요한가

프로젝트는 여러 앱을 묶고 환경 설정, 미들웨어, DB, 정적 파일 설정을 관리한다.

## 핵심 개념

- `settings.py`가 전역 설정을 담는다.
- `urls.py`가 URL 라우팅의 시작점이다.
- `manage.py`는 명령 실행 진입점이다.

## 예제

```bash
python manage.py runserver
```

## 실무 활용

웹 서버 실습, Docker 이미지화, WSGI/ASGI 배포의 기준 단위다.

## 관련 개념

- [[Django App]]
- [[Django Settings]]
- [[WSGI]]

자료 힌트: 11_web_server_workspace/_01_django_project

## 내 말로 다시 설명

Django Project은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[Django App]], [[Django Settings]], [[WSGI]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- Django Project을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
