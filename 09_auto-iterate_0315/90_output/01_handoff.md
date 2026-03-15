# Handoff — 다음 작업자를 위한 가이드

## 즉시 할 일
1. CLAUDE.md에 12_auto-iterate 프로젝트 등록
2. session-start.sh에 HEALTH.md score 표시 추가
3. security 4건 대응 (02_programs 자격증명)

## 이후 할 일
4. cron 설정: 매일 `python 12_auto-iterate/src/measure.py`
5. post-commit hook: 변경 파일 관련 test suite 자동 실행
6. 체크 항목 확장 (Obsidian 링크, agent 구조 검증 등)
7. 새 버그 발견 시 → test case 추가 → iterate 세션

## 하지 않을 일
- 무인 코드 수정 (Codex/Gemini iterate 금지)
- 합성 테스트 케이스 생성
- 인터페이스 변경 (이름, 경로, 구조)
