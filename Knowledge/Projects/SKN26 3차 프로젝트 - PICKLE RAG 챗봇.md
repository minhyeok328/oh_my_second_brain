---
type: "project"
status: "project-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'project_context'
  - 'project'
  - 'skn26'
  - 'rag'
  - 'langgraph'
source:
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project\src_test3'
---

# SKN26 3차 프로젝트 - PICKLE RAG 챗봇

태그: #project_context #project #skn26 #rag #langgraph

## 한 줄 요약

신대방삼거리 식당 데이터를 SQLite와 임베딩 검색으로 구축하고, LangGraph로 자연어 질문을 route, slot, DB 검색, 근거 기반 답변 생성 단계로 나눈 맛집 추천 RAG 챗봇이다.

## 문제 정의

맛집 검색은 단순 키워드만으로는 "혼밥", "분위기", "메뉴", "가성비" 같은 복합 조건을 다루기 어렵다. 순수 LLM은 존재하지 않는 식당이나 메뉴를 만들 수 있으므로, DB에 있는 후보만 사용하도록 검색과 생성의 경계를 분리했다.

## 사용한 지식

- [[RAG]]: 식당·메뉴·리뷰 데이터를 검색 근거로 넣어 답변한다.
- [[LangGraph]]: route, slot extraction, connector search, generate node를 상태 그래프로 연결한다.
- [[Function Calling]]: `@tool`과 JSON Schema 기반 슬롯 추출로 LLM 출력을 구조화한다.
- [[Embedding]], [[Retriever]], [[Reranking]]: category, tag, menu, food, review별 유사도 검색과 후보 재정렬을 수행한다.
- [[SQLite]]: 식당, 메뉴, 리뷰, 태그, 관계 테이블과 base64 임베딩을 보관한다.
- [[RAG 평가]]: goldset, route/payload/target/answer/retrieval check로 품질을 측정한다.

## 프로젝트 예시

- `src\pipeline.py`는 `GraphState`를 정의하고 `route_node`, `embedding_slot_node`, `fixed_slot_node`, `connector_search_node`, `generate_node`를 LangGraph로 연결한다.
- `src\router.py`는 질문을 `embedding` 또는 `fixed` 경로로 분기한다.
- `database\sql\utils.py`는 슬롯별 DB 검색과 식당 상세 조인을 담당한다.
- `src_test3\build_llm_goldset.py`는 `fixed 20개 + embedding 30개` 평가 케이스를 만든다.
- `src_test3\evaluate_llm.py`는 route, payload, target, answer, retrieval 점수를 가중 합산한다.

## 판단 기준

- 질문이 특정 식당/메뉴를 명시하면 fixed 검색으로 보내고, 분위기·상황·조건 중심이면 embedding 검색으로 보낸다.
- LLM은 후보 리스트 밖의 식당을 만들면 안 된다.
- 검색 실패는 route 실패, payload 추출 실패, target 미검색, answer 키워드 불일치, retrieval count 부족으로 나눠야 한다.
- SQLite에 임베딩을 저장할 때는 vector DB를 쓰지 않는 대신 디코딩과 유사도 계산 비용을 감안해야 한다.

## 경험 로그

- 의사결정: [[프로젝트 의사결정 로그#3차 PICKLE RAG 챗봇]]
- 실패/디버깅: [[프로젝트 실패와 디버깅 로그#3차 PICKLE RAG 챗봇]]
- 경험 MOC: [[프로젝트 경험 MOC#3차 PICKLE RAG 챗봇]]

## 개인 회고

- 직접 맡은 부분: RAG 구조 설계, LLM 모델링, 모델 평가, Streamlit 기반 UI 구현에 관여했다.
- route 판단: fixed route는 구현하면서 굳이 필요했는지 의문이 남았다. 질문 유형을 나누는 장점은 있었지만, route 자체가 복잡도를 만드는 지점도 있었다.
- 가장 어려웠던 축: route, payload, target, answer, retrieval 중 answer가 생각보다 어려웠다.
- LangGraph 판단: node를 나누면 route, slot, search, generate를 따로 볼 수 있어 관리와 디버깅이 쉬워진다고 느꼈다.
- 평가 관점: LLM 프로젝트의 핵심은 RAG 평가였고, 특히 검색 결과를 얼마나 잘 참조하는지가 중요했다.
- 답변 원칙: RAG의 핵심은 hallucination 방지이므로 후보 밖 답변 금지를 가장 신경 썼다.
- 다시 한다면: RAG 구조 자체를 크게 바꾸기보다 node를 더 세분화하거나, 에이전트 파이프라인을 구축해 최신 흐름의 기술을 더 다양하게 실험해보고 싶다.

## 실패 조건

- route가 틀리면 이후 슬롯과 검색이 모두 틀어진다.
- slot payload가 비어 있거나 잘못된 key에 들어가면 검색 후보가 과도하게 넓거나 좁아진다.
- 답변이 후보 dict가 아니라 모델 기억에 기대면 hallucination이 생긴다.

## 다음 보강 노트

- [[RAG]]
- [[LangGraph]]
- [[Function Calling]]
- [[SQLite]]
- [[RAG 평가]]

## 먼저 확인할 질문

- 이 실패는 검색이 못 찾은 문제인가, 생성이 근거를 지키지 않은 문제인가?
- goldset이 실제 DB 상태와 같은 시점의 데이터를 기준으로 만들어졌는가?
