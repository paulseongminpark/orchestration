# Research 인벤토리 — 수정 대상 + 측정 도구
> 2026-03-15

## 수정 가능 파일 인벤토리

### Agents (15개)
ai-synthesizer, code-reviewer, codex-reviewer, commit-writer, compressor, daily-ops, doc-ops, gemini-analyzer, linker, meta-orchestrator, orch-state, pf-ops, project-context, security-auditor, tr-ops

### Skills (14개+ user-invocable)
brainstorming, checkpoint, commit-push-pr, delegate-to-codex, delegate-to-gemini, excalidraw-diagram, gpt-review, loop, merge, pipeline, restore, simplify, cascade, frontend-design 등

### Hooks (14개)
auto_remember.py, governance-audit.sh, notify-sound.py, pipeline-watch.py, post-tool-live-context.sh, post_tool_impact.py, pre-compact.sh, pre-tool-use.sh, relay.py, session-start.sh, session_start_index.py, validate_merged.py, validate_output.py, validate_pipeline.py

### Rules (3개)
common-mistakes.md, pipeline-rules.md, workflow.md

### Config
config.json, keybindings.json

## 측정 인프라
- mcp-memory: recall() API, 169 tests 존재
- index-system: `python -m src.cli` CLI
- pipeline hooks: exit code 0/2 반환
- /restore skill: wall-clock 측정 가능
