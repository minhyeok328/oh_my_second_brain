---
type: "reference"
status: "reference"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'github'
  - 'aws'
  - 'reference'
source:
  - 'C:\lecture'
---

# GitHub Actions EB 배포 치트시트

태그: #github #aws #reference #llm_wiki

## 용도

GitHub Actions에서 Elastic Beanstalk로 배포할 때 필요한 핵심 항목이다.

## 빠른 참조

- `actions/checkout@v4`: 코드 체크아웃
- `actions/setup-python@v5`: Python 런타임 준비
- `python manage.py check`: Django 설정 검증
- `zip -r deploy.zip .`: 배포 패키지 생성
- `aws-actions/configure-aws-credentials@v4`: AWS 인증 설정
- `beanstalk-deploy@v22`: Elastic Beanstalk 배포

## 관련 노트

- [[GitHub Actions Workflow]]
- [[AWS Elastic Beanstalk]]
- [[GitHub Actions Secrets]]
