# Claude Code 심화 가이드

## CLAUDE.md 계층 구조

```
~/.claude/CLAUDE.md              <- 글로벌 (매 턴 자동, 모든 프로젝트)
~/.claude/rules/*.md             <- 글로벌 규칙 모듈 (매 턴 자동)
{project}/.claude/CLAUDE.md      <- 프로젝트별 (해당 cwd에서만)
{project}/.claude/rules/*.md     <- 프로젝트 규칙 (조건부 로드)
MEMORY.md                        <- 자동 메모리 (200줄, 세션 간 유지)
```

### 현재 설정

**글로벌** (`~/.claude/CLAUDE.md`) — 4줄:
```
- Executor. 간결 출력: DONE/FILES/NEXT
- 불확실 -> 보류+이유. 범위 밖 금지.
- 한국어. "ㅇㅇ해" = 즉시 실행.
- 파일 재읽기 금지.
```

**글로벌 규칙** (`~/.claude/rules/`):
- `common-mistakes.md`: 반복 실수 패턴 방지
- `workflow.md`: 작업 흐름 및 에이전트 사용 기준

**프로젝트** (`01_orchestration/.claude/CLAUDE.md`):
- SoT 위치, Architecture, Skills 목록, Pages URL

**프로젝트** (`02_portfolio/.claude/CLAUDE.md`):
- 기술 스택, 컨벤션, 주요 파일, Skills 목록

## Skills

### 구조

```
{project}/.claude/skills/{name}/SKILL.md
~/.claude/skills/{name}/SKILL.md          <- 글로벌
```

### 현재 등록된 Skills

**글로벌** (`~/.claude/skills/`):

| Skill | 동작 |
|-------|------|
| `/morning` | 모든 프로젝트 STATE 읽기 -> 전체 브리핑 |
| `/sync-all` | orchestration + portfolio + dev-vault 일괄 커밋+푸시 |
| `/verify` | 통합 검증 (브랜치/STATE/커밋/LOG 형식) |
| `/todo` | TODO.md 관리 (INBOX 동기화) |
| `/docs-review` | stale 문서 점검 |
| `/session-insights` | 토큰 사용량/비용 분석 |
| `/memory-review` | Auto Memory 주간 정리 |
| `/research` | 딥 리서치 워크플로우 |

**프로젝트별**:

| Skill | 위치 | 동작 |
|-------|------|------|
| `/sync` | orchestration, portfolio | STATE.md 갱신 -> git commit -> push |
| `/handoff` | orchestration | AI별 핸드오프 문서 생성 |

## Hooks

### 현재 설정 (v2.2)

| 이벤트 | 동작 |
|--------|------|
| SessionStart | 오늘 LOG tail-30 + 미커밋 상태 + decisions.md 미반영 항목 |
| PostToolUse (Write/Edit) | stdin JSON에서 file_path 추출, context/*.md 변경 알림 |
| PreToolUse (Bash) | 위험 명령 차단 (rm -rf, force push) - 페일클로즈 |
| PreCompact | /verify 권장 알림 |
| SessionEnd | 미커밋 현황 + /sync 권장 + Auto Memory 분석 |
| TeammateIdle | 유휴 상태 정보 메시지 (비차단) |

## Custom Agents (v2.2)

15개 에이전트 (`~/.claude/agents/`):

**PROACTIVELY (자동 감지):**
- code-reviewer (Opus): 구현 완료 시
- commit-writer (Haiku): 커밋 필요 시
- compressor (Sonnet): 세션 마무리 시
- orch-state (Sonnet): 방향 파악 시

**Portfolio:** pf-context, pf-reviewer, pf-deployer
**Orchestration:** orch-doc-writer, orch-skill-builder
**Monet-lab:** ml-experimenter, ml-porter
**기타:** morning-briefer, content-writer, gemini-analyzer, security-auditor

## MEMORY.md

세션 간 기억 유지 자동 메모리 시스템.
- 위치: `~/.claude/projects/{project-hash}/memory/MEMORY.md`
- 매 세션 시작 시 자동 로드 (200줄까지)

## 관련 문서
- [[architecture]] — 전체 구조에서의 위치
- [[ai-roles]] — AI별 역할
