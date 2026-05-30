---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'designpattern'
  - 'oop'
  - 'behavioral'
source:
  - 'C:\lecture'
---

# Strategy Pattern

태그: #designpattern #oop #behavioral #llm_wiki

## 한 줄 정의

알고리즘군을 캡슐화해 실행 시점에 교체 가능하게 하는 행위 패턴이다.

## 왜 중요한가

디자인 패턴은 반복되는 설계 문제에 이름을 붙인 해법이다. 이름이 붙으면 팀 안에서 구조, 장단점, 적용 시점을 짧게 공유할 수 있다.

## 핵심 개념

- 문제 상황, 참여 객체, 협력 방식으로 이해한다.
- 패턴은 정답 코드가 아니라 설계 어휘다.
- 적용하면 복잡도가 줄어드는지, 오히려 추상화가 늘어나는지 함께 판단한다.

## 예제

```python
context.set_strategy(QuickSort())
```

## 실무 활용

Java와 Python 예제처럼 객체 협력 구조를 연습한 뒤, Django 서비스 계층, React 컴포넌트 조합, LLM 도구 실행 구조에 맞게 응용한다.

## 관련 개념

- [[State Pattern]]
- [[Template Method Pattern]]
- [[Scikit-learn Estimator]]

자료 힌트: 13_react-cicd_workspace/02_design_pattern/.../strategy

## 내 말로 다시 설명

Strategy Pattern은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[State Pattern]], [[Template Method Pattern]], [[Scikit-learn Estimator]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- Strategy Pattern을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
