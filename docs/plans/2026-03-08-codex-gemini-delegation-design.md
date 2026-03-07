# Claude-Codex-Gemini 위임 오케스트레이션 설계
_작성: 2026-03-08_

## 개요
Claude Code가 오케스트레이터로서 Codex(gpt-5.4 xhigh) / Gemini(2.5-pro)에게
대규모 분석 작업을 위임해 컨텍스트를 절약하고 병렬 처리를 실현하는 시스템.

## 역할 분담

### Claude Code (오케스트레이터)
- 의사결정, 방향 설정, 사용자 대화
- 단순 MCP 호출: recall, remember, get_context (직접 실행)
- 위임 트리거 감지 → 스킬 호출 → 결과 통합

### Codex (gpt-5.4, xhigh 기본)
**위임 대상:**
- 파일 5개+ 동시 읽고 분석
- 전체 코드베이스 탐색 ("어느 파일 봐야 하나?")
- 여러 결과 교차 비교/종합 (예: schema.yaml vs config.py vs DB)
- enrichment 등 배치 작업
- 유지보수 분석 (CRITICAL 버그 수정안 제안, 파일 수정 금지)
- 벌크 테스트 파일 생성 (workspace-write, tests/ 폴더만)

**샌드박스 모드:**
- 분석/탐색: `read-only`
- 테스트 생성: `workspace-write` (tests/ 폴더만)

### Gemini (Auto (gemini-3.1-pro, -m 플래그 없이 실행), --yolo)
**위임 대상:**
- 전체 소스 + 스펙 동시 로딩 → 수정 영향 범위 분석
- Codex 결과물 반박/보완
- 아키텍처 설계 2nd opinion
- 대형 설계 문서 검토

**항상 프롬프트에 포함**: "파일 수정 금지. 분석 결과만 출력하라."

## 파일/폴더 구조

```
.ctx/
  shared-context.md          # session-end hook 전용 (건드리지 않음)
  delegates/                 # 위임 결과 히스토리
    YYYY-MM-DD-HH-{task}.md
  codex-latest.md            # Claude가 읽는 최신 Codex 결과
  gemini-latest.md           # Claude가 읽는 최신 Gemini 결과
```

mcp-memory 프로젝트 내부 파일은 건드리지 않음.

## 제한사항 (하드 룰)

| 제한 | 내용 |
|------|------|
| 커밋 권한 | Claude만. Codex/Gemini 커밋 절대 금지 |
| Codex 샌드박스 | 분석=read-only, 테스트생성=workspace-write(tests/만) |
| Codex 세션 | `--ephemeral` 항상 (세션 저장 안 함) |
| Gemini | `--yolo` + 프롬프트에 파일수정금지 명시 |
| 결과 저장 | `.ctx/delegates/` 에만 (프로젝트 내부 금지) |
| xhigh | 기본값 유지 (단순/복잡 구분 없이) |

## 구현 목록

1. `delegate-to-codex` 스킬 — 작업 타입 감지 → 프롬프트 구성 → exec → 결과 저장
2. `delegate-to-gemini` 스킬 — 영향 범위 분석 / 반박 특화
3. CLAUDE.md 위임 트리거 규칙 추가
4. `.ctx/delegates/` 폴더 생성

## 검증 완료

- Codex exec + mcp-memory recall: OK (gpt-5.4 xhigh, 비대화형)
- Gemini -p + mcp-memory recall: OK (Auto (gemini-3.1-pro, -m 플래그 없이 실행), 비대화형)
