# 확정 결정

1. auto-iterate = 측정 자동 + 수정은 세션(Claude+사용자)
2. Opus 소비 0. Codex/Gemini는 분석만.
3. measure.py: AI 없음, 스크립트만, 참/거짓 판정
4. HEALTH.md: session-start에서 1줄 표시
5. 테스트: 실제 경험에서만 추가 (합성 금지)
6. 인터페이스 불변: 이름/구조/경로 안 바꿈
7. 트리거: 이벤트 기반(코드 변경 시) + 매일 health check + 주간 deep scan
8. 12_auto-iterate: 독립 프로젝트로 분리
9. results.tsv: Karpathy 형식 유지 (5컬럼 TSV)
10. program.md: iterate 세션용 지시서 (세션에서만 사용)
