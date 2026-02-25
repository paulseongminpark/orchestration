# Orchestration STATE

> 마지막 갱신: 2026-02-25 (v3.3 구현 완료 + e2e PASS)

## 현재 상태

**시스템 버전**: v3.3
**활성 프로젝트**: tech-review, portfolio, orchestration, monet-lab

## 진행 중

### orchestration
- **v3.2 완료** (2026-02-24, 커밋 2977f78 + 83970f1)
  - SoT 확립: CLAUDE.md/STATE.md/KNOWLEDGE.md/MEMORY.md 리팩토링
  - 리좀형 4팀 + 디스패치 허브 재설계 완료
  - doc-syncer 신규, /dispatch 신규, live-context auto-trim
  - pf-context → project-context 범용화
- **v3.3 구현 완료** (2026-02-25, 커밋 b57c15c, 048572a, 3f9f87d, 174505d)
  - Codex CLI: instructions.md + config.toml 프로필 3종(extract/verify/review) + prompts 3종
  - Gemini CLI: GEMINI.md + 스킬 4종(system/project/state-scanner, news-verifier)
  - Claude 에이전트 3개 재작성: gemini-analyzer(벌크추출), codex-reviewer(정밀검증), ai-synthesizer(adversarial verify)
  - Claude 스킬 3개 신규: /context-scan, /tr-verify, /cross-review
  - 세션 전환 체인 신설 (CLAUDE.md + KNOWLEDGE.md)
  - Verify Barrier 3단계 (구조→스팟체크→반박)
  - e2e 테스트 23/23 ALL PASS
- **다음**: Obsidian 문서화 + Gemini system-scanner 실전 재테스트

### monet-lab
- PMCC 상세페이지 완성 (Visual Cues + Activity Gallery)
- **다음**: empty-house, skin-diary 상세페이지

### tech-review
- sonar-deep-research 파이프라인 전환 완료 (2026-02-24)
  - deep research + sonar-pro 폴백, URL 검증, 도메인 필터, 분량 검증
  - 프롬프트 7개: 3건→5건, 분량 강화, 일요일 글로벌 AI 현장
- **다음**: GitHub Actions 통합 테스트 (workflow_dispatch)

### daily-memo
- GitHub Actions 자동 sync 파이프라인 완성 (2026-02-25)
  - 핸드폰 Claude Code → 브랜치 push → Actions → main Inbox.md 자동 반영
  - 워크플로우: `.github/workflows/sync-claude-to-main.yml`
  - 레포 알림 무시 설정 완료 (이메일 수신 안 함)
- **다음**: daily-ops 팀 연동 실전 테스트 (/todo, /morning)

### portfolio
- TechReviewSystemSection.tsx 완료
- **미완**: 07~10 스크린샷 → lab.md 이미지 링크

## 시스템 인벤토리 (SoT)

### Agents (24개)
**ops 팀**: morning-briefer[Haiku], inbox-processor[Haiku], tr-updater[Sonnet], tr-monitor[Haiku]
**build 팀**: code-reviewer[Opus], pf-reviewer[Opus], pf-deployer[Sonnet], ml-experimenter[Opus], security-auditor[Sonnet]
**analyze 팀**: ai-synthesizer[Opus,adversarial-verify], gemini-analyzer[Sonnet,벌크추출], codex-reviewer[Sonnet,정밀검증]
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

### Skills (14개)
- 운영: /morning, /sync-all, /todo, /dispatch, /compressor
- 검증: /verify, /docs-review, /cross-review
- 분석: /session-insights, /memory-review, /research, /context-scan
- 콘텐츠: /write, /tr-verify

### 외부 CLI 설정 (v3.3)
- **Codex CLI**: instructions.md(글로벌), config.toml 프로필(review/extract/verify), prompts 3종
  - 경로: /c/Users/pauls/.codex/
  - 5시간 롤링 제한 주의
- **Gemini CLI**: GEMINI.md(글로벌), skills 4종(system-scanner/project-scanner/state-scanner/news-verifier)
  - 경로: /c/Users/pauls/.gemini/
  - 절대 경로 필수 (/c/Users/pauls/): ~/ 사용 금지 (로컬 .claude/ 우선 읽기 문제)
  - -m gemini-3.1-pro-preview 필수

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
