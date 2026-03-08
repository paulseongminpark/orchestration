# Codex Skill Trigger Patches

Source inputs read:
- `C:\dev\.agents\skills\diff-only\SKILL.md`
- `C:\dev\.agents\skills\review-checklist\SKILL.md`
- `C:\dev\.agents\skills\state-reader\SKILL.md`
- `C:\dev\.agents\skills\test-matrix\SKILL.md`
- `C:\dev\.agents\skills\worktree-setup\SKILL.md`
- `C:\dev\01_projects\01_orchestration\02_implementation\2026-03-08\gm-skill-trigger-audit.md`

Each `Current` line below is an exact copy of the current `description` value.

### diff-only
**Current**: 설명 없이 diff만 생성한다. 순수 변경분만 출력.

**Proposed**:
```yaml
name: diff-only
description: |
  설명 없이 diff만 생성한다. 순수 변경분만 출력한다.
  TRIGGER when: user explicitly asks for diff only, patch only, change-only output, or says no explanation is needed
  DO NOT TRIGGER when: user asks for code review, explanation, debugging, root-cause analysis, or full-file/context reading
```

### review-checklist
**Current**: 보안/회귀/테스트 관점에서 체크리스트 기반 리뷰를 수행한다.

**Proposed**:
```yaml
name: review-checklist
description: |
  보안/회귀/테스트 관점에서 체크리스트 기반 리뷰를 수행한다.
  TRIGGER when: user asks for code review, PR review, diff review, security review, regression review, or checklist-based verification
  DO NOT TRIGGER when: user asks for implementation, file creation, pure diff output, or project state/status summarization
```

### state-reader
**Current**: STATE.md + git status를 읽고 1페이지 압축 요약을 JSON으로 출력한다.

**Proposed**:
```yaml
name: state-reader
description: |
  STATE.md + git status를 읽고 1페이지 압축 요약을 JSON으로 출력한다.
  TRIGGER when: user asks for current project status, work-start context, STATE.md summary, git status summary, or recent-commit overview
  DO NOT TRIGGER when: user asks for code changes, test execution, diff generation, or checklist-based review
```

### test-matrix
**Current**: 변경된 파일에 필요한 최소 테스트셋을 추출한다.

**Proposed**:
```yaml
name: test-matrix
description: |
  변경된 파일에 필요한 최소 테스트셋을 추출한다.
  TRIGGER when: user asks what tests to run, minimal test scope, affected tests, test impact analysis, or post-change verification scope
  DO NOT TRIGGER when: user asks for feature implementation, code review, pure diff output, or project state/status summarization
```

### worktree-setup
**Current**: worktree override 파일(AGENTS.override.md)을 자동 생성한다.

**Proposed**:
```yaml
name: worktree-setup
description: |
  worktree override 파일(AGENTS.override.md)을 자동 생성한다.
  TRIGGER when: user asks to start isolated work in a worktree, set up worktree task context, or generate AGENTS.override.md for a new scoped task
  DO NOT TRIGGER when: user asks for implementation inside an existing task, code review, test execution, or general repo status summarization
```
