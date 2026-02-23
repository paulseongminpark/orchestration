# Orchestration STATE

> 마지막 갱신: 2026-02-24 (v3.1 Living Docs + monet-lab page-12 PMCC 완성)
> /sync 스킬로 자동 갱신됩니다.

## 현재 상태

**시스템 버전**: v3.1
**활성 프로젝트**: tech-review, portfolio, orchestration, monet-lab

## 진행 중

### orchestration
- **v3.1 Living Docs 전면 갱신 완료** (2026-02-24)
  - README.md: 빈 파일 → v3.1 전체 소개 (역사, 아키텍처, 핵심 기능)
  - ROADMAP.md: v3.0, v3.1 완료 표시, v3.2 구조 정리 계획
  - SYSTEM-GUIDE.md: v3.0→v3.1 (에이전트 7개, 팀 3개, Linker)
  - USER-GUIDE.md: v3.0→v3.1 (팀 사용법, v3.1 변경점 부록)
  - HOME.md: v2.2→v3.1 반영 (프로젝트 폴더 구조, v3.1 요약)
  - compressor 강화: 7단계 MEMORY.md 추가 (agent.md + SKILL.md)
- **v3.2 계획 정리**: 문서 소스 단일화, 폴더 구조 정리 (02_ai_config, 03_evidence 등)
- **다음**: tech-review/portfolio 미반영 결정 4건 처리

### monet-lab
- **PMCC 상세페이지 완전 완성** (2026-02-24)
  - VisualCuesGallery: 9개 이미지 비대칭 배치
  - ActivityGallery: CSS grid-area 5개 항목
  - 동영상 6개 _web.mp4 변환 (hero_gather, jujitsu, hyrox, yoga, crossfit, community_voice)
  - PageEditor: DEV only (구현 중단)
  - 섹션 구분선: GALLERY, GROWTH & METRICS 앞
- **마지막 커밋**: 5e9866a + 73d1e52
- **다음**: empty-house, skin-diary 상세페이지 작업

### tech-review
- Smart Brevity 형식 전면 도입 완료
- **미완**: 월~토 프롬프트 6개 Smart Brevity 형식 업데이트
- **미완**: keywords-log.md 신설, fetch-perplexity KST 버그 수정
- **확인 필요**: 2/23 GitHub Actions 자동 생성 결과

### portfolio
- TechReviewSystemSection.tsx 신규 생성 완료
- **다음**: Tech Review System 스토리텔링 글 작성
- **미완**: 07~10 스크린샷 → lab.md 이미지 링크 추가

## 완료된 것

- [2026-02-24] v3.1 Living Docs 전면 갱신 (README, ROADMAP, SYSTEM-GUIDE, USER-GUIDE, HOME.md)
- [2026-02-24] monet-lab PMCC 상세페이지 완전 완성 (Visual Cues + Activity Gallery)
- [2026-02-24] compressor 7단계 강화 (MEMORY.md 추가)
- [2026-02-23] v3.1 Agent Teams & Linker System (에이전트 7개 + 팀 3개 + hooks)
- [2026-02-23] Codex CLI 교차 검증 파이프라인 최적화 (15분→2분)
- [2026-02-23] codex-reviewer + gemini-analyzer 병렬 Task 실행 파이프라인 구축
- [2026-02-23] v3.0 에이전틱 워크플로우 강화 (Phase A~D)
- [2026-02-23] 전체 시스템 점검 + v3.0 플랜 작성
- [2026-02-23] 플러그인 3개 비활성화 + hooks 전면 업데이트
- [2026-02-22] Gemini 교차 분석 + MCP 정리 + 종합 사용 가이드 작성
- [2026-02-22] monet-lab page-12 UI 개선 및 portfolio 원본 컴포넌트 이식
- [2026-02-22] v2.2 시스템 오버홀 완료
- [2026-02-22] CHANGELOG.md v2.0 hooks 7종 완성
- [2026-02-22] Session Visibility System 구현
- [2026-02-22] PAT 보안: settings.json 제거 → Windows 환경변수
- [2026-02-22] PreToolUse 페일클로즈 전환

## 시스템 현황

### Agents (23개)
- PROACTIVELY: code-reviewer[Opus], commit-writer[Haiku], orch-state[Sonnet], compressor[Sonnet], context-linker[Haiku], project-linker[Sonnet]
- Portfolio: pf-context[Sonnet], pf-reviewer[Opus], pf-deployer[Sonnet]
- Orchestration: orch-doc-writer[Opus], orch-skill-builder[Opus], meta-orchestrator[Sonnet]
- Monet-lab: ml-experimenter[Opus], ml-porter[Sonnet]
- Tech-review: tr-monitor[Haiku], tr-updater[Sonnet]
- AI Pipeline: gemini-analyzer[Opus], codex-reviewer[Sonnet+Codex], ai-synthesizer[Opus]
- Daily: inbox-processor[Haiku], morning-briefer[Haiku]
- 기타: content-writer[Opus], security-auditor[Sonnet]

### Teams (3개)
- tech-review-ops: tr-monitor → tr-updater → commit-writer
- ai-feedback-loop: gemini + codex → ai-synthesizer
- daily-ops: inbox-processor → orch-state → morning-briefer

### Skills (13개 글로벌)
- 운영: /morning, /sync-all, /todo, /catchup, /compressor
- 검증: /verify, /docs-review
- 분석: /session-insights, /memory-review, /research
- 생성: /skill-creator, /hook-creator
- 기타: /write

### Hooks (7종)
- SessionStart: session-start.sh 통합 스크립트 (오늘 LOG + 미커밋 + 미반영 결정 + docs-review 경과)
- SessionEnd: 미커밋 현황 + /sync 권장 + Auto Memory + MEMORY.md 경고
- PreToolUse: 위험 명령 차단 (git reset --hard, clean -f) + 브랜치 혼동 경고 + node_modules 경고
- PostToolUse: context/*.md 변경 감지
- PreCompact: 미커밋 수 확인 + 구체적 행동 안내
- TeammateIdle: 팀원 이름 파싱 + 행동 안내
- TaskCompleted: 태스크 제목/담당자 파싱 + 다음 태스크 안내

### Plugins (16개 활성)
- 비활성화됨: agent-sdk-dev, hookify, code-review (2026-02-23)

## 브랜치 정보
- orchestration: main
- portfolio: master
- dev-vault: main
- tech-review blog: main
