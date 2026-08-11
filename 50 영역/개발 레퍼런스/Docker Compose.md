---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'docker'
  - 'compose'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.docker.com/reference/cli/docker/compose/'
  - 'https://docs.docker.com/reference/compose-file/'
source_quality: 'mixed'
verified: false
id: '20260530000000-54e7'
---

# Docker Compose

## 용도

Compose 파일에 정의된 여러 서비스를 함께 실행하고 상태를 확인한다.

## 빠른 참조

- `docker compose config`: Compose 파일을 해석해 유효한 구성인지 확인
- `docker compose up`: 서비스를 생성하고 시작
- `docker compose up -d`: 서비스를 분리 모드로 시작
- `docker compose ps`: 프로젝트의 서비스 컨테이너 상태 확인
- `docker compose logs -f`: 서비스 로그를 이어서 확인
- `docker compose down`: 서비스 컨테이너와 기본 네트워크 정리

## 검증 범위

- 2026-08-11: Docker 공식 Compose CLI와 Compose 파일 레퍼런스에서 위 명령을 확인했다.
- 프로젝트의 Compose 파일, 프로파일, 볼륨 삭제 옵션, healthcheck와 실제 readiness는 확인하지 않았다. 특히 데이터 볼륨에 영향을 주는 옵션은 `docker compose down --help`를 확인한 뒤 사용한다.

## 관련 노트

- [[Docker Compose는 여러 컨테이너의 실행 계약을 한곳에 모은다]]
- [[20 소스 노트/강의/DevOps와 배포 강의|DevOps와 배포 강의]]
- [[50 영역/개발 레퍼런스/Docker CLI|Docker CLI 작업 참조]]
