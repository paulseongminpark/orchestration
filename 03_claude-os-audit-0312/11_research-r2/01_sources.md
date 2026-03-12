# Research R2: 온톨로지 + mcp-memory — 추출 결과
> 2026-03-12 | 직접 읽기 (25K tokens, Cascade 불필요)
> 캐시 활용: .ctx/gemini-ontology-analysis.md (2026-03-08)

## 현재 온톨로지 상태 (v3.0.0-rc, config.py 기준)

### 15 Active Types / 4 Layers
| Layer | 이름 | 타입 |
|---|---|---|
| L0 (surface) | 관찰/경험 | Observation, Narrative, Question |
| L1 (operational) | 행위/사건 | Decision, Experiment, Failure, Signal, Goal, Tool, Project |
| L2 (structural) | 개념/패턴 | Pattern, Insight, Framework |
| L3 (core) | 원칙/정체성 | Principle, Identity |
| Meta | - | Unclassified |

### 48 Relation Types (8 카테고리)
causal / structural / layer_movement / diff_tracking / semantic / perspective / temporal / cross_domain

### 핵심 승격 경로 (VALID_PROMOTIONS)
Observation → Signal → Pattern/Insight → Principle/Framework

---

## 설계 원본 vs 구현 비교

| 항목 | 원본 설계 (03-ontology-layer-design.md) | 현재 구현 (v3.0.0-rc) |
|---|---|---|
| 레이어 수 | 6 (L0~L5, Deleuze 영감) | 4 (L0~L3, 실용) |
| 타입 수 | 50+ | 15 (active) |
| 철학 타입 | Virtual, Line_of_Flight, Assemblage, Fold 등 | 없음 (미구현) |
| 분류 전략 | 2단계 (레이어→타입) | 직접 분류 (classifier.py) |

→ 의도적 단순화. Gemini 분석(2026-03-08) → v3.0.0 마이그레이션으로 51→15 축소.

---

## 08/09/10 ↔ 온톨로지 연결 매핑

| 시스템 | 연결 방식 | 실제 코드 통합 |
|---|---|---|
| 08 (pipeline decisions) | 파이프라인 완료 시 → remember() → Decision 노드 | ❌ 없음 (수동 호출) |
| 09 (cascade lens) | lens 축적 → remember() → Pattern/Insight 노드 | ❌ 없음 (명시적 호출) |
| 10 (index) | 에코시스템 구조 → 10은 mcp-memory와 별도 운영 | ❌ 없음 (설계: "분리 운영 후 연결") |
| Claude OS 훅 | auto_remember.py → FILE_TYPE_MAP/BASH_SIGNAL_MAP | ✅ 있음 (PostToolUse Hook) |

**핵심**: 통합은 auto_remember.py(훅 레벨)에서만 작동. 08/09/10 → mcp-memory 직접 연결 코드 없음.

---

## 신규 gap 포인트

| # | Gap | 위치 | 심각도 |
|---|---|---|---|
| G8 | MEMORY.md 버전 드리프트: "v2.2.1" 표기 vs 실제 STATE.md = v3.0.0-rc | ~/.claude/projects/.../MEMORY.md | Warning |
| G9 | Deleuze 철학 타입 (L4-L5: Virtual, Line_of_Flight 등) 미구현 | docs/03-ontology-layer-design.md vs config.py | Info (의도적) |
| G10 | 08/09/10 → mcp-memory 직접 코드 통합 없음. auto_remember.py만 작동 | 전체 시스템 | **핵심 설계 결정 미반영** |

---

## v3.0.0-rc 현황 요약
- 상태: Phase 5 Step 2.5~4 잔여 (re-embed, co-retrieval, dispatch, NDCG검증)
- Tests: 169/169 PASS
- Active nodes: ~2,947
- retrieval_hints: 99.3% 완료
- NDCG@5: 미측정 (Phase 6 예정, 목표 0.9)

---

## 다음: Research R3
- 대상: Claude OS 레이어 — ~/.claude/ (CLAUDE.md, rules/, skills/, hooks/)
- 목표: OS 설정이 08/09/10/온톨로지와 정합하는가
