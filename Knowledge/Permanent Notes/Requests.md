---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'python'
  - 'api'
  - 'data_collection'
source:
  - 'C:\lecture'
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders\API_Side\CarOil.py'
  - 'C:\MinHyeok\skn26_1st_2nd\joy-riders\API_Side\CarPrice.py'
---

# Requests

태그: #python #api #data_collection #llm_wiki

## 한 줄 정의

Requests는 Python에서 HTTP 요청을 보내고 응답의 status, header, body를 다루는 대표적인 HTTP client 라이브러리다.

## 왜 중요한가

외부 API나 웹 페이지에서 데이터를 가져오는 프로젝트는 네트워크 실패, 응답 구조 변경, 인증 키 누락, HTML 구조 변경을 항상 마주친다. Requests를 쓸 때는 "요청을 보냈다"보다 "실패를 구분하고 안전하게 파싱했다"가 더 중요하다.

## 핵심 개념

- `requests.get()`은 HTTP GET 요청을 보낸다.
- `params`는 query string을 안전하게 구성할 때 사용한다.
- `headers`는 인증 키나 API 요구 header를 넘길 때 사용한다.
- `timeout`을 지정하지 않으면 응답 지연 때 앱 전체가 멈출 수 있다.
- `status_code`, `raise_for_status()`, 예외 처리로 네트워크 실패를 분리한다.
- JSON, HTML, XML은 응답 형식에 맞는 parser로 처리한다.

## 프로젝트 예시

[[SKN26 1차 프로젝트 - 차량 TCO]]의 `API_Side\CarOil.py`는 공공 API에 차량 모델명을 query parameter로 보내고 JSON 응답을 파싱한다.

- `headers`: `CAR_ID` 값을 전달한다.
- `params`: `pageNo`, `numOfRows`, `q2` 모델명 검색어를 전달한다.
- `response.status_code == 200`일 때만 JSON body를 읽는다.
- 응답 구조에 `response.body.items.item`이 없으면 빈 리스트를 반환한다.

`API_Side\CarPrice.py`는 `requests.get(url).text`로 HTML을 가져와 BeautifulSoup으로 차량 가격 후보를 파싱한다. 이 방식은 빠르게 만들 수 있지만 timeout, status check, HTML 구조 변경 대응이 없으면 실패 원인을 찾기 어렵다.

## 언제 쓰는가

- REST API에서 JSON 데이터를 가져올 때
- 검색어를 query parameter로 넘겨 외부 데이터를 수집할 때
- 간단한 HTML 페이지를 가져와 parser에 넘길 때
- 외부 서비스 응답을 DB 적재 전에 검증해야 할 때

## 언제 쓰면 안 되는가

- JavaScript 렌더링 후에야 데이터가 생기는 페이지를 정적 요청만으로 수집하려 할 때
- 장시간 대량 수집에서 retry, rate limit, backoff 없이 단순 loop로 호출할 때
- 인증 키나 개인정보를 URL 문자열에 직접 노출해야 하는 구조일 때

## 실패 조건

- timeout이 없으면 외부 API 지연이 Streamlit 화면 전체를 붙잡을 수 있다.
- status code만 보고 JSON 구조가 맞다고 가정하면 `KeyError`나 `TypeError`가 난다.
- HTML selector가 바뀌면 `select_one(...).text`에서 `NoneType` 오류가 난다.
- API key가 없을 때 빈 결과와 인증 실패를 구분하지 않으면 디버깅이 길어진다.
- `response.status_code`가 실패인데도 결과 변수를 반환하려 하면 초기화되지 않은 값 문제가 생길 수 있다.

## 관련 개념

- [[OpenAPI]]
- [[정적 웹 스크래핑]]
- [[Python 예외 처리]]
- [[MySQL Connector Python]]
- [[SKN26 1차 프로젝트 - 차량 TCO]]

## 먼저 확인할 질문

- 이 요청은 timeout, status check, 예외 처리를 갖고 있는가?
- 실패했을 때 빈 데이터, 인증 실패, 네트워크 오류를 구분할 수 있는가?
- API 응답 구조나 HTML selector 변경에 취약하지 않은가?
- 외부 데이터를 DB에 넣기 전에 필수 필드 검증을 했는가?
