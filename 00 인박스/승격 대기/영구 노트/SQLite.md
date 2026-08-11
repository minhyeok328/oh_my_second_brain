---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'database'
  - 'sqlite'
source:
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-2977'
---

# SQLite

태그: #llm_wiki #database #sqlite

## 한 줄 정의

SQLite는 별도 서버 없이 하나의 파일에 테이블과 데이터를 저장하는 경량 관계형 데이터베이스다.

## 내 말로 다시 설명

SQLite는 개발용 DB, 작은 데이터 서비스, RAG용 구조화 데이터 저장에 잘 맞는다. 서버가 없어서 배포와 백업은 단순하지만, 동시 쓰기와 대규모 운영에는 한계가 있다.

## 언제 쓰는가

- 팀 프로젝트 데모나 개발 환경에서 DB 서버 없이 빠르게 데이터를 저장할 때
- 크롤링/전처리 결과를 관계형 테이블로 묶어 조회해야 할 때
- RAG에서 식당, 메뉴, 리뷰, 태그 같은 구조화 근거를 보관해야 할 때

## 언제 쓰면 안 되는가

- 다중 사용자가 동시에 많은 쓰기를 수행하는 운영 DB가 필요할 때
- 권한, replication, connection pool 등 서버형 DB 기능이 필요한 경우
- vector DB 수준의 ANN 검색 성능을 기대하는 경우

## 프로젝트 예시

[[SKN26 3차 PICKLE 맛집 추천 챗봇]]은 `restaurant.db`에 식당, 메뉴, 리뷰, category, food, tag, 관계 테이블을 저장하고, 임베딩은 base64 인코딩된 TEXT 컬럼으로 보관했다. [[SKN26 4차 LG Home AI 가전 상담]]은 Django 개발 DB로 SQLite를 사용했다.

## 자주 헷갈리는 점

- SQLite 파일 하나가 DB이므로 파일 경로와 현재 working directory가 중요하다.
- 임베딩을 TEXT로 저장할 수는 있지만, 검색 성능과 디코딩 비용은 직접 관리해야 한다.
- Django에서 SQLite를 쓰더라도 ORM 모델 설계는 나중에 다른 DB로 옮길 수 있게 유지하는 편이 좋다.

## 관련 개념

- [[관계형 데이터베이스]]
- [[SQL JOIN]]
- [[Django ORM Model]]
- [[벡터 저장소는 임베딩과 메타데이터를 함께 관리해야 한다]]

## 먼저 확인할 질문

- 이 데이터는 파일 DB로 충분한 규모와 동시성인가?
- 검색 성능 병목이 SQL 조인인지, 임베딩 유사도 계산인지 분리했는가?
