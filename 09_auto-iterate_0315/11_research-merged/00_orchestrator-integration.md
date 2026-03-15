# Research 통합 — autoresearch → auto-iterate 매핑
> 통합일: 2026-03-15

## 핵심 발견

### autoresearch 3원칙 → 우리 적용
1. **단일 수정 대상** — 1 iteration = 1 파일만 변경
2. **단일 메트릭** — iteration마다 하나의 메트릭으로 판정
3. **고정 예산** — 테스트 시나리오 1회 실행 (시간 아닌 횟수)

### 구조 매핑 확정
| autoresearch | auto-iterate |
|---|---|
| `prepare.py` (불변) | Claude Code + MCP + git (불변 인프라) |
| `train.py` (수정 대상) | agent/skill/hook/rules 설정 파일 |
| `program.md` (지시서) | program.md (최적화 방향 + 제약) |
| `val_bpb` | M1~M4 메트릭 (iteration마다 1개 선택) |
| 5분 wall-clock | 테스트 시나리오 1회 |
| keep/discard | git commit / git revert |

### 메트릭 4종 정의
- **M1** recall 정확도 (mcp-memory precision@k)
- **M2** 세션 복구 시간 (/restore wall-clock초)
- **M3** 경로 해결 성공률 (index-system %)
- **M4** 규칙 위반율 (hook exit code 정탐/오탐) ← 첫 실험 권장

### 구현 우선순위
M4 → M1 → M3 → M2 (측정 용이성 순)
