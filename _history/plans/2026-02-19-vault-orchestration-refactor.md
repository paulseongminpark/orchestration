# Vault & Orchestration 전면 리팩토링 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** C:\dev 옵시디언 볼트를 중앙 허브로 재구성하고, orchestration이 AI 관련 모든 진실의 원천이 되도록 구조 정리

**Architecture:** 볼트 루트에 HOME.md(중앙 MOC) 신설, ai-config를 orchestration/config/로 흡수, 분산된 프로젝트 폴더를 01_projects/ 아래로 집중. 독립 git repo(opcode, tech-review)는 중첩 금지이므로 01_projects/ 시블링으로 이동.

**Tech Stack:** git, bash, Obsidian markdown

---

## 주의사항

- `opcode/` → 독립 git repo (Tauri 앱). orchestration 내부 중첩 금지. `01_projects/05_opcode/`로 이동.
- `tech-review/` → 독립 git repo (Jekyll). `03_tech-review/`도 git repo. `01_projects/03_tech-review-blog/`로 이동 (별도 시블링).
- `02_ai_config/` → git repo 유지 (히스토리 보존). 파일만 복사, repo 삭제 안 함.
- 커밋 브랜치: orchestration=main, portfolio=master

---

## Task 1: HOME.md 생성 (볼트 중앙 허브)

**Files:**
- Create: `C:\dev\HOME.md`
- Delete: `C:\dev\null` (빈 파일)

**Step 1: null 파일 삭제**
```bash
rm "C:/dev/null"
```

**Step 2: HOME.md 생성**

`C:\dev\HOME.md` 내용:
```markdown
# HOME — Dev Workspace Hub
_Updated: 2026-02-19_

## Projects
| Project | Status | Last Updated | Next |
|---------|--------|-------------|------|
| [[01_projects/01_orchestration/context/STATE\|orchestration]] | Phase 10 완료 | 2026-02-17 | 실전 테스트 |
| [[01_projects/02_portfolio/context/STATE\|portfolio]] | W5 완료 | 2026-02-19 | W6 시작 |
| [[01_projects/03_tech-review/STATE\|tech-review]] | 기획중 | 2026-02-19 | 방향 결정 |
| [[01_projects/03_tech-review-blog/README\|tech-review-blog]] | Jekyll 유지 | - | 포스팅 |
| [[01_projects/05_opcode/README\|opcode]] | Tauri 앱 개발중 | - | - |

## Today's Session
- Date: {{date}}
- Focus: {{focus}}
- Log: [[01_projects/01_orchestration/context/logs/{{date}}]]

## Open Decisions
- [ ] portfolio W6 착수 시점
- [ ] tech-review 포스팅 주제/빈도 방향
- [ ] opcode 완성 목표 시점

## Tools & Skills
- AI Config: `01_projects/01_orchestration/config/`
- Hooks & Scripts: `~/.claude/`
- 주요 스킬: `/morning`, `/sync-all`, `/verify`, `/token-check`, `/docs-review`

## Archive
- [[02_ai_config/README|ai-config (archived)]] — orchestration/config/ 로 이동됨
```

**Step 3: 확인**
```bash
ls "C:/dev/HOME.md" && echo "OK"
```

---

## Task 2: orchestration config/ 디렉토리 생성 및 ai-config 파일 복사

**Files:**
- Create dir: `01_projects/01_orchestration/config/`
- Copy from: `02_ai_config/claude/`, `gpt/`, `gemini/`, `perplexity/`, `projects/`, `docs/`

**Step 1: config 디렉토리 구조 생성**
```bash
mkdir -p "C:/dev/01_projects/01_orchestration/config/claude"
mkdir -p "C:/dev/01_projects/01_orchestration/config/gpt"
mkdir -p "C:/dev/01_projects/01_orchestration/config/gemini"
mkdir -p "C:/dev/01_projects/01_orchestration/config/perplexity"
mkdir -p "C:/dev/01_projects/01_orchestration/config/projects"
```

**Step 2: ai-config 파일 복사 (git repo는 유지, 파일만 복사)**
```bash
cp -r "C:/dev/02_ai_config/claude/." "C:/dev/01_projects/01_orchestration/config/claude/"
cp -r "C:/dev/02_ai_config/gpt/." "C:/dev/01_projects/01_orchestration/config/gpt/"
cp -r "C:/dev/02_ai_config/gemini/." "C:/dev/01_projects/01_orchestration/config/gemini/"
cp -r "C:/dev/02_ai_config/perplexity/." "C:/dev/01_projects/01_orchestration/config/perplexity/"
cp -r "C:/dev/02_ai_config/projects/." "C:/dev/01_projects/01_orchestration/config/projects/"
```

**Step 3: ai-config/docs 복사**
```bash
cp -r "C:/dev/02_ai_config/docs/." "C:/dev/01_projects/01_orchestration/config/docs/"
```
(폴더 없으면 생성)

**Step 4: 복사 확인**
```bash
ls "C:/dev/01_projects/01_orchestration/config/"
```
Expected: claude/ gpt/ gemini/ perplexity/ projects/ docs/

**Step 5: orchestration에 커밋**
```bash
git -C "C:/dev/01_projects/01_orchestration" add config/
git -C "C:/dev/01_projects/01_orchestration" commit -m "[orchestration] config/ 추가 (ai-config 흡수)"
```

---

## Task 3: vault docs/ → orchestration docs/ 이동 완료

**Files:**
- Copy: `C:\dev\docs\plans\2026-02-18-auto-memory-phase1.md` → orchestration
- `C:\dev\docs\plans\2026-02-19-vault-orchestration-redesign-design.md` (이미 복사됨)
- Remove: `C:\dev\docs\` 폴더 (이동 완료 후)

**Step 1: 나머지 plan 파일 복사**
```bash
cp "C:/dev/docs/plans/2026-02-18-auto-memory-phase1.md" \
   "C:/dev/01_projects/01_orchestration/docs/plans/"
```

**Step 2: 이 구현 계획 파일도 복사**
```bash
cp "C:/dev/docs/plans/2026-02-19-vault-orchestration-refactor.md" \
   "C:/dev/01_projects/01_orchestration/docs/plans/"
```

**Step 3: orchestration에 커밋**
```bash
git -C "C:/dev/01_projects/01_orchestration" add docs/
git -C "C:/dev/01_projects/01_orchestration" commit -m "[orchestration] docs/plans 이동 완료 (vault docs/ 흡수)"
```

**Step 4: vault 루트 docs/ 제거**
```bash
rm -rf "C:/dev/docs/"
```

**Step 5: 확인**
```bash
ls "C:/dev/01_projects/01_orchestration/docs/plans/"
```

---

## Task 4: ai-config 아카이브 처리

**Files:**
- Create/Overwrite: `C:\dev\02_ai_config\README.md`

**Step 1: ARCHIVED README 작성**

`C:\dev\02_ai_config\README.md` 내용:
```markdown
# ai-config — ARCHIVED

> **이 저장소는 아카이브되었습니다.**
>
> 모든 콘텐츠는 `01_orchestration/config/` 로 이동되었습니다.
> - Claude 설정: `01_projects/01_orchestration/config/claude/`
> - GPT 설정: `01_projects/01_orchestration/config/gpt/`
> - Gemini 설정: `01_projects/01_orchestration/config/gemini/`
> - Perplexity 설정: `01_projects/01_orchestration/config/perplexity/`
>
> **이 저장소를 직접 수정하지 마세요.**
> Git 히스토리 보존을 위해 물리적 삭제는 하지 않습니다.

_Archived: 2026-02-19_
```

**Step 2: ai-config에 커밋 및 푸시**
```bash
git -C "C:/dev/02_ai_config" add README.md
git -C "C:/dev/02_ai_config" commit -m "[ai-config] ARCHIVED — content moved to orchestration/config/"
git -C "C:/dev/02_ai_config" push
```

---

## Task 5: opcode 이동 (01_projects/05_opcode/)

**주의:** opcode/는 독립 git repo. 단순 폴더 이동으로 git 히스토리 보존.

**Step 1: 현재 opcode 상태 확인**
```bash
git -C "C:/dev/opcode" status
```
Expected: unstaged 변경 있음 (확인만, 커밋 안 함)

**Step 2: 폴더 이동 (bash mv)**
```bash
mv "C:/dev/opcode" "C:/dev/01_projects/05_opcode"
```

**Step 3: git 원격 설정 확인**
```bash
git -C "C:/dev/01_projects/05_opcode" remote -v
```
Expected: origin URL 표시됨

**Step 4: 이동 후 git 정상 작동 확인**
```bash
git -C "C:/dev/01_projects/05_opcode" status
```
Expected: 동일한 unstaged 변경 표시

---

## Task 6: tech-review 이동 (01_projects/03_tech-review-blog/)

**주의:** tech-review/와 03_tech-review/ 둘 다 독립 git repo. 중첩 불가.
해결: tech-review/ (Jekyll) → `01_projects/03_tech-review-blog/`로 이동 (별도 시블링)

**Step 1: 폴더 이동**
```bash
mv "C:/dev/tech-review" "C:/dev/01_projects/03_tech-review-blog"
```

**Step 2: 이동 후 git 확인**
```bash
git -C "C:/dev/01_projects/03_tech-review-blog" remote -v
```

**Step 3: 볼트 루트 확인 (tech-review/ 없어졌는지)**
```bash
ls "C:/dev/" | grep tech
```
Expected: 없음

---

## Task 7: 03_tech-review STATE.md 신설

**Files:**
- Create: `C:\dev\01_projects\03_tech-review\STATE.md`

**Step 1: STATE.md 작성**

`C:\dev\01_projects\03_tech-review\STATE.md` 내용:
```markdown
# tech-review STATE
_Updated: 2026-02-19_

## 목적
기술 리뷰 프로젝트 트래킹 (설계/기획/가스 스크립트)
Jekyll 블로그는 [[03_tech-review-blog]] 참조

## 현재 상태
- 완료: 프로젝트 폴더 구조 (design/, gas/, perplexity-prompts/)
- 진행중: 방향 결정
- 다음: 포스팅 주제/빈도 결정

## 최근 결정
- 2026-02-19: Jekyll 블로그를 03_tech-review-blog/ 로 분리 (독립 git repo 유지)
- 2026-02-19: 이 폴더는 기획/트래킹 전용

## 막힌 것
- 포스팅 방향 미결정
```

**Step 2: 커밋**
```bash
git -C "C:/dev/01_projects/03_tech-review" add STATE.md
git -C "C:/dev/01_projects/03_tech-review" commit -m "[tech-review] STATE.md 신설 (Living Doc)"
```

---

## Task 8: orchestration STATE.md Living Doc 형식 업데이트

**Files:**
- Modify: `C:\dev\01_projects\01_orchestration\context\STATE.md`

현재 내용을 Living Doc 표준으로 업데이트:

```markdown
# orchestration STATE
_Updated: 2026-02-19_

## 목적
Claude Code AI 활용 시스템 설계 및 진행 추적
AI 설정(config/), 문서(docs/), 스크립트(scripts/)의 단일 진실 원천

## 현재 상태
- 완료: Phase 1~10 (폴더구조, CLAUDE.md, Skills, Hooks, Obsidian,
         Multi-AI, 로깅, 검증, 행동모드, 토큰관리)
- 완료: 볼트 전면 리팩토링 (2026-02-19)
         — ai-config → config/ 흡수
         — HOME.md 신설
         — docs/, opcode/, tech-review/ 정리
- 진행중: 실전 테스트
- 다음: Packet 흐름 실전 테스트, 포트폴리오 본격 시작

## 최근 결정
- 2026-02-19: ai-config → orchestration/config/ 머지 (중앙집중화)
- 2026-02-19: Vault Hub & Spoke 구조 채택 (HOME.md)
- 2026-02-17: Phase 10 완료 (토큰 관리 자동화)

## 막힌 것
- 없음
```

**Step: 커밋 및 푸시**
```bash
git -C "C:/dev/01_projects/01_orchestration" add context/STATE.md
git -C "C:/dev/01_projects/01_orchestration" commit -m "[orchestration] STATE.md Living Doc 형식 업데이트 + 리팩토링 반영"
git -C "C:/dev/01_projects/01_orchestration" push
```

---

## Task 9: portfolio STATE.md Living Doc 형식 업데이트

**Files:**
- Modify: `C:\dev\01_projects\02_portfolio\context\STATE.md`

현재 내용 유지하되 헤더 형식만 표준화:

```markdown
# portfolio STATE
_Updated: 2026-02-19_

## 목적
개인 포트폴리오 웹사이트 개발 (React + Vite)

## 현재 상태
- 완료: W1~W5 (Work 슬롯, TOC, All탭, 상세 라우팅, MD 주입,
         실콘텐츠 주입, 탭 필터, 스크롤스파이)
- 진행중: W6 준비
- 다음: W6 OpenAI 스타일 레이아웃 전환

## 최근 결정
- 2026-02-19: TechReview 통합 복원
- 2026-02-15: W5 완료 확인

## 막힌 것
- All탭 스크롤 중 간헐적 Writing/Resume 점프
- TOC 간헐적 사라짐
- 이미지 에셋 미준비
- Resume/Contact 탭 노출 여부 미결정
```

**Step: 커밋**
```bash
git -C "C:/dev/01_projects/02_portfolio" add context/STATE.md
git -C "C:/dev/01_projects/02_portfolio" commit -m "[portfolio] STATE.md Living Doc 형식 업데이트"
```

---

## Task 10: CLAUDE.md 업데이트 (경로 참조 수정)

**Files:**
- Modify: `C:\dev\CLAUDE.md`
- Modify: `C:\Users\pauls\.claude\projects\C--dev\memory\MEMORY.md`

**Step 1: C:\dev\CLAUDE.md 업데이트**

기존 내용 유지, 하단에 추가:
```markdown
## 프로젝트 구조
- orchestration: C:\dev\01_projects\01_orchestration (main 브랜치)
- portfolio: C:\dev\01_projects\02_portfolio (master 브랜치)
- ai-config: C:\dev\02_ai_config (ARCHIVED → orchestration/config/ 사용)
- tech-review: C:\dev\01_projects\03_tech-review (트래킹)
- tech-review-blog: C:\dev\01_projects\03_tech-review-blog (Jekyll)
- opcode: C:\dev\01_projects\05_opcode (Tauri 앱)
- 볼트 허브: C:\dev\HOME.md
```

**Step 2: MEMORY.md 업데이트**

`C:\Users\pauls\.claude\projects\C--dev\memory\MEMORY.md` 수정:
```markdown
# Auto Memory

## Project Structure
- orchestration: C:\dev\01_projects\01_orchestration (main 브랜치)
- portfolio: C:\dev\01_projects\02_portfolio (master 브랜치)
- ai-config: C:\dev\02_ai_config (ARCHIVED — config is in orchestration/config/)
- tech-review: C:\dev\01_projects\03_tech-review (트래킹, main)
- tech-review-blog: C:\dev\01_projects\03_tech-review-blog (Jekyll)
- opcode: C:\dev\01_projects\05_opcode (Tauri)
- 볼트 허브: C:\dev\HOME.md

## Common Patterns
- 세션 transcript: ~/.claude/projects/C--dev/*.jsonl (JSONL 형식)
- 세션 파일 구조: type 필드 (user/assistant/tool_use/tool_result/progress)
- 도구 이름: "name" 필드 (tool_name 아님)
- 사용자 메시지: "type":"user" (role:"human" 아님)

## Error Solutions
- rustc not found: Rust 미설치 환경
- bun not found: Bun 미설치 환경

## Auto Memory System
- Phase 1: SessionEnd Hook → analyze-session.sh → pending.md
- Phase 2: /sync-all → sync-memory.sh → MEMORY.md 검증 이동
- Phase 3: /memory-review → memory-review.sh → 주간 정리
- 파일: ~/.claude/scripts/, ~/.claude/hooks/, ~/.claude/skills/

## Vault Structure (2026-02-19 리팩토링)
- 볼트 허브: HOME.md (중앙 MOC)
- AI 설정: orchestration/config/ (ai-config 흡수)
- 문서: orchestration/docs/plans/
```

---

## Task 11: orchestration/config/ CLAUDE.md 참조 파일 업데이트

**Files:**
- Modify: `C:\dev\01_projects\01_orchestration\.claude\CLAUDE.md`

`config/` 섹션 추가:
```markdown
## Config (AI 도구 설정)
- Claude: config/claude/
- GPT: config/gpt/
- Gemini: config/gemini/
- Perplexity: config/perplexity/

(구 ai-config 저장소에서 흡수. ai-config는 ARCHIVED 상태)
```

**Step: 커밋 및 푸시**
```bash
git -C "C:/dev/01_projects/01_orchestration" add .claude/CLAUDE.md
git -C "C:/dev/01_projects/01_orchestration" commit -m "[orchestration] CLAUDE.md config/ 섹션 추가"
git -C "C:/dev/01_projects/01_orchestration" push
```

---

## Task 12: 볼트 최종 상태 검증

**Step 1: 볼트 루트 확인**
```bash
ls "C:/dev/" | sort
```
Expected 있어야 할 것: HOME.md, CLAUDE.md, .claude/, .obsidian/, 01_projects/, 02_ai_config/, 03_evidence/, 99_archive/
Expected 없어야 할 것: docs/, opcode/, tech-review/, null

**Step 2: 01_projects 구조 확인**
```bash
ls "C:/dev/01_projects/"
```
Expected: 01_orchestration/, 02_portfolio/, 03_tech-review/, 03_tech-review-blog/, 04_tech-review-comments/, 05_opcode/

**Step 3: orchestration config/ 확인**
```bash
ls "C:/dev/01_projects/01_orchestration/config/"
```
Expected: claude/, gpt/, gemini/, perplexity/, projects/

**Step 4: HOME.md 링크 유효성 시각 확인**
Obsidian에서 HOME.md 열어서 모든 [[링크]] 정상 여부 확인

**Step 5: orchestration push 완료 확인**
```bash
git -C "C:/dev/01_projects/01_orchestration" status
git -C "C:/dev/01_projects/01_orchestration" log --oneline -5
```

---

## 실행 요약

| Task | 내용 | 관련 Repo |
|------|------|-----------|
| 1 | HOME.md 생성 + null 삭제 | vault (no git) |
| 2 | orchestration config/ + ai-config 복사 | orchestration |
| 3 | vault docs/ → orchestration docs/ | orchestration |
| 4 | ai-config ARCHIVED README | ai-config |
| 5 | opcode/ → 01_projects/05_opcode/ | opcode (이동) |
| 6 | tech-review/ → 01_projects/03_tech-review-blog/ | tech-review (이동) |
| 7 | 03_tech-review STATE.md 신설 | tech-review |
| 8 | orchestration STATE.md Living Doc | orchestration |
| 9 | portfolio STATE.md Living Doc | portfolio |
| 10 | CLAUDE.md + MEMORY.md 경로 업데이트 | vault/memory |
| 11 | orchestration/.claude/CLAUDE.md config 섹션 | orchestration |
| 12 | 최종 검증 | all |
