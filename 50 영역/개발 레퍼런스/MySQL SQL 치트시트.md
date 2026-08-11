---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'sql'
  - 'mysql'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://dev.mysql.com/doc/refman/8.4/en/sql-statements.html'
source_quality: 'mixed'
verified: false
id: '20260530000000-6ccf'
---

# MySQL SQL 치트시트

## 용도

MySQL에서 데이터베이스 선택, 조회와 변경, 트랜잭션 확인에 쓰는 기본 SQL을 모은다.

## 빠른 참조

- `SHOW DATABASES;`: 서버가 보여 주는 데이터베이스 목록 확인
- `USE db_name;`: 현재 세션의 기본 데이터베이스 선택
- `SELECT col FROM table_name WHERE condition;`: 열과 조건을 명시해 조회
- `INSERT INTO table_name (col) VALUES (value);`: 새 행 삽입
- `UPDATE table_name SET col = value WHERE condition;`: 조건에 맞는 행 변경
- `COMMIT;`: 현재 트랜잭션의 변경 확정
- `ROLLBACK;`: 확정하지 않은 현재 트랜잭션 변경 취소

## 사용 전 확인

- 애플리케이션 입력은 문자열 결합이 아니라 드라이버의 parameter binding으로 전달한다.
- `UPDATE`와 `DELETE`는 먼저 같은 `WHERE` 조건으로 `SELECT`해 범위를 확인한다.
- autocommit, 격리 수준, 계정 권한과 테이블 스키마를 실행 환경에서 확인한다.

## 검증 범위

- 2026-08-11: MySQL 8.4 공식 SQL Statements 레퍼런스에서 위 문장 범주를 확인했다.
- 실제 스키마, 권한, 트랜잭션 설정과 MySQL 다른 버전의 차이는 검증하지 않았다.

## 관련 노트

- [[20 소스 노트/강의/MySQL과 관계형 데이터베이스 강의|MySQL과 관계형 데이터베이스 강의]]
- [[SELECT와 WHERE는 조회 범위와 조건을 분리한다]]
- [[MySQL Connector는 SQL 실행과 트랜잭션 경계를 명시해야 한다]]
