---
type: "permanent"
status: "wiki-standardized"
created: "2026-05-30"
updated: "2026-05-30"
reviewed: "2026-05-30"
tags:
  - 'llm_wiki'
  - 'github'
  - 'cicd'
  - 'devops'
source:
  - 'C:\lecture'
---

# GitHub Actions Workflow

태그: #github #cicd #devops #llm_wiki

## 한 줄 정의

GitHub Actions에서 트리거, job, step을 선언하는 YAML 자동화 단위다.

## 왜 중요한가

워크플로우 구조를 이해하면 CI와 CD를 읽고 수정할 수 있다.

## 핵심 개념

- `on`은 실행 조건이다.
- `jobs`는 실행 작업 묶음이다.
- `steps`는 순차 실행되는 세부 명령이다.

## 예제

```yaml
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps: []
```

## 실무 활용

테스트 자동화, Docker 이미지 빌드, Elastic Beanstalk 배포에 사용한다.

## 관련 개념

- [[GitHub Actions]]
- [[GitHub Actions Secrets]]
- [[AWS Elastic Beanstalk]]

자료 힌트: 13_react-cicd_workspace/03_gha_cicd/sample_app/.github/workflows/deploy-eb.yml

## 내 말로 다시 설명

GitHub Actions Workflow은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- [[GitHub Actions]], [[GitHub Actions Secrets]], [[AWS Elastic Beanstalk]]와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- GitHub Actions Workflow을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
