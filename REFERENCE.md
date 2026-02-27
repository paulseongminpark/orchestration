# Orchestration v4.0 — Reference

> 최종 수정: 2026-02-27

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
(구현)            → code-reviewer → commit-writer → linker
/dispatch         → 방향 전환 시 재호출 가능
```

### 마무리 (세션 전환 체인)
```
/verify           → 규칙 검증
/sync all         → 전체 프로젝트 동기화
/compact          → 세션 압축 (9단계)
linker            → 크로스세션 맥락 기록
→ 완료 후에만 /clear 허용
```

---

## 3. 리좀형 팀 구조 (v4.0)

```
           meta-orchestrator (디스패치 허브, /dispatch)
           ┌───────┼───────┐
    ops    │  build │ analyze
           └───┬───┘
            maintain

리좀 연결자: linker ◆── live-context.md + .ctx/shared-context.md
크로스팀: commit-writer, orch-state, project-context
```

| 팀 | 리드 | 멤버 | 진입점 |
|----|------|------|--------|
| ops | daily-ops | tr-ops | /morning |
| build | code-reviewer | pf-ops, security-auditor | 구현 시작 |
| analyze | ai-synthesizer(adversarial verify) | gemini-analyzer(벌크추출), codex-reviewer(정밀검증) | 추출/검증 체인 |
| maintain | compressor | doc-ops | /compact |

---

## 4. 스킬 사용법

| 스킬 | 용도 | 빈도 |
|------|------|------|
| /morning | 전체 브리핑 + Inbox + TODO | 매일 아침 |
| /dispatch | 팀 추천 + 세션 목표 설정 | 세션 시작 / 방향 전환 |
| /todo | TODO CRUD + Inbox 동기화 | 수시 |
| /verify | 커밋 전 규칙 검증 | 커밋 전 |
| /sync | STATE 갱신 + git push (/sync all: 전체) | 세션 마무리 |
| /compact | 세션 압축 (9단계) | 세션 종료 전 |
| /session-insights | 토큰 사용량 분석 | 필요 시 |
| /handoff | CLI 간 작업 위임 (.ctx/ 갱신) | 필요 시 |
| /status | 현재 시스템 상태 | 필요 시 |

### 200K Context 운영 (v3.3.1)

| 임계값 | 조치 |
|--------|------|
| ~42K | baseline (고정) |
| 100K | compact 권장 |
| 120K | compact 필수 |
| 150K | auto-compact (최후 방어선) |

- **.chain-temp/**: 에이전트 체인 결과 파일 오프로딩 → 메인 context에 1줄 요약만
- compact 전 스냅샷 → compact 후 자동 Read → 맥락 보존

---

## 5. 에이전트 체인 (SoT: CLAUDE.md)

### 구현 체인
```
implement → code-reviewer(Opus) → commit-writer(Haiku) → linker(Haiku)
```

### 배포 체인
```
pf-ops(deploy) → security-auditor → 사용자 확인 → push
```

### 추출/검증 체인
```
Gemini 추출(벌크) + Codex 추출(정밀) → Claude verify barrier(3단계) → 사용
- Gemini: -m gemini-3.1-pro-preview --output-format json --yolo
- Codex: codex exec -p [extract|verify|review|implement]
- 외부 CLI 출력 → 반드시 _meta 블록 검증 후 사용
```

### 세션 전환 체인
```
"새 세션" 제안 시 반드시 먼저:
verify → /sync all → /compact → linker → "새 세션 준비 완료"
```

### 디스패치 체인
```
/dispatch → linker(Haiku, 자동) → meta-orchestrator(Opus) → 팀 활성화
```

### 압축 체인
```
compressor 9단계 → doc-ops(항상) → doc-ops verify
```

### Cross-CLI 위임 (v4.0)
```
/handoff <cli> "<작업>" → .ctx/shared-context.md 갱신 → worktree 안내 → CLI 실행 안내
worktree: /c/dev/scripts/worktree-create.sh <project> <cli> <task>
정리: /c/dev/scripts/worktree-cleanup.sh [name]
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

## 8. 멀티 AI 오케스트레이션 (v4.0)

| AI | 역할 | 플랜 | 제한 |
|----|------|------|------|
| Claude Code (Opus 4.6) | 설계/결정/코드 작성 + 최종 판단 (verify barrier) | Max | 1M 컨텍스트 |
| Codex CLI (GPT-5.3) | 정밀 검증기: diff 리뷰 + 포맷 QA + git 추출 | Plus $20 | 5시간 롤링, 세션당 3~5회 |
| Gemini CLI (3.1 Pro) | 벌크 추출기: 컨텍스트 오프로딩 + 웹 검색 | AI Pro $20 | 일일 rate limit, 1M 컨텍스트 |
| Perplexity | tech-review 소스 (sonar-deep-research) | Pro | 월 예산 $5 |

### 외부 CLI 설정 위치
- Codex: `~/.codex/` (instructions.md, config.toml, skills/)
- Gemini: `~/.gemini/` (settings.json, skills/, memories/)
- 규칙 동기화: `rulesync generate` → CLAUDE.md/GEMINI.md/AGENTS.md 자동 생성

### Cross-CLI 공유 메모리 (.ctx/)
- `.ctx/shared-context.md`: 모든 CLI가 읽고 쓰는 공유 상태
- `.ctx/provenance.log`: 출처 추적 ([claude]/[gemini]/[codex])
- `.ctx/gemini/`, `.ctx/codex/`: CLI별 결과 저장
- gitignored (로컬 상태)

### Verify Barrier (모든 외부 CLI 출력에 적용)
1. 구조 검증: JSON 파싱 + _meta 블록 확인
2. 스팟체크: 임의 2~3개 항목 원본 대조
3. 반박 검증: 고위험 작업 시 "빠진 것 없는가?"

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
