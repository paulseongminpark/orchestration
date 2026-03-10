# Ontology v3 — R3 최종 통합 보고서

> 날짜: 2026-03-10
> 입력: R1 (방향 설정, 4파일) + Phase 0 (갭 보충, 16 인사이트 + 실측) + R2 (데이터 검증 + 설계 구체화, 4파일)
> 출력: 확정 결정 목록 + 구현 우선순위 + 리스크 평가
> 이 문서가 Phase 3 (Impl Design)의 입력.

---

## 1. 의존성 그래프

```
01 타입 마이그레이션 ──────────────────┐
  │                                    │
  │ type_defs deprecated               │ 타입 축소 → co-retrieval 재계산 필요
  │ retrieval_hints 컬럼 추가           │
  │                                    ▼
  │                              03 co-retrieval
  │                                │
  │ recall 품질 = L3 품질            │ co-retrieval → NDCG 개선
  ▼                                ▼
02 에이전트 자율성 ◄──── NDCG 0.9 ────┘
  │
  │ 세션 목표 자동 구성
  ▼
04 dispatch 컨텍스트화
```

**강결합**: 01 → 03 (타입 축소가 co-retrieval 데이터를 무효화)
**약결합**: 02 ↔ 04 (세션 목표 vs 세션 컨텍스트, 보완적)
**독립**: 04는 DB 변경 불필요 (에이전트 프롬프트 수정만)

---

## 2. 충돌 해결

### 충돌 1: 타입 축소 → co-retrieval 데이터 무효화

Workflow(532개)가 co-retrieval top pairs의 허브. 47% archived되면 현재 co-occurrence 데이터가 왜곡.

**해결**: 타입 마이그레이션(01) 완료 후 co-retrieval(03) 재계산.
순서: Step 1→2→3(01) → co-retrieval 재계산(03).

### 충돌 2: L3 recall 증가 vs dispatch 토큰 절약

L3는 recall 횟수 증가(+800 토큰), dispatch는 컨텍스트 축소(impl-index만).

**해결**: 충돌 아님. L3 recall은 세션 시작 1회. dispatch는 출력 범위 축소. 양립 가능.
총 추가 비용: ~800 토큰/세션 (200K 대비 0.4%).

### 충돌 3: archived 노드의 검색 처리

47% Workflow가 archived되면, 이 노드들이 검색에서 어떻게 되는가?

**해결**: `status='archived'` 노드는 hybrid_search에서 제외.
검색 대상: active 노드만 (~2,520개). 검색 공간 16% 축소 → 정밀도 개선 기대.

---

## 3. 확정 결정 목록

### 타입 체계 (V3-01 ~ V3-06)

| ID | 결정 | 근거 |
|----|------|------|
| **V3-01** | 31개 타입 → 15개 (Tier1: 7 + Tier2: 5 + Tier3: 3) | R2-01 실측: 폐기 대상 1,084개(36%), type_defs deprecated 인프라 이미 존재 |
| **V3-02** | 폐기는 삭제가 아닌 deprecated + replaced_by 점진 전환 | Phase 0 Codex: a-r1-4 Wikidata 3-rank 패턴 |
| **V3-03** | Workflow 532개: LLM 배치 재분류 (47% archived, 나머지 5개 타입 분배) | R2-01 Phase 0-2 샘플 실측 |
| **V3-04** | 단순 1:1 매핑 우선 실행 (Skill→Tool, Agent→Tool 등 528개) | 리스크 최소, 즉시 실행 가능 |
| **V3-05** | retrieval_hints는 nodes 테이블 JSON 컬럼 | R2-01: JOIN 비용 회피, 유연성 |
| **V3-06** | retrieval_hints 생성은 enrichment E-NEW로 배치 | R2-01: 기존 파이프라인 확장, 3,007개 배치 |

### 검색 고도화 (V3-07 ~ V3-10)

| ID | 결정 | 근거 |
|----|------|------|
| **V3-07** | co-retrieval min_co_count=5 (338 pairs) | R2-03 실측: ≥3은 1,160(과다), ≥10은 49(과소) |
| **V3-08** | 허브 노드(degree centrality 상위 5%) pair는 co-retrieval boost 제외 | R2-03: top pairs 전부 허브 조합, 의미 없는 boost 방지 |
| **V3-09** | CO_RETRIEVAL_WEIGHT: 선형 스케일 min(0.1*(co_count-4), 0.5) | R2-03: co_count=5→0.1, co_count=10→0.5 |
| **V3-10** | edges 테이블에 co_retrieval_count + co_retrieval_boost 컬럼 추가 | R2-03: 기존 edge 구조에 자연 통합 |

### 에이전트 자율성 (V3-11 ~ V3-13)

| ID | 결정 | 근거 |
|----|------|------|
| **V3-11** | L3 경계: 추론은 자유, 실행은 제안 (코드 수정/커밋은 항상 사용자 승인) | R2-02: 3-05 사고 교훈. L5 시도 → 사고 |
| **V3-12** | 세션 목표 자동 구성: dispatch + recall 결합 (Pre-flight Recall 확장) | R2-02: 이미 부분 구현, +800 토큰(0.4%) |
| **V3-13** | 목표 충돌 우선순위: 사용자 명시 지시 > 프로젝트 목표 > 과거 패턴 | R2-02: 명시적 hierarchy 필요 |

### dispatch 컨텍스트화 (V3-14 ~ V3-16)

| ID | 결정 | 근거 |
|----|------|------|
| **V3-14** | /dispatch 3단계: impl-index → 프로젝트 필터 → 전체 fallback | R2-04: 추가 인프라 불필요, 기존 패턴 활용 |
| **V3-15** | impl-index 탐색 범위: 3일 이내 | R2-04: 대부분 1-2일 내 이어감 |
| **V3-16** | session-start.sh에 impl-index 존재 알림 추가 | R2-04: "📋 이전 작업 인덱스" 표시 |

### NDCG (V3-17)

| ID | 결정 | 근거 |
|----|------|------|
| **V3-17** | NDCG 목표 0.9. 미달 시 A/B로 병목 분리 측정 | S5 설정: retrieval_hints + co-retrieval + intent + 타입축소 합산 |

**총 17개 결정.**

---

## 4. 구현 우선순위

### P1: 즉시 (DB + API)

```
V3-04  단순 1:1 타입 매핑 (528개 노드)
V3-05  retrieval_hints JSON 컬럼 추가
V3-10  edges에 co-retrieval 컬럼 추가
V3-16  session-start.sh impl-index 알림
```

**의존성 없음. 병렬 실행 가능. 리스크 최소.**

### P2: 단기 (마이그레이션 + 배치)

```
V3-01  type_defs deprecated 설정 (15개 폐기 타입)
V3-02  deprecated + replaced_by 반영
V3-03  Workflow LLM 배치 재분류 (532개, ~1.6M tokens)
V3-06  retrieval_hints E-NEW 배치 생성 (~3,007개)
```

**V3-04 완료 후. Workflow 재분류는 토큰 비용 있음.**

### P3: 중기 (검색 + dispatch)

```
V3-07  co-retrieval 계산 (타입 마이그레이션 완료 후)
V3-08  허브 노드 필터링
V3-09  CO_RETRIEVAL_WEIGHT 적용
V3-14  orch-state 에이전트 프롬프트 v2
V3-15  impl-index 3일 탐색 로직
```

**V3-03 완료 후. co-retrieval은 타입 축소 반영 필요.**

### P4: 장기 (자율성)

```
V3-11  L3 안전 장치 코드화
V3-12  세션 목표 자동 구성
V3-13  목표 충돌 우선순위 구현
V3-17  NDCG 0.9 달성 검증 + A/B 테스트
```

**P1-P3 완료 후. recall 품질 개선이 전제.**

---

## 5. 구현 순서 (의존성 반영)

```
Phase 5 Step 1 (P1, 병렬):
  ├─ V3-04: 단순 타입 매핑 528개
  ├─ V3-05: nodes.retrieval_hints 컬럼
  ├─ V3-10: edges.co_retrieval_count/boost 컬럼
  └─ V3-16: session-start.sh 수정

Phase 5 Step 2 (P2, 순차):
  V3-01/02: type_defs deprecated 설정
  → V3-03: Workflow LLM 배치 (gpt-5-mini, ~1.6M tokens)
  → V3-06: retrieval_hints E-NEW 배치 (~3,007개)

Phase 5 Step 3 (P3, V3-03 이후):
  V3-07/08/09: co-retrieval 계산 + 허브 필터 + weight
  V3-14/15: dispatch orch-state 수정

Phase 5 Step 4 (P4, 점진):
  V3-11/12/13: L3 자율성
  V3-17: NDCG 0.9 검증
```

---

## 6. 리스크 평가

| 리스크 | 영향 | 확률 | 대응 |
|--------|------|------|------|
| Workflow LLM 재분류 정확도 낮음 | 잘못된 타입 배정 → 검색 품질 저하 | 중 | 30개 샘플 정확도 측정 후 배치 (Phase 0-2 데이터 활용) |
| 타입 축소 후 NDCG 하락 | 타입 기반 필터 깨짐 | 낮 | deprecated는 alias 유지 — 기존 쿼리 호환 |
| co-retrieval 허브 편향 잔존 | boost가 일반 노드에 도움 안 됨 | 중 | percentile 튜닝 (95%→90% 조정 가능) |
| 3,007개 retrieval_hints 배치 비용 | ~9M tokens (소형 풀 4일분) | 낮 | 일 2.25M 한도 → 4일 분산 실행 |
| L3 잘못된 추론 | 불필요한 행동 제안 | 중 | L3 = 제안만, 실행은 사용자 승인 (V3-11) |
| impl-index 작성 규율 이탈 | dispatch 컨텍스트 없음 → 전체 모드 fallback | 중 | compact 규칙에 이미 포함 (common-mistakes.md) |

### 롤백 전략

```
타입 마이그레이션 롤백:
  → type_defs에 deprecated_at 기록 → 해당 시점 이후 변경만 역전
  → nodes.type을 이전 값으로 복원 (type_defs.name 기준)

co-retrieval 롤백:
  → edges.co_retrieval_boost = 0.0 으로 리셋 (UCB에서 무시됨)

retrieval_hints 롤백:
  → nodes.retrieval_hints = NULL (enrichment에서 무시됨)
```

모든 변경이 **additive** (기존 데이터 삭제 없음) → 롤백 안전.

---

## 7. 성공 기준

| 지표 | 현재 | 목표 | 측정 시점 |
|------|------|------|-----------|
| NDCG@5 (recall) | 0.724 | 0.9 | Phase 6 |
| 활성 타입 수 | 31 | 15 | Step 2 완료 후 |
| 검색 대상 노드 | 3,007 | ~2,520 | Step 2 완료 후 |
| co-retrieval pairs (≥5) | 338 | 재측정 | Step 3 완료 후 |
| ZERO 쿼리 수 | 10/75 | ≤3/75 | Phase 6 |
| 기존 테스트 | 163 pass | 163 pass | 매 Step 후 |

---

## 8. v2.1과의 차이

| | v2.1 | v3 |
|---|------|------|
| 타입 | 31개, 평면 | 15개, Tier 1/2/3 계층 |
| 저장 | content + type + tags | + retrieval_hints (인출 맥락) |
| 검색 | hybrid + composite | + co-retrieval + intent 분기 |
| 에이전트 | L1 규칙 기반 | L3 목표 추론 (제안 한정) |
| dispatch | 전체 STATE.md | 세션 컨텍스트 (impl-index) |
| NDCG | 0.724 | 목표 0.9 |
