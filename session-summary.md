# 세션 요약

> 최종 수정: 2026-03-04

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: tech-review 아카이브 시스템 구현 (taxonomy + 섹션 추출 + 태그 재매핑 + topics 페이지)

완료:
  - [tech-review] fetch-perplexity.js: Smart Brevity system message 강화 (callSonarPro + submitDeepResearch)
  - [tech-review] max_tokens 10000 → 7500 (fetch + translate 동시 축소)
  - [tech-review] taxonomy.json 신규: tier1(8개) + tier2(20개+) + fallback_map
  - [tech-review] extract-sections.js 신규: `## N.` 섹션 추출 → `_data/sections/YYYY-MM-DD-{lang}.json` (36개 소급)
  - [tech-review] remap-tags.js 신규: 기존 태그 taxonomy 재매핑 (18일치)
  - [tech-review] ko/topics.html + en/topics.html 신규: 태그별 아카이브 (JS hash routing)
  - [tech-review] tier1 카테고리 섹션 태그에서 제외 결정 — tier2만 사용
  - [tech-review] create-post.yml: 섹션 추출 단계 추가
  - [tech-review] H1 헤더 제거 소급 (16개 포스트) + parse-content.js 방어 로직
  - [tech-review] 3/4 사실 오류 수정 (Department of War → Department of Defense)
  - [tech-review] API 비용 분석: ~$3/월, $5 예산 내 여유
  - [tech-review] STATE.md 갱신 + 커밋 + push 완료
  - [orchestration] settings.json: memory MCP (python3 복원) + Serena MCP 재추가

현재 상태:
  아카이브 시스템(taxonomy + 섹션 추출 + topics 페이지) 구현 완료. 일일 파이프라인에 extract-sections 통합됨. 새 소스(트위터/스레드/유튜브) 미구현.

실패 기록 (삭제 금지):
  - (이번 세션 실패 없음)

다음 할 것:
  1. 트위터 소스 파이프라인 (Playwright + following 피드, 280자+/스레드/외부링크 필터)
  2. 스레드 소스 파이프라인 (Playwright 공개 프로필 스크래핑)
  3. 유튜브 소스 파이프라인 (YouTube Data API + yt-dlp + Gemini AI Studio, youtube-sources.json)
  4. portfolio: PR 5174 검토 + master 병합
  5. mcp-memory: 커밋+push + enrichment --dry-run

열린 결정:
  - source_type 필드 통합 방식 (perplexity | twitter | threads | youtube)
  - 트위터 following 피드 vs 리스트 기반 선택
  - 유튜브 AI Studio 무료 한도 내 운영 가능성
  - portfolio PR 5174 병합 타이밍

주의사항:
  - tech-review blog 레포: paulseongminpark/tech-review (master 브랜치)
  - tech-review ops 레포: paulseongminpark/tech-review-ops (master 브랜치)
  - taxonomy.json: tier1은 분류용, 실제 검색 태그는 tier2만
  - topics.html: JS hash routing (/ko/topics/#nvidia)
  - 월 API 비용 ~$3 ($5 예산 내)

[재작성] 세션 목표: tech-review 아카이브 구현 (taxonomy+섹션추출+topics) | 남은 할 것: 1. 트위터 파이프라인 2. 스레드 파이프라인 3. 유튜브 파이프라인 4. portfolio PR 5174 병합 5. mcp-memory enrichment
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

---

=== 이전 세션 (2026-03-04) ===

세션 목표: portfolio 빌드 수정 + .worktrees 재편 + P1~P3 구조 변경

완료:
  - [portfolio] TS 데드코드 3개 제거 (b0c3555), .worktrees 재편, 6섹션 구현, 미결 A-F 트래킹
  - checkpoint #4087~#4092

실패 기록 (삭제 금지):
  - (없음)

=== 이전 세션 (2026-03-04) ===

세션 목표: portfolio 전체 섹션 구조 재편 설계 — 6섹션 구조 확정

완료:
  - [portfolio] 6섹션 확정, audit 416줄, 4카드 타이틀 변경, checkpoint #4057~#4059
  - 커밋 392e724 → master push

실패 기록 (삭제 금지):
  - (없음)

=== 실패 기록 아카이브 (삭제 금지) ===
  - [시도] QMD BM25 한글 검색 → [실패] 한글 토크나이징 안됨 → [원인] BM25 기본 토크나이저가 한글 미지원
  - [시도] QMD query + LLM reranker → [실패] context 오류 → [원인] reranker가 LLM context 미포함 상태에서 호출
  - [시도] QMD search → [실패] 영어 쿼리만 부분 동작 → [원인] get만 정상, search/query는 한글 환경에서 불안정
