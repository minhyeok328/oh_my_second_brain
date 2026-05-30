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
external:
  - 'https://en.wikipedia.org/wiki/Retrieval-augmented_generation'
  - 'https://docs.langchain.com/oss/python/langchain/rag'
---

# RAG

태그: #llm_wiki #llm #rag #retrieval

## 한 줄 정의

RAG는 생성 모델이 내부 파라미터만 믿고 답하지 않도록, 외부 문서를 검색한 뒤 그 근거를 컨텍스트로 넣어 답변하게 만드는 패턴이다.

## 내 말로 다시 설명

LLM은 말솜씨가 좋지만 최신 자료, 사내 문서, 긴 강의 자료를 항상 알고 있지는 않다. RAG는 먼저 질문을 검색 문제로 바꾸고, 관련 문서를 가져오고, 그 문서 안에서만 답을 만들도록 제한한다. 핵심은 "검색 품질이 답변 품질의 상한을 만든다"는 점이다.

## 작동 흐름

- 문서를 chunk로 나누고 metadata를 붙인다.
- chunk를 [[Embedding]]으로 바꿔 [[Vector Store]]에 저장한다.
- 사용자 질문을 같은 embedding 공간으로 보낸다.
- [[Retriever]]가 관련 chunk를 가져온다.
- 필요하면 [[Reranking]]이나 [[Query Expansion]]으로 문맥을 정제한다.
- LLM이 검색 근거를 바탕으로 답변하고 출처를 남긴다.

## 언제 쓰는가

- 강의 자료, 회사 문서, 정책, 매뉴얼처럼 답변 근거가 외부 지식에 있을 때
- 최신성이나 출처 추적이 중요할 때
- fine-tuning보다 지식 교체와 감사 가능성이 더 중요할 때

## 언제 쓰면 안 되는가

- 답변이 단순한 문장 변환, 요약, 분류처럼 외부 검색 없이 가능한 경우
- 검색 대상 문서가 너무 부실하거나 권한 관리가 정리되지 않은 경우
- 정답 계산이 필요한데 검색 문서만으로 검증할 수 없는 경우

## 자주 헷갈리는 점

- RAG는 모델을 똑똑하게 만드는 기술이라기보다, 모델이 참고할 근거를 잘 전달하는 시스템 설계다.
- embedding 검색만 붙이면 RAG가 완성되는 것이 아니다. chunking, metadata, reranking, prompt, 평가가 함께 필요하다.
- 검색 결과가 틀리면 LLM은 그럴듯하게 틀린 답을 만들 수 있다.

## 설계 체크리스트

- 질문 유형별로 필요한 문서 단위가 정해져 있는가?
- chunk 크기가 정의, 절차, 코드 예제를 끊어먹지 않는가?
- metadata로 강의 주차, 파일 경로, 버전, 권한을 필터링할 수 있는가?
- 검색 실패와 모르는 질문을 "모른다"로 처리하는가?
- 답변에 근거 문서 링크나 파일 경로가 남는가?

## 관련 개념

- [[LLM]]
- [[Embedding]]
- [[Vector Store]]
- [[Retriever]]
- [[Reranking]]
- [[LangChain]]
- [[LangGraph]]

## 확인 질문

- 지금 문제는 모델 지식 부족인가, 검색 대상 문서 품질 부족인가?
- 답변이 틀렸을 때 검색, 컨텍스트, 프롬프트, 생성 중 어디를 먼저 의심할 것인가?

## 외부 참조

- https://en.wikipedia.org/wiki/Retrieval-augmented_generation
- https://docs.langchain.com/oss/python/langchain/rag
