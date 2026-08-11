---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'django'
  - 'orm'
  - 'query'
aliases:
  - 'Django QuerySet'
sources:
  - 'https://docs.djangoproject.com/en/6.0/ref/models/querysets/#when-querysets-are-evaluated'
  - 'C:\MinHyeok\skn26_projects\4th_project\products\models.py'
source_quality: 'mixed'
verified: true
id: '20260530000000-5c76'
---

# QuerySet은 평가 시점을 늦춰 쿼리 조합을 가능하게 한다

## 주장

QuerySet은 `filter()` 같은 조건을 바로 실행 결과로 굳히지 않고 새 조회 표현으로 이어 붙일 수 있게 한다. 반복, `list()`, `len()`, 불리언 검사처럼 결과가 필요한 시점에 데이터베이스를 조회하므로, 요청에서 모은 조건을 [[Django ORM 모델은 데이터 구조와 제약을 코드로 표현한다]]의 필드에 맞춰 단계적으로 조합할 수 있다.

## 연결

[[Django JSON API는 화면과 서버 책임을 분리한다]]는 이렇게 조합한 결과를 응답 데이터로 바꿀 수 있다. 프로젝트 코드에서 확인한 적용을 내 관점으로 정리하면, [[SKN26 4차 LG Home AI 가전 상담]]의 상품 검색은 조건 사전을 만든 뒤 한 번의 `filter(**filters)`로 QuerySet을 구성한다.

## 한계와 반례

지연 평가가 쿼리 수를 자동으로 줄여 주지는 않는다. 반복문 안에서 관련 객체를 계속 읽으면 N+1 조회가 생길 수 있고, `len()`이나 불리언 검사도 평가를 일으키므로 실행 시점과 생성된 SQL을 따로 확인해야 한다. 이미 결과 전체가 필요한 작은 컬렉션이라면 지연 자체가 실질적인 이점이 아닐 수도 있다.

## 확인한 근거

- 2026-08-11: Django 공식 QuerySet API에서 QuerySet을 구성·필터링하는 동안 데이터베이스에 접근하지 않으며 반복, `list()`, `len()`, 불리언 검사 등이 평가를 일으키는 조건을 확인했다.
- 프로젝트 코드 확인(개인 해석): 승인된 `4th_project/products/models.py`에서 조건을 모아 `model.objects.filter(**filters)`로 조회하는 구현을 확인했다.
