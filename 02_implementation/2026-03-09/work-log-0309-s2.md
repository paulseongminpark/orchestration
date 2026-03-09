# Work Log — 2026-03-09 세션 2

> 테마: Memory-Merger 구현 + CLI 전략 + Ontology 검증
> 세션: Main (WezTerm, Opus 4.6)
> 시작: ~14:00 KST

---

## 1. 세션 목표

orchestration + ontology + mcp-memory 집중. portfolio/tech-review 제외.
- Track A: Memory-Merger 구현 (Phase 3-04)
- Track B: Codex/Gemini CLI 전략 수립
- Track C: Ontology 실전 검증

## 2. 전역 규칙 확립

### 5단계 작업 파이프라인 (전역)
- Ideation(R1→R2→R3) → Impl Design(R1→R2→R3) → Impl Review(R1→R2) → 실제 구현 → Code Review(R1→R2)
- 폴더 생성은 단계별 (해당 단계 진입 시에만)
- 각 폴더에 index 필수
- 한번에 하나의 작업만 (Stage 5까지 완료 후 다음)
- mcp-memory #4348 (Principle)

### CLI 배치 규칙
- Claude가 매 Stage 진입 시 Codex/Gemini 배치 판단
- ideation-pattern.md에 Stage별 매트릭스 추가

## 3. Track A: Memory-Merger (Phase 3-04)

### Stage 4 — 실제 구현
| # | 태스크 | 상태 |
|---|--------|------|
| M1 | session-start.sh에 get_becoming() 알림 | ✅ |
| M2 | /merge 스킬 생성 | ✅ |
| M3 | 병합 로직 (스킬 내 포함) | ✅ |
| M4 | e2e: #4120 Signal→Pattern 승격 → KNOWLEDGE.md 반영 | ✅ |

**발견사항:**
- SWR gate 대부분 실패 (0.02 < 0.55) — recall 횟수 부족. Pre-flight Recall이 자리잡으면 자연 해결.
- skip_gates MCP 미노출 → server.py에 파라미터 추가 + paul/claude 보안 가드

### Stage 5 R1 — CX (Codex) 리뷰
| 파일 | CX 판정 | 수정 |
|------|---------|------|
| session-start.sh | FAIL → ✅ | overflow "외 N건" + summary sanitize |
| SKILL.md | FAIL → ✅ | target_type 선택, domain 필터, Concept 추가, Heuristic 규칙 |
| server.py | FAIL → ✅ | skip_gates 보안 가드 (paul/claude만) |
| KNOWLEDGE.md | PASS | — |

## 4. Track B: CLI 전략

- 0-cli-strategy.md 작성 (역할 매트릭스, 위임 트리거, 프롬프트 템플릿)
- 핵심 결정: Codex full-auto 권한 + 프롬프트 스코프 제한 (기존 코드 수정 금지)
- Gemini: -o 출력 유지
- CLAUDE.md + delegate-to-codex 스킬 업데이트

## 5. Track C: NDCG 수치 차이

- 원인: goldset 50개(q026-q075) → 75개(q001-q075) 크기 차이
- 0.460 = 50개 기준, 0.359 = 75개 기준. 같은 코드, 같은 DB.
- STATE.md 수정: 75개 기준 0.359로 통일

## 6. 커밋 기록

| 레포 | 해시 | 메시지 |
|------|------|--------|
| mcp-memory | `aa0a66b` | promote_node skip_gates MCP 노출 + 보안 가드 |
| orchestration | `3c47dd5` | Memory-Merger Stage 4+5 완료 |
| orchestration | `0662ca6` | CLI 전략 수립 |
| orchestration | `d517f5d` | NDCG 수치 통일 + STATE.md |

## 7. mcp-memory 저장

| ID | 타입 | 내용 |
|----|------|------|
| #4348 | Principle | 5단계 파이프라인 전역 규칙 |
| #4349 | Decision | Memory-Merger e2e 완료 |

## 8. 수정된 파일

### 코드
- `mcp-memory/server.py` — skip_gates 파라미터 노출 + 보안 가드

### 규칙/설정
- `~/.claude/CLAUDE.md` — Codex full-auto 권한 규칙
- `~/.claude/skills/delegate-to-codex/SKILL.md` — 전면 재작성
- `~/.claude/skills/merge/SKILL.md` — 신규 생성 + CX 리뷰 수정
- `~/.claude/hooks/session-start.sh` — get_becoming() 알림
- `~/.claude/projects/C--dev/memory/ideation-pattern.md` — 5단계 파이프라인 + CLI 배치
- `~/.claude/projects/C--dev/memory/MEMORY.md` — 파이프라인 요약

### 문서
- `orchestration/KNOWLEDGE.md` — 설계 패턴 섹션 (#4120 승격)
- `orchestration/STATE.md` — NDCG 수치 통일 + Memory-Merger
- `orchestration/TODO.md` — Warp/tech-review/YouTube 제거
- `orchestration/decisions.md` — Memory-Merger 승격 기록
- `orchestration/02_implementation/2026-03-09/0-impl-index-0309.md` — 세션 인덱스
- `orchestration/02_implementation/2026-03-09/0-cli-strategy.md` — CLI 전략
- `orchestration/02_implementation/2026-03-08/0-impl-index.md` — Phase 3-04 완료

## 9. 다음 할 일

1. Codex full-auto 플래그 실측 (`--full-auto` vs `--dangerously-bypass-approvals-and-sandbox`)
2. Gemini `.geminiignore` .py 차단 해제 실측
3. q001-q025 NDCG 개선
4. Phase 5 항목 (Discovery 패턴, Wave DAG — 선택)
