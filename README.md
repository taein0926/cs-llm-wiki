# 🚀 MCP-based Intelligent CS Wiki (Project 2)

본 프로젝트는 인간과 AI 에이전트가 공동으로 운영하며, 스스로 지식을 확장하고 구조적 결함을 검수하는 **지능형 컴퓨터 과학(CS) 지식 베이스**입니다.

## 1. 프로젝트 배경 및 연구 (from Task 1)
### 1.1 LLM Wiki vs. 일반적인 RAG 시스템
기존의 RAG(Retrieval-Augmented Generation) 시스템은 단편적인 키워드 매칭을 통해 문서를 검색하지만, **LLM Wiki**는 다음과 같은 차별점을 가집니다.
- **상호 참조 지식 그래프**: 문서 간의 `[[내부 링크]]`를 통해 지식의 유기적 연결성을 시각화하고 탐색합니다.
- **에이전트 자율 관리**: 에이전트가 단순히 정보를 읽는 것에 그치지 않고, 지식의 결함을 수정하고 새로운 연관 관계를 스스로 구축합니다.
- **데이터 거버넌스**: 인간의 통찰이 담긴 구역을 보호하면서 AI의 자동화 효율을 극대화하는 하이브리드 운영 모델을 지향합니다.

## 2. 지식 도메인 (Target Domain)
- **운영체제(OS)**: 프로세스 관리, 메모리 구조, 커널 보안.
- **컴퓨터 네트워크**: TCP/IP 스택, 슬라이딩 윈도우, 흐름 제어.
- **컴퓨터 보안**: 버퍼 오버플로우, 취약점 분석, CVE 데이터 연계.

## 3. 핵심 기술 규격 (MCP Wiki Tools)
`src/tools/wiki_tools.py`에 구현된 내장형 MCP 도구들의 상세 기능입니다.

### 📂 File I/O Tools
- **`read_wiki(page_name)`**: `docs/wiki/` 경로의 마크다운 문서를 읽어 에이전트에게 전달합니다.
- **`write_wiki(page_name, content)`**: 에이전트가 생성한 지식을 기록합니다. **데이터 거버넌스 엔진**이 내장되어 있어 기존 문서의 `[Human Protected]` 구역을 감지하고 보존합니다.

### 🛡 Security Extension Tools
- **`search_cve(keyword)`**: 보안 도메인 특화 툴로, 가상의 CVE 데이터베이스를 조회하여 최신 취약점 정보를 위키 문서에 자동으로 주입합니다.

### 📑 Data Governance Policy
에이전트는 다음 태그 사이의 내용을 절대로 수정하거나 삭제할 수 없습니다.
```markdown
<!-- [Human Protected: Start] -->
인간 관리자의 고유 메모리 및 주석 영역
<!-- [Human Protected: End] -->
```

## 4. 시스템 아키텍처 및 역할 분담
- **Gemini Agent**: 대규모 컨텍스트 분석 및 문서 간 자동 상호 참조 링크 생성.
- **Claude Agent**: `page_template.md` 스키마 준수 여부 린팅 및 변경 이력 로그 관리.
- **Main Engine (`main.py`)**: Subprocess API를 통한 에이전트 간 오케스트레이션 수행.

## 5. 실행 방법 (Usage)

### 5.1 환경 준비
- Python 3.8+ 이상이 설치되어 있어야 합니다.
- 별도의 외부 라이브러리 의존성 없이 표준 라이브러리(os, re, sys 등)로 작동합니다.

### 5.2 MCP 툴 자체 테스트
내장된 데이터 거버넌스 및 CVE 검색 로직을 테스트하려면 다음 명령을 실행하십시오.
```bash
python src/tools/wiki_tools.py
```

### 5.3 메인 위키 엔진 실행
에이전트들이 Raw 데이터를 분석하여 위키를 생성하는 전체 파이프라인을 실행합니다.
```bash
python src/main.py
```

---
**Author**: CSE-3308 Project Team (AI Agent Managed)
**Last Updated**: 2026-06-14
