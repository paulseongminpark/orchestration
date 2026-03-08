# Lessons — 자동 축적 교훈

> 에이전트 실패, 사용자 교정, 반복 실수에서 자동 추출.
> compressor Learn 단계에서 갱신. 최대 20개, FIFO.

## 최근 교훈

- [2026-03-08] Codex CLI: -p extract는 read-only sandbox → 파일 생성 시 반드시 -p implement 사용
- [2026-03-08] Codex CLI: cd로 workdir 변경 시 PowerShell이 /c/ 경로를 C:\c\로 이중 변환 — workdir 기본값 유지하거나 Windows 경로 사용
- [2026-03-08] Gemini -o 플래그는 output-format용, 파일 저장은 > 리다이렉트 사용
- [2026-03-08] defer_loading이 이미 auto 모드로 작동 중이었음 — MEMORY.md 정보가 outdated
- [2026-03-08] Codex -o 플래그: 파일 생성 불안정. stdout redirect (> file.md) 방식이 더 확실
- [2026-03-08] Codex 프롬프트: 한번에 3태스크 주면 스킬/메모리 읽기에 토큰 소모 → 1태스크씩 분리
