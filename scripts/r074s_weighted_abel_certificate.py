#!/usr/bin/env python3
"""Finite certificate for the R0.74S weighted stopped-Abel no-gain gate."""

from __future__ import annotations

import hashlib
import json
import re
from decimal import Decimal, getcontext
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "research/r074s_weighted_abel_no_gain.md"
JSON_OUT = REPO / "research/r074s_weighted_abel_certificate.json"
REPORT_OUT = REPO / "research/r074s_weighted_abel_certificate_report.md"


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


def proxy_checks() -> dict:
    """Exhaust pointwise Abel, component, and saturation identities for M=4."""
    m = 4
    weights = [Fraction(32, 35) ** k for k in range(m)]
    boundary = [
        Fraction(5, 7),
        Fraction(-3, 8),
        Fraction(11, 13),
        Fraction(-2, 5),
        Fraction(7, 9),
    ]
    abel_ok = component_ok = sharp_ok = True
    for mask in range(1 << m):
        c = [
            weights[k] if mask & (1 << k) else Fraction(0)
            for k in range(m)
        ]
        left = sum(
            c[k] * (boundary[k + 1] - boundary[k]) for k in range(m)
        )
        right = (
            -c[0] * boundary[0]
            + c[-1] * boundary[-1]
            + sum(
                (c[k - 1] - c[k]) * boundary[k]
                for k in range(1, m)
            )
        )
        abel_ok &= left == right

        extended = [Fraction(0), *c, Fraction(0)]
        variation = sum(
            abs(extended[k] - extended[k - 1])
            for k in range(1, len(extended))
        )
        roots = [
            k
            for k in range(m)
            if mask & (1 << k)
            and not (k > 0 and mask & (1 << (k - 1)))
        ]
        component_ok &= variation == 2 * sum(weights[k] for k in roots)

        coefficients = [
            -c[0],
            *[c[k - 1] - c[k] for k in range(1, m)],
            c[-1],
        ]
        beta = Fraction(17, 11)
        saturating = [
            beta if d > 0 else -beta if d < 0 else Fraction(0)
            for d in coefficients
        ]
        sharp_ok &= (
            sum(d * b for d, b in zip(coefficients, saturating))
            == beta * variation
        )
    return {
        "id": "exhaustive_proxy_identities_m4",
        "masks_checked": 1 << m,
        "abel_identity_pass": abel_ok,
        "component_formula_pass": component_ok,
        "sharpness_identity_pass": sharp_ok,
        "pass": abel_ok and component_ok and sharp_ok,
    }


def actual_weight_checks() -> dict:
    """Exhaust all binary active sets through M=12 for actual weights."""
    getcontext().prec = 80
    m = 12
    weights = [
        (-(Decimal(4) ** k) / Decimal(32)).exp() for k in range(m)
    ]
    low = Decimal(6) / Decimal(35)
    min_neighbor = Decimal("Infinity")
    min_lower = Decimal("Infinity")
    min_upper = Decimal("Infinity")
    max_component_error = Decimal(0)
    for k in range(m - 1):
        min_neighbor = min(
            min_neighbor,
            Decimal(32) / Decimal(35) - weights[k + 1] / weights[k],
        )
    for mask in range(1 << m):
        c = [
            weights[k] if mask & (1 << k) else Decimal(0)
            for k in range(m)
        ]
        extended = [Decimal(0), *c, Decimal(0)]
        variation = sum(
            abs(extended[k] - extended[k - 1])
            for k in range(1, len(extended))
        )
        roots = [
            k
            for k in range(m)
            if mask & (1 << k)
            and not (k > 0 and mask & (1 << (k - 1)))
        ]
        declared = 2 * sum(weights[k] for k in roots)
        max_component_error = max(
            max_component_error, abs(variation - declared)
        )
        mass = sum(c)
        min_lower = min(min_lower, variation - low * mass)
        min_upper = min(min_upper, 2 * mass - variation)
    rounding_tolerance = Decimal("1e-70")
    passed = (
        min_neighbor >= -rounding_tolerance
        and min_lower >= -rounding_tolerance
        and min_upper >= -rounding_tolerance
        and max_component_error < rounding_tolerance
    )
    return {
        "id": "actual_exponential_weights_exhaustive_m12",
        "masks_checked": 1 << m,
        "minimum_neighbor_ratio_margin": str(min_neighbor),
        "minimum_lower_bound_margin": str(min_lower),
        "minimum_upper_bound_margin": str(min_upper),
        "maximum_component_identity_error": str(max_component_error),
        "rounding_tolerance": str(rounding_tolerance),
        "decimal_precision": getcontext().prec,
        "pass": passed,
    }


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.([^}]+)\}", body)
    expected = [str(k) for k in range(1, 22)]
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
        "\\gamma_k-\\gamma_{k+1}\\ge\\frac3{35}\\gamma_k",
        "V_\\gamma(A)=2\\sum_{\\nu=1}^{J}\\gamma_{p_\\nu}",
        "\\frac6{35}\\sum_{k\\in A}\\gamma_k",
        "\\frac{24}{35R}\\gamma_k\\vartheta'(z)",
        "absolute-value bound after Abel summation is algebraically sharp",
        "not Navier--Stokes solutions",
        "**PROVED ALGEBRAIC NO-GAIN. NOT CLAY.**",
    )
    forbidden = (
        "the actual R0.74P flux has the exact adjacent-boundary form",
        "signed cancellation proves (Q.1)",
        "global regularity follows",
        "Millennium problem is solved",
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
        "# R0.74S weighted stopped-Abel certificate report",
        "",
        "## Result",
        "",
        f"**{payload['summary']['result']}** — "
        f"{payload['summary']['exact_passed']}/"
        f"{payload['summary']['exact_total']} exact rational checks, "
        f"{payload['summary']['finite_passed']}/"
        f"{payload['summary']['finite_total']} exhaustive finite checks, and "
        f"{payload['summary']['structural_passed']}/"
        f"{payload['summary']['structural_total']} structural checks passed.",
        "",
        "## Exact rational ledger",
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
            "## Exhaustive finite ledgers",
            "",
            "- All 16 binary active sets at \(M=4\) satisfy the exact Abel",
            "  identity, component formula, and saturation identity for",
            "  rational proxy weights.",
            "- All 4096 binary active sets at \(M=12\) satisfy the component",
            "  formula and the \(6/35\)--\(2\) mass comparison for the actual",
            "  exponential weights at 80-decimal precision.",
            "",
            "## Boundary",
            "",
            "The certificate does not prove the analytic exponential",
            "inequality, bind the ideal adjacent model to the R0.74P padded",
            "flux, or certify a Navier--Stokes sign estimate.  It checks",
            "arithmetic, exhaustive finite fixtures, tags, and claim sentinels.",
            "",
            "**FINITE ONLY. NOT CLAY.**",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    body = NOTE.read_text(encoding="utf-8")
    exact_checks = [
        exact(
            "minimum_exponent_gap",
            Fraction(4 - 1, 32),
            Fraction(3, 32),
            "first adjacent exponent difference",
        ),
        exact(
            "rational_ratio_majorant",
            Fraction(1, 1) / (Fraction(1, 1) + Fraction(3, 32)),
            Fraction(32, 35),
            "exponential ratio majorant",
        ),
        exact(
            "relative_gap",
            Fraction(1, 1) - Fraction(32, 35),
            Fraction(3, 35),
            "uniform adjacent relative gap",
        ),
        exact(
            "variation_mass_constant",
            Fraction(2, 1) * Fraction(3, 35),
            Fraction(6, 35),
            "two block endpoints times the gap",
        ),
        exact(
            "geometric_sum",
            Fraction(1, 1) / (Fraction(1, 1) - Fraction(32, 35)),
            Fraction(35, 3),
            "block mass relative to its first weight",
        ),
        exact(
            "collar_derivative_constant",
            Fraction(8, 1) * Fraction(3, 35),
            Fraction(24, 35),
            "R/8 collar derivative times the gap",
        ),
    ]
    finite_checks = [proxy_checks(), actual_weight_checks()]
    structural = structural_checks(body)
    passed = (
        all(item["pass"] for item in exact_checks)
        and all(item["pass"] for item in finite_checks)
        and all(item["pass"] for item in structural)
    )
    payload = {
        "schema": "r074s-weighted-stopped-abel-certificate-v1",
        "scope": "FINITE ONLY: rational constants, binary active sets, exact Abel fixtures, and claim boundaries",
        "note": str(NOTE.relative_to(REPO)),
        "note_sha256": sha256(NOTE),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "claim_boundary": {
            "stopped_abel_identity": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "binary_component_formula": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "coefficient_no_gain": "PROVED_IN_IDEAL_ADJACENT_MODEL",
            "actual_padded_flux_binding": "OPEN",
            "navier_stokes_signed_improvement": "OPEN",
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
