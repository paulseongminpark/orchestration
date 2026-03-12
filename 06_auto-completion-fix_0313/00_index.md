<!-- pipeline: auto-completion-fix | type: full-impl | mode: lightweight | status: DONE -->
<!-- phase: implementation | updated: 2026-03-13T03:12 -->
<!-- current_task: done | next: — -->

# Auto-Completion Fix
> 시작: 2026-03-13 | 타입: full-impl (경량)

## 문제
Claude가 코드 구현 완료 후 Living Docs → 커밋 → push를 자동으로 이어가지 않음.
common-mistakes.md 체크리스트가 있지만 soft enforcement — 3/12~13 세션에서 최소 3회 재현.

## 해결
`pipeline-watch.py`에 역할 4 추가: 프로젝트 파일 N개 수정 후 STATE.md 미편집 시 리마인드.

## Phase 상태
| Phase | 폴더 | 상태 |
|---|---|---|
| Implementation | (inline) | 🔄 |

## Decisions
- 경량 파이프라인 — 단일 Phase, inline 구현
- threshold=3, cooldown=180s
- STATE.md 편집 시 dirty 클리어
- git commit 시 dirty 클리어
