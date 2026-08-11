---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'rag'
  - 'evaluation'
aliases:
  - 'RAG 평가'
sources:
  - 'https://arxiv.org/abs/2309.15217'
  - 'https://docs.langchain.com/oss/python/deepagents/retrieval'
source_quality: 'primary'
verified: true
id: '20260530000000-5dac'
---

# RAG 평가는 검색과 생성을 분리해서 측정해야 한다

RAG의 최종 답변 점수 하나만 보면 검색 후보가 틀렸는지, 후보는 맞았지만 생성이 근거를 무시했는지 알 수 없다. RAGAS 연구가 컨텍스트 관련성·답변 충실성·답변 관련성을 서로 다른 축으로 둔 것처럼, 나는 [[검색기는 질문과 관련된 근거 후보를 좁힌다|검색]]과 생성의 책임을 분리해 측정해야 개선 지점을 찾을 수 있다고 본다.

최소한 질문별로 기대 근거, 실제 검색 후보, LLM에 전달한 후보, 최종 답변을 나란히 남긴다. 그러면 기대 근거가 후보에 포함됐는지는 검색 지표로, 답변이 전달된 근거를 따랐는지는 생성 지표로 볼 수 있다. [[RAG의 성능은 검색 단계의 품질에서 시작된다]]와 [[프롬프트는 모델에 전달하는 작업 계약이다]]를 각각 바꾸었을 때 어느 점수가 움직였는지도 비교할 수 있다.

단, 자동 평가 지표도 정답 자체는 아니다. 평가용 LLM은 편향될 수 있고, 하나의 정답으로 고정하기 어려운 탐색형 질문에서는 여러 타당한 답을 놓칠 수 있다. 데이터베이스나 인덱스가 바뀌면 기대 근거도 함께 갱신해야 하며, 고위험 답변은 사람의 근거 확인을 남겨야 한다.

## 확인한 근거

- 2026-08-11: Es et al., *RAGAS: Automated Evaluation of Retrieval Augmented Generation* — 검색 컨텍스트와 생성 답변을 구분하는 평가 축을 확인했다.
- 2026-08-11: LangChain 공식 Retrieval 문서 — 현재 RAG 구성에서 검색과 생성이 별도 단계임을 확인했다.
- 강의 맥락: [[LLM과 RAG 강의]]와 [[RAG 평가 질문 세트]]의 route·target·answer 기록 방식을 재현 가능한 평가 단위로 정리했다.
