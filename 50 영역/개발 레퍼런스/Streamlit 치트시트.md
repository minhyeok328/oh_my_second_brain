---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'streamlit'
  - 'python'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.streamlit.io/develop/api-reference'
  - 'https://docs.streamlit.io/develop/api-reference/caching-and-state/st.session_state'
source_quality: 'mixed'
verified: false
id: '20260530000000-f69e'
---

# Streamlit 치트시트

## 용도

Streamlit 화면 출력, 입력 위젯과 rerun 사이의 상태를 다룰 때 기본 API를 확인한다.

## 빠른 참조

- `st.title(text)`: 제목 출력
- `st.write(obj)`: 객체를 화면에 표시
- `st.dataframe(df)`: DataFrame 형태의 대화형 표 표시
- `value = st.text_input(label, key="...")`: 텍스트 입력값 받기
- `st.session_state[key]`: 같은 사용자 세션의 rerun 사이에 값을 보존

## 사용 전 확인

- 위젯 key를 명시적으로 관리해 중복과 의도치 않은 상태 공유를 피한다.
- session state의 키를 읽기 전에 초기화 여부를 확인한다.
- 캐시는 세션 상태와 목적이 다르므로 데이터·리소스 수명에 맞는 공식 cache API를 확인한다.

## 검증 범위

- 2026-08-11: Streamlit 공식 API Reference와 Session State 문서에서 위 API를 확인했다.
- 프로젝트의 Streamlit 버전, multipage 구성, cache invalidation과 배포 세션 동작은 검증하지 않았다.

## 관련 노트

- [[Streamlit UI는 위에서 아래로 재실행되는 흐름을 따른다]]
- [[Streamlit 세션 상태는 재실행 사이의 값을 보존한다]]
- [[20 소스 노트/강의/Python 기초와 Streamlit 강의|Python 기초와 Streamlit 강의]]
