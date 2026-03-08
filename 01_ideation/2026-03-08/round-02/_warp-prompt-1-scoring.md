# Warp Pane 1 프롬프트: 복합 스코어링 (A1+A4+A6)

> 이 프롬프트를 Warp의 Claude Opus 1M 세션에 붙여넣기

---

```
mcp-memory recall 스코어링을 3차원으로 확장하는 작업이다.

## 현재 상태
- mcp-memory v2.2.1, 경로: /c/dev/01_projects/06_mcp-memory/
- recall = 3-Layer search (RRF: vector + FTS5 + type channel + diversity cap)
- NDCG@5: 0.460, NDCG@10: 0.488
- q026-q050 NDCG@5: 0.519, q051-q075 NDCG@5: 0.244
- 163 테스트 PASS
- promote_node 존재하지만 recall 점수에 미반영
- 노드 2,869개, 전부 동일 가중치, 시간 감쇠 없음

## 구현할 것 (3개)

### 1. 복합 스코어링 프레임워크 (A1)
현재 recall의 최종 점수를 다차원으로 확장:
```
final_score = rrf_score × 0.5 + decay_score × 0.3 + importance_score × 0.2
```
- rrf_score: 기존 RRF 점수 (vector + FTS5 + type channel)
- decay_score: 아래 2번
- importance_score: Layer(L0~L5) 기반. L5=1.0, L4=0.8, L3=0.6, L2=0.4, L1=0.2, L0=0.1

### 2. Half-life Decay (A4)
```python
import math
decay_score = importance × math.exp(-lambda_val × days_since_access)
```
- `days_since_access`: 마지막 access (recall로 검색되거나 수동 조회) 이후 경과일
- `lambda_val`: 0.01 (반감기 ~69일). 튜닝 가능하도록 config 상수화.
- `importance`: Layer 기반 (위와 동일)
- nodes 테이블에 `last_accessed_at` 컬럼 필요 (없으면 추가)
- recall() 호출 시 반환된 노드의 last_accessed_at 갱신

### 3. Reviewed-item Multiplier (A6)
- promote_node()로 승격된 노드에 1.5x multiplier
- 구현: nodes 테이블의 `promoted` 또는 `review_count` 필드 확인
- final_score 계산 시: promoted 노드면 × 1.5

## 가중치 상수
모든 가중치를 config.py에 상수로:
```python
COMPOSITE_WEIGHT_RRF = 0.5
COMPOSITE_WEIGHT_DECAY = 0.3
COMPOSITE_WEIGHT_IMPORTANCE = 0.2
DECAY_LAMBDA = 0.01  # half-life ~69 days
PROMOTED_MULTIPLIER = 1.5
```

## 제약 조건
- 기존 163 테스트 깨지면 안 됨
- goldset (q026-q075) NDCG 측정 후 비교
- recall() 인터페이스 변경 최소화 (기존 호출 코드 호환)

## 작업 순서
1. config.py에 상수 추가
2. nodes 테이블에 last_accessed_at 컬럼 추가 (마이그레이션)
3. recall() 내부에서 composite scoring 적용
4. recall() 호출 시 last_accessed_at 갱신
5. promote_node → multiplier 반영
6. 기존 테스트 실행 (163개 PASS 확인)
7. goldset NDCG 재측정 (pytest tests/test_goldset.py -v)

## Codex 사전분석 결과 (정확한 삽입 지점)

- **스코어 최종 할당**: `storage/hybrid.py:541-548` — `node["score"] = scores[node_id] + enrichment_bonus + tier_bonus`
- **이 줄을 composite_score()로 교체**하면 됨
- **RRF 누적**: hybrid.py:514-527 (vector, FTS, graph, typed channel)
- **`last_accessed_at` 컬럼 없음** — nodes 테이블에 ALTER TABLE 추가 필요
- **promote_node**: layer/type만 변경, 점수 직접 반영 없음 → multiplier 추가 필요
- **nodes 기존 컬럼에 `layer`, `tier`, `quality_score` 있음** — layer를 importance 프록시로 사용
- **config.py 상수 위치**: RRF_K=18 (line 22), GRAPH_BONUS=0.005 (line 23), TYPE_CHANNEL_WEIGHT=0.5 (line 290)
- **상세**: `/c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/cx-pre-scoring-analysis.md`

소스코드 수정 금지 대상: 없음 (구현 세션). git commit 자유.
```
