# F. 외부 연동

## F1. gws Google Workspace CLI
- **소스**: @sawyerhood X + GitHub (googleworkspace/cli)
- **설치**: `npm install -g @googleworkspace/cli`
- **인증**: `gws auth login --scopes gmail,calendar,drive`
- **핵심 특징**:
  - Google Discovery Service에서 실시간으로 API 문서 읽어 명령어 자동 생성
  - 모든 응답 JSON 형식 (`--format json`) — 에이전트 통합 용이
  - 100+ 에이전트 스킬 내장
- **30+ 스킬 카테고리**: gmail(triage/send/watch), calendar(agenda/insert), drive(upload), docs(write), sheets(read/append), chat(send), forms, keep, meet, modelarmor
- **gmail +triage**: `gws gmail +triage --max 5 --query 'from:boss' --format json` — 읽기 전용 inbox 요약
- **calendar +agenda**: `gws calendar +agenda --today --format table` — 오늘 일정
- **Model Armor**: 프롬프트 인젝션 방지 (sanitize-prompt/sanitize-response)
- **안전**: triage/agenda는 read-only, send/insert는 별도 스킬
- **적용**: Gmail/Calendar → mcp-memory 자동 파이프라인. daily-memo 확장

## F2. Vercel CLI Marketplace
- **소스**: Vercel changelog
- **3단계**: discover (탐색) → guide (설정 가이드) → add (설치)
- **에이전트 최적화**: `--format=json` 비대화형 출력, 약관 동의만 인간 개입
- **구체적 사용**:
  ```bash
  vercel integration discover --format=json
  vercel integration add neon --format=json
  vercel integration add upstash/upstash-redis -m primaryRegion=iad1 --format=json
  ```
- **적용**: portfolio 배포 시 필요 서비스 자동 탐색/설치

## F3. Playwright CLI Wrapper
- **소스**: OpenAI curated skills `playwright`
- **래퍼 스크립트**: `$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh`
- **핵심 워크플로우**: open → snapshot(refs 획득) → interact(refs 사용) → re-snapshot(변경 후) → capture(screenshot/pdf)
- **snapshot 재취득 시점**: 네비게이션, UI 변경, 모달, 탭 전환 후
- **적용**: 현재 Playwright MCP 사용 중. CLI wrapper 패턴으로 비-Claude 에이전트도 브라우저 제어 가능

## F4. GitNexus — 코드베이스 → 지식 그래프
- **소스**: @MillieMarconnni X
- GitHub 리포를 시각적 그래프 구조로 변환, AI 에이전트와 대화형 상호작용
- 서버/설정 없이 즉시 사용
- **적용 우선순위**: 낮음 (학습 목적). 우리 6개 프로젝트 시각화에 활용 가능

## F5. AgentOS MCP 서버 자기 노출
- **소스**: agno-agi/agentos-docker-template
- `enable_mcp_server=True` → FastMCP로 자기 자신을 MCP 서버로 노출
- 21개 MCP 도구 자동 생성: `list_agents`, `run_agent`, `search_knowledge`, `list_memories` 등
- 다른 AI 에이전트가 이 AgentOS를 MCP 서버로 사용 — 에이전트 간 합성
- **적용**: mcp-memory를 MCP 서버로 노출 (이미 구현됨). 오케스트레이션도 MCP 서버화 가능

## F6. Pal 스케줄 태스크 5개
- **소스**: agno-agi/pal 소스코드
- | 태스크 | 스케줄 | 설명 |
  |--------|--------|------|
  | daily_briefing | 평일 8AM | 캘린더+이메일+우선순위 |
  | inbox_digest | 평일 12PM | 오전 이메일 요약 |
  | weekly_review | 금 5PM | 주간 리뷰 → context/meetings/ 저장 |
  | context_refresh | 매일 8AM | 컨텍스트 파일 재인덱싱 |
  | learning_summary | 월 10AM | 학습 패턴 요약 |
- **구현**: `ScheduleManager.create()` → DB cron 등록 → 폴러가 due 시 HTTP 요청 → 자연어 프롬프트
- **결과 전파**: 모든 태스크가 Slack #pal-updates에 결과 포스팅
- **적용**: 현재 Task Scheduler 3개(YouTube/Twitter/Bookmark). Pal 패턴으로 daily briefing/weekly review 추가 가능
