# Auto-Iterate Workflow

## 수동 루프 (Phase 1)
```
1. baseline 측정 → results/baseline.json
2. agent에게 program.md 기반 수정 지시
3. 재측정 → results/iter-N.json
4. 비교 → keep (commit) / discard (revert)
5. program.md 실험 로그에 결과 append
6. 반복 (MAX_ITER까지)
```

## 반자동 루프 (Phase 2)
스크립트가 1~5를 자동 실행. 사람은 program.md를 3회마다 리뷰.

## 판정 흐름
```
측정 실패 → discard
recall < baseline → discard
precision ≤ baseline → discard
precision > baseline AND recall ≥ baseline → keep
```
