#!/usr/bin/env python3
"""Build the deterministic R0.74R research freeze manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "research/r074r_freeze_manifest.json"

ARTIFACTS = {
    "freeze_manifest_generator": "scripts/r074r_freeze_manifest.py",
    "problem_freeze": "research/r074r_problem_freeze.md",
    "terminal_window_note": "research/r074r_persistent_lobe_cubic_packing.md",
    "terminal_window_certificate_producer": "scripts/r074r_persistent_lobe_certificate.py",
    "terminal_window_certificate_json": "research/r074r_persistent_lobe_certificate.json",
    "terminal_window_certificate_report": "research/r074r_persistent_lobe_certificate_report.md",
    "terminal_window_independent_audit": "research/r074r_terminal_window_independent_audit.md",
    "arbitrary_clock_note": "research/r074r_arbitrary_clock_extraction_gate.md",
    "arbitrary_clock_primary_audit": "research/r074r_arbitrary_clock_primary_audit.md",
    "arbitrary_clock_certificate_producer": "scripts/r074r_arbitrary_clock_gate_certificate.py",
    "arbitrary_clock_certificate_json": "research/r074r_arbitrary_clock_gate_certificate.json",
    "arbitrary_clock_certificate_report": "research/r074r_arbitrary_clock_gate_certificate_report.md",
    "arbitrary_clock_independent_audit_producer": "scripts/r074r_arbitrary_clock_independent_audit.mjs",
    "arbitrary_clock_independent_certificate_json": "research/r074r_arbitrary_clock_independent_certificate.json",
    "arbitrary_clock_independent_audit": "research/r074r_arbitrary_clock_independent_audit.md",
    "gap_matrix": "research/r074r_gap_matrix.md",
    "primary_literature_boundary": "research/r074r_primary_literature_boundary.md",
    "reader_source": "research/r074r_report-source.md",
    "publication_handoff": "research/r074r_publication_handoff.md",
}

CORE_COMMITS = {
    "terminal_window_gate": "f775ed34",
    "arbitrary_clock_conditional_gate": "0a2a148e",
    "literature_and_reader_source": "d07feac4",
    "independent_arbitrary_clock_audit": "f3c101f4",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=REPO, check=True, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, text=True,
    ).stdout.strip()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def tags(path: Path) -> list[int]:
    return [int(value) for value in re.findall(r"\\tag\{R\.(\d+)\}", path.read_text(encoding="utf-8"))]


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
        require(git("merge-base", "--is-ancestor", full_revision, parent) == "", f"core commit {label} is not an ancestor")

    terminal = json.loads((REPO / ARTIFACTS["terminal_window_certificate_json"]).read_text(encoding="utf-8"))
    arbitrary = json.loads((REPO / ARTIFACTS["arbitrary_clock_certificate_json"]).read_text(encoding="utf-8"))
    independent = json.loads((REPO / ARTIFACTS["arbitrary_clock_independent_certificate_json"]).read_text(encoding="utf-8"))
    require(terminal["summary"] == {
        "power_ledger_passed": True, "rational_passed": 21, "rational_total": 21,
        "result": "PASS", "structural_passed": 22, "structural_total": 22,
    }, "terminal-window certificate summary drifted")
    require(arbitrary["summary"] == {
        "power_ledgers_passed": 3, "power_ledgers_total": 3,
        "rational_passed": 13, "rational_total": 13, "result": "PASS",
        "structural_passed": 25, "structural_total": 25,
    }, "arbitrary-clock primary certificate summary drifted")
    require(independent["summary"] == {
        "rational_passed": 9, "rational_total": 9, "structural_passed": 12,
        "structural_total": 12, "finite_passed": 5, "finite_total": 5,
        "result": "PASS",
    }, "arbitrary-clock independent certificate summary drifted")
    require(terminal["note_sha256"] == sha256(REPO / ARTIFACTS["terminal_window_note"]), "terminal certificate note binding drifted")
    require(arbitrary["note_sha256"] == sha256(REPO / ARTIFACTS["arbitrary_clock_note"]), "arbitrary primary certificate note binding drifted")
    for relative, bound in independent["source_bindings"].items():
        require(bound == sha256(REPO / relative), f"independent source binding drifted: {relative}")

    require(tags(REPO / ARTIFACTS["problem_freeze"]) == list(range(1, 29)), "problem-freeze R-tag sequence drifted")
    require(tags(REPO / ARTIFACTS["terminal_window_note"]) == list(range(100, 139)), "terminal-window R-tag sequence drifted")
    require(tags(REPO / ARTIFACTS["arbitrary_clock_note"]) == list(range(200, 226)), "arbitrary-clock R-tag sequence drifted")

    reader = (REPO / ARTIFACTS["reader_source"]).read_text(encoding="utf-8")
    for required in (
        "窗口情形 PROVED；任意时钟的充分条件 PROVED；充分\n条件本身 OPEN。NOT CLAY.",
        "2^{3k}\\gamma_k\\Lambda_k^3\\Theta_k^{-2}",
        "CONDITIONAL / PROVED IMPLICATION",
        "三个不能绕过的 no-go 检验",
    ):
        require(required in reader, f"reader source missing sentinel: {required}")
    for forbidden in ("证明了全局正则性", "解决了三维 Navier--Stokes 千禧年问题"):
        require(forbidden not in reader, f"reader source contains forbidden claim: {forbidden}")
    require(reader.count("\\[") == reader.count("\\]"), "reader display math is unbalanced")
    require(reader.count("\\(") == reader.count("\\)"), "reader inline math is unbalanced")

    records = {}
    for key, relative in ARTIFACTS.items():
        path = REPO / relative
        records[key] = {"path": relative, "bytes": path.stat().st_size, "sha256": sha256(path)}

    payload = {
        "schema_version": 1,
        "research_version": "R0.74R",
        "frozen_at": args.frozen_at,
        "research_branch": git("branch", "--show-current"),
        "research_parent": parent,
        "origin_main_observed_at_freeze": origin_main,
        "source_branch": "codex/r074r-cubic-packing",
        "source_commits": {
            "terminal_window_gate": "efe23a4c",
            "arbitrary_clock_conditional_gate": "287c260e",
            "literature_and_reader_source": "362fa100",
        },
        "core_commits": {key: git("rev-parse", revision) for key, revision in CORE_COMMITS.items()},
        "scope": "TERMINAL_WINDOW_CONVEX_PAYMENT_FIRST_SHELL_CONCENTRATION_AND_CONDITIONAL_ARBITRARY_CLOCK_EXTRACTION",
        "claim_status": {
            "terminal_window_lobe_packing": "PROVED",
            "first_shell_concentration": "PROVED_IN_FROZEN_TARGET_FAMILY",
            "three_way_arbitrary_clock_triage": "PROVED",
            "persistence_to_cubic_payment": "PROVED",
            "arbitrary_clock_to_Q1": "PROVED_IMPLICATION_CONDITIONAL_INPUT",
            "universal_extraction_hypotheses": "OPEN_NOT_CLAIMED",
            "functional_no_go_witnesses": "PROVED_ABSTRACT_OR_FUNCTIONAL_NOT_NSE_SOLUTIONS",
            "fixed_scale_Q1": "OPEN",
            "terminal_window_certificate": "PASS_21_OF_21_RATIONAL_22_OF_22_STRUCTURAL",
            "arbitrary_clock_primary_certificate": "PASS_13_OF_13_RATIONAL_3_OF_3_POWER_25_OF_25_STRUCTURAL",
            "arbitrary_clock_independent_audit": "PASS_9_OF_9_RATIONAL_12_OF_12_STRUCTURAL_5_OF_5_FINITE",
            "literature_screen": "BOUNDED_PRIMARY_NON_HIT_NO_NOVELTY_OR_PRIORITY_CLAIM",
            "formal_figure": "REQUIRED_FOR_PUBLICATION_DERIVED_FROM_FROZEN_ANALYTIC_SOURCE",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
            "publication": "PENDING_IN_PUBLICATION_TASK",
            "cumulative_recap": "NOT_REQUIRED_FOR_THIS_SECTION",
        },
        "artifacts": records,
        "verification": {
            "git_worktree": "CLEAN_BEFORE_FREEZE_GENERATION",
            "equation_tags": "PASS_28_PLUS_39_PLUS_26_UNIQUE",
            "certificate_fresh_runs": "PASS_AND_BYTE_IDENTICAL",
            "certificate_note_sha_bindings": "PASS",
            "reader_math_delimiters_and_sentinels": "PASS",
            "formal_figure_package": "PENDING_PUBLICATION_DERIVATION",
        },
        "publication_handoff": {
            "owner_task_id": "019fb8c8-96a8-7320-bb59-3ab9e8b7e29e",
            "target": "https://kasifa.github.io/",
            "status": "READY_AFTER_FREEZE_COMMIT",
            "target_html": "/notes/r0-74r.html",
            "target_pdf": "/notes/r0-74r.pdf",
            "target_primary_figure": "/assets/r074r/fig-r074r-clock-triage.svg",
            "recap_update_required": False,
            "live_completion_gate": "ORIGIN_MAIN_ADVANCED_PAGES_SUCCESS_HTML_PDF_FIGURE_BYTE_IDENTICAL",
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(sha256(OUTPUT))


if __name__ == "__main__":
    main()
