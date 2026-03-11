# Lessons — 자동 축적 교훈

> 에이전트 실패, 사용자 교정, 반복 실수에서 자동 추출.
> compressor Learn 단계에서 갱신. 최대 20개, FIFO.

## 최근 교훈

- [2026-03-11] 08 시스템 미준수 근본: Claude의 기본 행동이 "문제 해결"을 우선하여 /pipeline을 바이패스. 유기적 전환("논의→고치자→코드")은 트리거 목록으로 잡히지 않음. 해법은 행동 감지 Hook(Edit/Write 시 pipeline 체크).
- [2026-03-11] compact 후 복구에 2레이어 필요: 장기 기억(DB, get_context/recall) + 단기 작업 상태(파이프라인 index). save_session() active_pipeline으로 연결.
- [2026-03-11] index-system v1: Code Review R1에서 Critical 버그 4개(경로, 순환참조, 인코딩, edge 중복) 발견. R1 없이 배포 불가. 리뷰 2라운드(R1:버그, R2:검증)가 최적.
- [2026-03-11] 라운드 방향성(Diverge/Cross/Converge)은 권장 패턴이지 강제 순서 아님 — 고정하면 사고 제약. foundation 3축은 Ideation 완료 시 한꺼번에 생성.
- [2026-03-11] Opus는 merged만 읽어야 한다. 개별 라운드 파일을 읽으면 컨텍스트 낭비 + 편향 발생.
- [2026-03-08] Codex CLI: -p extract는 read-only sandbox → 파일 생성 시 반드시 -p implement 사용
- [2026-03-08] Codex CLI: cd로 workdir 변경 시 PowerShell이 /c/ 경로를 C:\c\로 이중 변환 — workdir 기본값 유지하거나 Windows 경로 사용
- [2026-03-08] Gemini -o 플래그는 output-format용, 파일 저장은 > 리다이렉트 사용
- [2026-03-08] defer_loading이 이미 auto 모드로 작동 중이었음 — MEMORY.md 정보가 outdated
- [2026-03-08] Codex -o 플래그: 파일 생성 불안정. stdout redirect (> file.md) 방식이 더 확실
- [2026-03-08] Codex 프롬프트: 한번에 3태스크 주면 스킬/메모리 읽기에 토큰 소모 → 1태스크씩 분리
