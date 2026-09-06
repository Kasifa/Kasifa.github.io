#!/usr/bin/env python3
"""Read-only deterministic QA for the AY--BB lagged-pressure source bundle.

This validates bytes, Markdown/TeX hygiene, formula-tag sequences, exact
Fraction exponent arithmetic, and the preceding frozen manifest.  It is not a
PDE proof checker and does not write files.
"""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction as F
from pathlib import Path
from typing import Any


REPO = Path(__file__).resolve().parents[1]
PREVIOUS_MANIFEST = Path(
    "research/clay_b_pressure_test_coupling_release_20260906.json"
)
BB_SOURCE = Path(
    "research/clay_b_lag_scale_pressure_budget_preflight_20260906.md"
)
SOURCES = (
    (
        Path("research/clay_b_time_ordered_pressure_preflight_20260906.md"),
        "AY",
        33,
    ),
    (
        Path("research/clay_b_joint_early_heat_work_preflight_20260906.md"),
        "AZ",
        23,
    ),
    (
        Path(
            "research/clay_b_lagged_heat_pressure_reduction_preflight_20260906.md"
        ),
        "BA",
        17,
    ),
    (
        BB_SOURCE,
        "BB",
        25,
    ),
    (
        Path("research/clay_b_lagged_pressure_report_20260906.md"),
        "",
        0,
    ),
    (
        Path("research/clay_b_lagged_pressure_literature_scope_20260906.md"),
        "",
        0,
    ),
    (
        Path("research/clay_b_recent_source_work_plan_20260906.md"),
        "",
        0,
    ),
    (
        Path("research/clay_b_lagged_pressure_internal_audit_20260906.md"),
        "",
        0,
    ),
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def q(value: F) -> str:
    if value.denominator == 1:
        return str(value.numerator)
    return f"{value.numerator}/{value.denominator}"


def delimiter_check(text: str, opener: str, closer: str) -> bool:
    token_re = re.compile(
        f"(?:{re.escape(opener)}|{re.escape(closer)})"
    )
    depth = 0
    for match in token_re.finditer(text):
        if match.group(0) == opener:
            depth += 1
            if depth != 1:
                return False
        else:
            depth -= 1
            if depth != 0:
                return False
    return depth == 0


def source_record(
    relative: Path, prefix: str, expected_tags: int, failures: list[str]
) -> dict[str, Any]:
    path = REPO / relative
    if not path.is_file():
        failures.append(f"missing source: {relative}")
        return {"path": str(relative), "status": "FAIL"}

    data = path.read_bytes()
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        failures.append(f"non-UTF-8 source: {relative}")
        return {
            "path": str(relative),
            "sha256": sha256(data),
            "bytes": len(data),
            "status": "FAIL",
        }

    tags = re.findall(r"\\tag\{([A-Z]+)\.([0-9]+)\}", text)
    tag_prefixes = [item[0] for item in tags]
    tag_numbers = [int(item[1]) for item in tags]
    expected_numbers = list(range(1, expected_tags + 1))
    unique_tags = len(tags) == len(set(tags))
    ordered_tags = (
        tag_prefixes == [prefix] * expected_tags
        and tag_numbers == expected_numbers
    )
    no_controls = all(ord(char) >= 32 or char == "\n" for char in text)
    no_trailing = all(
        line == line.rstrip(" \t") for line in text.splitlines()
    )
    inline_ok = delimiter_check(text, r"\(", r"\)")
    display_ok = delimiter_check(text, r"\[", r"\]")
    final_newline = data.endswith(b"\n")

    checks = {
        "utf8": True,
        "no_control_characters": no_controls,
        "no_trailing_whitespace": no_trailing,
        "inline_delimiters": inline_ok,
        "display_delimiters": display_ok,
        "final_newline": final_newline,
        "unique_formula_tags": unique_tags,
        "continuous_ordered_formula_tags": ordered_tags,
    }
    for name, passed in checks.items():
        if not passed:
            failures.append(f"{relative}: {name}")

    return {
        "path": str(relative),
        "prefix": prefix,
        "sha256": sha256(data),
        "bytes": len(data),
        "lines": data.count(b"\n"),
        "formula_tags": len(tags),
        "first_formula_tag": f"{prefix}.1" if expected_tags else None,
        "last_formula_tag": (
            f"{prefix}.{expected_tags}" if expected_tags else None
        ),
        "checks": checks,
    }


def git_blob(commit: str, relative: str) -> bytes:
    completed = subprocess.run(
        ["git", "show", f"{commit}:{relative}"],
        cwd=REPO,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.decode("utf-8", errors="replace").strip()
        )
    return completed.stdout


def previous_manifest_record(failures: list[str]) -> dict[str, Any]:
    manifest_path = REPO / PREVIOUS_MANIFEST
    raw = manifest_path.read_bytes()
    manifest = json.loads(raw.decode("utf-8"))
    source_commit = manifest["source_commit"]
    base_commit = manifest["base_commit"]
    file_rows = manifest["files"]
    dependency_rows = manifest["dependencies"]
    rows = [*file_rows, *dependency_rows]

    paths = [row["path"] for row in rows]
    unique_paths = len(paths) == len(set(paths))
    declared_count = manifest["qa"]["hash_rows_expected"]
    declared_checked = manifest["qa"]["hash_rows_checked"]
    count_ok = (
        len(file_rows) == 12
        and len(dependency_rows) == 25
        and len(rows) == 37
        and declared_count == 37
        and declared_checked == 37
        and unique_paths
    )
    if not count_ok:
        failures.append("previous manifest: row count or path uniqueness")

    commit_type = subprocess.run(
        ["git", "cat-file", "-t", source_commit],
        cwd=REPO,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    commit_object_ok = (
        commit_type.returncode == 0 and commit_type.stdout.strip() == "commit"
    )
    if not commit_object_ok:
        failures.append("previous manifest: source_commit is not a commit")

    parent = subprocess.run(
        ["git", "rev-parse", f"{source_commit}^"],
        cwd=REPO,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    parent_ok = parent.returncode == 0 and parent.stdout.strip() == base_commit
    if not parent_ok:
        failures.append("previous manifest: base_commit is not the parent")

    worktree_matches = 0
    commit_matches = 0
    row_failures: list[str] = []
    for row in rows:
        relative = row["path"]
        expected_hash = row["sha256"]
        expected_bytes = row["bytes"]
        path = REPO / relative
        if not path.is_file():
            row_failures.append(f"missing worktree path: {relative}")
            continue
        local = path.read_bytes()
        local_ok = (
            sha256(local) == expected_hash and len(local) == expected_bytes
        )
        if local_ok:
            worktree_matches += 1
        else:
            row_failures.append(f"worktree hash/size mismatch: {relative}")

        row_commit = row.get("commit", source_commit)
        if row_commit != source_commit:
            row_failures.append(f"row commit mismatch: {relative}")
            continue
        try:
            committed = git_blob(source_commit, relative)
        except RuntimeError as error:
            row_failures.append(f"missing commit blob: {relative}: {error}")
            continue
        committed_ok = (
            committed == local
            and sha256(committed) == expected_hash
            and len(committed) == expected_bytes
        )
        if committed_ok:
            commit_matches += 1
        else:
            row_failures.append(f"commit byte/hash/size mismatch: {relative}")

    failures.extend(f"previous manifest: {item}" for item in row_failures)
    return {
        "path": str(PREVIOUS_MANIFEST),
        "sha256": sha256(raw),
        "bytes": len(raw),
        "physical_lines": raw.count(b"\n"),
        "source_commit": source_commit,
        "base_commit": base_commit,
        "source_commit_object": commit_object_ok,
        "base_is_source_parent": parent_ok,
        "file_rows": len(file_rows),
        "dependency_rows": len(dependency_rows),
        "hash_rows": len(rows),
        "unique_paths": unique_paths,
        "worktree_matches": worktree_matches,
        "commit_matches": commit_matches,
        "checks": {
            "declared_counts_match": count_ok,
            "all_worktree_hashes_and_sizes_match": worktree_matches == 37,
            "all_commit_bytes_hashes_and_sizes_match": commit_matches == 37,
        },
        "row_failures": row_failures,
    }


def fraction_checks(bb_text: str, failures: list[str]) -> dict[str, Any]:
    delta = F(-4)
    terminal = F(3)
    b_k2 = F(9, 8)
    integrals = {
        "I3": {"A_J": F(-1), "constant": delta},
        "I2": {"A_J": F(-2), "constant": delta},
        "I1": {"A_J": F(-3), "constant": delta},
    }
    bb10_input = (
        ("B2_I3", 2, "I3", F(-7, 4), F(-19, 4)),
        ("B3_I2", 3, "I2", F(-13, 8), F(-29, 8)),
        ("B4_I1", 4, "I1", F(-3, 2), F(-5, 2)),
        ("B1_I3", 1, "I3", F(-23, 8), F(-47, 8)),
        ("B2_I2", 2, "I2", F(-11, 4), F(-19, 4)),
    )
    bb10: list[dict[str, Any]] = []
    for name, b_power, integral, expected_aj, expected_constant in bb10_input:
        computed_aj = (
            b_power * b_k2 + integrals[integral]["A_J"] - terminal
        )
        computed_constant = (
            b_power * b_k2 + integrals[integral]["constant"] - terminal
        )
        passed = (
            computed_aj == expected_aj
            and computed_constant == expected_constant
        )
        if not passed:
            failures.append(f"Fraction BB.10 mismatch: {name}")
        bb10.append(
            {
                "term": name,
                "computed_A_J_exponent": q(computed_aj),
                "expected_A_J_exponent": q(expected_aj),
                "computed_constant_exponent": q(computed_constant),
                "expected_constant_exponent": q(expected_constant),
                "pass": passed,
            }
        )

    beta_slope = F(4)
    beta_aj_intercept = integrals["I1"]["A_J"] - terminal
    beta_constant_intercept = integrals["I1"]["constant"] - terminal
    beta_threshold = -beta_aj_intercept / beta_slope
    bb12_pass = (
        beta_aj_intercept == F(-6)
        and beta_constant_intercept == F(-7)
        and beta_threshold == F(3, 2)
        and beta_slope * beta_threshold + beta_aj_intercept == 0
        and beta_slope * beta_threshold + beta_constant_intercept == -1
    )
    if not bb12_pass:
        failures.append("Fraction BB.12 mismatch")

    gamma = F(8, 3)
    bb21_input = (
        ("B2_I3_A_J", F(3, 2), F(-4), F(0)),
        ("B2_I3_constant", F(3, 2), F(-7), F(-3)),
        ("B1_I3_A_J", F(3, 4), F(-4), F(-2)),
        ("B1_I3_constant", F(3, 4), F(-7), F(-5)),
        ("pure_bb", F(2), F(-7), F(-5, 3)),
    )
    bb21: list[dict[str, Any]] = []
    for name, slope, intercept, expected in bb21_input:
        computed = slope * gamma + intercept
        passed = computed == expected
        if not passed:
            failures.append(f"Fraction BB.21/BB.23 mismatch: {name}")
        bb21.append(
            {
                "term": name,
                "gamma_coefficient": q(slope),
                "intercept": q(intercept),
                "gamma": q(gamma),
                "computed": q(computed),
                "expected": q(expected),
                "pass": passed,
            }
        )

    k_power = F(3, 4)
    conversions = {
        "K^-2_to_Lambda": -2 * k_power,
        "K^3/2_to_Lambda": F(3, 2) * k_power,
        "Lambda^-2_to_K": F(-2) / k_power,
        "Lambda^-8/3_to_K": F(-8, 3) / k_power,
        "tau_over_delta_at_gamma_8/3": F(-8, 3) - delta,
    }
    expected_conversions = {
        "K^-2_to_Lambda": F(-3, 2),
        "K^3/2_to_Lambda": F(9, 8),
        "Lambda^-2_to_K": F(-8, 3),
        "Lambda^-8/3_to_K": F(-32, 9),
        "tau_over_delta_at_gamma_8/3": F(4, 3),
    }
    conversion_pass = conversions == expected_conversions
    if not conversion_pass:
        failures.append("Fraction K/Lambda conversion mismatch")

    normalized_bb = re.sub(r"\s+", "", bb_text)
    source_fragments = (
        r"\Lambda^{-7/4}A_J^{3/4}+\Lambda^{-19/4}",
        r"\Lambda^{-13/8}A_J^{1/2}+\Lambda^{-29/8}",
        r"\Lambda^{-3/2}A_J^{1/4}+\Lambda^{-5/2}",
        r"\Lambda^{-23/8}A_J^{3/4}+\Lambda^{-47/8}",
        r"\Lambda^{-11/4}A_J^{1/2}+\Lambda^{-19/4}",
        r"\Lambda^{4\beta-6}A_J^{1/4}+\Lambda^{4\beta-7}",
        r"\Lambda^{3\gamma/2-4}A_J^{3/4}",
        r"\Lambda^{3\gamma/2-7}",
        r"\Lambda^{3\gamma/4-4}A_J^{3/4}",
        r"\Lambda^{3\gamma/4-7}",
        r"\Lambda^{2\gamma-7}",
        r"\tau=\Lambda^{-8/3}=K^{-32/9}",
    )
    missing_fragments = [
        fragment for fragment in source_fragments if fragment not in normalized_bb
    ]
    if missing_fragments:
        failures.extend(
            f"BB source exponent fragment missing: {fragment}"
            for fragment in missing_fragments
        )

    return {
        "method": "Python fractions.Fraction exact arithmetic",
        "inputs": {
            "delta_Lambda_exponent": q(delta),
            "terminal_H_lower_exponent": q(terminal),
            "B_at_tau_cK^-2_Lambda_exponent": q(b_k2),
            "I3_A_J_and_constant_exponents": [
                q(integrals["I3"]["A_J"]),
                q(integrals["I3"]["constant"]),
            ],
            "I2_A_J_and_constant_exponents": [
                q(integrals["I2"]["A_J"]),
                q(integrals["I2"]["constant"]),
            ],
            "I1_A_J_and_constant_exponents": [
                q(integrals["I1"]["A_J"]),
                q(integrals["I1"]["constant"]),
            ],
        },
        "BB.10": bb10,
        "BB.12": {
            "beta_slope": q(beta_slope),
            "A_J_intercept": q(beta_aj_intercept),
            "constant_intercept": q(beta_constant_intercept),
            "sufficient_beta_endpoint": q(beta_threshold),
            "endpoint_A_J_exponent": q(
                beta_slope * beta_threshold + beta_aj_intercept
            ),
            "endpoint_constant_exponent": q(
                beta_slope * beta_threshold + beta_constant_intercept
            ),
            "pass": bb12_pass,
        },
        "BB.21_BB.23": bb21,
        "K_Lambda_conversions": {
            "computed": {name: q(value) for name, value in conversions.items()},
            "expected": {
                name: q(value) for name, value in expected_conversions.items()
            },
            "pass": conversion_pass,
        },
        "source_exponent_fragments_present": not missing_fragments,
        "missing_source_fragments": missing_fragments,
    }


def main() -> int:
    failures: list[str] = []
    source_records = [
        source_record(relative, prefix, expected_tags, failures)
        for relative, prefix, expected_tags in SOURCES
    ]
    previous = previous_manifest_record(failures)
    bb_text = (REPO / BB_SOURCE).read_text(encoding="utf-8")
    arithmetic = fraction_checks(bb_text, failures)
    script_raw = Path(__file__).read_bytes()
    payload = {
        "schema_version": 1,
        "status": "PASS" if not failures else "FAIL",
        "classification": (
            "deterministic source integrity, Markdown/TeX hygiene, exact "
            "rational exponent ledger, and preceding-manifest byte binding; "
            "not a PDE proof certificate or external peer review"
        ),
        "validator": {
            "path": str(Path(__file__).resolve().relative_to(REPO)),
            "sha256": sha256(script_raw),
            "read_only": True,
        },
        "source_files": source_records,
        "source_file_count": len(source_records),
        "formula_tag_total": sum(
            record.get("formula_tags", 0) for record in source_records
        ),
        "fraction_checks": arithmetic,
        "previous_release_manifest": previous,
        "failures": failures,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
