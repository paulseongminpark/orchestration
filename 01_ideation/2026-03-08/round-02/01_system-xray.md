# 01. 시스템 X-Ray — 8대 약점 진단

> STATE.md, KNOWLEDGE.md, PLANNING.md, MEMORY.md, 실제 운영 데이터 기반

---

## W1. 토큰 예산 위기 (THE #1 BOTTLENECK)

**현상**: 200K 컨텍스트 중 절반 이상이 시작 전에 소진된다.

```
고정 비용 분해:
├── System prompt + Tools 정의:  ~42K (KNOWLEDGE.md 기록)
├── MCP 5서버 58도구 풀 로드:   ~55K (MEMORY.md 기록)
├── CLAUDE.md + rules + MEMORY:  ~5K
└── 합계:                        ~102K (200K 중 51%)

남는 작업 공간:                   ~98K
compact 권장 임계:                100K
→ 실제 작업 가능량:               ~0K (시작하자마자 compact 임계)
```

**근본 원인**: MCP 도구 58개가 매 턴 풀 로드되는 구조. 도구 하나당 ~950 토큰.

**증거**:
- PLANNING.md D-023: "baseline ~46K 토큰으로 작업 가용 영역 부족"
- PLANNING.md D-024: 에이전트 24→15 통합했지만 MCP 도구는 건드리지 못함
- v3.3.1에서 Playwright/document-skills 비활성화로 6.5K 절감 시도 — 근본 해결 아님
- MEMORY.md: "5서버 58도구 ≈ 55K 토큰 오버헤드" 명시

**영향 범위**: 모든 것. 토큰이 부족하면 더 자주 compact → 정보 손실 → 품질 저하 → 재작업 → 더 많은 토큰 소모. 악순환.

**심각도**: ★★★★★ (시스템 전체 성능 천장)

---

## W2. Recall 품질 한계

**현상**: mcp-memory recall이 "비슷한 것"은 찾지만 "필요한 것"을 못 찾는다.

```
현재 recall 점수 = similarity (1차원)

NDCG@5 현황:
├── 전체:         0.460 (상위 5개 결과의 46%만 최적)
├── q026-q050:    0.519 (튜닝 후 개선)
├── q051-q075:    0.244 (신규 쿼리, 매우 낮음)
└── 목표:         0.700+ (실용 수준)

누락된 차원:
├── recency:      6개월 전 메모 = 어제 메모 (동일 가중치)
├── importance:   L0 관찰 = L5 가치관 (동일 가중치)
├── correction:   사용자 교정 기록 없음
└── co-retrieval: 자주 함께 검색되는 노드 연결 없음
```

**근본 원인**: recall이 벡터 유사도 + 키워드 부스트 + 다양성 상한만으로 작동. 시간, 중요도, 사용자 피드백 차원이 없음.

**증거**:
- mcp-memory v2.2.1: NDCG@5 0.460 (goldset v2.2 기준)
- q051-q075 NDCG@5: 0.244 — 새로운 쿼리 유형에 취약
- promote_node 존재하지만 recall 점수에 미반영
- 2,869 노드 전부 동일 가중치, 아무것도 잊히지 않음

**영향 범위**: mcp-memory 기반 모든 작업 — checkpoint, recall, get_context, 에이전트 메모리 조회.

**심각도**: ★★★★☆ (핵심 인프라이지만, 현재도 "동작은 함")

---

## W3. Compact 시 지식 손실

**현상**: compact 할 때마다 정보가 줄어든다. 스냅샷이 있지만 "뭘 배웠는지"는 압축에서 사라진다.

```
정보 흐름:
대화 (풀 컨텍스트) → compact 요약 (200자 이내) → 다음 컨텍스트
                    ↑
              여기서 90%+ 손실

현재 안전망:
├── PreCompact 스냅샷:     snapshot-{date}.md (파일 보존)
├── mcp-memory:            checkpoint 스킬 (수동 호출)
├── auto_remember.py:      PostToolUse hook (2026-03-08 설치, 미검증)
├── relay.py:              PreCompact → mcp-memory (2026-03-08 설치, 미검증)
└── MEMORY.md:             200줄 고정 (넘치면 truncate)

누락:
├── "이 세션에서 뭘 배웠나" 구조화 추출: ❌
├── 실패에서 배운 교훈 자동 기록: ❌
├── 성숙한 기억 → 규칙 자동 승격: ❌
└── compact 요약 품질 커스터마이징: ❌
```

**근본 원인**: compact = 기계적 요약. "중요한 것"과 "사라져도 되는 것"의 구분 로직 없음.

**심각도**: ★★★★☆ (반복 발생, 누적 비용 높음)

---

## W4. 세션 격리 (Fresh Start 문제)

**현상**: 매 세션이 거의 백지에서 시작한다. 이전 세션의 맥락을 "재발견"하는 데 토큰을 소모한다.

```
세션 시작 시 사용 가능한 컨텍스트:
├── SessionStart hook:     미커밋 현황 + ❌결정 5건 + live-context 5줄
├── MEMORY.md:             200줄 (고정, 일반적)
├── mcp-memory recall:     수동 호출해야 함
└── 이전 세션 목표/진행:   없음 ❌

누락:
├── TASK_CONTRACT:         세션 완료 조건 명시 ❌
├── 세션 시작 시 자동 recall: ❌ (수동으로 recall 해야)
├── 이전 세션 교훈:        lessons.md 같은 누적 기록 ❌
└── 작업 유형 자동 분류:   Classify 단계 ❌
```

**근본 원인**: 세션 간 연결이 느슨. 기억은 mcp-memory에 있지만 자동으로 불러오지 않음. 세션 목표/완료 기준이 형식화되어 있지 않음.

**증거**:
- MEMORY.md 교훈: "구현 완료 ≠ DONE" (2026-02-26 2회 지적) — 세션 완료 기준 불명확
- .ctx/ Cross-CLI 공유 메모리가 2026-03-03에 폐기됨 — 유지 비용 대비 효과 없었음

**심각도**: ★★★☆☆ (매 세션 5-10분 오버헤드, 누적하면 큼)

---

## W5. 스킬 트리거 부정확

**현상**: 9개 스킬 중 어떤 스킬이 언제 발동해야 하는지 경계가 모호하다.

```
현재 스킬 description 상태:
├── /morning, /sync, /todo:       명확 (키워드 트리거)
├── /dispatch, /compact:          중간 (조건이 넓음)
├── /verify, /session-insights:   모호 (언제 자동 발동?)
├── /handoff, /status:            거의 미사용
└── superpowers/* 12개:           brainstorming은 잘 발동, 나머지 불규칙

누락:
├── TRIGGER / DO NOT TRIGGER 명시적 패턴: ❌
├── 스킬 품질 측정 (evaluations/): ❌
├── allowed-tools 제한: ❌ (brainstorming이 코드 수정 가능)
└── Progressive disclosure (Level 1/2/3): 부분적
```

**심각도**: ★★☆☆☆ (불편하지만 치명적이진 않음)

---

## W6. 에이전트 체인 경직성

**현상**: 모든 체인이 선형(A→B→C). 병렬 실행 불가. 학습 단계 없음.

```
현재 체인:
├── 구현:     implement → code-reviewer → commit-writer → linker
├── 배포:     pf-ops → security-auditor → 사용자 확인 → push
├── 추출:     Gemini/Codex → ai-synthesizer → 사용
├── 압축:     compressor → doc-ops → doc-ops verify
└── 디스패치: /dispatch → linker → meta-orchestrator → 팀

누락:
├── Wave/DAG 병렬 실행:         ❌ (독립 태스크도 순차)
├── Classify 단계:              ❌ (작업 유형 자동 분류 없음)
├── Learn 단계:                 ❌ ("뭘 배웠나" 기록 없음)
├── Context sub-agent:          ❌ (실행 전 컨텍스트 수집 분리 없음)
└── Rolling pool (12+ agents):  ❌ (대규모 독립 태스크에 비효율)
```

**심각도**: ★★★☆☆ (현재 워크로드에선 선형으로 충분하지만, 규모 확장 시 병목)

---

## W7. 거버넌스 갭

**현상**: `--dangerously-skip-permissions`로 모든 권한을 열어놓고 운영 중. 사고 발생 이력 있음.

```
현재 보안 구조:
├── PreToolUse hook:     rm -rf, force push 차단 (단순 regex)
├── --dangerously-skip-permissions: 나머지 전부 허용 ⚠️
├── 2026-03-05 사고:    멀티세션 아이디에이션에서 B가 소스코드 커밋, C가 config 커밋
└── git revert로 복구:  30분 소요

누락:
├── allow/review/deny 3계층 정책:     ❌
├── 코드 레벨 거버넌스:                ❌ (enable_delete=False 같은)
├── Approval 데코레이터:               ❌ (blocking/audit)
├── 위협 실시간 스캔:                  ❌ (governance-audit hook)
└── 외부 영향(push/PR/메시지)만 review: ❌
```

**증거**: MEMORY.md 교훈에 아이디에이션 사고 기록. common-mistakes.md에 "아이디에이션 세션 안전 규칙" 별도 섹션.

**심각도**: ★★★☆☆ (사고 1회 발생, 재발 가능성 있음)

---

## W8. 외부 연동 빈약

**현상**: 정보 입력이 대부분 수동. 자동화 파이프라인이 tech-review에만 존재.

```
현재 자동화:
├── tech-review:  Perplexity → Jekyll 파이프라인 (자동)
├── tech-review:  YouTube/Twitter/Bookmark Task Scheduler (3개)
├── daily-memo:   핸드폰 → GitHub Actions → Inbox.md (자동)
└── 나머지:       전부 수동

자동화 안 된 것:
├── Gmail 요약/트리아지:           수동
├── Calendar 일정 파악:            수동
├── 주간 리뷰:                     수동 (또는 안 함)
├── 학습 패턴 요약:                수동
├── context/ 파일 재인덱싱:        수동
└── 일일 브리핑 (/morning):        스킬 있지만 외부 데이터 없음
```

**심각도**: ★★☆☆☆ (불편하지만 시스템 자체 성능과 무관)

---

## 약점 심각도 요약

| 순위 | 약점 | 심각도 | 영향 범위 |
|------|------|--------|-----------|
| **1** | **W1. 토큰 예산 위기** | ★★★★★ | 전체 시스템 천장 |
| **2** | **W2. Recall 품질** | ★★★★☆ | 기억 기반 모든 작업 |
| **3** | **W3. 지식 손실** | ★★★★☆ | 세션 간 연속성 |
| **4** | **W4. 세션 격리** | ★★★☆☆ | 매 세션 오버헤드 |
| **5** | **W6. 체인 경직** | ★★★☆☆ | 병렬 작업 불가 |
| **6** | **W7. 거버넌스** | ★★★☆☆ | 안전성 |
| **7** | **W5. 스킬 트리거** | ★★☆☆☆ | UX |
| **8** | **W8. 외부 연동** | ★★☆☆☆ | 편의성 |
