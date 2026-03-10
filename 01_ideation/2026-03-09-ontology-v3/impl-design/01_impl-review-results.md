# Ontology v3 — Phase 4 Impl Review 결과

> 날짜: 2026-03-10
> Codex (gpt-5.4): 코드 수준 리뷰 — Critical 3, High 4, Medium 4
> Gemini (Auto): 아키텍처 리뷰 — 핵심 4건
> 상태: **설계 수정 필요.** 현재 설계대로 구현하면 안전하지 않음.

---

## Codex 리뷰 (11건)

### Critical (3건) — 구현 전 반드시 해결

| # | 문제 | 상세 | 필요 조치 |
|---|------|------|-----------|
| C1 | **sync_schema()가 deprecated 상태를 리셋** | 서버 재시작 시 schema.yaml 기준으로 type_defs를 active로 되돌림. DB에서 deprecated 처리해도 재시작하면 풀림. | schema.yaml + sync_schema() 정책을 같이 수정. deprecated 타입은 sync에서 skip 또는 유지. |
| C2 | **마이그레이션이 type만 변경, layer/tier/vector metadata 미갱신** | nodes.layer는 access control, firewall, scoring에 사용. type 바꿔도 layer/tier가 옛 값이면 scoring 어긋남. Chroma 메타도 옛 타입. | type + layer + tier + Chroma metadata + E7 재실행을 한 세트로 마이그레이션. |
| C3 | **50개 타입 중 20개 매핑 누락** | Aporia, Assumption, Boundary, Commitment, Concept, Constraint, Context, Correction, Evidence, Heuristic, Lens, Mental Model, Metaphor, Paradox, Plan, Ritual, Trade-off, Trigger, Vision, Wonder — 설계에 경로 없음. | 모든 51개 타입에 대해 keep/merge/archive/edge-convert/hard-block 확정 필요. |

### High (4건) — 구현 품질에 직접 영향

| # | 문제 | 필요 조치 |
|---|------|-----------|
| H1 | **recall() type_filter에 deprecated canonicalization 없음** | recall/hybrid_search에서 type_filter 입력 시 deprecated→replaced_by 자동 변환 |
| H2 | **recall_log 세션 식별 불안정** (GROUP BY query,timestamp — 같은 초 중복) | recall_log에 recall_id 컬럼 추가, co-retrieval은 recall_id로 세션화 |
| H3 | **co-retrieval edge 방향/중복 + build_graph()에 boost 미전달** | (source_id,target_id) 복합 index + uniqueness, build_graph()에 co_retrieval_boost attr 추가 |
| H4 | **retrieval_hints가 insert_node/FTS/E7에 연결 안 됨** | sqlite_store.insert_node() plumbing + FTS trigger 수정 + E7 prompt에 hints 반영 + re-embed 계획 |

### Medium (4건) — 개선 권고

| # | 문제 | 필요 조치 |
|---|------|-----------|
| M1 | retrieval_hints JSON edge case (NULL vs {}, malformed, string extend 깨짐) | schema validation + parse fallback + 타입 체크 |
| M2 | co-retrieval이 correction/patch 후 결과를 학습 | raw vs surfaced result set 중 학습 대상 결정 |
| M3 | recall_log/edges 인덱스 부족 + 트랜잭션 경계 미설정 | 인덱스 추가 + explicit transaction + checkpoint |
| M4 | classifier.py import 깨짐 (get_valid_node_types 없음) | classifier load path 복구 후 v3 수정 |

---

## Gemini 리뷰 (4건)

| # | 문제 | 필요 조치 |
|---|------|-----------|
| G1 | **Vector 재임베딩 누락** — retrieval_hints가 embedding_text에 포함되려면 ChromaDB 전체 재임베딩 필수 | Step 2.5: hints 생성 후 re-embed 단계 추가 |
| G2 | **테스트 기대값 수정** — 타입 매핑 후 163개 테스트의 expected type 일괄 업데이트 | Test Adaptation 단계 필수 |
| G3 | **마이그레이션 전 DB 백업** — 롤백이 복잡하므로 memory.db.v2_final 스냅샷 | migrate_v3.py 시작 시 자동 백업 |
| G4 | **동시성** — 마이그레이션 중 remember() 호출 시 신/구 온톨로지 충돌 | 마이그레이션 중 서버 read-only 또는 v3 규칙 선배포 |

---

## Codex "Minimum Safe Changes" (구현 전 필수 8항목)

1. schema.yaml + type_defs + sync_schema() 같이 수정 → deprecated 유지
2. type migration 시 type + layer + tier + vector metadata + E7 한 세트
3. recall_log에 recall_id 추가 → co-retrieval 세션 키
4. edges(source_id, target_id) 복합 index + uniqueness 전략
5. build_graph()에 co_retrieval_boost 전달 경로
6. type_filter에 deprecated canonicalization
7. retrieval_hints는 insert_node + FTS + E7 + re-embed까지 포함
8. classifier.py import path 복구

---

## 설계 수정 방향 (Phase 4 R3 — 직접 통합)

### Impl Design 수정 항목

| 설계 섹션 | 수정 내용 |
|----------|----------|
| D-1 DB 스키마 | + recall_log.recall_id, + edges 복합 index, sync_schema() 정책 변경 |
| D-1 마이그레이션 | + layer/tier 갱신, + Chroma re-embed, + DB 백업, + 51개 전타입 매핑표 |
| D-2 API | + type_filter canonicalization in recall() |
| D-3 enrichment | + E7에 retrieval_hints 반영, + re-embed 단계 (Step 2.5) |
| D-4 분류기 | + classifier.py import 복구 선행 |
| D-5 co-retrieval | + recall_id 세션화, + build_graph() boost 전달, + edge uniqueness |
| D-7 테스트 | + Test Adaptation 단계, + DB 백업 검증 |

### 구현 순서 수정

```
기존:  Step 1 → 2 → 3 → 4
수정:
  Step 0 (선행): classifier.py 복구 + recall_log.recall_id + edges 복합 index
  Step 1 (P1): 스키마 + 단순 매핑 (+ layer/tier/sync_schema 동시)
  Step 1.5: DB 백업 (memory.db.v2_final) + 테스트 기대값 수정
  Step 2 (P2): Workflow LLM + retrieval_hints + 51개 전타입 매핑표
  Step 2.5: ChromaDB re-embed (retrieval_hints 반영)
  Step 3 (P3): co-retrieval (recall_id 기반 + build_graph 수정)
  Step 4 (P4): dispatch + L3
```

---

## 다음 세션 TODO

1. **Impl Design 수정판** (00_impl-design-v2.md) — Codex/Gemini 피드백 전부 반영
2. **51개 전타입 매핑표** 작성 (누락 20개 포함)
3. **classifier.py import 복구** (M4, 선행 작업)
4. **수정된 설계 → Phase 5 구현 시작**
