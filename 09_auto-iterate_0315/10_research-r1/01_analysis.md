# autoresearch → auto-iterate 분석
> 2026-03-15 | Research R1

## 1. autoresearch 핵심 구조

### 3-file 아키텍처
| 파일 | 역할 | 수정 여부 |
|---|---|---|
| `prepare.py` | 고정 상수, 데이터 준비, 유틸리티 | ❌ 불변 |
| `train.py` | 모델, 옵티마이저, 학습 루프 | ✅ agent 수정 대상 |
| `program.md` | agent에게 주는 지시서 (연구 목표, 제약) | 사람이 반복 수정 |

### 실험 루프
```
1. Measure  — val_bpb 측정 (현재 성능)
2. Modify   — train.py 변경 (하이퍼파라미터, 아키텍처)
3. Measure  — 5분 고정 학습 → val_bpb 재측정
4. Decision — 개선이면 keep, 아니면 discard (revert)
5. Repeat   — 시간당 ~12회, 밤새 ~100회
```

### 설계 원칙
- **단일 수정 대상**: train.py만 변경 → diff 추적 용이
- **단일 메트릭**: val_bpb (낮을수록 좋음) → 판단 명확
- **고정 예산**: 5분 wall-clock → 공정 비교
- **자기 완결**: 외부 의존 최소, 단일 GPU

---

## 2. 우리 시스템으로의 매핑

### 구조 매핑

| autoresearch | 우리 시스템 | 비고 |
|---|---|---|
| `prepare.py` (불변 인프라) | core 시스템: Claude Code, MCP, git | 수정 불가 기반 |
| `train.py` (수정 대상) | 설정 파일군 (아래 상세) | agent가 수정 |
| `program.md` (지시서) | `auto-iterate/program.md` | 최적화 방향 정의 |
| `val_bpb` (단일 메트릭) | 복합 메트릭 (아래 4종) | 도메인 차이 |
| 5분 고정 예산 | 1 iteration = 특정 시나리오 1회 실행 | 시간→횟수 |
| keep/discard | git commit / git revert | 동일 |

### 수정 대상 파일 (= train.py에 해당)

우리 시스템에서 자율 최적화할 수 있는 설정 파일:

| 카테고리 | 파일 | 최적화 대상 |
|---|---|---|
| Agent 정의 | `~/.claude/agents/*.md` | 프롬프트 문구, 도구 선택, 모델 할당 |
| Skill 정의 | `~/.claude/skills/*.md` | 워크플로우 단계, 체크리스트 항목 |
| Hook 설정 | `~/.claude/hooks/*.py` | 트리거 조건, 필터 로직 |
| Rules | `~/.claude/rules/*.md` | 규칙 표현, 우선순위 |
| Config | `~/.claude/config.json` | 모델 선택, 환경 설정 |

**제약**: 한 iteration에 하나의 파일만 수정 (autoresearch의 단일 대상 원칙).

---

## 3. 메트릭 정의

### M1: mcp-memory recall 정확도
- **측정**: 알려진 질의 N개 → recall() 호출 → 기대 결과와 비교
- **단위**: precision@k (상위 k개 결과 중 정답 비율)
- **측정 방법**: 테스트 셋 (질의, 기대 노드 ID) 쌍 준비 → 자동 실행
- **현재 baseline**: 측정 필요
- **수정 대상**: mcp-memory 설정, 온톨로지, BM25 파라미터

### M2: 세션 복구 시간
- **측정**: /restore 실행 → 복구 완료까지 wall-clock 시간
- **단위**: 초 (낮을수록 좋음)
- **측정 방법**: compact 후 restore 시나리오 자동 실행, 시간 기록
- **현재 baseline**: 측정 필요
- **수정 대상**: restore 스킬, compressor agent, save_session 구조

### M3: index-system 경로 해결 성공률
- **측정**: 알려진 경로 쿼리 N개 → `python -m src.cli refs/deps <path>` → 정답률
- **단위**: % (높을수록 좋음)
- **측정 방법**: (쿼리, 기대 결과) 테스트 셋 → 자동 실행
- **현재 baseline**: 측정 필요
- **수정 대상**: index-system 스캔 설정, 관계 추출 로직

### M4: 파이프라인 규칙 위반율
- **측정**: 파이프라인 작업 시뮬레이션 → hook exit code 집계
- **단위**: 위반 건수 / 전체 체크 수 (낮을수록 좋음)
- **측정 방법**: 테스트 시나리오 (올바른 구조, 의도적 위반) → hook 실행 → 정탐/오탐 비율
- **현재 baseline**: 측정 필요
- **수정 대상**: hook 로직, phase-rules.json, pipeline-rules.md

---

## 4. 실험 루프 설계 (초안)

```
┌─────────────────────────────────────────────┐
│  program.md (사람이 작성)                     │
│  - 최적화 목표 (어떤 메트릭?)                  │
│  - 수정 허용 범위 (어떤 파일?)                 │
│  - 제약 조건 (깨뜨리면 안 되는 것)              │
└──────────────┬──────────────────────────────┘
               │
               ▼
┌─────────── iteration N ──────────────┐
│                                       │
│  1. git checkout -b iter-N            │
│  2. measure(baseline)                 │
│  3. agent reads program.md            │
│  4. agent modifies target file        │
│  5. measure(candidate)                │
│  6. if improved:                      │
│       git commit "iter-N: +0.3%"      │
│     else:                             │
│       git checkout -- <file>          │
│  7. log results                       │
│                                       │
└───────────────────────────────────────┘
               │
               ▼ (repeat)
```

### autoresearch와의 차이점

| 항목 | autoresearch | auto-iterate (우리) |
|---|---|---|
| 메트릭 | 단일 (val_bpb) | 복합 (M1-M4, 선택) |
| 예산 | 5분 wall-clock | 1 iteration = 시나리오 1회 |
| 수정 대상 | train.py (코드) | .md/.py 설정 (선언적) |
| 평가 | 학습 실행 | 테스트 셋 실행 |
| 환경 | GPU, PyTorch | Claude Code CLI |
| 난이도 | 높음 (ML) | 중간 (설정 최적화) |

---

## 5. 구현 우선순위

### Phase 1: 가장 측정 가능한 것부터
1. **M4 (규칙 위반율)** — 테스트 셋 만들기 가장 쉬움. hook이 이미 exit code 반환.
2. **M1 (recall 정확도)** — mcp-memory에 테스트 인프라 일부 존재.
3. **M3 (경로 해결)** — index-system CLI 존재.
4. **M2 (복구 시간)** — 측정은 쉽지만 최적화 범위가 넓음.

### Phase 2: program.md 작성
- 메트릭 하나 선택
- 수정 허용 파일 지정
- 제약 조건 명시
- agent에게 iteration 지시

### Phase 3: 루프 자동화
- 스크립트: measure → agent 호출 → measure → diff → keep/discard
- 로그: iteration별 메트릭, diff, 판정

---

## 6. 열린 질문

1. **메트릭 선택**: 4종 중 첫 실험에 어떤 것? → M4 (규칙 위반율) 권장
2. **agent 모델**: iteration 내 수정을 누가? Sonnet(빠름) vs Opus(정확)
3. **iteration 예산**: 밤새 자동? 아니면 사람 감독 하에 N회?
4. **안전장치**: 수정이 시스템을 깨뜨리면? → git revert + 원본 백업
5. **program.md 진화**: 사람이 매일 개선? 아니면 meta-program도 자동?

---

## 7. 다음 단계

Research R1 완료 후 → Ideation R1:
- program.md 초안 작성
- M4 테스트 셋 설계
- iteration 스크립트 설계
- 첫 수동 실험 (agent 없이 사람이 루프 1회 돌려보기)
