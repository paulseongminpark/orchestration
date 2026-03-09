# Cross-CLI Shared Context
> 자동 관리. 모든 CLI 공유 메모리.
> 출처 마커: [claude], [gemini], [codex]

## Session: tech-review 세션 2 — YouTube 파이프라인 + 포트폴리오 연동 (2026-03-08 22:45~)
[claude] tech-review + portfolio 크로스 작업:
- tech-review analyze-youtube.py 변경:
  - validate_quotes 로직 추가 (100K 용량 지원)
  - key schema 갱신 (apply_points {text, key} 포맷)
  - Whisper fallback STT 안정화
- tech-review youtube.html 8회 수정:
  - TOC child 네비게이션
  - 섹션번호 렌더링
  - blue quote 강조 스타일
  - smart_brevity "why_watch" 통합
- tech-review sources.json 갱신:
  - build-sources-feed.js 실행 → bookmarks.json + youtube-*.json 병합
  - 포트폴리오 TechReviewMultiSource.tsx에 3회 fetch 반영됨
- portfolio TechReviewMultiSource.tsx 3회 수정:
  - sources.json fetch URL 통합 (SOURCES_URL 정의)
  - YoutubeItem 인터페이스 section_count, published_at 필드
  - 데이터 매핑: youtube.summary → why_watch 변환
- tech-review STATE.md 갱신
- 영향도:
  - portfolio 렌더링 자동 동기화 (sources.json fetch 메커니즘)
  - YouTube 파이프라인: analyze-youtube.py → youtube.html → build-sources-feed.js → sources.json → portfolio
  - bookmarks.json 갱신 시 3가지 소스 (Blog, YouTube, Twitter) 모두 refreshed

## Session: QMD 설치 + 시각화 인프라 (2026-03-03)
[claude] orchestration 완료:
- QMD @tobilu/qmd v1.0.7 설치 (CPU 모드)
- collection: knowledge(83 md), sessions(3 md)
- 시각화 3종 신규:
  - `_auto/session-graph.html`: D3 force graph, live-context.md 기반 세션↔파일 관계
  - `_auto/orch-timeline.html`: v0→v4 수직 타임라인, 버전 카드 + 스파크라인
  - `_auto/orch-graph.html`: D3 force-directed, 버전11+개념36 노드, CON_EDGES 진화 체인
- 커밋 1f1fe9e
- 영향도: orchestration 자동화 인프라 강화, 다른 프로젝트 코드 미영향

## Session: portfolio cleanup & verification (2026-02-28)
[claude] portfolio 마무리:
- deploy.yml: vercel.json→dist/ 복사 추가 (Vercel gh-pages 빌드 차단)
- STATE.md: v1.0-clean 구조 정리 반영
- 커밋 3950810, e463a7b push 완료
- verify 발견: aiWorkflowData.ts 로컬 미커밋 변경 → AiWorkflowSection.tsx 42개 TS에러 (CI 정상, 로컬만)

## 크로스 프로젝트 영향
- tech-review sources.json ← portfolio TechReviewMultiSource.tsx fetch (서로 동기)
- youtube 분석 파이프라인 → portfolio 렌더링 자동 연결
- orchestration 시각화 → portfolio knowledge 검색 개선 (간접)
- portfolio deploy.yml → Vercel CI/CD 동작 검증 필요
- monet-lab aiWorkflowData.ts ↔ portfolio: 동명 파일 확인됨 (별도 프로젝트)
- codex/gemini 브랜치: master와 동일 고정 완료

## 다음 세션
- tech-review sources.json 첫 실행 결과 검증 (portfolio fetch 정상 반영)
- bookmarks.json 갱신 → sources.json 재생성 자동화 검증
- YouTube 플레이리스트 추가 기능
- E2E 파이프라인 검증 (analyze-youtube → build-sources → portfolio fetch)
- Vercel 배포 모니터링
- monet-lab 44개 미커밋 정리 스케줄
- QMD 인덱싱 활용: knowledge 검색 시스템 파일럿
