# SOT Metrics — 성과 지표

> 목적: 에이전트 효과성 + 작업 품질 데이터 누적. "뭐가 실제로 도움이 됐나"를 측정.

---

## 에이전트 효과성 로그

| 날짜 | 에이전트 | 작업 | 품질(1-5) | 메모 |
|------|----------|------|-----------|------|
| 2026-02-22 | gemini-analyzer | 연동 테스트 | - | 설치 완료, 실분석 미실시 |
| 2026-02-22 | gemini-analyzer(Opus) | 오케스트레이션 시스템 전체 비판 분석 | 5 | 11개 개선 태스크 도출, 모두 완료 |
| 2026-02-22 | codex-reviewer | 설계 결함 검증 1차 (todo 삭제 설계) | 4 | 16개 결함 발견. 실전 유용. 2차 4개 신규/미해결 |
| 2026-02-22 | ml-porter (역할) | monet-lab page-12 portfolio 컴포넌트 이식 | 5 | AiWorkflowSection, TechReviewSystemSection, aiWorkflowData 완전 이식 |

**기준:**
- 5: 직접 쓸 수 있는 결과물
- 4: 약간 수정 후 사용
- 3: 방향은 맞지만 재작업 필요
- 2: 참고만 가능
- 1: 재호출 필요

---

## 배포 성과 로그 (portfolio)

| 날짜 | 변경 내용 | 배포 결과 | 이슈 |
|------|----------|-----------|------|
| 2026-02-22 | TechReviewSystemSection.tsx 신규 생성 | git push master (b5a623f) | localhost:5173 시각 확인 대기 |

---

## monet-lab 실험 로그

| 날짜 | 페이지 | 변경 내용 | 커밋 |
|------|--------|----------|------|
| 2026-02-22 | page-12 | FadeIn style prop, 형광펜 highlight | 7567d96 |
| 2026-02-22 | page-12 | orange→background, blue 섹션 하이라이트 | c93b956 |
| 2026-02-22 | page-12 | SectionNarrative → wd-callout 구조 교체 | 509b6f4 |
| 2026-02-22 | page-12 | AI/TR 상세 섹션 portfolio 원본 이식 | cce9486 |

---

## 세션 생산성 로그

| 날짜 | 완료 작업 | 소요 시간 | 주요 병목 |
|------|----------|-----------|----------|
| 2026-02-22 | Gemini CLI, n8n 설치, CHANGELOG 완성, hook 버그 수정, 리서치 58개 | ~3h | 다중 창 소통 불가 |
| 2026-02-22 | orch-system-overhaul 11개 태스크 (보안+자동화+정리) | ~2h | - |
| 2026-02-22 | codex-reviewer 에이전트 설계+구현+실전 테스트 | ~1h | Codex CLI 샌드박스 오류 디버깅 |
| 2026-02-22 | monet-lab page-12 UI 개선 + portfolio 컴포넌트 이식 | ~1h | - |

---

## 패턴 인사이트

### 효과 있었던 것
- gemini-analyzer 비판 분석 → 11개 구체적 태스크 도출 (실행률 100%)
- compressor 5곳 저장으로 컨텍스트 복구 완성도 향상
- codex-reviewer 1차 스캔: 16개 결함 발견 → 설계 검증 도구로 실용성 확인
- portfolio 원본 컴포넌트 직접 이식: 중복 작업 없이 빠른 구현

### 효과 없었던 것
- (누적 예정)

### 반복되는 병목
- 세션 간 컨텍스트 전달 (→ /catchup으로 부분 해결)
- 다중 창 AI 소통 불가 (→ 단일 창 Task 툴로 해결)
- Codex CLI Windows 샌드박스 오류 (→ 파일 시스템 접근 금지 조건으로 해결)
