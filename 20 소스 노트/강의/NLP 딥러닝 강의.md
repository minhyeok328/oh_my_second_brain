---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'lecture'
  - 'nlp'
aliases: []
sources:
  - 'C:\MinHyeok\lecture\07_deep_learning_nlp_workspace'
source_path: 'C:\MinHyeok\lecture\07_deep_learning_nlp_workspace'
source_quality: 'primary'
verified: true
id: '20260530000000-7ecf'
---

# NLP 딥러닝 강의

## 출처

- 원본 경로: `C:\MinHyeok\lecture\07_deep_learning_nlp_workspace`
- 확인일: 2026-08-11

## 핵심 내용

- 관찰: `02_preprocessing`은 토큰화, 정제·정규화, 어간·표제어, 정규식, 정수 인코딩·패딩, 원-핫 인코딩을 분리해 실습한다.
- 관찰: `03_text_vectorization`은 BoW·DTM·TF-IDF, 임베딩, PyTorch 임베딩과 FastText를 비교한다.
- 관찰: `04_sequence_model`은 RNN, LSTM, GRU를 감성 분류와 주가 예측 예제로 연결한다.
- 관찰: `08_seq2seq\01_seq2seq_translation.ipynb`는 데이터 전처리, 인코더·디코더, 교사 강요, 학습과 추론 모델을 번역 과제로 구성한다.
- 관찰: `09_transformer`는 단일·다중 헤드 자기 주의와 위치 인코딩, 인코더·디코더 구현을 다루며, `10_transfer_learning`은 BERT 기반 전이 학습과 파이프라인 과제로 이어진다.

## 내 해석과 의문

- 해석: 텍스트를 토큰과 벡터로 바꾸는 선택이 뒤의 모델 입력과 평가 방식까지 제약한다는 흐름으로 읽힌다.
- 질문: 한국어 토큰화·정규화 선택이 데이터셋과 과제에 따라 어떤 오류를 만드는가?
- 질문: Seq2Seq와 Transformer 예제를 같은 번역 데이터와 평가 지표로 비교할 수 있는가?

## 분리한 영구 노트

- 토큰화는 모델이 처리할 텍스트 단위를 정한다 — 후속 영구 노트 후보
- TF-IDF는 문서 집합 안에서 단어의 상대적 중요도를 표현한다 — 후속 영구 노트 후보
- LSTM은 순환 상태에 게이트를 더한다 — 후속 영구 노트 후보
- 자기 주의는 토큰 사이의 관련도를 가중합으로 반영한다 — 후속 영구 노트 후보
