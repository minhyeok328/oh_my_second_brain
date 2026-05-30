---
type: "project"
status: "project-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'project'
  - 'skn26'
  - 'django'
  - 'langgraph'
source:
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
related_source:
  - 'C:\MinHyeok\skn26_4th_1st\4th_project_change_react'
---

# SKN26 4차 프로젝트 - LG Home

태그: #llm_wiki #project #skn26 #django #langgraph

## 한 줄 요약

LG 가전 상품 DB, Django SSR UI, 찜/계정 기능, LangGraph 기반 LGneer 챗봇, Pinecone 사용설명서 RAG를 결합한 가전 검색·추천 서비스다.

## 공식 프로젝트 기준

공식 4차 프로젝트 기준은 `C:\MinHyeok\skn26_4th_1st\4th_project`다. `4th_project_change_react`는 프로젝트 종료 후 개인적으로 진행한 React SPA 전환 실험이므로, 이 노트에서는 별도 "개인 확장"으로만 분리해 기록한다.

## 문제 정의

가전 제품은 카테고리마다 스펙 기준이 다르고, 사용설명서와 고객지원 정보가 흩어져 있다. 사용자는 필터 UI로 조건을 직접 선택하거나, 자연어로 "전기세 적게 쓰는 냉장고", "세탁기 UE 에러"처럼 질문할 수 있어야 한다.

## 사용한 지식

- [[Django Project]], [[Django App]], [[Django ORM Model]]: 상품, 계정, 찜, 채팅 도메인을 앱으로 분리한다.
- [[Django Template]], [[Django View]], [[Django URL Routing]]: SSR 화면과 AJAX API를 함께 제공한다.
- [[Django Chatbot]]: chat endpoint에서 LangGraph 챗봇을 호출하고 대화방 state를 유지한다.
- [[LangGraph]]: fall case, 후속 질문, 제품군 분류, intent/slot 추출, DB 검색, 답변 생성을 노드로 분리한다.
- [[Vector Store]], [[Embedding]], [[RAG]]: Pinecone `user_manual` namespace에서 제품군별 매뉴얼 chunk를 검색한다.
- [[React SPA]], [[Django JSON API]]: 프로젝트 후 개인 확장에서 SSR 구조를 React SPA와 JSON API 구조로 분리하는 실험에 사용했다.

## 프로젝트 예시

- `common\llm.py`는 `GraphState`를 정의하고, 검색 조건 병합, 제품군별 검색 가능 조건, LangGraph 노드 흐름을 관리한다.
- `common\llm_agent.py`는 structured output 기반 fall case, 후속 질문, 제품군 분류, 슬롯 추출 프롬프트를 담당한다.
- `common\vector_search.py`는 OpenAI embedding으로 query vector를 만들고 Pinecone에서 제품군별 매뉴얼 청크를 검색한다.
- `api\views.py`의 `send_chat`은 JSON POST를 받아 로그인 여부, 입력값, chatroom 소유 여부를 확인한 뒤 `llm.add_chat`을 호출한다.
- `static\js\api-response.js`는 fetch JSON 응답, CSRF, 네트워크/파싱 실패 UX를 공통화한다.

## 판단 기준

- 자연어 검색 조건은 Django ORM lookup으로 변환되기 전에 빈 값, 범위 조건, `in`, `icontains` 병합 규칙을 정해야 한다.
- 대화형 검색은 이전 대화 state를 유지해야 후속 질문을 처리할 수 있다.
- 제품 추천과 매뉴얼 Q&A는 검색 대상이 다르므로 DB 검색과 vector search를 분리해야 한다.
- SSR과 AJAX를 섞을 때는 CSRF, 로그인 redirect, JSON parse 실패 처리를 공통화해야 한다.

## 개인 확장 메모

`4th_project_change_react`는 공식 팀 산출물 이후의 개인 확장이다. 여기서 Django 템플릿 SSR을 React + TypeScript + Tailwind SPA로 분리하고, Django를 JSON API 서버로 재구성했다. 이 경험은 [[React SPA]], [[Django JSON API]], [[React API Fetch]] 노트의 프로젝트 예시로만 사용한다.

개인 회고 기준으로는 공식 4차 프로젝트에서 Django template SSR 방식으로 구성했던 부분을 React로 분리된 구조로 다시 만들어 보고 싶은 욕구가 있었다. 프로젝트 종료 후 혼자 `4th_project_change_react`로 재공학하면서, 프론트 렌더링과 Django 백엔드 API 책임을 나누는 구조를 실험했다.

## 개인 회고

- 직접 맡은 부분: 공식 프로젝트에서는 프론트엔드 파트, 문서 작업, GitHub 조직 관리를 맡았다.
- SSR 구조 판단: Django SSR에서 특별히 편하다고 느낀 점은 크지 않았다. React 없이 SSR 구조를 맞추려다 보니 작성하고 관리해야 할 template, partial, static JS 파일이 많아진 점이 가장 불편했다.
- 챗봇 난점: LangGraph 제품 상담 챗봇에서는 후속 질문 처리가 가장 어렵게 느껴졌다.
- 모델링/RAG 분리: 상품 DB 검색과 매뉴얼 RAG 분리 기준은 모델링 쪽 담당 범위가 아니어서 개인 판단을 확정하기 어렵다.
- QA 기준: 프론트 QA 평가서에서는 챗봇 세션 만료 401의 로그인 유도, `filter.js` 모듈 분리, 회원가입·비밀번호 찾기 검증, 인라인 스크립트 정리, 모바일 실기기 QA가 잔여 개선점으로 남았다.
- React 재공학 후 판단: React SPA로 분리해보니 Django는 화면을 직접 조립하기보다 DB, 인증, LLM 호출 결과를 JSON API로 제공하는 구조가 더 명확해 보였다.

## 경험 로그

- 의사결정: [[프로젝트 의사결정 로그#4차 LG Home]]
- 실패/디버깅: [[프로젝트 실패와 디버깅 로그#4차 LG Home]]
- 경험 MOC: [[프로젝트 경험 MOC#4차 LG Home]]

## 실패 조건

- 챗봇이 제품 상담 범위 밖 질문을 처리하려 하면 서비스 목적이 흐려진다.
- 후속 질문 판별이 틀리면 이전 조건을 잘못 이어받거나 새 질문을 놓친다.
- Pinecone/OpenAI API key가 모듈 import 시점에 강하게 필요하면 Django check나 배포가 실패할 수 있다.
- CSRF와 credentials 처리를 페이지마다 따로 만들면 AJAX 실패가 화면별로 다르게 나타난다.

## 다음 보강 노트

- [[Django Chatbot]]
- [[LangGraph]]
- [[Vector Store]]
- [[Django JSON API]]
- [[React SPA]]

## 먼저 확인할 질문

- 현재 질문은 상품 DB 검색인가, 매뉴얼 RAG인가, 대화 맥락 이어가기인가?
- 공식 프로젝트 근거와 개인 확장 근거가 한 문장 안에서 섞이지 않았는가?
