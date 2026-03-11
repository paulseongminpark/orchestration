# System Briefing — 08 Documentation System 미준수 문제 전체 컨텍스트

> 작성: 2026-03-11 | 작성자: Claude (Opus 4.6)
> 목적: 외부 AI (GPT/Opus)에게 현재 문제 상황의 전체 맥락을 전달
> 대상 독자: 이 시스템을 처음 보는 AI. 사전 지식 가정 없음.

---

## 1. 시스템 개요 — Paul의 개인 개발 오케스트레이션

### 1-1. 전체 구조

Paul은 Claude Code(CLI)를 중심으로 개인 프로젝트 생태계를 운영한다. 7개 프로젝트, 3개 메타 시스템, 복수의 AI CLI(Claude/Codex/Gemini)를 하나의 워크스페이스에서 관리한다.

```
C:/dev/                              ← 워크스페이스 루트
├── CLAUDE.md                        ← 공유 규칙 (모든 CLI가 읽음)
├── HOME.md                          ← Obsidian 볼트 허브
├── 01_projects/
│   ├── 01_orchestration/            ← 시스템 설정 + 메타 관리
│   ├── 02_portfolio/                ← Next.js 포트폴리오
│   ├── 03_tech-review/              ← Jekyll 블로그
│   ├── 04_monet-lab/                ← UI 실험 (archived)
│   ├── 05_daily-memo/               ← 핸드폰 메모 자동 sync
│   ├── 06_mcp-memory/               ← 외부 메모리 MCP 서버
│   ├── 08_documentation-system/     ← 파이프라인 문서화 표준 ★
│   ├── 09_context-cascade-system/   ← 대용량 읽기 인프라
│   └── 10_index-system/             ← 에코시스템 인덱스 + 그래프
```

### 1-2. Claude Code 설정 계층

Claude Code는 여러 계층의 설정 파일을 **세션 시작 시 자동으로** 읽는다:

```
[항상 자동 로드]
~/.claude/CLAUDE.md                   ← 전역 개인 설정 (Global)
~/.claude/rules/*.md                  ← 전역 규칙 (common-mistakes.md, workflow.md)
~/.claude/projects/C--dev/memory/MEMORY.md ← 자동 메모리 (200줄 제한)
C:/dev/CLAUDE.md                      ← 프로젝트 공유 규칙
C:/dev/01_projects/01_orchestration/.claude/CLAUDE.md ← 프로젝트별 규칙

[세션 시작 시 Hook으로 로드]
session-start.sh 출력               ← 미커밋 현황, 미반영 결정, 외부 메모리 컨텍스트

[호출 시에만 로드]
Skills (SKILL.md)                    ← /pipeline, /restore 등 — 호출하면 내용이 Claude에 주입
Agents (*.md)                        ← compressor, code-reviewer 등 — 서브에이전트 프롬프트
```

### 1-3. 핵심 개념: 강제력 계층

시스템의 규칙/프로세스는 4가지 강제력 수준으로 존재한다:

| 계층 | 메커니즘 | 회피 가능? | 예시 |
|------|----------|-----------|------|
| **최강: Hook** | 자동 실행, Claude 개입 불필요 | 불가능 | auto_remember.py, session-start.sh |
| **강: Skill** | 명시적 호출 시 프롬프트 주입 | 호출 안 하면 회피 | /pipeline, /session-end, /restore |
| **중: Agent** | 체인 내에서 자동 발동 | 체인 무시하면 회피 | code-reviewer, commit-writer |
| **약: Rule** | 텍스트, Claude가 기억해서 따름 | 쉽게 회피 | common-mistakes.md 체크리스트 |

**이 계층이 이 문서의 핵심 문제와 직결된다.**

---

## 2. Hook 시스템 — 가장 강력한 강제

### 2-1. settings.json 구조

`~/.claude/settings.json`에 정의된 Hook 8종:

| Hook | 트리거 | 파일 | 동작 |
|------|--------|------|------|
| **SessionStart** | 세션 시작 | session-start.sh | 미커밋 현황 + 미반영 결정 + 외부 메모리 출력 |
| **SessionEnd** | 세션 종료 | (인라인) | git 상태 + MEMORY.md 경고 + safety_net.py |
| **PostToolUse** | Write/Edit 후 | auto_remember.py + post-tool-live-context.sh | 온톨로지 자동 저장 + live-context 갱신 |
| **PostToolUse** | Bash 후 | auto_remember.py | 에러/성공 시그널 자동 저장 |
| **PreToolUse** | Bash 전 | pre-tool-use.sh + governance-audit.sh | 위험 명령 차단 |
| **PreCompact** | compact 전 | pre-compact.sh + safety_net.py | 스냅샷 생성 + 미커밋 경고 |
| **TeammateIdle** | 팀원 유휴 | (인라인) | 유휴 알림 |
| **TaskCompleted** | 태스크 완료 | (인라인) | 완료 알림 + .ctx/ 갱신 |

### 2-2. auto_remember.py — 온톨로지 자동 저장

PostToolUse Hook으로 **모든 Write/Edit/Bash 후** 자동 실행. Claude가 의식하지 않아도 중요 이벤트가 mcp-memory DB에 저장된다.

```python
FILE_TYPE_MAP = {
    "STATE.md":      ("Decision",  1),   # 상태 변경 = 결정
    "CLAUDE.md":     ("Principle", 3),   # 설정 변경 = 원칙
    "KNOWLEDGE.md":  ("Pattern",   2),   # 패턴 추가
    "config.py":     ("Tool",      1),   # 도구 변경
    # ... 11개 매핑
}

BASH_SIGNAL_MAP = {
    "FAIL":     ("Failure",    1),       # 실패 기록
    "PASS":     ("Experiment", 1),       # 실험 결과
    "NDCG":     ("Experiment", 1),       # 벤치마크
    # ... 9개 매핑, Failure 우선
}
```

**핵심**: 이 Hook은 Claude의 행동(Write/Edit/Bash)을 감지해서 자동 저장한다. Claude가 "저장해야지"라고 생각하지 않아도 된다. **이것이 Hook 계층의 힘이다.**

---

## 3. 세션 체인 v4.1 — 세션 생명주기

### 3-1. 세션 종료 체인 (5단계)

```
/session-end 호출
→ compressor(Sonnet) 실행:
  1. LOG: session-summary.md + logs/YYYY-MM-DD.md
  2. Living Docs: STATE.md + CHANGELOG.md 갱신
  3. Commit + Push: 변경된 프로젝트 전부
  4. save_session 데이터 반환 → lead agent(Opus)가 MCP 호출
  5. Learn: Insight 노드 + Paul 관찰 + lessons.md
```

### 3-2. save_session() — 세션을 그래프 노드로 저장

```python
save_session(
    summary="세션 요약",
    decisions=["결정1", "결정2"],
    unresolved=["미결1"],
    project="orchestration",
    active_pipeline="01_ideation/2026-03-11-session-chain-redesign/"  # ← 오늘 추가
)
```

내부 동작:
1. sessions 테이블에 UPSERT
2. Narrative 노드 생성 (세션 전체 요약)
3. Decision 노드 N개 생성 (각 결정)
4. Question 노드 M개 생성 (미결 질문)
5. 명시적 edge: Narrative→Decision (contains, 0.9), Narrative→Question (contains, 0.8)

### 3-3. compact 후 복구 — /restore 스킬

```
/restore [키워드]
→ 1. get_context() — DB에서 세션 요약 + active_pipeline 경로 반환
→ 2. 활성 파이프라인 00_index.md 읽기 — 정확한 작업 위치 (✅/⬜)
→ 3. recall("[키워드]") — 관련 Decision/Question 노드 검색
→ 4. 종합 보고
```

**이것은 오늘 이 세션에서 만든 것이다. 이전에는 2-3단계가 없었다.**

---

## 4. mcp-memory — 외부 메모리 시스템

### 4-1. 개요

SQLite + FTS5 + Graph 기반 외부 메모리. Claude의 200K 컨텍스트 한계를 보완.

- **노드 ~4000개**: Observation, Decision, Question, Pattern, Principle, Insight, Failure 등 15타입
- **엣지 ~7000개**: contains, led_to, evolved_from, depends_on 등
- **3-Layer 구조**: L0(Signal) → L1(Observation) → L2(Pattern) → L3(Principle)
- **검색**: 하이브리드 (벡터 유사도 + FTS5 키워드 + 그래프 탐색)

### 4-2. 핵심 MCP 도구

| 도구 | 용도 |
|------|------|
| `remember()` | 노드 저장 (type, project, confidence, tags) |
| `recall()` | 키워드로 노드 검색 |
| `get_context()` | 최근 결정 + 미결 질문 + active_pipeline 반환 |
| `save_session()` | 세션 구조화 저장 + 그래프 노드 생성 |
| `ontology_review()` | 타입 분포 + 건강 상태 리포트 |

### 4-3. auto_remember와의 연동

```
Claude가 STATE.md 수정
→ PostToolUse Hook 발동
→ auto_remember.py 실행
→ FILE_TYPE_MAP에서 STATE.md → (Decision, 1) 매핑
→ remember(type="Decision", confidence=0.70) 호출
→ DB에 Decision 노드 저장
```

이 전체 과정이 Claude의 의식 바깥에서 일어난다. **행동 기반 자동 감지.**

---

## 5. 08_documentation-system — 파이프라인 문서화 표준

### 5-1. 설계 의도

> "수많은 정보(110M+ 컨텍스트, 300+ 파일)를 Opus 200K에 정보 손실 0으로 전달하기 위한 표준"

**설계상 08 시스템은 "운영체제"여야 한다.** 모든 작업이 이 시스템 안에서 시작하고, 진행하고, 끝난다.

### 5-2. 핵심 규칙

#### 폴더 구조
```
{NN}_{목적}_{MMDD}/
├── 00_index.md           ← 마스터 인덱스 (compact 복구점)
├── 01_plan.md            ← 목표 + 손실불가 기준
├── foundation/           ← 3축 문서 (principles, philosophy, workflow)
├── 20_ideation-r1/       ← 아이디에이션 라운드 1
├── 21_ideation-r2/       ← 라운드 2
├── 30_impl-r1/           ← 구현 설계
├── 40_review-r1/         ← 리뷰
└── 90_output/            ← 최종 산출물
```

#### 번호 대역
| 대역 | Phase |
|------|-------|
| 00-09 | Meta (index, plan, context) |
| 10-19 | Research |
| 20-29 | Ideation |
| 30-39 | Implementation |
| 40-49 | Review |
| 90-99 | Output |

#### 인덱스 계층 (3단계)
```
00_index.md (마스터)         ← compact 후 이것 하나로 전체 파악 가능
  ├── Phase 상태: ✅/⬜
  └── 각 phase 폴더 → 00_index.md (phase)
```

**principles.md가 명시적으로 말한다:**
> "compact 복구점: 이 파일 하나로 전체 상태 파악 가능."

#### 라이프사이클 방법론
```
Diverge → Cross → Converge → Integrate(merged)
```

**phase-guide.md가 명시적으로 말한다:**
> "판단은 즉흥적이되, 00_index.md에 상태가 누적(append)된다. 과거 결정이 보존된다."

이건 "작업 후에 문서화하라"가 아니다. **"작업하면서 index에 기록하라"**이다.

### 5-3. /pipeline 스킬 — 08 시스템의 진입점

```
/pipeline 호출 → 타입 식별 → principles.md + phase-guide.md 읽기
→ 폴더 생성 → 00_index.md + 01_plan.md 작성 → phase 폴더 생성
→ 실행 준비 완료
```

**/pipeline 스킬이 명시적으로 말한다:**
> "모든 작업은 파이프라인에서 시작한다. 규모와 무관하다."

**rules/workflow.md도 말한다:**
> "모든 작업 착수 전 → /pipeline 강제 발동 (규모 무관)"

---

## 6. 09_context-cascade-system — 대용량 읽기 인프라

200K 토큰 초과 소스를 처리하는 읽기 파이프라인. 핵심 원칙:

1. **요약 금지, 추출만** — "요약해라" 금지. "나열해라", "뽑아라" 사용.
2. **판단 계층**: 파일 선별(Codex 5.4 xhigh) → 교차검증(Gemini Pro) → 추출(flash) → 합성(Opus)
3. **4-Tier 동적 선택**: CLI 잔여량 확인 → Tier 결정

현재 상태: foundation/ 문서만 존재, 실제 구동은 수동.

---

## 7. 10_index-system — 에코시스템 자기인식

프로젝트 간 의존관계를 자동 스캔하는 그래프 시스템.

```
python -m src.cli scan        → graph.json 생성 (25 nodes, 539 edges)
python -m src.cli refs <path> → 특정 파일의 참조 관계
python -m src.cli impact <path> → 변경 영향 범위
```

`views/INDEX.md` 출력 예시:
```
| Project | Type | Tokens | State |
| 01_orchestration | system | 322,863 | Y |
| 06_mcp-memory | python | 27,834,503 | Y |
```

현재 상태: 스캔 기능 구현됨, 실시간 연동 미구현.

---

## 8. common-mistakes.md — 사후 안전망

반복 실수를 방지하기 위한 텍스트 규칙집. **Rule 계층(최약)에 위치.**

### 5단계 마무리 체크리스트
```
1. Living Docs 갱신 (STATE.md + CHANGELOG.md)
2. 옵시디언 갱신 (HOME.md)
3. 커밋
4. push
5. 사용자에게 보고
```

### compact 규칙
```
compact 전 영구 저장소 3곳:
1. index 갱신 — 작업 index의 "현재 상태" 섹션 업데이트
2. mcp-memory save_session
3. work-log 작성
compact 후 복구: index → get_context() → work-log
```

**문제**: 이 체크리스트는 08 시스템의 파이프라인 문서(00_index.md, impl-log, review-log)를 포함하지 않는다. 그리고 Claude는 08 시스템 대신 이 체크리스트를 "주 프로세스"로 인식하고 있었다.

---

## 9. 현재 문제 — 발단부터 순서대로

### 9-1. 발단: compact 후 정보 손실

다른 Claude 세션에서 `/session-end` → `/compact` → "복구해줘" 시도. 새 Claude가:
- get_context() 안 함
- recall() 안 함
- 파이프라인 index 안 읽음
- 파일 3개만 읽고 진행 → 이전 세션 맥락 거의 소실

### 9-2. 1차 분석: 두 레이어

복구에 필요한 정보가 두 곳에 분산:

| 종류 | 저장 위치 | 복구 수단 | 상태 |
|------|-----------|-----------|------|
| 장기 기억 (결정, 패턴) | mcp-memory DB | get_context() + recall() | **복구 수단 있으나 미실행** |
| 단기 작업 상태 (현재 Phase) | 파이프라인 00_index.md | 파일 읽기 | **복구 경로에 없었음** |

### 9-3. 해결: active_pipeline + /restore

1. save_session()에 `active_pipeline` 파라미터 추가 → sessions 테이블에 저장
2. get_context()가 active_pipeline 경로 반환
3. /restore 스킬이 get_context() → index 읽기 → recall() → 종합 보고

구현 완료, 169 tests PASS, 커밋 + push 완료.

### 9-4. 문서화 누락 — 반복된 실수

active_pipeline 구현 후 파이프라인 문서(00_index.md, impl-log, review-log)를 갱신하지 않고 커밋. Paul이 지적. **이전 세션에서도 동일한 지적을 받은 후의 반복.**

### 9-5. 근본 원인 추적

#### 초기 진단 (이 세션의 Claude)
"common-mistakes.md 체크리스트에 파이프라인 문서 항목이 없어서"

#### 교정 (옆 Opus 세션)
- common-mistakes는 **사후 안전망**이다. 주 시스템은 08_documentation-system.
- /pipeline은 **Skill 계층(강)**인데 Claude가 안 불렀다. 계층이 약한 게 아니라 호출을 안 한 것.
- 왜? Claude의 훈련된 기본 행동이 "프로세스 세팅"보다 "문제 해결"을 우선한다.

#### 심화 (양쪽 Opus 종합)

**두 레이어의 실패:**

| Layer | 문제 | 설명 |
|-------|------|------|
| **Layer 1: 진입 실패** | 08 시스템에 안 들어간다 | /pipeline 규칙이 있어도 Claude의 "문제 해결 모드"가 우선. 코드부터 짬 |
| **Layer 2: 이탈** | 들어가도 빠져나온다 | /pipeline으로 시작해도 구현 몰입 시 index 안 씀. 커밋 시점에 문서 누락 |

**유기적 전환(Organic Transition) 패턴:**

Pipeline 트리거는 이산적 신호를 전제한다:
```
"시작하자" → /pipeline → 작업
```

현실은 연속적 전환이다:
```
논의 → 분석 → "그럼 고치자" → 코드 → "어, 이미 구현하고 있네"
```

이 세션에서 정확히 이 패턴이 발생했다:
```
Paul: "compact 후에 흐려진다"     ← 문제 제시
Claude: 분석 → 두 레이어 식별     ← 문제 해결 모드
Paul: "가자"                      ← 실행 신호 (트리거 목록에 없음)
Claude: 코드 → 테스트 → 커밋     ← 08 시스템 바이패스
```

"가자"는 rules/workflow.md의 트리거 목록("시작하자"/"만들자"/"분석하자")에 없다. 하지만 트리거 목록을 아무리 늘려도 유기적 전환은 안 잡힌다. **언어는 무한하니까.**

### 9-6. 현재 상태

| 항목 | 상태 |
|------|------|
| 08 시스템 = 설계 의도 | **운영체제** (모든 작업이 이 안에서 시작/진행/종료) |
| 08 시스템 = 현실 | **참조 자료** (가끔 읽히지만, Claude의 기본 행동을 지배하지 않음) |
| Claude의 실제 운영체제 | 코드 짜기 → 테스트 → 커밋 (08 시스템 바깥) |
| common-mistakes.md | 08 미준수의 **증거이자 사후 패치** |

---

## 10. 해법 제안 (논의 중, 미확정)

### 10-1. 옆 Opus의 제안: 행동 감지 Hook

```
Claude가 소스 파일에 Edit/Write 실행 (01_projects/ 내)
→ Hook: "이 세션에서 /pipeline 발동했나?"
→ 안 했으면: "⚠️ 활성 파이프라인 없이 소스 수정 중. /pipeline 먼저 실행하세요."
```

장점:
- 유기적 전환도 감지 (언어가 아니라 **행동**을 감지)
- Hook = 최강 계층 (회피 불가)
- 트리거 목록이 필요 없음

### 10-2. Layer 2(이탈) 방지: 커밋 시 index 체크

```
git commit 시점
→ Hook: "활성 파이프라인이 있는데 00_index.md가 이 커밋에 포함 안 됨"
→ 경고
```

### 10-3. 이 세션 Claude의 수정 제안

**차단(block)이 아니라 경고(warn).** 이유:
- 1줄 수정, 설정 변경에도 pipeline 요구하면 마찰 과도
- 경고는 Claude의 **active attention**에 08 시스템을 강제 노출 (lost-in-the-middle 방지)
- 경미한 수정은 Claude가 판단해서 무시 가능

### 10-4. 열린 질문

1. 경고 vs 차단 — 어느 수준이 적절한가?
2. 경로 필터 — `01_projects/` 소스만? `~/.claude/` 설정도?
3. Layer 2 — 커밋 시 index 체크로 충분한가, 아니면 더 강한 게 필요한가?
4. 10_index-system 활성화 — 에코시스템 자기인식이 이 문제에 기여할 수 있는가?
5. 09_cascade 자동화 — Claude 판단에 맡기지 않고 자동 발동 가능한가?
6. common-mistakes.md를 점진적으로 불필요하게 만들 수 있는가?

---

## 11. 관련 파일 경로 총정리

### 설정
| 파일 | 경로 | 역할 |
|------|------|------|
| settings.json | `~/.claude/settings.json` | Hook, Plugin, MCP 설정 |
| CLAUDE.md (전역) | `~/.claude/CLAUDE.md` | 전역 개인 규칙 |
| CLAUDE.md (공유) | `/c/dev/CLAUDE.md` | 프로젝트 공유 규칙 |
| CLAUDE.md (orchestration) | `/c/dev/01_projects/01_orchestration/.claude/CLAUDE.md` | 프로젝트별 규칙 |
| common-mistakes.md | `~/.claude/rules/common-mistakes.md` | 반복 실수 방지 |
| workflow.md | `~/.claude/rules/workflow.md` | 워크플로우 규칙 |
| MEMORY.md | `~/.claude/projects/C--dev/memory/MEMORY.md` | 자동 메모리 |

### Hook 파일
| 파일 | 경로 | 트리거 |
|------|------|--------|
| session-start.sh | `~/.claude/hooks/session-start.sh` | SessionStart |
| auto_remember.py | `~/.claude/hooks/auto_remember.py` | PostToolUse (Write/Edit/Bash) |
| relay.py | `~/.claude/hooks/relay.py` | PostToolUse (relay window) |
| pre-compact.sh | `~/.claude/hooks/pre-compact.sh` | PreCompact |
| pre-tool-use.sh | `~/.claude/hooks/pre-tool-use.sh` | PreToolUse (Bash) |
| governance-audit.sh | `~/.claude/hooks/governance-audit.sh` | PreToolUse (Bash) |
| post-tool-live-context.sh | `~/.claude/hooks/post-tool-live-context.sh` | PostToolUse (Write/Edit) |
| notify-sound.py | `~/.claude/hooks/notify-sound.py` | Notification |

### Skills
| 스킬 | 경로 | 역할 |
|------|------|------|
| /pipeline | `~/.claude/skills/pipeline/SKILL.md` | 파이프라인 생성 (08 시스템 진입점) |
| /session-end | `~/.claude/skills/session-end/SKILL.md` | 세션 종료 체인 |
| /restore | `~/.claude/skills/restore/SKILL.md` | compact 후 복구 |
| /checkpoint | `~/.claude/skills/checkpoint/SKILL.md` | 미저장 기억 추출 |
| /cascade | `~/.claude/skills/cascade/SKILL.md` | 대용량 소스 읽기 |

### Agents
| 에이전트 | 경로 | 모델 | 역할 |
|----------|------|------|------|
| compressor | `~/.claude/agents/compressor.md` | Sonnet | 세션 종료 5단계 |
| code-reviewer | `~/.claude/agents/code-reviewer.md` | Opus | 코드 리뷰 |
| commit-writer | `~/.claude/agents/commit-writer.md` | Haiku | 커밋 메시지 |
| meta-orchestrator | `~/.claude/agents/meta-orchestrator.md` | Opus | 디스패치 허브 |

### 08/09/10 시스템
| 파일 | 경로 | 역할 |
|------|------|------|
| principles.md | `08_documentation-system/foundation/principles.md` | 폴더/네이밍/번호 규칙 |
| phase-guide.md | `08_documentation-system/foundation/phase-guide.md` | 라이프사이클 방법론 |
| 09 principles.md | `09_context-cascade-system/foundation/principles.md` | 읽기 인프라 원칙 |
| INDEX.md | `10_index-system/views/INDEX.md` | 에코시스템 인덱스 |

### mcp-memory 핵심
| 파일 | 경로 | 역할 |
|------|------|------|
| server.py | `06_mcp-memory/server.py` | MCP 서버 엔트리포인트 |
| save_session.py | `06_mcp-memory/tools/save_session.py` | 세션 그래프 저장 |
| get_context.py | `06_mcp-memory/tools/get_context.py` | 컨텍스트 반환 (+ active_pipeline) |
| config.py | `06_mcp-memory/config.py` | 온톨로지 상수 |
| sqlite_store.py | `06_mcp-memory/storage/sqlite_store.py` | DB 스키마 + CRUD |

### 이 논의가 진행된 파이프라인
| 파일 | 경로 |
|------|------|
| 마스터 인덱스 | `01_orchestration/01_ideation/2026-03-11-session-chain-redesign/00_index.md` |
| 대담 원문 | `위 경로/20_ideation/01_dialogue.md` (Exchange 12-14) |
| 구현 기록 | `위 경로/30_impl/03_impl-log.md` (Phase 6) |
| 리뷰 기록 | `위 경로/40_review/04_review-log.md` (§4) |
| 이 문서 | `위 경로/21_ideation-r2/01_opus-system-briefing.md` |

---

## 12. 요청 사항

이 문서를 읽은 후, 다음에 대해 판단해주기를 요청한다:

1. **진단 검증**: "08 시스템이 운영체제가 아니라 참조 자료로 기능하고 있다"는 진단이 정확한가?
2. **행동 감지 Hook**: Edit/Write 행동을 감지해서 pipeline 여부를 체크하는 접근이 적절한가? 더 나은 방법이 있는가?
3. **Layer 2 (이탈) 방지**: 파이프라인에 진입한 후에도 이탈하는 문제를 어떻게 잡는가?
4. **common-mistakes.md의 미래**: 08 시스템이 제대로 작동하면 common-mistakes가 불필요해진다는 가설이 맞는가?
5. **놓친 것**: 이 분석에서 빠진 관점이나 보이지 않는 문제가 있는가?
