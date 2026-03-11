# Impl Design — Session Chain + Ontology Redesign

> **작성**: 2026-03-11
> **기반**: 01_dialogue.md (R1 Exchange 1-6, R2 Exchange 7-11)
> **총 변경**: 17건 (변경 9, 신규 2, 폐기 5, 제거 1)
> **Impl Review**: R1 세부 점검 8건, R2 전체 관점 4건 → 수정 8건 반영

## 의존성 그래프

```
Phase 0 (Foundation)          Phase 1 (Core)           Phase 1.5 (Monitor)
┌─────────────┐              ┌──────────────────┐      ┌───────────────────┐
│ config.py   │─────────────→│ auto_remember.py │─────→│ 2~3세션 모니터링   │
│ +3 RULES    │              │ +TYPE_MAP (11개) │      │ ontology_review   │
└─────────────┘              │ -테스트/완료 제거 │      │ 타입 분포 확인     │
                             └──────────────────┘      └───────────────────┘
┌─────────────┐              ┌──────────────────┐
│ relay.py    │              │ save_session.py  │
│ →Narrative  │              │ +node creation   │
└─────────────┘              │ +명시적 edge     │      Phase 2 (Migration)
                             └──────────────────┘      ┌─────────────────────┐
                                      │                │ migration script    │
                                      │                │ sessions→nodes      │
                              Phase 3 (Chain)          │ pending→반자동      │
                             ┌──────────────────┐      │ lessons→nodes       │
                             │ compressor.md    │      │ MEMORY.md verify    │
                             │ 5단계, sonnet    │      └─────────┬───────────┘
                             │ +Bash tool       │                │
                             ├──────────────────┤        Phase 4 (Cleanup)
                             │ session-end SKILL│      ┌─────────────────────┐
                             ├──────────────────┤      │ session-stop.sh     │
                             │ claude.md rules  │      │ →제거 or 최소 로깅  │
                             └──────────────────┘      ├─────────────────────┤
                                                       │ sync/SKILL.md       │
                                                       │ -/sync all          │
                                                       ├─────────────────────┤
                                                       │ render_memory_md.py │
                                                       │ +COALESCE 처리      │
                                                       └─────────┬───────────┘
                                                                 │
                                                         Phase 5 (Delete)
                                                       ┌─────────────────────┐
                                                       │ ❌ analyze-session.sh│
                                                       │ ❌ auto-promote.sh   │
                                                       │ ❌ sync-memory.sh    │
                                                       │ ❌ pending.md        │
                                                       │ ❌ session-stop.sh   │
                                                       └─────────────────────┘
```

## 실행 계획

### Phase 0: Foundation (의존성 없음)

**P0-1. config.py — RELATION_RULES 3개 추가**
- 파일: `/c/dev/01_projects/06_mcp-memory/config.py`
- 변경: RELATION_RULES dict에 3개 추가
  ```python
  ("Narrative", "Decision"): "contains",
  ("Narrative", "Question"): "contains",
  ("Decision", "Question"): "led_to",
  ```
- 테스트: 기존 163 tests 전부 통과 확인
- 모델: 직접 (1줄 × 3)

**P0-2. relay.py — type 변경**
- 파일: `/c/Users/pauls/.claude/hooks/relay.py`
- 변경: `type="Observation"` → `type="Narrative"`, `confidence=0.5`
- 테스트: hook 실행 시 에러 없는지 수동 확인
- 모델: 직접 (1줄)

---

### Phase 1: Core Pipeline (Phase 0 완료 후)

**P1-1. auto_remember.py — TYPE_MAP + SIGNAL_MAP**
- 파일: `/c/Users/pauls/.claude/hooks/auto_remember.py`
- 변경:
  1. `FILE_TYPE_MAP` dict 추가 (**11개** 매핑)
     ```python
     FILE_TYPE_MAP = {
         "STATE.md":      ("Decision",  1),
         "decisions.md":  ("Decision",  1),
         "CHANGELOG.md":  ("Decision",  1),
         "PLANNING.md":   ("Decision",  1),   # ← 추가
         "CLAUDE.md":     ("Principle", 3),
         "GEMINI.md":     ("Framework", 2),
         "AGENTS.md":     ("Framework", 2),
         "KNOWLEDGE.md":  ("Pattern",   2),   # ← 추가
         "REFERENCE.md":  ("Framework", 2),   # ← 추가
         "schema.yaml":   ("Framework", 2),
         "config.py":     ("Tool",      1),
     }
     ```
  2. `BASH_SIGNAL_MAP` dict 추가 (**9개**, 모호한 "테스트"/"완료" 제거)
     ```python
     BASH_SIGNAL_MAP = {
         "FAIL":     ("Failure",    1),
         "ERROR":    ("Failure",    1),
         "error:":   ("Failure",    1),
         "❌":       ("Failure",    1),
         "실패":     ("Failure",    1),
         "PASS":     ("Experiment", 1),
         "✅":       ("Experiment", 1),
         "NDCG":     ("Experiment", 1),
         "hit_rate": ("Experiment", 1),
     }
     # "테스트", "완료" → 저장 트리거만, 타입은 Observation(기본)
     ```
  3. `CONFIDENCE_BY_LAYER` dict 추가 (4개 레이어)
  4. `handle_write_edit()`: IMPORTANT_FILES + FILE_TYPE_MAP 통합
     - IMPORTANT_FILES를 FILE_TYPE_MAP.keys()로 대체
     - FILE_TYPE_MAP에 없으면 Observation(L0) fallback
  5. `handle_bash()`: Failure 우선 매칭
  6. `handle_bash()`: `get_project(cmd)` 적용
- 테스트:
  - 수동: STATE.md 수정 → Decision 타입 확인
  - 수동: Bash PASS → Experiment 확인
  - 수동: Bash FAIL → Failure 확인
- 모델: 직접

**P1-2. save_session.py — 노드 생성 + 명시적 edge**
- 파일: `/c/dev/01_projects/06_mcp-memory/tools/save_session.py`
- 변경:
  1. `from tools.remember import remember` 추가
  2. `from storage import sqlite_store` (이미 있음)
  3. sessions 테이블 저장 후:
     - Narrative 노드 생성 → `session_node_id` 저장
     - 각 decision → Decision 노드 생성 → `decision_ids` 수집
     - 각 unresolved → Question 노드 생성 → `question_ids` 수집
  4. **명시적 edge 생성** (link() 벡터 유사도에 의존하지 않음):
     ```python
     for did in decision_ids:
         sqlite_store.insert_edge(
             source_id=session_node_id,
             target_id=did,
             relation="contains",
             strength=0.9,
         )
     for qid in question_ids:
         sqlite_store.insert_edge(
             source_id=session_node_id,
             target_id=qid,
             relation="contains",
             strength=0.8,
         )
     ```
  5. 에러 핸들링: remember() 실패 시 sessions 테이블 저장은 유지
- 테스트:
  - 단위: save_session → 노드 3개 + edge 2개 생성 확인
  - 단위: recall() → Narrative 노드 조회 가능 확인
  - 기존 163 tests 통과
- 모델: 직접

---

### Phase 1.5: 모니터링 (Phase 1 완료 후, 2~3세션)

**구현 아닌 관찰 단계.**

- `ontology_review` 또는 `inspect`로 확인:
  - 새로 생성된 노드의 타입 분포 (L0 일색이 아닌지)
  - save_session() edge 생성 정상 여부
  - auto_remember TYPE_MAP 매칭 정확도
- 문제 발견 시 Phase 1 수정 후 Phase 2로 진행

---

### Phase 2: Migration (Phase 1.5 확인 후)

**P2-1. 마이그레이션 스크립트**
- 파일: `/c/dev/01_projects/06_mcp-memory/scripts/migrate_to_nodes.py` (신규)
- 내용:
  ```python
  # 1. sessions 테이블 → 새 save_session()으로 재실행
  #    중복 방지: content_hash (remember 내장)

  # 2. pending.md → 반자동 (Claude가 각 항목 타입 판단)
  #    스크립트는 파싱 + remember() 호출만
  #    타입 결정은 실행 시 인자로 전달

  # 3. lessons.md → Insight(L2) 노드
  #    각 줄 파싱: "- [{날짜}] {내용}" → remember(type="Insight")

  # 4. MEMORY.md 수동 섹션 → Claude가 확인 후 수동 remember()
  ```
- 실행: **DRY_RUN=True 먼저 → 확인 → 실제 실행**
- 모델: 직접 (일회성)

---

### Phase 3: Chain Update (Phase 1 완료 후, Phase 2와 병렬 가능)

**P3-1. compressor.md — 5단계 + Sonnet + Bash**
- 파일: `/c/Users/pauls/.claude/agents/compressor.md`
- 변경:
  1. `model: opus` → `model: sonnet`
  2. `tools: Read, Write` → `tools: Read, Write, Bash`
  3. 11단계 → 5단계 재작성:
     ```
     1. LOG: session-summary.md 갱신 + LOG append
     2. Living Docs: STATE.md + CHANGELOG.md 갱신
     3. Commit: git commit+push (변경 프로젝트 전부)
     4. [반환] save_session 데이터 → main Claude가 MCP 호출
     5. Learn: Insight(기술) + Insight(Paul 관찰) + lessons.md
     ```
  4. Learn 단계 구조:
     ```
     Discovery: 새로 알게 된 것
     Lesson: 실패에서 배운 것
     Improvement: 다음에 다르게 할 것
     Paul 관찰: 이 세션에서 Paul에 대해 알게 된 것 ← 신규
     ```
  5. 검증: "5곳 저장 확인" (LOG, STATE+CHANGELOG, git, mcp-memory, Insight+lessons)
- 모델: 직접 (문서 재작성)

**P3-2. session-end/SKILL.md — 동기화**
- 파일: `/c/Users/pauls/.claude/skills/session-end/SKILL.md`
- 변경:
  1. 5단계 설명으로 동기화
  2. 체인: `/session-end → /compact`
  3. compressor agent(Sonnet) 호출 설명
  4. main Claude의 역할: save_session() MCP + render_memory_md.py
- 모델: 직접

**P3-3. claude.md rules — 체인 정의**
- 파일: `/c/dev/.claude/rules/claude.md`
- 변경:
  1. 세션 아카이브: `/session-end → compressor(Sonnet) 5단계`
  2. 세션 전환: `/session-end → /compact` (verify, /sync all, linker 제거)
  3. `/sync all` 참조 모두 제거
- 모델: 직접

---

### Phase 4: Cleanup (Phase 2 + Phase 3 완료 후)

**P4-1. session-stop.sh → 제거**
- 파일: `/c/Users/pauls/.claude/hooks/session-stop.sh`
- 처리: settings.json SessionEnd 훅에서 제거
  - session-stop.sh의 전체 로직이 analyze+promote → 둘 다 폐기
  - git status echo와 MEMORY.md 줄 수 체크는 별도 훅으로 이미 존재
- 모델: 직접

**P4-2. sync/SKILL.md — /sync all 제거**
- 파일: `/c/dev/01_projects/01_orchestration/.claude/skills/sync/SKILL.md`
- 변경: `/sync all` 섹션 제거, `/sync`만 유지
- 모델: 직접

**P4-3. render_memory_md.py — 신규**
- 파일: `/c/dev/01_projects/06_mcp-memory/scripts/render_memory_md.py` (신규)
- 내용:
  ```python
  # DB 직접 쿼리 (AI 토큰 0)
  # 1. Fixed 섹션: 템플릿 또는 기존 MEMORY.md에서 추출
  # 2. L3 전체: SELECT * FROM nodes WHERE layer=3
  # 3. L2 상위 15개:
  #    SELECT * FROM nodes WHERE layer=2
  #    ORDER BY COALESCE(quality_score, 0.65) DESC
  #    LIMIT 15
  # 4. 최근 7일 Decision 상위 5개
  # 5. 미해결 Question 전체
  # 6. 최근 Failure 3개
  # → MEMORY.md 덮어쓰기 (200줄 이내 보장)
  ```
- **COALESCE 처리**: unenriched 노드의 quality_score NULL → UNENRICHED_DEFAULT_QS[layer]
- 테스트: 실행 후 200줄 이내, 구조 올바른지 확인
- 모델: 직접

---

### Phase 5: Delete (Phase 4 완료 후, 사용자 확인 필수)

**P5-1. 파일 삭제**
- `/c/Users/pauls/.claude/scripts/analyze-session.sh` → 삭제
- `/c/Users/pauls/.claude/scripts/auto-promote.sh` → 삭제
- `/c/Users/pauls/.claude/scripts/sync-memory.sh` → 삭제
- `/c/Users/pauls/.claude/hooks/session-stop.sh` → 삭제
- `/c/dev/01_projects/01_orchestration/pending.md` → 삭제 (마이그레이션 완료 후)

**P5-2. settings.json 정리**
- SessionEnd 훅에서 session-stop.sh 항목 제거
- 불필요한 훅 정리

---

## 실행 요약

| Phase | 작업 수 | 복잡도 | 병렬 |
|-------|---------|--------|------|
| 0: Foundation | 2 | 낮 | P0-1 ∥ P0-2 |
| 1: Core | 2 | 중 | P1-1 ∥ P1-2 |
| 1.5: Monitor | 0 (관찰) | - | 2~3세션 |
| 2: Migration | 1 | 중 | Phase 3과 병렬 |
| 3: Chain | 3 | 낮 | P3-1 → P3-2 → P3-3 |
| 4: Cleanup | 3 | 낮~중 | 전부 병렬 |
| 5: Delete | 2 | 낮 | 전부 병렬 |

**총: 13 작업 + 1 모니터링, 6 Phase**

## Impl Review 반영 사항

| # | R1/R2 발견 | 수정 |
|---|-----------|------|
| 1 | save_session() link() 벡터 유사도 부족 | 명시적 edge 생성으로 변경 |
| 2 | compressor에 Bash 도구 없음 | tools에 Bash 추가 |
| 3 | IMPORTANT_FILES 누락 3개 | KNOWLEDGE, REFERENCE, PLANNING 추가 (8→11) |
| 4 | "테스트"/"완료" 모호 | BASH_SIGNAL_MAP에서 제거 (11→9) |
| 5 | session-stop.sh 빈 스크립트 | settings.json에서 제거 + 파일 삭제 |
| 6 | render quality_score NULL | COALESCE 처리 명시 |
| 7 | pending.md 파싱 판단 필요 | 반자동 (Claude 판단) |
| 8 | 구현 후 모니터링 없음 | Phase 1.5 추가 |

## 위험 관리

| 위험 | 완화 |
|------|------|
| TYPE_MAP 잘못된 타입 대량 생성 | Phase 1.5 모니터링 (ontology_review) |
| save_session() remember() 실패 | graceful degradation: sessions 테이블 항상 저장 |
| 마이그레이션 중복 노드 | content_hash 내장 방어 (remember.py 269행) |
| compressor Sonnet 품질 부족 | 1~2세션 평가, Opus 복귀 가능 |
| MEMORY.md 200줄 초과 | top_k 파라미터 조절 |
| 명시적 edge 생성 시 insert_edge 오류 | try/except, 노드는 생성됨 edge만 누락 |

## auto_remember ↔ /checkpoint 병렬 구조

```
[자동] auto_remember          [수동] /checkpoint           [세션 종료] Learn
├── 감지: 파일 수정/Bash     ├── 감지: 대화 중 메타 관찰  ├── 기술: Discovery/Lesson
├── 방식: 기계적 TYPE_MAP    ├── 방식: Claude 해석적 판단  ├── Paul: 메타 관찰
├── confidence: 0.65~0.85    ├── confidence: 0.7~0.9       └── → Insight(L2) 노드
└── → 다양한 타입 노드       └── → 다양한 타입 노드
```

세 트랙은 병렬. 대체 불가. 각각 다른 정보 원천.

## 구현 시작 조건

- [ ] Ideation 완료 (01_dialogue.md) ✅
- [ ] Impl Design 완료 (이 문서) ✅
- [ ] Impl Review R1 + R2 완료 ✅
- [ ] 사용자 승인 → 구현 시작
