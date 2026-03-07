# Claude-Codex-Gemini 위임 시스템 구현 계획

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Claude Code가 대규모 분석 작업을 Codex/Gemini에 자동 위임해 컨텍스트를 절약하는 시스템 구축

**Architecture:** `delegate-to-codex` / `delegate-to-gemini` 스킬을 만들어 Claude가 트리거 감지 시 호출. 결과는 `.ctx/delegates/`에 저장하고 Claude는 요약본만 읽음. 글로벌 CLAUDE.md에 트리거 규칙 추가해 모든 프로젝트에서 작동.

**Tech Stack:** Claude Code Skills (SKILL.md), Bash (codex exec / gemini -p), `.ctx/` 핸드오프 폴더

---

### Task 1: `.ctx/delegates/` 폴더 생성

**Files:**
- Create: `/c/dev/.ctx/delegates/.gitkeep`

**Step 1: 폴더 생성**

```bash
mkdir -p /c/dev/.ctx/delegates
touch /c/dev/.ctx/delegates/.gitkeep
```

**Step 2: 검증**

```bash
ls /c/dev/.ctx/delegates/
```
Expected: `.gitkeep` 존재

**Step 3: Commit**

```bash
cd /c/dev && git add .ctx/delegates/.gitkeep
git commit -m "[orchestration] .ctx/delegates/ 위임 결과 폴더 생성"
```

---

### Task 2: `delegate-to-codex` 스킬 작성

**Files:**
- Create: `/c/Users/pauls/.claude/skills/delegate-to-codex/SKILL.md`

**Step 1: 폴더 생성**

```bash
mkdir -p /c/Users/pauls/.claude/skills/delegate-to-codex
```

**Step 2: SKILL.md 작성**

```markdown
---
name: delegate-to-codex
description: >
  Claude가 대규모 분석 작업을 Codex(gpt-5.4 xhigh)에 위임.
  파일 5개+ 분석, 코드베이스 탐색, 배치 작업, 벌크 테스트 생성에 사용.
  결과는 .ctx/codex-latest.md + .ctx/delegates/에 저장.
user-invocable: false
disable-model-invocation: false
context: inline
---

## 목적
대규모 분석/탐색 작업을 Codex에 위임해 Claude 컨텍스트를 절약한다.

## 트리거 조건 (이 중 하나 해당 시 자동 사용)
- 파일 5개 이상 동시 읽고 분석해야 할 때
- 전체 코드베이스 탐색이 필요할 때 ("어느 파일 봐야 하나?")
- 여러 파일 교차 비교/종합 (schema vs config vs DB 등)
- enrichment, 배치 분석 등 장시간 작업
- 벌크 테스트 파일 생성

## 실행 절차

### 1. 타임스탬프 생성
```bash
TIMESTAMP=$(date +"%Y-%m-%d-%H")
TASK_NAME="[작업 이름 슬러그]"
OUT_FILE="/c/dev/.ctx/delegates/${TIMESTAMP}-${TASK_NAME}.md"
```

### 2. 분석 전용 (read-only)
```bash
PYTHONIOENCODING=utf-8 codex exec \
  "[구체적 프롬프트]. 파일 수정 금지. 분석 결과만 마크다운으로 출력하라." \
  -s read-only --ephemeral \
  -o "$OUT_FILE"

cp "$OUT_FILE" /c/dev/.ctx/codex-latest.md
```

### 3. 테스트 파일 생성 (workspace-write)
tests/ 폴더에만 파일을 쓰는 케이스:
```bash
PYTHONIOENCODING=utf-8 codex exec \
  "[테스트 생성 프롬프트]. tests/ 폴더에만 파일 생성. 소스코드 수정/커밋 금지." \
  -s workspace-write --ephemeral \
  --add-dir /c/dev/[프로젝트]/tests \
  -o "$OUT_FILE"
```

### 4. 결과 읽기
```bash
# Claude는 요약본만 읽음
cat /c/dev/.ctx/codex-latest.md
```

## 하드 룰
- `--ephemeral` 항상 (세션 저장 금지)
- 커밋은 Claude만. 프롬프트에 "커밋 금지" 명시
- 테스트 생성 외에는 read-only 고정
- xhigh 기본값 유지 (config.toml에 이미 설정됨)
```

**Step 3: 검증**

스킬이 Claude에서 인식되는지 확인:
```
/delegate-to-codex
```
또는 Claude에게 "delegate-to-codex 스킬 있어?" 물어보기

---

### Task 3: `delegate-to-gemini` 스킬 작성

**Files:**
- Create: `/c/Users/pauls/.claude/skills/delegate-to-gemini/SKILL.md`

**Step 1: 폴더 생성**

```bash
mkdir -p /c/Users/pauls/.claude/skills/delegate-to-gemini
```

**Step 2: SKILL.md 작성**

```markdown
---
name: delegate-to-gemini
description: >
  Claude가 영향 범위 분석 / Codex 결과 반박 / 아키텍처 2nd opinion을
  Gemini(gemini-3.1-pro)에 위임. 결과는 .ctx/gemini-latest.md에 저장.
user-invocable: false
disable-model-invocation: false
context: inline
---

## 목적
Codex 결과를 독립적으로 검증하거나, 수정 영향 범위를 전체 소스 기반으로 분석한다.

## 트리거 조건
- Codex 분석 결과를 반박/보완할 때
- 전체 소스 + 스펙 동시 로딩 → 수정 영향 범위 분석
- 아키텍처 설계 2nd opinion
- 대형 설계 문서 검토

## 실행 절차

### 1. 타임스탬프 생성
```bash
TIMESTAMP=$(date +"%Y-%m-%d-%H")
TASK_NAME="[작업 이름 슬러그]"
OUT_FILE="/c/dev/.ctx/delegates/${TIMESTAMP}-gemini-${TASK_NAME}.md"
```

### 2. 실행
```bash
PYTHONIOENCODING=utf-8 gemini \
  -p "[구체적 프롬프트]. 파일 수정 금지. 커밋 금지. 분석 결과만 마크다운으로 출력하라." \
  --yolo \
  > "$OUT_FILE" 2>&1

cp "$OUT_FILE" /c/dev/.ctx/gemini-latest.md
```

### 3. 결과 읽기
```bash
cat /c/dev/.ctx/gemini-latest.md
```

## 하드 룰
- 프롬프트에 항상 "파일 수정 금지. 커밋 금지." 포함
- `--yolo` 필수 (비대화형 자동 승인)
- 커밋은 Claude만
```

**Step 3: 검증**

```bash
PYTHONIOENCODING=utf-8 gemini -m gemini-3.1-pro \
  -p "현재 날짜를 출력하라. 파일 수정 금지." \
  --yolo > /c/dev/.ctx/gemini-latest.md 2>&1
cat /c/dev/.ctx/gemini-latest.md
```
Expected: 날짜 출력 (오류 없음)

---

### Task 4: 글로벌 CLAUDE.md에 위임 트리거 규칙 추가

**Files:**
- Modify: `/c/Users/pauls/.claude/CLAUDE.md`

**Step 1: 현재 파일 읽기 (Read 도구로)**

**Step 2: 위임 트리거 섹션 추가**

아래 내용을 CLAUDE.md 적절한 위치에 추가:

```markdown
## Codex/Gemini 위임 규칙

### Codex에 위임 (delegate-to-codex 스킬)
다음 중 하나 해당 시 자동 위임:
- 파일 5개 이상 동시 읽고 분석
- 전체 코드베이스 탐색
- 여러 파일 교차 비교/종합
- enrichment, 배치 분석 등 장시간 작업
- 벌크 테스트 파일 생성 (tests/ 폴더만)

### Gemini에 위임 (delegate-to-gemini 스킬)
- Codex 결과 반박/보완
- 전체 소스 + 스펙 → 수정 영향 범위 분석
- 아키텍처 2nd opinion

### Claude가 직접 (위임 금지)
- recall, remember, get_context (단순 MCP 호출)
- 파일 4개 이하 읽기
- 커밋 (Codex/Gemini 커밋 절대 금지)
```

**Step 3: 검증**

Claude Code 재시작 후 CLAUDE.md 규칙 반영 확인.

---

### Task 5: 통합 검증

**Step 1: Codex 위임 end-to-end 테스트**

```bash
# mcp-memory 전체 구조 탐색 위임
TIMESTAMP=$(date +"%Y-%m-%d-%H")
PYTHONIOENCODING=utf-8 codex exec \
  "mcp-memory 프로젝트(/c/dev/01_projects/06_mcp-memory/) 전체 폴더 구조를 읽고, init_db 관련 파일과 라인 목록만 추출하라. 파일 수정 금지. 커밋 금지." \
  -s read-only --ephemeral \
  -o "/c/dev/.ctx/delegates/${TIMESTAMP}-init-db-map.md"

cat "/c/dev/.ctx/delegates/${TIMESTAMP}-init-db-map.md"
```
Expected: init_db 관련 파일/라인 목록 마크다운

**Step 2: Gemini 위임 end-to-end 테스트**

```bash
TIMESTAMP=$(date +"%Y-%m-%d-%H")
PYTHONIOENCODING=utf-8 gemini -m gemini-3.1-pro \
  -p "mcp-memory 프로젝트의 config.py와 schema 관련 파일을 읽고, 타입 불일치 가능성이 있는 부분만 리포트하라. 파일 수정 금지. 커밋 금지." \
  --yolo \
  > "/c/dev/.ctx/delegates/${TIMESTAMP}-gemini-config-review.md" 2>&1

cat "/c/dev/.ctx/delegates/${TIMESTAMP}-gemini-config-review.md"
```
Expected: 타입 불일치 리포트

**Step 3: 최종 커밋**

```bash
cd /c/dev && git add .ctx/delegates/.gitkeep
git commit -m "[orchestration] Codex/Gemini 위임 시스템 구현 완료"
```
