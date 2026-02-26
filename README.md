# Orchestration System

> 최종 수정: 2026-02-27

Claude Code 기반 멀티 프로젝트 오케스트레이션 시스템 **v3.3.1**

---

## 개요

| 항목 | 수치 |
|------|------|
| 에이전트 | 24개 (4팀 + 허브 + 리좀 연결자 + 크로스팀 유틸리티) |
| 팀 | 4팀 + 허브 (ops, build, analyze, maintain + meta-orchestrator) |
| 스킬 | 14개 |
| Hooks | 8종 (SessionStart/End, Pre/PostToolUse, PreCompact/PostCompact, TeammateIdle, TaskCompleted) |
| 관리 프로젝트 | 5개 (orchestration, portfolio, tech-review, tech-review-blog, monet-lab) |

---

## 디렉토리 구조 (Flat Root)

```
orchestration/
├── *.md (12개)       # Living Docs — 루트에서 바로 접근
│   ├── STATE.md      # 시스템 인벤토리 SoT
│   ├── CHANGELOG.md  # 버전 이력
│   ├── KNOWLEDGE.md  # 규칙, 패턴
│   ├── PLANNING.md   # ADR (설계 결정)
│   ├── REFERENCE.md  # 종합 가이드
│   ├── ROADMAP.md    # 개발 계획
│   ├── METRICS.md    # 시스템 지표
│   ├── TODO.md       # 작업 관리
│   ├── decisions.md  # 결정 추적
│   ├── session-summary.md  # 세션 요약
│   └── pending.md    # 미반영 결정
├── _history/         # 시간순 기록 (읽기 전용)
│   ├── logs/         # 세션 로그
│   ├── plans/        # 설계 문서
│   ├── evidence/     # 버전별 검증 기록
│   └── archive/      # 아카이브
├── _prompts/         # 외부 AI 프롬프트
│   ├── claude/, gemini/, gpt/, perplexity/
├── _auto/            # 자동 관리 (에이전트 전용)
│   ├── live-context.md
│   └── .chain-temp/
├── scripts/          # 훅 스크립트
└── .claude/          # Claude Code 설정
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
| 구현 | implement → code-reviewer(Opus) → commit-writer(Haiku) → project-linker(Sonnet) → living docs |
| 배포 | pf-deployer → security-auditor → 사용자 확인 → push |
| 추출/검증 (v3.3) | Gemini 추출(벌크) + Codex 추출(정밀) → Claude verify barrier(3단계) → 사용 |
| 디스패치 | /dispatch → context-linker(Haiku) → meta-orchestrator(Opus) → 팀 활성화 |
| 압축 | compressor 9단계 → orch-doc-writer(항상) → doc-syncer |
| 세션 전환 (v3.3) | verify → sync-all → compressor → context-linker → "새 세션 준비 완료" |

---

## Quick Start

```
1. /dispatch         — 팀 추천 + 작업 방향
2. /morning          — 전체 브리핑 (미커밋, TODO, 미반영)
3. 작업 시작         — 해당 에이전트 체인 실행
```

---

## 문서

- [CHANGELOG](CHANGELOG.md) — 버전별 변경 이력
- [REFERENCE](REFERENCE.md) — 종합 가이드
- [ROADMAP](ROADMAP.md) — 개발 계획
- [KNOWLEDGE](KNOWLEDGE.md) — 규칙, 패턴, 모범 사례

---

_v3.3.1 · 최종 수정: 2026-02-27_
