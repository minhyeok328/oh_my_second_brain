---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'pandas'
  - 'data_analysis'
source:
  - 'C:\lecture'
---

# Pandas Merge

태그: #pandas #data_analysis #llm_wiki

## 한 줄 정의

두 DataFrame을 키 기준으로 결합하는 기능이다.

## 왜 중요한가

분석에 필요한 정보가 여러 테이블에 나뉘어 있을 때 하나의 학습/분석 테이블로 조립한다.

## 핵심 개념

- `merge`는 SQL JOIN과 유사하다.
- `how`로 inner, left, right, outer 방식을 고른다.
- 키 중복은 행 수 증가를 만들 수 있다.

## 예제

```python
result = users.merge(orders, on="user_id", how="left")
```

## 실무 활용

주문과 사용자 속성 결합, 추천 데이터 생성, 피처 테이블 조립에 쓰인다.

## 관련 개념

- [[SQL JOIN]]
- [[Pandas DataFrame]]
- [[Feature Engineering]]

자료 힌트: 04_data_analysis_workspace/02_pandas

## 내 말로 다시 설명

Pandas Merge은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[SQL JOIN]], [[Pandas DataFrame]], [[Feature Engineering]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- Pandas Merge을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
