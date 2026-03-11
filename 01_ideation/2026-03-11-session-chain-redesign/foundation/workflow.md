# 워크플로우 — 세션 체인 v4.1 사용자 가이드

## 세션 시작

바뀐 것 없음. 평소대로 시작.
- session-start.sh가 미커밋 현황 + 미반영 결정 알려줌
- Claude가 recall()로 이전 세션 맥락 가져옴 (이제 Decision/Question 노드로 검색됨)

### compact 후 복구 프롬프트

compact 직후 새 세션을 시작할 때 Claude에게 이렇게 말한다:

```
이전 세션 복구해줘. [작업 키워드]
```

예시:
```
이전 세션 복구해줘. mcp-memory 온톨로지 작업.
이전 세션 복구해줘. portfolio 레이아웃 결정.
```

Claude가 하는 것:
1. `get_context()` — 최근 저장된 세션 요약 + 미결 질문 가져옴
2. `recall("[작업 키워드]")` — 관련 Decision/Question 노드 검색
3. 복구된 내용 요약 후 "이어서 진행할까요?" 확인

**키워드 없이 그냥 "복구해줘"도 됨** — get_context()로 최근 세션 맥락은 자동으로 가져옴.
키워드를 주면 해당 작업의 Decision/Question 노드까지 정확히 검색됨.

## 세션 중

### 자동 (신경 안 써도 됨)
- 파일 수정하면 auto_remember가 타입 매핑해서 DB에 저장
  - STATE.md 수정 → Decision, CLAUDE.md 수정 → Principle, 등
- Bash에서 FAIL/PASS 나오면 Failure/Experiment로 자동 저장
- 이전: 전부 Observation으로 뭉뚱그려 저장 → 이제: 파일명이 타입을 결정

### 수동 (/checkpoint)
- 이전과 동일. Claude가 대화 중 메타 관찰해서 기억 저장
- 이것은 기계적 auto_remember와 다른 종류의 정보 — 둘 다 필요

## 세션 종료

### 이전 (11단계 + 사전/사후 작업)
```
verify → /sync all → /session-end → compressor(Opus) 11단계:
  1. session-summary.md
  2. LOG append
  3. STATE.md
  4. decisions.md
  5. METRICS.md
  6. pending.md (선택)
  7. MEMORY.md (선택)
  8. doc-ops
  9. doc-ops verify
  10. Learn
  11. save_session 데이터 전달
→ /compact → linker → "새 세션 준비 완료"
```

### 지금 (2단계)
```
/session-end → /compact
```

끝. 내부에서 일어나는 것:
1. compressor(Sonnet)가 LOG + Living Docs + Commit + Learn 처리
2. Claude(Opus)가 save_session() 호출 → Decision/Question이 그래프 노드로 저장
3. /compact로 세션 전환

**없어진 것:**
- `/sync all` — 필요 없음. compressor가 commit+push 함
- `verify` — 세션 전환 전에 별도로 안 돌려도 됨
- `linker` — 세션 전환 후 별도 호출 불필요
- `pending.md` — 에이전트 학습 후보 수집 폐기. DB 노드가 대체
- `decisions.md append` — save_session()이 Decision 노드로 저장
- `METRICS.md` — 별도 저장 불필요
- `doc-ops verify` — compressor 검증으로 통합

## MEMORY.md

### 이전
- Claude가 수동으로 갱신
- analyze-session.sh + auto-promote.sh + /sync all이 반자동 갱신

### 지금
- 고정 섹션: 직접 수정 (System Version, User Preferences 등)
- 동적 섹션: `python render_memory_md.py`로 DB에서 자동 생성
- `<!-- DYNAMIC -->` 마커 아래는 스크립트가 덮어씀
- 아직 수동 실행. 필요할 때 돌리면 됨.

## 요약: Paul이 달라지는 것

| 항목 | 이전 | 지금 |
|------|------|------|
| 세션 종료 | `/sync all` → `/session-end` → `/compact` + 후처리 | `/session-end` → `/compact` |
| pending.md | 가끔 확인, /sync all 때 검증 | 없음. DB 노드로 대체 |
| decisions.md | compressor가 append | save_session()이 노드로 저장 |
| MEMORY.md 갱신 | Claude 수동 | 스크립트 또는 Claude |
| 세션 맥락 복구 | MEMORY.md 읽기 + recall | recall()만 (노드가 더 풍부) |
