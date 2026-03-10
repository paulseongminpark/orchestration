# R2-03: Co-Retrieval 실측 데이터 + 설계

> R1: 방안A(edge boost) 채택, 추정 500-1000 pairs.
> Phase 0: edge ctx_log 기반 데이터, RRF k=30+RWR 0.05 조합.
> 이 문서: 실데이터 기반 파라미터 확정.

---

## 1. 실측 결과

### 1-1. recall_log 구조 (R1 가정과 다름)

R1 가정: `recall_log(query, result_ids JSON)`
실제: `recall_log(id, query, node_id, rank, score, mode, timestamp)` — **row per result**

→ co-occurrence 계산: `GROUP BY (query, timestamp)` 로 세션 구성

### 1-2. 수치

```
총 recall_log:          2,548건
2+ 결과 세션:             352건
Unique pairs:          10,783개
co_count ≥ 3:           1,160 pairs (R1 추정 500-1000 → 실측 초과)
co_count ≥ 5:             338 pairs
co_count ≥ 10:             49 pairs
```

### 1-3. 분포

```
co_count=1:    7,667 pairs (71%)  ← 노이즈, 무시
co_count=2:    1,956 pairs (18%)  ← 약한 신호
co_count=3-4:    822 pairs (8%)   ← 유효
co_count=5-9:    289 pairs (3%)   ← 강한 신호
co_count=10+:     49 pairs (0.5%) ← 허브 연결
```

### 1-4. Top 15 pairs

```
#1129(Project)  + #3895(Identity)  = 27회  ← 허브 pair
#3895(Identity) + #4124(Insight)   = 27회
#224(Workflow)   + #575(Workflow)   = 26회
#224(Workflow)   + #3895(Identity)  = 25회
#575(Workflow)   + #3895(Identity)  = 25회
#224(Workflow)   + #1129(Project)   = 24회
#575(Workflow)   + #1129(Project)   = 24회
#1129(Project)  + #4124(Insight)   = 24회
#224(Workflow)   + #4124(Insight)   = 22회
#575(Workflow)   + #4124(Insight)   = 22회
#2755(Goal)      + #2756(Workflow)  = 22회
#2755(Goal)      + #2766(Connection)= 21회
#2755(Goal)      + #3259(Workflow)  = 20회
#2756(Workflow)  + #2766(Connection)= 19회
#3895(Identity)  + #4049(Pattern)  = 18회
```

### 1-5. 관찰

1. **#3895(Identity), #1129(Project), #4124(Insight)** 가 허브 — 거의 모든 top pair에 포함
2. **Workflow 노드 (#224, #575)** 가 상위 — Workflow가 "범용 연결자" 역할 (타입 축소 시 주의)
3. **허브 노드 편향**: top pair가 모두 허브 노드 조합. 진짜 의미 있는 co-retrieval은 **허브 제외 후** 분석 필요

---

## 2. 설계 수정

### 2-1. min_co_count 결정

| 기준 | pairs | 용도 |
|------|-------|------|
| ≥3 | 1,160 | 너무 많음 → edge 폭발 |
| **≥5** | **338** | **적정 — edge 테이블 관리 가능** |
| ≥10 | 49 | 너무 적음 — 허브만 남음 |

**결정: min_co_count=5**

### 2-2. 허브 노드 필터링

degree centrality 상위 5%를 허브로 정의. 허브-허브 pair는 co-retrieval boost 제외.

```python
def update_co_retrieval(conn, min_co_count=5, hub_percentile=95):
    # 1. 허브 노드 식별
    hub_ids = get_hub_nodes(conn, percentile=hub_percentile)

    # 2. co_count 계산 (허브-허브 제외)
    pairs = calculate_co_occurrence(conn, min_co_count)
    filtered = [(a, b, cnt) for a, b, cnt in pairs
                if not (a in hub_ids and b in hub_ids)]

    # 3. edge boost 적용
    for a, b, cnt in filtered:
        boost = min(0.1 * (cnt - min_co_count + 1), 0.5)
        upsert_edge(conn, a, b, co_retrieval_boost=boost)
```

### 2-3. CO_RETRIEVAL_WEIGHT

R1 제안: 0.1~0.3 범위.

실측 기반:
- co_count=5의 pair는 약한 연결 → 0.1
- co_count=10+는 강한 연결 → 0.3~0.5
- 선형 스케일: `weight = min(0.1 * (co_count - 4), 0.5)`

**UCB traverse에서:**
```python
score = w_ij + c * sqrt(ln(N_i+1) / (N_j+1))
if co_retrieval_boost > 0:
    score += co_retrieval_boost  # 0.1 ~ 0.5
```

### 2-4. edges 테이블 변경

```sql
ALTER TABLE edges ADD COLUMN co_retrieval_count INTEGER DEFAULT 0;
ALTER TABLE edges ADD COLUMN co_retrieval_boost REAL DEFAULT 0.0;
```

### 2-5. 갱신 주기

daily_enrich Phase에 추가 (Phase 1 완료 후).
대안: 매 100 recall 마다 자동 갱신 (recall_log count 기반 트리거).

---

## 3. 예상 효과

- 338 유효 pair → 338 edge boost 추가
- 허브 편향 제거 → 진짜 의미적 공동 출현만 강화
- NDCG 기여: graph traverse에서 2nd-hop 도달률 개선 예상

---

## 4. 미결

- [ ] 허브 percentile 값 튜닝 (95%? 90%?)
- [ ] A/B 테스트 설계: boost ON/OFF goldset 비교
- [ ] Workflow 타입 축소 후 co-retrieval 재계산 필요 (현재 Workflow 허브가 결과 왜곡)
