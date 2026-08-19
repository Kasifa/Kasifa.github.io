#!/usr/bin/env python3
"""R0.51 exploratory affine charge-weight optimization.

For the exact degree-80 center, replace the multiplicative charge character
used in R0.50 by

    omega_s(c, lambda) = c^s (1 + lambda |s|),
    c > 0, lambda >= 0.

The triangle inequality proves omega_{a+b} <= omega_a omega_b, so this is an
algebra weight with constant one.  For every positive input charge s >= 2 the
center has q >= -1 and hence

    omega_{s+q}/omega_s = c^q (1 + alpha_s q),
    alpha_s = lambda/(1 + lambda s).

This script first follows the active-only stationary branch for (j,s)=(81,
162), then solves the candidate active/zero-sector KKT system

    B_162 = 1, Z_0 = 1,
    (d_t B_162)(d_lambda Z_0)
      - (d_lambda B_162)(d_t Z_0) = 0,

where t=log(c).  It scans all finite positive-charge endpoint bounds and the
three exceptional sectors at every reported candidate.

All optimization and comparisons in this file use floating-point arithmetic.
The output is candidate localization only, not an interval certificate or an
all-order proof for the affine family.  Exact certification is a separate
R0.51 obligation.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import gmpy2
import numpy as np
from scipy.optimize import root

import edge_charge_character_optimization_audit as r050
import edge_charge_resolved_audit as r039
import edge_charge_threshold_root_audit as r048
import edge_rational_asymptotic_audit as r028
import edge_short_continuation_audit as r036
import edge_weighted_restart_audit as r037


Rational = gmpy2.mpq
R050_POLYNOMIAL_SHA256 = (
    "056a0adba7f3cba41a6e9bd6d943a8f59be28f50f44c6035df1f68393ed26be7"
)


def progress(started: float, stage: str, **details: object) -> None:
    suffix = "" if not details else " " + json.dumps(details, sort_keys=True)
    print(
        f"[R0.51 explore +{time.perf_counter() - started:8.2f}s] {stage}{suffix}",
        file=sys.stderr,
        flush=True,
    )


def to_float(value: Rational) -> float:
    return float(int(value.numerator)) / float(int(value.denominator))


def alpha(input_charge: int, lam: float) -> float:
    return lam / (1.0 + lam * input_charge)


def alpha_derivative(input_charge: int, lam: float) -> float:
    return 1.0 / (1.0 + lam * input_charge) ** 2


def weight_ratio(input_charge: int, center_charge: np.ndarray, lam: float) -> np.ndarray:
    output_charge = input_charge + center_charge
    return (1.0 + lam * np.abs(output_charge)) / (
        1.0 + lam * abs(input_charge)
    )


class Explorer:
    def __init__(
        self,
        terms: list[tuple[int, int, Rational]],
        active_terms: list[tuple[int, int, Rational]],
        maximum_degree: int,
        positive_charge_cutoff: int,
    ) -> None:
        self.maximum_degree = maximum_degree
        self.positive_charge_cutoff = positive_charge_cutoff
        self.degree = np.asarray([int(item[0]) for item in terms], dtype=np.int64)
        self.charge = np.asarray([int(item[1]) for item in terms], dtype=np.int64)
        self.coefficient = np.asarray(
            [to_float(item[2]) for item in terms], dtype=np.float64
        )
        self.active_degree = np.asarray(
            [int(item[0]) for item in active_terms], dtype=np.int64
        )
        self.active_charge = np.asarray(
            [int(item[1]) for item in active_terms], dtype=np.int64
        )
        self.active_coefficient = np.asarray(
            [to_float(item[2]) for item in active_terms], dtype=np.float64
        )

    def center_scale(self, log_r: float, log_c: float) -> np.ndarray:
        return self.coefficient * np.exp(
            self.degree * log_r + self.charge * log_c
        )

    def active_moments(
        self, log_r: float, log_c: float, maximum_charge_power: int = 2
    ) -> list[float]:
        scaled = self.active_coefficient * np.exp(
            self.active_degree * log_r + self.active_charge * log_c
        )
        return [
            float(np.sum(scaled * self.active_charge**power))
            for power in range(maximum_charge_power + 1)
        ]

    def active_value_and_derivatives(
        self, log_r: float, log_c: float, lam: float
    ) -> dict[str, float]:
        moments = self.active_moments(log_r, log_c, 2)
        a = alpha(162, lam)
        da = alpha_derivative(162, lam)
        return {
            "value": moments[0] + a * moments[1],
            "logC": moments[1] + a * moments[2],
            "lambda": da * moments[1],
            "M0": moments[0],
            "M1": moments[1],
            "M2": moments[2],
        }

    def zero_value_and_derivatives(
        self, log_r: float, log_c: float, lam: float
    ) -> dict[str, float]:
        minimum_degree = int(r039.minimum_tail_degree(0, self.maximum_degree))
        scaled = self.center_scale(log_r, log_c)
        nonzero = self.charge != 0
        base = np.zeros_like(scaled)
        base[nonzero] = (
            scaled[nonzero]
            * (self.degree[nonzero] + minimum_degree)
            / (self.degree[nonzero] + minimum_degree - 1)
            * np.abs(self.charge[nonzero])
            / 3.0
        )
        charge_abs = np.abs(self.charge)
        affine = 1.0 + lam * charge_abs
        return {
            "value": float(np.sum(base * affine)),
            "logC": float(np.sum(base * affine * self.charge)),
            "lambda": float(np.sum(base * charge_abs)),
        }

    def positive_endpoint_values(
        self, input_charge: int, log_r: float, log_c: float, lam: float
    ) -> tuple[float, float, int]:
        """All-degree convex endpoint bounds for one fixed s>=2."""

        s = int(input_charge)
        minimum_degree = int(
            r039.minimum_tail_degree(s, self.maximum_degree)
        )
        maximum_slope = s / minimum_degree
        scaled = self.center_scale(log_r, log_c)
        degree_factor = (
            self.degree + minimum_degree
        ) / (self.degree + minimum_degree - 1)
        charge_factor = np.abs(s - self.charge) / (
            3.0 * np.abs(s + self.charge)
        )
        common = scaled * degree_factor * charge_factor
        affine = 1.0 + alpha(s, lam) * self.charge
        infinity = float(np.sum(common * np.abs(self.charge) * affine))
        minimum = float(
            np.sum(
                common
                * np.abs(self.degree * maximum_slope - self.charge)
                * affine
            )
        )
        return infinity, minimum, minimum_degree

    def direct_column(
        self,
        input_degree: int,
        input_charge: int,
        log_r: float,
        log_c: float,
        lam: float,
    ) -> float:
        j = int(input_degree)
        s = int(input_charge)
        factors = np.asarray(
            [
                to_float(
                    Rational(int(d) + j, j)
                    * abs(
                        r039.monomial_derivative_coefficient(
                            int(d), int(q), j, s
                        )
                    )
                )
                for d, q in zip(self.degree, self.charge, strict=True)
            ],
            dtype=np.float64,
        )
        return float(
            np.sum(
                self.center_scale(log_r, log_c)
                * factors
                * weight_ratio(s, self.charge, lam)
            )
        )

    def plus_one_bound(self, log_r: float, log_c: float, lam: float) -> float:
        minimum_degree = int(
            r039.minimum_tail_degree(1, self.maximum_degree)
        )
        factors = np.asarray(
            [
                to_float(
                    r039.finite_charge_factor(
                        int(d), int(q), 1, minimum_degree
                    )
                )
                for d, q in zip(self.degree, self.charge, strict=True)
            ],
            dtype=np.float64,
        )
        return float(
            np.sum(
                self.center_scale(log_r, log_c)
                * factors
                * weight_ratio(1, self.charge, lam)
            )
        )

    def sector_scan(
        self, log_r: float, log_c: float, lam: float
    ) -> dict[str, object]:
        records: list[tuple[str, float, str]] = []
        active = self.active_value_and_derivatives(log_r, log_c, lam)["value"]
        records.append(("s=162,j=81", active, "active exact column"))
        for s in range(2, self.positive_charge_cutoff + 1):
            infinity, minimum, degree_floor = self.positive_endpoint_values(
                s, log_r, log_c, lam
            )
            records.append((f"s={s},x=0", infinity, "fixed-charge endpoint"))
            records.append(
                (
                    f"s={s},j={degree_floor}",
                    minimum,
                    "fixed-charge endpoint",
                )
            )
        zero = self.zero_value_and_derivatives(log_r, log_c, lam)["value"]
        records.append(("s=0", zero, "exact all-degree endpoint"))
        plus = self.plus_one_bound(log_r, log_c, lam)
        records.append(("s=1", plus, "termwise all-degree bound"))
        minus_degree = int(
            r039.minimum_tail_degree(-1, self.maximum_degree)
        )
        minus = self.direct_column(
            minus_degree, -1, log_r, log_c, lam
        )
        records.append(
            (f"s=-1,j={minus_degree}", minus, "minimum-degree candidate")
        )
        ordered = sorted(records, key=lambda item: item[1], reverse=True)
        return {
            "maximum": {
                "label": ordered[0][0],
                "value": ordered[0][1],
                "classification": ordered[0][2],
            },
            "top": [
                {"label": label, "value": value, "classification": kind}
                for label, value, kind in ordered[:12]
            ],
            "recordsScanned": len(records),
            "positiveChargeCutoffInclusive": self.positive_charge_cutoff,
            "largeChargeAllOrderCertified": False,
            "minusOneAllDegreeCertified": False,
        }


def solve_active_branch(
    explorer: Explorer,
    lam: float,
    initial_log_r: float,
    initial_log_c: float,
) -> tuple[float, float, dict[str, object]]:
    def equations(x: np.ndarray) -> np.ndarray:
        values = explorer.active_value_and_derivatives(x[0], x[1], lam)
        return np.asarray([values["value"] - 1.0, values["logC"]])

    solution = root(equations, np.asarray([initial_log_r, initial_log_c]))
    residual = equations(solution.x)
    if not solution.success or np.max(np.abs(residual)) > 5e-10:
        raise RuntimeError(
            f"active branch solve failed at lambda={lam}: "
            f"{solution.message}; residual={residual}"
        )
    log_r, log_c = (float(solution.x[0]), float(solution.x[1]))
    return log_r, log_c, {
        "success": True,
        "functionEvaluations": int(solution.nfev),
        "maximumAbsoluteResidual": float(np.max(np.abs(residual))),
    }


def solve_active_zero_kkt(
    explorer: Explorer,
    initial_log_r: float,
    initial_log_c: float,
    initial_log_lambda: float,
) -> tuple[float, float, float, dict[str, object]]:
    def equations(x: np.ndarray) -> np.ndarray:
        log_r, log_c, log_lambda = x
        lam = float(np.exp(log_lambda))
        active = explorer.active_value_and_derivatives(log_r, log_c, lam)
        zero = explorer.zero_value_and_derivatives(log_r, log_c, lam)
        kkt = (
            active["logC"] * zero["lambda"]
            - active["lambda"] * zero["logC"]
        )
        return np.asarray([active["value"] - 1.0, zero["value"] - 1.0, kkt])

    solution = root(
        equations,
        np.asarray([initial_log_r, initial_log_c, initial_log_lambda]),
    )
    residual = equations(solution.x)
    if not solution.success or np.max(np.abs(residual)) > 5e-9:
        raise RuntimeError(
            "active/zero KKT solve failed: "
            f"{solution.message}; residual={residual}"
        )
    log_r, log_c, log_lambda = (float(value) for value in solution.x)
    return log_r, log_c, float(np.exp(log_lambda)), {
        "success": True,
        "functionEvaluations": int(solution.nfev),
        "maximumAbsoluteResidual": float(np.max(np.abs(residual))),
        "equations": [
            "B_162-1=0",
            "Z_0-1=0",
            "(d_t B_162)(d_lambda Z_0)-(d_lambda B_162)(d_t Z_0)=0",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-total-degree", type=int, default=80)
    parser.add_argument("--positive-charge-cutoff", type=int, default=500)
    parser.add_argument(
        "--lambda-grid",
        default="0,0.001,0.01,0.03,0.1,0.2,0.4,0.6,0.8,1.0",
    )
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    if arguments.max_total_degree != 80:
        raise SystemExit("R0.51 exploration is pinned to degree 80")
    if arguments.positive_charge_cutoff < 241:
        raise SystemExit("--positive-charge-cutoff must be at least 241")

    started = time.perf_counter()
    progress(started, "constructing exact degree-80 center")
    active_field, _, _, recurrence_interactions = r028.rational_edge_recurrence(
        arguments.max_total_degree, True, started
    )
    polynomial = r036.field_to_polynomial(
        active_field, arguments.max_total_degree
    )
    polynomial_digest = r037.polynomial_digest(polynomial)
    if polynomial_digest != R050_POLYNOMIAL_SHA256:
        raise AssertionError("degree-80 polynomial digest changed")
    terms = r048.independent_terms(polynomial)
    active_terms = r050.active_laurent_terms(terms, 81, 162)
    explorer = Explorer(
        terms,
        active_terms,
        arguments.max_total_degree,
        arguments.positive_charge_cutoff,
    )
    progress(
        started,
        "formed affine column evaluator",
        centerTerms=len(terms),
        activeTerms=len(active_terms),
        chargeMinimum=min(item[1] for item in terms),
        chargeMaximum=max(item[1] for item in terms),
    )

    lambda_grid = [
        float(item.strip())
        for item in arguments.lambda_grid.split(",")
        if item.strip()
    ]
    if not lambda_grid or min(lambda_grid) < 0:
        raise SystemExit("--lambda-grid must contain nonnegative values")

    log_r = float(np.log(0.3826198137095655))
    log_c = float(np.log(0.80245638275))
    branch = []
    crossing_seed: tuple[float, float, float] | None = None
    previous_zero = None
    previous_point = None
    for lam in lambda_grid:
        log_r, log_c, solver = solve_active_branch(
            explorer, lam, log_r, log_c
        )
        scan = explorer.sector_scan(log_r, log_c, lam)
        zero = explorer.zero_value_and_derivatives(log_r, log_c, lam)["value"]
        branch.append(
            {
                "lambda": lam,
                "alpha162": alpha(162, lam),
                "r": float(np.exp(log_r)),
                "c": float(np.exp(log_c)),
                "zeroSectorValue": zero,
                "solver": solver,
                "sectorScan": scan,
            }
        )
        progress(
            started,
            "active-only branch point",
            lambdaValue=lam,
            radius=float(np.exp(log_r)),
            character=float(np.exp(log_c)),
            zeroSector=zero,
            maximumSector=scan["maximum"]["label"],
            maximumValue=scan["maximum"]["value"],
        )
        if (
            previous_zero is not None
            and previous_zero < 1.0 <= zero
            and previous_point is not None
        ):
            crossing_seed = (
                0.5 * (previous_point[0] + log_r),
                0.5 * (previous_point[1] + log_c),
                max(1e-9, 0.5 * (previous_point[2] + lam)),
            )
        previous_zero = zero
        previous_point = (log_r, log_c, lam)

    if crossing_seed is None:
        closest = min(branch, key=lambda item: abs(item["zeroSectorValue"] - 1.0))
        crossing_seed = (
            float(np.log(closest["r"])),
            float(np.log(closest["c"])),
            max(1e-9, float(closest["lambda"])),
        )
    progress(started, "solving active/zero KKT candidate")
    kkt_log_r, kkt_log_c, kkt_lambda, kkt_solver = solve_active_zero_kkt(
        explorer,
        crossing_seed[0],
        crossing_seed[1],
        float(np.log(crossing_seed[2])),
    )
    kkt_scan = explorer.sector_scan(
        kkt_log_r, kkt_log_c, kkt_lambda
    )
    kkt_active = explorer.active_value_and_derivatives(
        kkt_log_r, kkt_log_c, kkt_lambda
    )
    kkt_zero = explorer.zero_value_and_derivatives(
        kkt_log_r, kkt_log_c, kkt_lambda
    )
    progress(
        started,
        "candidate localized",
        radius=float(np.exp(kkt_log_r)),
        character=float(np.exp(kkt_log_c)),
        lambdaValue=kkt_lambda,
        maximumSector=kkt_scan["maximum"]["label"],
        maximumValue=kkt_scan["maximum"]["value"],
    )

    source_digest = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    payload = {
        "schemaVersion": "0.1-exploratory",
        "classification": (
            "floating-point candidate localization; not an interval proof "
            "and not an all-order affine-weight certificate"
        ),
        "createdAtUtc": datetime.now(timezone.utc).isoformat(),
        "weight": {
            "formula": "omega_s(c,lambda)=c^s(1+lambda*|s|)",
            "domain": "c>0, lambda>=0",
            "submultiplicativity": (
                "1+lambda|a+b| <= (1+lambda|a|)(1+lambda|b|)"
            ),
            "positiveChargeCompression": (
                "B_s=A_s+alpha_s*d_t A_s, "
                "alpha_s=lambda/(1+lambda*s), s>=2"
            ),
        },
        "finiteConstruction": {
            "maximumTotalDegree": arguments.max_total_degree,
            "centerTerms": len(terms),
            "activeTerms": len(active_terms),
            "recurrenceOrderedInteractions": recurrence_interactions,
            "degreeEightyPolynomialSha256": polynomial_digest,
            "sourceSha256": source_digest,
        },
        "activeOnlyBranch": branch,
        "activeZeroKktCandidate": {
            "r": float(np.exp(kkt_log_r)),
            "c": float(np.exp(kkt_log_c)),
            "lambda": kkt_lambda,
            "alpha162": alpha(162, kkt_lambda),
            "active": kkt_active,
            "zero": kkt_zero,
            "solver": kkt_solver,
            "sectorScan": kkt_scan,
        },
        "remainingExactObligations": [
            "isolate the active/zero KKT solution in a rational box",
            "prove the KKT candidate is the global max-min optimum",
            "certify both active constraints and every inactive sector uniformly",
            "extend the affine positive-charge bounds to all s beyond the finite list",
            "reprove the s=-1 all-degree endpoint under the affine charge weight",
            "separate the exact degree-80 center from every all-order tail claim",
        ],
        "computation": {
            "floatingPoint": "numpy float64 / scipy root",
            "randomness": False,
            "gpu": False,
            "wallSeconds": time.perf_counter() - started,
        },
    }
    rendered = json.dumps(payload, indent=2, sort_keys=True)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
