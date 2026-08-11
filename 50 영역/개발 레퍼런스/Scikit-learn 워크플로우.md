---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'scikit-learn'
  - 'machine-learning'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://scikit-learn.org/stable/common_pitfalls.html'
  - 'https://scikit-learn.org/stable/modules/cross_validation.html'
source_quality: 'mixed'
verified: false
id: '20260530000000-30a2'
---

# Scikit-learn 워크플로우

## 용도

데이터 분리부터 전처리, 학습과 평가까지 누수를 줄이는 기본 순서를 확인한다.

## 빠른 참조

1. `train_test_split(X, y, ...)`로 최종 평가 데이터를 먼저 분리한다.
2. 전처리기와 모델을 `Pipeline`으로 묶어 학습 fold 안에서만 전처리기를 `fit`한다.
3. `pipeline.fit(X_train, y_train)`으로 학습한다.
4. `pipeline.predict(X_test)`와 문제에 맞는 지표로 최종 평가한다.
5. 모델 선택은 훈련 데이터 안에서 `cross_validate(...)` 또는 적절한 교차검증 도구로 수행한다.

## 사용 전 확인

- 분류 데이터는 class 비율, 그룹·시간 구조와 중복 개체를 고려해 split 전략을 선택한다.
- 최종 test set으로 하이퍼파라미터를 반복 조정하지 않는다.
- random seed, split 기준, 전처리와 metric을 실험 기록에 남긴다.

## 검증 범위

- 2026-08-11: scikit-learn 공식 common pitfalls와 cross-validation 문서에서 분리, Pipeline과 교차검증 원칙을 확인했다.
- 데이터셋별 split 전략, estimator 호환성, metric 선택과 계산 비용은 검증하지 않았다.

## 관련 노트

- [[학습 데이터와 평가 데이터는 모델 선택 전에 분리해야 한다]]
- [[분류 평가는 클래스 불균형에 맞는 지표를 선택해야 한다]]
- [[특성 공학은 모델보다 먼저 데이터 표현을 개선한다]]
- [[20 소스 노트/강의/머신러닝 강의|머신러닝 강의]]
