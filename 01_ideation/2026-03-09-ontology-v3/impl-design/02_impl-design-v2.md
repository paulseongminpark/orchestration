# Ontology v3 — Impl Design v2

> v1: 00_impl-design.md
> 리뷰: 01_impl-review-results.md (Codex Critical 3, High 4, Medium 4 + Gemini 4)
> **이 문서가 최종 구현 스펙. v1은 참고용.**

---

## 변경 요약 (v1 → v2)

| # | 출처 | 문제 | v2 반영 |
|---|------|------|---------|
| C1 | Codex | sync_schema()가 deprecated 리셋 | D-1: sync_schema() 정책 변경 |
| C2 | Codex | 마이그레이션이 layer/tier/Chroma 미갱신 | D-1: 마이그레이션에 layer+tier+Chroma 포함 |
| C3 | Codex | 51개 타입 중 20개 매핑 누락 | D-1: 전타입 매핑표 추가 |
| H1 | Codex | type_filter deprecated canonicalization 없음 | D-2: recall/hybrid_search에 자동 변환 추가 |
| H2 | Codex | recall_log 세션 식별 불안정 | D-1: recall_log.recall_id 컬럼 추가 |
| H3 | Codex | co-retrieval edge 방향/중복 + build_graph boost 미전달 | D-5: 복합 index + uniqueness + boost 전달 |
| H4 | Codex | retrieval_hints가 insert_node/FTS/E7에 미연결 | D-3: 전체 plumbing 추가 |
| M1 | Codex | retrieval_hints JSON edge case | D-2: schema validation + fallback |
| M2 | Codex | co-retrieval이 correction 후 결과 학습 | D-5: surfaced result만 학습 |
| M3 | Codex | recall_log/edges 인덱스 + 트랜잭션 경계 | D-1: 인덱스 추가 + explicit transaction |
| M4 | Codex | classifier.py import 깨짐 | Step 0: 선행 복구 |
| G1 | Gemini | Vector 재임베딩 누락 | D-3: Step 2.5 re-embed 단계 |
| G2 | Gemini | 테스트 기대값 수정 필요 | D-7: Test Adaptation 단계 |
| G3 | Gemini | 마이그레이션 전 DB 백업 | D-1: 자동 백업 |
| G4 | Gemini | 동시성 문제 | D-1: 마이그레이션 중 read-only 모드 |

---

## 코드베이스 맵 (v2 — 수정 파일 추가)

| 파일 | 역할 | 수정 |
|------|------|------|
| `storage/sqlite_store.py:33` | DB init | **수정** — 컬럼 추가, sync_schema() 정책, 인덱스 |
| `tools/remember.py:240` | remember() | **수정** — retrieval_hints 파라미터 + validation |
| `tools/recall.py:11` | recall() | **수정** — recall_id 생성 + type_filter canonicalization |
| `storage/hybrid.py:448` | hybrid_search() | **수정** — co-retrieval boost + type canonicalization |
| `storage/hybrid.py:531-595` | composite scoring | **수정** — co-retrieval weight |
| `enrichment/classifier.py:54` | 타입 분류기 | **수정** — import 복구 + 15개 타입 |
| `scripts/daily_enrich.py` | enrichment | **수정** — E-NEW, co-retrieval |
| `server.py:41-133` | MCP 서버 | **수정** — retrieval_hints 스키마 |
| `config.py` | 설정 | **수정** — CO_RETRIEVAL_WEIGHT 등 |
| `storage/graph_store.py` | build_graph() | **수정** — co_retrieval_boost attr 전달 |
| `scripts/migrate_v3.py` | 마이그레이션 (신규) | layer/tier/Chroma/백업/read-only |
| `scripts/enrich/hints_generator.py` | hints 생성 (신규) | — |
| `scripts/enrich/co_retrieval.py` | co-retrieval 계산 (신규) | — |
| `scripts/migrate_workflow.py` | Workflow 재분류 (신규) | — |

---

## D-1: DB 스키마 변경 (v2)

### 마이그레이션 SQL

```sql
-- V3-05: nodes.retrieval_hints
ALTER TABLE nodes ADD COLUMN retrieval_hints TEXT DEFAULT NULL;

-- V3-10: edges co-retrieval
ALTER TABLE edges ADD COLUMN co_retrieval_count INTEGER DEFAULT 0;
ALTER TABLE edges ADD COLUMN co_retrieval_boost REAL DEFAULT 0.0;

-- H2: recall_log.recall_id
ALTER TABLE recall_log ADD COLUMN recall_id TEXT DEFAULT NULL;

-- M3: 인덱스 추가
CREATE INDEX IF NOT EXISTS idx_recall_log_recall_id ON recall_log(recall_id);
CREATE INDEX IF NOT EXISTS idx_recall_log_query_ts ON recall_log(query, timestamp);
CREATE INDEX IF NOT EXISTS idx_edges_source_target ON edges(source_id, target_id);

-- H3: edges uniqueness (source_id, target_id, relation)
CREATE UNIQUE INDEX IF NOT EXISTS uq_edges_pair_rel
    ON edges(source_id, target_id, relation) WHERE status='active';
```

### sync_schema() 정책 변경 (C1 해결)

```python
# storage/sqlite_store.py — sync_schema() 수정
def sync_schema(conn, schema_config):
    """schema.yaml의 타입을 type_defs에 동기화.
    v2: deprecated 타입은 건드리지 않음."""
    existing = {row['name']: row for row in
        conn.execute("SELECT name, status FROM type_defs").fetchall()}

    for type_def in schema_config['types']:
        name = type_def['name']
        if name in existing:
            # ★ C1 수정: deprecated면 skip — active로 되돌리지 않음
            if existing[name]['status'] == 'deprecated':
                continue
            # active면 설명 등 업데이트만
            conn.execute("""
                UPDATE type_defs SET description=?, tier=?
                WHERE name=? AND status='active'
            """, (type_def.get('description', ''), type_def.get('tier', 1), name))
        else:
            # 새 타입 추가
            conn.execute("""
                INSERT INTO type_defs (name, description, tier, status, version)
                VALUES (?, ?, ?, 'active', 1)
            """, (name, type_def.get('description', ''), type_def.get('tier', 1)))

    conn.commit()
```

### 마이그레이션 스크립트 (v2 — C2, C3, G3, G4 반영)

```python
# scripts/migrate_v3.py
import shutil, json, uuid
from datetime import datetime

def migrate(conn, chroma_collection=None, dry_run=False):
    """v3 마이그레이션 — type + layer + tier + Chroma 한 세트."""

    # ── G3: DB 백업 ──
    db_path = conn.execute("PRAGMA database_list").fetchone()[2]
    backup_path = f"{db_path}.v2_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(db_path, backup_path)
    print(f"백업: {backup_path}")

    # ── G4: 마이그레이션 중 쓰기 차단 플래그 ──
    conn.execute("CREATE TABLE IF NOT EXISTS _migration_lock (locked INTEGER)")
    conn.execute("INSERT INTO _migration_lock VALUES (1)")
    conn.commit()

    try:
        _do_migrate(conn, chroma_collection, dry_run)
    finally:
        # 잠금 해제
        conn.execute("DELETE FROM _migration_lock")
        conn.execute("DROP TABLE IF EXISTS _migration_lock")
        conn.commit()

# ── 전타입 매핑표 (C3 해결 — 51개 전부) ──
# keep: 유지, merge: 1:1 매핑, archive: 일괄 archived, edge: edge 전환, llm: LLM 재분류
TYPE_MAP = {
    # === Tier 1 유지 (7) ===
    "Decision":   {"action": "keep", "tier": 1, "layer": "core"},
    "Pattern":    {"action": "keep", "tier": 1, "layer": "core"},
    "Principle":  {"action": "keep", "tier": 1, "layer": "core"},
    "Failure":    {"action": "keep", "tier": 1, "layer": "core"},
    "Insight":    {"action": "keep", "tier": 1, "layer": "core"},
    "Goal":       {"action": "keep", "tier": 1, "layer": "core"},
    "Experiment": {"action": "keep", "tier": 1, "layer": "core"},

    # === Tier 2 유지 (5) ===
    "Project":    {"action": "keep", "tier": 2, "layer": "context"},
    "Tool":       {"action": "keep", "tier": 2, "layer": "context"},
    "Framework":  {"action": "keep", "tier": 2, "layer": "context"},
    "Narrative":  {"action": "keep", "tier": 2, "layer": "context"},
    "Identity":   {"action": "keep", "tier": 2, "layer": "context"},

    # === Tier 3 유지 (3) ===
    "Signal":      {"action": "keep", "tier": 3, "layer": "transient"},
    "Observation": {"action": "keep", "tier": 3, "layer": "transient"},
    "Question":    {"action": "keep", "tier": 3, "layer": "transient"},

    # === 단순 merge (12) — Step 1 ===
    "Skill":          {"action": "merge", "target": "Tool",      "tier": 2, "layer": "context"},
    "Agent":          {"action": "merge", "target": "Tool",      "tier": 2, "layer": "context"},
    "SystemVersion":  {"action": "merge", "target": "Project",   "tier": 2, "layer": "context"},
    "Breakthrough":   {"action": "merge", "target": "Insight",   "tier": 1, "layer": "core"},
    "Conversation":   {"action": "merge", "target": "Observation","tier": 3, "layer": "transient"},
    "Tension":        {"action": "merge", "target": "Question",  "tier": 3, "layer": "transient"},
    "AntiPattern":    {"action": "merge", "target": "Failure",   "tier": 1, "layer": "core"},
    "Preference":     {"action": "merge", "target": "Identity",  "tier": 2, "layer": "context"},
    "Philosophy":     {"action": "merge", "target": "Principle", "tier": 1, "layer": "core"},
    "Value":          {"action": "merge", "target": "Principle", "tier": 1, "layer": "core"},
    "Belief":         {"action": "merge", "target": "Principle", "tier": 1, "layer": "core"},
    "Axiom":          {"action": "merge", "target": "Principle", "tier": 1, "layer": "core"},

    # === edge 전환 (2) — Step 1 ===
    "Evolution":  {"action": "edge", "target": "Pattern",  "edge_type": "evolved_from",
                   "tier": 1, "layer": "core"},
    "Connection": {"action": "edge", "target": "Insight",  "edge_type": "connects",
                   "tier": 1, "layer": "core"},

    # === LLM 재분류 (1 대분류) — Step 2 ===
    "Workflow":  {"action": "llm", "candidates": ["Pattern", "Framework", "Tool",
                  "Goal", "Experiment", "ARCHIVED"]},

    # === C3 누락 20개: 개별 경로 확정 ===
    "Aporia":       {"action": "merge", "target": "Question",   "tier": 3, "layer": "transient",
                     "reason": "해결 불가능한 난제 = 열린 질문"},
    "Assumption":   {"action": "merge", "target": "Principle",  "tier": 1, "layer": "core",
                     "reason": "전제/가정 = 원칙의 변형"},
    "Boundary":     {"action": "merge", "target": "Decision",   "tier": 1, "layer": "core",
                     "reason": "경계 설정 = 결정"},
    "Commitment":   {"action": "merge", "target": "Goal",       "tier": 1, "layer": "core",
                     "reason": "약속/헌신 = 목표의 변형"},
    "Concept":      {"action": "merge", "target": "Insight",    "tier": 1, "layer": "core",
                     "reason": "개념 정리 = 인사이트"},
    "Constraint":   {"action": "merge", "target": "Decision",   "tier": 1, "layer": "core",
                     "reason": "제약 조건 = 결정의 일부"},
    "Context":      {"action": "merge", "target": "Observation","tier": 3, "layer": "transient",
                     "reason": "맥락 기록 = 관찰"},
    "Correction":   {"action": "merge", "target": "Failure",    "tier": 1, "layer": "core",
                     "reason": "수정 = 실패 후 조치"},
    "Evidence":     {"action": "merge", "target": "Observation","tier": 3, "layer": "transient",
                     "reason": "증거/데이터 = 관찰"},
    "Heuristic":    {"action": "merge", "target": "Pattern",    "tier": 1, "layer": "core",
                     "reason": "경험 법칙 = 패턴"},
    "Lens":         {"action": "merge", "target": "Framework",  "tier": 2, "layer": "context",
                     "reason": "관점/렌즈 = 프레임워크"},
    "Mental Model": {"action": "merge", "target": "Framework",  "tier": 2, "layer": "context",
                     "reason": "멘탈 모델 = 프레임워크"},
    "Metaphor":     {"action": "merge", "target": "Narrative",  "tier": 2, "layer": "context",
                     "reason": "비유 = 내러티브"},
    "Paradox":      {"action": "merge", "target": "Question",   "tier": 3, "layer": "transient",
                     "reason": "역설 = 열린 질문"},
    "Plan":         {"action": "merge", "target": "Goal",       "tier": 1, "layer": "core",
                     "reason": "계획 = 목표"},
    "Ritual":       {"action": "merge", "target": "Pattern",    "tier": 1, "layer": "core",
                     "reason": "의식/루틴 = 반복 패턴"},
    "Trade-off":    {"action": "merge", "target": "Decision",   "tier": 1, "layer": "core",
                     "reason": "트레이드오프 = 결정"},
    "Trigger":      {"action": "merge", "target": "Signal",     "tier": 3, "layer": "transient",
                     "reason": "트리거 = 시그널"},
    "Vision":       {"action": "merge", "target": "Goal",       "tier": 1, "layer": "core",
                     "reason": "비전 = 장기 목표"},
    "Wonder":       {"action": "merge", "target": "Question",   "tier": 3, "layer": "transient",
                     "reason": "궁금증 = 질문"},

    # === 안전망: Unclassified ===
    "Unclassified": {"action": "keep", "tier": 3, "layer": "transient"},
}

# tier → layer 매핑
TIER_LAYER = {1: "core", 2: "context", 3: "transient"}

def _do_migrate(conn, chroma_collection, dry_run):
    """실제 마이그레이션 로직."""

    # ── Step 0: 컬럼 추가 ──
    cols = {c[1] for c in conn.execute("PRAGMA table_info(nodes)").fetchall()}
    if "retrieval_hints" not in cols:
        conn.execute("ALTER TABLE nodes ADD COLUMN retrieval_hints TEXT DEFAULT NULL")

    cols_e = {c[1] for c in conn.execute("PRAGMA table_info(edges)").fetchall()}
    if "co_retrieval_count" not in cols_e:
        conn.execute("ALTER TABLE edges ADD COLUMN co_retrieval_count INTEGER DEFAULT 0")
        conn.execute("ALTER TABLE edges ADD COLUMN co_retrieval_boost REAL DEFAULT 0.0")

    cols_r = {c[1] for c in conn.execute("PRAGMA table_info(recall_log)").fetchall()}
    if "recall_id" not in cols_r:
        conn.execute("ALTER TABLE recall_log ADD COLUMN recall_id TEXT DEFAULT NULL")

    # 인덱스
    conn.execute("CREATE INDEX IF NOT EXISTS idx_recall_log_recall_id ON recall_log(recall_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_recall_log_query_ts ON recall_log(query, timestamp)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_edges_source_target ON edges(source_id, target_id)")

    # ── Step 1: type_defs deprecated + 노드 매핑 ──
    stats = {"merge": 0, "edge": 0, "layer_tier": 0, "chroma": 0}

    for old_type, spec in TYPE_MAP.items():
        action = spec["action"]

        if action == "keep":
            # layer/tier 정규화
            tier = spec.get("tier")
            layer = spec.get("layer")
            if tier and layer:
                cnt = conn.execute("""
                    UPDATE nodes SET layer=?, tier=?
                    WHERE type=? AND status='active' AND (layer!=? OR tier!=?)
                """, (layer, tier, old_type, layer, tier)).rowcount
                stats["layer_tier"] += cnt
            continue

        if action in ("merge", "edge"):
            target = spec["target"]
            tier = spec.get("tier", 1)
            layer = spec.get("layer", TIER_LAYER.get(tier, "core"))

            # type_defs deprecated
            reason = spec.get("reason", f"v3 타입 축소: {old_type} → {target}")
            conn.execute("""
                UPDATE type_defs SET
                    status='deprecated', deprecated_reason=?,
                    replaced_by=?, deprecated_at=datetime('now'), version=version+1
                WHERE name=? AND status='active'
            """, (reason, target, old_type))

            # ★ C2 수정: type + layer + tier 동시 갱신
            count = conn.execute("""
                UPDATE nodes SET type=?, layer=?, tier=?
                WHERE type=? AND status='active'
            """, (target, layer, tier, old_type)).rowcount
            stats["merge"] += count

            if action == "edge":
                # edge 전환: 원본 content 기반 edge 생성
                edge_type = spec.get("edge_type", "related")
                # Edge 전환 로직은 content 분석 필요 — Step 1에서 type만 변경,
                # edge 생성은 별도 스크립트에서 처리
                stats["edge"] += count

            # ★ C2 수정: Chroma metadata 갱신
            if chroma_collection and not dry_run:
                node_ids = [r[0] for r in conn.execute(
                    "SELECT id FROM nodes WHERE type=? AND status='active'",
                    (target,)
                ).fetchall()]
                for nid in node_ids:
                    try:
                        chroma_collection.update(
                            ids=[str(nid)],
                            metadatas=[{"type": target, "layer": layer, "tier": tier}]
                        )
                        stats["chroma"] += 1
                    except Exception as e:
                        print(f"  Chroma update failed for {nid}: {e}")

        # llm은 Step 2에서 별도 처리
        if action == "llm":
            continue

    conn.commit()
    print(f"Step 1 완료: merge={stats['merge']}, edge={stats['edge']}, "
          f"layer_tier={stats['layer_tier']}, chroma={stats['chroma']}")

    return stats
```

---

## D-2: API 변경 (v2)

### remember() — retrieval_hints + validation (M1 해결)

```python
# tools/remember.py
import json

def _validate_hints(hints):
    """M1: retrieval_hints JSON validation + fallback."""
    if hints is None:
        return None
    if isinstance(hints, str):
        try:
            hints = json.loads(hints)
        except (json.JSONDecodeError, TypeError):
            return None
    if not isinstance(hints, dict):
        return None

    # 필드 타입 검증
    validated = {}
    if isinstance(hints.get("when_needed"), str):
        validated["when_needed"] = hints["when_needed"][:500]  # 길이 제한
    if isinstance(hints.get("related_queries"), list):
        validated["related_queries"] = [
            str(q)[:200] for q in hints["related_queries"][:10]
        ]
    if isinstance(hints.get("context_keys"), list):
        validated["context_keys"] = [
            str(k)[:100] for k in hints["context_keys"][:10]
        ]
    return validated if validated else None

def remember(content, type="", tags="", project="", metadata=None,
             confidence=1.0, source="claude", retrieval_hints=None):
    # ... 기존 로직 ...
    hints_json = None
    validated = _validate_hints(retrieval_hints)
    if validated:
        hints_json = json.dumps(validated, ensure_ascii=False)
    # INSERT에 retrieval_hints=hints_json 추가
```

### H1: recall() type_filter canonicalization

```python
# tools/recall.py 또는 storage/hybrid.py

def canonicalize_type_filter(type_filter, conn):
    """H1: deprecated 타입 → replaced_by 자동 변환."""
    if not type_filter:
        return type_filter

    # 캐싱 (서버 수명 동안 유효)
    if not hasattr(canonicalize_type_filter, '_cache'):
        rows = conn.execute("""
            SELECT name, replaced_by FROM type_defs
            WHERE status='deprecated' AND replaced_by IS NOT NULL
        """).fetchall()
        canonicalize_type_filter._cache = {r[0]: r[1] for r in rows}

    cache = canonicalize_type_filter._cache

    if isinstance(type_filter, str):
        return cache.get(type_filter, type_filter)
    if isinstance(type_filter, list):
        return list(set(cache.get(t, t) for t in type_filter))
    return type_filter

# recall()에서 호출:
# type_filter = canonicalize_type_filter(type_filter, conn)
```

### H2: recall_id 생성

```python
# tools/recall.py
import uuid

def recall(query, ...):
    recall_id = str(uuid.uuid4())[:8]  # 짧은 ID
    # ... 검색 수행 ...
    # recall_log 저장 시 recall_id 포함
    for rank, (node_id, score) in enumerate(results):
        conn.execute("""
            INSERT INTO recall_log (query, node_id, rank, score, mode, timestamp, recall_id)
            VALUES (?, ?, ?, ?, ?, datetime('now'), ?)
        """, (query, node_id, rank, score, mode, recall_id))
```

---

## D-3: enrichment 확장 (v2 — H4, G1 반영)

### H4: retrieval_hints 전체 plumbing

```
remember() → _validate_hints() → INSERT (hints_json)
                                     ↓
                              FTS5 rebuild (related_queries 포함)
                                     ↓
                              E7 prompt (when_needed + context_keys 포함)
                                     ↓
                              ChromaDB embedding_text (when_needed + related_queries)
```

### sqlite_store.py — insert_node() plumbing

```python
# storage/sqlite_store.py — insert_node() 수정
def insert_node(self, content, type, tags="", project="", metadata=None,
                confidence=1.0, source="claude", retrieval_hints=None):
    # ... 기존 INSERT 로직 ...
    # ★ H4: retrieval_hints를 INSERT에 포함
    hints_json = None
    if retrieval_hints:
        from tools.remember import _validate_hints
        validated = _validate_hints(retrieval_hints)
        if validated:
            hints_json = json.dumps(validated, ensure_ascii=False)

    cursor = conn.execute("""
        INSERT INTO nodes (content, type, tags, project, metadata,
            confidence, source, retrieval_hints, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'active', datetime('now'))
    """, (content, type, tags, project, json.dumps(metadata),
          confidence, source, hints_json))

    node_id = cursor.lastrowid

    # ★ H4: FTS 인덱스에 hints 반영
    fts_text = self._build_fts_text(content, retrieval_hints=validated)
    self._update_fts(node_id, fts_text)

    return node_id
```

### FTS5 rebuild에 hints 반영

```python
def _build_fts_text(self, content, retrieval_hints=None):
    """FTS5 인덱스용 텍스트. hints의 related_queries 포함."""
    parts = [content]
    if retrieval_hints:
        if retrieval_hints.get('related_queries'):
            parts.extend(retrieval_hints['related_queries'])
    return ' '.join(parts)
```

### E7 prompt에 hints 반영

```python
# enrichment 프롬프트 (E7)에 추가
def build_enrichment_prompt(node):
    prompt = f"""노드 enrichment...
내용: {node['content'][:500]}
타입: {node['type']}"""

    # ★ H4: hints 반영
    hints = json.loads(node.get('retrieval_hints') or '{}')
    if hints.get('when_needed'):
        prompt += f"\n인출 맥락: {hints['when_needed']}"
    if hints.get('context_keys'):
        prompt += f"\n맥락 키: {', '.join(hints['context_keys'])}"

    return prompt
```

### embedding_text에 hints 반영

```python
def build_embedding_text(node):
    parts = [node['content'], node.get('summary', '')]
    hints = json.loads(node.get('retrieval_hints') or '{}')
    if hints.get('when_needed'):
        parts.append(hints['when_needed'])
    if hints.get('related_queries'):
        parts.extend(hints['related_queries'])
    return '\n'.join(filter(None, parts))
```

### G1: Step 2.5 — ChromaDB re-embed

```python
# scripts/reembed_v3.py (신규)
def reembed_with_hints(conn, chroma_collection, embed_fn, batch_size=100):
    """retrieval_hints가 있는 노드의 embedding 재생성."""
    nodes = conn.execute("""
        SELECT id, content, summary, retrieval_hints FROM nodes
        WHERE status='active' AND retrieval_hints IS NOT NULL
    """).fetchall()

    for i in range(0, len(nodes), batch_size):
        batch = nodes[i:i+batch_size]
        ids = [str(n[0]) for n in batch]
        texts = [build_embedding_text({
            'content': n[1], 'summary': n[2], 'retrieval_hints': n[3]
        }) for n in batch]
        embeddings = embed_fn(texts)
        chroma_collection.update(ids=ids, embeddings=embeddings)
        print(f"  re-embed {i+len(batch)}/{len(nodes)}")

    return len(nodes)
```

### hints_generator.py (v1과 동일 — 변경 없음)

v1의 D-3 hints_generator.py 그대로 사용.

---

## D-4: 분류기 수정 (v2 — M4 선행)

### M4: classifier.py import 복구 (Step 0 — 최우선)

```python
# enrichment/classifier.py 상단
# 기존 (깨짐):
#   from storage.sqlite_store import get_valid_node_types
# 수정:
from config import VALID_TYPES  # v3에서 config.py로 이동

# 또는 type_defs에서 동적 로드:
def get_valid_node_types(conn):
    """type_defs에서 active 타입 목록 동적 조회."""
    rows = conn.execute(
        "SELECT name FROM type_defs WHERE status='active'"
    ).fetchall()
    return [r[0] for r in rows]
```

### 15개 타입 프롬프트 (v1과 동일)

v1의 D-4 VALID_TYPES + CLASSIFICATION_HINT 그대로.

---

## D-5: co-retrieval (v2 — H2, H3, M2 반영)

### H2: recall_id 기반 세션화

```python
# scripts/enrich/co_retrieval.py (v2)
def calculate_co_retrieval(conn, min_co_count=5, hub_percentile=95):
    """recall_log에서 co-occurrence 계산 → edges에 반영.
    v2: recall_id 기반 세션화 (H2)."""

    # 1. 허브 노드 식별 (v1과 동일)
    hub_ids = _get_hub_ids(conn, hub_percentile)

    # 2. co-occurrence 계산 — recall_id 기반 (H2)
    pairs = conn.execute("""
        WITH sessions AS (
            SELECT recall_id, GROUP_CONCAT(node_id) as nids
            FROM recall_log
            WHERE recall_id IS NOT NULL
            GROUP BY recall_id
            HAVING COUNT(*) >= 2
        )
        SELECT a.value as a_id, b.value as b_id, COUNT(*) as co_count
        FROM sessions s,
             json_each('[' || s.nids || ']') a,
             json_each('[' || s.nids || ']') b
        WHERE CAST(a.value AS INT) < CAST(b.value AS INT)
        GROUP BY a_id, b_id
        HAVING co_count >= ?
    """, (min_co_count,)).fetchall()

    # 2-fallback: recall_id 없는 레거시 데이터 — query+timestamp 기반
    legacy_pairs = conn.execute("""
        WITH sessions AS (
            SELECT query, timestamp, GROUP_CONCAT(node_id) as nids
            FROM recall_log
            WHERE recall_id IS NULL
            GROUP BY query, timestamp
            HAVING COUNT(*) >= 2
        )
        SELECT a.value as a_id, b.value as b_id, COUNT(*) as co_count
        FROM sessions s,
             json_each('[' || s.nids || ']') a,
             json_each('[' || s.nids || ']') b
        WHERE CAST(a.value AS INT) < CAST(b.value AS INT)
        GROUP BY a_id, b_id
        HAVING co_count >= ?
    """, (min_co_count,)).fetchall()

    # 병합 (같은 pair면 co_count 합산)
    pair_map = {}
    for a_id, b_id, co_count in list(pairs) + list(legacy_pairs):
        key = (int(a_id), int(b_id))
        pair_map[key] = pair_map.get(key, 0) + co_count

    # 3. 허브-허브 제외 + edge 반영
    updated = 0
    with conn:  # M3: explicit transaction
        for (a, b), co_count in pair_map.items():
            if co_count < min_co_count:
                continue
            if a in hub_ids and b in hub_ids:
                continue

            boost = min(0.1 * (co_count - min_co_count + 1), 0.5)

            # H3: UPSERT with unique constraint
            conn.execute("""
                INSERT INTO edges (source_id, target_id, relation, strength,
                    co_retrieval_count, co_retrieval_boost, status, created_at)
                VALUES (?, ?, 'co_retrieved', ?, ?, ?, 'active', datetime('now'))
                ON CONFLICT(source_id, target_id, relation)
                    WHERE status='active'
                DO UPDATE SET
                    co_retrieval_count=excluded.co_retrieval_count,
                    co_retrieval_boost=excluded.co_retrieval_boost
            """, (a, b, boost, co_count, boost))
            updated += 1

    return updated

def _get_hub_ids(conn, hub_percentile=95):
    """상위 N% degree 노드 식별."""
    degrees = conn.execute("""
        SELECT node_id, COUNT(*) as deg FROM (
            SELECT source_id as node_id FROM edges WHERE status='active'
            UNION ALL
            SELECT target_id as node_id FROM edges WHERE status='active'
        ) GROUP BY node_id ORDER BY deg DESC
    """).fetchall()
    if not degrees:
        return set()
    threshold_idx = int(len(degrees) * (1 - hub_percentile / 100))
    hub_threshold = degrees[threshold_idx][1] if threshold_idx < len(degrees) else 999
    return {d[0] for d in degrees if d[1] >= hub_threshold}
```

### M2: surfaced result만 학습

```python
# co-retrieval 학습 대상 결정:
# recall_log에 저장되는 건 surfaced results (사용자에게 보여진 결과)만.
# correction/patch 후 결과는 별도 correction_log에 기록하되,
# co-retrieval 학습에는 포함하지 않음.
# → 현재 recall_log 구조가 이미 surfaced only이므로 추가 변경 불필요.
# 단, 향후 correction 기능 추가 시 recall_log와 분리 필수.
```

### H3: build_graph()에 co_retrieval_boost 전달

```python
# storage/graph_store.py — build_graph() 수정
def build_graph(conn, node_ids=None):
    """그래프 구성 — co_retrieval_boost 포함."""
    edges = conn.execute("""
        SELECT source_id, target_id, relation, strength,
               co_retrieval_count, co_retrieval_boost
        FROM edges WHERE status='active'
    """).fetchall()

    for edge in edges:
        # ★ H3: co_retrieval_boost를 edge attribute로 포함
        graph.add_edge(
            edge['source_id'], edge['target_id'],
            relation=edge['relation'],
            weight=edge['strength'],
            co_retrieval_boost=edge.get('co_retrieval_boost', 0.0),
            co_retrieval_count=edge.get('co_retrieval_count', 0)
        )
```

### hybrid.py — co-retrieval boost (v1과 유사 + H3)

```python
# storage/hybrid.py — UCB traverse
if CO_RETRIEVAL_ENABLED:
    # ★ H3: build_graph()에서 전달된 boost 사용
    co_boost = graph.edges[source, target].get('co_retrieval_boost', 0.0)
    if co_boost > 0:
        score += co_boost  # 0.1 ~ 0.5
```

---

## D-6: dispatch (v1과 동일 — 변경 없음)

v1의 D-6 그대로 사용. 리뷰에서 추가 이슈 없음.

---

## D-7: 테스트 계획 (v2 — G2 반영)

### G2: Test Adaptation

```python
# scripts/adapt_tests_v3.py (신규)
"""v3 마이그레이션 후 테스트 기대값 업데이트.
163개 기존 테스트에서 type 관련 assertion 수정."""

TYPE_MAP = {  # D-1 TYPE_MAP의 merge만 추출
    "Skill": "Tool", "Agent": "Tool",
    "SystemVersion": "Project", "Breakthrough": "Insight",
    "Conversation": "Observation", "Tension": "Question",
    "AntiPattern": "Failure", "Preference": "Identity",
    "Philosophy": "Principle", "Value": "Principle",
    "Belief": "Principle", "Axiom": "Principle",
    # + C3 누락 20개 (merge만)
    "Aporia": "Question", "Assumption": "Principle",
    "Boundary": "Decision", "Commitment": "Goal",
    "Concept": "Insight", "Constraint": "Decision",
    "Context": "Observation", "Correction": "Failure",
    "Evidence": "Observation", "Heuristic": "Pattern",
    "Lens": "Framework", "Mental Model": "Framework",
    "Metaphor": "Narrative", "Paradox": "Question",
    "Plan": "Goal", "Ritual": "Pattern",
    "Trade-off": "Decision", "Trigger": "Signal",
    "Vision": "Goal", "Wonder": "Question",
}

def adapt_test_file(path):
    """테스트 파일에서 deprecated 타입 assertion을 v3 타입으로 수정."""
    content = open(path).read()
    for old, new in TYPE_MAP.items():
        # assert ... type == "Skill" → "Tool"
        content = content.replace(f'type="{old}"', f'type="{new}"')
        content = content.replace(f"type='{old}'", f"type='{new}'")
        content = content.replace(f'== "{old}"', f'== "{new}"')
    open(path, 'w').write(content)
```

### 테스트 매트릭스 (v2)

| # | 테스트 | 파일 | 검증 |
|---|--------|------|------|
| T1 | retrieval_hints 저장/로드 + validation | tests/test_remember.py | remember(hints={...}) → JSON 저장 + 잘못된 형식 fallback |
| T2 | deprecated 타입 자동 교정 | tests/test_classifier.py | recall(type_filter="Skill") → "Tool"로 변환 |
| T3 | co-retrieval 계산 (recall_id 기반) | tests/test_co_retrieval.py | recall_log mock → recall_id로 세션화 → pairs |
| T4 | co-retrieval boost in search | tests/test_hybrid.py | boost edge → score 상승 |
| T5 | Workflow 재분류 정확도 | tests/test_migrate_workflow.py | 30개 샘플 ≥80% 일치 |
| T6 | NDCG 비교 | tests/test_ndcg.py | v2→v3 전후 비교 |
| T7 | 마이그레이션 + 롤백 | tests/test_migrate_v3.py | migrate → 백업 확인 → 원복 |
| T8 | **sync_schema() deprecated 보존** | tests/test_schema.py | sync 후 deprecated 타입 그대로 |
| T9 | **layer/tier 정규화** | tests/test_migrate_v3.py | 마이그레이션 후 모든 노드 layer/tier 일치 |
| T10 | **edge uniqueness** | tests/test_co_retrieval.py | 동일 pair 중복 insert → UPSERT |
| T11 | **DB 백업 생성** | tests/test_migrate_v3.py | migrate() 시작 시 .v2_final 파일 존재 |
| T12 | **insert_node hints plumbing** | tests/test_remember.py | insert_node(hints) → FTS 검색 가능 |

### NDCG 측정 기준 (v1과 동일)

```
Phase 6:
  1. goldset 75개 → recall() 기반 NDCG@5
  2. 목표: 0.9
  3. A/B: retrieval_hints ON/OFF, co-retrieval ON/OFF, 타입 축소 전/후
```

---

## 구현 순서 (v2 — 최종)

```
Step 0 (선행 — 즉시):
  ├─ M4: classifier.py import 복구
  ├─ H2: recall_log.recall_id 컬럼 추가
  ├─ H3: edges 복합 index + unique constraint
  ├─ M3: recall_log 인덱스 추가
  └─ 기존 163 테스트 PASS 확인

Step 1 (P1 — 스키마 + 단순 매핑):
  ├─ G3: DB 백업 (memory.db.v2_final)
  ├─ C1: sync_schema() deprecated 보존 정책
  ├─ C3: 전타입 매핑표 (51개) 기반 마이그레이션
  ├─ C2: type + layer + tier + Chroma metadata 동시 갱신
  ├─ G4: 마이그레이션 중 _migration_lock
  ├─ T8, T9, T11 테스트
  └─ 기존 163 테스트 PASS 확인

Step 1.5 (G2 — Test Adaptation):
  ├─ adapt_tests_v3.py: 기존 테스트 기대값 수정
  └─ 163+ 테스트 PASS 확인

Step 2 (P2 — enrichment):
  ├─ classifier.py 15개 타입 프롬프트
  ├─ migrate_workflow.py: Workflow LLM 배치 (~532개)
  ├─ hints_generator.py: retrieval_hints 배치 (~2,520개)
  ├─ H4: insert_node + FTS + E7 hints plumbing
  ├─ M1: hints validation
  ├─ T1, T2, T5, T12 테스트
  └─ 163+ 테스트 PASS 확인

Step 2.5 (G1 — re-embed):
  ├─ reembed_v3.py: ChromaDB 재임베딩 (hints 반영)
  └─ NDCG 중간 측정

Step 3 (P3 — co-retrieval):
  ├─ co_retrieval.py: recall_id 기반 계산 + 레거시 fallback
  ├─ H3: build_graph() co_retrieval_boost 전달
  ├─ hybrid.py: co-retrieval boost 적용
  ├─ H1: type_filter canonicalization
  ├─ M2: surfaced result만 학습 (현재 구조 유지)
  ├─ T3, T4, T10 테스트
  └─ NDCG 재측정

Step 4 (P4 — dispatch + L3):
  ├─ orch-state 프롬프트 v2
  ├─ session-start.sh impl-index 알림
  ├─ L3 자율성 규칙 코드화
  ├─ T6 NDCG 비교
  └─ NDCG 0.9 최종 검증
```

---

## 리스크 및 완화

| 리스크 | 확률 | 영향 | 완화 |
|--------|------|------|------|
| Workflow LLM 배치 비용 | 중 | 낮 | gpt-5-mini 무료 토큰 활용 |
| re-embed 시간 | 중 | 중 | batch_size=100, 병렬 불필요 (순차 OK) |
| NDCG 0.9 미달 | 중 | 중 | A/B로 병목 식별 → 개별 튜닝 |
| sync_schema 변경 부작용 | 낮 | 높 | T8 테스트 + 기존 163 전수 확인 |
| Chroma metadata 불일치 | 낮 | 높 | migrate_v3.py에서 한 세트 처리 |
| 레거시 recall_log (recall_id 없음) | 확정 | 중 | 2-fallback 쿼리로 양쪽 지원 |
