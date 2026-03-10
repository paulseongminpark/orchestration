# Ontology v3 — Impl Design

> 입력: R3 최종 보고서 (17개 결정, V3-01~V3-17)
> 출력: 코드 수준 스펙 — 이 문서만 읽고 구현 가능해야 함
> 대상: mcp-memory 코드베이스 + orchestration 에이전트

---

## 코드베이스 맵

| 파일 | 역할 | 수정 여부 |
|------|------|-----------|
| `storage/sqlite_store.py:33` | DB init (CREATE TABLE) | **수정** — 컬럼 추가 |
| `tools/remember.py:240` | remember() MCP 도구 | **수정** — retrieval_hints 파라미터 |
| `tools/recall.py:11` | recall() MCP 도구 | 수정 없음 (Phase 5 Step 4) |
| `storage/hybrid.py:448` | hybrid_search() | **수정** — co-retrieval boost |
| `storage/hybrid.py:531-595` | composite scoring | **수정** — co-retrieval weight |
| `enrichment/classifier.py:54` | 타입 분류기 | **수정** — 15개 타입 프롬프트 |
| `scripts/daily_enrich.py` | enrichment 파이프라인 | **수정** — E-NEW, co-retrieval 단계 |
| `server.py:41-133` | MCP 서버 (remember 등록) | **수정** — retrieval_hints 스키마 |
| `config.py` | 설정값 | **수정** — CO_RETRIEVAL_WEIGHT 등 |

---

## D-1: DB 스키마 변경

### 마이그레이션 SQL

```sql
-- V3-05: nodes.retrieval_hints
ALTER TABLE nodes ADD COLUMN retrieval_hints TEXT DEFAULT NULL;
-- JSON: {"when_needed": "...", "related_queries": [...], "context_keys": [...]}

-- V3-10: edges co-retrieval
ALTER TABLE edges ADD COLUMN co_retrieval_count INTEGER DEFAULT 0;
ALTER TABLE edges ADD COLUMN co_retrieval_boost REAL DEFAULT 0.0;
```

### sqlite_store.py 수정

`init_db()` (line 33)의 CREATE TABLE nodes에 `retrieval_hints TEXT DEFAULT NULL` 추가.
CREATE TABLE edges에 `co_retrieval_count INTEGER DEFAULT 0, co_retrieval_boost REAL DEFAULT 0.0` 추가.

### 마이그레이션 스크립트

```python
# scripts/migrate_v3.py
def migrate():
    conn = get_connection()

    # 1. 컬럼 존재 확인 후 추가
    cols = {c[1] for c in conn.execute("PRAGMA table_info(nodes)").fetchall()}
    if "retrieval_hints" not in cols:
        conn.execute("ALTER TABLE nodes ADD COLUMN retrieval_hints TEXT DEFAULT NULL")

    cols_e = {c[1] for c in conn.execute("PRAGMA table_info(edges)").fetchall()}
    if "co_retrieval_count" not in cols_e:
        conn.execute("ALTER TABLE edges ADD COLUMN co_retrieval_count INTEGER DEFAULT 0")
        conn.execute("ALTER TABLE edges ADD COLUMN co_retrieval_boost REAL DEFAULT 0.0")

    # 2. type_defs deprecated 설정 (V3-01, V3-02, V3-04)
    SIMPLE_MAP = {
        "Skill": "Tool", "Agent": "Tool",
        "SystemVersion": "Project",
        "Breakthrough": "Insight", "Conversation": "Observation",
        "Tension": "Question", "AntiPattern": "Failure",
        "Preference": "Identity",
        "Philosophy": "Principle", "Value": "Principle",
        "Belief": "Principle", "Axiom": "Principle",
    }
    for old_type, new_type in SIMPLE_MAP.items():
        conn.execute("""
            UPDATE type_defs SET
                status='deprecated', deprecated_reason='v3 타입 축소: 1:1 매핑',
                replaced_by=?, deprecated_at=datetime('now'), version=version+1
            WHERE name=? AND status='active'
        """, (new_type, old_type))

        count = conn.execute(
            "UPDATE nodes SET type=? WHERE type=? AND status='active'",
            (new_type, old_type)
        ).rowcount
        print(f"  {old_type} → {new_type}: {count}개")

    # 3. Workflow는 별도 (V3-03, LLM 배치)
    # Evolution, Connection도 별도 (edge 전환)

    conn.commit()
```

---

## D-2: API 변경

### remember() 파라미터 추가 (V3-05)

```python
# server.py — remember 스키마에 추가
"retrieval_hints": {
    "type": "object",
    "description": "인출 맥락 힌트 (선택). when_needed, related_queries, context_keys",
    "properties": {
        "when_needed": {"type": "string"},
        "related_queries": {"type": "array", "items": {"type": "string"}},
        "context_keys": {"type": "array", "items": {"type": "string"}}
    }
}

# tools/remember.py — remember() 함수 시그니처
def remember(content, type="", tags="", project="", metadata=None,
             confidence=1.0, source="claude", retrieval_hints=None):
    # ... 기존 로직 ...
    # store 시 retrieval_hints JSON 직렬화
    if retrieval_hints:
        hints_json = json.dumps(retrieval_hints, ensure_ascii=False)
    else:
        hints_json = None
    # INSERT에 retrieval_hints=hints_json 추가
```

### 하위 호환

retrieval_hints는 optional (DEFAULT NULL). 기존 호출 100% 호환.

---

## D-3: enrichment 확장 (V3-06)

### E-NEW: retrieval_hints 배치 생성

```python
# scripts/enrich/hints_generator.py (신규)
def generate_retrieval_hints(node_content, node_type, node_tags, model="gpt-5-mini"):
    """노드 content에서 retrieval_hints 자동 생성."""
    prompt = f"""이 기억 노드의 인출 맥락을 설계하라.

노드 타입: {node_type}
내용: {node_content[:500]}
태그: {node_tags}

다음 JSON으로 응답:
{{
    "when_needed": "이 기억이 필요한 구체적 상황 1문장",
    "related_queries": ["예상 검색어 3-5개"],
    "context_keys": ["맥락 키워드 3-5개"]
}}"""
    # LLM 호출 → JSON 파싱 → 반환

def batch_generate_hints(conn, batch_size=50, model="gpt-5-mini"):
    """retrieval_hints가 NULL인 노드에 배치 생성."""
    nodes = conn.execute("""
        SELECT id, type, content, tags FROM nodes
        WHERE status='active' AND retrieval_hints IS NULL
        LIMIT ?
    """, (batch_size,)).fetchall()

    for node_id, ntype, content, tags in nodes:
        hints = generate_retrieval_hints(content, ntype, tags, model)
        conn.execute(
            "UPDATE nodes SET retrieval_hints=? WHERE id=?",
            (json.dumps(hints, ensure_ascii=False), node_id)
        )
    conn.commit()
```

### daily_enrich.py에 추가

```python
# phase1() 또는 새 phase에 추가
def phase_hints(conn, api):
    """E-NEW: retrieval_hints 배치 생성."""
    from scripts.enrich.hints_generator import batch_generate_hints
    batch_generate_hints(conn, batch_size=100, model=api.bulk_model)
```

### enrichment 시 embedding_text에 반영

```python
# 기존 embedding_text 생성 로직에 추가
def build_embedding_text(node):
    parts = [node['content'], node.get('summary', '')]
    hints = json.loads(node.get('retrieval_hints') or '{}')
    if hints.get('when_needed'):
        parts.append(hints['when_needed'])
    if hints.get('related_queries'):
        parts.extend(hints['related_queries'])
    return '\n'.join(filter(None, parts))
```

### FTS5 rebuild에 반영

```python
# FTS5 인덱스에 related_queries 포함
def build_fts_text(node):
    parts = [node['content']]
    hints = json.loads(node.get('retrieval_hints') or '{}')
    if hints.get('related_queries'):
        parts.extend(hints['related_queries'])
    return ' '.join(parts)
```

---

## D-4: 분류기 수정 (V3-01, V3-03)

### classifier.py 프롬프트 수정

```python
# enrichment/classifier.py — classify_batch()
# 15개 타입으로 축소
VALID_TYPES = [
    # Tier 1 (핵심)
    "Decision", "Pattern", "Principle", "Failure",
    "Insight", "Goal", "Experiment",
    # Tier 2 (맥락)
    "Project", "Tool", "Framework", "Narrative", "Identity",
    # Tier 3 (전환)
    "Signal", "Observation", "Question",
]

# 분류 프롬프트에 deprecated 매핑 힌트 추가
CLASSIFICATION_HINT = """
이전에 사용된 타입과 매핑:
- Workflow, Skill, Agent → Tool (도구/절차)
- SystemVersion → Project
- Breakthrough → Insight
- Conversation → Observation
- Tension → Question
- AntiPattern → Failure
- Philosophy, Value, Belief, Axiom → Principle
- Preference → Identity

"일회성 구현 태스크"는 archived 표시할 것 (type은 가장 가까운 것으로).
"""
```

### Workflow LLM 배치 재분류 (V3-03)

```python
# scripts/migrate_workflow.py (신규)
def reclassify_workflows(conn, model="gpt-5-mini"):
    """Workflow 532개를 LLM으로 개별 재분류."""
    workflows = conn.execute("""
        SELECT id, content, tags FROM nodes
        WHERE type='Workflow' AND status='active'
    """).fetchall()

    prompt_template = """이 노드의 content를 읽고 가장 적절한 타입을 선택하라.

Content: {content}
Tags: {tags}

선택지:
- Pattern: 반복 사용되는 절차/패턴
- Framework: 설계 구조, 아키텍처
- Tool: 도구, 스크립트, 템플릿
- Goal: 구현 계획, 로드맵
- Experiment: 실험 계획
- ARCHIVED: 일회성 구현 태스크 (이미 실행 완료, 검색 가치 없음)

JSON으로 응답: {{"type": "...", "reason": "한줄 이유"}}"""

    for node_id, content, tags in workflows:
        result = llm_call(prompt_template.format(
            content=content[:500], tags=tags
        ), model=model)

        if result['type'] == 'ARCHIVED':
            conn.execute("UPDATE nodes SET status='archived' WHERE id=?", (node_id,))
        else:
            conn.execute("UPDATE nodes SET type=? WHERE id=?", (result['type'], node_id))

    conn.commit()
```

---

## D-5: co-retrieval (V3-07~09)

### co-retrieval 계산 스크립트

```python
# scripts/enrich/co_retrieval.py (신규)
def calculate_co_retrieval(conn, min_co_count=5, hub_percentile=95):
    """recall_log에서 co-occurrence 계산 → edges에 반영."""

    # 1. 허브 노드 식별
    hub_ids = set()
    degrees = conn.execute("""
        SELECT node_id, COUNT(*) as deg FROM (
            SELECT source_id as node_id FROM edges WHERE status='active'
            UNION ALL
            SELECT target_id as node_id FROM edges WHERE status='active'
        ) GROUP BY node_id ORDER BY deg DESC
    """).fetchall()
    if degrees:
        threshold_idx = int(len(degrees) * (1 - hub_percentile / 100))
        hub_threshold = degrees[threshold_idx][1] if threshold_idx < len(degrees) else 999
        hub_ids = {d[0] for d in degrees if d[1] >= hub_threshold}

    # 2. co-occurrence 계산
    pairs = conn.execute("""
        WITH sessions AS (
            SELECT query, timestamp, GROUP_CONCAT(node_id) as nids
            FROM recall_log GROUP BY query, timestamp HAVING COUNT(*) >= 2
        )
        SELECT a.value as a_id, b.value as b_id, COUNT(*) as co_count
        FROM sessions s,
             json_each('[' || s.nids || ']') a,
             json_each('[' || s.nids || ']') b
        WHERE CAST(a.value AS INT) < CAST(b.value AS INT)
        GROUP BY a_id, b_id
        HAVING co_count >= ?
    """, (min_co_count,)).fetchall()

    # 3. 허브-허브 제외 + edge 반영
    updated = 0
    for a_id, b_id, co_count in pairs:
        a, b = int(a_id), int(b_id)
        if a in hub_ids and b in hub_ids:
            continue

        boost = min(0.1 * (co_count - min_co_count + 1), 0.5)

        # 기존 edge 있으면 update, 없으면 insert
        existing = conn.execute(
            "SELECT id FROM edges WHERE source_id=? AND target_id=?", (a, b)
        ).fetchone()

        if existing:
            conn.execute("""
                UPDATE edges SET co_retrieval_count=?, co_retrieval_boost=?
                WHERE id=?
            """, (co_count, boost, existing[0]))
        else:
            conn.execute("""
                INSERT INTO edges (source_id, target_id, relation, strength,
                    co_retrieval_count, co_retrieval_boost, status, created_at)
                VALUES (?, ?, 'co_retrieved', ?, ?, ?, 'active', datetime('now'))
            """, (a, b, boost, co_count, boost))
        updated += 1

    conn.commit()
    return updated
```

### hybrid_search() 수정 (V3-09)

```python
# storage/hybrid.py — UCB traverse 부분
# 기존 score 계산 후 co-retrieval boost 추가

# config.py에 추가
CO_RETRIEVAL_ENABLED = True

# hybrid.py에서:
if CO_RETRIEVAL_ENABLED:
    co_boost = edge.get('co_retrieval_boost', 0.0)
    if co_boost > 0:
        score += co_boost  # 0.1 ~ 0.5
```

---

## D-6: dispatch (V3-14~16)

### orch-state 에이전트 수정

파일: orchestration 에이전트 설정 (STATE.md에서 위치 확인 필요)

프롬프트 교체: R2-04의 "수정 프롬프트" 그대로 적용.

### session-start.sh 수정 (V3-16)

```bash
# ~/.claude/hooks/session-start.sh에 추가
ORCH="/c/dev/01_projects/01_orchestration"

# impl-index 탐색 (오늘 → 어제 → 최근 3일)
TODAY=$(date +%Y-%m-%d)
INDEX=$(find "$ORCH/02_implementation/$TODAY" -name "0-impl-index*.md" 2>/dev/null | head -1)
if [ -z "$INDEX" ]; then
    YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d 2>/dev/null)
    INDEX=$(find "$ORCH/02_implementation/$YESTERDAY" -name "0-impl-index*.md" 2>/dev/null | head -1)
fi
if [ -z "$INDEX" ]; then
    INDEX=$(find "$ORCH/02_implementation/" -name "0-impl-index*.md" -newer "$ORCH/02_implementation/" -mtime -3 2>/dev/null | sort -r | head -1)
fi

if [ -n "$INDEX" ]; then
    echo "📋 이전 작업 인덱스: $(basename $(dirname $INDEX))/$(basename $INDEX)"
    echo "   /dispatch로 이어서 진행 가능"
fi
```

---

## D-7: 테스트 계획

### 기존 테스트 호환 (163개)

```bash
# 매 Step 후 실행
PYTHONIOENCODING=utf-8 python -m pytest tests/ -q
# 기대: 163 passed, 0 failed
```

### 신규 테스트

| # | 테스트 | 파일 | 검증 |
|---|--------|------|------|
| T1 | retrieval_hints 저장/로드 | tests/test_remember.py | remember(hints={...}) → 노드에 JSON 저장 |
| T2 | deprecated 타입 자동 교정 | tests/test_classifier.py | remember(type="Skill") → "Tool"로 저장 |
| T3 | co-retrieval 계산 | tests/test_co_retrieval.py | recall_log mock → pairs 계산 → edge 반영 |
| T4 | co-retrieval boost in search | tests/test_hybrid.py | boost 있는 edge → score 상승 |
| T5 | Workflow 재분류 정확도 | tests/test_migrate_workflow.py | 30개 샘플 → Phase 0-2 결과와 일치율 ≥80% |
| T6 | NDCG 비교 | tests/test_ndcg.py | 마이그레이션 전후 NDCG 비교 |
| T7 | 롤백 | tests/test_migrate_v3.py | migrate → rollback → 원복 확인 |

### NDCG 측정 기준

```
Phase 6 측정 스크립트:
  1. goldset 75개 → recall() 기반 NDCG@5 (verify.py 아님)
  2. 목표: 0.9
  3. 미달 시: 개별 요소 A/B
     - retrieval_hints ON/OFF
     - co-retrieval ON/OFF
     - 타입 축소 전/후
```

---

## 구현 순서 (최종)

```
Step 1 (P1, 병렬):
  ├─ migrate_v3.py: 스키마 + 단순 매핑 528개 (V3-04/05/10)
  ├─ session-start.sh: impl-index 알림 (V3-16)
  └─ tests: T1, T2, T7
  → pytest 163 pass 확인

Step 2 (P2, 순차):
  type_defs deprecated 설정 (V3-01/02)
  → classifier.py 15개 타입 프롬프트 (V3-01)
  → migrate_workflow.py: Workflow 532개 LLM 배치 (V3-03)
  → hints_generator.py: retrieval_hints 배치 ~2,520개 (V3-06)
  → tests: T5, T6
  → pytest 163+ pass 확인

Step 3 (P3, Step 2 이후):
  co_retrieval.py: 계산 + edge 반영 (V3-07/08/09)
  → hybrid.py: co-retrieval boost 적용 (V3-09)
  → orch-state 프롬프트 v2 (V3-14/15)
  → tests: T3, T4
  → NDCG 재측정

Step 4 (P4, 점진):
  L3 자율성 규칙 코드화 (V3-11/12/13)
  → NDCG 0.9 최종 검증 (V3-17)
```
