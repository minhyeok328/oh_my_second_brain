---
type: "moc"
status: "active"
created: "2026-05-30"
updated: "2026-06-23"
reviewed: "2026-06-23"
tags:
  - 'llm_wiki'
  - 'moc'
  - 'backlog'
  - 'quality'
source:
  - 'C:\Obsidian\KnowledgeVault\Knowledge'
---

# LLM Wiki 보강 백로그

태그: #llm_wiki #moc #backlog #quality

## 현재 위험

- `wiki-standardized` 노트가 199개 남아 있다.
- placeholder 문구는 전체 `Knowledge` 기준 399건 남아 있다.
- 기존 프로젝트 보강 대상 노트는 정리됐지만, 전체 vault 검색에서는 덜 익은 노트가 아직 노이즈가 될 수 있다.
- 따라서 [[LLM Wiki 검색 품질 게이트]]를 먼저 적용하고, 이후 공식 문서 확인 비용이 크고 학습 빈도가 높은 노트부터 승격한다.

## 승격 완료 기준

`wiki-standardized` 노트를 `wiki-expanded`로 승격하려면 아래 항목을 채운다.

- boilerplate 문구 제거
- 공식/강의 근거와 프로젝트 사례 분리
- 한 문장 정의와 실제 사용하는 이유 분리
- 사용 조건과 쓰지 말아야 할 조건 작성
- 공식 문서, 강의 실습, 검증된 레퍼런스 중 최소 하나 연결
- 프로젝트 예시는 적용 사례 섹션에만 연결
- 실패 조건 작성
- 먼저 확인할 질문 작성
- 관련 MOC와 프로젝트 노트에서 역링크 확인

## 승격 완료

- 2026-05-30 1차 차량 TCO: [[Streamlit Session State]], [[MySQL Connector Python]], [[SQL SELECT와 WHERE]], [[Requests]]
- 2026-05-30 2차 카드 이탈 예측: [[분류 평가 지표]], [[Train Test Split]], [[Feature Engineering]]

## 1순위: 공식 공부 효율이 큰 노트

- [[RAG]], [[Embedding]], [[Vector Store]], [[Retriever]]
- [[LangGraph]], [[Function Calling]], [[OpenAI API]]
- [[Django QuerySet]], [[Django ORM Model]], [[Django View]], [[Django Session과 Auth]]
- [[React API Fetch]], [[useEffect]], [[React State]]
- [[Docker Compose]], [[Dockerfile]], [[GitHub Actions Workflow]]

## 2순위: 프로젝트 적용 사례가 있는 노트

### 1차 차량 TCO

- 완료: rerun 이후 검색/선택 상태 유지, DB 연결과 cursor, 차량명 `LIKE` 검색, 외부 API 호출 실패 기준을 보강했다.

### 2차 카드 이탈 예측

- 완료: accuracy, recall, precision, F1, ROC-AUC 선택 기준, train/test 분리, feature 생성과 누수 기준을 보강했다.
- [[데이터 전처리]]: Unknown 값 처리, 라벨/타깃 누수 방지 기준 보강
- [[Random Forest]], [[앙상블 학습]]: XGBoost/LightGBM 비교 기준 보강

### 3차 PICKLE RAG

- [[Text Splitter]]: chunk 크기와 검색 실패의 관계 보강
- [[Document Loader]]: 원천 데이터 적재와 RAG 근거 추적 기준 보강
- [[Reranking]]: 후보 재정렬이 필요한 조건 보강
- [[Query Expansion]]: 사용자의 모호한 맛집 질문을 확장할 때의 위험 보강
- [[Generation Optimization]]: 근거 밖 답변 억제와 출력 제약 보강

### 4차 LG Home

- [[Django ORM Model]]: 상품/찜/리뷰/사용자 모델 관계 보강
- [[Django Session과 Auth]]: 로그인, 찜, 챗봇 상태 관리 기준 보강
- [[Django Template]]: SSR 기준 공식 프로젝트 맥락 보강
- [[Django View]]: HTML view와 JSON API view 분리 기준 보강
- [[Middleware]]: 인증, 세션, 요청 흐름에서 확인할 기준 보강

## 3순위: 면접/회고 효율이 큰 노트

- [[과적합]], [[교차검증]], [[하이퍼파라미터 튜닝]]
- [[SQL JOIN]], [[SQL 트랜잭션]], [[SQL 제약조건]]
- [[React]], [[React State]], [[useEffect]], [[useState]], [[useMemo]], [[useCallback]]
- [[Dockerfile]], [[Docker Container]], [[Docker Image]], [[Docker Network]]

## 4순위: 새로 만들 후보

아래는 프로젝트에서 쓰였거나 언급됐지만 아직 독립 Permanent Note가 약한 후보들이다. 생성 여부는 다음 작업에서 결정한다.

- LightGBM
- EasyEnsemble
- 클래스 불균형 처리
- Pinecone
- TypeScript
- Tailwind CSS
- 모델 서빙 파이프라인
- Django AJAX

## 낮은 우선순위

- 디자인 패턴 세부 노트는 프로젝트 코드와 직접 연결된 사례가 확인되기 전까지 뒤로 둔다.
- 멀티모달 세부 노트는 실제 프로젝트 근거가 생기기 전까지 개념 보강만 최소화한다.

## 다음 결정 필요

- 다음 승격 배치를 ML/DB/Web/RAG 중 어느 축으로 잡을지 결정해야 한다.
- 새 후보 노트는 먼저 공식/강의 기반 개념 노트로 만들고, 프로젝트 근거는 적용 사례로만 붙일지 결정해야 한다.

## 연결

- [[LLM Wiki 검색 품질 게이트]]
- [[LLM Wiki 운영 원칙]]
- [[프로젝트 적용 로그]]
- [[Knowledge Index]]
