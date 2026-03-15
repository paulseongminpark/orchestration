# Implementation R1 — Context
> 2026-03-15 | FROM: 21_ideation-merged

## FROM
21_ideation-merged (00_orchestrator-final.md + 01_confirmed-decisions.md)

## CONFIRMED DECISIONS
- 첫 실험 대상: validate_pipeline.py
- agent 모델: Sonnet
- iteration 10회 수동
- 판정: recall ≥ baseline AND precision > baseline → keep
- 기록: program.md 내 실험 로그 테이블

## CARRY FORWARD
- validate_pipeline.py 구조 (204줄, 12개 규칙 체크)
- program.md 포맷 (6섹션)
- 테스트 셋 4분류 (정상/위반/경계/오탐)

## DO NOT CARRY
- autoresearch ML 세부사항
- 반자동 루프 (Phase 1 수동 먼저)

## OPEN QUESTIONS
- 테스트 케이스 몇 개가 적정한가 (최소 20개?)

## REQUIRED INPUT FILES
- validate_pipeline.py (204줄)
- phase-rules.json

## ENTRY CONDITION
Ideation merged ✅ + foundation/ 3축 ✅
