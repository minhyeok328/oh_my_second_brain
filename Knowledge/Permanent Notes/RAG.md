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
  - 'retrieval'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
external:
  - 'https://en.wikipedia.org/wiki/Retrieval-augmented_generation'
  - 'https://docs.langchain.com/oss/python/langchain/rag'
---

# RAG

태그: #llm_wiki #llm #rag #retrieval

## 한 줄 정의

RAG는 LLM이 내부 기억만으로 답하지 않게, 외부 문서나 DB 검색 결과를 근거로 넣어 답변하게 만드는 검색-생성 패턴이다.

## 내 말로 다시 설명

RAG의 핵심은 "답변을 잘 쓰는 것"보다 "맞는 근거를 가져오는 것"이다. 검색 후보가 틀리면 LLM은 그럴듯하게 틀린 답을 만든다. 그래서 RAG는 chunking, metadata, retrieval, reranking, prompt, 평가가 함께 있어야 한다.

## 언제 쓰는가

- 사내 문서, 강의 자료, 식당 DB, 제품 매뉴얼처럼 답변 근거가 외부 데이터에 있을 때
- 최신성, 출처 추적, 권한 분리가 중요한 경우
- fine-tuning보다 지식 교체와 감사 가능성이 더 중요한 경우

## 언제 쓰면 안 되는가

- 단순 문장 변환, 분류, 요약처럼 외부 근거가 필요 없는 경우
- 검색 대상 데이터가 부실하거나 권한 경계가 정리되지 않은 경우
- 계산이나 DB 조회로 바로 해결할 수 있는 문제를 굳이 생성 모델에 맡기는 경우

## 프로젝트 예시

- [[SKN26 3차 프로젝트 - PICKLE RAG 챗봇]]은 SQLite의 식당·메뉴·리뷰·태그 데이터를 검색하고, 후보 식당 dict 안에서만 답하도록 제한했다.
- [[SKN26 4차 프로젝트 - LG Home]]은 Pinecone `user_manual` namespace에서 제품군별 매뉴얼 chunk를 검색해 제품 사용법과 오류 해결 답변에 사용했다.

## 설계 체크리스트

- 질문을 검색 가능한 route와 slot으로 바꾸는 단계가 있는가?
- 검색 후보와 LLM에 실제 전달한 후보를 따로 기록하는가?
- 답변에 후보 밖 정보 생성 금지 규칙이 있는가?
- DB나 index가 바뀔 때 평가 goldset도 갱신하는가?

## 실패 조건

- embedding 검색만 붙이고 metadata, 관계 테이블, reranking을 설계하지 않는 경우
- 검색 실패와 생성 실패를 같은 오류로 처리하는 경우
- 답변에 출처나 후보 근거를 남기지 않는 경우

## 관련 개념

- [[Embedding]]
- [[Vector Store]]
- [[Retriever]]
- [[Reranking]]
- [[RAG 평가]]
- [[LangGraph]]

## 먼저 확인할 질문

- 지금 실패는 검색 후보가 틀린 문제인가, 답변 생성이 근거를 무시한 문제인가?
- 검색 대상 문서/DB는 사용자 질문의 표현과 같은 언어·단위로 준비되어 있는가?

## 외부 참조

- https://en.wikipedia.org/wiki/Retrieval-augmented_generation
- https://docs.langchain.com/oss/python/langchain/rag
