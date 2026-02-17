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
- Phase 8: 문서 구조 확장 (PLANNING.md, KNOWLEDGE.md)
- SuperClaude Framework 패턴 적용 (문서 3분화)
- Phase 9: 행동 모드 스킬 (/token-mode, /research)

**다음 할 일**
- 전체 시스템 실전 테스트 (/verify, /token-mode, /research)
- PLANNING.md 지속 업데이트 (새 결정 기록)
- Obsidian 볼트 사용성 확인 (docs/ 학습)
- Packet 흐름 실전 테스트 (GPT → Claude → STATE)
- 포트폴리오 프로젝트 본격 시작

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

## 참고 문서

- **[PLANNING.md](./PLANNING.md)**: 아키텍처 결정 기록 (ADR)
- **[KNOWLEDGE.md](./KNOWLEDGE.md)**: 모범 사례, 규칙, 패턴
