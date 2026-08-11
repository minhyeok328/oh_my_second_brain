---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'streamlit'
  - 'state'
  - 'python'
aliases:
  - 'Streamlit Session State'
sources:
  - 'https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state'
  - 'https://docs.streamlit.io/develop/api-reference/caching-and-state'
  - 'C:\MinHyeok\lecture\01_python_workspace'
source_quality: 'mixed'
verified: true
id: '20260530000000-9091'
---

# Streamlit 세션 상태는 재실행 사이의 값을 보존한다

## 주장

`st.session_state`는 한 사용자 세션의 변수를 스크립트 재실행과 멀티페이지 앱 사이에서 공유하게 한다. [[Streamlit UI는 위에서 아래로 재실행되는 흐름을 따른다]]에서 버튼 한 번마다 지역 변수가 다시 만들어지는 문제를 피하고, [[MLflow는 실험 조건과 결과를 함께 추적한다]]에서 고른 run 같은 화면 선택값을 같은 세션 동안 유지하는 경계다.

## 연결

[[Python 기초와 Streamlit 강의]]의 위젯 실습을 내 관점으로 정리하면, 위젯 `key`와 세션 상태 키를 화면의 임시 상태 계약으로 명시해야 재실행 후 값의 출처를 추적하기 쉽다.

## 한계와 반례

세션 상태는 데이터베이스나 사용자 계정 저장소가 아니다. WebSocket 연결이 끊기거나 탭을 다시 불러오면 상태가 초기화될 수 있고, 세션 사이에서 값을 공유하지 않는다. 직렬화 강제 설정에서 pickle을 사용할 때는 신뢰하지 않는 데이터를 역직렬화해서도 안 된다.

## 확인한 근거

- 2026-08-11: Streamlit 공식 Session State 문서에서 변수가 사용자 세션별로 재실행과 멀티페이지 앱 사이에 유지되며, WebSocket 연결이 재설정되면 상태도 초기화되는 범위를 확인했다.
- 2026-08-11: Streamlit 공식 caching and state 개요에서 위젯의 기본 상태와 Session State의 추가 상태 관리 책임을 확인했다.
- 강의 자료 확인(개인 해석): 승인된 `01_python_workspace`에서 Streamlit 위젯 예제를 확인했고, 재실행 시점과 세션 격리는 공식 문서로 보강해야 한다는 근거 공백을 반영했다.
