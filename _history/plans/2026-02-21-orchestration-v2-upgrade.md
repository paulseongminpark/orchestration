# Orchestration System v2 Upgrade Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** cc-system의 HIGH/MEDIUM VALUE 컴포넌트를 흡수하고, 오케스트레이션 시스템을 v1으로 공식 문서화하며, Obsidian↔GitHub 자동 동기화 체계를 구축한다.

**Architecture:**
- 현재 시스템(v1)을 기준점으로 CHANGELOG.md에 기록
- cc-system 스킬/프롬프트를 `~/.claude/skills/` 및 `orchestration/config/docs/`에 통합
- Obsidian Git 플러그인으로 볼트(C:\dev) 전체 자동 커밋/푸시

**Tech Stack:** Claude Code Skills (Markdown + YAML), Python (cc-system scripts), Obsidian Git plugin, GitHub

---

## 현황 (작업 전 상태)

### 오케스트레이션 시스템 v1 구성
- `~/.claude/skills/`: morning, todo, sync-all, memory-review, docs-review, research, token-check, token-mode, verify, verify-project-rules, verify-log-format (11개)
- `~/.claude/scripts/`: analyze-session.sh, sync-memory.sh, memory-review.sh, docs-review.sh, token-monitor.sh
- `~/.claude/agents/`: orchestrator.md
- `orchestration/config/`: claude/, docs/, gpt/, gemini/, perplexity/
- Obsidian 볼트: C:\dev (Git 플러그인 미설치)

### cc-system 가져올 대상
**HIGH VALUE (4개)**
1. `crystalize-prompt.md` — 프롬프트 압축 방법론
2. `skill-creator` 스킬 — 스킬 초기화/패키징/검증
3. `subagent-creator` 스킬 — 에이전트 생성 프레임워크
4. `design-pipeline.md` — AI 파이프라인 설계 원칙

**MEDIUM VALUE (2개)**
5. `hook-creator` 스킬 — 훅 생성 + 이벤트 레퍼런스
6. references 폴더 구조 — 기존 스킬들에 적용

---

## Task 1: v1 공식 문서화

**Files:**
- Create: `C:\dev\01_projects\01_orchestration\docs\CHANGELOG.md`
- Create: `C:\dev\01_projects\01_orchestration\docs\VERSIONS.md`

**Step 1:** `docs/CHANGELOG.md` 생성 — v1 현황 기록
**Step 2:** `docs/VERSIONS.md` 생성 — 버전 로드맵 (v1 → v2 목표)
**Step 3:** orchestration git commit

```bash
git -C /c/dev/01_projects/01_orchestration add docs/CHANGELOG.md docs/VERSIONS.md
git -C /c/dev/01_projects/01_orchestration commit -m "[orchestration] v1 공식 문서화"
```

---

## Task 2: crystalize-prompt.md 가져오기

**Files:**
- Create: `C:\dev\01_projects\01_orchestration\config\docs\crystalize-prompt.md`

**Source:** `https://raw.githubusercontent.com/greatSumini/cc-system/main/prompt/crystalize-prompt.md`

**활용 방법:**
- GPT/Gemini/Perplexity `master_prompt.md` 최적화 시 이 원칙 적용
- 프롬프트가 길어질 때 → "crystalize" 세션 열고 압축
- 압축 원칙: 의도 보존, 고해상도 토큰화, 중복 제거

**Step 1:** raw URL에서 내용 가져와 저장
**Step 2:** `orchestration/config/docs/INDEX.md`에 항목 추가
**Step 3:** commit

---

## Task 3: design-pipeline.md 가져오기

**Files:**
- Create: `C:\dev\01_projects\01_orchestration\config\docs\design-pipeline.md`

**Source:** `https://raw.githubusercontent.com/greatSumini/cc-system/main/prompt/design-pipeline.md`

**활용 방법:**
- 멀티 AI 파이프라인 설계 시 참고 (컨텍스트 효율, 전처리 분리)
- Claude Code + 서브에이전트 작업 위임 패턴 적용
- 큰 데이터 → Python 전처리 후 AI에 전달하는 원칙

**Step 1:** 저장
**Step 2:** INDEX.md 업데이트
**Step 3:** commit

---

## Task 4: skill-creator 스킬 가져오기

**Files:**
- Create: `~/.claude/skills/skill-creator/SKILL.md`
- Create: `~/.claude/skills/skill-creator/scripts/init_skill.py`
- Create: `~/.claude/skills/skill-creator/scripts/package_skill.py`
- Create: `~/.claude/skills/skill-creator/scripts/quick_validate.py`
- Create: `~/.claude/skills/skill-creator/references/workflows.md`
- Create: `~/.claude/skills/skill-creator/references/output-patterns.md`

**Source URLs:**
```
https://raw.githubusercontent.com/greatSumini/cc-system/main/.claude/skills/skill-creator/SKILL.md
https://raw.githubusercontent.com/greatSumini/cc-system/main/.claude/skills/skill-creator/scripts/init_skill.py
...
```

**활용 방법:**
- 새 스킬 만들 때: `python init_skill.py <skill-name>` → 폴더 구조 자동 생성
- 배포 전: `python package_skill.py` → 검증 + 패키징
- 빠른 검증: `python quick_validate.py` → SKILL.md 형식 체크

**Step 1:** 폴더 생성 및 파일들 저장
**Step 2:** Python 스크립트 실행 테스트 (`python quick_validate.py`)

---

## Task 5: subagent-creator 스킬 가져오기

**Files:**
- Create: `~/.claude/skills/subagent-creator/SKILL.md`
- Create: `~/.claude/skills/subagent-creator/assets/subagent-template.md`
- Create: `~/.claude/skills/subagent-creator/references/available-tools.md`
- Create: `~/.claude/skills/subagent-creator/references/examples.md`

**활용 방법:**
- 새 에이전트 만들 때: subagent-creator 스킬 호출
- 템플릿 + 도구 레퍼런스 + 6가지 예시 (Code Reviewer, Debugger, Data Scientist 등)
- 현재 `orchestrator.md` 외 에이전트 추가 시

**Step 1:** 파일들 저장

---

## Task 6: hook-creator 스킬 가져오기

**Files:**
- Create: `~/.claude/skills/hook-creator/SKILL.md`
- Create: `~/.claude/skills/hook-creator/references/hook-events.md`
- Create: `~/.claude/skills/hook-creator/references/examples.md`

**활용 방법:**
- 새 훅 만들 때 참고 (10가지 이벤트 설명)
- hookify와 별개로 직접 shell 훅 작성 시 examples.md 참고
- Auto-formatting, File protection, Notification 패턴

**Step 1:** 파일들 저장

---

## Task 7: references 폴더 구조 기존 스킬에 적용

**현재 스킬들 (단순 SKILL.md만 있음):**
- morning, sync-all, docs-review, research, todo, verify

**적용 방식:**
- 각 스킬의 SKILL.md를 분석
- 자주 참조하는 외부 정보나 레퍼런스가 있는 경우 `references/` 서브폴더로 분리
- 지금 당장 대상: `research/` 스킬 (웹 검색 패턴, 검증 체크리스트 등)

**Step 1:** research 스킬에 `references/` 적용 (파일럿)
**Step 2:** 결과 보고 후 나머지 적용 여부 결정

---

## Task 8: Obsidian Git 플러그인 설치 (사용자 직접)

**현황:** `C:\dev\.obsidian/plugins/` 폴더 없음 → community 플러그인 미설치

**설치 방법 (Obsidian UI에서):**
1. Obsidian 설정 → Community plugins → Safe mode 끄기
2. Browse → "Obsidian Git" 검색 → Install
3. Enable

**설정 (Obsidian Git 권장값):**
```
Vault backup interval: 10 (분)
Auto pull interval: 0 (수동)
Commit message: "obsidian: {{date}}"
Push on backup: true
Pull before push: true
```

**대상 repo:** `C:\dev` 전체는 git repo가 아님 (서브폴더들만 repo)

**⚠️ 중요 이슈:** Obsidian Git은 볼트 루트가 git repo여야 함.
`C:\dev`는 git repo가 아니므로, 다음 중 선택:
- **Option A**: C:\dev를 git repo로 초기화 (HOME.md, CLAUDE.md 등 모두 추적)
- **Option B**: Obsidian 볼트를 orchestration 폴더로 지정 (범위 축소)
- **Option C**: Obsidian Git 대신 각 프로젝트별 /sync-all로만 관리 (현재 방식 유지)

→ **결정 필요: 어떤 옵션 선택?**

---

## Task 9: 버전 로드맵 Obsidian 연동

**Files:**
- Create: `C:\dev\01_projects\01_orchestration\docs\ROADMAP.md`

**내용:** v1 → v2 → v3 업그레이드 계획을 Obsidian에서 볼 수 있도록

```markdown
# Orchestration System Roadmap

## v1 (2026-02-21) ✅ CURRENT
- skills 11개, scripts 5개, orchestrator.md
- orchestration/config/ (gpt/gemini/perplexity)
- auto memory system

## v2 (진행 중)
- cc-system 통합 (crystalize-prompt, skill-creator, subagent-creator, design-pipeline, hook-creator)
- Obsidian Git 연동
- CHANGELOG.md 버전 관리

## v3 (계획)
- TBD (v2 완료 후 결정)
```

---

## 실행 순서 요약

```
Task 1: v1 문서화 (CHANGELOG.md, VERSIONS.md)
Task 2: crystalize-prompt.md 가져오기
Task 3: design-pipeline.md 가져오기
Task 4: skill-creator 스킬
Task 5: subagent-creator 스킬
Task 6: hook-creator 스킬
Task 7: references 구조 파일럿 (research 스킬)
Task 8: Obsidian Git 설치 (사용자 직접 + 옵션 결정 필요)
Task 9: ROADMAP.md 생성
```

**예상 결과:** `~/.claude/skills/` 14개 스킬 (현재 11 + 3 신규), orchestration/config/docs/ 2개 추가, 버전 관리 체계 구축

---

## 참고: cc-system 원본 위치

```
https://github.com/greatSumini/cc-system
https://raw.githubusercontent.com/greatSumini/cc-system/main/.claude/skills/skill-creator/SKILL.md
https://raw.githubusercontent.com/greatSumini/cc-system/main/.claude/skills/subagent-creator/SKILL.md
https://raw.githubusercontent.com/greatSumini/cc-system/main/.claude/skills/hook-creator/SKILL.md
https://raw.githubusercontent.com/greatSumini/cc-system/main/prompt/crystalize-prompt.md
https://raw.githubusercontent.com/greatSumini/cc-system/main/prompt/design-pipeline.md
```
