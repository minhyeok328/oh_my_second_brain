---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'llm'
  - 'ai'
source:
  - 'C:\lecture'
external:
  - 'https://en.wikipedia.org/wiki/Large_language_model'
  - 'https://platform.openai.com/docs/concepts'
source_quality: 'mixed'
verified: false
id: '20260530000000-8570'
---

# LLM

태그: #llm_wiki #llm #ai

## 한 줄 정의

LLM은 대규모 텍스트와 코드 데이터에서 언어 패턴을 학습해 다음 토큰을 예측하고, 그 능력을 대화, 요약, 추론 보조, 코드 생성에 활용하는 모델이다.

## 내 말로 다시 설명

LLM은 지식 데이터베이스가 아니라 확률적 언어 엔진이다. 질문을 받으면 내부 파라미터, 입력 컨텍스트, 지시문을 조합해 가장 그럴듯한 출력을 만든다. 그래서 잘 쓰려면 모델에게 무엇을 해야 하는지뿐 아니라 무엇을 근거로 삼아야 하는지도 명확히 줘야 한다.

## 핵심 개념

- 토큰: 모델이 읽고 쓰는 텍스트 단위다.
- 컨텍스트: 모델이 한 번에 참고할 수 있는 입력 범위다.
- instruction: 출력 목적과 제약을 정하는 지시다.
- grounding: 답변을 외부 근거에 묶는 방식이다.
- hallucination: 근거가 부족한데도 그럴듯하게 생성하는 실패다.

## 언제 쓰는가

- 자연어 설명, 요약, 변환, 초안 작성, 코드 보조처럼 언어적 판단이 필요한 경우
- 규칙은 복잡하지만 예시와 맥락으로 의도를 전달할 수 있는 경우
- [[RAG]]나 도구 호출로 외부 지식과 행동을 결합할 때

## 언제 쓰면 안 되는가

- 엄밀한 계산, 권한 변경, 결제, 의료/법률 판단처럼 검증 없는 자동 실행이 위험한 경우
- 정답이 데이터베이스 조회로 바로 나오는 경우
- 입력 데이터의 보안 경계가 정리되지 않은 경우

## 자주 헷갈리는 점

- temperature를 낮춘다고 사실성이 보장되지는 않는다.
- 긴 프롬프트가 좋은 프롬프트는 아니다. 필요한 역할, 근거, 출력 형식, 실패 조건이 분명해야 한다.
- fine-tuning은 지식 주입보다 행동 양식과 형식 안정화에 더 적합한 경우가 많다.

## 관련 개념

- [[Prompt Engineering]]
- [[OpenAI API]]
- [[Function Calling]]
- [[RAG]]
- [[Fine-tuning]]
- [[SLLM]]

## 확인 질문

- 이 작업은 LLM이 판단해야 하는가, 아니면 검색/계산/규칙으로 해결해야 하는가?
- 답변을 검증할 근거와 실패 처리 방식이 있는가?

## 외부 참조

- https://en.wikipedia.org/wiki/Large_language_model
- https://platform.openai.com/docs/concepts
