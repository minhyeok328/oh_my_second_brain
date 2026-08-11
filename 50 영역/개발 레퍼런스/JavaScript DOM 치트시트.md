---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'javascript'
  - 'dom'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://developer.mozilla.org/en-US/docs/Web/API/Document/querySelector'
  - 'https://developer.mozilla.org/en-US/docs/Web/API/EventTarget/addEventListener'
  - 'https://developer.mozilla.org/en-US/docs/Web/API/Window/fetch'
source_quality: 'mixed'
verified: false
id: '20260530000000-ec65'
---

# JavaScript DOM 치트시트

## 용도

브라우저 DOM 선택, 내용 변경, 이벤트 연결과 네트워크 요청의 기본 형태를 빠르게 확인한다.

## 빠른 참조

- `const el = document.querySelector(selector)`: 일치하는 첫 요소 또는 `null` 반환
- `el.textContent = value`: 요소의 텍스트 내용 변경
- `el.classList.add(name)`: 요소의 클래스 목록에 이름 추가
- `el.addEventListener('click', handler)`: 클릭 이벤트 리스너 등록
- `const response = await fetch(url, options)`: HTTP 응답을 Promise로 받음

## 사용 전 확인

- `querySelector` 결과는 `null`일 수 있으므로 사용 전에 확인한다.
- `fetch`는 HTTP 오류 상태를 자동으로 예외 처리하지 않으므로 `response.ok`와 응답 형식을 확인한다.
- 이벤트 해제가 필요한 컴포넌트 수명에서는 같은 handler 참조로 `removeEventListener`를 호출할 수 있어야 한다.

## 검증 범위

- 2026-08-11: MDN의 각 Web API 레퍼런스에서 위 동작을 확인했다.
- 대상 브라우저 호환성, CORS, 자격 증명, 취소 처리와 프레임워크 수명주기는 확인하지 않았다.

## 관련 노트

- [[20 소스 노트/강의/웹 클라이언트 강의|웹 클라이언트 강의]]
- [[HTTP 요청은 타임아웃과 실패 처리를 기본값으로 가져야 한다]]
- [[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]]
