#  STATE — AI Orchestration System

## 지금 상태 (2026-02-12 기준)

**완료**
- STATE 자동 Push (바탕화면 아이콘 → Git Hook)
- 로그 이원화 (LOGS 요약 + EVIDENCE 상세)
- EVIDENCE 시스템 (Paul/claude, KST, 평문)
- push-state.ps1 완전 자동화 (1클릭)

**다음 할 일**
- Packet 흐름 전체 테스트 (GPT → Claude → STATE)
- 포트폴리오 UI 착수

**막힌 것**
- GPT/Gemini 시스템 프롬프트 실전 테스트 안 해봄

---

## 시스템 작동 방식

**데이터 흐름**
AI_작업실 (SoT)  
↓ (수동: 바탕화면 아이콘)  
Git 로컬  
↓ (자동: Git Hook)  
GitHub  
↓ (자동: Pages)  
공개 URL → GPT/Gemini 읽기


**역할**
- Claude: 실행 + 쓰기 (유일)
- GPT: 사고 (읽기만)
- Gemini: 검증 (읽기만)

**핵심 원칙**
- SoT = AI_작업실
- Git = 미러
- 중요한 것만 기록
- 자동화 > 수동

---

## 과거 결정

**2026-02-12**
- 로그 이원화: LOGS (한줄요약) + EVIDENCE (세션상세)
- EVIDENCE: copy-session-log.py (Paul/claude, KST, 평문, 원본보존)
- EVIDENCE 하이브리드: 중요 작업 로그 기록 시 자동 갱신 (~100토큰/회)
- "today" 명령어 자동화: 최근 2일 TODAY + EVIDENCE + STATE 읽기 → 오늘 TODAY 생성 → 작업 상황 출력
- push-state.ps1 통합 (session+split+STATE, 1클릭 자동화)
- Python: split-logs.py (인코딩 문제 해결)
- 효율: CLAUDE.md 320토큰, echo 사용

**2026-02-10**
- Obsidian 단일 볼트 통합
- Auto-Logging 도입
- 출력 3줄 제한 규칙
