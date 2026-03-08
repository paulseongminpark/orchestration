# Phase 4: 거버넌스 + 스킬

> 세션: Main + GM (Gemini 분석)
> 예상 시간: 3시간
> 전제: 없음 (독립, 다른 Phase와 병렬 가능)

---

## P4-01: governance-audit hook

**목표**: PreToolUse에서 5가지 위협 실시간 스캔

### P4-01-a: Gemini로 초안 생성
- [ ] 위의 GM 명령어 실행 → `gm-governance-hook-draft.sh` 생성
- [ ] 초안 검토 + 수정

### P4-01-b: hook 설치
- [ ] `/c/Users/pauls/.claude/hooks/governance-audit.sh` 생성
  - 5가지 위협 카테고리:
    1. `data_exfiltration`: curl/wget + 외부 URL, base64 encode 패턴
    2. `privilege_escalation`: chmod 777, sudo, --dangerously 패턴
    3. `system_destruction`: rm -rf /, drop table, git push --force 패턴
    4. `prompt_injection`: "ignore previous", "you are now" 패턴
    5. `credential_exposure`: .env, API_KEY=, password= 패턴
  - 높은 확신 (≥0.9): 차단 + 로그
  - 중간 확신 (0.6~0.9): 경고 + 로그
  - 로그: `/c/dev/01_projects/01_orchestration/_auto/governance-audit.jsonl`

### P4-01-c: settings.json에 hook 등록
- [ ] PreToolUse hook에 governance-audit.sh 추가
  ```json
  {
    "matcher": "Bash",
    "hooks": [{
      "type": "command",
      "command": "bash /c/Users/pauls/.claude/hooks/governance-audit.sh"
    }]
  }
  ```

### P4-01-d: 테스트
- [ ] 안전한 명령어 → 통과 확인
- [ ] `rm -rf /` 패턴 → 차단 확인
- [ ] `.env` 읽기 패턴 → 경고 확인
- [ ] audit.jsonl에 로그 기록 확인
- [ ] git commit "[orchestration] P4-01: governance-audit hook"

---

## P4-02: 스킬 TRIGGER 패턴 점검

**목표**: 9개 스킬 + superpowers 12개에 TRIGGER/DO NOT TRIGGER 명시

### P4-02-a: Gemini로 현재 상태 분석
- [ ] 위의 GM 명령어 실행 → `gm-skill-trigger-audit.md` 생성
- [ ] 분석 결과 검토

### P4-02-b: 스킬 description 수정
- [ ] 9개 orchestration 스킬 SKILL.md 수정
  - `/morning`: TRIGGER when: 세션 시작, 아침 브리핑 요청 / DO NOT TRIGGER when: 구현 작업 중
  - `/sync`: TRIGGER when: 작업 완료 후, commit 후 / DO NOT TRIGGER when: 작업 진행 중
  - `/todo`: TRIGGER when: TODO 확인/수정 요청 / DO NOT TRIGGER when: 구현 작업 중
  - `/dispatch`: TRIGGER when: 복합 작업, 팀 필요 / DO NOT TRIGGER when: 단순 파일 수정
  - `/compact`: TRIGGER when: 토큰 100K+, 세션 전환 / DO NOT TRIGGER when: 작업 진행 중
  - `/verify`: TRIGGER when: 커밋 전, 배포 전 / DO NOT TRIGGER when: 탐색/리서치 중
  - `/session-insights`: TRIGGER when: 세션 종료 시 / DO NOT TRIGGER when: 작업 초기
  - `/handoff`: TRIGGER when: CLI 전환 시 / DO NOT TRIGGER when: 단일 CLI 작업
  - `/status`: TRIGGER when: 현재 상태 파악 / DO NOT TRIGGER when: 구현 중

### P4-02-c: superpowers 스킬 확인 (수정 불필요하면 skip)
- [ ] brainstorming, writing-plans 등 주요 스킬 description 확인
- [ ] 필요 시 TRIGGER 추가

### P4-02-d: 검증
- [ ] 각 스킬 SKILL.md에 TRIGGER/DO NOT TRIGGER 존재 확인
- [ ] git commit "[orchestration] P4-02: 스킬 TRIGGER 패턴"

---

## P4-03: scripts/ 블랙박스 패턴

**목표**: 스킬 내 scripts/ 폴더가 있으면 소스 읽기 금지 지시

### P4-03-a: scripts/ 있는 스킬 확인
- [ ] `find ~/.claude/skills -name "scripts" -type d` + `.agents/skills`
- [ ] 해당 스킬 SKILL.md에 추가:
  ```
  ## scripts/ 사용법
  Always run scripts with `--help` first.
  DO NOT read the source until you try running the script first.
  These scripts can be very large and pollute your context window.
  ```

### P4-03-b: 검증
- [ ] scripts/ 있는 스킬에 블랙박스 지시 존재 확인
- [ ] git commit "[orchestration] P4-03: scripts 블랙박스 패턴"

---

## Phase 4 검증

- [ ] P4-CX-01: governance hook 안전성 리뷰 (Codex)
- [ ] governance-audit hook 5개 패턴 테스트 통과
- [ ] 9개 스킬에 TRIGGER/DO NOT TRIGGER 존재
- [ ] scripts/ 블랙박스 지시 추가

**Phase 4 완료 기준**:
- [ ] governance-audit.sh 설치 + 5패턴 테스트 PASS
- [ ] 9개 스킬 description 업데이트
- [ ] scripts/ 블랙박스 적용
- [ ] CX 리뷰 PASS
