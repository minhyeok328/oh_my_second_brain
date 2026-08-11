---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'pandas'
  - 'reference'
source:
  - 'C:\lecture'
source_quality: 'mixed'
verified: false
id: '20260530000000-bebd'
---

# Pandas 치트시트

태그: #pandas #reference #llm_wiki

## 용도

DataFrame 분석에서 자주 쓰는 명령이다.

## 빠른 참조

- `pd.read_csv(path)`: CSV 로딩
- `df.info()`: 컬럼과 결측 확인
- `df.loc[mask, cols]`: 조건 기반 선택
- `df.groupby(col).agg(...)`: 그룹 집계
- `df.merge(other, on=key)`: 테이블 결합

## 관련 노트

- [[Pandas DataFrame]]
- [[Pandas GroupBy]]
- [[Pandas Merge]]
