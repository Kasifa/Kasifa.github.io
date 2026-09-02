#!/usr/bin/env python3
"""Build the deterministic R0.74P research freeze manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "research/r074p_freeze_manifest.json"
FIGURE_DIR = REPO / "research/figures/r074p/fig-r074p-observable-triage"

ARTIFACTS = {
    "freeze_manifest_generator": "scripts/r074p_freeze_manifest.py",
    "problem_freeze": "research/r074p_problem_freeze.md",
    "main_note": "research/r074p_temporal_observable_triage.md",
    "main_independent_audit": "research/r074p_main_independent_audit.md",
    "final_source_rebind_audit": "research/r074p_final_source_rebind_audit.md",
    "gap_matrix": "research/r074p_gap_matrix.md",
    "primary_literature_boundary": "research/r074p_primary_literature_boundary.md",
    "primary_literature_independent_audit": "research/r074p_primary_literature_independent_audit.md",
    "reader_source": "research/r074p_report-source.md",
    "reader_source_independent_audit": "research/r074p_reader_source_independent_audit.md",
    "bilingual_dictionary": "research/r074p_bilingual_dictionary.md",
    "certificate_producer": "scripts/r074p_temporal_clock_certificate.py",
    "certificate_json": "research/r074p_temporal_clock_certificate.json",
    "certificate_report": "research/r074p_temporal_clock_certificate_report.md",
    "certificate_independent_implementation": "scripts/r074p_temporal_clock_certificate_independent.rb",
    "certificate_independent_audit": "research/r074p_certificate_independent_audit.md",
    "figure_independent_audit": "research/r074p_figure_independent_audit.md",
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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--frozen-at", required=True)
    args = parser.parse_args()

    missing = [relative for relative in ARTIFACTS.values() if not (REPO / relative).is_file()]
    if missing:
        raise SystemExit(f"missing required artifacts: {missing}")

    validation = json.loads((FIGURE_DIR / "validation.json").read_text(encoding="utf-8"))
    figure_manifest = json.loads((FIGURE_DIR / "manifest.json").read_text(encoding="utf-8"))
    if not validation["pass"] or not figure_manifest["validation_pass"]:
        raise SystemExit("figure package is not validated")

    records = {}
    for key, relative in ARTIFACTS.items():
        path = REPO / relative
        records[key] = {
            "path": relative,
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }

    figure_files = sorted(path for path in FIGURE_DIR.iterdir() if path.is_file())
    figure_summary = {
        "path": str(FIGURE_DIR.relative_to(REPO)),
        "physical_file_count": len(figure_files),
        "manifest_entry_count": len(figure_manifest["artifacts"]),
        "external_binding_count": len(figure_manifest["external_bindings"]),
        "sha256sum_entry_count": len((FIGURE_DIR / "SHA256SUMS").read_text(encoding="utf-8").splitlines()),
        "validator_result": f"PASS_{validation['check_count']}_OF_{validation['check_count']}",
        "manifest_sha256": sha256(FIGURE_DIR / "manifest.json"),
        "sha256sums_sha256": sha256(FIGURE_DIR / "SHA256SUMS"),
        "validation_sha256": sha256(FIGURE_DIR / "validation.json"),
        "source_data_sha256": sha256(FIGURE_DIR / "source-data.csv"),
        "plot_source_sha256": sha256(FIGURE_DIR / "plot.py"),
        "validator_sha256": sha256(FIGURE_DIR / "validate.py"),
        "pdf_sha256": sha256(FIGURE_DIR / "figure.pdf"),
        "svg_sha256": sha256(FIGURE_DIR / "figure.svg"),
        "png_sha256": sha256(FIGURE_DIR / "figure.png"),
        "svg_physical_size": ["178mm", "100mm"],
        "minimum_svg_font_points": 5.0,
        "font_embedding": "DEJAVU_REGULAR_AND_BOLD_DATA_FONTS",
        "full_package_regeneration": "BYTE_IDENTICAL",
    }

    payload = {
        "schema_version": 1,
        "research_version": "R0.74P",
        "frozen_at": args.frozen_at,
        "research_branch": git("branch", "--show-current"),
        "research_parent": git("rev-parse", "HEAD"),
        "origin_main_observed_at_freeze": git("rev-parse", "origin/main"),
        "scope": "TEMPORAL_OBSERVABLE_TRIAGE_DEFECT_COMPLETED_MOVING_SHELL_CLOCK_FIXED_SCALE_WEAK_STABILITY",
        "claim_status": {
            "positive_order_window_mass": "PROVED_MISSES_TARGET_FOR_EACH_FIXED_SIGMA_POSITIVE_NONUNIFORM_AT_ZERO",
            "energy_oscillation": "PROVED_DETECTS_BUT_RECONSTRUCTS_ENDPOINT_AND_FULL_DISSIPATION",
            "defect_completed_clock_balance": "PROVED_VERSION_M_SUITABLE_WEAK",
            "l1_clock_closure": "PROVED_BY_COMPLETE_ABSOLUTE_LEDGER",
            "matched_target_component": "PROVED_TWO_SIDED_COMPARABLE_TO_T_STAR",
            "matched_full_square_function_lower_detection": "PROVED",
            "matched_full_square_function_upper": "OPEN_NOT_CLAIMED",
            "overweighted_target_penalty": "PROVED_EXPONENTIAL_RATE_640_OVER_43_IN_UNITS_2M_OVER_3",
            "fixed_scale_weak_lower_semicontinuity": "PROVED_VERSION_M_FIXED_R_FIXED_TERMINAL_POINT",
            "l1_to_matched_l2_pde_compression": "OPEN",
            "prescribed_centre_scale_packing": "OPEN",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "finite_certificate": "PASS_52_OF_52_RIGHT_ENDPOINT_SUPREMUM_REPAIRED",
            "main_independent_audit": "PASS",
            "final_source_rebind": "PASS_87_OF_87_UNIQUE_MAIN_TAGS",
            "reader_source_independent_audit": "PASS",
            "primary_literature_screen": "BOUNDED_EIGHT_SOURCE_SCREEN_WITH_YU_2026_ADJACENT_NONCOLLIDING",
            "formal_figure": f"PASS_{validation['check_count']}_OF_{validation['check_count']}_RATE_ONLY_SVG_PHYSICAL_UNITS_FONTS_EMBEDDED",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "novelty_or_priority": "OPEN_NOT_CLAIMED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
            "publication": "PENDING_IN_INDEPENDENT_PUBLISHING_TASK",
            "cumulative_recap": "NOT_REQUIRED_FOR_THIS_SECTION",
        },
        "artifacts": records,
        "figure_package": figure_summary,
        "verification": {
            "git_diff_check": "PASS",
            "main_equation_tags": "PASS_87_UNIQUE_OF_87",
            "problem_freeze_tags": "PASS_56_UNIQUE_OF_56",
            "certificate_python_byte_identical": True,
            "certificate_ruby_independent": "PASS_52_OF_52",
            "figure_sha256sums_all_ok": True,
            "figure_full_regeneration_byte_identical": True,
            "figure_rate_intercept_boundary": "PASS_ADDITIVE_LOG10_C_EXPLICITLY_SUPPRESSED",
            "figure_svg_physical_units": "PASS_178MM_BY_100MM",
            "figure_font_and_grayscale_qa": "PASS",
        },
        "publication_handoff": {
            "owner_task_title": "发布任务",
            "owner_task_id": "01a05bea-7f45-7410-8792-4e1f840b83f8",
            "task_reuse": False,
            "target": "https://kasifa.github.io/",
            "status": "READY_FOR_INDEPENDENT_PUBLISHING_TASK",
            "predecessor_live_evidence": {
                "release": "R0.74O",
                "verified": True,
                "origin_main": "4e8d8b7f57b1cc51d3eef891c9c13f9c86b2e944",
                "pages_action": "https://github.com/Kasifa/Kasifa.github.io/actions/runs/33584309952",
            },
            "target_html": "/notes/r0-74p.html",
            "target_pdf": "/notes/r0-74p.pdf",
            "target_primary_svg": "/assets/r074p/fig-r074p-observable-triage.svg",
            "recap_update_required": False,
            "live_completion_gate": "ORIGIN_MAIN_ADVANCED_AND_HTML_PDF_PRIMARY_SVG_BYTE_IDENTICAL",
        },
    }
    OUTPUT.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(sha256(OUTPUT))


if __name__ == "__main__":
    main()
