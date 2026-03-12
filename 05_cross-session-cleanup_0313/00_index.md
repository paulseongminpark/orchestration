<!-- pipeline: cross-session-cleanup | type: custom | mode: lightweight | status: ACTIVE -->
<!-- phase: implementation | updated: 2026-03-13T02:30 -->
<!-- current_task: 전체 현황 파악 + 문제 분류 완료, Fixer 프롬프트 생성 중 | next: Fixer 실행 → 검증 → commit -->

# 05_cross-session-cleanup_0313 — 교차 세션 미커밋 정리

> 시작: 2026-03-13 | 타입: custom | 모드: 경량

## 목적

4개 병렬 Opus 세션의 미커밋 변경사항을 이 세션(Meta Orchestrator + Fixer 2대)에서 검증·수정·커밋한다.

## 세션 맵

| # | 세션 | 핵심 작업 | 커밋 상태 |
|---|---|---|---|
| 1 | User Guide | 11_user-guide 생성, ideation→impl merged | ❌ git repo 없음 |
| 2 | 새 작업 배치 가이드 | CLAUDE.md 계층+흐름도, orchestration 파이프라인 | ✅ 커밋+push 완료 |
| 3 | Lightweight pipeline | 경량 분기 로직 (hook/skill/rules) | ✅ 커밋 완료 |
| 4 | T1 + Living Docs | T1 phase-conditional 8파일 + dirty 마커 | ❌ 미커밋 10파일 |

## Phase 상태

| Phase | 상태 |
|---|---|
| 현황 파악 + 문제 분류 | ✅ |
| Fixer 프롬프트 생성 | 🔄 |
| Fixer 실행 | ⬜ |
| 검증 + commit | ⬜ |
| Living Docs 갱신 | ⬜ |

## 대상 Repo

| Repo | 미커밋 | 심각도 |
|---|---|---|
| 11_user-guide | **GIT REPO 없음**, 19파일 | CRITICAL |
| ~/.claude | 10파일, +176/-42 | HIGH |
| 08_documentation-system | 3파일, +64/-16 | HIGH |
| dev-vault | AGENTS.md | Medium |

## 문제 분류

### CRITICAL
- C1: 11_user-guide git repo 없음
- C2: ~/.claude 10파일 미커밋

### HIGH
- H1: 11_user-guide/STATE.md 오래됨 (impl R1 → 실제 impl merged)
- H2: 11_user-guide/CHANGELOG.md impl-merged 누락
- H3: 08/STATE.md lightweight 미반영
- H4: 08/CHANGELOG.md T1+lightweight 엔트리 없음
- H5: HOME.md에 user-guide 누락
- H6: user-guide 00_index.md type: ideation (실제 custom) + mode 필드 없음

### MEDIUM
- M1: dev-vault AGENTS.md 미커밋
- M2: Hook 교차 검증 미완

## Pane 분배

- **Fixer 1**: H1, H2, H5, H6 (11_user-guide 문서 + HOME.md)
- **Fixer 2**: M2, H3, H4 (Hook 검증 + 08 Living Docs)
- **Meta**: C1, C2, M1 (git init + commit 전체)

## Decisions

- D1: 경량 파이프라인으로 운영 (단일 Phase, 이 세션 안에서 완결)
- D2: portfolio/tech-review 미커밋은 범위 밖 (별도 세션)
- D3: Fixer는 수정만, git 금지 (커밋은 Meta에서만)
