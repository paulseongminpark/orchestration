# Phase 1: Auto Memory Detection System

> **Status: COMPLETED** (2026-02-18 구현, 2026-02-19 검증)

**Goal:** 세션 종료 시 자동으로 메모리 후보를 감지하여 pending.md에 기록

**Architecture:** SessionEnd Hook → analyze-session.sh → pending.md 누적 → /sync-all로 검증 → MEMORY.md 이동

**Tech Stack:** Bash, jq (선택), grep/awk

---

## 구현 완료 파일

| 파일 | 경로 | 상태 |
|------|------|------|
| `analyze-session.sh` | `~/.claude/scripts/analyze-session.sh` | ✅ 완성 |
| `session-stop.sh` | `~/.claude/hooks/session-stop.sh` | ✅ 완성 |
| `sync-memory.sh` | `~/.claude/scripts/sync-memory.sh` | ✅ 완성 (Phase 2) |
| `memory-review.sh` | `~/.claude/scripts/memory-review.sh` | ✅ 완성 (Phase 3) |
| `pending.md` | `~/.claude/projects/C--dev/memory/pending.md` | ✅ 운용 중 |
| Hook 등록 | `~/.claude/settings.json` → `SessionEnd` | ✅ 완성 |

---

## 실제 구현 내용

### analyze-session.sh

세션 transcript를 분석하여 pending.md에 기록:

```bash
#!/bin/bash
SESSION_FILE="$1"
PENDING_FILE="/c/Users/pauls/.claude/projects/C--dev/memory/pending.md"

detect_patterns() {
    # "name" 필드 추출 (실제 필드명, tool_name 아님)
    grep -o '"name":"[^"]*"' "$session_file" | grep -v '"name":"message"' | \
        cut -d'"' -f4 | sort | uniq -c | sort -rn | \
        awk '$1 >= 2 {printf "- [ ] 도구 반복: %s | 횟수: %d | 신뢰도: %s\n", \
             $2, $1, ($1 >= 3 ? "high" : "medium")}'
}

detect_errors() {
    # "type":"progress" 제외, node_modules 제외
    grep -i -E '(error|failed|exception)' "$session_file" | \
        grep -v '"type":"progress"' | grep -v "node_modules" | head -5
}

detect_preferences() {
    # "type":"user" 필드 (role:"human" 아님)
    grep -i -E '(항상|절대|always|never|prefer|기억해)' "$session_file" | \
        grep '"type":"user"'
}

# 결과가 하나라도 있을 때만 pending.md에 추가 (빈 결과 스킵)
update_pending "$PENDING_FILE"
```

**핵심 수정사항 (플랜 대비):**
- `tool_name` → `name` (실제 JSON 필드명)
- `"role":"user"` → `"type":"user"` (실제 구조)
- 빈 결과 스킵 로직 추가

---

### session-stop.sh

Hook 방식으로 stdin JSON 파싱:

```bash
#!/bin/bash
# stdin에서 SessionEnd JSON 받기
INPUT=$(cat /dev/stdin)

# jq 있으면 사용, 없으면 grep으로 대체
TRANSCRIPT=$(echo "$INPUT" | jq -r '.transcript_path // empty')
SESSION_ID=$(echo "$INPUT" | jq -r '.session_id // empty')

# transcript_path 우선, 없으면 session_id로 경로 구성
if [ -n "$TRANSCRIPT" ] && [ -f "$TRANSCRIPT" ]; then
    bash "$SCRIPT_DIR/analyze-session.sh" "$TRANSCRIPT"
fi
```

**핵심 수정사항 (플랜 대비):**
- `$1` 인자 방식 → stdin JSON 방식 (실제 Claude Code hook 동작)
- jq/grep 이중 지원

---

### settings.json Hook 등록

```json
"SessionEnd": [
  {
    "hooks": [
      {
        "type": "command",
        "command": "bash /c/Users/pauls/.claude/hooks/session-stop.sh",
        "timeout": 30
      }
    ]
  }
]
```

---

### sync-memory.sh (Phase 2 — /sync-all)

pending.md 항목 요약 출력 → Claude가 채택/보류/삭제 판단:
- 세션 분석 결과 없으면 조기 종료
- MEMORY.md 현재 내용 함께 출력
- 4가지 검증 기준 안내

### memory-review.sh (Phase 3 — /memory-review)

MEMORY.md 상태 요약 + 리뷰 가이드:
- 줄 수 / 항목 수 / 200줄 제한 상태
- CLAUDE.md 규칙 출력 (모순 검사용)
- 리뷰 기준 5가지

---

## 검증 완료 항목

- [x] pending.md 템플릿 생성됨
- [x] analyze-session.sh 패턴/에러/선호사항 감지
- [x] SessionEnd Hook 자동 실행
- [x] pending.md에 결과 누적
- [x] /sync-all → pending.md 검증 워크플로우
- [x] /memory-review → 주간 정리 워크플로우

---

## 알려진 제약사항

1. **jq 없는 환경:** grep/awk 대체 (정확도 다소 낮음)
2. **중복 필터링:** analyze-session.sh 단계에서는 미구현 → /sync-all에서 Claude가 판단
3. **대용량 세션:** head -5, head -60 등으로 제한하여 처리

---

## Phase 2 / Phase 3

- **Phase 2:** `/sync-all` → `sync-memory.sh` → MEMORY.md 검증 이동 ✅
- **Phase 3:** `/memory-review` → `memory-review.sh` → 주간 정리 ✅

두 Phase 모두 구현 완료. 전체 Auto Memory 시스템 운용 중.
