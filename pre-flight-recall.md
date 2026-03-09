# Pre-flight Recall — 작업 전 기억 조회

> 상세 규칙은 mcp-memory에 저장돼 있다. 이 파일은 트리거만.
> recall("pre-flight-recall") → #4327-#4339

---

## 규칙 (3줄)

1. **작업 시작 전 recall() 필수.** recall 없이 구현 = 규칙 위반.
2. **recall 결과의 Decision/Pattern/Principle은 반드시 따른다.**
3. **새 결정을 내리면 remember()로 저장한다.**

---

## 트리거 시점

| 시점 | recall 쿼리 |
|------|------------|
| TASK_CONTRACT | `recall(세션 목표 키워드)` |
| 구현 시작 | `recall(대상, project=프로젝트명)` |
| 폴더 생성 | `recall("폴더 규칙 네이밍")` |
| ideation | `recall("ideation 표준 패턴")` |
| compact 전 | index 갱신 + save_session + work-log |

상세 쿼리 템플릿 → `recall("pre-flight-recall standard-query")`

---

## mcp-memory 카테고리

| 카테고리 태그 | 내용 | 관련 노드 |
|--------------|------|----------|
| `category:workflow` | 5단계 파이프라인, 작업 흐름, 완료 체크리스트 | #4337, #4338, #4339 |
| `pre-flight-recall` | recall 규칙, 표준 쿼리 | #4328, #4337 |
| `ideation` | R0→R1→R2→R3 패턴 | #4327 |
| `folder-rule` | 날짜별 폴더, Jeff Su, 네이밍 | #4329 |
| `compact` | 정보소실 0, 영구 저장소 3곳 | #4330, #4336 |
| `index` | 범용 index 규칙, 필수 요소 | #4336 |
