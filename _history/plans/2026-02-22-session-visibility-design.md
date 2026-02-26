# Session Visibility System — 설계 문서

**날짜:** 2026-02-22
**작성:** Claude Sonnet 4.6 + 박성민
**상태:** 승인됨, 구현 대기

---

## 배경 & 문제

Warp에서 여러 Claude Code 세션을 동시 운영 중:
- 세션 A: orchestration 조율 + tech-review
- 세션 B: portfolio AI system 기록
- 세션 C: monet-lab UI 실험

**실제 발생한 문제:**
- 세션 A에서 AI system 구조 변경 → 세션 B가 모르고 stale 내용 기록
- 각 세션이 git 커밋/STATE.md 갱신 여부를 파악하기 어려움
- 세션 마무리 없이 종료 시 기록 누락

**핵심 니즈:** 지식 전파(Knowledge Propagation) — 한 세션의 중요 결정이 다른 세션에 자동으로 전달

---

## 설계

### 파일 구조

```
~/.claude/
└── decisions.md          ← 전역 결정 사항 (신규)
```

### decisions.md 형식

```markdown
## 미반영 결정 (자동 표시)

2026-02-22 [orch] compressor 확장: LOG+STATE 3곳 저장 | pf:❌ tr:✅ ml:✅
2026-02-22 [tech-review] Smart Brevity 도입, 수요일 AI×Industry | pf:❌ tr:✅
2026-02-22 [portfolio] AiWorkflowSection type import 제거 | pf:✅

## 아카이브

2026-02-21 [orch] sync-all dev-vault 경로 수정 | pf:✅ tr:✅
```

**태그 의미:**
- `pf` = portfolio에 반영 여부
- `tr` = tech-review에 반영 여부
- `ml` = monet-lab에 반영 여부
- `❌` = 미반영 (다음 세션 시작 시 표시)
- `✅` = 반영 완료 (아카이브로 이동)

---

### 자동화 흐름

#### SessionStart Hook 강화
```bash
# 기존: 오늘 LOG tail-30 출력
# 추가: decisions.md에서 미반영 항목 필터링 출력

DECISIONS="$HOME/.claude/decisions.md"
if [ -f "$DECISIONS" ]; then
  echo "=== 미반영 결정 사항 ==="
  grep "❌" "$DECISIONS" | tail -10
fi
```

#### SessionEnd Hook 강화
```bash
# 세션 종료 시 각 프로젝트 git 상태 출력
echo "=== 세션 종료 시 git 상태 ==="
for proj in orchestration portfolio tech-review; do
  STATUS=$(git -C "/c/dev/01_projects/0X_$proj" status -s 2>/dev/null | wc -l)
  [ "$STATUS" -gt 0 ] && echo "⚠️ $proj: $STATUS 미커밋" || echo "✅ $proj: clean"
done
```

#### compressor 에이전트 업데이트
저장 대상 4곳으로 확장:
1. `session-summary.md` (기존)
2. `context/logs/YYYY-MM-DD.md` append (기존)
3. 프로젝트 `STATE.md` 갱신 (기존)
4. `~/.claude/decisions.md` append **(신규)**

decisions.md 기록 형식:
```
YYYY-MM-DD [project] 핵심 결정 1줄 요약 | pf:❌ tr:❌ ml:❌
```
→ 반영이 필요 없는 프로젝트는 태그 생략

---

### 토큰 최적화

- 1줄 형식: 항목당 20~30 토큰
- `tail -10`: 최근 10개만 SessionStart에서 읽음 = 최대 300 토큰
- 자동 아카이브: 모든 태그 `✅` 되면 `## 아카이브` 섹션으로 이동
- 결과: 미반영 항목만 상단에 유지 → 파일이 항상 작음

---

## 구현 목록

| 항목 | 파일 | 작업 |
|------|------|------|
| decisions.md 초기화 | `~/.claude/decisions.md` | 신규 생성 |
| SessionStart Hook | `settings.json` | grep "❌" 추가 |
| SessionEnd Hook | `settings.json` | git status 루프 추가 |
| compressor 에이전트 | `~/.claude/agents/compressor.md` | decisions.md append 추가 |

---

## 기대 효과

**Before:**
- 세션 B: AI system 변경 사항 모른 채 stale 내용 기록
- git 상태 파악 불가
- 세션 마무리 누락 시 기록 없음

**After:**
- 세션 B 시작 시: "⚠️ [orch] AI system 변경 → portfolio 미반영" 자동 표시
- 모든 세션 종료 시: git 미커밋 현황 자동 출력
- compressor가 decisions.md에 기록 → 영구 추적

---

## 연관 시스템

- hookify 규칙 추가 (다른 세션에서 병행): 명세 건너뛰기 차단
- compressor: session-summary + LOG + STATE + decisions 4곳 저장 (이미 수정됨)
