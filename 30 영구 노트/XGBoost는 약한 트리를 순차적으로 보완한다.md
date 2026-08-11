---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'machine_learning'
  - 'xgboost'
  - 'boosting'
aliases:
  - 'XGBoost'
sources:
  - 'https://xgboost.readthedocs.io/en/stable/tutorials/model.html'
  - 'https://arxiv.org/abs/1603.02754'
  - 'C:\MinHyeok\lecture\05_machine_learning_workspace'
source_quality: 'mixed'
verified: true
id: '20260530000000-4a0c'
---

# XGBoost는 약한 트리를 순차적으로 보완한다

## 주장

XGBoost의 tree booster는 기존 앙상블의 예측을 고정한 채 목적함수를 줄이는 새 트리를 하나씩 더하는 가법 학습을 사용한다. 그러므로 [[특성 공학은 모델보다 먼저 데이터 표현을 개선한다]]로 입력을 정리한 뒤에도 트리 수·깊이·규제 조건을 [[MLflow는 실험 조건과 결과를 함께 추적한다]]의 run에 함께 남겨야 비교가 가능하다.

## 연결

[[머신러닝 강의]]의 부스팅 실습을 내 관점으로 정리하면, 모델 이름보다 분할 방식과 [[분류 평가는 클래스 불균형에 맞는 지표를 선택해야 한다]]의 평가 계약을 먼저 고정해야 XGBoost 결과를 다른 모델과 공정하게 비교할 수 있다.

## 한계와 반례

새 트리가 이전 오차를 보완한다는 구조가 모든 표 데이터에서 우월함을 뜻하지 않는다. 잡음이 많거나 데이터가 작으면 복잡한 앙상블이 과적합할 수 있고, 순차 학습은 독립적으로 만든 트리의 단순 병렬 학습과 다르다. 성능은 학습률·규제·트리 수와 평가 분할에 의존한다.

## 확인한 근거

- 2026-08-11: XGBoost 공식 boosted tree 문서에서 학습 손실과 규제를 합한 목적함수, 기존 예측에 새 트리를 하나씩 더하는 additive training을 확인했다.
- 2026-08-11: Chen과 Guestrin의 원 논문에서 XGBoost가 확장 가능한 tree boosting 시스템이며 희소 데이터와 근사 트리 학습을 위한 알고리즘을 제시한 범위를 확인했다.
- 강의 자료 확인(개인 해석): 승인된 `05_machine_learning_workspace`에서 boosting 계열 모델 실습을 확인했으며, 모델 비교에는 동일한 분할과 평가 계약이 필요하다고 해석했다.
