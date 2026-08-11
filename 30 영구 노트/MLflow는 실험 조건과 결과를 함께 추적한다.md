---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'machine_learning'
  - 'mlops'
  - 'experiment_tracking'
aliases:
  - 'MLflow'
sources:
  - 'https://mlflow.org/docs/latest/ml/tracking/'
  - 'https://mlflow.org/docs/latest/ml/tracking/tracking-api/'
source_quality: 'primary'
verified: true
id: '20260530000000-417b'
---

# MLflow는 실험 조건과 결과를 함께 추적한다

## 주장

MLflow Tracking은 한 번의 학습 실행을 run으로 묶어 파라미터, 지표, 코드 버전과 산출물을 함께 기록한다. 따라서 [[XGBoost는 약한 트리를 순차적으로 보완한다]] 같은 모델의 설정과 [[분류 평가는 클래스 불균형에 맞는 지표를 선택해야 한다]]의 측정값을 같은 실행 문맥에서 비교할 수 있다.

## 연결

여러 사람이 같은 기록을 보려면 추적 서버와 저장소 구성이 필요하므로 [[Docker Compose는 여러 컨테이너의 실행 계약을 한곳에 모은다]]와 연결된다. 내 운영 규칙은 모델 파일만 남기지 않고 그 파일을 만든 run과 데이터 조건을 함께 식별하는 것이다.

## 한계와 반례

내 운영 판단: run 기록만으로 재현성과 배포 모델 선택이 완료됐다고 취급하지 않는다. 내가 적용할 규칙은 데이터 버전, 실행 환경과 평가 기준을 별도로 식별하고, 가장 최근 run이 아니라 미리 정한 승인 기준을 통과한 run을 선택하는 것이다. 일회성 탐색에는 필요한 기록 범위를 줄일 수 있다.

## 확인한 근거

- 2026-08-11: MLflow 공식 Tracking 문서에서 run이 파라미터·지표·시작/종료 시각 같은 메타데이터와 모델 파일 등의 산출물을 함께 기록하는 단위임을 확인했다.
- 2026-08-11: MLflow 공식 Tracking API 문서에서 파라미터, 지표, 데이터셋 정보와 산출물을 명시적으로 기록하는 API 범위를 확인했다.
