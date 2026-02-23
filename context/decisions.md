# Decisions Log

> 세션별 중요 결정 사항. compressor가 자동 append.
> 태그: pf=portfolio, tr=tech-review, ml=monet-lab, orch=orchestration
> ❌=미반영, ✅=반영완료, 🚫=취소

## 미반영

2026-02-22 [tech-review] keywords-log.md 신설, fetch-perplexity KST 버그 수정 | tr:❌
2026-02-22 [portfolio] 07~10 스크린샷 → lab.md 이미지 링크 추가 | pf:❌
2026-02-22 [tech-review] 나머지 요일 프롬프트(월~토 6개) Smart Brevity 형식 업데이트 | tr:❌
2026-02-22 [portfolio] Tech Review System 스토리텔링 글 작성 | pf:❌
2026-02-23 [orch] commit-commands, playground, claude-code-setup, skill-creator 4개 플러그인 비활성화 | orch:✅
2026-02-23 [orch] 에이전트 학습 패턴: 하이브리드 방식 채택 (compressor 수집→sync-all 검증→반영) | orch:✅
2026-02-23 [orch] v3.0 플랜 실행 (Task 1~7, Phase A~D) | orch:✅
2026-02-23 [orch] Codex CLI + Gemini CLI 교차 검증 파이프라인 최적화 | orch:✅

## 아카이브

2026-02-23 [orch] Codex CLI 교차 검증 최적화: sandbox bypass + reasoning medium + 도구 3~5회 = 2분 목표 (15분→2분) | orch:✅
2026-02-23 [orch] ~/.codex/config.toml [profiles.review] 추가 (reasoning_effort=medium, disk-full-read-access) | orch:✅
2026-02-23 [orch] codex-reviewer.md 3회 최적화: sandbox→bypass, 프롬프트 간결화, 도구 호출 3~5회 지시 | orch:✅
2026-02-23 [orch] 전체 시스템 직접 점검 완료 (16 agents, 14 skills, 19 plugins, 7 hooks) | orch:✅
2026-02-23 [orch] 플러그인 3개 비활성화 (agent-sdk-dev, hookify, code-review) | orch:✅
2026-02-23 [orch] subagent-creator 스킬 삭제 → orch-skill-builder로 통합 | orch:✅
2026-02-23 [orch] 유령 참조 제거 (STATE.md, KNOWLEDGE.md, MEMORY.md) | orch:✅
2026-02-23 [orch] SessionStart 5개 → session-start.sh 통합 | orch:✅
2026-02-23 [orch] PreToolUse 강화: git reset --hard, clean -f 차단 + 브랜치 혼동 경고 + node_modules 경고 | orch:✅
2026-02-23 [orch] PreCompact 강화: 미커밋 수 확인 + 구체적 행동 안내 | orch:✅
2026-02-23 [orch] TeammateIdle 강화: 팀원 이름 파싱 + 행동 안내 | orch:✅
2026-02-23 [orch] TaskCompleted 강화: 태스크 제목/담당자 파싱 + 다음 태스크 안내 | orch:✅
2026-02-23 [orch] v3.0 에이전틱 워크플로우 강화 플랜 8개 태스크 설계 완료 | orch:✅
2026-02-22 [ml] page-12: 카드 요약 유지 + portfolio 원본 컴포넌트 이식 방식 채택 | ml:✅
2026-02-22 [ml] 형광펜 하이라이트: color: 대신 background: rgba() + <mark> 태그 방식 | ml:✅
2026-02-22 [orch] v2.2 시스템 오버홀 — 죽은 자동화 수리, 불필요 제거, stale 수정 | orch:✅
2026-02-22 [orch] codex-reviewer 에이전트 복구 (잘못된 삭제 판단 번복) | orch:✅
2026-02-22 [orch] 역할 분리 확정: Gemini=분석, Claude/Opus=구현, Codex=결함 검증 | orch:✅
2026-02-22 [orch] codex-reviewer 2차 스캔 = Claude 명시 요청 시만 (GPT Plus 절약) | orch:✅
2026-02-22 [orch] gemini-analyzer 결과 크로스 검증 필수 (사용자 확인 없이 삭제 금지) | orch:✅
2026-02-22 [orch] compressor 확장(LOG+STATE 3곳), sync-all dev-vault | orch:✅
2026-02-22 [orch] Session Visibility System 설계 및 구현 | orch:✅
2026-02-22 [orch] PAT → Windows 환경변수, settings.json 제거 | orch:✅
2026-02-22 [orch] PreToolUse 페일클로즈 전환 (exit 2 = 차단) | orch:✅
2026-02-22 [orch] decisions.md git-tracked 전환 (orchestration/context/) | orch:✅
2026-02-22 [orch] compressor = 5곳 저장 (+ METRICS.md) | orch:✅
2026-02-22 [orch] morning-briefer = catchup + orch-state 통합 엔트리포인트 | orch:✅
2026-02-22 [orch] compressor = 4곳 저장 (session-summary + LOG + STATE.md + decisions.md) | orch:✅
2026-02-22 [orch] decisions.md 신설: ❌/✅ + 태그(pf/tr/ml/orch) 추적 시스템 | orch:✅
2026-02-22 [pf] TechReviewSystemSection.tsx 신규 생성 (8개 서브섹션) | pf:✅
2026-02-22 [pf] PIVOT 카드: GAS+Gmail → Perplexity API 전환 스토리 시각화 | pf:✅
2026-02-22 [tech-review] Smart Brevity 전면 도입, 수요일 AI×Industry | pf:✅
2026-02-22 [orch] CHANGELOG v2.0 hooks 7종 완성 | tr:✅ pf:✅
2026-02-22 [orch] orchestrator 비활성화 — Claude 직접 라우팅 | orch:✅
2026-02-22 [orch] MCP 최소화 원칙 (GitHub=gh, Puppeteer=playwright) | orch:✅
2026-02-22 [orch] PROACTIVELY 4개만 확정 | orch:✅
2026-02-22 [pf] AiWorkflowSection.tsx TS6133 빌드 에러 수정 | pf:✅
