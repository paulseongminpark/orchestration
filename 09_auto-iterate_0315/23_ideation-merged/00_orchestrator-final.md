# Ideation 최종 — auto-iterate 전체 설계

## 핵심 결정
1. **측정만 자동, 수정은 세션에서** — Codex/Gemini 무인 수정 금지
2. **measure.py = 순수 스크립트** — AI 없음, 참/거짓만 판정
3. **HEALTH.md = 체온계** — session-start에서 한 줄 표시
4. **테스트는 실제 경험에서** — 합성 케이스 아닌 실사용 버그에서 추가
5. **autoresearch에서 가져온 것** — 단일 메트릭, results.tsv, program.md, keep/discard
6. **가져오지 않은 것** — NEVER STOP, 무인 수정, 밤새 100회

## 11 섹터 × 3 계층
- 계층 A: 변경 시 즉시 (hook/rule 수정 후 test suite)
- 계층 B: 매일 (cron, security/git/external)
- 계층 C: 주간 (drift, memory, living docs)

## 구현 결과
- measure.py v0.1: 10개 체크, score 70/100
- test_pipeline_rules.py: 37 scenarios, F1=1.0
- validate_pipeline.py: bootstrap exempt 4곳 수정
- 12_auto-iterate 프로젝트 생성
