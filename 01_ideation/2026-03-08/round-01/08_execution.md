# H. 실행 계획

## Tier 1: 이번 주 (즉시 ROI)

| # | 작업 | 근거 | 예상 효과 | 난이도 |
|---|---|---|---|---|
| 1 | **MCP 도구 defer_loading** | C2 (@trq212 + API docs) | 58도구 55K → ~8K 토큰 (85% 절감) | 중 |
| 2 | **MEMORY.md 분리** | C1+C5 (캐시+IF-ELSE) | 매 턴 15-20K 토큰 절감 | 하 |
| 3 | **스킬 description WHAT+WHEN 점검** | E3 (TRIGGER/DO NOT TRIGGER) | 트리거 정확도 향상 | 하 |
| 4 | **에이전트 스파 데이 1회** | E7 (@sysls + memory-merger) | 누적 모순 제거 | 하 |
| 5 | **TASK_CONTRACT.md 도입** | C6 (@sysls) | 세션 완료 기준 명확화 | 하 |
| 6 | **scripts/ 블랙박스 패턴** | E2 (anthropics/skills) | 스킬 내 스크립트 소스 읽기 금지 | 하 |

## Tier 2: 이번 주~다음 주 (설계 + 구현)

| # | 작업 | 근거 | 예상 효과 | 난이도 |
|---|---|---|---|---|
| 7 | **mcp-memory importance + half-life** | A1+A4 (@joaomoura + Karpathy) | recall 품질 구조적 개선 | 중 |
| 8 | **quirk/correction 노드 타입** | A5 (@jamesquint + Pal) | 사용자 수정 자동 반영 | 중 |
| 9 | **Wave 기반 DAG dispatching** | B2 (codex-skills parallel-task) | 병렬 에이전트 의존성 관리 | 중 |
| 10 | **reviewed-item multiplier** | A6 (@jamesquint) | 인간 검증 지식 우선 순위 | 하 |
| 11 | **governance-audit hook** | D4 (awesome-copilot) | 5가지 위협 실시간 스캔 | 중 |
| 12 | **Discovery 패턴** | A8 (Pal 소스) | co-retrieval shortcut 엣지 | 중 |
| 13 | **gws 설치 + 연동** | F1 (gws CLI) | Gmail/Calendar → mcp-memory | 중 |

## Tier 3: 설계 필요 (2주+)

| # | 작업 | 근거 | 예상 효과 | 난이도 |
|---|---|---|---|---|
| 14 | **3차원 자가 채점** | A7 (@jamesquint self-scoring) | 에이전트 출력 신뢰도 향상 | 상 |
| 15 | **Classify→Learn 5단계 루프** | B1 (Pal) | 오케스트레이션 아키텍처 진화 | 상 |
| 16 | **LLM Council 합의 시스템** | B4 (codex-skills llm-council) | 설계 합의 (bias 제거) | 상 |
| 17 | **거버넌스 3계층** | D1+D2 (agent-governance + AgentOS) | --dangerously-skip-permissions 대체 | 상 |
| 18 | **Approval 데코레이터** | D2 (AgentOS) | blocking/audit 2모드 | 중 |
| 19 | **agentic-eval 자기 평가** | G8 (awesome-copilot) | 에이전트 출력 자동 평가 | 중 |
| 20 | **context/ voice guide** | C11 (Pal) | 에이전트별 출력 톤 제어 | 하 |
| 21 | **agents.md + llms.txt** | E10 (awesome-copilot) | 레포별 에이전트 진입점 | 하 |
| 22 | **메모리 충돌 감지** | A3 (@joaomoura) | 의미적 모순 자동 해소 | 상 |
| 23 | **원자 메모리 추출** | A10 (@joaomoura) | remember() 시 자동 분해 | 중 |
| 24 | **Iterative Refinement 패턴** | E4 (Anthropic 5 patterns) | 품질 체크→재생성 루프 | 중 |

## 연구/인박스 (우선순위 낮음)

| # | 항목 | 소스 |
|---|---|---|
| 25 | GitNexus — 6개 프로젝트 코드 그래프 시각화 | F4 (@MillieMarconnni) |
| 26 | build-your-own-x — vector DB/search engine 직접 구현 | G7 (codecrafters-io) |
| 27 | security-threat-model 8단계 → security-auditor 강화 | D6 (OpenAI skills) |
| 28 | context-map + what-context-needed 스킬 설치 (npx) | C8+C9 (awesome-copilot) |
| 29 | 계획 파이프라인 체인 도입 | B10 (awesome-copilot) |
| 30 | security-ownership-map git history 분석 | D7 (awesome-copilot) |

---

## 의존성 맵

```
Tier 1 (독립, 병렬 가능):
  [1] defer_loading
  [2] MEMORY.md 분리
  [3] 스킬 description
  [4] 에이전트 스파 데이
  [5] TASK_CONTRACT
  [6] scripts 블랙박스

Tier 2 (일부 의존):
  [7] importance → [10] reviewed-item
  [8] correction 타입 → [12] Discovery 패턴
  [9] Wave DAG (독립)
  [11] governance hook (독립)
  [13] gws (독립)

Tier 3 (설계 필요):
  [14] self-scoring → [19] agentic-eval
  [15] 5단계 루프 → [16] LLM Council
  [17] 거버넌스 → [18] Approval
  [22] 충돌 감지 → [23] 원자 추출
```

## 원본 소스 참조

| 파일 | 내용 |
|---|---|
| `_raw-pal.md` | Pal 전체 아키텍처, 5단계 루프, Knowledge/Learning 시스템, 거버넌스, 스케줄 |
| `_raw-agentos.md` | AgentOS 6 기둥, JWT RBAC, Approval, MCP 합성, UserFeedbackTools |
| `_raw-anthropics-skills.md` | 17개 스킬, Progressive Disclosure, skill-creator eval, scripts 블랙박스 |
| `_raw-karpathy-api.md` | microgpt.py 전체 소스, Compaction API, Tool Search API, Auto-caching |
| `_raw-awesome-copilot.md` | 200+ 스킬, 160+ instructions, governance-audit hook, 계획 체인 |
| `_raw-codex-skills.md` | 18 스킬, 26 에이전트, Wave/Swarm/Council 3전략, Context Pack |
