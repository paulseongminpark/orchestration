# Claude Code 설정 계층

## 자동 로드 순서 (매 턴)

```
1. ~/.claude/CLAUDE.md                    ← 글로벌 (4줄)
2. ~/.claude/rules/*.md                   ← 글로벌 규칙 모듈
3. {cwd}/.claude/CLAUDE.md               ← 프로젝트별
4. {cwd}/.claude/rules/*.md              ← 프로젝트 규칙
5. MEMORY.md                              ← 자동 메모리 (200줄)
```

## 현재 파일 위치

### 글로벌
```
C:\Users\pauls\.claude\
├── CLAUDE.md                             ← 4줄 핵심 규칙
├── rules\
│   ├── common-mistakes.md               ← 반복 실수 패턴
│   └── workflow.md                      ← 워크플로우 규칙
├── skills\                               ← /dispatch, /morning, /compressor 등 14개
└── agents\                               ← 24개 커스텀 에이전트
```

### 오케스트레이션
```
C:\dev\01_projects\01_orchestration\.claude\
├── CLAUDE.md                             ← 프로젝트 컨텍스트
├── settings.json                         ← permissions + hooks
├── skills\
│   ├── sync\skill.md                     ← /sync
│   ├── handoff\SKILL.md                  ← /handoff
│   └── status\SKILL.md                   ← /status
└── agents\
    ├── architect.md                      ← Opus 설계 에이전트
    └── reviewer.md                       ← Haiku 검증 에이전트
```

### 포트폴리오
```
C:\dev\01_projects\02_portfolio\.claude\
├── CLAUDE.md                             ← 프로젝트 컨텍스트
├── settings.json                         ← permissions + hooks
└── skills\
    ├── sync\SKILL.md                     ← /sync
    └── status\SKILL.md                   ← /status
```

## 상세: REFERENCE.md 참조
