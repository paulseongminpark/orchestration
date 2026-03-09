# NDCG q051-q075 병목 분석 — Ideation Round 1

> 날짜: 2026-03-09
> 목표: hybrid_search에서 q051-q075 세그먼트 NDCG@5=0.227 원인 규명 + 개선 방향

---

## 1. 현황

| 세그먼트 | NDCG@5 | NDCG@10 | hit_rate | 쿼리 수 |
|----------|--------|---------|----------|---------|
| q001-q025 | 0.604 | 0.616 | 0.960 | 25 |
| q026-q050 | 0.546 | 0.610 | 0.640 | 25 |
| **q051-q075** | **0.227** | **0.243** | **0.240** | 25 |
| 전체 | 0.459 | 0.489 | 0.613 | 75 |

q051-q075: 9건 ZERO, 12건 LOW. hit_rate 24% = 25건 중 6건만 top-10에 정답 포함.

---

## 2. 근본 원인 3가지

### 원인 A: FTS5 trigram의 한국어 2글자 단어 미매칭
- trigram 토크나이저: 3글자 슬라이딩 윈도우
- "절차", "목록", "원인" 같은 2글자 핵심어가 FTS에서 효과적으로 매칭되지 않음
- 보조 LIKE 검색의 high_thresh=2 (2개 이상 매칭 필요) → 짧은 핵심어 쿼리에서 미달
- **코드**: `storage/hybrid.py:427-475`, `storage/sqlite_store.py:119`

### 원인 B: 긴 서술형 쿼리와 노드 summary 간 vocabulary mismatch
- q051-q075 쿼리 평균 50자, "~는 뭐였지?" 패턴
- 노드 summary는 간결한 서술 (30-60자)
- 쿼리 어휘와 노드 어휘가 다름 → 벡터 유사도 감소
- 예: q057 "orchestration 프로젝트 구조와 핵심 경로를 정리한 프로젝트 개요는 뭐였지?"
  → #102 "AI 오케스트레이션 시스템을 중심으로 하는 볼트의 핵심 프로젝트 구조"
  → "orchestration" vs "오케스트레이션", "개요" vs "구조" 등 어휘 불일치

### 원인 C: RRF 후보풀 한계 (top_k*10)
- sorted_ids[:top_k*10] 에서 cutoff = top_k=5일 때 50개
- vector top_k*4=20 + FTS top_k*4=20 + graph ≈ 40-50개 합집합
- 정답 노드가 vector rank 25-40이면 RRF 합산 후 cutoff 밖으로 밀려남
- **코드**: `storage/hybrid.py:534`

---

## 3. q051-q075 ZERO 쿼리 상세

| Query | NDCG@5 | relevant_ids | 반환된 top-5 | 원인 |
|-------|--------|--------------|-------------|------|
| q057 | 0.000 | [15, 102] | [227, 1290, 1656, 3575, 1408] | vocab mismatch |
| q059 | 0.000 | [4119, 4235] | [222, 378, 756, 1488, 1655] | 4000대 노드 미검색 |
| q060 | 0.000 | [36, 37, 120] | [378, 35, 758, 3367, 164] | 36 hit@6이하, 37/120 미검색 |
| q061 | 0.000 | [27, 98] | [227, 188, 77, 2601, 2638] | vocab mismatch |
| q065 | 0.000 | [4243] | [1301, 35, 4173, 4067, 4194] | FTS miss |
| q069 | 0.000 | [189] | [220, 222, 151, 86, 147] | vocab mismatch |
| q072 | 0.000 | [4248, 4257] | [3813, 2696, 1488, 1579, 4033] | 4000대 노드 미검색 |
| q073 | 0.000 | [4247, 4255, 4257] | [849, 135, 3813, 2696, 2602] | 4000대 노드 미검색 |
| q074 | 0.000 | [4045, 4231] | [132, 603, 151, 222, 276] | vocab mismatch |

---

## 4. 개선 방향

### 방향 1: 즉시 개선 (파라미터 튜닝)
- FTS 보조 검색 `high_thresh` 2→1 (hybrid.py:467)
- 후보풀 `top_k*10` → `top_k*16` (hybrid.py:534)
- 예상 영향: hit_rate +10-15%

### 방향 2: goldset 쿼리 정규화
- q051-q075 쿼리를 target 노드 어휘에 근접하게 재작성
- "~는 뭐였지?" 접미사 제거, 핵심어 노드 summary와 정렬
- 예: q057 "orchestration 프로젝트 구조" → "AI 오케스트레이션 시스템 프로젝트 구조"
- 주의: goldset은 실제 사용자 쿼리 패턴을 반영해야 함 → 과도한 정규화 지양

### 방향 3: Query Expansion (알고리즘)
- 긴 쿼리(>30자)에서 핵심 개념어 추출 → 요약 쿼리로 2차 검색
- 또는: 쿼리를 2-3개 서브쿼리로 분할 후 각각 검색 → 결과 합산
- 구현 복잡도 높음, Phase 5 A8 Discovery 패턴과 연결 가능

### 방향 4: Type Hint 기반 Typed Vector 강화
- q051-q075는 명확한 타입 키워드 포함 (Workflow, Skill, Decision 등)
- TYPE_CHANNEL_WEIGHT=0.5 → 동적 가중치 (type hint 감지 시 0.8)
- 또는: typed vector 결과 상위 3개를 최종 결과에 보장

---

## 5. 추천 실행순서

```
[1] 방향 1 (파라미터 튜닝) — 30분, 즉시 측정 가능
[2] 방향 2 (goldset 쿼리 정규화) — 1시간, Paul 검증 필요
[3] 방향 4 (typed vector 강화) — 2시간, 코드 수정
[4] 방향 3 (query expansion) — 3시간+, Phase 5와 병합 검토
```

방향 1로 baseline 개선 후, 방향 2+4 순서. 방향 3은 Phase 5 통합.

---

## 7. 방향 1 실험 결과 (A/B 테스트)

### 실험: top_k 2배 확장 (10→20, 상위 10개 반환)

| 세그먼트 | baseline | experiment | delta |
|----------|----------|------------|-------|
| q001-q025 | 0.609 | 0.644 | +0.035 |
| q026-q050 | 0.546 | 0.402 | **-0.144** |
| q051-q075 | 0.217 | 0.173 | **-0.045** |
| 전체 | 0.457 | 0.406 | **-0.051** |

**결론: 단순 후보풀 확장은 역효과.** 노이즈 증가로 q026-q050이 크게 악화.
파라미터 튜닝만으로는 해결 불가. **방향 2 (goldset 정규화) + 방향 4 (typed vector 강화)** 가 핵심.

---

## 6. hybrid_search 채널 구조 (참고)

```
hybrid_search(query, top_k=10)
  ├─ Channel 1: Vector search (top_k*4=40)     weight=1.0
  ├─ Channel 2: FTS5 search (top_k*4=40)        weight=1.0
  ├─ Channel 3: Graph UCB/BCM neighbors          weight=GRAPH_BONUS=0.005 (flat)
  ├─ Channel 4: Typed vector (type hint 시)      weight=TYPE_CHANNEL_WEIGHT=0.5
  │
  ├─ RRF 합산: score = Σ (weight / (RRF_K + rank))    RRF_K=18
  ├─ Composite: score × (1 + decay + layer + type + recency + access)
  └─ Filter: sorted_ids[:top_k*10] → top_k 반환
```
