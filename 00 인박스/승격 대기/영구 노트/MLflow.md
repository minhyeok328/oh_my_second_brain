---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'machine_learning'
  - 'mlops'
source:
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-417b'
---

# MLflow

태그: #llm_wiki #machine_learning #mlops

## 한 줄 정의

MLflow는 머신러닝 실험의 run, metric, parameter, artifact, model을 추적하고 재사용하게 해주는 실험 관리 도구다.

## 내 말로 다시 설명

노트북에서 모델을 여러 번 학습하면 어떤 데이터, 파라미터, 성능, 모델 파일이 최종 대시보드에 쓰였는지 흐려진다. MLflow는 실험 결과를 run 단위로 남겨, 나중에 "최신 XGBoost 모델"이나 "가장 성능 좋은 LightGBM 모델"을 코드로 다시 찾을 수 있게 한다.

## 언제 쓰는가

- 여러 모델을 비교하고 성능 기록을 보존해야 할 때
- Streamlit, FastAPI, batch job에서 학습된 모델 artifact를 다시 로드해야 할 때
- 팀원이 각자 만든 모델을 같은 기준으로 비교해야 할 때

## 언제 쓰면 안 되는가

- 한 번 실행하고 버릴 단순 실험이라 추적 비용이 더 클 때
- metric 정의가 정리되지 않아 run 기록만 많아지는 경우
- artifact path와 model flavor 규칙을 정하지 않은 채 dashboard에서 바로 로드하려는 경우

## 프로젝트 예시

[[SKN26 2차 신용카드 고객 이탈 분석]]의 `load_latest_model_by_name.py`는 experiment와 model name을 기준으로 최신 run을 찾고, 모델 flavor에 따라 `mlflow.sklearn`, `mlflow.lightgbm`, `mlflow.pyfunc` loader를 선택한다.

## 자주 헷갈리는 점

- MLflow run 이름과 화면 표시용 모델 이름은 다를 수 있다.
- 최신 run이 항상 운영에 쓸 모델이라는 뜻은 아니다. status, score, artifact path를 함께 확인해야 한다.
- sklearn wrapper로 저장된 XGBoost와 native xgboost flavor는 로더가 다를 수 있다.

## 관련 개념

- [[XGBoost]]
- [[FastAPI]]
- [[Streamlit 기본 UI]]
- [[Docker Compose]]

## 먼저 확인할 질문

- 지금 로드한 모델이 어느 experiment, run id, artifact path에서 왔는가?
- 모델 성능 지표와 실제 서비스에서 쓰는 모델 파일이 같은 run에 묶여 있는가?
