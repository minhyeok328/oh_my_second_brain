---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'python'
  - 'streamlit'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders'
  - 'C:\MinHyeok\skn26_2nd_1st\2nd_project'
source_quality: 'mixed'
verified: false
id: '20260530000000-3e27'
---

# Streamlit 기본 UI

태그: #llm_wiki #python #streamlit

## 한 줄 정의

Streamlit 기본 UI는 Python 코드만으로 입력 위젯, 표, 차트, 페이지 레이아웃을 빠르게 구성하는 데이터 앱 화면 패턴이다.

## 내 말로 다시 설명

Streamlit은 분석 코드와 화면을 가깝게 붙여준다. 모델 결과나 계산 로직을 빠르게 보여주기 좋지만, 상태 관리와 UI 구조를 정리하지 않으면 notebook 같은 script가 화면 전체를 지배하게 된다.

## 언제 쓰는가

- 데이터 분석 결과나 모델 예측을 빠르게 대시보드로 보여줄 때
- 사용자가 입력값을 바꾸면 계산 결과가 바로 갱신되는 도구를 만들 때
- 팀 프로젝트에서 백엔드/프론트 분리 전에 프로토타입을 검증할 때

## 언제 쓰면 안 되는가

- 복잡한 프론트 라우팅, 권한, 대규모 컴포넌트 상태가 필요한 경우
- DB/API 호출을 매 rerun마다 무제한 반복하는 경우
- session state 없이 단계형 UX를 억지로 구현하는 경우

## 프로젝트 예시

- [[SKN26 1차 차량 운영비 프로젝트]]는 Streamlit에서 차량 모델, 등급, 연도를 입력받고 DB 조회 결과와 TCO 계산 결과를 보여준다.
- [[SKN26 2차 신용카드 고객 이탈 분석]]은 Streamlit으로 분석 대시보드, 모델별 확률, 전략 보고서 페이지를 구성했다.

## 실패 조건

- `st.session_state`를 쓰지 않으면 검색 후 선택 상태가 rerun 때 사라진다.
- `st.cache_data`를 무분별하게 쓰면 오래된 DB/API 결과를 보여줄 수 있다.
- CSS를 과하게 주입하면 Streamlit 버전 변화에 취약하다.

## 관련 개념

- [[Streamlit Session State]]
- [[Pandas DataFrame]]
- [[MLflow]]
- [[XGBoost]]

## 먼저 확인할 질문

- 이 화면은 분석용 prototype인가, 운영 서비스 UI인가?
- rerun이 발생해도 사용자의 선택과 계산 결과가 일관되게 유지되는가?
