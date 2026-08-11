---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'lecture'
  - 'django'
aliases: []
sources:
  - 'C:\MinHyeok\lecture\11_web_server_workspace'
source_path: 'C:\MinHyeok\lecture\11_web_server_workspace'
source_quality: 'primary'
verified: true
id: '20260530000000-42d0'
---

# Django 웹 서버 강의

## 출처

- 원본 경로: `C:\MinHyeok\lecture\11_web_server_workspace`
- 확인일: 2026-08-11

## 핵심 내용

- 관찰: `_01_django_project`와 `_02_django_template`은 프로젝트·앱 생성, URL과 View 연결, 템플릿 변수·필터·태그·레이아웃·정적 파일을 실습한다.
- 관찰: `_03_django_orm`은 모델과 마이그레이션, Django shell 조회 코드를 게시글·상품 예제로 구성한다.
- 관찰: `_04_qna`는 질문·답변 모델, QuerySet 조회, ModelForm 기반 생성·수정, 로그인·권한 검사와 회원가입 트랜잭션을 하나의 Q&A 앱으로 연결한다.
- 관찰: `_05_django_session\app\views.py`는 세션 값의 생성·수정·삭제와 쿠키 속성을 요청·응답 처리로 보여 준다.
- 관찰: `_06_chatbot`은 JSON 응답 엔드포인트, 세션 ID, 데이터베이스 기반 대화 기록과 LangChain 메시지 기록 래퍼를 결합한다.

## 내 해석과 의문

- 해석: URL, View, Template, Model을 별개 정의로 외우기보다 하나의 요청이 각 경계를 지나는 과정으로 복습하기 좋다.
- 질문: 일부 챗봇 엔드포인트가 CSRF 검사를 비활성화한 실습 선택은 운영 환경에서 어떤 인증·출처 검증으로 대체해야 하는가?
- 질문: QuerySet 평가 시점과 쿼리 수를 실제 로그로 확인하면 Q&A 목록·상세 화면의 병목이 어떻게 달라지는가?

## 분리한 영구 노트

- [[Django ORM Model]] · [[Django QuerySet]]
- [[Django CSRF]] · [[Django JSON API]]
- [[Django Chatbot]]
- Django 세션과 인증 경계 — 후속 영구 노트 후보
