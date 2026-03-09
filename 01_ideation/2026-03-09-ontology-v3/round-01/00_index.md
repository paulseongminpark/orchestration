# Ontology v3 Ideation — Round 1

> 날짜: 2026-03-09
> 기반: v2.1 아이디에이션 80개 인사이트 (4세션×3라운드, 29결정)
> 맥락: v2.1 구현 완료 → v2.2.1 운영 → enrichment 배치 후 NDCG 0.724
> 트리거: "저장은 되는데 활용 구조가 없다" (Paul, S1 근본 문제)

---

## 핵심 질문

v2.1에서 **어떻게 저장/검색/승격하는가**를 구현했다.
이제 묻는 건: **왜 이 구조인가, 이것으로 충분한가, 다음은 뭔가**.

---

## 주제 (4개 → 1축)

```
에이전트의 본질 (목표 지향 자율성)
    ↓
온톨로지 재설계 (31개 타입 → 저장/인출 체계)
    ↓
A8 Discovery (co-retrieval, 인출 고도화)
    ↓
dispatch 컨텍스트화 (세션별 작업 분리)
```

### 01: 온톨로지 타입 진단 + 저장/인출 체계
- 31개 타입 운영 실태 (Workflow 532 vs Signal 4 — 불균형)
- write-only 탈피: "언제 꺼낼지"를 저장 시 설계
- recall() NDCG 0.724 달성했지만, 그건 벡터 유사도. 의미적 인출은 다른 문제.
- v2.1 결정 B1(분류→회상→조회→실행→학습)의 "회상" 단계 현황

### 02: 에이전트 자율성 → 시스템 반영
- 목표 이해 → 방법 선택 → 결과 평가 → 방향 수정
- 현재: Claude가 규칙을 읽고 따름. 목표 지향이 아닌 규칙 지향.
- 필요: 목표(Paul의 의도)를 기억하고 그에 맞게 행동을 선택하는 구조

### 03: A8 Discovery (co-retrieval 패턴)
- v2.1 결정 #22 recall mode (focus/auto/dmn) 기반 확장
- 함께 검색되는 노드 패턴 → shortcut 학습
- enrichment 배치 후 quality_score 분포 변화 활용

### 04: dispatch 컨텍스트화
- 현재: /dispatch → 모든 TODO/STATE 전체 출력
- 필요: 해당 세션 작업만 이어서
- 세션-작업 바인딩 구현 방향

---

## 오늘 세션 (S1-S4) 축적

| 세션 | 핵심 | ideation 반영 |
|------|------|---------------|
| S1 | Pre-flight Recall 확립, "write-only" 근본 문제 | 01의 출발점 |
| S1 | Memory-Merger 설계 (Detect→Present→Promote→Merge→Record) | 03과 연결 |
| S2 | Memory-Merger 구현 | 승격 파이프라인 운영 경험 |
| S3 | NDCG 개선 (goldset/typed vector/enrichment bias) | 01의 데이터 |
| S4 | Enrichment 배치 166개 → NDCG 0.724 | 01의 기반 |
| S4 | verify.py(hybrid_search)=0.390 vs recall()=0.724 | composite scoring 효과 증명 |

---

## v2.1 인사이트 참조 (핵심만)

| ID | 내용 | 이번 반영 |
|----|------|-----------|
| B1 | 분류→**회상**→조회→실행→학습 5단계 | 01: 회상 단계 설계 |
| C5 | "CLAUDE.md는 IF-ELSE 디렉토리" | 02: 규칙 지향 → 목표 지향 전환 |
| C9 | What-Context-Needed | 01: 저장 시 인출 맥락 설계 |
| #22 | recall mode (focus/auto/dmn) | 03: Discovery 확장 기반 |
| #23 | 그래프 캐싱 TTL 5분 | 03: co-retrieval 캐시 기반 |

---

## 파일 구조

| # | 파일 | 상태 |
|---|------|------|
| 00 | 이 인덱스 | 완료 |
| 01 | ontology-retrieval-design.md | 완료 |
| 02 | agent-autonomy.md | 완료 |
| 03 | discovery-pattern.md | 완료 |
| 04 | dispatch-context.md | 완료 |
