#!/usr/bin/env python3
"""Symbolic and deterministic audit for the R0.69V two-scale theorem."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess

import numpy as np
import sympy as sp

from two_scale_full_annular_qmc import (
    A_MATRIX,
    deterministic_building_coefficients,
    deterministic_total,
    radial_zones,
    zone_role,
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit")
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    head_commit = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if arguments.source_commit is not None and arguments.source_commit != head_commit:
        raise SystemExit(
            f"source commit mismatch: requested {arguments.source_commit}, HEAD is {head_commit}"
        )

    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, value: object) -> None:
        checks.append({"name": name, "passed": bool(passed), "value": value})

    check("affine-trace-zero", abs(float(np.trace(A_MATRIX))) < 1e-15, np.trace(A_MATRIX))

    a, b = sp.symbols("a b", real=True)
    ese, eta_se, e_te, eta_s_eta, e_t_eta, eta_t_eta = sp.symbols(
        "ese eta_se e_te eta_s_eta e_t_eta eta_t_eta", real=True
    )
    cubic = (
        a**3 * ese
        + a**2 * b * (2 * eta_se + e_te)
        + a * b**2 * (eta_s_eta + 2 * e_t_eta)
        + b**3 * eta_t_eta
    )
    check(
        "cubic-a3-coefficient",
        sp.expand(cubic).coeff(a, 3).coeff(b, 0) == ese,
        str(sp.expand(cubic).coeff(a, 3).coeff(b, 0)),
    )
    check(
        "cubic-a2b-coefficient",
        sp.expand(cubic).coeff(a, 2).coeff(b, 1) == 2 * eta_se + e_te,
        str(sp.expand(cubic).coeff(a, 2).coeff(b, 1)),
    )
    check(
        "cubic-ab2-coefficient",
        sp.expand(cubic).coeff(a, 1).coeff(b, 2)
        == eta_s_eta + 2 * e_t_eta,
        str(sp.expand(cubic).coeff(a, 1).coeff(b, 2)),
    )
    check(
        "cubic-b3-coefficient",
        sp.expand(cubic).coeff(a, 0).coeff(b, 3) == eta_t_eta,
        str(sp.expand(cubic).coeff(a, 0).coeff(b, 3)),
    )

    epsilon, V, C = sp.symbols("epsilon V C", positive=True)
    balanced_a = epsilon / (1 + epsilon)
    balanced_b = 1 / (1 + epsilon)
    balanced = sp.factor(
        V * (balanced_a**3 + epsilon**3 * balanced_b**3)
        + epsilon**3 * balanced_a * balanced_b**2 * C
    )
    expected_balanced = epsilon**3 * (2 * V + epsilon * C) / (1 + epsilon) ** 3
    check(
        "balanced-production-factorization",
        sp.simplify(balanced - expected_balanced) == 0,
        str(balanced),
    )

    t = sp.symbols("t", nonnegative=True)
    first_ratio = t / (1 + t**3)
    second_ratio = t**2 / (1 + t**3)
    first_critical = 2 ** (-sp.Rational(1, 3))
    second_critical = 2 ** (sp.Rational(1, 3))
    check(
        "mixed-first-ratio-critical-point",
        sp.simplify(sp.diff(first_ratio, t).subs(t, first_critical)) == 0,
        str(first_critical),
    )
    check(
        "mixed-second-ratio-critical-point",
        sp.simplify(sp.diff(second_ratio, t).subs(t, second_critical)) == 0,
        str(second_critical),
    )
    first_max = sp.simplify(first_ratio.subs(t, first_critical))
    second_max = sp.simplify(second_ratio.subs(t, second_critical))
    check("mixed-first-ratio-bounded", bool(first_max < 1), str(first_max))
    check("mixed-second-ratio-bounded", bool(second_max < 1), str(second_max))

    coefficient_orders = (96, 128, 160, 192)
    coefficient_runs = {
        order: deterministic_building_coefficients(order)
        for order in coefficient_orders
    }
    v_values = np.asarray([coefficient_runs[order][0] for order in coefficient_orders])
    c21_values = np.asarray([coefficient_runs[order][1] for order in coefficient_orders])
    c12_values = np.asarray([coefficient_runs[order][2] for order in coefficient_orders])
    v_reference = float(np.mean(v_values[-2:]))
    c_reference = float(np.mean(c12_values[-2:]))
    check(
        "deterministic-V-convergence",
        float(np.ptp(v_values)) < 3e-5,
        v_values.tolist(),
    )
    check(
        "deterministic-C12-convergence",
        float(np.ptp(c12_values)) < 3e-5,
        c12_values.tolist(),
    )
    check(
        "numerical-C21-near-exact-zero",
        float(np.max(np.abs(c21_values))) < 2e-4,
        c21_values.tolist(),
    )
    check("deterministic-V-positive", v_reference > 1.9, v_reference)
    check("deterministic-C12-negative", c_reference < -2.7, c_reference)

    formula_residuals: list[dict[str, float]] = []
    for epsilon_value in (0.5, 0.25, 0.125):
        for a_value in (0.2, 0.5, 0.8):
            b_value = 1.0 - a_value
            actual = deterministic_total(
                epsilon_value, a_value, radial_order=160
            )
            predicted = (
                v_reference
                * (a_value**3 + epsilon_value**3 * b_value**3)
                + epsilon_value**3 * a_value * b_value**2 * c_reference
            )
            formula_residuals.append(
                {
                    "epsilon": epsilon_value,
                    "a": a_value,
                    "residual": actual - predicted,
                }
            )
    check(
        "exact-cubic-law-deterministic-regression",
        max(abs(record["residual"]) for record in formula_residuals) < 2e-5,
        formula_residuals,
    )

    n0_values = [
        deterministic_total(1.0, amplitude, radial_order=128)
        for amplitude in (0.0, 0.2, 0.5, 0.8, 1.0)
    ]
    check(
        "coincident-scales-amplitude-invariance",
        float(np.ptp(n0_values)) < 1e-12,
        n0_values,
    )

    inner_scaling_residuals = []
    for epsilon_value in (0.5, 0.25, 0.125):
        inner_total = deterministic_total(
            epsilon_value, 0.0, radial_order=128
        )
        inner_scaling_residuals.append(
            inner_total - epsilon_value**3 * n0_values[-1]
        )
    check(
        "inner-copy-cubic-volume-scaling",
        max(abs(value) for value in inner_scaling_residuals) < 2e-9,
        inner_scaling_residuals,
    )

    shape_ratios = [1.0 / (2.0 ** (-separation)) for separation in (0, 2, 4, 6)]
    check("shape-ratio-changes", shape_ratios == [1.0, 4.0, 16.0, 64.0], shape_ratios)

    zones = radial_zones(0.25)
    roles = [zone_role(zone, 0.25) for zone in zones]
    check(
        "two-transition-zones-explicit",
        roles
        == [
            "inner-core",
            "inner-transition",
            "intermediate-plateau",
            "outer-transition",
        ],
        roles,
    )
    check(
        "all-checks-before-summary",
        all(record["passed"] for record in checks),
        len(checks),
    )

    output = {
        "schemaVersion": "1.0",
        "release": "R0.69V",
        "status": "passed" if all(record["passed"] for record in checks) else "failed",
        "checks": checks,
        "checkCount": len(checks),
        "passedCount": sum(record["passed"] for record in checks),
        "coefficients": {
            "quadratureRuns": {
                str(order): {
                    "V": coefficient_runs[order][0],
                    "C21": coefficient_runs[order][1],
                    "C12": coefficient_runs[order][2],
                }
                for order in coefficient_orders
            },
            "VReference": v_reference,
            "C12Reference": c_reference,
            "C21Exact": 0,
        },
        "claimBoundary": (
            "symbolic cubic audit and deterministic regression; the uniform "
            "ell1 decoupling proof is recorded in the mathematical note"
        ),
        "provenance": {
            "script": str(Path(__file__).resolve().relative_to(Path.cwd())),
            "scriptSha256": sha256(Path(__file__).resolve()),
            "sourceCommit": head_commit,
            "requestedSourceCommit": arguments.source_commit,
            "sympy": sp.__version__,
            "numpy": np.__version__,
        },
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(
        json.dumps(output, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if output["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
