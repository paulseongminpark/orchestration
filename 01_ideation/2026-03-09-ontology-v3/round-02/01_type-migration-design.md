# R2-01: 타입 마이그레이션 설계

> R1: 31→~15 Tier 계층. Phase 0: type_defs 이미 존재, Workflow 47% archived, deprecated 전환 확인.
> 이 문서: 실데이터 기반 구체적 마이그레이션 설계.

---

## 1. 실측 데이터

### 1-1. 현재 분포 (3,007 active 노드)

```
Tier 1 (핵심 7):    1,256개 (41.8%)
  Decision    334  ██████████████
  Insight     265  ███████████
  Principle   231  █████████
  Pattern     133  █████
  Goal        122  █████
  Failure     101  ████
  Experiment   70  ███

Tier 2 (맥락 5):      574개 (19.1%)
  Tool        154  ██████
  Framework   142  ██████
  Narrative   126  █████
  Project     121  █████
  Identity     31  █

Tier 3 (전환 3):       55개 (1.8%)
  Observation  39  ██
  Question     12  ▏
  Signal        4  ▏

폐기 대상 (15):     1,084개 (36.0%)
  Workflow    532  ██████████████████████
  Skill       128  █████
  SystemVersion 114  ████
  Agent       114  ████
  Conversation 66  ███
  Breakthrough  54  ██
  Evolution     25  █
  Connection    21  █
  Tension       16  █
  AntiPattern    5  ▏
  Preference     3  ▏
  Philosophy     2  ▏
  Value          2  ▏
  Belief         1  ▏
  Axiom          1  ▏
```

**Unclassified**: 38개 (계산 외)

### 1-2. type_defs 인프라

테이블 이미 존재 (51행). 핵심 컬럼:
```
name, layer, super_type, description, status, rank,
deprecated_reason, replaced_by, deprecated_at, version
```

→ `status='deprecated'` + `replaced_by='Pattern'` 식으로 점진 전환 가능.
→ **신규 테이블/컬럼 불필요.**

---

## 2. 마이그레이션 매핑

### 2-1. 폐기 타입 → 재분류 매핑

| 폐기 타입 | 개수 | 매핑 전략 | 대상 |
|----------|------|-----------|------|
| **Workflow** | 532 | LLM 배치 재분류 (0-2 결과 기반 6가지) | 47% archived, 23% Framework, 10% Pattern, 10% Goal, 7% Tool, 3% Experiment |
| **Skill** | 128 | → Tool (도구/능력) | Tool |
| **SystemVersion** | 114 | → Project (프로젝트 버전 기록) | Project |
| **Agent** | 114 | → Tool (도구) | Tool |
| **Conversation** | 66 | → Observation (일회성 관찰) | Observation |
| **Breakthrough** | 54 | → Insight (발견/깨달음) | Insight |
| **Evolution** | 25 | → edge temporal_chain으로 표현 | edge 전환 + archived |
| **Connection** | 21 | → edge로 표현 | edge 전환 + archived |
| **Tension** | 16 | → Question (미해결) | Question |
| **AntiPattern** | 5 | → Failure (실패 패턴) | Failure |
| **Preference** | 3 | → Identity | Identity |
| **Philosophy** | 2 | → Principle | Principle |
| **Value** | 2 | → Principle | Principle |
| **Belief** | 1 | → Principle | Principle |
| **Axiom** | 1 | → Principle | Principle |

### 2-2. 마이그레이션 단계

```
Step 1: 단순 매핑 (1:1, 즉시)
  Skill→Tool, Agent→Tool, SystemVersion→Project,
  Breakthrough→Insight, Conversation→Observation,
  Tension→Question, AntiPattern→Failure,
  Preference→Identity, Philosophy/Value/Belief/Axiom→Principle
  → 528개 노드, type_defs에 deprecated + replaced_by 설정

Step 2: Evolution/Connection → edge 전환
  각 노드의 content에서 관계 추출 → edge 생성 → 노드 archived
  → 46개 노드

Step 3: Workflow LLM 배치 재분류
  532개를 LLM으로 개별 판단 (gpt-5-mini)
  → ~250개 archived, ~120개 Framework, ~50개 Pattern, ~50개 Goal, ~35개 Tool, ~15개 Experiment, ~12개 기타
  → 예상 토큰: 532 × ~3K = ~1.6M (소형 풀 한도 내)

Step 4: Unclassified 38개 재분류
  Step 3과 동일 방식
```

### 2-3. type_defs 업데이트 SQL

```sql
-- Step 1: 단순 매핑 deprecate
UPDATE type_defs SET
  status = 'deprecated',
  deprecated_reason = 'v3 타입 축소: 1:1 매핑',
  replaced_by = 'Tool',
  deprecated_at = datetime('now'),
  version = version + 1
WHERE name IN ('Skill', 'Agent');

-- nodes 업데이트
UPDATE nodes SET type = 'Tool'
WHERE type IN ('Skill', 'Agent') AND status = 'active';

-- 반복: 각 매핑 그룹별
```

### 2-4. 롤백 전략

```sql
-- type_defs에 이전 매핑 기록이 남으므로 역전환 가능
UPDATE nodes SET type = td.name
FROM type_defs td
WHERE nodes.type = td.replaced_by
  AND td.deprecated_at > '2026-03-10'
  AND td.status = 'deprecated';
```

---

## 3. retrieval_hints 스키마

### 3-1. 저장 위치

**선택: nodes 테이블에 JSON 컬럼 추가**

```sql
ALTER TABLE nodes ADD COLUMN retrieval_hints TEXT DEFAULT NULL;
-- JSON: {"when_needed": "...", "related_queries": [...], "context_keys": [...]}
```

이유:
- 별도 테이블은 JOIN 비용
- JSON이면 유연 (필드 추가 용이)
- enrichment 파이프라인에서 E-NEW로 배치 생성 가능

### 3-2. 생성 시점

```
remember() → classify → store → [비동기 enrichment]
                                   ↓
                              E-NEW: retrieval_hints 생성
                              - when_needed: "이 기억이 필요한 상황"
                              - related_queries: 예상 검색어 3-5개
                              - context_keys: 맥락 키워드 3-5개
```

기존 3,007 노드: gpt-5-mini 배치 (Phase 5 Step 3)

### 3-3. 활용

```python
# enrichment 시 embedding_text에 포함
embedding_text = f"{content}\n{summary}\n{retrieval_hints['when_needed']}\n{' '.join(retrieval_hints['related_queries'])}"

# FTS5에 related_queries 포함
fts_text = f"{content} {' '.join(retrieval_hints.get('related_queries', []))}"
```

---

## 4. 결과 예측

| 마이그레이션 후 | Tier 1 | Tier 2 | Tier 3 | archived |
|----------------|--------|--------|--------|----------|
| 예상 노드 수 | ~1,600 | ~800 | ~120 | ~500 |
| 비율 | 53% | 27% | 4% | 17% |

검색 유효 노드: ~2,520 (현재 3,007 대비 84% — 16% archived 정리)

---

## 5. 미결

- [ ] Workflow LLM 재분류 프롬프트 설계 (정확도 검증 필요)
- [ ] archived 노드의 검색 제외 vs 낮은 가중치 결정
- [ ] retrieval_hints 생성 프롬프트 품질 기준
- [ ] type_defs 51행 중 v3에서 안 쓰는 타입 정리
