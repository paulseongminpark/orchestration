# Orchestration System

## Context
- **STATE.md**: 시스템 인벤토리 SoT (에이전트/스킬/팀/플러그인)
- **PLANNING.md**: 아키텍처 결정 기록 (ADR)
- **KNOWLEDGE.md**: 패턴, 규칙, 모범 사례
- **REFERENCE.md**: 종합 가이드 (docs/)
- **logs/**: 시간순 상세 로그 (읽기 금지, append만)

## Architecture
- Claude Code = 유일한 쓰기
- GPT/Gemini/Perplexity = 읽기 (GitHub Pages URL)
- Obsidian = 뷰어 (편집 금지)

## Read Priority
1. MEMORY (자동)
2. STATE.md (현재 상태)
3. PLANNING.md (결정 이유)
4. KNOWLEDGE.md (규칙/패턴)
5. 작업 파일만 (범위 제한)

## Skills
/dispatch: 팀 추천 + 세션 목표
/morning: 통합 대시보드 브리핑
/sync: STATE 갱신 + git push
/sync-all: 모든 프로젝트 동기화
/verify: 통합 규칙 검증
/todo: TODO 관리
/compressor: 세션 압축 (9단계)

## Pages URL
https://paulseongminpark.github.io/orchestration/STATE.md
