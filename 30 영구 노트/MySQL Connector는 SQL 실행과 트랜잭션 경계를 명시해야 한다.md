---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'mysql'
  - 'python'
  - 'database'
aliases:
  - 'MySQL Connector Python'
sources:
  - 'https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html'
  - 'https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlconnection-commit.html'
  - 'C:\MinHyeok\lecture\02_mysql_workspace'
source_quality: 'mixed'
verified: true
id: '20260530000000-9718'
---

# MySQL Connector는 SQL 실행과 트랜잭션 경계를 명시해야 한다

## 주장

MySQL Connector/Python에서 cursor의 SQL 실행과 connection의 commit·rollback은 서로 다른 책임이다. [[SELECT와 WHERE는 조회 범위와 조건을 분리한다]]처럼 SQL 자체의 범위를 정한 뒤에도, 변경 작업은 성공한 묶음만 확정하고 실패한 묶음은 되돌리는 트랜잭션 경계를 코드에 드러내야 한다.

## 연결

[[MySQL과 관계형 데이터베이스 강의]]의 SQL·트랜잭션 실습을 애플리케이션에 옮길 때는 [[Django ORM 모델은 데이터 구조와 제약을 코드로 표현한다]] 같은 ORM 경계와 직접 connector 경계를 섞지 않는 편이 추적하기 쉽다. 내 운영 규칙은 사용자 값을 SQL 문자열에 합치지 않고 connector의 파라미터 바인딩을 사용하는 것이다.

## 한계와 반례

commit은 이미 잘못 작성된 SQL이나 여러 서비스에 걸친 일관성을 해결하지 않는다. 읽기 전용 조회에는 변경 트랜잭션 확정이 필요하지 않을 수 있고, 연결 풀·재시도·격리 수준이 중요한 서비스에서는 단순한 함수 하나로 connection을 열고 닫는 구조가 부족하다.

## 확인한 근거

- 2026-08-11: MySQL Connector/Python 공식 `cursor.execute()` 문서에서 SQL 문과 파라미터를 분리해 실행하는 API를 확인했다.
- 2026-08-11: MySQL Connector/Python 공식 `commit()` 문서에서 트랜잭션 테이블의 변경을 확정하며, 폐기할 때는 `rollback()`을 사용한다는 경계를 확인했다.
- 강의 자료 확인(개인 해석): 승인된 `02_mysql_workspace`에는 SQL과 트랜잭션 예제가 있지만 애플리케이션의 connection·예외 처리 경계는 후속 질문으로 남아 있음을 확인했다.
