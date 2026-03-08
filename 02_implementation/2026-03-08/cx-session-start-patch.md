#!/bin/bash
# session-start.sh — 세션 시작 브리핑 (v3.3.1 경량화)

echo "High Effort Mode Active"
echo '📋 TASK_CONTRACT 작성 권장 — 세션 목표와 완료 조건을 먼저 정의하세요'

# 세션 목표 초기화
python3 -c "import os; f=os.path.join(os.environ.get('TEMP','/tmp'),'claude-session-goal'); os.path.exists(f) and os.remove(f)" 2>/dev/null || true

# 0. Obsidian 미의도 편집 감지 (dev-vault)
VAULT_DIRTY=$(git -C /c/dev status -s --ignore-submodules=dirty 2>/dev/null | grep -v '^\?' | head -5)
if [ -n "$VAULT_DIRTY" ]; then
    echo ""
    echo "⚠️  Obsidian 미의도 변경 감지 (git checkout으로 복구 권장):"
    echo "$VAULT_DIRTY"
fi

# 1. 프로젝트 미커밋 상태
echo "=== 프로젝트 상태 ==="
for PROJ in "01_orchestration" "02_portfolio" "03_tech-review"; do
    DIR="/c/dev/01_projects/$PROJ"
    if [ -d "$DIR/.git" ]; then
        CNT=$(git -C "$DIR" status -s 2>/dev/null | wc -l | tr -d ' ')
        NAME=$(echo "$PROJ" | sed 's/0[0-9]_//')
        if [ "$CNT" -gt 0 ]; then
            echo "  ⚠️  $NAME: ${CNT}개 미커밋"
        else
            echo "  ✅ $NAME: clean"
        fi
    fi
done
echo "=================="

# 2. 미반영 결정 사항 (❌만, 최대 5건)
DECISIONS="/c/dev/01_projects/01_orchestration/decisions.md"
if [ -f "$DECISIONS" ]; then
    PENDING=$(sed -n '/^## 미반영$/,/^## /p' "$DECISIONS" 2>/dev/null | grep '❌')
    if [ -n "$PENDING" ]; then
        CNT=$(echo "$PENDING" | wc -l | tr -d ' ')
        echo ""
        echo "=== 미반영 결정 (${CNT}건, ❌만) ==="
        echo "$PENDING" | head -5
        [ "$CNT" -gt 5 ] && echo "  ... 외 $((CNT - 5))건"
        echo "=================="
    fi
fi

# 3. live-context.md 최근 5줄
LIVE_CTX="/c/dev/01_projects/01_orchestration/_auto/live-context.md"
if [ -f "$LIVE_CTX" ]; then
    RECENT=$(tail -5 "$LIVE_CTX" 2>/dev/null | grep -v '^$')
    if [ -n "$RECENT" ]; then
        echo ""
        echo "=== 크로스세션 (최근 5건) ==="
        echo "$RECENT"
        echo "=================="
    fi
fi

# 4. compact 스냅샷 존재 시 알림
CHAIN_TEMP="/c/dev/01_projects/01_orchestration/_auto/.chain-temp"
LATEST_SNAP=$(ls -t "$CHAIN_TEMP"/snapshot-*.md 2>/dev/null | head -1)
if [ -n "$LATEST_SNAP" ]; then
    echo ""
    echo "📋 이전 compact 스냅샷: $LATEST_SNAP"
fi

# 6. 미검토 선호도 알림
PENDING_FILE="/c/Users/pauls/.claude/projects/C--dev/memory/pending.md"
if [ -f "$PENDING_FILE" ]; then
    PREF_CNT=$(grep -c "출처: 명시적 요청" "$PENDING_FILE" 2>/dev/null || echo 0)
    if [ "$PREF_CNT" -gt 0 ]; then
        echo ""
        echo "💬 미검토 선호도 ${PREF_CNT}건 — /sync 권장"
    fi
fi

# 5. 외부 메모리 컨텍스트 (최근 결정/질문/실패/인사이트)
MEM_CTX=$(PYTHONIOENCODING=utf-8 python3 /c/dev/01_projects/06_mcp-memory/scripts/session_context.py 2>/dev/null)
if [ -n "$MEM_CTX" ]; then
    echo ""
    echo "=== 외부 메모리 컨텍스트 ==="
    echo "$MEM_CTX"
    echo "=================="
fi

true
