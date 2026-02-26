# Vault & Orchestration 전면 리팩토링 설계
_Created: 2026-02-19_
_Status: APPROVED_

## 문제 정의

- 클코(Claude Code) 작업 히스토리를 한 눈에 트래킹 불가
- orchestration과 ai-config 역할 혼란
- 볼트 전체 진입점(허브) 부재
- 파일이 분산되어 Living Doc 관리 안 됨

## 설계 목표

1. Obsidian 볼트 = 네비게이션 허브 (HOME.md)
2. orchestration = AI 관련 모든 진실의 원천 (SoT)
3. 모든 파일 Living Doc 표준 적용
4. 중앙 집중형 구조

## 최종 볼트 구조

```
C:\dev\
├── HOME.md                         ← NEW: 중앙 MOC 허브
├── CLAUDE.md                       ← 유지
├── 01_projects/
│   ├── 01_orchestration/           ← 대폭 확장
│   │   ├── config/                 ← NEW: ai-config 흡수
│   │   │   ├── claude/
│   │   │   ├── gpt/
│   │   │   ├── gemini/
│   │   │   └── perplexity/
│   │   ├── context/                ← 유지 (STATE/PLANNING/KNOWLEDGE/logs)
│   │   ├── docs/                   ← NEW: vault docs/ 이동
│   │   │   └── plans/
│   │   ├── tools/
│   │   │   └── opcode/             ← NEW: vault opcode/ 이동
│   │   ├── .claude/                ← 유지
│   │   └── scripts/                ← 유지
│   ├── 02_portfolio/               ← 유지 (STATE.md Living Doc 업데이트)
│   ├── 03_tech-review/             ← 확장: Jekyll blog + 프로젝트 트래킹 통합
│   │   ├── (기존 파일들)
│   │   ├── (tech-review/ Jekyll 이동)
│   │   └── STATE.md                ← NEW
│   └── 04_tech-review-comments/
├── 02_ai_config/                   ← ARCHIVED (README 추가, 삭제 안 함)
├── 03_evidence/                    ← 유지
└── 99_archive/                     ← 유지

# 제거되는 루트 폴더
- docs/        → 01_orchestration/docs/ 로 이동 후 제거
- opcode/      → 01_orchestration/tools/opcode/ 로 이동 후 제거
- tech-review/ → 01_projects/03_tech-review/ 로 이동 후 제거
```

## HOME.md 표준 형식

```markdown
# HOME — Dev Workspace Hub
_Updated: YYYY-MM-DD_

## Projects
| Project | Status | Last | Next |
|---------|--------|------|------|
| [[01_projects/01_orchestration/context/STATE\|orchestration]] | ... | ... | ... |
| [[01_projects/02_portfolio/context/STATE\|portfolio]] | ... | ... | ... |
| [[01_projects/03_tech-review/STATE\|tech-review]] | ... | ... | ... |

## Today
- [[01_projects/01_orchestration/context/logs/YYYY-MM-DD]]

## Open Decisions
- [ ] ...

## Tools & Skills
- AI Config: [[01_projects/01_orchestration/config/]]
- Hooks/Scripts: ~/.claude/
- Skills: /morning, /sync-all, /verify, /token-check
```

## Living Doc 표준 형식 (모든 STATE.md)

```markdown
# [이름] STATE
_Updated: YYYY-MM-DD_

## 목적
한 줄 설명

## 현재 상태
- 완료: ...
- 진행중: ...
- 다음: ...

## 최근 결정
- [YYYY-MM-DD] 결정 내용 → 이유

## 막힌 것
- ...
```

## ai-config 아카이브 처리

1. ai-config 모든 파일 → orchestration/config/ 복사
2. ai-config/README.md 추가: "ARCHIVED: Content moved to 01_orchestration/config/"
3. ai-config repo는 git 히스토리 보존을 위해 물리적 삭제 안 함
4. 참조 업데이트: ~/.claude/ rules, MEMORY.md에서 ai-config 경로 → orchestration/config/

## 실행 Phase

### Phase 1: 볼트 허브 설정
- HOME.md 생성
- 볼트 루트 정리 (null 파일 등)

### Phase 2: orchestration 확장
- config/ 디렉토리 생성
- ai-config 파일들 복사
- docs/ 이동 (vault docs/ → orchestration/docs/)
- tools/opcode/ 이동

### Phase 3: ai-config 아카이브
- README.md 추가
- orchestration 커밋

### Phase 4: tech-review 통합
- vault tech-review/ (Jekyll) → 01_projects/03_tech-review/ 이동/통합
- STATE.md 신설

### Phase 5: Living Doc 전체 적용
- 모든 STATE.md Living Doc 형식 업데이트
- 02_ai_config STATE.md 기존 없었으므로 아카이브 README로 대체
- CLAUDE.md 업데이트 (ai-config 경로 참조 수정)
- MEMORY.md 업데이트

## 결정 기록

- 2026-02-19: Approach A (Hub & Spoke + ai-config 머지) 채택
- 2026-02-19: opcode → orchestration/tools/ 통합
- 2026-02-19: tech-review Jekyll → 01_projects/03_tech-review/ 통합
- 2026-02-19: ai-config → 아카이브 (삭제 아님, 히스토리 보존)
