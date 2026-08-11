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
  - 'rag'
  - 'retrieval'
source:
  - 'C:\Obsidian\KnowledgeVault\Knowledge'
---

# LLM Wiki 검색 품질 게이트

태그: #llm_wiki #moc #governance #rag #retrieval

## 목적

LLM 검색이나 RAG에서 공식 지식, 프로젝트 적용 사례, 개인 회고가 섞이지 않게 한다. 이 문서는 공부용 개념 답변에는 공식/강의 기반 노트를 먼저 쓰고, 프로젝트와 개인 문맥은 필요할 때만 붙이는 기준을 정한다.

현재 파일별 스코프는 [[LLM Wiki 검색 스코프]]와 `Knowledge/Assets/retrieval_scope.json`에서 관리한다.

## 기본 답변 인덱스

- `wiki-expanded`: 정의, 공식/강의 근거, 사용 조건, 금지 조건이 보강된 Permanent Note다.
- `source-expanded`: 강의 흐름과 실습 맥락을 확인할 때 사용한다.
- `reference`: 명령어, 치트시트, 빠른 실행 절차를 확인할 때 사용한다.

## 적용 사례 인덱스

- `project-expanded`: 프로젝트에서 실제로 사용한 지식이다. 공식 개념 설명의 1차 근거가 아니라, "프로젝트에서 어떻게 적용했는가"를 설명할 때 사용한다.

## 라우팅 인덱스

- `operating-guide`, `policy`: vault 운영 방식과 출처 기준을 확인할 때 사용한다.
- `wiki-map`: 탐색 경로를 잡을 때 사용하되, 최종 답변 근거로는 세부 노트를 우선한다.
- `entrypoint`, `map`: 전체 탐색 출발점으로만 사용한다.

## 조건부 포함

- `active`: 질문 인박스, 프로젝트 적용 로그, RAG 평가 자료처럼 현재 관리 중인 문서다. 사용자의 질문이 프로젝트 회고, 평가, 다음 작업, 디버깅에 관한 경우 포함한다.
- `personal-context`: 개인 회고, 개발자 정체성, 개인 규칙처럼 주관이 들어간 문서다. 공식 지식 답변에는 포함하지 않는다.
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

1. 개념 설명 질문이면 같은 이름의 `wiki-expanded` Permanent Note를 먼저 본다.
2. 강의 흐름이나 실습 맥락이 필요하면 `source-expanded` Literature Note를 붙인다.
3. 구현 절차 질문이면 `reference` 노트를 같이 본다.
4. 프로젝트 적용 질문이면 [[프로젝트 적용 로그]]와 `project-expanded` 노트를 보조 근거로 본다.
5. 개인 회고나 포트폴리오 서사 질문이면 `personal-context` 노트를 온디맨드로 본다.
6. 위 근거가 부족하고 사용자가 초안 수준 답변을 허용할 때만 `wiki-standardized` 노트를 fallback으로 본다.

## 재순위화 기준

- 공식 문서, 강의 원천, 검증된 레퍼런스가 분리되어 있는 노트는 우선순위를 올린다.
- 정의, 사용 조건, 금지 조건, 혼동 지점이 모두 있는 노트는 우선순위를 올린다.
- 프로젝트 노트에서 직접 링크한 Permanent Note는 프로젝트 적용 질문에서만 우선순위를 올린다.
- `실패 조건`, `먼저 확인할 질문`, `프로젝트 예시`가 모두 있는 노트는 우선순위를 올린다.
- placeholder 문구가 남은 노트는 우선순위를 크게 낮춘다.
- MOC는 답변 본문 근거보다 탐색용 routing 근거로 사용한다.
- `retrieval_scope.json`에서 `quarantine` bucket인 문서는 기본 답변 인덱스에 넣지 않는다.

## 답변 안전 규칙

- 근거가 `wiki-standardized`뿐이면 단정하지 않는다.
- 프로젝트 코드에서 확인한 내용과 일반 개념 설명을 분리한다.
- 개인 회고와 개발자 정체성 문장은 공식 지식 근거로 쓰지 않는다.
- 외부 문서 확인 없이 최신 API 세부값을 단정하지 않는다.
- 프로젝트 노트와 Permanent Note가 충돌하면 공식 문서/강의 원천을 다시 확인하고, 프로젝트 노트는 특정 환경의 사례로 표시한다.

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
