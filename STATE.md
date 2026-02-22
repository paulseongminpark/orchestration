# Orchestration STATE

> 마지막 갱신: 2026-02-22 (codex-reviewer 통합 세션)
> /sync 스킬로 자동 갱신됩니다.

## 현재 상태

**시스템 버전**: v2.1 (Session Visibility System + Security Hardening)
**활성 프로젝트**: tech-review, portfolio, orchestration

## 진행 중

### tech-review
- Smart Brevity 형식 전면 도입 완료 (2/15~2/22 포스트 16개 재변환)
- 수요일 AI × Industry 큐레이션 개편 완료
- keywords-log.md 신설, KST 버그 수정 완료
- **미완**: 월~토 프롬프트 6개 Smart Brevity 형식 업데이트
- **확인 필요**: 2/23 GitHub Actions 자동 생성 결과

### portfolio
- AiWorkflowSection.tsx TS6133 빌드 에러 수정 완료
- aiWorkflowData.ts 데이터/UI 분리 완료
- TechReviewSystemSection.tsx 신규 생성 완료 (8개 서브섹션)
  - seed.ts + Page.tsx 연결 완료
  - git push master (b5a623f)
- **다음**: localhost:5173 확인 → UI 조정 → 스토리텔링 글 작성
- **미완**: 07~10 스크린샷 → lab.md 이미지 링크 추가

### orchestration
- gemini-analyzer 비판 분석 기반 시스템 overhaul 완료 (11개 태스크)
- 보안 강화: PAT → Windows 환경변수, PreToolUse 페일클로즈
- SNAPSHOT.txt 아카이브 완료 (context/archive/)
- decisions.md git-tracked 전환 (orchestration/context/)
- KNOWLEDGE.md stale 항목 정리 완료
- morning-briefer 통합 엔트리포인트로 업그레이드
- compressor 5곳 저장으로 확장 (METRICS.md 추가)
- codex-reviewer 에이전트 추가 (설계 결함 검증관)
- **다음**: v2.1 공식 문서화, codex-reviewer 실전 적용

## 완료된 것

- [2026-02-22] codex-reviewer 에이전트 생성 (Codex CLI 통합, 8개 검증 관점)
- [2026-02-22] CHANGELOG.md v2.0 hooks 7종 완성
- [2026-02-22] Session Visibility System 구현 (decisions.md + SessionStart/End Hook + compressor 확장)
- [2026-02-22] gemini-analyzer 오케스트레이션 비판 분석 + overhaul 11개 태스크 완료
- [2026-02-22] PAT 보안: settings.json 제거 → Windows 환경변수
- [2026-02-22] PreToolUse 페일클로즈 전환
- [2026-02-22] decisions.md git-tracked (orchestration/context/)
- [2026-02-22] KNOWLEDGE.md stale 정리
- [2026-02-22] morning-briefer 통합 업그레이드

## 시스템 현황

### Agents (15개)
- PROACTIVELY: code-reviewer[Opus], commit-writer[Haiku], orch-state[Sonnet], compressor[Sonnet]
- Portfolio: pf-context[Sonnet], pf-reviewer[Opus], pf-deployer[Sonnet]
- Orchestration: orch-doc-writer[Opus], orch-skill-builder[Opus]
- Monet-lab: ml-experimenter[Opus], ml-porter[Sonnet]
- Security: security-auditor[Opus]
- Analysis: gemini-analyzer[Sonnet]
- Morning: morning-briefer[Haiku]
- Codex: codex-reviewer[Sonnet+Codex] — 설계 결함 검증관

### Skills (19개)
- /sync, /handoff, /status, /catchup
- /gpt-review, /commit-push-pr
- /skill-creator, /subagent-creator, /hook-creator
- /crystalize-prompt, /design-pipeline
- /todo, /sync-all, /memory-review
- /morning, /install-github-app
- /compact (compressor 트리거)

### Hooks (9개)
- SessionStart: 미반영 decisions 출력 + git 상태 + docs-review 7일 경과 경고
- SessionEnd: git 상태 자동 출력 + MEMORY.md 150줄 초과 경고
- Stop: 미커밋 차단
- PreToolUse: 위험 명령 차단 (페일클로즈: exit 2)
- TeammateIdle, TaskCompleted, Notification
- PostToolUse, SubagentStop

## 결정 이력 (최근)
- Codex = 설계 결함 검증관 단일 역할 (명시 호출만, PROACTIVELY 아님)
- 역할 분리: Gemini=분석, Claude/Opus=구현, Codex=결함 검증
- 2차 스캔: Claude 명시 요청 시만 (GPT Plus 절약)
- compressor = 5곳 저장 (session-summary + LOG + STATE.md + decisions.md + METRICS.md)
- decisions.md: orchestration/context/decisions.md (git-tracked)
- PAT: Windows 환경변수로 관리 (settings.json 제거)
- PreToolUse 페일클로즈: exit 2 = 차단 (|| echo "" 방식 폐기)
- morning-briefer = catchup + orch-state 통합 엔트리포인트
- decisions.md: ❌/✅ + 태그(pf/tr/ml/orch) 추적
- Smart Brevity = Today in One Line + Why it matters + 불릿3 + What's next
- orchestrator 비활성화 — Claude 직접 라우팅
- MCP 최소화 원칙
- Tech Review System 섹션: AiWorkflowSection 동일 C 객체 팔레트 사용

## 브랜치 정보
- orchestration: main
- portfolio: master
- dev-vault: main
- tech-review blog: main
- monet-lab: master (리모트 미연결)
