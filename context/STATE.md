# STATE — AI Orchestration System

## 지금 상태 (2026-02-17 기준)

**완료**
- Phase 1: 폴더 구조 마이그레이션 (Jeff Su 방법론)
- Phase 2: CLAUDE.md 재작성 (글로벌 4줄 + rules/ + 프로젝트별 + agents)
- Phase 3: Skills 구현 (/sync, /handoff, /status, /morning)
- Phase 4: Hooks + permissions.deny 설정
- Phase 5: Obsidian Junction + Git post-commit hook
- Phase 6: Multi-AI 프롬프트 (GPT/Gemini/Perplexity)
- 3-Layer 로깅 시스템 (STATE + LOG + Evidence)
- GitHub repo rename (portfolio_ui_test_v2 → portfolio_20260215)
- GitHub repo archive (구 portfolio)
- ai-config repo 생성 (private) + Obsidian 볼트
- 학습 문서 8개 생성 (docs/)
- AI 프롬프트 7개 생성/갱신
- 구 시스템 잔재 아카이브 (hooks, agents, AI_작업실)
- Phase 7: 검증 시스템 (/verify, /verify-project-rules, /verify-log-format)
- /sync-all 글로벌화 (어디서든 실행 가능)
- kimoring-ai-skills 패턴 적용 (verify-* 스킬 구조)

**다음 할 일**
- /verify 스킬 실전 테스트 (orchestration, portfolio 프로젝트)
- /sync에 자동 검증 통합 확인
- verify-state-sync 스킬 추가 (STATE.md ↔ 실제 상태 일치)
- Obsidian에서 볼트 사용성 확인 (docs/ 학습 시작)
- Packet 흐름 실전 테스트 (GPT → Claude → STATE)

**막힌 것**
- 없음

---

## 시스템 작동 방식

**데이터 흐름**
```
Claude Code (유일한 쓰기)
→ STATE.md + LOG 갱신
→ git commit
→ post-commit hook → auto push
→ GitHub → GitHub Pages
→ GPT/Gemini/Perplexity (URL로 읽기)
→ Obsidian (Junction으로 실시간 보기)
```

**3-Layer 로깅**
```
Layer 1: STATE.md      — "지금 어디인가" (고수준)
Layer 2: logs/날짜.md  — "언제 뭘 왜 했는가" (상세, 시간순)
Layer 3: 03_evidence/  — 원본 대화 전문 (raw, 로컬)
```

**폴더 구조**
```
C:\dev\
├── 01_projects\01_orchestration\  (Git: orchestration)
├── 01_projects\02_portfolio\      (Git: portfolio_20260215)
├── 02_ai_config\                  (Git: ai-config, Obsidian 볼트)
├── 03_evidence\                   (로컬 전용)
└── 99_archive\                    (구 시스템 백업)
```

**역할**
- Claude Code: 실행 + 기록 (유일한 쓰기)
- GPT Plus: 사고 확장, Canvas, Packet 생성
- Gemini Pro: 대량 검증 (100만 토큰)
- Perplexity Pro: 리서치 + 교차검증

**핵심 원칙**
- SoT = Git (context/STATE.md)
- 쓰기 = Claude Code만
- 사고는 휘발, 기록은 남음
- 토큰은 자원 (CLAUDE.md 4줄)
- 구조가 규율을 강제

---

## 과거 결정

**2026-02-16**
- STATE.md URL 전환: GitHub Pages → raw.githubusercontent.com (GPT 읽기 안정성 개선)

**2026-02-15**
- 오케스트레이션 재설계 전체 실행 (Phase 1-6)
- SoT 전환: Obsidian → Git
- LOGS/TODAY 폐기 → 3-Layer 로깅 (STATE + LOG + Evidence)
- CLAUDE.md 축소: 146줄 → 4줄 (95% 토큰 절감)
- Jeff Su 방법론 채택 (5레벨 MAX, 2자리 넘버링, 99=Archive)
- .claudeignore 대신 permissions.deny
- .claude/commands/ 대신 .claude/skills/
- Symlink 대신 Junction (관리자 권한 불필요)

**2026-02-12**
- 로그 이원화: LOGS (한줄요약) + EVIDENCE (세션상세)
- push-state.ps1 통합 자동화

**2026-02-10**
- Obsidian 단일 볼트 통합
- Auto-Logging 도입
