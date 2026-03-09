# Work Log 2026-03-09 Session 3

## 완료한 작업

### 1. CLI 플래그 실측
- Codex `--full-auto` = `-a on-request -s workspace-write` (샌드박스 내 자동)
- `--dangerously-bypass-approvals-and-sandbox` = 승인+샌드박스 없음 → 사용 금지
- Gemini .py 읽기 정상 확인. `.geminiignore` 불필요
- 스킬+전략 문서 업데이트, 커밋 `c129620`

### 2. NDCG 세그먼트 분석
- 실측: q001-q025=0.604, q026-q050=0.546, q051-q075=0.227
- 병목 = q051-q075 (q001-q025가 아님), TODO 수정
- 커밋 `c129620`

### 3. NDCG 개선 Ideation R1+R2
- R1: 원인 3개(FTS trigram, vocab mismatch, RRF 후보풀) + top_k 확장 역효과
- R2: ZERO 9건 분류 — goldset 오류 3건, vocab mismatch 3건, 검색 실패 2건
- 커밋 `79fa78c`, `3bac859`

### 4. 구현: goldset 수정 + typed vector 동적 가중치
- goldset 5건 수정 (q057/q060 쿼리 정규화, q065/q069/q074 relevant_ids)
- TYPE_CHANNEL_WEIGHTS: Pattern/Decision=1.0, Signal=0.8
- NDCG@5: 0.459 → 0.475 (+3.5%), 169 tests PASS
- 커밋 `f81d55f` (mcp-memory), `b3b1b53` (orchestration STATE)

### 5. enrichment bias 분석
- 발견: unenriched 노드(qs=0, 193개)가 RRF 1위여도 enriched tier=0에 밀림
- #4235: RRF rank 1 (0.1053) vs #222: enrichment+tier 0.432 → 4배
- cap 실험: q051+0.163 but q001-0.156 → 트레이드오프 미적용
- 커밋 `bc2bdee` (분석 문서화)

## 미결
- 193개 unenriched 노드 enrichment 배치 (OpenAI API 필요)
- q059/q073 ZERO 유지
- Phase 5 A8 Discovery 패턴 (다음 세션)

## 커밋 이력
| 레포 | 해시 | 메시지 |
|------|------|--------|
| orchestration | `c129620` | CLI 실측 + NDCG 세그먼트 |
| orchestration | `79fa78c` | NDCG ideation R1 |
| orchestration | `3bac859` | NDCG ideation R2 |
| orchestration | `b3b1b53` | STATE.md NDCG 반영 |
| orchestration | `d3c7c58` | ideation R2 enrichment bias 기록 |
| mcp-memory | `f81d55f` | goldset 수정 + 동적 가중치 |
| mcp-memory | `bc2bdee` | enrichment bias 분석 |

## mcp-memory 저장
- `20260309_s3` (5 decisions, 4 unresolved)
- checkpoint: #4371~#4375
