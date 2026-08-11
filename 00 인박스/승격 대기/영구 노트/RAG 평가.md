---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'rag'
  - 'evaluation'
source:
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project\src_test3'
source_quality: 'mixed'
verified: false
id: '20260530000000-5dac'
---

# RAG 평가

태그: #llm_wiki #rag #evaluation

## 한 줄 정의

RAG 평가는 질문에 대한 답변만 보는 것이 아니라 route, query/slot, retrieval target, answer grounding, 후보 수를 나눠 검색-생성 전체 품질을 측정하는 과정이다.

## 내 말로 다시 설명

RAG가 틀렸을 때 "LLM 답변이 틀림"이라고만 하면 고칠 수 없다. 질문 분류가 틀렸는지, 검색어가 틀렸는지, 검색 후보가 빠졌는지, 후보는 맞는데 답변이 근거를 무시했는지를 분해해야 한다.

## 언제 쓰는가

- RAG 챗봇의 품질을 반복 비교해야 할 때
- 검색 전략이나 prompt를 바꾼 뒤 좋아졌는지 확인해야 할 때
- hallucination, 검색 실패, slot extraction 실패를 구분해야 할 때

## 언제 쓰면 안 되는가

- goldset이 실제 DB 상태와 맞지 않는 경우
- 정답이 하나로 고정될 수 없는 탐색형 질문을 단일 정답으로만 평가하는 경우
- 답변 문체 점수만 보고 검색 품질을 생략하는 경우

## 프로젝트 예시

[[SKN26 3차 PICKLE 맛집 추천 챗봇]]의 `src_test3\evaluate_llm.py`는 route 30%, payload 25%, target 25%, answer 10%, retrieval 10% 가중치로 케이스별 점수를 계산한다. goldset은 `fixed 20개 + embedding 30개`로 구성된다.

프로젝트 회고상 가장 중요하게 느낀 기준은 "검색 결과를 얼마나 잘 참조하는가"였다. 특히 answer 단계에서 후보 밖 식당이나 메뉴를 말하면, 문장이 자연스러워도 RAG의 핵심인 hallucination 방지에 실패한 것으로 본다.

## 자주 헷갈리는 점

- answer가 자연스러워도 target 식당이 검색되지 않았으면 RAG는 실패다.
- retrieval 후보가 맞아도 최종 answer가 후보 밖 정보를 만들면 실패다.
- goldset은 DB가 바뀔 때 같이 재생성해야 한다.

## 관련 개념

- [[RAG]]
- [[Retriever]]
- [[Embedding]]
- [[Prompt Engineering]]
- [[RAG 평가 질문 세트]]
- [[RAG 검색 실패 사례]]

## 먼저 확인할 질문

- 실패한 케이스는 route, payload, target, answer, retrieval 중 어디서 처음 깨졌는가?
- 평가 질문이 실제 사용자 질문과 DB 분포를 대표하는가?
- answer가 retrieval 후보 밖 정보를 만들지 않도록 프롬프트와 후처리에서 함께 제한하는가?
