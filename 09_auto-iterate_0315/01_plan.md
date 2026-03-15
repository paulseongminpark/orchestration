# Auto-Iterate Plan
> 확정: 2026-03-15

## 작업 목표
autoresearch의 "program.md → agent 수정 → 고정 예산 실행 → 단일 메트릭 → keep/discard" 루프를
우리 orchestration 시스템에 적용하여, 설정 파일을 자율적으로 개선하는 프레임워크 구축.

## 손실불가 기준
- 기존 시스템 안정성 (현재 동작하는 hook/agent/skill 깨뜨리지 않음)
- 모든 실험은 revertable (git 기반 keep/discard)
- 메트릭 측정은 자동화, 사람 개입 최소

## 대상 파일/범위
- 입력: autoresearch 레포 (program.md, train.py, prepare.py 구조)
- 출력: 우리 시스템용 auto-iterate 프레임워크
- 수정 대상 후보: agent/*.md, skills/*.md, hooks/*.py, rules/*.md

## Phase 분할
| Phase | 목표 | 라운드 |
|---|---|---|
| Research (10-19) | autoresearch 분석 + 메트릭 정의 + 매핑 | R1 |
| Ideation (20-29) | 적용 설계: program.md 구조, 실험 루프, 메트릭 수집 | R1-R2 |
| Implementation (30-39) | 프레임워크 구현 + 첫 실험 | R1 |
| Review (40-49) | 결과 검증 + 개선점 | R1 |

## Pane 분할
- 단일 Pane (B) — 설계 중심, 구현은 경량
