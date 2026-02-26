# v3.3.1 — 200K Context 최적화 (2026-02-26)

## 배경

1M context 사용 시 extra usage 과금 발생. Extra usage OFF 후 200K Default만 사용 가능.
기존 baseline 46K(23%), 작업 가용 ~54K(100K 기준), 체인 1개 완주에 40-60K → 200K 내에서 빠듯.

## 핵심 변경

### 1. Baseline 축소 (~3.7K tokens 절감)

| 대상 | 변경 | 절감 |
|------|------|------|
| MEMORY.md | Common Patterns 제거, Codex/Gemini 1줄 축약, 교훈 8→3 | ~700 |
| session-start.sh | ❌만 5건, live-context 5줄, 오늘 로그 삭제 | ~1,000 |
| CLAUDE.md | 프로젝트 구조→MEMORY.md 참조, CLI 위임, Living Docs 축약 | ~400 |
| decisions.md | 중복 4건 제거, ✅→아카이브 분리 | ~500 |
| workflow.md | 모델 사용 기준 중복 제거 | ~100 |

### 2. 플러그인 비활성화 (~6.5K tokens 절감)

| 플러그인 | 절감 |
|----------|------|
| Playwright MCP | ~4,700 |
| document-skills | ~1,800 |

### 3. .chain-temp 패턴 (체인당 20-30K 절감)

체인 에이전트 결과를 파일로 오프로딩, 메인 context에 1줄 요약만 반환.

```
orchestration/context/.chain-temp/
├── review-{date}.md     ← code-reviewer 상세 결과
├── gemini-{date}.txt    ← gemini-analyzer 추출 결과
├── codex-{date}.txt     ← codex-reviewer 검증 결과
├── synthesis-{date}.md  ← ai-synthesizer 교차 검증
├── docs-{date}.md       ← orch-doc-writer Living Docs
└── snapshot-{date}.md   ← compact 전 맥락 스냅샷
```

다음 체인 에이전트는 `.chain-temp/` 파일을 직접 Read.

### 4. Compact 전략

| 임계값 | 동작 |
|--------|------|
| 100K | compact 권장 (수동) |
| 120K | compact 필수 |
| 150K | auto-compact (최후 방어선) |

- compact 전: PreCompact hook → 스냅샷 자동 생성
- compact 후: PostCompact hook → 스냅샷 Read 안내
- 언제 compact해도 맥락 보존되는 구조

### 5. 200K 세션 예산 모델

```
200K 세션 예산 (최적화 후)
├── Baseline:        ~42K (고정, 매 세션 자동 주입)
├── 작업 Phase:     42K → 100K (~20-30 턴)
├── Compact 후:     ~50K → 100K까지 추가 작업
├── 체인 예약:      ~25K (.chain-temp 사용)
└── Auto-compact:   150K (최후 방어선)
```

## 수치 비교

| 항목 | Before (v3.3) | After (v3.3.1) |
|------|---------------|----------------|
| Baseline | ~46K | ~36K (플러그인 포함) |
| 작업 가용 (compact까지) | ~54K | ~64K |
| 체인 비용 (메인 context) | 40-60K | ~25K |
| Compact 후 baseline | 54-70K | 48-56K |
| 세션당 체인 | 1 (빠듯) | 1-2 (여유) |

## 수정 파일 (15개)

### 신규 (3개)
- `context/.chain-temp/.gitkeep`
- `hooks/pre-compact.sh`
- `settings.json` PostCompact hook

### 수정 (12개)
- `MEMORY.md`, `workflow.md`, `CLAUDE.md`, `decisions.md`
- `session-start.sh`, `KNOWLEDGE.md`
- `code-reviewer.md`, `gemini-analyzer.md`, `codex-reviewer.md`, `ai-synthesizer.md`
- `dispatch/SKILL.md`, `compressor.md`

## 커밋

| Hash | 메시지 |
|------|--------|
| 5b56867 | [dev] v3.3.1 200K Context 최적화: CLAUDE.md 경량화 |
| 8b25887 | [orchestration] v3.3.1 KNOWLEDGE.md + decisions.md + .chain-temp |
| 105fccf | [orchestration] v3.3.1 Living Docs 갱신: STATE.md + CHANGELOG.md |
| 8167f62 | [dev] HOME.md v3.3.1 반영 |
| f670c3c | [dev] Obsidian 북마크 추가: v3.3 e2e-test-report |
| 6cda0da | [orchestration] v3.3.1 compressor 9단계 완료 |

## 설계 원칙

1. **100K에서 compact** — 이전 맥락은 스냅샷으로 보존
2. **서브에이전트 적극 활용** — 메인 context는 의사결정용
3. **.chain-temp = 체인의 공유 메모리** — 메인 context 대신 파일 전달
4. **스냅샷 = compact 안전망** — 언제 compact해도 맥락 복구 가능
5. **구현 완료 ≠ DONE** — Living Docs → 옵시디언 → 커밋 → push 까지가 완료

## 교훈

- 구현 후 Living Docs/push 누락 2회 지적 → common-mistakes.md에 마무리 체크리스트 추가
- orch-doc-writer/compressor가 HOME.md(옵시디언 허브)를 안 건드림 → 다음 세션에서 재설정 필요
- 기록은 maintain 팀(compressor 리드)의 역할 — 메인 context에서 수동 갱신하는 게 아님

## 다음 세션 TODO

1. 옵시디언 폴더 구조 정리
2. orch-doc-writer / compressor 기록 대상 재설정 (HOME.md 포함)
3. baseline 토큰 실측 (새 세션에서 42K 이하 확인)
4. compact 스냅샷 e2e 테스트
