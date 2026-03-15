<!-- pipeline: auto-iterate | type: custom | mode: standard | status: DONE -->
<!-- phase: output | updated: 2026-03-16T00:40 -->
<!-- current_task: 완료 | next: handoff 항목 실행 -->

# Auto-Iterate
> 시작: 2026-03-15 | 완료: 2026-03-16 | 타입: custom (research → ideation → impl → review)

## 목표
Andrej Karpathy의 autoresearch 방법론을 우리 시스템에 현실적으로 적용.
측정 자동 + 수정 세션 + Opus 소비 0.

## Phase 상태
| Phase | 폴더 | 상태 |
|---|---|---|
| Research | `10_research-r1/`, `11_research-merged/` | ✅ |
| Ideation | `20~22/`, `23_ideation-merged/` | ✅ |
| Implementation | `30_impl-r1/`, `31_impl-merged/` | ✅ |
| Review | `40_review-r1/`, `41_review-merged/` | ✅ |
| Output | `90_output/` | ✅ |

## 산출물
- `12_auto-iterate/src/measure.py` — 시스템 건강 측정 (10체크, 70/100)
- `30_impl-r1/test_pipeline_rules.py` — hook 테스트 (37 scenarios, F1=1.0)
- `validate_pipeline.py` — bootstrap exempt 수정 4곳
- 확정 결정 10개, 전체 원자 분해 (11섹터, ~450항목)

## Decisions
- 측정 자동, 수정은 세션에서 (무인 수정 금지)
- Opus 소비 0. measure.py = 스크립트, iterate = Sonnet
- 테스트는 실제 경험에서만 (합성 금지)
- 인터페이스 불변 (이름, 구조, 경로)
- 3계층: 즉시(변경 시) + 매일(health) + 주간(drift)
