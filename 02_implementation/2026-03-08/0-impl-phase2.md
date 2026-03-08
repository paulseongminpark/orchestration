# Phase 2: Recall 혁명

> 세션: Warp-1 (스코어링) + Warp-2 (Correction)
> 예상 시간: Warp-1 6시간, Warp-2 3시간
> 전제: 없음 (Phase 1과 병렬 가능)
> 검증: CX (Codex CLI)

---

## Warp-1: 복합 스코어링 (A1 + A4 + A6)

### P2-W1-01: config.py 상수 추가

- [x] P2-W1-01-a: config.py에 복합 스코어링 상수 추가
  ```python
  # Composite Scoring (Phase 2, 2026-03-08 ideation)
  COMPOSITE_WEIGHT_RRF = 0.5
  COMPOSITE_WEIGHT_DECAY = 0.3
  COMPOSITE_WEIGHT_IMPORTANCE = 0.2
  DECAY_LAMBDA = 0.01           # half-life ~69 days
  PROMOTED_MULTIPLIER = 1.5     # reviewed-item boost
  LAYER_IMPORTANCE = {
      "L5": 1.0, "L4": 0.8, "L3": 0.6,
      "L2": 0.4, "L1": 0.2, "L0": 0.1,
      "Unclassified": 0.1
  }
  ```
- [x] P2-W1-01-b: git commit "[mcp-memory] P2-W1-01: composite scoring 상수"

### P2-W1-02: last_accessed_at 컬럼 추가

- [x] P2-W1-02-a: nodes 테이블에 `last_accessed_at TEXT` 컬럼 추가 (3359노드 초기화 완료)
- [x] P2-W1-02-b: sqlite_store.py에서 마이그레이션 함수 추가 (기존 패턴 따라 ALTER TABLE + UPDATE)
- [x] P2-W1-02-c: git commit "[mcp-memory] P2-W1-02: last_accessed_at 컬럼"

### P2-W1-03: recall()에 composite scoring 적용

- [x] P2-W1-03-a: storage/hybrid.py의 recall 로직에서 최종 점수 계산 변경
  ```python
  import math
  from datetime import datetime

  def composite_score(rrf_score, node):
      # importance from layer
      layer = node.get("layer", "Unclassified")
      importance = LAYER_IMPORTANCE.get(layer, 0.1)

      # decay from last access
      last_access = node.get("last_accessed_at") or node.get("updated_at")
      days = (datetime.now() - last_access).days if last_access else 365
      decay = importance * math.exp(-DECAY_LAMBDA * days)

      # promoted multiplier
      multiplier = PROMOTED_MULTIPLIER if node.get("promoted") else 1.0

      # final
      score = (COMPOSITE_WEIGHT_RRF * rrf_score +
               COMPOSITE_WEIGHT_DECAY * decay +
               COMPOSITE_WEIGHT_IMPORTANCE * importance) * multiplier
      return score
  ```
- [x] P2-W1-03-b: recall() BCM에서 last_accessed_at 갱신 (last_activated→last_accessed_at)
- [x] P2-W1-03-c: 기존 테스트 실행 (161 PASS, 사전실패 2건=Correction top-inject)
- [x] P2-W1-03-d: git commit "[mcp-memory] P2-W1-03: composite scoring 적용"

### P2-W1-04: Goldset NDCG 재측정

- [ ] P2-W1-04-a: `pytest tests/test_goldset.py -v` 실행
- [ ] P2-W1-04-b: NDCG@5, NDCG@10 기록 (q026-q050, q051-q075 분리)
- [ ] P2-W1-04-c: 가중치 튜닝 필요 시 조정 (COMPOSITE_WEIGHT_* 변경)
- [ ] P2-W1-04-d: 최종 NDCG 기록 → 이 문서에 업데이트

**NDCG 결과**: (Warp-1이 채울 것)
```
Before: NDCG@5=0.460, NDCG@10=0.488
After:  NDCG@5=_____, NDCG@10=_____
  q026-q050: NDCG@5=_____
  q051-q075: NDCG@5=_____
```

---

## Warp-2: Correction 노드 타입 (A5)

**전제: Warp-1이 config.py 커밋 완료 후 시작.** `git pull` 먼저.

### P2-W2-01: Correction 타입 정의

- [x] P2-W2-01-a: config.py PROMOTE_LAYER Layer 3에 "Correction": 3 추가, schema.yaml도 등록
- [x] P2-W2-01-b: git commit "[mcp-memory] P2-W2-01: Correction 타입 추가"

### P2-W2-02: recall() top-inject

- [x] P2-W2-02-a: tools/recall.py에 Correction top-inject 로직 추가
  - 기존 RRF 검색 수행
  - hybrid_search(type_filter="Correction") 호출, score > 0.5 필터
  - 결과 맨 앞에 삽입 (ID 기준 중복 제거)
  - Correction 0개면 기존 동작 동일
- [x] P2-W2-02-b: 기존 테스트 169개 PASS 확인 (163→169, mock 업데이트)
- [x] P2-W2-02-c: git commit "[mcp-memory] P2-W2-02: Correction top-inject"

### P2-W2-03: 테스트

- [x] P2-W2-03-a: tests/test_correction.py — top-inject, dedup, low-score 필터 테스트
- [x] P2-W2-03-b: Correction 0개 시 기존 동작 동일 확인 (test_no_correction_same_behavior)
- [x] P2-W2-03-c: git commit "[mcp-memory] P2-W2-03: Correction 테스트"

---

## Phase 2 검증 (CX)

- [ ] P2-CX-01: goldset NDCG 재측정 (위 Codex 명령어)
- [ ] P2-CX-02: 코드 리뷰 — scoring 공식, edge cases, 호환성 (위 Codex 명령어)
- [ ] P2-CX-03: 전체 테스트 163 + 신규 PASS 확인

**Phase 2 완료 기준**:
- [ ] NDCG@5 ≥ 0.55 (전체)
- [ ] NDCG@5(q051-q075) ≥ 0.35 (현재 0.244에서 개선)
- [x] 163 + 신규 테스트 전부 PASS (169 PASS)
- [x] Correction top-inject 동작 확인
- [ ] CX 리뷰 PASS
