---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'llm'
  - 'prompt'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-1943'
---

# Prompt Engineering

태그: #llm_wiki #llm #prompt

## 한 줄 정의

Prompt Engineering은 LLM이 어떤 역할로, 어떤 근거를 사용해, 어떤 형식과 제약으로 출력할지 설계하는 작업이다.

## 내 말로 다시 설명

좋은 프롬프트는 긴 지시문이 아니라 실패 가능성을 줄이는 계약이다. 특히 RAG나 agent에서는 "무엇을 답할지"보다 "무엇을 근거로 삼고, 무엇을 만들면 안 되는지"가 더 중요하다.

## 언제 쓰는가

- route, slot, product classification처럼 LLM 출력을 다음 코드 단계가 사용하는 경우
- 후보 리스트 밖 정보를 만들면 안 되는 grounded answer를 생성할 때
- fall case, 후속 질문, 검색 실패 안내처럼 UX 규칙이 필요한 경우

## 언제 쓰면 안 되는가

- 데이터 정합성 문제를 prompt로 숨기려는 경우
- schema와 parser 없이 자유문장 출력에 의존하는 경우
- 프롬프트 변경 후 평가 질문 세트로 회귀 검증하지 않는 경우

## 프로젝트 예시

- [[SKN26 3차 PICKLE 맛집 추천 챗봇]]은 system prompt에서 후보 식당 리스트 밖 정보 생성을 제한한다.
- [[SKN26 4차 LG Home AI 가전 상담]]은 fall case, 후속 질문, 제품군 분류, intent/slot 추출마다 다른 prompt를 둔다.

## 실패 조건

- "친절하게 답해줘"처럼 추상 지시만 있으면 검색 실패와 hallucination을 막지 못한다.
- 같은 prompt에서 분류, 검색어 생성, 답변 생성을 모두 시키면 디버깅 지점이 사라진다.
- 금지 조건과 fallback 문구가 없으면 모델이 없는 정보를 채워 넣는다.

## 관련 개념

- [[LLM]]
- [[Output Parser]]
- [[Function Calling]]
- [[RAG 평가]]

## 먼저 확인할 질문

- 이 프롬프트의 출력은 사람이 읽는가, 코드가 소비하는가?
- 답변이 틀렸을 때 prompt, retrieval, schema 중 무엇을 먼저 의심할 것인가?
