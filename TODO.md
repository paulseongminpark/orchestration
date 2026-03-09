# TODO — 앞으로 하고싶은것

> 최종 수정: 2026-03-09

## 긴급 (2026-03-09)

- [x] **Codex/Gemini CLI 전략 수립** — 실측 완료 (2026-03-09)
  - Codex: `--full-auto` = workspace-write + on-request. 프롬프트 스코프 제한.
  - Gemini: .py 읽기 정상 확인. `.geminiignore` 불필요.
  - 문서: 02_implementation/2026-03-09/0-cli-strategy.md

- [ ] **mcp-memory NDCG 개선** — q051-q075 병목 (NDCG@5=0.227, hit_rate=24%)
  - q001-q025: 0.604 (양호), q026-q050: 0.546, q051-q075: 0.227 (심각)
  - 원인: 긴 서술형 쿼리 + low-ID 노드 매칭 실패
  - 5단계 파이프라인 대상 (ideation부터)


## 우선순위 높음
- [x] daily-memo 파이프라인 문서화 완성
  - [x] architecture.md에 시스템 구조도 추가
  - [x] daily-workflow.md에 워크플로우 통합
  - [x] claude-code-guide.md에 SessionStart hook 예시
  - 완료: 2026-02-18

## 우선순위 높음 (2026-02-22 추가)
- [x] CHANGELOG.md v2.0 내용 업데이트 + orchestration 커밋
  - 완료: 2026-02-22

- [x] docs/SYSTEM-GUIDE.md 종합 사용 가이드 작성
  - 완료: 2026-02-22

- [x] [orchestration] 중복 플러그인 비활성화
  - v3.2에서 coderabbit, feature-dev, code-simplifier, claude-md-management 비활성화
  - 완료: 2026-02-24

- [x] [orchestration] 스킬-에이전트 통합 검토
  - catchup → dispatch로 흡수, skill-creator/hook-creator 삭제
  - orch-skill-builder가 생성 담당
  - 완료: 2026-02-24

## 백로그 (portfolio/tech-review — 별도 세션)

## 인박스 (2026-03-08)

### AI CLI 도구 마스터리
- [ ] Claude Code 고급 세팅 — CLAUDE.md IF-ELSE 디렉토리 패턴, TASK_CONTRACT.md, context bar 커스터마이징
  - ref: https://github.com/ykdojo/claude-code-tips (45+ tips)
  - ref: @sysls 트윗 (CLAUDE.md = IF-ELSE 디렉토리, 세션당 1계약)
- [ ] Codex CLI 고급 활용 — skills 구조, curated skills 참고
  - ref: https://github.com/openai/skills/tree/main/skills/.curated (35개 curated skills)
  - ref: https://skills.sh/ (450K+ 설치, npx skillsadd 패턴)
- [ ] Gemini CLI 활용 확장 — Claude Code fallback으로서의 역할 (Reddit 콘텐츠 등)
- [ ] Google Workspace CLI (gws) 도입 검토 — Gmail/Calendar/Drive CLI 제어, JSON 출력, 에이전트 연동
  - ref: https://github.com/googleworkspace/cli
- [ ] Vercel CLI marketplace — discover→guide→add 3단계, JSON 에이전트 최적화
  - ref: https://vercel.com/changelog/vercel-cli-for-marketplace-integrations-optimized-for-agents
- [ ] 4 AI CLI 통합 대시보드 리서치
  - ref: https://www.reddit.com/r/ClaudeAI/comments/1qsr6gr/built_a_unified_dashboard_for_4_ai_clis_claude/

### AI 도구 + 개인 메모리 연결
- [ ] mcp-memory recall 개선 — importance 가중치 추가 (similarity×w + recency×w + importance×w)
  - ref: @joaomoura CrewAI 메모리 복합 스코어링
- [ ] mcp-memory 메모리 충돌 감지 — 의미적 모순 자동 해소 (PostgreSQL→MySQL 패턴)
- [ ] mcp-memory half-life 망각 — 중요도×시간 함수 기반 자연 감쇠
- [ ] quirk store 패턴 — 사용자 수정사항을 "correction" 노드 타입으로 영구 저장
  - ref: @jamesquint 시맨틱 레이어→컨텍스트 관리
- [ ] Pal 아키텍처 참고 — Classify→Recall→Retrieve→Act→Learn 5단계 루프
  - ref: https://github.com/agno-agi/pal
- [ ] AgentOS 6기둥 체크리스트 — 내구성/격리/거버넌스/영속성/확장성/조합성
  - ref: https://github.com/agno-agi/agentos-docker-template
- [ ] Notion 에이전트 자동화 패턴 — 반복 업무 발견→에이전트 위임, 학습형 라우팅
  - ref: https://maily.so/josh/posts/g0zmw2k3oql

### 연구/읽기
- [ ] Claude Cycles 논문 (Don Knuth, Stanford) — Claude Opus 4.6의 탐색 방법론 31 explorations
  - file: C:/Users/pauls/OneDrive/문서/카카오톡 받은 파일/claude-cycles.pdf
  - 핵심: plan.md 추적, SA→순수수학 전환, fiber decomposition 발견
- [ ] 에이전트 스파 데이 — rules/skills 모순 주기적 정리
- [ ] lessons.md 에이전트 자동 갱신 hook 설계

## 백로그
- 2026-02-24 03:13 테크 리뷰 방식 자체를 바꿔야 하나 아키텍쳐를
- 2026-02-24 02:43 매일 저녁 오늘 배운 사항 - 어떻게 ai 를 핸들링할건지. 에 대하여 기록
- 2026-02-24 02:32 이 그래프 라그 어떻게 구현할지 어떤 효용있는지 https://youtu.be/AISuJHMCWog?si=zoYGdSbPT7oWSXo-
- 2026-02-24 02:32 멀티 세션으로 4개 프로젝트 동시에 tmux 윈도우를 여러 개 만들면 돼요. 이 부분 나도 구현된건지
- 2026-02-24 02:25 일단 현재 만들어놓은거 허점 파악. 잘 돌아가는지
  - 너가 바라보고 있는 범위가 어디냐 → 시스템, 옵시디언, 깃?
  - 범주를 먼저 나눠보자
- 2026-02-24 02:22 깃허브 레포 정리도 한번 해야 한다
  - 안쓰는 폴더, 안쓰는 파일 점검
  - 안에 들어가있는 형식까지 다 점검
- 2026-02-24 02:21 문서 소스 단일화, 폴더 구조 정리, living docs 자동화 완성. 중앙 집중형으로
  - 안쓰는 폴더들 다 제외시키고 (opcode, ytm, n8n 등 삭제)
  - 먼저 지금 에이전트 구조부터 파악
  - home.md에서 모든 걸 다 파악할 수 있게 시스템 구성
- 2026-02-24 02:17 c dev에서 오푸스 1m 토큰으로 작업한다
- 2026-02-24 02:16 옵시디언 리빙 닥 만들기 - 현재 구조 트래킹 하기 어려움
  - memory.md를 sync all과 compressor에 추가할지? → 꼭 다 해야 하나?
  - 스킬들도 점검해야 한다
  - 오케스트레이션 v3.2 만든다 (내일)
- 2026-02-24 01:50 클로드가 내 핸드폰 작업에서 이상한 짓함 - 자기가 막 찾아보려고 함, 내가 보내는 메시지 지멋재로 요약함
- 2026-02-24 01:50 진짜 문제는 AI가 일관성 있고, 내가 지시한 바를 정확한 엣지를 지켜가며 따르게 하느냐의 문제다
- 2026-02-24 01:50 그냥 인박스에만 넣으라고 다른 작업하지 말고
- 2026-02-24 01:49 데일리 메모 인박스 지침도 한번 손보자
- 2026-02-24 01:48 오늘자 테크뉴스 또 말썽이네.. 퍼플렉시티 프롬프트 점검 한번 하자
- 2026-02-22 14:xx [긴급] portfolio에 Tech Review 설계 로직 섹션 추가 — Smart Brevity 방법론, 요일별 큐레이션, keywords-log 중복 방지, Claude와 나눈 대화 스토리텔링으로 기록
- 2026-02-22 13:33 분야 전문성과 기술 전문성 / 미디어 산업에서 테크 기술, 자동차 산업에서 영업 기술 등
- 2026-02-22 02:23 Codex cli 랑 gemini cli 어떻게 사용할건지, perplexity cli 까지. 클로드가 결정하도록. - 최적화의 전략
- 2026-02-22 12:28 오늘자 뉴스 영어 배너 누르면 한국어로 표기됨 - 다시 발생하지않게 조치
  - 내용 이전날이랑 비슷함 (2/20일자랑 비슷함) → 주제 겹치지 않게 하려면?
  - ~습니다 어투가 갑자기 바뀜 (다른 날짜는 ~다로 끝남) → 말투 형식 어떻게 강제?
  - 조사가 얕은 것 같음 → 해결책 제시, 형식 만들기
- 2026-02-21 09:11 데일리 리뷰 ko/en 내용 다름 ...
