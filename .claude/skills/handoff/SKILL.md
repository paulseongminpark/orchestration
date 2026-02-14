---
name: handoff
description: 다른 AI에게 전달할 컨텍스트 문서 생성
argument-hint: <gpt|gemini|perplexity> <요청내용>
user-invocable: true
allowed-tools: Read, Write
---

$ARGUMENTS[0] = 대상 AI
$ARGUMENTS[1:] = 요청 내용

## Steps
1. context/STATE.md 읽기
2. 대상 AI에 맞는 핸드오프 문서 생성
3. 클립보드에 복사 안내

## AI별 형식
- GPT: Canvas용 구조 + "Claude Code 실행 지침" 포함
- Gemini: 검증 체크리스트 형식
- Perplexity: 리서치 질문 + 소스 URL 요구

## Output
핸드오프 문서 전문 (복사용)
