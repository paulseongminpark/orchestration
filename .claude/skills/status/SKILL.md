---
name: status
description: 프로젝트 현황
user-invocable: true
allowed-tools: Read, Bash
context: fork
agent: Explore
model: haiku
---

## Steps
1. context/STATE.md 읽기
2. `git log --oneline -5`
3. `git status --short`

## Output
완료 N / 진행 N / 막힌것 N + 최근 커밋
