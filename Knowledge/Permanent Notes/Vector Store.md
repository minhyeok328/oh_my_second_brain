---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'llm'
  - 'vector_store'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
---

# Vector Store

태그: #llm_wiki #llm #vector_store

## 한 줄 정의

Vector Store는 embedding vector와 metadata를 저장하고, query vector와 가까운 항목을 검색하게 해주는 저장소다.

## 내 말로 다시 설명

Vector Store는 "의미 검색용 인덱스"다. 어떤 문서 chunk인지, 어떤 제품군인지, 어떤 식당/리뷰와 연결되는지 metadata를 함께 저장해야 실제 서비스 검색이 된다.

## 언제 쓰는가

- 대량 문서나 리뷰에서 유사한 내용을 빠르게 찾을 때
- product_code, page_number, category 같은 metadata filter가 필요한 RAG를 만들 때
- embedding 검색 결과를 DB 상세 정보와 다시 조인해야 할 때

## 언제 쓰면 안 되는가

- 정확한 SQL 조건 검색으로 충분한 경우
- metadata 없이 vector만 저장해 검색 결과를 설명할 수 없는 경우
- index와 원본 DB의 동기화 정책이 없는 경우

## 프로젝트 예시

[[SKN26 3차 프로젝트 - PICKLE RAG 챗봇]]은 별도 vector DB 대신 SQLite에 base64 embedding을 저장하고 런타임에 유사도를 계산했다. [[SKN26 4차 프로젝트 - LG Home]]은 Pinecone `user_manual` namespace에 매뉴얼 chunk와 `product_code_header` metadata를 저장해 제품군별로 검색했다.

## 실패 조건

- vector 검색 결과가 원본 테이블의 entity와 연결되지 않으면 답변 근거가 약해진다.
- metadata filter가 없으면 다른 카테고리나 권한의 문서가 섞인다.
- index를 갱신했는데 goldset이나 평가 기준을 갱신하지 않으면 성능 판단이 틀어진다.

## 관련 개념

- [[Embedding]]
- [[Retriever]]
- [[RAG]]
- [[SQLite]]

## 먼저 확인할 질문

- vector store의 검색 결과를 어떤 DB row나 문서 링크로 되돌릴 수 있는가?
- metadata filter가 검색 품질과 보안 경계를 동시에 보장하는가?
