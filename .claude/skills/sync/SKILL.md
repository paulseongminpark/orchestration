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
4. LOG append (읽기 금지, echo만):
   ```
   LOG="context/logs/$(date '+%Y-%m-%d').md"
   printf "\n## $(date '+%Y-%m-%d %H:%M') [orchestration] Claude Code\n- 작업 요약\n- [Decision|Pending|Discarded] 결정 내용\n" >> "$LOG"
   ```
5. git add context/ && git commit -m "[orchestration] STATE+LOG 갱신" && git push

## LOG 규칙
- 읽기 절대 금지 (토큰 보호). echo append만.
- 태그: [orchestration], [portfolio], [cowork]
- 결정: [Decision], [Pending], [Discarded]
- 시간: 시스템 시간 $(date '+%Y-%m-%d %H:%M')

## Output
DONE: STATE+LOG 갱신 + push 완료
URL: https://paulseongminpark.github.io/orchestration/context/STATE.md
