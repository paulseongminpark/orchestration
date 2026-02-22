# Orchestration System v2.2 — 종합 사용 가이드

> 이 문서는 시스템의 모든 요소를 처음부터 끝까지 설명합니다.
> 마지막 갱신: 2026-02-22

---

## 1. 시스템 개요

이 시스템은 **Claude Code를 중심으로 여러 AI(GPT, Gemini, Perplexity)와 도구(Git, Obsidian, GitHub)를 통합 운영**하는 개인 개발 워크스페이스입니다.

```
C:\dev\                          ← 볼트 허브 (dev-vault, git: main)
├── HOME.md                      ← 중앙 허브 (Obsidian MOC)
├── CLAUDE.md                    ← 전역 규칙 (모든 프로젝트 공통)
├── 01_projects/
│   ├── 01_orchestration/        ← AI 오케스트레이션 (git: main)
│   ├── 02_portfolio/            ← 포트폴리오 사이트 (git: master)
│   ├── 03_tech-review/          ← 기술 리뷰 트래커
│   ├── 03_tech-review-blog/     ← Jekyll 블로그 (git: main)
│   └── 04_opcode/               ← Tauri 앱 (git: 별도)
├── 02_ai_config/                ← [ARCHIVED] → orchestration/config/
└── 03_evidence/                 ← 스크린샷, 세션 증거
```

### 핵심 원칙

| 원칙 | 설명 |
|------|------|
| **SoT = Git** | 진실의 원천은 Git. 모든 상태는 Git으로 추적 |
| **Claude Code = 유일한 쓰기** | 상태 문서(STATE.md 등)는 Claude Code만 수정 |
| **Obsidian = 읽기 전용 뷰어** | Obsidian에서 편집하면 충돌. Junction으로 연결해 보기만 |
| **외부 AI = 읽기만** | GPT/Gemini/Perplexity는 GitHub Pages URL로 읽기만 |
| **1세션 = 1목표** | 한 세션에서 한 가지 목표만 집중 |

---

## 2. Git 구조

### 2-1. 레포지토리 & 브랜치

| 프로젝트 | 경로 | 브랜치 | GitHub |
|---------|------|--------|--------|
| dev-vault | `C:\dev` | main | paulseongminpark/dev-vault |
| orchestration | `01_projects/01_orchestration` | **main** | paulseongminpark/orchestration |
| portfolio | `01_projects/02_portfolio` | **master** | paulseongminpark/portfolio_20260215 |
| tech-review-blog | `01_projects/03_tech-review-blog` | main | paulseongminpark/tech-review |

> **주의**: orchestration은 `main`, portfolio는 `master`. 혼동하면 push 실패합니다.

### 2-2. 커밋 규칙

```
[project] 한줄 설명
```

예시:
- `[orchestration] v2.2 시스템 오버홀 완료`
- `[portfolio] TechReviewSection 추가`
- `vault: HOME.md 갱신`

**금지 사항:**
- `git push --force` — 절대 금지
- `git reset --hard` — 사용자 확인 없이 금지
- STATE.md 변경 후 커밋 안 하기 — 변경 즉시 commit+push

### 2-3. GitHub Pages

orchestration 프로젝트는 GitHub Pages로 STATE.md를 외부 AI에 공개합니다.

```
https://paulseongminpark.github.io/orchestration/STATE.md
```

GPT/Gemini/Perplexity에게 이 URL을 주면 현재 프로젝트 상태를 읽을 수 있습니다.

---

## 3. Obsidian 연동

### 3-1. 구조

`C:\dev` 전체가 하나의 Obsidian 볼트입니다. `HOME.md`가 중앙 허브(MOC) 역할을 합니다.

```
HOME.md → 모든 프로젝트 STATE 링크
        → Open Decisions
        → Today's Session
        → UI Lab
```

### 3-2. Junction 연결

Windows에서는 Junction(`mklink /J`)으로 프로젝트 폴더를 연결합니다. 관리자 권한 불필요.

### 3-3. Obsidian Git 플러그인

- Obsidian Git 플러그인으로 자동 커밋/push (dev-vault)
- **중요**: context/ 폴더의 문서는 Obsidian에서 **절대 편집 금지** — Claude Code만 수정

---

## 4. MD 문서 체계

### 4-1. 3분화 구조 (D-017)

각 프로젝트는 세 종류의 핵심 문서를 갖습니다:

| 문서 | 역할 | 읽는 시점 |
|------|------|----------|
| **STATE.md** | "지금 어디에 있는가" | 세션 시작, 방향 파악 |
| **PLANNING.md** | "왜 이렇게 했는가" (ADR) | 결정 이유 확인 |
| **KNOWLEDGE.md** | "어떻게 해야 하는가" | 규칙/패턴 확인 |

> 토큰 효율: 필요한 문서만 읽어서 토큰 낭비를 방지합니다.

### 4-2. Orchestration 문서 맵

```
orchestration/
├── STATE.md                    ← 현재 상태 (루트, 고수준)
├── context/
│   ├── session-summary.md      ← compressor 출력 (/catchup이 읽음)
│   ├── decisions.md            ← 결정 추적 (❌미반영/✅반영/🚫취소)
│   ├── PLANNING.md             ← 아키텍처 결정 기록 (ADR)
│   ├── METRICS.md              ← 세션별 완료 태스크/결정 수
│   └── logs/
│       └── 2026-02-22.md       ← 시간순 상세 로그 (읽기 금지, append만)
├── config/
│   ├── claude/                 ← Claude 설정
│   ├── gpt/                    ← GPT 설정
│   ├── gemini/                 ← Gemini 설정
│   └── docs/
│       ├── TODO.md             ← 할 일 목록
│       ├── architecture.md     ← 아키텍처 개요
│       └── daily-workflow.md   ← 일일 워크플로우
├── docs/
│   ├── CHANGELOG.md            ← 버전 이력
│   ├── ROADMAP.md              ← 로드맵
│   ├── SYSTEM-GUIDE.md         ← 이 문서
│   └── plans/                  ← 설계/구현 계획서
└── scripts/
    └── copy-session-log.py     ← 세션 로그 복사
```

### 4-3. 문서별 규칙

**logs/ (읽기 금지)**
- Claude Code가 절대 읽지 않음. `echo` append만.
- 시간순 상세 기록. 나중에 사람이 검색용으로 읽음.

**decisions.md (추적 시스템)**
```
YYYY-MM-DD [project] 결정 내용 | pf:❌ tr:❌
```
- `❌` = 아직 해당 프로젝트에 반영 안 됨
- `✅` = 반영 완료
- `🚫` = 취소됨
- SessionStart 훅이 미반영 항목을 자동 알림

**session-summary.md (세션 연속성)**
- compressor 에이전트가 세션 종료 시 자동 저장
- 다음 세션에서 `/catchup`으로 5초 안에 복구

---

## 5. 에이전트 시스템

### 5-1. 에이전트란?

에이전트는 **특정 역할에 특화된 서브프로세스**입니다. 메인 Claude Code가 상황을 판단해 자동으로(PROACTIVELY) 호출하거나, 사용자가 명시적으로 요청할 수 있습니다.

파일 위치: `~/.claude/agents/<name>.md`

### 5-2. 에이전트 구조

```yaml
---
name: agent-name
description: 호출 조건 설명
tools: Read, Grep, Glob, Bash    # 사용 가능한 도구
model: opus/sonnet/haiku          # 사용 모델
---

# Agent Title
## 역할
## 수집 (어떤 정보를 모으는가)
## 출력 (어떤 형식으로 보고하는가)
## 원칙
```

### 5-3. 전체 에이전트 목록 (16개)

#### 자동 호출 (PROACTIVELY, 4개)

| 에이전트 | 모델 | 트리거 |
|---------|------|--------|
| **code-reviewer** | Opus | "만들었어", "완성", 구현 마무리 감지 |
| **commit-writer** | Haiku | "커밋해", "올려", code-reviewer 완료 후 |
| **orch-state** | Sonnet | "뭐 해야 해", "어디까지 했지", 방향 파악 필요 |
| **compressor** | Sonnet | "/compact", "마무리", "끝내자", 토큰 높을 때 |

**사용 예시:**
```
사용자: "이 기능 구현 완료됐어"
→ code-reviewer 자동 호출 → 리뷰 결과 출력
→ commit-writer 자동 호출 → 커밋 메시지 제안
```

#### Portfolio (3개)

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| **pf-context** | Sonnet | portfolio 현재 상태 수집 (작업 시작 전) |
| **pf-reviewer** | Opus | 코드/디자인/접근성 심층 리뷰 |
| **pf-deployer** | Sonnet | Vercel 배포 전 체크리스트 (GO/NO-GO) |

#### Orchestration (2개)

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| **orch-doc-writer** | Opus | 결정 기록, 아키텍처 문서, CHANGELOG |
| **orch-skill-builder** | Opus | 새 스킬/에이전트/훅 설계 및 생성 |

#### 분석/검증 (3개)

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| **gemini-analyzer** | Sonnet* | Gemini CLI로 대규모 코드베이스 분석 (100만 토큰) |
| **codex-reviewer** | Sonnet* | Codex CLI로 8개 관점 결함 분석 |
| **security-auditor** | Opus | 배포 전 보안 취약점 점검 |

> *Sonnet은 래퍼 모델. 실제 분석은 Gemini/Codex가 수행.

#### Monet-lab (2개)

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| **ml-experimenter** | Opus | UI 컴포넌트 실험 리뷰/개선 제안 |
| **ml-porter** | Sonnet | 실험 결과 → portfolio 이식 판단 |

#### 기타 (2개)

| 에이전트 | 모델 | 역할 |
|---------|------|------|
| **morning-briefer** | Haiku | /morning 브리핑 (catchup + orch-state 통합) |
| **content-writer** | Opus | 글 작성 (블로그, 케이스스터디 등) |

### 5-4. 모델 선택 기준

| 모델 | 비용 | 용도 | 에이전트 |
|------|------|------|---------|
| **Haiku** | 저 | 수집, 확인, 포맷팅 | commit-writer, morning-briefer |
| **Sonnet** | 중 | 분석, 중간 복잡도 | orch-state, compressor, pf-context, pf-deployer, ml-porter |
| **Opus** | 고 | 리뷰, 설계, 작성 | code-reviewer, pf-reviewer, orch-doc-writer, ml-experimenter, content-writer, security-auditor |

### 5-5. 교차 검증 파이프라인

gemini-analyzer와 codex-reviewer를 **병렬 독립 실행** → Claude가 두 결과를 교차 검증합니다.

```
┌─────────────────┐     ┌──────────────────┐
│ gemini-analyzer  │     │  codex-reviewer   │
│ (Gemini CLI)     │     │  (Codex CLI)      │
│ 100만 토큰 광역  │     │  8개 관점 결함    │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         └───────┬───────────────┘
                 ↓
         ┌───────────────┐
         │  Claude 심판   │
         │ 불일치 = 깊이  │
         │ 일치 = 신뢰도↑ │
         └───────────────┘
```

**불일치 처리:**
- 한쪽만 발견 → Claude가 직접 확인 후 판단
- 양쪽 발견 → 높은 신뢰도, 즉시 조치
- 양쪽 미발견 → blind spot 가능성 인지

**사용법:**
```
"시스템 전체 점검해줘, Gemini랑 Codex 둘 다 써서"
→ Claude가 두 에이전트를 병렬 Task로 실행
→ 두 결과를 받아 교차 비교
→ 종합 보고서 출력
```

> **교훈**: 단일 AI 분석은 blind spot이 있을 수 있음. 반드시 교차 검증.

---

## 6. 스킬 시스템

### 6-1. 스킬이란?

스킬은 **반복 작업을 자동화하는 프롬프트 템플릿**입니다. `/명령어`로 호출합니다.

파일 위치: `~/.claude/skills/<name>/SKILL.md`

### 6-2. 커스텀 스킬 (16개)

#### 운영 (5개)

| 스킬 | 용도 | 사용 시점 |
|------|------|----------|
| `/morning` | 전체 프로젝트 브리핑 | 하루 시작 |
| `/sync-all` | 모든 프로젝트 git commit+push + 메모리 동기화 | 세션 종료 전 |
| `/todo` | TODO 관리 + 핸드폰 INBOX 동기화 | 언제든 |
| `/catchup` | 이전 세션 요약 복구 (5초) | 세션 시작 |
| `/compressor` | 세션 압축 저장 (5곳) | 세션 종료 전 |

#### 검증 (2개)

| 스킬 | 용도 | 사용 시점 |
|------|------|----------|
| `/verify` | 브랜치/STATE/커밋/LOG 규칙 검증 | 커밋 전 |
| `/docs-review` | Living Docs stale 감지 | 주간 |

#### 분석 (3개)

| 스킬 | 용도 | 사용 시점 |
|------|------|----------|
| `/session-insights` | 토큰 사용량/비용 분석 (ccusage) | 궁금할 때 |
| `/memory-review` | MEMORY.md 주간 정리 | 주간 |
| `/research` | 딥 리서치 (코드+웹+크로스 검증) | 조사 필요 시 |

#### 생성 (3개)

| 스킬 | 용도 | 사용 시점 |
|------|------|----------|
| `/skill-creator` | 새 스킬 생성 | 필요 시 |
| `/subagent-creator` | 새 에이전트 생성 | 필요 시 |
| `/hook-creator` | 새 훅 생성 | 필요 시 |

#### 기타 (3개)

| 스킬 | 용도 |
|------|------|
| `/write` | 글쓰기 프로세스 (content-writer 연동) |
| `/commit-push-pr` | 커밋 → push → PR 원스톱 |
| `/gpt-review` | GPT에게 보낼 비판적 리뷰 프롬프트 생성 |

### 6-3. 플러그인 제공 스킬 (superpowers)

superpowers 플러그인이 개발 워크플로우 스킬을 제공합니다:

| 스킬 | 용도 |
|------|------|
| `brainstorming` | 아이디어 → 설계 (새 기능 시작 시 **필수**) |
| `writing-plans` | 설계 → 구현 계획 |
| `subagent-driven-development` | 계획 → 서브에이전트별 구현 |
| `executing-plans` | 별도 세션에서 계획 실행 |
| `test-driven-development` | TDD 워크플로우 |
| `using-git-worktrees` | 격리된 작업 환경 |
| `systematic-debugging` | 체계적 디버깅 |
| `requesting-code-review` | 코드 리뷰 요청 |
| `finishing-a-development-branch` | 브랜치 완료/머지 |

### 6-4. 일반적인 기능 개발 흐름

```
사용자: "새 기능 추가해줘"
  1. superpowers:brainstorming → 아이디어 구체화, 설계
  2. superpowers:writing-plans → 구현 계획 작성
  3. implement → 코드 작성
  4. code-reviewer → 자동 리뷰
  5. commit-writer → 자동 커밋 메시지
  6. /sync-all → push
```

---

## 7. 훅 시스템

### 7-1. 훅이란?

훅은 **특정 이벤트 발생 시 자동 실행되는 셸 명령**입니다. 설정 위치: `~/.claude/settings.json`의 `hooks` 섹션.

### 7-2. 현재 훅 (7종)

#### SessionStart (세션 시작 시, 5개 훅)

| # | 동작 | 비고 |
|---|------|------|
| 1 | "High Effort Mode Active" 출력 | 항상 |
| 2 | 오늘 작업 로그 마지막 30줄 출력 | 로그 있을 때만 |
| 3 | 미커밋 파일 수 경고 | async |
| 4 | decisions.md 미반영(❌) 항목 출력 | 있을 때만 |
| 5 | docs-review 7일 경과 경고 | async |

**효과**: 세션 시작 시 자동으로 오늘 할 일, 미커밋 상태, 미반영 결정을 알려줍니다.

#### SessionEnd (세션 종료 시, 4개 훅)

| # | 동작 | 비고 |
|---|------|------|
| 1 | 각 프로젝트 미커밋 수 출력 | 항상 |
| 2 | "/sync recommended" 안내 | context/ 있을 때 |
| 3 | Auto Memory 분석 실행 | session-stop.sh |
| 4 | MEMORY.md 150줄 초과 경고 | async |

#### PreToolUse (도구 사용 전)

```
위험 명령 차단: rm -rf, git push --force, git push -f
```
- 페일클로즈: 파싱 실패 시에도 차단 (`exit 2`)

#### PostToolUse (도구 사용 후)

```
Write/Edit 시 context/*.md 변경 감지 → 커밋 전 확인 알림
```

#### PreCompact (압축 전)

```
"/verify recommended" 안내
```

#### TeammateIdle (팀원 유휴)

```
정보 메시지만 출력 (비차단, exit 0)
```

#### TaskCompleted (태스크 완료)

```
완료 알림
```

---

## 8. 플러그인

### 8-1. 활성화된 플러그인

| 플러그인 | 역할 |
|---------|------|
| **superpowers** | 개발 워크플로우 스킬 묶음 (brainstorming, TDD, 계획 등) |
| **context7** | 라이브러리 최신 문서 조회 |
| **frontend-design** | UI 디자인 스킬 |
| **vercel** | Vercel 배포/로그 |
| **document-skills** | 문서 스킬 (PDF, DOCX, PPTX, XLSX 등) |
| **code-simplifier** | 코드 간소화 |
| **hookify** | 훅 자동 생성 |
| **playground** | HTML 인터랙티브 플레이그라운드 |
| **claude-md-management** | CLAUDE.md 관리 |
| **coderabbit** | 코드 리뷰 |
| **playwright** | 웹 테스팅 |
| **code-review** | 코드 리뷰 스킬 |
| **commit-commands** | 커밋 관련 스킬 |
| **claude-code-setup** | 초기 설정 |
| **feature-dev** | 기능 개발 |
| **agent-sdk-dev** | Agent SDK |
| **greptile** | 코드 검색 |

### 8-2. 비활성화된 플러그인

| 플러그인 | 이유 |
|---------|------|
| **github** | gh CLI로 대체 |
| **example-skills** | document-skills와 100% 중복 |

---

## 9. MCP (Model Context Protocol)

### 9-1. 현재 상태

v2.2에서 MCP 서버 3개를 모두 제거했습니다:

| 서버 | 제거 이유 |
|------|----------|
| `memory` | Auto Memory Phase 1/2/3와 충돌 |
| `desktop-commander` | 보안 위험 + Bash 도구로 대체 가능 |
| `sequential-thinking` | Claude에 내장된 기능 |

### 9-2. MCP 최소화 원칙 (D-xxx)

> GitHub 연동 = `gh` CLI, 웹 테스팅 = `playwright`, 메모리 = Auto Memory.
> MCP 서버는 대체 불가능한 경우에만 추가.

---

## 10. 자동 메모리 시스템

### 10-1. 3-Phase 구조

```
Phase 1: 자동 수집 (SessionEnd)
  세션 종료 → session-stop.sh → analyze-session.sh → pending.md

Phase 2: 검증 이동 (/sync-all)
  pending.md 항목 → 4가지 기준 검증 → MEMORY.md 또는 삭제

Phase 3: 주간 정리 (/memory-review)
  MEMORY.md 품질 관리, 오래된/부정확한 항목 제거
```

### 10-2. Phase 1 상세

```
세션 종료
  → SessionEnd 훅 → session-stop.sh
  → stdin에서 transcript_path 또는 session_id 읽기
  → 없으면 최신 JSONL 파일 사용 (fallback)
  → analyze-session.sh 호출
  → JSONL 분석:
     - 도구 반복 패턴 (2회 이상 사용된 도구)
     - 에러/실패 메시지
     - 사용자 선호 표현 ("항상", "절대", "기억해")
  → pending.md에 append
```

### 10-3. Phase 2 검증 기준

`/sync-all` 실행 시 pending.md 각 항목을 검증:

| 기준 | 설명 |
|------|------|
| 2회 이상 확인? | 한 번만 나온 패턴은 보류 |
| MEMORY.md 중복 없음? | 이미 있는 내용이면 삭제 |
| CLAUDE.md 모순 없음? | 규칙과 충돌하면 삭제 |
| 다음 세션에 유용? | 일시적 정보면 삭제 |

### 10-4. MEMORY.md

위치: `~/.claude/projects/C--dev/memory/MEMORY.md`

매 세션 시작 시 자동 로드됩니다. 150줄 이후는 잘리므로 간결하게 유지.

**내용:**
- 프로젝트 구조, 경로
- 공통 패턴, 에러 해결법
- 사용자 선호 (dev 서버 실행 금지, KST 시간 등)
- 시스템 버전 이력

---

## 11. 토큰 관리

### 11-1. 기본 규칙

| 구간 | 동작 |
|------|------|
| 0~100K | 일반 모드 |
| 100K~150K | 효율 모드 (탐색은 서브에이전트로) |
| 150K+ | `/compact` 또는 `/clear` 필수 |

### 11-2. 토큰 절약 전략

1. **파일 재읽기 금지** — 이미 읽은 파일은 다시 읽지 않음
2. **탐색은 서브에이전트** — Explore 에이전트로 위임
3. **파일 묶음 처리** — 2-3개 파일을 한 턴에
4. **금지 경로** — `node_modules/`, `.git/`, `dist/`, `build/`
5. **logs/ 읽기 금지** — append만

### 11-3. 모델별 비용

| 모델 | 상대 비용 | 용도 |
|------|----------|------|
| Haiku | 1x | 수집, 확인, 포맷팅 |
| Sonnet | 5x | 분석, 탐색 |
| Opus | 10x+ | 설계, 리뷰, 복잡한 작업 |

> 서브에이전트 모델은 작업 복잡도에 맞춰 선택됩니다.

---

## 12. 세션 워크플로우

### 12-1. 세션 시작

```
Claude Code 시작
  → SessionStart 훅 자동 실행
  → "High Effort Mode Active"
  → 오늘 작업 로그 출력
  → 미커밋 경고
  → 미반영 결정 출력
  → MEMORY.md 자동 로드
```

**첫 명령어 옵션:**
- `/morning` — 전체 브리핑 (추천)
- `/catchup` — 이전 세션 복구만
- 바로 작업 시작

### 12-2. 작업 중

```
작업 흐름 (새 기능):
  brainstorming → writing-plans → implement → review → commit

작업 흐름 (버그 수정):
  systematic-debugging → fix → review → commit

작업 흐름 (분석):
  gemini-analyzer + codex-reviewer (병렬) → Claude 교차 검증
```

**중간 체크포인트:**
- 구현 완료 → code-reviewer 자동
- 커밋 필요 → commit-writer 자동
- 방향 잃음 → orch-state 자동

### 12-3. 세션 종료

```
1. /compressor → 세션 요약 저장 (5곳)
   - session-summary.md
   - LOG append
   - STATE.md 갱신
   - decisions.md append
   - METRICS.md append

2. /sync-all → 모든 프로젝트 commit+push + 메모리 동기화

3. 세션 종료
   → SessionEnd 훅 자동 실행
   → 미커밋 경고
   → Auto Memory Phase 1 실행
```

**순서 중요**: `/compressor` 먼저, `/sync-all` 나중.

---

## 13. 병렬 세션 워크플로우

### 13-1. 에이전트 팀

Claude Code는 팀을 만들어 여러 에이전트가 동시에 작업할 수 있습니다.

```
사용자: "팀으로 작업해줘"
  → TeamCreate → 팀 생성
  → TaskCreate → 태스크 목록 생성
  → Task (background) → 에이전트 병렬 실행
  → 결과 수집 → 통합
```

### 13-2. 서브에이전트 사용

독립적인 조사/분석을 서브에이전트에 위임:

```
사용자: "이 코드베이스 분석해줘"
  → Explore 에이전트 → 파일 구조 파악
  → gemini-analyzer → 전체 코드 분석
  → codex-reviewer → 결함 분석
  → Claude → 결과 교차 검증
```

### 13-3. Worktree 격리

기능 개발 시 worktree로 격리된 환경 생성:

```
EnterWorktree → .claude/worktrees/ 에 새 브랜치 생성
  → 격리된 환경에서 작업
  → 완료 후 merge 또는 폐기
```

### 13-4. 주의사항

- **같은 파일 동시 수정 금지** — 병렬 Write는 reject됨
- **에이전트 간 통신은 SendMessage** — 텍스트 출력은 다른 에이전트에게 안 보임
- **TaskList로 진행 상황 확인** — 에이전트 완료 시 자동 알림

---

## 14. 주요 명령어 치트시트

### 세션 관리
```
/morning          전체 프로젝트 브리핑
/catchup          이전 세션 복구
/compressor       세션 압축 저장
/sync-all         모든 프로젝트 push + 메모리 동기화
```

### 검증
```
/verify           커밋 전 규칙 검증
/docs-review      문서 stale 감지
```

### TODO
```
/todo             할 일 목록 + INBOX 동기화
/todo add "내용"  항목 추가
/todo done 1      첫 번째 미완료 항목 완료
```

### 분석
```
/session-insights  토큰 사용량/비용
/memory-review     MEMORY.md 정리
/research          딥 리서치
```

### 생성
```
/skill-creator     새 스킬 만들기
/subagent-creator  새 에이전트 만들기
/hook-creator      새 훅 만들기
```

### 개발 (superpowers)
```
brainstorming      아이디어 → 설계
writing-plans      설계 → 구현 계획
TDD               테스트 주도 개발
debugging          체계적 디버깅
```

---

## 15. Daily Memo 시스템

핸드폰에서 Claude Code로 메모 → 컴퓨터에서 `/todo`로 동기화.

```
핸드폰 Claude Code
  → daily-memo 레포 claude/add-inbox-hello-71SP3 브랜치
  → Inbox.md에 날짜/시간 메모 추가

컴퓨터 /todo
  → 브랜치 Inbox.md 읽기
  → main과 비교 → 새 항목 감지
  → PR merge → TODO.md 백로그에 추가
```

---

## 16. 문제 해결

### 자주 묻는 질문

**Q: 세션이 끊겼는데 이전 작업을 이어가고 싶어**
→ `/catchup` 실행. session-summary.md에서 자동 복구.

**Q: 토큰이 너무 많이 쓰였어**
→ `/compact` 실행. 또는 `/session-insights`로 사용량 확인.

**Q: 커밋 전에 규칙 위반이 없는지 확인하고 싶어**
→ `/verify` 실행.

**Q: 전체 시스템에 문제가 없는지 점검하고 싶어**
→ "시스템 전체 점검해줘, Gemini랑 Codex 둘 다 써서"

**Q: 다른 AI에게 현재 상태를 알려주고 싶어**
→ GitHub Pages URL 공유: `https://paulseongminpark.github.io/orchestration/STATE.md`
→ 또는 `/gpt-review`로 리뷰용 프롬프트 생성

**Q: MEMORY.md가 너무 길어졌어**
→ `/memory-review` 실행. 또는 150줄 넘으면 SessionEnd에서 자동 경고.

---

## 부록: 파일 경로 빠른 참조

| 구분 | 경로 |
|------|------|
| 전역 규칙 | `C:\dev\CLAUDE.md` |
| 글로벌 설정 | `~/.claude/settings.json` |
| 에이전트 | `~/.claude/agents/*.md` |
| 스킬 | `~/.claude/skills/*/SKILL.md` |
| 규칙 | `~/.claude/rules/*.md` |
| 메모리 | `~/.claude/projects/C--dev/memory/MEMORY.md` |
| 훅 스크립트 | `~/.claude/hooks/`, `~/.claude/scripts/` |
| Orchestration STATE | `01_projects/01_orchestration/STATE.md` |
| Portfolio STATE | `01_projects/02_portfolio/context/STATE.md` |
| 결정 추적 | `01_projects/01_orchestration/context/decisions.md` |
| 세션 요약 | `01_projects/01_orchestration/context/session-summary.md` |
| TODO | `01_projects/01_orchestration/config/docs/TODO.md` |
| 작업 로그 | `01_projects/01_orchestration/context/logs/YYYY-MM-DD.md` |
| 세션 Transcript | `~/.claude/projects/C--dev/*.jsonl` |
