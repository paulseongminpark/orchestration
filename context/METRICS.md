# SOT Metrics — 성과 지표

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
| 2026-02-23 | (직접 구현) | monet-lab page-12 CSS 레이아웃 + 이미지 그리드 + 블록 타입 확장 | 5 | 1100→1540px, 4개 블록 추가, 7개 이미지 교체 |
| 2026-02-23 | (직접 구현) | monet-lab 프로그레스 바 드래그 기능 + 커밋 2개 | 5 | animation-delay 음수 패턴, 히어로 슬라이더 UX 완성 |
| 2026-02-24 | (직접 구현) | monet-lab VisualCuesGallery + ActivityGallery + 페이지 에디터 | 4 | 9개 이미지 비대칭, 5항목 grid-area, 에디터 DEV only (구현 중단) |
| 2026-02-24 | (직접 문서화) | orchestration v3.1 Living Docs 전면 갱신 | 5 | README, ROADMAP, SYSTEM-GUIDE, USER-GUIDE, HOME.md |
| 2026-02-24 | (직접 구현) | orchestration v3.2 전체 구현 (Phase 0~5) | 5 | 리좀형 4팀+허브, SoT 확립, doc-syncer+/dispatch 신규, auto-trim, 2커밋 pushed |

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
