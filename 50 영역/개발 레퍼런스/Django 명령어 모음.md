---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'django'
  - 'python'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.djangoproject.com/en/5.2/ref/django-admin/'
source_quality: 'mixed'
verified: false
id: '20260530000000-a316'
---

# Django 명령어 모음

## 용도

Django 프로젝트에서 반복 사용하는 관리 명령을 빠르게 확인한다.

## 빠른 참조

- `django-admin startproject config`: 새 프로젝트 뼈대 생성
- `python manage.py startapp app`: 현재 프로젝트에 앱 뼈대 생성
- `python manage.py makemigrations`: 모델 변경을 바탕으로 마이그레이션 생성
- `python manage.py migrate`: 설정된 데이터베이스에 마이그레이션 적용
- `python manage.py check`: 프로젝트의 일반적인 설정 문제 점검
- `python manage.py runserver`: 개발 서버 실행

## 검증 범위

- 2026-08-11: Django 5.2 공식 `django-admin` 문서에서 위 관리 명령의 용도를 확인했다.
- 프로젝트별 Django 버전, 설정 모듈, 앱 이름, 데이터베이스 상태는 확인하지 않았다. 실행 전 `python -m django --version`과 `python manage.py help <command>`를 확인한다.
- `runserver`는 개발용이다. 운영 배포 명령은 [[50 영역/개발 레퍼런스/WSGI ASGI 배포 명령어|WSGI ASGI 배포 명령어]]에서 따로 확인한다.

## 관련 노트

- [[20 소스 노트/강의/Django 웹 서버 강의|Django 웹 서버 강의]]
- [[Django ORM 모델은 데이터 구조와 제약을 코드로 표현한다]]
- [[QuerySet은 평가 시점을 늦춰 쿼리 조합을 가능하게 한다]]
