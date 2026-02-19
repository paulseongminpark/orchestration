# KNOWLEDGE — Best Practices

프로젝트별 모범 사례, 규칙, 패턴. 신규 기여자 온보딩 가이드.

---

## Git 규칙

### 브랜치 전략
- **orchestration**: main 브랜치
- **portfolio**: master 브랜치
- **ai-config**: main 브랜치

### 커밋 메시지
```
형식: [project] 한줄 설명

예시:
✅ [orchestration] Phase 7: 검증 시스템 구현
✅ [portfolio] 랜딩 페이지 반응형 개선
❌ update files
❌ fix bug
```

**필수**:
```
Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

### 금지 사항
- ❌ `git push --force` (절대 금지)
- ❌ `git clean -f` (검증 없이)
- ❌ `git reset --hard` (커밋 전)
- ❌ `--no-verify` (훅 우회)

### 워크플로우
```bash
# 작업 완료 후
> /verify              # 검증 먼저
> /sync                # STATE.md 갱신 + 커밋+푸시

# 전체 프로젝트 동기화
> /sync-all

# 세션 종료 전
> /verify
> /sync (또는 /sync-all)
```

---

## 파일 구조

### context/ (프로젝트 컨텍스트)
```
context/
├── STATE.md         # 지금 상태 (고수준)
├── PLANNING.md      # 아키텍처 결정 (ADR)
├── KNOWLEDGE.md     # 모범 사례 (이 파일)
└── logs/
    └── YYYY-MM-DD.md  # 시간순 상세 로그
```

### STATE.md 형식
```markdown
## 지금 상태 (YYYY-MM-DD 기준)

**완료**
- Phase X: 설명

**다음 할 일**
- 구체적 작업

**막힌 것**
- 없음 (또는 구체적 블로커)
```

### LOG 형식 (append만, 읽기 금지)
```bash
## YYYY-MM-DD HH:MM [project] Claude Code
- 작업 요약
- [Decision] 확정된 결정
- [Pending] 보류 중인 사항
- [Discarded] 폐기한 아이디어
```

**태그**:
- 프로젝트: `[orchestration]`, `[portfolio]`, `[ai-config]`
- 결정: `[Decision]`, `[Pending]`, `[Discarded]`
- 협업: `[cowork]` (다른 AI와 협업 시)

---

## 토큰 관리

### 규칙
- **1세션 = 1목표**: 한 세션에 하나의 명확한 목표만
- **150K+**: /compact 또는 /clear
- **탐색**: 서브에이전트 (메인 컨텍스트 보호)
- **파일 묶음**: 2-3개 한 턴에 처리
- **읽기 금지**: node_modules/, .git/, dist/, build/, logs/

### 모니터링
```bash
# 터미널에서
claude --context

# 또는 /context (세션 내)
```

### 서브에이전트 모델 선택
- **Haiku**: 상태 확인, 브리핑, 요약 (빠름, 저렴)
- **Sonnet**: 탐색, 검색, 코드 분석 (균형)
- **Opus**: 설계 결정, 크로스 검증, 복잡한 실행 (느림, 비쌈)

---

## 스킬 사용법

### 글로벌 스킬 (어디서든)
```bash
/morning              # 전체 프로젝트 브리핑
/sync-all             # 전체 동기화
/verify               # 통합 검증
/verify-project-rules # 브랜치/STATE/커밋 검증
/verify-log-format    # LOG 형식 검증
```

### 프로젝트별 스킬 (orchestration)
```bash
/sync                 # STATE.md 갱신 + LOG + 커밋+푸시
/handoff gpt "요청"   # GPT에게 핸드오프 문서 생성
/status               # 프로젝트 현황
```

### 사용 시나리오

**시나리오 1: 일일 작업 시작**
```bash
cd C:\dev\02_ai_config
claude
> /morning            # 전체 브리핑 확인
# (작업 결정)
cd C:\dev\01_projects\01_orchestration
claude
# (작업 진행)
```

**시나리오 2: 작업 완료**
```bash
> /verify             # 검증
> /sync               # 동기화
```

**시나리오 3: 세션 종료 전**
```bash
> /verify
> /sync-all           # 모든 프로젝트 동기화
# (세션 종료)
```

---

## 권한 (Permissions)

### 허용 (Allow)
- Read (전체, 단 deny 제외)
- Edit (코드, 문서)
- Bash (git, npm, npx)

### 거부 (Deny)
- ❌ `Read(.env*)` - 환경 변수
- ❌ `Read(C:/dev/03_evidence/**)` - 세션 로그
- ❌ `Read(**/.ssh/**)` - SSH 키
- ❌ `Read(**/secrets/**)` - 시크릿
- ❌ `Bash(rm -rf *)` - 파괴적 삭제
- ❌ `Bash(git push --force*)` - Force push
- ❌ `Bash(curl *)`, `Bash(wget *)` - 외부 다운로드

---

## 멀티 AI 오케스트레이션

### 역할 분담
- **Claude Code**: 실행 + 기록 (유일한 쓰기)
- **GPT Plus**: 사고 확장, Canvas, Packet 생성
- **Gemini Pro**: 대량 검증 (100만 토큰)
- **Perplexity Pro**: 리서치 + 교차검증

### 데이터 흐름
```
Claude Code (쓰기)
→ STATE.md 갱신
→ git commit + push
→ GitHub Pages
→ GPT/Gemini/Perplexity (읽기)
   ↓
  분석/검증/리서치
   ↓
  Packet 생성
   ↓
Claude Code (실행)
```

### STATE.md URL (읽기 전용)
- **Orchestration**: https://raw.githubusercontent.com/paulseongminpark/orchestration/main/context/STATE.md
- **Portfolio**: https://raw.githubusercontent.com/paulseongminpark/portfolio_20260215/master/context/STATE.md

### 핸드오프 패턴
```bash
# orchestration에서
> /handoff gpt "포트폴리오 디자인 검증 요청"

# GPT에 붙여넣기
# (GPT가 분석)

# GPT Canvas에서 Packet 생성
# (Claude Code로 다시 전달)
```

---

## 자주하는 실수

### ❌ STATE.md 직접 편집 (Obsidian)
→ ✅ Claude Code + /sync만 사용

### ❌ 커밋 전 검증 생략
→ ✅ /verify 먼저, /sync 나중

### ❌ 여러 목표를 한 세션에
→ ✅ 1세션 = 1목표

### ❌ logs/ 파일 읽기
→ ✅ append만, 읽기 금지 (토큰 보호)

### ❌ 프로젝트 컨텍스트 없이 /sync 실행
→ ✅ 프로젝트 디렉토리에서 실행

---

## Hooks

### SessionStart (ai-config)
- 자동: 전체 프로젝트 최근 변경 표시
- 목적: 작업 시작 시 컨텍스트 파악

### PostToolUse (orchestration, ai-config)
- 트리거: Edit, Write 도구 사용
- 대상: STATE.md, CLAUDE.md, docs/*.md
- 알림: "⚠️ 중요 파일 변경. /sync 권장"

### Stop (orchestration, ai-config)
- 자동: 세션 로그 복사 (03_evidence/)
- 검증: STATE.md 미커밋 체크
- 차단: 미커밋 시 세션 종료 경고

---

## 참고 자료

- [PLANNING.md](./PLANNING.md): 아키텍처 결정 기록
- [STATE.md](./STATE.md): 현재 프로젝트 상태
- [C:\dev\CLAUDE.md](../../CLAUDE.md): 전역 규칙
- [GitHub: orchestration](https://github.com/paulseongminpark/orchestration)
