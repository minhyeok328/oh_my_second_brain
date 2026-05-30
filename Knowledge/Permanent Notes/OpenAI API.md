---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'llm'
  - 'api'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
---

# OpenAI API

태그: #llm_wiki #llm #api

## 한 줄 정의

OpenAI API는 애플리케이션 코드에서 OpenAI 모델의 채팅, 임베딩, 구조화 출력 등을 호출하기 위한 인터페이스다.

## 내 말로 다시 설명

노트북에서 프롬프트를 테스트하는 것과 서비스에서 API를 호출하는 것은 다르다. 서비스에서는 API key, 모델명, temperature, 입력 schema, 응답 파싱, 실패 처리, 비용을 모두 코드 계약으로 관리해야 한다.

## 언제 쓰는가

- RAG 답변 생성, router 판단, slot extraction처럼 자연어 판단이 필요한 경우
- 텍스트를 [[Embedding]]으로 바꿔 검색에 사용할 경우
- Django, Streamlit, LangGraph node에서 LLM 기능을 서비스 흐름에 넣을 때

## 언제 쓰면 안 되는가

- DB 조회나 계산으로 확정 가능한 일을 모델에게 맡기는 경우
- API key, rate limit, 실패 fallback 없이 사용자 요청 경로에 바로 붙이는 경우
- 최신 모델명이나 파라미터를 공식 문서 확인 없이 고정하는 경우

## 프로젝트 예시

- [[SKN26 3차 프로젝트 - PICKLE RAG 챗봇]]은 `ChatOpenAI`로 router와 generator를 호출하고, `text-embedding-3-small`로 식당 관련 텍스트를 임베딩했다.
- [[SKN26 4차 프로젝트 - LG Home]]은 `gpt-4o-mini`로 제품군 분류, 후속 질문 판별, 슬롯 추출, 최종 답변을 만들고, OpenAI embedding으로 Pinecone 매뉴얼 검색 query vector를 만든다.

## 실패 조건

- API key가 import 시점에 강하게 필요하면 Django check나 배포가 실패할 수 있다.
- temperature를 낮춰도 사실성이 보장되지는 않는다.
- LLM 응답을 JSON으로 기대하면서 schema 검증을 하지 않으면 downstream node가 깨진다.

## 관련 개념

- [[LLM]]
- [[Chat Model]]
- [[Embedding]]
- [[Function Calling]]
- [[RAG]]

## 먼저 확인할 질문

- 이 호출은 분류, 추출, 생성, 임베딩 중 어떤 책임을 갖는가?
- 실패하면 사용자에게 무엇을 보여주고 어떤 fallback으로 넘어갈 것인가?
