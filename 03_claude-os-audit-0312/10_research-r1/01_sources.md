# Research R1: 인프라 시스템 — 추출 결과
> 2026-03-12 | Codex 5.4 xhigh 파일 선별 + 읽기 완료
> 위임: delegate-to-codex → `/c/dev/.ctx/delegates/2026-03-12-1931-system-file-selection.md`

## 파일 선별 결과 (31개)

### [08] documentation-system (16개)
| 파일 | 역할 |
|---|---|
| `foundation/philosophy.md` | 설계 최상위 의도 ("압축은 구조화", mcp-memory 영감 출발점) |
| `foundation/principles.md` | 폴더/파일/번호/인덱스/pane 규칙 핵심 명문화 |
| `foundation/workflow.md` | 실제 운영 플로우 + mcp-memory recall/save_session 연결 직접 명시 |
| `foundation/phase-guide.md` | 최신 인간용 SoT. Phase 전환/02_context/merged/DONE gate 기준선 |
| `phase-rules.json` | 기계 실행 가능 SoT (35개 규칙, D1~D19) — 감사 핵심 판단 기준 |
| `templates/research.template.md` | Research 규칙 → 템플릿 구현 증거 |
| `templates/ideation.template.md` | Ideation merged 구조 (00_orchestrator-final/01_confirmed-decisions) |
| `templates/full-impl.template.md` | Implementation/Review 전체 사이클 구조 |
| `templates/code-review.template.md` | 리뷰 도메인 병렬 규칙 구현 |
| `templates/custom.template.md` | 예외 작업 최소 골격 |
| `examples/mcp-memory-v2.md` | 08 규칙이 ontology/mcp-memory 실전 적용된 가장 직접적 사례 |
| `STATE.md` | v2.0, hook 4개+pipeline skill+규칙전파 완료 확인 |
| `CHANGELOG.md` | 설계→구현 변천 근거 |
| `03_meta-loop-fix_0312/90_output/00_final-output.md` | phase-rules.json+hook+AGENTS 전파 실제 구현 산출물 요약 |
| `03_meta-loop-fix_0312/90_output/01_handoff.md` | SoT 전파 레이어: ~/.claude/hooks, ~/.claude/rules, /c/dev/AGENTS.md |
| `index.md` | 시스템 범위 진입점 |

### [09] context-cascade-system (5개)
| 파일 | 역할 |
|---|---|
| `foundation/philosophy.md` | 09 존재 이유 + 08/10/mcp-memory 관계 명시 |
| `foundation/principles.md` | 파일 선별/추출/검증/축적 역할 분담 + mcp-memory 축적 원칙 |
| `foundation/workflow.md` | Step 0~4 흐름, Codex 선별, INDEX.md 사용, mcp-memory 연결 포인트 |
| `01_reading-pipeline_0310/22_ideation-merged/00_index.md` | 최종 merged 문서 + 08 최신 규칙 대비 gap 확인점 |
| `01_reading-pipeline_0310/90_output/01_design-summary.md` | 10 후속 설계, lens 라이브러리의 mcp-memory 저장 계획 |

### [10] index-system (12개)
| 파일 | 역할 |
|---|---|
| `foundation/philosophy.md` | graph-first, derived-data, mcp-memory 분리 철학 |
| `foundation/principles.md` | 08 규칙 연동, 엣지 타입, short-name/경로 정규화, mcp-memory 관계 설계 |
| `foundation/workflow.md` | cascade Step 0 대체, CLI 사용 흐름, 구현 순서 |
| `01_design-pipeline_0310/23_ideation-merged/00_index.md` | 최종 설계 통합본. 08/09/06 의도적 관계 명시 |
| `01_design-pipeline_0310/90_output/01_design-summary.md` | 구현 범위 + 후속 작업 |
| `src/config.py` | 스캔 범위, 제외 규칙, SHORT_NAME_MAP, edge taxonomy 정책 레이어 |
| `src/scanner.py` | 08 규칙 파싱, reference 추출, path 정규화, project 분류 핵심 코드 |
| `src/graph.py` | 그래프 모델 + refs/deps/rdeps/impact/topology/stale 쿼리 |
| `src/views.py` | graph.json → views/INDEX.md 투영 |
| `src/cli.py` | CLI 구현 진입점 |
| `graph.json` | 실제 그래프 데이터 (노드+엣지 실상태) |
| `views/INDEX.md` | 현재 그래프 세션 시작용 조감도 |

---

## Skip 목록 (8개)
- `02_ecosystem-setup_0311/foundation/*` — 최신 root foundation이 최신 SoT
- `03_meta-loop-fix_0312/foundation/*` — root foundation과 역할 중복
- `02_ecosystem-setup_0311/90_output/00_index.md` — 정보 밀도 낮음
- `01_lifecycle-methodology_0311/90_output/` — 비어 있음
- `src/__init__.py` — 기능 없음
- `01_design-pipeline_0310/90_output/02_pane1-prompt.md` — 프롬프트 흔적
- `01_design-pipeline_0310/90_output/03_pane1-fix-prompt.md` — 프롬프트 흔적

---

## 예상 gap 포인트 (Codex 사전 발견, R1 기준)

| # | Gap | 위치 | 심각도 |
|---|---|---|---|
| G1 | 09/10 merged 폴더에 `00_orchestrator-final.md`, `01_confirmed-decisions.md` 누락 | 09: `22_ideation-merged/`, 10: `23_ideation-merged/` | T1 규칙 위반 후보 |
| G2 | graph.json에 08/09/10 간 연결 edge 없음 | `10/graph.json` | 설계-구현 gap |
| G3 | `SHORT_NAME_MAP`이 `scanner.py`에서 실제 미사용 | `10/src/config.py` vs `scanner.py` | 시스템 간 참조 누락 |
| G4 | edge 6종 중 `depends-on`, `path-ref`만 구현 (4종 미구현) | `10/src/scanner.py` | 설계-구현 gap |
| G5 | `index scan --diff` 옵션 없음 | `10/src/cli.py` | CLI 설계-구현 불일치 |
| G6 | `move_check()` 구현 부족 | `10/src/graph.py` | 설계-구현 gap |
| G7 | 온톨로지/mcp-memory 연결: 문서적 연결만 있고 코드 레벨 직접 통합 없음 | 전체 시스템 | **핵심 gap** |

---

## 현재 상태 요약 (Codex 읽기 기준)

- **08**: v2.0 완전 구현. phase-rules.json(35규칙) + Hook 4개 + 규칙전파 완료. SoT 명확.
- **09**: 설계 완료. foundation 3축 + workflow 명확. 구현은 스킬(cascade/SKILL.md)로 위임됨.
- **10**: 설계 완료, 구현 부분 완료. graph.json 생성 기능 작동. 연결 edge 일부 미구현.
- **전체**: 시스템 간 연결은 설계 문서에 명시되어 있지만 코드/그래프 레벨 통합 미완.

---

## 다음: Research R2
- 대상: `06_mcp-memory/` 온톨로지 설계 문서 + entity/relation 타입 정의
- 연결 매핑: 온톨로지 ↔ 08/09/10 ↔ Claude OS 레이어
