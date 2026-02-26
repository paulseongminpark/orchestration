# AI 오케스트레이션 시스템

> 2026-02-15 설계 구축, 2026-02-17 보안/동기화/토큰 강화 (D-016). 이 문서는 전체 시스템의 목차이자 출발점.

## 문서 목록

| 문서 | 내용 |
|------|------|
| [[architecture]] | 전체 아키텍처 — 폴더, Git, GitHub Pages, 데이터 흐름 |
| [[philosophy]] | 설계 철학 — 왜 이렇게 만들었는가 |
| [[ai-roles]] | AI별 역할 — Claude, GPT, Gemini, Perplexity |
| [[claude-code-guide]] | Claude Code 심화 — CLAUDE.md, Skills, Hooks, Agents, Permissions |
| [[git-workflow]] | Git 워크플로우 — SoT, auto-push, GitHub Pages |
| [[daily-workflow]] | 일일 사용법 — 아침부터 저녁까지 |
| [[decisions]] | 주요 결정 기록 — 무엇을 왜 선택/폐기했는가 |
| [[TODO]] | 할 일 목록 — 앞으로 하고싶은것 |
| [[crystalize-prompt]] | 프롬프트 압축 방법론 (cc-system) — 의도 보존, 고해상도 토큰화 |
| [[design-pipeline]] | AI 파이프라인 설계 원칙 (cc-system) — 컨텍스트 효율, 전처리 분리 |

## AI 프롬프트 파일 (스냅샷)

> SoT는 각 플랫폼 설정. 이 파일들은 참고용 스냅샷.

| AI | 파일 |
|----|------|
| GPT 글로벌 | `gpt/master_prompt.md` |
| GPT 포트폴리오 | `gpt/projects/portfolio.md` |
| GPT 코워크 | `gpt/projects/cowork.md` |
| Perplexity 글로벌 | `perplexity/master_prompt.md` |
| Perplexity 오케스트레이션 | `perplexity/spaces/orchestration.md` |
| Perplexity 포트폴리오 | `perplexity/spaces/portfolio.md` |
| Gemini 글로벌 | `gemini/master_prompt.md` |
| Gemini 체크리스트 | `gemini/validation_checklist.md` |
| Claude 계층 설명 | `config/claude/hierarchy.md` |

## 핵심 원칙 (한 눈에)

1. **단일 진실 소스(SoT)**: Git의 `context/STATE.md`가 유일한 진실
2. **쓰기 권한 분리**: Claude Code만 쓴다. 나머지 AI는 읽기만.
3. **사고는 휘발, 기록은 남음**: GPT의 토론은 사라져도 된다. Claude의 커밋은 영원하다.
4. **토큰은 자원**: 매 턴마다 CLAUDE.md가 로드된다. 4줄이면 충분하다.
5. **구조가 규율**: 좋은 폴더 구조는 규칙을 강제한다.
