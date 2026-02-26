# Orchestration System Roadmap

> 최종 수정: 2026-02-27

## v1.0 ✅ (2026-02-21)
**기준점 — 현재 안정 버전**
- Skills 11개, Scripts 5개, orchestrator 에이전트
- orchestration/config/ (claude/gpt/gemini/perplexity)
- Auto Memory System (3-phase)
- Daily Memo 파이프라인 (daily-memo repo)

## v2.0 ✅ (2026-02-21)
**cc-system 통합 + 볼트 Git 연동 + Worker 에이전트 구조**
- [x] crystalize-prompt 프롬프트 압축 방법론 도입
- [x] design-pipeline AI 파이프라인 설계 원칙 도입
- [x] skill-creator 스킬 (init/package/validate 자동화)
- [x] subagent-creator 스킬 (에이전트 생성 프레임워크)
- [x] hook-creator 스킬 (훅 이벤트 레퍼런스)
- [x] C:\dev git 초기화 + dev-vault GitHub 연결
- [x] CHANGELOG.md 버전 관리 체계
- [x] Skills 11 → 14개
- [x] Worker 에이전트 11개 구축 (orchestrator 업그레이드 포함)
- [x] /morning 스킬 → morning-briefer 에이전트 + TODO 연동
- [ ] Obsidian Git Auto push interval 설정 (사용자 직접)
- [x] monet-lab Worker 2개 (ml-experimenter, ml-porter)

## v2.2 ✅ (2026-02-22)
**System Overhaul — 죽은 자동화 수리, 불필요 제거**
- [x] 죽은 훅 6건 수리
- [x] 불필요 파일 17건 삭제
- [x] stale 문서 10건 최신화
- [x] MCP 서버 3개 제거 (memory, desktop-commander, sequential-thinking)
- [x] example-skills 플러그인 비활성화
- [x] docs/SYSTEM-GUIDE.md 종합 사용 가이드 작성

## v3.0 ✅ (2026-02-23)
**Hooks System + 에이전트 체계 정비**
- [x] Hooks System 구축 (PreToolUse 3, PostToolUse 3, Notification 1, SessionStart 2, SessionEnd 1)
- [x] 에이전트 체인 규칙 정립 (구현 / 배포 / 분석 / tech-review / 일일운영 / 디스패치)
- [x] Living Docs 업데이트 규칙 확립
- [x] 에이전트 16개 체계 정비 및 문서화
- [x] 플러그인 정리 (중복 비활성화)
- [x] security-auditor 에이전트 추가

## v3.1 ✅ (2026-02-23)
**Agent Teams & Linker System**
- [x] 에이전트 16 → 23개 확장
- [x] Agent Teams 3개 구성 (tech-review-ops, ai-feedback-loop, daily-ops)
- [x] Linker System 구축 (context-linker + project-linker)
- [x] live-context.md 실시간 갱신 (PostToolUse hook 연동)
- [x] Meta-orchestrator: 팀 활성화 및 태스크 디스패치
- [x] 스킬 13개 (사용자 + 플러그인 통합 집계)
- [x] README.md v3.1 업데이트

## v3.2 ✅ (2026-02-24)
**리좀형 팀 재설계 + SoT 확립**
- [x] SoT 확립: CLAUDE.md(체인), STATE.md(인벤토리), KNOWLEDGE.md(패턴)
- [x] 에이전트 23→24개 (doc-syncer 신규, pf-context→project-context)
- [x] 스킬 13→11개 (catchup/skill-creator/hook-creator 삭제, dispatch 신규)
- [x] 리좀형 4팀+허브 (ops/build/analyze/maintain + meta-orchestrator)
- [x] 리좀 연결자 (context-linker + project-linker + live-context.md)
- [x] 크로스팀 유틸리티 (commit-writer, orch-state, project-context, content-writer)
- [x] 자동화 강화 (live-context auto-trim, session-start OVERDUE)
- [x] compressor 7→9단계
- [x] 플러그인 4개 비활성화 + stale 파일 정리
- [x] REFERENCE.md (SYSTEM-GUIDE + USER-GUIDE 통합)

## v3.3 ✅ (2026-02-25)
**Codex/Gemini CLI 통합 + Verify Barrier**
- [x] Codex CLI 설정: instructions.md + config.toml 프로필 3종 + prompts 3종
- [x] Gemini CLI 설정: GEMINI.md + 스킬 4종
- [x] 에이전트 3개 재작성: gemini-analyzer(벌크추출), codex-reviewer(정밀검증), ai-synthesizer(adversarial verify)
- [x] 스킬 3개 신규: /context-scan, /tr-verify, /cross-review
- [x] Verify Barrier 3단계 (구조→스팟체크→반박)
- [x] 세션 전환 체인 신설 (verify→sync-all→compressor→context-linker)
- [x] meta-orchestrator → Opus 승격
- [x] e2e 테스트 23/23 ALL PASS (12시나리오, 1차 기본 + 2차 All Opus)
- [x] 에비던스 문서: diagram.md + members-skills.md + e2e-test-plan/report

## v3.3.1 ✅ (2026-02-26~27)
**200K Context 최적화 + Flat Root**
- [x] baseline 축소 (~10K 절감): MEMORY.md/CLAUDE.md/workflow.md/session-start.sh 경량화
- [x] .chain-temp/ 디렉토리: 에이전트 4개 체인 결과 오프로딩
- [x] compact 3단계 임계값: 100K 권장 / 120K 필수 / 150K 최후 방어선
- [x] PreCompact/PostCompact hook 추가 (스냅샷 자동 생성 + Read 안내)
- [x] Playwright/document-skills 플러그인 비활성화 (~6.5K 절감)
- [x] statusline.py 세션 목표 🎯 표시
- [x] Flat Root 폴더 개편: Living Docs 12개 루트 이동, _history/_prompts/_auto/ 신설
- [x] 에이전트 10개 + 훅 3개 + 스킬 3개 + 스크립트 1개 경로 갱신

## 다음 (미정)
- [ ] portfolio 모바일 반응형 (768px 이하)
- [ ] monet-lab 44개 미커밋 정리 (스크린샷 PNG)
- [ ] Obsidian Git Auto push 설정
- [ ] HOME.md 자동 갱신 체계

---

_최종 수정: 2026-02-27_
