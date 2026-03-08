# Round 01 — 시스템 강화 종합 Ideation

> 2026-03-08 19:00~21:30 KST
> 22개 소스 분석, 80+ 인사이트, 6개 에이전트 병렬 원문 분석

## 소스 인벤토리 (22개)

| # | 소스 | 유형 | 핵심 키워드 |
|---|---|---|---|
| 1 | @jamesquint — "How to Build a Data Agent in 2026" | X Article (294K views, 2.3K bookmarks) | context management, quirk store, self-scoring |
| 2 | @joaomoura — CrewAI 인지적 메모리 | X Thread (tech-review blog) | 5 cognitive ops, composite scoring, half-life |
| 3 | @ashpreetbedi — Pal 개인 에이전트 | X + GitHub (agno-agi/pal) | 5-step loop, Discovery, Knowledge Map |
| 4 | @ashpreetbedi — AgentOS 프로덕션 런타임 | X + GitHub (agno-agi/agentos-docker-template) | 6 pillars, 3-tier governance, Approval |
| 5 | @jackculpan — 에이전트 7원칙 | X Thread (tech-review blog) | Plan→Verify→Learn, lessons.md |
| 6 | @sysls — 단순함이 최강 | X Thread (tech-review blog) | IF-ELSE CLAUDE.md, TASK_CONTRACT, agent spa day |
| 7 | @trq212 (Thariq, Anthropic) — "Prompt Caching Is Everything" | X Article (1.9M views, 12K bookmarks) | prefix matching, defer_loading, cache-safe forking |
| 8 | @aidenbai — React→Claude Code 워크플로우 | X Thread | npx, component selection |
| 9 | @svpino — Playwright MCP 브라우저 제어 | X Thread | Claude Code + Playwright |
| 10 | @sawyerhood — Google Workspace CLI | X Thread | gws, Gmail/Calendar/Drive |
| 11 | @MillieMarconnni — GitNexus 코드 그래프 | X Thread | repo → knowledge graph |
| 12 | @julienbek — AI 비즈니스 모델 | X Thread | 서비스 > 도구 판매 |
| 13 | Anthropic — Tracing Thoughts 해석 연구 | Research page | 환각 메커니즘, 사전 계획, 병렬 경로 |
| 14 | Anthropic — The Complete Guide to Building Skills (33p PDF) | PDF | 3-level progressive disclosure, 5 patterns |
| 15 | OpenAI — curated skills (35개) | GitHub (openai/skills) | security 3종, playwright, notion 4종 |
| 16 | skills.sh — 에이전트 스킬 디렉토리 (86K+) | Web | swarm-planner, context-map, agent-governance |
| 17 | gws — Google Workspace CLI | GitHub (googleworkspace/cli) | 30+ agent skills, JSON output, Model Armor |
| 18 | ykdojo — claude-code-tips (45개) | GitHub | context bar, worktrees, HANDOFF.md, slim prompt |
| 19 | Vercel CLI marketplace | Web | discover→guide→add, agent JSON |
| 20 | Josh newsletter — Notion AI agents | Email (maily.so) | 관찰력 > 기술력, 16 agents by non-dev |
| 21 | Knuth — Claude Cycles (5p) | PDF (Stanford) | 31 explorations, plan.md, strategy switching |
| 22 | Karpathy — microgpt.py | Gist | 500줄 GPT, "본질 vs 효율" |

## 에이전트 원문 분석 (6개)

| 에이전트 | 대상 | 파일 | 소요 |
|---|---|---|---|
| Agent 1 | agno-agi/pal 전체 소스 | `_raw-pal.md` | 222s |
| Agent 2 | agno-agi/agentos-docker-template | `_raw-agentos.md` | 237s |
| Agent 3 | anthropics/skills 17개 스킬 | `_raw-anthropics-skills.md` | 193s |
| Agent 4 | Karpathy gist + Claude API docs | `_raw-karpathy-api.md` | 200s |
| Agent 5 | awesome-copilot 200+ 스킬/160+ instructions | `_raw-awesome-copilot.md` | 143s |
| Agent 6 | am-will/codex-skills 18개 스킬/26개 에이전트 | `_raw-codex-skills.md` | 152s |

## 섹션 파일 목록

| 파일 | 영역 | 인사이트 수 |
|---|---|---|
| `01_mcp-memory.md` | A. mcp-memory 강화 | 10 |
| `02_orchestration.md` | B. 오케스트레이션 강화 | 7+4 |
| `03_context.md` | C. 컨텍스트 관리 + 프롬프트 캐싱 | 9+1 |
| `04_governance.md` | D. 거버넌스/보안 | 5+2 |
| `05_skills.md` | E. 스킬 생태계 | 6+3 |
| `06_external.md` | F. 외부 연동 | 4 |
| `07_methodology.md` | G. 탐색/학습 방법론 | 7 |
| `08_execution.md` | H. 실행 계획 (Tier 1~3) | — |
