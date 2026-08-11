---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'llm'
  - 'embedding'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-93ee'
---

# Embedding

태그: #llm_wiki #llm #embedding

## 한 줄 정의

Embedding은 텍스트, 문서, 메뉴명, 리뷰 같은 비정형 데이터를 의미가 비슷할수록 가까운 숫자 벡터로 바꾸는 표현 방식이다.

## 내 말로 다시 설명

키워드가 정확히 같지 않아도 "혼밥하기 좋은 초밥집"과 관련 있는 식당을 찾으려면 의미 기반 비교가 필요하다. Embedding은 문장을 벡터로 바꿔 코사인 유사도 같은 방식으로 가까운 후보를 찾게 해준다.

## 언제 쓰는가

- 자연어 질문과 문서/리뷰/메뉴 설명의 의미 유사도를 비교할 때
- RAG 검색 index를 만들 때
- 태그나 카테고리처럼 사용자가 다른 표현으로 물어볼 수 있는 필드를 검색할 때

## 언제 쓰면 안 되는가

- 정확한 ID, 코드, 가격 범위, 날짜처럼 구조화 조건으로 조회해야 하는 경우
- 데이터가 너무 짧거나 중복되어 embedding 차이가 의미를 잘 드러내지 못하는 경우
- embedding 모델을 바꿨는데 기존 vector store를 재색인하지 않는 경우

## 프로젝트 예시

[[SKN26 3차 PICKLE 맛집 추천 챗봇]]은 category, food, menu, tag, review별 embedding을 만들고 SQLite에 base64 TEXT로 저장했다. [[SKN26 4차 LG Home AI 가전 상담]]은 OpenAI embedding으로 사용설명서 query vector를 만들고 Pinecone에서 제품군별 chunk를 찾았다.

## 실패 조건

- 질문과 문서가 다른 단위로 임베딩되면 검색 후보가 흔들린다.
- 모델 변경 후 재색인을 하지 않으면 query vector와 저장 vector의 기준이 달라진다.
- 유사도 점수만 믿고 metadata filter를 생략하면 권한이나 제품군이 섞인다.

## 관련 개념

- [[Vector Store]]
- [[Retriever]]
- [[RAG]]
- [[RAG 평가]]

## 먼저 확인할 질문

- 어떤 텍스트 단위를 embedding하고, 어떤 단위로 검색 결과를 보여줄 것인가?
- embedding 모델과 저장된 vector가 같은 기준으로 만들어졌는가?
