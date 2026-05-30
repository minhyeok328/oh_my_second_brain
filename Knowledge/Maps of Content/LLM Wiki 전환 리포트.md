---
type: "moc"
status: "migration-report"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'migration'
  - 'moc'
---

# LLM Wiki 전환 리포트

태그: #llm_wiki #moc #migration

## 요약

- 기준일: 2026-05-30
- Markdown 파일: 311개
- 빈 Markdown 파일: 0개
- frontmatter 누락: 0개
- 확인된 미해결 wikilink: 0개

## 상태 분포

- `active`: 11개
- `entrypoint`: 1개
- `map`: 6개
- `migration-report`: 1개
- `operating-guide`: 3개
- `policy`: 1개
- `project-expanded`: 4개
- `reference`: 21개
- `source-expanded`: 14개
- `source-outline`: 1개
- `template`: 1개
- `wiki-expanded`: 34개
- `wiki-map`: 14개
- `wiki-standardized`: 199개

## 이번 전환에서 보완한 치명점

- frontmatter와 상태값이 없어 LLM이 노트 성격을 구분하기 어렵던 문제를 해결했다.
- Permanent Note가 짧은 정의에 머물러 있던 문제를 보완해 사용 조건, 금지 조건, 혼동 지점, 확인 질문을 추가했다.
- MOC가 단순 링크 목록이던 문제를 학습 경로와 문제 해결 경로 중심으로 바꾸었다.
- Literature Note와 프로젝트 적용 로그를 연결해 강의 원천, 개념, 실제 사용 사이의 루프를 만들었다.
- 외부 공식 문서와 wiki 참조 정책을 분리해 강의 자료와 외부 지식의 충돌 가능성을 관리하게 했다.
- SKN26 1~4차 프로젝트별 상세 노트를 추가해 프로젝트 근거가 있는 지식과 일반 개념 노트를 분리했다.
- [[LLM Wiki 검색 품질 게이트]], [[LLM Wiki 검색 스코프]], [[LLM Wiki 보강 백로그]]를 추가해 덜 익은 노트가 검색 결과를 오염시키지 않도록 운영 기준을 만들었다.
- 1차 차량 TCO 프로젝트에 직접 연결된 [[Streamlit Session State]], [[MySQL Connector Python]], [[SQL SELECT와 WHERE]], [[Requests]]를 `wiki-expanded`로 승격했다.
- 2차 카드 이탈 예측 프로젝트의 모델 평가 축인 [[분류 평가 지표]], [[Train Test Split]], [[Feature Engineering]]을 `wiki-expanded`로 승격했다.
- second brain 용도로 프로젝트 경험을 관리하기 위해 [[프로젝트 경험 MOC]], [[프로젝트 의사결정 로그]], [[프로젝트 실패와 디버깅 로그]]를 추가했다.
- 프로젝트 개인 회고 입력을 준비하기 위해 [[프로젝트 회고 질문 세트]]를 추가했다.

## 우선 확장한 허브 노트

- [[RAG]]
- [[LLM]]
- [[LangGraph]]
- [[Pandas DataFrame]]
- [[Django ORM Model]]
- [[useEffect]]
- [[Django QuerySet]]
- [[Embedding]]
- [[Vector Store]]
- [[React API Fetch]]
- [[Docker Compose]]

## 남은 보강 후보

- 각 강의 실습 코드에서 대표 예제를 Permanent Note의 예제 섹션으로 더 직접 연결한다.
- `wiki-standardized` 199개 중 프로젝트 연결도가 높은 노트부터 [[LLM Wiki 보강 백로그]] 순서로 승격한다.
- placeholder성 문구 399건은 검색/RAG 기본 대상에서 낮추고, 승격 시 제거한다.
- 새 후보 노트는 실제 프로젝트 근거가 있는지 확인한 뒤 생성한다.

## 검증 메모

- 이 리포트의 숫자는 2026-05-30 프로젝트 상세 보강 및 검색 품질 게이트 추가 이후 다시 집계했다.
- 검색/RAG 스코프는 `Tools/Update-RetrievalScope.ps1`로 `Knowledge/Assets/retrieval_scope.json`을 재생성해 관리한다.
- 최종 완료 전 별도 검증 명령으로 빈 파일, frontmatter, wikilink, placeholder 문구를 다시 확인한다.
