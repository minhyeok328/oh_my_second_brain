---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'react'
  - 'api'
  - 'frontend'
source:
  - 'C:\lecture'
external:
  - 'https://react.dev/reference/react/useEffect'
  - 'https://react.dev/learn/you-might-not-need-an-effect'
---

# React API Fetch

태그: #llm_wiki #react #api #frontend

## 한 줄 정의

React API Fetch는 컴포넌트나 라우트가 서버 API에서 데이터를 받아 화면 상태와 동기화하는 프론트엔드 데이터 로딩 패턴이다.

## 내 말로 다시 설명

React에서 API 호출은 단순히 `fetch()`를 쓰는 문제가 아니다. 언제 요청할지, 로딩과 에러를 어떻게 보여줄지, 이전 요청이 늦게 도착했을 때 어떻게 막을지, 컴포넌트가 사라질 때 정리할지가 함께 따라온다.

## 기본 흐름

- 요청에 필요한 입력 상태를 정한다.
- loading, data, error 상태를 분리한다.
- 요청 성공 시 data를 갱신한다.
- 실패 시 사용자에게 보여줄 error를 저장한다.
- 컴포넌트 unmount나 입력 변경 시 stale response를 막는다.

## 언제 쓰는가

- 서버 데이터가 화면 렌더링에 필요할 때
- 사용자의 검색 조건, 페이지, 필터에 따라 API를 다시 호출해야 할 때
- 작은 앱에서 별도 data fetching 라이브러리 없이 처리해도 충분할 때

## 언제 쓰면 안 되는가

- 서버 상태 캐싱, 중복 요청 제거, pagination, mutation invalidation이 복잡한 경우
- 라우터 loader나 query library가 이미 데이터 흐름을 맡고 있는 경우
- 렌더링 중 계산 가능한 값을 굳이 API 상태로 분리하는 경우

## 자주 헷갈리는 점

- `useEffect` 안 fetch는 race condition을 만들 수 있다.
- HTTP 에러와 네트워크 에러를 구분해야 한다.
- API 응답 shape가 바뀌면 화면 상태와 타입도 같이 깨진다.

## 작은 예제

```jsx
useEffect(() => {
  let ignore = false;
  setLoading(true);

  fetch(`/api/posts?q=${query}`)
    .then((res) => {
      if (!res.ok) throw new Error("Request failed");
      return res.json();
    })
    .then((data) => {
      if (!ignore) setPosts(data);
    })
    .catch((error) => {
      if (!ignore) setError(error.message);
    })
    .finally(() => {
      if (!ignore) setLoading(false);
    });

  return () => {
    ignore = true;
  };
}, [query]);
```

## 관련 개념

- [[useEffect]]
- [[React State]]
- [[JavaScript 비동기]]
- [[Requests]]
- [[Django View]]

## 확인 질문

- 이 데이터는 서버 상태인가, 컴포넌트 내부 상태인가?
- 요청이 늦게 도착했을 때 이전 화면을 덮어쓰지 않는가?

## 외부 참조

- https://react.dev/reference/react/useEffect
- https://react.dev/learn/you-might-not-need-an-effect
