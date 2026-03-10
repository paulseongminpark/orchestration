# 구현 인덱스 — 0309 세션 2 (Orchestration + Ontology + mcp-memory)

> compact 후 이 파일만 읽고 이어서 진행한다.
> 이전 세션: 0309 세션 1 (Pre-flight Recall 확립, work-log-0309.md 참조)
> 0308 메인 인덱스: 02_implementation/2026-03-08/0-impl-index.md

---

## 세션 스코프

orchestration + ontology + mcp-memory만. portfolio/tech-review 제외.

---

## Track A: Memory-Merger 구현 (Phase 3-04)

> 설계 완료: 0-design-memory-merger.md
> 의존성: mcp-memory v2.2.1+ (get_becoming, promote_node)

| # | 태스크 | 상태 | 파일 |
|---|--------|------|------|
| A1 | session-start.sh에 get_becoming 알림 추가 | [ ] | ~/.claude/hooks/session-start.sh |
| A2 | /merge 스킬 생성 (Present→Promote→Merge→Record) | [ ] | ~/.claude/skills/merge/SKILL.md |
| A3 | KNOWLEDGE.md 병합 로직 (도메인→섹션 매핑 + 중복 체크) | [ ] | 스킬 내 로직 |
| A4 | 실제 Signal 1건 승격 테스트 → KNOWLEDGE.md 반영 확인 | [ ] | KNOWLEDGE.md |

## Track B: Codex/Gemini CLI 전략 수립

> 긴급 TODO 항목. 현재 제약사항 정리 → 역할 매트릭스 확정.
> ref: mcp-memory #4323, #4324

| # | 태스크 | 상태 | 파일 |
|---|--------|------|------|
| B1 | 현재 제약 조건 정리 (실측 기반) | [x] | 0-cli-strategy.md |
| B2 | 역할 매트릭스 설계 (작업→CLI 매핑) | [x] | 0-cli-strategy.md |
| B3 | CLAUDE.md + delegate-to-codex 스킬 업데이트 | [x] | 규칙 파일들 |

## Track C: Ontology 실전 검증

> Pre-flight Recall 실전 + 승격 파이프라인 e2e 테스트

| # | 태스크 | 상태 | 파일 |
|---|--------|------|------|
| C1 | get_becoming으로 현재 승격 후보 확인 | [ ] | — |
| C2 | analyze_signals로 클러스터 분석 | [ ] | — |
| C3 | Memory-Merger e2e: Signal→Pattern 1건 승격+파일 반영 | [ ] | = A4와 동일 |
| C4 | NDCG 수치 차이 원인 확인 (STATE.md 0.460 vs 측정 0.353) | [x] | goldset 50→75개 차이. STATE.md 수정. |

---

## 실행 순서

```
[1] Track B (CLI 전략) — ideation, 짧은 리서치
[2] Track A (Memory-Merger) — 구현, 가장 큰 블록
[3] Track C (Ontology 검증) — A 완료 후 e2e 테스트
```

Track A와 C3는 동일 태스크 (Memory-Merger 검증 = 승격 e2e).

---

## 현재 상태 (compact 후 이 섹션 먼저 확인)

**세션 7 완료. Phase 5 Step 0~2 구현, hints 배치 백그라운드 실행 중.**

완료:
- [x] Track A~C, S3~S6 (이전 세션 — 상세 생략)
- [x] S7: Impl Design v2 작성 (02_impl-design-v2.md, 15건 피드백 반영)
- [x] S7: Step 0 — classifier.py import 복구, recall_id, edges index, retrieval_hints 컬럼
- [x] S7: Step 1 — DB 백업 + sync_schema C1 fix + 전타입 마이그레이션 (506 merge + 46 edge, leaked=0)
- [x] S7: Step 1.5 — PROMOTE_LAYER/RELATION_RULES/VALID_PROMOTIONS v3 + 테스트 적응 (169 pass)
- [x] S7: Step 2 코드 — classifier 15개 프롬프트, Workflow 532개 재분류(61 archived), hints plumbing, type_filter canonicalization
- [x] S7: Step 3 코드 준비 — co_retrieval.py, type_filter canonicalization

미결:
- [~] **hints 배치** 실행 중 (task bc9ebakoj, ~100/2947 시점에서 세션 종료). 완료 확인 필요.
- [ ] Step 2.5: ChromaDB re-embed (hints 완료 후)
- [ ] Step 3: co-retrieval 실행 (co_retrieval.py 준비 완료)
- [ ] Step 4: dispatch + L3 자율성
- [ ] Phase 6: NDCG 0.9 검증
- [ ] edges co_retrieval_count/boost 컬럼 추가 (라이브 DB)
- [ ] schema.yaml v3 업데이트 (deprecated 타입 제거)

gpt-5-mini 참고:
- reasoning 모델 — max_completion_tokens 크게 (2000+), temperature/max_tokens 미지원
- 배치 20개/호출 최적 (reasoning tokens 포함 ~3000-6000 토큰/배치)

수정 파일 (mcp-memory, 미커밋):
- ontology/validators.py: get_valid_node_types() 추가
- storage/sqlite_store.py: retrieval_hints 컬럼, recall_id 마이그레이션, sync_schema C1 fix, insert_node hints 파라미터
- tools/recall.py: recall_id 생성, type_filter canonicalization (H1)
- tools/remember.py: retrieval_hints 체인 (server→remember→store→insert_node)
- server.py: remember() retrieval_hints 파라미터
- enrichment/classifier.py: v3 15개 타입 프롬프트
- config.py: PROMOTE_LAYER/RELATION_RULES/VALID_PROMOTIONS v3
- tests/: test_correction, test_remember_v2, test_schema_consistency 적응
- scripts/migrate_v3.py (신규): Step 1 마이그레이션
- scripts/migrate_workflow.py (신규): Workflow LLM 재분류
- scripts/enrich/hints_generator.py (신규): retrieval_hints 배치 생성
- scripts/enrich/co_retrieval.py (신규): co-retrieval 계산

---

---
