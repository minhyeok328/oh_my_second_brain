---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'sql'
  - 'database'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders\DB_Side\DBLoader.py'
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders\main.py'
source_quality: 'mixed'
verified: false
id: '20260530000000-84db'
---

# SQL SELECT와 WHERE

태그: #sql #database #llm_wiki

## 한 줄 정의

`SELECT`는 테이블에서 필요한 컬럼을 고르고, `WHERE`는 필요한 행만 남기는 SQL 조회의 기본 구문이다.

## 왜 중요한가

서비스 화면, 분석 리포트, 모델 학습 데이터는 대부분 "필요한 데이터를 정확히 가져오는가"에서 출발한다. 조회 조건이 느슨하면 사용자가 엉뚱한 후보를 보게 되고, 조건이 과하면 실제로 존재하는 데이터가 검색되지 않는다.

## 핵심 개념

- `SELECT`는 반환할 컬럼을 정한다.
- `FROM`은 조회할 테이블을 정한다.
- `WHERE`는 행 단위 조건을 적용한다.
- `LIKE`는 부분 문자열 검색에 쓰지만 wildcard와 escaping을 신경 써야 한다.
- `ORDER BY`, `LIMIT`은 결과 순서와 개수를 통제한다.
- 사용자 입력이 조건에 들어가면 parameterized query를 우선한다.

## 프로젝트 예시

[[SKN26 1차 차량 운영비 프로젝트]]에서는 차량 모델명 검색에 `WHERE model_name LIKE ...` 흐름을 사용했다.

```sql
select *
from car_oil
where model_name like '%아반떼%'
```

`main.py`에서는 정비 부품 계산을 위해 필요한 컬럼만 가져온다.

```sql
SELECT part_name, cycle_km, price_tierA, price_tierB, price_tierC
FROM tco_system.parts
```

첫 번째 쿼리는 검색 UX에는 편하지만 사용자 입력을 직접 문자열에 넣으면 위험하다. 두 번째 쿼리는 계산에 필요한 컬럼만 가져와 화면/계산 코드의 의존성을 줄인다.

## 언제 쓰는가

- 모델명, 사용자명, 상품명처럼 조건 검색이 필요할 때
- 계산이나 화면 출력에 필요한 컬럼만 가져오고 싶을 때
- 대시보드 필터, 검색 결과, 추천 후보를 DB에서 좁힐 때
- API 응답 전에 DB row를 조회해야 할 때

## 언제 쓰면 안 되는가

- 여러 테이블 관계를 함께 봐야 하는데 단일 테이블 `WHERE`만으로 억지로 처리할 때
- 사용자 입력을 검증하지 않고 문자열 조립으로 조건에 넣을 때
- 대량 테이블에서 index 없이 `%keyword%` 검색을 무제한 수행할 때

## 실패 조건

- `WHERE` 조건이 없으면 필요 이상으로 많은 row를 가져온다.
- `%검색어%`는 편하지만 앞 wildcard 때문에 index 활용이 어려울 수 있다.
- 모델명 검색처럼 유사 문자열이 많은 데이터는 후보가 과다하게 나올 수 있다.
- f-string SQL은 따옴표가 들어간 입력이나 SQL injection에 취약하다.
- `SELECT *`에 의존하면 컬럼 순서 변경이 Python tuple index 버그로 이어질 수 있다.

## 관련 개념

- [[MySQL Connector Python]]
- [[SQL DML]]
- [[SQL JOIN]]
- [[Pandas 인덱싱]]
- [[SKN26 1차 차량 운영비 프로젝트]]

## 먼저 확인할 질문

- 이 조회는 어떤 컬럼만 있으면 충분한가?
- 사용자 입력이 조건에 들어간다면 parameter binding을 쓰고 있는가?
- 검색 결과가 없을 때와 DB 오류가 났을 때를 구분하는가?
- `LIKE` 검색이 너무 넓거나 느리지 않은가?
