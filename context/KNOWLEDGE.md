# KNOWLEDGE — Best Practices

프로젝트 규칙, 패턴, 모범 사례. 에이전트/스킬/팀 목록은 **STATE.md** 참조.

---

## Git 규칙

- **orchestration**: main, **portfolio**: master
- 커밋: `[project] 한줄 설명` + `Co-Authored-By:`
- 금지: `git push --force`, `git clean -f`, `git reset --hard`, `--no-verify`

## 파일 구조

```
context/
├── STATE.md         # 지금 상태 (SoT: 시스템 인벤토리)
├── PLANNING.md      # 아키텍처 결정 (ADR)
├── KNOWLEDGE.md     # 모범 사례 (이 파일)
├── decisions.md     # 결정 추적 (❌/✅)
├── live-context.md  # 세션 간 공유 (hook 자동, 100줄 캡)
├── METRICS.md       # 세션별 완료/결정 수
└── logs/            # 시간순 상세 (읽기 금지, append만)
```

## 토큰 관리

- 1세션=1목표, 150K+ → /compact
- 읽기 금지: node_modules/, .git/, dist/, build/, logs/
- 서브에이전트: Haiku(요약) / Sonnet(분석) / Opus(설계)

## 리좀형 팀 구조 (v3.2)

```
meta-orchestrator (디스패치 허브, /dispatch)
    ├── ops: 일상 운영 (morning-briefer 리드)
    ├── build: 구현/배포 (code-reviewer 리드)
    ├── analyze: 분석/검증 (ai-synthesizer 리드)
    └── maintain: 문서/시스템 (compressor 리드)

리좀 연결자: context-linker ◆── live-context.md ──◆ project-linker
크로스팀 유틸리티: commit-writer, orch-state, project-context, content-writer
```

## 에이전트 체인 (SoT: CLAUDE.md)

- **구현**: implement → code-reviewer → commit-writer → project-linker → living docs
- **배포**: pf-deployer → security-auditor → 사용자 확인 → push
- **추출/검증 (v3.3)**: Gemini 추출(벌크) + Codex 추출(정밀) → Claude verify barrier(3단계) → 사용
- **디스패치**: /dispatch → context-linker → meta-orchestrator → 팀 활성화
- **압축**: compressor 7단계 → orch-doc-writer(조건부) → doc-syncer
- **세션 전환 (v3.3)**: verify → sync-all → compressor → context-linker → "새 세션 준비 완료"

## 에이전트 표준 구조

모든 agent.md 필수 섹션:
1. **검증**: 자기 작업 완료 전 확인 (번호 목록)
2. **암묵지**: 프로젝트별 핵심 규칙 (브랜치, 경로, 스택)
3. **학습된 패턴**: 세션 간 축적 (최대 5줄, compressor 자동 업데이트)

## Hooks

| Hook | 트리거 | 역할 |
|------|--------|------|
| SessionStart | 세션 시작 | 오늘 LOG + 미커밋 + 미반영 결정 + live-context 최근 10줄 |
| PostToolUse | Write/Edit | live-context.md auto-append + auto-trim (100줄 캡) |
| PreToolUse | Bash | 위험 명령 차단 (rm -rf, force push) |
| SessionEnd | 세션 종료 | 미커밋 현황 + MEMORY.md 줄 수 경고 |

## 멀티 AI 오케스트레이션

- **Claude Code**: 유일한 쓰기
- **GPT Plus**: 사고 확장, Canvas
- **Gemini Pro**: 대량 검증 (1M 토큰)
- **Perplexity Pro**: 리서치 + 교차검증

## 권한

- 허용: Read, Edit, Bash (git/npm/npx)
- 거부: .env*, .ssh/**, secrets/**, rm -rf, force push, curl/wget

## 참고

- [PLANNING.md](./PLANNING.md): 아키텍처 결정
- [STATE.md](../STATE.md): 현재 상태 + 시스템 인벤토리
- [CLAUDE.md](../../CLAUDE.md): 전역 규칙 + 체인
