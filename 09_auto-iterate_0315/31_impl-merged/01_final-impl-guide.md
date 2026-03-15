# Implementation 최종 가이드

## 산출물 2개

### 1. validate_pipeline.py iterate PoC
- 위치: 09_auto-iterate_0315/30_impl-r1/
- test_pipeline_rules.py: 37 scenarios, F1=1.0
- program.md: 5회 iteration 로그
- validate_pipeline.py: bootstrap exempt 수정 4곳 (N17, I1, P1/F1, R2)

### 2. measure.py (시스템 건강 측정)
- 위치: 12_auto-iterate/src/measure.py
- 10개 체크: projects_match, agents, hooks, memory, living_docs, rules_sync, security, git, test_suites, external
- HEALTH.md 자동 생성
- 현재 score: 70/100

## 기술 결정
- Windows cp949 → PYTHONIOENCODING=utf-8 + encoding="utf-8" errors="replace"
- 경로: MSYS /c/dev ↔ C:/dev 양쪽 호환
- security: .venv/node_modules 제외
- living_docs: git 프로젝트만, 70% 이상 pass
- git_hygiene: 정보 제공만, 작업 중 미커밋은 fail 아님
