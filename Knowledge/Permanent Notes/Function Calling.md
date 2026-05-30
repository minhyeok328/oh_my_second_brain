---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'llm'
  - 'tools'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_3rd_3rd\3rd_project'
  - 'C:\MinHyeok\skn26_4th_1st\4th_project'
---

# Function Calling

태그: #llm_wiki #llm #tools

## 한 줄 정의

Function Calling은 LLM이 자연어를 정해진 함수명과 인자 schema에 맞는 구조화 데이터로 바꾸고, 실제 실행은 코드가 담당하게 하는 패턴이다.

## 내 말로 다시 설명

모델에게 "검색해줘"라고 말하게 하는 것이 아니라, `{restaurant: "유태우스시", menu: "회전초밥"}`처럼 다음 코드가 안전하게 사용할 수 있는 인자를 만들게 하는 방식이다. 실행 권한은 모델이 아니라 애플리케이션 코드가 가진다.

## 언제 쓰는가

- 자연어 질문에서 DB 검색 조건을 추출할 때
- route별로 다른 slot schema가 필요한 경우
- LLM 출력이 JSON처럼 downstream 코드의 입력이 되는 경우

## 언제 쓰면 안 되는가

- schema가 너무 느슨해 자유 텍스트와 다르지 않은 경우
- 모델이 만든 인자를 검증하지 않고 바로 DB/API에 넘기는 경우
- 단순 UI filter처럼 사용자가 이미 구조화된 값을 고른 경우

## 프로젝트 예시

[[SKN26 3차 프로젝트 - PICKLE RAG 챗봇]]의 `slot_extractor.py`는 embedding 경로와 fixed 경로에 다른 schema를 두고, LangGraph node에서 `.invoke()`로 슬롯을 추출한다. [[SKN26 4차 프로젝트 - LG Home]]은 Pydantic structured output으로 제품군, 후속 질문, 조건 슬롯을 추출한다.

## 실패 조건

- route가 틀리면 올바른 function/schema도 선택되지 않는다.
- 빈 문자열과 누락 값의 의미가 정리되지 않으면 검색 조건이 과도하게 넓어진다.
- schema와 DB 필드 이름이 어긋나면 검색 결과가 없어도 원인을 찾기 어렵다.

## 관련 개념

- [[OpenAI API]]
- [[Prompt Engineering]]
- [[LangGraph Node와 Edge]]
- [[Django QuerySet]]

## 먼저 확인할 질문

- 이 function의 인자는 어떤 코드가 소비하는가?
- 각 인자 값이 비었을 때 무시, fallback, 에러 중 무엇으로 처리하는가?
