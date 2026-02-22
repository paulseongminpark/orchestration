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
│   │   │   └── skills/             ← /sync, /handoff
│   │   ├── STATE.md                ← ★ SoT (단일 진실 소스, 루트)
│   │   ├── context\                ← 컨텍스트 문서
│   │   │   └── logs\YYYY-MM-DD.md  ← 상세 시간순 기록 (중앙)
│   │   ├── config\                 ← AI 설정/프롬프트 (구 ai-config 흡수)
│   │   │   ├── docs\               ← 시스템 문서
│   │   │   ├── gpt\
│   │   │   ├── gemini\
│   │   │   └── perplexity\
│   │   └── scripts\
│   │       └── copy-session-log.py ← Evidence 백업
│   ├── 02_portfolio\               ← Git repo (GitHub: portfolio_20260215)
│   │   ├── .claude\                ← Claude Code 설정
│   │   ├── context\STATE.md        ← ★ SoT
│   │   └── src\                    ← React + Vite 소스
│   ├── 03_tech-review\             ← tech-review 블로그 (Jekyll)
│   ├── 05_opcode\                  ← Tauri 앱
│   └── 99_archive\
│
├── 02_ai_config\                   ← ARCHIVED (orchestration/config/ 로 이전)
│   └── README.md                   ← "이동됨" 안내
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
    ├─ SessionEnd Hook #1 ──→ 프로젝트별 미커밋 현황 출력
    │
    ├─ SessionEnd Hook #2 ──→ /sync recommended 알림
    │
    ├─ SessionEnd Hook #3 ──→ analyze-session.sh ──→ pending.md
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

### Daily-Memo 파이프라인 (D-019)

```
핸드폰 Claude Code (cloud env)
    → claude/add-inbox-hello-71SP3 브랜치 → Inbox.md 누적

컴퓨터 /todo 실행:
    → 브랜치 Inbox.md 읽기 → main과 diff
    → 새 항목 → main merge → 로컬 TODO.md 반영
```

참고: D-019 — cloud env 제약으로 main 직접 push 불가, 브랜치 고정.

## GitHub 구성

| 로컬 | GitHub Repo | 유형 | Pages |
|------|------------|------|-------|
| 01_orchestration | orchestration | public | ✅ STATE.md 공개 |
| 02_portfolio | portfolio_20260215 | public | ✅ STATE.md 공개 |
| 02_ai_config | ai-config | private (ARCHIVED) | ❌ (orchestration/config/로 이전) |
| 03_tech-review/blog | tech-review | public | ✅ Jekyll 블로그 |
| — | portfolio (구) | archived | — |

## 관련 문서
- [[philosophy]] — 왜 이 구조인가
- [[git-workflow]] — Git 상세
- [[claude-code-guide]] — Claude Code 설정 상세
