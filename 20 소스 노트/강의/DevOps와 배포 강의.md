---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'lecture'
  - 'devops'
aliases: []
sources:
  - 'C:\MinHyeok\lecture\12_devops_workspace'
source_path: 'C:\MinHyeok\lecture\12_devops_workspace'
source_quality: 'primary'
verified: true
id: '20260530000000-4c24'
---

# DevOps와 배포 강의

## 출처

- 원본 경로: `C:\MinHyeok\lecture\12_devops_workspace`
- 확인일: 2026-08-11

## 핵심 내용

- 관찰: `01_aws\about_aws.md`는 EC2 인스턴스·보안 그룹·SSH 접속, Nginx 설치, Django 실행과 Nginx 리버스 프록시 설정을 한 실습 흐름으로 기록한다.
- 관찰: `02_docker\about_dockeer.md`와 `docker-handout\mds`는 이미지·컨테이너, 실행·중지·삭제, 포트·환경 변수·볼륨, Dockerfile과 이미지 빌드를 다룬다.
- 관찰: `02_docker\_01_django_image\Dockerfile`은 Python 3.12 기반 Django 이미지를 만들고 개발 서버를 컨테이너의 8000 포트에서 실행한다.
- 관찰: `02_docker\02_docker_compose`는 Django와 Nginx 서비스를 Compose 네트워크로 묶고, Nginx가 서비스 이름 `django`로 요청을 전달하도록 구성한다.
- 관찰: `03_wsgi_asgi`는 Gunicorn 기반 WSGI와 Uvicorn 기반 ASGI 컨테이너를 만들고 동기·비동기 요청 동시성 비교 실험을 안내한다.

## 내 해석과 의문

- 해석: 배포를 단일 명령이 아니라 인프라, 실행 이미지, 프로세스 서버, 프록시와 네트워크 경계의 조합으로 읽을 수 있다.
- 질문: Django 개발 서버를 실행하는 이미지 예제와 Gunicorn·Uvicorn 예제의 목적 차이를 배포 체크리스트에 어떻게 드러낼 것인가?
- 질문: 이미지 태그, 비밀 값, 상태 확인, 롤백과 관측 가능성은 이 실습 범위 밖에서 어떤 근거로 보강해야 하는가?

## 분리한 영구 노트

- [[00 인박스/승격 대기/영구 노트/Docker Compose|Docker Compose]]
- Docker 이미지와 컨테이너의 수명 주기 — 후속 영구 노트 후보
- Nginx 리버스 프록시 경계 — 후속 영구 노트 후보
- WSGI와 ASGI의 실행 모델 — 후속 영구 노트 후보
