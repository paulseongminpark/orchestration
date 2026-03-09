# 세션 요약

> 최종 수정: 2026-03-09

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: tech-review 세션 8 — Portfolio Twitter 카드 딥링크 전환 + 0307 누락 복구 + parse-content.js 인용 URL 제거

완료:
  - [portfolio] Twitter 카드: overlay 모달 제거 → tech-review /lang/twitter/#bm-xxx 딥링크 전환
    - TechReviewMultiSource.tsx: TwitterModal 제거, TwitterCard → `<a>` 링크
    - TwitterItem: id 필드 추가
    - 커밋 84e3c94 (master push)
  - [tech-review] ko/en/twitter.html: URL hash(#bm-xxx) 자동 모달 오픈 로직 추가
    - sources.json: id 필드 추가 (build-sources-feed.js)
    - 커밋 faea484 (master push)
  - [tech-review] 0307 포스트 누락 발견 및 수동 재생성
    - 원인: sonar-deep-research "Today in One Line" 형식 이탈 → HARD FAIL → 자동 폐기
    - workflow_dispatch post_date=2026-03-07 수동 트리거 → 성공 (312f839)
  - [tech-review] parse-content.js 인용 URL 제거 로직 추가
    - regex: (?<!\])(https?://[^)\s]+\)) 제거 + [미확인] 주석 제거
    - 0306 ko/en, 0308 ko 포스트 소급 수정
    - 커밋 67660f2 (master push)
  - [mcp-memory] save_session + checkpoint #4415~#4418

현재 상태:
  tech-review blog master 67660f2, portfolio master 84e3c94 — 양쪽 push 완료. Twitter 카드가 portfolio에서 딥링크로 전환되어 tech-review 블로그에서 모달 열림. 인용 URL 제거 로직이 parse-content.js에 추가되어 향후 자동 방어.

실패 기록 (삭제 금지):
  - [시도] TYPE_BOOST additive 0.03 → [실패] enrichment 격차 대비 무효 → [원인] additive boost가 RRF 스코어 차이를 뒤집기엔 너무 작음 → Typed Vector Channel (RRF 채널)로 교체
  - [시도] Playwright로 Twitter 스크래핑 → [실패] 구현 복잡도+비용 과다 → [원인] 로그인 세션 관리/2FA/rate limit 불안정
  - [시도] Gemini AI Studio로 YouTube 요약 자동화 → [실패] API 무료 한도+복잡도 → [원인] 자막만으로도 충분
  - [시도] 0307 포스트 자동 생성 → [실패] HARD FAIL로 자동 폐기 → [원인] sonar-deep-research가 "Today in One Line" 형식 이탈, isRejected 감지 → 알림 없이 사일런트 폐기

다음 할 것:
  1. GitHub Actions HARD FAIL 재시도/알림 메커니즘 구현 (사일런트 누락 방지)
  2. sources.json 자동 갱신 자동화 (현재 수동)
  3. YouTube 플레이리스트 확대
  4. 2단계 파이프라인 설계: deep research 조사 → sonar-pro 구조화

열린 결정:
  - HARD FAIL 알림 방식: Slack/Email/GitHub Issue 중 선택
  - sources.json 갱신 자동화 방식: Task Scheduler vs GitHub Actions
  - YouTube 플레이리스트 추가 대상 선정

주의사항:
  - portfolio 레포: paulseongminpark/portfolio_20260215, 브랜치: master
  - tech-review 레포: paulseongminpark/tech-review, 브랜치: master
  - portfolio 미커밋 파일 다수 있음 (이전 세션 작업, 이번 세션 범위 밖)
  - parse-content.js 인용 URL 제거: negative lookbehind (?<!\]) — markdown 링크 내 URL은 보존
  - 0307 재생성은 수동 workflow_dispatch — 자동 재시도 미구현 상태

[재작성] 세션 목표: tech-review 세션 8 — Twitter 딥링크 + 0307 복구 + 인용 URL 제거 | 남은 할 것: 1. HARD FAIL 알림 메커니즘 2. sources.json 자동 갱신 3. YouTube 플레이리스트 확대 4. 2단계 파이프라인 설계
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

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
