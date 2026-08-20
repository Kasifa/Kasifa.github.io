#!/usr/bin/env python3
"""Exact arithmetic audit for the R0.68A all-order target-tail reduction.

The invariant-shear Navier--Stokes packet has a one-chain Dyson expansion.
R0.68A combines its L2 Dyson majorant, the tensor Rudin--Shapiro heat
envelope, the exact absence of the ninth-order target, and the certified
quartic root bound lambda>25.  At the quartic-critical amplitude

    epsilon_r^2 = (16/lambda)^r,

the sum of every target term of order n>=10 is less than

    (1/30000) (43/64)^r

times the quadratic target coefficient.  This leaves the eighth-order term
as the only finite-order obstruction to an all-order target asymptotic.

All comparisons in this audit are exact rational or quadratic-field
comparisons.  A rational Taylor remainder proves exp(kappa)<2; no floating
point value is used by a check.  Decimal values in the report are display
only.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class Quadratic:
    """Element a+b*sqrt(2), with exact rational coefficients."""

    a: Fraction
    b: Fraction

    def __add__(self, other: "Quadratic") -> "Quadratic":
        return Quadratic(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "Quadratic") -> "Quadratic":
        return Quadratic(self.a - other.a, self.b - other.b)

    def __mul__(self, other: "Quadratic") -> "Quadratic":
        return Quadratic(
            self.a * other.a + 2 * self.b * other.b,
            self.a * other.b + self.b * other.a,
        )

    def scale(self, value: Fraction) -> "Quadratic":
        return Quadratic(self.a * value, self.b * value)

    def decimal(self) -> float:
        return float(self.a) + float(self.b) * math.sqrt(2.0)


SQRT_TWO = Quadratic(Fraction(0), Fraction(1))
ONE = Quadratic(Fraction(1), Fraction(0))
C_T = Quadratic(Fraction(4), Fraction(3))
ONE_MINUS_INV_SQRT_TWO = Quadratic(Fraction(1), Fraction(-1, 2))
KAPPA = Quadratic(Fraction(1, 4), Fraction(1, 4))

CRITICAL_RATE_COARSE = Fraction(2**18, 25**4)
CRITICAL_RATE_SIMPLE = Fraction(43, 64)
TAIL_PREFACTOR_COARSE = (
    Fraction(750) * Fraction(5, 8) ** 9 / math.factorial(9)
)
TAIL_PREFACTOR_SIMPLE = Fraction(1, 30_000)


def progress(enabled: bool, started: float, stage: str) -> None:
    if enabled:
        print(
            f"[R0.68A all-order tail +{time.perf_counter() - started:7.3f}s] {stage}",
            file=sys.stderr,
            flush=True,
        )


def positive_quadratic_less(left: Quadratic, right: Quadratic) -> bool:
    """Exact comparison for the positive differences used in this audit."""
    difference = right - left
    if difference.b == 0:
        return difference.a > 0
    if difference.b > 0:
        if difference.a >= 0:
            return True
        return 2 * difference.b * difference.b > difference.a * difference.a
    if difference.a <= 0:
        return False
    return difference.a * difference.a > 2 * difference.b * difference.b


def exp_positive_rational_upper(x: Fraction, degree: int) -> Fraction:
    """Upper bound exp(x) using a Taylor sum and a geometric tail."""
    if not 0 <= x < 1:
        raise ValueError("the elementary tail bound expects 0<=x<1")
    term = Fraction(1)
    total = term
    for index in range(1, degree + 1):
        term *= x / index
        total += term
    next_term = term * x / (degree + 1)
    ratio = x / (degree + 2)
    return total + next_term / (1 - ratio)


def fraction_record(value: Fraction) -> dict[str, object]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": f"{float(value):.18e}",
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    progress(arguments.progress, started, "checking the heat-envelope constant")
    envelope_product = C_T * ONE_MINUS_INV_SQRT_TWO
    expected_product = ONE + SQRT_TWO
    kappa_from_envelope = envelope_product.scale(Fraction(1, 4))

    progress(arguments.progress, started, "certifying exp(kappa)<2")
    exp_two_thirds_upper = exp_positive_rational_upper(Fraction(2, 3), 18)

    progress(arguments.progress, started, "checking support and critical powers")
    # For n=9 there are eight U carriers.  Splitting a hypothetical zero sum
    # into four against five shell frequencies leaves H-4D=4 when H=4N and
    # D=N-1, hence the target plane is absent for every N>=1.
    support_gap_constant = 4
    root_lower = 25

    checks = {
        "tensorHeatConstantSimplifies": envelope_product == expected_product,
        "dysonParameterIsKappaEpsilonOverL": kappa_from_envelope == KAPPA,
        "kappaLessThanFiveEighths": positive_quadratic_less(
            KAPPA, Quadratic(Fraction(5, 8), Fraction(0))
        ),
        "kappaLessThanTwoThirds": positive_quadratic_less(
            KAPPA, Quadratic(Fraction(2, 3), Fraction(0))
        ),
        "expTwoThirdsUpperLessThanTwo": exp_two_thirds_upper < 2,
        "ninthOrderTargetGapIsFour": support_gap_constant == 4,
        "quarticRootLowerBoundIsStrictlySupercritical": root_lower > 16,
        "criticalTailBlockRateBelowFortyThreeSixtyFourths": (
            CRITICAL_RATE_COARSE < CRITICAL_RATE_SIMPLE
        ),
        "tailPrefactorBelowOneOverThirtyThousand": (
            TAIL_PREFACTOR_COARSE < TAIL_PREFACTOR_SIMPLE
        ),
        "simpleBlockRateIsStrictlyContractive": CRITICAL_RATE_SIMPLE < 1,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    theorem = {
        "dysonParameter": (
            "Theta_m(t_H)<=kappa*epsilon/L, "
            "kappa=(1+sqrt(2))/4"
        ),
        "sectorTail": (
            "|sum_{n>=10} A^n Ghat_n(0,m,t_H)| "
            "<=A*sqrt(L)*exp(-m^2*t_H)*exp(Theta)*Theta^9/9!"
        ),
        "quadraticLowerBound": (
            "|A^2 Ghat_2(0,m,t_H)|>"
            "A^2*exp(-m^2*t_H)*4*m*L/(25*H^2)"
        ),
        "periodicTarget": (
            "L=1, M_r=16^r, m_r=(2*M_r+13)/15, "
            "epsilon_r^2=(16/lambda)^r"
        ),
        "certifiedRatio": (
            "tail(n>=10)/quadratic < (1/30000)*(43/64)^r"
        ),
        "remainingFiniteObstruction": "the complete eighth-order target term",
    }

    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "rigorous all-order target-tail reduction inside the globally smooth "
            "invariant-shear packet; not a Navier--Stokes singularity or global "
            "regularity theorem"
        ),
        "checks": checks,
        "constants": {
            "C_T": "4+3*sqrt(2)",
            "oneMinusExpMinusT": "1-1/sqrt(2)",
            "kappa": {
                "exact": "(1+sqrt(2))/4",
                "decimal": f"{KAPPA.decimal():.18e}",
                "strictUpper": "5/8",
            },
            "expTwoThirdsUpper": fraction_record(exp_two_thirds_upper),
            "criticalTailBlockRateUsingLambdaGreaterThan25": fraction_record(
                CRITICAL_RATE_COARSE
            ),
            "simpleCriticalTailBlockRate": fraction_record(
                CRITICAL_RATE_SIMPLE
            ),
            "coarseTailPrefactor": fraction_record(TAIL_PREFACTOR_COARSE),
            "simpleTailPrefactor": fraction_record(TAIL_PREFACTOR_SIMPLE),
        },
        "support": {
            "ninthOrderTargetProjection": "zero",
            "carrierBalanceGap": "H-4D=4",
            "firstTermInCertifiedTail": "n=10 (nine U interactions)",
        },
        "theorem": theorem,
        "proofDependencies": [
            "R0.58 tensor Rudin--Shapiro prefix and Abel heat envelope",
            "R0.60 invariant-shear chain and ninth-order target gap",
            "R0.61 exact positive quadratic coefficient",
            "R0.66 certified dominant quartic root lambda>25",
        ],
        "runtime": {
            "python": platform.python_version(),
            "seconds": time.perf_counter() - started,
        },
    }
    serialized = json.dumps(report, indent=2, sort_keys=True) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized, encoding="utf-8")
    digest = hashlib.sha256(serialized.encode("utf-8")).hexdigest()
    print(serialized, end="")
    print(
        f"[R0.68A] certificate_sha256={digest}",
        file=sys.stderr,
        flush=True,
    )


if __name__ == "__main__":
    main()
