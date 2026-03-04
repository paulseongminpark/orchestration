# 세션 요약

> 최종 수정: 2026-03-04

> compressor 에이전트가 자동 업데이트합니다.

=== 컨텍스트 압축 요약 (최신) ===

세션 목표: portfolio GitHub Actions/Vercel 빌드 수정 + .worktrees 재편 + P1~P3 섹션 구조 변경

완료:
  - [portfolio] GitHub Actions + Vercel 빌드 실패 수정 (SYSTEM_ITEMS list 데드코드 TS 에러 3개 제거, commit b0c3555)
  - [portfolio] .worktrees 구조 재편: 03_claude(claude/portfolio 브랜치) 추가, codex/gemini master 동기화, _sandbox 정리
  - [portfolio] P1~P3 섹션 구조 변경 (claude/portfolio 브랜치):
      - 02·How I Think (4카드만)
      - 03·How I Build (HOW I AI + Ontology placeholder + Obsidian placeholder)
      - 04·Work / 05·Writing(TR통합) / 06·Contact
      - Nav 6항목 정리, TOC 업데이트
  - [portfolio] 미결 A~F 트래킹: docs/design/2026-03-04-portfolio-full-audit.md 섹션 6
  - [mcp-memory] checkpoint 6건 저장 (node #4087~#4092)
  - 세션 전환 체인 실행 완료

현재 상태:
  claude/portfolio 브랜치에서 6섹션 구조 구현 완료. PR 5174 검토 중. 미결 A~F 트래킹 진행 중.

실패 기록 (삭제 금지):
  - (이번 세션 실패 없음)

다음 할 것:
  1. PR 5174 검토 및 master 병합
  2. 미결 A~F 항목 순차 해결 (audit doc 섹션 6 기준)
  3. mcp-memory 커밋+push (미커밋 ~15개 파일)
  4. mcp-memory enrichment pipeline 첫 실행 테스트 (--dry-run)

열린 결정:
  - PR 5174 병합 타이밍 (검토 후)
  - 미결 A~F 우선순위 결정
  - mcp-memory F-19: phase_limit 변수 사용/제거
  - mcp-memory F-22: 프롬프트 언어 통일 정책

주의사항:
  - portfolio: claude/portfolio 브랜치 = P1~P3 구조 변경 작업 공간
  - portfolio: master 브랜치 = 안정 배포 브랜치
  - _sandbox 폴더 node_modules 잠금 문제 — Windows native cmd.exe 필요
  - mcp-memory 경로: /c/dev/01_projects/06_mcp-memory/
  - 미결 트래킹: /c/dev/01_projects/02_portfolio/docs/design/2026-03-04-portfolio-full-audit.md

[재작성] 세션 목표: portfolio 빌드 수정 + .worktrees 재편 + P1~P3 구조 변경 | 남은 할 것: 1. PR 5174 병합 2. 미결 A~F 해결 3. mcp-memory 커밋+push+첫 실행
=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===

---

=== 이전 세션 (2026-03-04) ===

세션 목표: portfolio 전체 섹션 구조 재편 설계 — 6섹션 구조 확정

완료:
  - [portfolio] 6섹션 확정, audit 416줄, 4카드 타이틀 변경, checkpoint #4057~#4059
  - 커밋 392e724 → master push

실패 기록 (삭제 금지):
  - (없음)

=== 이전 세션 (2026-03-04) ===

세션 목표: HOW I AI 섹션 Evolution 파트 전면 재작성 (글 + UI)

완료:
  - [portfolio] 3주 타임라인 + 질문 중심 UI + 인터뷰 원본 저장
  - 커밋 e0b1c3c, f95e390 → master push

실패 기록 (삭제 금지):
  - (없음)

=== 실패 기록 아카이브 (삭제 금지) ===
  - [시도] QMD BM25 한글 검색 → [실패] 한글 토크나이징 안됨 → [원인] BM25 기본 토크나이저가 한글 미지원
  - [시도] QMD query + LLM reranker → [실패] context 오류 → [원인] reranker가 LLM context 미포함 상태에서 호출
  - [시도] QMD search → [실패] 영어 쿼리만 부분 동작 → [원인] get만 정상, search/query는 한글 환경에서 불안정
