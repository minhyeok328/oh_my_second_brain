---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'sklearn'
  - 'reference'
source:
  - 'C:\lecture'
source_quality: 'mixed'
verified: false
id: '20260530000000-30a2'
---

# Scikit-learn 워크플로우

태그: #sklearn #reference #llm_wiki

## 용도

전처리부터 평가까지의 기본 모델링 순서다.

## 빠른 참조

- `train_test_split(X, y)`: 데이터 분리
- `scaler.fit(X_train)`: 전처리 학습
- `model.fit(X_train, y_train)`: 모델 학습
- `model.predict(X_test)`: 예측
- `cross_val_score(model, X, y, cv=5)`: 교차검증

## 관련 노트

- [[Scikit-learn Estimator]]
- [[Train Test Split]]
- [[교차검증]]
