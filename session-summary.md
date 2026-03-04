# 세션 요약

> 최종 수정: 2026-03-04

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: mcp-memory v2.0 enrichment pipeline 3종 e2e 리뷰 → 19개 Fix 통합 수정 → 검증 PASS

완료:
  - [mcp-memory] 3종 e2e 리뷰 실행: Sonnet(78/100), Opus(B+), Codex gpt-5.3-codex xhigh(48/100)
  - [mcp-memory] 3종 통합 분석 → 19개 Fix 도출 (F-1~F-25, Tier 0~3)
  - [mcp-memory] 19개 Fix 즉시 수정 적용, 10개 파일 수정
  - [mcp-memory] 구문(ast.parse) + 기능(assert) + 통합 검증 전부 PASS
  - [mcp-memory] checkpoint 5건 저장 (#4082~#4086)
  - [mcp-memory] data/reports/e2e-fix-summary.md 문서화 (103줄)
  - [mcp-memory] data/reports/e2e-review-{sonnet,opus,codex}.md 3건

현재 상태:
  v2.0 enrichment pipeline Step 1-10 구현 + 19개 Fix 완료. 미커밋 ~15개 파일. 첫 실행 테스트 미실시.

실패 기록 (삭제 금지):
  - (이번 세션 실패 없음)

다음 할 것:
  1. 커밋 + push (미커밋 ~15개 파일)
  2. enrichment pipeline 첫 실행 테스트 (--dry-run)
  3. v2.1 defer 항목: 시간 감쇠 스크립트 (F-5)
  4. v2.1 defer 항목: init_db v2 (F-10), schema.yaml v2 (F-11)
  5. v2.1 defer 항목: relate/connect MCP 도구 (F-16)

열린 결정:
  - F-19: phase_limit 변수 — 사용 or 제거 결정 필요
  - F-22: 프롬프트 언어 통일 정책 (한국어/영어 혼재)
  - 시간 감쇠 daily decay 스크립트 설계 방향 미정

주의사항:
  - mcp-memory 경로: /c/dev/01_projects/06_mcp-memory/
  - _session_state.md: /c/dev/01_projects/06_mcp-memory/scripts/enrich/_session_state.md (Step 1-10 전체 기록)
  - e2e-fix-summary.md: /c/dev/01_projects/06_mcp-memory/data/reports/e2e-fix-summary.md (19개 Fix 상세)
  - 주요 수정 파일: graph_analyzer.py, node_enricher.py, hybrid.py, daily_enrich.py, migrate_v2.py, config.py, relation_extractor.py, remember.py, get_becoming.py, 프롬프트 YAML 2개
  - 복수 모델 교차 검증 패턴 확인 — 각 모델이 다른 시각으로 다른 문제 발견

[재작성] 세션 목표: mcp-memory v2.0 e2e 리뷰 19개 Fix 완료 | 남은 할 것: 1. 커밋+push 2. --dry-run 첫 실행 3. v2.1 defer (감쇠/init_db/schema/relate도구)
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

---

=== 이전 세션 (2026-03-04) ===

세션 목표: portfolio 전체 섹션 구조 재편 설계 — 6섹션 구조 확정

완료:
  - [portfolio] 6섹션 확정, audit 416줄, 4카드 타이틀 변경, checkpoint #4057~#4059
  - 커밋 392e724 → master push

실패 기록 (삭제 금지):
  - (없음)

=== 이전 세션 (2026-03-04) ===

세션 목표: HOW I AI 섹션 Evolution 파트 전면 재작성 (글 + UI)

완료:
  - [portfolio] 3주 타임라인 + 질문 중심 UI + 인터뷰 원본 저장
  - 커밋 e0b1c3c, f95e390 → master push

실패 기록 (삭제 금지):
  - (없음)

=== 실패 기록 아카이브 (삭제 금지) ===
  - [시도] QMD BM25 한글 검색 → [실패] 한글 토크나이징 안됨 → [원인] BM25 기본 토크나이저가 한글 미지원
  - [시도] QMD query + LLM reranker → [실패] context 오류 → [원인] reranker가 LLM context 미포함 상태에서 호출
  - [시도] QMD search → [실패] 영어 쿼리만 부분 동작 → [원인] get만 정상, search/query는 한글 환경에서 불안정
