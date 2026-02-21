# Orchestration System Changelog

---

## v2.0 — 완료 (2026-02-21)

### 추가
- cc-system 통합: crystalize-prompt, design-pipeline, skill-creator, subagent-creator, hook-creator
- C:\dev 볼트 git repo 초기화 → dev-vault GitHub 연결 (main 브랜치)
- Skills 11개 → 14개 (skill-creator, subagent-creator, hook-creator 신규)
- 버전 관리 체계 (CHANGELOG.md, ROADMAP.md)
- Worker 에이전트 11개 구축:
  - orchestrator (업그레이드: 라우터 전용 Haiku)
  - morning-briefer (프로젝트 현황 + TODO 통합 브리핑)
  - pf-context, pf-reviewer [Opus], pf-deployer (portfolio 전용)
  - orch-state, orch-doc-writer [Opus], orch-skill-builder [Opus] (orchestration 전용)
  - code-reviewer [Opus], commit-writer, compressor (cross-project)
- /morning 스킬 → morning-briefer 에이전트 연동 + TODO 포함

### 미완료 (v2 잔여)
- Obsidian Git Auto push interval 설정 (사용자 직접)
- monet-lab Worker 2개 (ml-experimenter, ml-porter) — 대기 중

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
