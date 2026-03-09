# 세션 요약

> 최종 수정: 2026-03-09

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: portfolio Writing > Tech Review 전면 재설계 — Problem-3Sources-실시간피드-수치-Design Decisions 구조

완료:
  - [portfolio] Writing > Tech Review 전면 재설계
    - 구조: Problem → 3소스(Perplexity/Twitter/YouTube) → 실시간 피드 → 수치 → Design Decisions/Ongoing
    - TR_SYSTEM_KO.md 재작성
    - TechReviewSystemSection.tsx 전면 재작성
    - index.tsx 순서 재배치
  - [portfolio] StatsBar: 매일/Jekyll/자동/API → 100+Posts/3Sources/KO-EN/~$3
  - [portfolio] TechReviewMultiSource @author 폰트 fontFamily: inherit
  - [portfolio] 커밋 5540902 (master push)
  - [tech-review] 커밋 147de65 (master push)
  - [mcp-memory] checkpoint: node #4331~#4335 저장

현재 상태:
  portfolio Writing > Tech Review 섹션이 Problem→3Sources→실시간피드→수치→Design Decisions/Ongoing 구조로 전면 재설계 완료. StatsBar 라벨도 100+Posts/3Sources/KO-EN/~$3로 변경. 양쪽 레포 master push 완료.

실패 기록 (삭제 금지):
  - [시도] TYPE_BOOST additive 0.03 → [실패] enrichment 격차 대비 무효 → [원인] additive boost가 RRF 스코어 차이를 뒤집기엔 너무 작음 → Typed Vector Channel (RRF 채널)로 교체
  - [시도] Playwright로 Twitter 스크래핑 → [실패] 구현 복잡도+비용 과다 → [원인] 로그인 세션 관리/2FA/rate limit 불안정
  - [시도] Gemini AI Studio로 YouTube 요약 자동화 → [실패] API 무료 한도+복잡도 → [원인] 자막만으로도 충분

다음 할 것:
  1. bookmarks.json 첫 실행 (inbox/에 Twitter export JSON)
  2. sources.json 자동 갱신 자동화
  3. YouTube 플레이리스트 확대
  4. portfolio PR 5173에서 새 Writing 섹션 시각 확인

열린 결정:
  - bookmarks.json 첫 실행 시점
  - YouTube 플레이리스트 추가 대상 선정
  - sources.json 갱신 자동화 방식 (Task Scheduler vs GitHub Actions)

주의사항:
  - portfolio 레포: paulseongminpark/portfolio_20260215, 브랜치: master
  - tech-review 레포: paulseongminpark/tech-review, 브랜치: master
  - TechReviewSystemSection.tsx: 전면 재작성됨 — 이전 코드와 완전히 다름
  - StatsBar 라벨 변경: 매일/Jekyll/자동/API → 100+Posts/3Sources/KO-EN/~$3

[재작성] 세션 목표: portfolio Writing > Tech Review 전면 재설계 | 남은 할 것: 1. bookmarks.json 첫 실행 2. sources.json 자동 갱신 3. YouTube 플레이리스트 확대 4. PR 5173 시각 확인
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

---

=== 이전 세션 (2026-03-08 s3) ===

세션 목표: mcp-memory v2.2.1 — TYPE_BOOST additive→Typed Vector Channel 리팩터 + Goldset v2.2 Paul 수동 검증 (q026-q075)

완료:
  - [mcp-memory] v2.2.1 구현+커밋+push (e82a82a)
  - [mcp-memory] Goldset v2.2: q026-q075 Paul 수동 검증 완료 (50개 쿼리)
  - [mcp-memory] 전체: NDCG@5=0.460, NDCG@10=0.488, hit_rate=0.627, 163 tests PASS

실패 기록 (삭제 금지):
  - [시도] TYPE_BOOST additive 0.03 → [실패] enrichment 격차 대비 무효 → [원인] additive boost가 RRF 스코어 차이를 뒤집기엔 너무 작음

=== 이전 세션 (2026-03-08 s2) ===

세션 목표: tech-review YouTube 품질 강화 + Portfolio 멀티소스 전환

완료:
  - [tech-review] analyze-youtube.py 품질 강화 (validate_quotes, 100K transcript, 12섹션)
  - [portfolio] TechReviewMultiSource 전환, sources.json

실패 기록 (삭제 금지):
  - (이전 실패 아카이브 참조)

=== 실패 기록 아카이브 (삭제 금지) ===
  - [시도] QMD BM25 한글 검색 → [실패] 한글 토크나이징 안됨 → [원인] BM25 기본 토크나이저가 한글 미지원
  - [시도] QMD query + LLM reranker → [실패] context 오류 → [원인] reranker가 LLM context 미포함 상태에서 호출
  - [시도] QMD search → [실패] 영어 쿼리만 부분 동작 → [원인] get만 정상, search/query는 한글 환경에서 불안정
  - [시도] Playwright로 Twitter 스크래핑 → [실패] 구현 복잡도+비용 과다 → [원인] 로그인 세션 관리/2FA/rate limit 불안정
  - [시도] Gemini AI Studio로 YouTube 요약 자동화 → [실패] API 무료 한도+복잡도 → [원인] 자막만으로도 충분
