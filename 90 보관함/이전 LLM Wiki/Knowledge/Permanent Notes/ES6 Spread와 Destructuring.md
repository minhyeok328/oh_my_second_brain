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

# ES6 Spread와 Destructuring

태그: #javascript #web #llm_wiki

## 한 줄 정의

배열과 객체를 펼치거나 필요한 값만 꺼내는 ES6 문법이다.

## 왜 중요한가

불변 업데이트와 API 응답 파싱을 간결하게 만든다.

## 핵심 개념

- spread는 `...`로 값을 펼친다.
- destructuring은 구조에서 값을 바로 할당한다.
- 중첩 구조에서는 기본값을 함께 쓰면 안전하다.

## 예제

```js
const { name, age = 0 } = user;
const next = { ...user, active: true };
```

## 실무 활용

프론트엔드 상태 업데이트, 함수 인자 정리, JSON 응답 처리에 사용한다.

## 관련 개념

- [[JavaScript 객체 리터럴]]
- [[JavaScript 배열]]
- [[DOM]]

자료 힌트: 10_web_client_workspace/03_js/02_javascript_es6

## 내 말로 다시 설명

ES6 Spread와 Destructuring은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[JavaScript 객체 리터럴]], [[JavaScript 배열]], [[DOM]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- ES6 Spread와 Destructuring을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
