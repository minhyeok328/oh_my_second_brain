---
type: 'source'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'git'
  - 'collaboration'
  - 'cheatsheet'
aliases: []
sources:
  - 'https://git-scm.com/docs'
source_quality: 'mixed'
verified: false
id: '20260530000000-c029'
---

# Git 명령어 모음

## 용도

변경 상태, 스테이징, 커밋과 이력을 확인하는 기본 명령을 모은다.

## 빠른 참조

- `git status --short`: 작업 트리와 인덱스 상태를 짧게 확인
- `git diff -- <path>`: 스테이징하지 않은 변경 확인
- `git diff --cached -- <path>`: 스테이징한 변경 확인
- `git add -- <path>`: 지정 경로를 인덱스에 추가
- `git commit -m "<message>"`: 스테이징된 변경으로 커밋 생성
- `git log --oneline --decorate -n 10`: 최근 이력을 한 줄씩 확인
- `git branch --show-current`: 현재 브랜치 이름 확인

## 검증 범위

- 2026-08-11: Git 공식 레퍼런스에서 각 명령을 확인했다.
- 원격 저장소 정책, hook, 서명, merge/rebase 전략은 확인하지 않았다. 되돌리기·삭제 성격의 명령은 이 노트에 두지 않았으며 사용 전 해당 명령의 공식 문서를 별도로 확인한다.

## 관련 노트

- [[20 소스 노트/강의/Git 기초 강의|Git 기초 강의]]
- [[개인 Dev Rules]]
