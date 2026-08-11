---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'database'
  - 'sqlite'
  - 'persistence'
aliases:
  - 'SQLite'
sources:
  - 'https://www.sqlite.org/onefile.html'
  - 'https://www.sqlite.org/whentouse.html'
  - 'C:\MinHyeok\skn26_projects\3rd_project\database\sql\utils.py'
source_quality: 'mixed'
verified: true
id: '20260530000000-2977'
---

# SQLite는 단일 파일로 작은 애플리케이션의 영속성을 단순화한다

## 주장

SQLite 데이터베이스는 하나의 디스크 파일에 담기므로 별도 데이터베이스 서버를 운영하지 않고도 애플리케이션과 함께 옮기고 백업할 수 있다. 로컬 저장과 낮은 쓰기 동시성이 맞는 작은 서비스에서는 이 배포 단순성이 [[Django ORM 모델은 데이터 구조와 제약을 코드로 표현한다]]가 만든 관계형 구조를 빠르게 영속화하는 장점이 된다.

## 연결

[[벡터 저장소는 임베딩과 메타데이터를 함께 관리해야 한다]]와 달리 SQLite 자체는 근사 최근접 벡터 검색 계층이 아니다. 프로젝트 코드에서 확인한 적용을 내 관점으로 정리하면, [[SKN26 3차 PICKLE 맛집 추천 챗봇]]은 `restaurant.db` 경로를 기준으로 구조화 데이터를 조회하고 임베딩은 읽어 애플리케이션 메모리에서 유사도를 계산한다.

## 한계와 반례

SQLite는 데이터베이스 파일마다 동시에 한 writer만 허용한다. 여러 프로세스가 동시에 자주 쓰거나 네트워크를 통해 많은 클라이언트가 직접 접근해야 한다면 client/server 데이터베이스가 더 적합하다. 단일 파일이라는 점도 파일 권한·백업 시점·경로 관리를 자동으로 해결해 주지는 않는다.

## 확인한 근거

- 2026-08-11: SQLite 공식 Single File Database 문서에서 데이터베이스가 단일 파일이며 이식 가능한 애플리케이션 파일 형식으로 사용할 수 있음을 확인했다.
- 2026-08-11: SQLite 공식 Appropriate Uses 문서에서 낮은 writer 동시성에는 적합하지만 동시 writer가 많으면 client/server 엔진을 선택해야 함을 확인했다.
- 프로젝트 코드 확인(개인 해석): 승인된 `3rd_project/database/sql/utils.py`에서 `restaurant.db` 파일 연결과 SQL 조회 후 애플리케이션 메모리에서 임베딩 유사도를 계산하는 구조를 확인했다.
