---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'python'
  - 'conda'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.conda.io/projects/conda/en/stable/commands/env/create.html'
  - 'https://docs.conda.io/projects/conda/en/latest/commands/env/export.html'
  - 'https://docs.conda.io/projects/conda/en/stable/commands/remove.html'
source_quality: 'mixed'
verified: false
id: '20260530000000-a410'
---

# Conda 환경 설정

## 용도

프로젝트별 Conda 환경을 만들고 내보내고 제거할 때 빠르게 확인하는 작업 노트다.

## 빠른 참조

- `conda env create -f environment.yml`: 환경 정의 파일로 환경 생성
- `conda activate <env>`: 이름으로 환경 활성화
- `conda export --from-history > environment.yml`: 직접 요청한 패키지 중심의 환경 정의 내보내기
- `conda remove -n <env> --all`: 이름으로 지정한 환경과 그 안의 패키지 제거

## 검증 범위

- 2026-08-11: Conda 공식 명령 문서에서 위 명령의 존재와 기본 용도를 확인했다.
- 로컬 셸에서 실제 생성·활성화·삭제는 실행하지 않았다. Conda 버전, 설치된 환경 포맷 플러그인, 운영체제에 따른 활성화 방식은 사용 전 다시 확인한다.
- 환경 재현성이 중요하면 `environment.yml`의 채널·버전 범위와 `conda export --help`의 현재 출력 형식을 함께 확인한다.

## 관련 노트

- [[20 소스 노트/강의/Python 기초와 Streamlit 강의|Python 기초와 Streamlit 강의]]
- [[20 소스 노트/강의/딥러닝 기초 강의|딥러닝 기초 강의]]
