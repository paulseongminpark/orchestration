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
| C4 | NDCG 수치 차이 원인 확인 (STATE.md 0.460 vs 측정 0.353) | [ ] | — |

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

**현재: Track A(Memory-Merger S4+S5) 완료, Track B(CLI 전략) 완료. Track C 시작 대기.**

완료:
- [x] Track A: Memory-Merger 구현 + CX 리뷰 + 수정 (aa0a66b, 3c47dd5)
- [x] Track B: CLI 전략 문서 + CLAUDE.md/스킬 업데이트
- [ ] Track C: Ontology 검증 (NDCG 수치 차이 확인 남음)

---
