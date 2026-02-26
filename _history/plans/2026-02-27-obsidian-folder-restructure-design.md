# Design: Obsidian Folder Restructure — orchestration

_Date: 2026-02-27_
_Status: Approved_
_Scope: 01_orchestration only (Phase 1)_

## Problem

- 문서가 context/, docs/, config/ 3곳에 분산
- Living Doc과 Archive 구분 불명확
- config/ 폴더 역할 모호 (AI 프롬프트 + TODO 혼재)
- 경로가 깊어 Obsidian 탐색 불편
- 기록 에이전트(compressor, context-linker) 대상 파일 한정적

## Goal

- **Living Doc**: 폴더 열면 시스템 전체가 바로 보임
- **삭제 없음**: 모든 기존 파일은 archive로 이동
- **2단계**: 폴더 구조 최적화 → 기록 에이전트 대상 파일 수정

## Design: Flat Root + _history

### Root Living Docs (12개)

| 파일 | 현재 위치 | 역할 |
|------|----------|------|
| STATE.md | root (유지) | SoT 인벤토리 |
| CHANGELOG.md | docs/ → root | 버전 변경 이력 |
| KNOWLEDGE.md | context/ → root | 규칙/패턴 |
| REFERENCE.md | docs/ → root | 종합 가이드 |
| ROADMAP.md | docs/ → root | 개발 계획 |
| PLANNING.md | context/ → root | 아키텍처 ADR |
| METRICS.md | context/ → root | 성능 지표 |
| decisions.md | context/ → root | 열린 결정 추적 |
| session-summary.md | context/ → root | 세션 요약 (compressor) |
| pending.md | context/ → root | 패턴 후보 (compressor) |
| TODO.md | config/docs/ → root | 전체 할 일 |
| README.md | root (유지) | 프로젝트 소개 (v3.3.1 갱신) |

### _history/ (시간순 기록 통합)

```
_history/
├── logs/           ← context/logs/ + logs/ 통합
├── plans/          ← docs/plans/ 이동
├── evidence/       ← context/evidence/ + docs/evidence/ 통합
│   ├── v3.2/
│   ├── v3.3/
│   └── v3.3.1/
└── archive/        ← context/archive/ + docs/archive/ + config snapshots
    ├── docs/       ← docs/archive/ (SYSTEM-GUIDE, USER-GUIDE 등 10개)
    ├── context/    ← context/archive/ (SNAPSHOT 등)
    └── config/     ← _SNAPSHOT.md 3개 + 기타
```

### _prompts/ (외부 AI 프롬프트)

```
_prompts/
├── claude/         hierarchy.md
├── gemini/         master_prompt.md, validation_checklist.md
├── gpt/            master_prompt.md, projects/cowork.md, projects/portfolio.md
└── perplexity/     master_prompt.md, research_template.md, spaces/*.md
```

### _auto/ (Claude Code 자동 관리)

```
_auto/
├── live-context.md     ← PostToolUse hook 자동 append
└── .chain-temp/        ← 에이전트 임시 결과 오프로딩
```

### 변경 없음

- `.claude/` — Claude Code 에이전트/스킬/설정
- `scripts/` — 유틸리티 스크립트
- `.nojekyll`, `_config.yml` — GitHub Pages 설정

## 이동 맵 (구체적)

### context/ → root
- KNOWLEDGE.md → root
- PLANNING.md → root
- METRICS.md → root
- decisions.md → root
- pending.md → root
- session-summary.md → root

### context/ → _history/
- logs/ → _history/logs/
- evidence/ → _history/evidence/
- archive/ → _history/archive/context/

### context/ → _auto/
- live-context.md → _auto/live-context.md
- .chain-temp/ → _auto/.chain-temp/

### docs/ → root
- CHANGELOG.md → root
- REFERENCE.md → root
- ROADMAP.md → root

### docs/ → _history/
- plans/ → _history/plans/
- evidence/ → _history/evidence/ (v3.3, v3.3.1 통합)
- archive/ → _history/archive/docs/

### config/ → _prompts/
- claude/ → _prompts/claude/
- gemini/ → _prompts/gemini/ (master_prompt, validation_checklist)
- gpt/ → _prompts/gpt/
- perplexity/ → _prompts/perplexity/

### config/ → root
- docs/TODO.md → root/TODO.md

### config/ → _history/archive/
- gemini/_SNAPSHOT.md → _history/archive/config/
- gpt/_SNAPSHOT.md → _history/archive/config/
- perplexity/_SNAPSHOT.md → _history/archive/config/

### 삭제 대상 (비게 되는 폴더)
- context/ (전부 이동 후)
- docs/ (전부 이동 후)
- config/ (전부 이동 후)
- logs/ (루트 레벨, _history/logs/로 통합)

### 기타
- t_v2" 파일: 내용 확인 후 archive
- README.md: v3.2 → v3.3.1 갱신

## Phase 2 (별도 세션)

폴더 구조 완료 후, 기록 에이전트들의 대상 파일 경로 수정:
- compressor → session-summary.md, pending.md (새 경로)
- context-linker → _auto/live-context.md
- orch-doc-writer → root CHANGELOG.md
- session-start.sh → root decisions.md, _auto/live-context.md
- post-tool-live-context.sh → _auto/live-context.md
- pre-compact.sh → _auto/.chain-temp/

## Success Criteria

1. Obsidian에서 01_orchestration 열면 Living Doc 12개가 바로 보임
2. context/, docs/, config/ 폴더 없음 (비어서 삭제)
3. 모든 기존 파일 보존 (_history/archive/)
4. 기록 에이전트 정상 동작 (Phase 2)
