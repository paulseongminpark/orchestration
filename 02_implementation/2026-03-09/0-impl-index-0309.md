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

**세션 6 완료. 다음: Impl Design v2 (Codex/Gemini 피드백 반영) → Phase 5 구현.**

완료:
- [x] Track A: Memory-Merger 구현 + CX 리뷰 + 수정 (aa0a66b, 3c47dd5)
- [x] Track B: CLI 전략 문서 + CLAUDE.md/스킬 업데이트 (0662ca6)
- [x] Track C: NDCG 수치 차이 확인 (goldset 50→75개, STATE.md 수정)
- [x] S3: CLI 플래그 실측 (Codex/Gemini, c129620)
- [x] S3: goldset 5건 수정 + typed vector 동적 가중치 → NDCG 0.459→0.475 (f81d55f)
- [x] S3: enrichment bias 발견 + 분석 (bc2bdee)
- [x] S4: Enrichment 배치 166개 (gpt-5-mini, 1.44M tokens, err=0)
- [x] S4: NDCG 0.475→0.724 (+52%) — q059/q073 ZERO 해소
- [x] S4: verify.py vs recall() 차이 원인 확인 (hybrid_search=0.390 vs recall+composite=0.724)
- [x] S4: OpenAI 무료 토큰 정보 기록 (#4376 + MEMORY.md)
- [x] S4: STATE.md 갱신 + push (39f6e6f)
- [x] S4: Ontology v3 Ideation R1 (4개 파일)
- [x] S5: 전체 파이프라인 계획 문서화 (05_full-pipeline-plan.md)
- [x] S5: NDCG 0.9 목표 설정 + 달성 전략 정리
- [x] S5: R1 갭 분석 (80개 인사이트 미교차검증, Workflow 샘플 미검증)
- [x] S6: Phase 0 완료 (Codex 16건 추출, Workflow 47% archived, ZERO 10건 분류, goldset 2건 수정)
- [x] S6: Phase 1 R2 완료 (4파일: 타입마이그레이션/L3자율성/co-retrieval실측/dispatch스펙)
- [x] S6: Phase 2 R3 완료 (17개 결정 V3-01~V3-17, 구현 우선순위 P1~P4)
- [x] S6: Phase 3 Impl Design 완료 (D-1~D-7 코드 수준 스펙)
- [x] S6: Phase 4 Impl Review — Codex Critical 3/High 4/Medium 4, Gemini 4건

미결:
- [x] Phase 0: R1 갭 보충 완료
- [x] Phase 1: Ideation R2 심화 완료
- [x] Phase 2: Ideation R3 통합 완료 (17개 결정)
- [x] Phase 3: Impl Design 완료
- [x] Phase 4: Impl Review 완료 (Critical 3건 발견 — 설계 수정 필요)
- [ ] **Impl Design v2**: Codex/Gemini 피드백 반영 (Critical 3 + High 4 + Gemini 4)
- [ ] **51개 전타입 매핑표**: 누락 20개 타입 경로 확정
- [ ] **classifier.py import 복구**: 선행 작업
- [ ] Phase 5: 구현 (Step 1~4)
- [ ] Phase 6: 검증 (NDCG 0.9 목표, 테스트, A/B)
- [ ] 21개 unenriched 노드 남음

---
