# Orchestration v3.2 — Reference

> SYSTEM-GUIDE + USER-GUIDE 통합. 마지막 갱신: 2026-02-24

---

## 1. 시스템 개요

Claude Code 중심으로 여러 AI(GPT, Gemini, Perplexity)와 도구(Git, Obsidian, GitHub)를 통합 운영하는 개인 개발 워크스페이스.

```
C:\dev\                          ← 볼트 허브 (dev-vault, git: main)
├── HOME.md                      ← 중앙 허브 (Obsidian MOC)
├── CLAUDE.md                    ← 전역 규칙 + 체인 (SoT)
├── 01_projects/
│   ├── 01_orchestration/        ← AI 오케스트레이션 (git: main)
│   ├── 02_portfolio/            ← 포트폴리오 (git: master)
│   ├── 03_tech-review/          ← 기술 리뷰 트래커
│   ├── 03_tech-review-blog/     ← Jekyll 블로그 (git: main)
│   └── 04_monet-lab/            ← UI 실험
└── 03_evidence/                 ← 스크린샷, 세션 증거
```

### 핵심 원칙
| 원칙 | 설명 |
|------|------|
| SoT = Git | 모든 상태는 Git으로 추적 |
| Claude Code = 유일한 쓰기 | STATE.md 등은 Claude Code만 수정 |
| Obsidian = 읽기 전용 뷰어 | Junction으로 연결, 편집 금지 |
| 1세션 = 1목표 | 집중과 토큰 효율 |

---

## 2. 하루 흐름

### 아침
```
/morning          → 전체 브리핑 (미커밋, TODO, 미반영 결정, Inbox)
/dispatch         → 팀 추천 + 작업 방향
```

### 작업 중
```
(구현)            → code-reviewer → commit-writer → project-linker
/dispatch         → 방향 전환 시 재호출 가능
```

### 마무리
```
/verify           → 규칙 검증
/sync-all         → 전체 프로젝트 동기화
/compressor       → 세션 압축 (9단계)
```

---

## 3. 리좀형 팀 구조

```
           meta-orchestrator (디스패치 허브, /dispatch)
           ┌───────┼───────┐
    ops    │  build │ analyze
           └───┬───┘
            maintain

리좀 연결자: context-linker ◆── live-context.md ──◆ project-linker
크로스팀: commit-writer, orch-state, project-context, content-writer
```

| 팀 | 리드 | 멤버 | 진입점 |
|----|------|------|--------|
| ops | morning-briefer | inbox-processor, tr-updater, tr-monitor | /morning |
| build | code-reviewer | pf-reviewer, pf-deployer, ml-experimenter, security-auditor | 구현 시작 |
| analyze | ai-synthesizer | gemini-analyzer, codex-reviewer | 명시적 요청 |
| maintain | compressor | doc-syncer, orch-doc-writer, orch-skill-builder | /compressor |

---

## 4. 스킬 사용법

| 스킬 | 용도 | 빈도 |
|------|------|------|
| /morning | 전체 브리핑 + Inbox + TODO | 매일 아침 |
| /dispatch | 팀 추천 + 세션 목표 설정 | 세션 시작 / 방향 전환 |
| /todo | TODO CRUD + Inbox 동기화 | 수시 |
| /verify | 커밋 전 규칙 검증 | 커밋 전 |
| /sync-all | 전체 프로젝트 동기화 | 세션 마무리 |
| /compressor | 세션 압축 (9단계) | 세션 종료 전 |
| /docs-review | stale 문서 점검 | 주 1회 |
| /research | 딥 리서치 워크플로우 | 필요 시 |
| /write | 글쓰기 (content-writer) | 필요 시 |
| /session-insights | 토큰 사용량 분석 | 필요 시 |
| /memory-review | MEMORY.md 주간 정리 | 주 1회 |

---

## 5. 에이전트 체인 (SoT: CLAUDE.md)

### 구현 체인
```
implement → code-reviewer(Opus) → commit-writer(Haiku) → project-linker(Sonnet)
```

### 배포 체인
```
pf-deployer → security-auditor → 사용자 확인 → push
```

### 분석 체인
```
gemini + codex (병렬) → ai-synthesizer(Opus) → agent.md 반영
```

### 디스패치 체인
```
/dispatch → context-linker(Haiku) → meta-orchestrator(Sonnet) → 팀 활성화
```

### 압축 체인
```
compressor 7단계 → orch-doc-writer(조건부) → doc-syncer
```

---

## 6. SoT 맵

| 정보 | SoT 파일 | 나머지 |
|------|---------|--------|
| 에이전트/스킬/팀/플러그인 | STATE.md | → STATE.md 참조 |
| 체인 규칙 | CLAUDE.md | → CLAUDE.md 참조 |
| 버전 이력 | CHANGELOG.md | STATE.md에 현재 버전 1줄 |
| 패턴/규칙 | KNOWLEDGE.md | 중복 제거 |
| 훅/스크립트 | KNOWLEDGE.md | STATE.md에 목록만 |
| 결정 기록 | PLANNING.md (ADR) | decisions.md(추적) |

---

## 7. 자주 하는 실수

| 실수 | 올바른 방법 |
|------|------------|
| STATE.md Obsidian에서 편집 | Claude Code + /sync만 |
| 커밋 전 검증 생략 | /verify 먼저 |
| 여러 목표 한 세션 | 1세션=1목표 |
| logs/ 파일 읽기 | append만, 읽기 금지 |
| orchestration=master 혼동 | orchestration=main, portfolio=master |

---

## 8. 멀티 AI

| AI | 역할 |
|----|------|
| Claude Code | 실행 + 기록 (유일한 쓰기) |
| GPT Plus | 사고 확장, Canvas |
| Gemini Pro | 대량 검증 (1M 토큰) |
| Perplexity | 리서치 + 교차검증 |

STATE.md URL: `https://raw.githubusercontent.com/paulseongminpark/orchestration/main/STATE.md`

---

## 9. 문서 맵

| 문서 | 역할 | 읽기 우선순위 |
|------|------|-------------|
| MEMORY.md | 세션 간 영속 | 1 (자동) |
| STATE.md | 현재 상태 + 인벤토리 | 2 |
| CLAUDE.md | 전역 규칙 + 체인 | 3 (자동) |
| KNOWLEDGE.md | 패턴/규칙 | 4 (필요 시) |
| PLANNING.md | ADR | 5 (필요 시) |
| REFERENCE.md | 종합 가이드 (이 파일) | 참고용 |
| CHANGELOG.md | 버전 이력 | 참고용 |
