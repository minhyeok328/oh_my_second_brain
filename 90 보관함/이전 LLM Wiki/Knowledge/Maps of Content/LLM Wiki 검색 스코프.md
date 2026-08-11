---
type: "moc"
status: "operating-guide"
created: "2026-05-30"
updated: "2026-06-23"
reviewed: "2026-06-23"
tags:
  - 'llm_wiki'
  - 'moc'
  - 'retrieval'
  - 'indexing'
  - 'governance'
source:
  - 'C:\Obsidian\KnowledgeVault\Knowledge\Assets\retrieval_scope.json'
  - 'C:\Obsidian\KnowledgeVault\Knowledge\Assets\retrieval_policy.json'
---

# LLM Wiki 검색 스코프

태그: #llm_wiki #moc #retrieval #indexing #governance

## 목적

이 문서는 현재 vault의 Markdown 노트를 검색/RAG 관점에서 어떤 인덱스에 넣을지 고정한다. 핵심 원칙은 `wiki-standardized` 노트를 기본 답변 인덱스에서 제외하고, 공식/강의 기반 지식 노트를 먼저 검색하며 프로젝트와 개인 회고는 별도 문맥으로 분리하는 것이다.

## 현재 스코프

- 전체 Markdown: 312개
- 기본 답변 인덱스: 69개
- 프로젝트 적용 컨텍스트: 4개
- 라우팅/운영 인덱스: 25개
- 필요할 때만 보는 작업 문서: 8개
- 개인 사고/회고 컨텍스트: 4개
- 기본 격리 대상: 202개
- `wiki-standardized`: 199개
- 기존 boilerplate/placeholder 매칭: 399건

## 인덱스 구분

### 기본 답변 인덱스

사용자의 질문에 직접 답할 때 먼저 검색한다.

- `primary_answer_index`: 69개
  - `wiki-expanded`
  - `source-expanded`
  - `reference`

### 프로젝트 적용 컨텍스트

프로젝트에서 실제로 어떻게 썼는지 확인할 때만 포함한다. 공식 개념 설명의 1차 근거로 쓰지 않는다.

- `applied_context_index`: 4개
  - `project-expanded`

### 라우팅 인덱스

어떤 주제 묶음으로 이동할지 정할 때 사용한다. 답변의 최종 근거는 세부 노트를 우선한다.

- `routing_index`: 25개
  - `entrypoint`
  - `map`
  - `wiki-map`
  - `operating-guide`
  - `policy`

### 온디맨드 문맥

진행 중인 질문, 프로젝트 적용 로그, RAG 평가처럼 현재 작업 문맥이 필요할 때만 포함한다.

- `on_demand_context`: 8개
  - `active`

### 개인 사고/회고 컨텍스트

개인 회고, 개발자 정체성, 개인 운영 규칙처럼 주관이 들어간 문서는 공식 지식 답변에서 제외한다.

- `personal_context`: 4개
  - `personal-context`

### 격리 대상

기본 답변 인덱스에 넣지 않는다.

- `quarantine`: 202개
  - `wiki-standardized`
  - `template`
  - `migration-report`
  - `source-outline`

## 운영 규칙

- `wiki-standardized`는 기본 답변 인덱스에 넣지 않는다.
- `wiki-standardized`만 근거로 답해야 할 때는 초안 수준임을 표시한다.
- `migration-report`와 `source-outline`은 구조 감사용으로만 사용한다.
- `template`은 답변 근거로 사용하지 않는다.
- 개념 설명 질문은 `wiki-expanded`를 우선하고, 부족할 때 `source-expanded`와 `reference`를 보조로 본다.
- 프로젝트 적용 질문은 `project-expanded`를 보조 근거로 보고, 해당 프로젝트 노트에서 링크한 Permanent Note를 다시 확인한다.
- 개인 회고나 포트폴리오 질문은 `personal-context`를 온디맨드로만 본다.

## 기계 판독 파일

- `Knowledge/Assets/retrieval_policy.json`: 상태별 인덱싱 규칙
- `Knowledge/Assets/retrieval_scope.json`: 현재 파일별 bucket, status, placeholder count, 격리 사유

## 스코프 재생성 기준

새 노트를 추가하거나 status를 바꾸면 `retrieval_scope.json`도 다시 생성한다. 재생성 뒤 아래 값이 맞는지 확인한다.

```powershell
powershell -ExecutionPolicy Bypass -File Tools/Update-RetrievalScope.ps1
```

- `counts_by_status`
- `buckets.primary_answer_index.count`
- `buckets.applied_context_index.count`
- `buckets.personal_context.count`
- `buckets.quarantine.count`
- `items[].bucket`
- `items[].reason`

## 연결

- [[LLM Wiki 검색 품질 게이트]]
- [[LLM Wiki 운영 원칙]]
- [[LLM Wiki 보강 백로그]]
- [[프로젝트 적용 로그]]
