---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'javascript'
  - 'web'
source:
  - 'C:\lecture'
---

# JavaScript 비동기

태그: #javascript #web #llm_wiki

## 한 줄 정의

네트워크 요청처럼 시간이 걸리는 작업을 블로킹 없이 처리하는 JavaScript 실행 방식이다.

## 왜 중요한가

웹 앱은 API 응답을 기다리면서도 화면이 멈추지 않아야 한다. Promise와 async/await는 이를 다루는 핵심 문법이다.

## 핵심 개념

- Promise는 미래의 성공/실패 값을 표현한다.
- `async/await`는 비동기 코드를 동기 코드처럼 읽게 한다.
- 오류 처리는 `try/catch`로 한다.

## 예제

```js
async function load() {
  const res = await fetch("/api/items");
  return await res.json();
}
```

## 실무 활용

API 호출, 파일 업로드, 챗봇 응답 스트리밍, 동적 웹 스크래핑 이해에 필요하다.

## 관련 개념

- [[DOM Event]]
- [[OpenAPI]]
- [[Django View]]

자료 힌트: 10_web_client_workspace/03_js/03_js_browser/05_async

## 내 말로 다시 설명

JavaScript 비동기은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[DOM Event]], [[OpenAPI]], [[Django View]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- JavaScript 비동기을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
