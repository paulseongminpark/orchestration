# Plan — Session Chain + Ontology 통합 재설계

> **시작**: 2026-03-11
> **범위**: orchestration × mcp-memory 교차
> **참여**: Paul + Claude (Opus)

## 목표

1. 세션 종료 체인 단순화 (11단계 → 5단계)
2. auto_remember 온톨로지 타입 매핑 (L0 Observation 일색 → 다층 타입)
3. save_session()을 그래프 노드 생성기로 확장
4. 이중 메모리 시스템 통합 (MEMORY.md = mcp-memory DB 렌더링 뷰)
5. 폐기 대상 정리 (analyze-session.sh, auto-promote.sh, /sync all 등)

## 손실불가 기준

- 기존 163 unit tests 전부 통과
- sessions 테이블 데이터 보존 (마이그레이션은 추가, 삭제 아님)
- content_hash dedup으로 마이그레이션 중복 방어
- auto_remember ↔ /checkpoint 병렬 구조 유지 (대체 불가)

## 작업 흐름

```
[세션 1] Ideation R1 대담 (6 Exchanges)
    → R2 구체화 (3 Exchanges)
    → 최종 점검 (2 Exchanges, 08/09/10 교차)
    → Impl Design (6 Phase, 13 Task)
    → Impl Review R1 (8건) + R2 (4건)

[세션 2] compact 후 복구
    → Ultrathink 전체 점검
    → Phase 0~5 구현
    → E2E 테스트 16건
    → 마이그레이션 47세션
    → Phase 1.5 모니터링 1회차
    → 문서화
```

## Pane 구성

| Pane | 담당 | 모델 |
|------|------|------|
| 0 (Main) | 설계+구현+검증 전체 | Opus |

단일 Pane. 설계-구현-검증 전부 같은 세션에서 순차 진행.
