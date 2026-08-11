---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'machinelearning'
  - 'data_analysis'
  - 'feature_engineering'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project\README.md'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project\model_evaluation.md'
source_quality: 'mixed'
verified: false
id: '20260530000000-679d'
---

# Feature Engineering

태그: #machinelearning #data_analysis #feature_engineering #llm_wiki

## 한 줄 정의

Feature Engineering은 원본 데이터를 모델이 더 잘 학습하고 사람이 더 잘 해석할 수 있는 변수 표현으로 바꾸는 과정이다.

## 왜 중요한가

모델 성능은 알고리즘만으로 결정되지 않는다. 카드 이탈처럼 행동 변화가 중요한 문제에서는 단순 고객 속성보다 거래 횟수 변화, 사용률, 비활성 기간, 고객센터 접촉 같은 행동 피처가 더 강한 신호가 된다. 좋은 feature는 모델 성능과 비즈니스 해석을 동시에 돕는다.

## 핵심 개념

- 원본 컬럼을 조합해 행동 변화나 비율을 만든다.
- 범주형 변수는 모델이 읽을 수 있게 encoding한다.
- numeric feature는 필요한 경우 scaling한다.
- target 이후에만 알 수 있는 정보는 feature로 쓰면 안 된다.
- feature importance는 모델 설명의 출발점이지 곧바로 인과 해석은 아니다.

## 프로젝트 예시

[[SKN26 2차 신용카드 고객 이탈 분석]]은 카드 고객의 이탈 신호를 고객 속성보다 행동 변수에서 더 강하게 찾았다.

- `Total_Trans_Ct`: 연간 총 거래 횟수
- `Total_Trans_Amt`: 연간 총 거래 금액
- `Avg_Utilization_Ratio`: 신용 한도 대비 사용률
- `Total_Ct_Chng_Q4_Q1`: 거래량 변화율
- `Months_Inactive_12_mon`: 최근 12개월 비활성 개월 수
- `Contacts_Count_12_mon`: 고객센터 연락 횟수

Unknown Income 보정 실험에서는 income이 있는 known 데이터와 unknown 데이터를 분리하고, 고객 속성/행동 feature로 income class를 예측했다. multi-class 성능이 낮게 나오자 Low/High binary 재구성이라는 문제 정의 변경도 feature 해석 결과와 함께 검토했다.

## 언제 쓰는가

- 원본 컬럼만으로 모델이 도메인 신호를 잡기 어려울 때
- 비율, 변화량, 기간, 빈도처럼 해석 가능한 행동 지표가 필요할 때
- Unknown 값 보정이나 고객 세그먼트 분류처럼 feature 분포 비교가 중요한 때
- 모델 결과를 비즈니스 전략으로 설명해야 할 때

## 언제 쓰면 안 되는가

- target 정보를 직접 또는 간접적으로 담은 컬럼을 feature로 만들 때
- test나 unknown 데이터 분포를 보고 feature를 과하게 맞출 때
- 모델 성능만 보고 사람이 설명할 수 없는 feature를 무작정 늘릴 때
- 결측/Unknown의 의미를 확인하지 않고 단순 숫자 대체만 할 때

## 실패 조건

- feature가 많아져도 신호보다 노이즈가 늘면 test 성능은 떨어질 수 있다.
- train/test 분리 전에 encoding, scaling, imputation을 fit하면 데이터 누수가 생긴다.
- Unknown 값을 학습 라벨처럼 다루면 예측 보정 모델이 오염된다.
- feature importance를 인과관계로 해석하면 잘못된 비즈니스 전략이 나올 수 있다.
- 데이터셋의 마스킹된 범주나 임계치를 실제 금융 운영 기준처럼 단정하면 위험하다.

## 관련 개념

- [[데이터 전처리]]
- [[Train Test Split]]
- [[분류 평가 지표]]
- [[XGBoost]]
- [[SKN26 2차 신용카드 고객 이탈 분석]]

## 먼저 확인할 질문

- 이 feature는 예측 시점에 실제로 알 수 있는 값인가?
- 이 feature가 모델 성능뿐 아니라 결과 해석에도 도움이 되는가?
- Unknown이나 결측값은 삭제, 별도 class, 예측 보정 중 어떤 의미로 처리하는가?
- feature 생성과 전처리가 train/test split 이후 올바른 순서로 적용되는가?
