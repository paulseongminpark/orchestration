# Warp Pane 2 프롬프트: Correction 노드 타입 (A5)

> 이 프롬프트를 Warp의 Claude Opus 1M 세션에 붙여넣기

---

```
mcp-memory에 Correction 노드 타입을 추가하고, recall 시 top-inject하는 작업이다.

## 현재 상태
- mcp-memory v2.2.1, 경로: /c/dev/01_projects/06_mcp-memory/
- 50개 노드 타입 존재 (config.py TYPE_DEFS)
- recall()은 RRF 기반 3-Layer search
- 사용자 교정 기록 메커니즘 없음

## 배경
사용자(Paul)가 에이전트를 교정하면 그 교정이 영구 지식이 되어야 한다.
예: "PostgreSQL 아니라 MySQL이야" → 다음에 DB 관련 recall 시 이 교정이 최우선 노출.

Pal(agno-agi/pal)에서의 구현:
- `Correction:` 접두사로 `pal_learnings`에 저장
- "Correction은 항상 최우선 — 다른 학습과 충돌 시 Correction 우선"

jamesquint(Data Agent)에서의 구현:
- "quirk"으로 추출, pgvector + BM25 hybrid retrieval
- 새 질문마다 관련 quirk를 context에 항상 주입

## 구현할 것

### 1. Correction 노드 타입 추가
- config.py의 TYPE_DEFS에 `Correction` 타입 추가
- Layer: L3 (Principle 수준 — 교정은 높은 우선순위)
- remember() 시 type="Correction"으로 저장 가능

### 2. recall() Top-inject
recall() 결과 반환 시:
1. 기존 RRF 검색 수행
2. 별도로 Correction 타입 노드 중 쿼리와 관련된 것 검색
3. 관련 Correction을 결과 **맨 앞에** 삽입 (top-inject)
4. 일반 결과와 Correction이 겹치면 중복 제거

```python
# 의사 코드
def recall(query, ...):
    # 1. 기존 검색
    results = existing_rrf_search(query, ...)

    # 2. Correction 검색 (vector similarity > 0.5)
    corrections = search_by_type(query, type="Correction", threshold=0.5)

    # 3. Top-inject (중복 제거)
    result_ids = {r.id for r in results}
    top = [c for c in corrections if c.id not in result_ids]

    return top + results  # Corrections first
```

### 3. 자동 교정 감지 (선택)
사용자가 "아니야, X가 아니라 Y야" 패턴으로 말하면 자동으로 Correction 노드 생성.
이건 복잡하니까 일단 수동 remember(type="Correction")만 구현.
자동 감지는 Phase 3에서.

## 제약 조건
- 기존 163 테스트 깨지면 안 됨
- recall() 반환 형식 변경 없음 (기존 호출 코드 호환)
- Correction 노드가 0개여도 기존 동작 동일

## 작업 순서
1. config.py TYPE_DEFS에 Correction 추가
2. recall()에 Correction top-inject 로직 추가
3. 테스트: Correction 노드 생성 → recall → 최상위 노출 확인
4. 기존 테스트 실행 (163개 PASS 확인)

## 테스트 시나리오
```python
# Correction 생성
remember("Paul은 PostgreSQL이 아닌 MySQL을 사용한다. 이전 기록 교정.", type="Correction")

# recall 시 최상위 노출
results = recall("Paul의 데이터베이스")
assert results[0].type == "Correction"
assert "MySQL" in results[0].content
```

소스코드 수정 금지 대상: 없음 (구현 세션). git commit 자유.
```
