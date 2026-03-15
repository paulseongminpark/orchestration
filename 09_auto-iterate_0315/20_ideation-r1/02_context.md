# Ideation R1 — Context
> 2026-03-15 | FROM: 11_research-merged

## FROM
11_research-merged (00_orchestrator-integration.md + 01_definitive-inventory.md)

## CONFIRMED DECISIONS
- autoresearch 3원칙 적용: 단일 수정 대상, 단일 메트릭, 고정 예산
- 구조 매핑: program.md + 설정 파일 + git keep/discard
- 메트릭 4종: M1(recall) M2(복구시간) M3(경로해결) M4(위반율)
- 첫 실험: M4 (규칙 위반율) — 측정 가장 용이

## CARRY FORWARD
- 수정 대상 인벤토리 (agents 15, skills 14+, hooks 14, rules 3)
- 측정 인프라 (hook exit code, mcp-memory API, index-system CLI)

## DO NOT CARRY
- autoresearch의 ML 세부사항 (GPU, PyTorch, BPE 등)
- val_bpb 직접 사용 (우리 메트릭으로 대체 완료)

## OPEN QUESTIONS
1. program.md 구체적 포맷?
2. iteration 내 agent 모델 — Sonnet vs Opus?
3. iteration 자동화 수준?
4. 안전장치 — git revert만으로 충분?
5. 첫 실험 대상 파일?

## REQUIRED INPUT FILES
- 11_research-merged/00_orchestrator-integration.md
- 11_research-merged/01_definitive-inventory.md

## ENTRY CONDITION
Research merged 완료 ✅
