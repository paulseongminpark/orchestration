# v3.3 전체 시스템 e2e 테스트 플랜

> 작성: 2026-02-25 | 모델: Opus 4.6 (1M)
> 목적: 24에이전트 + 14스킬 + 4팀 + 6체인 + 7훅 + 2CLI 전수 검증

## 테스트 구조

- **1차 실험**: 기본 모델 정책 (Haiku/Sonnet/Opus 각 에이전트 설정대로)
- **2차 실험**: 모든 과정 Opus 사용
- **비교 분석**: 1차 vs 2차 품질·정확도·비용 비교

## 원소 매핑

| 카테고리 | 수량 | 테스트 시나리오 |
|----------|------|----------------|
| Agents | 24 글로벌 + 2 로컬 | S1~S10 |
| Skills | 14 글로벌 + 5 프로젝트 | S1~S10 + 개별 |
| Teams | 4 + hub | S1, S2, S3, S4, S6 |
| Chains | 6 | S2, S3, S5, S6, S7 |
| Hooks | 7 | S1, S2, S4, S6 |
| CLIs | 2 (Codex, Gemini) | S3 |

---

## 시나리오 목록

### S1: Morning Operations (ops 팀)
**테스트 대상**: morning-briefer, inbox-processor, tr-monitor, /morning, /todo, SessionStart hook
**절차**:
1. SessionStart hook 출력 검증 (이미 발동됨)
2. /morning 스킬 호출 → morning-briefer 에이전트 동작 확인
3. /todo 스킬 호출 → inbox 체크 + TODO 출력
4. tr-monitor 에이전트 → GitHub Actions 결과 수집
5. inbox-processor 에이전트 → Inbox.md 파싱
**통과 기준**:
- [ ] SessionStart: 프로젝트 상태 + 미커밋 + 미반영 결정 출력됨
- [ ] /morning: 전체 프로젝트 현황 대시보드 출력
- [ ] /todo: TODO.md 내용 + Inbox 체크 완료
- [ ] tr-monitor: Actions 결과 또는 "실행 내역 없음" 반환
- [ ] inbox-processor: Inbox 파싱 결과 반환

### S2: Code Change & Review (build 팀 - 구현 체인)
**테스트 대상**: code-reviewer, commit-writer, /verify, /cross-review, PreToolUse hook, PostToolUse hook, 구현 체인
**절차**:
1. 테스트용 파일 수정 (evidence 문서에 테스트 마커 추가)
2. /verify 스킬 호출 → 규칙 검증
3. code-reviewer 에이전트 → 변경사항 리뷰 (4축: 버그/보안/성능/가독성)
4. /cross-review 스킬 → Codex 병렬 리뷰 (Codex 사용량 주의)
5. commit-writer 에이전트 → 커밋 메시지 생성
6. PreToolUse hook 검증: `rm -rf` 시도 → 차단 확인
7. PostToolUse hook 검증: 파일 수정 시 live-context.md 기록 확인
**통과 기준**:
- [ ] /verify: SAFE TO COMMIT 또는 구체적 위반사항 출력
- [ ] code-reviewer: 4축 리뷰 결과 (RED/YELLOW/GREEN)
- [ ] /cross-review: Claude + Codex 교차 결과
- [ ] commit-writer: `[project] 설명` 형식 메시지
- [ ] PreToolUse: 위험 명령 차단 (exit 2)
- [ ] PostToolUse: live-context.md에 기록 추가

### S3: Context Extraction & Verification (analyze 팀 - 추출/검증 체인)
**테스트 대상**: gemini-analyzer, codex-reviewer, ai-synthesizer, /context-scan, Gemini CLI, Codex CLI, 추출/검증 체인
**절차**:
1. /context-scan system → Gemini system-scanner 호출
2. Gemini 출력 JSON 파싱 + _meta 검증
3. /context-scan git → Codex extract-git-history 호출
4. Codex 출력 JSON 파싱 + _meta 검증
5. ai-synthesizer → Verify Barrier 3단계 (구조→스팟체크→반박)
**통과 기준**:
- [ ] Gemini: JSON 출력 + _meta(model, completeness, files_scanned, fields_extracted, skipped)
- [ ] Codex: JSON 출력 + _meta(files_scanned, fields_extracted, skipped)
- [ ] ai-synthesizer: 3단계 검증 통과 또는 구체적 불일치 보고
- [ ] /context-scan: 전체 파이프라인 완료 + 요약 출력

### S4: Documentation Maintenance (maintain 팀)
**테스트 대상**: doc-syncer, orch-doc-writer, orch-skill-builder, /docs-review, /sync-all, /memory-review
**절차**:
1. doc-syncer 에이전트 → STATE.md vs 실제 파일 3레이어 검증
2. /docs-review 스킬 → 전체 Living Docs stale 감지
3. orch-doc-writer 에이전트 → 테스트 결과 문서 작성 지시
4. orch-skill-builder 에이전트 → 스킬 템플릿 생성 능력 확인
5. /memory-review 스킬 → MEMORY.md 품질 점검
6. /sync-all 스킬 → 전체 프로젝트 동기화 (최종 단계에서)
**통과 기준**:
- [ ] doc-syncer: 3레이어 검증 리포트 (로컬/GitHub/HOME.md)
- [ ] /docs-review: STALE/CURRENT 분류 + 업데이트 제안
- [ ] orch-doc-writer: 구조화된 문서 출력
- [ ] orch-skill-builder: 올바른 스킬 템플릿 형식
- [ ] /memory-review: MEMORY.md 항목별 상태 + 정리 제안
- [ ] /sync-all: 모든 프로젝트 commit + push 성공

### S5: Session Management (압축 체인)
**테스트 대상**: compressor, context-linker, /compressor, /session-insights, 압축 체인
**절차**:
1. /session-insights 스킬 → 현재 세션 토큰/비용 분석
2. context-linker 에이전트 → live-context.md 정리
3. compressor 에이전트 → 7단계 압축 시뮬레이션 (dry-run)
**통과 기준**:
- [ ] /session-insights: 토큰 사용량 + 비용 + 구간 판정
- [ ] context-linker: live-context.md 업데이트 (프로젝트별 분류)
- [ ] compressor: 7단계 구조 확인 (session-summary, LOG, STATE, decisions, METRICS, pending, MEMORY)

### S6: Team Dispatch (디스패치 체인)
**테스트 대상**: meta-orchestrator, orch-state, /dispatch, TeammateIdle hook, TaskCompleted hook, 디스패치 체인
**절차**:
1. orch-state 에이전트 → 현재 상태 분석 + 다음 3개 액션 제안
2. meta-orchestrator 에이전트 → 팀 추천 + 이유
3. /dispatch 이미 실행됨 → 결과 검증
4. 미니 팀 생성 → 태스크 할당 → TeammateIdle/TaskCompleted hook 발동 확인
**통과 기준**:
- [ ] orch-state: STATE 분석 + 3개 액션 제안
- [ ] meta-orchestrator: 팀 추천 + 근거
- [ ] /dispatch: 세션 방향 + 추천 출력
- [ ] TeammateIdle: 유휴 알림 메시지 수신
- [ ] TaskCompleted: 완료 알림 메시지 수신

### S7: Portfolio Pipeline (배포 체인)
**테스트 대상**: pf-reviewer, pf-deployer, security-auditor, project-context, 배포 체인
**절차**:
1. project-context 에이전트 → portfolio STATE + git log + diff 수집
2. pf-reviewer 에이전트 → 코드/디자인/접근성 리뷰
3. pf-deployer 에이전트 → 배포 체크리스트 실행 (GO/NO-GO)
4. security-auditor 에이전트 → XSS/env/CORS/인증 점검
**통과 기준**:
- [ ] project-context: portfolio 컨텍스트 수집 완료
- [ ] pf-reviewer: TypeScript + 반응형 + 접근성 리뷰 결과
- [ ] pf-deployer: 체크리스트 결과 + GO/NO-GO 판정
- [ ] security-auditor: 보안 점검 결과 + GO/NO-GO 판정

### S8: Content & Tech Review
**테스트 대상**: content-writer, tr-updater, /write, /tr-verify, /research
**절차**:
1. /write 스킬 → content-writer 질문 프레임워크 확인
2. content-writer 에이전트 → 짧은 테스트 글 작성
3. tr-updater 에이전트 → tech-review 현황 확인
4. /tr-verify 스킬 → 최신 포스트 QA (Gemini + Codex 병렬)
5. /research 스킬 → 간단한 리서치 태스크 (--depth quick)
**통과 기준**:
- [ ] /write: 5가지 질문 프레임워크 출력
- [ ] content-writer: 구조화된 글 출력 (아웃라인→초안)
- [ ] tr-updater: tech-review 상태 리포트
- [ ] /tr-verify: 팩트체크 + 포맷 QA 결과
- [ ] /research: 코드베이스 탐색 결과 + 소스

### S9: Cross-Project Impact
**테스트 대상**: project-linker, context-linker, project-context
**절차**:
1. project-linker 에이전트 → 연관 맵 기반 영향 분석
2. project-context 에이전트 → orchestration 컨텍스트 수집
3. context-linker 에이전트 → 크로스세션 맥락 필터링 + 주입
**통과 기준**:
- [ ] project-linker: 영향받는 프로젝트 목록 + TODO 생성
- [ ] project-context: STATE + git log + diff 출력
- [ ] context-linker: live-context.md 정리 완료

### S10: Monet Lab Experiments
**테스트 대상**: ml-experimenter, ml-porter
**절차**:
1. ml-experimenter 에이전트 → monet-lab 현재 실험 리뷰
2. ml-porter 에이전트 → portfolio 이식 준비 상태 판단
**통과 기준**:
- [ ] ml-experimenter: 실험 리뷰 + 개선 방향 제안
- [ ] ml-porter: 이식 가능 여부 + 필요 작업 목록

---

## 추가 개별 테스트

### S11: Hook 개별 검증
- [ ] PreCompact hook: 미커밋 있을 때 경고 출력 확인
- [ ] SessionEnd hook: 스크립트 존재 + 동작 로직 확인 (실제 발동은 세션 종료 시)
- [ ] Notification hook: notify-sound.py 존재 확인

### S12: 로컬 에이전트
- [ ] architect (orchestration): 설계 문서 출력 능력
- [ ] reviewer (orchestration): STATE 검증 체크리스트 실행

---

## 실행 순서

```
Phase 1 (읽기 전용): S1 → S6 → S9 → S10 → S11 → S12
Phase 2 (분석/리뷰): S3 → S7 → S8
Phase 3 (상태 변경): S2 → S4 → S5
```

## 커버리지 매트릭스

| 에이전트 | 시나리오 | 스킬 | 시나리오 | 훅 | 시나리오 |
|----------|---------|------|---------|-----|---------|
| morning-briefer | S1 | /morning | S1 | SessionStart | S1 |
| inbox-processor | S1 | /sync-all | S4 | SessionEnd | S11 |
| tr-monitor | S1 | /todo | S1 | PreToolUse | S2 |
| tr-updater | S8 | /dispatch | S6 | PostToolUse | S2 |
| code-reviewer | S2 | /compressor | S5 | PreCompact | S11 |
| pf-reviewer | S7 | /verify | S2 | TeammateIdle | S6 |
| pf-deployer | S7 | /docs-review | S4 | TaskCompleted | S6 |
| ml-experimenter | S10 | /cross-review | S2 | | |
| security-auditor | S7 | /session-insights | S5 | | |
| ai-synthesizer | S3 | /memory-review | S4 | | |
| gemini-analyzer | S3 | /research | S8 | | |
| codex-reviewer | S3 | /context-scan | S3 | | |
| compressor | S5 | /write | S8 | | |
| doc-syncer | S4 | /tr-verify | S8 | | |
| orch-doc-writer | S4 | | | | |
| orch-skill-builder | S4 | | | | |
| context-linker | S5/S9 | | | | |
| project-linker | S9 | | | | |
| commit-writer | S2 | | | | |
| orch-state | S6 | | | | |
| project-context | S7/S9 | | | | |
| content-writer | S8 | | | | |
| meta-orchestrator | S6 | | | | |
| ml-porter | S10 | | | | |
