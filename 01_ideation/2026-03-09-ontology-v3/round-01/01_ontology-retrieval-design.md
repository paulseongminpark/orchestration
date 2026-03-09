# 01: 온톨로지 타입 진단 + 저장/인출 체계 설계

> v2.1 결정 기반, v2.2.1 운영 데이터 반영
> 핵심: "저장할 때 꺼낼 맥락을 함께 설계한다"

---

## 1. 현황 진단

### 1-1. 타입별 분포 (2026-03-09)

```
Workflow      532  ████████████████████  (15.5%)
Decision      326  ████████████         (9.5%)
Insight       264  ██████████           (7.7%)
Principle     231  █████████            (6.7%)
Tool          154  ██████               (4.5%)
Framework     142  █████                (4.1%)
Pattern       133  █████                (3.9%)
Skill         128  █████                (3.7%)
Narrative     126  █████                (3.7%)
Project       121  ████                 (3.5%)
Goal          120  ████                 (3.5%)
SystemVersion 114  ████                 (3.3%)
Agent         114  ████                 (3.3%)
Failure        99  ████                 (2.9%)
Experiment     70  ███                  (2.0%)
Conversation   66  ██                   (1.9%)
Breakthrough   54  ██                   (1.6%)
Unclassified   38  █                    (1.1%)
Observation    37  █                    (1.1%)
Identity       30  █                    (0.9%)
Evolution      25  █                    (0.7%)
Connection     21  █                    (0.6%)
Tension        16  █                    (0.5%)
Question       12  ▏                    (0.3%)
AntiPattern     5  ▏                    (0.1%)
Signal          4  ▏                    (0.1%)
Preference      3  ▏                    (0.1%)
Value           2  ▏                    (0.1%)
Philosophy      2  ▏                    (0.1%)
Belief          1  ▏                    (0.0%)
Axiom           1  ▏                    (0.0%)
```

총 3,435 active 노드, 31개 타입.

### 1-2. 문제

**A. 과잉 분류 (31개 → 실효 20개 미만)**
- Belief(1), Axiom(1), Philosophy(2), Value(2) → Principle에 흡수 가능
- Preference(3) → Identity에 흡수 가능
- Signal(4) → 승격 전 임시 타입이라 적은 게 정상
- Agent(114), SystemVersion(114) → Tool 또는 Project의 하위

**B. Workflow 과대 (532 = 15.5%)**
- remember() 분류기가 "~하는 방법"을 전부 Workflow로 태깅
- 실제로는 Procedure(절차), Habit(습관), Config(설정) 등이 혼재

**C. 분류 기준 모호**
- Insight vs Pattern: 구분 기준이 "반복 관찰 여부"인데, remember() 시점에 판단 불가
- Narrative vs Conversation: 사용자가 이야기한 건 Narrative? Conversation?

**D. 인출 시 타입의 실제 유용성**
- recall("에이전트 워크플로우") → Workflow, Tool, Agent, Skill 모두 후보
- type_filter 하나로는 의미적 구분 불가
- 타입이 많으면 기계적 분류만 가능, 의미적 분류는 안 됨

### 1-3. 핵심 통찰

> **타입은 저장 시 분류를 위한 것이 아니라, 인출 시 필터를 위한 것이어야 한다.**

v2.1 결정 C9 "What-Context-Needed": 노드를 저장할 때 "이 기억이 필요한 상황"을 함께 기록해야 한다.

---

## 2. 설계 방향

### 2-1. 타입 레이어 정리 (31 → 구조적 계층)

**Tier 1: 핵심 타입 (인출 필터로 실효)**
| 타입 | 의미 | 인출 시나리오 |
|------|------|---------------|
| Decision | 결정, 선택, 판단 | "~를 왜 이렇게 했지?" |
| Pattern | 반복 관찰된 패턴 | "~할 때 보통 어떻게 하지?" |
| Principle | 규칙, 원칙, 가치관 | "~에 대한 원칙이 뭐지?" |
| Failure | 실패, 실수, 교훈 | "~에서 뭘 잘못했지?" |
| Insight | 발견, 깨달음, 분석 | "~에 대해 뭘 알고 있지?" |
| Goal | 목표, 방향 | "지금 뭘 하려고 하지?" |
| Experiment | 실험, 시도 | "~를 시도해본 적 있나?" |

**Tier 2: 맥락 타입 (그래프 연결로 가치)**
| 타입 | 의미 | 인출 방식 |
|------|------|-----------|
| Project | 프로젝트 컨텍스트 | project 필터 |
| Tool | 도구, 기술 | 이름으로 직접 검색 |
| Framework | 설계 구조 | 아키텍처 질문 시 |
| Narrative | 사용자 이야기/서사 | get_becoming() 경유 |
| Identity | 사용자 정체성 | get_becoming() 경유 |

**Tier 3: 전환 타입 (생애주기)**
| 타입 | 의미 | 생애 |
|------|------|------|
| Signal | 미확인 관찰 | → Pattern/Principle로 승격 |
| Observation | 일회성 관찰 | → Signal로 승격 또는 소멸 |
| Question | 미해결 질문 | → Insight로 전환 또는 archived |

**폐기 후보**: Workflow(→ Pattern/Tool로 재분류), Conversation(→ Observation), Breakthrough(→ Insight), SystemVersion(→ Project), Agent(→ Tool), Skill(→ Tool), Connection(→ edge로 표현), Tension(→ Question), Evolution(→ edge temporal_chain), AntiPattern(→ Failure), Belief/Axiom/Philosophy/Value(→ Principle), Preference(→ Identity)

### 2-2. 저장 시 인출 맥락 설계

**현재**: `remember(content, type, tags, project)`
**제안**: `remember(content, type, tags, project, retrieval_hints)`

```python
retrieval_hints = {
    "when_needed": "에이전트 워크플로우 설계 시",  # 어떤 상황에서 꺼낼지
    "related_queries": ["에이전트 구조", "워크플로우 패턴"],  # 예상 검색어
    "context_keys": ["orchestration", "v4.0"],  # 맥락 키워드
}
```

이걸 별도 필드로 저장하면:
- enrichment 시 embedding_text에 retrieval_hints 포함 → 벡터 유사도 개선
- FTS5 인덱스에 related_queries 포함 → 텍스트 매칭 개선
- recall() 시 when_needed 매칭 → 맥락 기반 필터링

### 2-3. 인출 경로 재설계

**현재 인출 경로:**
```
recall(query) → hybrid_search(vector+FTS+UCB) → composite_scoring → 결과
```

**제안 인출 경로:**
```
recall(query, intent?)
  → intent 분류 (질문/탐색/확인/회상)
  → intent별 검색 전략 선택
    - 질문: "~뭐지?" → type_filter + vector
    - 탐색: "관련된 거 다 보여줘" → DMN mode + graph traverse
    - 확인: "~맞지?" → exact match + Correction 주입
    - 회상: "예전에 ~한 적 있지?" → temporal + Narrative
  → composite_scoring
  → 결과
```

v2.1 결정 #22의 mode(focus/auto/dmn)를 intent까지 확장.

---

## 3. 실측 데이터 기반 분석

### 3-1. enrichment 후 quality_score 분포

enrichment 166개 노드 후, quality_score 분포가 변화.
이전: 193개 unenriched (qs=0) → enrichment bias로 검색 밀림.
현재: 21개 unenriched 남음. NDCG 0.475→0.724.

**의미**: enrichment는 검색 품질의 핵심. 모든 노드가 enriched여야 공정한 검색 가능.
→ **규칙: remember() 후 즉시 E1-E5 enrichment (비동기)**

### 3-2. verify.py 0.390 vs recall() 0.724

- verify.py: hybrid_search() 직접 → raw RRF만
- recall(): composite_scoring + BCM/UCB 보너스 → 학습된 검색

**의미**: composite scoring이 검색 품질의 핵심 차별점 (+85% 개선).
→ verify.py를 recall() 기반으로 전환하면 진짜 NDCG 반영 가능.

### 3-3. ZERO 10건 분석

enrichment 후에도 ZERO인 10건: q020, q025, q028, q054, q057, q060, q061, q063, q068, q069
→ 이것들은 goldset 오류이거나, 근본적 vocabulary mismatch.
→ retrieval_hints가 있었다면 해결 가능한 케이스 다수.

---

## 4. 구현 우선순위

| # | 작업 | 영향도 | 복잡도 | 우선 |
|---|------|--------|--------|------|
| 1 | 타입 계층 정리 (31→~15) | 높음 | 중간 | P1 |
| 2 | retrieval_hints 필드 추가 | 높음 | 높음 | P1 |
| 3 | remember() 직후 비동기 enrichment | 중간 | 낮음 | P1 |
| 4 | intent 기반 recall 분기 | 높음 | 높음 | P2 |
| 5 | verify.py → recall() 기반 전환 | 낮음 | 낮음 | P2 |
| 6 | 기존 3,435 노드 재분류 배치 | 중간 | 높음 | P3 |

---

## 5. 미결

- [ ] retrieval_hints 스키마 확정 (JSON 필드? 별도 테이블?)
- [ ] 기존 노드 retrieval_hints 생성 (enrichment 파이프라인 확장?)
- [ ] 타입 폐기 시 기존 노드 마이그레이션 전략
- [ ] intent 분류기 구현 방법 (규칙 기반? LLM?)
