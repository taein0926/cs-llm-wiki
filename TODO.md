# TODO: LLM Wiki Prototype 구현 체크리스트

## Phase 1: 기반 설정 (Foundation)
- [ ] `docs/scheme/default_scheme.json` 정의 (위키 필수 항목 필드 정의)
- [ ] `config/config.yaml` 템플릿 작성 (API Key, Prompt 설정)
- [ ] `requirements.txt` 작성 (openai, google-generativeai, pyyaml 등)
- [ ] `.env` 파일 설정 가이드 작성 (보안 정보 관리)

## Phase 2: 파이프라인 엔진 개발 (Core Engine)
- [ ] `src/utils/file_handler.py`: 파일 읽기/쓰기 모듈 구현
- [ ] `src/core/llm_client.py`: LLM API 요청 및 응답 처리 로직
- [ ] `src/core/parser.py`: LLM 응답을 파싱하여 스키마 검증
- [ ] `src/core/generator.py`: 데이터를 마크다운 템플릿으로 변환

## Phase 3: 문서 관리 및 유지보수 (Management)
- [ ] `src/core/archiver.py`: 기존 파일 변경 시 `docs/archive/`로 이동하는 기능
- [ ] 중복 체크 로직: 동일 항목에 대한 처리 방식(덮어쓰기 vs 업데이트) 구현
- [ ] `docs/wiki/` 내 인덱스 페이지(Home.md) 자동 갱신 기능

## Phase 4: 테스트 및 사용자 인터페이스 (Refinement)
- [ ] 샘플 raw 데이터(`data/sample.txt`)를 이용한 전체 파이프라인 테스트
- [ ] `main.py`: 실행 인자를 받는 CLI 진입점 개발
- [ ] 에러 핸들링: API 할당량 초과, 잘못된 데이터 형식 대응

## Phase 5: 최종 검증 (Finalization)
- [ ] 생성된 위키 문서의 가독성 및 링크 연결 확인
- [ ] 프로젝트 결과 보고서 작성을 위한 로그 및 통계 기능 추가
