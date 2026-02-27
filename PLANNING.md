# PLANNING — Architecture Decisions

> 최종 수정: 2026-02-27

아키텍처 결정 기록 (Architecture Decision Records). 왜 이렇게 했는가.

---

## D-024: Context as Currency v4.0 (2026-02-27)

**문제**:
1. 에이전트 24개 → 세션 baseline 과다 (에이전트 정의 로딩)
2. 스킬 14개 중 사용 빈도 낮은 스킬이 토큰 점유
3. Claude/Codex/Gemini CLI 간 컨텍스트 공유 수단 없음
4. rulesync 없이 규칙 동기화 수동 (CLAUDE.md ↔ GEMINI.md ↔ AGENTS.md)
5. 병렬 작업 시 격리 환경(worktree) 부재

**결정**: 에이전트 통합 + 스킬 축소 + Cross-CLI 인프라 + worktree
- Phase 1: 에이전트 24→15 (삭제 4 + 병합 10→5 + memory:user 3개)
  - 삭제: morning-briefer, inbox-processor, tr-monitor, tr-updater (→ daily-ops, tr-ops로 병합)
  - 병합: project-linker+context-linker→linker, pf-reviewer+pf-deployer→pf-ops, doc-syncer+orch-doc-writer→doc-ops
  - memory:user 전환: content-writer, orch-skill-builder, ml-experimenter
- Phase 2: 스킬 14→9 (삭제 9, 신규 4: /status, /handoff, /session-insights, /context-scan→disable)
  - AUTOCOMPACT 50%, disable-model-invocation
- Phase 3: rulesync v7.9.0 도입 (.rulesync/ SoT → CLAUDE.md/GEMINI.md/AGENTS.md 자동 생성)
- Phase 4: Codex CLI 세팅 (config.toml 프로필 4종: review/implement/extract/verify + 스킬 5종 + worktree 템플릿)
- Phase 5: Gemini CLI 세팅 (settings.json + bulk-extract + Conductor)
- Phase 6: .ctx/ Cross-CLI 공유 메모리 (shared-context.md + provenance.log + hooks)
- Phase 7: Worktree 인프라 (create/cleanup 스크립트 + /handoff 스킬)
- Phase 8: Living Docs 전체 갱신 + 최종 검증

**이유**:
- 에이전트 통합: 유사 기능 에이전트 병합 → baseline 토큰 절감 + 관리 복잡도 감소
- 스킬 축소: 저빈도 스킬 제거 → 로딩 토큰 절감
- rulesync: 규칙 SoT 1곳 관리 → 멀티 CLI 규칙 불일치 제거
- .ctx/: CLI 간 작업 위임 시 컨텍스트 유실 방지
- worktree: 병렬 CLI 작업 시 git 충돌 방지

**영향**:
- 에이전트 24→15, 스킬 14→9, 팀 구조 유지 (4+허브)
- .rulesync/ 디렉토리 신설 (rules/ SoT)
- .ctx/ 디렉토리 신설 (shared-context.md, provenance.log)
- scripts/ 2개 신설 (worktree-create.sh, worktree-cleanup.sh)
- Codex config.toml 프로필 3→4종 (implement 추가)
- /handoff 스킬 신규 (CLI 간 위임)
- Living Docs 12개 전체 갱신

**대안 고려**:
- 에이전트 수 유지 + 지연 로딩만: baseline 절감 불충분 → 기각
- MCP 서버로 CLI 통합: 유연성 부족, 설정 복잡 → 기각
- 단일 CLI(Claude만): Gemini 1M/Codex 정밀검증 못 씀 → 기각

---

## D-023: 200K Context 최적화 v3.3.1 (2026-02-26)

**문제**:
1. baseline ~46K 토큰으로 작업 가용 영역 부족 (200K 중 절반 이상 고정 소모)
2. 에이전트 체인 결과가 메인 context에 직접 포함 → compact 빈번
3. compact 시 맥락 유실 위험 (스냅샷 없음)

**결정**: baseline 축소 + .chain-temp 오프로딩 + compact 3단계 전략
- MEMORY.md 축약 (~700 tokens 절감): Common Patterns 제거, Codex/Gemini 1줄 축약, 교훈 8→3
- CLAUDE.md 경량화 (~400 tokens): 프로젝트 구조→"MEMORY.md 참조", CLI 플래그→에이전트 위임
- workflow.md 모델 섹션 제거 (~100 tokens)
- session-start.sh 축소 (~1,000 tokens): ❌만 5건, live-context 5줄
- Playwright/document-skills 플러그인 비활성화 (~6.5K tokens)
- .chain-temp/ 디렉토리: 에이전트 체인 중간 결과 파일 오프로딩
- 에이전트 4개 .chain-temp 오프로딩: code-reviewer, gemini-analyzer, codex-reviewer, ai-synthesizer
- PreCompact hook: 스냅샷 자동 생성 (compact 전 맥락 보존)
- PostCompact hook: 스냅샷 자동 Read 안내
- compact 임계값: 100K 권장, 120K 필수, 150K 최후 방어선

**이유**:
- baseline 축소: ~10K 토큰 절감 → 작업 20~30턴 추가 여유
- .chain-temp: 체인 결과를 파일로 전달 → 메인 context에 1줄 요약만 (체인 예약 ~25K 절약)
- 스냅샷: 언제 compact해도 맥락 보존 보장
- 3단계 임계값: 명확한 기준으로 수동 판단 제거

**영향**:
- MEMORY.md, CLAUDE.md, workflow.md, session-start.sh, KNOWLEDGE.md 경량화
- .chain-temp/ 디렉토리 및 패턴 신설
- 에이전트 4개 오프로딩 로직 추가
- PreCompact/PostCompact hook 2개 추가 (총 8종)
- statusline.py 세션 목표 🎯 표시
- dispatch SKILL.md 갱신

**대안 고려**:
- auto-compact 임계값만 조정: 근본 해결 안 됨 (baseline이 큰 게 문제) → 기각
- 에이전트 수 축소: 기능 손실 → 기각
- 서브에이전트 전면 전환: 의사결정 품질 저하 → 기각, 병행 전략 채택

---

## D-022: Codex/Gemini CLI 통합 v3.3 (2026-02-25)

**문제**:
1. 외부 CLI(Codex, Gemini) 결과를 Claude가 무비판적 수용 → 오류 전파 위험
2. 세션당 ~195K 토큰 소모 (대규모 분석 시)
3. 외부 CLI 역할 불명확 (중복 실행, 비효율)

**결정**: Claude=결정권자, Codex=정밀검증, Gemini=벌크추출 + Verify Barrier 3단계
- Codex CLI: instructions.md + config.toml 프로필 3종(extract/verify/review) + prompts 3종
- Gemini CLI: GEMINI.md + 스킬 4종(system/project/state-scanner, news-verifier)
- 에이전트 3개 재작성: gemini-analyzer(벌크추출), codex-reviewer(정밀검증), ai-synthesizer(adversarial verify)
- 스킬 3개 신규: /context-scan, /tr-verify, /cross-review
- Verify Barrier: 구조 검증 → 스팟체크 → 반박 검증
- _meta 블록: 외부 CLI JSON 출력에 검증용 메타데이터 강제
- 세션 전환 체인: verify → sync-all → compressor → context-linker
- meta-orchestrator → Opus 승격

**이유**:
- 역할 분리: Gemini=벌크(1M 컨텍스트, 넉넉), Codex=정밀(5시간 롤링, 귀한 자원)
- Verify Barrier: 외부 추출 결과를 Claude(Opus)가 3단계 검증 → 오류 전파 차단
- 토큰 절약: 세션당 ~170K 토큰(88%) 절감 (컨텍스트 오프로딩)
- Claude 독립성: 해석은 Claude만, 외부는 사실 추출만

**영향**:
- Codex/Gemini CLI 설정 파일 구축 (~/.codex/, ~/.gemini/)
- 에이전트 3개 재작성 + 스킬 3개 신규
- CLAUDE.md: 추출/검증 체인 + 세션 전환 체인 추가
- KNOWLEDGE.md: 멀티 AI 오케스트레이션 섹션 추가
- e2e 테스트 23/23 ALL PASS (에비던스: _history/evidence/v3.3/)

**대안 고려**:
- 외부 CLI 결과 무조건 신뢰: 오류 전파 위험 → 기각
- Claude만으로 모든 분석: 토큰 한계 (200K) → 기각
- MCP 서버로 통합: 유연성 부족 → 기각, CLI 직접 호출이 더 유연

---

## D-021: 리좀형 팀 재설계 + SoT 확립 v3.2 (2026-02-24)

**문제**:
1. 정보 분산: 에이전트/스킬 목록이 STATE, KNOWLEDGE, MEMORY, SYSTEM-GUIDE에 중복
2. 5개 에이전트 dead code (context-linker, project-linker, meta-orchestrator, orch-doc-writer, pf-context)
3. 3개 팀이 국소적 (워크플로우별만, 크로스팀 연결 없음)
4. live-context.md 무한 팽창

**결정**: SoT 확립 + 리좀형 4팀 + 디스패치 허브
- SoT 맵: STATE.md(인벤토리), CLAUDE.md(체인), KNOWLEDGE.md(패턴), CHANGELOG.md(이력)
- 4팀: ops/build/analyze/maintain + meta-orchestrator 허브
- 리좀 연결자: context-linker + project-linker + live-context.md (팀 소속 없음, 모든 팀 관통)
- 크로스팀 유틸리티: commit-writer, orch-state, project-context, content-writer
- pf-context → project-context 범용화 (프로젝트 파라미터)
- doc-syncer 신규 (3레이어 검증)
- live-context.md auto-trim 100줄 캡

**이유**:
- SoT: 정보 1곳 관리 → 불일치 제거, 토큰 ~3,700 절감
- 리좀형: 수평 자율 팀 + 수직 조율 리드 → 유연한 조합
- 연결자: 팀 간 정보 흐름이 live-context.md 경유 → 중앙집중 없이 협력
- auto-trim: 무한 팽창 방지, 300 토큰 상한

**영향**:
- CLAUDE.md 89→60줄, KNOWLEDGE.md 366→120줄, MEMORY.md 89→55줄
- 에이전트 23→24, 스킬 13→11, 팀 3→4+허브
- SYSTEM-GUIDE + USER-GUIDE → REFERENCE.md 통합
- config/docs/ 9개 stale → archive
- session-start.sh, post-tool-live-context.sh 업데이트

**대안 고려**:
- 허브-스포크만 (meta-orch가 모든 팀 제어): 단일 실패점, 토큰 소모 → 기각
- 팀 없이 개별 에이전트만: 크로스팀 협력 불가 → 기각
- 중앙 데이터베이스 SoT: Git 외부 의존성 → 기각

---

## D-020: Agent Teams & Linker System v3.1 (2026-02-23)

**문제**:
1. 동시 열린 여러 Warp 세션 간 맥락 공유 불가
2. 프로젝트 간 변경 영향 수동 추적
3. tech-review 반복 작업 수동
4. 멀티 AI 분석 결과 수동 통합

**결정**: B+C 하이브리드 — 팀 기반 + Meta-Orchestrator
- 신규 에이전트 7개 (16→23): context-linker, project-linker, meta-orchestrator, inbox-processor, tr-monitor, tr-updater, ai-synthesizer
- 팀 3개: tech-review-ops, ai-feedback-loop, daily-ops
- PostToolUse hook으로 live-context.md 실시간 append (0 토큰)
- context-linker는 주기적 Haiku 호출로 정리/스캔
- project-linker는 커밋 시점만 트리거 (토큰 절약)
- meta-orchestrator는 Sonnet (Opus 불필요, 트리아지만)

**이유**:
- 팀 구조: Phase E 팀 기능 활용, 워크플로우 단위 관리
- Meta-Orchestrator: 중앙 디스패치로 불필요한 팀 활성화 방지
- 토큰 최적화: hook(0토큰) + Haiku(경량) + 커밋 시점 트리거 = 일 $0.81 추가(+6%)

**대안 고려**:
- A. 개별 에이전트만 추가: 단순하지만 팀 조율 부재 → 기각
- C. 허브-스포크만: meta-orch 단일 실패점, 토큰 소모 큼 → 기각
- 매 Edit마다 Sonnet 호출: 일 $10 + 레이턴시 → 기각, 커밋 시점으로 최적화

**영향**:
- CLAUDE.md: 체인 규칙 5개 추가
- STATE.md: v3.1, Agents 23개, Teams 3개
- KNOWLEDGE.md: 체인/에이전트/hooks 섹션 v3.1 업데이트
- settings.json: PostToolUse hook 추가
- context/live-context.md: 신규 파일
- 설계 문서: docs/plans/2026-02-23-agent-teams-design.md

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
