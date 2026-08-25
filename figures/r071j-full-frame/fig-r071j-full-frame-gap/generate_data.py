#!/usr/bin/env python3
"""Generate closed-form source data for the R0.71J full-frame figure."""

from __future__ import annotations

import argparse
import csv
import json
import math
import platform
import time
from pathlib import Path


FIELDNAMES = (
    "panel",
    "series",
    "x",
    "value",
    "category",
    "auxiliary",
    "parameter",
    "evidenceClass",
    "formula",
)


def add(
    rows: list[dict[str, str]],
    panel: str,
    series: str,
    x: float,
    value: float,
    category: str,
    auxiliary: str,
    parameter: str,
    evidence: str,
    formula: str,
) -> None:
    rows.append(
        {
            "panel": panel,
            "series": series,
            "x": f"{x:.17g}",
            "value": f"{value:.17g}",
            "category": category,
            "auxiliary": auxiliary,
            "parameter": parameter,
            "evidenceClass": evidence,
            "formula": formula,
        }
    )


def profiles(theta: float) -> tuple[float, float, float, float, float, float]:
    """Return B0, D0, Y0, F0^2, A0, and dA0/dtheta."""

    exponential = lambda power: math.exp(-power * theta)
    b_zero = 4.0 * (exponential(34.0) - exponential(52.0))
    d_zero = (
        32.0 * exponential(32.0)
        + 1156.0 * exponential(34.0)
        + 50.0 * exponential(50.0)
        + 2704.0 * exponential(52.0)
    )
    y_zero = (
        2.0 * exponential(2.0)
        + 2.0 * exponential(32.0)
        + 68.0 * exponential(34.0)
        + 2.0 * exponential(50.0)
        + 104.0 * exponential(52.0)
    )
    f_zero_square = (
        4.0 * exponential(34.0)
        + 192.0 * exponential(36.0)
        + 4.0 * exponential(52.0)
        + 300.0 * exponential(54.0)
    )
    if b_zero == 0.0:
        return b_zero, d_zero, y_zero, f_zero_square, 0.0, 0.0
    b_prime = 4.0 * (-34.0 * exponential(34.0) + 52.0 * exponential(52.0))
    d_prime = -(
        32.0 * 32.0 * exponential(32.0)
        + 34.0 * 1156.0 * exponential(34.0)
        + 50.0 * 50.0 * exponential(50.0)
        + 52.0 * 2704.0 * exponential(52.0)
    )
    y_prime = -(
        2.0 * 2.0 * exponential(2.0)
        + 32.0 * 2.0 * exponential(32.0)
        + 34.0 * 68.0 * exponential(34.0)
        + 50.0 * 2.0 * exponential(50.0)
        + 52.0 * 104.0 * exponential(52.0)
    )
    a_zero = b_zero * b_zero / (d_zero * y_zero)
    a_prime = a_zero * (
        2.0 * b_prime / b_zero - d_prime / d_zero - y_prime / y_zero
    )
    return b_zero, d_zero, y_zero, f_zero_square, a_zero, a_prime


def exact_a_star() -> float:
    ninth_root_two = 2.0 ** (1.0 / 9.0)
    return 4.0 / (
        57.0
        * (ninth_root_two + 44.0)
        * (3.0 * ninth_root_two + 4.0 * 2.0 ** (7.0 / 9.0) + 120.0)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data.csv"))
    parser.add_argument("--metadata", type=Path, default=Path("figure-data-metadata.json"))
    args = parser.parse_args()
    started = time.perf_counter()
    rows: list[dict[str, str]] = []

    theta_star = math.log(2.0) / 18.0
    b_star, d_star, y_star, _, a_star_profile, a_prime_star = profiles(theta_star)
    a_star = exact_a_star()
    source_star = 0.5 * (a_prime_star + 32.0 * a_star_profile)
    positive_source = max(source_star, 0.0)
    negative_source = max(-source_star, 0.0)
    identity_parameter = "theta*=log(2)/18;kappa=4K;theta=nu*K^2*t"
    identity_evidence = (
        "pointwise instance of exact positive-defect identity for the selected "
        "parent shell in the closed-form 2D3C heat limit"
    )
    for series, value, category, formula in (
        ("positiveCreation", 2.0 * positive_source, "left side", "2*s_plus"),
        ("timeDerivative", a_prime_star, "right-side component", "dA0/dtheta"),
        ("viscousMass", 32.0 * a_star_profile, "right-side component", "32*A0"),
        ("negativeDefect", 2.0 * negative_source, "right-side component", "2*s_minus"),
    ):
        add(
            rows,
            "A",
            series,
            theta_star,
            value,
            category,
            f"A*={a_star:.17g};B*={b_star:.17g};D*={d_star:.17g};Y*={y_star:.17g}",
            identity_parameter,
            identity_evidence,
            formula,
        )

    b_normalizer = b_star
    d_normalizer = 3942.0
    y_normalizer = 178.0
    profile_parameter = (
        "theta=nu*K^2*t;global cell chi=1;parent index j=J+2;kappa=4K"
    )
    profile_evidence = (
        "closed-form fixed-window heat limit of an exact global-smooth 2D3C NSE family"
    )
    for index in range(201):
        theta = 0.4 * index / 200.0
        b_zero, d_zero, y_zero, _, a_zero, _ = profiles(theta)
        for series, value, auxiliary, formula in (
            ("Bnormalized", b_zero / b_normalizer, "normalizer=B0(theta*)", "B0/B0(theta*)"),
            ("Dnormalized", d_zero / d_normalizer, "normalizer=D0(0)=3942", "D0/3942"),
            ("Ynormalized", y_zero / y_normalizer, "normalizer=Y0(0)=178", "Y0/178"),
            ("anormalized", a_zero / a_star, "normalizer=A*=A0(theta*)", "A0/A*"),
        ):
            add(
                rows,
                "B",
                series,
                theta,
                value,
                "normalized profile",
                auxiliary,
                profile_parameter,
                profile_evidence,
                formula,
            )

    gap_constant = 1.0 - 2.0 ** (-1.0 / 9.0)
    ratio_constant = a_star / (32.0 * gap_constant)
    bound_parameter = (
        "nu=1;K dyadic;Z_lower=A*/(64*K^2);"
        "H_upper=(1-2^(-1/9))/(2*K^4)"
    )
    bound_evidence = (
        "algebraic asymptotic comparison bounds; Z lower bound is asserted only "
        "for sufficiently large dyadic K with no quantified K0"
    )
    for exponent in range(3, 14):
        frequency = float(2**exponent)
        z_lower = a_star / (64.0 * frequency**2)
        h_upper = gap_constant / (2.0 * frequency**4)
        for series, value, formula in (
            ("Zlower", z_lower, "A*/(64*K^2)"),
            ("Hupper", h_upper, "(1-2^(-1/9))/(2*K^4);nu=1"),
            ("ratioOverK2", z_lower / h_upper / frequency**2, "A*/(32*(1-2^(-1/9)))"),
        ):
            add(
                rows,
                "C",
                series,
                frequency,
                value,
                "dyadic reference point",
                f"ratioConstant={ratio_constant:.17g}",
                bound_parameter,
                bound_evidence,
                formula,
            )

    ledger_parameter = "initial time;horizontal groups abs(m)=0,1,2;vertical channels n=4,5"
    ledger_evidence = "exact Fourier group ledger for the global-smooth 2D3C datum"
    ledger = {
        0: {"Bgroup": 36.0, "F2group": 328.0, "dgroup": 82.0},
        1: {"Bgroup": -36.0, "F2group": 8.0, "dgroup": 3860.0},
        2: {"Bgroup": 0.0, "F2group": 164.0, "dgroup": 0.0},
    }
    for group, values in ledger.items():
        for series, value in values.items():
            formula = {
                "Bgroup": "sum Re(conj(Fhat)*Chat) in horizontal group",
                "F2group": "sum |Fhat|^2 in horizontal group",
                "dgroup": "sum |Chat|^2 in horizontal group",
            }[series]
            add(
                rows,
                "D",
                series,
                float(group),
                value,
                f"|m|={group}",
                "units after factoring the displayed K powers",
                ledger_parameter,
                ledger_evidence,
                formula,
            )

    support_parameter = (
        "parent j=J+2;flat top m(log2(|xi|)-j)=1 on normalized radius [1,sqrt(2)]"
    )
    support_evidence = "exact radius check for every listed initial Lamb mode"
    for group in (0, 1, 2):
        for channel in (4, 5):
            radius = math.sqrt(float(group * group + channel * channel)) / 4.0
            add(
                rows,
                "D",
                "frameRadius",
                float(group),
                radius,
                f"n={channel}",
                f"mode=(|m|,|n|)=({group},{channel})",
                support_parameter,
                support_evidence,
                "sqrt(m^2+n^2)/4",
            )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    metadata = {
        "release": "R0.71J",
        "status": "generated",
        "rows": len(rows),
        "method": "closed-form formula evaluation only",
        "randomSeed": None,
        "dns": False,
        "pdeTimeStepping": False,
        "fittedData": False,
        "parameters": {
            "panelA": {
                "thetaStar": "log(2)/18",
                "terms": 4,
                "dimensionlessIdentity": "2*s_plus=A0_theta+32*A0+2*s_minus",
            },
            "panelB": {"thetaRange": [0.0, 0.4], "samplesPerProfile": 201},
            "panelC": {
                "viscosity": 1.0,
                "dyadicFrequencies": [2**i for i in range(3, 14)],
                "lowerBoundThreshold": "sufficiently large K; K0 not quantified",
            },
            "panelD": {
                "horizontalGroups": [0, 1, 2],
                "verticalChannels": [4, 5],
                "parentFlatTopNormalizedRadius": [1.0, "sqrt(2)"],
            },
        },
        "exactConstants": {
            "kineticEnergy": "2041/200",
            "initialYOverK2": 178,
            "initialF2OverK2": 500,
            "initialDOverK4": 3942,
            "initialBOverK3": 0,
            "AStar": a_star,
            "thetaStar": theta_star,
            "ratioOverK2Nu1": ratio_constant,
        },
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "wallSeconds": time.perf_counter() - started,
        "claimBoundary": (
            "Parent-only broad dyadic frame from R0.71E section 10.1, global cell "
            "chi=1, and heat height zero. The curves are exact formula evaluations "
            "or asymptotic comparison bounds, not DNS or finite-K trajectories. No "
            "matched-cell, child-refinement, face-paid BV, regularity, singularity, "
            "originality, or Millennium-problem claim is made."
        ),
    }
    args.metadata.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
