---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'aws'
  - 'devops'
  - 'cicd'
source:
  - 'C:\lecture'
---

# AWS Elastic Beanstalk

태그: #aws #devops #cicd #llm_wiki

## 한 줄 정의

애플리케이션 코드를 업로드하면 EC2, 로드밸런서, 배포, 헬스체크를 관리해 주는 AWS PaaS 서비스다.

## 왜 중요한가

인프라 세부 설정을 모두 직접 구성하지 않고도 Django 같은 웹 앱을 빠르게 배포할 수 있다.

## 핵심 개념

- application은 앱의 논리적 묶음이다.
- environment는 실행 중인 배포 환경이다.
- 버전 zip을 업로드해 환경에 배포한다.

## 예제

```bash
eb init
eb use <env>
eb deploy
```

## 실무 활용

Django 샘플 앱 배포, GitHub Actions 기반 자동 배포, AWS 배포 흐름 학습에 사용한다.

## 관련 개념

- [[EB CLI]]
- [[Procfile]]
- [[AWS IAM Role]]

자료 힌트: 13_react-cicd_workspace/03_gha_cicd

## 내 말로 다시 설명

AWS Elastic Beanstalk은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[EB CLI]], [[Procfile]], [[AWS IAM Role]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- AWS Elastic Beanstalk을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
