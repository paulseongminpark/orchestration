# B. 오케스트레이션 강화

## B1. Classify→Recall→Retrieve→Act→Learn 5단계 루프
- **소스**: Pal 소스코드 (agno-agi/pal — `pal/agent.py` BASE_INSTRUCTIONS)
- **현재**: 상태읽기→프롬프트→실행 (3단계)
- **Pal 구현**: 코드가 아닌 **프롬프트**로 5단계 구현. GPT-5.2가 지시를 따르는 것에 의존
- **Intent-Source 매핑 테이블**:
  - `capture` → SQL만
  - `retrieve` → SQL + Files + Knowledge
  - `connect` → SQL + Files + Gmail + Calendar (멀티소스 종합)
  - `research` → Exa
  - `email_read`/`email_draft` → Gmail + Files (voice)
  - 복합 의도: "Reply to Sarah's email about Project X" = email_read + retrieve + email_draft
- **Recall 단계**: search_knowledge → search_learnings → search_files (절대 건너뛰지 않음)
- **Learn 단계**: 인터랙션 후 자동 업데이트
  - 새 테이블 → `update_knowledge("Schema: pal_X", ...)`
  - 크로스소스 성공 → `update_knowledge("Discovery: Topic", ...)`
  - 사용자 교정 → `save_learning("Correction: ...", ...)` — 최우선순위
- **적용**: Classify(작업 분류) + Learn("이 세션에서 뭘 배웠나" 구조화) 단계 추가

## B2. Wave 기반 DAG 병렬 실행
- **소스**: am-will/codex-skills `parallel-task` 스킬
- **구조**: 태스크 ID + depends_on 배열 → DAG 구축
  ```
  T1: [depends_on: []] Create schema
  T2: [depends_on: []] Install packages
  T3: [depends_on: [T1]] Create repository layer
  T5: [depends_on: [T3, T4]] Implement business logic
  ```
- **실행**: Wave 1(의존성 없는 것 전부 병렬) → 완료 검증 + plan.md 로그 → Wave 2(새로 unblocked) → 반복
- **서브에이전트 안전 규칙**: COMMIT만 PUSH 금지, 자기 파일만 stage (`git add .` 금지), plan.md에 즉시 로그
- **적용**: dispatching-parallel-agents 스킬에 depends_on DAG + Wave 구조 추가

## B3. 롤링 풀 실행 (Super-Swarm)
- **소스**: am-will/codex-skills `super-swarm-spark` 스킬
- **차이**: 의존성을 "인식은 하되 차단하지 않음"
- **최대 12~15 에이전트 동시** — 슬롯 비면 즉시 다음 태스크 투입
- **Context Pack**: 태스크별 canonical 파일 경로 + 인접 태스크 충돌 정보 사전 패키징. 에이전트가 Pack 밖의 파일 만들려면 먼저 보고 필수
- **최종 통합 패스**: 전체 완료 후 충돌 해소, 중복 파일명 정리, 테스트
- **적용**: 대규모 독립 태스크(테스트 생성, 문서 생성 등)에 적합

## B4. LLM Council 합의 시스템
- **소스**: am-will/codex-skills `llm-council` 스킬
- **워크플로우**: Intake 질문 → 플래너 프롬프트 생성 → Claude+Codex+Gemini+OpenCode **각각 독립** 플래닝 → 익명화+순서 랜덤화(position bias 제거) → Judge가 루브릭 기반 통합 → final-plan.md
- **웹 UI 실시간 모니터링**, 30분 세션 유지 필수
- **적용**: 현재 delegate-to-codex/gemini는 "추출"만. Council로 진화시키면 "합의 기반 설계"

## B5. Plan→Verify→Learn + lessons.md 에이전트 갱신
- **소스**: @jackculpan (7원칙)
- **원문**: "수정 받을 때마다 tasks/lessons.md 즉시 업데이트. 완료 선언 전 반드시 작동 증명"
- **'Would a staff engineer approve this?' 자기 검증 질문**
- **적용**: PostToolUse hook에서 "실패 감지 시 lessons 자동 추가". 에이전트가 틀릴 때마다 자기 규칙 갱신

## B6. Context Sub-agent (실행 전 컨텍스트 수집 분리)
- **소스**: @jamesquint 전문
- **원문**: "Before your main agent writes any SQL, dispatch a sub-agent whose only job is to investigate the data landscape. It reads the relevant model files, traces upstream dependencies, checks application code, and returns a structured brief."
- **brief 구성**: tables, columns, join paths, filters, dedup rules, caveats
- **적용**: 모든 구현 전 context-map 생성 의무화 (수정 파일 → 의존성 → 테스트 → 리스크)

## B7. Bug Hunting 3-Agent (find+refute+judge)
- **소스**: @sysls
- **구조**: 찾기(+10점) → 반박(-2배 패널티) → 심판
- **적용**: mcp-memory CRITICAL 이슈 검증, 보안 리뷰, 아키텍처 결정 검증

## B8. Structured-Autonomy-Plan (커밋 단위 계획)
- **소스**: awesome-copilot `structured-autonomy-plan` 스킬
- **각 step = 1 commit + testable increment**. 전체 계획 = 1 PR on dedicated branch
- **연구 가이드**: 서브에이전트 파견하여 코드 컨텍스트/문서/의존성/패턴 80% 확신까지 조사
- **적용**: writing-plans 스킬에 commit-단위 계획 통합

## B9. Plan-Harder Gotchas
- **소스**: am-will/codex-skills `plan-harder` 스킬
- **Phase 4: Gotchas** — 계획 저장 후 "어디서 뭐가 틀어질 수 있는가?" 분석
- "Is there a missing step, dependency, or pitfall?"
- **적용**: writing-plans 스킬 마지막에 gotchas 단계 추가

## B10. 계획 파이프라인 체인
- **소스**: awesome-copilot
- **체인**: PRD → breakdown-epic-arch(아키텍처) → create-implementation-plan(구현) → breakdown-plan(이슈) → breakdown-test(테스트)
- 각 단계의 출력이 다음 단계의 입력. "Related Planning Prompts" 섹션에서 명시적 연결
- **AI-to-AI 통신**: 모호함 제로, 구조화된 식별자 (REQ-, TASK-, ALT-, DEP-), JSON 기계 파싱 최적화

## B11. 26개 Typed 에이전트 (codex-skills)
- **소스**: am-will/codex-skills `agents/agents_config_block.toml`
- **전문 역할 18개**: architect(설계전용, 코드금지), debugger(과학적방법론), scout(최소모델탐색), reviewer(변경금지), frontend, backend, security, refactorer, documenter 등
- **범용 Worker 8개**: worker_xhigh/high/medium/mini + spark 변종
- **모델 계층화**: codex(high)=설계/리뷰, codex-spark(high)=빠른구현, codex-mini(low)=탐색
