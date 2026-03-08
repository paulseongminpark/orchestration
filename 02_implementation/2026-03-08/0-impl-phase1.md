# Phase 1: 토큰 해방

> 세션: Main (이 세션)
> 예상 시간: 1시간
> 전제: 없음 (즉시 시작 가능)

---

## P1-01: MEMORY.md IF-ELSE 분리

**목표**: MEMORY.md 200줄 → 80줄 포인터 + topic별 상세 파일

**태스크**:
- [ ] P1-01-a: MEMORY.md에서 topic별 분리 대상 식별
  - `tmux 설정` → memory/tmux.md
  - `Terminal: WezTerm` → memory/wezterm.md
  - `Hardware` → memory/hardware.md
  - `CLI 연동` → memory/cli.md
  - `mcp-memory` (54~64줄) → 이미 별도 관리 (STATE.md)
  - `MCP Memory (v2.0...)` (102~113줄) → memory/mcp-memory-legacy.md (또는 삭제)
  - `MCP 연결 현황` → memory/mcp-connections.md
  - `04_memory_export` → memory/memory-export.md
  - `Serena MCP` → memory/serena.md
  - `Tech Review 파이프라인` → memory/tech-review.md
  - `Portfolio` 관련 (87~100줄) → memory/portfolio.md
  - `Daily Memo` → memory/daily-memo.md
- [ ] P1-01-b: topic 파일 7~10개 생성 (memory/ 디렉토리에)
- [ ] P1-01-c: MEMORY.md를 80줄 이하 포인터로 축소
  - 각 topic에 대해 `→ 상세: memory/{topic}.md` 형태로 1줄 참조
  - 유지할 것: System Version, User Preferences, 교훈 (핵심만), 사고 방식
- [ ] P1-01-d: 검증 — MEMORY.md가 80줄 이하인지 `wc -l`

**소유 파일**: `~/.claude/projects/C--dev/memory/MEMORY.md`, `~/.claude/projects/C--dev/memory/*.md`

---

## P1-02: 캐시 순서 규칙 문서화

**목표**: 프롬프트 캐싱 규칙을 KNOWLEDGE.md에 추가

**태스크**:
- [ ] P1-02-a: KNOWLEDGE.md에 "프롬프트 캐싱 규칙" 섹션 추가
  ```
  ## 프롬프트 캐싱 (2026-03-08)
  - 순서: Static system prompt + Tools → CLAUDE.md → Session context → Messages
  - 금지: mid-session 도구 추가/제거, 모델 변경, 시스템 프롬프트 타임스탬프
  - <system-reminder>로 업데이트 (시스템 프롬프트 변경 대신)
  - defer_loading: auto 모드로 이미 활성 (55K→3-5K)
  - ENABLE_TOOL_SEARCH=auto (기본값, 추가 설정 불필요)
  ```
- [ ] P1-02-b: MEMORY.md에서 "55K 토큰 오버헤드" 관련 outdated 정보 정리 (이미 1건 수정됨, 나머지 확인)

---

## P1-03: Phase 1 검증

- [ ] P1-03-a: MEMORY.md 줄 수 ≤ 80
- [ ] P1-03-b: topic 파일 각각 존재 확인 (`ls memory/*.md`)
- [ ] P1-03-c: KNOWLEDGE.md에 캐싱 규칙 존재 확인
- [ ] P1-03-d: git commit "[orchestration] Phase 1: MEMORY.md 분리 + 캐시 규칙"
