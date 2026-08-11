---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'pandas'
  - 'data_analysis'
source:
  - 'C:\lecture'
external:
  - 'https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html'
source_quality: 'mixed'
verified: false
id: '20260530000000-922d'
---

# Pandas DataFrame

태그: #llm_wiki #pandas #data_analysis

## 한 줄 정의

Pandas DataFrame은 행과 열 인덱스를 가진 2차원 표 데이터 구조로, 정형 데이터를 정리, 필터링, 집계, 결합하는 중심 도구다.

## 내 말로 다시 설명

DataFrame은 엑셀 표처럼 보이지만, 내부적으로는 컬럼별 dtype과 인덱스를 가진 분석 객체다. 데이터 분석에서 "데이터가 지금 어떤 행 단위와 열 의미를 갖는가"를 명확히 드러내는 그릇이다.

## 핵심 개념

- row index: 행을 식별하거나 정렬 기준이 되는 축이다.
- column: 변수 또는 feature를 나타낸다.
- dtype: 각 컬럼의 연산 가능성을 결정한다.
- missing value: 결측치 처리 전략이 분석 결과를 바꾼다.
- vectorized operation: 반복문보다 컬럼 단위 연산을 우선한다.

## 언제 쓰는가

- CSV, Excel, SQL 결과처럼 행/열 구조가 있는 데이터를 다룰 때
- [[Pandas GroupBy]], [[Pandas Merge]], [[Pandas 인덱싱]]이 필요한 분석 흐름
- 모델링 전 EDA와 feature engineering을 할 때

## 언제 쓰면 안 되는가

- 데이터가 너무 커서 메모리에 올릴 수 없는 경우
- 이미지, 오디오, 그래프처럼 표 구조가 본질이 아닌 경우
- 엄격한 schema와 transaction이 필요한 운영 저장소 역할

## 자주 헷갈리는 점

- index는 그냥 행 번호가 아니라 정렬, join, selection에 영향을 주는 축이다.
- view와 copy 경고는 원본 변경 여부가 모호할 때 생긴다.
- `object` dtype은 문자열뿐 아니라 섞인 타입을 포함할 수 있다.

## 작은 예제

```python
import pandas as pd

df = pd.DataFrame({
    "team": ["A", "A", "B"],
    "score": [10, 15, 8],
})
summary = df.groupby("team")["score"].mean()
```

## 관련 개념

- [[Pandas Series]]
- [[Pandas GroupBy]]
- [[Pandas Merge]]
- [[Pandas 결측치 처리]]
- [[EDA]]

## 확인 질문

- 현재 행 하나는 무엇을 의미하는가?
- 분석 전 index, dtype, 결측치를 확인했는가?

## 외부 참조

- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
