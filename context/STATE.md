# AI Orchestration System

## Scope
- 대상: Claude Code / GPT / Gemini 간 컨텍스트 공유 시스템
- 범위: GitHub Pages 기반 STATE.md 자동 공유 + 각 AI 시스템 프롬프트 설정
- 제외: API 연동, 유료 추가 도구

## Decisions
- GitHub Pages로 STATE.md를 공개 URL로 제공 (GPT/Gemini 브라우징 접근)
- Obsidian → git push → Pages 자동 배포 흐름 확정
- Claude Code = 오케스트레이터 (유일한 쓰기 권한)
- GPT = 브레인스토밍/기획 (사용제한 없음 활용)
- Gemini = 리서치/검증
- 로컬 단일 진실(SoT) + GitHub 미러 운영 원칙 유지
- AHK + PowerShell 스냅샷 파이프라인 유지

## Open
- GPT/Gemini 시스템 프롬프트에 STATE URL 자동 참조 규칙 적용 필요
- CLAUDE.md에 오케스트레이션 규칙 추가 필요

## Now
오케스트레이션 시스템 아키텍처 설계 + 각 AI 설정 적용

## Next
GPT Custom Instructions / Gemini Gems에 STATE URL 참조 규칙 작성