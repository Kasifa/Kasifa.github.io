#!/usr/bin/env python3
"""Finite certificate for the R0.74S actual padded-collar decomposition."""

from __future__ import annotations

import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
NOTE = REPO / "research/r074s_actual_collar_signed_decomposition.md"
JSON_OUT = REPO / "research/r074s_actual_collar_decomposition_certificate.json"
REPORT_OUT = REPO / "research/r074s_actual_collar_decomposition_certificate_report.md"


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


def interval_checks() -> dict:
    """Check pairwise separation of all model collars through m=12."""
    delta = Fraction(1, 8)
    intervals = []
    for m in range(1, 13):
        radius = Fraction(2**m)
        intervals.append((radius - delta, radius, f"{m}-"))
        intervals.append((radius, radius + delta, f"{m}+"))
    overlap_pairs = []
    for i, (a, b, label_a) in enumerate(intervals):
        for c, d, label_b in intervals[i + 1 :]:
            if max(a, c) < min(b, d):
                overlap_pairs.append([label_a, label_b])
    return {
        "id": "lifted_collar_intervals_m1_to_m12",
        "interval_count": len(intervals),
        "overlap_pairs": overlap_pairs,
        "pass": not overlap_pairs,
    }


def block_decomposition_checks() -> dict:
    """Exhaust direct shell and four-channel block sums for M=6."""
    mmax = 6
    weights = [Fraction(32, 35) ** k for k in range(mmax)]
    jminus = [
        Fraction(3, 5),
        Fraction(-7, 11),
        Fraction(5, 13),
        Fraction(17, 19),
        Fraction(-2, 7),
        Fraction(11, 23),
    ]
    jplus = [
        Fraction(13, 17),
        Fraction(-5, 9),
        Fraction(7, 15),
        Fraction(-3, 8),
        Fraction(19, 21),
        Fraction(-11, 25),
        Fraction(2, 3),
    ]
    direct_ok = True
    internal_ok = True
    checked = 0
    for mask in range(1 << mmax):
        active = [k for k in range(mmax) if mask & (1 << k)]
        direct = sum(
            weights[k] * (jminus[k] - jplus[k + 1]) for k in active
        )
        blocks = []
        k = 0
        while k < mmax:
            if not mask & (1 << k):
                k += 1
                continue
            p = k
            while k + 1 < mmax and mask & (1 << (k + 1)):
                k += 1
            blocks.append((p, k))
            k += 1

        root = sum(weights[p] * jminus[p] for p, _ in blocks)
        outer = sum(weights[q] * jplus[q + 1] for _, q in blocks)
        gap = Fraction(0)
        mismatch = Fraction(0)
        internal_direct = Fraction(0)
        for p, q in blocks:
            for m in range(p + 1, q + 1):
                internal_direct += (
                    weights[m] * jminus[m]
                    - weights[m - 1] * jplus[m]
                )
                gap -= (weights[m - 1] - weights[m]) * jplus[m]
                mismatch += weights[m] * (jminus[m] - jplus[m])
        direct_ok &= direct == root - outer + gap + mismatch
        internal_ok &= internal_direct == gap + mismatch
        checked += 1
    return {
        "id": "exhaustive_four_channel_decomposition_m6",
        "masks_checked": checked,
        "direct_block_identity_pass": direct_ok,
        "internal_pair_identity_pass": internal_ok,
        "pass": direct_ok and internal_ok,
    }


def structural_checks(body: str) -> list[dict]:
    tags = re.findall(r"\\tag\{S\.([^}]+)\}", body)
    expected = [str(k) for k in range(39, 60)]
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
        "C_m^-:=\\{r_m-\\delta<|y|<r_m\\}",
        "C_m^+:=\\{r_m<|y|<r_m+\\delta\\}",
        "\\left|\\sum_{k\\in A}\\gamma_k\\nabla\\psi_k^R(y)\\right|",
        "=J_{k,R}^-(t)-J_{k+1,R}^+(t)",
        "\\mathcal R_R(t)-\\mathcal L_R(t)",
        "\\mathcal G_R(t)+\\mathcal M_R(t)",
        "\\gamma_m(J_{m,R}^--J_{m,R}^+)",
        "\\mathcal W_{\\rm kin}+\\mathcal W_{\\rm pr}+\\mathcal W_{\\rm drift}",
        "\\mathcal C_R^{\\rm kin}",
        "\\le CP_R^M",
        "functional \\(L^1\\) witness, not a Navier--Stokes work density",
        "The bridge remains **OPEN**",
        "**NOT CLAY.**",
    )
    forbidden = (
        "adjacent padded gradients cancel pointwise",
        "L1 continuity proves the collar bridge",
        "the four positive channels are bounded by A_R",
        "global regularity is proved",
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
        "# R0.74S actual-collar decomposition certificate report",
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
            "- The 24 open radial collars through index 12 have no positive",
            "  length overlap after setting \(R=1\).",
            "- All 64 active-shell masks at \(M=6\) satisfy the exact direct",
            "  shell sum, four-channel block decomposition, and internal",
            "  weight-drop plus bridge-mismatch identity.",
            "",
            "## Boundary",
            "",
            "The certificate does not prove the analytic cutoff derivative,",
            "unfolding, a uniform PDE collar bridge, or a signed depletion",
            "estimate.  It checks rational geometry, finite algebra, tags,",
            "and fail-closed claim sentinels.",
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
            "collar_width",
            Fraction(1, 8),
            Fraction(1, 8),
            "delta/R",
        ),
        exact(
            "two_collar_widths",
            2 * Fraction(1, 8),
            Fraction(1, 4),
            "total two-sided thickness",
        ),
        exact(
            "minimum_boundary_spacing",
            Fraction(2, 1),
            Fraction(2, 1),
            "r_2-r_1 in units of R",
        ),
        exact(
            "minimum_gap_after_collars",
            Fraction(2, 1) - Fraction(1, 4),
            Fraction(7, 4),
            "positive separation of successive collar pairs",
        ),
        exact(
            "derivative_scale",
            Fraction(1, 1) / Fraction(1, 8),
            Fraction(8, 1),
            "inverse collar width in units of R",
        ),
        exact(
            "weight_gap_constant",
            Fraction(1, 1) - Fraction(32, 35),
            Fraction(3, 35),
            "inherited adjacent relative gap",
        ),
    ]
    finite_checks = [interval_checks(), block_decomposition_checks()]
    structural = structural_checks(body)
    passed = (
        all(item["pass"] for item in exact_checks)
        and all(item["pass"] for item in finite_checks)
        and all(item["pass"] for item in structural)
    )
    payload = {
        "schema": "r074s-actual-collar-decomposition-certificate-v1",
        "scope": "FINITE ONLY: collar geometry, block algebra, tags, and claim boundaries",
        "note": str(NOTE.relative_to(REPO)),
        "note_sha256": sha256(NOTE),
        "exact_checks": exact_checks,
        "finite_checks": finite_checks,
        "structural_checks": structural,
        "claim_boundary": {
            "padded_gradient_support_disjointness": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "four_channel_decomposition": "PROVED_ANALYTICALLY_NOT_BY_CERTIFICATE",
            "l1_bridge_no_go": "PROVED_FUNCTIONAL_ONLY",
            "navier_stokes_collar_bridge": "OPEN",
            "signed_depletion": "OPEN",
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
