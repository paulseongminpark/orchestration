# KNOWLEDGE — Best Practices

> 최종 수정: 2026-02-27

프로젝트 규칙, 패턴, 모범 사례. 에이전트/스킬/팀 목록은 **STATE.md** 참조.

---

## Git 규칙

- **orchestration**: main, **portfolio**: master
- 커밋: `[project] 한줄 설명` + `Co-Authored-By:`
- 금지: `git push --force`, `git clean -f`, `git reset --hard`, `--no-verify`

## 파일 구조 (Flat Root, v3.3.1)

```
orchestration/
├── *.md (12개)       # Living Docs — 루트에서 바로 접근
│   ├── STATE.md      # 시스템 인벤토리 SoT
│   ├── CHANGELOG.md  # 버전 이력
│   ├── KNOWLEDGE.md  # 규칙, 패턴 (이 파일)
│   ├── PLANNING.md   # ADR (설계 결정)
│   ├── REFERENCE.md  # 종합 가이드
│   ├── ROADMAP.md    # 개발 계획
│   ├── METRICS.md    # 시스템 지표
│   ├── TODO.md       # 작업 관리
│   ├── decisions.md  # 결정 추적 (❌/✅)
│   ├── session-summary.md  # 세션 요약
│   └── pending.md    # 미반영 결정
├── _history/         # 시간순 기록 (읽기 전용)
│   ├── logs/         # 세션 로그
│   ├── plans/        # 설계 문서
│   ├── evidence/     # 버전별 검증 기록
│   └── archive/      # 아카이브
├── _prompts/         # 외부 AI 프롬프트
├── _auto/            # 자동 관리 (에이전트 전용)
│   ├── live-context.md   # 세션 간 공유 (100줄 캡)
│   └── .chain-temp/      # 체인 중간 결과 오프로딩
└── scripts/          # 훅 스크립트
```

## 토큰 관리 (200K Context, v3.3.1)

- 1세션=1목표
- **100K → compact 권장, 120K → compact 필수** (150K auto-compact은 최후 방어선)
- compact 요약: 200자 이내, 파일명+결정 위주, 대화 반복 금지
- compact 전 스냅샷 → compact 후 자동 Read → 맥락 보존
- 읽기 금지: node_modules/, .git/, dist/, build/, logs/
- 서브에이전트: Haiku(요약) / Sonnet(분석) / Opus(설계)

## .chain-temp 패턴 (v3.3.1)

체인 에이전트 결과를 파일로 오프로딩, 메인 context에 1줄 요약만 반환:
- `code-reviewer` → `.chain-temp/review-{date}.md`, 메인에 "3 RED, 2 YELLOW"
- `gemini-analyzer` → `.chain-temp/gemini-{date}.txt`, 메인에 "추출 N건"
- `codex-reviewer` → `.chain-temp/codex-{date}.txt`, 메인에 요약 1줄
- `ai-synthesizer` → `.chain-temp/synthesis-{date}.md`, 메인에 GO/NO-GO
- `compressor` → `.chain-temp/docs-{date}.md` (doc-ops 결과)
- 다음 체인 에이전트는 `.chain-temp/` 파일을 직접 Read

## 200K 세션 운영 (v3.3.1)

```
200K 세션 예산
├── Baseline:        ~42K (고정)
├── 작업 Phase:     42K → 100K (~20-30 턴)
├── Compact 후:     ~50K → 100K까지 추가 작업
├── 체인 예약:      ~25K (.chain-temp 사용)
└── Auto-compact:   150K (최후 방어선)
```

체인 전 확인: 현재 context + 25K < 120K

## 리좀형 팀 구조 (v4.0)

```
meta-orchestrator (디스패치 허브, /dispatch)
    ├── ops: 일상 운영 (daily-ops 리드)
    ├── build: 구현/배포 (code-reviewer 리드)
    ├── analyze: 분석/검증 (ai-synthesizer 리드)
    └── maintain: 문서/시스템 (compressor 리드)

리좀 연결자: linker ◆── live-context.md + .ctx/shared-context.md
크로스팀 유틸리티: commit-writer, orch-state, project-context
```

## 에이전트 체인 (SoT: CLAUDE.md)

- **구현**: implement → code-reviewer → commit-writer → linker → living docs
- **배포**: pf-ops(deploy) → security-auditor → 사용자 확인 → push
- **추출/검증**: Gemini 추출(벌크) + Codex 추출(정밀) → ai-synthesizer verify barrier(3단계) → 사용
- **디스패치**: /dispatch → linker(자동) → meta-orchestrator → 팀 활성화
- **압축**: compressor 9단계 → doc-ops(항상) → doc-ops verify
- **세션 전환**: verify → /sync all → /compact → linker → "새 세션 준비 완료"

## 에이전트 표준 구조

모든 agent.md 필수 섹션:
1. **검증**: 자기 작업 완료 전 확인 (번호 목록)
2. **암묵지**: 프로젝트별 핵심 규칙 (브랜치, 경로, 스택)
3. **학습된 패턴**: 세션 간 축적 (최대 5줄, compressor 자동 업데이트)

## Hooks

| Hook | 트리거 | 역할 |
|------|--------|------|
| SessionStart | 세션 시작 | 미커밋 + ❌결정(5건) + live-context(5줄) + .ctx/ 공유 상태 + 스냅샷 |
| PostToolUse | Write/Edit | live-context.md auto-append + auto-trim (100줄 캡) |
| PreToolUse | Bash | 위험 명령 차단 (rm -rf, force push) |
| PreCompact | compact 전 | 스냅샷 생성 + 미커밋 경고 |
| SessionEnd | 세션 종료 | 미커밋 현황 + MEMORY.md 줄 수 경고 |
| Notification | 알림 | 시스템 알림 |
| TaskCompleted | 태스크 완료 | 알림 + .ctx/shared-context.md 자동 갱신 |
| TeammateIdle | 팀원 유휴 | 유휴 알림 |

## Cross-CLI 공유 메모리 (v4.0)

- **.ctx/shared-context.md**: 모든 CLI(Claude/Gemini/Codex)가 읽고 쓰는 공유 상태
- **.ctx/provenance.log**: 출처 마커 ([claude], [gemini], [codex])로 기록 추적
- **SessionStart hook**: 세션 시작 시 .ctx/shared-context.md 자동 표시
- **TaskCompleted hook**: 태스크 완료 시 자동 갱신
- **/handoff 스킬**: CLI 간 작업 위임 → shared-context.md 갱신 + 실행 안내

## 멀티 AI 오케스트레이션 (v4.0)

- **Claude Code (Opus 4.6)**: 유일한 설계/결정권자 + 코드 작성 + 최종 판단 (verify barrier)
- **Codex CLI (GPT-5.3, Plus $20)**: 정밀 검증기. diff 리뷰 + 포맷 QA + git 추출. 5시간 롤링, 세션당 3~5회.
- **Gemini CLI (3.1 Pro, AI Pro $20)**: 벌크 추출기. 컨텍스트 오프로딩 + 웹 검색. 1M 컨텍스트.
- **Perplexity Pro**: 리서치 + tech-review 소스 (sonar-deep-research)

## 권한

- 허용: Read, Edit, Bash (git/npm/npx)
- 거부: .env*, .ssh/**, secrets/**, rm -rf, force push, curl/wget

## 프롬프트 캐싱 (2026-03-08)

- 순서: Static system prompt + Tools → CLAUDE.md → Session context → Messages
- 금지: 시스템 프롬프트에 타임스탬프, mid-session 도구 추가/제거, 모델 변경
- `<system-reminder>`로 업데이트 (시스템 프롬프트 변경 대신)
- defer_loading: auto 모드 활성 (ENABLE_TOOL_SEARCH=auto), 58도구 → 3-5K 토큰
- Compaction: 동일 system prompt + tools로 parent 캐시 재사용

## 설계 패턴

- **마찰 제거 원칙**: 모든 접근을 단축키/스킬/hook으로 만들어 생각↔행동 간격을 최소화한다 (← Memory-Merger #4120, 2026-03-09)

## 참고

- [PLANNING.md](./PLANNING.md): 아키텍처 결정
- [STATE.md](./STATE.md): 현재 상태 + 시스템 인벤토리
- [CLAUDE.md](../../CLAUDE.md): 전역 규칙 + 체인
