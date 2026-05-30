---
type: "moc"
status: "operating-guide"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'moc'
  - 'governance'
---

# LLM Wiki 운영 원칙

태그: #moc #llm_wiki #governance

## 목적

이 vault는 강의 자료를 그대로 쌓는 저장소가 아니라, LLM이 검색하고 사람이 복습할 수 있는 설명형 wiki로 운영한다.

## 원칙

- 한 노트는 하나의 개념이나 판단 기준을 설명한다.
- 모든 Permanent Note는 정의, 사용 조건, 금지 조건, 혼동 지점, 확인 질문을 가진다.
- MOC는 단순 목록이 아니라 학습 경로와 문제 해결 경로를 제공한다.
- 외부 문서는 공식 문서와 위키를 보조 근거로 쓰고, 강의 원천과 충돌하면 출처를 분리해서 남긴다.
- 프로젝트에서 사용한 지식은 [[프로젝트 적용 로그]]에 기록해 죽은 지식이 되지 않게 한다.
- 검색/RAG에는 [[LLM Wiki 검색 품질 게이트]]와 [[LLM Wiki 검색 스코프]]를 적용해 `wiki-standardized` 노트가 보강된 노트를 밀어내지 않게 한다.

## 보강 우선순위

- 검색 품질을 좌우하는 [[RAG]], [[Embedding]], [[Vector Store]], [[Retriever]]
- 실제 앱 구현에 자주 쓰는 [[Django QuerySet]], [[React API Fetch]], [[Docker Compose]]
- 혼동 비용이 큰 lifecycle, migration, state, transaction 관련 노트

## 품질 게이트

- `project-expanded`와 `wiki-expanded`를 기본 근거로 삼는다.
- `wiki-standardized`는 fallback 후보로만 쓰고, 답변 근거로 쓸 때는 초안 수준임을 표시한다.
- placeholder 문구가 남은 노트는 보강 전까지 검색 우선순위를 낮춘다.
- 기본 답변 인덱스의 실제 파일 목록은 `Knowledge/Assets/retrieval_scope.json`에서 관리한다.
- 다음 승격 후보는 [[LLM Wiki 보강 백로그]]에서 관리한다.
