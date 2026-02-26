# Orchestration System Overhaul Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** gemini-analyzer 비판 분석 결과를 전면 반영해 보안·자동화·스킬 정리·컨텍스트 연속성을 강화한다.

**Architecture:** settings.json(보안) → hooks(자동화) → agents/skills(정리) → Auto Memory(디버그) → decisions(git 전환) 순서로 진행. 각 태스크는 독립적이므로 병렬 가능한 것은 병렬로.

**Tech Stack:** bash, python3, settings.json(JSON), Claude Code agents/skills

---

## Task 1: [보안] GitHub PAT → ~/.bashrc 이전 + settings.json 제거

> ⚠️ 이 태스크 전에 사용자가 GitHub에서 PAT 토큰 로테이션 필요.
> `https://github.com/settings/tokens` 에서 기존 토큰 revoke → 새 토큰 생성.

**Files:**
- Modify: `~/.claude/settings.json` — env.GITHUB_PERSONAL_ACCESS_TOKEN 키 제거
- Modify: `~/.bashrc` (또는 `~/.bash_profile`) — 새 PAT 환경변수 추가

**Step 1: settings.json에서 PAT 제거**

```bash
python3 -c "
import json
with open('/c/Users/pauls/.claude/settings.json', 'r', encoding='utf-8') as f:
    d = json.load(f)
d.get('env', {}).pop('GITHUB_PERSONAL_ACCESS_TOKEN', None)
with open('/c/Users/pauls/.claude/settings.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print('PAT removed from settings.json')
"
```

**Step 2: ~/.bashrc에 환경변수 추가** (새 토큰으로)

```bash
echo 'export GITHUB_PERSONAL_ACCESS_TOKEN="<새_토큰>"' >> ~/.bashrc
source ~/.bashrc
```

**Step 3: 검증**

```bash
python3 -c "import json; d=json.load(open('/c/Users/pauls/.claude/settings.json')); print('PAT in env:', 'GITHUB_PERSONAL_ACCESS_TOKEN' in d.get('env', {}))"
# Expected: PAT in env: False
echo "PAT in env: ${GITHUB_PERSONAL_ACCESS_TOKEN:0:4}..."
# Expected: PAT in env: ghp_...
```

---

## Task 2: [정리] SNAPSHOT.txt 아카이브

**Files:**
- Delete: `/c/dev/01_projects/01_orchestration/context/SNAPSHOT.txt`

**Step 1: 내용 확인 후 아카이브**

```bash
mkdir -p /c/dev/01_projects/01_orchestration/context/archive
mv /c/dev/01_projects/01_orchestration/context/SNAPSHOT.txt \
   /c/dev/01_projects/01_orchestration/context/archive/SNAPSHOT.2026-02-09.txt
```

**Step 2: 검증**

```bash
ls /c/dev/01_projects/01_orchestration/context/SNAPSHOT.txt 2>/dev/null && echo "FAIL" || echo "PASS: 삭제됨"
ls /c/dev/01_projects/01_orchestration/context/archive/
```

**Step 3: 커밋**

```bash
git -C /c/dev/01_projects/01_orchestration add -A
git -C /c/dev/01_projects/01_orchestration commit -m "[orchestration] SNAPSHOT.txt 아카이브 (stale 2026-02-09 데이터)"
```

---

## Task 3: [보안] PreToolUse 페일클로즈 전환

현재 python3 파싱 실패 시 빈 문자열 → 차단 안 됨 (페일오픈). `|| exit 2`로 페일클로즈 전환.

**Files:**
- Modify: `~/.claude/settings.json` — PreToolUse Bash hook 명령어

**Step 1: 현재 PreToolUse command 확인**

```bash
python3 -c "
import json
with open('/c/Users/pauls/.claude/settings.json') as f:
    d = json.load(f)
pre = d.get('hooks', {}).get('PreToolUse', [])
for h in pre:
    for hook in h.get('hooks', []):
        print(hook.get('command', '')[:200])
        print('---')
"
```

**Step 2: 페일클로즈 패치 적용**

`|| exit 2` 가 없는 위험 명령 차단 라인에 추가.
예: `python3 ... | grep ...` → `python3 ... | grep ... || exit 2`

```python
# 패치 스크립트
import json, re

path = '/c/Users/pauls/.claude/settings.json'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()
    d = json.loads(content)

pre_hooks = d.get('hooks', {}).get('PreToolUse', [])
for hook_group in pre_hooks:
    for hook in hook_group.get('hooks', []):
        cmd = hook.get('command', '')
        # 위험 명령 감지 후 || exit 2 없으면 추가
        if ('rm -rf' in cmd or 'force' in cmd or 'DANGEROUS' in cmd):
            if '|| exit 2' not in cmd and 'exit 2' not in cmd:
                hook['command'] = cmd.rstrip() + ' || exit 2'
                print(f"Patched: {cmd[:50]}...")

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("Done")
```

**Step 3: 검증**

```bash
python3 -c "
import json
d = json.load(open('/c/Users/pauls/.claude/settings.json'))
pre = d['hooks']['PreToolUse']
print(json.dumps(pre, indent=2, ensure_ascii=False)[:500])
"
```

---

## Task 4: [자동화] SessionStart docs-review 7일 경과 경고

마지막 docs-review 실행일을 체크해 7일 초과 시 경고 출력.

**Files:**
- Modify: `~/.claude/settings.json` — SessionStart hooks에 명령어 추가

**Step 1: 추가할 명령어 로직**

```bash
# docs-review 마지막 실행일 체크 (LOG에서 감지)
LAST=$(grep -r "docs-review" /c/dev/01_projects/01_orchestration/context/logs/*.md 2>/dev/null | \
       grep -o '[0-9]\{4\}-[0-9]\{2\}-[0-9]\{2\}' | sort | tail -1)
if [ -n "$LAST" ]; then
    DAYS=$(( ( $(date +%s) - $(date -d "$LAST" +%s 2>/dev/null || echo 0) ) / 86400 ))
    [ "$DAYS" -gt 7 ] && echo "⚠️  docs-review 마지막 실행: ${DAYS}일 전 (/docs-review 권장)"
fi
true
```

**Step 2: settings.json SessionStart에 추가**

```python
import json

path = '/c/Users/pauls/.claude/settings.json'
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

new_hook = {
    "type": "command",
    "command": "LAST=$(grep -r 'docs-review' /c/dev/01_projects/01_orchestration/context/logs/*.md 2>/dev/null | grep -o '[0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\}' | sort | tail -1); if [ -n \"$LAST\" ]; then DAYS=$(( ( $(date +%s) - $(date -d \"$LAST\" +%s 2>/dev/null || echo $(date +%s)) ) / 86400 )); [ \"$DAYS\" -gt 7 ] && echo \"⚠️  docs-review 마지막: ${DAYS}일 전 (/docs-review 권장)\"; fi; true",
    "async": True
}

# SessionStart 첫 번째 그룹에 추가
d['hooks']['SessionStart'][0]['hooks'].append(new_hook)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("Added docs-review warning to SessionStart")
```

---

## Task 5: [자동화] SessionEnd MEMORY.md 150줄 경고

**Files:**
- Modify: `~/.claude/settings.json` — SessionEnd hooks에 명령어 추가

**Step 1: 추가할 명령어**

```bash
LINES=$(wc -l < /c/Users/pauls/.claude/projects/C--dev/memory/MEMORY.md 2>/dev/null || echo 0)
[ "$LINES" -gt 150 ] && echo "⚠️  MEMORY.md ${LINES}줄 — 200줄 한계 근접 (/memory-review 권장)"
true
```

**Step 2: settings.json SessionEnd에 추가**

```python
import json

path = '/c/Users/pauls/.claude/settings.json'
with open(path, 'r', encoding='utf-8') as f:
    d = json.load(f)

new_hook = {
    "type": "command",
    "command": "LINES=$(wc -l < /c/Users/pauls/.claude/projects/C--dev/memory/MEMORY.md 2>/dev/null || echo 0); [ \"$LINES\" -gt 150 ] && echo \"⚠️  MEMORY.md ${LINES}줄 — /memory-review 권장\" || true",
    "async": True
}

d['hooks']['SessionEnd'][0]['hooks'].append(new_hook)

with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("Added MEMORY.md line count warning to SessionEnd")
```

---

## Task 6: [자동화] compressor → METRICS.md auto-append

compressor 에이전트가 4곳 저장 시 METRICS.md에도 요약 행을 자동 추가.

**Files:**
- Modify: `~/.claude/agents/compressor.md`
- Create if missing: `/c/dev/01_projects/01_orchestration/context/METRICS.md`

**Step 1: METRICS.md 파일 확인**

```bash
cat /c/dev/01_projects/01_orchestration/context/METRICS.md 2>/dev/null | head -20 || echo "파일 없음"
```

**Step 2: compressor.md 에 METRICS append 지시 추가**

현재 compressor.md의 "저장 목록" 섹션 끝에 다음을 추가:

```markdown
5. **METRICS.md** (`/c/dev/01_projects/01_orchestration/context/METRICS.md`)
   다음 행을 파일 끝에 append:
   `| {날짜} | {완료 태스크 수} | {주요 프로젝트} | {결정 사항 수} |`
   파일이 없으면 헤더 행 먼저 생성:
   `| 날짜 | 완료 | 프로젝트 | 결정 |`
```

**Step 3: 검증**

compressor 에이전트를 수동 호출해 METRICS.md에 행이 추가되는지 확인.

---

## Task 7: [statusline] 미커밋 파일 수 표시

**Files:**
- Modify: `~/.claude/statusline.py`

**Step 1: 미커밋 수 계산 로직 추가**

현재 `parts` 리스트 생성 부분 뒤에 추가:

```python
# 미커밋 파일 수 (orchestration + portfolio)
try:
    import subprocess
    o_cnt = subprocess.run(
        ["git", "-C", "/c/dev/01_projects/01_orchestration", "status", "-s"],
        capture_output=True, text=True, timeout=2
    ).stdout.strip().count('\n') + (1 if subprocess.run(
        ["git", "-C", "/c/dev/01_projects/01_orchestration", "status", "-s"],
        capture_output=True, text=True, timeout=2
    ).stdout.strip() else 0)
    p_cnt = subprocess.run(
        ["git", "-C", "/c/dev/01_projects/02_portfolio", "status", "-s"],
        capture_output=True, text=True, timeout=2
    ).stdout.strip().count('\n') + (1 if subprocess.run(
        ["git", "-C", "/c/dev/01_projects/02_portfolio", "status", "-s"],
        capture_output=True, text=True, timeout=2
    ).stdout.strip() else 0)
    # 간결하게: subprocess 1번만 호출
    o_out = subprocess.run(["git", "-C", "/c/dev/01_projects/01_orchestration", "status", "-s"], capture_output=True, text=True, timeout=2).stdout.strip()
    p_out = subprocess.run(["git", "-C", "/c/dev/01_projects/02_portfolio", "status", "-s"], capture_output=True, text=True, timeout=2).stdout.strip()
    o_cnt = len(o_out.splitlines()) if o_out else 0
    p_cnt = len(p_out.splitlines()) if p_out else 0
    total = o_cnt + p_cnt
    if total > 0:
        parts.append(f"\033[31m↑{total}\033[0m")  # 빨간색으로 미커밋 수
except Exception:
    pass
```

실제 삽입 위치: `print(" | ".join(parts))` 바로 위.

**Step 2: 검증**

```bash
echo '{}' | python3 /c/Users/pauls/.claude/statusline.py
# Expected: 시간 | 모델 | 프로젝트 | ctx:% | $0.00 | ↑N (미커밋 있을 때)
```

---

## Task 8: [Auto Memory] Phase 1 디버깅

**Files:**
- Read+Debug: `~/.claude/hooks/session-stop.sh`
- Read+Debug: `~/.claude/scripts/analyze-session.sh`

**Step 1: 최신 JSONL 파일로 수동 테스트**

```bash
LATEST=$(ls -t /c/Users/pauls/.claude/projects/C--dev/*.jsonl 2>/dev/null | head -1)
echo "테스트 파일: $LATEST"
echo "{\"transcript_path\":\"$LATEST\"}" | bash /c/Users/pauls/.claude/hooks/session-stop.sh
cat /c/Users/pauls/.claude/projects/C--dev/memory/pending.md | tail -30
```

**Step 2: 결과 분석**

- pending.md에 새 섹션이 추가되면 → PASS (Phase 1 작동)
- "No notable items detected" → 정상 (감지된 패턴 없음)
- "Session file not found" → transcript_path 전달 문제 → jq 없음 확인

```bash
which jq || echo "jq 없음 — grep 폴백 경로"
```

**Step 3: jq 없을 때 폴백 검증**

```bash
# jq 없는 환경 시뮬레이션
echo '{"transcript_path":"'"$LATEST"'"}' | bash -c '
    INPUT=$(cat)
    TRANSCRIPT=$(echo "$INPUT" | grep -o "\"transcript_path\":\"[^\"]*\"" | cut -d"\"" -f4)
    echo "Extracted: $TRANSCRIPT"
'
```

**Step 4: 문제 발견 시 수정**

jq 경로 문제 시 → `jq` 설치 또는 grep 폴백 강화:

```bash
# analyze-session.sh detect_preferences 함수 — JSONL 구조에 맞게 수정
# "type":"user" → content 추출 개선
```

---

## Task 9: [decisions] git-tracked 전환

**Files:**
- Move: `~/.claude/decisions.md` → `/c/dev/01_projects/01_orchestration/context/decisions.md`
- Modify: `~/.claude/settings.json` — SessionStart hook의 decisions.md 경로 업데이트

**Step 1: 파일 이동**

```bash
cp /c/Users/pauls/.claude/decisions.md \
   /c/dev/01_projects/01_orchestration/context/decisions.md
echo "복사 완료 — 원본 유지 (심볼릭 링크 고려)"
```

**Step 2: settings.json SessionStart hook 경로 수정**

```python
import json

path = '/c/Users/pauls/.claude/settings.json'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# decisions.md 경로 교체
content = content.replace(
    '/c/Users/pauls/.claude/decisions.md',
    '/c/dev/01_projects/01_orchestration/context/decisions.md'
)

d = json.loads(content)
with open(path, 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)
print("decisions.md path updated in settings.json")
```

**Step 3: 심볼릭 링크 (선택사항)**

```bash
# 기존 경로로도 접근 가능하게 유지
ln -sf /c/dev/01_projects/01_orchestration/context/decisions.md \
       /c/Users/pauls/.claude/decisions.md
```

**Step 4: git 커밋**

```bash
git -C /c/dev/01_projects/01_orchestration add context/decisions.md
git -C /c/dev/01_projects/01_orchestration commit -m "[orchestration] decisions.md git-tracked 전환"
```

---

## Task 10: [에이전트] morning-briefer 통합 엔트리포인트

**Files:**
- Modify: `~/.claude/agents/morning-briefer.md` — catchup + orch-state 내부 호출 지시 추가

**Step 1: morning-briefer.md 현재 내용 확인**

```bash
cat /c/Users/pauls/.claude/agents/morning-briefer.md
```

**Step 2: 통합 지시 추가**

morning-briefer.md 내부에 다음 섹션 추가:

```markdown
## 실행 순서
1. `/c/Users/pauls/.claude/projects/C--dev/memory/session-summary.md` 최신 항목 읽기 (catchup 역할)
2. orchestration STATE.md + 미완료 TODO 확인 (orch-state 역할)
3. 각 프로젝트 git status 요약
4. 통합 브리핑 출력

> orch-state, catchup 에이전트를 별도 호출할 필요 없음. morning-briefer가 통합 엔트리포인트.
```

---

## Task 11: [정리] KNOWLEDGE.md stale 항목 업데이트

**Files:**
- Modify: `~/.claude/agents/` 또는 `/c/dev/01_projects/01_orchestration/` 내 KNOWLEDGE.md

**Step 1: KNOWLEDGE.md 위치 확인**

```bash
find /c/dev/01_projects/01_orchestration -name "KNOWLEDGE.md" 2>/dev/null
find /c/Users/pauls/.claude -name "KNOWLEDGE.md" 2>/dev/null
```

**Step 2: stale 항목 수정**

수정 대상:
- `ai-config: main 브랜치` → `ai-config: DELETED (orchestration/config/ 로 이전)`
- `Co-Authored-By: Claude Sonnet 4.5` → `Claude Sonnet 4.6 (1M context)`
- 존재하지 않는 경로(`C:\dev\02_ai_config`) 제거 또는 주석 처리

---

## 실행 체크리스트

| # | 태스크 | 우선순위 | 파일 수 | 상태 |
|---|--------|----------|---------|------|
| 1 | PAT 제거 (사용자 로테이션 먼저) | 🔴 긴급 | 2 | - |
| 2 | SNAPSHOT.txt 아카이브 | 🟡 중간 | 1 | - |
| 3 | PreToolUse 페일클로즈 | 🟡 중간 | 1 | - |
| 4 | SessionStart docs-review 경고 | 🟢 낮음 | 1 | - |
| 5 | SessionEnd MEMORY.md 경고 | 🟢 낮음 | 1 | - |
| 6 | compressor METRICS.md append | 🟢 낮음 | 1 | - |
| 7 | statusline.py 미커밋 수 | 🟢 낮음 | 1 | - |
| 8 | Auto Memory 디버깅 | 🟡 중간 | 2 | - |
| 9 | decisions git-tracked | 🟡 중간 | 2 | - |
| 10 | morning-briefer 통합 | 🟢 낮음 | 1 | - |
| 11 | KNOWLEDGE.md stale 정리 | 🟢 낮음 | 1 | - |

병렬 실행 가능: Task 2+3, Task 4+5, Task 6+7, Task 10+11
순차 필요: Task 1 → (사용자 토큰 로테이션) → 나머지
