---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'numpy'
  - 'data_analysis'
source:
  - 'C:\lecture'
---

# NumPy ndarray

태그: #numpy #data_analysis #llm_wiki

## 한 줄 정의

동일한 타입의 값을 다차원 배열로 저장하고 벡터화 연산을 제공하는 NumPy 핵심 구조다.

## 왜 중요한가

Pandas, scikit-learn, PyTorch 모두 배열 계산의 사고방식을 공유한다. ndarray는 수치 계산의 기초다.

## 핵심 개념

- `shape`은 배열 차원을 나타낸다.
- 벡터화 연산은 반복문보다 빠르고 간결하다.
- 슬라이싱과 불리언 마스킹을 지원한다.

## 예제

```python
import numpy as np
arr = np.array([[1, 2], [3, 4]])
arr.mean(axis=0)
```

## 실무 활용

피처 행렬, 이미지 픽셀, 모델 입력 텐서를 이해하는 출발점이다.

## 관련 개념

- [[NumPy 브로드캐스팅]]
- [[Pandas DataFrame]]
- [[PyTorch Tensor]]

자료 힌트: 04_data_analysis_workspace/01_numpy

## 내 말로 다시 설명

NumPy ndarray은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[NumPy 브로드캐스팅]], [[Pandas DataFrame]], [[PyTorch Tensor]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- NumPy ndarray을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
