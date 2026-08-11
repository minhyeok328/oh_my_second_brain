---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'django'
  - 'deployment'
  - 'wsgi'
  - 'asgi'
aliases: []
sources:
  - 'https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/gunicorn/'
  - 'https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/uvicorn/'
source_quality: 'mixed'
verified: false
id: '20260530000000-603f'
---

# WSGI ASGI 배포 명령어

## 용도

Django 애플리케이션을 WSGI 또는 ASGI 서버로 시작할 때 모듈 경로 형태를 확인한다.

## 빠른 참조

- `python -m gunicorn myproject.wsgi`: 일반적인 Django WSGI 애플리케이션 시작
- `python -m uvicorn myproject.asgi:application`: 일반적인 Django ASGI 애플리케이션 시작
- 개발 중 Uvicorn 자동 재시작은 `--reload`를 쓸 수 있지만 운영 설정으로 그대로 옮기지 않는다.

## 사용 전 확인

- `myproject`를 실제 설정 패키지 이름으로 바꾸고 `manage.py`가 있는 디렉터리에서 모듈 import를 확인한다.
- worker 수, timeout, proxy header, TLS, 정적 파일, process manager와 graceful shutdown은 배포 환경별로 결정한다.
- `nginx`와 `systemctl` 명령은 호스트 권한과 서비스 이름에 영향을 주므로 이 노트에서 고정 명령으로 제공하지 않는다.

## 검증 범위

- 2026-08-11: Django 5.2 공식 Gunicorn·Uvicorn 배포 문서에서 위 기본 실행 형태를 확인했다.
- 실제 운영 서버, reverse proxy, 서비스 관리자와 프로젝트 버전은 검증하지 않았다. 배포 전 Django deployment checklist와 서버 공식 문서를 확인한다.

## 관련 노트

- [[20 소스 노트/강의/Django 웹 서버 강의|Django 웹 서버 강의]]
- [[20 소스 노트/강의/DevOps와 배포 강의|DevOps와 배포 강의]]
- [[Django 챗봇은 대화 상태와 요청 경계를 함께 관리해야 한다]]
