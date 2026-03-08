# E. 스킬 생태계

## E1. Anthropic 3레벨 Progressive Disclosure (공식 표준)
- **소스**: Anthropic Skills Guide (33p PDF)
- **Level 1 (YAML frontmatter)**: 항상 시스템 프롬프트에 로드. description만. 트리거 판단용
- **Level 2 (SKILL.md body)**: 관련 있다고 판단 시 로드. 핵심 지시사항
- **Level 3 (references/, scripts/, assets/)**: 필요할 때만 추가 로드
- **적용**: superpowers/ 스킬에 references/ 폴더 추가, 상세 문서 분리

## E2. scripts/ 블랙박스 패턴
- **소스**: anthropics/skills `webapp-testing` 스킬
- **원문**: "Always run scripts with `--help` first. DO NOT read the source until you try running the script first. These scripts can be very large and thus pollute your context window."
- scripts/는 **컨텍스트 윈도우 보호** 장치
- **적용**: 스킬 내 스크립트에 "소스 읽기 금지" 지시 추가

## E3. TRIGGER / DO NOT TRIGGER 패턴
- **소스**: anthropics/skills `claude-api` 스킬
- **원문**:
  ```
  TRIGGER when: code imports `anthropic`/`@anthropic-ai/sdk`/`claude_agent_sdk`,
                or user asks to use Claude API
  DO NOT TRIGGER when: code imports `openai`/other AI SDK,
                       general programming, ML/data-science tasks
  ```
- **적용**: 전 스킬 description에 positive/negative 트리거 명시

## E4. 5 Skill Patterns (Anthropic 공식)
- **소스**: Anthropic Skills Guide Chapter 5
- **Pattern 1: Sequential Workflow** — 순서대로 실행, 단계별 검증 (현재 우리 주력)
- **Pattern 2: Multi-MCP Coordination** — 여러 MCP 서버 조합 (Design→Drive→Linear→Slack)
- **Pattern 3: Iterative Refinement** — 초안→검증→개선 루프, quality threshold까지 반복 (**현재 부재**)
- **Pattern 4: Context-Aware Tool Selection** — 파일 크기/타입에 따라 다른 도구 선택
- **Pattern 5: Domain-Specific Intelligence** — 전문 지식 내장 (금융 컴플라이언스 등)
- **적용**: Pattern 3 (Iterative Refinement) 도입 — 품질 체크 → 재생성 루프

## E5. allowed-tools 필드
- **소스**: Anthropic Skills Guide
- YAML frontmatter에 `allowed-tools: "Bash(python:*) Bash(npm:*) WebFetch"`
- 특정 스킬에서 위험 도구 접근 차단 가능
- **적용**: brainstorming 스킬에서 Edit/Write 차단 (코드 수정 방지)

## E6. evaluations/ 폴더 (스킬 품질 측정)
- **소스**: OpenAI curated skills + anthropics/skills skill-creator
- **skill-creator eval 시스템**: with_skill vs without_skill 블라인드 비교, N회 반복, 분산 분석
- **agents/ 서브에이전트 3역할**: analyzer(패턴 분석), grader(expectations 검증), comparator(A/B 블라인드)
- **scripts/**: `run_eval.py`, `run_loop.py`, `aggregate_benchmark.py`, `generate_report.py`
- **적용**: 스킬 추가/수정 시 자동 평가 파이프라인

## E7. 에이전트 스파 데이
- **소스**: @sysls
- 주기적으로 rules/skills 모순 정리를 에이전트에 위임
- memory-merger 패턴으로 자동화 가능

## E8. Notion Spec-to-Implementation
- **소스**: OpenAI curated skills `notion-spec-to-implementation`
- 5단계: locate spec → parse requirements → create plan → create tasks → track progress
- **references/ 7개 템플릿**: spec-parsing.md, standard-implementation-plan.md, task-creation.md, task-creation-template.md, progress-tracking.md, progress-update-template.md, milestone-summary-template.md

## E9. OpenAI 스킬 파일 구조 표준
- **소스**: OpenAI curated skills 분석
- ```
  skill-name/
  ├── LICENSE.txt
  ├── SKILL.md
  ├── agents/         # 서브에이전트 프롬프트
  │   └── openai.yaml
  ├── references/     # 프레임워크별 참고 문서
  ├── scripts/        # 실행 스크립트
  ├── assets/         # 템플릿, 아이콘
  └── evaluations/    # 자동 테스트
  ```

## E10. agents.md + llms.txt 표준
- **소스**: awesome-copilot `create-agentsmd`, `create-llms`
- **agents.md**: "에이전트를 위한 README" — 프로젝트 개요, 셋업, 테스트, 코드 스타일, 빌드/배포
- **llms.txt**: LLM이 레포를 이해하기 위한 진입점 — H1(프로젝트명) + blockquote(요약) + H2 섹션별 링크
- **Optional 섹션**: LLM이 컨텍스트 축소 시 건너뛸 수 있음을 의미
- **적용**: 우리 6개 프로젝트에 agents.md / llms.txt 생성

## E11. skills.sh 외부 스킬 즉시 도입
- `npx skillsadd anthropics/skills` — frontend-design, mcp-builder, webapp-testing
- `npx skillsadd github/awesome-copilot` — agent-governance, context-map, agentic-eval
- `npx skillsadd am-will/codex-skills` — swarm-planner, parallel-task, context7

## E12. 안티-AI 슬롭 명시적 금지
- **소스**: anthropics/skills `frontend-design`, `web-artifacts-builder`
- Inter/Roboto 폰트 금지, 보라색 그래디언트 금지, 센터 레이아웃 금지
- **적용**: 우리 frontend-design 스킬에도 generic AI aesthetic 금지 목록 추가
