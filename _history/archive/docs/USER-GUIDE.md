# v3.1 사용자 가이드

> 마지막 갱신: 2026-02-24
> 이 문서는 **사용자 관점**에서 시스템을 어떻게 쓰는지 설명합니다.
> 기술 구조가 궁금하면 → [SYSTEM-GUIDE.md](./SYSTEM-GUIDE.md)

---

## 목차

1. [하루 흐름](#1-하루-흐름)
2. [세션 시작하기](#2-세션-시작하기)
3. [코드 작성하기](#3-코드-작성하기)
4. [배포하기](#4-배포하기)
5. [시스템 분석하기](#5-시스템-분석하기)
6. [글 쓰기](#6-글-쓰기)
7. [팀으로 병렬 작업하기](#7-팀으로-병렬-작업하기)
8. [세션 마무리하기](#8-세션-마무리하기)
9. [자주 쓰는 명령어 모음](#9-자주-쓰는-명령어-모음)
10. [에이전트 전체 목록과 역할](#10-에이전트-전체-목록과-역할)
11. [뭔가 잘못됐을 때](#11-뭔가-잘못됐을-때)
12. [알아두면 좋은 것들](#12-알아두면-좋은-것들)
13. [부록: v3.0 → v3.1 변경점](#13-부록-v30--v31-변경점)

---

## 1. 하루 흐름

### 전형적인 하루

```
아침 (첫 세션)
  claude 실행 → 자동 브리핑 뜸 → /morning → 오늘 할 일 파악
  ↓
오전 작업 (세션 1)
  "이거 구현해줘" → 구현 → 자동 리뷰 → 자동 커밋
  토큰 많이 쓰면 → /compressor → /sync-all → /clear
  ↓
오후 작업 (세션 2)
  /catchup → 이전 세션 복구 → 다음 작업 진행
  ↓
마무리
  /compressor → /sync-all → 세션 종료
```

### 핵심 원칙

- **1세션 = 1목표**: 여러 프로젝트를 한 세션에 섞지 않는다
- **150K 토큰 넘으면**: `/compressor` → `/sync-all` → `/clear` 또는 `/compact`
- **세션 종료 전 반드시**: `/compressor` → `/sync-all`

---

## 2. 세션 시작하기

### 2-1. Claude Code를 켜면 자동으로 뜨는 것들

```
=== 오늘 작업 로그 ===
(이전 세션에서 한 것들)

=== 프로젝트 상태 ===
  ⚠️  orchestration: 3개 미커밋
  ✅ portfolio: clean

=== 미반영 결정 사항 (N건) ===
2026-02-22 [portfolio] 스크린샷 → lab.md 이미지 링크 추가 | pf:❌
```

이건 SessionStart 훅이 자동으로 보여주는 겁니다. 따로 명령 안 쳐도 됩니다.

### 2-2. 첫 명령어 선택

| 상황 | 명령어 | 설명 |
|------|--------|------|
| 뭘 해야 할지 모를 때 | `/morning` | 전체 프로젝트 브리핑 + TODO + 추천 액션 3개 |
| 어제 하던 거 이어할 때 | `/catchup` | 이전 세션 요약만 빠르게 (5초) |
| 이미 알고 있을 때 | 바로 작업 | "portfolio에 다크모드 추가해줘" |

### 2-3. /morning 실행하면 나오는 것

```
=== 모닝 브리핑 (2026-02-23) ===

[orchestration]
완료: v3.0 에이전틱 워크플로우 강화
다음: Phase E 파일럿 테스트
미커밋: 0개

[portfolio]
완료: TechReviewSystemSection 생성
다음: 스토리텔링 글 작성
미커밋: 0개

[TODO]
우선순위 높음:
  - [ ] 07~10 스크린샷 → lab.md 이미지 링크

=== 오늘 추천 액션 ===
1. portfolio: Tech Review System 스토리텔링 글 작성
2. tech-review: 월~토 프롬프트 Smart Brevity 업데이트
3. orchestration: Agent Teams 병렬 테스트
```

여기서 하나 골라서 시작하면 됩니다.

### 2-4. /catchup 실행하면 나오는 것

```
=== 이전 세션 요약 ===
세션 목표: v3.1 에이전트 확장 및 팀 시스템 추가
완료:
  - CLAUDE.md 체인 규칙 추가
  - agent.md 23개 표준화
다음 할 것:
  1. Linker System 파일럿 테스트
  2. 팀 운영 검증
```

---

## 3. 코드 작성하기

### 3-1. 기본 흐름: 말하면 자동으로 체인이 돌아간다

**당신이 하는 것:**
```
"portfolio에 다크모드 토글 버튼 추가해줘"
```

**시스템이 자동으로 하는 것:**

```
Step 1: brainstorming (superpowers)
  → "다크모드 구현 방법이 여러 가지인데요..."
  → 토글 위치, 저장 방식, 색상 전환 방식 질문
  → 당신이 답변

Step 2: writing-plans (superpowers)
  → 구현 계획서 작성
  → 당신이 승인

Step 3: implement
  → 실제 코드 작성
  → "완성했습니다"

Step 4: code-reviewer (자동 호출, Opus)
  → [code-reviewer]
  → 🔴 버그·보안 (1개)
  →   1. [DarkModeToggle.tsx:23] localStorage 접근 시 SSR 에러 가능
  →      → typeof window !== 'undefined' 체크 추가
  → 🟡 개선 (1개)
  →   1. [DarkModeToggle.tsx:45] color 전환 애니메이션 없음
  →      → transition: 'colors 0.2s' 추가 권장
  → 리뷰 요약: SSR 호환성 수정 필요, 그 외 양호

Step 5: 수정
  → 🔴 항목 수정

Step 6: code-reviewer (재리뷰)
  → ✅ 통과

Step 7: commit-writer (자동 호출, Haiku)
  → 제안 커밋 메시지:
  → [portfolio] 다크모드 토글 버튼 추가
  → 변경 파일: 3개
```

### 3-2. 핵심: 체인은 건너뛸 수 없다

```
구현 완료
  ↓
code-reviewer 실행 (자동)
  ├─ 🔴 있으면 → 수정 → 재리뷰 (commit-writer 호출 안 됨!)
  └─ ✅ 이면 → commit-writer 실행 (자동)
```

- **🔴가 하나라도 있으면** commit-writer가 호출되지 않습니다
- 수정 후 재리뷰를 거쳐야만 커밋으로 넘어갑니다
- 이건 CLAUDE.md에 규칙으로 박혀 있어서 Claude가 임의로 건너뛸 수 없습니다

### 3-3. 버그 수정할 때

```
"이 에러 수정해줘: TypeError: Cannot read property 'map' of undefined"
```

시스템이 자동으로:
1. `systematic-debugging` (superpowers) → 체계적으로 원인 추적
2. 수정
3. code-reviewer → commit-writer (체인 동일)

### 3-4. 중간에 커밋만 하고 싶을 때

```
"여기까지 커밋해줘"
```

→ commit-writer가 자동 호출됩니다.
→ 단, code-reviewer를 거치지 않은 커밋도 가능합니다 (명시적 요청 시).

### 3-5. 리뷰 없이 빠르게 커밋하고 싶을 때

```
"리뷰 생략하고 바로 커밋해"
```

→ 가능합니다. 하지만 체인 규칙상 권장하지 않습니다.

---

## 4. 배포하기

### 4-1. 배포 체인

```
"배포해줘" (또는 "deploy", "Vercel")
  ↓
pf-deployer (자동 호출)
  체크리스트 실행:
  ├─ TypeScript 에러? → npx tsc --noEmit
  ├─ console.log 남아있음? → grep 검사
  ├─ localhost 하드코딩? → grep 검사
  ├─ 미커밋 파일? → git status
  └─ 이미지 alt 텍스트? → 확인

  결과:
  ✅ 통과: 4개
  ❌ 실패: 1개 (console.log 2건)
  판정: NO-GO ❌

→ NO-GO면 여기서 멈춤. 수정 후 다시 요청.
```

```
수정 후 "다시 배포 체크해줘"
  ↓
pf-deployer → GO ✅
  ↓
security-auditor (자동 연결)
  ├─ 하드코딩 시크릿? → grep 검사
  ├─ .env 노출? → process.env 검사
  ├─ XSS? → dangerouslySetInnerHTML 검사
  ├─ npm audit? → 취약점 검사
  └─ 외부 http:// URL? → grep 검사

  결과:
  🟢 통과
  판정: GO ✅

→ 둘 다 GO여야 배포 진행
  ↓
"push해도 될까요?" → 당신이 확인 → push
```

### 4-2. 배포 체크리스트에서 실패하면

```
pf-deployer가 NO-GO를 내면:
  → 실패 항목과 파일:줄번호가 나옵니다
  → 수정하면 됩니다
  → "다시 체크해줘"하면 재실행

security-auditor가 NO-GO를 내면:
  → CRITICAL 항목이 있다는 뜻
  → 반드시 수정 후 재실행
  → CRITICAL 하나라도 있으면 절대 GO 안 나옵니다
```

---

## 5. 시스템 분석하기

### 5-1. 전체 코드베이스 점검

```
"시스템 전체 점검해줘, Gemini랑 Codex 둘 다 써서"
```

→ 두 도구가 **동시에** 독립적으로 분석합니다:

| 도구 | 방식 | 강점 |
|------|------|------|
| **gemini-analyzer** | Gemini CLI, 100만 토큰 | 전체를 한 번에 보는 광역 분석 |
| **codex-reviewer** | Codex CLI, 8개 관점 | 구조적 결함 감지 (명세 모순, 상태 누락 등) |

→ ai-synthesizer(Opus)가 두 결과를 비교해서:
- 양쪽 다 발견 → 높은 신뢰도, 즉시 조치
- 한쪽만 발견 → ai-synthesizer가 직접 확인
- 양쪽 다 못 찾음 → blind spot 가능성 인지
- 합의 항목 → agent.md 자동 반영 가능
- 불일치 항목 → 사용자 판단 필수

### 5-2. 특정 프로젝트만 분석

```
"portfolio 코드 리뷰해줘"
→ code-reviewer가 portfolio만 리뷰

"orchestration 설정 시스템 분석해줘"
→ gemini-analyzer가 설정 파일들 분석
```

---

## 6. 글 쓰기

### 6-1. 글쓰기 프로세스

```
"Tech Review System에 대한 포트폴리오 글을 써줘"
  ↓
content-writer (자동 호출)
  → 질문 5개를 순서대로 합니다:
    1. 글 유형? (포트폴리오 / 블로그 / 케이스스터디)
    2. 타깃 독자? (채용담당자 / 개발자 / 일반인)
    3. 핵심 메시지? (한 문장)
    4. 톤? (전문적 / 대화체 / 스토리텔링)
    5. 길이? (짧게 300자 / 중간 800자 / 길게 1500자+)
  ↓
  기존 글 스타일 분석 (HOME_INTRO_TO_RELATION_KO.md 참고)
  ↓
  아웃라인 제안 → 당신 승인
  ↓
  초안 작성
  ↓
  퇴고 체크리스트 (5항목) 자체 검증
  ↓
  최종본 출력
  "파일로 저장할까요?"
```

### 6-2. /write로 직접 호출

```
/write
```
→ content-writer와 동일한 프로세스가 시작됩니다.

---

## 7. 팀으로 병렬 작업하기

### 7-1. 언제 쓰나

- 독립적인 작업 2-3개를 동시에 처리하고 싶을 때
- 분석/리서치를 병렬로 돌리고 싶을 때
- 정기적인 자동화 작업을 팀으로 묶어 실행할 때

### 7-2. 사용 방법

```
"이 3개 작업을 팀으로 병렬 처리해줘:
1. portfolio 코드 리뷰
2. tech-review 프롬프트 분석
3. orchestration 문서 점검"
```

→ 시스템이 자동으로:
1. 팀 생성 (TeamCreate)
2. 태스크 3개 생성
3. 팀원 3명 배포 (각각 독립 작업)
4. 결과 수신
5. 통합 → 반영
6. 팀 해산

### 7-3. 사전 정의 팀 (v3.1 신규)

자주 쓰는 조합을 팀으로 바로 호출할 수 있습니다:

| 팀 | 호출 방법 | 하는 일 |
|----|----------|---------|
| **tech-review-ops** | "tech-review 팀 돌려줘" | tr-monitor → tr-updater → commit-writer |
| **ai-feedback-loop** | "Gemini Codex 교차 분석해줘" | gemini+codex 병렬 → ai-synthesizer 검증 |
| **daily-ops** | "일일 운영 체인 돌려줘" | inbox-processor → orch-state → morning-briefer |

### 7-4. 주의사항

- **같은 파일을 동시에 수정하면 안 됩니다** (하나가 reject됨)
- 팀원이 "유휴(idle)" 상태로 나오는 건 정상입니다 — 결과 보내고 대기 중
- worktree로 격리할 수도 있습니다 (브랜치 분리)

---

## 8. 세션 마무리하기

### 8-1. 마무리 루틴 (2단계)

```
Step 1: /compressor
  → 이번 세션 요약을 6곳에 저장
    1. session-summary.md — 다음 /catchup이 읽을 파일
    2. LOG (날짜별) — 시간순 기록
    3. STATE.md — 프로젝트 현재 상태
    4. decisions.md — 결정 사항 추적
    5. METRICS.md — 통계 (완료 태스크, 결정 수)
    6. pending.md — 에이전트 학습 패턴 후보 (있으면)

Step 2: /sync-all
  → 모든 프로젝트 커밋 + push
  → 메모리 동기화 (pending.md → MEMORY.md 검증)
  → 에이전트 학습 패턴 검증 (pending.md → agent.md)
```

**반드시 이 순서!** compressor가 먼저 파일을 만들고, sync-all이 커밋합니다.

### 8-2. 중간에 끊어야 할 때

토큰이 많이 쌓였거나 작업을 전환해야 할 때:

```
/compressor → /sync-all → /clear (또는 새 세션)
```

다음 세션에서 `/catchup`으로 바로 이어갑니다.

### 8-3. 급하게 끊어야 할 때

최소한 이것만:
```
/sync-all
```
→ 적어도 코드는 커밋+push됩니다.
→ 세션 요약은 없지만 SessionEnd 훅이 Auto Memory를 실행합니다.

---

## 9. 자주 쓰는 명령어 모음

### 세션 관리

| 명령어 | 설명 | 언제 |
|--------|------|------|
| `/morning` | 전체 브리핑 + TODO + 추천 액션 | 하루 시작 |
| `/catchup` | 이전 세션 복구 (5초) | 세션 시작 |
| `/compressor` | 세션 요약 6곳 저장 | 세션 종료 전 |
| `/sync-all` | 모든 프로젝트 커밋+push | 세션 종료 전 |

### 검증

| 명령어 | 설명 | 언제 |
|--------|------|------|
| `/verify` | 브랜치/STATE/커밋 규칙 검증 | 커밋 전 |
| `/docs-review` | 문서 stale 감지 | 주간 |

### TODO

| 명령어 | 설명 |
|--------|------|
| `/todo` | 할 일 목록 보기 + 핸드폰 INBOX 동기화 |
| `/todo add "내용"` | 항목 추가 |
| `/todo done 1` | 첫 번째 미완료 항목 완료 |

### 분석

| 명령어 | 설명 |
|--------|------|
| `/session-insights` | 토큰 사용량, 비용 분석 |
| `/memory-review` | MEMORY.md 정리 (주간) |
| `/research` | 딥 리서치 (코드+웹) |

### 기타

| 명령어 | 설명 |
|--------|------|
| `/write` | 글쓰기 프로세스 시작 |
| `/handoff gpt "요청"` | GPT에게 보낼 문서 생성 |

---

## 10. 에이전트 전체 목록과 역할

### 자동 호출 (PROACTIVELY) — 말 안 해도 알아서 뜸

| 에이전트 | 모델 | 언제 자동 호출되나 | 하는 일 |
|---------|------|-------------------|---------|
| **code-reviewer** | Opus | "만들었어", "완성", 구현 마무리 | 버그·보안·성능·가독성 리뷰, 파일:줄번호 포함 |
| **commit-writer** | Haiku | "커밋해", code-reviewer ✅ 후 | 커밋 메시지 생성 ([project] 한줄 설명) |
| **orch-state** | Sonnet | "뭐 해야 해", 방향 파악 필요 | STATE.md 분석 → 다음 액션 3개 추천 |
| **compressor** | Sonnet | "/compressor", "마무리" | 세션 요약 6곳 저장 |

### Portfolio 전용

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **pf-context** | Sonnet | portfolio 현재 상태 수집 (작업 시작 전) |
| **pf-reviewer** | Opus | 코드/디자인/접근성 심층 리뷰 (첫 5초 임팩트, 모바일 반응형) |
| **pf-deployer** | Sonnet | 배포 전 체크리스트 (GO/NO-GO) |

### Orchestration 전용

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **orch-doc-writer** | Opus | 결정 기록, CHANGELOG, 아키텍처 문서 작성 |
| **orch-skill-builder** | Opus | 새 스킬/에이전트/훅 생성 |

### 분석/검증

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **gemini-analyzer** | Sonnet* | Gemini CLI로 100만 토큰 광역 분석 |
| **codex-reviewer** | Sonnet* | Codex CLI로 8개 관점 설계 결함 분석 |
| **security-auditor** | Opus | 배포 전 보안 점검 (XSS, 시크릿, CORS) |

> *Sonnet은 래퍼. 실제 분석은 Gemini/Codex가 수행.

### Monet-lab

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **ml-experimenter** | Opus | UI 실험 리뷰 + portfolio 이식 가능성 평가 |
| **ml-porter** | Sonnet | 실험 → portfolio 이식 판단 + 절차 안내 |

### Linker / 연동 (v3.1 신규)

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **context-linker** | Haiku | bash hook → live-context.md 읽기 → 프로젝트 간 맥락 연결·주입 |
| **project-linker** | Sonnet | 커밋 감지 → 관련 프로젝트 TODO 생성 + 알림 |

### 운영 자동화 (v3.1 신규)

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **meta-orchestrator** | Sonnet | catchup 후 팀 활성화 + 태스크 디스패치 |
| **inbox-processor** | Haiku | 일일 인박스 처리, 운영 체인 시작 |
| **ai-synthesizer** | Opus | gemini+codex 병렬 결과 교차 검증 → 합의/불일치 분류 → agent.md 반영 판단 |

### Tech-Review (v3.1 신규)

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **tr-monitor** | Haiku | tech-review 키워드 모니터링, 신규 감지 시 tr-updater 트리거 |
| **tr-updater** | Sonnet | tech-review 블로그 콘텐츠 업데이트 |

### 기타

| 에이전트 | 모델 | 하는 일 |
|---------|------|---------|
| **morning-briefer** | Haiku | /morning 브리핑 (catchup + orch-state 통합) |
| **content-writer** | Opus | 글 작성 (질문→구조→초안→퇴고) |

### 에이전트가 공통으로 아는 것 (암묵지)

모든 에이전트가 자기 agent.md에 이걸 갖고 있습니다:
- orchestration = main 브랜치, portfolio = master 브랜치
- dev 서버는 사용자가 직접 실행 (Claude 실행 금지)
- 시간은 KST 기준
- node_modules, .git, dist, build 읽기 금지

---

## 11. 뭔가 잘못됐을 때

### 토큰이 너무 많이 쌓였어

```
/compressor → /sync-all → /clear
```
다음 세션에서 `/catchup`으로 복구.

### 커밋 전에 규칙 위반이 없는지 확인하고 싶어

```
/verify
```
브랜치, STATE.md, 커밋 메시지 형식 등을 검증합니다.

### 세션이 끊겼는데 이전 작업을 이어가고 싶어

```
/catchup
```
session-summary.md에서 자동 복구. 5초면 파악됩니다.

### 전체 시스템에 문제가 없는지 점검하고 싶어

```
"시스템 전체 점검해줘, Gemini랑 Codex 둘 다 써서"
```
두 AI가 독립 분석 → Claude가 교차 검증.

### MEMORY.md가 너무 길어졌어

```
/memory-review
```
150줄 넘으면 SessionEnd에서도 자동 경고됩니다.

### 다른 AI에게 현재 상태를 알려주고 싶어

```
/handoff gpt "이것 검토해줘"
```
또는 GitHub Pages URL 공유:
`https://paulseongminpark.github.io/orchestration/STATE.md`

### 핸드폰에서 메모한 거 동기화하고 싶어

```
/todo
```
daily-memo 브랜치에서 Inbox.md를 읽어 TODO에 반영합니다.

---

## 12. 알아두면 좋은 것들

### 12-1. 에이전트 학습 시스템

에이전트는 세션이 쌓일수록 똑똑해집니다.

```
세션 중: code-reviewer가 "portfolio에서 any 타입 반복 발견" 패턴 감지
  ↓
/compressor: pending.md에 "[패턴후보][code-reviewer] portfolio any 타입 반복" 저장
  ↓
/sync-all: Opus가 검증
  ✅ 2회 이상 확인됨
  ✅ code-reviewer.md에 중복 없음
  ✅ 기존 규칙과 모순 없음
  ✅ 다음 세션에 유용함
  → code-reviewer.md "학습된 패턴" 섹션에 추가
  ↓
다음 세션: code-reviewer가 portfolio 리뷰 시 any 타입을 더 주의깊게 확인
```

- 최대 5개까지 축적, 넘으면 가장 오래된 것 교체
- Sonnet이 수집하고 Opus가 검증 → 잘못된 패턴 차단
- 당신이 따로 할 건 없습니다 (자동)

### 12-2. decisions.md 추적 시스템

모든 결정은 `decisions.md`에 기록됩니다.

```
2026-02-23 [orch] 플러그인 4개 비활성화 | orch:✅
2026-02-22 [portfolio] 스크린샷 → lab.md 링크 | pf:❌
```

- `❌` = 아직 해당 프로젝트에 반영 안 됨
- `✅` = 반영 완료
- SessionStart 훅이 매 세션마다 미반영(❌) 항목을 알려줍니다

### 12-3. 훅이 자동으로 하는 것들

| 시점 | 자동 동작 |
|------|----------|
| **세션 시작** | 오늘 로그 + 미커밋 경고 + 미반영 결정 출력 |
| **세션 종료** | 미커밋 현황 + Auto Memory 분석 |
| **Bash 실행 전** | 위험 명령 차단 (rm -rf, git push --force, git reset --hard) |
| **파일 수정 후** | context/*.md 변경 감지 → 커밋 전 확인 |
| **compact 전** | 미커밋 파일 있으면 /verify + /sync-all 권장 |
| **팀원 유휴** | 미완료 태스크 있으면 계속 진행 안내 |
| **태스크 완료** | 검증 포함 여부 확인 + 다음 태스크 안내 |

### 12-4. 플러그인 현황

**활성 (11개):**
superpowers, context7, frontend-design, vercel, document-skills, code-simplifier, claude-md-management, coderabbit, playwright, feature-dev, greptile

**비활성 (8개):**
github(gh CLI 대체), example-skills(중복), hookify(이중실행), code-review(custom 대체), agent-sdk-dev(미사용), commit-commands(commit-writer 대체), playground(미사용), claude-code-setup(완성됨), skill-creator(orch-skill-builder 대체)

### 12-5. 프로젝트별 브랜치 (혼동 주의!)

| 프로젝트 | 브랜치 | 절대 틀리면 안 됨 |
|---------|--------|-----------------|
| orchestration | **main** | |
| portfolio | **master** | ← main 아님! |
| dev-vault | **main** | |
| tech-review blog | **main** | |

### 12-6. 파일 위치 빠른 참조

| 뭘 찾을 때 | 어디 |
|-----------|------|
| 전역 규칙 | `C:\dev\CLAUDE.md` |
| 에이전트 파일 | `~/.claude/agents/*.md` |
| 스킬 파일 | `~/.claude/skills/*/SKILL.md` |
| 설정 | `~/.claude/settings.json` |
| 메모리 | `~/.claude/projects/C--dev/memory/MEMORY.md` |
| STATE | `01_projects/01_orchestration/STATE.md` |
| TODO | `01_projects/01_orchestration/config/docs/TODO.md` |
| 결정 추적 | `01_projects/01_orchestration/context/decisions.md` |
| 세션 요약 | `01_projects/01_orchestration/context/session-summary.md` |

---

## 부록: v2.2 → v3.0 변경점

| 항목 | v2.2 | v3.0 |
|------|------|------|
| 체인 보장 | Claude 판단에 의존 | CLAUDE.md에 규칙 명시, 건너뛰기 금지 |
| 에이전트 검증 | 없음 | 모든 에이전트에 자기 검증 단계 |
| 암묵지 전달 | 안 됨 | agent.md에 프로젝트 규칙 포함 |
| 세션 간 학습 | 없음 | 하이브리드 파이프라인 (수집→검증→반영) |
| 플러그인 | 19개 | 11개 (중복/미사용 제거) |
| Agent Teams | 미사용 | 파일럿 검증 완료, 실전 투입 가능 |
| 학습 방식 | - | compressor(Sonnet) 수집 → sync-all(Opus) 검증 |

---

## 13. 부록: v3.0 → v3.1 변경점

| 항목 | v3.0 | v3.1 |
|------|------|------|
| 에이전트 수 | 16개 | 23개 (+7) |
| 분석 체인 | gemini+codex → Claude 교차 검증 | gemini+codex → ai-synthesizer(Opus) → 합의/불일치 분류 → agent.md 반영 |
| 팀 시스템 | 수동 조합 | tech-review-ops, ai-feedback-loop, daily-ops 3개 사전 정의 팀 |
| Linker System | 없음 | context-linker + project-linker (파일 변경 → 맥락 자동 연결) |
| tech-review 자동화 | 없음 | tr-monitor → tr-updater → commit-writer 체인 |
| 일일 운영 자동화 | 없음 | inbox-processor → orch-state → morning-briefer 체인 |
| 디스패치 | 수동 | catchup → meta-orchestrator → 팀 활성화 체인 |
| context/ 파일 | 5개 | 6개 (live-context.md 추가) |
| 체인 규칙 | 3개 | 7개 (분석강화+tech-review+일일운영+디스패치+프로젝트연동) |
