---
type: 'project'
status: 'growing'
created: '2026-08-11'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'project_context'
  - 'project'
  - 'skn26'
  - 'frontend'
aliases:
  - 'SKN26 Final 프로젝트 - HumouR'
  - 'HumouR'
sources:
  - '[[20 소스 노트/프로젝트/HumouR README와 포트폴리오|HumouR README와 포트폴리오]]'
  - 'C:\MinHyeok\skn26_projects\Final_project\README.md'
  - 'C:\MinHyeok\skn26_projects\Final_project\docs\00-overview\project-overview.md'
  - 'C:\MinHyeok\minhyeok328.github.io\src\data\portfolio.ts'
  - 'https://minhyeok328.github.io/'
source_quality: 'mixed'
verified: true
id: '20260811000000-fb7a'
---

# SKN26 Final HumouR AI HR 채용 보조

## 프로젝트 사실

- HumouR는 회사 정보와 JD, 체크리스트, 지원서, AI 분석 리포트, 면접 질문, 문서 채팅과 외부 제한 공유를 한 흐름으로 연결한 팀 채용 보조 서비스다. AI 결과는 합격·불합격의 자동 결정이 아니라 담당자가 원문 근거와 후속 질문을 검토하기 위한 참고 정보다. (근거: [[HumouR README와 포트폴리오]], 저장소 README·overview)
- 팀 시스템은 React·TypeScript 프론트엔드, Django API, Celery, LangGraph, Pinecone과 AWS 배포로 구성된다. 포트폴리오가 적은 진행 기간 `2026.05.22 – 07.15`는 저장소 README에 없어 개인 서술로만 기록한다. (근거: 저장소 README, 포트폴리오 상세 모달)

## 팀 산출물

- 팀은 회사·JD·평가 기준·지원서 입력에서 비동기 분석, 리포트·면접 질문 검토, API Key 제한 공유와 문서 채팅까지 이어지는 제품 흐름을 구현했다. 기능과 모델 평가 수치는 팀 결과이며 개인의 단독 성과로 귀속하지 않는다. (근거: 저장소 README `서비스 흐름`, `구현 기능`, `평가 결과`)
- README 역할표는 AI 모델링, 데이터 수집·검색, 백엔드·배포와 프론트엔드 역할을 여러 팀원에게 나눈다. API Key 관리·제한 모드·공유 리포트 UI도 다른 프론트엔드 팀원의 주요 기여로 명시된다. (근거: 저장소 README `팀 구성과 기여`)

## 직접 기여

- README 역할표와 개인 포트폴리오는 서민혁에게 프론트 구조, 인증·CSRF·응답 계약, 요청 수명주기, QA·보안 안정화와 문서화를 귀속한다. 저장소에는 Axios 공통 요청, 도메인 client, Zod schema, adapter와 TanStack Query 흐름이 확인된다. 코드 존재는 구현의 보강 근거이며 개인 작성자를 독립적으로 증명하지 않는다. (근거: [[HumouR README와 포트폴리오]], `frontend/src/api/`)
- 포트폴리오는 일반 로그인과 외부 API Key 제한 흐름의 공통 인증·세션·Query 캐시 경계를 직접 기여로 적는다. 저장소는 인증 방식을 구분하고 불투명 세션 식별자로 query key를 나누며 API Key 제거·세션 전환을 테스트한다. 제한 공유 UI 전체의 소유권은 주장하지 않는다. (근거: 포트폴리오, `useAuthSession.ts`, `queryOptions.ts`와 tests)
- 포트폴리오는 요청 취소, 오래된 응답 차단, 인증 만료, 오류 정규화와 캐시 정리를 직접 다뤘다고 기록한다. 저장소의 요청 controller, request id, 전역 만료 handler와 테스트가 이 동작의 존재를 보강한다. (근거: `httpClient.ts`, `queryClient.ts`, `useAuthExpiryHandler.ts`, `useSharedReportSession.ts`와 tests)
- 포트폴리오는 JD·지원서·분석 리포트·면접 질문·외부 공유·문서 채팅의 화면과 API 흐름 통합, 프론트엔드 테스트·QA·인터페이스 문서 체계 구축과 확장을 기여로 적는다. 저장소의 pages, domain clients, Vitest·Playwright와 검증 스크립트·인터페이스 문서가 해당 산출물의 존재를 보강한다. (근거: 포트폴리오, 저장소 README `검증 방법`, `주요 산출물`)

## 의사결정과 근거

- 실제 서버 응답을 화면 전에 검증하기 위해 Axios·CSRF → 도메인 client → Zod → adapter → TanStack Query로 경계를 나눴다는 판단은 포트폴리오에 개인 결정으로 기록되어 있다. 저장소 구조가 이 계층을 확인시켜 주며 [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]]와 연결된다.
- 계정 세션과 API Key 제한 세션이 같은 캐시를 섞어 쓰지 않도록 인증 방식과 불투명 세션 식별자를 query key에 포함했다. 이는 서버 권한 검사를 대신하지 않는 프론트 상태 경계다. (근거: 포트폴리오, `queryOptions.ts`, `useAuthSession.ts`)
- 요청 취소와 request id를 함께 사용하고, 인증 만료 시 진행 중 요청·캐시·인증 상태를 정리한 뒤 로그인으로 복구했다. 이 경험은 [[인증 만료는 오류가 아니라 사용자 흐름의 일부다]], [[오래된 비동기 응답은 최신 상태를 덮지 못하게 해야 한다]], [[프론트엔드 상태는 권한 경계와 함께 정리해야 한다]]로 분리했다.

## 실패·디버깅

- 포트폴리오는 늦은 응답이 최신 상태를 덮는 경우와 인증 만료 뒤 보호 데이터가 화면·캐시에 남는 위험을 문제 상황으로 기록한다. 저장소 테스트는 늦은 account 응답, query 취소·캐시 제거와 공유 조회 request id 경계를 검증한다. 개별 운영 장애의 발생 횟수나 사용자 피해는 근거가 없어 적지 않는다.
- 저장소가 밝힌 남은 범위에는 외부 AI·검색 서비스 의존, 임시 비밀번호 복구, 상대적으로 약한 백엔드 테스트와 배포 gate가 있다. 프론트엔드 안정화가 전체 시스템의 보안 인증이나 운영 SLA를 뜻하지 않는다.

## 회고

> 개인 회고: 4차 프로젝트에서 화면과 서버 통신의 오류 상태까지 다룬 뒤, HumouR에서는 인증·권한·비동기 상태·오류·테스트를 실제 서비스 흐름의 일부로 함께 검토하게 되었다. 보기 좋은 화면을 넘어 안전하고 예측 가능한 상태를 만들고 검증하는 프론트엔드 개발자로 성장하고 싶다는 방향을 기록했다. (근거: 포트폴리오 HumouR 회고, 2026-08-11 확인)

## 연결

- 근거: [[HumouR README와 포트폴리오]]
- 개념: [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]], [[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]], [[CSRF 방어는 브라우저 세션 요청의 출처를 검증한다]]
- 파생 지식: [[인증 만료는 오류가 아니라 사용자 흐름의 일부다]], [[오래된 비동기 응답은 최신 상태를 덮지 못하게 해야 한다]], [[프론트엔드 상태는 권한 경계와 함께 정리해야 한다]]
- 경험 기록: [[프로젝트 의사결정 로그]], [[프로젝트 실패와 디버깅 로그]], [[프로젝트 경험 지도#Final HumouR]]
- 이전 경험: [[SKN26 4차 LG Home AI 가전 상담]]

## 확인한 근거

- `C:\MinHyeok\skn26_projects\Final_project\README.md`와 `docs\00-overview\project-overview.md` — 서비스 범위, 팀 역할, 기술 구조, 검증과 한계 (2026-08-11 확인)
- `C:\MinHyeok\minhyeok328.github.io\src\data\portfolio.ts`와 `https://minhyeok328.github.io/` — HumouR 상세 모달의 개인 역할·판단·회고 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\`와 `frontend\src\hooks\`의 관련 코드·테스트 — 응답 계약, 인증·세션·캐시 경계, 요청 취소와 만료 복구 구현 (2026-08-11 확인)
