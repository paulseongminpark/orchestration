# 워크플로우 — 세션 체인 실행

## 세션 중: 자동 기록

```
[PostToolUse Hook — auto_remember.py]

Write/Edit 감지
  → 파일명이 FILE_TYPE_MAP에 있으면:
    → 타입+레이어 결정 (STATE.md → Decision L1)
    → confidence = CONFIDENCE_BY_LAYER[layer]
    → remember() 호출
  → 없으면: 무시

Bash 감지
  → 출력에 BASH_SIGNAL_MAP 시그널 있으면:
    → Failure 우선 매칭
    → get_project(cmd)로 프로젝트 감지
    → remember() 호출
  → BASH_TRIGGER_ONLY ("테스트", "완료")만 있으면:
    → Observation L0으로 기록
  → 없으면: 무시
```

이것은 완전 자동. Claude도 Paul도 관여하지 않는다.

## 세션 중: 수동 관찰

```
[/checkpoint — Claude 판단]

Claude가 대화 중 메타적으로 관찰:
  → Paul의 사고 패턴, 선호, 행동
  → 기술적 발견, 실패에서 배운 것
  → remember() 호출 (type은 Claude가 판단)
```

이것은 수동. Claude가 적절한 시점에 실행한다.

## 세션 종료: 5단계 체인

```
/session-end 호출
  → compressor(Sonnet) 에이전트 가동

1. LOG
   - session-summary.md 갱신 (최근 3개 유지)
   - _history/logs/YYYY-MM-DD.md에 append
   - 타임스탬프: `date +%H:%M` (LLM 추정 금지)

2. Living Docs
   - STATE.md 갱신 (이번 세션 주 프로젝트)
   - CHANGELOG.md 갱신

3. Commit
   - 변경된 프로젝트 전부 git add → commit → push
   - 메시지: "[project] 한줄 설명"

4. save_session 데이터 반환
   - compressor → lead agent(Opus)에게 전달:
     summary, decisions[], unresolved[], project
   - lead agent가 save_session() MCP 호출
   - → Narrative + Decision + Question 노드 생성
   - → 명시적 edge (contains) 연결

5. Learn
   - Discovery / Lesson / Improvement / Paul 관찰 (4줄)
   - lead agent가 remember(type="Insight") MCP 호출
   - lessons.md에 append (20개 FIFO)

→ lead agent: /compact 진행
```

## 세션 전환

```
이전: verify → /sync all → /session-end → /compact → linker → "준비 완료"
이후: /session-end → /compact
```

6단계 → 2단계. verify, /sync all, linker 제거.

## 모니터링 (Phase 1.5)

```
구현 후 2~3세션 동안:
  → ontology_review 실행
  → 확인: Observation 비율이 다시 높아지지 않는지
  → 확인: save_session edge가 정상 생성되는지
  → 확인: auto_remember TYPE_MAP 매칭 정확도
  → 문제 발견 시: TYPE_MAP 또는 SIGNAL_MAP 수정
```

## 렌더링 (선택적)

```
python scripts/render_memory_md.py
  → DB 쿼리: L3 전체, L2 상위 15, 최근 Decision 5, Question 전체, Failure 3
  → MEMORY.md의 DYNAMIC_MARKER 이후를 교체
  → 200줄 이내 보장
```

자동 실행 아님. 필요할 때 수동 또는 cron.
