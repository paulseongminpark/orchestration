# 세션 요약

> 최종 수정: 2026-03-09

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: 08_documentation-system에 라이프사이클 방법론 추가

완료:
  - [documentation-system] 01_lifecycle-methodology_0311 파이프라인 생성 + R1→R2→R3→merged 완료
  - [documentation-system] foundation/phase-guide.md 신규 생성
    - 라운드 방향성 (Diverge/Cross/Converge, 유동적)
    - Phase별 내용 방법론 (Research/Ideation/Impl/Review)
    - Phase 간 연결 (merged → context.md)
    - foundation/ 3축 생성 시점 정의
  - [documentation-system] 커밋 e366600 (push 완료)
  - [orchestration] 세션 체인 v4.1 재설계 구현 + Living Docs 갱신 (eaff304)
  - [mcp-memory] checkpoint #4450~#4457 (결정 3개 + Paul 패턴 5개)

확정된 결정:
  1. phase-guide.md 신규 추가 (principles.md 수정 없음)
  2. 라운드 유동적 — 방향성이지 고정 순서 아님
  3. foundation/ 3축 — Ideation 완료 시점, 구현 전, 3개 한꺼번에
  4. 50대역 없음. 40-49 안에서 번호 구분
  5. 같은 lifecycle = 같은 파이프라인 폴더 번호 이어감
  6. Phase 간: merged/confirmed-decisions → 다음 Phase 02_context.md
  7. Opus는 merged만 읽는다
  8. Cascade = 범용 도구

현재 상태:
  documentation-system e366600 push 완료. orchestration main eaff304 push 완료. mcp-memory checkpoint 저장.

실패 기록 (삭제 금지):
  - [시도] TYPE_BOOST additive 0.03 → [실패] enrichment 격차 대비 무효 → [원인] additive boost가 RRF 스코어 차이를 뒤집기엔 너무 작음 → Typed Vector Channel (RRF 채널)로 교체
  - [시도] Playwright로 Twitter 스크래핑 → [실패] 구현 복잡도+비용 과다 → [원인] 로그인 세션 관리/2FA/rate limit 불안정
  - [시도] Gemini AI Studio로 YouTube 요약 자동화 → [실패] API 무료 한도+복잡도 → [원인] 자막만으로도 충분
  - [시도] 0307 포스트 자동 생성 → [실패] HARD FAIL로 자동 폐기 → [원인] sonar-deep-research가 "Today in One Line" 형식 이탈, isRejected 감지 → 알림 없이 사일런트 폐기

다음 할 것:
  1. phase-guide.md 원자 단위 구체화
  2. mcp-memory ingest 노드 정리 (SQLite 스크립트)
  3. /pipeline 스킬에 phase-guide 내용 반영
  4. mcp-memory Ontology v3 Phase 2.5~6 (re-embed → co-retrieval → dispatch → NDCG 0.9)

열린 결정:
  - mcp-memory #4444~4449 잘못 저장된 노드 정리 방법 (ingest-cleanup-0311.md 참조)

주의사항:
  - documentation-system은 orchestration과 별도 git repo
  - mcp-memory checkpoint 전 다른 pane 작업 여부 확인 (DB 충돌 방지)
  - orchestration: main 브랜치, portfolio: master 브랜치

[재작성] 세션 목표: documentation-system 라이프사이클 방법론 추가 | 남은 할 것: 1. phase-guide 원자 단위 구체화 2. mcp-memory ingest 정리 3. /pipeline 스킬 반영 4. Ontology v3 Phase 2.5~6
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

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
