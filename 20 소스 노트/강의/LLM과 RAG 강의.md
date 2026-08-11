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

- [[LLM은 다음 토큰 확률로 문맥에 맞는 출력을 만든다]] · [[프롬프트는 모델에 전달하는 작업 계약이다]] · [[OpenAI API 호출은 입력 출력 오류 경계를 함께 설계해야 한다]] · [[함수 호출은 자연어 요청을 구조화된 도구 입력으로 바꾼다]]
- [[임베딩은 의미 기반 비교를 위한 좌표 표현이다]] · [[검색기는 질문과 관련된 근거 후보를 좁힌다]] · [[벡터 저장소는 임베딩과 메타데이터를 함께 관리해야 한다]]
- [[RAG의 성능은 검색 단계의 품질에서 시작된다]] · [[RAG 평가는 검색과 생성을 분리해서 측정해야 한다]]
- [[LangGraph는 상태 전이를 명시해 LLM 흐름을 제어한다]] · [[LangGraph 상태는 노드 사이의 데이터 계약이다]] · [[조건부 엣지는 상태에 따라 다음 실행 경로를 선택한다]]
