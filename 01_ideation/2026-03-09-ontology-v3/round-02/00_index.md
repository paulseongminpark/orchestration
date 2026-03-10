# Ontology v3 Ideation — Round 2

> 날짜: 2026-03-10
> 기반: R1 4파일 + Phase 0 결과 (06_phase0-results.md)
> 목적: R1 방향을 **실데이터로 검증** + **설계 구체화**

---

## R1 → R2 변경점

| R1 제안 | Phase 0 실측 | R2 수정 |
|---------|-------------|---------|
| Workflow → Pattern/Tool 재분류 | 47% 일회성 태스크 → archived | Workflow deprecated, 6가지 재분류 |
| 타입 축소 신규 인프라 필요 | type_defs 테이블 이미 존재 (deprecated/replaced_by) | 기존 인프라 활용 |
| co-retrieval ~500-1000 pairs | 실측 1,160 pairs (≥3) | 예상보다 많음, min_co_count=5 검토 |
| retrieval_hints 신규 | Codex: classify→store→link 분리 완료 | classify에 hints 생성 추가 |

---

## 파일 구조

| # | 파일 | 상태 |
|---|------|------|
| 00 | 이 인덱스 | 완료 |
| 01 | type-migration-design.md | 완료 |
| 02 | agent-autonomy-l3.md | 완료 |
| 03 | co-retrieval-data.md | 완료 |
| 04 | dispatch-impl-spec.md | 완료 |
