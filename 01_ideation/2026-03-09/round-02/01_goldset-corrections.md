# Goldset q051-q075 수정 제안 — Round 2

> 날짜: 2026-03-09
> 목적: ZERO 9건의 근본 원인별 수정 제안. Paul 검증 필요.

---

## 1. goldset 오류 (relevant_ids 잘못 지정) — 3건

### q065 (ZERO → 수정 후 예상 개선)
- **현재 쿼리**: "E14 전체 배치가 100% 실패했던 직접 원인과 거기서 얻은 교훈은 뭐였지?"
- **현재 relevant_ids**: [4243] — "오케스트레이터 통합 중 범용 프롬프트 사고" (내용 불일치)
- **수정 제안**: relevant_ids=[4173], also_relevant=[4132]
  - #4173 [Insight]: "E14 미실행 근본원인 파악" (rank 5에서 발견)
  - #4132 [Pattern]: "OpenAI 무료 할당 소진으로 엔리치먼트 건너뜀"

### q069 (ZERO → 수정 후 예상 개선)
- **현재 쿼리**: "Subagent-Driven Development로 UI Lab 07부터 10까지 구현한 실험 기록은 뭐였지?"
- **현재 relevant_ids**: [189] — "Codex/Gemini 3개월 검증" (내용 불일치)
- **수정 제안**: relevant_ids=[942, 3481], also_relevant=[3398]
  - #942 [Experiment]: "monet-lab UI 실험 환경 구축" (rank 9)
  - #3481 [Decision]: "Subagent-Driven vs 직접 실행 선택" (rank 10)
  - #3398 [Pattern]: "monet-lab→portfolio 이식 파이프라인"

### q074 (ZERO → 수정 후 예상 개선)
- **현재 쿼리**: "Auto Memory 개선과 Cross-CLI .ctx 정리, Playwright MCP 활성화를 목표로 한 세션 목표는 뭐였지?"
- **현재 relevant_ids**: [4045, 4231] — 전혀 다른 목표 (온톨로지, 수학 모델)
- **수정 제안**: relevant_ids=[1040], also_relevant=[1039, 175]
  - #1040 [Decision]: "Cross-CLI 메모 폐기, rulesync 축소, Playwright MCP 활성화" (rank 9, 정확 일치)
  - #1039 [Workflow]: "메모리 시스템 정리, 세션 스크립트 개선, CLI 통합"
  - #175 [SystemVersion]: "크로스 플랫폼 공유 메모리 시스템"

---

## 2. vocabulary mismatch (쿼리 어휘 ≠ 노드 어휘) — 3건

### q057: "orchestration" vs "오케스트레이션"
- **현재 쿼리**: "orchestration 프로젝트 구조와 핵심 경로를 정리한 프로젝트 개요는 뭐였지?"
- **노드 #102**: "AI 오케스트레이션 시스템을 중심으로 하는 볼트의 핵심 프로젝트 구조"
- **수정 제안**: 쿼리 → "오케스트레이션 프로젝트 구조와 핵심 경로 프로젝트 개요"
  - 또는: #102 summary에 "orchestration" alias 추가 (코드 측)

### q060: "dev 볼트" vs "Obsidian 볼트"
- **현재 쿼리**: "dev 볼트 구조를 계층적으로 설명한 프레임워크 문서는 뭐였지?"
- **노드 #36**: "Obsidian 볼트의 계층적 구조 설계"
- **수정 제안**: 쿼리 → "Obsidian dev 볼트 구조 계층적 프레임워크"

### q061: 구체적 세션 사건 vs 일반적 볼트 설명
- **현재 쿼리**: "portfolio에서 Obsidian 섹션 v4.0을 재작성하며 Hook, Architecture..."
- **노드 #98/#27**: 볼트 구조 일반 서술
- **판단**: 쿼리가 너무 구체적 (특정 세션의 특정 작업). 이 수준의 구체성은 검색 한계.
- **수정 제안**: 쿼리 유지, relevant_ids 재검토 (Paul 판단 필요)

---

## 3. 검색 실패 (쿼리 ≈ summary인데 못 찾음) — 2건

### q059: 거의 동일한 summary인데 rank 20 밖
- **쿼리**: "컨텍스트 비대화를 막기 위해 병렬 독립 세션과 index 파일을 쓰는 패턴은 뭐였지?"
- **#4235**: "컨텍스트 비대화를 막기 위해 독립 세션을 병렬로 운영하고, 각 세션이 한 줄 인덱스 파일을 유지..."
- **실제 결과**: #4235 top-20 안에 없음! #4119는 rank 20 (score 0.3532)
- **원인 추정**: Pattern 타입(L2)이 Principle 타입(L1) 대비 vector space에서 밀림. Principle 노드가 압도적.
- **해결**: typed vector 채널에서 Pattern 타입 부스트 or 쿼리에 "패턴" 키워드로 type hint 강화

### q073: 내용 그대로인데 못 찾음
- **쿼리**: "리뷰 아키텍처를 3 CLI x 3 Rounds x 9 Categories로 설계한 결정은 뭐였지?"
- **#4257**: "v2.1 리뷰 체계는 3개 CLI, 3개 라운드, 9개 카테고리를 조합한 매트릭스"
- **실제 결과**: #4257 top-20 안에 없음
- **원인 추정**: "3 CLI x 3 Rounds x 9 Categories" (영+숫자+기호) vs "3개 CLI, 3개 라운드, 9개 카테고리" (한국어). trigram FTS와 vector 모두 어휘 차이에 약함.
- **해결**: FTS에서 숫자+단위 정규화 ("3 CLI" ↔ "3개 CLI") 또는 goldset 쿼리 정규화

---

## 4. 예상 영향

| 수정 유형 | 대상 | 예상 NDCG@5 변화 |
|----------|------|-----------------|
| goldset 수정 | q065, q069, q074 (3건) | ZERO → 0.3-0.5 (hit_rate +12%) |
| 쿼리 정규화 | q057, q060 (2건) | LOW → 0.4-0.6 |
| 검색 개선 | q059, q073 (2건) | 코드 수정 필요, 별도 구현 |
| 나머지 | q061 (1건) | 쿼리 너무 구체적, 한계 |

goldset 수정 3건 + 쿼리 정규화 2건만으로 q051-q075 NDCG@5 **0.227 → ~0.30-0.35** 예상.

---

## 5. enrichment bias 발견 (2026-03-09 추가)

### 근본 원인
q059, q073은 goldset 오류가 아닌 **enrichment bias** 버그:
- #4235 (q059): 벡터 rank 1, FTS rank 1, RRF rank 1 → 그런데 최종 결과 top-50 밖!
- 원인: enriched Principle 노드(tier=0, qs=0.92)의 보너스 합계 0.432 >> RRF 1위 0.105

| 구성요소 | enriched (#222) | unenriched (#4235) |
|---------|-----------------|-------------------|
| RRF score | ~0.030 | 0.105 |
| enrichment bonus | 0.282 | 0.000 |
| tier bonus | 0.150 | 0.000 |
| **합계** | **0.462** | **0.105** |

### 실험 결과
cap 적용 시: q051-q075 +0.163 but q001-q025 -0.156, q026-q050 -0.168 → 트레이드오프

### 해결 방향
**근본 해결**: 193개 unenriched 노드에 enrichment 배치 실행 (OpenAI API 필요)
- 실행 시 `scripts/enrich/node_enricher.py` 사용
- UNENRICHED_DEFAULT_QS 상수를 참조값으로 추가해둠
