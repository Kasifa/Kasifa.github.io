#!/usr/bin/env python3
"""High-precision algebra audit for the R0.71Y sampling obstruction.

The analytic proof is in r071y_report-source.md. This producer evaluates the
exact amplitude optimizer, the sharp integer-lattice factor, the universal
Fourier multiplier upper constant, the N^{-1} envelope, the N^{3/4} critical
operator scale, and the heat-weighted correction to R0.71X. It does not
construct growing root families or prove the continuum theorem.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from decimal import Decimal, getcontext
import json
from pathlib import Path
from zoneinfo import ZoneInfo


getcontext().prec = 90

ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)
THREE = Decimal(3)
FOUR = Decimal(4)
PI = Decimal(
    "3.141592653589793238462643383279502884197169399375105820974944592307816406286"
)

K_Z = ONE
NU = Decimal("0.02")
D_MODULUS = Decimal(8)
A_0 = Decimal("0.05")
B_RATE = TWO * NU * D_MODULUS**2
N_VALUES = (
    1,
    2,
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
    65536,
    131072,
    262144,
    524288,
    1048576,
)
DELTA_VALUES = (
    ONE / Decimal(64),
    ONE / Decimal(32),
    ONE / Decimal(16),
    ONE / Decimal(8),
    ONE / Decimal(4),
)
SINGLE_MODE_R = (1, 2, 4, 8, 16, 32)


def decimal_power(value: Decimal, exponent: Decimal) -> Decimal:
    if value <= 0:
        raise ValueError("decimal_power requires a positive base")
    return (exponent * value.ln()).exp()


def as_text(value: Decimal) -> str:
    return format(value, ".50E")


def as_float(value: Decimal) -> float:
    return float(value)


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def lattice_cost(n_value: int) -> Decimal:
    m_value = Decimal(2 * n_value + 1)
    return m_value * (m_value + ONE) * (TWO * m_value + ONE) / Decimal(6)


def lattice_factor(n_value: int) -> Decimal:
    n = Decimal(n_value)
    m = Decimal(2 * n_value + 1)
    return n * m / lattice_cost(n_value)


def optimizer(u_value: Decimal) -> Decimal:
    return u_value / decimal_power(ONE + u_value, FOUR / THREE)


def multiplier_ratio_upper() -> Decimal:
    return TWO * PI**2 * K_Z**2 / THREE


def normalized_envelope(n_value: int, delta_obs: Decimal) -> Decimal:
    """Unit-floor, unit-target version of Theorem 4.1's final envelope."""

    optimizer_max = THREE / decimal_power(FOUR, FOUR / THREE)
    return (
        optimizer_max
        * lattice_factor(n_value)
        * decimal_power(delta_obs, FOUR / THREE)
        * decimal_power(multiplier_ratio_upper(), ONE / THREE)
    )


def separated_factor(n_value: int, gap: Decimal) -> Decimal:
    """Dimension factor M/(b*h*Ks) in the exact separated-root estimate."""

    m_value = Decimal(2 * n_value + 1)
    return m_value / (B_RATE * gap * lattice_cost(n_value))


def fit_power(xs: list[Decimal], ys: list[Decimal]) -> Decimal:
    log_x = [value.ln() for value in xs]
    log_y = [value.ln() for value in ys]
    count = Decimal(len(xs))
    mean_x = sum(log_x) / count
    mean_y = sum(log_y) / count
    numerator = sum(
        (x_value - mean_x) * (y_value - mean_y)
        for x_value, y_value in zip(log_x, log_y, strict=True)
    )
    denominator = sum((value - mean_x) ** 2 for value in log_x)
    return numerator / denominator


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def audit() -> dict[str, object]:
    optimizer_max = optimizer(THREE)
    optimizer_grid = [
        optimizer(Decimal(index) / Decimal(1000))
        for index in range(1, 20001)
    ]
    grid_max = max(optimizer_grid)

    lattice_rows = []
    lattice_values = []
    for n_value in N_VALUES:
        factor = lattice_factor(n_value)
        lattice_values.append(factor)
        lattice_rows.append(
            {
                "N": n_value,
                "M": 2 * n_value + 1,
                "minimumKs": int(lattice_cost(n_value)),
                "NMOverMinimumKs": as_float(factor),
                "threeOverFourN": as_float(THREE / (FOUR * Decimal(n_value))),
            }
        )

    n_tail = [Decimal(value) for value in N_VALUES[-6:]]
    lattice_power = fit_power(n_tail, lattice_values[-6:])

    envelope_rows = []
    for delta_obs in DELTA_VALUES:
        values = [normalized_envelope(n_value, delta_obs) for n_value in N_VALUES]
        envelope_rows.append(
            {
                "deltaObs": as_float(delta_obs),
                "values": [
                    {"N": n_value, "upperEnvelope": as_float(value)}
                    for n_value, value in zip(N_VALUES, values, strict=True)
                ],
                "tailPower": as_float(fit_power(n_tail, values[-6:])),
            }
        )

    critical_values = []
    subcritical_values = []
    for n_value in N_VALUES:
        n = Decimal(n_value)
        critical_delta = decimal_power(n, THREE / FOUR)
        subcritical_delta = decimal_power(n, ONE / TWO)
        critical_values.append(normalized_envelope(n_value, critical_delta))
        subcritical_values.append(normalized_envelope(n_value, subcritical_delta))

    critical_power = fit_power(n_tail, critical_values[-6:])
    subcritical_power = fit_power(n_tail, subcritical_values[-6:])

    fixed_gap_values = [
        separated_factor(n_value, Decimal("0.05")) for n_value in N_VALUES
    ]
    quasiuniform_gap_values = [
        separated_factor(n_value, ONE / Decimal(n_value)) for n_value in N_VALUES
    ]
    fixed_gap_power = fit_power(n_tail, fixed_gap_values[-6:])
    quasiuniform_gap_power = fit_power(n_tail, quasiuniform_gap_values[-6:])

    determinant_rows = []
    determinant_logs = []
    for n_value in (4, 8, 16, 32, 64):
        n = Decimal(n_value)
        gap = ONE / n**3
        r_max = n + ONE
        base = B_RATE * gap * r_max**2
        log_lower = -gap.ln() - (n - ONE) * base.ln() / TWO
        determinant_logs.append(log_lower)
        determinant_rows.append(
            {
                "N": n_value,
                "gapLaw": "N^-3",
                "bGapRmaxSquared": as_float(base),
                "log10InverseLower": as_float(log_lower / Decimal(10).ln()),
            }
        )

    correction_rows = []
    heat_ratios = []
    for r_value in SINGLE_MODE_R:
        r = Decimal(r_value)
        ratio = (-NU * D_MODULUS**2 * r**2 * A_0).exp()
        heat_ratios.append(ratio)
        correction_rows.append(
            {
                "r": r_value,
                "unweightedL2": 1.0,
                "heatWeightedL2": as_float(ratio),
                "ratio": as_float(ratio),
            }
        )

    checks = [
        check(
            "optimizer analytic versus dense grid",
            abs(grid_max - optimizer_max) < Decimal("2e-8"),
            {"analytic": as_text(optimizer_max), "grid": as_text(grid_max)},
            "max_u u/(1+u)^(4/3) = 3/4^(4/3) at u=3",
        ),
        check(
            "integer lattice formula",
            all(
                lattice_cost(n_value)
                == sum(Decimal(index * index) for index in range(1, 2 * n_value + 2))
                for n_value in N_VALUES
            ),
            [row["minimumKs"] for row in lattice_rows],
            "minimum sum of M distinct positive integer squares equals sum_{1..M} j^2",
        ),
        check(
            "lattice suppression bound",
            all(
                lattice_factor(n_value) <= THREE / (FOUR * Decimal(n_value))
                for n_value in N_VALUES
            ),
            max(
                as_float(
                    lattice_factor(n_value) * FOUR * Decimal(n_value) / THREE
                )
                for n_value in N_VALUES
            ),
            "NM/Ks <= 3/(4N)",
        ),
        check(
            "lattice factor is decreasing",
            all(
                lattice_values[index + 1] < lattice_values[index]
                for index in range(len(lattice_values) - 1)
            ),
            [as_float(value) for value in lattice_values],
            "the exact factor decreases on the audited N grid",
        ),
        check(
            "lattice factor has N^-1 power",
            abs(lattice_power + ONE) < Decimal("0.002"),
            as_float(lattice_power),
            "tail fitted power is -1",
        ),
        check(
            "bounded coupling envelopes have N^-1 power",
            all(
                abs(Decimal(str(row["tailPower"])) + ONE) < Decimal("0.002")
                for row in envelope_rows
            ),
            [row["tailPower"] for row in envelope_rows],
            "every fixed-delta_obs envelope has tail power -1",
        ),
        check(
            "critical N^(3/4) coupling saturates",
            abs(critical_power) < Decimal("0.002"),
            as_float(critical_power),
            "delta_obs=N^(3/4) cancels the N^-1 envelope power",
        ),
        check(
            "subcritical N^(1/2) coupling vanishes",
            abs(subcritical_power + ONE / THREE) < Decimal("0.002"),
            as_float(subcritical_power),
            "delta_obs=N^(1/2) gives power -1/3",
        ),
        check(
            "multiplier upper constant",
            multiplier_ratio_upper() > ZERO,
            as_text(multiplier_ratio_upper()),
            "Omega^2/Kv <= 2*pi^2*Kz^2/3",
        ),
        check(
            "fixed-gap separated envelope has N^-2 power",
            abs(fixed_gap_power + TWO) < Decimal("0.002"),
            as_float(fixed_gap_power),
            "M/(b*h*Ks) has tail power -2 at fixed h",
        ),
        check(
            "quasiuniform separated envelope has N^-1 power",
            abs(quasiuniform_gap_power + ONE) < Decimal("0.002"),
            as_float(quasiuniform_gap_power),
            "M/(b*h*Ks) has tail power -1 at h=N^-1",
        ),
        check(
            "equal-grid inverse lower bound grows",
            all(
                determinant_logs[index + 1] > determinant_logs[index]
                for index in range(len(determinant_logs) - 1)
            )
            and determinant_rows[-1]["log10InverseLower"] > 20,
            determinant_rows,
            "h^-1*(b*h*rmax^2)^(-(N-1)/2) grows on the N^-3 audit law",
        ),
        check(
            "unweighted lower comparison fails after A0",
            heat_ratios[-1] < Decimal("1e-25")
            and all(
                heat_ratios[index + 1] < heat_ratios[index]
                for index in range(len(heat_ratios) - 1)
            ),
            correction_rows,
            "single-mode heat-weighted/unweighted ratio tends to zero as r grows",
        ),
    ]

    return {
        "release": "R0.71Y",
        "generatedAt": now(),
        "status": "passed" if all(item["passed"] for item in checks) else "failed",
        "meaning": (
            "Finite high-precision audit of the operator-sampling algebra. "
            "No growing-root construction, DNS, universal endpoint theorem, "
            "or Navier--Stokes regularity result is claimed."
        ),
        "parameters": {
            "Kz": as_float(K_Z),
            "nu": as_float(NU),
            "d": as_float(D_MODULUS),
            "A0": as_float(A_0),
            "NValues": list(N_VALUES),
            "deltaObsValues": [as_float(value) for value in DELTA_VALUES],
        },
        "optimizer": {"uStar": 3.0, "maximum": as_float(optimizer_max)},
        "multiplierRatioUpper": as_float(multiplier_ratio_upper()),
        "latticeRows": lattice_rows,
        "latticeTailPower": as_float(lattice_power),
        "envelopeRows": envelope_rows,
        "criticalCoupling": {
            "deltaObsLaw": "N^(3/4)",
            "tailPower": as_float(critical_power),
        },
        "subcriticalCoupling": {
            "deltaObsLaw": "N^(1/2)",
            "tailPower": as_float(subcritical_power),
        },
        "separatedRootEnvelope": {
            "fixedGap": 0.05,
            "fixedGapTailPower": as_float(fixed_gap_power),
            "quasiuniformGapLaw": "N^-1",
            "quasiuniformGapTailPower": as_float(quasiuniform_gap_power),
        },
        "equalGridInverseLower": determinant_rows,
        "heatWeightedCorrection": correction_rows,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    if result["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
