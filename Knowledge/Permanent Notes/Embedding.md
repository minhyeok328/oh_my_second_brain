---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'llm'
  - 'rag'
  - 'embedding'
source:
  - 'C:\lecture'
external:
  - 'https://platform.openai.com/docs/api-reference/embeddings'
  - 'https://platform.openai.com/docs/concepts'
---

# Embedding

태그: #llm_wiki #llm #rag #embedding

## 한 줄 정의

Embedding은 텍스트, 이미지 같은 입력을 의미적 유사도를 계산할 수 있는 숫자 벡터로 변환한 표현이다.

## 내 말로 다시 설명

Embedding은 문장을 좌표 공간에 놓는 일이다. 비슷한 의미의 문장은 가까운 좌표에 놓이고, 전혀 다른 의미는 멀어진다. RAG에서는 질문과 문서 chunk를 같은 공간에 넣어 "문자열이 같은가"가 아니라 "의미가 가까운가"로 검색한다.

## 핵심 개념

- vector dimension: embedding 벡터의 길이다.
- similarity: cosine, dot product 등으로 가까움을 계산한다.
- normalization: 거리 계산 방식에 따라 벡터 정규화가 중요할 수 있다.
- chunk granularity: 너무 큰 chunk는 의미가 흐려지고, 너무 작은 chunk는 맥락이 끊긴다.
- metadata: embedding만으로 부족한 필터링 정보를 보완한다.

## 언제 쓰는가

- [[RAG]]에서 문서 검색을 의미 기반으로 하고 싶을 때
- 중복 문서 탐지, 유사 질문 추천, semantic clustering이 필요할 때
- 키워드 검색으로 표현 차이를 잡지 못할 때

## 언제 쓰면 안 되는가

- 정확한 문자열 일치나 정규식 검색이 필요한 경우
- 숫자 계산이나 날짜 범위 필터처럼 구조화 query가 더 정확한 경우
- 데이터 권한과 개인정보 처리 기준이 정리되지 않은 경우

## 자주 헷갈리는 점

- embedding 검색은 "정답"이 아니라 "유사 후보"를 돌려준다.
- 모델, dimension, 거리 metric을 바꾸면 기존 index와 비교 기준도 달라진다.
- 좋은 embedding도 나쁜 chunking을 구제하지 못한다.

## 관련 개념

- [[Vector Store]]
- [[Retriever]]
- [[Text Splitter]]
- [[RAG]]
- [[Word Embedding]]

## 확인 질문

- 검색하려는 단위는 문단, 코드 블록, 파일, 강의 섹션 중 무엇인가?
- 의미 검색과 metadata filter를 어떻게 나눌 것인가?

## 외부 참조

- https://platform.openai.com/docs/api-reference/embeddings
- https://platform.openai.com/docs/concepts
