# Plan — Cross-Session Cleanup

## 목표
3~4개 Opus 세션의 미커밋 변경을 검증·정리·커밋

## 손실불가 기준
- 모든 세션의 변경사항 보존 (덮어쓰기 금지)
- Hook/Skill 정합성 (T1 + lightweight 공존 검증)

## 대상
- 11_user-guide (전체)
- ~/.claude (hooks, skills, rules, settings)
- 08_documentation-system (phase-rules.json, phase-guide.md, STATE.md)
- dev-vault (AGENTS.md, HOME.md)

## 단계
1. ✅ 현황 파악 + 문제 분류
2. 🔄 Fixer 프롬프트 생성
3. ⬜ Fixer 1 + 2 병렬 실행
4. ⬜ Fixer 결과 검증
5. ⬜ git init (11_user-guide) + commit (4개 repo) + push
6. ⬜ Living Docs 갱신 (STATE.md, CHANGELOG.md, HOME.md)

## Pane 분배
- Fixer 1 (Opus): 문서 정비 — 11_user-guide Living Docs + HOME.md
- Fixer 2 (Opus): 시스템 검증 — Hook 교차 검증 + 08 Living Docs
- Meta (Opus 1M): 조율 + git + 최종 검증
