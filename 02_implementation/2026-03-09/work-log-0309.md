# Work Log — 2026-03-09

> 테마: "읽기 경로 완성" — mcp-memory를 write-only DB에서 active recall 시스템으로 전환
> 세션: Main (WezTerm, Opus 4.6)
> 시작: ~10:00 KST / 종료: ~13:00 KST

---

## 1. 문제 정의

### 1-1. 이전 세션(0308) 잔여 작업
0308 세션에서 Ideation R1+R2, Implementation Phase 1-4를 진행했으나 아래가 미완료:
- Phase 2 CX 리뷰 (Codex goldset NDCG 재측정 + 코드 리뷰)
- Phase 3-02: compressor.md에 Learn 단계 실제 적용
- Phase 3-04: Memory-Merger 설계
- Phase 4-02: 5 SKILL.md에 TRIGGER 패턴 적용
- Codex-generated 패치 3건 적용 대기

### 1-2. 세션 중 발견된 근본 문제
설계 문서(Memory-Merger)를 읽다가 사용자가 지적:
> "mcp-memory에 checkpoint로 넣어놨는데, 왜 Claude가 그걸 안 따르고 있는지"

진단 결과:
- **쓰기 경로만 있고, 읽기 트리거가 없다**
- remember(), checkpoint, save_session → 저장은 잘 됨
- recall()은 도구로 존재하지만, **작업 시작 시 호출하는 규칙/트리거가 없음**
- session-start의 get_context()는 200토큰 고정 스냅샷 — 작업 특화 쿼리 아님
- B1 인사이트의 5단계(분류→**회상**→조회→실행→학습)에서 "회상" 단계가 구현 안 됨
- mcp-memory 2,800+ 노드가 사실상 write-only DB

### 1-3. 추가 발견
- compact 기준 "정보 소실 0"이 규칙으로 정의되지 않았음
- 파일 날짜 규칙 (0308 vs 0309) 미준수 — 오늘 작업물이 0308 폴더에 들어가고 있었음
- Codex에 `-m o3` 지정 시 ChatGPT 계정 미지원 오류 — config.toml 기본값(gpt-5.4) 사용해야 함

---

## 2. 원자 태스크 분해 + 실행 기록

### Phase 2 CX 리뷰
| # | 태스크 | 상태 | 방법 |
|---|--------|------|------|
| 2-1 | Codex에 CX 리뷰 위임 | ✅ | `codex --full-auto exec` (gpt-5.4 xhigh) |
| 2-2 | 결과 분석: hybrid.py 4/4 PASS | ✅ | Codex 출력 grep |
| 2-3 | 결과 분석: recall.py 1 PASS 2 FAIL | ✅ | NO-GO 판정 |
| 2-4 | recall.py 버그 3건 수정 | ✅ | 직접 Edit (L55-64) |
| 2-5 | Correction 테스트 6/6 PASS 확인 | ✅ | `pytest tests/test_correction.py` |
| 2-6 | 전체 테스트 169/169 PASS 확인 | ✅ | `pytest tests/` |
| 2-7 | NDCG 재측정 | ✅ | `checks/search_quality.py` → 0.353/0.396/0.613 |
| 2-8 | cx-phase2-review.md 작성 | ✅ | NO-GO→GO 판정 기록 |

**recall.py 수정 내용:**
```python
# Before (버그)
corrections_raw = hybrid_search(query, type_filter="Correction", top_k=top_k, mode=mode)
# ...
results = corrections_new + results

# After (수정)
if not type_filter:  # type_filter 명시 시 Correction 주입 스킵
    corrections_raw = hybrid_search(
        query, type_filter="Correction", project=project, top_k=top_k, mode=mode
    )  # project 전달 추가
    # ...
    results = (corrections_new + results)[:top_k]  # top_k trim 추가
```

### 패치 적용 (0308 잔여)
| # | 태스크 | 상태 | 파일 |
|---|--------|------|------|
| P-1 | compressor.md Learn 단계 10 삽입 | ✅ | ~/.claude/agents/compressor.md |
| P-2 | compressor.md 9단계→11단계 | ✅ | 위와 동일 |
| P-3 | diff-only SKILL.md TRIGGER 추가 | ✅ | .agents/skills/diff-only/SKILL.md |
| P-4 | review-checklist SKILL.md TRIGGER | ✅ | .agents/skills/review-checklist/SKILL.md |
| P-5 | state-reader SKILL.md TRIGGER | ✅ | .agents/skills/state-reader/SKILL.md |
| P-6 | test-matrix SKILL.md TRIGGER | ✅ | .agents/skills/test-matrix/SKILL.md |
| P-7 | worktree-setup SKILL.md TRIGGER | ✅ | .agents/skills/worktree-setup/SKILL.md |
| P-8 | session-start.sh 확인 | ✅ | 이미 CONTRACT 알림 있음 |

### Memory-Merger 설계
| # | 태스크 | 상태 |
|---|--------|------|
| M-1 | 기존 analyze_signals/promote_node/get_becoming 조사 | ✅ |
| M-2 | 빠진 부분 식별: "Merger 브릿지" | ✅ |
| M-3 | 5단계 아키텍처 설계 (Detect→Present→Promote→Merge→Record) | ✅ |
| M-4 | 구현 계획 M1-M4 작성 | ✅ |
| M-5 | 미결 사항 4건 기록 | ✅ |

### Pre-flight Recall (근본 문제 해결)
| # | 태스크 | 상태 | 파일 |
|---|--------|------|------|
| R-1 | mcp-memory recall로 현재 저장 상태 확인 | ✅ | 3개 recall 쿼리 |
| R-2 | 80개 인사이트에서 관련 항목 확인 | ✅ | C5, B1, C9 식별 |
| R-3 | pre-flight-recall.md 본체 작성 | ✅ | orchestration/pre-flight-recall.md |
| R-4 | common-mistakes.md에 포인터 추가 | ✅ | 2줄 루트 패턴 |
| R-5 | workflow.md 체인에 recall 삽입 | ✅ | 작업 흐름 첫 단계 |
| R-6 | ideation-pattern.md R0/I0/V0 추가 | ✅ | Pre-flight 단계 |
| R-7 | TASK_CONTRACT Step 0 추가 | ✅ | recall 결과 섹션 |
| R-8 | compressor에 recall 체크 추가 | ✅ | Learn 단계 하단 |
| R-9 | mcp-memory 4패턴 remember() | ✅ | #4327-#4330 |

### 기타
| # | 태스크 | 상태 |
|---|--------|------|
| X-1 | compact 규칙 "정보 소실 0" 기록 | ✅ |
| X-2 | MEMORY.md compact 기준 추가 | ✅ |
| X-3 | common-mistakes.md compact 절차 추가 | ✅ |
| X-4 | cli.md Codex `-m o3` 불가 기록 | ✅ |
| X-5 | 0308 → 0309 파일 이동 (날짜 규칙) | ✅ |

---

## 3. Pain Points

### 3-1. Codex `-m o3` 오류
- `ERROR: The 'o3' model is not supported when using Codex with a ChatGPT account.`
- config.toml에 gpt-5.4가 기본값으로 설정돼 있었으나, `-m o3`으로 오버라이드해서 실패
- **해결**: 모델 지정 없이 실행 → config.toml 기본값 사용
- **기록**: cli.md에 추가

### 3-2. Codex sandbox tempdir 권한
- Codex sandbox에서 pytest 실행 시 `sqlite3.OperationalError: unable to open database file`
- `C:\windows\TEMP`에 DB 생성 권한 없음
- **해결**: Codex pytest 결과는 참고용. 실제 검증은 로컬 pytest로.

### 3-3. NDCG 수치 혼란
- STATE.md 기록: NDCG@5=0.460 (goldset v2.2)
- 오늘 측정: NDCG@5=0.353
- Warp-1 세션 측정: 0.336→0.359
- **원인**: goldset 버전/쿼리 subset 차이. 0.353은 Warp-1의 0.359와 일관.
- 임계값(0.25) 기준 PASS이므로 문제 없음.

### 3-4. pre-compact 스냅샷 미채움
- pre-compact hook이 스냅샷 템플릿만 생성하고 Claude가 채우기 전에 compact 진행됨
- **해결**: common-mistakes.md에 compact 4단계 절차 규칙 추가

### 3-5. mcp-memory 읽기 경로 부재 (근본 문제)
- 2,800+ 노드 저장, 저장 잘 됨
- 작업 시작 시 recall 안 함 → 과거 결정 무시
- **해결**: Pre-flight Recall 규칙 + 5개 파일에 배치

---

## 4. Ideation 참조

이번 작업에서 참조한 80개 인사이트 중 핵심:
- **B1**: 분류→**회상**→조회→실행→학습 5단계 → Pre-flight Recall의 근거
- **C5**: "CLAUDE.md는 IF-ELSE 디렉토리" → 파일 루트 패턴의 근거
- **C6**: TASK_CONTRACT → Step 0 Pre-flight Recall 추가
- **C9**: What-Context-Needed → recall이 그 선언

---

## 5. 커밋 기록

| 시각 | 레포 | 해시 | 메시지 |
|------|------|------|--------|
| ~12:15 | mcp-memory | `5933ff9` | recall.py Correction injection 버그 3건 수정 |
| ~12:15 | orchestration | `581f780` | Phase 2 CX 리뷰 완료 + Memory-Merger 설계 |
| ~12:50 | dev | `8cf1122` | 5 SKILL.md에 TRIGGER/DO NOT TRIGGER 패턴 추가 |
| ~12:50 | orchestration | `db99268` | Pre-flight Recall 규칙 + TASK_CONTRACT Step 0 |

모든 레포 push 완료 (dev/orchestration/mcp-memory).

---

## 6. mcp-memory 저장

| ID | 타입 | 내용 |
|----|------|------|
| #4327 | Pattern | Ideation→Implementation→Review 표준 패턴 |
| #4328 | Principle | Pre-flight Recall 규칙 |
| #4329 | Pattern | 날짜별 폴더 규칙 |
| #4330 | Principle | Compact 정보소실 0 기준 |

---

## 7. 수정된 파일 전체 목록

### 코드 수정
- `mcp-memory/tools/recall.py` — Correction injection 버그 3건

### 규칙/설정 수정
- `~/.claude/agents/compressor.md` — Learn 단계 10 + recall 체크
- `~/.claude/rules/common-mistakes.md` — Pre-flight Recall + Compact 규칙
- `~/.claude/rules/workflow.md` — recall 단계 삽입
- `~/.claude/projects/C--dev/memory/MEMORY.md` — compact 기준
- `~/.claude/projects/C--dev/memory/ideation-pattern.md` — R0/I0/V0
- `~/.claude/projects/C--dev/memory/cli.md` — Codex 모델 제약

### 문서 생성
- `orchestration/pre-flight-recall.md` — Active Recall 규칙 본체
- `orchestration/02_implementation/2026-03-09/0-design-memory-merger.md` — 설계
- `orchestration/02_implementation/2026-03-09/cx-phase2-review.md` — CX 리뷰
- `orchestration/02_implementation/2026-03-09/work-log-0309.md` — 이 파일

### 스킬 수정
- `.agents/skills/diff-only/SKILL.md` — TRIGGER 패턴
- `.agents/skills/review-checklist/SKILL.md` — TRIGGER 패턴
- `.agents/skills/state-reader/SKILL.md` — TRIGGER 패턴
- `.agents/skills/test-matrix/SKILL.md` — TRIGGER 패턴
- `.agents/skills/worktree-setup/SKILL.md` — TRIGGER 패턴

### 인덱스 갱신
- `orchestration/02_implementation/2026-03-08/0-impl-index.md` — 체크박스 + 다음 할 일
- `orchestration/02_implementation/2026-03-08/task-contract-template.md` — Step 0
