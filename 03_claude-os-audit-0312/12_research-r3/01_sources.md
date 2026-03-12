# Research R3: Claude OS 레이어 — 추출 결과
> 2026-03-12 | 직접 읽기 (16K tokens)

## Hook 등록 상태 (settings.json)

| 이벤트 | Hook | 역할 | 상태 |
|---|---|---|---|
| SessionStart | session-start.sh | 브리핑 (프로젝트 상태/파이프라인/결정) | ✅ |
| PreToolUse (Bash) | pre-tool-use.sh | 위험 명령 차단 + C1~C3 commit gate | ✅ |
| PreToolUse (Bash) | governance-audit.sh | 보안 5종 위협 감지 | ✅ |
| PreToolUse (Write\|Edit) | validate_pipeline.py | M1~R2 구조 검증 | ✅ |
| PreToolUse (Write\|Edit) | validate_merged.py | T1 merged 완결성 검증 | ✅ |
| PreToolUse (Write\|Edit) | validate_output.py | G1~G5 DONE gate | ✅ |
| PostToolUse (Write\|Edit) | auto_remember.py | mcp-memory 직접 저장 | ✅ (async) |
| PostToolUse (Write\|Edit) | pipeline-watch.py | index 갱신 리마인드 + D19 전파 | ✅ (async) |
| PostToolUse (Bash) | auto_remember.py | mcp-memory 직접 저장 | ✅ (async) |
| PreCompact | pre-compact.sh + safety_net.py | compact 전 상태 보존 | ✅ |
| SessionEnd | git 상태 + MEMORY.md + safety_net.py | 종료 정리 | ✅ |

---

## validate_pipeline.py 분석

### 구현 규칙 (M1~R2)
- M1: 파이프라인 루트 00_index.md 존재 ✅
- M2: 01_*.md 있어야 Phase 폴더 생성 ✅
- M3: Phase 폴더 내 00_index.md ✅
- I1: Ideation 라운드 01_dialogue.md ✅
- P1+F1: Impl 진입 시 foundation/ 3축 ✅
- P2: Impl 진입 시 Ideation merged ✅ (30_impl-r1 에만)
- P3: 30_impl-r1에 02_context.md ✅
- R1: Review 진입 시 `3?_impl-merged` 존재 ✅
- R2: Review 진입 시 foundation/ 존재 ✅

### 발견된 Issues
- **N17 미구현**: Phase 전환 시 02_context.md 필수 (새 Phase 첫 라운드) → 훅에 없음
- **타입 판별 없음**: 파이프라인 타입(code-review vs full-impl)을 구분하지 않음 → R1 규칙이 custom 파이프라인에도 강제 적용됨 **(G16 → 현재 세션 영향)**

---

## auto_remember.py 분석

### 08/09/10 ↔ mcp-memory 연결
```python
FILE_TYPE_MAP = {
    "STATE.md":      ("Decision",  1),
    "CHANGELOG.md":  ("Decision",  1),
    "CLAUDE.md":     ("Principle", 3),
    "AGENTS.md":     ("Framework", 2),
    "KNOWLEDGE.md":  ("Pattern",   2),
    "config.py":     ("Tool",      1),
    ...
}
```
→ 파이프라인 파일(00_index.md, 01_sources.md 등)은 FILE_TYPE_MAP에 없음
→ 파이프라인 작업 내용이 mcp-memory에 자동 저장되지 않음 (의도적)

---

## pipeline-watch.py 분석

### D19 전파 메커니즘
- phase-rules.json 수정 감지 → pipeline-rules.md + AGENTS.md 자동 갱신 ✅
- **설계 gap**: 훅 Python 코드(validate_pipeline.py 등)는 자동 갱신 안 됨
  → phase-rules.json 규칙 변경 시 훅도 수동 수정 필요

---

## settings.json 주요 설정

| 설정 | 값 | 비고 |
|---|---|---|
| CLAUDE_AUTOCOMPACT_PCT_OVERRIDE | "0" | 자동 compact 비활성화 (의도적) |
| CLAUDE_CODE_EFFORT_LEVEL | "high" | 항상 high effort |
| skipDangerousModePermissionPrompt | true | 위험 모드 프롬프트 생략 |
| language | "ko" | 한국어 |

---

## 신규 gap 포인트

| # | Gap | 위치 | 심각도 |
|---|---|---|---|
| G11 | NotebookEdit 훅 라우팅 불확실: matcher "Write\|Edit"가 NotebookEdit 포함하는지 미확인 | settings.json | Warning |
| G15 | 훅 규칙 하드코딩: phase-rules.json 변경 시 validate_*.py 자동 갱신 안 됨 | hooks/*.py | Warning (by design) |
| **G16** | **validate_pipeline.py R1 규칙이 custom 파이프라인 차단: code-review/research-only 타입에서 Review Phase 진입 시 `3?_impl-merged` 없어서 block** | validate_pipeline.py:L68 | **🚨 Critical (현재 세션 영향)** |
| G17 | N17 미구현: Phase 전환 시 02_context.md 필수 규칙이 훅에 없음 | validate_pipeline.py | Warning |
| G18 | 파이프라인 파일이 FILE_TYPE_MAP에 없어 mcp-memory 자동 저장 안 됨 | auto_remember.py | Info |

---

## 전체 OS 레이어 평가

**강점:**
- 4중 안전망 (PreToolUse 3개 검증기 + PostToolUse auto_remember + governance)
- D19 전파 메커니즘으로 SoT(phase-rules.json) → context(pipeline-rules.md/AGENTS.md) 자동 동기화
- mcp-memory 통합이 FILE_TYPE_MAP 기반으로 체계적

**약점:**
- validate_pipeline.py가 파이프라인 타입을 모름 → custom/code-review 타입에서 R1 규칙 오적용
- phase-rules.json 규칙 변경 시 Python 훅 코드는 수동 유지 필요
