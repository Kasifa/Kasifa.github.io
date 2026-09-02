#!/usr/bin/env python3
"""Finite certificate for the R0.74S boundary-mismatch clock."""

from __future__ import annotations

import hashlib
import json
import os
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = Path(
    os.environ.get(
        "R074S_BOUNDARY_NOTE",
        REPO / "research/r074s_boundary_mismatch_clock.md",
    )
)
JSON_OUT = Path(
    os.environ.get(
        "R074S_BOUNDARY_JSON",
        REPO / "research/r074s_boundary_mismatch_certificate.json",
    )
)
REPORT_OUT = Path(
    os.environ.get(
        "R074S_BOUNDARY_REPORT",
        REPO / "research/r074s_boundary_mismatch_certificate_report.md",
    )
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fs(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def exact(identifier: str, left: Fraction, right: Fraction, note: str) -> dict:
    return {
        "id": identifier,
        "left": fs(left),
        "right": fs(right),
        "margin": fs(left - right),
        "note": note,
        "pass": left == right,
    }


def theta_piecewise(value: Fraction) -> Fraction:
    """Exact monotone transition model for finite dominance sampling only."""
    if value <= -1:
        return Fraction(0)
    if value >= 0:
        return Fraction(1)
    return value + 1


def cutoff_dominance_check() -> dict:
    """Check beta <= psi on an exact rational radial grid."""
    delta = Fraction(1, 8)
    radius = Fraction(2)
    next_radius = Fraction(4)
    samples = [
        radius + Fraction(j, 64)
        for j in range(-24, 25)
    ]
    failures = []
    nonzero_outside = []
    for rho in samples:
        inner_arg = (rho - radius) / delta
        beta = theta_piecewise(inner_arg) * theta_piecewise(-inner_arg)
        psi = theta_piecewise(inner_arg) * theta_piecewise(
            (next_radius - rho) / delta
        )
        if not (Fraction(0) <= beta <= psi):
            failures.append(
                {
                    "rho": fs(rho),
                    "beta": fs(beta),
                    "psi": fs(psi),
                }
            )
        if not (radius - delta <= rho <= radius + delta) and beta != 0:
            nonzero_outside.append({"rho": fs(rho), "beta": fs(beta)})
    return {
        "id": "exact_rational_cutoff_dominance_grid",
        "samples_checked": len(samples),
        "dominance_failures": failures,
        "support_failures": nonzero_outside,
        "pass": not failures and not nonzero_outside,
    }


def affine_integral(a: Fraction, b: Fraction, left: Fraction, right: Fraction) -> Fraction:
    """Integral of a+b*t over [left,right]."""
    return a * (right - left) + b * (right * right - left * left) / 2


def stopped_mismatch_check() -> dict:
    """Exhaust one nontrivial stopped-family indexing fixture exactly."""
    tau = Fraction(3)
    shell_set = {1, 2, 3, 5, 6}
    stops = {
        1: Fraction(1, 2),
        2: Fraction(3, 2),
        3: Fraction(1),
        5: Fraction(2),
        6: Fraction(1, 4),
    }
    internal = sorted(
        m for m in range(2, 8) if m - 1 in shell_set and m in shell_set
    )
    weights = {m: Fraction(32, 35) ** (m - 1) for m in internal}
    affine_rows = {
        2: (Fraction(5, 7), Fraction(-2, 9)),
        3: (Fraction(-4, 11), Fraction(7, 13)),
        6: (Fraction(9, 10), Fraction(3, 17)),
    }

    breakpoints = sorted({Fraction(0), tau, *stops.values()})
    direct = Fraction(0)
    segment_count = 0
    for left, right in zip(breakpoints, breakpoints[1:]):
        if left == right:
            continue
        midpoint = (left + right) / 2
        active = {
            k for k in shell_set if stops[k] < midpoint <= tau
        }
        for m in internal:
            if m - 1 in active and m in active:
                a, b = affine_rows[m]
                direct += weights[m] * affine_integral(a, b, left, right)
        segment_count += 1

    clock_rows = {}
    clock_sum = Fraction(0)
    for m in internal:
        start = max(stops[m - 1], stops[m])
        a, b = affine_rows[m]
        row = weights[m] * affine_integral(a, b, start, tau)
        clock_rows[str(m)] = {
            "max_stop": fs(start),
            "weighted_increment": fs(row),
        }
        clock_sum += row
    return {
        "id": "exact_stopped_boundary_clock_fixture",
        "internal_indices": internal,
        "segments_checked": segment_count,
        "direct_active_integral": fs(direct),
        "clock_increment_sum": fs(clock_sum),
        "clock_rows": clock_rows,
        "pass": direct == clock_sum,
    }


def exceptional_cauchy_check() -> dict:
    """Check the squared finite-set Cauchy inequality on all small subsets."""
    values = [
        Fraction(2, 5),
        Fraction(7, 11),
        Fraction(5, 4),
        Fraction(9, 13),
        Fraction(3, 8),
        Fraction(11, 9),
    ]
    failures = []
    checked = 0
    nmax = 3
    for mask in range(1 << len(values)):
        indices = [i for i in range(len(values)) if mask & (1 << i)]
        if len(indices) > nmax:
            continue
        left = sum((values[i] for i in indices), Fraction(0)) ** 2
        right = Fraction(len(indices)) * sum(
            (value * value for value in values), Fraction(0)
        )
        if left > right:
            failures.append(
                {
                    "mask": mask,
                    "left_squared": fs(left),
                    "right_squared": fs(right),
                }
            )
        checked += 1
    return {
        "id": "all_exception_subsets_cauchy_n_le_3",
        "subsets_checked": checked,
        "failures": failures,
        "pass": not failures,
    }


def composite_coefficient_check() -> dict:
    """Check every extended-value branch of the packed coefficient."""

    def coefficient(
        m: int,
        gamma: Fraction,
        lam: Fraction,
        theta: Fraction | str,
    ) -> Fraction | str:
        if lam == 0:
            return Fraction(0)
        if theta == 0:
            return "+infinity"
        if theta == "+infinity":
            return Fraction(0)
        assert isinstance(theta, Fraction)
        return Fraction(2 ** (2 * m)) * gamma * lam**3 / theta**2

    cases = [
        {
            "id": "lambda_zero_theta_zero",
            "actual": coefficient(2, Fraction(3, 5), Fraction(0), Fraction(0)),
            "expected": Fraction(0),
        },
        {
            "id": "lambda_positive_theta_zero",
            "actual": coefficient(2, Fraction(3, 5), Fraction(2), Fraction(0)),
            "expected": "+infinity",
        },
        {
            "id": "lambda_zero_theta_infinite",
            "actual": coefficient(2, Fraction(3, 5), Fraction(0), "+infinity"),
            "expected": Fraction(0),
        },
        {
            "id": "lambda_positive_theta_infinite",
            "actual": coefficient(2, Fraction(3, 5), Fraction(2), "+infinity"),
            "expected": Fraction(0),
        },
        {
            "id": "ordinary_finite_row",
            "actual": coefficient(2, Fraction(3, 5), Fraction(2), Fraction(4)),
            "expected": Fraction(24, 5),
        },
    ]
    for item in cases:
        for key in ("actual", "expected"):
            if isinstance(item[key], Fraction):
                item[key] = fs(item[key])
        item["pass"] = item["actual"] == item["expected"]
    return {
        "id": "composite_extended_value_conventions",
        "cases": cases,
        "pass": all(item["pass"] for item in cases),
    }


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.([^}]+)\}", body)
    expected = [str(k) for k in range(60, 85)]
    checks = [
        {
            "id": "tags_consecutive",
            "actual": tags,
            "expected": expected,
            "pass": tags == expected,
        },
        {
            "id": "tags_unique",
            "actual_count": len(tags),
            "unique_count": len(set(tags)),
            "pass": len(tags) == len(set(tags)) == len(expected),
        },
    ]
    required = (
        "0\\le\\beta_m^R\\le\\psi_m^R",
        "\\{r_m-\\delta\\le |y|\\le r_m+\\delta\\}",
        "for \\(y\\ne0\\)",
        "defined to be zero at \\(y=0\\)",
        "0\\le B_m^R\\le\\Psi_m^R",
        "=E_{m,R}^{\\partial}+D_{m,R}^{\\partial}\\ge0",
        "0\\le K_{m,R}^{\\partial}(t)\\le K_{m,R}(t)",
        "\\sum_{m\\ge1}\\operatorname {TV}Q_{m,R}^{\\partial}",
        "\\sum_{m\\ge1}p_{m,R}^{\\partial}(J_m)",
        "\\widehat\\sigma_m:=\\max(\\sigma_{m-1},\\sigma_m)",
        "[F_{m,R}^{\\partial}(\\tau)",
        "\\sum_{m\\in I^\\partial}K_{m,R}^{\\partial}(\\tau)",
        "2^{2m/3}\\gamma_m^{1/3}",
        "2^{2m}\\gamma_m\\Lambda_m^3",
        "\\mathcal A_{m,R}^{\\partial}(\\tau;J,\\Lambda)",
        "read the entire right side of (S.77) as",
        "0,&\\Lambda=0",
        "+\\infty,&\\Lambda>0,\\quad\\Theta_{m,R}^{\\partial}(\\tau;J)=0",
        "forms either \\(+\\infty\\cdot0\\) or \\(0\\cdot+\\infty\\)",
        "the entire right side of (S.79) is defined to be",
        "\\sqrt{N_\\partial}\\,Y_{2,R}^{\\rm sf}",
        "The clock-to-endpoint extraction and temporal persistence hypotheses remain",
        "result controls only the mismatch channel",
        "**OPEN / NOT CLAIMED**",
        "**NOT CLAY.**",
    )
    forbidden = (
        "the hypotheses of Theorem 6.1 are proved",
        "root, outer, and weight-drop channels are controlled",
        "the stopped-work inequality is unconditional",
        "global regularity is proved",
        "Millennium problem is solved",
        "\\subset C_m^-\\cup\\{|y|=r_m\\}\\cup C_m^+",
    )
    for sentinel in required:
        checks.append(
            {
                "id": "required_"
                + hashlib.sha256(sentinel.encode()).hexdigest()[:12],
                "sentinel": sentinel,
                "pass": sentinel in body,
            }
        )
    for phrase in forbidden:
        checks.append(
            {
                "id": "forbidden_"
                + hashlib.sha256(phrase.encode()).hexdigest()[:12],
                "phrase": phrase,
                "pass": phrase not in body,
            }
        )
    checks.extend(
        [
            {
                "id": "boundary_volume_exponent_count",
                "literal": "2^{2m}R^3",
                "minimum_count": 2,
                "actual_count": body.count("2^{2m}R^3"),
                "pass": body.count("2^{2m}R^3") >= 2,
            },
            {
                "id": "persistence_cube_exponent_count",
                "literal": "2^{2m}\\gamma_m",
                "minimum_count": 3,
                "actual_count": body.count("2^{2m}\\gamma_m"),
                "pass": body.count("2^{2m}\\gamma_m") >= 3,
            },
            {
                "id": "display_math_balanced",
                "left_count": body.count("\\["),
                "right_count": body.count("\\]"),
                "pass": body.count("\\[") == body.count("\\]"),
            },
            {
                "id": "inline_math_balanced",
                "left_count": body.count("\\("),
                "right_count": body.count("\\)"),
                "pass": body.count("\\(") == body.count("\\)"),
            },
            {
                "id": "no_disallowed_control_characters",
                "pass": not any(
                    ord(ch) < 32 and ch not in "\n\t" for ch in body
                ),
            },
        ]
    )
    return checks


def build_report(payload: dict) -> str:
    lines = [
        "# R0.74S boundary-mismatch clock certificate report",
        "",
        "## Result",
        "",
        f"**{payload['summary']['result']}** — "
        f"{payload['summary']['exact_passed']}/"
        f"{payload['summary']['exact_total']} exact rational checks, "
        f"{payload['summary']['finite_passed']}/"
        f"{payload['summary']['finite_total']} finite ledgers, and "
        f"{payload['summary']['structural_passed']}/"
        f"{payload['summary']['structural_total']} structural checks passed.",
        "",
        "## Exact rational and exponent ledger",
        "",
        "| Check | Left | Right | Margin |",
        "|---|---:|---:|---:|",
    ]
    for item in payload["exact_checks"]:
        lines.append(
            f"| {item['id']} | {item['left']} | {item['right']} | "
            f"{item['margin']} |"
        )
    lines.extend(
        [
            "",
            "## Finite ledgers",
            "",
            "- The exact rational cutoff model checks pointwise "
            "\\(0\\le\\beta\\le\\psi\\) and two-collar support on "
            f"{payload['finite_checks'][0]['samples_checked']} radial samples.",
            "- A nonconsecutive five-shell stopped family checks the maximum-stop",
            "  activation identity against cumulative boundary-clock increments.",
            "- Every subset of six rational exception values with cardinality at",
            "  most three satisfies the squared Cauchy--Schwarz bound.",
            "- All five zero, positive, finite, and infinite branches of the",
            "  composite persistence coefficient satisfy the frozen convention.",
            "",
            "## Exponent chain",
            "",
            "The certificate checks that a boundary support volume "
            "\\(2^{2m}R^3\\) contributes \\(2^m\\) after the spatial",
            "square root, then \\(2^{2m/3}\\gamma_m^{1/3}\\) after the",
            "time-persistence step, and finally",
            "\\(2^{2m}\\gamma_m\\Lambda_m^3(\\Theta_m^\\partial)^{-2}\\)",
            "after the shellwise cubic Hölder step.",
            "",
            "## Boundary",
            "",
            "This finite certificate does not prove the suitable local-energy",
            "identity, periodized support ledger, positivity of the dissipation",
            "measure, or the conditional hypotheses of Theorem 6.1.  It does not",
            "control the root, outer, or weight-drop channels.",
            "",
            "**FINITE ONLY. NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = [
        exact("collar_half_width", Fraction(1, 8), Fraction(1, 8), "delta/R"),
        exact(
            "two_collar_total_width",
            2 * Fraction(1, 8),
            Fraction(1, 4),
            "two-sided thickness in units of R",
        ),
        exact(
            "minimum_inner_radius",
            Fraction(2) - Fraction(1, 8),
            Fraction(15, 8),
            "r_1-delta in units of R",
        ),
        exact(
            "annulus_volume_polynomial_m1",
            (Fraction(2) + Fraction(1, 8)) ** 3
            - (Fraction(2) - Fraction(1, 8)) ** 3,
            6 * Fraction(2) ** 2 * Fraction(1, 8)
            + 2 * Fraction(1, 8) ** 3,
            "radial cubic difference before 4*pi/3",
        ),
        exact(
            "holder_conjugacy",
            Fraction(1, 3) + Fraction(2, 3),
            Fraction(1),
            "shellwise Holder exponents",
        ),
        exact(
            "volume_square_root_shell_power",
            Fraction(2) * Fraction(1, 2),
            Fraction(1),
            "2m volume exponent before time integration",
        ),
        exact(
            "endpoint_shell_power",
            Fraction(1) * Fraction(2, 3),
            Fraction(2, 3),
            "power after solving the 3/2 persistence inequality",
        ),
        exact(
            "preintegration_gamma_split",
            Fraction(3, 2) - Fraction(1),
            Fraction(1, 2),
            "gamma exponent left after factoring the payment density",
        ),
        exact(
            "endpoint_gamma_power",
            Fraction(1, 2) * Fraction(2, 3),
            Fraction(1, 3),
            "boundary endpoint coefficient",
        ),
        exact(
            "endpoint_theta_power",
            Fraction(-1) * Fraction(2, 3),
            Fraction(-2, 3),
            "persistence denominator power",
        ),
        exact(
            "coefficient_cube_shell_power",
            Fraction(2, 3) * 3,
            Fraction(2),
            "2^(2m) after cubing",
        ),
        exact(
            "coefficient_cube_gamma_power",
            Fraction(1, 3) * 3,
            Fraction(1),
            "gamma_m after cubing",
        ),
        exact(
            "coefficient_cube_theta_power",
            Fraction(-2, 3) * 3,
            Fraction(-2),
            "Theta_m^(-2) after cubing",
        ),
        exact(
            "payment_outer_power",
            Fraction(1) * Fraction(2, 3),
            Fraction(2, 3),
            "sum p_m enters at two-thirds power",
        ),
    ]
    finite_checks = [
        cutoff_dominance_check(),
        stopped_mismatch_check(),
        exceptional_cauchy_check(),
        composite_coefficient_check(),
    ]
    structural = structural_checks(body)
    passed = (
        all(item["pass"] for item in exact_checks)
        and all(item["pass"] for item in finite_checks)
        and all(item["pass"] for item in structural)
    )
    try:
        note_field = str(NOTE.relative_to(REPO))
    except ValueError:
        note_field = str(NOTE)
    payload = {
        "schema": "r074s-boundary-mismatch-certificate-v1",
        "scope": (
            "FINITE ONLY: boundary geometry, stopped indexing, exponent "
            "bookkeeping, tags, and claim boundaries"
        ),
        "note": note_field,
        "note_sha256": sha256(NOTE),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "claim_boundary": {
            "boundary_bump_geometry": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "completed_boundary_clock": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "mismatch_stopped_identity": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "boundary_persistence_coefficient": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "conditional_theorem_implication": "PROVED_CONDITIONAL",
            "clock_to_endpoint_hypothesis": "OPEN",
            "temporal_persistence_packing": "OPEN",
            "root_outer_weight_drop_channels": "OPEN",
            "fixed_scale_Q1_unconditional": "OPEN",
            "clay_millennium_problem_solved": False,
        },
        "summary": {
            "result": "PASS" if passed else "FAIL",
            "exact_passed": sum(bool(x["pass"]) for x in exact_checks),
            "exact_total": len(exact_checks),
            "finite_passed": sum(bool(x["pass"]) for x in finite_checks),
            "finite_total": len(finite_checks),
            "structural_passed": sum(bool(x["pass"]) for x in structural),
            "structural_total": len(structural),
        },
    }
    JSON_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUT.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    REPORT_OUT.write_text(build_report(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
