---
type: 'project'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'project_context'
  - 'project'
  - 'skn26'
  - 'django'
aliases:
  - 'SKN26 4차 프로젝트 - LG Home'
sources:
  - 'C:\MinHyeok\skn26_projects\4th_project\README.md'
  - 'C:\MinHyeok\skn26_projects\4th_project\products\views.py'
  - 'C:\MinHyeok\skn26_projects\4th_project\static\js\api-response.js'
  - 'C:\MinHyeok\skn26_projects\4th_project\static\js\chatpage.js'
  - 'C:\MinHyeok\skn26_projects\4th_project\static\js\wishlist-toggle.js'
  - 'C:\MinHyeok\skn26_projects\4th_project\static\js\search\filter.js'
  - 'https://minhyeok328.github.io/'
source_quality: 'mixed'
verified: true
id: '20260530000000-69b5'
---

# SKN26 4차 LG Home AI 가전 상담

## 프로젝트 사실

- LG 가전 다섯 범주의 검색·상품 상세·찜·계정·상담을 Django 웹 애플리케이션으로 연결한 팀 프로젝트다. 상품 조건 검색은 Django ORM을, 제품 상담은 LangGraph를, 사용설명서 질의는 Pinecone RAG를 사용한다. (근거: `README.md` Overview, Features, Tech Stack)
- README가 기록한 제한에는 비밀번호 찾기·결제의 서버 미연동, 일부 목업 데이터, 챗봇 세션 만료 시 로그인 유도 미정이 포함된다. (근거: `README.md` Limitations)
- 개인 포트폴리오는 진행 기간을 `2026-05-20 ~ 2026-05-21`로 적지만 README에는 기간이 없다. 따라서 기간은 개인 서술로만 기록한다. (근거: 포트폴리오 상세 모달, 2026-08-11 확인)

## 팀 산출물

- 팀은 Django SSR 화면과 상품 DB, 인증·찜, 대화 이력, LangGraph 상담 흐름과 사용설명서 검색을 하나의 서비스로 구성했다. 저장소의 기능 존재는 팀 결과를 설명하며 특정인의 소유권을 뜻하지 않는다. (근거: `README.md` Features, Directory Structure)
- 검색 뷰는 GET 조건을 ORM 검색에 넘기고 12건 단위로 페이지를 나눈다. 공통 JavaScript는 JSON 응답·CSRF·오류 처리를 묶고, 채팅 코드는 요청 중 재전송 방지와 제한된 HTML 정제를 구현한다. (근거: `products\views.py`, `static\js\api-response.js`, `static\js\chatpage.js`)

## 직접 기여

- README 역할 표는 서민혁에게 Frontend를 배정한다. 서민혁 개인 회고는 Figma 화면 구조, Tailwind CSS·Django 템플릿·JavaScript 구현, Git 브랜치와 static/template 구조 정리를 직접 수행했다고 기록한다. (근거: `README.md` Team, 서민혁 개인 회고)
- 개인 포트폴리오는 GET·SSR 검색 상태와 페이지네이션, 찜·채팅 JSON 통신의 CSRF·오류·로딩·중복 요청 처리, AI 응답 정제와 DOM 표시를 직접 기여로 적는다. 저장소에는 해당 구현이 확인된다. (근거: 포트폴리오 직접 기여, `products\views.py`, `static\js\api-response.js`, `static\js\chatpage.js`, `static\js\wishlist-toggle.js`, `static\js\search\filter.js`)
- LangGraph·Pinecone·상품 DB는 팀 시스템 연동 범위다. README 역할 표가 각각 다른 팀원에게 Backend, RAG, Database, LangGraph를 배정하므로 서민혁의 모델링 단독 기여로 쓰지 않는다. (근거: `README.md` Team)

## 의사결정과 근거

- 검색 조건과 페이지 상태를 URL 쿼리스트링에 보존하는 GET·SSR 흐름을 사용했다. 새로고침 뒤에도 서버 검색 결과와 화면 조건을 같은 기준으로 복원하려는 선택이다. (근거: 포트폴리오 기술 설계와 판단, `products\views.py`, `static\js\search\filter.js`)
- 찜·채팅 요청은 공통 JSON 응답 처리, CSRF, 오류 표시와 기능별 실행 중 상태를 사용했다. 정상 응답뿐 아니라 실패와 반복 입력도 화면 상태로 다루려는 선택이며 [[CSRF 방어는 브라우저 세션 요청의 출처를 검증한다]]와 연결된다. (근거: 포트폴리오 기술 설계와 판단, `static\js\api-response.js`, `static\js\chatpage.js`, `static\js\wishlist-toggle.js`)

## 실패·디버깅

- Tailwind CSS와 Django를 연결하는 동안 패키지 충돌, Node 실행 오류와 경로 설정 문제가 반복되었다. 개인 회고는 실행 구조와 설정을 분석하며 원인을 찾았다고 기록하지만, 개별 오류의 재현 절차와 수정 커밋은 근거에 없어 더 구체화하지 않는다. (근거: `README.md` 서민혁 개인 회고, 포트폴리오 성장과 회고)
- 챗봇 401·세션 만료의 로그인 유도, 비밀번호 찾기·결제 서버 연동과 일부 목업 데이터는 완료되지 않은 범위로 남았다. (근거: `README.md` Limitations)

## 회고

> 개인 회고: 화면을 예쁘게 만드는 일보다 사용자가 어떤 순서로 정보를 보고 각 동작이 서버와 어떻게 연결되는지를 함께 설계해야 한다는 점을 배웠다. UI·서버 통신·환경 설정과 협업 구조까지 경험했지만 인증·권한·테스트·배포를 하나의 운영 관점으로 체계화하는 단계는 다음 과제로 남았다. (근거: `README.md` 서민혁 개인 회고, 개인 포트폴리오 성장과 회고)

## 연결

- 개념: [[Django ORM 모델은 데이터 구조와 제약을 코드로 표현한다]], [[QuerySet은 평가 시점을 늦춰 쿼리 조합을 가능하게 한다]], [[Django 챗봇은 대화 상태와 요청 경계를 함께 관리해야 한다]], [[벡터 저장소는 임베딩과 메타데이터를 함께 관리해야 한다]]
- 학습 출처: [[Django 웹 서버 강의]], [[웹 클라이언트 강의]], [[LLM과 RAG 강의]]
- 경험 기록: [[프로젝트 의사결정 로그#프로젝트 경험 — 4차 SSR과 검색 책임 분리]], [[프로젝트 실패와 디버깅 로그#미확인 디버깅 후보 — 4차 LG Home]], [[프로젝트 경험 지도#4차 LG Home]]
- 이전 경험: [[SKN26 3차 PICKLE 맛집 추천 챗봇]]

## 확인한 근거

- `C:\MinHyeok\skn26_projects\4th_project\README.md` — 팀 역할, 서비스 범위, 기술 구성, 제한과 개인 회고 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\4th_project\products\views.py` — GET 조건·ORM 검색·Paginator 흐름 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\4th_project\static\js\api-response.js` — 공통 JSON·CSRF·오류 처리 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\4th_project\static\js\wishlist-toggle.js` — `wishlistInFlight` 중복 요청 차단, 버튼 disabled·`aria-busy` 상태와 CSRF 포함 `fetchJson` 요청·네트워크/파싱 오류 처리 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\4th_project\static\js\chatpage.js` 및 `static\js\search\filter.js` — 채팅 정제·중복 요청 방지와 필터 상태 처리 (2026-08-11 확인)
- `https://minhyeok328.github.io/` — LG Home AI 가전 상담 상세 모달의 개인 역할·판단·회고; 별도 심층 URL은 제공되지 않음 (2026-08-11 확인)
