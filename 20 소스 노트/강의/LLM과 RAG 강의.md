---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'lecture'
  - 'llm'
  - 'rag'
aliases: []
sources:
  - 'C:\MinHyeok\lecture\08_llm_workspace'
source_path: 'C:\MinHyeok\lecture\08_llm_workspace'
source_quality: 'primary'
verified: true
id: '20260530000000-29b2'
---

# LLM과 RAG 강의

## 출처

- 원본 경로: `C:\MinHyeok\lecture\08_llm_workspace`
- 확인일: 2026-08-11

## 핵심 내용

- 관찰: `01_llm_overview`부터 `04_gpt_finetuning`까지 여러 LLM 호출, 프롬프트 구성, OpenAI API의 채팅·음성·임베딩·모더레이션·함수 호출, 미세 조정을 실습한다.
- 관찰: `05_lanchain\02_langchain_component\02_retrieval.ipynb`는 문서 로더, 임베딩 모델, FAISS 벡터 저장소와 검색기를 구성 요소로 나눈다.
- 관찰: `06_rag\01_2-stage_rag.ipynb`는 문서 로드·분할·임베딩·벡터 저장의 인덱싱 단계와 검색·생성 단계를 구분한다.
- 관찰: `07_advanced_rag`는 BM25·밀집 검색 비교, RRF·HyDE·재순위화·문맥 압축·메타데이터 필터링과 생성 최적화 실험을 포함한다.
- 관찰: `08_langgraph`와 `09_langgraph_multi_agent`는 상태 그래프, 도구·메모리·사람 개입, 에이전틱 RAG와 감독자 구성을 다룬다.
- 관찰: `10_sllm`은 소형 언어 모델 개요와 LoRA·QLoRA 미세 조정 실습으로 이어진다.

## 내 해석과 의문

- 해석: RAG를 하나의 호출로 보지 않고 인덱싱, 검색, 생성과 평가 가능한 경계로 나누는 것이 이 자료의 재사용 가치가 크다.
- 질문: 노트북의 라이브러리 버전과 현재 API가 달라진 부분은 공식 문서로 별도 검증해야 한다.
- 질문: 검색 개선 실험은 같은 질의·정답·평가 지표로 재현 가능한가, 생성 품질과 검색 품질을 분리해 기록했는가?

## 분리한 영구 노트

- [[LLM]] · [[Prompt Engineering]] · [[OpenAI API]] · [[Function Calling]]
- [[Embedding]] · [[Retriever]] · [[Vector Store]]
- [[RAG]] · [[RAG 평가]]
- [[LangGraph]] · [[LangGraph State]] · [[LangGraph Conditional Edge]]
