---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'pandas'
  - 'data-analysis'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://pandas.pydata.org/docs/user_guide/10min.html'
source_quality: 'mixed'
verified: false
id: '20260530000000-bebd'
---

# Pandas 치트시트

## 용도

DataFrame을 읽고 구조를 살피고 선택·집계·결합할 때 자주 쓰는 표현을 모은다.

## 빠른 참조

- `pd.read_csv(path)`: CSV를 DataFrame으로 읽기
- `df.info()`: 열, dtype, non-null 개수와 메모리 정보 확인
- `df.loc[mask, cols]`: label과 boolean 조건으로 행·열 선택
- `df.groupby(key).agg(...)`: 그룹별 집계
- `df.merge(other, on=key, validate=...)`: 키를 기준으로 결합하고 예상 관계 검증

## 사용 전 확인

- 파일 인코딩, dtype, 날짜 파싱, 결측치 표현을 명시한다.
- 결합 전 양쪽 키의 중복과 null을 확인하고 가능한 경우 `validate`로 관계를 제한한다.
- 수정할 때 chained assignment에 기대지 말고 `.loc`로 대상 범위를 명시한다.

## 검증 범위

- 2026-08-11: pandas 공식 사용자 가이드에서 데이터 읽기, 선택, 그룹화와 결합 API를 확인했다.
- 실제 데이터의 스키마와 pandas 버전별 dtype·Copy-on-Write 동작 차이는 검증하지 않았다.

## 관련 노트

- [[DataFrame은 열 단위 데이터 변환을 구조화한다]]
- [[20 소스 노트/강의/데이터 분석 강의|데이터 분석 강의]]
- [[학습 데이터와 평가 데이터는 모델 선택 전에 분리해야 한다]]
