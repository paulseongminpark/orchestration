---
name: sync
description: STATE.md 갱신 + LOG append + git commit + push
user-invocable: true
allowed-tools: Read, Edit, Bash
---

## Steps

0. (선택) /verify-project-rules 실행 (경고만, 차단 안 함)

1. context/STATE.md 읽기

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
   LOG="context/logs/$(date '+%Y-%m-%d').md"
   printf "위 내용" >> "$LOG"
   ```

   **중요:** 형식만 echo하지 말고 실제 이번 세션 내용을 채워서 기록.

5. git add context/ && git commit -m "[orchestration] STATE+LOG 갱신" && git push

## LOG 규칙
- 읽기 절대 금지 (토큰 보호). echo append만.
- 태그: [orchestration], [portfolio], [cowork]
- 결정: [Decision], [Pending], [Discarded]
- 시간: 시스템 시간 $(date '+%Y-%m-%d %H:%M')

## Output
DONE: STATE+LOG 갱신 + push 완료
URL: https://paulseongminpark.github.io/orchestration/context/STATE.md
