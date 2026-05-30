---
type: "reference"
status: "reference"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'nlp'
  - 'reference'
source:
  - 'C:\lecture'
---

# NLP 전처리 치트시트

태그: #nlp #reference #llm_wiki

## 용도

텍스트 정제와 벡터화의 기본 단계를 정리한다.

## 빠른 참조

- `text.lower().strip()`: 기본 정규화
- `tokenizer.encode(text)`: 토큰 ID 변환
- `TfidfVectorizer().fit_transform(texts)`: TF-IDF 벡터화
- `padding/truncation`: 입력 길이 맞춤

## 관련 노트

- [[NLP 전처리]]
- [[토큰화]]
- [[BoW와 TF-IDF]]
