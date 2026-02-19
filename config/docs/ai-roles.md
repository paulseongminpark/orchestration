# AI별 역할

## 역할 매트릭스

| AI | 역할 | 접근 | 쓰기 | 비용 특성 |
|----|------|------|------|----------|
| Claude Code | 실행+기록 | 로컬 파일, Git | ✅ 유일 | 턴 당 과금 |
| Claude Chat | 설계 토론 | 대화만 | ❌ | Opus 사용 시 주의 |
| GPT Plus | 전략, Canvas | GitHub Pages URL | ❌ | 무제한 (Plus) |
| Gemini Pro | 대량 검증 | GitHub Pages URL | ❌ | 100만 토큰 무료 |
| Perplexity Pro | 리서치 | 웹 + GitHub Pages | ❌ | 무제한 (Pro) |

## Claude Code (실행자)

**왜 실행자인가**: 유일하게 파일을 직접 읽고, 쓰고, Git push까지 할 수 있다.

### 3가지 에이전트 모드

| 에이전트 | 모델 | 역할 | 사용 시점 |
|---------|------|------|----------|
| @reader | Haiku 4.5 | 파일 탐색, 구조 파악 | 먼저 읽고 이해할 때 |
| @executor | Sonnet 4.5 | 코드 생성/수정 | 실제 작업 (기본값) |
| @architect | Opus 4.6 | 시스템 설계 | 큰 결정 (하루 10-15회) |

### Skills (사용자가 호출하는 명령)

**프로젝트별**:

| Skill | 동작 | 위치 |
|-------|------|------|
| `/sync` | STATE.md 갱신 → git commit → push | orchestration, portfolio |
| `/handoff <ai> <내용>` | 다른 AI용 핸드오프 문서 생성 | orchestration |
| `/status` | 현황 요약 (Haiku 서브에이전트) | orchestration, portfolio |

**글로벌** (`~/.claude/skills/`):

| Skill | 동작 |
|-------|------|
| `/morning` | 전체 프로젝트 브리핑 (Haiku) |
| `/sync-all` | 3개 repo 일괄 커밋+푸시 |
| `/memory-review` | Auto Memory 주간 정리 |
| `/research` | Perplexity 스타일 리서치 |
| `/todo` | TODO.md 관리 |
| `/token-check` | 현재 컨텍스트 토큰 확인 |
| `/token-mode` | 토큰 절약 모드 전환 |
| `/verify` | 프로젝트 규칙 검증 |
| `/verify-log-format` | 로그 포맷 검증 |
| `/verify-project-rules` | 프로젝트 규칙 전체 검증 |

### Hooks (자동 트리거)

| 이벤트 | 동작 |
|--------|------|
| SessionStart | `/clear` 실행 후 `/morning` Skill 실행 → 전체 프로젝트 브리핑 |
| PostToolUse (Edit/Write) | STATE.md/CLAUDE.md/docs 변경 시에만 "/sync 권장" (정밀 matcher) |
| PostToolUse (Edit/Write) | auto prettier (포트폴리오, .tsx/.ts/.css/.json만) |
| Stop | Evidence 백업 (copy-session-log.py → 03_evidence/) |
| Stop | STATE.md 미커밋 차단 (/sync 가드, exit 1) |
| Stop | Auto Memory 분석 (analyze-session.sh → pending.md) |

→ 상세: [[claude-code-guide]]

## GPT Plus (사고 확장자)

**왜 GPT인가**: Canvas로 옵션 비교가 시각적이고, 대화형 설계 토론에 강하다.

### 운영 모드

**log 모드**: 결정 추적
```
[Decision] Phase 1 폴더 구조 확정 — Jeff Su 방법론, 5레벨 MAX
[Pending] Obsidian 플러그인 선택 — obsidian-git vs manual
[Discarded] .claudeignore 사용 — 보안 이슈로 폐기
```

**tracker 모드**: 진행 상황
```
TRACKER (2026-02-15)
[오늘] Phase 1-6 실행 완료
[앞으로] Skills 테스트, Obsidian 검증
[DECISION CANDIDATE] workout_project를 01_projects로 이동할지
```

### Packet 시스템

GPT의 사고를 Claude의 행동으로 번역하는 프로토콜:

```
[PACKET]
PROJECT=orchestration        ← 어떤 프로젝트
AGENT: @executor             ← 어떤 에이전트
EVENTS: [Decision]           ← 무슨 결정
STATE_UPDATES: (변경)         ← STATE에 뭘 반영
EXECUTE: (명령)               ← Claude에게 무엇을 시킬지
[/PACKET]
```

**사용 흐름**:
1. GPT와 토론 → 결정 도출
2. GPT가 Packet 생성
3. 사용자가 승인
4. Packet을 Claude Code에 붙여넣기
5. Claude가 실행

### Claude 지시문 형식

GPT가 Claude에게 보내는 작업 지시:
```
AGENT: @executor
READ_ALLOW: context/STATE.md, src/ui3/Page.tsx
CHANGE_ONLY: src/ui3/Page.tsx
NON-GOALS: 다른 컴포넌트 수정 금지
BUNDLE: Page.tsx + styles.css 한 턴에 처리
```

## Gemini Pro (검증자)

**왜 Gemini인가**: 100만 토큰 컨텍스트. 대량 코드를 한 번에 읽고 검증할 수 있다.

### 사용 시나리오

1. **구조 검증**: 전체 폴더 구조가 규칙을 지키는지
2. **코드 리뷰**: 큰 리팩토링 후 전체 코드 검증
3. **STATE 완전성**: STATE.md가 실제 상태를 정확히 반영하는지

### 출력 형식

```
[gemini-review]
통과: 5개 / 실패: 2개
실패 항목:
- 넘버링 중복: 01_orchestration과 01_projects 혼동 가능 → 명확한 경로 사용 권장
- STATE 섹션: "막힌 것" 섹션 누락 → 추가 필요
```

## Perplexity Pro (리서처)

**왜 Perplexity인가**: 웹 검색 + AI 분석을 결합. 소스 URL이 항상 붙는다.

### 사용 시나리오

1. **기술 검증**: "Claude Code hooks에 onFileWrite가 실제로 있나?"
2. **최신 정보**: "React 19의 새 기능은?"
3. **교차검증**: GPT가 제안한 방법이 실제로 작동하는지

### Spaces 구성

| Space | 범위 | 특화 |
|-------|------|------|
| 오케스트레이션 | AI 워크플로우, Claude Code, Git | 시스템 설계 리서치 |
| 포트폴리오 | React, Vite, CSS, UX | 웹 개발 리서치 |

### 출력 형식

```
[perplexity-research]
주제: Claude Code hooks PostToolUse matcher 문법
결론: matcher는 tool 이름의 regex 패턴. path matcher는 별도 지원 안 함.
소스:
- docs.anthropic.com/...: 공식 hooks 문서
- github.com/anthropics/...: 설정 예제
Claude 실행 지침:
1. settings.json의 matcher를 "Edit|Write"로 설정
2. command에서 $TOOL_INPUT_PATH로 경로 필터링
```

## 워크플로우: AI 간 협업

```
1. 문제 발생
   │
2. Perplexity로 리서치 ──→ [perplexity-research] 결과
   │
3. GPT로 전략 토론 ──→ [PACKET] + Claude 지시문
   │
4. 사용자 승인
   │
5. Claude Code 실행 ──→ 코드 수정 + git push
   │
6. (필요 시) Gemini로 검증 ──→ [gemini-review] 결과
   │
7. Claude Code로 수정 반영
```

## 관련 문서
- [[philosophy]] — 역할 분리의 이유
- [[daily-workflow]] — 실제 사용 예시
- [[claude-code-guide]] — Claude Code 상세
