# Git 워크플로우

## 개요

이 시스템에서 Git은 단순한 버전 관리가 아니라 **데이터 전달 파이프라인**이다.

```
Claude Code ──→ git commit ──→ git push ──→ GitHub ──→ GitHub Pages
                                                          │
                                    GPT/Gemini/Perplexity ←┘ (URL로 읽기)
                                    Obsidian ← Junction (로컬 실시간)
```

## GitHub Repos

| Repo               | 용도                  | 유형       | URL                                            |
| ------------------ | ------------------- | -------- | ---------------------------------------------- |
| orchestration      | 오케스트레이션 시스템         | public   | github.com/paulseongminpark/orchestration      |
| portfolio_20260215 | 포트폴리오 프로젝트          | public   | github.com/paulseongminpark/portfolio_20260215 |
| ai-config          | AI 설정 + Obsidian 볼트 | private  | github.com/paulseongminpark/ai-config          |
| portfolio (구)      | 이전 포트폴리오            | archived | —                                              |

## GitHub Pages

### 활성화 방법

각 public repo에서: Settings → Pages → Source: main branch

### URL 패턴

```
https://paulseongminpark.github.io/{repo-name}/context/STATE.md
```

- 오케: https://raw.githubusercontent.com/paulseongminpark/orchestration/main/context/STATE.md
- 포트: https://raw.githubusercontent.com/paulseongminpark/portfolio_20260215/master/context/STATE.md

### 중요 파일

각 repo 루트에 필요:
- `.nojekyll` — Jekyll 처리 비활성화 (마크다운을 raw로 제공)
- `_config.yml` — 기본 설정

## Auto-Push (post-commit hook)

### 동작

STATE.md가 커밋에 포함되면 자동으로 push.

### 코드

`{project}/.git/hooks/post-commit`:
```bash
#!/bin/sh
if git diff-tree --name-only --no-commit-id HEAD | grep -q "context/STATE.md"; then
  git push origin main 2>/dev/null &
  echo "STATE auto-pushed"
fi
```

### 흐름

```
Claude: /sync 실행
  → STATE.md 수정
  → git add context/STATE.md
  → git commit -m "[orchestration] STATE 갱신"
  → post-commit hook 트리거
  → git push origin main (백그라운드)
  → GitHub Pages 자동 갱신 (~1분)
  → GPT/Gemini/Perplexity에서 최신 STATE 접근 가능
```

## 커밋 메시지 규칙

```
[project] 한줄 설명
```

예시:
```
[orchestration] STATE 갱신
[portfolio] Empty House 이미지 슬라이더 구현
[orchestration] Phase 1 폴더 구조 마이그레이션
```

## Git 안전 규칙

| 규칙 | 이유 |
|------|------|
| force push 금지 | 히스토리 손실 |
| main 브랜치 직접 작업 | 1인 프로젝트, 브랜치 오버헤드 불필요 |
| .env 커밋 금지 | 보안 |
| permissions.deny로 차단 | `git push --force`, `git clean`, `rm -rf`, `rm -r` |
| curl/wget 차단 | 데이터 유출 방지 |

## Obsidian 연동 (Junction)

### Junction vs Symlink

| 방식 | 관리자 필요 | 지원 |
|------|-----------|------|
| Symlink (mklink /D) | ✅ 필요 | 제한적 |
| **Junction (mklink /J)** | ❌ 불필요 | **완전 지원** |

### 현재 Junction

```
C:\dev\02_ai_config\projects\orchestration → 01_orchestration\context
C:\dev\02_ai_config\projects\portfolio     → 02_portfolio\context
```

### 특성

- Junction은 **로컬 실시간** 반영 (git pull 불필요)
- Claude Code가 STATE.md 수정 → Obsidian에서 즉시 보임
- Obsidian에서 편집 가능하지만 **하지 말 것** (SoT 충돌)

## Evidence 백업 + Stop Hook

### Stop Hook 전체 구성 (3단계)

세션 종료 시 Stop hook이 순서대로 실행:

```
Stop Hook #1: copy-session-log.py
    세션 .jsonl 파일 → 파싱 → 03_evidence/claude/{project}/{date}.md

Stop Hook #2: STATE.md 미커밋 차단
    git status 확인 → 미커밋 감지 → exit 1 (세션 종료 차단)

Stop Hook #3: analyze-session.sh (Auto Memory)
    세션 .jsonl 파싱 → 인사이트 추출 → pending.md 축적
```

### Evidence 출력 경로

```
C:\dev\03_evidence\
├── claude\
│   ├── orchestration\2026-02-15.md
│   └── portfolio\2026-02-15.md
└── chatgpt\
    └── 2026-02-04_portfolio_text_finalization.md
```

### Evidence 특징

- Git 추적 안 함 (로컬 전용)
- 코드 블록 자동 제거 (가독성)
- UTC → KST 시간 변환

### Auto Memory 특징

- `~/.claude/scripts/analyze-session.sh` 실행
- 결과 → `~/.claude/projects/{hash}/memory/pending.md`
- `/sync-all` 또는 `/memory-review` 호출 시 MEMORY.md로 승격
- Git 추적 안 함 (로컬 전용)

## 관련 문서
- [[architecture]] — 전체 구조
- [[claude-code-guide]] — Hooks 상세
- [[daily-workflow]] — 실제 사용 흐름
