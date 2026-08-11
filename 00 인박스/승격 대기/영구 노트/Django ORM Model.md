---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'django'
  - 'orm'
  - 'database'
source:
  - 'C:\lecture'
external:
  - 'https://docs.djangoproject.com/en/6.0/topics/db/models/'
source_quality: 'mixed'
verified: false
id: '20260530000000-8593'
---

# Django ORM Model

태그: #llm_wiki #django #orm #database

## 한 줄 정의

Django ORM Model은 Python 클래스로 데이터베이스 테이블 구조와 비즈니스 객체를 정의하는 Django의 데이터 모델 계층이다.

## 내 말로 다시 설명

Model은 "DB 테이블을 Python 코드로 선언한 것"에 가깝다. 필드는 컬럼이 되고, 클래스는 테이블이 되며, migration은 그 선언을 실제 DB schema 변화로 옮긴다. Django 앱에서 데이터의 의미와 제약을 가장 오래 보존하는 장소다.

## 핵심 개념

- field: 컬럼 타입과 제약을 정의한다.
- relationship: ForeignKey, OneToOne, ManyToMany로 테이블 관계를 표현한다.
- migration: 모델 변경을 DB schema 변경 이력으로 기록한다.
- manager/queryset: 모델 데이터를 조회하고 조작하는 API다.
- admin/form/view: 모델 정의를 기준으로 화면과 관리 기능이 연결된다.

## 언제 쓰는가

- Django 앱에서 저장해야 할 핵심 도메인 개념이 있을 때
- [[Django QuerySet]]으로 조회/필터링할 데이터가 있을 때
- 인증, 게시판, 챗봇 대화 로그처럼 DB에 남길 상태가 있을 때

## 언제 쓰면 안 되는가

- API 응답 임시 구조처럼 저장하지 않을 데이터
- 복잡한 분석용 임시 테이블을 앱 모델로 억지로 표현해야 하는 경우
- migration 전략 없이 운영 DB 구조를 자주 흔드는 경우

## 자주 헷갈리는 점

- 모델 클래스를 바꿨다고 DB가 바로 바뀌지 않는다. `makemigrations`와 `migrate`가 필요하다.
- `null=True`는 DB 레벨, `blank=True`는 form validation 레벨 의미가 강하다.
- relationship은 편하지만 잘못 쓰면 N+1 query가 생긴다.

## 관련 개념

- [[Django Migration]]
- [[Django QuerySet]]
- [[Django View]]
- [[Django Form]]
- [[관계형 데이터베이스]]

## 확인 질문

- 이 필드는 도메인 규칙인가, 화면 입력 편의를 위한 값인가?
- 관계를 모델에 둘 때 조회 성능과 삭제 정책을 고려했는가?

## 외부 참조

- https://docs.djangoproject.com/en/6.0/topics/db/models/
