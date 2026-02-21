# 일일 워크플로우

## 핵심 규칙 (먼저 읽기)

| 규칙 | 이유 |
|------|------|
| **프로젝트 폴더에서 `claude` 열기** | `.claude/` 설정이 로드됨. `C:\`에서 열면 안 먹음 |
| **의미 있는 작업마다 `/sync`** | STATE + LOG 갱신 + push. 안 하면 기록 유실 |
| **1세션 = 1프로젝트** | 컨텍스트 오염 방지 |
| **Obsidian에서 STATE 편집 금지** | Claude Code만 쓴다 (SoT 규칙) |
| **로그 파일 읽기 요청 금지** | 토큰 낭비. 필요하면 Obsidian에서 직접 보기 |

---

## 아침: 시작

### 1. 프로젝트 폴더에서 Claude Code 열기

```bash
cd C:\dev\01_projects\01_orchestration
claude
```
또는
```bash
cd C:\dev\01_projects\02_portfolio
claude
```

**절대 `C:\`에서 열지 않는다.** 프로젝트 폴더에서 열어야:
- `.claude/CLAUDE.md` 로드됨
- `settings.json` (permissions, hooks) 활성화됨
- Skills (/sync, /status 등) 사용 가능

### 2. 자동 브리핑 (SessionStart Hook)

세션이 시작되면 **자동으로**:
1. `/clear` 실행 (컨텍스트 초기화)
2. `/morning` Skill 실행 → 모든 프로젝트 STATE.md 읽기
3. 브리핑 출력:

```
오케: 완료 13 / 진행 0 / 막힌것 0 — Phase 1-6 완료
포트: 완료 6 / 진행 0 / 막힌것 4 — W6부터 재개
추천: 포트폴리오 막힌 것 해결 우선
```

**수동 입력 불필요.** SessionStart hook이 자동 실행.

### 3. (선택) GPT에서 "today"

→ GPT가 GitHub Pages URL로 STATE 2개 읽고 현황 출력
→ tracker 모드로 오늘 할 일 정리

### 4. (선택) Obsidian 확인

- `01_orchestration/context/STATE.md` — 실시간 최신
- `02_portfolio/context/STATE.md` — 실시간 최신
- `01_orchestration/config/docs/` — 아키텍처 학습 문서

### 5. (선택) Daily Memo 동기화

```
> /todo
```

핸드폰에서 메모한 내용이 있으면 자동으로 TODO.md에 반영됨.

**파이프라인 (D-019)**:
- 핸드폰 Claude Code → `claude/add-inbox-hello-71SP3` 브랜치 → `Inbox.md` 누적
- `/todo` 실행 시: 브랜치 Inbox.md 읽기 → main과 diff → 새 항목 merge → 로컬 `C:\dev\02_ai_config\docs\TODO.md` 반영 (ARCHIVED 경로 — MEMORY.md 확인)

---

## 작업 중: 4가지 패턴

### 패턴 A: 단순 작업 (Claude만)

```
나: "OO 수정해"
Claude: 수정 → 커밋
나: "/sync"
```

가장 흔한 패턴. 대부분의 작업이 이것.

### 패턴 B: 설계가 필요할 때 (GPT → Claude)

```
1. GPT에서 토론
   나: "이 기능 어떻게?"
   GPT: 옵션 A vs B 비교 (Canvas)

2. GPT가 Packet 생성
   [PACKET]
   PROJECT=portfolio
   AGENT: @executor
   EVENTS: [Decision] lazy loading 적용
   STATE_UPDATES: W7 완료 처리
   EXECUTE: src/ui3/Page.tsx 수정
   [/PACKET]

3. 나: 승인

4. Claude Code에 붙여넣기
   나: "AGENT: @executor
        READ_ALLOW: src/ui3/Page.tsx
        CHANGE_ONLY: src/ui3/Page.tsx
        실행해"

5. Claude: 실행 → 커밋
6. 나: "/sync"
```

### 패턴 C: 리서치가 필요할 때 (Perplexity → Claude)

```
1. Perplexity Space (오케스트레이션 또는 포트폴리오)에서 질문
   나: "React 19 Suspense 적용법은?"

2. 결과 받기 ([perplexity-research] 형식 + 소스 URL)

3. Claude Code에 전달
   나: "Perplexity 결과야: [붙여넣기]. 이대로 실행해"

4. Claude: 실행 → 커밋
5. 나: "/sync"
```

### 패턴 D: 대량 검증 (Gemini → Claude)

```
1. Gemini에 코드/구조 전달
   나: "이 프로젝트 전체 검증해줘" + STATE URL

2. [gemini-review] 결과 받기
   통과: 5 / 실패: 2

3. Claude Code에서 수정
   나: "Gemini 리뷰 결과야: [붙여넣기]. 실패 항목 수정해"

4. /sync
```

---

## /sync — 가장 중요한 습관

```
> /sync
```

**하는 일:**
1. `context/STATE.md` 읽기 → 완료/다음/막힌것 갱신
2. `context/logs/YYYY-MM-DD.md`에 시간+작업+결정 append (읽기 없음, echo만)
3. `git add context/ && git commit && git push`
4. GitHub Pages 자동 갱신 (~1분)

**언제 하는가:**
- 의미 있는 작업 완료 후 (매번)
- 프로젝트 전환 전
- ***세션 종료 전 (필수)***

---

## 멀티AI 핸드오프

### Claude → 다른 AI

```
> /handoff gpt "포트폴리오 네비게이션 재설계 논의"
> /handoff perplexity "React 19 Suspense 적용 방법"
> /handoff gemini "전체 폴더 구조 규칙 검증"
```
→ 핸드오프 문서 생성 → 복사 → 해당 AI에 붙여넣기

### 다른 AI → Claude

결과 복사 → Claude Code에 붙여넣기 + "실행해"

---

## 프로젝트 전환

```
나: "/sync"                          ← 현재 프로젝트 마무리
(터미널에서)
cd C:\dev\01_projects\02_portfolio   ← 프로젝트 이동
claude                               ← 새 세션 시작
```

**1세션 = 1프로젝트.** 전환 시 반드시 새 세션.

---

## 세션 종료

```
나: "/sync"           ← STATE + LOG 갱신 + push (필수)
(세션 닫기)
→ Stop hook #1        ← Evidence 백업 (copy-session-log.py → 03_evidence/)
→ Stop hook #2        ← STATE.md 미커밋 차단 (/sync 안 했으면 exit 1)
→ Stop hook #3        ← Auto Memory: analyze-session.sh → pending.md 축적
```

**Stop /sync 가드**: `/sync` 잊어도 시스템이 차단해줌. 하지만 습관적으로 먼저 하는 게 좋음.

**Auto Memory**: Stop hook이 세션 인사이트를 자동 추출. `/sync-all` 실행 시 MEMORY.md로 승격.

### Auto Memory 워크플로우

```
매 세션 (자동):
    세션 종료 → analyze-session.sh → pending.md에 추가

주기적 (수동):
    /sync-all → pending.md 검증 → MEMORY.md 병합
    /memory-review → 오래된 항목 정리 (주 1회 권장)
```

---

## 주간 루틴

| 요일 | 작업 |
|------|------|
| 월 | `/morning`으로 전체 파악 → 주간 목표 설정 |
| 수 | Gemini로 중간 검증 (구조, STATE 정합성) |
| 금 | `/sync` 최종 → STATE에 주간 회고 + **프롬프트 버전 체크** |
| 주 1회 | `/memory-review` → Auto Memory 정리 + `/docs-review` → stale 문서 점검 |

### 금요일 프롬프트 버전 체크

각 `_SNAPSHOT.md`의 `PROMPT_VERSION`과 실제 플랫폼 설정을 비교:
- GPT: Custom GPT Instructions와 `gpt/master_prompt.md` 비교
- Gemini: Gem 설정과 `gemini/master_prompt.md` 비교
- Perplexity: Space 설정과 `perplexity/master_prompt.md` 비교
- 불일치 발견 시: 플랫폼 → 스냅샷 파일로 재복사 + PROMPT_VERSION 갱신

---

## 트러블슈팅

### "STATE.md가 GitHub Pages에 반영 안 됨"
1. `git log --oneline -1` → 최신 커밋 확인
2. 수동 push: orchestration은 `git push origin main`, portfolio는 `git push origin master`
3. 1-2분 대기 (Pages 갱신 지연)

### "Obsidian에서 STATE가 안 보임"
1. Obsidian vault가 `C:\dev\`를 가리키는지 확인 (Settings → Files & Links → Attachment folder)
2. context/STATE.md는 직접 경로로 접근: `01_orchestration/context/STATE.md`

### "프로젝트 설정이 안 먹음"
→ `C:\`에서 열었을 가능성 높음. 프로젝트 폴더에서 다시 열기.

### "토큰이 너무 빨리 소모됨"
1. `/context`로 확인
2. 30턴 또는 100K → `/compact` 권장
3. 150K+ → `/compact` 필수 또는 `/clear`
4. 탐색/검색은 서브에이전트 위임 (메인 컨텍스트 보호)
5. 로그 파일 읽기 요청 하지 않기

---

## 절대 하지 말 것

| 금지 | 이유 |
|------|------|
| `C:\`에서 Claude 열기 | 프로젝트 설정 미로드 |
| Obsidian에서 STATE 편집 | SoT 충돌 |
| /sync 안 하고 세션 닫기 | STATE/LOG 유실 |
| 한 세션에 여러 프로젝트 | 컨텍스트 오염 |
| Claude에게 로그 읽기 요청 | 토큰 낭비 (Obsidian에서 직접 보기) |
| git push --force | 히스토리 손실 (permissions.deny로 차단됨) |

---

## 관련 문서
- [[ai-roles]] — AI별 역할 상세
- [[claude-code-guide]] — Skills, Hooks 상세
- [[git-workflow]] — Git 흐름
- [[philosophy]] — 왜 이렇게 하는가
