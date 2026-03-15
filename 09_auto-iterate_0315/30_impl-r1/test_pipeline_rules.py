#!/usr/bin/env python3
"""
test_pipeline_rules.py — validate_pipeline.py 정확도 측정
fixture 기반 시나리오 → hook 실행 → precision/recall/F1 보고
"""
import json, os, sys, subprocess, tempfile, shutil
from pathlib import Path

HOOK = os.path.expanduser("~/.claude/hooks/validate_pipeline.py")

# ─── Fixture builder ───────────────────────────────────────────────

def make_pipeline(tmp, name="01_test-pipe_0315", index_content=None,
                  plan=True, phase_dirs=None, foundation=False,
                  lightweight=False):
    """테스트용 파이프라인 구조 생성"""
    pipe_root = os.path.join(tmp, "01_projects", "01_orch", name)
    os.makedirs(pipe_root, exist_ok=True)

    if index_content is None:
        mode = "lightweight" if lightweight else "standard"
        index_content = (
            f"<!-- pipeline: test | type: custom | mode: {mode} | status: ACTIVE -->\n"
            f"<!-- phase: research | updated: 2026-03-15T00:00 -->\n"
            f"<!-- current_task: test | next: test -->\n"
        )
    with open(os.path.join(pipe_root, "00_index.md"), "w") as f:
        f.write(index_content)

    if plan:
        with open(os.path.join(pipe_root, "01_plan.md"), "w") as f:
            f.write("# Plan\n")

    if foundation:
        fnd = os.path.join(pipe_root, "foundation")
        os.makedirs(fnd, exist_ok=True)
        for axis in ("philosophy.md", "principles.md", "workflow.md"):
            with open(os.path.join(fnd, axis), "w") as f:
                f.write(f"# {axis}\n")

    if phase_dirs:
        for d_name, files in phase_dirs.items():
            d_path = os.path.join(pipe_root, d_name)
            os.makedirs(d_path, exist_ok=True)
            for fname, content in files.items():
                with open(os.path.join(d_path, fname), "w") as f:
                    f.write(content)

    return pipe_root


def run_hook(file_path, tool="Write"):
    """validate_pipeline.py 실행 → exit code 반환"""
    payload = json.dumps({
        "tool_name": tool,
        "tool_input": {"file_path": file_path}
    })
    result = subprocess.run(
        [sys.executable, HOOK],
        input=payload, capture_output=True, text=True, timeout=10
    )
    return result.returncode


# ─── Scenarios ─────────────────────────────────────────────────────

def build_scenarios():
    """모든 테스트 시나리오 생성"""
    scenarios = []

    # === SHOULD PASS (exit 0) ===

    # 1. Non-pipeline path
    scenarios.append({
        "name": "non_pipeline_path",
        "desc": "파이프라인 밖 경로 → pass",
        "file_path": "/c/dev/some_random_file.md",
        "expected": 0,
        "setup": lambda tmp: None,
        "rule": "none"
    })

    # 2. Non-write tool
    scenarios.append({
        "name": "non_write_tool",
        "desc": "Read 도구 → pass",
        "expected": 0,
        "tool": "Read",
        "rule": "none",
        "setup": lambda tmp: make_pipeline(tmp),
    })

    # 3. Valid complete pipeline — research phase
    def setup_valid_research(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {
                "00_index.md": "<!-- phase: research-r1 -->\n",
                "01_sources.md": "# Sources\n"
            }
        })
    scenarios.append({
        "name": "valid_research",
        "desc": "정상 research 파이프라인 → pass",
        "expected": 0,
        "setup": setup_valid_research,
        "target_file": "10_research-r1/01_sources.md",
        "rule": "all"
    })

    # 4. Writing 00_index.md itself (M1 self-create)
    def setup_m1_self(tmp):
        pipe = os.path.join(tmp, "01_projects", "01_orch", "01_test-pipe_0315")
        os.makedirs(pipe, exist_ok=True)
        return pipe
    scenarios.append({
        "name": "m1_self_create",
        "desc": "00_index.md 자체를 쓸 때 → pass (M1 예외)",
        "expected": 0,
        "setup": setup_m1_self,
        "target_file": "00_index.md",
        "rule": "M1"
    })

    # 5. Writing 00_index.md in phase folder (M3 self-create)
    def setup_m3_self(tmp):
        pipe = make_pipeline(tmp, phase_dirs={
            "10_research-r1": {}
        })
        return pipe
    scenarios.append({
        "name": "m3_self_create",
        "desc": "phase 00_index.md 자체를 쓸 때 → pass (M3 예외)",
        "expected": 0,
        "setup": setup_m3_self,
        "target_file": "10_research-r1/00_index.md",
        "rule": "M3"
    })

    # 6. Custom type review without impl-merged (R1 예외)
    def setup_r1_custom(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "40_review-r1": {
                "00_index.md": "<!-- phase: review-r1 -->\n",
                "02_context.md": "# Context\n## FROM\n## CONFIRMED DECISIONS\n## CARRY FORWARD\n## DO NOT CARRY\n## OPEN QUESTIONS\n## REQUIRED INPUT FILES\n## ENTRY CONDITION\n",
                "01_review.md": "# Review\n"
            }
        })
    scenarios.append({
        "name": "r1_custom_skip",
        "desc": "custom 타입 review — impl-merged 없어도 pass (R1 예외)",
        "expected": 0,
        "setup": setup_r1_custom,
        "target_file": "40_review-r1/01_review.md",
        "rule": "R1"
    })

    # 7. Lightweight pipeline impl without foundation (P1/F1 면제)
    def setup_lightweight(tmp):
        return make_pipeline(tmp, lightweight=True, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {
                "00_index.md": "<!-- phase: impl-r1 -->\n",
                "02_context.md": "# Context\n## FROM\n## CONFIRMED DECISIONS\n## CARRY FORWARD\n## DO NOT CARRY\n## OPEN QUESTIONS\n## REQUIRED INPUT FILES\n## ENTRY CONDITION\n",
                "01_code.md": "# Code\n"
            }
        })
    scenarios.append({
        "name": "lightweight_no_foundation",
        "desc": "경량 파이프라인 impl — foundation 없어도 pass",
        "expected": 0,
        "setup": setup_lightweight,
        "target_file": "30_impl-r1/01_code.md",
        "rule": "P1/F1"
    })

    # 8. Writing 02_context.md itself (N17 self-create)
    def setup_n17_self(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {
                "00_index.md": "idx\n",
            },
            "20_ideation-r1": {
                "00_index.md": "idx\n",
                "01_dialogue.md": "d\n",
            }
        })
    scenarios.append({
        "name": "n17_self_create",
        "desc": "02_context.md 자체를 쓸 때 → pass (N17 예외)",
        "expected": 0,
        "setup": setup_n17_self,
        "target_file": "20_ideation-r1/02_context.md",
        "rule": "N17"
    })

    # === EDGE CASES — 실제 겪은 오탐 ===

    # EC1. I1/N17 순환 의존: 01_dialogue.md 쓸 때 N17이 block
    # ideation-r1에서 01_dialogue.md 쓰려는데, 이전 phase 있고 02_context.md 없음
    # 01_dialogue.md는 I1 exempt이지만 N17 exempt 아님 → 오탐
    def setup_ec1(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {"00_index.md": "idx\n"},
            "20_ideation-r1": {"00_index.md": "idx\n"}
        })
    scenarios.append({
        "name": "ec1_dialogue_blocked_by_n17",
        "desc": "01_dialogue.md 작성 시 N17이 block → 오탐 (bootstrap 파일)",
        "expected": 0,  # SHOULD pass — bootstrap file
        "setup": setup_ec1,
        "target_file": "20_ideation-r1/01_dialogue.md",
        "rule": "N17/I1 circular"
    })

    # EC2. I1/N17 순환 의존: 02_context.md 쓸 때 I1이 block
    # ideation-r1에서 02_context.md 쓰려는데 01_dialogue.md 없음
    # 02_context.md는 N17 exempt이지만 I1 exempt 아님 → 오탐
    def setup_ec2(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {"00_index.md": "idx\n"},
            "20_ideation-r1": {"00_index.md": "idx\n"}
        })
    scenarios.append({
        "name": "ec2_context_blocked_by_i1",
        "desc": "02_context.md 작성 시 I1이 block → 오탐 (bootstrap 파일)",
        "expected": 0,  # SHOULD pass — bootstrap file
        "setup": setup_ec2,
        "target_file": "20_ideation-r1/02_context.md",
        "rule": "I1/N17 circular"
    })

    # EC3. impl-r1에서 02_context.md 쓸 때 — P3 exempt인데 P1이 먼저 block
    # foundation/ 없는 상태에서 02_context.md부터 쓰려 할 때
    # 02_context.md는 P3 exempt이지만 P1/F1이 먼저 발동
    def setup_ec3(tmp):
        return make_pipeline(tmp, foundation=False, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {"00_index.md": "idx\n"}
        })
    scenarios.append({
        "name": "ec3_impl_context_blocked_by_p1",
        "desc": "impl 02_context.md 쓸 때 P1(foundation)이 block → 오탐",
        "expected": 0,  # SHOULD pass — creating context before foundation is valid bootstrap
        "setup": setup_ec3,
        "target_file": "30_impl-r1/02_context.md",
        "rule": "P1 vs P3"
    })

    # EC4. research에 이전 phase 없는데도 N17 체크하는 경우 (정상 pass 확인)
    def setup_ec4(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {"00_index.md": "idx\n"}
        })
    scenarios.append({
        "name": "ec4_first_phase_no_n17",
        "desc": "첫 phase(research) — 이전 phase 없으므로 N17 미적용 → pass",
        "expected": 0,
        "setup": setup_ec4,
        "target_file": "10_research-r1/01_sources.md",
        "rule": "N17"
    })

    # EC5. research-merged T1 필수 파일 순서: 00_orchestrator-integration.md 쓸 때
    # 01_definitive-inventory.md가 아직 없음 → T1이 block하면 안 됨
    def setup_ec5(tmp):
        return make_pipeline(tmp, phase_dirs={
            "11_research-merged": {"00_index.md": "idx\n"}
        })
    scenarios.append({
        "name": "ec5_merged_required_file_self",
        "desc": "merged 필수 파일 자체를 쓸 때 → pass (T1 self-exempt)",
        "expected": 0,
        "setup": setup_ec5,
        "target_file": "11_research-merged/00_orchestrator-integration.md",
        "rule": "T1"
    })

    # EC6. impl-r1이 아닌 impl-r2에서 P2 체크 안 하는지 확인
    def setup_ec6(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "ctx\n",
                "01_code.md": "c\n"
            },
            "31_impl-r2": {
                "00_index.md": "idx\n",
            }
        })
    scenarios.append({
        "name": "ec6_impl_r2_no_p2_check",
        "desc": "impl-r2에서는 P2 재체크 안 함 → pass",
        "expected": 0,
        "setup": setup_ec6,
        "target_file": "31_impl-r2/01_code.md",
        "rule": "P2"
    })

    # EC7. impl-merged T1: 01_final-impl-guide.md 자체를 쓸 때
    def setup_ec7(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            "31_impl-merged": {"00_index.md": "idx\n"}
        })
    scenarios.append({
        "name": "ec7_impl_merged_self",
        "desc": "impl-merged 필수 파일 자체를 쓸 때 → pass",
        "expected": 0,
        "setup": setup_ec7,
        "target_file": "31_impl-merged/01_final-impl-guide.md",
        "rule": "T1"
    })

    # === DEEPER EDGE CASES (iter 3+) ===

    # EC8. review phase에서 02_context.md 작성 — R2(foundation) 이전
    def setup_ec8(tmp):
        pipe = make_pipeline(tmp, foundation=False, phase_dirs={
            "31_impl-merged": {
                "00_index.md": "idx\n",
                "01_final-impl-guide.md": "g\n",
            },
            "40_review-r1": {"00_index.md": "idx\n"}
        })
        with open(os.path.join(pipe, "00_index.md"), "w") as f:
            f.write("<!-- pipeline: test | type: full-impl | mode: standard | status: ACTIVE -->\n"
                    "<!-- phase: review | updated: 2026-03-15T00:00 -->\n"
                    "<!-- current_task: t | next: n -->\n")
        return pipe
    scenarios.append({
        "name": "ec8_review_context_blocked_by_r2",
        "desc": "review 02_context.md 쓸 때 R2(foundation) block → 오탐",
        "expected": 0,  # bootstrap file
        "setup": setup_ec8,
        "target_file": "40_review-r1/02_context.md",
        "rule": "R2"
    })

    # EC9. N17 — non-r1 라운드 (r2)는 N17 안 걸림 확인
    def setup_ec9(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {"00_index.md": "idx\n"},
            "20_ideation-r1": {
                "00_index.md": "idx\n",
                "01_dialogue.md": "d\n",
                "02_context.md": "c\n",
            },
            "21_ideation-r2": {"00_index.md": "idx\n"}
        })
    scenarios.append({
        "name": "ec9_r2_no_n17",
        "desc": "ideation-r2는 N17 안 걸림 (r1만 체크) → pass",
        "expected": 0,
        "setup": setup_ec9,
        "target_file": "21_ideation-r2/01_dialogue.md",
        "rule": "N17"
    })

    # EC10. P3 — impl-r1에서 00_index.md 작성 시 P3 exempt 확인
    def setup_ec10(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {}
        })
    scenarios.append({
        "name": "ec10_impl_r1_index_no_p3",
        "desc": "impl-r1 00_index.md 쓸 때 P3 exempt → pass",
        "expected": 0,
        "setup": setup_ec10,
        "target_file": "30_impl-r1/00_index.md",
        "rule": "P3"
    })

    # EC11. impl에서 일반 파일 쓸 때 foundation 없으면 여전히 block (정탐 확인)
    def setup_ec11(tmp):
        return make_pipeline(tmp, foundation=False, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "ctx\n",
            }
        })
    scenarios.append({
        "name": "ec11_impl_code_still_blocked_no_foundation",
        "desc": "impl 일반 파일은 foundation 없으면 여전히 block (정탐)",
        "expected": 2,
        "setup": setup_ec11,
        "target_file": "30_impl-r1/03_code.md",
        "rule": "P1"
    })

    # EC12. ideation에서 일반 파일 쓸 때 dialogue 없으면 여전히 block (정탐 확인)
    def setup_ec12(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {"00_index.md": "idx\n"},
            "20_ideation-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "c\n",
                # 01_dialogue.md 없음!
            }
        })
    scenarios.append({
        "name": "ec12_ideation_general_still_blocked",
        "desc": "ideation 일반 파일은 dialogue 없으면 여전히 block (정탐)",
        "expected": 2,
        "setup": setup_ec12,
        "target_file": "20_ideation-r1/03_something.md",
        "rule": "I1"
    })

    # === STRESS TEST (iter 5) ===

    # EC13. 완전히 새로운 파이프라인: 모든 phase를 r1부터 bootstrap 가능해야 함
    # research-r1에서 첫 파일을 00_index.md로 쓸 때 → 01_plan.md 없으면 M2
    # 하지만 파이프라인 루트의 00_index.md와 01_plan.md가 있으면 pass
    def setup_ec13(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {}
        })
    scenarios.append({
        "name": "ec13_fresh_research_index",
        "desc": "새 research-r1에 00_index.md 작성 → pass",
        "expected": 0,
        "setup": setup_ec13,
        "target_file": "10_research-r1/00_index.md",
        "rule": "M2/M3"
    })

    # EC14. review-merged T1: review 필수 파일 (cross-validation) 쓸 때 자체 exempt
    def setup_ec14(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            "41_review-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-integration.md": "oi\n",
            }
        })
    scenarios.append({
        "name": "ec14_review_merged_cross_val_self",
        "desc": "review-merged 01_cross-validation.md 자체 작성 → pass",
        "expected": 0,
        "setup": setup_ec14,
        "target_file": "41_review-merged/01_cross-validation.md",
        "rule": "T1"
    })

    # EC15. impl-merged에서 필수 외 파일 쓸 때 — 필수 파일 누락 시 block (정탐)
    def setup_ec15(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            "31_impl-merged": {
                "00_index.md": "idx\n",
                # 01_final-impl-guide.md 없음!
            }
        })
    scenarios.append({
        "name": "ec15_impl_merged_extra_without_required",
        "desc": "impl-merged 필수 파일 없이 추가 파일 → T1 block (정탐)",
        "expected": 2,
        "setup": setup_ec15,
        "target_file": "31_impl-merged/02_notes.md",
        "rule": "T1"
    })

    # EC16. Edit 도구 — Write와 동일 규칙 적용
    def setup_ec16(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {
                # 00_index.md 없음!
                "01_sources.md": "# Sources\n"
            }
        })
    scenarios.append({
        "name": "ec16_edit_tool_same_rules",
        "desc": "Edit 도구도 Write와 동일 규칙 → M3 block",
        "expected": 2,
        "setup": setup_ec16,
        "target_file": "10_research-r1/01_sources.md",
        "tool": "Edit",
        "rule": "M3"
    })

    # EC17. meta 대역 (00-09) — 규칙 체크 안 함
    def setup_ec17(tmp):
        return make_pipeline(tmp)
    scenarios.append({
        "name": "ec17_meta_band_no_check",
        "desc": "meta 대역(00-09) 파일 → phase 규칙 미적용 pass",
        "expected": 0,
        "setup": setup_ec17,
        "target_file": "00_index.md",
        "rule": "none"
    })

    # === SHOULD BLOCK (exit 2) ===

    # 9. Missing 00_index.md in pipeline root (M1)
    def setup_m1_fail(tmp):
        pipe = os.path.join(tmp, "01_projects", "01_orch", "01_test-pipe_0315")
        phase = os.path.join(pipe, "10_research-r1")
        os.makedirs(phase, exist_ok=True)
        # 01_plan.md 있지만 00_index.md 없음
        with open(os.path.join(pipe, "01_plan.md"), "w") as f:
            f.write("# Plan\n")
        with open(os.path.join(phase, "00_index.md"), "w") as f:
            f.write("idx\n")
        return pipe
    scenarios.append({
        "name": "m1_missing_index",
        "desc": "파이프라인 루트 00_index.md 없음 → M1 block",
        "expected": 2,
        "setup": setup_m1_fail,
        "target_file": "10_research-r1/01_sources.md",
        "rule": "M1"
    })

    # 10. Missing 01_plan.md (M2)
    def setup_m2_fail(tmp):
        pipe = os.path.join(tmp, "01_projects", "01_orch", "01_test-pipe_0315")
        os.makedirs(pipe, exist_ok=True)
        with open(os.path.join(pipe, "00_index.md"), "w") as f:
            f.write("<!-- pipeline: test | type: custom | mode: standard | status: ACTIVE -->\n<!-- phase: r | updated: 2026-01-01T00:00 -->\n<!-- current_task: t | next: n -->\n")
        phase = os.path.join(pipe, "10_research-r1")
        os.makedirs(phase, exist_ok=True)
        with open(os.path.join(phase, "00_index.md"), "w") as f:
            f.write("idx\n")
        return pipe
    scenarios.append({
        "name": "m2_missing_plan",
        "desc": "01_plan.md 없이 phase 폴더 → M2 block",
        "expected": 2,
        "setup": setup_m2_fail,
        "target_file": "10_research-r1/01_sources.md",
        "rule": "M2"
    })

    # 11. Missing 00_index.md in phase folder (M3)
    def setup_m3_fail(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {
                # 00_index.md 없음!
                "01_sources.md": "# Sources\n"
            }
        })
    scenarios.append({
        "name": "m3_missing_phase_index",
        "desc": "phase 폴더에 00_index.md 없음 → M3 block",
        "expected": 2,
        "setup": setup_m3_fail,
        "target_file": "10_research-r1/01_sources.md",
        "rule": "M3"
    })

    # 12. Missing 02_context.md on phase transition (N17)
    def setup_n17_fail(tmp):
        return make_pipeline(tmp, phase_dirs={
            "10_research-r1": {
                "00_index.md": "idx\n",
            },
            "20_ideation-r1": {
                "00_index.md": "idx\n",
                "01_dialogue.md": "d\n",
                # 02_context.md 없음!
            }
        })
    scenarios.append({
        "name": "n17_missing_context",
        "desc": "phase 전환 시 02_context.md 없음 → N17 block",
        "expected": 2,
        "setup": setup_n17_fail,
        "target_file": "20_ideation-r1/03_something.md",
        "rule": "N17"
    })

    # 13. Missing 01_dialogue.md in ideation (I1)
    def setup_i1_fail(tmp):
        return make_pipeline(tmp, phase_dirs={
            "20_ideation-r1": {
                "00_index.md": "idx\n",
                # 01_dialogue.md 없음!
            }
        })
    scenarios.append({
        "name": "i1_missing_dialogue",
        "desc": "ideation에 01_dialogue.md 없음 → I1 block",
        "expected": 2,
        "setup": setup_i1_fail,
        "target_file": "20_ideation-r1/02_something.md",
        "rule": "I1"
    })

    # 14. Missing foundation in impl (P1)
    def setup_p1_fail(tmp):
        return make_pipeline(tmp, foundation=False, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "ctx\n",
            }
        })
    scenarios.append({
        "name": "p1_missing_foundation",
        "desc": "impl에 foundation/ 없음 → P1 block",
        "expected": 2,
        "setup": setup_p1_fail,
        "target_file": "30_impl-r1/01_code.md",
        "rule": "P1"
    })

    # 15. Missing ideation-merged for impl (P2)
    def setup_p2_fail(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            # ideation-merged 없음!
            "30_impl-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "ctx\n",
            }
        })
    scenarios.append({
        "name": "p2_missing_ideation_merged",
        "desc": "impl에 ideation-merged 없음 → P2 block",
        "expected": 2,
        "setup": setup_p2_fail,
        "target_file": "30_impl-r1/01_code.md",
        "rule": "P2"
    })

    # 16. Missing foundation axis file (F1)
    def setup_f1_fail(tmp):
        pipe = make_pipeline(tmp, foundation=False, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "ctx\n",
            }
        })
        # foundation/ 있지만 파일 1개 누락
        fnd = os.path.join(pipe, "foundation")
        os.makedirs(fnd, exist_ok=True)
        for axis in ("philosophy.md", "principles.md"):
            with open(os.path.join(fnd, axis), "w") as f:
                f.write("x\n")
        # workflow.md 없음!
        return pipe
    scenarios.append({
        "name": "f1_missing_axis",
        "desc": "foundation/ workflow.md 누락 → F1 block",
        "expected": 2,
        "setup": setup_f1_fail,
        "target_file": "30_impl-r1/01_code.md",
        "rule": "F1"
    })

    # 17. Missing required files in ideation-merged (T1)
    def setup_t1_fail(tmp):
        return make_pipeline(tmp, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                # 00_orchestrator-final.md 없음!
                "01_confirmed-decisions.md": "d\n",
            }
        })
    scenarios.append({
        "name": "t1_missing_merged_file",
        "desc": "ideation-merged 필수 파일 누락 → T1 block",
        "expected": 2,
        "setup": setup_t1_fail,
        "target_file": "21_ideation-merged/02_extra.md",
        "rule": "T1"
    })

    # 18. Missing foundation in review (R2)
    def setup_r2_fail(tmp):
        return make_pipeline(tmp, foundation=False, phase_dirs={
            "31_impl-merged": {
                "00_index.md": "idx\n",
                "01_final-impl-guide.md": "g\n",
            },
            "40_review-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "ctx\n",
                "01_review.md": "r\n",
            }
        })
    # index를 non-custom 타입으로 변경
    scenarios.append({
        "name": "r2_missing_foundation_review",
        "desc": "review에 foundation/ 없음 → R2 block",
        "expected": 2,
        "setup": setup_r2_fail,
        "target_file": "40_review-r1/01_review.md",
        "rule": "R2",
        "index_type": "full-impl"
    })

    # 19. Missing 02_context.md in impl-r1 (P3)
    def setup_p3_fail(tmp):
        return make_pipeline(tmp, foundation=True, phase_dirs={
            "21_ideation-merged": {
                "00_index.md": "idx\n",
                "00_orchestrator-final.md": "f\n",
                "01_confirmed-decisions.md": "d\n"
            },
            "30_impl-r1": {
                "00_index.md": "idx\n",
                # 02_context.md 없음!
            }
        })
    scenarios.append({
        "name": "p3_missing_impl_context",
        "desc": "impl-r1에 02_context.md 없음 → P3 block",
        "expected": 2,
        "setup": setup_p3_fail,
        "target_file": "30_impl-r1/01_code.md",
        "rule": "P3"
    })

    # 20. Non-custom review without impl-merged (R1)
    def setup_r1_fail(tmp):
        pipe = make_pipeline(tmp, foundation=True, phase_dirs={
            "40_review-r1": {
                "00_index.md": "idx\n",
                "02_context.md": "ctx\n",
                "01_review.md": "r\n",
            }
        })
        # full-impl 타입으로 00_index.md 재작성
        with open(os.path.join(pipe, "00_index.md"), "w") as f:
            f.write("<!-- pipeline: test | type: full-impl | mode: standard | status: ACTIVE -->\n"
                    "<!-- phase: review | updated: 2026-03-15T00:00 -->\n"
                    "<!-- current_task: t | next: n -->\n")
        return pipe
    scenarios.append({
        "name": "r1_missing_impl_merged",
        "desc": "full-impl review에 impl-merged 없음 → R1 block",
        "expected": 2,
        "setup": setup_r1_fail,
        "target_file": "40_review-r1/01_review.md",
        "rule": "R1"
    })

    return scenarios


# ─── Runner ────────────────────────────────────────────────────────

def run_scenarios(scenarios, verbose=False):
    results = []
    for s in scenarios:
        tmp = tempfile.mkdtemp(prefix="autoit_")
        try:
            pipe_root = s["setup"](tmp)

            # index_type 오버라이드
            if s.get("index_type") and pipe_root:
                idx = os.path.join(pipe_root, "00_index.md")
                with open(idx, "w") as f:
                    f.write(f"<!-- pipeline: test | type: {s['index_type']} | mode: standard | status: ACTIVE -->\n"
                            f"<!-- phase: test | updated: 2026-03-15T00:00 -->\n"
                            f"<!-- current_task: t | next: n -->\n")

            if pipe_root and s.get("target_file"):
                file_path = os.path.join(pipe_root, s["target_file"])
                # 대상 파일이 없으면 생성 (hook이 경로만 봄)
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
            elif s.get("file_path"):
                file_path = s["file_path"]
            else:
                file_path = "/c/dev/dummy.md"

            tool = s.get("tool", "Write")
            actual = run_hook(file_path, tool)
            correct = actual == s["expected"]

            results.append({
                "name": s["name"],
                "desc": s["desc"],
                "rule": s["rule"],
                "expected": s["expected"],
                "actual": actual,
                "correct": correct,
            })

            if verbose:
                mark = "✅" if correct else "❌"
                print(f"  {mark} {s['name']}: expected={s['expected']} actual={actual} ({s['desc']})")
        except Exception as e:
            results.append({
                "name": s["name"],
                "desc": s["desc"],
                "rule": s["rule"],
                "expected": s["expected"],
                "actual": -1,
                "correct": False,
                "error": str(e)
            })
            if verbose:
                print(f"  💥 {s['name']}: ERROR {e}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    return results


def compute_metrics(results):
    """precision/recall/F1 계산"""
    # "block" = positive (위반 감지), "pass" = negative (정상 통과)
    tp = sum(1 for r in results if r["expected"] == 2 and r["actual"] == 2)
    fp = sum(1 for r in results if r["expected"] == 0 and r["actual"] == 2)
    fn = sum(1 for r in results if r["expected"] == 2 and r["actual"] == 0)
    tn = sum(1 for r in results if r["expected"] == 0 and r["actual"] == 0)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (tp + tn) / len(results) if results else 0

    return {
        "tp": tp, "fp": fp, "fn": fn, "tn": tn,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "accuracy": round(accuracy, 4),
        "total": len(results),
        "correct": tp + tn,
        "incorrect": fp + fn,
    }


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    json_out = "--json" in sys.argv

    scenarios = build_scenarios()
    if verbose:
        print(f"\n=== validate_pipeline.py 테스트 ({len(scenarios)}개 시나리오) ===\n")

    results = run_scenarios(scenarios, verbose=verbose)
    metrics = compute_metrics(results)

    if json_out:
        output = {"metrics": metrics, "results": results}
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n=== 결과 ===")
        print(f"Total: {metrics['total']} | Correct: {metrics['correct']} | Incorrect: {metrics['incorrect']}")
        print(f"TP={metrics['tp']} FP={metrics['fp']} FN={metrics['fn']} TN={metrics['tn']}")
        print(f"Precision: {metrics['precision']} | Recall: {metrics['recall']} | F1: {metrics['f1']}")
        print(f"Accuracy: {metrics['accuracy']}")

        # 실패 목록
        failures = [r for r in results if not r["correct"]]
        if failures:
            print(f"\n=== 실패 ({len(failures)}개) ===")
            for f in failures:
                print(f"  ❌ {f['name']}: expected={f['expected']} actual={f['actual']} — {f['desc']}")


if __name__ == "__main__":
    main()
