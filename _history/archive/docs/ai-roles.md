# AI별 역할

## 역할 매트릭스

| AI | 역할 | 접근 | 쓰기 | 비용 특성 |
|----|------|------|------|----------|
| Claude Code | 실행+기록 | 로컬 파일, Git | 유일 | 턴 당 과금 |
| GPT Plus | 전략, Canvas | GitHub Pages URL | 읽기만 | 무제한 (Plus) |
| Gemini Pro | 대량 검증 | GitHub Pages URL | 읽기만 | 100만 토큰 무료 |
| Perplexity Pro | 리서치 | 웹 + GitHub Pages | 읽기만 | 무제한 (Pro) |

## Claude Code (실행자)

유일하게 파일을 직접 읽고, 쓰고, Git push까지 할 수 있다.

### 에이전트 시스템 (v2.2)

**PROACTIVELY 호출 (자동 감지):**
- code-reviewer (Opus): 구현 완료 감지 시
- commit-writer (Haiku): 커밋 필요 시
- compressor (Sonnet): 세션 마무리 시
- orch-state (Sonnet): 방향 파악 필요 시

**Portfolio:**
- pf-context (Sonnet): 컨텍스트 수집
- pf-reviewer (Opus): 코드/디자인 리뷰
- pf-deployer (Sonnet): 배포 체크

**Orchestration:**
- orch-doc-writer (Opus): 문서 작성
- orch-skill-builder (Opus): 스킬/에이전트 생성

**Monet-lab:**
- ml-experimenter (Opus): 컴포넌트 실험
- ml-porter (Sonnet): 실험 결과 이식

**기타:**
- morning-briefer (Haiku): 전체 브리핑
- content-writer (Opus): 글 작성
- gemini-analyzer (Opus): 대량 분석
- security-auditor: 배포 보안 체크

### Skills (사용자 호출 명령)

| Skill | 동작 |
|-------|------|
| `/morning` | 전체 프로젝트 브리핑 |
| `/sync-all` | orchestration + portfolio + dev-vault 일괄 커밋+푸시 |
| `/verify` | 통합 규칙 검증 (브랜치/STATE/커밋/LOG) |
| `/todo` | TODO.md 관리 + INBOX 동기화 |
| `/docs-review` | stale 문서 점검 |
| `/session-insights` | 토큰 사용량/비용 분석 |

### Hooks (자동)

| 이벤트 | 동작 |
|--------|------|
| SessionStart | 오늘 LOG + 미커밋 상태 + 미반영 결정 출력 |
| PostToolUse (Write/Edit) | context/*.md 변경 감지 알림 |
| SessionEnd | 미커밋 현황 + Auto Memory 분석 |
| PreToolUse (Bash) | 위험 명령 차단 (rm -rf, force push) |

## GPT Plus (사고 확장자)

Canvas로 옵션 비교, 대화형 설계 토론.

## Gemini Pro (검증자)

100만 토큰 컨텍스트로 대량 코드 검증.

## Perplexity Pro (리서처)

웹 검색 + AI 분석 결합, 소스 URL 포함.

## 관련 문서
- [[daily-workflow]] — 실제 사용 예시
- [[claude-code-guide]] — Claude Code 상세
- [[architecture]] — 전체 구조
