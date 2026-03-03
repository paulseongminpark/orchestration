# 세션 요약

> 최종 수정: 2026-03-03

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: portfolio How I Operate 섹션 전면 재작성 + mcp-memory 시스템 확인

완료:
  - [portfolio] How I Operate 섹션 전면 재작성 — 추상 프레임워크(Time/Sensation/Relation) 5카드 → 외부 메모리 시스템 기반 4원칙 카드 (Connection / Context as Currency / Structure over Willpower / Governance)
  - [portfolio] parseSystemContent 함수 제거, SYSTEM_ITEMS 하드코딩, TOC 5→4, subtitle 교체
  - [portfolio] 커밋 6fab97d, e0bf37a → master 브랜치 push 완료
  - [orchestration] mcp-memory 시스템 확인 — /c/dev/01_projects/06_mcp-memory/ v0.1.0, 7개 MCP 도구, SQLite+FTS5+ChromaDB+NetworkX
  - [orchestration] /checkpoint 실행 — mcp-memory DB에 4건 저장 (node #3990, #3997, #3999, #4002)
  - [orchestration] CHANGELOG, HOME.md, Living Docs 갱신 + 전체 push

현재 상태:
  portfolio master 브랜치 clean. mcp-memory v0.1.0 가동 중.

실패 기록 (삭제 금지):
  - (이번 세션 실패 없음)

다음 할 것:
  1. Key Decisions 레이아웃 선택 (V1투톤/V2아코디언/V3내러티브 중) → AiWorkflowSection 반영
  2. 모바일 반응형 확인 (375px)
  3. untracked 파일 정리: public/orch-graph.html, public/work/pmcc/diagram_1_new.png, reference/ref_obsidian.jpg
  4. monet-lab 44개 미커밋 정리

열린 결정:
  - Key Decisions 레이아웃: V1(투톤) / V2(아코디언) / V3(내러티브) 중 미결
  - Resume/Contact 탭 노출 전략
  - "이색적인 접합" 4번 카드 제거됨 — show vs tell 원칙 (향후 Work 섹션에서 보여주는 방식)

주의사항:
  - portfolio 브랜치: master (main 아님)
  - untracked 파일 3개 방치 중 — 별도 정리 필요
  - mcp-memory: settings.json에 MCP 등록됨, 26 노드타입, 33 관계타입
  - Direction B 확정: How I Operate(원칙) → HOW I AI(구현)이 하나의 이야기

[재작성] 세션 목표: portfolio How I Operate 전면 재작성 + mcp-memory 확인 | 남은 할 것: 1. Key Decisions 레이아웃 선택+반영 2. 모바일 반응형 375px 3. untracked 파일 정리 4. monet-lab 미커밋 정리
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

---

=== 이전 세션 (2026-03-04) ===

세션 목표: HOW I AI 섹션 Evolution 파트 전면 재작성 (글 + UI)

완료:
  - [portfolio] aiWorkflowData.ts — TimelineItem 타입 변경, TIMELINE 3주 질문 기반 재작성
  - [portfolio] AiWorkflowSection.tsx — Evolution 세로스택 UI + 시스템에 대하여 수정
  - 커밋 e0b1c3c, f95e390 → master push

실패 기록 (삭제 금지):
  - (없음)

=== 이전 세션 (2026-03-03~04) ===

세션 목표: QMD 설치 + D3.js 시각화 3종

실패 기록 (삭제 금지):
  - [시도] QMD BM25 한글 검색 → [실패] 한글 토크나이징 안됨 → [원인] BM25 기본 토크나이저가 한글 미지원
  - [시도] QMD query + LLM reranker → [실패] context 오류 → [원인] reranker가 LLM context 미포함 상태에서 호출
  - [시도] QMD search → [실패] 영어 쿼리만 부분 동작 → [원인] get만 정상, search/query는 한글 환경에서 불안정
