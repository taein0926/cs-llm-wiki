# [Deliverable 3] PRD 및 제품 사양서 (Product Requirements Document)

## 1. 프로젝트 개요 및 핵심 목표
본 프로젝트의 목표는 인간과 AI 에이전트가 공동으로 운영하며, 스스로 지식을 확장하고 구조적 결함을 검수하는 **'MCP 기반 Intelligent CS Wiki'**를 구축하는 것이다.

### 1.1 아키텍처 비전
단순한 문서 저장소를 넘어, **Model Context Protocol(MCP)**을 통해 에이전트가 파일 시스템과 외부 데이터에 직접 접근하고 제어하는 지능형 지식 생태계를 지향한다. 에이전트는 지식의 '생성'에 그치지 않고, 문서 간의 '연결'과 '검수'를 자동화하여 지식의 엔트로피를 낮추고 가용성을 극대화한다.

## 2. 시스템 액터 및 유스케이스 (System Actors)

### 2.1 Human Maintainer (인간 관리자)
- **역할**: 지식의 원천(Raw Data) 제공 및 최종 의사결정자.
- **주요 유스케이스**:
  - 원시 데이터(Raw txt) 투고.
  - 에이전트가 생성한 위키 초안 검토 및 최종 승인.
  - '인간 보호 구역(Human Protected Section)' 내 주석 관리.

### 2.2 Gemini Agent (컨텍스트 분석 및 인덱서)
- **역할**: 대규모 컨텍스트 이해 및 지식 그래프 구축.
- **주요 유스케이스**:
  - Raw 데이터 분석 및 엔티티 추출.
  - 문서 간 상호 참조(Cross-Reference) 링크 자동 생성.
  - `docs/wiki/` 내의 전체 컨텍스트 인덱싱.

### 2.3 Claude Agent (린터 및 검수자)
- **역할**: 품질 관리 및 기술적 정합성 검사.
- **주요 유스케이스**:
  - `page_template.md` 스키마 준수 여부 검사.
  - 위키 문서 내 기술적 논리 오류 및 중복 검수.
  - 유지보수 로그(LLM Maintenance Log) 업데이트 및 이력 관리.

## 3. 핵심 MVP 기능 및 기술 규격 명세

### 3.1 Auto-Interlinker
- **기능**: 새로운 위키 문서 생성 또는 업데이트 시, 기존 문서들과의 연관성을 분석하여 마크다운 내부 링크(`[[개념]]`)를 자동 생성한다.
- **규격**:
  - `docs/wiki/` 디렉토리 내의 파일 제목(Title)을 인덱싱하여 키워드 매칭.
  - 개념적 유사도가 높은 항목을 '연관 항목(Relationships)' 섹션에 추천 및 삽입.

### 3.2 MCP Tool 1: File I/O (read_wiki / write_wiki)
- **기능**: 에이전트가 로컬 파일 시스템의 위키 페이지를 직접 읽고 수정할 수 있는 권한을 제공한다.
- **기술 규격**:
  - `read_wiki(path)`: 지정된 위키 경로의 마크다운 콘텐츠 반환.
  - `write_wiki(path, content)`: 스키마 검증 후 위키 문서 기록. `Human Protected` 섹션 보호 로직 포함 필수.

### 3.3 MCP Tool 2: Knowledge Extender (cve_searcher)
- **기능**: 보안 취약점 관련 문서 작성 시, 외부 CVE(Common Vulnerabilities and Exposures) 데이터베이스를 조회하여 최신 정보를 주입한다.
- **기술 규격**:
  - `search_cve(keyword)`: (가상/실제) API를 통해 키워드와 관련된 최신 CVE ID, 심각도(Severity), 요약 정보를 반환.
  - 반환된 데이터를 위키의 '상세 내용' 또는 '비고' 섹션에 형식화하여 자동 삽입.

### 3.4 Claude Linter & Log Generator
- **기능**: 문서의 구조적 무결성을 검사하고 변경 이력을 관리한다.
- **기술 규격**:
  - **Linter**: `docs/scheme/page_template.md`에 정의된 섹션(Frontmatter, Overview, Details, Relationships, Notes, Log) 존재 여부 및 순서 검사.
  - **Log Generator**: 변경 사항 발생 시 `LLM Maintenance Log` 테이블에 [Date, Agent, Action, Description] 형식을 유지하며 행(Row) 추가.

## 4. 데이터 흐름 및 보안 정책
- **보호 구역 정책**: `<!-- [Human Protected: Start] -->` 와 `<!-- [Human Protected: End] -->` 사이의 내용은 에이전트가 어떠한 경우에도 덮어쓰거나 삭제할 수 없다.
- **스키마 우선순위**: 모든 문서는 `docs/scheme/page_template.md`를 최우선 스펙으로 따르며, 린트 오류 발생 시 에이전트는 즉시 수정을 시도해야 한다.
