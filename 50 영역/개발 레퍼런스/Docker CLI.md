---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'docker'
  - 'devops'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.docker.com/reference/cli/docker/'
source_quality: 'mixed'
verified: false
id: '20260530000000-b0d1'
---

# Docker CLI

## 용도

이미지와 컨테이너 상태를 확인하고 실행할 때 자주 쓰는 명령을 모은다.

## 빠른 참조

- `docker build -t <name> .`: 현재 디렉터리의 빌드 컨텍스트로 이미지 빌드
- `docker image ls`: 로컬 이미지 목록 확인
- `docker run --name <container> -p 8000:8000 <name>`: 포트를 연결해 새 컨테이너 실행
- `docker container ls`: 실행 중인 컨테이너 확인
- `docker logs <container>`: 컨테이너 로그 조회
- `docker stop <container>`: 실행 중인 컨테이너 중지

## 검증 범위

- 2026-08-11: Docker 공식 CLI 레퍼런스에서 명령과 주요 옵션을 확인했다.
- 이미지 이름, 포트, 볼륨, 네트워크, 플랫폼 옵션은 프로젝트마다 다르며 실제 이미지를 빌드하거나 실행하지 않았다. 사용 전 `docker <command> --help`와 프로젝트 설정을 확인한다.

## 관련 노트

- [[20 소스 노트/강의/DevOps와 배포 강의|DevOps와 배포 강의]]
- [[Docker Compose는 여러 컨테이너의 실행 계약을 한곳에 모은다]]
- [[50 영역/개발 레퍼런스/Docker Compose|Docker Compose 작업 참조]]
