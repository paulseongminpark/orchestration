# 세션 요약

> compressor 에이전트가 자동 업데이트합니다.
> /catchup 스킬로 읽습니다.

=== 컨텍스트 압축 요약 ===

세션 목표: tech-review 파이프라인 근본 개편 — sonar-deep-research 전환

완료 (8항목):
  - [fetch-perplexity.js] 대규모 재작성: submitDeepResearch + callSonarPro 폴백 + callWithRetry
  - [fetch-perplexity.js] DOMAIN_FILTERS 7요일별 도메인, validateUrls HTTP HEAD 검증, validateContent 로컬 분량 검증
  - [fetch-perplexity.js] removeBracketHeadlines, getThisWeekAllKeywords 일요일 합산, isRejected 추출
  - [프롬프트 01~06] 3건→5건, 분량 강화 (10문장/항목), Source 다중URL, 대괄호 금지
  - [프롬프트 07] 주간종합 → 글로벌 AI 현장 5건 (미국 외 지역)
  - [translate] max_tokens 10000 + callWithRetry
  - [parse-content] 브라켓 헤드라인 방어 1줄
  - [create-post.yml] cron 30분 앞당김, timeout-minutes, USE_DEEP_RESEARCH env

현재 상태: deep research 파이프라인 동작 확인됨. GitHub Actions 통합 테스트 3회 시행착오 후 성공. deep research가 5건 요청에 3건만 반환하는 문제 + 대괄호 헤드라인 잔존. 다음 세션에서 2단계 파이프라인(deep research 조사 → sonar-pro 구조화) 설계부터 재진행.

다음 할 것:
  1. 2단계 파이프라인 설계: deep research → sonar-pro 구조화 (5건 보장)
  2. 대괄호 헤드라인 잔존 수정 (deep research 응답에 removeBracketHeadlines 미적용 확인)
  3. API 비용 검토 ($5/월 예산 내 2단계 파이프라인 가능 여부)

열린 결정:
  - deep research 단독 vs 2단계 파이프라인 (미결정, 다음 세션 설계)
  - 도메인 필터 20개 제한 대응 (현재 slice(0,20)으로 잘라내는 중)
  - deep research가 search_domain_filter 미지원 (제거됨, 프롬프트로만 안내)

주의사항:
  - blog/는 별도 git repo (tech-review와 분리)
  - deep research 거부 시 sonar-pro 폴백 작동 확인됨 (isRejected → fallback)
  - search_domain_filter max 20개 (Perplexity API 제한)
  - deep research에 domain filter 넣으면 거부 응답 반환 (제거 필수)
  - 기존 포스트 존재 시 parse-content.js가 덮어쓰지 않음 (재생성 시 삭제 필요)

=== 이 내용을 새 세션 시작 시 붙여넣으세요 ===
