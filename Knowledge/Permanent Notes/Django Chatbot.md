---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'llm'
  - 'web_server'
source:
  - 'C:\lecture'
---

# Django Chatbot

태그: #django #llm #web_server #llm_wiki

## 한 줄 정의

Django 웹 서버에서 LLM API를 호출해 사용자 메시지에 응답하는 챗봇 애플리케이션 구조다.

## 왜 중요한가

프론트엔드 입력, 서버 세션, 외부 모델 API, 응답 렌더링을 하나의 웹 서비스로 통합한다.

## 핵심 개념

- View가 사용자 메시지를 받는다.
- LLM API 호출 결과를 저장하거나 화면에 반환한다.
- 세션 또는 DB로 대화 기록을 관리한다.

## 예제

```text
browser -> Django view -> LLM API -> response -> template/json
```

## 실무 활용

사내 Q&A, 학습 도우미, 문서 검색 챗봇의 웹 서버 기반 구현에 사용한다.

## 관련 개념

- [[OpenAI API]]
- [[Django Session과 Auth]]
- [[RAG]]

자료 힌트: 11_web_server_workspace/_06_chatbot

## 내 말로 다시 설명

Django Chatbot은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[OpenAI API]], [[Django Session과 Auth]], [[RAG]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- Django Chatbot을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
