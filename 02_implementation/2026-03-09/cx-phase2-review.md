# Phase 2 CX 리뷰 결과 (Codex gpt-5.4 xhigh)

> 실행: 2026-03-09
> 상태: **NO-GO** — recall.py 버그 2건 수정 필요

---

## NDCG Results

| Metric | Baseline | Current | Delta |
|--------|----------|---------|-------|
| NDCG@5 | 0.460 | N/A | N/A |
| NDCG@10 | 0.488 | N/A | N/A |

> test_goldset.py 경로 변경으로 재측정 불가. checks/search_quality.py로 이동됨.
> 별도 세션에서 `python checks/search_quality.py` 실행 필요.

---

## Code Review: hybrid.py — ALL PASS

- **[PASS]** RRF + decay + importance 복합 스코어링 공식 정확성
  - additive mode로 base 보존, decay/importance bonus만 추가
- **[PASS]** decay 함수 edge case
  - 미래 시각/음수: max(0, ...) → 0일 처리
  - 0시간: 최대 recency bonus
  - 잘못된 날짜/누락: 365일 fallback
- **[PASS]** 가중치 곱셈 순서
  - bonus additive 합산 → PROMOTED_MULTIPLIER 마지막 적용
- **[PASS]** 하위 호환성
  - `enable_composite=False`면 기존 로직 유지 (경고: additive 가중치 하드코딩)

---

## Code Review: recall.py — 2 FAIL

- **[PASS]** Correction 노드 top-inject 로직 정확성
  - 맨 앞 삽입, 중복 제거, score > 0.5 필터 정상

- **[FAIL]** 기존 recall 흐름 충돌
  - **문제 1**: Correction 주입 시 `project` 파라미터 미전달
    → project-scoped recall에 다른 프로젝트의 Correction 노드 혼입 가능
  - **문제 2**: prepend 후 재-trim 없음
    → top_k=10 요청에 Correction 2개 추가되면 12개 반환 가능

- **[FAIL]** type 필터링 동작
  - `type_filter="Decision"` 호출에서도 Correction 무조건 주입
  - type_filter 조건을 Correction 검색/주입 로직이 존중하지 않음

---

## 수정 필요 사항

1. Correction 검색에 `project` 파라미터 전달
2. Correction 주입 후 `results = results[:top_k]` 재-trim
3. `type_filter`가 지정된 경우 Correction 주입 스킵 또는 필터 적용

## Overall Verdict: NO-GO → **GO (수정 완료, 2026-03-09)**

### 수정 적용 (recall.py L55-64)
1. `if not type_filter:` 조건 래핑 → type_filter 명시 시 Correction 주입 스킵
2. `project=project` 추가 → project-scoped Correction 검색
3. `[:top_k]` 재-trim 추가 → top_k 초과 방지

### 검증
- Correction 테스트: 6/6 PASS
- 전체 테스트: 169/169 PASS
- NDCG@5: 0.353 (임계값 0.25 ✅), NDCG@10: 0.396 (임계값 0.30 ✅)
- hit_rate: 0.613 (임계값 0.50 ✅)
