# PLANNING — Architecture Decisions

아키텍처 결정 기록 (Architecture Decision Records). 왜 이렇게 했는가.

---

## D-019: 토큰 관리 자동화 (2026-02-17)

**문제**: Opus 전환 시 비용 관리 필수, 수동 체크로는 부족

**결정**: 10만 단위 토큰 관리 + 자동화
- 0-100K: 일반 모드
- 100K-150K: /token-mode 권장
- 150K+: /compact 필수
- SessionStart Hook: 자동 알림
- token-monitor.sh: 백그라운드 모니터링

**이유**:
- 비용 관리: Opus는 Sonnet 대비 10배 비용
- 명확한 기준: 10만 단위로 단순화
- 자동화: 세션 시작 시 규칙 알림

**영향**:
- 글로벌 settings.json: model=opus, CLAUDE_CODE_EFFORT_LEVEL=high
- SessionStart Hook: 토큰 규칙 알림
- ~/.claude/scripts/token-monitor.sh: 실시간 모니터링
- /token-check 스킬 추가

**대안 고려**:
- 턴 수 기반 추정: → 부분 채택 (token-monitor.sh)
- 실시간 API 체크: → 불가능 (Claude Code API 없음)
- MCP 서버 (메모리 관리): → 보류 (현재 시스템 충분)

---

## D-018: 행동 모드 스킬 (2026-02-17)

**문제**: 토큰 관리가 수동, 리서치 워크플로우 없음

**결정**: SuperClaude Framework 패턴 적용
- /token-mode: 토큰 효율 모드
- /research: 딥 리서치 워크플로우

**이유**:
- 자동화: 모드 기반 토큰 관리
- 구조화: 리서치 프로세스 표준화
- 품질: 코드베이스 + 웹 + 크로스 검증

**영향**:
- 글로벌 스킬 2개 추가 (token-mode, research)
- 토큰 150K+ 시 /token-mode 활성화
- 대량 리서치 시 /research 사용

**대안 고려**:
- MCP 서버 (Serena, Tavily): → 보류 (멀티 AI 전략 유지)
- 16개 도메인 에이전트: → 보류 (서브에이전트 충분)

---

## D-017: 문서 3분화 (2026-02-17)

**문제**: STATE.md에 현재+과거+규칙이 혼재, 토큰 낭비

**결정**: SuperClaude Framework 패턴 적용
- STATE.md: 지금 상태 (고수준, "어디에 있는가")
- PLANNING.md: 아키텍처 결정 (ADR, "왜 이렇게 했는가")
- KNOWLEDGE.md: 모범 사례 (규칙, "어떻게 해야 하는가")

**이유**:
- 토큰 효율: 필요한 문서만 읽기
- 명확성: 역할 분리 (현재/결정/규칙)
- 온보딩: 신규 기여자/AI 학습 용이

**영향**:
- orchestration, portfolio에 PLANNING.md, KNOWLEDGE.md 추가
- STATE.md "과거 결정" 섹션 제거 → PLANNING.md 이동
- CLAUDE.md Read Priority 업데이트

**대안 고려**:
- 단일 STATE.md 유지: → 기각 (토큰 비효율, 역할 불명확)
- Wiki 별도 운영: → 기각 (Git 외부 의존성 증가)

---

## D-016: 검증 시스템 도입 (2026-02-17)

**문제**: 커밋 전 수동 체크, 실수 발생 (브랜치 불일치, STATE.md 미커밋, 커밋 메시지 형식)

**결정**: kimoring-ai-skills 패턴 채택
- verify-* 스킬 구조
- /verify 통합 검증
- /sync에 자동 검증 통합

**이유**:
- 자동화: 수동 체크 제거
- 일관성: 프로젝트 규칙 강제
- 토큰 보호: 사전 검증으로 재작업 방지

**영향**:
- /sync 워크플로우 변경 (Step 0: 검증)
- 글로벌 스킬 3개 추가 (verify, verify-project-rules, verify-log-format)

**대안 고려**:
- Pre-commit hook: Git 훅으로 자동 검증 → 기각 (유연성 부족)
- Manual checklist: 수동 체크리스트 → 기각 (휴먼 에러)

---

## D-015: /sync-all 글로벌화 (2026-02-17)

**문제**: /sync-all이 ai-config에서만 실행 가능

**결정**: 글로벌 스킬로 이동 (C:\Users\pauls\.claude\skills\sync-all\)

**이유**:
- 범용성: 절대 경로 사용 (C:/dev/01_projects/*)
- 편의성: 어디서든 전체 프로젝트 동기화

**영향**:
- ai-config/.claude/skills/sync-all 삭제
- C:\dev 어디서든 /sync-all 실행 가능

---

## D-014: SoT 전환 (2026-02-15)

**문제**: Obsidian 볼트 편집 시 충돌, Git 히스토리 누락

**결정**: SoT = Git (STATE.md)
- Claude Code = 유일한 쓰기
- Obsidian = 읽기 전용 뷰어 (Junction)
- GPT/Gemini/Perplexity = raw.githubusercontent.com으로 읽기

**이유**:
- Single Source of Truth: Git이 유일한 진실
- 충돌 방지: 쓰기 권한 분리
- 감사 추적: Git 히스토리로 모든 변경 추적

**영향**:
- Obsidian에서 context/ 편집 금지
- 모든 STATE.md 변경은 Claude Code + /sync로만

---

## D-013: 3-Layer 로깅 (2026-02-15)

**문제**: LOGS/TODAY.md 파일이 커져서 토큰 낭비, 세션 상세 누락

**결정**:
- Layer 1: STATE.md (고수준, "지금 어디")
- Layer 2: logs/날짜.md (상세, "언제 뭘 왜")
- Layer 3: 03_evidence/ (raw, 세션 전문)

**이유**:
- 토큰 효율: 고수준만 읽기, 상세는 append만
- 감사 추적: 세션 전문 보존
- 검색 가능: 날짜별 분리

**영향**:
- LOGS/ 폐기
- /sync 워크플로우 변경 (LOG append)
- Stop hook: 세션 로그 자동 복사

---

## D-012: CLAUDE.md 축소 (2026-02-15)

**문제**: 146줄 CLAUDE.md = 매 세션 토큰 낭비

**결정**: 4줄 글로벌 + rules/ + 프로젝트별
- C:\dev\CLAUDE.md: 4줄 (언어, 출력, 불확실 처리, 범위)
- C:\Users\pauls\.claude\rules\: git_workflow.md, token_budget.md
- 프로젝트별: 고유 규칙만

**이유**:
- 토큰 95% 절감
- 중복 제거 (계층 구조)
- 유지보수 향상 (단일 수정 지점)

**영향**:
- 모든 프로젝트 CLAUDE.md 재작성
- 재귀 로드 활성화 (CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1)

---

## D-011: Jeff Su 방법론 채택 (2026-02-15)

**문제**: 폴더 구조 불명확, 프로젝트 우선순위 없음

**결정**: Jeff Su PARA 변형
- 5레벨 MAX
- 2자리 넘버링 (01_, 02_)
- 99=Archive

**이유**:
- 명확성: 숫자로 우선순위 표시
- 확장성: 99개까지 정렬 유지
- 표준: 널리 알려진 방법론

**영향**:
- C:\dev\ 폴더 재구조화
- 01_projects, 02_ai_config, 03_evidence, 99_archive

---

## D-010: Permissions.deny 전환 (2026-02-15)

**문제**: .claudeignore 파일이 작동 안 함

**결정**: .claude/settings.json의 permissions.deny 사용

**이유**:
- 공식 지원: settings.json은 공식 기능
- 강력함: Read/Edit/Bash 모두 제어
- 명확함: JSON 구조

**영향**:
- .claudeignore 삭제
- orchestration, ai-config settings.json 설정

---

## D-009: Junction 선택 (2026-02-15)

**문제**: Symlink는 Windows에서 관리자 권한 필요

**결정**: Junction 사용 (mklink /J)

**이유**:
- 관리자 권한 불필요
- 디렉토리만 지원 (파일 불가) → 오케스트레이션엔 충분
- 안정성: Windows 네이티브

**영향**:
- ai-config/projects/ 아래 Junction으로 연결
- Obsidian 실시간 보기 가능

---

## 템플릿

### D-XXX: 결정 제목 (YYYY-MM-DD)

**문제**: 무엇이 문제였는가

**결정**: 어떻게 해결했는가

**이유**:
- 왜 이 방법을 선택했는가
- 어떤 이점이 있는가

**영향**:
- 시스템에 어떤 변화가 생겼는가
- 어떤 파일/워크플로우가 변경되었는가

**대안 고려** (선택):
- 고려했지만 채택하지 않은 방법
- 왜 기각했는가
