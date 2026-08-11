---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'lecture'
  - 'mysql'
aliases: []
sources:
  - 'C:\MinHyeok\lecture\02_mysql_workspace'
source_path: 'C:\MinHyeok\lecture\02_mysql_workspace'
source_quality: 'primary'
verified: true
id: '20260530000000-51ed'
---

# MySQL과 관계형 데이터베이스 강의

## 출처

- 원본 경로: `C:\MinHyeok\lecture\02_mysql_workspace`
- 확인일: 2026-08-11

## 핵심 내용

- 관찰: `01_create_user_database.sql`부터 `08_ddl.sql`까지 사용자·데이터베이스 생성, 자료형, 조회, 조인·서브쿼리, 데이터 변경, 트랜잭션, 스키마 정의를 순서대로 실습한다.
- 관찰: `03_dql_select.sql`과 `04_dql_select2.sql`은 `SELECT` 조건, 연산자, 문자열·숫자 함수와 집계를 다룬다.
- 관찰: `05_dql_join_subquery.sql`은 여러 테이블 조회와 하위 질의를, `06_dml.sql`은 `INSERT`, `UPDATE`, `DELETE`와 트랜잭션 시작을 포함한다.
- 관찰: `07_tcl.sql`은 `COMMIT`, `ROLLBACK`, `SAVEPOINT`를 하나의 논리적 작업 단위와 연결한다.
- 관찰: `erd.md`와 `employeedb.md`는 기본키·외래키 관계를 Mermaid ER 다이어그램으로 기록한다.

## 내 해석과 의문

- 해석: SQL 문법 파일과 ER 다이어그램을 함께 보면 조회문을 테이블 관계와 분리하지 않고 복습할 수 있다.
- 질문: 각 실습이 전제하는 MySQL 버전과 SQL 모드는 무엇이며, 현재 환경에서도 같은 결과가 나오는가?
- 질문: 트랜잭션 예제를 애플리케이션의 커넥션·예외 처리 경계와 어떻게 연결할 것인가?

## 분리한 영구 노트

- [[SQL SELECT와 WHERE]]
- 관계형 키와 참조 무결성 — 후속 영구 노트 후보
- SQL 조인과 하위 질의 — 후속 영구 노트 후보
- 트랜잭션의 커밋과 롤백 — 후속 영구 노트 후보
