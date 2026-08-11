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
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-5c76'
---

# Django QuerySet

태그: #llm_wiki #django #orm

## 한 줄 정의

Django QuerySet은 Django ORM에서 DB 조회 조건을 지연 평가되는 Python 객체로 표현한 것이다.

## 내 말로 다시 설명

QuerySet은 SQL을 바로 실행한 결과가 아니라 "이런 조건으로 조회하겠다"는 쿼리 표현이다. 조건을 체이닝하며 좁힐 수 있고, 실제 평가 시점에 DB query가 실행된다.

## 언제 쓰는가

- 사용자 필터 조건을 ORM 조회로 바꿀 때
- 로그인 사용자 소유 데이터만 조회해야 할 때
- `__in`, `__icontains`, `gte`, `lte` 같은 lookup으로 동적 검색 조건을 구성할 때

## 언제 쓰면 안 되는가

- 사용자가 준 필드명을 검증 없이 ORM lookup key로 만드는 경우
- 반복문 안에서 관련 객체를 계속 조회해 N+1 query가 생기는 경우
- QuerySet 평가 시점을 모른 채 캐싱이나 pagination을 섞는 경우

## 프로젝트 예시

[[SKN26 4차 LG Home AI 가전 상담]]은 제품군별 상품 검색 조건을 Django ORM lookup으로 변환한다. `common\llm.py`의 조건 병합 로직은 `gte`, `lte`, `in`, `icontains`의 병합 규칙을 분리해 자연어 슬롯을 검색 조건으로 바꾼다.

## 실패 조건

- 빈 값 조건을 제거하지 않으면 의도치 않은 전체 검색이나 0건 검색이 생긴다.
- `in` 조건을 단순 덮어쓰면 이전 조건과 새 조건의 교집합 의미가 사라진다.
- 사용자 입력을 lookup key로 직접 허용하면 예측 불가능한 필터가 생긴다.

## 관련 개념

- [[Django ORM Model]]
- [[Django View]]
- [[Django JSON API]]
- [[함수 호출은 자연어 요청을 구조화된 도구 입력으로 바꾼다]]

## 먼저 확인할 질문

- 이 조건은 정확 검색, 범위 검색, 포함 검색 중 무엇인가?
- QuerySet이 실제로 실행되는 시점과 query 수를 확인했는가?
