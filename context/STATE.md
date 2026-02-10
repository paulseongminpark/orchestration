# AI Orchestration System

## Scope
- 대상: Claude Code / GPT / Gemini 간 컨텍스트 공유 시스템
- 범위: GitHub Pages 기반 STATE.md 자동 공유 + 각 AI 시스템 프롬프트 설정
- 제외: API 연동, 유료 추가 도구, AHK/PowerShell 스크립트

## Decisions
- GitHub Pages로 STATE.md를 공개 URL로 제공 (GPT/Gemini 브라우징 접근)
- Obsidian → git push → Pages 자동 배포 흐름 확정
- Claude Code = 오케스트레이터 (유일한 쓰기 권한)
- GPT = 브레인스토밍/기획 (사용제한 없음 활용)
- Gemini = 리서치/검증
- 로컬 단일 진실(SoT) + GitHub 미러 운영 원칙 유지

## Open
- GPT/Gemini 시스템 프롬프트 적용 후 실제 Packet 흐름 테스트 필요

## Now
각 AI 시스템 프롬프트 적용 중

## Next
전체 Packet 흐름 테스트 (GPT → Packet → Claude Code → STATE 업데이트)

---

# Portfolio

## Scope
- 대상: (포트폴리오 작업 대상 기입)
- 범위: (작업 범위 기입)
- 제외: (제외 사항 기입)

## Decisions
- (포트폴리오 관련 결정사항)

## Open
- (미결 사항)

## Now
(현재 작업)

## Next
(다음 행동)