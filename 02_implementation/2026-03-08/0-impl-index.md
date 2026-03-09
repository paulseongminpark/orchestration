# 구현 인덱스 — Orchestration 시스템 강화 (Ideation 2026-03-08)

> compact 후 이 파일만 읽고 이어서 진행한다.
> 역할: 세션 관리, 태스크 추적, Phase 간 전환 제어

---

## 배경

`01_ideation/2026-03-08/round-02/`의 역분석 결과:
- 8대 약점 진단 (W1~W8)
- 게임 체인저 3개 (S1~S3) + 포스 멀티플라이어 6개 (A1~A6)
- 5-Phase 복리 실행순서

**defer_loading(C2)은 이미 작동 중 (auto 모드, 55K→3-5K). Phase 1-2의 S1은 완료.**

---

## 워크플로우

```
[Phase 1] MEMORY.md 분리 + 캐시 규칙 (이 세션)
[Phase 2] Recall 혁명 (Warp-1 + Warp-2 병렬) → CX/GM 검증
[Phase 3] 학습 루프 (이 세션) → CX 검증
[Phase 4] 거버넌스 + 스킬 (Gemini 분석 → 이 세션 구현)
[Phase 5] 확장 (선택)
```

**Phase N 완료 검증 전에 Phase N+1 시작 가능 (기술 의존성 없는 경우).**
단, Phase 2와 Phase 3의 A9(Memory-Merger)는 Phase 2 완료 후.

---

## 세션 구성

| 세션 | 도구 | 모델 | 역할 | 소유 영역 | 코드 수정 |
|------|------|------|------|----------|----------|
| **Main** | Claude Code (WezTerm) | Opus | 오케스트레이터: 태스크 관리, 인덱스, Phase 1/3 | orchestration/ 전체 | **Yes (문서+config)** |
| **Warp-1** | Claude Code (Warp) | Opus 1M | Phase 2: 복합 스코어링 (A1+A4+A6) | mcp-memory/ recall | **Yes** |
| **Warp-2** | Claude Code (Warp) | Opus 1M | Phase 2: Correction 타입 (A5) | mcp-memory/ remember+recall | **Yes** |
| **CX** | Codex CLI (WezTerm) | gpt-5.4 xhigh | 테스트 + 코드 리뷰 + goldset 검증 | 없음 | **절대 No** |
| **GM** | Gemini CLI (WezTerm) | Auto (3.1-pro) | 벌크 분석: 스킬 점검, 거버넌스 초안 | 없음 | **절대 No** |

### 파일 소유권

```
Warp-1 소유:
  06_mcp-memory/storage/hybrid.py (recall scoring 수정)
  06_mcp-memory/config.py (상수 추가)
  06_mcp-memory/tests/test_goldset.py (NDCG 재측정)

Warp-2 소유:
  06_mcp-memory/config.py (Correction 타입 추가) ← Warp-1과 충돌 주의
  06_mcp-memory/tools/recall.py (top-inject)
  06_mcp-memory/tools/remember.py (Correction 지원)

Main 소유:
  01_orchestration/ 전체
  ~/.claude/ (hooks, settings, rules, skills)

CX/GM: 읽기 전용. 코드 수정 절대 불가.
```

**충돌 관리**: Warp-1이 config.py 먼저 커밋 → Warp-2가 pull 후 작업.
Warp-1 (스코어링) 작업이 Warp-2 (Correction) 보다 config.py를 먼저 건드림.

---

## Phase 문서

| # | 파일 | 내용 | 세션 |
|---|------|------|------|
| 1 | `0-impl-phase1.md` | 토큰 해방: MEMORY.md 분리 + 캐시 규칙 | Main |
| 2 | `0-impl-phase2.md` | Recall 혁명: A1+A4+A5+A6 | Warp-1, Warp-2 |
| 3 | `0-impl-phase3.md` | 학습 루프: CONTRACT + Learn + lessons | Main |
| 4 | `0-impl-phase4.md` | 거버넌스 + 스킬: audit hook + TRIGGER | Main + GM |

---

## Codex / Gemini 사용 가이드

### CX (Codex CLI) — 검증

```bash
# Phase 2 완료 후: goldset NDCG 재측정
codex exec "cd /c/dev/01_projects/06_mcp-memory && \
  python -m pytest tests/test_goldset.py -v 2>&1. \
  Report NDCG@5 and NDCG@10 for q026-q050 and q051-q075 separately. \
  Compare with baseline: NDCG@5=0.460, NDCG@10=0.488." \
  -p review -o /c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/cx-phase2-ndcg.md

# Phase 2 코드 리뷰
codex exec "review changes in /c/dev/01_projects/06_mcp-memory/storage/hybrid.py \
  and /c/dev/01_projects/06_mcp-memory/tools/recall.py. \
  Check: composite scoring formula correctness, decay function edge cases, \
  multiplier application, backward compatibility. Output pass/fail per item." \
  -p review -o /c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/cx-phase2-review.md

# Phase 3 TASK_CONTRACT 검증
codex exec "review /c/Users/pauls/.claude/hooks/ for any new hooks added. \
  Check: proper error handling, async safety, no side effects on main session. \
  Also check new skill files for correct YAML frontmatter." \
  -p review -o /c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/cx-phase3-review.md
```

### GM (Gemini CLI) — 벌크 분석

```bash
# Phase 4: 스킬 9개 TRIGGER 패턴 일괄 분석
gemini "Read all SKILL.md files in /c/dev/.agents/skills/ and /c/Users/pauls/.claude/skills/. \
  For each skill, analyze: \
  1. Does it have explicit TRIGGER conditions? \
  2. Does it have DO NOT TRIGGER conditions? \
  3. Is the description clear enough for auto-detection? \
  Propose improved descriptions with TRIGGER/DO NOT TRIGGER for each. \
  Format as markdown table." \
  -o /c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/gm-skill-trigger-audit.md

# Phase 4: governance-audit hook 초안
gemini "Read the governance-audit hook spec from \
  /c/dev/01_projects/01_orchestration/01_ideation/2026-03-08/round-01/04_governance.md \
  section D4. Also read existing hooks at /c/Users/pauls/.claude/hooks/. \
  Generate a governance-audit.sh hook script that: \
  1. Scans PreToolUse input for 5 threat categories (data_exfiltration, privilege_escalation, \
     system_destruction, prompt_injection, credential_exposure) \
  2. Uses regex patterns with confidence scores \
  3. Blocks high-confidence threats, logs medium ones \
  4. Writes to logs/copilot/governance/audit.log (JSON Lines) \
  Format: complete bash script ready to install." \
  -o /c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/gm-governance-hook-draft.sh
```

---

## 트래킹 — compact 후 손실 0 보장

### 3중 추적

```
[Layer 1] Phase 문서 체크박스  ← Main만 갱신 (CX/GM 검증 후)
[Layer 2] 이 인덱스 "현재 상태" ← Main이 Phase 전환 시 갱신
[Layer 3] Git 커밋 메시지      ← 자동 감사 추적
```

### Compact 후 재개

```
1. 이 파일(0-impl-index.md) 읽기
2. "현재 상태" 섹션에서 현재 Phase + 마지막 완료 태스크 확인
3. 해당 Phase 문서(0-impl-phase{N}.md) 읽기
4. 미완료 체크박스부터 이어서 진행
```

### Warp 세션 Compact 지침

**Warp-1 (스코어링)**:
```
이 세션은 mcp-memory recall 복합 스코어링 구현 세션이다.
/c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/0-impl-index.md를 읽어라.
Phase 2의 Warp-1 태스크를 확인하고 진행하라.
소유 파일: storage/hybrid.py, config.py, tests/test_goldset.py
```

**Warp-2 (Correction)**:
```
이 세션은 mcp-memory Correction 노드 타입 구현 세션이다.
/c/dev/01_projects/01_orchestration/02_implementation/2026-03-08/0-impl-index.md를 읽어라.
Phase 2의 Warp-2 태스크를 확인하고 진행하라.
소유 파일: tools/recall.py, tools/remember.py, config.py (Warp-1 커밋 후)
```

---

## 안전 규칙

1. **CX/GM은 절대 코드 수정 안 함** — 읽기/분석/테스트만
2. **Warp-1이 config.py를 먼저 커밋** → Warp-2가 pull 후 작업
3. **커밋은 태스크 단위** — `[mcp-memory] 태스크 설명` 또는 `[orchestration] 태스크 설명`
4. **Phase 2 DB 변경 전 백업**: `cp data/memory.db data/memory.db.pre-scoring`

---

## 현재 상태 (compact 후 이 섹션을 가장 먼저 확인)

**현재: 실행 준비 완료. Phase 1~4 시작 대기.**

준비된 것:
- [x] Ideation Round 1 완료 (13개 문서 + 6개 raw)
- [x] Ideation Round 2 완료 (7개 문서)
- [x] defer_loading 이미 작동 확인 (C2 완료)
- [x] 구현 인덱스 작성 (이 파일)
- [x] Warp 프롬프트 2개 작성 (round-02/_warp-prompt-*.md)
- [x] Phase 1 완료 (MEMORY.md 182→58줄, topic 파일 7개)
- [x] Phase 2 Warp-1 완료 (composite scoring, NDCG 0.336→0.359 +6.8%)
- [x] Phase 2 Warp-2 완료 (Correction top-inject)
- [x] Phase 2 CX 리뷰 완료 (2026-03-09, NO-GO: recall.py 버그 2건 → 별도 세션 수정 필요)
- [x] Phase 3-01: TASK_CONTRACT 템플릿 생성 완료
- [x] Phase 3-02: Learn 단계 초안 완료 (cx-learn-step-draft.md)
- [x] Phase 3-03: lessons.md 생성 완료 (초기 3건)
- [x] Phase 3-02: compressor agent.md에 Learn 단계 10 적용 완료 (2026-03-09)
- [x] Phase 3-04: Memory-Merger 구현 완료 (2026-03-09, session-start.sh + /merge 스킬 + skip_gates + CX R1)
- [x] Phase 4-01: governance-audit.sh 설치 완료
- [x] Phase 4-02: KNOWLEDGE.md 캐싱 규칙 추가 완료
- [x] Phase 4-02: 스킬 TRIGGER 패턴 5개 적용 완료 (2026-03-09)

다음 할 일:
1. Phase 5 항목 (Discovery 패턴, Wave DAG — 선택)
2. Codex full-auto 플래그 실측 (CLI 전략 미결)
3. Gemini .geminiignore 실측
4. q001-q025 NDCG 개선

0309 세션1 기록: 02_implementation/2026-03-09/work-log-0309.md
0309 세션2 기록: 02_implementation/2026-03-09/work-log-0309-s2.md
0309 세션2 인덱스: 02_implementation/2026-03-09/0-impl-index-0309.md
