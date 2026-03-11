# 세션 요약

> 최종 수정: 2026-03-11 (20:45)

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: index-system v1 완성 — 설계→구현→리뷰→패치→sandbox 테스트 + wezterm config

완료:
  - [index-system] v1 초기 구현 — 에코시스템 그래프 + CLI (12a9d07)
  - [index-system] Code Review R1 → Critical 버그 4개 패치 (7d4b2e4)
  - [index-system] Code Review R2 → 검증 완료 (babece6)
  - [index-system] v1.1 Major 4개 패치 M1~M4+M5 (e3b16d4)
  - [index-system] sandbox 실전 테스트 + views self-loop 수정 (dbcfd0c)
  - [index-system] config 원복 — SCAN_ROOTS dev/ + ~/.claude (92b69ea)
  - [index-system] pending.md — v2 방향 + sandbox 테스트 기록 (8d2bd25)
  - [dev] CLAUDE.md — 10_index-system 추가, Index System 섹션 (ef8293e)
  - [dev] wezterm config 백업 — 03_wezterm 폴더 생성 (55bbee5)
  - [dev] HOME.md — mcp-memory v3.0.0-rc 반영 (94b8e66)

확정된 결정:
  1. index-system은 Python CLI — `python -m src.cli scan/refs/deps/impact/topology`
  2. views/INDEX.md = 전체 에코시스템 정적 지도 (세션 시작 시 참조용)
  3. SCAN_ROOTS = [dev/, ~/.claude] (sandbox 테스트 후 원복)
  4. v2 방향: SQLite 캐시 (노드 900+ 시), Provider 패턴 분리, asyncio

현재 상태:
  index-system master 92b69ea (push 필요). dev/ main 55bbee5. wezterm.lua + HOME.md 미커밋 변경 있음.

실패 기록 (삭제 금지):
  - [시도] TYPE_BOOST additive 0.03 → [실패] enrichment 격차 대비 무효 → [원인] additive boost가 RRF 스코어 차이를 뒤집기엔 너무 작음 → Typed Vector Channel (RRF 채널)로 교체
  - [시도] Playwright로 Twitter 스크래핑 → [실패] 구현 복잡도+비용 과다 → [원인] 로그인 세션 관리/2FA/rate limit 불안정
  - [시도] Gemini AI Studio로 YouTube 요약 자동화 → [실패] API 무료 한도+복잡도 → [원인] 자막만으로도 충분
  - [시도] 0307 포스트 자동 생성 → [실패] HARD FAIL로 자동 폐기 → [원인] sonar-deep-research가 "Today in One Line" 형식 이탈, isRejected 감지 → 알림 없이 사일런트 폐기

다음 할 것:
  1. index-system v2 — SQLite 캐시 + Provider 패턴 (노드 900+ 시)
  2. phase-guide.md 원자 단위 구체화
  3. mcp-memory ingest 노드 정리 (SQLite 스크립트)
  4. /pipeline 스킬에 phase-guide 내용 반영
  5. mcp-memory Ontology v3 Phase 2.5~6 (re-embed → co-retrieval → dispatch → NDCG 0.9)

열린 결정:
  - mcp-memory #4444~4449 잘못 저장된 노드 정리 방법 (ingest-cleanup-0311.md 참조)
  - index-system v2 착수 시점 (현재 노드 25개, 900+ 기준)

주의사항:
  - dev/ 미커밋: wezterm.lua, HOME.md
  - index-system: master 브랜치 (orchestration: main, portfolio: master)
  - mcp-memory checkpoint 전 다른 pane 작업 여부 확인 (DB 충돌 방지)

[재작성] 세션 목표: index-system v1 완성 + wezterm config | 남은 할 것: 1. index-system v2 (SQLite) 2. phase-guide 구체화 3. mcp-memory ingest 정리 4. /pipeline 반영 5. Ontology v3 Phase 2.5~6
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
