# 전체 아키텍처

## 시스템 개요

```
사용자 (판단/승인)
    │
    ├── GPT Plus ──────── 사고 확장, 전략, Canvas
    │                      ↓ Packet (Claude 지시문)
    ├── Claude Code ────── 실행 + 기록 (유일한 쓰기)
    │   ├── Git push ──→ GitHub ──→ GitHub Pages
    │   ├── STATE.md 갱신 (고수준 상태)
    │   ├── LOG append (상세 시간순 기록)
    │   └── Evidence 백업 (원본 대화)
    │                      ↑ GitHub Pages URL (읽기)
    ├── Gemini Pro ─────── 대량 검증 (100만 토큰)
    └── Perplexity Pro ─── 리서치 + 교차검증
```

## 폴더 구조

```
C:\dev\
├── 01_projects\                    ← 모든 프로젝트
│   ├── 01_orchestration\           ← Git repo (GitHub: orchestration)
│   │   ├── .claude\                ← Claude Code 설정
│   │   │   ├── CLAUDE.md           ← 프로젝트 컨텍스트
│   │   │   ├── settings.json       ← permissions + hooks
│   │   │   ├── skills/             ← /sync, /handoff, /status
│   │   │   └── agents/             ← architect, reviewer
│   │   ├── context\
│   │   │   ├── STATE.md            ← ★ SoT (단일 진실 소스)
│   │   │   └── logs\YYYY-MM-DD.md  ← 상세 시간순 기록 (중앙)
│   │   └── scripts\
│   │       └── copy-session-log.py ← Evidence 백업
│   ├── 02_portfolio\               ← Git repo (GitHub: portfolio_20260215)
│   │   ├── .claude\                ← Claude Code 설정
│   │   ├── context\STATE.md        ← ★ SoT
│   │   └── src\                    ← React + Vite 소스
│   └── 99_archive\
│
├── 02_ai_config\                   ← Git repo (GitHub: ai-config, private)
│   │                                  Obsidian 볼트
│   ├── docs/                       ← 이 문서들
│   ├── gpt/                        ← GPT 프롬프트 (스냅샷)
│   ├── gemini/                     ← Gemini 프롬프트 (스냅샷)
│   ├── perplexity/                 ← Perplexity 프롬프트 (스냅샷)
│   ├── claude/                     ← Claude 계층 설명
│   └── projects/                   ← Junction Points (읽기 전용 뷰)
│       ├── orchestration → 01_orchestration/context
│       └── portfolio → 02_portfolio/context
│
├── 03_evidence\                    ← 세션 로그 (로컬 전용, Git 추적 안 함)
│   ├── claude/orchestration/
│   ├── claude/portfolio/
│   └── chatgpt/
│
└── 99_archive\                     ← 아카이브 (구 AI_작업실 등)
```

### Jeff Su 방법론 적용

| 규칙 | 적용 |
|------|------|
| 5레벨 MAX | `C:\dev\01_projects\01_orchestration\context\STATE.md` = 5레벨 |
| 2자리 넘버링 | `01_projects`, `02_ai_config`, `03_evidence` |
| 99 = Archive | `99_archive` (프로젝트, 전역 모두) |
| 명확한 이름 | 폴더명만 봐도 내용 추론 가능 |

## 데이터 흐름

```
[Claude Code 작업]
    │
    ├─ SessionStart Hook ──→ /morning Skill ──→ 모든 STATE.md 읽기
    │                                             │
    │                                             └→ 자동 브리핑 (완료/진행/막힌것 + 추천)
    │
    ├─ STATE.md 수정 ──→ git commit ──→ post-commit hook ──→ auto push
    │                                                          │
    │                                        GitHub Pages ←────┘
    │                                            │
    │                    GPT/Gemini/Perplexity ←──┘ (URL로 읽기)
    │
    ├─ PostToolUse Hook ──→ "STATE 변경됨. /sync 실행 권장."
    │
    ├─ Stop Hook #1 ──→ copy-session-log.py ──→ 03_evidence/
    │                    (Layer 3: 프롬프트 단위 세션 회고)
    │
    ├─ Stop Hook #2 ──→ STATE.md 미커밋 감지 → exit 1 차단
    │                    (/sync 강제 게이트)
    │
    └─ Stop Hook #3 ──→ analyze-session.sh ──→ pending.md
                         (Auto Memory: 세션 인사이트 자동 추출)
                              │
                         /sync-all 호출
                              │
                         sync-memory.sh ──→ MEMORY.md (검증 후 승격)
                              │
                         /memory-review (주간)
                              │
                         memory-review.sh ──→ MEMORY.md 정리
```

### Daily-Memo 파이프라인 (D-017)

```
[세션 시작]
    │
    └─ SessionStart Hook (settings.json)
        │
        ├─ clear hook ──→ /clear 실행 (컨텍스트 초기화)
        │
        └─ morning hook ──→ /morning Skill 실행
            │
            ├─ orchestration STATE.md 읽기
            ├─ portfolio STATE.md 읽기
            ├─ (확장 가능: 다른 프로젝트)
            │
            └─ 자동 브리핑 출력:
                완료 N / 진행 N / 막힌것 N
                추천: [다음 작업 제안]
```

**특징**:
- `/morning` 수동 입력 불필요
- 매 세션 시작 시 자동 현황 파악
- Haiku 모델로 토큰 효율적

## GitHub 구성

| 로컬 | GitHub Repo | 유형 | Pages |
|------|------------|------|-------|
| 01_orchestration | orchestration | public | ✅ STATE.md 공개 |
| 02_portfolio | portfolio_20260215 | public | ✅ STATE.md 공개 |
| 02_ai_config | ai-config | private | ❌ |
| — | portfolio (구) | archived | — |

## 관련 문서
- [[philosophy]] — 왜 이 구조인가
- [[git-workflow]] — Git 상세
- [[claude-code-guide]] — Claude Code 설정 상세
