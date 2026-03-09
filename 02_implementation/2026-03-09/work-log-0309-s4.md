# Work Log — 2026-03-09 세션 4

> 테마: Enrichment 배치 + Ontology v3 Ideation R1
> 세션: Main (WezTerm, Opus 4.6)
> 이전: S3 (NDCG ideation + goldset/typed vector, work-log-0309-s3.md)

---

## 1. Enrichment 배치 실행

### 실행
- API: OpenAI (API_PROVIDER=openai), 모델: gpt-5-mini (소형 풀)
- .env에 OPENAI_API_KEY + ANTHROPIC_API_KEY 모두 설정됨
- 기본 API_PROVIDER=anthropic → openai로 환경변수 오버라이드
- 첫 시도: cp949 인코딩 에러 → PYTHONIOENCODING=utf-8로 해결
- Phase 1만 실행 (--phase 1)

### 결과
- 노드: 166/166 enriched (err=0)
- 토큰: 1,438,532 / 2,250,000 (63.9% 소형 풀)
- API calls: 504
- 후속: E7(embedding_text) 236/2963, E13(cross-domain) +93 edges
- 남은 unenriched: 21개 (일부는 첫 cp949 실행에서 부분 처리)

### NDCG 결과
- **recall() 기준**: 0.475 → 0.724 (+52%)
  - q001-q025: 0.609 → 0.860 (+0.251)
  - q026-q050: 0.554 → 0.829 (+0.275)
  - q051-q075: 0.258 → 0.485 (+0.227)
- **verify.py 기준**: 0.390 (hybrid_search 직접 호출, composite scoring 미적용)
- q059/q073 ZERO 해소 (enrichment bias 해결)
- 새 ZERO 10건: q020,q025,q028,q054,q057,q060,q061,q063,q068,q069

### verify.py vs recall() 차이 원인
- verify.py: `checks/search_quality.py` → `hybrid_search()` 직접 호출 (raw RRF)
- recall(): `tools/recall.py` → composite scoring + BCM/UCB 보너스
- composite scoring이 +85% 개선 효과

---

## 2. OpenAI 무료 토큰 기록

OpenAI Data Controls > Sharing 프로그램:
- 대형 모델: 250K tokens/일 (gpt-5.4, gpt-5.2, gpt-4.1, o1, o3 등)
- 소형 모델: 2.5M tokens/일 (gpt-5-mini, o3-mini, o4-mini 등)
- Weekly evals: 7회/주
- mcp-memory TOKEN_BUDGETS (large 225K / small 2.25M)이 한도 내 설정
- 저장: mcp-memory #4376 + MEMORY.md

---

## 3. Codex 위임 실패

- verify.py 차이 분석을 Codex에 위임 시도
- Windows sandbox refresh 에러 + 쓰기 경로 거부
- 직접 분석으로 전환 → 5분 내 원인 확인

---

## 4. Ontology v3 Ideation R1

80개 인사이트(v2.1 아이디에이션 64파일) + 오늘 S1-S4 작업 + Paul의 4개 주제를 통합.

### 파일
- `01_ideation/2026-03-09-ontology-v3/round-01/00_index.md`
- `01_ideation/2026-03-09-ontology-v3/round-01/01_ontology-retrieval-design.md`
- `01_ideation/2026-03-09-ontology-v3/round-01/02_agent-autonomy.md`
- `01_ideation/2026-03-09-ontology-v3/round-01/03_discovery-pattern.md`
- `01_ideation/2026-03-09-ontology-v3/round-01/04_dispatch-context.md`

### 핵심 축
```
에이전트 본질 (목표 지향 자율성)
  → 온톨로지 재설계 (31개→~15 타입, retrieval_hints)
  → A8 Discovery (co-retrieval 패턴 학습)
  → dispatch 컨텍스트화 (세션별 작업 분리)
```

### 주요 설계 방향
1. **타입 Tier 1/2/3 계층**: 핵심 7 + 맥락 5 + 전환 3 = ~15
2. **retrieval_hints**: 저장 시 "언제 꺼낼지" 함께 설계
3. **에이전트 자율성 L0-L5**: 현재 L1-L2, 목표 L3 (목표 추론)
4. **co-retrieval**: recall_log pair 추출 → edge boost
5. **dispatch**: impl-index 기반 세션 컨텍스트 (추가 인프라 불필요)

---

## 5. 커밋 기록

| 레포 | 해시 | 내용 |
|------|------|------|
| orchestration | 39f6e6f | STATE.md — enrichment + NDCG 0.724 반영 |

미커밋: Ideation R1 파일 5개 + impl-index 갱신 + work-log

---

## 6. 다음 세션

1. Ontology v3 Ideation R2 (4개 주제 심화, Paul 피드백 반영)
2. R2 → Impl Design → 구현 (5단계 파이프라인)
3. 우선순위: retrieval_hints > 타입 정리 > co-retrieval > dispatch
