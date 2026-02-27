# HOW I AI — Context as Currency

> v4.0 | 2026-02-27 | 7일간의 AI 오케스트레이션 시스템 설계 기록

---

## 1. 시작: 왜 오케스트레이션인가

Claude Code 하나로 시작했다. 파일을 읽고, 코드를 쓰고, 커밋했다. 문제는 **맥락**이었다.

세션이 바뀌면 어제의 결정이 사라졌다. 프로젝트를 옮기면 다른 프로젝트의 변경이 보이지 않았다. CLI를 바꾸면 이전 CLI의 작업이 증발했다. 200K 토큰 컨텍스트 윈도우는 무한하지 않았고, 매번 같은 파일을 읽어 들이는 데 예산의 절반을 썼다.

그래서 시스템을 만들기 시작했다. 처음에는 에이전트 몇 개. 그다음 팀 구조. 그러고는 멀티 CLI 연동. 7일 만에 24개 에이전트를 만들었다가, 다시 15개로 줄였다.

**이 문서는 그 7일의 기록이다.** 무엇을 만들었고, 왜 그렇게 결정했고, 어떻게 "빼기"가 "더하기"보다 더 나은 시스템을 만들었는지.

---

## 2. 설계 철학: Context as Currency

### 토큰은 화폐다

200K 토큰 컨텍스트 윈도우. 이것이 매 세션의 총예산이다.

```
200K 세션 예산
├── Baseline:     ~42K (고정 — 시스템 프롬프트, 규칙, 메모리)
├── 작업 Phase:   42K → 100K (~20-30 턴, 실제 작업)
├── Compact 후:   ~50K → 100K (2차 작업)
├── 체인 예약:    ~25K (.chain-temp 오프로딩)
└── Auto-compact: 150K (최후 방어선)
```

모든 설계 결정은 이 예산 제약 안에서 이루어졌다. 에이전트를 추가하면 baseline이 올라간다. 문서를 늘리면 읽기 비용이 증가한다. 스킬을 등록하면 시스템 프롬프트가 커진다.

**v4.0의 핵심 통찰: 시스템의 가치는 구성요소의 수가 아니라, 구성요소 하나당 토큰 효율이다.**

### 세 가지 원칙

1. **Baseline 최소화** — 세션 시작 시 고정 비용을 줄인다
2. **오프로딩** — 긴 결과는 파일에 쓰고, 메인 컨텍스트엔 1줄 요약만
3. **계층적 위임** — Haiku(수집) → Sonnet(분석) → Opus(설계/검증)

---

## 3. 시스템 토폴로지 (v4.0)

### 에이전트 15개, 4팀 + 디스패치 허브

```
                    ┌─────────────────────┐
                    │  meta-orchestrator  │
                    │   (Opus, /dispatch) │
                    └─────────┬───────────┘
                              │
          ┌───────────┬───────┴───────┬────────────┐
          ▼           ▼               ▼            ▼
    ┌─────────┐ ┌──────────┐  ┌───────────┐ ┌──────────┐
    │   ops   │ │  build   │  │  analyze  │ │ maintain │
    │ daily   │ │ code     │  │ ai        │ │ compress │
    │ -ops    │ │ -reviewer│  │ -synth    │ │ -or      │
    │ (Haiku) │ │ (Opus)   │  │ (Opus)    │ │ (Opus)   │
    │         │ │          │  │           │ │          │
    │ tr-ops  │ │ pf-ops   │  │ gemini    │ │ doc-ops  │
    │         │ │ security │  │ codex     │ │          │
    └─────────┘ └──────────┘  └───────────┘ └──────────┘

    크로스팀 유틸리티: commit-writer, orch-state, project-context
    리좀 연결자:      linker ◆── live-context.md + .ctx/shared-context.md
```

### 리좀 구조의 의미

전통적 트리 구조가 아니다. 어떤 에이전트든 `linker`를 통해 다른 팀과 연결된다. `code-reviewer`가 보안 이슈를 발견하면 `security-auditor`로 직접 연결. `daily-ops`가 portfolio 변경을 감지하면 `project-context`가 즉시 맥락을 제공.

이 "리좀"은 물리적 연결이 아니라 **공유 상태(shared state)**를 통한 간접 연결이다:
- `_auto/live-context.md` — 세션 내 실시간 맥락 (100줄 캡, auto-trim)
- `.ctx/shared-context.md` — Cross-CLI 공유 상태
- `.ctx/provenance.log` — 출처 추적 ([claude], [gemini], [codex])

### 모델 전략

| 역할 | 모델 | 비용 | 예시 |
|------|------|------|------|
| 수집/요약 | Haiku | $ | daily-ops, commit-writer, linker |
| 분석/검색 | Sonnet | $$ | tr-ops, pf-ops, doc-ops, project-context |
| 설계/검증 | Opus | $$$ | code-reviewer, ai-synthesizer, compressor, meta-orchestrator |

**Opus는 발견을 위해 쓴다.** 단순 실행이 아니라 숨겨진 문제, 패턴, 리스크를 자발적으로 탐색하는 것이 Opus의 차별점.

---

## 4. 핵심 결정 — 빼기의 미학

7일간 16개 아키텍처 결정(D-009~D-024)을 내렸다. 그중 시스템의 방향을 바꾼 6가지.

### DECISION 1: Source of Truth 확립 (v3.2)

**문제**: 문서가 여기저기 흩어져 있었다. 어떤 파일이 최신인지 알 수 없었다.

**결정**: 4개 문서로 SoT 확립.
- `STATE.md` — 시스템 인벤토리 (무엇이 있는가)
- `CLAUDE.md` — 에이전트 체인 (어떻게 작동하는가)
- `KNOWLEDGE.md` — 패턴과 규칙 (왜 그렇게 하는가)
- `PLANNING.md` — ADR (왜 그렇게 결정했는가)

**영향**: 이후 모든 변경은 이 4개 파일을 갱신해야만 "완료". Living Docs 패턴의 시작.

### DECISION 2: 리좀형 팀 재설계 (v3.2)

**문제**: 에이전트가 늘어나면서 누가 누구에게 보고하는지 혼란.

**결정**: 4팀(ops/build/analyze/maintain) + 디스패치 허브(meta-orchestrator) + 리좀 연결자(linker).

**핵심 인사이트**: 팀 구조는 "명령 체계"가 아니라 "책임 범위". 크로스팀 유틸리티(commit-writer, orch-state, project-context)는 어느 팀에도 속하지 않고 모든 팀이 사용.

### DECISION 3: Verify Barrier (v3.3)

**문제**: 외부 CLI(Gemini, Codex)의 출력을 그대로 신뢰할 수 없다.

**결정**: 3단계 검증 — 구조 검사 → 교차 검증 → 스팟체크 반박.

```
Gemini 벌크 추출
        ↓
Codex 정밀 검증
        ↓
ai-synthesizer verify barrier (Opus)
  ├── 1단계: 구조 (_meta 블록 확인)
  ├── 2단계: 교차 (원본과 대조)
  └── 3단계: 스팟체크 (의도적 반박 시도)
        ↓
    GO / NO-GO
```

**원칙**: "Claude = 유일한 설계/결정권자. 외부 CLI는 추출만, 해석 금지."

### DECISION 4: .chain-temp 오프로딩 (v3.3.1)

**문제**: 코드 리뷰 결과가 수천 줄. 메인 컨텍스트를 잡아먹었다.

**결정**: 체인 에이전트 결과를 `.chain-temp/` 파일로 오프로딩. 메인 컨텍스트엔 1줄 요약만 반환.

```
code-reviewer → .chain-temp/review-2026-02-27.md
  메인에는: "3 RED, 2 YELLOW"

gemini-analyzer → .chain-temp/gemini-2026-02-27.txt
  메인에는: "추출 47건"
```

다음 체인 에이전트는 `.chain-temp/` 파일을 직접 Read. 메인 컨텍스트 오염 없이 체인이 이어진다.

**절감 효과**: 체인당 ~25K 토큰 절약.

### DECISION 5: Flat Root 구조 (v3.3.1)

**문제**: `context/`, `docs/`, `config/docs/`... 문서를 찾으려면 3단계 디렉토리를 탐색해야 했다.

**결정**: Living Docs 12개를 루트로 올린다.

```
orchestration/
├── *.md (12개)       # 루트에서 바로 접근
├── _history/         # 시간순 기록 (읽기 전용)
├── _prompts/         # 외부 AI 프롬프트
├── _auto/            # 자동 관리
└── scripts/          # 훅 스크립트
```

**인사이트**: 디렉토리 깊이 = 탐색 비용 = 토큰 비용. 가장 자주 읽는 파일을 가장 가까이.

### DECISION 6: Context as Currency (v4.0)

v4.0의 제목이자 철학. 이전 5개 결정의 귀결.

**문제**: v3.3에서 에이전트 24개, 스킬 14개까지 늘렸다. 시스템은 강력해졌지만, baseline이 비대해졌다. 세션 시작만으로 42K를 소비하는데, 에이전트를 더 만들면 이 비용이 계속 올라간다.

**결정**: 빼기.

| 항목 | Before (v3.3) | After (v4.0) | 변화 |
|------|---------------|--------------|------|
| Agents | 24 | 15 | -37.5% |
| Skills | 14 | 9 | -35.7% |
| CLAUDE.md | 74줄 | 38줄 | -48.6% |
| disable-model-invocation | 일부 | 전체 | 스킬이 모델 호출 차단 |

**동시에 더하기**:
- **rulesync v7.9.0**: `.rulesync/rules/` SoT 하나에서 `CLAUDE.md`, `GEMINI.md`, `AGENTS.md` 자동 생성. 규칙 동기화 비용 → 0.
- **.ctx/ Cross-CLI 공유 메모리**: Claude/Gemini/Codex가 같은 `shared-context.md`를 읽고 쓴다. CLI 전환 시 맥락 소실 → 0.
- **Worktree 인프라**: 격리된 작업 환경 + `/handoff` 스킬로 CLI 간 작업 위임.
- **AUTOCOMPACT 50%**: 100K에서 자동 압축 (기존 75%).

**핵심**: 구성요소를 줄이면서 기능은 늘렸다. 에이전트를 병합하니 한 에이전트가 더 많은 책임을 가졌고, memory:user로 세션 간 학습이 가능해졌다. 스킬에 disable-model-invocation을 걸어 불필요한 모델 호출을 차단했다.

---

## 5. 멀티 AI 오케스트레이션

하나의 AI로 모든 것을 하는 것은 비효율적이다. 각 AI의 강점이 다르다.

### 역할 분담

```
┌─────────────────────────────────────────────────────┐
│                  Claude Code (Opus 4.6)              │
│            유일한 설계/결정권자 + 코드 작성            │
│                 + Verify Barrier 최종 판단            │
└──────────┬──────────────┬──────────────┬────────────┘
           │              │              │
     ┌─────▼─────┐ ┌─────▼──────┐ ┌────▼──────────┐
     │ Codex CLI │ │ Gemini CLI │ │ Perplexity Pro│
     │ (GPT-5.3) │ │(3.1 Pro)   │ │(sonar-deep)   │
     │           │ │            │ │               │
     │ 정밀 검증  │ │ 벌크 추출   │ │ 리서치         │
     │ diff 리뷰  │ │ 컨텍스트    │ │ tech-review   │
     │ 포맷 QA   │ │ 오프로딩    │ │ 소스          │
     │ git 추출  │ │ 웹 검색    │ │               │
     │           │ │            │ │               │
     │ 5h 롤링   │ │ 1M 컨텍스트 │ │ deep research │
     └───────────┘ └────────────┘ └───────────────┘
```

### Cross-CLI 메모리

CLI를 전환할 때마다 맥락이 사라지는 문제. v4.0에서 `.ctx/` 디렉토리로 해결.

```
.ctx/
├── shared-context.md    # 현재 목표 / 진행 중 / 최근 완료
├── provenance.log       # [claude] / [gemini] / [codex] 출처 마커
├── gemini/              # Gemini CLI 결과
└── codex/               # Codex CLI 결과
```

**SessionStart hook**이 세션 시작 시 `.ctx/shared-context.md`를 자동 표시. **TaskCompleted hook**이 태스크 완료 시 자동 갱신. `/handoff` 스킬이 CLI 간 작업 위임 시 컨텍스트를 정리.

### 규칙 동기화: rulesync

3개 CLI의 규칙을 수동으로 동기화하는 것은 불가능했다.

```
.rulesync/
├── rulesync.jsonc       # 설정 (targets: claudecode/geminicli/codexcli)
└── rules/
    ├── global.md        # 공유 규칙 (모든 CLI)
    ├── claude.md        # Claude 전용
    ├── gemini.md        # Gemini 전용
    └── codex.md         # Codex 전용

→ `rulesync generate` 1회 실행
→ CLAUDE.md, GEMINI.md, AGENTS.md 자동 생성
```

SoT는 `.rulesync/rules/` 하나. 나머지는 파생물.

---

## 6. 에이전트 체인

에이전트는 혼자 동작하지 않는다. 체인으로 연결된다.

### 구현 체인 (가장 빈번)

```
implement → code-reviewer(Opus) → commit-writer(Haiku) → linker(Haiku)
```

1. 코드를 작성한다
2. `code-reviewer`가 버그/보안/성능/가독성을 점검하고 `.chain-temp/`에 상세 리뷰 저장
3. `commit-writer`가 `[project] 한줄 설명` + `Co-Authored-By:` 형식으로 커밋 생성
4. `linker`가 크로스 프로젝트 영향을 감지하고 다른 프로젝트에 TODO/알림 생성

### 추출/검증 체인

```
Gemini 벌크 추출 → Codex 정밀 검증 → ai-synthesizer verify barrier → 사용
```

외부 CLI의 출력은 절대 바로 사용하지 않는다. 반드시 verify barrier를 통과해야 한다.

### 압축 체인

```
compressor 9단계 → doc-ops(항상) → doc-ops verify
```

컨텍스트가 100K에 도달하면 9단계 압축:
1. 핵심 결정 추출
2. 완료 작업 정리
3. 다음 할 일 명시
4. 파일명+라인 번호 보존
5. 실패 기록 보존 (Preserve Failures)
6. Attention Manipulation (중요도 가중치)
7. 200자 이내 압축
8. doc-ops가 Living Docs 갱신
9. doc-ops가 자기 작업 검증

---

## 7. Hooks: 자동화 레이어

8종 hook이 시스템의 반사 신경 역할을 한다.

| Hook | 트리거 | 하는 일 |
|------|--------|---------|
| **SessionStart** | 세션 시작 | 미커밋 경고 + 미결정 ❌ 5건 + live-context 5줄 + .ctx/ 공유 상태 |
| **SessionEnd** | 세션 종료 | 미커밋 현황 + MEMORY.md 줄 수 경고 |
| **PreToolUse** | Bash 실행 전 | `rm -rf`, `force push` 등 위험 명령 차단 |
| **PostToolUse** | Write/Edit 후 | `live-context.md` auto-append + auto-trim (100줄 캡) |
| **PreCompact** | compact 전 | 스냅샷 생성 + 미커밋 경고 |
| **TaskCompleted** | 태스크 완료 | 알림 + `.ctx/shared-context.md` 자동 갱신 |
| **TeammateIdle** | 팀원 유휴 | 유휴 알림 (리더에게) |
| **Notification** | 시스템 알림 | 범용 알림 |

**설계 원칙**: Hook은 "수동으로 하면 잊는 것"을 자동화한다. 미커밋 경고, live-context 갱신, 위험 명령 차단 — 모두 인간이 실수하는 지점.

---

## 8. 증거: 숫자가 말하는 것

### 시스템 규모

| 지표 | 값 |
|------|-----|
| Agents | 15 (v3.3: 24) |
| Skills | 9 (v3.3: 14) |
| Teams | 4 + 디스패치 허브 |
| Hooks | 8종 |
| ADRs | 16 (D-009 ~ D-024) |
| Agent Chains | 6종 |
| External CLIs | 3 (Codex, Gemini, Perplexity) |
| Living Docs | 12개 (Flat Root) |
| Plugins | 4 (superpowers, context7, vercel, frontend-design) |

### e2e 검증

- **v3.3 e2e**: 12 시나리오, 26 에이전트 + 12 스킬 + 8 훅 + 5 체인 + 5 팀 + 2 CLI → FAIL 0, WARN 3
- **v4.0 e2e**: 8 시나리오, PASS 4 / FAIL 3 / WARN 1 → FAIL 3건 오탐 확인 후 수정

### Context 효율

| 지표 | v3.3 | v4.0 | 절감 |
|------|------|------|------|
| CLAUDE.md | 74줄 | 38줄 | -48.6% |
| Baseline (추정) | ~55K | ~42K | -23.6% |
| 에이전트 수 | 24 | 15 | -37.5% |
| 스킬 수 | 14 | 9 | -35.7% |

### 활성 프로젝트

5개 프로젝트를 하나의 오케스트레이션 시스템으로 관리:
- **orchestration** — 이 시스템 자체
- **portfolio** — Next.js 포트폴리오
- **tech-review** — Jekyll 기술 블로그 (Perplexity + GitHub Actions)
- **monet-lab** — UI 실험실
- **daily-memo** — 모바일 메모 → GitHub Actions 자동 sync

---

## 9. 진화: 7일간의 기록

```
Day 1 (2/21)  v1.0  ▓░░░░░░░░░  첫 에이전트 3개. 수동 운영.
Day 2 (2/22)  v2.0  ▓▓░░░░░░░░  에이전트 12개. 팀 구조 도입.
Day 3 (2/23)  v3.0  ▓▓▓▓░░░░░░  에이전트 19개. 리좀형 재설계 시작.
Day 4 (2/24)  v3.2  ▓▓▓▓▓░░░░░  SoT 확립. 4팀 + 허브.
Day 5 (2/25)  v3.3  ▓▓▓▓▓▓▓░░░  Codex+Gemini 통합. Verify Barrier. e2e 23/23 PASS.
Day 6 (2/26)  v3.3.1▓▓▓▓▓▓▓▓░░  200K 최적화. .chain-temp. Flat Root.
Day 7 (2/27)  v4.0  ▓▓▓▓▓▓▓▓▓▓  Context as Currency. 24→15. Cross-CLI. rulesync.
```

### 성숙 곡선: 더하기에서 빼기로

```
에이전트 수
    24 ┤                    ╭─╮
       │                 ╭──╯ │
    19 ┤              ╭──╯    │
       │           ╭──╯       │
    15 ┤        ╭──╯          ╰────── v4.0 (빼기)
    12 ┤     ╭──╯
       │  ╭──╯
     3 ┤──╯
       └──┬──┬──┬──┬──┬──┬──┬──
         D1 D2 D3 D4 D5 D6 D7

       ← 더하기 Phase →← 빼기 Phase →
```

**더하기 Phase (Day 1~5)**: 문제를 발견할 때마다 에이전트를 만들었다. 필요했다. 각 에이전트는 실제 문제를 풀었다.

**빼기 Phase (Day 6~7)**: 시스템이 자기 자신의 무게로 느려졌다. Baseline이 비대해지고, 스킬 목록이 시스템 프롬프트를 잡아먹었다. "이 에이전트가 정말 필요한가?"를 물었다.

**결과**: 더 적은 에이전트로 더 많은 일을 했다. 병합된 에이전트는 더 넓은 책임을 가졌고, memory:user로 세션 간 학습이 가능해졌다.

---

## 10. 배운 것

### 시스템에 대해

1. **빼기가 더하기보다 어렵다.** 에이전트를 만드는 건 쉽다. 어떤 에이전트를 없앨지 결정하는 건 어렵다. 하지만 빼기가 시스템을 더 강하게 만든다.

2. **문서가 곧 시스템이다.** Living Docs는 단순한 기록이 아니다. 에이전트가 매 세션 읽는 "실행 가능한 지식"이다. 문서가 틀리면 시스템이 틀리게 동작한다.

3. **Hook이 습관을 만든다.** 미커밋 경고, live-context 갱신, 위험 명령 차단 — 수동으로 하면 잊는 것을 자동화하면 습관이 된다.

4. **SoT는 하나여야 한다.** 같은 정보가 두 곳에 있으면 반드시 diverge한다. rulesync가 이 문제를 해결했다.

### AI에 대해

5. **AI는 도구가 아니라 팀원이다.** 잘 설계된 시스템에서 AI는 "시키는 일"만 하지 않는다. 예상 못 한 문제를 발견하고, 패턴을 인식하고, 개선을 제안한다.

6. **모든 AI를 같은 방식으로 쓰면 안 된다.** Claude는 결정, Gemini는 대량 처리, Codex는 정밀 검증, Perplexity는 리서치. 각자의 강점에 맞는 역할.

7. **신뢰하되 검증하라.** Verify Barrier는 "AI의 출력을 무조건 신뢰하지 않는다"는 원칙의 구현체. 특히 멀티 AI 환경에서 필수.

### 프로세스에 대해

8. **7일이면 충분하다.** 완벽한 설계를 기다리지 않고 만들면서 개선했다. 매일 e2e 테스트를 돌리고, 실패에서 배우고, 다음 날 수정했다.

9. **구현 완료 ≠ 완료.** 코드를 쓰는 것은 절반. Living Docs 갱신 → 커밋 → push → 사용자 보고까지가 진짜 완료.

---

## 11. 다음

- **portfolio에 시스템 쇼케이스**: 이 오케스트레이션 시스템을 portfolio 사이트의 인터랙티브 섹션으로
- **monet-lab 상세페이지**: empty-house, skin-diary
- **tech-review 자동화 강화**: GitHub Actions workflow_dispatch 통합 테스트
- **daily-ops 실전 가동**: /morning, /todo 일일 루틴 정착

---

*이 문서 자체가 이 시스템으로 작성되었다. Claude Code(Opus 4.6)가 설계하고, brainstorming 스킬이 구조를 잡고, 15개 에이전트 중 meta-orchestrator가 방향을 제시했다.*

*— 2026-02-27, 오케스트레이션 시스템 v4.0*
