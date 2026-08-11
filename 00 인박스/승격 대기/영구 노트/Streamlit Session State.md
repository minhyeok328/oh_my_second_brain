---
type: 'inbox'
status: 'seed'
created: '2026-05-30'
updated: '2026-05-30'
reviewed: '2026-05-30'
tags:
  - 'llm_wiki'
  - 'streamlit'
  - 'python'
  - 'web'
  - 'state'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders\main.py'
source_quality: 'mixed'
verified: false
id: '20260530000000-9091'
---

# Streamlit Session State

태그: #streamlit #python #web #state #llm_wiki

## 한 줄 정의

Streamlit Session State는 위젯 조작으로 스크립트가 다시 실행되어도 사용자별 선택값과 중간 결과를 유지하는 상태 저장소다.

## 왜 중요한가

Streamlit은 버튼 클릭, 입력 변경, selectbox 선택 때마다 파일을 위에서부터 다시 실행한다. 검색 결과를 본 뒤 차량을 선택하고, 그 선택을 다시 비용 계산에 넘겨야 하는 앱에서는 상태를 명시적으로 저장하지 않으면 사용자가 방금 고른 차량 정보가 사라진다.

## 핵심 개념

- `st.session_state`는 사용자 세션별 key-value 저장소다.
- 위젯에 `key`를 주면 같은 이름으로 값이 자동 저장된다.
- 직접 만든 상태값은 사용 전에 초기화해야 한다.
- 검색 버튼처럼 한 번 눌린 뒤 화면을 열어두어야 하는 흐름은 boolean 상태로 보관한다.
- DB/API 결과 row를 저장할 때는 row index 의미가 바뀌지 않는지 같이 확인해야 한다.

## 프로젝트 예시

[[SKN26 1차 차량 운영비 프로젝트]]의 `main.py`는 차량 검색과 비용 계산이 여러 단계로 나뉜다.

- `open_result`: 검색 버튼을 누른 뒤 결과 영역을 유지한다.
- `model_name`: 모델명 입력값을 검색 조건으로 사용한다.
- `use_grade`, `in_grade`: 등급 필터 사용 여부와 선택 등급을 유지한다.
- `use_year`, `in_year`: 연식 필터 사용 여부와 입력 연식을 유지한다.
- `in_oil`: 사용자가 선택한 차량 연비 row를 비용 계산 단계로 넘긴다.
- `in_price`: 사용자가 선택한 가격 row를 최종 견적 요약에 사용한다.

이 구조 덕분에 사용자는 차량 검색, 상세 모델 선택, 주행 패턴 선택, 정비비 계산을 한 화면 흐름 안에서 이어갈 수 있다.

## 언제 쓰는가

- Streamlit 앱에서 검색 결과를 다음 단계 계산에 넘겨야 할 때
- checkbox, selectbox, text_input 값이 rerun 이후에도 유지되어야 할 때
- 챗봇 메시지, 멀티스텝 폼, 필터 상태, 선택된 DB row를 저장해야 할 때
- 버튼 클릭 이후 특정 영역을 계속 보여줘야 할 때

## 언제 쓰면 안 되는가

- 여러 사용자에게 공유되는 전역 캐시나 공통 데이터 저장소가 필요할 때
- DB에 영구 저장해야 하는 주문, 예측 결과, 사용자 로그를 임시 상태로만 들고 있으려 할 때
- key 이름과 row index 의미가 정리되지 않아 상태가 오히려 숨은 의존성이 될 때

## 실패 조건

- key를 초기화하지 않으면 첫 렌더링에서 `KeyError`가 난다.
- 검색 조건을 바꿨는데 이전 `in_oil`이나 `in_price`를 비우지 않으면 낡은 선택값으로 계산할 수 있다.
- DB row를 tuple index로 저장하면 API 컬럼 순서가 바뀔 때 계산이 조용히 틀어질 수 있다.
- 버튼 클릭 상태를 저장하지 않으면 rerun 직후 결과 영역이 닫힌다.

## 관련 개념

- [[Streamlit 기본 UI]]
- [[Python 딕셔너리]]
- [[Pandas DataFrame]]
- [[SKN26 1차 차량 운영비 프로젝트]]

## 먼저 확인할 질문

- 이 값은 rerun 뒤에도 남아야 하는가, 아니면 매번 새로 계산해야 하는가?
- 사용자가 검색 조건을 바꿀 때 함께 초기화해야 하는 상태는 무엇인가?
- 상태 key 이름만 보고 어떤 화면 단계의 값인지 알 수 있는가?
- 저장한 row의 컬럼 순서를 코드가 암묵적으로 의존하고 있지는 않은가?
