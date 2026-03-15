# Ideation 최종 — auto-iterate 설계

## 구조
```
program.md (지시서 + 실험 로그)
    ↕ 에이전트가 읽고 쓴다
target file (수정 대상)
    ↕ 에이전트가 수정한다
test suite (fixtures/ + 측정 스크립트)
    ↕ 자동 측정
results/ (JSON 로그)
git log (keep만)
```

## program.md 포맷
목표 / 수정 허용 범위 / 제약 조건 / 측정 방법 / 판정 기준 / 실험 로그 테이블

## 판정 기준
- recall ≥ baseline (정탐 유지 필수)
- precision > baseline (오탐 감소) → keep
- 절대값 없음 — "어제보다 나은가"가 유일한 기준

## 기록
- program.md 내 실험 로그 테이블 (에이전트가 직접 append)
- results/*.json (보조)
- git log (keep만 남음)

## 안전장치
git revert, diff 체크, 측정실패=discard, MAX_ITER=10, 누적 재비교
