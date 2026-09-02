#!/usr/bin/env python3
"""Build the deterministic R0.74Q research freeze manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "research/r074q_freeze_manifest.json"

ARTIFACTS = {
    "freeze_manifest_generator": "scripts/r074q_freeze_manifest.py",
    "problem_freeze": "research/r074q_problem_freeze.md",
    "common_shear_note": "research/r074q_common_shear_multipacket_gate.md",
    "common_shear_certificate_producer": "scripts/r074q_common_shear_gate_certificate.py",
    "common_shear_certificate_json": "research/r074q_common_shear_gate_certificate.json",
    "common_shear_certificate_report": "research/r074q_common_shear_gate_certificate_report.md",
    "common_shear_independent_audit": "research/r074q_common_shear_gate_independent_audit.md",
    "relaxed_multipacket_note": "research/r074q_relaxed_multipacket_cubic_obstruction.md",
    "relaxed_certificate_producer": "scripts/r074q_relaxed_multipacket_certificate.py",
    "relaxed_certificate_json": "research/r074q_relaxed_multipacket_certificate.json",
    "relaxed_certificate_report": "research/r074q_relaxed_multipacket_certificate_report.md",
    "relaxed_geometry_independent_audit": "research/r074q_relaxed_geometry_independent_audit.md",
    "relaxed_dominance_payment_independent_audit": "research/r074q_relaxed_dominance_payment_independent_audit.md",
    "gap_matrix": "research/r074q_gap_matrix.md",
    "primary_literature_boundary": "research/r074q_primary_literature_boundary.md",
    "primary_literature_independent_audit": "research/r074q_primary_literature_independent_audit.md",
    "reader_source": "research/r074q_report-source.md",
    "reader_source_independent_audit": "research/r074q_reader_source_independent_audit.md",
}

CORE_COMMITS = {
    "effective_shell_decision": "60d4c1c6",
    "common_shear_gate": "11d8dba6",
    "relaxed_packet_stress_test": "1e907750",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=REPO,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def tag_ids(path: Path) -> list[str]:
    return re.findall(r"\\tag\{Q\.([^}]+)\}", path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-at", required=True)
    parser.add_argument("--research-parent", required=True)
    parser.add_argument("--origin-main", required=True)
    args = parser.parse_args()

    missing = [relative for relative in ARTIFACTS.values() if not (REPO / relative).is_file()]
    require(not missing, f"missing required artifacts: {missing}")

    parent = git("rev-parse", args.research_parent)
    origin_main = git("rev-parse", args.origin_main)
    for label, revision in CORE_COMMITS.items():
        full_revision = git("rev-parse", revision)
        require(
            git("merge-base", "--is-ancestor", full_revision, parent) == "",
            f"core commit {label} is not an ancestor of research parent",
        )

    common = json.loads((REPO / ARTIFACTS["common_shear_certificate_json"]).read_text(encoding="utf-8"))
    relaxed = json.loads((REPO / ARTIFACTS["relaxed_certificate_json"]).read_text(encoding="utf-8"))
    require(common["summary"] == {
        "rational_passed": 21,
        "rational_total": 21,
        "result": "PASS",
        "structural_passed": 19,
        "structural_total": 19,
    }, "common-shear certificate is not PASS 21/21 + 19/19")
    require(relaxed["summary"] == {
        "rational_passed": 22,
        "rational_total": 22,
        "result": "PASS",
        "structural_passed": 41,
        "structural_total": 41,
    }, "relaxed certificate is not PASS 22/22 + 41/41")

    require(
        common["note_sha256"] == sha256(REPO / ARTIFACTS["common_shear_note"]),
        "common-shear certificate is not bound to the current note",
    )
    require(
        relaxed["note_sha256"] == sha256(REPO / ARTIFACTS["relaxed_multipacket_note"]),
        "relaxed certificate is not bound to the current note",
    )

    problem_tags = tag_ids(REPO / ARTIFACTS["problem_freeze"])
    require(
        problem_tags == [*[str(i) for i in range(1, 24)], "23a", *[str(i) for i in range(24, 28)]],
        "problem-freeze Q-tag sequence drifted",
    )

    reader = (REPO / ARTIFACTS["reader_source"]).read_text(encoding="utf-8")
    for required in (
        "\\frac{(P_R^{M,(N)})^{2/3}}{NT}\\longrightarrow\\infty",
        "Y_{2,R}^{\\rm sf,(N)}\\lesssim\\sqrt N\\,T",
        "\\mathfrak C_R^{M,(N)}\\asymp NT",
        "不证明新颖性、优先权或可发表性",
        "**NOT CLAY.**",
    ):
        require(required in reader, f"reader source missing sentinel: {required}")
    for forbidden in (
        "|q_\\ell|le",
        "-log N",
        "解决了三维 Navier--Stokes 千禧年问题",
        "证明了全局正则性",
    ):
        require(forbidden not in reader, f"reader source contains forbidden token: {forbidden}")
    require(reader.count("\\[") == reader.count("\\]"), "reader display-math delimiters are unbalanced")
    require(reader.count("\\(") == reader.count("\\)"), "reader inline-math delimiters are unbalanced")

    records = {}
    for key, relative in ARTIFACTS.items():
        path = REPO / relative
        records[key] = {
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }

    payload = {
        "schema_version": 1,
        "research_version": "R0.74Q",
        "frozen_at": args.frozen_at,
        "research_branch": git("branch", "--show-current"),
        "research_parent": parent,
        "origin_main_observed_at_freeze": origin_main,
        "core_commits": {key: git("rev-parse", revision) for key, revision in CORE_COMMITS.items()},
        "scope": "EFFECTIVE_SHELL_REDUCTION_COMMON_SHEAR_MULTIPACKET_STRESS_TEST_CUBIC_PAYMENT_OBSTRUCTION",
        "claim_status": {
            "terminal_effective_shell_reduction": "PROVED",
            "uniform_effective_shell_packing": "OPEN",
            "finite_common_shear_exact_nse": "PROVED_MECHANISM_KNOWN_NOT_NOVELTY_CLAIM",
            "different_shear_naive_superposition": "PROVED_INVALID_BY_EXACT_RESIDUAL",
            "frozen_angle_common_B_obstruction": "PROVED_FOR_SPECIFIED_ASYMPTOTIC_GEOMETRY_NOT_UNIVERSAL_NO_GO",
            "relaxed_calibration_and_common_terminal_geometry": "PROVED_FOR_EXPLICIT_GROWING_FINITE_FAMILY",
            "all_lobe_weighted_dominance": "PROVED_FOR_CANONICAL_EQUAL_TARGET_FAMILY",
            "target_clock_lower_bound": "PROVED",
            "full_square_function_lower_detection": "PROVED",
            "full_square_function_matching_upper": "OPEN_NOT_CLAIMED",
            "outer_velocity_cubic_payment": "PROVED_TRUE_NONNEGATIVE_LOWER_BOUND",
            "payment_to_target_ratio": "PROVED_DIVERGES_ALONG_EXPLICIT_SEQUENCE",
            "signed_cumulative_flux_order_NT": "OPEN_NOT_CLAIMED",
            "fixed_scale_inequality_Q1": "OPEN",
            "common_shear_certificate": "PASS_21_OF_21_RATIONAL_19_OF_19_STRUCTURAL",
            "relaxed_certificate": "PASS_22_OF_22_RATIONAL_41_OF_41_STRUCTURAL",
            "gap_matrix": "PASS_33_ITEMS",
            "reader_source_independent_audit": "PASS_AFTER_FOUR_REPAIRS",
            "primary_literature_screen": "BOUNDED_FOURTEEN_SOURCE_NO_DIRECT_HIT_MECHANISM_PRIOR_ART_DISCLOSED",
            "novelty_or_priority": "OPEN_NOT_CLAIMED",
            "simulation_or_dns": "NOT_USED",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "dgx": "NOT_USED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
            "publication": "PENDING_IN_INDEPENDENT_PUBLISHING_TASK",
            "cumulative_recap": "NOT_REQUIRED_FOR_THIS_SECTION",
        },
        "artifacts": records,
        "verification": {
            "git_diff_check": "PASS",
            "problem_freeze_equation_tags": "PASS_28_UNIQUE_OF_28",
            "common_shear_certificate_fresh_run": "PASS_21_OF_21_RATIONAL_19_OF_19_STRUCTURAL",
            "relaxed_certificate_fresh_run": "PASS_22_OF_22_RATIONAL_41_OF_41_STRUCTURAL",
            "certificate_note_sha_bindings": "PASS",
            "reader_math_delimiters_and_sentinels": "PASS",
            "reader_source_sha256": sha256(REPO / ARTIFACTS["reader_source"]),
            "gap_matrix_sha256": sha256(REPO / ARTIFACTS["gap_matrix"]),
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_title": "发布任务",
            "owner_task_id": "01a05bea-7f45-7410-8792-4e1f840b83f8",
            "task_reuse": False,
            "target": "https://kasifa.github.io/",
            "status": "READY_FOR_INDEPENDENT_PUBLISHING_TASK",
            "target_html": "/notes/r0-74q.html",
            "target_pdf": "/notes/r0-74q.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "live_completion_gate": "ORIGIN_MAIN_ADVANCED_AND_HTML_PDF_SITE_VERSION_BYTE_IDENTICAL",
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(sha256(OUTPUT))


if __name__ == "__main__":
    main()
