# C. 컨텍스트 관리 + 프롬프트 캐싱

## C1. Prompt Caching 원칙 — Claude Code 내부 아키텍처 (@trq212)
- **소스**: @trq212 "Lessons from Building Claude Code: Prompt Caching Is Everything" (1.9M views)
- **핵심**: 프롬프트 캐싱 = prefix matching. 순서가 전부
- **Claude Code 프롬프트 순서**: Static system prompt + Tools → CLAUDE.md → Session context → Conversation messages
- **절대 금지**:
  - 시스템 프롬프트에 타임스탬프 넣기
  - 도구 순서 비결정적으로 셔플
  - 도구 추가/제거 (mid-session)
  - 모델 변경 (mid-session — Opus→Haiku 전환 시 전체 캐시 재구축, 더 비쌈)
- **<system-reminder> 패턴**: 시스템 프롬프트 변경 대신 메시지로 업데이트 → 캐시 보존
- **Plan Mode**: tool 유지 + EnterPlanMode/ExitPlanMode를 **tool로** 전환. 도구 정의는 변경 안 함
  - 보너스: 모델이 어려운 문제 감지 시 자율적으로 plan mode 진입 가능
- **Compaction (cache-safe forking)**: 요약 시 **정확히 동일한** system prompt + tools + context 사용 → parent 캐시 재사용. 새 토큰은 compaction prompt만
- **적용**: MEMORY.md 분리가 캐시와도 직결 — 변하지 않는 부분은 앞으로, 변하는 부분은 뒤로

## C2. defer_loading — 도구 토큰 85% 절감
- **소스**: @trq212 + Claude Tool Search API docs
- **현재**: 5서버 58도구 ≈ 55K 토큰 매 턴 풀 로드
- **defer_loading: true** → 도구 스텁(이름만)만 전송 → ToolSearch tool로 발견 시 풀 스키마 로드
- **API 사양**:
  - `tool_search_tool_regex` (정규식, 200자 이내) + `tool_search_tool_bm25` (자연어) 두 변종
  - 최대 10,000개 도구 지원, 요청당 3-5개 반환
  - `mcp_toolset` 타입으로 MCP 서버 도구 일괄 defer 가능
  - 자주 쓰는 3-5개 도구는 non-deferred 유지 권장
- **효과**: 55K → ~8K 토큰 (85%+ 절감)
- **적용**: MCP 5서버 도구를 mcp_toolset으로 일괄 defer 전환

## C3. Compaction API 전체 사양
- **소스**: platform.claude.com/docs/en/build-with-claude/compaction
- **전략**: `compact_20260112`, trigger 기본 150K 토큰 (최소 50K)
- **pause_after_compaction=true**: 요약 생성 후 `stop_reason: "compaction"` 반환 → 추가 콘텐츠 삽입 후 계속
- **커스텀 요약 프롬프트**: `instructions` 필드 → 기본 프롬프트를 **완전 대체** (추가가 아님)
- **캐시 조합**: compaction 블록에 `cache_control: {"type": "ephemeral"}` 추가 가능. 시스템 프롬프트에 별도 breakpoint 두면 compaction 발생 시에도 시스템 프롬프트 캐시 유지
- **토큰 예산 관리**: `n_compactions × TRIGGER_THRESHOLD >= TOTAL_TOKEN_BUDGET`

## C4. Auto-caching (RLanceMartin, Anthropic)
- **소스**: @RLanceMartin X Article (638K views)
- 요청 레벨에 `cache_control` 하나만 놓으면 마지막 cacheable 블록으로 breakpoint 자동 이동
- 대화가 길어져도 breakpoint이 자동으로 따라옴
- 블록 레벨 캐싱(시스템 프롬프트)과 병용 가능
- **Manus CTO 인용**: "캐시 히트율이 프로덕션 AI 에이전트의 가장 중요한 단일 메트릭"

## C5. CLAUDE.md IF-ELSE 디렉토리
- **소스**: @sysls
- **원문**: "CLAUDE.md는 IF-ELSE 디렉토리여야 한다 — 컨텍스트를 직접 담지 말고 어디서 찾을지만 지시"
- **Rules(선호)와 Skills(레시피)만 추가, 나머지는 제거**
- **적용**: MEMORY.md 200줄 → 80줄 + 별도 topic 파일 (memory/tech-review.md, memory/portfolio.md 등)

## C6. TASK_CONTRACT.md
- **소스**: @sysls
- **원문**: "TASK_CONTRACT.md = 테스트+스크린샷+검증 조건 명시, 이것이 충족되기 전까지 세션 종료 금지"
- **적용**: brainstorming 스킬 출력을 contract 문서로 분리

## C7. 세션당 1계약
- **소스**: @sysls
- 장시간 세션 = 무관한 컨텍스트 오염으로 성능 저하
- compact 전에 계약 갱신 또는 새 세션

## C8. Context-Map
- **소스**: awesome-copilot `context-map` 스킬
- 변경 전 매핑: Files to Modify → Dependencies → Test Files → Reference Patterns → Risk Assessment
- "Do not proceed with implementation until this map is reviewed"

## C9. What-Context-Needed
- **소스**: awesome-copilot `what-context-needed` 스킬
- 에이전트가 "이 질문에 답하려면 이 파일들이 필요하다"고 먼저 선언
- Must See (필수) / Should See (도움) / Already Have (이미 있음) / Uncertainties

## C10. 시스템 프롬프트 45% 축소
- **소스**: ykdojo tip 15
- 백업 + 패치 시스템으로 기본 프롬프트 슬림화
- 실제 작업에 더 많은 context 확보

## C11. context/ 디렉토리 패턴 (파일 편집 = 행동 변경)
- **소스**: Pal 소스코드
- `context/voice/email.md`, `context/voice/x-post.md` 등으로 채널별 톤 제어
- **Anti-pattern 금지어**: "synergy", "circle back", "game-changer", "thought leader" 등 명시 금지
- 코드 변경 없이 파일 편집만으로 에이전트 행동 수정
- **templates/**: 회의록, 주간 리뷰, 프로젝트 브리프 등 스캐폴드
