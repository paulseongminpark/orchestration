1. **Final score calculation and exact code path**

- Entry point: `def recall(query: str, type_filter: str = "", project: str = "", top_k: int = DEFAULT_TOP_K, mode: str = "auto") -> dict` at [tools/recall.py](C:\dev\01_projects\06_mcp-memory\tools\recall.py):11.
- `recall()` calls `hybrid_search(...)` at [tools/recall.py](C:\dev\01_projects\06_mcp-memory\tools\recall.py):26-32.
- Scoring happens in `def hybrid_search(...) -> list[dict]` at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):446-554:

  - RRF accumulation:
    - Vector channel: `scores[node_id] += 1.0 / (RRF_K + rank)` at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):516-517
    - FTS channel: same formula at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):518-519
    - Graph channel: additive constant `GRAPH_BONUS` at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):520-521
    - Typed vector channel: `TYPE_CHANNEL_WEIGHT / (RRF_K + rank)` at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):524-526
  - Final per-node score assignment:
    - `node["score"] = scores[node_id] + enrichment_bonus + tier_bonus` at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):541-548
  - Sorted by `node["score"]` at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):551.

- `recall()` may patch-switch and re-sort by the same `score` at [tools/recall.py](C:\dev\01_projects\06_mcp-memory\tools\recall.py):40-50, then rounds it for output at [tools/recall.py](C:\dev\01_projects\06_mcp-memory\tools\recall.py):75.

2. **Where to insert composite scoring (`similarity*0.5 + decay*0.3 + importance*0.2`)**

- Function: `hybrid_search(...)` in [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):446-554.
- Exact insertion/replacement zone: [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):541-548.
- Replace current final assignment at line 548 with composite calculation (using `scores[node_id]` as current similarity base), then set `node["score"]` there.

3. **`nodes` table columns (from `init_db`)**

From `def init_db() -> None` at [storage/sqlite_store.py](C:\dev\01_projects\06_mcp-memory\storage\sqlite_store.py):33, `CREATE TABLE nodes` at lines 36-69:

`id, type, content, metadata, project, tags, confidence, source, status, created_at, updated_at, layer, summary, key_concepts, facets, domains, secondary_types, quality_score, abstraction_level, temporal_relevance, actionability, enrichment_status, enriched_at, tier, maturity, observation_count, theta_m, activity_history, visit_count, score_history, promotion_candidate, content_hash`.

4. **`last_accessed_at` or similar column?**

- `nodes` table has **no** `last_accessed_at` and no `last_activated` column in `init_db` ([storage/sqlite_store.py](C:\dev\01_projects\06_mcp-memory\storage\sqlite_store.py):36-69).
- `edges` table **does** have `last_activated` at [storage/sqlite_store.py](C:\dev\01_projects\06_mcp-memory\storage\sqlite_store.py):84.
- Current code attempts to update `nodes.last_activated` in `_bcm_update()` at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):276-283, but that column is not defined in `nodes` schema here.

5. **How `promote_node` affects scoring currently**

Function: `def promote_node(...) -> dict` at [tools/promote_node.py](C:\dev\01_projects\06_mcp-memory\tools\promote_node.py):158-310.

Current effects relevant to recall scoring:

- Updates node `type` and `layer` at [tools/promote_node.py](C:\dev\01_projects\06_mcp-memory\tools\promote_node.py):257-261.
- Inserts `realized_as` edges with `strength=1.0` at [tools/promote_node.py](C:\dev\01_projects\06_mcp-memory\tools\promote_node.py):268-271.
- `hybrid_search` scoring does not directly read promotion history/metadata, but indirect effects are:
  - New edges can change graph traversal candidates and thus `GRAPH_BONUS` inclusion ([storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):501-521).
  - Edge strength can affect UCB traversal ranking (`w_ij`) at [storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):138-146.
  - Changed `type` can affect type filters and typed-vector channel eligibility ([storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):465-490, 535-536, 524-526).
- No direct recalculation of `quality_score`, `temporal_relevance`, or `tier` inside `promote_node`.

6. **RRF formula used**

In `hybrid_search()` ([storage/hybrid.py](C:\dev\01_projects\06_mcp-memory\storage\hybrid.py):514-527):

- Base RRF per rank: `1 / (RRF_K + rank)` for vector and FTS channels.
- Typed channel: `TYPE_CHANNEL_WEIGHT / (RRF_K + rank)`.
- Plus graph additive bonus: `+ GRAPH_BONUS` for graph neighbors (not reciprocal).

Constants from config:
- `RRF_K = 18` at [config.py](C:\dev\01_projects\06_mcp-memory\config.py):22
- `GRAPH_BONUS = 0.005` at [config.py](C:\dev\01_projects\06_mcp-memory\config.py):23
- `TYPE_CHANNEL_WEIGHT = 0.5` at [config.py](C:\dev\01_projects\06_mcp-memory\config.py):290