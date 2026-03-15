# Ideation R2 — Auto-Iterate 전체 대상 원자 분해
> 2026-03-15

---

## 섹터 A: 실행 코드 (Hooks — 1,850줄, 14개)

자동 테스트가 가장 쉬운 계층. 입력→출력이 명확하고 exit code로 판정.

### A1. validate_pipeline.py (211줄) ✅ PoC 완료
- **메트릭**: 규칙 정탐/오탐 F1
- **테스트**: fixture 파이프라인 구조 × 시나리오
- **수정 대상**: exempt 목록, 조건 순서, 정규식
- **현재 상태**: F1=1.0 (37 scenarios), baseline에서 4곳 수정

### A2. validate_merged.py (77줄)
- **메트릭**: T1 정탐/오탐 F1
- **테스트**: phase별 merged 폴더 fixture (ideation/impl/review/research × 정상/누락)
- **수정 대상**: 필수 파일 체크 로직, phase 감지
- **시나리오 수 추정**: ~16 (4 phase × 정상/파일누락/자체생성/추가파일)

### A3. validate_output.py (136줄)
- **메트릭**: G1-G5 DONE gate 정탐/오탐 F1
- **테스트**: 90_output/ fixture (정상/누락/pending 미완료)
- **수정 대상**: gate 체크 로직, pending 패턴 매칭
- **시나리오 수 추정**: ~15 (5 gate × 정상/위반/경계)

### A4. pipeline-watch.py (435줄, 가장 큼)
- **메트릭**: 파이프라인 상태 감지 정확도
- **테스트**: 다양한 git staged 파일 조합 → C1/C2/C3 발동 여부
- **수정 대상**: staged 파일 감지, 활성 파이프라인 판정, Living Docs 강제
- **시나리오 수 추정**: ~20 (파이프라인 내/외 파일 × commit 시나리오)

### A5. auto_remember.py (175줄)
- **메트릭**: 신호 감지 F1 (FILE_TYPE_MAP 11종 + BASH_SIGNAL_MAP 9종)
- **테스트**: (tool_name, tool_input, 기대 온톨로지 타입) 쌍
- **수정 대상**: 매핑 패턴, 정규식, 타입 추론 로직
- **시나리오 수 추정**: ~30 (20종 매핑 × 정상/경계/무관)
- **난이도**: 중 — mcp-memory API 호출 모킹 필요

### A6. post_tool_impact.py (223줄)
- **메트릭**: 영향 분석 정확도 (어떤 프로젝트 영향받는지)
- **테스트**: (tool_output, 기대 프로젝트) 쌍
- **수정 대상**: 경로→프로젝트 매핑, 영향 판정 로직
- **시나리오 수 추정**: ~15

### A7. relay.py (99줄)
- **메트릭**: 크로스세션 메시지 전달 성공률
- **테스트**: 송신 메시지 → 수신 파일 존재/내용 일치
- **수정 대상**: 메시지 포맷, 파일 쓰기 로직
- **시나리오 수 추정**: ~10

### A8. session-start.sh (130줄)
- **메트릭**: 시작 출력 정확도 (git status, 파이프라인 상태, 미반영 결정)
- **테스트**: 다양한 git 상태 → 기대 출력 섹션 존재 여부
- **수정 대상**: 출력 포맷, 필터링 로직
- **난이도**: 높 — bash 스크립트, 환경 의존

### A9. session_start_index.py (82줄)
- **메트릭**: index-system 상태 출력 정확도
- **테스트**: 다양한 프로젝트 구조 → 기대 출력
- **수정 대상**: 스캔 범위, 출력 포맷

### A10. governance-audit.sh (63줄)
- **메트릭**: 거버넌스 감사 정확도
- **테스트**: 다양한 규칙 상태 → 감사 결과
- **수정 대상**: 감사 항목, 임계값

### A11. pre-compact.sh (58줄)
- **메트릭**: compact 전 체크 완료율
- **테스트**: compact 전 상태 → 경고/차단 여부
- **수정 대상**: 체크 항목, 임계값

### A12. pre-tool-use.sh (81줄)
- **메트릭**: 사전 체크 정확도
- **테스트**: 다양한 tool_name → 체크 결과
- **수정 대상**: 필터링 조건

### A13. notify-sound.py (21줄)
- **auto-iterate 부적합** — 기능이 단순 (소리 재생), 메트릭 정의 불가

### A14. post-tool-live-context.sh (59줄)
- **메트릭**: 라이브 컨텍스트 업데이트 정확도
- **테스트**: tool 실행 후 컨텍스트 파일 변경 여부
- **수정 대상**: 업데이트 트리거 조건

---

## 섹터 B: 선언적 설정 (Agents 15개, Skills 17개, Rules 3개)

프롬프트 품질은 직접 측정이 어렵다. 하지만 **구조적 속성**은 측정 가능.

### B1. Agent 프롬프트 — 구조 검증
- **메트릭**: 필수 섹션 존재율, 도구 참조 정합성
- **테스트**: 각 agent.md → (description 존재, tools 섹션 유효, 출력 형식 명시)
- **수정 대상**: 프롬프트 구조, 도구 목록
- **원자 항목**:
  - B1a. description 필드 존재 + 길이 적정 (15개)
  - B1b. tools 목록이 실제 존재하는 도구와 일치 (15개)
  - B1c. 출력 형식(Write/Edit/Bash) 명시 여부 (15개)
  - B1d. model 지정 vs 미지정 (haiku/sonnet/opus) 적정성 (15개)

### B2. Agent 프롬프트 — 실행 품질
- **메트릭**: agent 호출 → 기대 결과 패턴 매칭
- **테스트**: 고정 입력 → agent 실행 → 출력에 기대 패턴 존재
- **수정 대상**: 프롬프트 문구, 지시 순서
- **원자 항목**:
  - B2a. commit-writer: git diff → 커밋 메시지 컨벤션 매칭 `[project] 설명` (1765줄)
  - B2b. code-reviewer: 코드 → 리뷰 결과에 필수 섹션 존재 (2137줄)
  - B2c. compressor: 컨텍스트 → 압축 결과에 핵심 항목 보존 (4658줄)
  - B2d. orch-state: STATE.md → 다음 3개 액션 제안 품질 (2097줄)
  - B2e. linker: 변경 → 크로스세션 매핑 정확도 (2431줄)

### B3. Skill 워크플로우 — 구조 검증
- **메트릭**: 스킬 정의 파일 구조 정합성
- **테스트**: 각 skill/ → (frontmatter 유효, 단계 명시, 입출력 정의)
- **원자 항목**:
  - B3a. frontmatter 유효성 (name, description, trigger 존재) (17개)
  - B3b. 참조 파일/경로 존재 여부 (17개)
  - B3c. 스킬 간 순환 참조 없음 (17개)

### B4. Rules — 정합성
- **메트릭**: 규칙 파일과 실제 시스템 상태 일치율
- **테스트**: rules/*.md 내용 → 실제 설정 교차 검증
- **원자 항목**:
  - B4a. pipeline-rules.md ↔ phase-rules.json 일치 (자동 생성이지만 drift 가능)
  - B4b. common-mistakes.md 내 경로 유효성 (예: /c/dev/... 경로 존재)
  - B4c. workflow.md 내 스킬/에이전트 이름 유효성

---

## 섹터 C: 지식 구조 (Memory, Ontology, Config)

### C1. Memory 파일 — 품질
- **메트릭**: frontmatter 유효성, 참조 정합성, 중복도
- **테스트**: memory/*.md → (frontmatter 파싱, 참조 경로 존재, 내용 중복 감지)
- **원자 항목**:
  - C1a. frontmatter 3필드 존재 (name, description, type) (18개)
  - C1b. MEMORY.md 인덱스 ↔ 실제 파일 일치 (누락/고아 감지)
  - C1c. 파일 간 내용 중복도 (cosine similarity 또는 키워드 겹침)
  - C1d. description 품질 — 실제 내용과 description 일치도

### C2. mcp-memory 온톨로지 — 정합성
- **메트릭**: 타입 커버리지, 관계 정밀도
- **테스트**: 기존 169 tests + 추가 쿼리 셋
- **원자 항목**:
  - C2a. recall() 정확도 — (질의, 기대 노드) 테스트 셋 (precision@k)
  - C2b. generic 관계 비율 — 87.2%에서 감소시킬 수 있는가
  - C2c. 타입 분포 균형 — 15 active 타입의 사용 빈도 편차
  - C2d. 관계 정밀화 — "relates_to" → 구체 관계로 변환 가능한 비율

### C3. phase-rules.json — 자기 일관성
- **메트릭**: 규칙 간 충돌 수, 순환 의존 수
- **테스트**: 모든 규칙 조합 시뮬레이션 → deadlock 감지
- **원자 항목**:
  - C3a. exempt 목록 상호 참조 (I1↔N17 같은 순환 → 방금 발견한 것)
  - C3b. phase 대역 겹침/간극 없음
  - C3c. trigger 조건 중복/충돌
  - C3d. error_msg 일관성 (포맷 통일)

### C4. config.json — 최적화
- **메트릭**: 설정 조합별 성능/비용
- **원자 항목**: 현재 `{"model": "sonnet"}` 1줄. auto-iterate 부적합 (변경 영향이 너무 큼)

### C5. keybindings.json — 충돌 감지
- **메트릭**: 키 조합 충돌 수
- **테스트**: 모든 바인딩 파싱 → 중복 감지
- **원자 항목**:
  - C5a. 동일 키 조합에 다른 액션 매핑 (충돌)
  - C5b. chord 시퀀스 접두사 충돌

---

## 섹터 D: 프로젝트 건강 (Living Docs, Git, 구조)

### D1. Living Docs 준수율
- **메트릭**: STATE.md + CHANGELOG.md 존재/갱신일 기준
- **테스트**: 11개 프로젝트 × (STATE 존재, CHANGELOG 존재, 최근 갱신)
- **원자 항목**:
  - D1a. STATE.md 존재 (현재 5/11 = 45%)
  - D1b. CHANGELOG.md 존재
  - D1c. 최근 30일 내 갱신 여부
  - D1d. STATE.md 필수 섹션 존재 (버전, 상태, 인벤토리)

### D2. Git 커밋 메시지 컨벤션
- **메트릭**: `[project] 설명` 패턴 준수율
- **테스트**: `git log --oneline -100` → 패턴 매칭
- **수정 대상**: commit-writer agent 프롬프트
- **원자 항목**:
  - D2a. [project] 접두사 존재율
  - D2b. 프로젝트 이름 유효성 (실제 프로젝트명과 일치)
  - D2c. 메시지 길이 적정성

### D3. 프로젝트 구조 정합성
- **메트릭**: CLAUDE.md 프로젝트 목록 ↔ 실제 폴더 일치율
- **테스트**: CLAUDE.md 파싱 → 실제 01_projects/ 폴더와 교차
- **원자 항목**:
  - D3a. CLAUDE.md에 있는데 폴더 없는 프로젝트 (고아 참조)
  - D3b. 폴더 있는데 CLAUDE.md에 없는 프로젝트 (미등록)
  - D3c. 브랜치 정보 일치 (main/master)

### D4. 루트 오염도
- **메트릭**: C:\dev 루트의 고아 파일 수
- **테스트**: 알려진 정상 파일/폴더 목록 vs 실제 → 차집합
- **원자 항목**:
  - D4a. .png 스크린샷 수 (현재 47개)
  - D4b. null, log 파일 존재
  - D4c. 정체 미확인 폴더 (conductor/ 등)

---

## 섹터 E: 크로스시스템 정합성

### E1. index-system 경로 해결
- **메트릭**: `python -m src.cli refs <path>` 성공률
- **테스트**: 알려진 경로 N개 → 기대 관계 존재
- **원자 항목**:
  - E1a. 프로젝트 간 의존성 정확도
  - E1b. 고아 노드 감지 (참조는 있지만 실체 없음)
  - E1c. 순환 의존 감지

### E2. CLAUDE.md ↔ 실제 시스템 drift
- **메트릭**: 문서에 적힌 것과 실제 상태의 차이
- **테스트**: CLAUDE.md 에이전트/스킬/hook 목록 → 실제 파일 존재 교차
- **원자 항목**:
  - E2a. 에이전트 목록 일치 (15개)
  - E2b. 스킬 목록 일치
  - E2c. hook 목록 일치
  - E2d. 프로젝트 경로 유효성

### E3. mcp-memory ↔ 파일 시스템 정합성
- **메트릭**: 메모리 노드가 참조하는 파일/경로 존재율
- **테스트**: 모든 노드의 메타데이터에서 경로 추출 → 존재 확인
- **원자 항목**:
  - E3a. 경로 참조 유효성
  - E3b. 프로젝트명 참조 유효성
  - E3c. 날짜 참조 일관성 (미래 날짜 없음 등)

---

## 섹터 F: 런타임 품질 (측정 어렵지만 가치 높음)

### F1. Compact 정보 보존율
- **메트릭**: compact 전 핵심 항목 N개 → compact 후 존재율
- **테스트**: 알려진 컨텍스트 → compact → 핵심 키워드/결정 존재 체크
- **원자 항목**:
  - F1a. 결정 사항 보존율
  - F1b. 파일 경로 보존율
  - F1c. 미결 질문 보존율

### F2. Restore 정보 복원율
- **메트릭**: restore 후 핵심 항목 복원율 + wall-clock 시간
- **테스트**: save_session → restore → 핵심 항목 체크리스트
- **원자 항목**:
  - F2a. 세션 목표 복원
  - F2b. 활성 파이프라인 상태 복원
  - F2c. 미결 질문 복원
  - F2d. 복원 소요 시간

### F3. 에이전트 토큰 효율
- **메트릭**: 작업 완료에 소비된 토큰 수
- **테스트**: 고정 작업 → agent 실행 → 토큰 카운트
- **auto-iterate 가능**: 프롬프트를 줄이면서 같은 결과를 내는 방향

---

## 전체 카탈로그 요약

| 섹터 | 원자 항목 수 | 자동화 난이도 | 가치 |
|---|---|---|---|
| A. Hooks (실행 코드) | 13 hook × ~15 시나리오 = ~195 | ⭐ 쉬움 | 높음 — 오탐 직접 제거 |
| B. Agents/Skills/Rules | 15+17+3 × ~4 속성 = ~140 | ⭐⭐ 중간 | 중간 — 구조 검증 |
| C. 지식 구조 | ~15 원자 항목 | ⭐⭐ 중간 | 높음 — 정합성 핵심 |
| D. 프로젝트 건강 | ~15 원자 항목 | ⭐ 쉬움 | 중간 — 위생 관리 |
| E. 크로스시스템 | ~12 원자 항목 | ⭐⭐⭐ 어려움 | 매우 높음 — drift 감지 |
| F. 런타임 품질 | ~10 원자 항목 | ⭐⭐⭐ 어려움 | 매우 높음 — 핵심 경험 |

**총 ~390 원자 시나리오, 6 섹터.**

---

## 접근 전략 — 섹터별

### 섹터 A (Hooks): PoC 패턴 복제
validate_pipeline.py에서 증명한 패턴을 나머지 12개 hook에 복제:
1. fixture builder 작성
2. 시나리오 정의 (정상/위반/경계/오탐)
3. F1 측정 스크립트
4. program.md 작성
5. iteration 실행

**우선순위**: A4(pipeline-watch, 435줄) > A5(auto_remember, 175줄) > A2(validate_merged) > A3(validate_output)

### 섹터 B (선언적 설정): 정적 분석 도구
프롬프트 "품질"은 주관적이지만, **구조 정합성**은 객관적:
1. agent/skill 파일 파서 작성
2. 필수 필드 체크리스트
3. 참조 유효성 검증 (도구 이름, 파일 경로)
4. B2 실행 품질은 benchmark 시나리오 셋 필요

**우선순위**: B4(Rules 정합성) > B1(Agent 구조) > B3(Skill 구조) > B2(실행 품질)

### 섹터 C (지식 구조): 자기 일관성 체커
1. C1(Memory) — frontmatter 파서 + 인덱스 교차 + 중복 감지
2. C3(phase-rules.json) — 규칙 시뮬레이터 (방금 순환 의존 발견한 것의 일반화)
3. C2(mcp-memory) — 기존 테스트에 recall 테스트 셋 추가

**우선순위**: C3(규칙 충돌) > C1(Memory 품질) > C2(온톨로지)

### 섹터 D (프로젝트 건강): 원샷 스크립트
1. Living Docs 스캐너 (존재/갱신일/필수 섹션)
2. 커밋 메시지 감사
3. CLAUDE.md ↔ 폴더 교차
4. 루트 오염 카운터

**이건 auto-iterate보다 health-check 대시보드에 가깝다.**

### 섹터 E (크로스시스템): drift 감지기
1. CLAUDE.md 파싱 → 실제 파일 존재 교차 (간단)
2. index-system 경로 해결 테스트 (CLI 있음)
3. mcp-memory 경로 유효성 (API 있음)

**우선순위**: E2(CLAUDE.md drift) > E1(index-system) > E3(memory 참조)

### 섹터 F (런타임): 가장 어렵지만 가장 가치 높음
실제 세션 시뮬레이션이 필요. Phase 2 (자동화 루프 완성 후) 대상.

---

---

## 섹터 G: 외부 서비스 연동

### G1. GitHub Actions — tech-review
- **워크플로우**: `sync-claude-to-main.yml` (daily-memo 처리)
- **메트릭**: 최근 N회 실행 성공률, 평균 실행 시간
- **테스트**: `gh run list --workflow=sync-claude-to-main.yml --json status`
- **원자 항목**:
  - G1a. 실행 성공률 (최근 30회)
  - G1b. 실패 시 에러 패턴 분류 (네트워크/인증/로직)
  - G1c. 실행 시간 추세 (느려지고 있나)

### G2. GitHub Actions — portfolio
- **워크플로우**: `deploy.yml` (Vercel 배포)
- **메트릭**: 배포 성공률, 빌드 시간
- **원자 항목**:
  - G2a. 배포 성공률 (최근 30회)
  - G2b. 빌드 시간 추세
  - G2c. 빌드 에러 패턴

### G3. Vercel 배포 상태
- **메트릭**: 사이트 응답 시간, 빌드 성공률
- **테스트**: `curl -o /dev/null -s -w '%{time_total}' https://paulpark.dev`
- **원자 항목**:
  - G3a. 사이트 응답 시간 (200ms 이하?)
  - G3b. HTTPS 인증서 유효 기간
  - G3c. 최근 배포 시간

### G4. MCP 서버 건강
- **대상**: gmail, memory(mcp-memory), serena
- **메트릭**: 응답 시간, 에러율
- **원자 항목**:
  - G4a. mcp-memory 응답 시간 (recall, save 각각)
  - G4b. serena 연결 상태 + 응답 시간
  - G4c. gmail MCP 연결 상태
  - G4d. MCP 서버 시작 시간 (세션 시작 bottleneck?)

### G5. Plugins 건강
- **대상**: Superpowers, Playwright, Context7, Frontend Design, Vercel
- **메트릭**: 도구 호출 성공률
- **원자 항목**:
  - G5a. Context7 resolve-library-id 성공률
  - G5b. Playwright browser_navigate 성공률
  - G5c. 각 플러그인 초기화 시간

### G6. GitHub API
- **메트릭**: `gh` CLI 명령 성공률, rate limit 여유분
- **원자 항목**:
  - G6a. rate limit 잔여 (X-RateLimit-Remaining)
  - G6b. PR/issue 작업 성공률
  - G6c. API 응답 시간

---

## 섹터 H: 환경/인프라

### H1. WezTerm 설정
- **파일**: `02_programs/03_wezterm/wezterm.lua`
- **메트릭**: 설정 문법 오류 수, 미사용 설정 항목
- **원자 항목**:
  - H1a. Lua 문법 유효성 (`luacheck` 또는 파싱)
  - H1b. 키바인딩 충돌
  - H1c. 폰트/색상 참조 유효성

### H2. tmux 설정
- **메트릭**: 세션/윈도우/pane 구조 최적성
- **원자 항목**:
  - H2a. 세션 수 적정성
  - H2b. 좀비 세션 존재
  - H2c. pane 레이아웃 일관성

### H3. Git 리포지토리 건강
- **대상**: 11개 프로젝트 × git 상태
- **원자 항목**:
  - H3a. uncommitted 변경 수 (프로젝트별)
  - H3b. untracked 파일 수
  - H3c. remote와의 동기화 상태 (ahead/behind)
  - H3d. 브랜치 수 (사용 안 하는 브랜치)
  - H3e. .gitignore 커버리지 (민감 파일 누출)

### H4. 디스크 공간
- **원자 항목**:
  - H4a. 99_archive/ 크기 (2.6GB)
  - H4b. 03_llm/ 크기 (63GB)
  - H4c. node_modules/ 크기 (portfolio)
  - H4d. .git/ 크기 (프로젝트별)
  - H4e. 전체 C:\dev 크기 추세

### H5. Python 환경
- **원자 항목**:
  - H5a. Python 버전 일관성
  - H5b. pip 패키지 보안 취약점 (`pip audit`)
  - H5c. 가상환경 존재/활성 상태

---

## 섹터 I: 보안

### I1. 자격증명 노출
- **알려진 위험**: gcp-oauth.keys.json.json, ytm_migrate/*.json
- **원자 항목**:
  - I1a. .env 파일 git tracked 여부
  - I1b. API 키 패턴 감지 (정규식: `[A-Za-z0-9_]{20,}`)
  - I1c. .gitignore에 민감 패턴 포함 여부
  - I1d. 커밋 이력에 자격증명 존재 (`git log -p | grep`)

### I2. 의존성 보안
- **원자 항목**:
  - I2a. npm audit (portfolio)
  - I2b. pip audit (mcp-memory, index-system)
  - I2c. 알려진 CVE 존재

### I3. 접근 제어
- **원자 항목**:
  - I3a. GitHub repo 공개/비공개 상태
  - I3b. Pages URL로 민감 정보 노출 여부
  - I3c. MCP 서버 인증 설정

---

## 섹터 J: Obsidian 볼트

### J1. 볼트 구조 정합성
- **원자 항목**:
  - J1a. HOME.md 프로젝트 테이블 ↔ 실제 프로젝트 일치
  - J1b. 깨진 내부 링크 (`[[broken]]`)
  - J1c. 고아 노트 (어디서도 링크 안 됨)
  - J1d. 플러그인 설정 유효성

### J2. HOME.md (볼트 허브)
- **메트릭**: 프로젝트 테이블 정확도
- **원자 항목**:
  - J2a. 버전 정보 일치 (STATE.md와)
  - J2b. 상태 정보 일치
  - J2c. 경로 정보 유효

---

## 섹터 K: 메타 — 측정 시스템 자체

### K1. 테스트 스위트 품질
- **메트릭**: 시나리오 커버리지, 테스트 실행 시간
- **원자 항목**:
  - K1a. 각 hook의 코드 라인 대비 시나리오 수 (커버리지 밀도)
  - K1b. 테스트 실행 시간 (전체 스위트)
  - K1c. flaky test 비율 (같은 입력, 다른 결과)
  - K1d. 시나리오 간 중복도

### K2. auto-iterate 프레임워크 자체
- **원자 항목**:
  - K2a. program.md 포맷 준수율
  - K2b. 실험 로그 완전성
  - K2c. keep/discard 판정 정확성 (사후 검증)

### K3. 측정 대시보드 건강
- **원자 항목**:
  - K3a. 마지막 측정 시간 (각 섹터)
  - K3b. 메트릭 추세 (개선/악화/정체)
  - K3c. 측정 실패율

---

## 완전한 카탈로그 — 최종 요약

| 섹터 | 범위 | 원자 항목 | 난이도 | 가치 | 접근 |
|---|---|---|---|---|---|
| **A** Hooks | 13 hook, 1850줄 | ~195 시나리오 | ⭐ | 높음 | fixture + F1 |
| **B** 선언적 설정 | 35 파일 | ~140 속성 | ⭐⭐ | 중간 | 정적 분석 |
| **C** 지식 구조 | memory+ontology+rules | ~15 항목 | ⭐⭐ | 높음 | 일관성 체커 |
| **D** 프로젝트 건강 | 11 프로젝트 | ~15 항목 | ⭐ | 중간 | health-check |
| **E** 크로스시스템 | 문서↔실제 | ~12 항목 | ⭐⭐⭐ | 매우 높음 | drift 감지 |
| **F** 런타임 품질 | compact/restore | ~10 항목 | ⭐⭐⭐ | 매우 높음 | 시뮬레이션 |
| **G** 외부 서비스 | GH Actions/Vercel/MCP | ~18 항목 | ⭐⭐ | 높음 | API 모니터링 |
| **H** 환경/인프라 | terminal/git/disk | ~18 항목 | ⭐ | 중간 | 스크립트 |
| **I** 보안 | 자격증명/의존성 | ~10 항목 | ⭐⭐ | 매우 높음 | 감사 |
| **J** Obsidian | 볼트 구조/링크 | ~7 항목 | ⭐ | 중간 | 파서 |
| **K** 메타 | 측정 시스템 자체 | ~9 항목 | ⭐⭐ | 높음 | 자기 참조 |

**총: 11 섹터, ~450 원자 항목.**

---

## 구현 로드맵 제안

### Wave 1: 즉시 가능 (인프라 있음)
A1-A4 (hooks F1) + D1-D4 (health-check) + H3 (git 건강) + I1 (자격증명)

### Wave 2: 도구 1개 만들면 가능
B1,B3,B4 (정적 분석기) + C1,C3 (일관성 체커) + E2 (drift 감지) + J1-J2 (Obsidian)

### Wave 3: 외부 연동 필요
G1-G6 (외부 서비스 모니터링) + A5-A8 (복잡한 hooks) + I2 (의존성 감사)

### Wave 4: 시뮬레이션 필요
B2 (agent 실행 품질) + F1-F3 (런타임) + K1-K3 (메타)

---

## 열린 질문

1. **프레임워크 위치**: `~/.claude/tests/auto-iterate/` vs 프로젝트 내?
2. **실행 주기**: 매 세션 시작? daily cron? 수동?
3. **대시보드**: 결과를 어디에? STATE.md 섹션? 별도 파일? Obsidian?
4. **섹터 우선순위**: Wave 순서대로? 아니면 가치 기준?
5. **자동화 수준**: health-check(측정만) vs auto-iterate(측정+수정+keep/discard)?
