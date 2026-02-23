# 세션 요약

> compressor 에이전트가 자동 업데이트합니다.
> /catchup 스킬로 읽습니다.

=== 컨텍스트 압축 요약 ===

세션 목표: tech-review 파이프라인 안정화 + 프롬프트 7개 전면 개편

완료:
  - [perplexity-prompts/ko/*.md] 7개 전면 개편 — Smart Brevity v2 통일, 요일별 영문 소스 가이드, 48시간 검색 범위, TOPIC_START/END 마커 제거, 분량 지시(항목당 8문장, 합계 25문장 이상)
  - [수요일 주제] "스타트업 & 투자" → "AI × Industry: 비즈니스 모델" (헬스케어→금융→법률→제조→교육→리테일 순환)
  - [scripts/fetch-perplexity.js] 거부 응답 감지 + 최소 500자 검증 + TITLE/TAGS 자동 주입 (프롬프트 추출 → 응답 앞에 붙임)
  - [scripts/parse-content.js] 제목 자동 추출 — "Today in One Line" 다음 줄을 제목으로 사용
  - [.github/workflows/create-post.yml] KO fetch 실패 시 EN 번역 건너뛰기 안전장치 추가
  - [프롬프트 TITLE: 제거] TAGS만 유지, 제목은 본문에서 자동 추출
  - [_posts/ko/2026-02-23] 실패 포스트 삭제 후 재생성 성공 (1,883자), 제목·태그 수동 수정
  - [_posts/en/2026-02-23] 동일 재생성 완료

실패 원인 분석 (2/23):
  - KO: Perplexity API가 검색 실패 후 거부 응답 반환 → 거부 응답 감지 없어 그대로 저장
  - EN: prompt injection 감지 → TOPIC_START/END 마커가 원인으로 추정 → 마커 제거로 해결

현재 상태: tech-review 파이프라인 안전장치 완비, 새 프롬프트 7개 적용 완료

다음 할 것:
  1. 2/24(화) GitHub Actions 자동 생성 결과 모니터링 (새 프롬프트 첫 실행)
  2. EN 번역 [1][2] 인용 마커 잔류 이슈 수정 (별도 세션)
  3. portfolio: localhost:5173/portfolio_ui_test_v2/ TR System 본문 내용 현재 상태에 맞게 업데이트 (technical writing section)
  4. decisions.md 미반영: tr 2건 (keywords-log.md 신설/KST 버그), pf 2건 (스크린샷/스토리텔링)
  5. orch: Phase E 파일럿, STATE.md 경로 불일치, copy-session-log.py overwrite 미처리 3건

주의사항:
  - tech-review blog: master 브랜치 (paulseongminpark/tech-review)
  - API 예산: $5/월 기준 일일 KO 2,000~2,200자 최적 (항목당 8문장 × 3섹션 = 25문장)
  - 프롬프트 TAGS는 유지, TITLE은 제거 (본문 Today in One Line 자동 추출)
  - KO fetch 실패 시 EN 번역 자동 건너뜀 (create-post.yml 안전장치)

=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===
