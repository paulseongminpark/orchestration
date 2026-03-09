# 04: dispatch 컨텍스트화 — 세션별 작업 분리

> Paul: "dispatch 하면 해당 세션에서 하던것만 이어서 하도록 하고 싶은데"
> 현재: /dispatch → 전체 TODO/STATE → 모든 항목 나열
> 필요: 세션-작업 바인딩

---

## 1. 현재 /dispatch 동작

```
/dispatch
  → orch-state 에이전트 실행
  → STATE.md 전체 읽기
  → TODO.md 전체 읽기
  → 다음 3개 액션 제안
```

**문제**: 모든 프로젝트의 모든 항목이 나옴. orchestration 작업 중인데 portfolio TODO가 보임.

---

## 2. 세션 컨텍스트의 정의

"세션"이란:
- tmux pane 하나 = Claude Code 인스턴스 하나
- 특정 프로젝트/작업에 집중
- compact 경계까지가 하나의 세션 단위

세션 컨텍스트가 가져야 할 정보:
```
session_context = {
    "session_id": "0309-s4",
    "project": "mcp-memory",
    "track": "NDCG 개선",
    "completed": ["enrichment 배치", "NDCG 측정"],
    "pending": ["verify.py 차이", "Phase 5 A8"],
    "active_files": ["config.py", "hybrid.py", "goldset.yaml"],
}
```

---

## 3. 구현 방안

### 방안 A: 세션 컨텍스트 파일 (가장 단순)

```
~/.claude/projects/C--dev/.session-context.json
```

- /dispatch 시작 시 이 파일 읽기
- 내용이 있으면 해당 세션 작업만 표시
- compact/session-end 시 갱신
- 세션 시작 시 이전 컨텍스트에서 복원

**장점**: 구현 1시간, 파일 하나
**단점**: tmux pane별로 다른 파일이 필요 (pane 구분 못함)

### 방안 B: mcp-memory 세션 태그

```python
remember("세션 0309-s4: NDCG 개선 → enrichment 배치 완료",
         type="Workflow", tags="session:0309-s4, project:mcp-memory")

# dispatch 시
recall("session:current", project="mcp-memory")
```

- save_session()이 이미 세션 정보 저장
- dispatch 시 get_context(project=현재프로젝트)로 필터

**장점**: 기존 인프라 활용, 크로스세션 연결 가능
**단점**: recall 품질에 의존, 토큰 비용

### 방안 C: impl-index 기반 (현재 패턴 활용)

현재 `0-impl-index-0309.md`가 이미 세션 상태를 추적:
```markdown
## 현재 상태 (compact 후 이 섹션 먼저 확인)
완료: [x] Track A, [x] Track B, [x] Track C
미결: [ ] enrichment 배치, [ ] Phase 5
```

- /dispatch가 현재 날짜의 impl-index를 찾아서 읽기
- impl-index의 "미결" 항목만 표시
- 없으면 전체 STATE.md fallback

**장점**: 이미 존재하는 패턴, 추가 인프라 불필요
**단점**: impl-index 작성 규율 필요

### 선택: 방안 C + A 하이브리드

1. impl-index가 있으면 → 그것 기반으로 dispatch (C)
2. 없으면 → .session-context.json fallback (A)
3. 둘 다 없으면 → 전체 STATE.md (현재 동작)

---

## 4. 구현 설계

### 4-1. orch-state 에이전트 수정

```markdown
# 수정된 /dispatch 로직

1. 현재 날짜의 impl-index 검색
   → 02_implementation/2026-MM-DD/0-impl-index*.md
2. 있으면:
   - "현재 상태" 섹션의 미결 항목 추출
   - 해당 항목만 기반으로 3개 액션 제안
3. 없으면:
   - .session-context.json 확인
   - project 필드로 STATE.md 필터
4. 둘 다 없으면:
   - 기존 동작 (전체 STATE.md + TODO.md)
```

### 4-2. session-start에서 컨텍스트 복원

```bash
# session-start.sh 수정
# 1. 오늘 날짜의 impl-index 존재 확인
INDEX=$(find $ORCH/02_implementation/$(date +%Y-%m-%d) -name "0-impl-index*.md" 2>/dev/null | head -1)
if [ -n "$INDEX" ]; then
    echo "📋 이전 작업 인덱스: $INDEX"
    echo "   /dispatch로 이어서 진행 가능"
fi
```

### 4-3. compact/session-end에서 저장

이미 work-log + impl-index 작성이 compact 절차에 포함됨 (common-mistakes.md).
→ 추가 구현 불필요. 기존 규칙 준수만으로 동작.

---

## 5. 02와의 연결 (에이전트 자율성)

dispatch 컨텍스트화는 L2(맥락 참조) 강화:
- 세션 맥락을 자동으로 로드 → 사용자가 "이어서 해" 한마디면 동작
- 이전: "무슨 작업이었는지 알려줘" 필요
- 이후: impl-index 자동 발견 → 미결 항목 제시 → 즉시 작업

---

## 6. 미결

- [ ] tmux pane별 구분: 같은 날짜에 여러 세션이면? (impl-index 파일명에 세션 번호)
- [ ] 다른 날짜 작업 이어가기: 0308에서 시작한 작업을 0309에서 이어가려면?
- [ ] dispatch 출력 포맷: 전체 vs 세션 모드 전환 UI
