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
  - 'rag'
  - 'retrieval'
source:
  - 'C:\Obsidian\KnowledgeVault\Knowledge'
---

# LLM Wiki 검색 품질 게이트

태그: #llm_wiki #moc #governance #rag #retrieval

## 목적

LLM 검색이나 RAG에서 아직 덜 익은 `wiki-standardized` 노트가 보강된 프로젝트 노트보다 먼저 잡히지 않게 한다. 이 문서는 답변 품질을 위해 어떤 노트를 기본 검색 대상에 넣고, 어떤 노트를 기본 인덱스에서 격리할지 정한다.

현재 파일별 스코프는 [[LLM Wiki 검색 스코프]]와 `Knowledge/Assets/retrieval_scope.json`에서 관리한다.

## 기본 답변 인덱스

- `project-expanded`: 프로젝트에서 실제로 사용한 지식이다. 가장 먼저 검색한다.
- `wiki-expanded`: 정의, 사용 조건, 실패 조건, 프로젝트 예시가 보강된 Permanent Note다.
- `source-expanded`: 강의 흐름을 확인해야 할 때 보조 근거로 사용한다.
- `reference`: 명령어, 치트시트, 빠른 실행 절차를 확인할 때 사용한다.

## 라우팅 인덱스

- `operating-guide`, `policy`: vault 운영 방식과 출처 기준을 확인할 때 사용한다.
- `wiki-map`: 탐색 경로를 잡을 때 사용하되, 최종 답변 근거로는 세부 노트를 우선한다.
- `entrypoint`, `map`: 전체 탐색 출발점으로만 사용한다.

## 조건부 포함

- `active`: 질문 인박스, 프로젝트 적용 로그, RAG 평가 자료처럼 현재 관리 중인 문서다. 사용자의 질문이 프로젝트 회고, 평가, 다음 작업, 디버깅에 관한 경우 포함한다.
- `wiki-standardized`: 기본 답변 인덱스에는 넣지 않는다. 정확한 제목 매칭이 있고, 같은 주제의 `wiki-expanded` 노트가 없을 때만 초안 근거로 사용한다. 이 상태의 노트만 근거로 답할 때는 "초안 수준"임을 표시한다.
- `migration-report`, `source-outline`: 구조 점검에는 사용하지만 개념 설명 근거로 쓰지 않는다.

## 기본 제외

- `template`: 답변 근거로 사용하지 않는다.
- `wiki-standardized`는 기본 답변 인덱스에서 제외한다.
- 자동생성 템플릿 문구가 남아 있는 노트는 격리 사유를 `retrieval_scope.json`에 남긴다.
  - 강의 개념을 일반적으로 설명한다는 boilerplate
  - 단일 예제를 모든 상황에 일반화하지 말라는 boilerplate
  - 한 문장 요약을 채우라는 placeholder
- `Assets` 하위의 자동 생성 JSON/분석 파일은 사람이 직접 검토하는 색인으로만 사용한다.

## 검색 순서

1. 프로젝트 관련 질문이면 [[프로젝트 적용 로그]]와 `project-expanded` 노트를 먼저 본다.
2. 개념 설명 질문이면 같은 이름의 `wiki-expanded` Permanent Note를 먼저 본다.
3. 구현 절차 질문이면 `reference` 노트를 같이 본다.
4. 강의 맥락이 필요할 때만 `source-expanded` Literature Note를 붙인다.
5. 위 근거가 부족하고 사용자가 초안 수준 답변을 허용할 때만 `wiki-standardized` 노트를 fallback으로 본다.

## 재순위화 기준

- 프로젝트 노트에서 직접 링크한 Permanent Note는 우선순위를 올린다.
- `source`에 실제 로컬 프로젝트 경로가 있는 노트는 우선순위를 올린다.
- `실패 조건`, `먼저 확인할 질문`, `프로젝트 예시`가 모두 있는 노트는 우선순위를 올린다.
- placeholder 문구가 남은 노트는 우선순위를 크게 낮춘다.
- MOC는 답변 본문 근거보다 탐색용 routing 근거로 사용한다.
- `retrieval_scope.json`에서 `quarantine` bucket인 문서는 기본 답변 인덱스에 넣지 않는다.

## 답변 안전 규칙

- 근거가 `wiki-standardized`뿐이면 단정하지 않는다.
- 프로젝트 코드에서 확인한 내용과 일반 개념 설명을 분리한다.
- 외부 문서 확인 없이 최신 API 세부값을 단정하지 않는다.
- 프로젝트 노트와 Permanent Note가 충돌하면 프로젝트 노트를 현재 vault의 1차 근거로 삼고, Permanent Note를 보강 대상으로 표시한다.

## 점검 명령

```powershell
powershell -ExecutionPolicy Bypass -File Tools/Update-RetrievalScope.ps1
```

```powershell
rg -n "강의에서 나온.*개념|예제 하나.*보고|이 개념.*한 문장" Knowledge
```

```powershell
Get-ChildItem -Recurse -File -Filter *.md Knowledge | ForEach-Object {
  $text = Get-Content -LiteralPath $_.FullName -Raw -Encoding UTF8
  if ($text -match '(?m)^status:\s*"?([^"\r\n]+)"?') { $Matches[1].Trim() }
} | Group-Object | Sort-Object Name
```

## 연결

- [[LLM Wiki 검색 스코프]]
- [[LLM Wiki 운영 원칙]]
- [[LLM Wiki 보강 백로그]]
- [[프로젝트 적용 로그]]
- [[RAG 평가 질문 세트]]
- [[RAG 검색 실패 사례]]
