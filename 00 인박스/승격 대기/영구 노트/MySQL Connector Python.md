---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'mysql'
  - 'python'
  - 'database'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders\DB_Side\DBLoader.py'
source_quality: 'mixed'
verified: false
id: '20260530000000-9718'
---

# MySQL Connector Python

태그: #mysql #python #database #llm_wiki

## 한 줄 정의

MySQL Connector Python은 Python 코드에서 MySQL 서버에 접속해 SQL을 실행하고 결과를 가져오는 드라이버다.

## 왜 중요한가

분석용 CSV나 외부 API 결과를 서비스 화면에서 다시 쓰려면 파일로만 들고 있기보다 DB에 적재하고 조회하는 흐름이 필요하다. Python 앱은 connector를 통해 연결, cursor, query 실행, fetch, commit, 예외 처리를 직접 관리한다.

## 핵심 개념

- 접속 정보는 코드에 박지 않고 환경변수나 설정 파일로 분리한다.
- connection은 DB 서버와의 연결이고, cursor는 SQL 실행 단위다.
- 조회 쿼리는 `fetchall()` 또는 `fetchone()`으로 결과를 가져온다.
- 변경 쿼리는 transaction 경계를 명확히 하고 commit/rollback을 관리한다.
- 사용자 입력이 들어가는 SQL은 문자열 조립보다 parameter binding을 우선한다.

## 프로젝트 예시

[[SKN26 1차 차량 운영비 프로젝트]]의 `DB_Side\DBLoader.py`는 `mysql.connector.connect(**config)`로 `tco_system` DB에 접속한다.

- `config`: `DB_USER`, `DB_PASSWORD`를 `.env`에서 읽어 접속 정보를 만든다.
- `sendquery`: 단일 SQL을 실행하고 `fetchall()` 결과를 반환한다.
- `sendquerys_with_commit`: 여러 SQL을 순서대로 실행하고 commit 경계를 둔다.
- `db_search`: 차량 모델명을 받아 `car_oil`, `car_price`에서 검색한다.

이 구조는 Streamlit 화면이 DB 연결 세부 구현을 몰라도 `DBLoader.db_search(...)`만 호출하게 만든다.

## 언제 쓰는가

- Python 수집 코드가 MySQL에 데이터를 적재해야 할 때
- Streamlit, FastAPI, 배치 스크립트에서 기존 MySQL 테이블을 조회해야 할 때
- CSV/API 결과를 서비스 조회용 테이블로 옮길 때
- ORM 없이 SQL을 직접 제어해야 할 때

## 언제 쓰면 안 되는가

- Django 모델 중심 앱에서 ORM으로 충분히 표현되는 조회를 굳이 raw connector로 우회할 때
- 사용자 입력을 f-string으로 SQL에 바로 넣어야 하는 구조일 때
- 연결 재사용, pooling, transaction 관리가 필요한 큰 서비스에서 단순 함수형 연결만으로 버티려 할 때

## 실패 조건

- 환경변수가 비어 있으면 로컬에서는 동작해도 다른 PC에서 접속이 실패한다.
- connection/cursor를 닫지 않으면 연결 누수나 lock 문제가 생길 수 있다.
- `LIKE '%사용자입력%'`를 문자열 조립으로 만들면 따옴표, `%`, `_`, SQL injection에 취약하다.
- 변경 쿼리에서 commit 경계가 불명확하면 일부 데이터만 반영되거나 rollback이 어렵다.
- 예외를 출력만 하고 빈 리스트를 반환하면 "데이터 없음"과 "DB 오류"가 구분되지 않는다.

## 관련 개념

- [[SQL SELECT와 WHERE]]
- [[SQL DML]]
- [[SQL 트랜잭션]]
- [[Python 예외 처리]]
- [[SKN26 1차 차량 운영비 프로젝트]]

## 먼저 확인할 질문

- 접속 정보가 코드 밖으로 분리되어 있는가?
- 사용자 입력이 들어가는 쿼리는 parameter binding으로 처리되는가?
- 빈 결과와 DB 오류를 호출자가 구분할 수 있는가?
- 여러 쿼리를 실행할 때 commit/rollback 경계가 명확한가?
