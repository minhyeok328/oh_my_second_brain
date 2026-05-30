---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'sql'
  - 'database'
source:
  - 'C:\lecture'
---

# SQL GROUP BY

태그: #sql #database #llm_wiki

## 한 줄 정의

행을 그룹으로 묶고 집계 함수를 적용하는 SQL 구문이다.

## 왜 중요한가

원자료를 의사결정 가능한 지표로 바꾸는 기본 도구다. 매출, 사용자, 로그 분석에서 필수다.

## 핵심 개념

- `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`와 함께 쓴다.
- `HAVING`은 집계 결과를 필터링한다.
- 그룹 기준 열과 집계 열을 구분해야 한다.

## 예제

```sql
SELECT category, AVG(price)
FROM menu
GROUP BY category;
```

## 실무 활용

EDA, KPI 집계, 피처 엔지니어링의 범주별 통계 생성에 활용한다.

## 관련 개념

- [[Pandas GroupBy]]
- [[SQL SELECT와 WHERE]]
- [[SQL JOIN]]

자료 힌트: 02_mysql_workspace

## 내 말로 다시 설명

SQL GROUP BY은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[Pandas GroupBy]], [[SQL SELECT와 WHERE]], [[SQL JOIN]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- SQL GROUP BY을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
