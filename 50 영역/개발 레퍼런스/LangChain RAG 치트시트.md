---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'langchain'
  - 'rag'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.langchain.com/oss/python/deepagents/retrieval'
  - '[[20 소스 노트/강의/LLM과 RAG 강의|LLM과 RAG 강의]]'
source_quality: 'mixed'
verified: false
id: '20260530000000-4d3c'
---

# LangChain RAG 치트시트

## 용도

문서 기반 질의응답을 구성할 때 인덱싱과 런타임 검색 단계를 빠뜨리지 않기 위한 순서표다.

## 빠른 참조

1. loader의 `load()`로 원문과 메타데이터를 문서 객체로 읽는다.
2. splitter의 `split_documents(docs)`로 검색 단위를 만든다.
3. 임베딩 모델과 벡터 저장소로 문서 표현과 원문 식별자를 함께 저장한다.
4. vector store의 `as_retriever()` 또는 현재 문서가 권장하는 검색 인터페이스로 후보를 얻는다.
5. 검색된 근거를 프롬프트에 넣고 모델 출력과 근거 식별자를 함께 기록한다.

## 검증 범위

- 2026-08-11: LangChain 공식 Retrieval 문서와 [[20 소스 노트/강의/LLM과 RAG 강의|로컬 강의 소스 노트]]에서 인덱싱·검색·생성 경계를 확인했다.
- loader, splitter, vector store의 import 경로와 생성자 인자는 패키지·버전별로 달라질 수 있어 검증하지 않았다. 설치 버전의 공식 API 레퍼런스를 확인한 뒤 사용한다.
- 위 목록은 설계 순서이며 그대로 실행되는 완성 코드가 아니다.

## 관련 노트

- [[RAG의 성능은 검색 단계의 품질에서 시작된다]]
- [[검색기는 질문과 관련된 근거 후보를 좁힌다]]
- [[벡터 저장소는 임베딩과 메타데이터를 함께 관리해야 한다]]
- [[RAG 평가는 검색과 생성을 분리해서 측정해야 한다]]
