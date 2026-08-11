---
type: "moc"
status: "wiki-map"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'moc'
source:
  - 'C:\lecture'
---

# LLM RAG MOC

태그: #moc #llm_wiki

## 학습 경로

- LLM 호출과 프롬프트를 이해한 뒤, 검색, 재순위화, LangGraph 흐름으로 확장한다.
- 처음 읽을 때는 정의 노트보다 흐름 노트를 먼저 보고, 막히는 용어만 Permanent Note로 내려간다.
- 실제 프로젝트 기준으로는 [[SKN26 3차 프로젝트 - PICKLE RAG 챗봇]]에서 SQLite 기반 RAG와 goldset 평가를 보고, [[SKN26 4차 프로젝트 - LG Home]]에서 Django 서비스 안의 LangGraph/Pinecone RAG를 비교한다.

## 문제 해결 경로

- 답변 품질이 낮으면 검색 실패, 컨텍스트 과다, 프롬프트 모호성, 생성 후 검증 부재를 나눠 본다.
- 해결 후에는 관련 Permanent Note의 확인 질문에 실제 사례를 한 줄로 남긴다.
- 평가가 필요한 경우 [[RAG 평가 질문 세트]]와 [[RAG 검색 실패 사례]]에서 route, payload, target, answer, retrieval 중 어느 단계가 실패했는지 먼저 분류한다.

## 핵심 노트
- [[LLM]]
- [[Prompt Engineering]]
- [[OpenAI API]]
- [[Function Calling]]
- [[LangChain]]
- [[RAG]]
- [[RAG 평가]]
- [[Retriever]]
- [[Embedding]]
- [[Vector Store]]
- [[Reranking]]
- [[LangGraph]]
- [[Multi-Agent]]
- [[SLLM]]

## 프로젝트 적용

- [[SKN26 3차 프로젝트 - PICKLE RAG 챗봇]]
- [[SKN26 4차 프로젝트 - LG Home]]
