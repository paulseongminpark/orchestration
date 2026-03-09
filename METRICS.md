# SOT Metrics — 성과 지표

> 최종 수정: 2026-03-03

> 목적: 에이전트 효과성 + 작업 품질 데이터 누적. "뭐가 실제로 도움이 됐나"를 측정.

---

## 에이전트 효과성 로그

| 날짜 | 에이전트 | 작업 | 품질(1-5) | 메모 |
|------|----------|------|-----------|------|
| 2026-02-22 | gemini-analyzer | 연동 테스트 | - | 설치 완료, 실분석 미실시 |
| 2026-02-22 | gemini-analyzer(Opus) | 오케스트레이션 시스템 전체 비판 분석 | 5 | 11개 개선 태스크 도출, 모두 완료 |
| 2026-02-22 | codex-reviewer | 설계 결함 검증 1차 (todo 삭제 설계) | 4 | 16개 결함 발견. 실전 유용. 2차 4개 신규/미해결 |
| 2026-02-22 | ml-porter (역할) | monet-lab page-12 portfolio 컴포넌트 이식 | 5 | AiWorkflowSection, TechReviewSystemSection, aiWorkflowData 완전 이식 |
| 2026-02-23 | (직접 점검) | 전체 시스템 점검 (hooks, plugins, agents, skills) | 5 | 유령 참조 제거, 플러그인 3개 비활성화, hooks 전면 강화 |
| 2026-02-23 | Agent Teams (파일럿) | plugin-analyst + learning-analyst 병렬 분석 | 5 | 2명 병렬 배포→분석→결과 수신→반영 전체 흐름 성공 |
| 2026-02-23 | codex-reviewer + gemini-analyzer | 병렬 교차 검증 파이프라인 테스트 | 4 | 34건 vs 3건 발견. 속도 15분→2분 최적화 완료 |
| 2026-02-23 | project-linker, meta-orchestrator, tr-monitor, inbox-processor | v3.1 신규 에이전트 실전 테스트 | 4 | 4개 모두 테스트 성공. ai-synthesizer 실전 대기 |
| 2026-02-23 | (직접 분석+구현) | tech-review 파이프라인 실패 원인 분석 + 프롬프트 7개 개편 | 5 | KO 거부 응답 감지+EN 마커 제거로 재생성 성공 (1,883자) |
| 2026-02-23 | (직접 구현) | monet-lab SurveyViz + SurveyTable 컴포넌트 신규 구현 | 4 | CSV 2개 병합 N=43, IntersectionObserver 애니메이션 |
| 2026-02-23 | (직접 구현) | monet-lab page-12 CSS 레이아웃 + 이미지 교체 + 블록 타입 확장 | 5 | 1100→1540px, 4개 블록 추가, 7개 이미지 교체 |
| 2026-02-23 | (직접 구현) | monet-lab 프로그레스 바 드래그 기능 + 커밋 2개 | 5 | animation-delay 음수 패턴, 히어로 슬라이더 UX 완성 |
| 2026-02-24 | (직접 구현) | monet-lab VisualCuesGallery + ActivityGallery + 페이지 에디터 | 4 | 9개 이미지 비대칭, 5항목 grid-area, 에디터 DEV only (구현 중단) |
| 2026-02-24 | (직접 문서화) | orchestration v3.1 Living Docs 전면 갱신 | 5 | README, ROADMAP, SYSTEM-GUIDE, USER-GUIDE, HOME.md |
| 2026-02-24 | (직접 구현) | orchestration v3.2 전체 구현 (Phase 0~5) | 5 | 리좀형 4팀+허브, SoT 확립, doc-syncer+/dispatch 신규, auto-trim, 2커밋 pushed |
| 2026-02-25 | (직접 설계) | orchestration v3.3 Codex/Gemini CLI 통합 설계 | 5 | 설계문서 ~950줄, 구현플랜 23태스크 6Phase, 커밋 e948b45 |
| 2026-02-25 | (직접 구현+테스트) | orchestration v3.3 전체 구현 (Phase 1~6, 23 tasks) + e2e PASS | 5 | Codex/Gemini CLI 설정 완성, 에이전트 3개 재작성, 스킬 3개 신규, 23/23 ALL PASS |
| 2026-02-25 | (직접 구현+문서화) | v3.3 에비던스 문서 2건 + HOME.md/REFERENCE.md 업데이트 + compressor 버그 수정 | 5 | diagram.md + members-skills.md, meta-orchestrator Opus 승격, 타임스탬프 규칙 확정 |
| 2026-02-25 | (직접 설계+실행) | v3.3 전체 e2e 테스트: 12시나리오 + 1차/2차 + 비교 분석 + 버그 3건 수정 | 5 | FAIL 0, WARN 3, Opus 추가 발견 +15건. meta-orchestrator/Codex/PreToolUse 실제 버그 발견 |
| 2026-02-26 | (직접 구현) | v3.3.1 200K Context 최적화: baseline 축소 + .chain-temp 오프로딩 + compact 전략 + hook | 5 | ~3.7K baseline 절감, ~6.5K 플러그인 절감, .chain-temp 패턴 신설, compact 3단계 임계값 확정 |
| 2026-02-27 | (직접 감사) | v3.3.1 전체 .md 일관성 감사: 80+ 파일 스캔, 15건 수정 | 5 | CRITICAL 1(hook 경로), HIGH 10(context/ URL+@agent), MEDIUM 3, LOW 1 |
| 2026-02-27 | (직접 검증+문서화) | v4.0 Living Docs 최신화 + e2e 8시나리오 | 5 | stale name 7건 수정, PostCompact 정리, 오탐 3건 확인 |
| 2026-03-02 | (직접 구현) | portfolio PMCC_DETAIL_KO.md 전면 개정 (13개 지시 + 표현 평이화) | 5 | flowchart 이동, Gallery 재배치, 어조 전환 완성. TS 타입 체크 PASS. commit 8e2ed5b |
| 2026-03-02 | (직접 구현) | portfolio Obsidian/E2E/index 섹션 전면 리라이트| 5 | 구조 10→5단계, Bedford 다이어그램, vanilla.js 마이그레이션, 타이포그래피 위계, sticky 헤더. commit 9e47cda, fb291ef |
| 2026-03-04 | (직접 구현) | portfolio E2EWorkflow 헤더/배경 분리 + Key Decisions sandbox 3종 | 5 | 헤더 흰색/파란배경 분리, v1(투톤)/v2(아코디언)/v3(내러티브) 제작. commit caca5a8 |
| 2026-03-03 | (직접 개선) | Auto Memory 파이프라인 개선 + .ctx 정리 + Playwright 활성화 | 5 | analyze-session.sh Python 기반 개선, auto-promote.sh 신규, .ctx/ 폐기, Playwright MCP 활성화 |
| 2026-03-04 | (직접 구현) | portfolio HOW I AI Evolution 전면 재작성 (3주 타임라인 + 질문 UI + 인터뷰 원본) | 5 | TimelineItem 타입 변경, 세로스택 UI, fetch .catch() 버그 수정. 커밋 e0b1c3c, f95e390 |
| 2026-03-03 | (직접 구현) | QMD 설치 + D3.js 시각화 3종 (session-graph, orch-timeline, orch-graph) | 5 | 버전11+개념36 노드, 서브에이전트11개, SAVED_POSITIONS, 멀티셀렉트 필터. 커밋 1f1fe9e |
| 2026-03-03 | (직접 구현) | portfolio How I Operate 전면 재작성 + mcp-memory 확인 | 5 | 추상5카드→4원칙카드, parseSystemContent 제거, mcp-memory v0.1.0 확인+checkpoint 4건. 커밋 6fab97d, e0bf37a |
| 2026-03-04 | (직접 설계) | portfolio 전체 섹션 구조 재편 설계 + audit 문서 | 5 | 6섹션 확정, 전체 코드베이스 파악, 416줄 audit, 4카드 타이틀 변경. 커밋 392e724, checkpoint #4057~#4059 |
| 2026-03-04 | (3종 교차 리뷰+직접 수정) | mcp-memory v2.0 e2e 리뷰 3종 → 19개 Fix 통합 수정 | 5 | Sonnet(78)+Opus(B+)+Codex(48) 교차 리뷰, Tier 0-3 19개 Fix, 10파일 수정, 3중 검증 PASS. checkpoint #4082~#4086 |
| 2026-03-04 | (직접 구현) | portfolio 빌드 수정 + .worktrees 재편 + P1~P3 구조 변경 | 5 | TS6133 데드코드 3개 제거, 03_claude 브랜치 추가, 6섹션 구현, 미결 A-F 트래킹 audit doc, checkpoint #4087~#4092 |
| 2026-03-04 | (직접 구현) | tech-review 아카이브 시스템 전체 구현 | 5 | taxonomy.json(tier1+tier2+fallback), extract-sections.js(36개 소급), remap-tags.js(18일치), topics.html(ko+en), H1 소급(16개), 비용 $3/월 |
| 2026-03-05 | (직접 구현) | tech-review 파이프라인 재설계 (Twitter+YouTube+daily-digest) | 5 | Playwright→GraphQL, Gemini→yt-dlp, digest 날짜별 그룹화, anchor 스크롤 JS, checkpoint 8건 |
| 2026-03-08 s1 | (직접 구현) | tech-review YouTube/Twitter 파이프라인 전면 개선 | 5 | TOC, apply_points, Whisper GPU, Task Scheduler 3개, fetch-twitter.yml 삭제 |
| 2026-03-08 s2 | (직접 구현) | tech-review YouTube 품질 강화 + Portfolio 멀티소스 전환 | 5 | validate_quotes, 100K transcript, 12섹션 일론 머스크, TechReviewMultiSource, sources.json |
| 2026-03-08 s3 | (직접 구현) | mcp-memory v2.2.1 Typed Vector Channel + Goldset v2.2 검증 | 5 | additive→RRF채널, q026-q050 NDCG +0.396, 163 tests, 전체 NDCG@5=0.460 |

**기준:**
- 5: 직접 쓸 수 있는 결과물
- 4: 약간 수정 후 사용
- 3: 방향은 맞지만 재작업 필요
- 2: 참고만 가능
- 1: 재호출 필요

---

## 배포 성과 로그 (portfolio)

| 날짜 | 변경 내용 | 배포 결과 | 이슈 |
|------|----------|-----------|------|
| 2026-02-22 | TechReviewSystemSection.tsx 신규 생성 | git push master (b5a623f) | localhost:5173 시각 확인 대기 |

---

## monet-lab 실험 로그

| 날짜 | 페이지 | 변경 내용 | 커밋 |
|------|--------|----------|------|
| 2026-02-22 | page-12 | FadeIn style prop, 형광펜 highlight | 7567d96 |
| 2026-02-22 | page-12 | orange→background, blue 섹션 하이라이트 | c93b956 |
| 2026-02-22 | page-12 | SectionNarrative → wd-callout 구조 교체 | 509b6f4 |
| 2026-02-22 | page-12 | AI/TR 상세 섹션 portfolio 원본 이식 | cce9486 |
| 2026-02-23 | PMCC/EH/SD | CSS 타이포 정비 + MD 구조 정리 + 이미지 연결 | 미커밋 |
| 2026-02-23 | PMCC | SurveyViz.tsx + SurveyTable.tsx 신규 구현 | 미커밋 |
| 2026-02-23 | PMCC | CSS 레이아웃 1100→1540px, 이미지 그리드, 블록 타입 4개 추가 | 미커밋 |
| 2026-02-23 | 히어로 슬라이더 | 프로그레스 바 드래그 조작 + animation-delay 음수 패턴 | a459e5c, 75ef598 |
| 2026-02-24 | PMCC | Visual Cues 갤러리 + Activity Gallery + 페이지 에디터 + 섹션 구분선 | 5e9866a, 73d1e52 |

---

## 세션 생산성 로그

| 날짜 | 완료 작업 | 소요 시간 | 주요 병목 |
|------|----------|-----------|----------|
| 2026-02-22 | Gemini CLI, n8n 설치, CHANGELOG 완성, hook 버그 수정, 리서치 58개 | ~3h | 다중 창 소통 불가 |
| 2026-02-22 | orch-system-overhaul 11개 태스크 (보안+자동화+정리) | ~2h | - |
| 2026-02-22 | codex-reviewer 에이전트 설계+구현+실전 테스트 | ~1h | Codex CLI 샌드박스 오류 디버깅 |
| 2026-02-22 | monet-lab page-12 UI 개선 + portfolio 컴포넌트 이식 | ~1h | - |
| 2026-02-23 | 전체 시스템 점검 + hooks 전면 업데이트 + v3.0 설계 | ~2h | 점검 항목 범위 파악 |
| 2026-02-23 | v3.0 플랜 실행 Phase A~E + USER-GUIDE 작성 | ~1.5h | - |
| 2026-02-23 | Codex CLI 연동 + 병렬 교차 검증 파이프라인 최적화 (15분→2분) | ~2h | sandbox bypass 플래그 탐색 |
| 2026-02-23 | v3.1 Agent Teams & Linker System 설계+구현 (에이전트 7개+팀 3개+hooks) | ~2h | - |
| 2026-02-23 | tech-review 파이프라인 실패 분석 + 프롬프트 7개 개편 + 안전장치 추가 + 재생성 | ~2h | 거부 응답 패턴 파악 |
| 2026-02-23 | monet-lab page-12 CSS 레이아웃 정비 + 이미지 교체 + 블록 타입 확장 + 컴포넌트 구현 | ~2h | 파일 이름 일관성 (rename 추적) |
| 2026-02-23 | monet-lab 프로그레스 바 드래그 기능 + 커밋 2개 | ~0.5h | - |
| 2026-02-24 | monet-lab Visual Cues + Activity Gallery + 페이지 에디터 구현 | ~1.5h | 에디터 UX 재고 (중단 결정) |
| 2026-02-24 | orchestration v3.1 Living Docs 전면 갱신 (5개 파일) | ~1.5h | - |
| 2026-02-25 | orchestration v3.3 Codex/Gemini 통합 설계 (설계문서+구현플랜 작성+커밋) | ~2h | - |
| 2026-02-25 | orchestration v3.3 전체 구현 + 리뷰 반영 + 미흡 해결 + e2e 23/23 PASS | ~4h | Gemini 경로 문제 디버깅 |
| 2026-02-25 | v3.3 에비던스 문서 + HOME.md/REFERENCE.md + compressor 버그 수정 + 문서화 | ~2h | - |
| 2026-02-26 | v3.3.1 200K Context 최적화 전체 (Phase A~D + 플러그인 비활성화 + hook + statusline + 리뷰 반영) | ~3h | 여러 파일 간 일관성 유지 |
| 2026-02-27 | v3.3.1 일관성 감사 (80+ 파일 스캔 + 15건 수정 + 커밋+push) | ~1h | 코드 블록 내 텍스트 매칭 |
| 2026-03-02 | PMCC_DETAIL_KO.md 전면 개정 (13개 지시 + 표현 평이화 + STATE.md 갱신) | ~1.5h | 표현 대안 탐색 반복 |
| 2026-03-04 | E2EWorkflow 헤더/배경 분리 + Key Decisions sandbox 3종 제작 | ~1h | - |
| 2026-03-03 | Auto Memory 개선 + .ctx 정리 + Playwright 활성화 (8개 작업) | ~1.5h | - |
| 2026-03-04 | HOW I AI Evolution 전면 재작성 (글+UI+인터뷰 원본+버그 수정) | ~1.5h | - |
| 2026-03-03 | QMD 설치 + D3 시각화 3종 + orch-graph 반복 개선 | ~2h | QMD 한글 검색 불가 (BM25 토크나이저 한계) |
| 2026-03-03 | How I Operate 전면 재작성 + mcp-memory 확인 + checkpoint 4건 | ~1h | - |
| 2026-03-04 | 전체 섹션 구조 재편 설계 + audit 416줄 + 4카드 타이틀 + checkpoint 3건 | ~1.5h | - |
| 2026-03-04 | 3종 e2e 리뷰 실행 + 통합 분석 + 19개 Fix 수정 + 3중 검증 + 문서화 | ~2h | Codex CLI 모델명 설정 주의 |
| 2026-03-04 | 빌드 수정 + .worktrees 재편 + P1~P3 구조변경 + 미결 A-F 트래킹 + 세션 전환 체인 | ~2h | _sandbox 폴더 Windows native 삭제 필요 |
| 2026-03-04 | tech-review 아카이브 시스템 (taxonomy + extract-sections + remap-tags + topics + H1 소급 + 비용 분석) | ~2h | - |
| 2026-03-05 | tech-review 파이프라인 재설계 (Twitter GraphQL + YouTube yt-dlp + daily-digest 개선 + post.html anchor) | ~2h | - |
| 2026-03-08 s1 | tech-review YouTube/Twitter 파이프라인 전면 개선 (TOC + apply_points + Whisper GPU + Task Scheduler + 구조 통일) | ~2h | CUDA/PyTorch 설치 |
| 2026-03-08 s2 | tech-review YouTube 품질 강화 + Portfolio 멀티소스 전환 (validate_quotes + 100K + UI + 일론 머스크 + MultiSource) | ~2h | git checkout 버전 복원 |
| 2026-03-08 s3 | mcp-memory v2.2.1 Typed Vector Channel + Goldset v2.2 q026-q075 수동 검증 | ~2h | goldset ID 수동 매칭 |
| 2026-03-09 | Writing>TR 전면 재설계 + StatsBar + @author 폰트 + TR_SYSTEM_KO + TechReviewSystemSection + checkpoint | ~1.5h | - |

---

## 세션 요약 테이블

| 날짜 | 완료 태스크 | 주요 프로젝트 | 결정 수 |
|------|------------|--------------|---------|
| 2026-02-22 | 다수 (v2.2 오버홀, monet-lab, portfolio 등) | orchestration/monet-lab/portfolio | 20개+ |
| 2026-02-23 | 9개 (시스템 점검, hooks, v3.0 설계) | orchestration | 8개 |
| 2026-02-23 | 7개 (v3.0 Phase A~E 실행, USER-GUIDE) | orchestration | 3개 |
| 2026-02-23 | 4개 (Codex 연동, 병렬 파이프라인 최적화) | orchestration | 3개 |
| 2026-02-23 | 14개 (v3.1 설계+구현 — 에이전트 7개+팀 3개+hooks+Living Docs) | orchestration | 6개 |
| 2026-02-23 | 8개 (파이프라인 실패 분석+프롬프트 7개 개편+안전장치+재생성 성공) | tech-review | 5개 |
| 2026-02-23 | 12개+2개 (CSS 레이아웃+이미지+블록+컴포넌트+동영상+드래그 기능) | monet-lab | 5개+1개 |
| 2026-02-24 | 10개 (Visual Cues + Activity Gallery + 페이지 에디터 + 섹션 구분) | monet-lab | 6개 |
| 2026-02-24 | 12개 (Living Docs 5개 파일 + compressor 강화) | orchestration | 2개 |
| 2026-02-24 | 9개 (v3.2 Phase 0~5 전체 구현 + 테스트 + 커밋) | orchestration | 5개 |
| 2026-02-24 | 11개 (fetch-perplexity 재작성 + 프롬프트 7개 + translate/parse/yml + 통합 테스트 3회) | tech-review | 4개 |
| 2026-02-25 | 5개 (daily-memo 파이프라인 수정 + e2e 2회 성공 + 알림 무시 + 문서 업데이트 + RC 리서치) | daily-memo/orchestration | 2개 |
| 2026-02-25 | 8개 (v3.3 Codex/Gemini 통합 설계+구현플랜 작성+커밋+sync) | orchestration | 5개 |
| 2026-02-25 | 23개 (v3.3 전체 구현 + Opus 리뷰 반영 + 미흡 해결 + e2e 23/23 PASS) | orchestration | 3개 |
| 2026-02-25 | 11개 (에비던스 문서 2건 + HOME.md/REFERENCE.md + compressor 버그 수정 + 타임스탬프 규칙) | orchestration | 3개 |
| 2026-02-25 | 7개 (v3.3 e2e 12시나리오 설계 + 1차·2차 실행 + 비교 분석 + 버그 3건 수정 + 에비던스 기록) | orchestration | 3개 |
| 2026-02-26 | 26개 (v3.3.1 200K 최적화 Phase A~D + 플러그인 비활성화 + hook + statusline + 리뷰 반영) | orchestration/dev | 6개 |
| 2026-02-27 | 15건 (전체 .md 일관성 감사 + context/ 경로 수정 + hook 패턴 수정 + 커밋+push) | orchestration | 2개 |
| 2026-03-02 | 4개 (PMCC_DETAIL_KO.md 개정 + 표현 평이화 + TS 체크 + STATE.md 갱신) | portfolio | 3개 |
| 2026-03-02 | 1개 (autocompact 50%→75% 설정 최적화) | orchestration | 1개 |
| 2026-03-04 | 5개 (E2EWorkflow 배경 분리 + sandbox v1/v2/v3 제작 + STATE.md 갱신 + push) | portfolio | 2개 |
| 2026-03-03 | 8개 (memory review + analyze-session + auto-promote + session hooks + .ctx 정리 + Playwright) | orchestration | 4개 |
| 2026-03-04 | 6개 (aiWorkflowData+AiWorkflowSection 재작성 + 인터뷰 원본 + 버그 수정 + STATE 갱신 + push) | portfolio | 3개 |
| 2026-03-03 | 7개 (QMD 설치 + D3 시각화 3종 + orch-graph 반복 개선 + CHANGELOG 실측 데이터 + STATE 갱신) | orchestration | 3개 |
| 2026-03-03 | 6개 (How I Operate 재작성 + mcp-memory 확인 + checkpoint + CHANGELOG/HOME 갱신) | portfolio/orchestration | 4개 |
| 2026-03-04 | 7개 (전체 코드베이스 파악 + audit 문서 생성 + 6섹션 구조 확정 + 4카드 타이틀 변경 + checkpoint 3건) | portfolio | 4개 |
| 2026-03-04 | 19개 Fix (3종 e2e 리뷰 통합 → 10파일 수정 + 3중 검증 PASS + checkpoint 5건 + 리포트 문서화) | mcp-memory | 8개 |
| 2026-03-04 | 빌드 수정 + .worktrees 재편 + P1~P3 구조변경(claude/portfolio 브랜치) + 미결 A-F 트래킹 + checkpoint 6건 | portfolio | 4개 |
| 2026-03-04 | tech-review 아카이브 구현 (taxonomy.json + extract-sections + remap-tags + topics.html + H1 소급 + 비용 분석) | tech-review | 5개 |
| 2026-03-05 | 6개 (Twitter GraphQL + YouTube yt-dlp + daily-digest 개선 + post.html anchor + Actions yml 수정 + checkpoint 8건) | tech-review | 3개 |
| 2026-03-08 | 9개 (YouTube TOC + apply_points 개인화 + Haiku→Codex 교체 + Whisper GPU + Task Scheduler + fetch-twitter.yml 삭제 + summary 통일 + highlights 규칙 + CUDA 설치) | tech-review | 6개 |
| 2026-03-08 s2 | 8개 (analyze-youtube.py 품질 강화 + youtube.html UI + 일론 머스크 확정 + TechReviewMultiSource + sources.json) | tech-review/portfolio | 7개 |
| 2026-03-08 s3 | 9개 (v2.2.1 Typed Vector Channel + Goldset v2.2 q026-q075 검증 + 163 tests + Living Docs 갱신) | mcp-memory | 3개 |
| 2026-03-09 | 6개 (Writing>TR 전면 재설계 + StatsBar + @author 폰트 + checkpoint 5건) | portfolio/tech-review | 4개 |
