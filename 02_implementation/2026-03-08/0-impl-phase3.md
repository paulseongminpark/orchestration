# Phase 3: 학습 루프

> 세션: Main (이 세션)
> 예상 시간: 4시간
> 전제: 없음 (Phase 2와 병렬 가능, A9만 Phase 2 후)

---

## P3-01: TASK_CONTRACT.md 템플릿

**목표**: 세션 시작 시 자동으로 계약 프롬프트 제안

### P3-01-a: 템플릿 파일 생성
- [ ] `~/.claude/projects/C--dev/memory/templates/task-contract.md` 생성
  ```markdown
  # TASK_CONTRACT — {날짜} {세션목표}

  ## 목표
  {1~2문장으로 이 세션에서 달성할 것}

  ## 완료 조건
  - [ ] {테스트/검증 조건 1}
  - [ ] {테스트/검증 조건 2}
  - [ ] {테스트/검증 조건 3}

  ## 범위 밖 (이 세션에서 하지 않을 것)
  - {유혹될 수 있지만 하지 않을 것}

  ## 완료 선언 전 필수
  - [ ] 완료 조건 전부 체크
  - [ ] Living Docs 갱신 (해당 시)
  - [ ] git commit (변경 있을 시)
  ```

### P3-01-b: SessionStart hook에 계약 알림 추가
- [ ] session-start.sh에 추가:
  ```bash
  echo "📋 TASK_CONTRACT 작성 권장 — 세션 목표와 완료 조건을 먼저 정의하세요"
  ```

### P3-01-c: 검증
- [ ] 새 세션 시작 시 계약 알림 출력 확인
- [ ] git commit "[orchestration] P3-01: TASK_CONTRACT 템플릿 + hook"

---

## P3-02: Learn 단계 프롬프트

**목표**: 세션 종료 전 "뭘 배웠나" 자동 추출

### P3-02-a: compressor 에이전트에 Learn 단계 추가
- [ ] `.agents/compressor/agent.md` 수정
  - 기존 9단계 압축 후, 10단계 추가:
  ```
  ## 10. Learn 단계
  세션에서 발견한 것을 3줄로 요약:
  1. 새로 알게 된 것 (discovery)
  2. 실패에서 배운 것 (lesson)
  3. 다음에 다르게 할 것 (improvement)

  이 3줄을 mcp-memory에 remember(type="Insight", tags="session-learning") 저장.
  ```

### P3-02-b: 검증
- [ ] /compact 실행 시 Learn 단계 출력 확인
- [ ] mcp-memory에 session-learning 노드 저장 확인
- [ ] git commit "[orchestration] P3-02: compressor Learn 단계"

---

## P3-03: lessons.md 자동 축적

**목표**: 실패 패턴을 자동으로 누적 기록

### P3-03-a: lessons.md 파일 생성
- [ ] `/c/dev/01_projects/01_orchestration/lessons.md` 생성
  ```markdown
  # Lessons — 자동 축적 교훈

  > 에이전트 실패, 사용자 교정, 반복 실수에서 자동 추출.
  > compressor Learn 단계에서 갱신.

  ## 최근 교훈 (최대 20개, FIFO)

  (자동 추가됨)
  ```

### P3-03-b: compressor Learn 단계에서 lessons.md 갱신
- [ ] Learn 단계 출력 중 "실패에서 배운 것"을 lessons.md에 append
  - 형식: `- [{날짜}] {교훈 1줄}`
  - 20개 초과 시 가장 오래된 것 제거

### P3-03-c: 검증
- [ ] lessons.md 존재 확인
- [ ] compressor 실행 후 lessons.md에 항목 추가 확인
- [ ] git commit "[orchestration] P3-03: lessons.md 자동 축적"

---

## P3-04: Memory-Merger 초안 (Phase 2 완료 후)

**목표**: 성숙한 memory → rules 자동 승격 메커니즘 설계

### P3-04-a: Merger 로직 설계
- [ ] mcp-memory에서 Signal→Pattern 승격 후보 식별 기준:
  - 같은 태그로 3회 이상 recall된 Signal
  - 30일 이상 경과
  - confidence ≥ 0.8
- [ ] 승격 후보 → 사용자에게 제안 (자동 승격 아님)
- [ ] 승격 시: memory에서 제거 + KNOWLEDGE.md 또는 rules/ 에 추가

### P3-04-b: analyze_signals 확장
- [ ] mcp-memory의 analyze_signals 도구에 "승격 후보" 출력 추가
  - 현재: 시그널 분석 + 패턴 제안
  - 추가: "승격 준비된 노드" 리스트

### P3-04-c: 검증
- [ ] analyze_signals 실행 시 승격 후보 출력 확인
- [ ] 실제 승격 1건 테스트 (수동)
- [ ] git commit "[mcp-memory] P3-04: Memory-Merger 초안"

---

## Phase 3 검증

- [ ] P3-CX-01: hook 안전성 리뷰 (Codex)
- [ ] TASK_CONTRACT 알림 동작 확인
- [ ] Learn 단계 mcp-memory 저장 확인
- [ ] lessons.md 자동 갱신 확인

**Phase 3 완료 기준**:
- [ ] 새 세션 시작 시 TASK_CONTRACT 알림
- [ ] /compact 시 Learn 3줄 + mcp-memory 저장
- [ ] lessons.md에 최소 1건 자동 추가
- [ ] analyze_signals에 승격 후보 표시
