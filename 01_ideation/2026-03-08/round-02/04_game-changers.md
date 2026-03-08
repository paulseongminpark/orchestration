# 04. 게임 체인저 분류

> 30개 항목을 3등급으로 분류.
> 기준: "이것이 시스템의 작동 방식 자체를 바꾸는가?"

---

## Tier S: 게임 체인저 (시스템 천장을 올림)

이것들 없이는 다른 개선이 의미가 약하다.

### S1. C2 defer_loading — "숨쉴 공간"
- **변화**: 작업 공간이 ~98K → ~148K (+51%)
- **왜 게임 체인저**: 토큰은 이 시스템의 화폐. 화폐가 51% 늘면 모든 것이 바뀜.
  - 더 긴 대화 = 더 복잡한 작업 가능
  - compact 빈도 감소 = 지식 손실 감소
  - 에이전트 체인에 여유 = 더 많은 단계 가능
- **없으면**: 어떤 개선을 해도 "토큰 부족으로 compact" 루프에 갇힘

### S2. A1+A4+A6 복합 스코어링 — "기억의 차원 확장"
- **변화**: recall이 1차원(유사도) → 3차원(유사도+시간+중요도)
- **왜 게임 체인저**: mcp-memory가 "검색엔진"에서 "기억 시스템"으로 전환.
  - NDCG 0.460 → 0.65+ = recall 결과의 질적 변화
  - 시간이 지나면 자연스럽게 정리됨 (half-life)
  - 검증된 지식이 우선 (multiplier)
- **없으면**: 2,869 노드가 계속 쌓이고, 관련 없는 노드가 상위에 계속 노출

### S3. B1+C6 Learn 단계 + TASK_CONTRACT — "성장하는 시스템"
- **변화**: 세션이 "소비"에서 "투자"로 전환
- **왜 게임 체인저**: 지금은 100세션 해도 1세션과 동일한 시스템.
  이것 후에는 100세션 → 100개 교훈이 축적된 시스템.
  - 시스템이 시간에 비례해 성장
  - 세션 완료 기준이 명확 (CONTRACT)
  - 매 세션 끝에 구조화된 학습 (Learn)
- **없으면**: 경험이 MEMORY.md에 수동 기록 → 200줄 한계에 막힘 → overflow

---

## Tier A: 포스 멀티플라이어 (기반 위에서 효과 2배)

게임 체인저가 깔린 후 적용하면 곱셈 효과.

### A1. A5 Correction 노드 타입
- **효과**: 사용자 교정이 영구 지식화 → 같은 실수 100% 방지
- **의존**: recall 스코어링 (S2) 위에 얹어야 효과적
- **독립 구현도 가능**: top-inject는 스코어와 무관

### A2. D4 governance-audit hook
- **효과**: 5가지 위협 실시간 차단 → 자율성 안전 확대
- **의존**: 없음 (독립 구현 가능)
- **매력**: 바로 PreToolUse hook에 추가하면 됨

### A3. C5 MEMORY.md IF-ELSE 분리
- **효과**: -3K 토큰 + 캐시 안정화
- **의존**: S1(defer_loading)과 함께 하면 효과 극대
- **단독으로도 유의미**: MEMORY.md 가독성 향상

### A4. E3 스킬 TRIGGER/DO NOT TRIGGER
- **효과**: 스킬 발동 정확도 향상 → 불필요한 스킬 로딩 감소
- **의존**: 없음
- **쉬움**: description 수정만

### A5. A9 Memory-Merger
- **효과**: 성숙한 기억 → 규칙 자동 승격
- **의존**: S3(Learn 단계)가 기억을 공급해야 의미 있음

### A6. B2 Wave DAG dispatching
- **효과**: 병렬 에이전트 실행 → 대규모 태스크 처리 가능
- **의존**: S1(토큰 여유)이 있어야 병렬 에이전트에 context 분배 가능

---

## Tier B: Nice-to-Have (있으면 좋지만 필수 아님)

기반이 있으면 자연스럽게 추가.

### B1. A8 Discovery 패턴
- co-retrieval shortcut. recall 안정화 후.

### B2. A3 메모리 충돌 감지
- 의미적 모순 해소. 온톨로지 성숙 후.

### B3. A10 원자 메모리 추출
- remember() 시 자동 분해. 현재 remember는 잘 작동 중.

### B4. B3 Rolling Pool
- 12-15 에이전트 동시. 현재 워크로드에선 과잉.

### B5. B4 LLM Council
- Claude+Codex+Gemini 합의. 설계 필요, 현재는 delegate로 충분.

### B6. F1 gws 연동
- Gmail/Calendar 자동화. 편의성이지 핵심이 아님.

### B7. D1+D2 GovernancePolicy + Approval
- 3계층 정책 프레임워크. D4(hook)로 충분한 현재.

### B8. C3 Compaction 커스터마이즈
- compact 요약 개선. API 변경 필요.

### B9. E6 evaluations/
- 스킬 품질 자동 측정. 스킬 수가 적어서 수동으로 충분.

---

## Tier C: 연구/탐색 (당장 불필요)

### C1. B10 계획 파이프라인 체인 (PRD→arch→plan→breakdown→test)
### C2. B7 Bug Hunting 3-Agent
### C3. F4 GitNexus 시각화
### C4. E12 Anti-AI Slop
### C5. G7 Karpathy 본질 vs 효율 (철학적 프레임)
### C6. G4 탈옥 내부 경로 (연구 참고)
### C7. F2 Vercel CLI Marketplace
### C8. G8 agentic-eval 3패턴

---

## 한눈에 보기

```
Tier S (게임 체인저, 3개):
  S1. defer_loading          → 토큰 51% 증가
  S2. 복합 스코어링          → NDCG 0.46→0.65+
  S3. Learn + CONTRACT       → 성장하는 시스템

Tier A (포스 멀티플라이어, 6개):
  A1. Correction 타입        → 반복 실수 제거
  A2. governance-audit hook  → 안전 자율성
  A3. MEMORY.md 분리         → 토큰 + 캐시
  A4. 스킬 TRIGGER 패턴      → 정확한 발동
  A5. Memory-Merger          → 기억→규칙
  A6. Wave DAG               → 병렬 실행

Tier B (Nice-to-Have, 9개):
  Discovery, 충돌감지, 원자추출, Rolling Pool,
  LLM Council, gws, GovernancePolicy, Compaction, evaluations

Tier C (연구, 8개):
  계획체인, Bug Hunting, GitNexus, Anti-Slop,
  본질vs효율, 탈옥경로, Vercel, agentic-eval
```

**S 3개 + A 6개 = 9개만 하면 시스템이 질적으로 다른 수준이 된다.**
나머지 21개는 이 9개 기반 위에서 필요할 때.
