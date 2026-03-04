# Decisions Log

> 최종 수정: 2026-03-03 (세션4)

> 세션별 중요 결정 사항. compressor가 자동 append.
> 태그: pf=portfolio, tr=tech-review, ml=monet-lab, orch=orchestration
> ❌=미반영, ✅=반영완료, 🚫=취소

## 미반영

2026-03-04 [mcp-memory] graph_analyzer run_* 메서드에 limit 파라미터 추가 (F-1) | mem:✅
2026-03-04 [mcp-memory] E7 ChromaDB 재임베딩을 node_enricher._apply()에서 직접 처리 (F-2) | mem:✅
2026-03-04 [mcp-memory] _update_node() 즉시 commit 추가 — C6 atomicity (F-3) | mem:✅
2026-03-04 [mcp-memory] 헤비안 학습 hybrid.py _hebbian_update() 구현 (F-4) | mem:✅
2026-03-04 [mcp-memory] Principle→Philosophy 승격 경로 + PROMOTE_LAYER 추가 (F-7) | mem:✅
2026-03-04 [mcp-memory] E24를 daily_enrich Phase 4에 연결 (F-8) | mem:✅
2026-03-04 [mcp-memory] graph_analyzer._insert_edge에 direction/reason 저장 (F-9) | mem:✅
2026-03-04 [mcp-memory] 복수 모델 교차 검증 패턴 확인 — 단일 리뷰 대비 커버리지 높음 | orch:✅
2026-03-04 [mcp-memory] v2.1 defer: 시간 감쇠 스크립트, init_db v2, schema.yaml v2, relate/connect 도구 | mem:❌
2026-03-04 [portfolio] 6섹션 구조 확정 — 01 About / 02 How I Think / 03 How I Build / 04 Work / 05 Writing (+TR) / 06 Contact | pf:❌
2026-03-04 [portfolio] TR → Writing 섹션 이동 결정 | pf:❌
2026-03-04 [portfolio] Obsidian 독립 섹션 → 03 How I Build 내 한 단락으로 축소 결정 | pf:❌
2026-03-04 [portfolio] 온톨로지: 03 How I Build 내 자리 확보 (별도 설계 세션) | pf:❌
2026-03-03 [portfolio] How I Operate 전면 재작성 — 추상 5카드 → 외부 메모리 4원칙 카드 (Connection/Context as Currency/Structure over Willpower/Governance) | pf:✅
2026-03-03 [portfolio] Direction B 확정: How I Operate(원칙) → HOW I AI(구현) 하나의 이야기 | pf:✅
2026-03-03 [portfolio] "이색적인 접합" 4번 카드 제거 — show vs tell 원칙 | pf:✅
2026-03-03 [orchestration] mcp-memory v0.1.0 가동 확인 — 7 MCP 도구, settings.json 등록됨 | orch:✅
2026-03-04 [portfolio] HOW I AI Evolution 전면 재작성 — 인터뷰 기반 3주 타임라인, 질문 중심 UI, TimelineItem 타입 phase/question/body[] | pf:✅
2026-03-04 [portfolio] 시스템에 대하여: opencode 삭제, 하네스 도구/agent engineering OS 맥락으로 재작성 | pf:✅
2026-03-03 [orchestration] orch-graph 데이터 소스: CHANGELOG.md 직접 읽기 (QMD 미활용) | orch:✅
2026-03-03 [orchestration] orch-graph 레이아웃: SAVED_POSITIONS로 사용자 정의 배치 저장 | orch:✅
2026-03-03 [orchestration] QMD 한글 검색 불가 확인 — BM25 토크나이저 한글 미지원, get만 동작 | orch:❌
2026-03-03 [orchestration] .ctx/ Cross-CLI 공유 메모리 폐기 — 실사용 없음, 복잡도만 추가 | orch:✅
2026-03-03 [orchestration] rulesync sandbox 세팅용으로만 유지 (프로덕션 미적용) | orch:✅
2026-03-03 [orchestration] Playwright MCP 플러그인 활성화 — 브라우저 자동 스크린샷/테스트용 | orch:✅
2026-03-03 [orchestration] auto-promote.sh 도입 — 에러 2회+ pending.md 항목 MEMORY.md 자동 승격 | orch:✅
2026-03-02 [portfolio] Obsidian 섹션 구조: 10단계 → 5단계 (Understand→Explore→Refactor→Test→Deploy) | pf:✅
2026-03-02 [portfolio] E2E 테스트 문서: 8개 → 10개 Phase (Prepare/Execute/Verify 세분화) | pf:✅
2026-03-02 [portfolio] 타입스크립트→vanilla.js 마이그레이션 (프레임워크 의존성 제거) | pf:✅
2026-03-02 [portfolio] 타이포그래피 위계 체계화 + sticky 헤더 구현 | pf:✅
2026-03-02 [orchestration] AUTOCOMPACT 임계값 50%→75% 상향 — compact 빈도 과다 해결 | orch:✅
2026-03-02 [portfolio] PMCC 어조 평이화 — 학술적 표현→일상 언어 전환 확정 | pf:✅
2026-03-02 [portfolio] flowchart 위치: Approach 뒤 배치, Gallery: Dataset 뒤 배치 | pf:✅
2026-02-25 [orchestration] monet-lab 44개 미커밋 정리 필요 (스크린샷 PNG 산재) | ml:❌
2026-02-24 [monet-lab] VisualCuesGallery: 전용 컴포넌트, 마크다운 블록 `**[visual-cues-gallery]**` | ml:❌
2026-02-24 [monet-lab] ActivityGallery: 전용 컴포넌트, CSS grid-area, `**[activity-gallery]**` | ml:❌
2026-02-24 [monet-lab] 가로선: GALLERY, GROWTH & METRICS eyebrow 기준으로만 삽입 | ml:❌
2026-02-23 [monet-lab] 프로그레스 바 드래그: animation-delay 음수로 해당 지점부터 재개 | ml:❌
2026-02-23 [monet-lab] SurveyTable CSV 병합: Survey 1(38명) col5=rating, Survey 2(5명) col6=rating | ml:❌
2026-02-23 [monet-lab] 파서 블록 문법: **[survey-viz]**, **[survey-table]** | ml:❌
2026-02-23 [portfolio] Obsidian 섹션 모바일 반응형 미확인 (375px 양옆 배치) | pf:❌
2026-02-22 [portfolio] 07~10 스크린샷 → lab.md 이미지 링크 추가 | pf:❌

## 아카이브

2026-02-27 [orchestration] v4.0 Context as Currency: 에이전트 24→15 통합, 스킬 14→9, rulesync, .ctx/ Cross-CLI, worktree 인프라 | orch:✅
2026-02-26 [orchestration] v3.3.1 200K Context 최적화: baseline 축소 + .chain-temp + compact 전략 | orch:✅
2026-02-25 [orchestration] Opus 가치="발견": 기본 수행 동일, 숨겨진 문제·패턴·리스크 자발적 탐색이 차별점 | orch:✅
2026-02-25 [orchestration] 모델 정책 e2e 검증 완료: Haiku=수집, Sonnet=분석, Opus=판단·리뷰 최적 | orch:✅
2026-02-25 [orchestration] compressor 타임스탬프: date +%H:%M 필수, LLM 추정 금지 | orch:✅
2026-02-25 [orchestration] meta-orchestrator + verify barrier = Opus 사용 명시 | orch:✅
2026-02-25 [orchestration] v3.3 전체 e2e: 24에이전트+14스킬+4팀+6체인+7훅+2CLI evidence/v3.3 기록 | orch:✅
2026-02-25 [orchestration] v3.3 세션 전환 체인: verify→sync-all→compressor→linker 건너뛰기 금지 | orch:✅
2026-02-25 [orchestration] Gemini 스킬 절대 경로 필수: ~/→/c/Users/pauls/ (로컬 .claude/ 우선 문제) | orch:✅
2026-02-25 [orchestration] _meta 스키마: Codex 3필드 vs Gemini 5필드 분리 확정 | orch:✅
2026-02-25 [orchestration] v3.3 Claude=결정권자 Codex/Gemini=추출기 Verify Barrier 3단계 | orch:✅
2026-02-25 [orchestration] v3.3 세션 전환 체인 신설: verify→sync-all→compressor→linker 후 /clear 허용 | orch:✅
2026-02-25 [orchestration] Gemini=벌크추출기(4스킬) Codex=정밀검증기(3프로필) 역할 분리 | orch:✅
2026-02-25 [orchestration] 컨텍스트 오프로딩 세션당 ~170K 토큰(88%) 절약 설계 | orch:✅
2026-02-25 [daily-memo] GitHub Actions 자동 sync 파이프라인 완성: 브랜치 push → main Inbox.md 자동 반영 + 레포 알림 무시 설정 | dm:✅
2026-02-23 [monet-lab] quote-image 블록: 엇갈린 배치, qiCount % 2 === 1이면 reverse | ml:✅
2026-02-23 [monet-lab] placeholder 블록: `**[placeholder: N]**` 문법 | ml:✅
2026-02-23 [tech-review] EN 번역 [1][2] 인용 마커 잔류 이슈 수정 | tr:✅
2026-02-22 [tech-review] keywords-log.md 신설, fetch-perplexity KST 버그 수정 | tr:✅
2026-02-24 [tech-review] sonar-deep-research 파이프라인 전환: 5건/일, URL검증, 도메인필터, 폴백 | tr:✅
2026-02-24 [tech-review] 일요일 프롬프트 글로벌 AI 현장 전환 + 이번 주 월~토 키워드 합산 | tr:✅
2026-02-24 [monet-lab] 페이지 에디터 구현 중단 — 직접 지시 방식이 더 효율적 | ml:✅
2026-02-24 [monet-lab] 피그마 내보내기 보류 — 수동 전달 비효율 | ml:✅
2026-02-24 [monet-lab] 동영상: 원본 git 미커밋, _web.mp4만 커밋 (기존 규칙 유지) | ml:✅
2026-02-24 [orchestration] v3.2 리좀형 4팀+허브 + SoT 확립 + 에이전트 24개 | orch:✅
2026-02-24 [orchestration] pf-context→project-context 범용화 (프로젝트 파라미터) | orch:✅
2026-02-24 [orchestration] doc-syncer 신규 (3레이어 검증) | orch:✅
2026-02-24 [orchestration] /dispatch 신규 스킬 (catchup 흡수) | orch:✅
2026-02-24 [orchestration] live-context.md auto-trim 100줄 캡 | orch:✅
2026-02-24 [orchestration] compressor 7단계에 MEMORY.md 추가 | orch:✅
(이전 기록 생략...)
