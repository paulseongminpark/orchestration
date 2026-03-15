# Ideation R1 — auto-iterate 적용 설계
> 2026-03-15

## 1. program.md 설계

### autoresearch 원본의 program.md 역할
- agent에게 "무엇을 최적화할 것인지" 지시
- 수정 허용 범위 명시
- 제약 조건 (깨뜨리면 안 되는 것)
- 사람이 반복 개선하여 "연구 방향"을 조율

### 우리 program.md 포맷

```markdown
# Auto-Iterate Program
> 최적화 대상: {메트릭 이름}
> 수정 대상: {파일 경로}
> 최대 iterations: {N}

## 목표
{메트릭}을 개선한다. 현재 baseline: {값}.

## 수정 허용 범위
- {파일}의 {어떤 부분}을 변경할 수 있다
- {구체적 제약: 예) 함수 시그니처 변경 금지}

## 제약 조건 (절대 위반 금지)
- 기존 테스트가 모두 통과해야 한다
- 다른 파일을 수정하지 않는다
- git commit 메시지에 iteration 번호와 메트릭 변화를 기록한다

## 측정 방법
{메트릭 측정 커맨드}

## 판정 기준
- 메트릭이 개선되면 keep (git commit)
- 메트릭이 동일하거나 악화되면 discard (git checkout -- {파일})
- 테스트 실패 시 무조건 discard
```

### M4 첫 실험용 program.md 예시

```markdown
# Auto-Iterate Program — Pipeline Hook 최적화
> 최적화 대상: M4 (규칙 위반율 — 오탐률 최소화)
> 수정 대상: ~/.claude/hooks/validate_pipeline.py
> 최대 iterations: 10

## 목표
validate_pipeline.py의 오탐(false positive)을 줄인다.
현재 baseline: 측정 필요.

## 수정 허용 범위
- validate_pipeline.py 내 검증 로직 수정
- 정규식 패턴, 경로 매칭, 예외 조건 변경 허용
- 함수 추가/삭제 허용

## 제약 조건
- phase-rules.json의 규칙 의미를 변경하지 않는다
- 정탐(true positive)을 놓치면 안 된다 (recall ≥ 현재)
- 다른 hook 파일 수정 금지

## 측정 방법
python test_pipeline_rules.py --report

## 판정 기준
- 오탐 감소 + 정탐 유지 → keep
- 오탐 동일/증가 또는 정탐 감소 → discard
```

---

## 2. 테스트 셋 설계 (M4 기준)

### 시나리오 분류

| 카테고리 | 예시 | 기대 |
|---|---|---|
| **정상 구조** | M1 충족 파이프라인 | pass (exit 0) |
| **의도적 위반** | 00_index.md 없는 폴더 | block (exit 2) |
| **경계 사례** | 비활성 파이프라인 수정 | pass |
| **오탐 유발** | 파이프라인 외 폴더에 index.md | pass |

### 테스트 셋 구조

```
tests/auto-iterate/
  fixtures/           # 테스트용 파이프라인 구조
    valid_pipeline/
    missing_index/
    wrong_naming/
    edge_case_1/
  test_pipeline_rules.py
  results/
```

### 측정 스크립트 핵심

```python
scenarios = load_fixtures()
for s in scenarios:
    exit_code = run_hook("validate_pipeline.py", s.staged_files)
    s.result = (exit_code == s.expected_exit)

precision = correct_blocks / total_blocks
recall = correct_passes / total_passes
f1 = 2 * precision * recall / (precision + recall)
```

---

## 3. Iteration 루프 설계

### Phase 1: 수동 루프

```bash
# 1. baseline 측정
python test_pipeline_rules.py --report > results/baseline.json
# 2. agent 수정 (Claude Code 세션에서)
# 3. 재측정
python test_pipeline_rules.py --report > results/iter-1.json
# 4. 비교 → keep (git commit) / discard (git checkout)
```

### Phase 2: 반자동 루프

```bash
#!/bin/bash
MAX_ITER=10
for i in $(seq 1 $MAX_ITER); do
  baseline=$(python test_pipeline_rules.py --json | jq '.f1')
  claude --print "program.md 읽고 validate_pipeline.py 개선. iteration $i"
  candidate=$(python test_pipeline_rules.py --json | jq '.f1')
  if (( $(echo "$candidate > $baseline" | bc -l) )); then
    git commit -am "auto-iterate iter-$i: F1 $baseline → $candidate"
  else
    git checkout -- ~/.claude/hooks/validate_pipeline.py
  fi
done
```

---

## 4. 안전장치

| 위험 | 대응 |
|---|---|
| 시스템 파손 | git revert + 사전 백업 |
| 범위 밖 수정 | program.md 제약 + git diff 체크 |
| 측정 실패 | 실패 = 자동 discard |
| 무한 루프 | MAX_ITER 하드 리밋 |
| 누적 악화 | N회마다 초기 baseline 재비교 |

---

## 5. 열린 결정

| # | 질문 | 제안 |
|---|---|---|
| 1 | 첫 실험 대상 | validate_pipeline.py |
| 2 | agent 모델 | Sonnet (빠름) |
| 3 | iteration 수 | 10회 수동 |
| 4 | 자동화 | Phase 1 수동 → Phase 2 반자동 |
| 5 | program.md 진화 | 3회마다 사람 리뷰 |
