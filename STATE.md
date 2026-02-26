# Orchestration STATE

> 마지막 갱신: 2026-02-27 (v3.3.1 Flat Root 폴더 개편)

## 현재 상태

**시스템 버전**: v3.3.1
**활성 프로젝트**: tech-review, portfolio, orchestration, monet-lab

## 진행 중

### orchestration
- **v3.2 완료** (2026-02-24, 커밋 2977f78 + 83970f1)
  - SoT 확립: CLAUDE.md/STATE.md/KNOWLEDGE.md/MEMORY.md 리팩토링
  - 리좀형 4팀 + 디스패치 허브 재설계 완료
  - doc-syncer 신규, /dispatch 신규, live-context auto-trim
  - pf-context → project-context 범용화
- **v3.3 완전 완료** (2026-02-25, 커밋 b57c15c, 048572a, 3f9f87d, 174505d, abcbc05, 95c09e2, ba0aa78)
  - Codex CLI: instructions.md + config.toml 프로필 3종(extract/verify/review) + prompts 3종
  - Gemini CLI: GEMINI.md + 스킬 4종(system/project/state-scanner, news-verifier)
  - Claude 에이전트 3개 재작성: gemini-analyzer(벌크추출), codex-reviewer(정밀검증), ai-synthesizer(adversarial verify)
  - Claude 스킬 3개 신규: /context-scan, /tr-verify, /cross-review
  - 세션 전환 체인 신설 (CLAUDE.md + KNOWLEDGE.md)
  - Verify Barrier 3단계 (구조→스팟체크→반박)
  - e2e 테스트 23/23 ALL PASS
  - meta-orchestrator → Opus 승격
  - compressor 타임스탬프 버그 수정 (date +%H:%M 필수)
  - 에비던스 문서 2건: docs/evidence/v3.3/diagram.md + members-skills.md
  - HOME.md + REFERENCE.md v3.3 업데이트
- **v3.3 e2e 테스트 완료** (2026-02-25, 커밋 3ca51cf, 10648e1)
  - 12개 시나리오: 26에이전트 + 12스킬 + 8훅 + 5체인 + 5팀 + 2CLI
  - 1차(기본 모델): FAIL 0, WARN 3 / 2차(All Opus): 추가 발견 +15건
  - 버그 3건 수정: meta-orchestrator model, Codex 문법, PreToolUse 파싱
  - 에비던스: docs/evidence/v3.3/e2e-test-plan.md + e2e-test-report.md
- **v3.3.1 완료** (2026-02-26)
  - 200K Context 최적화: baseline 축소(~4K), .chain-temp 오프로딩, compact 전략
  - MEMORY.md/CLAUDE.md/KNOWLEDGE.md 경량화
  - decisions.md 정리 (중복 제거, ✅→아카이브)
  - session-start.sh 축소 (❌만 5건, live-context 5줄)
  - 에이전트 4개 .chain-temp 오프로딩 (code-reviewer, gemini-analyzer, codex-reviewer, ai-synthesizer)
  - PreCompact 스냅샷 hook + PostCompact 자동 Read hook
  - Playwright/document-skills 플러그인 비활성화 (~6.5K 토큰 절감)
  - statusline.py 세션 목표 🎯 표시
- **Flat Root 폴더 개편** (2026-02-27)
  - Living Docs 12개 루트로 이동 (context/, docs/, config/docs/ → root)
  - _history/ (logs, plans, evidence, archive), _prompts/ (claude/gemini/gpt/perplexity), _auto/ (live-context, .chain-temp)
  - 에이전트 10개 + 훅 3개 + 스킬 3개 + 스크립트 1개 경로 갱신
  - context/, docs/, config/, logs/ 폴더 삭제
- **다음**: portfolio 모바일 반응형 + Tech Review 설계 섹션 + monet-lab 미커밋 정리

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
**디스패치 허브**: meta-orchestrator[Opus]
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

### Hooks (8종)
- SessionStart: session-start.sh (미커밋 + ❌결정 5건 + live-context 5줄 + 스냅샷 알림)
- SessionEnd: 미커밋 현황 + MEMORY.md 경고
- PreToolUse: 위험 명령 차단
- PostToolUse: *.md 감지 + _auto/live-context.md auto-append + auto-trim
- PreCompact: pre-compact.sh (스냅샷 생성 + 미커밋 경고)
- PostCompact: 스냅샷 자동 Read 안내
- TeammateIdle: 팀원 유휴 알림
- TaskCompleted: 태스크 완료 알림

### Plugins (4개 활성)
- superpowers, context7, vercel, frontend-design

## 브랜치 정보
- orchestration: main
- portfolio: master
- dev-vault: main
- tech-review blog: main
