---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'sql'
  - 'mysql'
  - 'database'
aliases:
  - 'SQL SELECT와 WHERE'
sources:
  - 'https://dev.mysql.com/doc/refman/8.4/en/select.html'
  - 'https://dev.mysql.com/doc/refman/8.4/en/selecting-rows.html'
  - 'https://dev.mysql.com/doc/refman/8.4/en/execution-plan-information.html'
  - 'C:\MinHyeok\lecture\02_mysql_workspace'
source_quality: 'mixed'
verified: true
id: '20260530000000-84db'
---

# SELECT와 WHERE는 조회 범위와 조건을 분리한다

## 주장

`SELECT`의 표현식은 결과에 가져올 열과 계산값을 정하고, `WHERE`는 각 행이 결과에 포함되기 위한 조건을 정한다. 이 둘을 분리해 읽으면 [[MySQL Connector는 SQL 실행과 트랜잭션 경계를 명시해야 한다]]에서 SQL의 의미와 실행 경계를 구분하고, 결과를 [[DataFrame은 열 단위 데이터 변환을 구조화한다]]로 넘길 때 필요한 열과 행을 먼저 줄일 수 있다.

## 연결

[[MySQL과 관계형 데이터베이스 강의]]의 조회 실습을 내 관점으로 정리하면, `SELECT *`를 습관적으로 쓰기보다 소비자가 요구하는 열과 조건을 쿼리에 명시하는 편이 데이터 계약을 검토하기 쉽다.

## 한계와 반례

`WHERE`를 생략하면 모든 행이 선택되며, `WHERE`는 집계가 끝난 그룹을 거르는 `HAVING`과 같은 단계가 아니다. 필요한 열과 조건을 적었다고 효율적인 조회가 자동 보장되는 것도 아니다. MySQL optimizer가 테이블·열·인덱스·조건을 바탕으로 선택한 실행 계획은 `EXPLAIN`으로 별도 확인해야 한다.

## 확인한 근거

- 2026-08-11: MySQL 8.4 공식 `SELECT` 문서에서 `select_expr`가 가져올 열을 나타내고 `WHERE` 조건이 참인 행을 선택하며, `WHERE`가 없으면 모든 행을 선택함을 확인했다.
- 2026-08-11: MySQL 공식 행 선택 예제에서 `WHERE`를 사용한 행 필터와 생략 시 전체 행 조회의 차이를 확인했다.
- 2026-08-11: MySQL 8.4 공식 실행 계획 문서에서 optimizer가 테이블·열·인덱스와 `WHERE` 조건을 바탕으로 실행 계획을 선택하며 `EXPLAIN`으로 이를 점검하는 범위를 확인했다.
- 강의 자료 확인(개인 해석): 승인된 `02_mysql_workspace`에서 DQL과 조건 조회 실습을 확인했지만 버전·SQL 모드에 따른 결과 차이는 후속 질문으로 남아 있음을 확인했다.
