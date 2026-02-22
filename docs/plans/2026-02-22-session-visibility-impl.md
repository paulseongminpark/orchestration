# Session Visibility System Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 여러 Claude Code 세션이 서로의 결정 사항을 자동으로 인지할 수 있도록 decisions.md + Hook 강화 + compressor 연동 구현

**Architecture:** 전역 파일 `~/.claude/decisions.md`에 세션별 결정 사항을 1줄 형식으로 기록. SessionStart Hook이 미반영 항목을 자동 출력. compressor가 세션 마무리 시 decisions.md에 append.

**Tech Stack:** bash (hooks), markdown (decisions.md), Claude agents (compressor)

---

### Task 1: decisions.md 초기화

**Files:**
- Create: `C:/Users/pauls/.claude/decisions.md`

**Step 1: 파일 생성**

```markdown
# Decisions Log

> 세션별 중요 결정 사항. compressor가 자동 append.
> 태그: pf=portfolio, tr=tech-review, ml=monet-lab, orch=orchestration
> ❌=미반영, ✅=반영완료

## 미반영

2026-02-22 [orch] compressor 확장(LOG+STATE 3곳), sync-all dev-vault | pf:❌ tr:✅
2026-02-22 [orch] Session Visibility System 구현 | pf:❌ tr:✅
2026-02-22 [tech-review] Smart Brevity 전면 도입, 수요일 AI×Industry | pf:❌

## 아카이브

2026-02-22 [orch] CHANGELOG v2.0 hooks 7종 | pf:✅ tr:✅
```

**Step 2: 확인**
```bash
cat /c/Users/pauls/.claude/decisions.md
```
Expected: 파일 정상 출력

---

### Task 2: SessionStart Hook에 decisions.md 출력 추가

**Files:**
- Modify: `C:/Users/pauls/.claude/settings.json` — SessionStart hooks 배열

**Step 1: settings.json 읽기**
현재 SessionStart에 3개 hook 존재 확인 완료.

**Step 2: 4번째 hook 명령어 추가**

추가할 명령어:
```bash
DECISIONS="/c/Users/pauls/.claude/decisions.md"; if [ -f "$DECISIONS" ]; then PENDING=$(grep "❌" "$DECISIONS" 2>/dev/null); if [ -n "$PENDING" ]; then echo ""; echo "=== 미반영 결정 사항 ==="; echo "$PENDING" | tail -10; echo "=================="; fi; fi; true
```

**Step 3: 테스트**
새 Claude Code 세션을 열거나 SessionStart를 시뮬레이션해서 decisions.md 내용이 출력되는지 확인.

---

### Task 3: SessionEnd Hook에 git 전체 상태 추가

**Files:**
- Modify: `C:/Users/pauls/.claude/settings.json` — SessionEnd hooks 배열

**Step 1: 현재 SessionEnd hook 확인**
```
- test -d context ... (sync 권장 알림)
- bash session-stop.sh
```

**Step 2: git 상태 체크 hook 추가 (session-stop.sh 앞에)**

추가할 명령어:
```bash
echo "=== 세션 종료 git 상태 ==="; for PROJ in "01_orchestration" "02_portfolio" "03_tech-review"; do DIR="/c/dev/01_projects/$PROJ"; if [ -d "$DIR/.git" ]; then CNT=$(git -C "$DIR" status -s 2>/dev/null | wc -l | tr -d ' '); NAME=$(echo $PROJ | sed 's/0[0-9]_//'); [ "$CNT" -gt 0 ] && echo "⚠️  $NAME: ${CNT}개 미커밋" || echo "✅ $NAME: clean"; fi; done; echo "========================"; true
```

---

### Task 4: compressor 에이전트에 decisions.md append 추가

**Files:**
- Modify: `C:/Users/pauls/.claude/agents/compressor.md`

**Step 1: compressor.md 현재 "저장" 섹션 확인**
현재: session-summary.md, LOG, STATE.md 3곳

**Step 2: 4번째 저장 대상 추가**

기존 `## 저장 (3곳에 동시 저장)` 섹션에 추가:

```markdown
### 4. decisions.md append (신규)
`/c/Users/pauls/.claude/decisions.md`의 `## 미반영` 섹션 아래에 append.

형식 (1줄):
```
YYYY-MM-DD [project] 핵심 결정 요약 (30자 이내) | pf:❌ tr:❌
```

규칙:
- 관련 없는 프로젝트 태그는 생략
- portfolio 반영이 필요한 결정에만 `pf:❌` 포함
- 이미 해당 프로젝트 세션에서 반영됐으면 `✅`
```

---

### Task 5: 커밋

**Step 1: decisions.md 커밋 (전역 파일은 dev-vault에)**
```bash
cd /c/dev && git add . && git commit -m "[vault] decisions.md 초기화 — Session Visibility System"
```

**Step 2: settings.json 변경사항 확인**
settings.json은 git 추적 안 됨 → 별도 백업 불필요

**Step 3: orchestration compressor.md 커밋**
```bash
cd /c/dev/01_projects/01_orchestration && git add . && git commit -m "[orchestration] compressor: decisions.md append 추가" && git push origin main
```

---

### Task 6: 검증

**Step 1: decisions.md 미반영 항목 표시 확인**
새 터미널에서 Claude Code 세션 시작 → SessionStart에서 "=== 미반영 결정 사항 ===" 출력 확인

**Step 2: SessionEnd git 상태 확인**
Claude Code 세션 종료 → "=== 세션 종료 git 상태 ===" 출력 확인

**Step 3: compressor 동작 확인**
"마무리하자" 입력 → compressor 실행 → decisions.md에 1줄 추가됐는지 확인
