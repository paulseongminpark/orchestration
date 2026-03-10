# 06: Phase 0 결과 — R1 갭 보충

> 실행: 2026-03-10
> 목적: R1의 3가지 검증 부족 보충 → R2 심화 기반 확보

---

## 0-1: 80개 인사이트 필터링 (Codex 위임)

73개 파일 검토 → **16건** v3 직접 관련 추출.
전체 결과: `/c/dev/01_projects/06_mcp-memory/report-2026-03-10-1507-v3-insights-filter.md`

### R1이 놓친 핵심 6건

| # | 놓친 것 | 출처 | R2 반영 포인트 |
|---|---------|------|---------------|
| 1 | **type_defs 테이블** 기반 타입 관리 — 이미 v2.1에서 설계됨 | a-r2-13, d-r3-11 | 타입 축소 시 신규 인프라 불필요, type_defs 활용 |
| 2 | **deprecated + replaced_by** 전환 — 삭제가 아니라 자연 전환 | a-r1-4, a-r1-11 | 31→15 마이그레이션이 파괴적이 아닌 점진적 |
| 3 | **remember() classify→store→link 분리** — 이미 설계 완료 | a-r1-1, a-r2-14, a-r3-18 | 타입 변경 시 classify만 수정 |
| 4 | **RRF k=30 + RWR_SURPRISE_WEIGHT=0.05** 조합 | c-r1-4, c-r2-9 | retrieval 튜닝 파라미터 |
| 5 | **edge에 사용 맥락 재기록** (ctx_log, 최근 5개) | b-r1-5 | co-retrieval의 기반 데이터 |
| 6 | **patch foraging** (Marginal Value Theorem, 수확 체감 → 새 패치) | b-r1-4 | dispatch 컨텍스트화와 직결 |

### Codex 추출 전체 (16건 요약)

**Type (7건)**:
1. remember() 세 역할(분류/저장/연결) 분리 → Palantir 교훈: 파서와 트랜스폼 분리 (a-r1-1)
2. deprecated를 전제로 한 버전 관리 — Wikidata 3-rank, Gene Ontology replaced_by (a-r1-4)
3. 타입 축소는 삭제가 아니라 대체 매핑 기반 deprecate (a-r1-11)
4. validator도 type_defs를 읽어야 함 — schema.yaml 대체 (a-r2-13)
5. live DB를 타입 정본으로 쓰고 deprecated는 자동 교정 (d-r3-11)
6. 새 타입 추가 시 수정 지점을 classify 하나로 축소 (a-r2-14)
7. remember 파이프라인은 분리하되 외부 API는 100% 호환 유지 (a-r3-18)

**Retrieval / Co-Retrieval (7건)**:
8. retrieval 소스(vector/fts5/graph)를 로그로 남겨야 co-retrieval 판단 가능 (b-r1-2)
9. 기본 검색은 3-way hybrid (Vector + FTS5 + UCB Graph + RRF) (b-r3-14)
10. RRF k=30으로 상위 집중도 높임 (c-r1-4)
11. k=30이면 RWR_SURPRISE_WEIGHT=0.05로 낮춰야 안전 (c-r2-9)
12. retrieval은 호출 맥락을 edge에 재기록 — ctx_log 최근 5개 (b-r1-5)
13. 그래프 탐색은 SQL CTE로 가능 — NetworkX BFS 대체 (b-r2-11)
14. 그래프 비용은 TTL 캐시(5분) 후 SQL-only UCB로 전환 (b-r3-16)

**Autonomy / Dispatch (2건)**:
15. recall은 패치 포화 시 새 패치로 재검색 — Marginal Value Theorem (b-r1-4)
16. recall mode(auto/focus/dmn)는 쿼리 문맥에 따라 탐색 성격을 바꿈 (b-r3-15)

---

## 0-2: Workflow 30개 샘플 분석

DB에서 Workflow 타입 active 노드 30개 랜덤 추출 후 수동 분류.

### 결과

| 재분류 | 개수 | 비율 | 대표 예시 |
|--------|------|------|-----------|
| **archived** (일회성 태스크, 이미 실행됨) | 14 | 47% | #1102(디렉토리 생성), #3255(Page.tsx 통합), #1226(hook 설정) |
| **Framework** (설계 구조) | 7 | 23% | #851(데이터 흐름), #1352(체인 스펙), #3927(hook 설계) |
| **Pattern** (반복 절차) | 3 | 10% | #723(AI→Claude 절차), #1322(검증 체크리스트) |
| **Goal/Plan** (구현 계획) | 3 | 10% | #1255(구현 로드맵), #4142(파이프라인 계획) |
| **Tool** (도구/템플릿) | 2 | 7% | #1433(스크립트 로직), #2949(프롬프트 템플릿) |
| **Experiment** | 1 | 3% | #883(e2e 테스트 플랜) |

### R1 제안 수정

**R1**: "Workflow → Pattern/Tool로 재분류"
**실측**: Pattern/Tool은 17%에 불과. **47%가 일회성 태스크 → archived 대상**.

수정된 Workflow 처리 전략:
1. **47% archived**: Obsidian 인제스트된 구현 계획의 개별 스텝. 실행 완료 후 검색 가치 없음 → status='archived'
2. **23% → Framework**: 설계 구조, 아키텍처 문서
3. **10% → Pattern**: 반복 사용되는 절차
4. **10% → Goal**: 구현 계획, 로드맵
5. **7% → Tool**: 스크립트, 템플릿
6. **3% → Experiment**: 실험 계획

→ **Workflow 타입 자체를 deprecated하고 위 6개로 재분류** (R1의 "폐기 후보" 확인됨)

---

## 0-3: ZERO 10건 원인 분류

enrichment 배치 후에도 NDCG=0인 10건의 원인 분석.

### 결과

| 원인 | 쿼리 | 상세 |
|------|------|------|
| **goldset 오류 (deleted node)** | q057, q061 | 정답 노드 #102, #98이 deleted 상태 → #40, #1056으로 대체 완료 |
| **vocabulary mismatch** | q020, q025 | 추상적 쿼리("감법 설계의 조합", "마찰 최소화") vs 구체적 원칙 텍스트. retrieval_hints의 related_queries가 해결 가능 |
| **매칭 가능한데 ZERO** | q028, q054, q060, q063, q068, q069 | 노드 active, 내용 관련성 있음. verify.py가 hybrid_search raw(0.390) 사용 때문일 가능성. recall() composite(0.724) 기준이면 해결 가능성 |

### 원인별 해결 방향

- **goldset 오류 2건**: 즉시 수정 완료 (q057: #102→#40, q061: #98→#1056)
- **vocabulary mismatch 2건**: retrieval_hints.related_queries로 해결 (Phase 5 Step 2)
- **매칭 가능 6건**: verify.py → recall() 기반 전환 시 자연 해결 예상. 전환 전 recall()로 재측정하여 확인 필요

---

## R2 반영 사항 요약

| R2 주제 | Phase 0에서 발견된 반영 포인트 |
|---------|-------------------------------|
| **01 타입+인출** | type_defs 활용, deprecated+replaced_by 점진 전환, Workflow 47% archived, classify 분리 이미 완료 |
| **02 에이전트자율성** | patch foraging(수확 체감), classify→store→link 파이프라인 분리 |
| **03 co-retrieval** | edge ctx_log(사용 맥락 재기록), retrieval 소스 로그, RRF k=30+RWR 0.05 |
| **04 dispatch** | patch foraging 직결 (프로젝트 전환 로직), recall mode(auto/focus/dmn) |
| **NDCG 0.9** | goldset 2건 수정, vocabulary mismatch는 retrieval_hints로, 6건은 verify.py 전환으로 |
