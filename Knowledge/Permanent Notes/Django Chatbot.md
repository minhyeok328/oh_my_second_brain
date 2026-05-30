---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'llm'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
---

# Django Chatbot

태그: #llm_wiki #django #llm

## 한 줄 정의

Django Chatbot은 Django view, session/auth, DB model, JavaScript 요청, LLM/RAG pipeline을 연결해 웹에서 대화형 기능을 제공하는 구조다.

## 내 말로 다시 설명

챗봇은 LLM 호출 하나가 아니라 사용자, 대화방, 이전 메시지, agent state, 검색 결과, 최종 응답을 저장하고 이어가는 웹 기능이다. Django에서는 view가 요청 검증과 권한을 맡고, LangGraph나 RAG는 비즈니스 흐름을 맡게 분리하는 것이 중요하다.

## 언제 쓰는가

- 로그인 사용자별 대화방과 메시지를 유지해야 할 때
- LLM 답변이 DB 검색, vector search, 후속 질문 state와 연결될 때
- AJAX로 채팅을 보내고 페이지 새로고침 없이 응답을 보여줘야 할 때

## 언제 쓰면 안 되는가

- view 안에 prompt, 검색, 모델 호출, 응답 포맷을 모두 몰아넣는 경우
- 사용자 소유 chatroom 검증 없이 `chat_id`만 믿는 경우
- API key나 vector DB 연결 실패가 Django import/check를 막는 경우

## 프로젝트 예시

[[SKN26 4차 프로젝트 - LG Home]]의 `api\views.py`는 `send_chat`에서 로그인, JSON body, `user_input`, chatroom 소유 여부를 확인한 뒤 `common.llm.add_chat()`을 호출한다. `common\llm.py`는 LangGraph로 제품군 분류, 조건 검색, 매뉴얼 RAG 답변을 처리한다.

프로젝트 회고상 가장 어렵게 느낀 부분은 후속 질문 처리였다. 사용자의 다음 발화가 이전 조건을 이어가는지, 새로운 제품 상담인지, 매뉴얼 질문인지 구분하지 못하면 state가 잘못 병합된다.

## 실패 조건

- 대화 state가 사용자별로 분리되지 않으면 다른 대화의 조건이 섞인다.
- 검색 결과가 너무 많을 때 목록을 전부 답변에 넣으면 UX와 비용이 나빠진다.
- 오류 응답 shape이 불안정하면 프론트 채팅 UI가 실패를 표현하지 못한다.

## 관련 개념

- [[Django JSON API]]
- [[Django Session과 Auth]]
- [[LangGraph]]
- [[RAG]]
- [[Django CSRF]]

## 먼저 확인할 질문

- chat request에서 사용자 권한, 입력 유효성, chatroom 소유권을 검증했는가?
- LLM pipeline 실패가 사용자에게 어떤 메시지로 보이는가?
- 후속 질문일 때 이어받아야 하는 state와 새로 덮어써야 하는 state를 구분했는가?
