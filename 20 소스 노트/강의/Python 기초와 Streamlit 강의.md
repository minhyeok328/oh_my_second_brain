---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'lecture'
  - 'python'
aliases: []
sources:
  - 'C:\MinHyeok\lecture\01_python_workspace'
source_path: 'C:\MinHyeok\lecture\01_python_workspace'
source_quality: 'primary'
verified: true
id: '20260530000000-1ce7'
---

# Python 기초와 Streamlit 강의

## 출처

- 원본 경로: `C:\MinHyeok\lecture\01_python_workspace`
- 확인일: 2026-08-11

## 핵심 내용

- 관찰: `chap01\01_python_workspace`는 변수와 자료형, 제어 흐름, 함수, 객체 지향, 모듈, 입출력, 예외 처리 순서로 구성되어 있다.
- 관찰: `_04_function\_01_function.py`는 함수 선언과 호출, 매개변수와 반환값, 일급 객체, `*args`와 `**kwargs`를 실행 예제로 다룬다.
- 관찰: `_07_module\_01_scope.py`는 전역·지역 범위와 LEGB 이름 탐색 순서를 예제로 확인한다.
- 관찰: `_10_streamlit\_01_basics`의 스크립트들은 텍스트·데이터·입력 위젯·미디어·세션 상태를 나누어 실습한다.
- 관찰: `_10_streamlit\_01_basics\_05_session_state.py`는 일반 변수 카운터와 `st.session_state` 카운터를 비교하고, 버튼 입력 뒤 재실행과 상태 보존을 보여 준다.

## 내 해석과 의문

- 해석: Python 문법 예제가 작은 실행 단위로 나뉘어 있어, 문법 자체보다 입력·상태·함수 경계를 복습하는 출발점으로 쓰기 좋다.
- 질문: Streamlit 예제의 재실행 시점과 세션별 상태 격리는 공식 문서와 함께 다시 검증해야 한다.
- 질문: OOP, 파일 입출력, 예외 처리 예제를 실제 프로젝트의 실패 사례와 어떻게 연결할 것인가?

## 분리한 영구 노트

- [[Streamlit 기본 UI]]
- [[Streamlit Session State]]
- Python 함수와 인자 전달 — 후속 영구 노트 후보
- Python 이름 범위와 LEGB — 후속 영구 노트 후보
