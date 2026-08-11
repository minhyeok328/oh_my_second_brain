---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'github-actions'
  - 'aws'
  - 'deployment'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.github.com/en/actions'
  - 'https://github.com/actions/checkout'
  - 'https://github.com/actions/setup-python'
  - 'https://github.com/aws-actions/configure-aws-credentials'
  - 'https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/Welcome.html'
source_quality: 'mixed'
verified: false
id: '20260530000000-8653'
---

# GitHub Actions EB 배포 치트시트

## 용도

GitHub Actions에서 Django 애플리케이션을 Elastic Beanstalk에 배포할 때 확인할 순서를 기록한다.

## 빠른 참조

1. 공식 `actions/checkout`으로 저장소를 체크아웃한다.
2. 공식 `actions/setup-python`으로 프로젝트가 요구하는 Python 버전을 준비한다.
3. 의존성 설치 후 `python manage.py check`와 프로젝트 테스트를 실행한다.
4. 공식 `aws-actions/configure-aws-credentials`로 짧은 수명의 AWS 자격 증명을 구성한다.
5. Elastic Beanstalk 애플리케이션 버전 생성과 환경 업데이트 절차는 AWS 공식 문서와 현재 AWS CLI 도움말을 기준으로 작성한다.

## 사용 전 확인

- Action의 `@vN`은 고정값으로 복사하지 말고 각 공식 저장소의 현재 릴리스와 변경 내역을 확인한다.
- 리전, 애플리케이션·환경 이름, S3 버킷, IAM 권한, 배포 패키지 제외 규칙을 저장소별로 확인한다.
- 장기 AWS 키를 워크플로에 직접 넣지 않는다. OIDC 또는 저장소 정책에 맞는 Secrets 구성을 확인한다.

## 검증 범위

- 2026-08-11: GitHub Actions 공식 문서, GitHub/AWS의 공식 Action 저장소, AWS Elastic Beanstalk 공식 문서에서 역할과 연결 순서를 확인했다.
- 실제 배포, IAM 권한, 패키징, Action 최신 major 버전은 검증하지 않았다. 배포 전 staging 환경에서 확인해야 한다.

## 관련 노트

- [[20 소스 노트/강의/React와 CI CD 강의|React와 CI CD 강의]]
- [[20 소스 노트/강의/DevOps와 배포 강의|DevOps와 배포 강의]]
- [[개인 Dev Rules]]
