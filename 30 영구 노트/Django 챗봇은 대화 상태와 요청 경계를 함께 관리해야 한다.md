---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'django'
  - 'chatbot'
  - 'state'
aliases:
  - 'Django Chatbot'
sources:
  - 'https://docs.djangoproject.com/en/6.0/topics/http/sessions/'
  - 'https://docs.langchain.com/oss/python/langgraph/persistence'
  - 'C:\MinHyeok\skn26_projects\4th_project\api\views.py'
  - 'C:\MinHyeok\skn26_projects\4th_project\chats\models.py'
source_quality: 'mixed'
verified: true
id: '20260530000000-8a51'
---

# Django 챗봇은 대화 상태와 요청 경계를 함께 관리해야 한다

## 주장

여러 턴을 잇는 Django 챗봇에서는 HTTP 요청을 처리하는 사용자·권한 경계와 대화 상태를 이어 주는 식별자를 같은 흐름에서 관리해야 한다. Django 세션은 방문자별 데이터를 구분하고 LangGraph 체크포인터는 `thread_id`별 상태를 저장하므로, 요청의 사용자와 대화방을 확인한 뒤에만 [[LangGraph 상태는 노드 사이의 데이터 계약이다]]를 불러오고 갱신해야 대화가 섞이지 않는다.

## 연결

이 요청 경계는 [[Django JSON API는 화면과 서버 책임을 분리한다]]가 입력 오류와 인증 실패를 상태 코드로 표현하는 자리다. 검색 근거를 쓰는 챗봇이라면 그 안쪽 흐름은 [[RAG의 성능은 검색 단계의 품질에서 시작된다]]와 연결된다. 프로젝트 코드에서 확인한 적용을 내 관점으로 정리하면, [[SKN26 4차 LG Home AI 가전 상담]]은 로그인 사용자의 대화방만 선택하고 모델의 `agent_state`에 후속 대화 상태를 보관한다.

## 한계와 반례

매 요청이 독립적인 단일 턴 도구라면 대화 상태를 영속화할 이유가 없다. 반대로 전체 대화 기록을 제한 없이 저장하면 개인정보 범위와 저장 비용이 커지므로 보존 기간, 삭제 정책, 상태 축약을 별도로 설계해야 한다.

## 확인한 근거

- 2026-08-11: Django 공식 Sessions 문서에서 방문자별 상태 저장과 세션 ID의 역할을 확인했다.
- 2026-08-11: LangGraph 공식 Persistence 문서에서 thread별 체크포인트가 연속 상호작용의 상태를 보존하는 방식을 확인했다.
- 프로젝트 코드 확인(개인 해석): 승인된 `4th_project/api/views.py`와 `chats/models.py`에서 로그인 사용자 소유 대화방 확인, 메시지와 `agent_state` 저장을 확인했다.
