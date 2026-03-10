# R2-04: dispatch 컨텍스트화 — 구현 스펙

> R1: 방안 C+A 하이브리드 (impl-index 우선 → session-context fallback).
> Phase 0: patch foraging, recall mode(auto/focus/dmn).
> 이 문서: orch-state 에이전트 수정 구체안.

---

## 1. 현재 /dispatch 동작

```
/dispatch
  → orch-state 에이전트 실행
  → STATE.md 전체 읽기
  → TODO.md 전체 읽기 (있으면)
  → "다음 3개 액션 제안"
```

**문제**: 모든 프로젝트의 모든 항목이 나옴.

---

## 2. 수정된 /dispatch 로직

```
/dispatch
  → Step 1: 오늘 날짜의 impl-index 검색
     02_implementation/$(date +%Y-%m-%d)/0-impl-index*.md
     또는 가장 최근 impl-index (3일 이내)

  → Step 2 (impl-index 있음):
     "현재 상태" 섹션의 미결 항목 추출
     → 미결 항목만 기반으로 3개 액션 제안
     → 출력에 "📋 세션 컨텍스트: {impl-index 파일명}" 표시

  → Step 3 (impl-index 없음):
     .session-context.json 확인
     → project 필드로 STATE.md 필터
     → 해당 프로젝트 항목만 표시

  → Step 4 (둘 다 없음):
     기존 동작 (전체 STATE.md)
     → 출력에 "⚠️ 세션 컨텍스트 없음 — 전체 모드" 표시
```

---

## 3. orch-state 에이전트 프롬프트 수정

### 3-1. 현재 프롬프트 (요약)

```
STATE.md를 분석하고 다음 3개 액션을 제안하라.
TODO.md가 있으면 함께 참조.
```

### 3-2. 수정 프롬프트

```markdown
# orch-state 에이전트 (v2 — 세션 컨텍스트)

## 우선순위 1: 세션 컨텍스트 탐색
1. 오늘 날짜의 impl-index 검색:
   `02_implementation/YYYY-MM-DD/0-impl-index*.md`
   최근 3일 이내도 허용.
2. 있으면: "현재 상태" 섹션의 미결([ ]) 항목 추출.
3. 미결 항목 기반으로 다음 3개 액션 제안.

## 우선순위 2: 프로젝트 필터
impl-index 없으면:
1. 현재 작업 디렉토리에서 프로젝트 추론 (pwd 기반).
2. STATE.md에서 해당 프로젝트 섹션만 읽기.
3. 해당 프로젝트 항목 기반으로 3개 액션 제안.

## 우선순위 3: 전체 모드 (fallback)
둘 다 없으면:
1. STATE.md 전체 + TODO.md 전체 읽기.
2. 전체 기반 3개 액션 제안.
3. "⚠️ 세션 컨텍스트 없음" 경고 출력.

## 출력 형식
📋 컨텍스트: {소스 — impl-index / 프로젝트 필터 / 전체}
1. [P{1-3}] 액션 설명 — 근거
2. [P{1-3}] 액션 설명 — 근거
3. [P{1-3}] 액션 설명 — 근거
```

---

## 4. impl-index 자동 탐색 로직

### 4-1. 탐색 순서

```bash
# 1. 오늘
INDEX=$(find $ORCH/02_implementation/$(date +%Y-%m-%d) -name "0-impl-index*.md" 2>/dev/null | head -1)

# 2. 어제
if [ -z "$INDEX" ]; then
    YESTERDAY=$(date -d "yesterday" +%Y-%m-%d 2>/dev/null || date -v-1d +%Y-%m-%d)
    INDEX=$(find $ORCH/02_implementation/$YESTERDAY -name "0-impl-index*.md" 2>/dev/null | head -1)
fi

# 3. 최근 3일
if [ -z "$INDEX" ]; then
    INDEX=$(find $ORCH/02_implementation/ -name "0-impl-index*.md" -mtime -3 2>/dev/null | sort -r | head -1)
fi
```

### 4-2. session-start.sh 수정

```bash
# 기존 get_becoming 알림 뒤에 추가
if [ -n "$INDEX" ]; then
    echo "📋 이전 작업 인덱스: $(basename $INDEX)"
    echo "   /dispatch로 이어서 진행 가능"
fi
```

---

## 5. 세션ID 구분 (멀티 pane)

### 5-1. 문제

같은 날짜에 여러 pane에서 다른 작업을 할 때, 하나의 impl-index로는 구분 불가.

### 5-2. 방안: impl-index 파일명에 세션 번호

```
0-impl-index-0310.md        ← 기본 (첫 세션)
0-impl-index-0310-s2.md     ← 두 번째 세션
0-impl-index-0310-s3.md     ← 세 번째 세션
```

dispatch가 여러 개 발견하면:
1. 가장 최근 수정된 것 사용
2. 또는 "여러 세션 인덱스 발견 — 어떤 작업을 이어가시겠습니까?" 제시

### 5-3. 현실적 판단

현재 Paul의 패턴: 대부분 1 pane = 1 프로젝트. 날짜별 impl-index 하나면 충분.
멀티 pane 구분은 **P2** — 실제 문제 발생 시 구현.

---

## 6. Phase 0 반영

### 6-1. patch foraging (b-r1-4)

dispatch가 세션 컨텍스트를 줄 때, 해당 프로젝트에 집중하되 cross-project 연결도 표시.
```
📋 컨텍스트: 0-impl-index-0310.md (orchestration)
1. [P1] Phase 0 완료 → R2 심화 진행
2. [P1] goldset 2건 수정 (mcp-memory) ← cross-project
3. [P2] 21개 unenriched 노드 배치 (mcp-memory)
```

### 6-2. recall mode (b-r3-15)

dispatch 컨텍스트에 따라 recall mode 자동 선택:
- impl-index 있음 → `mode=focus` (현재 작업 집중)
- impl-index 없음 → `mode=auto` (넓은 탐색)

---

## 7. 구현 단계

```
Step 1: orch-state 프롬프트 수정 (에이전트 파일)
Step 2: session-start.sh에 impl-index 탐색 추가
Step 3: 테스트 — impl-index 있는/없는 상태에서 /dispatch 비교
Step 4: (P2) 멀티 pane 세션 구분
```

---

## 8. 미결

- [ ] orch-state 에이전트 파일 위치 확인 (STATE.md에서)
- [ ] 3일 이내 범위가 적절한지 (작업이 길어지면?)
- [ ] dispatch 출력에 "전체 모드 전환" 명령 추가할지
