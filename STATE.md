# Orchestration STATE

> 마지막 갱신: 2026-02-24 (v3.2 리좀형 팀 + SoT 확립)

## 현재 상태

**시스템 버전**: v3.2
**활성 프로젝트**: tech-review, portfolio, orchestration, monet-lab

## 진행 중

### orchestration
- **v3.2 구현 진행 중** (2026-02-24)
  - SoT 확립: CLAUDE.md/STATE.md/KNOWLEDGE.md/MEMORY.md 리팩토링
  - 에이전트 배선: 5개 dead code → alive
  - 리좀형 4팀 + 디스패치 허브 재설계
  - 자동화 강화: session-start, live-context auto-trim
- **다음**: 검증 + 최종 갱신 + 커밋

### monet-lab
- PMCC 상세페이지 완성 (Visual Cues + Activity Gallery)
- **다음**: empty-house, skin-diary 상세페이지

### tech-review
- sonar-deep-research 파이프라인 전환 완료 (2026-02-24)
  - deep research + sonar-pro 폴백, URL 검증, 도메인 필터, 분량 검증
  - 프롬프트 7개: 3건→5건, 분량 강화, 일요일 글로벌 AI 현장
- **다음**: GitHub Actions 통합 테스트 (workflow_dispatch)

### portfolio
- TechReviewSystemSection.tsx 완료
- **미완**: 07~10 스크린샷 → lab.md 이미지 링크

## 시스템 인벤토리 (SoT)

### Agents (24개)
**ops 팀**: morning-briefer[Haiku], inbox-processor[Haiku], tr-updater[Sonnet], tr-monitor[Haiku]
**build 팀**: code-reviewer[Opus], pf-reviewer[Opus], pf-deployer[Sonnet], ml-experimenter[Opus], security-auditor[Sonnet]
**analyze 팀**: ai-synthesizer[Opus], gemini-analyzer[Sonnet], codex-reviewer[Sonnet+Codex]
**maintain 팀**: compressor[Sonnet], doc-syncer[Haiku], orch-doc-writer[Opus], orch-skill-builder[Opus]
**리좀 연결자**: context-linker[Haiku], project-linker[Sonnet]
**크로스팀 유틸리티**: commit-writer[Haiku], orch-state[Sonnet], project-context[Sonnet], content-writer[Opus]
**디스패치 허브**: meta-orchestrator[Sonnet]
**실험**: ml-porter[Sonnet]

### Teams (4팀 + 허브)
- **ops**: morning-briefer(리드) + inbox-processor + tr-updater + tr-monitor
- **build**: code-reviewer(리드) + pf-reviewer + pf-deployer + ml-experimenter + security-auditor
- **analyze**: ai-synthesizer(리드) + gemini-analyzer + codex-reviewer
- **maintain**: compressor(리드) + doc-syncer + orch-doc-writer + orch-skill-builder
- **허브**: meta-orchestrator (/dispatch)

### Skills (11개)
- 운영: /morning, /sync-all, /todo, /dispatch, /compressor
- 검증: /verify, /docs-review
- 분석: /session-insights, /memory-review, /research
- 기타: /write

### Hooks (7종)
- SessionStart: session-start.sh (오늘 LOG + 미커밋 + 미반영 결정 + live-context)
- SessionEnd: 미커밋 현황 + MEMORY.md 경고
- PreToolUse: 위험 명령 차단
- PostToolUse: context/*.md 감지 + live-context.md auto-append + auto-trim
- PreCompact: 미커밋 확인
- TeammateIdle: 팀원 유휴 알림
- TaskCompleted: 태스크 완료 알림

### Plugins (12개 활성)
- superpowers, context7, vercel, document-skills, playwright, greptile, frontend-design

## 브랜치 정보
- orchestration: main
- portfolio: master
- dev-vault: main
- tech-review blog: main
