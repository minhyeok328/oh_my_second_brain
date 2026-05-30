---
type: "reference"
status: "reference"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'django'
  - 'devops'
  - 'reference'
source:
  - 'C:\lecture'
---

# WSGI ASGI 배포 명령어

태그: #django #devops #reference #llm_wiki

## 용도

Django 운영 서버 실행 명령을 모은다.

## 빠른 참조

- `gunicorn project.wsgi:application`: WSGI 실행
- `uvicorn project.asgi:application`: ASGI 실행
- `nginx -t`: Nginx 설정 검사
- `systemctl restart nginx`: Nginx 재시작

## 관련 노트

- [[WSGI]]
- [[ASGI]]
- [[Nginx]]
