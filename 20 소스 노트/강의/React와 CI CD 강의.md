---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'lecture'
  - 'react'
  - 'cicd'
aliases: []
sources:
  - 'C:\MinHyeok\lecture\10_web_client_workspace'
  - 'C:\MinHyeok\lecture\12_devops_workspace'
source_path: 'C:\MinHyeok\lecture\10_web_client_workspace'
source_quality: 'primary'
verified: true
id: '20260530000000-4004'
---

# React와 CI CD 강의

## 출처

- 원본 경로: `C:\MinHyeok\lecture\10_web_client_workspace`
- 함께 확인한 경로: `C:\MinHyeok\lecture\12_devops_workspace`
- 확인일: 2026-08-11

## 핵심 내용

- 관찰: 웹 클라이언트 경로는 HTML, CSS, JavaScript core·ES6·browser API 예제로 구성되어 있으며 React 컴포넌트, Router, Hook 소스는 확인되지 않았다.
- 관찰: DevOps 경로는 AWS EC2, Docker·Compose, WSGI·ASGI와 Nginx 실습으로 구성되어 있으며 GitHub Actions 등 CI 워크플로 파일은 확인되지 않았다.
- 관찰: 두 승인 경로 모두에서 Elastic Beanstalk 강의 파일도 확인되지 않았다.
- 관찰: 따라서 기존 노트의 React 컴포넌트·Hook, 디자인 패턴, GitHub Actions·Elastic Beanstalk 자동 배포 요약은 현재 승인된 로컬 근거로 뒷받침되지 않는다.

## 내 해석과 의문

- 해석: 이 노트는 React와 CI/CD를 설명하는 완성된 출처가 아니라, 브라우저 기초·컨테이너 배포 자료와 누락된 후속 강의 사이의 경계를 기록한다.
- 질문: React와 CI/CD 원본이 다른 강의 디렉터리나 프로젝트 저장소에 있는지 확인해야 한다.
- 질문: 후속 영구 노트는 React 공식 문서와 실제 CI 설정을 별도 1차 자료로 확보한 뒤 검증한다.

## 분리한 영구 노트

- [[React SPA]] · [[React API Fetch]] · [[useEffect]] — 이 강의 경로만으로는 승격 근거가 부족함
- [[00 인박스/승격 대기/영구 노트/Docker Compose|Docker Compose]] — 승인된 DevOps 경로에서 직접 확인한 인접 개념
- CI/CD 파이프라인 — 실제 워크플로 파일을 찾은 뒤 후속 영구 노트 후보로 검토
