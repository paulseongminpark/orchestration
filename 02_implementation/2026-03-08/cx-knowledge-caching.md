`KNOWLEDGE.md`를 직접 쓰려고 했지만, 현재 세션이 `read-only` + `blocked by policy`라 파일 수정이 거부됐습니다.

추가할 내용은 아래와 같습니다 (파일: [KNOWLEDGE.md](C:\dev\01_projects\01_orchestration\KNOWLEDGE.md)):

```md
## 프롬프트 캐싱 (2026-03-08)

1. Order: Static system prompt + Tools -> CLAUDE.md -> Session context -> Messages.
2. Never add timestamps to system prompt.
3. Never shuffle tool order or add/remove tools mid-session.
4. Never change models mid-session.
5. Use <system-reminder> for updates instead of changing system prompt.
6. defer_loading: auto mode active (ENABLE_TOOL_SEARCH=auto), 58 tools -> 3-5K tokens.
7. Compaction uses identical system prompt+tools to preserve parent cache.
```