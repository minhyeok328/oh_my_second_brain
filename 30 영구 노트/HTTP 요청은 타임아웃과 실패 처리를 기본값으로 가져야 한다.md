---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'python'
  - 'http'
  - 'reliability'
aliases:
  - 'Requests'
sources:
  - 'https://requests.readthedocs.io/en/latest/user/quickstart/#timeouts'
  - 'https://requests.readthedocs.io/en/latest/user/quickstart/#errors-and-exceptions'
  - 'C:\MinHyeok\skn26_projects\1st_project\API_Side\CarOil.py'
  - 'C:\MinHyeok\skn26_projects\1st_project\API_Side\CarPrice.py'
source_quality: 'mixed'
verified: true
id: '20260530000000-3163'
---

# HTTP 요청은 타임아웃과 실패 처리를 기본값으로 가져야 한다

## 주장

Python Requests 호출은 응답 본문보다 먼저 대기 한도와 실패 분류를 정해야 한다. `timeout`을 생략하면 요청이 끝없이 기다릴 수 있고, JSON 파싱 성공도 HTTP 성공을 뜻하지 않으므로 `raise_for_status()` 또는 기대 상태 코드 검사와 `RequestException` 계열 처리를 호출 경계의 기본값으로 둬야 한다.

## 연결

이 규칙은 [[FastAPI는 타입 선언을 요청 검증과 문서화에 재사용한다]] 같은 외부 API를 소비할 때 서버의 입력 검증과 짝을 이룬다. [[SKN26 1차 차량 운영비 프로젝트]] 코드를 다시 확인해 보니 API와 HTML 요청 모두 타임아웃이 없었다. 이를 프로젝트 경험에서 얻은 개인 해석으로 기록하면, 정상 응답 파싱보다 먼저 호출 실패가 화면과 데이터 수집 흐름을 무기한 붙잡지 않게 해야 한다.

## 한계와 반례

Requests의 `timeout`은 전체 다운로드의 절대 마감 시간이 아니라 소켓에서 일정 시간 바이트를 받지 못할 때 적용되는 값이다. 재시도도 모든 실패에 자동으로 붙이면 안 되며, 비멱등 요청과 사용량 제한에는 별도 backoff·중복 방지 정책이 필요하다.

## 확인한 근거

- 2026-08-11: Requests 공식 Quickstart에서 명시적 timeout이 없으면 요청이 시간 제한 없이 대기하며, timeout·연결·HTTP 오류가 서로 다른 예외로 표현되는 범위를 확인했다.
- 2026-08-11: 같은 공식 문서에서 JSON 디코딩 성공과 HTTP 성공은 별개이고 `raise_for_status()`로 실패 상태를 확인해야 함을 확인했다.
- 프로젝트 코드 확인(개인 해석): 승인된 `1st_project/API_Side/CarOil.py`와 `CarPrice.py`의 실제 호출에 timeout이 없고 실패 처리가 부분적인 상태를 확인했다.
