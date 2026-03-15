# Cross Validation

## autoresearch 원본 대비
| 원본 | 우리 적응 | 검증 |
|---|---|---|
| NEVER STOP | 이벤트 기반 + 세션 | ✅ 비용 현실적 |
| train.py 1개 | 450 원자 항목 | ✅ measure.py로 커버 |
| val_bpb | F1 + 교차참조 + 존재체크 | ✅ 10개 체크 구현 |
| results.tsv | program.md + HEALTH.md | ✅ |
| 밤새 100회 | 세션에서 5회 | ✅ PoC 검증 |

## 위험 검증
- 무인 수정 배제 → 맥락 오해 위험 제거 ✅
- 인터페이스 불변 원칙 → 사용자 혼란 없음 ✅
- git revert 안전장치 → PoC에서 실제 작동 확인 ✅
