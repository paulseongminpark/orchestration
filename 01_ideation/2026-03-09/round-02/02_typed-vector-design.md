# Typed Vector 강화 설계 — Round 2

> 날짜: 2026-03-09
> 목적: q059, q073 같은 "summary 거의 동일인데 못 찾는" 문제 해결

---

## 1. 현재 구조

```
_detect_type_hints(query) → _type_hints 리스트
  ↓
if _type_hints:
    for hint_type in _type_hints:
        typed_vec_results = vector_search(query, where={type: hint_type})
        scores[node_id] += TYPE_CHANNEL_WEIGHT / (RRF_K + rank)   # 0.5 가중치
```

**문제**: TYPE_CHANNEL_WEIGHT=0.5로 typed vector 채널이 기본 채널(1.0) 대비 약함.
- Principle 타입이 압도적 (4000+ 노드 중 다수가 Principle)
- Pattern, Decision, Signal 등 소수 타입은 기본 벡터에서 밀림

---

## 2. _detect_type_hints 현재 로직

```python
# storage/hybrid.py:399-407 (추정)
TYPE_KEYWORDS = {
    "Principle": ["원칙", "규칙", "rule"],
    "Pattern": ["패턴", "pattern", "반복"],
    "Decision": ["결정", "decided", "확정"],
    "Failure": ["실패", "에러", "버그"],
    ...
}
```

**문제점**:
- q059: "패턴은 뭐였지?" → "패턴" 감지 → _type_hints=["Pattern"] 이지만, TYPE_CHANNEL_WEIGHT=0.5가 너무 낮아서 Principle에 밀림
- q073: "결정은 뭐였지?" → "결정" 감지 → _type_hints=["Decision"] 이지만, 역시 부족

---

## 3. 설계 제안

### 방안 A: TYPE_CHANNEL_WEIGHT 동적화

```python
# type hint 감지 시 가중치를 type별로 다르게
DYNAMIC_TYPE_WEIGHT = {
    "Pattern": 1.0,     # 소수 타입 → 강한 부스트
    "Decision": 1.0,    # 소수 타입
    "Signal": 0.8,
    "Failure": 0.8,
    "Experiment": 0.8,
    "Principle": 0.3,   # 다수 타입 → 약한 부스트 (이미 기본 검색에서 우세)
    "default": 0.5,
}
```

**장점**: 최소 변경 (1줄). **단점**: 하드코딩.

### 방안 B: Type Guarantee Slot

typed vector 결과 상위 N개를 최종 결과에 **보장**:

```python
# 최종 결과 구성 시
typed_guaranteed = []
for hint_type, t_results in typed_vec_by_type.items():
    # typed vector 상위 2개를 guaranteed slot으로 확보
    for node_id, distance, _ in t_results[:2]:
        if node_id not in [r['id'] for r in result]:
            typed_guaranteed.append(node_id)

# 최종 top_k에서 하위 N개를 typed_guaranteed로 교체
if typed_guaranteed:
    result = result[:top_k - len(typed_guaranteed)] + [get_node(nid) for nid in typed_guaranteed]
```

**장점**: type hint 감지 시 해당 타입 노드가 반드시 포함. **단점**: 다른 좋은 결과를 밀어냄.

### 방안 C: Query Decomposition (쿼리 분해)

긴 쿼리를 2개로 분할:
1. 핵심어 쿼리 (의미 검색)
2. 타입+키워드 쿼리 (타입 필터 검색)

```python
if len(query) > 30 and _type_hints:
    # 원래 쿼리로 기본 검색
    base_results = _hybrid_core(query, top_k)
    # 타입 필터 + 짧은 키워드로 보조 검색
    short_query = extract_keywords(query)  # "컨텍스트 비대화 병렬 세션 index"
    typed_results = vector_search(short_query, where={type: _type_hints[0]}, top_k=5)
    # 두 결과 합산
    merged = rrf_merge(base_results, typed_results)
```

**장점**: 근본적 해결. **단점**: 구현 복잡도 높음. 키워드 추출 로직 필요.

---

## 4. 추천

**방안 A (동적 가중치)** 먼저 적용 → 측정 → 부족하면 B 추가.

- 구현 난이도: 낮음 (config.py에 상수 추가, hybrid.py 3줄 수정)
- 예상 효과: q059, q073 같은 "type hint 감지됐지만 밀린" 케이스 해결
- 위험: Principle 이외 타입의 오탐 증가 가능 (검증 필요)

방안 C는 Phase 5 A8 Discovery 패턴과 통합 검토.

---

## 5. 실험 계획

```
[1] goldset 수정 3건 적용 (q065, q069, q074) → NDCG 재측정
[2] 쿼리 정규화 2건 적용 (q057, q060) → NDCG 재측정
[3] 방안 A (동적 가중치) 적용 → NDCG 재측정
[4] 방안 A+B 조합 → NDCG 재측정
```
