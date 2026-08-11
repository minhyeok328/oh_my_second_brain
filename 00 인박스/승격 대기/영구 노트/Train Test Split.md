---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'machinelearning'
  - 'sklearn'
  - 'evaluation'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project\model_evaluation.md'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project\notebooks\YooDongHyun\major_feature_LDA_commented.ipynb'
source_quality: 'mixed'
verified: false
id: '20260530000000-d474'
---

# Train Test Split

태그: #machinelearning #sklearn #evaluation #llm_wiki

## 한 줄 정의

Train Test Split은 모델이 학습에 사용한 데이터와 성능 평가에 사용할 데이터를 분리해 일반화 성능을 확인하는 절차다.

## 왜 중요한가

훈련 데이터에서 좋은 성능은 암기일 수 있다. 모델이 처음 보는 고객에게도 통하는지 보려면 학습에 사용하지 않은 test set이 필요하다. 특히 Unknown 값 보정처럼 정답이 없는 데이터에 모델을 적용할 때는, 먼저 정답이 있는 known 데이터에서 train/test 평가를 끝내야 한다.

## 핵심 개념

- `train_test_split`은 feature와 target을 같은 index 기준으로 나눈다.
- 분류 문제에서는 가능하면 `stratify`로 클래스 비율을 보존한다.
- scaler, encoder, imputer는 train에 `fit`하고 test에는 `transform`만 한다.
- test set은 모델 선택을 반복하는 개발용 점수판이 아니라 최종 확인용에 가깝다.
- Unknown 추론 데이터는 test set이 아니다. 정답이 없으면 성능 평가가 아니라 적용 대상이다.

## 프로젝트 예시

[[SKN26 2차 신용카드 고객 이탈 분석]]의 income 보정 실험은 known income과 unknown income을 먼저 분리했다.

- known 데이터: income label이 있는 고객
- unknown 데이터: income label이 없어 예측 적용 대상인 고객
- train: 7,280건
- test: 1,820건
- feature 수: 20개
- target: `income_id`

`model_evaluation.md`의 train/test 성능 차이는 과적합과 문제 재정의 필요성을 판단하는 근거가 됐다. multi-class에서는 train accuracy 0.8044, test accuracy 0.5989로 차이가 컸고, Low/High binary 재구성에서는 test accuracy 0.9027로 개선 가능성을 확인했다.

## 언제 쓰는가

- 새로운 분류/회귀 모델의 일반화 성능을 확인할 때
- Unknown 값을 예측하기 전에 known 데이터에서 검증 구조를 만들 때
- feature engineering이나 scaling이 데이터 누수를 만들지 점검할 때
- 모델별 성능을 MLflow 같은 실험 관리 도구에 비교 기록할 때

## 언제 쓰면 안 되는가

- 시계열처럼 시간 순서가 중요한 데이터를 무작위로 섞으면 안 되는 경우
- 같은 고객의 여러 row가 train과 test에 동시에 들어가 누수가 생기는 경우
- test 성능을 계속 보며 feature와 파라미터를 반복 조정하는 경우
- 전체 데이터에 scaler를 fit한 뒤 split해서 이미 누수가 생긴 경우

## 실패 조건

- class 비율이 train/test에서 크게 달라지면 소수 클래스 지표가 흔들린다.
- 전처리 객체를 전체 데이터에 fit하면 test 정보가 train에 새어 들어간다.
- Unknown 데이터를 train에 섞으면 label 의미가 흐려져 보정 모델이 오염된다.
- random_state를 고정하지 않으면 실험 결과 재현과 비교가 어려워진다.
- train/test 지표 차이를 보지 않으면 과적합을 성능 개선으로 착각할 수 있다.

## 관련 개념

- [[분류 평가 지표]]
- [[과적합]]
- [[데이터 전처리]]
- [[Feature Engineering]]
- [[SKN26 2차 신용카드 고객 이탈 분석]]

## 먼저 확인할 질문

- split 전에 target과 feature를 명확히 분리했는가?
- scaler, encoder, imputer는 train에만 fit했는가?
- test set이 모델 선택 과정에서 반복적으로 소비되고 있지는 않은가?
- Unknown 데이터는 평가 대상인가, 예측 적용 대상인가?
