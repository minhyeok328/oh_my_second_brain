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
- Markdown 파일: 289개
- 빈 Markdown 파일: 0개
- frontmatter 누락: 0개
- 확인된 미해결 wikilink: 0개

## 상태 분포

- `active`: 2개
- `entrypoint`: 1개
- `map`: 6개
- `migration-report`: 1개
- `operating-guide`: 1개
- `policy`: 1개
- `reference`: 21개
- `source-expanded`: 14개
- `source-outline`: 1개
- `template`: 1개
- `wiki-expanded`: 11개
- `wiki-map`: 14개
- `wiki-standardized`: 215개

## 이번 전환에서 보완한 치명점

- frontmatter와 상태값이 없어 LLM이 노트 성격을 구분하기 어렵던 문제를 해결했다.
- Permanent Note가 짧은 정의에 머물러 있던 문제를 보완해 사용 조건, 금지 조건, 혼동 지점, 확인 질문을 추가했다.
- MOC가 단순 링크 목록이던 문제를 학습 경로와 문제 해결 경로 중심으로 바꾸었다.
- Literature Note와 프로젝트 적용 로그를 연결해 강의 원천, 개념, 실제 사용 사이의 루프를 만들었다.
- 외부 공식 문서와 wiki 참조 정책을 분리해 강의 자료와 외부 지식의 충돌 가능성을 관리하게 했다.

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
- 프로젝트 적용 로그를 실제 프로젝트별로 분리한다.
- RAG 평가용 질문 세트와 검색 실패 사례를 [[질문 인박스]]에서 관리한다.

## 검증 메모

- 이 리포트는 재적용 스크립트가 파일 상태를 집계해 생성했다.
- 최종 완료 전 별도 검증 명령으로 빈 파일, frontmatter, wikilink를 다시 확인한다.
