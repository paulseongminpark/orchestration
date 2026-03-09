# Pre-flight Recall — 작업 전 기억 조회 규칙

> 원칙: mcp-memory에 저장한 결정/패턴을 작업 시작 전에 recall한다.
> 근거: B1 "분류→회상→조회→실행→학습" 5단계, C5 "IF-ELSE 디렉토리"
> 작성: 2026-03-09

---

## 왜 필요한가

mcp-memory에 2,800+ 노드가 있지만, Claude가 작업 시작 시 recall하지 않으면 과거 결정을 무시하게 된다.
session-start의 `get_context()`는 200토큰 고정 스냅샷일 뿐, **지금 하려는 작업에 맞는 쿼리가 아니다.**

---

## 트리거 — 언제 recall할 것인가

| 시점 | recall 쿼리 | 필수 여부 |
|------|------------|----------|
| TASK_CONTRACT 작성 | `recall(세션 목표 키워드)` | **필수** |
| 구현 시작 | `recall(구현 대상, project=프로젝트명)` | **필수** |
| 파일/폴더 생성 | `recall("폴더 규칙 날짜별 구조 네이밍")` | 필수 |
| ideation 시작 | `recall("ideation 표준 패턴 라운드")` | 필수 |
| Phase 전환 | `recall(Phase N 관련 키워드)` | 권장 |
| compact 전 | checkpoint 스킬 (저장 경로) | 필수 |

---

## 표준 쿼리 — 무엇을 recall할 것인가

### TASK_CONTRACT 작성 시
```python
recall(query="{세션 목표 키워드}", top_k=5)
recall(query="{프로젝트명} 결정", type_filter="Decision", project="{프로젝트명}", top_k=5)
```

### 구현 시작 시
```python
recall(query="구현 패턴 phase index 체크리스트 폴더", top_k=3)
recall(query="{구현 대상} 관련 패턴 버그 실패", project="{프로젝트명}", top_k=5)
```

### 파일/폴더 생성 시
```python
recall(query="폴더 규칙 날짜별 구조 Jeff Su 네이밍", top_k=3)
```

### ideation 시작 시
```python
recall(query="ideation implementation review 표준 패턴 라운드 규칙", top_k=3)
```

---

## recall 결과 반영 방법

1. recall 결과 중 **Decision, Pattern, Principle** 타입은 반드시 따른다
2. **Failure** 타입은 같은 실수를 피한다
3. 결과가 비어있으면 → 해당 영역에 대한 기존 결정이 없음 → 새로 결정 후 remember()
4. 결과가 현재 작업과 충돌하면 → 사용자에게 보고하고 결정 요청

---

## 워크플로우 통합

### B1 5단계 파이프라인
```
1. 분류 (Classify) — 작업 유형 판별
2. 회상 (Recall)   — mcp-memory recall() ← 이 문서의 핵심
3. 조회 (Query)    — 파일/코드 읽기
4. 실행 (Execute)  — 구현
5. 학습 (Learn)    — compressor Learn 단계
```

### Ideation→Implementation→Review 패턴
```
Ideation:
  R0: recall(프로젝트 관련 결정/패턴) ← Pre-flight
  R1: 소스 수집 + 분류
  R2: 역분석 + 게임체인저
  R3: 실행 순서

Implementation:
  I0: recall(구현 규칙, 폴더 패턴, 과거 실패) ← Pre-flight
  I1: impl-index 작성
  I2: Phase별 원자 태스크 분해 + 체크리스트
  ...

Review:
  V0: recall(리뷰 기준, 과거 실패 패턴) ← Pre-flight
  V1: CX (Codex 코드 리뷰)
  V2: GM (Gemini 영향 분석)
```

---

## 검증

- [ ] TASK_CONTRACT에 "Pre-flight Recall" 결과가 채워져 있는가
- [ ] recall 없이 구현을 시작하지 않았는가
- [ ] recall 결과의 Decision/Pattern을 작업에 반영했는가
- [ ] 새 결정을 내렸으면 remember()로 저장했는가

**recall 없이 구현 시작 = 규칙 위반. compressor Learn 단계에서 체크.**
