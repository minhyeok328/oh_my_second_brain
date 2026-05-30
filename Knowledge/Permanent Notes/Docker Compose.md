---
type: "permanent"
status: "wiki-expanded"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'docker'
  - 'devops'
source:
  - 'C:\lecture'
external:
  - 'https://docs.docker.com/compose/'
  - 'https://docs.docker.com/compose/compose-application-model/'
  - 'https://docs.docker.com/reference/compose-file/'
---

# Docker Compose

태그: #llm_wiki #docker #devops

## 한 줄 정의

Docker Compose는 여러 컨테이너 서비스, 네트워크, 볼륨, 환경 변수를 하나의 Compose 파일로 정의하고 함께 실행하는 도구다.

## 내 말로 다시 설명

실제 웹 앱은 Django 컨테이너 하나로 끝나지 않는다. DB, Redis, Nginx, worker 같은 여러 프로세스가 함께 움직인다. Compose는 이 묶음을 "로컬 또는 서버에서 재현 가능한 실행 단위"로 만든다.

## 핵심 개념

- service: 실행할 컨테이너 단위다.
- image/build: 이미지를 받을지 직접 빌드할지 정한다.
- ports: host와 container 포트를 연결한다.
- volumes: 데이터나 코드 경로를 컨테이너와 공유한다.
- networks: 서비스 간 통신 경계를 만든다.
- environment: 설정값과 secret 주입 경로다.

## 언제 쓰는가

- Django, DB, Nginx처럼 여러 컨테이너를 함께 실행할 때
- 로컬 개발 환경을 팀원과 동일하게 맞추고 싶을 때
- 배포 전 서비스 간 연결을 재현하고 테스트할 때

## 언제 쓰면 안 되는가

- 단일 컨테이너 실험이면 `docker run`이 충분한 경우
- 운영 오케스트레이션, auto scaling, rolling update가 필요한 경우
- secret과 volume 정책 없이 운영 설정을 그대로 담으려는 경우

## 자주 헷갈리는 점

- `depends_on`은 실행 순서를 보장할 뿐, DB 준비 완료를 보장하지 않는다.
- container 내부 포트와 host 노출 포트는 다르다.
- named volume은 컨테이너를 지워도 데이터가 남을 수 있다.

## 작은 예제

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:16
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

## 관련 개념

- [[Docker Container]]
- [[Docker Image]]
- [[Dockerfile]]
- [[Docker Network]]
- [[Docker Volume]]
- [[Nginx]]

## 확인 질문

- 서비스 간 이름 해석, 포트, volume 위치를 정확히 구분했는가?
- 운영 환경에서 secret과 persistent data를 어떻게 관리할 것인가?

## 외부 참조

- https://docs.docker.com/compose/
- https://docs.docker.com/compose/compose-application-model/
- https://docs.docker.com/reference/compose-file/
