# CLI 전략 — 멀티 AI 역할 매트릭스

> 작성: 2026-03-09
> 상태: 초안. 실행 플래그 실측 필요.

---

## 원칙

1. **Claude = 유일한 설계/결정권자.** Codex/Gemini는 추출/검증/문서화.
2. **Codex: 모든 권한, 프롬프트로 스코프 제한.** 기존 코드 수정 금지, 작업 범위 명시.
3. **Gemini: -o 플래그 기반 출력.** 현행 유지.
4. **커밋/push는 Claude만.** 예외 없음.

---

## CLI 프로필

### Claude Code (Opus 4.6)
- 역할: 오케스트레이터, 설계자, 코드 작성자
- 강점: MCP 접근, 200K 컨텍스트, 모든 도구
- 비용: Max 구독

### Codex (gpt-5.4 xhigh)
- 역할: 정밀 분석기 + 문서 작성기
- 권한: **full-auto (모든 권한)** — 프롬프트로 스코프 제한
- 할 수 있는 것:
  - 코드 리뷰 → 리뷰 문서 직접 생성
  - 코드베이스 분석 → 분석 보고서 직접 생성
  - 교차 비교 → 정합성 보고서 직접 생성
  - 테스트 파일 생성 (tests/ 폴더)
- 할 수 없는 것 (프롬프트로 강제):
  - 기존 소스 코드 수정
  - git commit/push
  - config/설정 파일 수정
- 실측 제약:
  - `.claude/` 경로 sandbox 차단 (보안 정책)
  - Windows tempdir 권한 문제 (pytest 실행 제한)
  - `-m o3` ChatGPT 계정 미지원
  - 5시간 롤링 리밋
- 비용: Plus $20/월

### Gemini (Auto → 3.1-pro)
- 역할: 벌크 분석기 + 2nd opinion
- 권한: `-o` 출력 전용 (현행 유지)
- 강점: 1M 컨텍스트, .md 대량 분석, 웹 검색
- 실측 제약: .py 읽기 차단, 디렉토리 접근 실패
- 비용: AI Pro $20/월

### Perplexity (sonar-deep-research)
- 역할: 웹 리서치 전용
- 용도: tech-review 소스, 외부 레퍼런스 조사
- 비용: Pro 구독

---

## 5단계 파이프라인별 배치

| Stage | Claude | Codex | Gemini |
|-------|--------|-------|--------|
| 1. Ideation | 오케스트레이터, 통합 | 코드베이스 5+파일 분석 → 보고서 생성 | 외부 소스 벌크 분석, 2nd opinion |
| 2. Impl Design | 설계 결정, Phase 분해 | 설계↔코드 정합성 → 검증 보고서 | 대안 설계 제안, 영향 범위 |
| 3. Impl Review | 최종 판단 (GO/NO-GO) | R1: 태스크별 코드 리뷰 → cx-*.md 생성 | R2: Phase별 아키텍처 리뷰 → gm-*.md |
| 4. 실제 구현 | 코드 작성 (독점) | — | — |
| 5. Code Review | 최종 판단, 병합 | R1: 파일별 리뷰 → cx-*.md 생성 | R2: 변경 영향 분석 → gm-*.md |

---

## 위임 트리거

### Codex 자동 위임
- 파일 5개+ 동시 분석
- 전체 코드베이스 탐색
- 교차 비교 (schema vs config vs DB)
- Stage 3/5 R1 코드 리뷰

### Gemini 자동 위임
- Codex 결과 반박/보완
- 전체 소스 + 스펙 → 영향 범위
- Stage 3/5 R2 아키텍처 리뷰
- .md 문서 대량 분석

### 위임 금지 (Claude 직접)
- mcp-memory MCP 호출
- 파일 4개 이하 읽기
- 커밋/push
- 설계 결정, 아키텍처 판단

---

## Codex 프롬프트 템플릿

모든 Codex 위임에 아래 접두어 필수:

```
[SCOPE] 이 작업의 범위: {작업 설명}
[WRITE] 새 파일 생성 허용: {경로 패턴} (예: docs/review/cx-*.md, .ctx/delegates/*.md)
[READ] 읽기 대상: {파일/폴더 목록}
[FORBIDDEN] 기존 소스 코드 수정 금지. git commit/push 금지. config 파일 수정 금지.
[OUTPUT] 결과를 {출력 경로}에 마크다운으로 작성하라.
```

---

## 결과 통합 경로

```
Codex → 직접 파일 생성 (cx-*.md, .ctx/delegates/)
Gemini → -o 출력 (gm-*.md, .ctx/delegates/)
    ↓
Claude 검증 (ai-synthesizer verify barrier)
    ↓
통합 판단 → 코드 반영 / 커밋
```

---

## 미결 (실측 필요)

- [ ] Codex full-auto 정확한 플래그 확인 (`--full-auto` vs `--dangerously-bypass-approvals-and-sandbox`)
- [ ] Codex sandbox off 시 `.claude/` 접근 가능한지
- [ ] Gemini `.geminiignore` 로 .py 차단 해제 가능한지
- [ ] Codex 5시간 롤링 정확한 제한 (회수? 토큰?)
- [ ] Perplexity CLI 존재 여부
