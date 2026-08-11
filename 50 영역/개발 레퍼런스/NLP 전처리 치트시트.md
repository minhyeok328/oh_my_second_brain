---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'nlp'
  - 'preprocessing'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://huggingface.co/docs/transformers/main_classes/tokenizer'
  - 'https://scikit-learn.org/stable/modules/feature_extraction.html'
  - '[[20 소스 노트/강의/NLP 딥러닝 강의|NLP 딥러닝 강의]]'
source_quality: 'mixed'
verified: false
id: '20260530000000-bfe9'
---

# NLP 전처리 치트시트

## 용도

텍스트를 규칙 기반 특징이나 모델 입력으로 바꾸기 전에 확인할 최소 단계다.

## 빠른 참조

- `text.strip()`: 앞뒤 공백 제거
- `text.lower()`: 대소문자 구분을 버리기로 한 실험에서 소문자화
- `tokenizer(text, padding=..., truncation=...)`: 사용 중인 Transformers tokenizer로 모델 입력 구성
- `TfidfVectorizer().fit_transform(texts)`: scikit-learn으로 말뭉치의 TF-IDF 특징 행렬 생성

## 사용 전 확인

- 소문자화, 특수문자 제거, 불용어 제거가 이름·코드·감성 같은 신호를 없애지 않는지 먼저 비교한다.
- tokenizer는 사용할 모델과 같은 체크포인트에서 불러오고 최대 길이, padding, truncation 정책을 기록한다.
- 학습·평가 분리 전 전체 데이터에 vectorizer를 `fit`하지 않는다.

## 검증 범위

- 2026-08-11: Hugging Face Transformers tokenizer와 scikit-learn feature extraction 공식 문서에서 API 역할을 확인했다.
- 한국어 형태소 분석, 특정 모델 tokenizer 설정, 정규화 규칙의 성능 영향은 검증하지 않았다. 데이터셋별 실험 전 확인이 필요하다.

## 관련 노트

- [[20 소스 노트/강의/NLP 딥러닝 강의|NLP 딥러닝 강의]]
- [[학습 데이터와 평가 데이터는 모델 선택 전에 분리해야 한다]]
- [[특성 공학은 모델보다 먼저 데이터 표현을 개선한다]]
