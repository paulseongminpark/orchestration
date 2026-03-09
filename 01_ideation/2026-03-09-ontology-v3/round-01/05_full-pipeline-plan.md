# 05: Ontology v3 — 전체 파이프라인 계획

> 작성: 2026-03-09 S5
> 기반: R1 4개 파일 (01~04) + R1 갭 분석 + NDCG 목표 설정
> 5단계 파이프라인: Ideation(R1→R2→R3) → Impl Design → Impl Review → 구현 → Code Review

---

## Phase 0: R1 갭 보충 (R2 시작 전)

R2에서 건전한 심화를 하려면 R1 기반이 확실해야 한다.

R1의 주의할 부분:
- "80개 인사이트 통합"이라고 하지만, S4에서 실제로 읽은 건 `0-orchestrator-round3-final.md`(최종 통합 보고서) 위주. 73개 개별 파일을 전부 읽었을 가능성은 낮다.
- R1은 **방향 설정** 수준. 구체적 트레이드오프 검증은 아직 안 됨 (예: Tier1 7개가 정말 맞는지, Workflow 532개를 어디로 재분류하는지).

| # | 작업 | 방법 | 목적 |
|---|------|------|------|
| 0-1 | 80개 인사이트 중 v3 관련 필터링 | `0-orchestrator-round3-final.md`의 29 결정 + 4세션 개별 파일에서 타입/인출/자율성 관련만 추출 | R1이 놓친 인사이트 확인 |
| 0-2 | Workflow 532개 샘플 분석 | DB에서 Workflow 30개 랜덤 추출 → 실제로 Pattern/Tool/Procedure 중 뭔지 수동 분류 | Tier 매핑 실효성 검증 |
| 0-3 | ZERO 10건 원인 분류 | q020,q025,q028,q054,q057,q060,q061,q063,q068,q069 각각 goldset 오류 vs vocabulary mismatch vs 구조적 한계 | retrieval_hints가 진짜 해결하는지 |

**위임**: 0-1은 Codex에 위임 가능 (파일 대량 분석), 0-2/0-3은 직접 (DB 쿼리+판단)

---

## Phase 1: Ideation R2 (심화)

R1의 4개 주제를 **데이터로 검증 + 설계 구체화**. Phase 0 결과 반영.

| # | 주제 | R2에서 할 것 | R1 대비 심화 포인트 |
|---|------|-------------|-------------------|
| 01 | 타입 + 인출 | Tier1 7개에 실제 노드 매핑 테스트, retrieval_hints JSON 스키마 확정, 기존 노드 마이그레이션 전략 | R1은 "이렇게 하자"만. R2는 "실제 데이터로 되는지" |
| 02 | 에이전트 자율성 | L3 경계선 구체화 (3-05 사고 기준), 목표 인식 파이프라인 구현 설계, 토큰 비용 시뮬레이션 | R1은 프레임워크. R2는 안전한 L3 구현 경로 |
| 03 | co-retrieval | recall_log 실데이터로 co_count SQL 실행, 유효 pair 수 확인, CO_RETRIEVAL_WEIGHT 범위 결정 | R1은 추정(~500-1000). R2는 실측 |
| 04 | dispatch | orch-state 에이전트 프롬프트 초안, impl-index 자동 탐색 로직, 세션ID 구분 방안 | R1은 방안 선택. R2는 구현 스펙 |

---

## Phase 2: Ideation R3 (통합 + 결정)

| # | 작업 | 산출물 |
|---|------|--------|
| R3-1 | 4개 주제 간 의존성 정리 | 의존성 그래프 (01↔03 강결합, 02↔04 약결합) |
| R3-2 | 충돌 해결 | 타입 축소가 co-retrieval에 미치는 영향, L3 자율성과 dispatch 컨텍스트 중복 |
| R3-3 | 최종 결정 목록 | v2.1처럼 번호 매긴 확정 결정 (예: V3-01 ~ V3-NN) |
| R3-4 | 구현 우선순위 확정 | P1/P2/P3 + 의존 순서 |
| R3-5 | 리스크 평가 | 마이그레이션 실패 시 롤백, 3,435 노드 재분류 비용 |

**산출물**: `round-03/00_final-report.md` — 이것이 Impl Design의 입력.

---

## Phase 3: Impl Design (구현 설계)

R3 결정 기반으로 **코드 수준 설계**.

| # | 영역 | 설계 내용 |
|---|------|----------|
| D-1 | DB 스키마 | nodes 테이블 변경 (retrieval_hints 컬럼, type ENUM 축소), edges 테이블 (co_retrieval_count), 마이그레이션 SQL |
| D-2 | API 변경 | `remember(content, type, ..., retrieval_hints)` 시그니처, `recall(query, intent?)` 파라미터 |
| D-3 | enrichment 확장 | E-NEW: retrieval_hints 자동 생성, 기존 노드 배치 생성 |
| D-4 | 분류기 수정 | remember() 타입 분류: 31→~15 매핑 테이블, LLM 프롬프트 수정 |
| D-5 | co-retrieval | daily_enrich에 co_count 계산 추가, UCB traverse에 co-retrieval weight |
| D-6 | dispatch | orch-state 에이전트 프롬프트 + impl-index 탐색 로직 |
| D-7 | 테스트 계획 | goldset 확장, NDCG 기대치, 마이그레이션 검증 쿼리 |

---

## Phase 4: Impl Review (구현 리뷰)

| # | 리뷰어 | 초점 |
|---|--------|------|
| R1 | Codex (gpt-5.4) | D-1~D-5 스키마/API 변경 후방 호환성, 엣지 케이스 |
| R2 | Gemini | 전체 아키텍처 영향도, mcp-memory 기존 163 테스트와의 충돌 |
| R3 | 직접 | R1+R2 피드백 통합, 최종 설계 확정 |

---

## Phase 5: 구현 (코드)

의존 순서대로 4단계. 각 Step 완료 후 **code-reviewer → 테스트 → 커밋**.

```
Step 1: DB 스키마 + 마이그레이션
  → nodes.retrieval_hints 컬럼 (JSON)
  → type ENUM 축소 (하위 호환 유지, 기존 타입은 alias)
  → edges.co_retrieval_count 컬럼

Step 2: API + 분류기
  → remember() retrieval_hints 파라미터
  → recall() intent 파라미터 (optional, 기본=auto)
  → 타입 분류 프롬프트 31→~15

Step 3: enrichment + co-retrieval
  → E-NEW: retrieval_hints 배치 생성 (기존 3,435 노드)
  → co_count 계산 + edge boost
  → remember() 직후 비동기 enrichment

Step 4: dispatch + L2 강화
  → orch-state impl-index 탐색
  → session-start recall 강화
```

---

## Phase 6: Code Review + 검증

| # | 검증 | 기준 |
|---|------|------|
| 6-1 | 기존 테스트 163개 통과 | 0 regression |
| 6-2 | NDCG 측정 | 0.724 이상 유지 (하락 시 롤백) |
| 6-3 | 타입 마이그레이션 검증 | 3,435 노드 전수 → ~15개 타입 매핑 완료 |
| 6-4 | retrieval_hints 효과 | ZERO 10건 중 최소 5건 해소 |
| 6-5 | co-retrieval 효과 | A/B 테스트 — boost ON/OFF NDCG 비교 |

---

## 전체 타임라인

```
Phase 0 (R1 갭)     ─── 0-1은 Codex 병렬, 0-2/0-3은 직접
        ↓
Phase 1 (R2 심화)   ─── 4개 주제, Phase 0 결과 반영
        ↓
Phase 2 (R3 통합)   ─── 결정 확정, 우선순위
        ↓
Phase 3 (설계)      ─── 코드 수준 스펙
        ↓
Phase 4 (리뷰)      ─── Codex/Gemini/직접 3단
        ↓
Phase 5 (구현)      ─── Step 1→2→3→4 순서
        ↓
Phase 6 (검증)      ─── NDCG + 테스트 + A/B
```

---

## Also TODO: NDCG 목표 0.9 달성

현재 recall() NDCG@5 = 0.724. 목표: **0.9**.

0.724→0.9는 +24%p 개선이 필요하며, 이 계획의 여러 Phase가 기여한다:
- **retrieval_hints** (Phase 5 Step 1-2): 저장 시 인출 맥락 설계 → vocabulary mismatch 해소 → ZERO 10건 중 다수 해결 기대
- **co-retrieval edge boost** (Phase 5 Step 3): 공동 출현 패턴 학습 → 그래프 traverse 품질 개선
- **intent 기반 recall 분기** (Phase 5 Step 2): 질문/탐색/확인/회상별 최적 전략 → 정밀도 향상
- **타입 축소 + 재분류** (Phase 5 Step 2): 31→~15 타입으로 분류 정확도 상승 → type_filter 실효성 개선

추가로 필요할 수 있는 것: goldset 75→100+ 확장 (측정 신뢰도), embedding 모델 업그레이드 검토, composite scoring 가중치 재튜닝.
NDCG 0.9 달성 여부는 Phase 6에서 측정하고, 미달 시 개별 기여 요소를 A/B로 분리 측정하여 병목을 찾는다.
