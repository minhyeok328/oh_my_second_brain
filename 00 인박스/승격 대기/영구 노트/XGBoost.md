---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'machine_learning'
  - 'xgboost'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-4a0c'
---

# XGBoost

태그: #llm_wiki #machine_learning #xgboost

## 한 줄 정의

XGBoost는 gradient boosting tree 기반의 강력한 지도학습 모델로, tabular 데이터의 분류·회귀 문제에서 자주 쓰인다.

## 내 말로 다시 설명

XGBoost는 여러 약한 결정트리를 순차적으로 쌓아 이전 모델의 오류를 줄인다. 성능이 좋지만 튜닝과 검증을 잘못하면 train 성능만 높고 실제 일반화는 낮을 수 있다.

## 언제 쓰는가

- tabular feature로 이탈, 등급, 위험도 같은 label을 예측할 때
- 선형 모델보다 변수 간 비선형 관계와 상호작용이 중요할 때
- feature importance와 성능 비교가 필요한 ML 프로젝트에서 baseline 이후 강한 모델이 필요할 때

## 언제 쓰면 안 되는가

- 데이터 수가 너무 작아 검증 분산이 큰 경우
- class imbalance와 overfitting을 평가하지 않고 정확도만 보는 경우
- 모델 결과를 비즈니스 전략으로 연결할 설명이 없는 경우

## 프로젝트 예시

[[SKN26 2차 신용카드 고객 이탈 분석]]에서 XGBoost는 카드 고객 이탈과 Income 예측 실험에 사용되었다. `model_evaluation.md`에서는 multi-class income 정확도가 낮았고, Low/High binary 재구성 실험에서 높은 성능을 확인했다.

## 실패 조건

- train/test 성능 차이를 보지 않으면 과적합을 놓친다.
- multi-class가 낮은 이유를 데이터 분포나 class 경계로 분석하지 않으면 모델만 바꾸는 반복이 된다.
- Unknown 값 보정 모델을 실제 pipeline에 반영했는지와 실험 결과만 있는지를 구분해야 한다.

## 관련 개념

- [[결정트리]]
- [[앙상블 학습]]
- [[Feature Engineering]]
- [[과적합]]
- [[MLflow]]

## 먼저 확인할 질문

- 이 모델의 목표는 최종 예측인가, 결측/Unknown 보정인가?
- 성능 지표가 비즈니스 의사결정에 필요한 오류 비용을 반영하는가?
