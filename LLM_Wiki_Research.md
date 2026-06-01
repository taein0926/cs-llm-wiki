# LLM Wiki Research: Human-LLM Collaboration in Knowledge Bases

본 문서는 '인간과 LLM이 함께 유지보수하는 마크다운 기반 위키'에 대한 조사 내용을 정리한 리포트입니다.

## 1. LLM Wiki의 핵심 개념 (The "Karpathy Pattern")
안드레이 카파시(Andrej Karpathy)가 제안한 이 개념은 단순히 AI와 채팅하는 것을 넘어, AI가 지속적이고 구조화된 지식 창고(Knowledge Base)를 관리하게 하는 방식입니다.

- **문제 의식**: 사람이 직접 관리하는 위키는 관리가 번거로워 시간이 지남에 따라 정보가 낡고 연결이 끊어지는 '관리 피로(Bookkeeping Fatigue)' 현상이 발생함.
- **해결책**: LLM을 '연구 사서(Research Librarian)'로 고용하여 마크다운 파일들의 연결과 정리를 자동화함.

## 2. 시스템 구조 (Architecture)
대부분의 LLM Wiki 시스템은 다음과 같은 폴더 구조를 따릅니다.

- **`raw/`**: 가공되지 않은 소스 데이터 (PDF, 웹 스크랩, 녹취록 등). 수정 불가능한 원본 보관소.
- **`wiki/`**: LLM에 의해 정제되고 서로 연결된 마크다운 파일들.
- **`index.md`**: 위키의 전체 목차 및 진입점.
- **`CLAUDE.md` / `AGENTS.md`**: 위키의 규칙, 스키마, 작성 스타일을 정의한 지침 파일.

## 3. 워크플로우 (Workflow)
1. **Ingest (섭취)**: 새로운 raw 데이터를 폴더에 추가.
2. **Compile (편찬)**: LLM이 데이터를 분석하여 새로운 페이지를 만들거나 기존 페이지를 업데이트.
3. **Lint (검사)**: 논리적 모순, 끊어진 링크, 스키마 위반 등을 LLM이 스스로 검사.
4. **Query (조회)**: 사용자는 원본 데이터가 아닌, 이미 잘 정리된 '위키'를 대상으로 질문하거나 정보를 탐색.

## 4. 인간과 LLM의 역할 분담
- **인간 (Director)**: 정보의 소스를 제공하고, 위키의 목적과 방향성을 설정하며, 최종 결과물을 검토(Curation).
- **LLM (Librarian)**: 요약, 태깅, 상호 참조(Cross-linking), 데이터 정합성 유지 등 반복적이고 지루한 '관리 작업' 수행.

## 5. 주요 도구 및 기술 스택
- **Obsidian**: 위키 문서를 시각화(Graph View)하고 탐색하는 최적의 뷰어.
- **Markdown**: 기계와 인간 모두에게 읽기 쉽고, Git을 통한 버전 관리가 용이함.
- **MCP (Model Context Protocol)**: AI 에이전트가 로컬 파일 시스템에 직접 접근하여 읽고 쓸 수 있게 해주는 최신 프로토콜.
- **Gemini / Claude CLI**: 로컬 환경에서 파이프라인을 구축하여 자동화를 수행하는 핵심 엔진.

---
*Reference: Based on the "Karpathy's LLM Wiki" model and modern AI-Agent workflows (2024-2025).*
