# Orchestration System

## Context
- **STATE.md**: 지금 상태 (루트, 고수준)
- **PLANNING.md**: 아키텍처 결정 기록 (ADR)
- **KNOWLEDGE.md**: 모범 사례, 규칙, 패턴
- **logs/**: 시간순 상세 로그 (읽기 금지, append만)
- **Evidence**: C:\dev\03_evidence\claude\orchestration\

## Architecture
- Claude Code = 유일한 쓰기
- GPT/Gemini/Perplexity = 읽기 (GitHub Pages URL)
- Obsidian = 뷰어 (편집 금지)

## Read Priority
1. MEMORY (자동, 세션 시작)
2. STATE.md (현재 상태 확인 시)
3. PLANNING.md (결정 이유 확인 시)
4. KNOWLEDGE.md (규칙/패턴 확인 시)
5. 작업 파일만 (범위 제한)

## Skills
/sync: STATE 갱신 + git push
/handoff: AI 간 문서 생성
/morning: 전체 프로젝트 브리핑
/sync-all: 모든 프로젝트 동기화
/verify: 통합 규칙 검증
/todo: TODO 관리

## Config (AI 도구 설정)
- Claude: config/claude/
- GPT: config/gpt/
- Gemini: config/gemini/
- Perplexity: config/perplexity/

## Pages URL
https://paulseongminpark.github.io/orchestration/STATE.md
