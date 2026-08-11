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
  - 'rag'
aliases:
  - 'SKN26 3차 프로젝트 - PICKLE RAG 챗봇'
sources:
  - 'C:\MinHyeok\skn26_projects\3rd_project\README.md'
  - 'C:\MinHyeok\skn26_projects\3rd_project\src\pipeline.py'
  - 'C:\MinHyeok\skn26_projects\3rd_project\src\slot_extractor.py'
  - 'C:\MinHyeok\skn26_projects\3rd_project\src_test3\evaluate_llm.py'
  - 'C:\MinHyeok\skn26_projects\3rd_project\src_test3\llm_eval_report.json'
  - 'https://minhyeok328.github.io/'
source_quality: 'mixed'
verified: true
id: '20260530000000-b119'
---

# SKN26 3차 PICKLE 맛집 추천 챗봇

## 프로젝트 사실

- 신대방삼거리 식당 100곳의 메뉴·리뷰·태그를 SQLite에 저장하고, 자연어 조건을 구조화해 근거가 있는 식당 한 곳을 추천하는 팀 프로젝트다. 데이터는 크롤링 시점의 고정 자료이며 다른 지역과 여러 식당 비교는 기본 범위가 아니다. (근거: `README.md` Overview, Evaluation Results, Limitations)
- 팀 저장소의 실행 흐름은 질문 라우팅, 슬롯 추출, DB 검색, 근거 기반 생성과 Streamlit 표시로 구성된다. (근거: `README.md` Features, `src\pipeline.py`)
- 개인 포트폴리오는 진행 기간을 `2026-04-24 ~ 2026-04-27`로 적지만 README에는 기간이 없다. 따라서 기간은 개인 서술로만 기록한다. (근거: 포트폴리오 상세 모달, 2026-08-11 확인)

## 팀 산출물

- LangGraph 상태 그래프가 `embedding`과 `fixed` 경로를 나누고 두 경로를 검색·생성 단계로 합류시킨다. 이는 저장소에서 확인되는 팀 구현이며 개인 기여는 다음 절의 명시적 귀속으로만 판단한다. (근거: `src\pipeline.py`)
- 최종 내부 평가는 같은 DB의 50개 사례에서 41개 전체 조건 통과, target hit 96%를 기록했다. 이는 프로덕션 정확도가 아니라 자동 생성된 내부 골드셋 기준 결과다. (근거: `README.md` 10장, `src_test3\llm_eval_report.json`)

## 직접 기여

- README 역할 표는 서민혁에게 LLM과 Frontend를 배정하고, 개인 회고는 LangChain에서 LangGraph로의 구조 전환과 사용자 질의부터 검색·생성까지의 파이프라인 구성을 직접 수행했다고 기록한다. (근거: `README.md` Team, 서민혁 개인 회고)
- 개인 포트폴리오는 LangGraph RAG 파이프라인, strict JSON Schema 기반 슬롯 형식, SQLite 검색 연결, Streamlit 통합과 내부 평가 체계를 직접 기여로 적는다. 해당 구조와 평가 코드는 저장소에서도 확인된다. (근거: 포트폴리오 직접 기여, `src\pipeline.py`, `src\slot_extractor.py`, `src_test3\evaluate_llm.py`)
- 저장소 존재만으로 단독 소유를 주장하지 않는다. 위 귀속은 README의 이름별 역할·개인 회고와 포트폴리오 개인 서술이 함께 지지하는 범위다.

## 의사결정과 근거

- 질문 유형에 따라 단계가 늘어나자 단일 LangChain 흐름을 상태와 조건 분기가 보이는 LangGraph로 바꿨다. 각 단계의 입력과 출력을 분리하려는 판단이며 [[LangGraph 상태는 노드 사이의 데이터 계약이다]], [[조건부 엣지는 상태에 따라 다음 실행 경로를 선택한다]]와 연결된다. (근거: README 개인 회고, 포트폴리오 기술 설계와 판단, `src\pipeline.py`)
- 슬롯 출력을 strict JSON Schema로 고정하고 평가는 route·payload·target·answer·retrieval로 분리했다. 자연스러운 답변만으로 검색 품질을 판단하지 않으려는 선택이다. (근거: `src\slot_extractor.py`, `src_test3\evaluate_llm.py`, 포트폴리오 기술 설계와 판단)

## 실패·디버깅

- 초기에 아키텍처와 기술 간 인터페이스를 충분히 합의하지 않은 채 설계와 구현을 병행해, 기능이 늘수록 기존 코드를 다시 수정하는 데 시간이 들었다. (근거: `README.md` 서민혁 개인 회고, 포트폴리오 성장과 회고)
- 최종 내부 평가에서도 9개 사례가 전체 조건을 통과하지 못했고, 주요 잔여 실패는 payload miss 7건과 target 미검색 2건이었다. 이를 검색 시스템의 완전한 성공으로 표현하지 않는다. (근거: `README.md` 10.4절, `src_test3\llm_eval_report.json`)

## 회고

> 개인 회고: 하나의 LLM 호출보다 상태, 검색 조건과 근거, 화면까지 이어지는 흐름을 나누는 일이 중요했다. 초기 구조 합의가 부족해 수정이 많았던 경험을 통해, 이후에는 구현 전에 데이터 흐름과 팀 작업 경계를 구체화하고 변경을 계속 공유하려 한다. (근거: `README.md` 서민혁 개인 회고, 개인 포트폴리오 성장과 회고)

## 연결

- 개념: [[RAG의 성능은 검색 단계의 품질에서 시작된다]], [[RAG 평가는 검색과 생성을 분리해서 측정해야 한다]], [[함수 호출은 자연어 요청을 구조화된 도구 입력으로 바꾼다]], [[SQLite는 단일 파일로 작은 애플리케이션의 영속성을 단순화한다]]
- 학습 출처: [[LLM과 RAG 강의]], [[Python 기초와 Streamlit 강의]]
- 경험 기록: [[프로젝트 의사결정 로그#프로젝트 경험 — 3차 RAG 경로와 평가 분리]], [[프로젝트 실패와 디버깅 로그#미확인 디버깅 후보 — 3차 PICKLE RAG 챗봇]], [[프로젝트 경험 지도#3차 PICKLE RAG 챗봇]]
- 앞뒤 경험: [[SKN26 2차 신용카드 고객 이탈 분석]], [[SKN26 4차 LG Home AI 가전 상담]]

## 확인한 근거

- `C:\MinHyeok\skn26_projects\3rd_project\README.md` — 팀 역할, 시스템 범위, 평가·한계와 개인 회고 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\3rd_project\src\pipeline.py` — LangGraph 상태·노드·조건 분기 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\3rd_project\src\slot_extractor.py` — strict JSON Schema 슬롯 출력 (2026-08-11 확인)
- `C:\MinHyeok\skn26_projects\3rd_project\src_test3\evaluate_llm.py` 및 `llm_eval_report.json` — 내부 평가 방법과 결과 (2026-08-11 확인)
- `https://minhyeok328.github.io/` — PICKLE 맛집 추천 챗봇 상세 모달의 개인 역할·판단·회고; 별도 심층 URL은 제공되지 않음 (2026-08-11 확인)
