<!-- pipeline: work-placement-guide | type: ideation | mode: lightweight | status: DONE -->
<!-- phase: ideation | updated: 2026-03-13T00:30 -->
<!-- current_task: 산출물 CLAUDE.md 반영 완료 | next: index-system 인프라 통합 (별도) -->

# work-placement-guide
> 시작: 2026-03-13 | 타입: ideation (경량) | 이동: 08 → 01 (scope 검증 결과)

## 목표
- "독립 프로젝트란 무엇인가" 정의
- 새 작업 배치 판단 흐름도 + 생성 절차 수립
- 각 프로젝트 scope 정의 → CLAUDE.md 반영

## Phase 상태
| Phase | 폴더 | 상태 |
|---|---|---|
| Ideation R1 | 20_ideation-r1/ | 🔄 |

## Current
- ✅ 산출물 반영 완료: CLAUDE.md scope + 흐름도 + 생성 절차
- DONE gate 미통과 (경량 파이프라인, review-merged/90_output 생략)

## Decisions
- D1: ~~08에 넣는 게 맞다~~ → 01_orchestration이 맞다 (scope 검증으로 번복)
- D2: 독립 프로젝트 기준 3줄: (1) 독립 산출물 (2) 자체 생명주기 (3) 목적 종속 ≠ 구조 종속
- D3: 판단 흐름도: Q1(독립 산출물) → Q2(기존 scope 범위 안?) → Q3(기존 프로젝트 없이 존재 가능?)
- D4: 불확실하면 사용자에게 묻는다 (이전 클로드의 실수: 확신 없이 혼자 결정)
- D5: OS 비유 — orchestration=커널, 06/08/09/10=서비스, 나머지=앱
- D6: CLAUDE.md 프로젝트 scope 구체화 필수 (현재 "시스템 설정" 같은 모호한 설명이 원인)
- D7: index-system gap — 스킬이 아닌 인프라로 별도 진행 (node #5020)
- D8: 가이드 이름 변경: "프로젝트 생성 가이드" → "새 작업 배치 가이드"
