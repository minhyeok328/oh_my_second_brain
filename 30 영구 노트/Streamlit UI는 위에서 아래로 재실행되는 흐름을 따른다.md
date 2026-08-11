---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'streamlit'
  - 'ui'
  - 'python'
aliases:
  - 'Streamlit 기본 UI'
sources:
  - 'https://docs.streamlit.io/get-started/fundamentals/main-concepts'
  - 'https://docs.streamlit.io/develop/api-reference/execution-flow'
  - 'C:\MinHyeok\lecture\01_python_workspace'
source_quality: 'mixed'
verified: true
id: '20260530000000-3e27'
---

# Streamlit UI는 위에서 아래로 재실행되는 흐름을 따른다

## 주장

Streamlit은 화면을 일반 Python 스크립트처럼 위에서 아래로 그리며, 기본적으로 코드 변경이나 위젯 상호작용 때 전체 스크립트를 다시 실행한다. 따라서 [[Streamlit 세션 상태는 재실행 사이의 값을 보존한다]]로 사용자 선택을 분리하고, 반복 비용이 큰 [[DataFrame은 열 단위 데이터 변환을 구조화한다]] 작업은 재실행 횟수와 캐시 경계를 함께 설계해야 한다.

## 연결

[[Python 기초와 Streamlit 강의]]에서 확인한 텍스트·버튼·입력·차트 예제를 내 관점으로 정리하면, 화면 선언 순서는 곧 기본 실행 순서이므로 입력 수집과 계산, 결과 출력을 읽히는 순서로 배치하는 것이 중요하다.

## 한계와 반례

항상 전체 앱만 재실행되는 것은 아니다. form은 여러 입력을 제출 시점까지 묶고 fragment는 일부 코드만 다시 실행할 수 있다. 위에서 아래로 썼다는 사실만으로 느린 I/O나 모델 추론이 효율적이지 않으므로 캐시, 상태, 실패 처리의 책임을 별도로 둬야 한다.

## 확인한 근거

- 2026-08-11: Streamlit 공식 기본 개념 문서에서 화면 갱신 시 Python 스크립트를 위에서 아래로 재실행하는 기본 데이터 흐름을 확인했다.
- 2026-08-11: Streamlit 공식 실행 흐름 문서에서 기본 전체 실행과 form·fragment·`st.rerun`·`st.stop`이 바꾸는 범위를 확인했다.
- 강의 자료 확인(개인 해석): 승인된 `01_python_workspace`에서 기본 위젯과 화면 구성 예제를 확인했고, 재실행 및 세션 격리 주장은 공식 문서로 보강했다.
