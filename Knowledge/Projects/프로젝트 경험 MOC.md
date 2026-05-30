---
type: "moc"
status: "active"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'project'
  - 'experience'
  - 'second_brain'
source:
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
---

# 프로젝트 경험 MOC

태그: #llm_wiki #project #experience #second_brain

## 목적

이 문서는 프로젝트를 단순 결과물이 아니라 second brain의 경험 지식으로 관리하기 위한 입구다. 개념 노트는 "무엇인가"를 설명하고, 프로젝트 경험 노트는 "내가 어떤 상황에서 왜 그것을 썼는가"를 설명한다.

## 경험 지식 구조

- [[프로젝트 적용 로그]]: 프로젝트와 사용 지식의 전체 index
- [[프로젝트 의사결정 로그]]: 코드와 README에서 확인되는 설계 선택
- [[프로젝트 실패와 디버깅 로그]]: 실패 조건, 디버깅 기준, 다음에 먼저 확인할 지점
- [[프로젝트 회고 질문 세트]]: 사용자 개인 회고 입력이 필요한 질문 모음
- [[프로젝트 기반 개발자 정체성]]: 프로젝트 경험을 통해 정리한 협업형 개발자 서사
- [[개인 Dev Rules]]: commit, branch, issue, docs 중심의 개인 협업 운영 원칙
- 프로젝트별 상세 노트: 문제 정의, 사용 기술, 판단 기준, 다음 보강 노트
- Permanent Note: 프로젝트 경험에서 반복 가능한 개념으로 끌어올린 원자 지식

## 프로젝트를 관통하는 정체성

- 가장 큰 전환점은 [[SKN26 2차 프로젝트 - 카드 이탈 예측]]이다. 이 프로젝트에서 문서 작업, 커밋 컨벤션, Docker, CLI git, 브랜치 전략을 접하며 팀 프로젝트에는 지켜야 할 규칙과 생각해야 할 비용이 많다는 것을 느꼈다.
- 다음 프로젝트에서 반드시 지키고 싶은 방식은 문서화와 dev rules다. 소통에는 한계가 있으므로 문서는 팀의 공유 기억이고, 규칙은 협업 비용을 줄이는 장치다.
- 어떤 프로젝트에서도 포기하지 않을 dev rules는 commit, branch, issue, docs다.
- 포트폴리오에서는 기술을 다루는 사람을 넘어, 협업을 위해 정말 많이 노력하는 개발자로 보이고 싶다.
- 정리 노트: [[프로젝트 기반 개발자 정체성]], [[개인 Dev Rules]]

## 프로젝트별 경험 축

### 1차 차량 TCO

- 상세 노트: [[SKN26 1차 프로젝트 - 차량 TCO]]
- 핵심 경험: Streamlit multi-step 상태 유지, MySQL 조회, 외부 차량/유가 데이터 수집, 월간 TCO 계산
- 승격된 지식: [[Streamlit Session State]], [[MySQL Connector Python]], [[SQL SELECT와 WHERE]], [[Requests]]
- 개인 회고: API 수집 영역에 가장 많이 관여했다. 노베이스에 가까운 상태에서 코딩, AI, 에이전트와 친숙해지는 첫 프로젝트라 전반적으로 어려웠고, 코딩은 많이 작성하고 가지고 놀아야 흡수가 빨라진다는 깨달음을 얻었다.
- 추가 입력 필요: 1차 프로젝트 자체를 다시 만든다면 API 수집, DB 조회, Streamlit 상태 관리 중 어떤 구조를 먼저 바꿀지

### 2차 카드 이탈 예측

- 상세 노트: [[SKN26 2차 프로젝트 - 카드 이탈 예측]]
- 핵심 경험: BankChurners EDA, Unknown Income 보정 실험, 모델 비교, MLflow 실험 관리, Docker Compose 실행 환경
- 승격된 지식: [[분류 평가 지표]], [[Train Test Split]], [[Feature Engineering]], [[MLflow]], [[FastAPI]], [[XGBoost]], [[Docker Compose]]
- 개인 회고: 모델링 영역에서 군집화와 차원축소까지 시도하며 결측치를 역으로 추정해보려 했다. Unknown Income은 시각화상 영향이 커서 삭제하기 어렵다고 봤고, 성능이 낮을 때는 class 불균형을 먼저 의심했다.
- 다음에 가져갈 점: 처음 접한 MLflow, Docker Compose, CLI git, 브랜치 전략은 어렵게 느껴졌지만 한 번 겪고 나니 이후 프로젝트 협업 환경을 이해하는 기반이 되었다. 특히 2차 프로젝트는 문서화와 협업 규칙의 중요성을 체감하게 한 전환점이었다.
- 다시 한다면: 결측치 예측을 다양한 실험으로 더 밀어붙이고, 결과를 더 명확한 결론으로 닫는다.

### 3차 PICKLE RAG 챗봇

- 상세 노트: [[SKN26 3차 프로젝트 - PICKLE RAG 챗봇]]
- 핵심 경험: LangGraph route, slot extraction, SQLite 검색, embedding/fixed 경로 분리, goldset 평가
- 승격된 지식: [[RAG]], [[LangGraph]], [[Function Calling]], [[SQLite]], [[RAG 평가]]
- 개인 회고: RAG 구조 설계, LLM 모델링, 모델 평가, Streamlit UI 구현에 관여했다. fixed route는 구현 후 굳이 필요했는지 의문이 남았고, 실제로는 answer 품질과 후보 밖 답변 금지가 가장 어렵고 중요하게 느껴졌다.
- 다음에 가져갈 점: LangGraph로 node를 나누면 각 단계의 책임이 보이기 때문에 관리와 디버깅이 쉬워진다.
- 다시 한다면: RAG 구조를 크게 갈아엎기보다 더 세분화하거나 에이전트 파이프라인을 붙여 최신 흐름을 실험한다.

### 4차 LG Home

- 상세 노트: [[SKN26 4차 프로젝트 - LG Home]]
- 핵심 경험: Django SSR 서비스, LangGraph 제품 상담, Pinecone 매뉴얼 RAG, JSON API, CSRF/fetch 처리
- 승격된 지식: [[Django Chatbot]], [[Django JSON API]], [[Django CSRF]], [[React SPA]], [[React API Fetch]]
- 개인 회고: 공식 프로젝트에서는 프론트엔드 파트, 문서 작업, GitHub 조직 관리를 맡았다. Django SSR은 특별히 편하다고 느낀 점보다 React 없이 template와 static JS를 맞추느라 관리 파일이 많아진 불편이 더 컸다.
- 다음에 가져갈 점: 후속 질문 처리는 챗봇에서 가장 어려운 지점으로 남았고, QA 리포트상 401 세션 만료 UX와 모바일 실기기 검증은 끝까지 확인해야 할 프론트 리스크다.
- 다시 한다면: React SPA로 분리하고 Django를 DB와 프론트엔드 사이의 JSON API 징검다리로 두는 구조를 더 명확히 잡는다.

## 경험 노트 작성 기준

- 코드와 README로 확인되는 사실은 local source 기준으로 쓴다.
- 개인의 감정, 동기, 협업 맥락은 사용자가 확인한 뒤 적는다.
- 일반 개념 설명으로 끝내지 말고 "그 프로젝트에서 왜 필요했는가"를 남긴다.
- 실패를 기록할 때는 원인 위치를 입력, 전처리, 모델, 검색, API, UI, 배포로 나눈다.

## 연결

- [[프로젝트 의사결정 로그]]
- [[프로젝트 실패와 디버깅 로그]]
- [[프로젝트 회고 질문 세트]]
- [[프로젝트 기반 개발자 정체성]]
- [[개인 Dev Rules]]
- [[LLM Wiki 보강 백로그]]
- [[LLM Wiki 검색 스코프]]
