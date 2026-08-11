---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'openai'
  - 'llm'
  - 'api'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://developers.openai.com/api/docs/quickstart'
  - 'https://developers.openai.com/api/docs/guides/text'
source_quality: 'mixed'
verified: false
id: '20260530000000-a397'
---

# OpenAI API 기본 호출

## 용도

OpenAI API로 텍스트 응답을 요청할 때 필요한 최소 입력과 실패 경계를 확인한다.

## 빠른 참조

```python
from openai import OpenAI

client = OpenAI()
response = client.responses.create(
    model="<사용 가능한 모델>",
    input="요청 내용",
)
print(response.output_text)
```

- API 키는 코드에 넣지 않고 SDK가 읽을 수 있는 `OPENAI_API_KEY` 환경 변수 등 안전한 비밀 관리 수단을 사용한다.
- 모델 이름은 계정과 프로젝트에서 실제로 사용할 수 있는 값을 선택한다.
- 호출 코드는 타임아웃, 재시도 가능 오류, 사용량과 응답 식별자를 함께 기록한다.

## 검증 범위

- 2026-08-11: OpenAI 공식 Quickstart와 Text generation 문서에서 Python SDK의 Responses API 기본 형태를 확인했다.
- 실제 API 호출, 계정별 모델 가용성, 비용, rate limit, 스트리밍과 도구 호출은 검증하지 않았다. 배포 전 현재 공식 문서와 프로젝트 설정을 확인한다.

## 관련 노트

- [[OpenAI API 호출은 입력 출력 오류 경계를 함께 설계해야 한다]]
- [[프롬프트는 모델에 전달하는 작업 계약이다]]
- [[20 소스 노트/강의/LLM과 RAG 강의|LLM과 RAG 강의]]
