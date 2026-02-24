# Orchestration System

Claude Code 기반 멀티 프로젝트 오케스트레이션 시스템 **v3.2**

---

## 개요

| 항목 | 수치 |
|------|------|
| 에이전트 | 24개 (4팀 + 허브 + 리좀 연결자 + 크로스팀 유틸리티) |
| 팀 | 4팀 + 허브 (ops, build, analyze, maintain + meta-orchestrator) |
| 스킬 | 11개 |
| Hooks | 7종 (SessionStart/End, Pre/PostToolUse, PreCompact, TeammateIdle, TaskCompleted) |
| 관리 프로젝트 | 5개 (orchestration, portfolio, tech-review, tech-review-blog, monet-lab) |

---

## 디렉토리 구조

```
orchestration/
├── context/          # 시스템 지식 베이스
│   ├── KNOWLEDGE.md  # 규칙, 패턴, 에이전트 목록
│   ├── PLANNING.md   # ADR (설계 결정 기록)
│   ├── decisions.md  # 결정 추적
│   └── live-context.md  # 실시간 갱신 컨텍스트 (Linker System)
├── docs/             # 문서
│   ├── SYSTEM-GUIDE.md
│   ├── USER-GUIDE.md
│   ├── CHANGELOG.md
│   └── ROADMAP.md
├── config/           # AI 모델 설정 (claude/gpt/gemini/perplexity)
└── hooks/            # 자동화 훅 스크립트
```

---

## 핵심 기능

- **에이전트 체인**: 구현 → 리뷰 → 커밋 → 문서 자동 체인
- **Linker System**: context-linker + project-linker + live-context.md 실시간 맥락 주입
- **Meta-orchestrator**: 팀 활성화 및 태스크 디스패치 자동화
- **Agent Teams**: tech-review-ops, ai-feedback-loop, daily-ops 팀 단위 운영
- **Hooks System**: 도구 사용 전후 자동 검증 및 상태 추적
- **Living Docs**: STATE.md / CHANGELOG.md / KNOWLEDGE.md 자동 유지

---

## 에이전트 체인

| 체인 | 흐름 |
|------|------|
| 구현 | implement → code-reviewer → commit-writer → living docs |
| 배포 | pf-deployer → security-auditor → 사용자 확인 → push |
| 분석 | gemini + codex (병렬) → ai-synthesizer → agent.md 반영 |
| Tech Review | tr-monitor → tr-updater → commit-writer |
| 일일 운영 | inbox-processor → orch-state → morning-briefer |
| 디스패치 | catchup → meta-orchestrator → 팀 활성화 |

---

## Quick Start

```
1. /catchup          — 현재 상태 파악
2. /orch-state       — 오늘 작업 브리핑
3. 작업 시작         — 해당 에이전트 체인 실행
```

---

## 문서

- [SYSTEM-GUIDE](docs/SYSTEM-GUIDE.md) — 시스템 전체 구조 설명
- [USER-GUIDE](docs/USER-GUIDE.md) — 사용자 운영 가이드
- [CHANGELOG](docs/CHANGELOG.md) — 버전별 변경 이력
- [ROADMAP](docs/ROADMAP.md) — 개발 계획

---

_v3.1 · 2026-02-24_
