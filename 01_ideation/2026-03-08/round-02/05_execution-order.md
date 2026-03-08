# 05. 복리 실행 순서

> 순서가 중요한 이유: Phase 1의 결과가 Phase 2의 효과를 증폭시킨다.
> 이것은 "우선순위 목록"이 아니라 "복리 투자 전략"이다.

---

## 핵심 원칙

```
Phase N의 결과 → Phase N+1의 기반

Phase 1 (토큰 해방) → 작업 공간 확보
Phase 2 (Recall 혁명) → 확보된 공간에서 더 좋은 정보
Phase 3 (학습 루프) → 좋은 정보로 시스템 성장
Phase 4 (안전 자율) → 성장하는 시스템을 안전하게 자율 운영
Phase 5 (확장) → 안전한 기반 위에서 고급 기능
```

---

## Phase 1: 토큰 해방 (Week 1, 1~2일)

### 목표: 작업 공간 ~98K → ~148K

| 순서 | 작업 | 시간 | 세션 | 비고 |
|------|------|------|------|------|
| 1-1 | C5 MEMORY.md IF-ELSE 분리 | 30분 | 이 세션 | 가장 쉬움, 즉시 효과 |
| 1-2 | C2 defer_loading 설정 | 2시간 | 이 세션 | MCP config 변경, ToolSearch 테스트 |
| 1-3 | C1 캐시 순서 검증 | 30분 | 이 세션 | 규칙 문서화 |

**검증 기준**:
- [ ] MEMORY.md 200줄 → 80줄 이하
- [ ] MCP 도구 토큰: 55K → 10K 이하 (ToolSearch 정상 작동)
- [ ] 새 세션 시작 시 baseline 토큰 측정

**다음 Phase를 위한 기반**:
- 50K 토큰 회수 → Recall 개선 테스트에 더 많은 반복 가능
- compact 빈도 감소 → Learn 단계 추가해도 세션 내 처리 가능

---

## Phase 2: Recall 혁명 (Week 1, 2~3일)

### 목표: NDCG@5 0.460 → 0.65+

**이 Phase는 Warp mcp-memory 세션에서 병렬 실행 가능.**

| 순서 | 작업 | 시간 | 세션 | 비고 |
|------|------|------|------|------|
| 2-1 | A1 복합 스코어링 프레임워크 | 3시간 | Warp | 공식 + 가중치 + 테스트 |
| 2-2 | A4 Half-life decay 함수 | 2시간 | Warp | A1에 plug-in |
| 2-3 | A6 Reviewed-item multiplier | 1시간 | Warp | promote_node → 점수 반영 |
| 2-4 | A5 Correction 노드 타입 | 2시간 | Warp | 독립 구현, top-inject |
| 2-5 | Goldset re-evaluation | 1시간 | Warp | q026-q075 NDCG 재측정 |

**검증 기준**:
- [ ] NDCG@5 ≥ 0.60 (q026-q050)
- [ ] NDCG@5 ≥ 0.40 (q051-q075, 현재 0.244)
- [ ] 163 기존 테스트 PASS
- [ ] correction 노드 생성 + recall top-inject 확인

**이 세션과 병렬**:
- Phase 1(토큰)은 이 세션에서
- Phase 2(Recall)는 Warp 세션에서
- 동시에 진행 가능 — 의존성 없음

---

## Phase 3: 학습 루프 (Week 2, 2~3일)

### 목표: 세션이 시스템을 성장시키는 구조

| 순서 | 작업 | 시간 | 비고 |
|------|------|------|------|
| 3-1 | C6 TASK_CONTRACT.md 템플릿 | 1시간 | 세션 시작 시 자동 생성 |
| 3-2 | B1 Learn 단계 프롬프트 | 2시간 | compressor에 통합 or 별도 hook |
| 3-3 | B5 lessons.md 자동 축적 | 1시간 | PostToolUse 실패 감지 → 기록 |
| 3-4 | A9 Memory-Merger 초안 | 3시간 | signal→pattern 승격 자동화 |

**검증 기준**:
- [ ] 새 세션 시작 시 TASK_CONTRACT 자동 프롬프트
- [ ] 세션 종료 시 Learn 단계 실행 (최소 3줄 학습 기록)
- [ ] lessons.md에 최근 5세션 교훈 누적
- [ ] Memory-Merger가 1개 이상 승격 후보 제안

**Phase 2가 먼저인 이유**:
- Learn 단계에서 mcp-memory에 저장 → recall 품질이 좋아야 의미 있음
- Recall이 나쁜 상태에서 Learn해도 나중에 못 찾음

---

## Phase 4: 안전 자율 (Week 2~3, 1~2일)

### 목표: --dangerously-skip-permissions를 지능적으로 대체

| 순서 | 작업 | 시간 | 비고 |
|------|------|------|------|
| 4-1 | D4 governance-audit hook | 2시간 | PreToolUse에 5위협 regex 추가 |
| 4-2 | E3 스킬 TRIGGER 패턴 점검 | 1시간 | 9개 스킬 description 수정 |
| 4-3 | E2 scripts/ 블랙박스 패턴 | 30분 | 스킬 내 스크립트 읽기 금지 지시 |

**검증 기준**:
- [ ] governance-audit hook 5가지 패턴 테스트 (각 1건 이상)
- [ ] 9개 스킬에 TRIGGER/DO NOT TRIGGER 명시
- [ ] 스킬 내 scripts/ 있는 경우 --help 우선 실행 확인

**Phase 3이 먼저인 이유**:
- 학습 루프가 돌면 governance 위반도 학습 → 자동 개선
- TASK_CONTRACT이 있으면 세션 범위가 명확 → 거버넌스 경계도 명확

---

## Phase 5: 확장 (Week 3+, 선택적)

### Phase 1~4 완료 후 필요에 따라 선택

| 작업 | 전제조건 | 비고 |
|------|---------|------|
| A8 Discovery 패턴 | Phase 2 완료 | co-retrieval shortcut |
| B2 Wave DAG | Phase 1 완료 | 병렬 에이전트 의존성 |
| A3 충돌 감지 | Phase 2 완료 | 의미적 모순 해소 |
| F1 gws 연동 | 독립 | Gmail/Calendar 자동화 |
| A10 원자 추출 | Phase 2 완료 | remember() 자동 분해 |
| D1 GovernancePolicy | Phase 4 완료 | 3계층 정책 프레임워크 |
| B4 LLM Council | Phase 1 완료 | 설계 필요 |

---

## 병렬 실행 맵

```
Week 1:
  [이 세션]          [Warp mcp-memory]
  Phase 1-1 (30분)   Phase 2-1 (3시간)
  Phase 1-2 (2시간)  Phase 2-2 (2시간)
  Phase 1-3 (30분)   Phase 2-3 (1시간)
                     Phase 2-4 (2시간)
                     Phase 2-5 (1시간)

Week 2:
  [세션 A]           [세션 B]
  Phase 3-1~3-2      Phase 4-1~4-2
  Phase 3-3~3-4      Phase 4-3

Week 3+:
  Phase 5 (필요시)
```

---

## 투자 대비 수익 (ROI) 요약

| Phase | 투자 시간 | 회수 (매 세션) | 회수 기간 |
|-------|----------|---------------|-----------|
| **1. 토큰 해방** | 3시간 | +50K 토큰/세션 | **즉시** |
| **2. Recall 혁명** | 9시간 | NDCG 0.46→0.65 | 1주 내 체감 |
| **3. 학습 루프** | 7시간 | 세션당 3+ 교훈 축적 | 2주 후 복리 |
| **4. 안전 자율** | 3.5시간 | 사고 예방 | 영구적 |
| **합계** | **~22.5시간** | | |

**22.5시간 투자 → 매 세션이 51% 더 넓고, 40% 더 정확하고, 점점 더 똑똑해지는 시스템.**

---

## 지금 당장 할 수 있는 것

### 이 세션:
1. **MEMORY.md 분리** (Phase 1-1, 30분)
2. **defer_loading 조사 + 설정** (Phase 1-2, 2시간)

### Warp에 보낼 프롬프트:
→ Phase 2 전체 (A1+A4+A5+A6 구현 + goldset 재측정)

### 즉시 결정 필요:
- Phase 1과 Phase 2를 **지금 병렬 시작**할 것인가?
- Phase 3~4는 다음 세션으로 미룰 것인가?
