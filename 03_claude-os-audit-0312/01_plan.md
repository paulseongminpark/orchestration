# Plan: Claude OS Audit
> 2026-03-12 | 파이프라인: 03_claude-os-audit-0312

## 작업 목표
Claude Code 운영체제 전체 시스템 검증:
1. 각 시스템(08/09/10)이 제대로 설계되었는가
2. 온톨로지가 시스템에 올바르게 연결되었는가
3. Claude Code OS 레이어(rules/skills/hooks)가 시스템과 정합성을 갖는가

## 손실불가 기준
- 각 시스템 설계 원칙 완전 이해
- 온톨로지 타입/관계 → 시스템 매핑 완성
- 이슈 목록: Critical / Warning / Info 분류

## 범위 + Phase 분할

### 10_research-r1: 인프라 시스템 (Cascade)
- `08_documentation-system/`: phase-rules.json, foundation/, STATE.md
- `09_context-cascade-system/`: foundation/, 핵심 설계
- `10_index-system/`: foundation/, views/INDEX.md, src/ CLI 진입점

### 11_research-r2: 온톨로지 + mcp-memory (Cascade)
- `06_mcp-memory/`: 온톨로지 설계 문서, entity/relation 타입 정의
- 온톨로지 ↔ 08/09/10 연결 매핑

### 12_research-r3: Claude OS 레이어 (Cascade)
- `~/.claude/`: CLAUDE.md, rules/ (3파일), skills/pipeline.md, hooks/
- 설정이 시스템 설계와 정합하는가

### 13_research-merged
- 3회전 통합 + 이슈 초안 + foundation/ 작성

### 40_review-r1: 독립 시스템 검증
- 각 시스템별 설계 원칙 vs 실제 구현 gap

### 41_review-r2: 연결 정합성 검증
- 온톨로지 ↔ 08/09/10 ↔ Claude OS 전체 연결

### 90_output
- 감사 리포트 + Critical 이슈 + 권장사항

## Cascade 전략
- 각 Research 라운드에서 /cascade 발동
- 추출만 (요약 금지), 판단은 Claude 직접
- 읽기 후 즉시 정형화된 매핑 파일 작성
