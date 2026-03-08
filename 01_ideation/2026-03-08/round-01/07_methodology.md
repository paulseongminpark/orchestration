# G. 탐색/학습 방법론

## G1. Claude Cycles — 31 Explorations + plan.md
- **소스**: Don Knuth, Stanford (2026-02-28, revised 03-04)
- **문제**: directed Hamiltonian cycles의 분해 — 수학 난제
- **Filip Stappers의 코칭 지시** (Claude에게):
  > "After EVERY exploreXX.py run, IMMEDIATELY update this file [plan.md] before doing anything else. No exceptions."
- **31번 탐색의 전략 전환 패턴**:
  ```
  #1-5:  직접적 시도 (DFS, serpentine pattern)
  #6-15: 프레임 전환 (fiber decomposition 발견)
  #16-25: 계산적 접근 (SA) → "순수 수학이 필요하다" 깨달음
  #26-31: 통찰 → 해결
  ```
- **#27 Near Miss**: "Only 3(m-1) out of m³ vertices have conflicts" — 거의 맞았지만 충돌 해소 불가
- **#30 돌파구**: SA 결과를 역분석 → "fiber별 선택이 단일 좌표에만 의존" 발견
- **#31 해결**: Python 프로그램 → m=3,5,7,9,11 전부 성공
- **적용**:
  - 매 exploration 후 즉시 문서화 (현재 compressor는 세션 끝에만)
  - **중간 체크포인트** 추가
  - 10번 시도해도 안 풀리면 프레임 전환 hook

## G2. 환각 메커니즘 (Anthropic 해석 연구)
- **소스**: anthropic.com/research/tracing-thoughts-language-model
- **핵심 발견**: 거절이 "기본 동작"
  - "알 수 없음" 회로가 기본적으로 활성화
  - 알려진 개체에 대해 "알려진 답변" 특징이 이 거절을 **억제**
  - Michael Batkin(미지의) 이름 인식 → "알려진 개체" 오활성화 → 거절 억제 → 환각
- **실험**: "알려진 답변" 특징을 인위적으로 활성화 → 일관되게 환각
- **적용**: recall 결과에 confidence 필드. "이 노드는 확실하지 않다" 표시. 에이전트가 불확실한 정보를 사실처럼 제시하는 것 방지

## G3. 병렬 경로 + 사전 계획
- **소스**: Anthropic 해석 연구
- **병렬 산술**: 덧셈 시 "대략적 답 계산 경로" + "마지막 자릿수 정확히 결정 경로"가 동시 작동
- **사전 계획**: 시를 쓸 때 두 번째 줄 시작 전에 운율 단어를 미리 계획. "rabbit" 특징 제거 → "habit"으로 변경
- **다단계 추론**: "Dallas가 있는 주의 수도?" → Dallas→Texas 활성화 → Texas→Austin 활성화. Texas를 California로 대체 → Sacramento
- **적용**: 에이전트 "빠른 추정 + 정밀 검증" 2-track 설계

## G4. 탈옥 공격의 내부 경로
- **소스**: Anthropic 해석 연구
- "Babies Outlive Mustard Block" → BOMB 조합
- 문법적 일관성 유지 압력이 안전 메커니즘을 **압도**
- Claude는 위험을 인지하지만 문법적 강압으로 대응 지연
- **적용**: 안전 메커니즘 설계 시 "문법적 완성 전에 거부" 패턴 필요

## G5. 관찰력 > 기술력
- **소스**: Josh newsletter (Notion AI agents)
- **야마다 (비개발자)**: 16개 에이전트 운영. 뉴스 수집(연 120시간 절감), 이메일 트리아지, 주간 진단
- **핵심 인용**: "자동화의 진입장벽은 기술력이 아니라 어떤 반복 업무를 발견하는 관찰력"
- **설계 철학**: "정보→반복 발견→에이전트 위임" 순서 필수
- **적용**: 주기적 "수동 작업 감사" — 지금 뭘 여전히 수동으로 하고 있는가?

## G6. Automation of Automation (메타 자동화)
- **소스**: ykdojo tip 41
- Claude Code 워크플로우 자체를 자동화하는 스크립트
- 우리: start.sh, relay.py, auto_remember.py — 이미 이 방향
- **적용**: 더 많은 워크플로우를 자동화 (세션 전환, 일일 브리핑 등)

## G7. Karpathy "본질 vs 효율"
- **소스**: Karpathy microgpt.py (gist)
- **원문**: "This file is the complete algorithm. Everything else is just efficiency."
- 500줄 순수 Python GPT: Value 클래스 autograd + 1-layer transformer + Adam
- 커뮤니티 포트: C++ 219x, Rust 440x, Julia 1581x, C+SIMD 19,380x 빠름
- **핵심 질문**: mcp-memory의 "complete algorithm"은 뭔가?
- **답**: `remember(embed + store) → recall(search + rank) → forget(decay)`
- **forget이 없으면 3분의 1이 빠진 시스템**. 나머지(enrichment, 3-Layer, promote, 온톨로지)는 전부 "efficiency"

## G8. agentic-eval 3패턴 (자기 평가)
- **소스**: awesome-copilot `agentic-eval` 스킬
- **Pattern 1: Basic Reflection** — Generate → Critique(JSON) → Refine (max 3회)
- **Pattern 2: Evaluator-Optimizer** — 생성/평가/최적화 분리 클래스, score_threshold 기반 종료
- **Pattern 3: Code-Specific Reflection** — 코드 생성 → 테스트 생성 → 테스트 실행 → 실패 시 수정 (TDD 루프)
- **평가 전략**: Outcome-Based / LLM-as-Judge / Rubric-Based(가중치 점수)
- **구조화된 JSON 출력으로 평가 결과 파싱 신뢰성 확보**
- **적용**: 에이전트 출력 자동 평가 → code-reviewer, ai-synthesizer에 Reflection 루프 추가

## G9. 메타 스킬 (스킬을 만드는 스킬)
- **소스**: awesome-copilot
- `boost-prompt` = 프롬프트를 만드는 프롬프트
- `create-agentsmd` = 에이전트 설정을 만드는 에이전트
- `create-llms` = LLM 컨텍스트 파일을 만드는 LLM
- `skill-creator` = 스킬을 만들고 평가하는 스킬
- **적용**: 우리 superpowers:writing-skills가 이 역할이지만, eval 파이프라인이 없음
