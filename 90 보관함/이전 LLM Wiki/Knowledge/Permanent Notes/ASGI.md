---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'asgi'
  - 'django'
  - 'devops'
source:
  - 'C:\lecture'
---

# ASGI

태그: #asgi #django #devops #llm_wiki

## 한 줄 정의

동기와 비동기 Python 웹 애플리케이션을 모두 지원하는 인터페이스 표준이다.

## 왜 중요한가

실시간 기능, WebSocket, 장시간 연결, 비동기 처리가 필요한 웹 앱에서 중요하다.

## 핵심 개념

- Django의 `asgi.py`가 진입점이다.
- HTTP와 WebSocket 같은 여러 프로토콜을 지원한다.
- Uvicorn, Daphne 같은 서버와 함께 쓴다.

## 예제

```bash
uvicorn project.asgi:application --host 0.0.0.0 --port 8000
```

## 실무 활용

실시간 챗봇, 스트리밍 응답, 비동기 API 서버 배포에 사용한다.

## 관련 개념

- [[WSGI]]
- [[Gunicorn과 Uvicorn]]
- [[Django Chatbot]]

자료 힌트: 12_devops_workspace/03_wsgi_asgi/02_asgi

## 내 말로 다시 설명

ASGI은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[WSGI]], [[Gunicorn과 Uvicorn]], [[Django Chatbot]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- ASGI을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
