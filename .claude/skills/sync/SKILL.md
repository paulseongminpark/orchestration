---
name: sync
description: STATE.md 갱신 + LOG append + git commit + push (sync-all 통합)
user-invocable: true
disable-model-invocation: true
model: haiku
---

## 모드

### `/sync` (기본 — 현재 프로젝트)

0. (선택) /verify 실행 (경고만, 차단 안 함)

1. STATE.md 읽기

2. 이번 세션 작업 반영 (완료/다음/막힌것 갱신)

3. 날짜 업데이트

4. **세션 요약 생성 후 LOG append**

   현재 대화를 분석하여 아래 형식으로 LOG에 기록:

   ```
   ## YYYY-MM-DD HH:MM [orchestration] Claude Code

   ### 작업 요약
   - 완료한 작업 1
   - 완료한 작업 2

   ### 결정 사항
   - [Decision] 결정 내용 (이유)
   - [Pending] 미결정 항목

   ### 다음 세션 시작점
   - 다음에 이어서 할 것
   - 주의사항
   ```

   bash append:
   ```bash
   LOG="_history/logs/$(date '+%Y-%m-%d').md"
   printf "위 내용" >> "$LOG"
   ```

   **중요:** 형식만 echo하지 말고 실제 이번 세션 내용을 채워서 기록.

5. git add STATE.md _history/logs/ && git commit -m "[orchestration] STATE+LOG 갱신" && git push

### `/sync all` (모든 프로젝트 — sync-all 통합)

1. **각 프로젝트별로**:
   - orchestration (main), portfolio (master), dev-vault (main) 순서
   - 변경된 파일 확인 (git status)
   - STATE.md 있으면 읽기 → 최근 작업 반영
   - 적절한 커밋 메시지: "[project] 한줄 설명"
   - git add + commit + push

2. **메모리 동기화**:
   ```bash
   bash /c/Users/pauls/.claude/scripts/sync-memory.sh
   ```
   - pending.md → MEMORY.md 4기준 검증 후 반영
   - 에이전트 학습 패턴 검증 (선택)

3. **보고**:
   ```
   DONE:
   - orchestration: [커밋 메시지]
   - portfolio: [커밋 메시지]
   - dev-vault: [커밋 메시지]
   - memory: [채택 N개 / 보류 N개 / 삭제 N개]
   ```

## LOG 규칙
- 읽기 절대 금지 (토큰 보호). echo append만.
- 태그: [orchestration], [portfolio], [cowork]
- 결정: [Decision], [Pending], [Discarded]
- 시간: 시스템 시간 $(date '+%Y-%m-%d %H:%M')

## 주의사항
- orchestration: main 브랜치
- portfolio: master 브랜치
- dev-vault (C:\dev): main 브랜치
- force push 절대 금지

## Output
DONE: STATE+LOG 갱신 + push 완료
URL: https://paulseongminpark.github.io/orchestration/STATE.md
