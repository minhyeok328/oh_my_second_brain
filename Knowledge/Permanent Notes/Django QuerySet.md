---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'orm'
  - 'database'
source:
  - 'C:\lecture'
external:
  - 'https://docs.djangoproject.com/en/6.0/ref/models/querysets/'
---

# Django QuerySet

태그: #llm_wiki #django #orm #database

## 한 줄 정의

Django QuerySet은 Django ORM에서 데이터베이스 조회 조건을 누적하고, 필요할 때 SQL로 평가되는 지연 실행 객체다.

## 내 말로 다시 설명

QuerySet은 "아직 실행되지 않은 DB 질문"이다. `filter()`, `exclude()`, `order_by()`를 이어 붙이면 질문이 더 구체화되고, 반복하거나 `list()`로 만들거나 값을 꺼낼 때 실제 query가 실행된다. Django 성능 문제는 QuerySet이 언제 평가되는지 모를 때 자주 생긴다.

## 핵심 개념

- lazy evaluation: QuerySet은 생성만으로 DB에 가지 않는다.
- chaining: 조건을 이어 붙여도 원본 QuerySet은 보통 변경되지 않는다.
- filtering: `filter`, `exclude`, field lookup으로 WHERE를 만든다.
- related loading: `select_related`, `prefetch_related`로 N+1 query를 줄인다.
- aggregation: `annotate`, `aggregate`로 DB에서 집계한다.

## 언제 쓰는가

- [[Django ORM Model]] 데이터를 조건별로 조회할 때
- View에서 목록, 상세, 검색, 페이지네이션을 만들 때
- DB가 잘하는 필터링과 정렬을 Python 반복문 대신 맡길 때

## 언제 쓰면 안 되는가

- 이미 메모리에 있는 작은 리스트를 단순 변환하는 경우
- 복잡한 분석 처리를 ORM으로 억지로 표현해 SQL이 불투명해지는 경우
- QuerySet 평가 시점을 모른 채 template에서 반복 접근하는 경우

## 자주 헷갈리는 점

- `get()`은 객체 하나를 바로 평가해서 반환하고, 없거나 여러 개면 예외가 난다.
- `filter()`는 0개여도 QuerySet을 반환한다.
- QuerySet을 template에서 반복하면서 related field를 매번 읽으면 N+1 query가 될 수 있다.

## 작은 예제

```python
posts = (
    Post.objects
    .filter(is_public=True)
    .select_related("author")
    .order_by("-created_at")
)
```

## 관련 개념

- [[Django ORM Model]]
- [[Django View]]
- [[Django Migration]]
- [[SQL SELECT와 WHERE]]
- [[SQL JOIN]]

## 확인 질문

- 이 QuerySet은 어느 줄에서 실제 DB에 접근하는가?
- related object 접근으로 query가 반복되지 않는가?

## 외부 참조

- https://docs.djangoproject.com/en/6.0/ref/models/querysets/
