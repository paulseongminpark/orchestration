# 설계 철학

## 핵심 문제

> "여러 AI를 쓰면서 정보가 흩어지고, 컨텍스트가 날아가고, 누가 무엇을 했는지 모른다."

이 시스템은 한 사람이 여러 AI를 동시에 활용하면서도 **혼돈에 빠지지 않는 방법**을 설계한 것이다.

## 7가지 설계 원칙

### 1. 단일 진실 소스 (Single Source of Truth)

**문제**: Obsidian에 쓰고, Claude에 말하고, GPT에서 토론하면 — 어디가 최신인가?

**해결**: Git의 `context/STATE.md`가 유일한 진실. 다른 모든 것은 이 파일의 복사본이거나 뷰이다.

**구현**:
- Claude Code만 STATE.md를 수정할 수 있다
- GitHub Pages가 STATE.md를 URL로 공개한다
- GPT/Gemini/Perplexity는 그 URL을 읽는다
- Obsidian은 Junction point로 로컬 파일을 본다

→ 진실은 하나. 읽는 경로만 여러 개.

### 2. 쓰기 권한 분리

**문제**: 여러 AI가 동시에 파일을 수정하면 충돌이 발생한다.

**해결**: Claude Code만 쓴다. 나머지는 읽기만.

**왜 Claude Code인가**:
- 유일하게 로컬 파일시스템에 접근 가능
- Git을 직접 조작할 수 있음
- 코드 실행 → 검증 → 커밋을 한 흐름으로 처리

**다른 AI의 역할**:
- GPT: "이렇게 하면 어떨까?" (사고) → Packet으로 Claude 지시문 생성
- Gemini: "이 코드에 문제가 있다" (검증) → 결과 테이블로 Claude에 전달
- Perplexity: "최신 문서에 따르면..." (리서치) → 소스 URL과 함께 전달

→ 생각하는 AI와 실행하는 AI를 분리하면 오류가 줄고 추적이 가능하다.

### 3. 사고는 휘발, 기록은 남음

**문제**: GPT 대화는 길어지면 잘린다. 중요한 결정이 대화 속에 묻힌다.

**해결**:
- GPT의 사고는 휘발되어도 된다 → 중요한 것만 Packet으로 추출
- Claude의 커밋은 Git에 영원히 남는다
- STATE.md가 현재 상태를 항상 반영한다

**Packet 시스템의 의미**:
```
[PACKET]
PROJECT=orchestration
AGENT: @executor
EVENTS: [Decision] Phase 1 폴더 구조 확정
STATE_UPDATES: 완료 목록에 Phase 1 추가
EXECUTE: mkdir -p 01_projects/...
[/PACKET]
```
이것은 "GPT의 사고"를 "Claude의 행동"으로 번역하는 프로토콜이다.

### 4. 토큰은 자원이다

**문제**: Claude Code는 매 턴마다 CLAUDE.md를 로드한다. 146줄짜리 CLAUDE.md = 매 턴 2000토큰 소모.

**해결**: 글로벌 CLAUDE.md를 4줄(~100토큰)로 축소. 나머지는 분리.

**수치**:
| 항목 | 이전 | 이후 | 절감 |
|------|------|------|------|
| CLAUDE.md/턴 | ~2000토큰 | ~100토큰 | 95% |
| 20턴 세션 | ~40K | ~2K | 38K |

**계층 구조**:
```
~/.claude/CLAUDE.md           ← 4줄 (매 턴 자동 로드)
~/.claude/rules/*.md          ← 모듈식 (매 턴 자동 로드, 작게 유지)
{project}/.claude/CLAUDE.md   ← 해당 프로젝트에서만 로드
{project}/.claude/rules/*.md  ← 조건부 로드
MEMORY.md                     ← 200줄 자동 로드 (세션 간 기억)
```

→ 불필요한 컨텍스트를 제거하면 더 많은 작업을 할 수 있다.

### 5. 구조가 규율을 강제한다

**문제**: "이 파일 어디에 넣지?" → 고민 → 아무 데나 → 혼돈

**해결**: Jeff Su 방법론. 규칙이 단순하면 따르기 쉽다.

**5가지 규칙**:
1. **5레벨 MAX**: `C:\dev\01\01\context\STATE.md` = 5. 더 깊으면 구조 재고
2. **2자리 넘버링**: `01_`, `02_`, ... `99_`. 순서가 명확하고 정렬됨
3. **99 = Archive**: 쓰지 않는 것은 99에. 삭제 대신 아카이브
4. **명확한 이름**: 폴더명만으로 내용 추론
5. **프로젝트 = 독립 단위**: 각 프로젝트는 자기 .claude/, context/, scripts/를 가짐

### 6. 자동화는 최소한으로

**문제**: 복잡한 자동화는 디버깅이 어렵고, 깨지면 전체가 멈춘다.

**해결**: 자동화는 3가지만.
1. **post-commit hook**: STATE.md 변경 시 자동 push (5줄 스크립트)
2. **Stop hook — Evidence**: 세션 종료 시 Evidence 백업 (copy-session-log.py)
3. **Stop hook — /sync 가드**: STATE.md 미커밋 시 세션 종료 차단 (exit 1)

나머지는 명시적 명령:
- `/sync` → 사용자가 직접 호출
- `/handoff` → 사용자가 직접 호출
- git push → post-commit이 자동으로 하되, 실패해도 수동으로 가능

→ "마법" 같은 자동화보다 "예측 가능한" 수동 + 게이트 기반 안전장치.

### 7. 세션 간 기억 (Auto Memory)

**문제**: 세션이 끝나면 Claude는 모든 것을 잊는다. 다음 세션에 같은 실수를 반복하고, 같은 질문을 다시 하고, 같은 패턴을 다시 발견한다.

**해결**: 세션 종료 시 자동으로 반복 패턴/에러/선호사항을 감지하여 `pending.md`에 기록. 검증 후 `MEMORY.md`로 이동. MEMORY.md는 매 턴 자동 로드된다.

**3단계 구조**:
```
Phase 1 — 자동 감지 (SessionEnd Hook)
  세션 종료 → analyze-session.sh → pending.md 누적
  감지 대상: 도구 반복 패턴, 에러+해결 쌍, 사용자 명시 선호사항

Phase 2 — 검증 (/sync-all)
  pending.md 항목 → 4가지 기준으로 Claude가 판단
  기준: 2회 이상 확인 / MEMORY.md 중복 없음 / CLAUDE.md 모순 없음 / 다음 세션에 유용

Phase 3 — 주간 정리 (/memory-review)
  MEMORY.md 품질 관리: 중복 제거, CLAUDE.md 모순 제거, 200줄 제한 유지
```

**설계 원칙**:
- 자동 감지 → 수동 검증: 자동화가 후보를 만들고, 사람이 최종 판단
- MEMORY.md 200줄 제한: 매 턴 자동 로드되므로 토큰 자원
- 사실만 기록: 한 세션에서만 나온 패턴은 보류. 2회 이상 확인된 것만

**파일 위치**:
```
~/.claude/scripts/analyze-session.sh   ← 세션 분석
~/.claude/hooks/session-stop.sh        ← SessionEnd Hook
~/.claude/projects/C--dev/memory/
  ├── pending.md                        ← 검증 대기 후보
  └── MEMORY.md                         ← 검증 완료 (매 턴 로드)
```

→ Claude의 기억을 세션 밖으로 확장하되, 노이즈가 아닌 신뢰할 수 있는 것만 남긴다.

## 안티패턴 (하지 말 것)

| 안티패턴 | 이유 | 대안 |
|---------|------|------|
| Obsidian에서 STATE 직접 편집 | SoT 충돌 | Claude Code로만 |
| .claudeignore 사용 | 보안 이슈 (우회 가능) | permissions.deny |
| 중앙 LOGS 폴더 | 토큰 낭비, 읽기 유혹 | STATE.md에 통합 |
| TODAY 파일 매일 생성 | 폴더 누적, 관리 부담 | STATE.md가 항상 최신 |
| 한 세션에 여러 목표 | 컨텍스트 오염 | 1세션 = 1목표 |
| 파일 재읽기 | 토큰 낭비 | MEMORY.md 활용 |

## 관련 문서
- [[architecture]] — 구체적 구조
- [[decisions]] — 각 결정의 상세 근거
- [[ai-roles]] — AI별 역할 심화
