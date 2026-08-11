---
type: 'permanent'
status: 'growing'
created: '2026-05-30'
updated: '2026-08-11'
reviewed: '2026-08-11'
tags:
  - 'react'
  - 'spa'
  - 'state'
aliases:
  - 'React SPA'
sources:
  - 'https://react.dev/learn/sharing-state-between-components'
  - 'https://react.dev/learn/synchronizing-with-effects'
source_quality: 'mixed'
verified: true
id: '20260530000000-aa87'
---

# React SPA는 화면 상태와 서버 상태의 경계를 분명히 해야 한다

## 주장

React SPA에서는 입력값, 선택 상태처럼 화면이 소유하는 값과 네트워크에서 읽어 온 서버 상태를 같은 종류의 state로 무작정 복제하지 않아야 한다. React가 각 상태의 단일 소유자를 정하고 외부 시스템과의 동기화를 Effect로 구분하라고 설명하는 점을, 나는 서버 데이터의 출처와 로딩 수명도 화면 상태와 명시적으로 나누라는 설계 원칙으로 해석한다.

## 연결

실제 동기화 경계에서는 [[React API 요청은 로딩 실패 취소 상태를 함께 다뤄야 한다]]가 네트워크 수명을 UI로 드러낸다. 서버가 데이터를 제공하는 쪽의 계약은 [[Django JSON API는 화면과 서버 책임을 분리한다]]와 이어진다. [[React와 CI CD 강의]]에는 React 원본이 없다는 근거 공백이 기록되어 있어 이 노트의 기술 주장은 React 공식 문서로 확인했다.

## 한계와 반례

화면 상태와 서버 상태를 나눈다는 말이 둘을 서로 다른 전역 저장소에 반드시 넣으라는 뜻은 아니다. React 공식 문서도 수동 Effect fetch의 waterfall·캐시 부재를 지적하므로, 프레임워크의 서버 렌더링이나 내장 데이터 로더가 있는 경우에는 그 경계가 더 적합할 수 있다. 상호작용이 적은 페이지라면 SPA 자체가 불필요한 복잡성일 수 있다.

## 확인한 근거

- 2026-08-11: React 공식 Sharing State 문서에서 각 상태마다 단일 소유자를 정하고 중복 상태를 피하는 원칙을 확인했다.
- 2026-08-11: React 공식 Synchronizing with Effects 문서에서 네트워크를 외부 시스템으로 다루며 cleanup과 프레임워크 데이터 로딩을 고려하는 범위를 확인했다.
- 로컬 근거 경계: [[React와 CI CD 강의]]와 [[웹 클라이언트 강의]]에는 React 소스가 없으므로 프로젝트 전환에 관한 기존 세부 주장을 근거로 사용하지 않았다.
