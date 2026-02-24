# Decisions Log

> 세션별 중요 결정 사항. compressor가 자동 append.
> 태그: pf=portfolio, tr=tech-review, ml=monet-lab, orch=orchestration
> ❌=미반영, ✅=반영완료, 🚫=취소

## 미반영

2026-02-24 [monet-lab] VisualCuesGallery: 전용 컴포넌트, 마크다운 블록 `**[visual-cues-gallery]**` | ml:❌
2026-02-24 [monet-lab] ActivityGallery: 전용 컴포넌트, CSS grid-area, `**[activity-gallery]**` | ml:❌
2026-02-24 [monet-lab] 페이지 에디터 구현 중단 — 직접 지시 방식이 더 효율적 | ml:✅
2026-02-24 [monet-lab] 피그마 내보내기 보류 — 수동 전달 비효율 | ml:✅
2026-02-24 [monet-lab] 가로선: GALLERY, GROWTH & METRICS eyebrow 기준으로만 삽입 | ml:❌
2026-02-24 [monet-lab] 동영상: 원본 git 미커밋, _web.mp4만 커밋 (기존 규칙 유지) | ml:✅
2026-02-24 [orchestration] v3.2 리좀형 4팀+허브 + SoT 확립 + 에이전트 24개 | orch:✅
2026-02-24 [orchestration] pf-context→project-context 범용화 (프로젝트 파라미터) | orch:✅
2026-02-24 [orchestration] doc-syncer 신규 (3레이어 검증) | orch:✅
2026-02-24 [orchestration] /dispatch 신규 스킬 (catchup 흡수) | orch:✅
2026-02-24 [orchestration] live-context.md auto-trim 100줄 캡 | orch:✅
2026-02-24 [orchestration] compressor 7단계에 MEMORY.md 추가 | orch:✅
2026-02-23 [monet-lab] 프로그레스 바 드래그: animation-delay 음수로 해당 지점부터 재개 | ml:❌
2026-02-23 [monet-lab] quote-image 블록: 엇갈린 배치, qiCount % 2 === 1이면 reverse | ml:✅
2026-02-23 [monet-lab] placeholder 블록: `**[placeholder: N]**` 문법 | ml:✅
2026-02-23 [monet-lab] SurveyTable CSV 병합: Survey 1(38명) col5=rating, Survey 2(5명) col6=rating | ml:❌
2026-02-23 [monet-lab] 파서 블록 문법: **[survey-viz]**, **[survey-table]** | ml:❌
2026-02-23 [tech-review] EN 번역 [1][2] 인용 마커 잔류 이슈 수정 | tr:❌
2026-02-23 [portfolio] Obsidian 섹션 모바일 반응형 미확인 (375px 양옆 배치) | pf:❌
2026-02-22 [portfolio] 07~10 스크린샷 → lab.md 이미지 링크 추가 | pf:❌
2026-02-22 [tech-review] keywords-log.md 신설, fetch-perplexity KST 버그 수정 | tr:❌

## 아카이브

2026-02-23 [monet-lab] page-12 CSS 레이아웃: 1100px→1540px, 프로즈/미디어 분리 (860px 중앙) | ml:✅
2026-02-23 [monet-lab] 이미지 그리드 자동 그룹핑 (2+개 연속) → preprocessBlocks | ml:✅
2026-02-23 [monet-lab] 히어로 슬라이더: CSS animation 무한루프, 프로그레스 바 드래그 | ml:✅
2026-02-23 [orch] Phase E 파일럿 테스트 (Agent Teams + worktree 병렬 처리) | orch:❌
2026-02-23 [orch] STATE.md 경로 불일치 수정 (교차 검증 발견) | orch:❌
2026-02-23 [orch] copy-session-log.py overwrite 문제 수정 | orch:❌
2026-02-23 [orch] v3.1 Agent Teams & Linker System — 에이전트 7개+팀 3개+hooks | orch:✅
2026-02-23 [orch] context-linker 실시간 세션 간 맥락 공유 (live-context.md + PostToolUse hook) | orch:✅
2026-02-23 [orch] project-linker 프로젝트 간 변경 영향 감지 (커밋 시점 트리거) | orch:✅
2026-02-23 [orch] meta-orchestrator 팀 디스패치 판단 (Sonnet) | orch:✅
2026-02-23 [orch] CLAUDE.md 전역 파일 = "global" 분류 (hook 타임스탬프 KST 수정 포함) | orch:✅
2026-02-23 [portfolio] Obsidian UI 목업: CSS 재현 방식 (스크린샷 아님) — 코드 렌더링 일관성 | pf:✅
2026-02-23 [portfolio] Graph View: 수동 배치 (force-directed 아님) — 의도된 클러스터 보장 | pf:✅
2026-02-23 [portfolio] 목업+그래프 양옆 배치 — Living Docs 블록 내 통합 | pf:✅
2026-02-23 [tech-review] 프롬프트 7개 Smart Brevity v2 통일 (소스 가이드 + 분량 지시 + 마커 제거) | tr:✅
2026-02-23 [tech-review] 수요일 주제: AI × Industry | tr:✅
2026-02-23 [tech-review] 제목 추출: TITLE 프롬프트 제거 → Today in One Line 본문 자동 추출 | tr:✅
2026-02-23 [tech-review] API 예산 $5/월 기준 일일 KO 2,000~2,200자 | tr:✅
2026-02-23 [tech-review] KO fetch 실패 시 EN 번역 자동 건너뜀 (create-post.yml 안전장치) | tr:✅
2026-02-23 [orch] Codex CLI 교차 검증 최적화: sandbox bypass + reasoning medium (15분→2분) | orch:✅
(이전 기록 생략...)
