from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(r"C:\Obsidian\KnowledgeVault")
KNOWLEDGE = ROOT / "Knowledge"
TODAY = "2026-05-30"


TOPICAL_MOCS = {
    "Python MOC": (
        "Python 기본 문법을 먼저 훑고, 함수와 객체로 로직을 묶은 뒤 Streamlit으로 작은 화면을 만들어 본다.",
        "문법 오류인지, 자료형 오류인지, 상태 관리 문제인지 먼저 나눈 다음 관련 노트로 내려간다.",
    ),
    "Database MOC": (
        "관계형 모델과 SQL 조회를 먼저 잡고, JOIN, GROUP BY, 트랜잭션 순서로 데이터 경계를 넓힌다.",
        "조회 결과가 이상하면 조건, 조인 키, 집계 기준, 트랜잭션 상태를 차례로 확인한다.",
    ),
    "Data Analysis MOC": (
        "NumPy 배열에서 Pandas 표 구조로 넘어가고, GroupBy와 시각화로 질문을 검증한다.",
        "분석 결과가 흔들리면 결측치, 인덱스, 조인 기준, 집계 단위를 먼저 점검한다.",
    ),
    "Machine Learning MOC": (
        "데이터 분리, 전처리, 평가 지표를 먼저 고정한 뒤 모델 계열을 비교한다.",
        "성능 문제가 생기면 누수, 과적합, 지표 선택, 검증 전략을 순서대로 확인한다.",
    ),
    "Deep Learning MOC": (
        "퍼셉트론, 손실, 역전파, 옵티마이저를 연결한 뒤 CNN과 Transformer로 확장한다.",
        "학습이 불안정하면 입력 스케일, 손실, 그래디언트, 정규화, 데이터 양을 분리해 본다.",
    ),
    "NLP MOC": (
        "토큰화와 임베딩으로 텍스트 표현을 만들고, RNN/LSTM에서 Attention과 Transformer로 넘어간다.",
        "텍스트 모델 문제가 생기면 전처리, vocabulary, sequence 길이, 평가 데이터 분포를 확인한다.",
    ),
    "LLM RAG MOC": (
        "LLM 호출과 프롬프트를 이해한 뒤, 검색, 재순위화, LangGraph 흐름으로 확장한다.",
        "답변 품질이 낮으면 검색 실패, 컨텍스트 과다, 프롬프트 모호성, 생성 후 검증 부재를 나눠 본다.",
    ),
    "Multimodal MOC": (
        "이미지 모델의 기본 표현을 잡고 CLIP/BLIP, 이미지 생성, 멀티모달 RAG로 확장한다.",
        "멀티모달 실패는 이미지 전처리, 텍스트-이미지 정렬, 검색 단위, 평가 기준을 분리해야 한다.",
    ),
    "Web MOC": (
        "HTML 구조, CSS 배치, JavaScript 상호작용을 먼저 잡고 Django 서버 흐름과 연결한다.",
        "웹 문제가 생기면 화면, 브라우저 상태, API 요청, 서버 라우팅, DB 쿼리 순서로 좁힌다.",
    ),
    "React MOC": (
        "컴포넌트와 Props/State를 먼저 이해하고, Hook과 Router, API fetch로 앱 흐름을 만든다.",
        "렌더링 문제가 생기면 상태 소유권, effect 의존성, key, 비동기 race를 확인한다.",
    ),
    "DevOps MOC": (
        "Git, Docker, Compose, 서버 프로세스, Nginx, CI/CD 순서로 배포 경계를 넓힌다.",
        "배포 실패는 코드, 이미지, 컨테이너 네트워크, 환경 변수, 프록시, CI secret 순서로 본다.",
    ),
    "Design Pattern MOC": (
        "생성, 구조, 행위 패턴을 문제 유형별로 나누고 코드 냄새를 줄이는 선택지로 이해한다.",
        "패턴을 적용하기 전에 변화 지점이 실제로 반복되는지, 단순 함수/클래스로 충분한지 확인한다.",
    ),
    "CI CD MOC": (
        "GitHub Actions workflow, secret, 배포 대상 순서로 자동화 경로를 만든다.",
        "파이프라인 실패는 checkout, dependency, build, test, credential, deploy 단계로 나누어 본다.",
    ),
}


EXTERNAL_SOURCES = {
    "RAG": [
        "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
        "https://docs.langchain.com/oss/python/langchain/rag",
    ],
    "LLM": [
        "https://en.wikipedia.org/wiki/Large_language_model",
        "https://platform.openai.com/docs/concepts",
    ],
    "LangGraph": [
        "https://docs.langchain.com/oss/python/langgraph/graph-api",
    ],
    "Pandas DataFrame": [
        "https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html",
    ],
    "Django ORM Model": [
        "https://docs.djangoproject.com/en/6.0/topics/db/models/",
    ],
    "useEffect": [
        "https://react.dev/reference/react/useEffect",
        "https://react.dev/learn/you-might-not-need-an-effect",
    ],
    "Django QuerySet": [
        "https://docs.djangoproject.com/en/6.0/ref/models/querysets/",
    ],
    "Embedding": [
        "https://platform.openai.com/docs/api-reference/embeddings",
        "https://platform.openai.com/docs/concepts",
    ],
    "Vector Store": [
        "https://docs.langchain.com/oss/python/integrations/vectorstores/",
        "https://docs.langchain.com/oss/python/integrations/retrievers/index",
    ],
    "React API Fetch": [
        "https://react.dev/reference/react/useEffect",
        "https://react.dev/learn/you-might-not-need-an-effect",
    ],
    "Docker Compose": [
        "https://docs.docker.com/compose/",
        "https://docs.docker.com/compose/compose-application-model/",
        "https://docs.docker.com/reference/compose-file/",
    ],
}


EXPANDED_BODIES = {
    "RAG": """# RAG

태그: #llm_wiki #llm #rag #retrieval

## 한 줄 정의

RAG는 생성 모델이 내부 파라미터만 믿고 답하지 않도록, 외부 문서를 검색한 뒤 그 근거를 컨텍스트로 넣어 답변하게 만드는 패턴이다.

## 내 말로 다시 설명

LLM은 말솜씨가 좋지만 최신 자료, 사내 문서, 긴 강의 자료를 항상 알고 있지는 않다. RAG는 먼저 질문을 검색 문제로 바꾸고, 관련 문서를 가져오고, 그 문서 안에서만 답을 만들도록 제한한다. 핵심은 "검색 품질이 답변 품질의 상한을 만든다"는 점이다.

## 작동 흐름

- 문서를 chunk로 나누고 metadata를 붙인다.
- chunk를 [[Embedding]]으로 바꿔 [[Vector Store]]에 저장한다.
- 사용자 질문을 같은 embedding 공간으로 보낸다.
- [[Retriever]]가 관련 chunk를 가져온다.
- 필요하면 [[Reranking]]이나 [[Query Expansion]]으로 문맥을 정제한다.
- LLM이 검색 근거를 바탕으로 답변하고 출처를 남긴다.

## 언제 쓰는가

- 강의 자료, 회사 문서, 정책, 매뉴얼처럼 답변 근거가 외부 지식에 있을 때
- 최신성이나 출처 추적이 중요할 때
- fine-tuning보다 지식 교체와 감사 가능성이 더 중요할 때

## 언제 쓰면 안 되는가

- 답변이 단순한 문장 변환, 요약, 분류처럼 외부 검색 없이 가능한 경우
- 검색 대상 문서가 너무 부실하거나 권한 관리가 정리되지 않은 경우
- 정답 계산이 필요한데 검색 문서만으로 검증할 수 없는 경우

## 자주 헷갈리는 점

- RAG는 모델을 똑똑하게 만드는 기술이라기보다, 모델이 참고할 근거를 잘 전달하는 시스템 설계다.
- embedding 검색만 붙이면 RAG가 완성되는 것이 아니다. chunking, metadata, reranking, prompt, 평가가 함께 필요하다.
- 검색 결과가 틀리면 LLM은 그럴듯하게 틀린 답을 만들 수 있다.

## 설계 체크리스트

- 질문 유형별로 필요한 문서 단위가 정해져 있는가?
- chunk 크기가 정의, 절차, 코드 예제를 끊어먹지 않는가?
- metadata로 강의 주차, 파일 경로, 버전, 권한을 필터링할 수 있는가?
- 검색 실패와 모르는 질문을 "모른다"로 처리하는가?
- 답변에 근거 문서 링크나 파일 경로가 남는가?

## 관련 개념

- [[LLM]]
- [[Embedding]]
- [[Vector Store]]
- [[Retriever]]
- [[Reranking]]
- [[LangChain]]
- [[LangGraph]]

## 확인 질문

- 지금 문제는 모델 지식 부족인가, 검색 대상 문서 품질 부족인가?
- 답변이 틀렸을 때 검색, 컨텍스트, 프롬프트, 생성 중 어디를 먼저 의심할 것인가?

## 외부 참조

- https://en.wikipedia.org/wiki/Retrieval-augmented_generation
- https://docs.langchain.com/oss/python/langchain/rag
""",
    "LLM": """# LLM

태그: #llm_wiki #llm #ai

## 한 줄 정의

LLM은 대규모 텍스트와 코드 데이터에서 언어 패턴을 학습해 다음 토큰을 예측하고, 그 능력을 대화, 요약, 추론 보조, 코드 생성에 활용하는 모델이다.

## 내 말로 다시 설명

LLM은 지식 데이터베이스가 아니라 확률적 언어 엔진이다. 질문을 받으면 내부 파라미터, 입력 컨텍스트, 지시문을 조합해 가장 그럴듯한 출력을 만든다. 그래서 잘 쓰려면 모델에게 무엇을 해야 하는지뿐 아니라 무엇을 근거로 삼아야 하는지도 명확히 줘야 한다.

## 핵심 개념

- 토큰: 모델이 읽고 쓰는 텍스트 단위다.
- 컨텍스트: 모델이 한 번에 참고할 수 있는 입력 범위다.
- instruction: 출력 목적과 제약을 정하는 지시다.
- grounding: 답변을 외부 근거에 묶는 방식이다.
- hallucination: 근거가 부족한데도 그럴듯하게 생성하는 실패다.

## 언제 쓰는가

- 자연어 설명, 요약, 변환, 초안 작성, 코드 보조처럼 언어적 판단이 필요한 경우
- 규칙은 복잡하지만 예시와 맥락으로 의도를 전달할 수 있는 경우
- [[RAG]]나 도구 호출로 외부 지식과 행동을 결합할 때

## 언제 쓰면 안 되는가

- 엄밀한 계산, 권한 변경, 결제, 의료/법률 판단처럼 검증 없는 자동 실행이 위험한 경우
- 정답이 데이터베이스 조회로 바로 나오는 경우
- 입력 데이터의 보안 경계가 정리되지 않은 경우

## 자주 헷갈리는 점

- temperature를 낮춘다고 사실성이 보장되지는 않는다.
- 긴 프롬프트가 좋은 프롬프트는 아니다. 필요한 역할, 근거, 출력 형식, 실패 조건이 분명해야 한다.
- fine-tuning은 지식 주입보다 행동 양식과 형식 안정화에 더 적합한 경우가 많다.

## 관련 개념

- [[Prompt Engineering]]
- [[OpenAI API]]
- [[Function Calling]]
- [[RAG]]
- [[Fine-tuning]]
- [[SLLM]]

## 확인 질문

- 이 작업은 LLM이 판단해야 하는가, 아니면 검색/계산/규칙으로 해결해야 하는가?
- 답변을 검증할 근거와 실패 처리 방식이 있는가?

## 외부 참조

- https://en.wikipedia.org/wiki/Large_language_model
- https://platform.openai.com/docs/concepts
""",
    "LangGraph": """# LangGraph

태그: #llm_wiki #llm #langgraph #agent

## 한 줄 정의

LangGraph는 LLM 애플리케이션을 상태, 노드, 엣지로 표현해 반복, 분기, 도구 호출, human-in-the-loop 흐름을 제어하는 그래프 실행 프레임워크다.

## 내 말로 다시 설명

단순 chain은 "A 다음 B"처럼 직선 흐름에 강하다. LangGraph는 상태를 들고 여러 노드를 오가며 조건에 따라 다음 행동을 고를 수 있다. 그래서 RAG 검색, 도구 호출, 검증, 재시도, 사용자 확인이 섞인 에이전트 흐름을 설명하기 좋다.

## 핵심 구성

- [[LangGraph State]]: 노드들이 공유하는 데이터 구조다.
- [[LangGraph Node와 Edge]]: 작업 단위와 이동 경로다.
- [[LangGraph Conditional Edge]]: 상태에 따라 다음 노드를 고르는 분기다.
- compile: 그래프 정의를 실행 가능한 객체로 만든다.

## 언제 쓰는가

- 검색, 생성, 검증, 재검색처럼 반복 흐름이 필요할 때
- LLM이 도구를 호출한 뒤 결과에 따라 다음 행동을 바꿔야 할 때
- 실패 시 재시도나 사람 확인 단계를 넣어야 할 때

## 언제 쓰면 안 되는가

- 한 번의 prompt와 한 번의 모델 호출로 충분한 경우
- 상태 설계 없이 노드만 늘려 흐름이 더 불투명해지는 경우
- 로그와 관찰 가능성 없이 복잡한 agent를 먼저 만들려는 경우

## 자주 헷갈리는 점

- LangGraph는 LLM 자체가 아니라 LLM 호출, 도구, 분기, 상태를 묶는 실행 구조다.
- node를 많이 만든다고 좋은 agent가 되지는 않는다. 상태와 종료 조건이 더 중요하다.
- graph가 복잡해질수록 각 node의 입력과 출력 로그가 없으면 디버깅이 어려워진다.

## 설계 체크리스트

- State에 꼭 필요한 값만 들어 있는가?
- 각 node가 한 가지 책임만 갖는가?
- 조건 분기가 테스트 가능한 기준으로 작성됐는가?
- 종료 조건과 실패 조건이 명확한가?
- 각 실행 단계의 입력/출력을 기록하는가?

## 관련 개념

- [[LangChain]]
- [[Runnable]]
- [[RAG]]
- [[Multi-Agent]]
- [[Function Calling]]

## 확인 질문

- 이 흐름은 chain으로 충분한가, 상태 기반 graph가 필요한가?
- 재시도와 종료 조건이 코드로 설명되는가?

## 외부 참조

- https://docs.langchain.com/oss/python/langgraph/graph-api
""",
    "Pandas DataFrame": """# Pandas DataFrame

태그: #llm_wiki #pandas #data_analysis

## 한 줄 정의

Pandas DataFrame은 행과 열 인덱스를 가진 2차원 표 데이터 구조로, 정형 데이터를 정리, 필터링, 집계, 결합하는 중심 도구다.

## 내 말로 다시 설명

DataFrame은 엑셀 표처럼 보이지만, 내부적으로는 컬럼별 dtype과 인덱스를 가진 분석 객체다. 데이터 분석에서 "데이터가 지금 어떤 행 단위와 열 의미를 갖는가"를 명확히 드러내는 그릇이다.

## 핵심 개념

- row index: 행을 식별하거나 정렬 기준이 되는 축이다.
- column: 변수 또는 feature를 나타낸다.
- dtype: 각 컬럼의 연산 가능성을 결정한다.
- missing value: 결측치 처리 전략이 분석 결과를 바꾼다.
- vectorized operation: 반복문보다 컬럼 단위 연산을 우선한다.

## 언제 쓰는가

- CSV, Excel, SQL 결과처럼 행/열 구조가 있는 데이터를 다룰 때
- [[Pandas GroupBy]], [[Pandas Merge]], [[Pandas 인덱싱]]이 필요한 분석 흐름
- 모델링 전 EDA와 feature engineering을 할 때

## 언제 쓰면 안 되는가

- 데이터가 너무 커서 메모리에 올릴 수 없는 경우
- 이미지, 오디오, 그래프처럼 표 구조가 본질이 아닌 경우
- 엄격한 schema와 transaction이 필요한 운영 저장소 역할

## 자주 헷갈리는 점

- index는 그냥 행 번호가 아니라 정렬, join, selection에 영향을 주는 축이다.
- view와 copy 경고는 원본 변경 여부가 모호할 때 생긴다.
- `object` dtype은 문자열뿐 아니라 섞인 타입을 포함할 수 있다.

## 작은 예제

```python
import pandas as pd

df = pd.DataFrame({
    "team": ["A", "A", "B"],
    "score": [10, 15, 8],
})
summary = df.groupby("team")["score"].mean()
```

## 관련 개념

- [[Pandas Series]]
- [[Pandas GroupBy]]
- [[Pandas Merge]]
- [[Pandas 결측치 처리]]
- [[EDA]]

## 확인 질문

- 현재 행 하나는 무엇을 의미하는가?
- 분석 전 index, dtype, 결측치를 확인했는가?

## 외부 참조

- https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
""",
    "Django ORM Model": """# Django ORM Model

태그: #llm_wiki #django #orm #database

## 한 줄 정의

Django ORM Model은 Python 클래스로 데이터베이스 테이블 구조와 비즈니스 객체를 정의하는 Django의 데이터 모델 계층이다.

## 내 말로 다시 설명

Model은 "DB 테이블을 Python 코드로 선언한 것"에 가깝다. 필드는 컬럼이 되고, 클래스는 테이블이 되며, migration은 그 선언을 실제 DB schema 변화로 옮긴다. Django 앱에서 데이터의 의미와 제약을 가장 오래 보존하는 장소다.

## 핵심 개념

- field: 컬럼 타입과 제약을 정의한다.
- relationship: ForeignKey, OneToOne, ManyToMany로 테이블 관계를 표현한다.
- migration: 모델 변경을 DB schema 변경 이력으로 기록한다.
- manager/queryset: 모델 데이터를 조회하고 조작하는 API다.
- admin/form/view: 모델 정의를 기준으로 화면과 관리 기능이 연결된다.

## 언제 쓰는가

- Django 앱에서 저장해야 할 핵심 도메인 개념이 있을 때
- [[Django QuerySet]]으로 조회/필터링할 데이터가 있을 때
- 인증, 게시판, 챗봇 대화 로그처럼 DB에 남길 상태가 있을 때

## 언제 쓰면 안 되는가

- API 응답 임시 구조처럼 저장하지 않을 데이터
- 복잡한 분석용 임시 테이블을 앱 모델로 억지로 표현해야 하는 경우
- migration 전략 없이 운영 DB 구조를 자주 흔드는 경우

## 자주 헷갈리는 점

- 모델 클래스를 바꿨다고 DB가 바로 바뀌지 않는다. `makemigrations`와 `migrate`가 필요하다.
- `null=True`는 DB 레벨, `blank=True`는 form validation 레벨 의미가 강하다.
- relationship은 편하지만 잘못 쓰면 N+1 query가 생긴다.

## 관련 개념

- [[Django Migration]]
- [[Django QuerySet]]
- [[Django View]]
- [[Django Form]]
- [[관계형 데이터베이스]]

## 확인 질문

- 이 필드는 도메인 규칙인가, 화면 입력 편의를 위한 값인가?
- 관계를 모델에 둘 때 조회 성능과 삭제 정책을 고려했는가?

## 외부 참조

- https://docs.djangoproject.com/en/6.0/topics/db/models/
""",
    "useEffect": """# useEffect

태그: #llm_wiki #react #hook

## 한 줄 정의

useEffect는 React 컴포넌트가 렌더링된 뒤 외부 시스템과 동기화해야 할 작업을 수행하게 해주는 Hook이다.

## 내 말로 다시 설명

useEffect는 "렌더링 결과를 바깥 세계와 맞추는 장치"다. DOM 제목 변경, 구독 연결, 네트워크 요청, 타이머처럼 React 렌더링만으로 끝나지 않는 일이 있을 때 쓴다. 상태 계산을 effect에 넣으면 불필요한 렌더링과 버그가 늘어난다.

## 언제 쓰는가

- 브라우저 API, timer, event listener, 외부 라이브러리와 동기화할 때
- 서버/API에서 데이터를 가져와 컴포넌트 상태에 반영할 때
- 컴포넌트 mount/unmount에 맞춰 연결과 정리를 해야 할 때

## 언제 쓰면 안 되는가

- props나 state에서 계산 가능한 값을 다시 state로 저장할 때
- 사용자 이벤트 처리로 충분한 로직을 렌더링 후 effect로 미룰 때
- 단순 데이터 fetching을 라우터/쿼리 라이브러리가 더 잘 처리하는 구조일 때

## 의존성 배열 기준

- effect 안에서 읽는 reactive 값은 의존성에 포함한다.
- 의존성을 줄이려고 lint를 끄기보다 함수 위치와 상태 구조를 다시 본다.
- cleanup은 이전 effect의 연결을 정리한다.

## 자주 헷갈리는 점

- 빈 배열은 "한 번만"이 아니라 "이 effect가 reactive 값을 읽지 않는다"는 선언에 가깝다.
- Strict Mode 개발 환경에서는 effect가 두 번 실행되어 cleanup 문제를 드러낼 수 있다.
- fetch effect는 race condition과 abort 처리를 신경 써야 한다.

## 관련 개념

- [[React]]
- [[React Lifecycle]]
- [[React State]]
- [[React API Fetch]]
- [[Custom Hook]]

## 확인 질문

- 이 코드는 외부 시스템 동기화인가, 렌더링 중 계산 가능한 값인가?
- cleanup이 필요한 연결을 만들고 있지는 않은가?

## 외부 참조

- https://react.dev/reference/react/useEffect
- https://react.dev/learn/you-might-not-need-an-effect
""",
    "Django QuerySet": """# Django QuerySet

태그: #llm_wiki #django #orm #database

## 한 줄 정의

Django QuerySet은 Django ORM에서 데이터베이스 조회 조건을 누적하고, 필요할 때 SQL로 평가되는 지연 실행 객체다.

## 내 말로 다시 설명

QuerySet은 "아직 실행되지 않은 DB 질문"이다. `filter()`, `exclude()`, `order_by()`를 이어 붙이면 질문이 더 구체화되고, 반복하거나 `list()`로 만들거나 값을 꺼낼 때 실제 query가 실행된다. Django 성능 문제는 QuerySet이 언제 평가되는지 모를 때 자주 생긴다.

## 핵심 개념

- lazy evaluation: QuerySet은 생성만으로 DB에 가지 않는다.
- chaining: 조건을 이어 붙여도 원본 QuerySet은 보통 변경되지 않는다.
- filtering: `filter`, `exclude`, field lookup으로 WHERE를 만든다.
- related loading: `select_related`, `prefetch_related`로 N+1 query를 줄인다.
- aggregation: `annotate`, `aggregate`로 DB에서 집계한다.

## 언제 쓰는가

- [[Django ORM Model]] 데이터를 조건별로 조회할 때
- View에서 목록, 상세, 검색, 페이지네이션을 만들 때
- DB가 잘하는 필터링과 정렬을 Python 반복문 대신 맡길 때

## 언제 쓰면 안 되는가

- 이미 메모리에 있는 작은 리스트를 단순 변환하는 경우
- 복잡한 분석 처리를 ORM으로 억지로 표현해 SQL이 불투명해지는 경우
- QuerySet 평가 시점을 모른 채 template에서 반복 접근하는 경우

## 자주 헷갈리는 점

- `get()`은 객체 하나를 바로 평가해서 반환하고, 없거나 여러 개면 예외가 난다.
- `filter()`는 0개여도 QuerySet을 반환한다.
- QuerySet을 template에서 반복하면서 related field를 매번 읽으면 N+1 query가 될 수 있다.

## 작은 예제

```python
posts = (
    Post.objects
    .filter(is_public=True)
    .select_related("author")
    .order_by("-created_at")
)
```

## 관련 개념

- [[Django ORM Model]]
- [[Django View]]
- [[Django Migration]]
- [[SQL SELECT와 WHERE]]
- [[SQL JOIN]]

## 확인 질문

- 이 QuerySet은 어느 줄에서 실제 DB에 접근하는가?
- related object 접근으로 query가 반복되지 않는가?

## 외부 참조

- https://docs.djangoproject.com/en/6.0/ref/models/querysets/
""",
    "Embedding": """# Embedding

태그: #llm_wiki #llm #rag #embedding

## 한 줄 정의

Embedding은 텍스트, 이미지 같은 입력을 의미적 유사도를 계산할 수 있는 숫자 벡터로 변환한 표현이다.

## 내 말로 다시 설명

Embedding은 문장을 좌표 공간에 놓는 일이다. 비슷한 의미의 문장은 가까운 좌표에 놓이고, 전혀 다른 의미는 멀어진다. RAG에서는 질문과 문서 chunk를 같은 공간에 넣어 "문자열이 같은가"가 아니라 "의미가 가까운가"로 검색한다.

## 핵심 개념

- vector dimension: embedding 벡터의 길이다.
- similarity: cosine, dot product 등으로 가까움을 계산한다.
- normalization: 거리 계산 방식에 따라 벡터 정규화가 중요할 수 있다.
- chunk granularity: 너무 큰 chunk는 의미가 흐려지고, 너무 작은 chunk는 맥락이 끊긴다.
- metadata: embedding만으로 부족한 필터링 정보를 보완한다.

## 언제 쓰는가

- [[RAG]]에서 문서 검색을 의미 기반으로 하고 싶을 때
- 중복 문서 탐지, 유사 질문 추천, semantic clustering이 필요할 때
- 키워드 검색으로 표현 차이를 잡지 못할 때

## 언제 쓰면 안 되는가

- 정확한 문자열 일치나 정규식 검색이 필요한 경우
- 숫자 계산이나 날짜 범위 필터처럼 구조화 query가 더 정확한 경우
- 데이터 권한과 개인정보 처리 기준이 정리되지 않은 경우

## 자주 헷갈리는 점

- embedding 검색은 "정답"이 아니라 "유사 후보"를 돌려준다.
- 모델, dimension, 거리 metric을 바꾸면 기존 index와 비교 기준도 달라진다.
- 좋은 embedding도 나쁜 chunking을 구제하지 못한다.

## 관련 개념

- [[Vector Store]]
- [[Retriever]]
- [[Text Splitter]]
- [[RAG]]
- [[Word Embedding]]

## 확인 질문

- 검색하려는 단위는 문단, 코드 블록, 파일, 강의 섹션 중 무엇인가?
- 의미 검색과 metadata filter를 어떻게 나눌 것인가?

## 외부 참조

- https://platform.openai.com/docs/api-reference/embeddings
- https://platform.openai.com/docs/concepts
""",
    "Vector Store": """# Vector Store

태그: #llm_wiki #llm #rag #vectorstore

## 한 줄 정의

Vector Store는 embedding 벡터와 원문 metadata를 저장하고, 유사도 검색으로 관련 문서를 찾아주는 저장 계층이다.

## 내 말로 다시 설명

Vector Store는 RAG의 검색 엔진 역할을 한다. 문서 chunk의 embedding을 저장해 두었다가 질문 embedding이 들어오면 가까운 벡터를 찾아 원문과 metadata를 돌려준다. 단순 저장소가 아니라 검색 기준, 필터, 업데이트 전략이 함께 설계되어야 한다.

## 핵심 개념

- index: vector similarity search를 빠르게 하기 위한 구조다.
- document id: chunk와 원본 파일/섹션을 다시 연결하는 키다.
- metadata filter: 강의, 주차, 권한, 파일 타입으로 검색 범위를 줄인다.
- top-k: 가져올 후보 개수다.
- refresh strategy: 원문이 바뀔 때 embedding과 index를 갱신하는 방식이다.

## 언제 쓰는가

- [[Embedding]] 기반 semantic search가 필요할 때
- 강의 자료, 문서 저장소, FAQ를 [[RAG]]에 연결할 때
- 검색 결과에 source path와 metadata를 함께 남겨야 할 때

## 언제 쓰면 안 되는가

- 데이터가 작아서 일반 full-text search나 dictionary lookup이면 충분한 경우
- 수치 범위, 정렬, join이 핵심인 구조화 데이터 조회
- 원문 업데이트가 잦은데 index 갱신 정책이 없는 경우

## 자주 헷갈리는 점

- Vector Store는 DB 전체를 대체하지 않는다. 원문 저장소와 권한 시스템은 따로 필요할 수 있다.
- top-k를 늘리면 recall은 오를 수 있지만 prompt noise도 늘어난다.
- metadata가 부실하면 비슷하지만 엉뚱한 문서가 섞인다.

## 관련 개념

- [[Embedding]]
- [[Retriever]]
- [[Text Splitter]]
- [[Reranking]]
- [[RAG]]

## 확인 질문

- 검색 결과가 틀렸을 때 embedding, metadata, chunking 중 어디를 먼저 조정할 것인가?
- 원문 삭제/수정 시 vector index도 함께 갱신되는가?

## 외부 참조

- https://docs.langchain.com/oss/python/integrations/vectorstores/
- https://docs.langchain.com/oss/python/integrations/retrievers/index
""",
    "React API Fetch": """# React API Fetch

태그: #llm_wiki #react #api #frontend

## 한 줄 정의

React API Fetch는 컴포넌트나 라우트가 서버 API에서 데이터를 받아 화면 상태와 동기화하는 프론트엔드 데이터 로딩 패턴이다.

## 내 말로 다시 설명

React에서 API 호출은 단순히 `fetch()`를 쓰는 문제가 아니다. 언제 요청할지, 로딩과 에러를 어떻게 보여줄지, 이전 요청이 늦게 도착했을 때 어떻게 막을지, 컴포넌트가 사라질 때 정리할지가 함께 따라온다.

## 기본 흐름

- 요청에 필요한 입력 상태를 정한다.
- loading, data, error 상태를 분리한다.
- 요청 성공 시 data를 갱신한다.
- 실패 시 사용자에게 보여줄 error를 저장한다.
- 컴포넌트 unmount나 입력 변경 시 stale response를 막는다.

## 언제 쓰는가

- 서버 데이터가 화면 렌더링에 필요할 때
- 사용자의 검색 조건, 페이지, 필터에 따라 API를 다시 호출해야 할 때
- 작은 앱에서 별도 data fetching 라이브러리 없이 처리해도 충분할 때

## 언제 쓰면 안 되는가

- 서버 상태 캐싱, 중복 요청 제거, pagination, mutation invalidation이 복잡한 경우
- 라우터 loader나 query library가 이미 데이터 흐름을 맡고 있는 경우
- 렌더링 중 계산 가능한 값을 굳이 API 상태로 분리하는 경우

## 자주 헷갈리는 점

- `useEffect` 안 fetch는 race condition을 만들 수 있다.
- HTTP 에러와 네트워크 에러를 구분해야 한다.
- API 응답 shape가 바뀌면 화면 상태와 타입도 같이 깨진다.

## 작은 예제

```jsx
useEffect(() => {
  let ignore = false;
  setLoading(true);

  fetch(`/api/posts?q=${query}`)
    .then((res) => {
      if (!res.ok) throw new Error("Request failed");
      return res.json();
    })
    .then((data) => {
      if (!ignore) setPosts(data);
    })
    .catch((error) => {
      if (!ignore) setError(error.message);
    })
    .finally(() => {
      if (!ignore) setLoading(false);
    });

  return () => {
    ignore = true;
  };
}, [query]);
```

## 관련 개념

- [[useEffect]]
- [[React State]]
- [[JavaScript 비동기]]
- [[Requests]]
- [[Django View]]

## 확인 질문

- 이 데이터는 서버 상태인가, 컴포넌트 내부 상태인가?
- 요청이 늦게 도착했을 때 이전 화면을 덮어쓰지 않는가?

## 외부 참조

- https://react.dev/reference/react/useEffect
- https://react.dev/learn/you-might-not-need-an-effect
""",
    "Docker Compose": """# Docker Compose

태그: #llm_wiki #docker #devops

## 한 줄 정의

Docker Compose는 여러 컨테이너 서비스, 네트워크, 볼륨, 환경 변수를 하나의 Compose 파일로 정의하고 함께 실행하는 도구다.

## 내 말로 다시 설명

실제 웹 앱은 Django 컨테이너 하나로 끝나지 않는다. DB, Redis, Nginx, worker 같은 여러 프로세스가 함께 움직인다. Compose는 이 묶음을 "로컬 또는 서버에서 재현 가능한 실행 단위"로 만든다.

## 핵심 개념

- service: 실행할 컨테이너 단위다.
- image/build: 이미지를 받을지 직접 빌드할지 정한다.
- ports: host와 container 포트를 연결한다.
- volumes: 데이터나 코드 경로를 컨테이너와 공유한다.
- networks: 서비스 간 통신 경계를 만든다.
- environment: 설정값과 secret 주입 경로다.

## 언제 쓰는가

- Django, DB, Nginx처럼 여러 컨테이너를 함께 실행할 때
- 로컬 개발 환경을 팀원과 동일하게 맞추고 싶을 때
- 배포 전 서비스 간 연결을 재현하고 테스트할 때

## 언제 쓰면 안 되는가

- 단일 컨테이너 실험이면 `docker run`이 충분한 경우
- 운영 오케스트레이션, auto scaling, rolling update가 필요한 경우
- secret과 volume 정책 없이 운영 설정을 그대로 담으려는 경우

## 자주 헷갈리는 점

- `depends_on`은 실행 순서를 보장할 뿐, DB 준비 완료를 보장하지 않는다.
- container 내부 포트와 host 노출 포트는 다르다.
- named volume은 컨테이너를 지워도 데이터가 남을 수 있다.

## 작은 예제

```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
  db:
    image: postgres:16
    volumes:
      - db_data:/var/lib/postgresql/data

volumes:
  db_data:
```

## 관련 개념

- [[Docker Container]]
- [[Docker Image]]
- [[Dockerfile]]
- [[Docker Network]]
- [[Docker Volume]]
- [[Nginx]]

## 확인 질문

- 서비스 간 이름 해석, 포트, volume 위치를 정확히 구분했는가?
- 운영 환경에서 secret과 persistent data를 어떻게 관리할 것인가?

## 외부 참조

- https://docs.docker.com/compose/
- https://docs.docker.com/compose/compose-application-model/
- https://docs.docker.com/reference/compose-file/
""",
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def strip_frontmatter(text: str) -> tuple[dict[str, object], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end == -1:
        return {}, text
    return {}, text[end + 5 :].lstrip("\n")


def title_from_body(path: Path, body: str) -> str:
    match = re.search(r"^#\s+(.+)$", body, re.M)
    return match.group(1).strip() if match else path.stem


def tags_from_body(body: str) -> list[str]:
    match = re.search(r"^태그:\s*(.+)$", body, re.M)
    tags: list[str] = []
    if match:
        for raw in match.group(1).split():
            tag = raw.strip().lstrip("#")
            if tag and tag not in tags:
                tags.append(tag)
    return tags


def ensure_inline_llm_tag(body: str) -> str:
    if re.search(r"^태그:", body, re.M):
        def repl(match: re.Match[str]) -> str:
            line = match.group(0)
            return line if "#llm_wiki" in line else line + " #llm_wiki"

        return re.sub(r"^태그:.*$", repl, body, count=1, flags=re.M)
    lines = body.splitlines()
    if lines and lines[0].startswith("# "):
        return lines[0] + "\n\n태그: #llm_wiki\n" + "\n".join(lines[1:]).lstrip("\n")
    return "태그: #llm_wiki\n\n" + body


def yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    return "\n" + "\n".join(f"  - '{item.replace("'", "''")}'" for item in items)


def frontmatter(
    *,
    note_type: str,
    status: str,
    tags: list[str],
    source: list[str] | None = None,
    external: list[str] | None = None,
    aliases: list[str] | None = None,
) -> str:
    clean_tags: list[str] = []
    for tag in ["llm_wiki", *tags]:
        tag = tag.strip().lstrip("#").replace(" ", "_")
        if tag and tag not in clean_tags:
            clean_tags.append(tag)
    lines = [
        "---",
        f'type: "{note_type}"',
        f'status: "{status}"',
        f'created: "{TODAY}"',
        f'updated: "{TODAY}"',
        f'reviewed: "{TODAY}"',
        "tags:" + yaml_list(clean_tags),
    ]
    if aliases:
        lines.append("aliases:" + yaml_list(aliases))
    if source:
        lines.append("source:" + yaml_list(source))
    if external:
        lines.append("external:" + yaml_list(external))
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def classify(path: Path) -> tuple[str, str]:
    parts = path.parts
    if "Permanent Notes" in parts:
        return "permanent", "wiki-standardized"
    if "Literature Notes" in parts:
        return "literature", "source-expanded"
    if "Reference Notes" in parts:
        return "reference", "reference"
    if "Maps of Content" in parts:
        return "moc", "wiki-map" if path.stem in TOPICAL_MOCS or path.stem == "Knowledge Index" else "map"
    if "Templates" in parts:
        return "template", "template"
    if "Questions" in parts:
        return "question-index", "active"
    if "Projects" in parts:
        return "project-log", "active"
    if "Sources" in parts:
        return "source-policy", "policy"
    if "Assets" in parts:
        return "asset", "source-outline"
    if path.name == "README.md":
        return "index", "entrypoint"
    return "note", "wiki-seed"


def related_links(body: str, limit: int = 3) -> list[str]:
    body_no_code = re.sub(r"```.*?```", "", body, flags=re.S)
    links = []
    for target in re.findall(r"\[\[([^\]|#]+)", body_no_code):
        if target not in links:
            links.append(target)
    return links[:limit]


def standardized_tail(title: str, body: str) -> str:
    links = related_links(body)
    link_hint = ", ".join(f"[[{link}]]" for link in links) if links else "인접 노트"
    return f"""

## 내 말로 다시 설명

{title}은/는 강의에서 나온 개념을 정의, 사용 조건, 주의점, 연결 개념으로 다시 설명하기 위한 LLM wiki 원자 노트다. 단순 암기보다 실제 문제에서 언제 꺼내 쓸지 판단하는 데 초점을 둔다.

## 언제 쓰는가

- 강의 실습 코드에서 같은 개념을 다시 만날 때
- 프로젝트에서 관련 오류나 설계 결정을 설명해야 할 때
- {link_hint}와 함께 문제 원인을 좁힐 때

## 언제 쓰면 안 되는가

- 구체적인 API 버전, 파라미터, 보안 정책이 필요한 경우에는 공식 문서를 먼저 확인한다.
- 예제 하나만 보고 모든 상황에 일반화해야 할 때는 보류한다.
- 이미 더 좁고 구체적인 노트가 있는 경우에는 그 노트로 이동한다.

## 자주 헷갈리는 점

- 이름이 비슷한 인접 개념과 책임 범위가 다를 수 있다.
- 강의 예제의 상황과 실제 프로젝트의 데이터, 환경, 버전 차이를 분리해야 한다.
- "동작한다"와 "운영에서 유지보수 가능하다"는 다른 기준이다.

## 확인 질문

- {title}을/를 쓰면 어떤 문제를 더 단순하게 설명할 수 있는가?
- 관련 개념과 구분되는 핵심 기준은 무엇인가?
- 실제 프로젝트에 적용하면 먼저 검증해야 할 실패 조건은 무엇인가?
"""


def apply_frontmatter_and_standard_sections() -> None:
    for path in sorted(KNOWLEDGE.rglob("*.md")):
        _, body = strip_frontmatter(read(path))
        body = ensure_inline_llm_tag(body) if body.strip() else body
        title = title_from_body(path, body)
        note_type, status = classify(path)
        tags = tags_from_body(body)
        source = [r"C:\lecture"] if note_type in {"permanent", "literature", "reference", "moc"} else []
        external = EXTERNAL_SOURCES.get(title, [])
        if note_type == "permanent" and title in EXPANDED_BODIES:
            status = "wiki-expanded"
        elif note_type == "permanent" and "## 내 말로 다시 설명" not in body:
            body = body.rstrip() + standardized_tail(title, body)
        if note_type == "literature" and "## LLM Wiki 확인 질문" not in body:
            body = body.rstrip() + f"""

## LLM Wiki 확인 질문

- 이 강의 묶음에서 프로젝트에 바로 적용할 수 있는 개념은 무엇인가?
- 개념 노트 중 실제 코드 예제와 다시 연결해야 할 노트는 무엇인가?
- 다음 복습 때 {title}에서 확인할 실패 사례는 무엇인가?

## 보강 후보

- 원본 강의 파일의 핵심 코드 예제를 각 Permanent Note의 예제 섹션으로 더 연결한다.
- 외부 공식 문서와 강의 실습 버전 차이를 비교한다.
"""
        fm = frontmatter(
            note_type=note_type,
            status=status,
            tags=tags,
            source=source,
            external=external,
            aliases=[title] if title != path.stem else [],
        )
        write(path, fm + body)


def apply_expanded_notes() -> None:
    for title, body in EXPANDED_BODIES.items():
        path = KNOWLEDGE / "Permanent Notes" / f"{title}.md"
        tags = tags_from_body(body)
        fm = frontmatter(
            note_type="permanent",
            status="wiki-expanded",
            tags=tags,
            source=[r"C:\lecture"],
            external=EXTERNAL_SOURCES.get(title, []),
        )
        write(path, fm + body)


def enhance_mocs() -> None:
    for title, (learning, troubleshooting) in TOPICAL_MOCS.items():
        path = KNOWLEDGE / "Maps of Content" / f"{title}.md"
        if not path.exists():
            continue
        _, body = strip_frontmatter(read(path))
        body = ensure_inline_llm_tag(body)
        if "## 학습 경로" not in body:
            insert = f"""## 학습 경로

- {learning}
- 처음 읽을 때는 정의 노트보다 흐름 노트를 먼저 보고, 막히는 용어만 Permanent Note로 내려간다.

## 문제 해결 경로

- {troubleshooting}
- 해결 후에는 관련 Permanent Note의 확인 질문에 실제 사례를 한 줄로 남긴다.

"""
            body = re.sub(r"(?m)^## 핵심 노트\s*\n", insert + "## 핵심 노트\n", body, count=1)
            if "## 학습 경로" not in body:
                body = body.rstrip() + "\n\n" + insert.rstrip() + "\n"
        fm = frontmatter(
            note_type="moc",
            status="wiki-map",
            tags=tags_from_body(body),
            source=[r"C:\lecture"],
        )
        write(path, fm + body)


def write_operating_docs() -> None:
    docs = {
        KNOWLEDGE / "Maps of Content" / "LLM Wiki 운영 원칙.md": (
            frontmatter(note_type="moc", status="operating-guide", tags=["moc", "llm_wiki", "governance"]) +
            """# LLM Wiki 운영 원칙

태그: #moc #llm_wiki #governance

## 목적

이 vault는 강의 자료를 그대로 쌓는 저장소가 아니라, LLM이 검색하고 사람이 복습할 수 있는 설명형 wiki로 운영한다.

## 원칙

- 한 노트는 하나의 개념이나 판단 기준을 설명한다.
- 모든 Permanent Note는 정의, 사용 조건, 금지 조건, 혼동 지점, 확인 질문을 가진다.
- MOC는 단순 목록이 아니라 학습 경로와 문제 해결 경로를 제공한다.
- 외부 문서는 공식 문서와 위키를 보조 근거로 쓰고, 강의 원천과 충돌하면 출처를 분리해서 남긴다.
- 프로젝트에서 사용한 지식은 [[프로젝트 적용 로그]]에 기록해 죽은 지식이 되지 않게 한다.

## 보강 우선순위

- 검색 품질을 좌우하는 [[RAG]], [[Embedding]], [[Vector Store]], [[Retriever]]
- 실제 앱 구현에 자주 쓰는 [[Django QuerySet]], [[React API Fetch]], [[Docker Compose]]
- 혼동 비용이 큰 lifecycle, migration, state, transaction 관련 노트
"""
        ),
        KNOWLEDGE / "Sources" / "외부 참조 정책.md": (
            frontmatter(note_type="source-policy", status="policy", tags=["llm_wiki", "source"]) +
            """# 외부 참조 정책

태그: #llm_wiki #source

## 기본 입장

이 vault의 1차 원천은 `C:\\lecture` 강의 자료다. 외부 wiki와 공식 문서는 개념의 표준 정의, 최신 API 차이, 용어 정리를 보완하는 2차 원천으로 사용한다.

## 우선순위

- 공식 문서: API, 옵션, 버전, 권장 패턴 확인
- Wikipedia: 큰 개념의 역사, 범위, 용어 확인
- 강의 자료: 실제 학습 흐름과 실습 코드의 기준

## 기록 방식

- 외부 자료를 사용한 노트는 frontmatter의 `external`과 본문 `외부 참조`에 URL을 남긴다.
- 강의와 외부 문서가 다르면 어느 쪽이 어떤 맥락에서 맞는지 적는다.
- LLM 답변에 넣을 근거는 가능하면 원문 경로, 공식 문서 URL, 노트 링크를 함께 준다.
"""
        ),
        KNOWLEDGE / "Templates" / "LLM Wiki Note Template.md": (
            frontmatter(note_type="template", status="template", tags=["llm_wiki", "template"]) +
            """# LLM Wiki Note Template

태그: #llm_wiki #template

## 한 줄 정의

이 개념을 한 문장으로 설명한다.

## 내 말로 다시 설명

강의 예제나 프로젝트 맥락에서 다시 설명한다.

## 언제 쓰는가

- 조건 1
- 조건 2

## 언제 쓰면 안 되는가

- 금지 조건 1
- 금지 조건 2

## 자주 헷갈리는 점

- 인접 개념과의 차이
- 자주 나는 오류

## 관련 개념

- [[Knowledge Index]]

## 확인 질문

- 이 개념을 쓰는 판단 기준은 무엇인가?
- 실제 프로젝트에서 먼저 검증할 것은 무엇인가?
"""
        ),
        KNOWLEDGE / "Questions" / "질문 인박스.md": (
            frontmatter(note_type="question-index", status="active", tags=["llm_wiki", "questions"]) +
            """# 질문 인박스

태그: #llm_wiki #questions

## 열린 질문

- [[RAG]]에서 검색 실패와 생성 실패를 어떻게 로그로 분리할 것인가?
- [[Embedding]] 모델을 바꿀 때 기존 [[Vector Store]]를 어떻게 재색인할 것인가?
- [[Django QuerySet]]의 N+1 query를 강의 예제에서 어떻게 재현하고 측정할 것인가?
- [[React API Fetch]]에서 race condition을 실제 화면 버그로 어떻게 관찰할 것인가?
- [[Docker Compose]]의 `depends_on`과 readiness check 차이를 어떤 실습으로 확인할 것인가?

## 닫는 기준

- 질문이 특정 Permanent Note의 확인 질문이나 프로젝트 로그로 이동하면 닫는다.
- 답이 공식 문서 확인만으로 끝나면 [[외부 참조 정책]]에 따라 URL을 남긴다.
"""
        ),
        KNOWLEDGE / "Projects" / "프로젝트 적용 로그.md": (
            frontmatter(note_type="project-log", status="active", tags=["llm_wiki", "project"]) +
            """# 프로젝트 적용 로그

태그: #llm_wiki #project

## 기록 규칙

- 프로젝트에서 실제로 사용한 노트만 남긴다.
- 문제, 적용한 개념, 결과, 다음 보강 노트를 한 묶음으로 적는다.
- 단순 감상보다 재사용 가능한 판단 기준을 남긴다.

## 적용 후보

- 강의 자료 QA: [[RAG]], [[Embedding]], [[Vector Store]], [[LangGraph]]
- Django 챗봇: [[Django ORM Model]], [[Django QuerySet]], [[Django Chatbot]], [[OpenAI API]]
- React 대시보드: [[React API Fetch]], [[useEffect]], [[React State]], [[React Router]]
- 배포 실습: [[Docker Compose]], [[Nginx]], [[WSGI]], [[ASGI]], [[GitHub Actions]]

## 로그

- 2026-05-30: LLM wiki 전환. 모든 Permanent Note에 사용 조건과 확인 질문을 추가하고, 핵심 허브 노트를 우선 확장했다.
"""
        ),
    }
    for path, text in docs.items():
        write(path, text)


def update_readme() -> None:
    path = KNOWLEDGE / "README.md"
    text = frontmatter(note_type="index", status="entrypoint", tags=["llm_wiki", "obsidian", "index"]) + """# Knowledge Vault

태그: #llm_wiki #obsidian #index

이 Vault는 `C:\\lecture` 강의 자료를 기반으로 만든 LLM wiki형 second brain이다. 목표는 단순 보관이 아니라, LLM이 검색하고 사람이 복습하며 프로젝트에 적용할 수 있는 지식 구조를 만드는 것이다.

## 시작점

- [[Knowledge Index]]
- [[LLM Wiki 운영 원칙]]
- [[LLM Wiki 전환 리포트]]
- [[질문 인박스]]
- [[프로젝트 적용 로그]]

## 핵심 지도

- [[LLM RAG MOC]]
- [[Python MOC]]
- [[Data Analysis MOC]]
- [[Machine Learning MOC]]
- [[Deep Learning MOC]]
- [[React MOC]]
- [[Web MOC]]
- [[DevOps MOC]]

## 운영 루프

- 새 강의 내용은 Literature Note에 먼저 남긴다.
- 개념은 Permanent Note로 쪼갠다.
- MOC에는 학습 경로와 문제 해결 경로를 유지한다.
- 실제 프로젝트에서 쓴 내용은 프로젝트 로그로 되돌린다.
"""
    write(path, text)


def all_note_names() -> set[str]:
    names = {p.stem for p in KNOWLEDGE.rglob("*.md")}
    names.add("README")
    return names


def links_in(text: str) -> list[str]:
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return [m.split("#", 1)[0].split("|", 1)[0] for m in re.findall(r"\[\[([^\]]+)\]\]", text)]


def status_distribution() -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in KNOWLEDGE.rglob("*.md"):
        text = read(path)
        match = re.search(r'^status:\s*"([^"]+)"', text, re.M)
        counts[match.group(1) if match else "missing"] += 1
    return counts


def write_report() -> None:
    md_files = sorted(KNOWLEDGE.rglob("*.md"))
    names = all_note_names()
    missing_fm = [str(p.relative_to(ROOT)) for p in md_files if not read(p).startswith("---\n")]
    empty = [str(p.relative_to(ROOT)) for p in md_files if p.stat().st_size == 0]
    broken = []
    for path in md_files:
        for target in links_in(read(path)):
            if target and target not in names:
                broken.append({"file": str(path.relative_to(ROOT)), "target": target})
    status_counts = status_distribution()
    report_body = f"""# LLM Wiki 전환 리포트

태그: #llm_wiki #moc #migration

## 요약

- 기준일: {TODAY}
- Markdown 파일: {len(md_files)}개
- 빈 Markdown 파일: {len(empty)}개
- frontmatter 누락: {len(missing_fm)}개
- 확인된 미해결 wikilink: {len(broken)}개

## 상태 분포

{chr(10).join(f"- `{status}`: {count}개" for status, count in sorted(status_counts.items()))}

## 이번 전환에서 보완한 치명점

- frontmatter와 상태값이 없어 LLM이 노트 성격을 구분하기 어렵던 문제를 해결했다.
- Permanent Note가 짧은 정의에 머물러 있던 문제를 보완해 사용 조건, 금지 조건, 혼동 지점, 확인 질문을 추가했다.
- MOC가 단순 링크 목록이던 문제를 학습 경로와 문제 해결 경로 중심으로 바꾸었다.
- Literature Note와 프로젝트 적용 로그를 연결해 강의 원천, 개념, 실제 사용 사이의 루프를 만들었다.
- 외부 공식 문서와 wiki 참조 정책을 분리해 강의 자료와 외부 지식의 충돌 가능성을 관리하게 했다.

## 우선 확장한 허브 노트

- [[RAG]]
- [[LLM]]
- [[LangGraph]]
- [[Pandas DataFrame]]
- [[Django ORM Model]]
- [[useEffect]]
- [[Django QuerySet]]
- [[Embedding]]
- [[Vector Store]]
- [[React API Fetch]]
- [[Docker Compose]]

## 남은 보강 후보

- 각 강의 실습 코드에서 대표 예제를 Permanent Note의 예제 섹션으로 더 직접 연결한다.
- 프로젝트 적용 로그를 실제 프로젝트별로 분리한다.
- RAG 평가용 질문 세트와 검색 실패 사례를 [[질문 인박스]]에서 관리한다.

## 검증 메모

- 이 리포트는 재적용 스크립트가 파일 상태를 집계해 생성했다.
- 최종 완료 전 별도 검증 명령으로 빈 파일, frontmatter, wikilink를 다시 확인한다.
"""
    fm = frontmatter(note_type="moc", status="migration-report", tags=["llm_wiki", "migration", "moc"])
    write(KNOWLEDGE / "Maps of Content" / "LLM Wiki 전환 리포트.md", fm + report_body)


def main() -> int:
    apply_frontmatter_and_standard_sections()
    apply_expanded_notes()
    enhance_mocs()
    write_operating_docs()
    update_readme()
    write_report()
    # The first report write fixes this file's own status; the second report
    # captures the final distribution including the migration-report status.
    write_report()
    md_files = list(KNOWLEDGE.rglob("*.md"))
    print(json.dumps({
        "markdown_files": len(md_files),
        "empty_files": sum(1 for p in md_files if p.stat().st_size == 0),
        "status_distribution": dict(sorted(status_distribution().items())),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
