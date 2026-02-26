# ai-config → orchestration 통합 Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** orchestration/config/ 아래 문서들을 실제 현황에 맞게 갱신하고, 구버전 중복 파일(config/projects/)을 정리하여 단일 진실 소스를 확립한다.

**Architecture:** ai-config는 이미 2026-02-19에 orchestration/config/로 복사 완료 + ARCHIVED 처리됨. 현재 문제는 (1) config/docs/가 최신화 안 됨, (2) config/projects/가 context/와 중복 구버전, (3) D-019 등 최신 결정이 양쪽에 동기화 안 됨. 이 플랜은 삭제보다 정리·최신화 중심.

**Tech Stack:** 파일 편집(Read/Edit/Write), git, GitHub

---

## 현황 요약

| 항목 | 상태 |
|------|------|
| ai-config/README.md | ✅ ARCHIVED 표시됨 |
| orchestration/config/ | ✅ 파일 복사됨 (단, 일부 구버전) |
| config/projects/ | ❌ context/의 구버전 — 중복, 정리 필요 |
| config/docs/decisions.md | ⚠️ D-019 미반영 여부 확인 필요 |
| config/docs/architecture.md | ❌ 리팩토링 이전 구조 반영 — 업데이트 필요 |
| config/docs/daily-workflow.md | ❌ daily-memo D-019 반영 안 됨 |
| context/STATE.md | ✅ SoT (2026-02-19 최신) |

---

### Task 1: decisions.md D-019 sync 확인

**Files:**
- Read: `C:\dev\01_projects\01_orchestration\config\docs\decisions.md`
- Compare: `C:\dev\02_ai_config\docs\decisions.md`

**Step 1: orchestration/config/docs/decisions.md 읽기**

```bash
# 마지막 항목 확인
tail -50 "C:\dev\01_projects\01_orchestration\config\docs\decisions.md"
```

**Step 2: D-019 존재 여부 확인**

- D-019 없으면: ai-config/docs/decisions.md에서 D-019 섹션 복사하여 추가
- D-019 있으면: Skip

**Step 3: D-019 추가 (필요한 경우)**

아래 내용을 파일 끝에 추가:

```markdown
## D-019: daily-memo 브랜치 구조 확정 (2026-02-21)

**결정**: 핸드폰 Claude Code cloud env 제약으로 인해 브랜치 기반 Inbox 파이프라인 확정.

**구조**:
```
핸드폰 Claude Code (cloud env)
    → claude/add-inbox-hello-71SP3 브랜치 → Inbox.md 누적
    ↓
컴퓨터 /todo → 브랜치 vs main 비교 → 새 항목 merge → TODO.md 반영
```

**배경**:
- cloud env는 GitHub 연동 시 항상 새 브랜치 자동 생성 (main 직접 push 불가)
- CLAUDE.md 지침으로도 우회 불가 — 앱 레벨 제약

**결정 이유**:
- 브랜치 고정: `claude/add-inbox-hello-71SP3` 핸드폰 전용 유지
- main은 merge된 최종 상태만 보관
- /todo 스킬이 브랜치-main diff 후 자동 merge

**D-017과의 차이**:
- D-017: INBOX.md → main 직접 push (이상적 설계)
- D-019: Inbox.md → 브랜치 누적 → /todo 시 merge (cloud env 실제 제약 반영)
```

**Step 4: 커밋**

```bash
cd C:\dev\01_projects\01_orchestration
git add config/docs/decisions.md
git commit -m "[orchestration] config/docs/decisions.md D-019 추가"
```

---

### Task 2: config/projects/ 구버전 정리

**Files:**
- Delete dir: `C:\dev\01_projects\01_orchestration\config\projects\`
- Reference (최신 SoT): `C:\dev\01_projects\01_orchestration\context\`

**배경:**
- `config/projects/orchestration/STATE.md` = 2026-02-17 (구버전)
- `context/STATE.md` = 2026-02-19 (최신, SoT)
- config/projects/는 orchestration/config/가 ai-config의 "projects/ junction"을 복사한 흔적 — 이제 불필요

**Step 1: config/projects/ 내용 최종 확인**

```bash
ls C:\dev\01_projects\01_orchestration\config\projects\
ls C:\dev\01_projects\01_orchestration\config\projects\orchestration\
ls C:\dev\01_projects\01_orchestration\config\projects\portfolio\
```

**Step 2: context/와 diff 확인 (unique 내용 있는지)**

```bash
# config/projects/에만 있는 고유 정보가 있는지 확인
diff "C:\dev\01_projects\01_orchestration\config\projects\orchestration\PLANNING.md" \
     "C:\dev\01_projects\01_orchestration\context\PLANNING.md"
```

**Step 3: 고유 정보 없으면 삭제**

고유 내용 없으면:
```bash
cd C:\dev\01_projects\01_orchestration
git rm -r config/projects/
git commit -m "[orchestration] config/projects/ 제거 — context/ SoT로 통합"
```

고유 내용 있으면: 해당 내용을 context/ 또는 config/docs/에 합친 후 삭제

---

### Task 3: config/docs/architecture.md 업데이트

**Files:**
- Modify: `C:\dev\01_projects\01_orchestration\config\docs\architecture.md`

**Step 1: 현재 내용 읽기**

```
Read: C:\dev\01_projects\01_orchestration\config\docs\architecture.md
```

**Step 2: 구버전 부분 파악**

아래 항목 확인:
- 폴더 구조 다이어그램에 `02_ai_config\` 등 구 경로가 있는지
- "Obsidian 볼트"로 설명된 부분이 실제와 맞는지
- `config/` 폴더가 SoT로 잘못 설명되어 있지 않은지

**Step 3: 업데이트 내용**

실제 현황에 맞게 수정:

```markdown
## 폴더 구조 (2026-02-19 리팩토링 이후)

C:\dev\
├── HOME.md                          ← 볼트 허브 (Obsidian MOC)
├── CLAUDE.md                        ← 전역 공통 규칙
├── 01_projects\
│   ├── 01_orchestration\            ← 오케스트레이션 (SoT)
│   │   ├── context\                 ← ★ 단일 진실 소스
│   │   │   ├── STATE.md
│   │   │   ├── PLANNING.md
│   │   │   └── KNOWLEDGE.md
│   │   ├── config\                  ← AI 설정/프롬프트 저장소
│   │   │   ├── docs\                ← 시스템 문서
│   │   │   ├── gpt\
│   │   │   ├── gemini\
│   │   │   └── perplexity\
│   │   └── docs\plans\              ← 구현 계획
│   ├── 02_portfolio\
│   └── 03_tech-review\
└── 02_ai_config\                    ← ARCHIVED (config\ 흡수)
    └── README.md                    ← "이 폴더는 아카이브됨"
```

**Step 4: 커밋**

```bash
cd C:\dev\01_projects\01_orchestration
git add config/docs/architecture.md
git commit -m "[orchestration] architecture.md 리팩토링 이후 구조 반영"
```

---

### Task 4: config/docs/daily-workflow.md 업데이트

**Files:**
- Modify: `C:\dev\01_projects\01_orchestration\config\docs\daily-workflow.md`

**Step 1: 현재 내용 읽기**

```
Read: C:\dev\01_projects\01_orchestration\config\docs\daily-workflow.md
```

**Step 2: 업데이트 대상 파악**

아래 확인:
- daily-memo 파이프라인 섹션이 D-017 기준인지 (구버전: main 직접 push)
- D-019 반영 여부 (브랜치 기반 Inbox)
- `/todo` 스킬 설명 현행화 여부

**Step 3: daily-memo 섹션 업데이트**

```markdown
## Daily Memo 파이프라인 (D-019, 2026-02-21 확정)

핸드폰 Claude Code (cloud env 제약으로 main 직접 push 불가)
  → `claude/add-inbox-hello-71SP3` 브랜치에 Inbox.md 누적

컴퓨터 /todo 실행:
  1. 브랜치 Inbox.md 읽기
  2. main Inbox.md와 diff
  3. 새 항목 감지 → main merge
  4. 로컬 TODO.md에 반영

**파일 위치**: `C:\dev\02_ai_config\docs\TODO.md`
**레포**: `paulseongminpark/daily-memo`
**브랜치**: `claude/add-inbox-hello-71SP3` (핸드폰 전용, 삭제 금지)
```

**Step 4: 커밋**

```bash
cd C:\dev\01_projects\01_orchestration
git add config/docs/daily-workflow.md
git commit -m "[orchestration] daily-workflow.md D-019 브랜치 기반 Inbox 반영"
```

---

### Task 5: config/docs/KNOWLEDGE.md 경로 수정

**Files:**
- Modify: `C:\dev\01_projects\01_orchestration\config\docs\KNOWLEDGE.md` (또는 claude-code-guide.md)

**Step 1: 현재 내용에서 구버전 경로 검색**

```
Grep: "02_ai_config" in C:\dev\01_projects\01_orchestration\config\docs\
```

**Step 2: 발견된 파일 각각 수정**

`cd C:\dev\02_ai_config` → `cd C:\dev\01_projects\01_orchestration\config` 로 변경
또는 해당 시나리오 자체를 삭제 (더 이상 유효하지 않은 예시라면)

**Step 3: 커밋**

```bash
cd C:\dev\01_projects\01_orchestration
git add config/docs/
git commit -m "[orchestration] config/docs/ ai-config 구버전 경로 수정"
```

---

### Task 6: ai-config 로컬 볼트 정리 (선택)

**Files:**
- `C:\dev\02_ai_config\` — 이미 ARCHIVED

**Step 1: ai-config 내 파일 중 orchestration/config/에 없는 파일 확인**

```bash
# ai-config에만 있고 orchestration/config에 없는 파일
diff <(ls C:\dev\02_ai_config\docs\) <(ls C:\dev\01_projects\01_orchestration\config\docs\)
```

**Step 2: 있으면 복사, 없으면 Skip**

```bash
# 예: TODO.md는 ai-config에서 관리 (orchestration/config/docs/TODO.md는 구버전)
# → ai-config/docs/TODO.md가 실제 사용 중이므로 그대로 유지
```

**Step 3: ai-config/docs/decisions.md 최종 확인**
- orchestration/config/docs/decisions.md와 동일해야 함
- D-019까지 동기화되어 있으면 완료

**NOTE:** ai-config 폴더 자체는 삭제하지 않는다.
- TODO.md: 실제 사용 중 (핵심 파일)
- Obsidian 볼트 링크가 이 폴더를 참조할 수 있음

---

### Task 7: 최종 동기화

**Step 1: orchestration STATE.md 업데이트**

`context/STATE.md`에 아래 추가:

```markdown
## 2026-02-21 통합 작업 완료
- config/docs/ 최신화 (D-019, architecture, daily-workflow)
- config/projects/ 정리 (context/ SoT 통합)
- ai-config/docs/decisions.md ↔ config/docs/decisions.md 동기화
```

**Step 2: /sync-all 실행**

```
/sync-all
```

---

## 실행 체크리스트

- [ ] Task 1: config/docs/decisions.md D-019 sync
- [ ] Task 2: config/projects/ 구버전 정리
- [ ] Task 3: config/docs/architecture.md 업데이트
- [ ] Task 4: config/docs/daily-workflow.md 업데이트
- [ ] Task 5: config/docs/ 구버전 경로 수정
- [ ] Task 6: ai-config ↔ orchestration/config 최종 검증
- [ ] Task 7: /sync-all

## 주의 사항

- `config/projects/` 삭제 전 반드시 context/에 없는 고유 정보 확인
- ai-config/docs/TODO.md는 **삭제하지 않음** — 실제 사용 중
- ai-config/ 폴더 자체는 삭제하지 않음 — Obsidian junction 참조 가능성
- 각 Task는 독립 커밋으로 (한 번에 모아서 커밋 금지)
