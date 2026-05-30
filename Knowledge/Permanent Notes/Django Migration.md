---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'database'
source:
  - 'C:\lecture'
---

# Django Migration

태그: #django #database #llm_wiki

## 한 줄 정의

Model 변경 사항을 데이터베이스 스키마 변경 파일로 기록하고 적용하는 시스템이다.

## 왜 중요한가

코드의 모델 정의와 실제 DB 구조를 일관되게 유지한다.

## 핵심 개념

- `makemigrations`가 변경 파일을 만든다.
- `migrate`가 DB에 적용한다.
- 운영 데이터가 있는 스키마 변경은 신중히 설계한다.

## 예제

```bash
python manage.py makemigrations
python manage.py migrate
```

## 실무 활용

모델 필드 추가, 관계 변경, 배포 시 DB 업데이트에 사용한다.

## 관련 개념

- [[Django ORM Model]]
- [[SQL DDL]]
- [[Docker Container]]

자료 힌트: 11_web_server_workspace/_03_django_orm

## 내 말로 다시 설명

Django Migration은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[Django ORM Model]], [[SQL DDL]], [[Docker Container]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- Django Migration을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
