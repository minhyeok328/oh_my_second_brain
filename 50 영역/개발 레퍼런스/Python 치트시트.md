---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'python'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://docs.python.org/3/tutorial/'
  - 'https://docs.python.org/3/library/venv.html'
  - 'https://pip.pypa.io/en/stable/cli/pip_install/'
source_quality: 'mixed'
verified: false
id: '20260530000000-ee34'
---

# Python 치트시트

## 용도

스크립트 실행, 가상환경, 패키지 설치와 UTF-8 파일 읽기의 기본 형태를 빠르게 확인한다.

## 빠른 참조

- `python script.py`: 선택된 Python 인터프리터로 스크립트 실행
- `python -m venv .venv`: 현재 인터프리터를 기준으로 가상환경 생성
- `python -m pip install <package>`: 현재 인터프리터 환경에 패키지 설치
- `python -m pip install -r requirements.txt`: 요구사항 파일에 적힌 패키지 설치
- `with open(path, encoding='utf-8') as file:`: UTF-8 텍스트 파일을 context manager로 열기

## 검증 범위

- 2026-08-11: Python 공식 Tutorial·`venv` 문서와 PyPA의 pip 공식 문서에서 위 사용 형태를 확인했다.
- 운영체제별 가상환경 활성화 명령, 프로젝트의 Python 버전, 패키지 호환성과 lockfile은 확인하지 않았다.
- 설치 전 가상환경 경로와 `python -m pip --version`이 같은 환경을 가리키는지 확인한다.

## 관련 노트

- [[20 소스 노트/강의/Python 기초와 Streamlit 강의|Python 기초와 Streamlit 강의]]
- [[50 영역/개발 레퍼런스/Conda 환경 설정|Conda 환경 설정]]
