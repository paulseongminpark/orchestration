# 세션 요약

> 최종 수정: 2026-03-11 (22:40)

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: compact 후 정보 손실 문제 해결 + 08_documentation-system 미준수 근본 원인 분석

완료:
  - [mcp-memory] save_session() active_pipeline 파라미터 추가 → get_context() 반환 (42d8a58)
  - [orchestration] workflow.md compact 후 복구 프롬프트 + /restore 연동 (7820709)
  - [orchestration] Phase 6 문서화 — active_pipeline + /restore 구현/리뷰 기록 (4f0f3de)
  - [orchestration] lessons.md — index-system R1 Critical 버그 교훈 추가 (7714466)
  - [orchestration] 08 시스템 미준수 근본 원인 분석 — 옆 Opus와 협업
  - [orchestration] 21_ideation-r2/ 시스템 브리핑 문서 (외부 AI용 전체 컨텍스트)
  - [orchestration] 01_dialogue.md Exchange 12~14 추가 (compact 손실, 문서화 누락, 근본 원인)

확정된 결정:
  1. 복구 2레이어: 장기 기억(mcp-memory DB) + 단기 작업 상태(파이프라인 00_index.md)
  2. save_session() active_pipeline → get_context()가 반환 → /restore에서 index 읽기
  3. 08 시스템이 운영체제가 아니라 참조 자료로 기능 — 이것이 문서화 누락의 근본 원인
  4. 해법 방향: 행동 감지 Hook (Edit/Write 시 pipeline 체크) — 미확정

현재 상태:
  orchestration main up to date. mcp-memory main up to date.
  orchestration 미커밋: dialogue.md 변경 + ideation-r2 briefing 신규.
  dev/ 미커밋: 04_memory_export submodule dirty.

실패 기록 (삭제 금지):
  - [시도] TYPE_BOOST additive 0.03 → [실패] enrichment 격차 대비 무효 → [원인] additive boost가 RRF 스코어 차이를 뒤집기엔 너무 작음 → Typed Vector Channel (RRF 채널)로 교체
  - [시도] Playwright로 Twitter 스크래핑 → [실패] 구현 복잡도+비용 과다 → [원인] 로그인 세션 관리/2FA/rate limit 불안정
  - [시도] Gemini AI Studio로 YouTube 요약 자동화 → [실패] API 무료 한도+복잡도 → [원인] 자막만으로도 충분
  - [시도] 0307 포스트 자동 생성 → [실패] HARD FAIL로 자동 폐기 → [원인] sonar-deep-research가 "Today in One Line" 형식 이탈, isRejected 감지 → 알림 없이 사일런트 폐기

다음 할 것:
  1. 08 시스템 미준수 해법 구현 — 행동 감지 Hook (Ideation R2 진행)
  2. index-system v2 — SQLite 캐시 + Provider 패턴 (노드 900+ 시)
  3. phase-guide.md 원자 단위 구체화
  4. mcp-memory ingest 노드 정리 (SQLite 스크립트)
  5. mcp-memory Ontology v3 Phase 2.5~6 (re-embed → co-retrieval → dispatch → NDCG 0.9)

열린 결정:
  - 08 시스템 행동 감지 Hook: 경고 vs 차단, 경로 필터, Layer 2 이탈 방지 방법
  - mcp-memory #4444~4449 잘못 저장된 노드 정리 방법 (ingest-cleanup-0311.md 참조)
  - index-system v2 착수 시점 (현재 노드 25개, 900+ 기준)

주의사항:
  - index-system: master 브랜치 (orchestration: main, portfolio: master)
  - mcp-memory checkpoint 전 다른 pane 작업 여부 확인 (DB 충돌 방지)

[재작성] 세션 목표: compact 후 복구 + 08 시스템 미준수 분석 | 남은 할 것: 1. 08 행동 감지 Hook 구현 2. index-system v2 3. phase-guide 구체화 4. mcp-memory ingest 정리 5. Ontology v3 Phase 2.5~6
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

---

=== 이전 세션 (2026-03-11 documentation-system) ===

세션 목표: 08_documentation-system에 라이프사이클 방법론 추가

완료:
  - [documentation-system] 01_lifecycle-methodology_0311 파이프라인 생성 + R1→R2→R3→merged 완료
  - [documentation-system] foundation/phase-guide.md 신규 생성
  - [orchestration] 세션 체인 v4.1 재설계 구현 + Living Docs 갱신 (eaff304)
  - [mcp-memory] checkpoint #4450~#4457

---

=== 이전 세션 (2026-03-09 s8) ===

세션 목표: tech-review 세션 8 — Portfolio Twitter 카드 딥링크 전환 + 0307 누락 복구 + parse-content.js 인용 URL 제거

완료:
  - [portfolio] Twitter 카드 딥링크 전환 (84e3c94)
  - [tech-review] URL hash 모달 오픈 + 0307 복구 + 인용 URL 제거 (67660f2)

---

=== 이전 세션 (2026-03-09 s7) ===

세션 목표: portfolio Writing > Tech Review 전면 재설계 — Problem-3Sources-실시간피드-수치-Design Decisions 구조

완료:
  - [portfolio] Writing > Tech Review 전면 재설계
  - [portfolio] StatsBar: 100+Posts/3Sources/KO-EN/~$3
  - [portfolio] TechReviewMultiSource @author 폰트 fontFamily: inherit
  - [portfolio] 커밋 5540902, [tech-review] 커밋 147de65 (master push)

실패 기록 (삭제 금지):
  - (위 최신 세션 참조)

=== 이전 세션 (2026-03-08 s3) ===

세션 목표: mcp-memory v2.2.1 — TYPE_BOOST additive→Typed Vector Channel 리팩터 + Goldset v2.2 Paul 수동 검증 (q026-q075)

완료:
  - [mcp-memory] v2.2.1 구현+커밋+push (e82a82a)
  - [mcp-memory] Goldset v2.2: q026-q075 검증, NDCG@5=0.460, 163 tests PASS

실패 기록 (삭제 금지):
  - [시도] TYPE_BOOST additive 0.03 → [실패] enrichment 격차 대비 무효 → [원인] additive boost가 RRF 스코어 차이를 뒤집기엔 너무 작음

=== 실패 기록 아카이브 (삭제 금지) ===
  - [시도] QMD BM25 한글 검색 → [실패] 한글 토크나이징 안됨 → [원인] BM25 기본 토크나이저가 한글 미지원
  - [시도] QMD query + LLM reranker → [실패] context 오류 → [원인] reranker가 LLM context 미포함 상태에서 호출
  - [시도] QMD search → [실패] 영어 쿼리만 부분 동작 → [원인] get만 정상, search/query는 한글 환경에서 불안정
  - [시도] Playwright로 Twitter 스크래핑 → [실패] 구현 복잡도+비용 과다 → [원인] 로그인 세션 관리/2FA/rate limit 불안정
  - [시도] Gemini AI Studio로 YouTube 요약 자동화 → [실패] API 무료 한도+복잡도 → [원인] 자막만으로도 충분
