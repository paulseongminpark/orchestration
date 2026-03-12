# Confirmed Decisions — Research Phase
> 2026-03-12

## 확정된 발견

### Critical (즉시 수정 필요)
- **G16**: validate_pipeline.py에 파이프라인 타입 체크 추가 필요
  - code-review / research-only 타입은 R1(impl-merged) 체크 면제
  - 해결: settings에서 파이프라인 타입 파싱 후 분기

### Warning (검토 필요)
- **G1-G7**: 10 시스템 구현 gap (edge 4종 미구현, --diff 없음, move_check 미완)
- **G8**: MEMORY.md 버전 v2.2.1 → v3.0.0-rc 업데이트 필요
- **G10**: 08/09/10 → mcp-memory 직접 코드 통합 없음 (설계 결정 미반영)
- **G15**: 훅 규칙 하드코딩 (phase-rules.json → 훅 자동 동기화 없음)
- **G17**: N17 규칙(Phase 전환 시 02_context.md) 훅 미구현

### Info (선택적)
- **G9**: Deleuze 철학 타입 미구현 (의도적 단순화)
- **G11**: NotebookEdit 훅 라우팅 확인 필요
- **G18**: 파이프라인 파일이 mcp-memory 자동 저장에서 제외됨

## 다음 단계
→ 90_output/ 감사 리포트 작성
→ G16 수정 계획 수립
→ 10 시스템 구현 완성 로드맵
