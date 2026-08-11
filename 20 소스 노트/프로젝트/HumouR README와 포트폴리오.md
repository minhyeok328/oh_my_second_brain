---
type: 'source'
status: 'growing'
created: '2026-08-11'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'project_source'
  - 'humour'
  - 'frontend'
  - 'evidence'
aliases:
  - 'HumouR 근거 노트'
sources:
  - 'C:\MinHyeok\skn26_projects\Final_project\README.md'
  - 'C:\MinHyeok\skn26_projects\Final_project\docs\00-overview\project-overview.md'
  - 'C:\MinHyeok\minhyeok328.github.io\src\data\portfolio.ts'
  - 'https://minhyeok328.github.io/'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\httpClient.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\backendSchemas.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\appDataService.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\queryOptions.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\queryClient.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\hooks\useAuthSession.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\hooks\useAuthExpiryHandler.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\hooks\useSharedReportSession.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\hooks\useAuthSession.test.tsx'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\hooks\useAuthExpiryHandler.test.tsx'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\queryOptions.test.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\api\httpClient.test.ts'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\components\jd\JdChatDrawer.test.tsx'
  - 'C:\MinHyeok\skn26_projects\Final_project\frontend\src\pages\SharedReportPage.test.tsx'
source_path: 'C:\MinHyeok\skn26_projects\Final_project\README.md'
source_quality: 'mixed'
verified: true
id: '20260811000000-290c'
---

# HumouR README와 포트폴리오

## 출처와 증거 경계

- 저장소 기준 경로: `C:\MinHyeok\skn26_projects\Final_project\README.md`, `C:\MinHyeok\skn26_projects\Final_project\docs\00-overview\project-overview.md` (2026-08-11 확인)
- 포트폴리오 기준 경로: `C:\MinHyeok\minhyeok328.github.io\src\data\portfolio.ts`의 `flagshipProject`와 `https://minhyeok328.github.io/`의 HumouR 상세 모달 (2026-08-11 확인)
- 구현 확인 경로: 위 frontmatter의 `frontend/src/api`, `frontend/src/hooks` 코드와 테스트 (2026-08-11 확인)
- README와 코드는 팀 저장소의 1차 자료다. 포트폴리오는 서민혁의 역할과 경험에 관한 개인 1차 자료이며 독립적인 제삼자 검증은 아니다. 코드가 저장소에 존재한다는 사실만으로 개인 작성자나 소유권을 판정하지 않는다.

## 저장소와 README에서 확인한 팀 사실

- HumouR는 회사 정보, JD, 체크리스트, 지원서, AI 분석 리포트, 면접 질문, 문서 채팅과 제한 공유를 하나의 채용 운영 흐름으로 연결한 팀 프로젝트다. 분석 결과는 합격 여부를 자동 결정하는 값이 아니라 담당자의 검토를 돕는 참고 정보로 설명된다.
- React·TypeScript 프론트엔드, Django API, Celery 비동기 작업, LangGraph 분석, Pinecone 검색과 AWS 배포가 팀 시스템을 이룬다. 이 구성은 팀 산출물이며 특정 개인의 단독 기여를 뜻하지 않는다.
- README 역할표는 서민혁에게 `프론트 구조, 인증·CSRF·응답 계약, 요청 수명주기, QA·보안 안정화, 문서화`를 배정한다. API Key 관리·제한 모드·공유 리포트 UI는 다른 프론트엔드 팀원의 주요 기여로도 명시된다.
- 저장소가 밝힌 한계에는 소표본 모델 평가, 프롬프트 버전 민감도, 외부 서비스 의존, 임시 비밀번호 복구 방식, 상대적으로 약한 백엔드 테스트·배포 gate가 포함된다.

## 포트폴리오의 개인 서술

- 포트폴리오는 기간을 `2026.05.22 – 07.15`로 기록하고, 서민혁이 React·TypeScript 프론트엔드 구조와 서비스 통합을 담당했다고 서술한다. 기간은 README에 없어 개인 서술 범위로만 남긴다.
- 직접 기여로 Axios·CSRF 요청 계층, 도메인 API client, Zod 응답 검증, adapter, TanStack Query 데이터 흐름을 기록한다.
- 일반 로그인과 외부 API Key 제한 화면의 인증·세션·Query 캐시 경계, 인증 만료·요청 취소·오래된 응답 차단·오류 정제·캐시 정리를 직접 다뤘다고 기록한다.
- JD·지원서·분석 리포트·면접 질문·외부 공유·문서 채팅의 화면과 API 흐름 통합, 프론트엔드 테스트·QA·인터페이스 문서 체계 구축과 확장을 기여로 적는다.
- 개인 회고는 4차 프로젝트의 화면·통신 중심 관점에서 인증·권한·상태·검증과 운영 환경을 함께 보는 관점으로 넓어졌다고 말한다. 감정과 성장 서술은 개인 경험이지 팀 저장소로 독립 검증된 결과가 아니다.

## 코드와 테스트가 보강하는 구현 사실

- `frontend/src/api/httpClient.ts`에는 Axios 인스턴스, same-origin 세션 쿠키, CSRF 헤더, 선택적 `X-API-Key`, 오류 정규화, 인증 실패 감지와 보호 요청 취소가 구현되어 있다. `backendSchemas.ts`, 도메인 client, `appDataService.ts`와 adapter들은 응답 검증·변환·화면 모델 경계를 보강한다.
- `queryOptions.ts`는 인증 방식과 불투명 세션 식별자를 query key에 넣고 TanStack Query의 `AbortSignal`을 loader에 전달한다. `useAuthSession.ts`는 account와 API Key 세션을 구분하고, 늦은 프로필 응답이 새 세션을 덮지 않도록 요청을 중단한다.
- `queryClient.ts`와 `useAuthExpiryHandler.ts`는 인증 만료 때 보호 요청과 query를 취소하고 캐시·인증 상태를 비운 뒤 로그인 화면으로 이동한다. 관련 테스트는 캐시와 mutation 제거 순서, 세션 namespace 분리와 늦은 응답 차단을 확인한다.
- `useSharedReportSession.ts`와 JD 채팅 구성은 `AbortController`와 request id를 함께 사용해 이전 요청과 뒤늦은 결과가 현재 화면을 갱신하지 못하게 한다.
- 페이지·도메인 client·검증 스크립트와 테스트가 JD, 지원서, 분석 리포트, 면접 질문, 제한 공유와 채팅 흐름의 존재를 뒷받침한다. 이 코드 근거는 포트폴리오 서술과 일치하는 구현을 보여 주지만 누가 각 줄을 작성했는지는 증명하지 않는다.

## 차이와 근거 공백

- README는 AWS 인프라와 배포 구성을 백엔드 팀원의 주요 기여로 배정한다. 포트폴리오도 서민혁의 범위를 프론트엔드·API 연동과 동작 검증으로 제한하므로 AWS 인프라 구축을 개인 기여로 기록하지 않는다.
- README는 API Key 관리·제한 모드·공유 리포트 UI를 다른 프론트엔드 팀원의 주요 기여로도 적는다. 따라서 서민혁의 기여는 포트폴리오가 명시한 공통 인증·세션·캐시 경계와 통합 범위로 한정하고, 기능 전체의 소유권을 주장하지 않는다.
- 저장소 코드와 테스트는 구현 상태를 확인할 수 있지만 개인별 commit·PR 검토나 독립 평가를 대신하지 않는다. README와 포트폴리오에 없는 개인 동기, 성과, 감정은 추론하지 않는다.
- README의 테스트 파일·검증 스크립트 수와 모델 성능은 팀 저장 시점의 기록이다. 이 노트에서는 개인 성과나 운영 SLA로 확대하지 않는다.

## 분리한 노트

- 프로젝트 맥락: [[SKN26 Final HumouR AI HR 채용 보조]]
- 파생 원칙: [[인증 만료는 오류가 아니라 사용자 흐름의 일부다]], [[오래된 비동기 응답은 최신 상태를 덮지 못하게 해야 한다]], [[프론트엔드 상태는 권한 경계와 함께 정리해야 한다]]
- 기존 개념: [[React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다]], [[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]], [[CSRF 방어는 브라우저 세션 요청의 출처를 검증한다]]
