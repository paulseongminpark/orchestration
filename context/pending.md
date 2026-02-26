# 에이전트 학습 후보 (pending)

> compressor가 수집 → sync-all/Opus 검증 → 채택 시 agent.md 반영
> 직접 agent.md 수정 금지. 이 파일에 append만.

[패턴후보][tr-updater] Perplexity API search_domain_filter 최대 20개 제한. 도메인 목록이 20개 초과 시 slice(0,20)으로 자름. deep research는 도메인 필터 미지원 (넣으면 거부 응답).
[패턴후보][code-reviewer] API 응답이 HTTP 200이지만 거부 메시지인 경우 폴백 미작동 버그 패턴. 거부 패턴 검사를 API 호출 직후 (폴백 분기 내)에서 수행해야 함.
[패턴후보][gemini-analyzer] Gemini CLI 스킬에서 ~/ 경로 사용 금지. Gemini가 프로젝트 로컬 .claude/ 디렉토리를 우선 읽어 경로 오작동 발생. 절대 경로 /c/Users/pauls/ 필수.
[패턴후보][compressor] 타임스탬프 LLM 추정 금지. 반드시 `date +%H:%M` 명령 실행 후 실제 시간 사용. 추정 시 수십 분 오차 발생.
[패턴후보][compressor] 구현 완료 ≠ DONE. 반드시 Living Docs → 옵시디언 → 커밋 → push → compressor 체크리스트 통과 후 DONE 선언. 중간 단계 생략 시 다음 세션에서 불일치 발생.
[패턴후보][code-reviewer] .chain-temp 오프로딩 패턴: 체인에서 에이전트 간 공유 메모리가 필요할 때 context에 직접 포함 대신 파일(context/.chain-temp/agent-name.md)로 전달. 메인 컨텍스트 절감 효과.

---

## 2026-02-23 [tech-review 세션, 다섯 번째]

### 패턴 1: Perplexity API 거부 응답 감지
- 관찰: fetch-perplexity.js가 거부 응답을 유효 응답으로 처리해 포스트로 저장됨
- 학습: API 응답에 "cannot", "unable", "I don't", "sorry" 등 거부 키워드 포함 시 실패 처리
- 적용 후보: tr-updater, tr-monitor
- 신뢰도: 높음 (실제 장애 사례 1건)

### 패턴 2: 프롬프트 마커가 prompt injection 유발
- 관찰: TOPIC_START/TOPIC_END 마커를 포함한 EN 프롬프트가 Perplexity API에서 prompt injection으로 감지됨
- 학습: 외부 AI API 프롬프트에 구분자 마커(XML 태그, 특수 구분선 등) 사용 시 injection 감지 가능 → 마커 대신 자연어 지시로 대체
- 적용 후보: tr-updater (프롬프트 작성 시 주의사항으로)
- 신뢰도: 중간 (추정 원인, 마커 제거 후 성공이 간접 증거)

### 패턴 3: 분량 지시는 문장 수로 명시
- 관찰: "충분히", "자세히" 등 모호한 지시 → 실제 출력량 차이 큼. "항목당 8문장, 합계 25문장 이상" 같은 수치 지시 효과적
- 학습: 콘텐츠 생성 프롬프트에서 분량 지시는 반드시 구체적 수치(문장 수, 글자 수)로
- 적용 후보: tr-updater, content-writer
- 신뢰도: 높음 (적용 후 1,883자 달성 확인)

### 패턴 4: 파이프라인 안전장치 — 앞 단계 실패 시 뒤 단계 건너뜀
- 관찰: KO 생성 실패 시에도 EN 번역이 실행돼 빈 EN 포스트 생성됨
- 학습: CI/CD 파이프라인에서 앞 단계(KO fetch) 실패 시 뒤 단계(EN 번역) exit code로 건너뛰는 조건부 실행 패턴이 필수
- 적용 후보: tr-monitor (파이프라인 검증 항목으로)
- 신뢰도: 높음 (실제 장애 원인)

### 패턴 6: GitHub Actions push 트리거는 해당 브랜치에 워크플로우 파일이 있어야 함
- 관찰: 새 브랜치에 `.github/workflows/` 없으면 push 이벤트가 워크플로우 미트리거
- 학습: 브랜치 생성 시 반드시 main(워크플로우 포함)에서 분기하거나 merge해야 함
- 적용 후보: inbox-processor, daily-ops (브랜치 생성 가이드)
- 신뢰도: 높음 (실제 장애 사례 + 수정 후 성공 확인)

### 패턴 7: gh CLI -f vs --field 타입 차이
- 관찰: `-f subscribed=false`는 문자열 "false"로 전달 → API boolean 파라미터에 오작동 가능
- 학습: boolean/숫자 파라미터는 `--field`(자동 타입 추론) 사용 필수. `-f`는 문자열 강제
- 적용 후보: 모든 gh api 호출에 타입 주의
- 신뢰도: 높음 (gh CLI 공식 동작)

### 패턴 5: 제목 추출 — 본문 첫 핵심 문장이 프롬프트 카테고리명보다 우수
- 관찰: 프롬프트에 TITLE 지시 시 카테고리명("AI 도구 & 코딩" 등)이 제목으로 추출됨 → 뉴스성 부족
- 학습: 포스트 제목은 "Today in One Line" 섹션 본문(실제 뉴스 핵심)에서 자동 추출하는 것이 SEO·뉴스성 모두 우수
- 적용 후보: tr-updater (프롬프트 작성 가이드에 반영)
- 신뢰도: 높음 (적용 후 뉴스성 제목 생성 확인)

### 패턴 8: Gemini CLI 절대 경로 필수
- 관찰: Gemini 스킬에서 ~/ 경로 사용 시 프로젝트 로컬 .claude/ 디렉토리를 우선 읽어 경로 오작동
- 학습: Gemini 스킬에서 파일 경로는 항상 /c/Users/pauls/ 절대 경로 사용. ~/ 금지.
- 적용 후보: gemini-analyzer (스킬 작성 가이드에 반영)
- 신뢰도: 높음 (실제 테스트에서 발견 + 수정 후 해결)

### 패턴 9: compressor 타임스탬프 — LLM 추정 금지
- 관찰: compressor가 타임스탬프를 LLM 추정값으로 기록 → 실제와 수십 분 오차 발생
- 학습: 타임스탬프는 반드시 `date +%H:%M` 명령 실행 후 실제 시간 사용. 추정 금지.
- 적용 후보: compressor (타임스탬프 작성 규칙에 반영)
- 신뢰도: 높음 (실제 버그 수정 사례)
