# 세션 요약

> 최종 수정: 2026-03-04

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: HOW I AI 섹션 Evolution 파트 전면 재작성 (글 + UI)

완료:
  - [portfolio] aiWorkflowData.ts — TimelineItem 타입 변경(phase/question/body[]), TIMELINE 3주 질문 기반 재작성
  - [portfolio] AiWorkflowSection.tsx — Evolution 섹션 UI (3칸 그리드→세로스택, 질문 21px bold 강조), 시스템에 대하여 수정(opencode 제거, 하네스 도구/agent engineering OS 맥락)
  - [portfolio] docs/evolution-interview-2026-03-03.md — 인터뷰 원본 저장
  - [portfolio] context/STATE.md 갱신
  - [portfolio] code-review 버그 수정: fetch .catch() 추가, systemDetail maxWidth 680→800
  - [portfolio] 커밋 e0b1c3c, f95e390 → master 브랜치 push 완료

현재 상태:
  portfolio master 브랜치 clean. 미반영 결정 없음.

실패 기록 (삭제 금지):
  - (이번 세션 실패 없음)

다음 할 것:
  1. Key Decisions 레이아웃 선택 (V1투톤/V2아코디언/V3내러티브 중) → AiWorkflowSection 반영
  2. 모바일 반응형 확인 (375px)
  3. untracked 파일 정리: public/orch-graph.html, public/work/pmcc/diagram_1_new.png, reference/ref_obsidian.jpg
  4. monet-lab 44개 미커밋 정리

열린 결정:
  - Key Decisions 레이아웃: V1(투톤) / V2(아코디언) / V3(내러티브) 중 미결
  - /compact 스킬 이름 충돌 해결 필요
  - Resume/Contact 탭 노출 전략

주의사항:
  - portfolio 브랜치: master (main 아님)
  - untracked 파일 3개 방치 중 — 별도 정리 필요
  - Playwright MCP 활성화됨 — 브라우저 스크린샷 테스트 가능

[재작성] 세션 목표: HOW I AI Evolution 전면 재작성 | 남은 할 것: 1. Key Decisions 레이아웃 선택+반영 2. 모바일 반응형 375px 3. untracked 파일 정리 4. monet-lab 미커밋 정리
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

---

=== 이전 세션 (2026-03-04) ===

세션 목표: QMD 설치 + D3.js 기반 오케스트레이션 시각화 3종 구현

완료:
  - QMD 설치, D3 시각화 3종 (session-graph, orch-timeline, orch-graph), CHANGELOG 실측 데이터 반영

실패 기록 (삭제 금지):
  - [시도] QMD BM25 한글 검색 → [실패] 한글 토크나이징 안됨 → [원인] BM25 기본 토크나이저가 한글 미지원
  - [시도] QMD query + LLM reranker → [실패] context 오류 → [원인] reranker가 LLM context 미포함 상태에서 호출
  - [시도] QMD search → [실패] 영어 쿼리만 부분 동작 → [원인] get만 정상, search/query는 한글 환경에서 불안정

=== 이전 세션 (2026-03-04) ===

세션 목표: portfolio E2EWorkflow 헤더/배경 분리 + Key Decisions sandbox 3종 제작

완료:
  - [portfolio] E2EWorkflowSection.tsx 헤더/배경 분리 (commit caca5a8)
  - [portfolio] Key Decisions sandbox 3종 (_sandbox/src/ v1/v2/v3)
