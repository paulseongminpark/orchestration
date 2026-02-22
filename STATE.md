# Orchestration STATE

> 마지막 갱신: 2026-02-22 (세션 최종)
> /sync 스킬로 자동 갱신됩니다.

## 현재 상태

**시스템 버전**: v2.1 (Session Visibility System 추가)
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
- **다음**: Tech Review System 섹션 구현 (portfolio_ui_test_v2, localhost:5173)

### orchestration
- CHANGELOG.md v2.0 hooks 7종 완성
- Session Visibility System 구현 완료
  - decisions.md (~/.claude/)
  - SessionStart/SessionEnd Hook 강화
  - compressor 4곳 저장 확장
- **다음**: v2.1 공식 문서화

## 시스템 현황

### Agents (14개)
- PROACTIVELY: code-reviewer[Opus], commit-writer[Haiku], orch-state[Sonnet], compressor[Sonnet]
- Portfolio: pf-context[Sonnet], pf-reviewer[Opus], pf-deployer[Sonnet]
- Orchestration: orch-doc-writer[Opus], orch-skill-builder[Opus]
- Monet-lab: ml-experimenter[Opus], ml-porter[Sonnet]
- Security: security-auditor[Opus]
- Analysis: gemini-analyzer[Sonnet]
- Morning: morning-briefer[Haiku]

### Skills (19개)
- /sync, /handoff, /status, /catchup
- /gpt-review, /commit-push-pr
- /skill-creator, /subagent-creator, /hook-creator
- /crystalize-prompt, /design-pipeline
- /todo, /sync-all, /memory-review
- /morning, /install-github-app
- /compact (compressor 트리거)

### Hooks (9개)
- SessionStart: 미반영 decisions 출력 + git 상태
- SessionEnd: git 상태 자동 출력
- Stop: 미커밋 차단
- PreToolUse: 위험 명령 차단
- TeammateIdle, TaskCompleted, Notification
- PostToolUse, SubagentStop

## 결정 이력 (최근)
- compressor = 4곳 저장 (session-summary + LOG + STATE.md + decisions.md)
- decisions.md: ❌/✅ + 태그(pf/tr/ml/orch) 추적
- Smart Brevity = Today in One Line + Why it matters + 불릿3 + What's next
- orchestrator 비활성화 — Claude 직접 라우팅
- MCP 최소화 원칙

## 브랜치 정보
- orchestration: main
- portfolio: master
- dev-vault: main
- tech-review blog: main
- monet-lab: master (리모트 미연결)
