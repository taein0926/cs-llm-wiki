# PLAN: LLM Wiki Prototype

본 프로젝트는 인간과 LLM이 협력하여 지식을 구조화하고 유지보수하는 마크다운 기반 위키 시스템의 프로토타입입니다. 가공되지 않은 텍스트 데이터를 LLM을 통해 정제하고, 정해진 스키마에 따라 위키 문서를 자동 생성 및 관리합니다.

## 1. 프로젝트 개요
- **목적**: 흩어져 있는 raw 데이터를 일관된 형식의 위키 문서로 자동 변환하고 관리 효율성을 증대.
- **핵심 컨셉**: 
    - **LLM-Driven Extraction**: 자연어 텍스트에서 주요 정보를 추출하여 구조화.
    - **Human-in-the-loop**: 생성된 마크다운 문서를 인간이 수정하고, LLM이 이를 학습하거나 반영하는 구조(지향).
    - **Schema-Based**: 모든 문서는 정의된 템플릿/스키마를 따름.

## 2. 시스템 아키텍처
- **Input Layer**: `data/` 폴더 내의 raw 텍스트 파일 (.txt, .md).
- **Processing Layer (Pipeline)**:
    - **Parser**: 원본 텍스트 읽기 및 전처리.
    - **LLM Client**: Prompt Engineering을 통해 텍스트를 JSON 등 구조화된 데이터로 변환.
    - **Generator**: 구조화된 데이터를 마크다운 위키 형식으로 렌더링.
- **Output Layer**: 
    - `docs/wiki/`: 최종 생성된 위키 페이지.
    - `docs/archive/`: 이전 버전의 위키 페이지 저장.
    - `docs/scheme/`: 위키 문서의 구조를 정의하는 스키마 파일.

## 3. 기술 스택
- **언어**: Python 3.10+
- **LLM**: OpenAI GPT-4o 또는 Google Gemini Pro API
- **설정 관리**: YAML/JSON
- **문서 형식**: Markdown

## 4. 로드맵
1. **Phase 1: Foundation**: 프로젝트 구조 확립 및 기본 스키마 정의.
2. **Phase 2: Core Pipeline**: LLM 연동 및 텍스트-위키 변환 엔진 개발.
3. **Phase 3: Versioning**: 문서 업데이트 시 자동 아카이빙 및 비교 로직 추가.
4. **Phase 4: Optimization**: 일괄 처리(Batch) 기능 및 CLI 도구 완성.
