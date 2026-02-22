# Orchestration System Changelog

---

## v2.3 — 진행 중 (2026-02-22)

### 완료
- MCP 서버 3개 제거 (memory, desktop-commander, sequential-thinking)
- example-skills 플러그인 비활성화 (document-skills와 100% 중복)
- docs/SYSTEM-GUIDE.md 종합 사용 가이드 작성 (16개 섹션)
- Gemini 교차 분석 완료 (10건 발견, 3건 처리)

### 미완 (다음 세션)
- 중복 플러그인 4개 비활성화 (code-review, commit-commands, skill-creator, hookify)
- playground 플러그인 비활성화
- 스킬-에이전트 통합 검토 (catchup+morning, creator 스킬들 → orch-skill-builder)
- SessionEnd JSONL 레이스컨디션 검토

---

## v2.2 — 완료 (2026-02-22)

### System Overhaul
죽은 자동화 수리 + 불필요 제거 + stale 문서 수정.

### 수리 (Phase 1)
- PostToolUse: `$CLAUDE_TOOL_RESULT` → stdin JSON에서 `tool_input.file_path` 파싱
- SessionEnd: `test -d context` 상대경로 → 절대경로
- PreCompact: 동일 상대경로 → 절대경로
- TeammateIdle: `exit 2` (차단) → `exit 0` (정보만)
- session-stop.sh: stdin 비어있을 때 최신 세션 파일 fallback + 디버그 로그 추가
- analyze-session.sh: `/tmp/` 하드코딩 → `${TMPDIR:-/tmp}/` MSYS 호환

### 삭제 (Phase 2)
- 에이전트: codex-reviewer (실행 불가), pf-orchestrator (비활성화)
- 스킬: token-check, token-mode, verify-log-format, verify-project-rules
- 스크립트: token-monitor.sh
- 규칙: git_workflow.md, token_budget.md (CLAUDE.md와 중복)
- orchestration: context/STATE.md (루트 STATE.md가 SoT), context/2026-02-22.md, config/docs/decisions.md
- 기타: ~/.claude/decisions.md, memory/Today.md, Notification 훅, Stop 훅
- verify 스킬에 verify-log-format + verify-project-rules 통합

### 수정 (Phase 3)
- settings.json: `language: "korea"` → `"ko"`
- todo 스킬: TODO 경로 02_ai_config → 01_orchestration/config/docs/
- sync-all 스킬: ai-config → dev-vault
- workflow.md: brainstorming → superpowers:brainstorming
- orchestration CLAUDE.md: Pages URL, Skills 목록 현행화
- KNOWLEDGE.md: 스킬 목록, STATE.md URL 수정
- HOME.md: 날짜, opcode 경로, Open Decisions 갱신
- decisions.md: codex 3건 취소, 구현완료 2건 반영
- config/docs/ 4건 최신화: ai-roles, claude-code-guide, daily-workflow, architecture
- MEMORY.md: 에이전트 수 v2.2 반영, v3.0 후보 → 구현완료 항목 정리

---

## v2.1 — 완료 (2026-02-22)

### 추가
- Gemini CLI 설치 완료 (`@google/gemini-cli` v0.29.5)
- gemini-analyzer 에이전트 연동 검증 완료
- Hooks 추가 2종: PreCompact (compact 전 /verify 권장), TaskCompleted (태스크 완료 알림)

### 결정
- GitHub App PR 자동 리뷰 설치 안 함 (불필요 판단)
- orchestrator 에이전트 비활성화 — Claude가 직접 라우팅 (중간 레이어 불필요)
- MCP 최소화 — CLI 대체 가능한 것은 설치 안 함 (GitHub=gh, Puppeteer=playwright)

---

## v2.0 — 완료 (2026-02-21)

### 추가
- cc-system 통합: crystalize-prompt, design-pipeline, skill-creator, subagent-creator, hook-creator
- C:\dev 볼트 git repo 초기화 → dev-vault GitHub 연결 (main 브랜치)
- Skills 11개 → 17개 신규: skill-creator, subagent-creator, hook-creator, catchup, gpt-review, commit-push-pr
- 버전 관리 체계 (CHANGELOG.md, ROADMAP.md)
- Rules 구조화: common-mistakes.md, workflow.md 추가
- MCP 2개 추가: sequential-thinking, memory
- session-summary.md 추가 (catchup 스킬 연동)
- 02_ai_config 로컬 폴더 완전 삭제 (config → orchestration/config/ 흡수)
- Agent Teams 활성화 (CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)

### 에이전트 14개 구축
**PROACTIVELY (4개)**
- code-reviewer [Opus], commit-writer [Haiku], orch-state [Sonnet], compressor [Sonnet]

**Portfolio (3개)**
- pf-context [Sonnet], pf-reviewer [Opus], pf-deployer [Sonnet]

**Orchestration (2개)**
- orch-doc-writer [Opus], orch-skill-builder [Opus]

**Monet-lab (2개)**
- ml-experimenter [Opus], ml-porter [Sonnet]

**Analysis (2개)**
- gemini-analyzer [Sonnet], security-auditor [Opus]

**Morning (1개)**
- morning-briefer [Haiku]

### Hooks (7종)
- Stop: 미커밋 변경사항 자동 차단 (작업 세션 보호)
- SessionStart: 작업 로그 브리핑 + git status 자동 출력
- SessionEnd: 세션 종료 시 /sync 권장 알림
- PreToolUse: 위험 명령어 차단 (rm -rf, force push 등)
- PostToolUse: context/*.md 수정 감지 → 커밋 전 확인
- TeammateIdle: 팀원 유휴 알림
- Notification: 작업 완료 알림

### 미완료 (v2 잔여)
- Obsidian Git Auto push interval 설정 (사용자 직접)

---

## v1.0 — 기준점 (2026-02-21)

### 시스템 구성

**글로벌 설정 (`~/.claude/`)**
- CLAUDE.md: Executor 원칙 (4줄 핵심 규칙)
- rules/: git_workflow.md, token_budget.md
- agents/: orchestrator.md (멀티 프로젝트 상태 동기화)

**Skills (11개)**
- 운영: morning, todo, sync-all, memory-review
- 문서: docs-review, research
- 토큰: token-check, token-mode
- 검증: verify, verify-project-rules, verify-log-format

**Scripts (5개)**
- analyze-session.sh: 세션 대화 분석 → pending.md
- sync-memory.sh: MEMORY.md 동기화 검증
- memory-review.sh: 주간 정리
- docs-review.sh: stale 문서 감지
- token-monitor.sh: 5분마다 토큰 체크

**Auto Memory System**
- Phase 1: SessionEnd Hook → analyze-session.sh → pending.md
- Phase 2: /sync-all → sync-memory.sh → MEMORY.md 검증 이동
- Phase 3: /memory-review → 주간 정리

**Orchestration Config (`orchestration/config/`)**
- claude/: hierarchy.md
- docs/: architecture.md, ai-roles.md, claude-code-guide.md, daily-workflow.md, decisions.md, git-workflow.md, philosophy.md
- gpt/, gemini/, perplexity/: master_prompt + snapshot

**Architecture**
- Claude Code = 유일한 쓰기 (Write/Edit)
- GPT/Gemini/Perplexity = 읽기 (GitHub Pages URL)
- Obsidian = 뷰어 (편집 금지)

### 리포지토리
- orchestration: paulseongminpark/orchestration (main)
- portfolio: paulseongminpark/portfolio (master)
- tech-review: paulseongminpark/tech-review (Jekyll)
- daily-memo: paulseongminpark/daily-memo

---

## v0.0 — 초기 (2026-02 이전)

ai-config 저장소에서 시작. orchestration/config/로 흡수 후 ai-config 폐기.
