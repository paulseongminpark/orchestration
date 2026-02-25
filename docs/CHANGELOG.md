# Orchestration System Changelog

---

## v3.3 — Codex/Gemini CLI 통합 강화 (2026-02-25)

### 추가
- Codex CLI 설정: instructions.md(글로벌 페르소나), config.toml 프로필 3종(review/extract/verify), prompts 3종
- Gemini CLI 설정: GEMINI.md(글로벌 페르소나), 커스텀 스킬 4종(system-scanner/project-scanner/state-scanner/news-verifier)
- Claude Code 스킬 3종: /context-scan(컨텍스트 오프로딩), /tr-verify(tech-review QA), /cross-review(병렬 코드 리뷰)
- Verify Barrier: 모든 외부 CLI 출력에 3단계 검증(구조→스팟체크→반박)
- _meta 블록: 외부 CLI JSON 출력에 검증용 메타데이터 강제
- 에비던스 문서: docs/evidence/v3.3/diagram.md + members-skills.md (전체 시스템 카탈로그)
- 세션 전환 체인: verify→sync-all→compressor→linker (건너뛰기 금지, CLAUDE.md + KNOWLEDGE.md 반영)

### 변경
- gemini-analyzer: 코드베이스 분석 → 벌크 추출기(컨텍스트 오프로딩 + 웹 검색)
- codex-reviewer: 8관점 설계 결함 → 정밀 검증기(diff 리뷰 + 포맷 QA + git 추출)
- ai-synthesizer: 교차 검증 합성 → adversarial verifier(completeness + 반박 검증)
- meta-orchestrator: Sonnet → Opus 승격 (디스패치 판단 품질 강화)
- verify barrier: Opus 명시 (검증 말단 품질 보장)
- compressor: 타임스탬프 규칙 강화 (date +%H:%M 명령 필수, LLM 추정 금지)
- live-context hook: codex-cli, gemini-cli 경로 분류 추가
- 분석 체인 → 추출/검증 체인 재정의

### 설계 원칙
- Claude = 유일한 설계/결정권자. 외부 CLI = 사실 확인과 추출만.
- 해석이 아니라 추출. JSON 구조화 출력으로 신뢰성 확보.
- Gemini = 벌크(넉넉, 1M). Codex = 정밀(귀한, 5시간 롤링).
- 세션당 컨텍스트 절약 추정: ~170K 토큰 (88%)

### e2e 검증
- Codex extract 실전 테스트: 16커밋 JSON 추출 성공
- Gemini system-scanner 실전 테스트: 24개 에이전트 추출 성공 (절대 경로 수정 후)
- Opus e2e 23/23 ALL PASS

---

## v3.2 — 리좀형 팀 + SoT 확립 (2026-02-24)

### SoT 확립
- **CLAUDE.md**: 89줄→60줄 (v3.2 체인 규칙: 구현/디스패치/압축)
- **STATE.md**: 시스템 인벤토리 SoT (24에이전트, 11스킬, 4팀+허브)
- **KNOWLEDGE.md**: 366줄→~120줄 (패턴/규칙만, 인벤토리는 STATE 참조)
- **MEMORY.md**: 89줄→~55줄 (버전 이력 압축, 교훈/패턴 중심)
- **REFERENCE.md**: SYSTEM-GUIDE + USER-GUIDE 통합 (~300줄)

### 에이전트 (23→24)
- **doc-syncer** [Haiku] 신규: 3레이어 검증 (로컬/GitHub/HOME.md 링크)
- **project-context** [Sonnet]: pf-context 범용화 (프로젝트 파라미터)
- **compressor**: 7단계→9단계 (+orch-doc-writer +doc-syncer)
- 5개 dead code → alive: context-linker, project-linker, meta-orchestrator, orch-doc-writer, project-context

### 리좀형 4팀 + 디스패치 허브
- **ops**: morning-briefer(리드) + inbox-processor + tr-updater + tr-monitor
- **build**: code-reviewer(리드) + pf-reviewer + pf-deployer + ml-experimenter + security-auditor
- **analyze**: ai-synthesizer(리드) + gemini-analyzer + codex-reviewer
- **maintain**: compressor(리드) + doc-syncer + orch-doc-writer + orch-skill-builder
- **리좀 연결자**: context-linker, project-linker, live-context.md
- **크로스팀 유틸리티**: commit-writer, orch-state, project-context, content-writer

### 스킬 (13→11)
- 삭제: catchup, skill-creator, hook-creator
- 신규: **/dispatch** (catchup 흡수 + 팀 추천 + 세션 목표 설정)
- 강화: /morning (통합 대시보드: Inbox + live-context + 미반영 결정)

### 자동화
- **session-start.sh**: live-context 최근 10줄 출력 + OVERDUE 7일+ 마커
- **post-tool-live-context.sh**: auto-trim 100줄 캡 (헤더 4줄 + 최신 50줄)
- **live-context.md**: v3.2 리셋 (무한 팽창 → 100줄 캡)

### 정리
- 플러그인 4개 비활성화: coderabbit, feature-dev, code-simplifier, claude-md-management
- ai-config GitHub archived
- config/docs/ stale 9개 → docs/archive/
- SYSTEM-GUIDE + USER-GUIDE → docs/archive/ (REFERENCE.md로 대체)

### 체인 규칙 갱신
- 구현: +project-linker (커밋 후 크로스프로젝트 감지)
- 디스패치: /dispatch → context-linker → meta-orchestrator → 팀 활성화
- 압축: +orch-doc-writer(조건부) +doc-syncer(검증)

---

## v3.1 — Agent Teams & Linker System (2026-02-23)

### 신규 에이전트 (7개, 16→23)
- **context-linker** [Haiku, PROACTIVE]: 실시간 세션 간 맥락 공유 (live-context.md)
- **project-linker** [Sonnet, PROACTIVE]: 프로젝트 간 변경 영향 감지 → TODO/알림
- **meta-orchestrator** [Sonnet]: 세션 상태 분석 → 팀 디스패치 판단
- **inbox-processor** [Haiku]: daily-memo Inbox.md → TODO.md 분류
- **tr-monitor** [Haiku]: tech-review GitHub Actions 결과 수집
- **tr-updater** [Sonnet]: 프롬프트/키워드 업데이트, Smart Brevity 적용
- **ai-synthesizer** [Opus]: gemini+codex 교차 검증 통합 → agent.md 자동 반영

### 팀 (3개)
- **tech-review-ops**: tr-monitor → tr-updater → commit-writer
- **ai-feedback-loop**: gemini + codex → ai-synthesizer
- **daily-ops**: inbox-processor → orch-state → morning-briefer

### Hooks
- PostToolUse: live-context.md 자동 append (bash, 0 토큰)
- 타임스탬프: TZ 강제 제거 → 시스템 시간(KST) 직접 사용
- CLAUDE.md global 분류 추가

### 체인 규칙 추가 (5개)
- 분석 체인 강화 (ai-synthesizer)
- tech-review 체인, 일일 운영 체인, 디스패치 체인, 프로젝트 연동

### 문서
- CLAUDE.md, STATE.md, KNOWLEDGE.md, PLANNING.md, CHANGELOG.md 모두 v3.1 반영
- 설계: docs/plans/2026-02-23-agent-teams-design.md
- 구현: docs/plans/2026-02-23-agent-teams-impl.md

---

## v3.0 — 에이전틱 워크플로우 강화 (2026-02-23)

(v2.3 내용을 v3.0으로 승격)

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
- 02_ai_config 로컬 폴더 완전 삭제 (config → orchestration/config/로 흡수)
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
