---
type: "moc"
status: "operating-guide"
created: "2026-05-30"
updated: "2026-06-23"
reviewed: "2026-06-23"
tags:
  - 'llm_wiki'
  - 'moc'
  - 'governance'
---

# LLM Wiki 운영 원칙

태그: #moc #llm_wiki #governance

## 목적

이 vault는 개인 생각을 기본 근거로 삼는 second brain이 아니라, LLM이 검색하고 사람이 복습할 수 있는 공식 지식 중심 wiki로 운영한다. 프로젝트 경험과 개인 회고는 지식을 이해하는 보조 레이어이며, 개념 설명의 1차 근거가 아니다.

## 레이어 구분

- 공식 지식 레이어: `wiki-expanded`, `source-expanded`, `reference` 노트. 정의, 공식/강의 근거, 사용 조건, 금지 조건을 담는다.
- 프로젝트 적용 레이어: `project-expanded` 노트. 실제 프로젝트에서 개념이 어떻게 쓰였는지 보여주는 사례다.
- 작업 문맥 레이어: `active` 노트. 질문, 평가, 디버깅, 다음 작업처럼 현재 관리 중인 문맥이다.
- 개인 사고 레이어: `personal-context` 노트. 회고, 정체성, 개인 규칙처럼 주관이 들어간 내용이다.

## 원칙

- 한 노트는 하나의 개념이나 공식 판단 기준을 설명한다.
- 모든 Permanent Note는 정의, 공식/강의 근거, 사용 조건, 금지 조건, 혼동 지점, 확인 질문을 가진다.
- MOC는 단순 목록이 아니라 학습 경로와 문제 해결 경로를 제공한다.
- 외부 공식 문서는 API, 표준 동작, 권장 패턴의 1차 확인 근거로 쓰고, 강의 원천과 충돌하면 출처를 분리해서 남긴다.
- 프로젝트에서 사용한 지식은 [[프로젝트 적용 로그]]에 기록하되, 공식 지식의 정의를 대체하지 않는다.
- 개인 판단, 회고, 포트폴리오 서사는 [[생각과 회고 MOC]]로 분리한다.
- 검색/RAG에는 [[LLM Wiki 검색 품질 게이트]]와 [[LLM Wiki 검색 스코프]]를 적용해 `wiki-standardized` 노트가 보강된 노트를 밀어내지 않게 한다.

## 보강 우선순위

- 공식 문서 확인 비용이 큰 [[RAG]], [[Embedding]], [[Vector Store]], [[Retriever]]
- API와 버전 차이가 중요한 [[Django QuerySet]], [[React API Fetch]], [[Docker Compose]]
- 혼동 비용이 큰 lifecycle, migration, state, transaction 관련 노트

## 품질 게이트

- `wiki-expanded`, `source-expanded`, `reference`를 기본 근거로 삼는다.
- `project-expanded`는 프로젝트 적용 사례가 필요할 때 보조 근거로만 쓴다.
- `wiki-standardized`는 fallback 후보로만 쓰고, 답변 근거로 쓸 때는 초안 수준임을 표시한다.
- placeholder 문구가 남은 노트는 보강 전까지 검색 우선순위를 낮춘다.
- 기본 답변 인덱스의 실제 파일 목록은 `Knowledge/Assets/retrieval_scope.json`에서 관리한다.
- 다음 승격 후보는 [[LLM Wiki 보강 백로그]]에서 관리한다.
