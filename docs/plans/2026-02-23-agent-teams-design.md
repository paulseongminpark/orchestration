# Agent Teams & Linker System Design

> Date: 2026-02-23
> Status: Approved
> Version: v3.1 확장

## 개요

기존 v3.0 에이전트 16개 시스템에 **팀 3개 + 독립 에이전트 2개 + 디스패처 1개** 추가.
목표: 반복 작업 자동화, 멀티 AI 피드백 루프 닫기, 실시간 세션 간 맥락 공유.

## 아키텍처

```
사용자 요청 or 세션 시작
        │
  ┌─────▼──────┐
  │ meta-orch  │ ← 상태 분석 → 팀 선택 → 디스패치
  │ (Sonnet)   │
  └─┬───┬───┬──┘
    │   │   │
    ▼   ▼   ▼
 ┌──────┐ ┌──────────┐ ┌──────────┐
 │ T1   │ │ T2       │ │ T3       │
 │tech- │ │ai-feed   │ │daily-ops │
 │review│ │back-loop │ │          │
 │-ops  │ │          │ │          │
 └──────┘ └──────────┘ └──────────┘

  독립 PROACTIVE (상시):
  ┌────────────────┐  ┌────────────────┐
  │ context-linker │  │ project-linker │
  │ (Haiku, 상시)  │  │ (Sonnet, 커밋) │
  └────────────────┘  └────────────────┘
```

## 신규 에이전트 (7개, 16→23)

### 1. meta-orchestrator (독립)

| 항목 | 내용 |
|------|------|
| 모델 | Sonnet |
| 트리거 | 세션 시작 시 (catchup 직후), `/dispatch` 수동 |
| 입력 | STATE.md + 미반영 결정 + 미커밋 현황 + Inbox.md 신규 여부 |
| 출력 | 활성화할 팀 목록 + 각 팀 작업 지시 |

판단 로직:
- tech-review 미커밋 > 5개 → T1 활성화
- Inbox.md 새 항목 → T3 활성화
- 코드 변경 큰 세션 후 → T2 활성화
- 일반 작업 → 팀 없이 기존 에이전트만

### 2. context-linker (독립 PROACTIVE)

| 항목 | 내용 |
|------|------|
| 모델 | Haiku |
| 트리거 | (1) bash hook으로 매 Edit시 경량 append (에이전트 호출 없음) (2) 5분 간격 or 프로젝트 전환 시 에이전트 호출로 정리/스캔 |
| 역할 | 동시 열린 세션 간 실시간 맥락 공유 |

공유 파일: `orchestration/context/live-context.md`

```markdown
# Live Context
> 자동 관리. 수동 편집 금지.

## Active Sessions
| Session | Project | Started | Last Update |
|---------|---------|---------|-------------|

## Session: <id> (<project>)
- [HH:MM] 작업 내용 1줄 요약
```

작동 방식:
1. PostToolUse bash hook → live-context.md에 1줄 append (0 토큰)
2. 5분 간격 or 프로젝트 전환 → context-linker(Haiku) 호출
   - 다른 세션 항목 스캔
   - 관련 맥락 있으면 현재 세션에 알림
3. 세션 종료 → 해당 세션 섹션 제거
4. 24시간 지난 항목 자동 정리

기존 시스템과 관계:
```
context-linker (실시간, 세션 중) → 동시 세션 간 공유
    ↓ 세션 종료 시
compressor (요약 → session-summary.md, decisions.md) → 순차 세션 간 전달
    ↓ 다음 세션
catchup (복원) → 맥락 복구
```

### 3. project-linker (독립 PROACTIVE)

| 항목 | 내용 |
|------|------|
| 모델 | Sonnet |
| 트리거 | (1) 커밋 시점 (PostToolUse Bash에서 git commit 감지) (2) 세션 시작 시 어제 커밋 스캔 (3) 수동 호출 |
| 역할 | 프로젝트 간 변경 영향 감지 → TODO/알림 생성 |

작동 예시:
- portfolio에서 TechReviewSection 수정 커밋 → "tech-review 블로그 연계 검토 필요" TODO
- monet-lab 실험 커밋 → "ml-porter로 portfolio 이식 검토" TODO
- tech-review 프롬프트 변경 → "portfolio TechReviewSystemSection 영향 가능" 알림

### 4. tr-monitor (T1: tech-review-ops)

| 항목 | 내용 |
|------|------|
| 모델 | Haiku |
| 역할 | GitHub Actions 결과 수집, 생성 성공/실패 판별, KST 변환 |

### 5. tr-updater (T1: tech-review-ops)

| 항목 | 내용 |
|------|------|
| 모델 | Sonnet |
| 역할 | 프롬프트 파일 업데이트, keywords-log.md 관리, Smart Brevity 포맷 적용 |

### 6. ai-synthesizer (T2: ai-feedback-loop)

| 항목 | 내용 |
|------|------|
| 모델 | Opus |
| 역할 | gemini+codex 분석 결과 교차 검증 → 합의/불일치 분류 → 액션 아이템 도출 |

출력:
- 합의 항목 → agent.md "학습된 패턴"에 자동 반영
- 불일치 항목 → 사용자 판단 요청
- 액션 아이템 → TODO.md 추가

### 7. inbox-processor (T3: daily-ops)

| 항목 | 내용 |
|------|------|
| 모델 | Haiku |
| 역할 | daily-memo Inbox.md 파싱 → 카테고리 분류 → TODO.md 반영 |

## 팀 구성

### Team 1: tech-review-ops

| 에이전트 | 모델 | 신규? |
|----------|------|-------|
| tr-monitor | Haiku | 신규 |
| tr-updater | Sonnet | 신규 |
| content-writer | Opus | 기존 |
| commit-writer | Haiku | 기존 |

워크플로우:
```
tr-monitor → Actions 결과 수집
  → 실패: 원인 보고 (사용자 확인)
  → 성공: tr-updater에 전달
    → tr-updater → 프롬프트/키워드 업데이트
      → commit-writer → 커밋
```

트리거: meta-orchestrator 디스패치 or 수동

### Team 2: ai-feedback-loop

| 에이전트 | 모델 | 신규? |
|----------|------|-------|
| gemini-analyzer | Opus | 기존 |
| codex-reviewer | Sonnet+Codex | 기존 |
| ai-synthesizer | Opus | 신규 |

워크플로우:
```
gemini + codex (병렬)
  → ai-synthesizer
    → 합의 → agent.md 자동 반영
    → 불일치 → 사용자 판단
    → 액션 → TODO.md
```

트리거: 분석 체인 호출 시 자동

### Team 3: daily-ops

| 에이전트 | 모델 | 신규? |
|----------|------|-------|
| inbox-processor | Haiku | 신규 |
| orch-state | Sonnet | 기존 |
| morning-briefer | Haiku | 기존 |

워크플로우:
```
inbox-processor → 새 메모 TODO 반영
  → orch-state → STATE.md 갱신
    → morning-briefer → 통합 브리핑
```

트리거: meta-orchestrator 디스패치 or 세션 시작 시

## 체인 규칙 추가

```
# 기존 체인 (유지)
implement → code-reviewer(Opus) → commit-writer(Haiku)
pf-deployer → security-auditor → 사용자 확인 → push

# 분석 체인 (강화)
gemini + codex (병렬) → ai-synthesizer → 사용자 확인 → agent.md 반영

# tech-review 체인 (신규)
tr-monitor → tr-updater → commit-writer

# 일일 운영 체인 (신규)
inbox-processor → orch-state → morning-briefer

# 디스패치 체인 (신규)
catchup → meta-orchestrator → 팀 활성화

# 프로젝트 연동 (독립, 상시)
파일 변경 → bash hook append → context-linker(주기적) → 맥락 주입
커밋 감지 → project-linker → TODO/알림
```

## PROACTIVE 에이전트 목록 (업데이트)

```
기존: code-reviewer[Opus], commit-writer[Haiku], orch-state[Sonnet], compressor[Sonnet]
추가: context-linker[Haiku], project-linker[Sonnet]
합계: 6개
```

## 토큰 효율

| 에이전트 | 모델 | 일일 호출 | 일일 비용 |
|----------|------|----------|----------|
| meta-orchestrator | Sonnet | 3 | $0.27 |
| context-linker | Haiku | 30 | $0.03 |
| project-linker | Sonnet | 7 | $0.22 |
| ai-synthesizer | Opus | 0.3 | $0.25 |
| inbox-processor | Haiku | 1 | $0.01 |
| tr-monitor | Haiku | 0.4 | $0.01 |
| tr-updater | Sonnet | 0.4 | $0.02 |
| **합계** | | | **$0.81/일 (+6%)** |

최적화 포인트:
- context-linker: bash hook으로 매 Edit append (0 토큰) + 주기적 Haiku 정리
- project-linker: 커밋 시점만 트리거 (매 Edit 아님)
- meta-orchestrator: Opus → Sonnet 다운그레이드 (트리아지 작업)

## 구현 순서

1. **Phase 1**: context-linker + project-linker (독립 PROACTIVE, 즉시 효용)
   - live-context.md 생성
   - PostToolUse bash hook 추가
   - agent.md 2개 작성
2. **Phase 2**: meta-orchestrator + daily-ops 팀
   - meta-orchestrator agent.md
   - inbox-processor agent.md
   - 디스패치 스킬 `/dispatch`
3. **Phase 3**: tech-review-ops 팀
   - tr-monitor, tr-updater agent.md
   - GitHub Actions API 연동
4. **Phase 4**: ai-feedback-loop 강화
   - ai-synthesizer agent.md
   - 분석 체인 자동 연결

## 새 파일 목록

```
~/.claude/agents/meta-orchestrator.md
~/.claude/agents/context-linker.md
~/.claude/agents/project-linker.md
~/.claude/agents/tr-monitor.md
~/.claude/agents/tr-updater.md
~/.claude/agents/ai-synthesizer.md
~/.claude/agents/inbox-processor.md
orchestration/context/live-context.md
```
