# 03: A8 Discovery — Co-retrieval 패턴 학습

> Phase 5 항목. v2.1 결정 #22(recall mode) + #23(TTL 캐시) 기반 확장.
> 핵심: 함께 검색되는 노드 패턴을 학습해서 인출 품질을 올린다.

---

## 1. 현재 검색 학습 메커니즘

### 1-1. BCM (Bienenstock-Cooper-Munro)

```
recall("X") → 결과에 노드 A, B, C
  → A를 사용 (높은 유용성)
  → B를 무시
  → C를 사용 (낮은 유용성)
  → edge A↔query 강화, C↔query 약한 강화, B↔query 약화
```

BCM은 **개별 노드-쿼리 관계**를 학습. "X를 검색하면 A가 유용하다" 학습.

### 1-2. UCB (Upper Confidence Bound)

```
recall("X") → graph traverse
  → visit_count가 적은 노드 탐험 (explore)
  → 이미 검증된 노드 활용 (exploit)
  → c 값으로 explore/exploit 비율 조절
```

UCB는 **탐험-활용 균형**. 새로운 노드 발견 촉진.

### 1-3. 빠진 것: Co-retrieval

BCM은 "쿼리→노드" 관계. **"노드→노드" 공동 출현 패턴**은 학습하지 않는다.

예:
- recall("에이전트 설계") → 항상 #8(Claude 권한), #47(설계 원칙), #257(거버넌스)이 함께 나옴
- 이 3개는 서로 관련 — 하나를 찾으면 나머지도 필요할 가능성 높음
- 현재: 매번 독립적으로 검색
- 제안: 공동 출현 패턴 학습 → shortcut

---

## 2. Co-retrieval 설계

### 2-1. 공동 출현 기록

recall_log에 이미 결과가 기록됨:
```sql
recall_log(query, result_ids, mode, created_at)
-- result_ids: [8, 47, 257, 120, 43]
```

공동 출현 빈도:
```sql
-- 노드 A와 B가 같은 recall 결과에 몇 번 함께 나왔는가
SELECT a.node_id, b.node_id, COUNT(*) as co_count
FROM recall_results a
JOIN recall_results b ON a.recall_id = b.recall_id AND a.node_id < b.node_id
GROUP BY a.node_id, b.node_id
HAVING co_count >= 3  -- 3번 이상 함께 출현
```

### 2-2. 활용 방안

**방안 A: 공동 출현 edge 강화**
- co_count >= 3인 노드 쌍의 edge strength 보너스
- UCB traverse 시 co-retrieval edge 우선 탐색
- 장점: 기존 구조 활용, 구현 간단
- 단점: edge가 너무 많아질 수 있음

**방안 B: Retrieval Cluster (shortcut)**
- 자주 함께 나오는 노드 그룹을 클러스터로 저장
- recall 시 하나가 hit되면 클러스터 전체 boost
- 장점: 검색 속도 개선, 의미적 그룹핑
- 단점: 클러스터 관리 복잡도

**방안 C: recall_log 기반 추천**
- "이 노드를 본 사람은 이것도 봤다" (협업 필터링 패턴)
- recall 결과 + 과거 co-retrieval 기반 추가 추천
- 장점: 새로운 연결 발견
- 단점: cold start (초기 데이터 부족)

### 2-3. 선택 근거

**방안 A 우선 (P1)**:
- 기존 edge strength + UCB 구조에 자연스럽게 통합
- recall_log 데이터 이미 축적 중 (1,567+ 로그)
- enrichment E16 (strength recalibration)에서 co_count 반영 가능

**방안 B는 P2**:
- Phase 2 완료 후, 충분한 recall_log 축적 후
- 클러스터 = E22 assemblage detection 확장

---

## 3. 구현 설계

### 3-1. Phase 1: edge co-occurrence boost

```python
# daily_enrich.py 또는 별도 스크립트
def update_co_retrieval_edges(conn, min_co_count=3):
    """recall_log에서 공동 출현 빈도 계산 → edge strength 보너스."""
    pairs = conn.execute("""
        WITH recall_pairs AS (
            SELECT r1.node_id as a, r2.node_id as b, r1.recall_id
            FROM recall_results r1
            JOIN recall_results r2
              ON r1.recall_id = r2.recall_id AND r1.node_id < r2.node_id
        )
        SELECT a, b, COUNT(DISTINCT recall_id) as co_count
        FROM recall_pairs
        GROUP BY a, b
        HAVING co_count >= ?
    """, (min_co_count,)).fetchall()

    for a, b, co_count in pairs:
        # 기존 edge가 있으면 strength boost, 없으면 신규 생성
        boost = min(0.1 * co_count, 0.5)  # max boost 0.5
        # edge 업데이트 로직...
```

### 3-2. hybrid_search에서 활용

```python
# UCB traverse 시 co-retrieval edge 보너스
def _ucb_traverse(self, seed_ids, ...):
    # 기존 UCB score 계산
    score = w_ij + c * sqrt(ln(N_i+1) / (N_j+1))
    # co-retrieval 보너스
    if edge.co_retrieval_count > 0:
        score += CO_RETRIEVAL_WEIGHT * min(edge.co_retrieval_count / 10, 1.0)
```

### 3-3. 데이터 현황

```
recall_log: 1,567+ 로그
평균 결과 수: 5/recall
→ 예상 pair 수: 1,567 × C(5,2) = ~15,670 pairs
→ min_co_count=3 필터 후: 예상 ~500-1,000 유효 pairs
```

충분한 데이터가 이미 있음.

---

## 4. enrichment 배치와의 연결

오늘 실행한 enrichment 배치(166개)로:
- 기존 unenriched 노드에 summary, key_concepts, quality_score 부여
- 이 노드들이 이제 검색에서 공정하게 경쟁
- co-retrieval은 이 새로운 enriched 노드들의 위치를 그래프에서 확립하는 역할

---

## 5. 미결

- [ ] co_retrieval_count를 edges 테이블에 추가할지, 별도 테이블에 저장할지
- [ ] 갱신 주기: daily_enrich에 포함? 별도 스크립트?
- [ ] CO_RETRIEVAL_WEIGHT 초기값 (0.1~0.3 범위 A/B 테스트)
- [ ] recall_results 테이블 존재 확인 (현재 recall_log 구조 확인 필요)
