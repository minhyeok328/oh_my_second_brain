---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'docker'
  - 'devops'
  - 'operations'
aliases:
  - 'Docker Compose'
sources:
  - 'https://docs.docker.com/compose/intro/compose-application-model/'
  - 'https://docs.docker.com/compose/'
  - 'C:\MinHyeok\lecture\12_devops_workspace'
source_quality: 'mixed'
verified: true
id: '20260530000000-6aaa'
---

# Docker Compose는 여러 컨테이너의 실행 계약을 한곳에 모은다

## 주장

Docker Compose는 한 애플리케이션을 이루는 서비스, 네트워크, 볼륨과 실행 설정을 Compose 파일이라는 하나의 선언에 모으고 CLI가 그 선언을 실행하게 한다. 그래서 [[MLflow는 실험 조건과 결과를 함께 추적한다]] 서버와 [[Streamlit UI는 위에서 아래로 재실행되는 흐름을 따른다]] 앱처럼 함께 움직여야 하는 여러 컨테이너의 조합을 반복 가능한 실행 계약으로 다룰 수 있다.

## 연결

[[DevOps와 배포 강의]]에서 확인한 Docker·Compose 실습은 이 계약을 로컬에서 실행하는 맥락을 제공한다. 내 해석으로는 명령 순서를 README에만 적는 것보다 Compose 파일에 서비스 관계를 남길 때 실행 구성이 검토 가능한 지식이 된다.

## 한계와 반례

Compose 파일은 애플리케이션의 실행 구성을 선언하지만 서비스가 실제 요청을 받을 준비가 됐는지, 비밀 값이 안전한지, 운영 환경에서 확장과 롤백이 가능한지까지 자동 보장하지 않는다. 단일 프로세스만 필요한 작업에는 이 계약의 유지 비용이 더 클 수 있다.

## 확인한 근거

- 2026-08-11: Docker 공식 Compose 애플리케이션 모델에서 서비스·네트워크·볼륨·설정·비밀을 Compose 파일로 정의하고 `docker compose up`으로 실행하는 범위를 확인했다.
- 2026-08-11: Docker 공식 Compose 개요에서 하나의 YAML 파일이 여러 컨테이너 애플리케이션의 서비스와 수명 주기를 관리하는 기준임을 확인했다.
- 강의 자료 확인(개인 해석): 승인된 `12_devops_workspace`에는 Dockerfile과 Compose 실습이 있지만 상태 확인·비밀 관리·롤백은 근거 공백으로 남아 있음을 확인했다.
