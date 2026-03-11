# Review Log — Session Chain + Ontology Redesign

> **실행일**: 2026-03-11
> **단계**: 구현 전 Ultrathink 점검 + 구현 후 E2E 검증

## 1. 구현 전 Ultrathink 전체 점검

compact 후 컨텍스트 복구 → 02_impl-design.md + 실제 코드 4개 파일 대조.

### 검증 항목

| 항목 | 설계 vs 실제 | 결과 |
|------|-------------|------|
| RELATION_RULES 3개 | `contains`, `led_to` ∈ ALL_RELATIONS (L128, L131) | ✅ 일치 |
| Narrative/Decision/Question | PROMOTE_LAYER에 전부 존재 (L249-250) | ✅ 일치 |
| `insert_edge()` 시그니처 | `(source_id, target_id, relation, description, strength)` | ✅ 일치 |
| `remember()` 반환값 | `{"node_id": int}` 항상 (duplicate 포함) | ✅ 일치 |
| `get_project()` bash 적용 | substring 매칭 → cmd 문자열에도 동작 | ✅ 가능 |

### 발견한 주의사항 (3건)

**1. `insert_edge()` 중복 방어 없음**
- 상태: UNIQUE 제약 없이 plain INSERT
- 위험: 같은 세션 재저장 시 edge 중복
- 판단: 세션 재저장은 드물고, `content_hash`가 노드 중복은 방어. **수용**

**2. "테스트"/"완료" 시그널 유지 필요**
- 상태: BASH_SIGNAL_MAP에서 제거하되 저장 트리거는 유지해야 함
- 해결: `BASH_TRIGGER_ONLY` 리스트 분리 → 타입은 Observation fallback. **구현 반영**

**3. save_session duplicate 노드 → edge 생성**
- 상태: `remember()` duplicate 반환 시에도 `node_id` 사용 가능
- 판단: edge 생성 로직에서 duplicate 무관하게 처리. **수용**

### 결론
> 설계 그대로 구현 가능. 블로커 없음.

---

## 2. 구현 후 E2E 검증

### 2-1. save_session 노드+edge 검증

```
session_id: e2e_test_2026_0311
nodes_created: {narrative: 1, decisions: 2, questions: 1, edges: 3}

DB edge 확인:
  #4458 → #4459 (contains, strength=0.9)  ← Narrative→Decision
  #4458 → #4460 (contains, strength=0.9)  ← Narrative→Decision
  #4458 → #4461 (contains, strength=0.8)  ← Narrative→Question
```

recall() 벡터 검색으로는 새 노드 미발견 (의미적 거리 > 임계값) — 이것이 Impl Review R1 Issue 1에서 발견한 문제 그 자체. 명시적 edge로 해결한 것이 정확.

### 2-2. RELATION_RULES 검증

```python
infer_relation("Narrative", 0, "Decision", 1) == "contains"  # ✅
infer_relation("Narrative", 0, "Question", 0) == "contains"  # ✅
infer_relation("Decision", 1, "Question", 0) == "led_to"     # ✅
```

### 2-3. auto_remember TYPE_MAP 검증 (9건)

| 입력 | 기대 타입 | 기대 confidence | 결과 |
|------|-----------|----------------|------|
| Write STATE.md | Decision | 0.70 | ✅ |
| Edit CLAUDE.md | Principle | 0.85 | ✅ |
| Edit KNOWLEDGE.md | Pattern | 0.75 | ✅ |
| Edit random.txt | None (스킵) | - | ✅ |
| Bash FAIL (mcp-memory) | Failure | 0.70, proj=mcp-memory | ✅ |
| Bash PASS (portfolio) | Experiment | 0.70, proj=portfolio | ✅ |
| Bash FAIL+PASS | Failure (우선) | - | ✅ |
| Bash "테스트" | Observation | 0.65 | ✅ |
| Bash ls | None (스킵) | - | ✅ |

### 2-4. 중복 방어 검증

같은 session_id로 재실행 → `content_hash` dedup 동작 확인.
새 summary는 새 Narrative 생성, 동일 Decision은 duplicate 반환.

### 2-5. 전체 테스트 스위트

169 unit tests — Phase 0, 1, 4 변경 후 모두 통과.

---

## 3. Phase 1.5 모니터링 1회차

ontology_review (2026-03-11):

| 지표 | 값 | 판단 |
|------|-----|------|
| 총 노드 | 4008 | 마이그레이션 후 증가 정상 |
| Observation 비율 | 3% (108/4008) | L0 일색 해소 |
| Decision | 631 (16%) | 마이그레이션 259개 추가 |
| Question | 213 (5%) | 마이그레이션 180개 추가 |
| Narrative | 240 (6%) | 마이그레이션 47개 추가 |
| 고립 노드 | 4% (167/4008) | 양호 |
| contains edge | 653 | 세션→노드 edge 대량 추가 |
| Unclassified | 38 (1%) | 대부분 라이선스/frontmatter 노이즈 |

**판단**: 정상. 다음 2~3세션에서 auto_remember 실시간 매칭 관찰 후 Phase 1.5 종료.
