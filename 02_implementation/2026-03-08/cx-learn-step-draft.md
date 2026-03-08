# Learn 단계 — compressor agent.md 추가분

> `.agents/compressor/agent.md`의 기존 9단계 후에 추가

```markdown
## 10. Learn 단계

세션에서 발견한 것을 3줄로 요약하라:

1. **Discovery**: 새로 알게 된 것 (패턴, 도구, 방법)
2. **Lesson**: 실패에서 배운 것 (버그, 잘못된 가정, 시간 낭비)
3. **Improvement**: 다음에 다르게 할 것 (프로세스, 규칙, 습관)

이 3줄을 아래 두 곳에 저장:
- mcp-memory: `remember(content=3줄, type="Insight", tags="session-learning,{프로젝트}")`
- lessons.md: `/c/dev/01_projects/01_orchestration/lessons.md`에 append
  - 형식: `- [{날짜}] {Lesson 1줄}`
  - 20개 초과 시 가장 오래된 것 제거

Learn 단계를 건너뛰지 마라. 배운 것이 없으면 "이 세션에서 특별히 배운 것 없음"이라고 기록.
```
