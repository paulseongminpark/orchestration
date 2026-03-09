# Memory-Merger 설계 — Phase 3-04

> 성숙한 memory 노드를 orchestration 파일 시스템으로 승격시키는 브릿지
> 작성: 2026-03-09
> 상태: 설계 완료, 구현 대기

---

## 문제

현재 시스템에 이미 있는 것:
- `analyze_signals`: Signal 클러스터 분석 + 성숙도 + 추천 (auto_promote/user_review)
- `promote_node`: 3-gate 검증 (SWR/Bayesian/MDL) → DB에서 type 변경
- `get_becoming`: 승격 후보 목록 조회

**빠진 것: 승격 후 "어디에 반영할 것인가"**
- promote_node는 DB 타입만 바꿈 → KNOWLEDGE.md, rules/ 등 파일에 반영 안 됨
- 세션 시작 시 승격 후보 알림 없음
- 승격 콘텐츠의 포맷 표준 없음

---

## 아키텍처

```
┌─────────────────────────────────────────────────┐
│                  Memory-Merger                   │
├─────────────────────────────────────────────────┤
│                                                  │
│  [1] Detect        session-start.sh              │
│      │             get_becoming() 호출           │
│      │             "N개 승격 준비" 알림           │
│      ▼                                          │
│  [2] Present       Claude가 후보 표시            │
│      │             summary + domains + maturity  │
│      │             사용자에게 승인 요청           │
│      ▼                                          │
│  [3] Promote       promote_node() 호출           │
│      │             3-gate 통과 확인              │
│      ▼                                          │
│  [4] Merge         대상 파일에 콘텐츠 추가       │
│      │             KNOWLEDGE.md / rules/*.md     │
│      ▼                                          │
│  [5] Record        decisions.md + mcp-memory     │
│                    "승격 완료" 기록              │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 상세 설계

### 1. Detect — 세션 시작 시 자동 감지

**수정 대상**: `session-start.sh`

```bash
# 7. Memory-Merger: 승격 후보 알림
MERGER_OUT=$(PYTHONIOENCODING=utf-8 python3 -c "
import sys; sys.path.insert(0, '/c/dev/01_projects/06_mcp-memory')
from tools.get_becoming import get_becoming
result = get_becoming(top_k=5)
ready = result.get('ready_count', 0)
if ready > 0:
    nodes = [n for n in result['nodes'] if n['maturity'] > 0.6]
    for n in nodes[:3]:
        print(f\"  #{n['id']} [{n['type']}→{','.join(n['can_promote_to'])}] {n['summary'][:60]}\")
    print(f'total_ready={ready}')
" 2>/dev/null)

if [ -n "$MERGER_OUT" ]; then
    READY_CNT=$(echo "$MERGER_OUT" | grep 'total_ready=' | sed 's/total_ready=//')
    echo ""
    echo "=== Memory-Merger: ${READY_CNT}개 승격 후보 ==="
    echo "$MERGER_OUT" | grep -v 'total_ready='
    echo "  → '승격 진행' 또는 '/merge' 로 시작"
    echo "=================="
fi
```

**비용**: python3 호출 1회, ~200ms. session-start.sh 마지막에 추가.

### 2. Present — 후보 상세 표시

Claude가 사용자에게 보여줄 포맷:

```
## 승격 후보 3건

| # | ID | 현재 타입 | 목표 | 성숙도 | 요약 |
|---|----|----------|------|--------|------|
| 1 | #4301 | Signal | Pattern | 0.82 | checkpoint 전 다른 pane 확인 필요 |
| 2 | #4305 | Signal | Insight | 0.71 | defer_loading auto 모드로 55K→3K |
| 3 | #4310 | Observation | Pattern | 0.65 | Codex sandbox는 프로젝트 dir에서 실행 |

승격할 항목 번호를 선택하세요 (예: 1,3):
```

### 3. Promote — 3-gate 승격

기존 `promote_node` MCP 도구 그대로 사용:

```python
promote_node(
    node_id=4301,
    target_type="Pattern",
    reason="3회+ recall, 30일+ 경과, maturity 0.82",
    related_ids=[4302, 4303]  # 같은 클러스터
)
```

Gate 실패 시 → 사용자에게 보고, skip_gates 사용 여부 확인.

### 4. Merge — 파일 시스템 반영

**승격 대상 → 반영 위치 매핑:**

| 목표 타입 | 반영 파일 | 섹션 |
|----------|----------|------|
| Pattern | KNOWLEDGE.md | 해당 도메인 섹션 하단 |
| Principle | KNOWLEDGE.md | 새 섹션 또는 기존 원칙에 병합 |
| Framework | KNOWLEDGE.md | 새 섹션 |
| Heuristic | rules/*.md | 관련 규칙 파일 |
| Insight | KNOWLEDGE.md (또는 무시) | 참고사항으로만 |

**병합 포맷:**

```markdown
## {섹션명}
...기존 내용...

- **{승격 내용 1줄 요약}** (← Memory-Merger #4301, 2026-03-09)
```

**규칙:**
- 1줄 요약으로 압축 (KNOWLEDGE.md는 간결해야 함)
- 출처 마커 `(← Memory-Merger #{id}, {date})` 필수
- 중복 체크: 이미 KNOWLEDGE.md에 유사 내용 있으면 병합/업데이트

### 5. Record — 추적

```
decisions.md:
  2026-03-09 [orchestration] Memory-Merger: #4301 Signal→Pattern 승격 | pf:❌ tr:❌

mcp-memory:
  remember(
    content="Memory-Merger 승격: #4301 → Pattern, KNOWLEDGE.md 반영",
    type="Decision",
    tags="memory-merger,promotion"
  )
```

---

## 구현 계획

### M1: session-start.sh 수정 (30분)
- get_becoming 호출 추가
- 승격 후보 알림 출력

### M2: /merge 스킬 생성 (1시간)
- 승격 후보 표시 → 사용자 선택 → promote_node → 파일 반영
- `~/.claude/skills/merge/SKILL.md`

### M3: KNOWLEDGE.md 병합 로직 (30분)
- 도메인 → 섹션 매핑
- 중복 체크 (grep으로 유사 내용 검색)
- 출처 마커 자동 추가

### M4: 검증 (30분)
- 실제 Signal 1건 승격 테스트
- KNOWLEDGE.md 반영 확인
- decisions.md 기록 확인

---

## 미결 사항

1. **자동 vs 수동**: auto_promote 추천이면 사용자 확인 없이 진행할 것인가?
   → 현재 설계: 항상 사용자 확인 (안전 우선)
2. **승격 후 원본 노드**: DB에서 삭제? 타입만 변경?
   → 현재 설계: 타입 변경 (promote_node 기본 동작), 삭제 안 함
3. **rules/ 반영**: rules/*.md에 직접 쓸 것인가, KNOWLEDGE.md만?
   → 현재 설계: 기본은 KNOWLEDGE.md, Heuristic만 rules/
4. **빈도**: 매 세션마다? 일주일에 한 번?
   → 현재 설계: session-start에서 알림, 실행은 사용자 판단

---

## 의존성

- mcp-memory v2.2.1+ (get_becoming, promote_node 필요)
- Phase 2 composite scoring 완료 (승격 판단의 정확도 향상)
