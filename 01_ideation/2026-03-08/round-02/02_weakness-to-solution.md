# 02. 약점 → 해법 매핑

> Round 1 인사이트(A1~G9)를 시스템 약점(W1~W8)에 역매핑
> 방향: "이 인사이트가 어디에 쓰이나"가 아니라 "이 약점을 뭘로 고치나"

---

## W1. 토큰 예산 위기 → 해법 3개

### 1차 해법: C2 defer_loading (55K → 8K)
- **문제**: MCP 58도구가 매 턴 풀 로드 = 55K 토큰
- **해법**: `defer_loading: true` → 이름만 로드, ToolSearch로 필요시 풀 스키마
- **효과**: 55K → ~8K (85% 절감, 47K 회수)
- **난이도**: 중 (MCP config 변경 + ToolSearch 패턴 학습)
- **소스**: @trq212, Claude Tool Search API docs

### 2차 해법: C5 MEMORY.md IF-ELSE 디렉토리
- **문제**: MEMORY.md 200줄이 매 턴 로드 = ~5K 토큰
- **해법**: MEMORY.md를 80줄 포인터로 축소, 상세는 topic별 파일
- **효과**: ~5K → ~2K (3K 회수)
- **난이도**: 하 (파일 분리 + 경로만 기록)
- **소스**: @sysls

### 3차 해법: C1 프롬프트 캐싱 순서 준수
- **문제**: 현재 캐시 히트율 불명. 도구/시스템 변경이 캐시 무효화할 수 있음
- **해법**: Static→Tools→CLAUDE.md→Session→Messages 순서 엄수, mid-session 도구 변경 금지
- **효과**: 캐시 히트 시 90% 비용 절감 (비용, 토큰은 간접)
- **난이도**: 하 (인식 + 규칙 준수)
- **소스**: @trq212

### W1 합산 효과
```
현재:    ~102K 고정
1차 적용: ~102K - 47K = ~55K
2차 적용: ~55K - 3K = ~52K
캐싱:    비용 절감 (토큰 수는 유지, 비용 90%↓)

결과: 작업 가용 영역 ~98K → ~148K (+50K, 51% 증가)
```

---

## W2. Recall 품질 한계 → 해법 5개

### 1차 해법: A1 복합 스코어링
- **문제**: similarity 단일 차원 → 시간/중요도 무시
- **해법**: `final_score = similarity×0.5 + decay_score×0.3 + keyword_boost×0.2`
- **NDCG 예상**: 0.460 → 0.55~0.65 (recency+importance 반영만으로)
- **소스**: @joaomoura, @jamesquint

### 2차 해법: A4 Half-life 망각
- **문제**: 2,869 노드 전부 동일 가중치
- **해법**: `decay_score = importance × e^(-λ × days_since_access)`
- **효과**: 오래 안 읽힌 노드 자연 감소. recall 시 access 갱신 = 수명 연장
- **A1과 결합**: decay_score가 복합 스코어링의 한 축
- **소스**: @joaomoura, Karpathy

### 3차 해법: A5 Correction 노드 타입
- **문제**: 사용자 교정 기록 없음 → 같은 실수 반복
- **해법**: `type: "correction"` 노드, recall 시 top-inject
- **효과**: 교정된 지식이 항상 최우선 → 반복 실수 제거
- **독립 구현 가능**: 기존 스코어링과 무관하게 top-inject 로직만 추가
- **소스**: @jamesquint, Pal 소스

### 4차 해법: A6 Reviewed-item Multiplier
- **문제**: promote_node가 Layer만 올리고 recall 점수에 미반영
- **해법**: promote_node된 노드에 1.5x multiplier
- **효과**: 인간 검증 지식 > 자동 학습. goldset 정확도 향상
- **소스**: @jamesquint

### 5차 해법: A8 Discovery 패턴
- **문제**: 자주 같이 검색되는 노드가 매번 독립 검색
- **해법**: co-retrieval 히스토리에서 shortcut 엣지 자동 생성
- **효과**: 연관 노드군 일괄 검색 → recall 커버리지 향상
- **Tier 2**: 스코어링 안정화 후 구현
- **소스**: Pal 소스

### W2 합산 효과
```
현재:     1차원 (similarity)
1+2차:    3차원 (similarity + decay + importance) → NDCG 0.55~0.65
3차:      교정 top-inject → 반복 실수 제거
4차:      promote 반영 → 검증 지식 우선
5차:      co-retrieval → 커버리지 확대

예상 NDCG@5: 0.460 → 0.65~0.75
```

---

## W3. 지식 손실 → 해법 4개

### 1차 해법: B1 Learn 단계
- **문제**: 세션이 끝나도 "뭘 배웠나" 구조화되지 않음
- **해법**: 세션 종료 전 `Learn:` 단계 — 새 발견, 실패 교훈, 패턴 인식을 구조화 추출
- **Pal 방식**: 코드가 아닌 프롬프트로 구현. "이 세션에서 뭘 배웠는가?" 자동 질문
- **소스**: Pal 소스, @jackculpan

### 2차 해법: A9 Memory-Merger
- **문제**: Signal→Pattern 승격이 수동
- **해법**: 성숙한 memory 항목 자동 식별 → 사용자 승인 → rules/instructions에 병합 → memory에서 제거
- **Quality Bar**: zero knowledge loss + minimal redundancy + maximum scannability
- **소스**: awesome-copilot memory-merger

### 3차 해법: C3 Compaction 커스터마이즈
- **문제**: compact 요약이 기계적 (200자 이내)
- **해법**: `instructions` 필드로 커스텀 요약 프롬프트. "결정사항과 학습을 우선 보존"
- **효과**: compact 후에도 핵심 결정이 살아남음
- **소스**: Claude Compaction API docs

### 4차 해법: A10 원자 메모리 추출
- **문제**: remember()가 500자 덩어리를 하나의 노드로 저장
- **해법**: remember() 시 자동 atomic fact 분해 → 개별 노드 생성
- **효과**: 검색 정밀도 향상 (큰 덩어리에서 일부만 관련 → 미스)
- **Tier 3**: recall 안정화 후 구현
- **소스**: @joaomoura

---

## W4. 세션 격리 → 해법 4개

### 1차 해법: C6 TASK_CONTRACT.md
- **문제**: 세션 완료 조건이 불명확 → "DONE"인데 아닌 상태
- **해법**: 세션 시작 시 계약서 작성 — 테스트 조건 + 검증 기준 + 완료 정의
- **효과**: 세션 목표 명확화, 미완료 판별 기계화
- **소스**: @sysls

### 2차 해법: C7 세션=1계약
- **문제**: 장시간 세션에서 무관한 컨텍스트 오염
- **해법**: 1세션 = 1계약. compact 전에 계약 갱신 또는 새 세션
- **현재와 차이**: 지금도 "1세션=1목표" 규칙이지만 강제하는 메커니즘 없음
- **소스**: @sysls

### 3차 해법: B5 lessons.md 누적
- **문제**: 에이전트가 같은 실수를 반복
- **해법**: 실패 감지 → lessons.md 자동 업데이트. "Would a staff engineer approve this?" 자기 검증
- **PostToolUse hook에서**: 실패 패턴 감지 시 자동 추가
- **소스**: @jackculpan

### 4차 해법: B6 Context Sub-agent
- **문제**: 구현 시작 전 컨텍스트 수집이 메인 context를 소모
- **해법**: 서브에이전트가 먼저 데이터 조사 → structured brief 반환 → 메인은 brief만 사용
- **이미 유사 패턴**: project-context 에이전트가 존재하지만 자동 발동 안 됨
- **소스**: @jamesquint

---

## W5. 스킬 트리거 → 해법 4개

### E3 TRIGGER/DO NOT TRIGGER
- 모든 스킬 description에 positive/negative 트리거 명시
### E1 Progressive Disclosure 3레벨
- Level 1(YAML) → Level 2(SKILL.md) → Level 3(references/)
### E6 evaluations/
- with_skill vs without_skill 블라인드 비교로 품질 측정
### E5 allowed-tools
- brainstorming에서 Edit/Write 차단

---

## W6. 체인 경직 → 해법 3개

### B2 Wave DAG
- depends_on 배열로 의존성 그래프 → Wave 단위 병렬 실행
### B1 Classify→Learn 5단계
- 현재 3단계(읽기→실행→기록)를 5단계(분류→회상→조회→실행→학습)로
### B3 Rolling Pool
- 대규모 독립 태스크에 12-15 에이전트 슬롯 동시 투입

---

## W7. 거버넌스 → 해법 3개

### D1+D3 GovernancePolicy + 코드 레벨
- allow/deny/review 3계층 + enable_delete=False 같은 코드 강제
### D4 governance-audit hook
- 5가지 위협 실시간 regex 스캔 (data_exfil, priv_esc, destruction, injection, credential)
### D2 Approval 데코레이터
- push/PR 시 blocking approval, 나머지는 audit-only

---

## W8. 외부 연동 → 해법 2개

### F1 gws (Google Workspace CLI)
- Gmail triage + Calendar agenda → mcp-memory 자동 파이프라인
### F6 Pal 스케줄 태스크
- daily_briefing(8AM), inbox_digest(12PM), weekly_review(금5PM)

---

## 매핑 요약 매트릭스

| 약점 | 1차 해법 | 2차 해법 | 3차 해법 | 4차 해법 | 5차 해법 |
|------|---------|---------|---------|---------|---------|
| W1 토큰 | **C2 defer** | C5 MEMORY분리 | C1 캐시순서 | | |
| W2 Recall | **A1 복합스코어** | A4 Half-life | A5 Correction | A6 Multiplier | A8 Discovery |
| W3 손실 | **B1 Learn** | A9 Merger | C3 Compaction | A10 Atomic | |
| W4 격리 | **C6 CONTRACT** | C7 1계약 | B5 lessons | B6 Sub-agent | |
| W5 스킬 | **E3 TRIGGER** | E1 3레벨 | E6 eval | E5 allowed | |
| W6 체인 | **B2 Wave DAG** | B1 5단계 | B3 Pool | | |
| W7 거버넌스 | **D1+D3 Policy** | D4 audit hook | D2 Approval | | |
| W8 외부 | **F1 gws** | F6 스케줄 | | | |

**굵은 글씨** = 각 약점의 가장 임팩트 큰 해법
