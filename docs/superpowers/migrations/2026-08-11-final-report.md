# Second Brain 마이그레이션 최종 검증 보고서

- 검증일: 2026-08-12
- 검증 기준 커밋: `ed4a67d`
- 검증 범위: 활성 Second Brain, 보관함, 템플릿, 보호된 Obsidian 설정, 외부 강의·프로젝트 소스 스냅샷
- strict verifier 결과: 오류 0건 (`2026-08-11-final-report.json`의 정확한 바이트는 `5B 5D 0A`, 즉 `[]\n`)

## 자동 검증

| 검증 | 명령 | 종료 코드 | 결과 |
|---|---|---:|---|
| 전체 테스트 | `python -m unittest discover -s Tools/second_brain/tests -v` | 0 | 총 151개 중 143개 통과, Windows 심볼릭 링크 권한 관련 예상 스킵 8개 |
| strict 최종 검증 | `python -m Tools.second_brain.verify --vault . --final --obsidian-snapshot docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json --source-snapshot docs/superpowers/migrations/2026-08-11-source-snapshot.json --json docs/superpowers/migrations/2026-08-11-final-report.json` | 0 | JSON `[]\n` |
| 레거시 표식 검색 | `rg -n 'llm_wiki|wiki-standardized|wiki-expanded|source-expanded|project-expanded|LLM Wiki 검색'`을 홈과 활성 루트에 실행 | 1 | 무매치(예상 결과) |
| 이전 절대 경로 검색 | `rg -n 'C:\\lecture|C:\\MinHyeok\\skn26_(1st|2nd|3rd|4th)'`를 홈과 활성 루트에 실행 | 1 | 무매치(예상 결과) |
| Obsidian 보호 스냅샷 | `python -m Tools.second_brain.snapshot --verify-hashes docs/superpowers/migrations/2026-08-11-obsidian-snapshot.json` | 0 | 승인된 작업 복사본과 일치 |
| 외부 소스 스냅샷 | `python -m Tools.second_brain.snapshot --verify-tree docs/superpowers/migrations/2026-08-11-source-snapshot.json` | 0 | 강의·프로젝트 원본 트리와 일치 |
| diff 형식 | `git diff --check 3345148..HEAD` | 0 | 전체 마이그레이션 범위 오류 없음 |

회귀 검색 범위는 `Second Brain 홈.md`, `00 인박스`, `10 데일리`, `20 소스 노트`, `30 영구 노트`, `40 프로젝트`, `50 영역`, `60 구조 노트`, `99 템플릿`으로 제한했다. 저장소 문서와 테스트 fixture는 검색 대상에서 제외했다.

## 산출물과 정확한 개수

- `SKN26`로 시작하는 루트 프로젝트 허브: 5개
- 승인 계약의 학습 지도: 12개
- 템플릿: 5개
- 강의 소스 노트: 14개
- 영구 노트: 37개(승격된 34개 + HumouR 파생 3개)
- `90 보관함/이전 LLM Wiki`의 레거시 Markdown: 228개
- `00 인박스/승격 대기/영구 노트` 아래 파일: 0개
- 활성 노트의 중복 ID: 0개

### 프로젝트 허브 5개

1. `SKN26 1차 차량 운영비 프로젝트.md`
2. `SKN26 2차 신용카드 고객 이탈 분석.md`
3. `SKN26 3차 PICKLE 맛집 추천 챗봇.md`
4. `SKN26 4차 LG Home AI 가전 상담.md`
5. `SKN26 Final HumouR AI HR 채용 보조.md`

### 학습 지도 12개

1. `Python 학습 지도.md`
2. `MySQL 학습 지도.md`
3. `데이터 수집 학습 지도.md`
4. `데이터 분석 학습 지도.md`
5. `머신러닝 학습 지도.md`
6. `딥러닝 기초 학습 지도.md`
7. `NLP 딥러닝 학습 지도.md`
8. `LLM과 RAG 학습 지도.md`
9. `멀티모달 딥러닝 학습 지도.md`
10. `웹 클라이언트 학습 지도.md`
11. `웹 서버 학습 지도.md`
12. `DevOps 학습 지도.md`

### 템플릿 5개

- `데일리 노트 템플릿.md`
- `소스 노트 템플릿.md`
- `영구 노트 템플릿.md`
- `프로젝트 노트 템플릿.md`
- `회고 노트 템플릿.md`

## 활성 노트 인벤토리

`Tools.second_brain.note_io.parse_markdown`와 검증기의 archive/template/repository-root 제외 함수를 사용해 계산했다. 파일명으로 유형을 추정하지 않았다.

- 활성 노트 합계: 107개
- type별: `area` 6, `inbox` 4, `permanent` 37, `project` 8, `reflection` 1, `source` 36, `structure` 15
- status별: `growing` 103, `seed` 4
- 중복 ID: 0개

`seed` 4개 중 세 개는 아래 미답변 질문 노트이고, 하나는 관리용 `가져오기 검토 목록.md`다.

## 수동 콘텐츠·내비게이션 검토

- 프로젝트 허브 5개를 모두 읽었다. 팀 산출물, 직접 기여, 의사결정, 실패·디버깅, 개인 회고와 근거가 구분되어 있으며 README·코드·개인 포트폴리오의 증거 수준을 섞지 않았다.
- 강의 소스 노트 14개를 모두 읽었다. 각 노트는 로컬 원본 경로의 관찰, 개인 해석·의문, 분리한 영구 노트를 구분한다. `Git 기초 강의.md`와 `React와 CI CD 강의.md`는 승인 경로의 근거 공백을 명시한다.
- 학습 지도 12개와 영역 노트 `기술 학습.md`, `커리어.md`, `개인 목표.md`, `개발 원칙.md`를 모두 읽었다. 지도는 가나다순 링크 덤프가 아니라 출발점, 개념 순서, 프로젝트 적용, 다음 질문의 의미 있는 경로를 제공한다.
- `Second Brain 홈.md`를 읽었다. 빠른 기록, 영역, 프로젝트 경험, 학습, 회고로 이동하는 간결한 진입점이며 보관함은 복구 경로로만 연결한다.
- 표본 영구 노트 `RAG의 성능은 검색 단계의 품질에서 시작된다.md`, `React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다.md`, `학습 데이터와 평가 데이터는 모델 선택 전에 분리해야 한다.md`를 읽었다. 각각 한 핵심 주장, 연결, 한계·반례와 확인 근거를 갖는다.
- 실용 참조 `Git 명령어 모음.md`와 개인 회고 `프로젝트 기반 개발자 정체성.md`를 읽었다. 명령 참조의 검증 한계와 개인 서사의 성격이 명시되어 있다.
- 질문 노트 `RAG 검색 실패 사례.md`, `RAG 평가 질문 세트.md`, `질문 인박스.md`를 모두 읽었다. 관찰·가설·확인 질문과 미답변 상태를 구분해 검증 전 내용을 사실로 승격하지 않는다.
- `HumouR README와 포트폴리오.md`와 파생 영구 노트 `인증 만료는 오류가 아니라 사용자 흐름의 일부다.md`, `오래된 비동기 응답은 최신 상태를 덮지 못하게 해야 한다.md`, `프론트엔드 상태는 권한 경계와 함께 정리해야 한다.md`를 읽었다. 팀 사실, 개인 기여 서술, 코드로 확인된 동작과 해석의 경계가 유지된다.
- 검토 표본에서 부자연스러운 한국어, 반복되는 LLM Wiki 템플릿, 발명된 프로젝트 기여·개인 목표, 근거 없는 확정 표현 또는 평면적인 가나다순 지도 덤프를 발견하지 않았다.

## 보호 설정과 외부 원본 기준선

`.obsidian/core-plugins.json`, `.obsidian/graph.json`, `.obsidian/workspace.json`은 마이그레이션 전에 존재하던 승인된 작업 복사본 상태이며, 이 세 파일은 스테이징하거나 복원하지 않았다. 현재 바이트는 작업 복사본 스냅샷과 일치한다. Git blob 기준 `core-plugins.json`은 HEAD와 동일하고 `graph.json`, `workspace.json`만 HEAD와 다르다. Git status가 세 파일을 모두 표시하는 것은 `core-plugins.json`의 작업 트리 줄바꿈 상태까지 포함한 결과다.

- `.obsidian/core-plugins.json`: `763cf20a921fd9955735b278006820b90b207b2fc04d9e79ca648279c7c14276`
- `.obsidian/graph.json`: `d26e4e9b656d9161d71127a4a66afe7bc4bf19c69fe378c307d91eb9e819ec41`
- `.obsidian/workspace.json`: `aa372cd537776c13cccf17a166fc5ba3b23e1253cf9cfef3c0808243fd742f4e`

외부 `C:\MinHyeok\lecture`와 `C:\MinHyeok\skn26_projects` 트리는 승인된 source snapshot과 일치한다. 외부 원본을 수정하거나 스냅샷 차이를 복원하지 않았다. 프로젝트 트리는 계획 초안의 예상 996개가 아니라 최초 실제 스냅샷 생성 시 확인된 1005개이며, 문서화된 제외 규칙을 임의로 늘리지 않고 그 실제 기준선을 보존했다.

## 의도적으로 남긴 검토 부채

다음 항목은 strict verifier 오류가 아니며 검증된 최신 사실로 간주하지 않는다.

- `50 영역/개발 레퍼런스`의 실용 참조 21개는 모두 `verified: false`다. 명령·API·도구 버전에 민감하므로 실제 사용 시 해당 공식 문서와 현재 버전을 다시 확인해야 한다.
- `RAG 검색 실패 사례.md`, `RAG 평가 질문 세트.md`, `질문 인박스.md`의 질문은 미답변이다. 재현 결과와 근거가 생기기 전에는 영구 사실로 승격하지 않는다.
- `가져오기 검토 목록.md`는 미처리 항목을 위한 관리용 seed다.
- `Git 기초 강의.md`와 `React와 CI CD 강의.md`는 승인된 강의 경로에서 직접 근거를 찾지 못한 범위를 명시한다. 별도 공식 자료나 실제 프로젝트 설정을 확보하기 전에는 그 공백을 채운 것으로 보지 않는다.
- 마이그레이션 적용의 파일 변경 경로는 Windows handle 기반으로 안전성을 확보했으며 다른 운영체제에서는 변경 전에 `ENOTSUP`으로 중단한다. 롤백 저널은 메모리 기반이므로 프로세스 강제 종료나 전원 손실 뒤에는 승인 plan과 파일시스템을 수동 대조해야 한다.
