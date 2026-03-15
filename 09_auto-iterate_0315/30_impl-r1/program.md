# Auto-Iterate Program — Pipeline Hook 최적화
> 최적화 대상: M4 (규칙 위반율 — 오탐률 최소화)
> 수정 대상: ~/.claude/hooks/validate_pipeline.py
> 최대 iterations: 5

## 목표
validate_pipeline.py의 오탐(false positive)을 줄인다.
현재 baseline: F1=0.889, Precision=0.8, Recall=1.0 (27 scenarios, 3 FP)

## 알려진 오탐 3건
1. **EC1**: ideation-r1에서 01_dialogue.md 쓸 때 N17이 block (01_dialogue.md는 bootstrap 파일)
2. **EC2**: ideation-r1에서 02_context.md 쓸 때 I1이 block (02_context.md는 bootstrap 파일)
3. **EC3**: impl-r1에서 02_context.md 쓸 때 P1(foundation)이 block (context 작성은 foundation 전에 가능해야 함)

## 수정 허용 범위
- validate_pipeline.py 내 검증 로직 수정
- 규칙 간 exempt 목록 확장 허용
- 조건 순서 변경 허용
- 함수 추가/삭제 허용

## 제약 조건
- phase-rules.json의 규칙 의미를 변경하지 않는다
- 정탐(true positive)을 놓치면 안 된다 (recall ≥ 1.0)
- 다른 hook 파일 수정 금지
- validate_pipeline.py 외 파일 수정 금지

## 측정 방법
```
PYTHONIOENCODING=utf-8 python test_pipeline_rules.py --json 2>/dev/null
```

## 판정 기준
- precision 개선 + recall ≥ baseline(1.0) → keep
- precision 동일/악화 또는 recall 감소 → discard

## 실험 로그
| iter | 변경 내용 | Precision | Recall | F1 | action |
|---|---|---|---|---|---|
| 0 | baseline (27 scenarios) | 0.8 | 1.0 | 0.889 | — |
| 1 | N17에 01_dialogue.md exempt, I1에 02_context.md exempt 추가 | 0.923 | 1.0 | 0.960 | keep |
| 2 | P1/F1에 02_context.md/00_index.md bootstrap exempt 추가 | 1.0 | 1.0 | 1.0 | keep |
| 3 | +5 edge cases (32 scenarios) — EC8 발견: review R2도 bootstrap 필요 | 0.933 | 1.0 | 0.966 | keep (test expansion) |
| 4 | R2에 02_context.md/00_index.md bootstrap exempt 추가 | 1.0 | 1.0 | 1.0 | keep |
| 5 | +5 stress tests (37 scenarios) — 새 오탐 0 | 1.0 | 1.0 | 1.0 | keep |
