# Claude Code 심화 가이드

## CLAUDE.md 계층 구조

Claude Code는 실행할 때마다 여러 설정 파일을 자동으로 읽는다.

```
~/.claude/CLAUDE.md              ← 글로벌 (매 턴 자동, 모든 프로젝트)
~/.claude/rules/*.md             ← 글로벌 규칙 모듈 (매 턴 자동)
{project}/.claude/CLAUDE.md      ← 프로젝트별 (해당 cwd에서만)
{project}/.claude/rules/*.md     ← 프로젝트 규칙 (조건부 로드)
MEMORY.md                        ← 자동 메모리 (200줄, 세션 간 유지)
```

### 현재 설정

**글로벌** (`~/.claude/CLAUDE.md`) — 4줄:
```
- Executor. 간결 출력: DONE/FILES/NEXT
- 불확실 → 보류+이유. 범위 밖 금지.
- 한국어. "ㅇㅇ해" = 즉시 실행.
- 파일 재읽기 금지.
```

**글로벌 규칙** (`~/.claude/rules/`):
- `token_budget.md`: 1세션=1목표, 30턴/100K→/compact 권장, 150K+→필수, 탐색은 서브에이전트
- `git_workflow.md`: STATE 변경 시 commit+push, 커밋 메시지 형식

**프로젝트** (`01_orchestration/.claude/CLAUDE.md`):
- SoT 위치, Architecture 설명, Skills 목록, Pages URL

**프로젝트** (`02_portfolio/.claude/CLAUDE.md`):
- 기술 스택, 컨벤션, 주요 파일, Skills 목록

### 토큰 영향

| 파일 | 로드 시점 | 크기 | 매 턴 비용 |
|------|----------|------|-----------|
| 글로벌 CLAUDE.md | 매 턴 | ~100토큰 | ~100 |
| rules/*.md (2개) | 매 턴 | ~200토큰 | ~200 |
| 프로젝트 CLAUDE.md | 매 턴 | ~300토큰 | ~300 |
| MEMORY.md | 매 턴 | ~500토큰 | ~500 |
| **합계** | | | **~1100/턴** |

이전 글로벌 CLAUDE.md만 ~2000토큰/턴이었으므로 대폭 절감.

## Skills

### 구조

```
{project}/.claude/skills/{name}/SKILL.md
~/.claude/skills/{name}/SKILL.md          ← 글로벌
```

### SKILL.md 형식

```markdown
---
name: skill-name
description: 한줄 설명
user-invocable: true          ← /명령어로 호출 가능
allowed-tools: Read, Edit, Bash
context: fork                 ← (선택) 별도 컨텍스트
agent: Explore                ← (선택) 서브에이전트 유형
model: haiku                  ← (선택) 모델 지정
---

## Steps
1. 첫 번째 단계
2. 두 번째 단계

## Output
출력 형식 설명
```

### 현재 등록된 Skills

**프로젝트별**:

| Skill | 위치 | 동작 |
|-------|------|------|
| `/sync` | orchestration, portfolio | STATE.md 읽기 → 세션 작업 반영 → git add + commit + push |
| `/handoff` | orchestration | `<gpt\|gemini\|perplexity> <요청>` → AI별 핸드오프 문서 |
| `/status` | orchestration, portfolio | STATE + git log + git status → 요약 (Haiku) |

**글로벌** (`~/.claude/skills/`):

| Skill | 동작 |
|-------|------|
| `/morning` | 모든 프로젝트 STATE 읽기 → 전체 브리핑 (Haiku) |
| `/sync-all` | 3개 repo (orchestration, portfolio, ai-config) 일괄 커밋+푸시 |
| `/memory-review` | Auto Memory 주간 정리 (pending.md → MEMORY.md 병합/정리) |
| `/research` | Perplexity 스타일 리서치 워크플로우 |
| `/todo` | C:/dev/02_ai_config/docs/TODO.md 관리 |
| `/token-check` | 현재 컨텍스트 토큰 사용량 확인 |
| `/token-mode` | 토큰 절약 모드 전환 (Haiku 서브에이전트 우선) |
| `/verify` | 프로젝트 규칙 검증 |
| `/verify-log-format` | 로그 파일 포맷 검증 |
| `/verify-project-rules` | 프로젝트 전체 규칙 검증 (5레벨, 넘버링 등) |

## Hooks

### 개요

Hooks는 특정 이벤트 발생 시 자동으로 실행되는 셸 명령이다.

**지원되는 이벤트**:
- `SessionStart`: 세션 시작 시 (최초 1회)
- `PreToolUse`: 도구 실행 전
- `PostToolUse`: 도구 실행 후
- `Notification`: 알림 발생 시
- `Stop`: 세션/응답 종료 시

**지원되지 않는 이벤트** (Perplexity 교차검증 결과):
- ~~onFileWrite~~ → PostToolUse + matcher 사용
- ~~onStateChange~~ → PostToolUse + path matcher 사용
- ~~onTokenThreshold~~ → 존재하지 않음, 규칙으로만 관리

### 현재 설정

**settings.json 내 hooks (전 프로젝트 통일)**:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [{
          "type": "slash-command",
          "command": "clear",
          "async": false
        }]
      },
      {
        "hooks": [{
          "type": "slash-command",
          "command": "morning",
          "async": false
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{
          "type": "command",
          "command": "bash -c '...STATE.md|CLAUDE.md|docs 변경 시에만 /sync 권장...'",
          "async": true
        }]
      }
    ],
    "Stop": [
      {
        "hooks": [{
          "type": "command",
          "command": "python C:/dev/01_projects/01_orchestration/scripts/copy-session-log.py {project}"
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "bash -c '...STATE.md 미커밋 시 exit 1로 차단...'"
        }]
      },
      {
        "hooks": [{
          "type": "command",
          "command": "bash ~/.claude/scripts/analyze-session.sh → pending.md (Auto Memory)"
        }]
      }
    ]
  }
}
```

**SessionStart**: `/clear` 실행 후 `/morning` Skill 자동 실행 → 전체 프로젝트 브리핑
**PostToolUse 정밀 matcher**: STATE.md, CLAUDE.md, docs/*.md 변경만 감지 (일반 코드 수정은 무시)
**포트폴리오 추가**: .tsx/.ts/.css/.json 파일에만 prettier 자동 실행
**Stop /sync 가드**: STATE.md가 미커밋 상태면 세션 종료 차단 (exit 1)
**Stop Auto Memory**: `analyze-session.sh` 실행 → 세션 인사이트를 `pending.md`에 축적 → `/sync-all` 또는 `/memory-review` 호출 시 MEMORY.md로 승격

### matcher 문법

- 문자열: 도구 이름 regex (`"Edit|Write"`)
- `$TOOL_INPUT_PATH`: 도구가 조작한 파일 경로 (환경변수)

## Custom Agents

### 구조

```
{project}/.claude/agents/{name}.md
```

### 현재 등록된 에이전트

**architect.md**:
```yaml
name: architect
model: opus
allowed-tools: Read, Glob, Grep, WebSearch, WebFetch
```
- 코드 작성 금지. Decision 문서만 출력
- Output: What / Why / Impact / Trade-offs

**reviewer.md**:
```yaml
name: reviewer
model: haiku
allowed-tools: Read, Glob, Grep, Bash
```
- 체크리스트 기반 검증
- 5레벨 규칙, 넘버링 중복, STATE 섹션, Git 상태, 링크 유효성

## Permissions

### settings.json 내 permissions

**공통 deny 규칙 (전 프로젝트 통일)**:
```json
{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Read(C:/dev/03_evidence/**)",
      "Read(**/.ssh/**)",
      "Read(**/secrets/**)",
      "Bash(rm -rf *)",
      "Bash(rm -r *)",
      "Bash(git push --force*)",
      "Bash(git clean *)",
      "Bash(curl *)",
      "Bash(wget *)"
    ]
  }
}
```

**ai-config 추가 제한**: Edit은 docs/gpt/gemini/perplexity 경로만 허용, git push는 origin main만 허용

### 보안 계층 (deny는 보조)

| 계층 | 역할 | 수준 |
|------|------|------|
| OS 샌드박스 | 파일시스템/네트워크 격리 | 1차 방어 |
| permissions.deny | Claude Code 엔진 차단 | 2차 가드레일 |
| CLAUDE.md 규칙 | 행동 지침 | 3차 소프트 제한 |

- `.claudeignore`는 우회 가능 → 사용 안 함
- `permissions.deny`는 엔진 레벨 차단이지만 절대적이진 않음
- 진짜 민감한 자원은 OS 권한으로 보호하는 것이 원칙

## MEMORY.md

### 역할

세션 간 기억을 유지하는 자동 메모리 시스템.

- 위치: `~/.claude/projects/{project-hash}/memory/MEMORY.md`
- 매 세션 시작 시 자동 로드 (200줄까지)
- Claude가 스스로 판단하여 기록/수정

### 기록 대상

- 안정적 패턴, 아키텍처 결정
- 사용자 선호 (언어, 도구, 스타일)
- 반복 문제의 해결책

### 기록하지 않을 것

- 세션별 임시 정보
- 검증되지 않은 추측
- CLAUDE.md와 중복되는 내용

## 관련 문서
- [[architecture]] — 전체 구조에서의 위치
- [[philosophy]] — 토큰 절약 철학
- [[git-workflow]] — Git 연동 상세
