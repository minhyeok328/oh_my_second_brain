---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'pytorch'
  - 'deep-learning'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html'
source_quality: 'mixed'
verified: false
id: '20260530000000-ea2d'
---

# PyTorch 학습 루프 치트시트

## 용도

미니배치 학습과 평가 루프에서 모드 전환과 그래디언트 갱신 순서를 확인한다.

## 빠른 참조

```python
model.train()
for X, y in train_loader:
    pred = model(X)
    loss = loss_fn(pred, y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
```

평가에서는 `model.eval()`로 모드를 바꾸고 `torch.no_grad()` 또는 현재 공식 문서가 권장하는 추론 컨텍스트에서 그래디언트 기록을 끈다.

## 사용 전 확인

- 입력과 모델이 같은 device와 dtype에 있는지 확인한다.
- loss 집계의 분모가 batch 수인지 sample 수인지 기록한다.
- scheduler, gradient clipping, mixed precision, gradient accumulation은 실험 설정과 함께 별도 기록한다.

## 검증 범위

- 2026-08-11: PyTorch 공식 Optimization tutorial에서 학습·평가 모드와 기본 갱신 순서를 확인했다.
- 실제 모델, 데이터 로더, 분산 학습, AMP와 optimizer별 세부 동작은 검증하지 않았다.

## 관련 노트

- [[20 소스 노트/강의/딥러닝 기초 강의|딥러닝 기초 강의]]
- [[20 소스 노트/강의/NLP 딥러닝 강의|NLP 딥러닝 강의]]
- [[학습 데이터와 평가 데이터는 모델 선택 전에 분리해야 한다]]
