# D. 거버넌스/보안

## D1. GovernancePolicy 3계층 (allow/deny/review)
- **소스**: awesome-copilot `agent-governance` 스킬
- **구현 코드** (Python):
  ```python
  class PolicyAction(Enum):
      ALLOW = "allow"
      DENY = "deny"
      REVIEW = "review"  # flag for human review

  class GovernancePolicy:
      allowed_tools: list[str]       # allowlist
      blocked_tools: list[str]       # blocklist
      blocked_patterns: list[str]    # content filters
      max_calls_per_request: int = 100
      require_human_approval: list[str]
  ```
- **compose_policies()**: 여러 정책 병합, most-restrictive-wins
- **적용**: rules/ 구조를 policy 객체로 코드화

## D2. AgentOS 거버넌스 3-Tier (실제 구현)
- **소스**: agno-agi/agentos-docker-template + agno 프레임워크 소스
- **Tier 1: Security Key 인증** — `OS_SECURITY_KEY` Bearer 토큰
- **Tier 2: JWT RBAC 인가**
  - `JWTMiddleware`: JWT 검증 + scope 추출
  - Scope 포맷: `resource:action` (글로벌) / `resource:<id>:action` (per-resource) / `resource:*:action` (와일드카드)
  - `agent_os:admin` → 모든 접근 허용
  - 25+ 리소스 타입: agents, teams, workflows, sessions, memories, knowledge, metrics, evals, traces, schedules, approvals
  - `filter_resources_by_access()`: 사용자 scope 기반 리소스 필터링
- **Tier 3: Approval System (Human-in-the-Loop)**
  - `@approval` 데코레이터: 도구에 승인 요구 부착
  - `ApprovalType.required` — blocking. admin 승인까지 run 중단
  - `ApprovalType.audit` — non-blocking. 감사 기록 생성
  - CRUD API: `/approvals` (list, get, resolve, delete, count, polling)
- **적용**: hooks에 blocking approval 도입 (push, PR 시)

## D3. Governance Boundary
- **소스**: Pal 소스코드
- **코드 레벨 거버넌스** (프롬프트로만은 깨질 수 있는 보안 경계를 코드로 강제):
  - `FileTools(enable_delete_file=False)` — 파일 삭제 불가
  - `GmailTools(send_email=False, send_email_reply=False)` — 항상 드래프트만
  - Slack: `enable_send_message=True`만 활성, 나머지 전부 비활성
- **프롬프트 레벨 거버넌스**:
  - "Calendar events with external attendees → always confirm first"
  - "No external attendees = no confirmation needed"
  - "Every query must be scoped to user_id"
- **적용**: 외부 영향(push, PR, 메시지)만 review, 나머지 allow. `--dangerously-skip-permissions`의 지능적 대체

## D4. governance-audit Hook
- **소스**: awesome-copilot `hooks/governance-audit`
- **이벤트**: sessionStart + sessionEnd + userPromptSubmitted
- **5가지 위협 실시간 스캔** (regex 패턴 매칭):
  - data_exfiltration (0.7~0.95)
  - privilege_escalation (0.8~0.95)
  - system_destruction (0.9~0.95)
  - prompt_injection (0.6~0.9)
  - credential_exposure (0.9~0.95)
- **4단계 거버넌스 레벨**: open(로그만) / standard(선택적 차단) / strict(전부 차단) / locked(전부 차단)
- **프라이버시**: 프롬프트 전문 미기록. 매칭된 패턴 스니펫만 `logs/copilot/governance/audit.log` (JSON Lines)
- **적용**: 우리 hooks/에 위협 감지 hook 추가

## D5. Security-Best-Practices 3모드
- **소스**: OpenAI curated skills `security-best-practices`
- **3모드**: passive(작업 중 자동 감지) / active(요청 시 리포트) / fix(수정 제안)
- **references/ 폴더에 프레임워크별 보안 스펙 10개**:
  - Next.js 16.1.x (TypeScript): 11개 감사 영역 (배포→라우팅→인증→CSRF→XSS→캐시→파일→인젝션→SSRF→리다이렉트→CORS)
  - Python: Django, FastAPI, Flask
  - Go: 범용 백엔드
  - JavaScript: Express, React, Vue, jQuery
- **MUST/SHOULD/MAY 규범적 요구사항** + 감사 규칙 (bad patterns, 감지법, 수정법)
- **적용**: security-auditor 에이전트에 3모드 + references/ 통합

## D6. Security-Threat-Model 8단계
- **소스**: OpenAI curated skills `security-threat-model`
- **prompt-template.md**: Senior AppSec engineer 시스템 프롬프트
- **8단계**: Scope→Boundaries→Calibrate→Enumerate→Prioritize→Validate→Mitigate→Quality Check
- **Mermaid 다이어그램 필수**: flowchart TD/LR, `-->` 화살표만
- **리스크 우선순위**: High(pre-auth RCE, auth bypass) / Medium(targeted DoS) / Low(info leak)
- **적용**: 배포 전 자동 threat model 생성

## D7. Security-Ownership-Map
- **소스**: awesome-copilot `security-ownership-map`
- **git history → bipartite graph (people↔files)** → bus factor + co-change clustering
- NetworkX community detection, Jaccard 유사도
- Neo4j/Gephi export (GraphML)
- **적용**: 6개 프로젝트 소유자 가시화, 보안 hotspot 감지
