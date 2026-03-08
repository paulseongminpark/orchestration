# A. mcp-memory 강화

## A1. 복합 스코어링 (importance + recency + similarity)
- **소스**: @joaomoura (CrewAI v1.10.1), @jamesquint (Data Agent 전문)
- **현재**: recall = 3-Layer search (타입 태그 임베딩 + 키워드 부스트 0.03 + 다양성 60% 상한)
- **문제**: similarity만으로는 "6개월 전 아키텍처 결정"과 "어제 디버그 메모"가 같은 rank
- **적용**: `final_score = similarity×0.5 + decay_score×0.3 + keyword_boost×0.2`
- **구현**: nodes 테이블에 `importance` 컬럼 추가, promote_node 시 자동 증가, Layer(L0~L5) 자체가 importance 프록시

## A2. 5가지 인지 연산 (encode/consolidate/recall/extract/forget)
- **소스**: @joaomoura — CrewAI v1.10.1의 메모리 시스템
- **현재 상태**:
  - encode (remember) ✅
  - recall ✅
  - extract (enrichment) 부분적
  - consolidate ❌ — 중복+유사 노드 병합 없음
  - forget ❌ — 2,869 노드 전부 동일 가중치, 아무것도 잊히지 않음
- **적용**: consolidate = embedding 유사도 > 0.9인 동일 타입 노드 자동 병합. forget = half-life 감쇠

## A3. 메모리 충돌 감지
- **소스**: @joaomoura
- **예시**: "PostgreSQL 이전" 노드 → 나중에 "MySQL 이전" 노드 생성 → 구버전 자동 폐기
- **현재**: content_hash 기반 완전 중복만 잡음. 의미적 모순 감지 없음
- **구현 방안**: embedding 유사도 > 0.85 + 동일 타입 + 시간차 > 7일 → 충돌 후보 추출 → 최신 우선

## A4. Half-life 망각
- **소스**: @joaomoura, Karpathy "본질 vs 효율" (forget = mcp-memory 3대 연산 중 누락된 것)
- **공식**: `decay_score = importance × e^(-λ × days_since_access)`
- access 시 갱신 (recall로 읽히면 수명 연장), recall 시 decay 반영
- **효과**: 2,869 노드 중 실제로 쓸모없는 노드의 rank가 자연 감소 → recall 품질 향상

## A5. Quirk Store (사용자 수정 → 영구 지식)
- **소스**: @jamesquint 전문 (Data Agent)
- **구체적 구현 (jamesquint)**:
  - 사용자가 에이전트를 교정하면 "quirk"으로 추출
  - pgvector + pg_textsearch(BM25) + reciprocal-rank fusion으로 저장
  - 새 질문마다 hybrid retrieval → 상위 matches를 context agent brief와 함께 주입
  - "이것이 institutional knowledge base — 한 사람의 머릿속에만 있던 것"
- **Pal 구현** (소스코드 확인):
  - `Correction:` 접두사로 `pal_learnings`에 저장
  - **Correction은 항상 최우선** — 다른 학습과 충돌 시 Correction 우선
- **적용**: mcp-memory에 `type: "correction"` 노드 타입 추가. recall 시 관련 correction을 **항상** top-inject

## A6. Reviewed-item Multiplier
- **소스**: @jamesquint 전문
- **원문**: "A reviewed-item multiplier ensures human-approved knowledge ranks higher than stuff the agent learned on its own"
- **적용**: promote_node된 노드에 1.5x multiplier in recall scoring. 현재 promote_node가 Layer를 올리지만 recall 점수에 직접 반영 안 됨

## A7. Self-Scoring Loop (3차원 자가 채점)
- **소스**: @jamesquint 전문
- **3차원**: 구조적 정확성 + 실행 신뢰성 + 컨텍스트 정합성
- **context-gap brief**: 하위질문별 evidence 체크 → gap이 남으면 targeted prompt로 재시도 or context enrichment 재실행
- **Haiku fallback**: Haiku로 semantic/context 체크, 불가 시 deterministic fallback
- **적용**: ai-synthesizer verify barrier에 3차원 채점 추가

## A8. Knowledge Map / Discovery 패턴 (발견 경로 저장)
- **소스**: Pal 소스코드 (agno-agi/pal)
- **Discovery 패턴**: 크로스소스 검색 성공 시 `Discovery:` 엔트리를 `pal_knowledge`에 저장 → 다음 동일 쿼리 시 광범위 검색 없이 직행. **캐시/학습 하이브리드**
- **메타데이터만 임베딩**: context/ 파일 콘텐츠를 임베딩하지 않음. 경로+intent 태그만 벡터DB에 저장. 파일 수정 시 재인덱싱 불필요
- **적용**: recall 히스토리에서 "자주 같이 검색되는 노드군" 감지 → co-retrieval shortcut 엣지 자동 생성

## A9. Memory-Merger 패턴 (성숙한 기억 → 규칙 승격)
- **소스**: awesome-copilot memory-merger 스킬
- **워크플로우**: domain-memory.md 읽기 → 성숙한 항목 식별 → 사용자 승인 → quality bar 10/10 → domain.instructions.md에 병합 → memory에서 제거
- **Quality Bar**: (1) zero knowledge loss (2) minimal redundancy (3) maximum scannability
- **적용**: Signal→Pattern 승격 시 자동으로 관련 instruction 갱신. `applyTo` 패턴 병합

## A10. 원자 메모리 추출 (Atomic Memory Extraction)
- **소스**: @joaomoura
- **개념**: 500자 요약을 개별 사실로 분해 → 각각 독립 노드화
- **현재**: remember()는 하나의 노드로 저장
- **적용**: remember() 시 자동으로 atomic facts 추출 후 개별 노드 생성. enrichment보다 저장 시점에서 분해

## Hybrid Search 튜닝 (jamesquint 전문에서 추가)
- **Collection weights**: metrics vs quirks 밸런스 조정
- **Reviewed-item multiplier**: 인간 승인 > 자동 학습
- **Reciprocal-rank fusion**: vector + BM25 → 단일 순위 (현재 mcp-memory v2.2.0에서 사용 중)
- **Fixed context budget**: recall 결과 수 제한 — 전체 knowledge store를 프롬프트에 넣지 말 것
