#!/usr/bin/env python3
"""High-precision algebra and scaling audit for R0.71Z.

The analytic argument is in ``research/r071z_report-source.md``.  This
producer independently recomputes the constants and powers that enter the
final launch-inclusive, all-root envelope.  It is deliberately not a time
integrator: it performs no DNS and does not prove the continuum theorem.
"""

from __future__ import annotations

import argparse
from datetime import datetime
from decimal import Decimal, getcontext
import json
from pathlib import Path
from zoneinfo import ZoneInfo


PRECISION_DIGITS = 110
getcontext().prec = PRECISION_DIGITS

ZERO = Decimal(0)
ONE = Decimal(1)
TWO = Decimal(2)
THREE = Decimal(3)
FOUR = Decimal(4)
SIX = Decimal(6)
SEVEN = Decimal(7)

# The numerical normalization is used only to expose the constants.  None of
# the audited M-powers depends on these choices.
NU = Decimal("0.02")
D_MODULUS = Decimal(8)
K_Z = ONE
A_0 = Decimal("0.05")
LAMBDA_0_L = Decimal("0.125")
KAPPA = NU * D_MODULUS**2

M_VALUES = tuple(2**power + 1 for power in range(1, 31))
BOUNDED_ETA_VALUES = (
    ONE / Decimal(64),
    ONE / Decimal(16),
    ONE / FOUR,
    ONE,
    FOUR,
)
RETENTION_FREQUENCIES = (1, 2, 4, 8, 16, 32, 64, 128)


def decimal_pi() -> Decimal:
    """Compute pi with the Decimal context by the Gauss--Legendre AGM."""

    a_value = ONE
    b_value = ONE / TWO.sqrt()
    t_value = ONE / FOUR
    p_value = ONE
    for _ in range(10):
        next_a = (a_value + b_value) / TWO
        next_b = (a_value * b_value).sqrt()
        next_t = t_value - p_value * (a_value - next_a) ** 2
        a_value, b_value, t_value = next_a, next_b, next_t
        p_value *= TWO
    return (a_value + b_value) ** 2 / (FOUR * t_value)


PI = decimal_pi()


def decimal_power(value: Decimal, exponent: Decimal) -> Decimal:
    if value <= ZERO:
        raise ValueError("decimal_power requires a positive base")
    return (exponent * value.ln()).exp()


def as_text(value: Decimal) -> str:
    return format(value, ".70E")


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def fit_power(xs: list[Decimal], ys: list[Decimal]) -> Decimal:
    if len(xs) != len(ys) or len(xs) < 2:
        raise ValueError("fit_power requires equally sized nontrivial samples")
    if any(value <= ZERO for value in xs + ys):
        raise ValueError("fit_power requires positive samples")
    log_x = [value.ln() for value in xs]
    log_y = [value.ln() for value in ys]
    count = Decimal(len(xs))
    mean_x = sum(log_x, ZERO) / count
    mean_y = sum(log_y, ZERO) / count
    numerator = sum(
        (
            (x_value - mean_x) * (y_value - mean_y)
            for x_value, y_value in zip(log_x, log_y, strict=True)
        ),
        ZERO,
    )
    denominator = sum(((value - mean_x) ** 2 for value in log_x), ZERO)
    return numerator / denominator


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def minimum_lattice_cost(m_value: int) -> Decimal:
    m = Decimal(m_value)
    return m * (m + ONE) * (TWO * m + ONE) / SIX


def lattice_factor(m_value: int) -> Decimal:
    return Decimal(m_value) / minimum_lattice_cost(m_value)


def optimizer(u_value: Decimal) -> Decimal:
    return u_value / decimal_power(ONE + u_value, FOUR / THREE)


def c_kappa() -> Decimal:
    return PI**2 / (Decimal(45).sqrt() * KAPPA)


def multiplier_ratio_upper() -> Decimal:
    return TWO * PI**2 * K_Z**2 / THREE


def c_bv(eta: Decimal) -> Decimal:
    return (TWO * LAMBDA_0_L).exp() * (FOUR + c_kappa() * eta)


def normalized_envelope(m_value: int, eta: Decimal) -> Decimal:
    """Constant-normalized right side of (6.9) in the report."""

    optimizer_max = THREE / decimal_power(FOUR, FOUR / THREE)
    return (
        optimizer_max
        * c_bv(eta)
        * lattice_factor(m_value)
        * decimal_power(eta, FOUR / THREE)
        * decimal_power(multiplier_ratio_upper(), ONE / THREE)
    )


def floor_cancellation_rows() -> list[dict[str, object]]:
    cases = (
        ("dyadic", ONE / Decimal(8), Decimal(8), (ONE / Decimal(8), ONE / TWO, TWO, Decimal(8))),
        ("scaled-dyadic", ONE / FOUR, Decimal(16), (ONE / FOUR, ONE, FOUR, Decimal(16))),
    )
    rows: list[dict[str, object]] = []
    for label, inf_y, sup_y, roots in cases:
        contrast = sup_y / inf_y
        for root_y in roots:
            left = ONE / (root_y * contrast)
            right = ONE / sup_y
            identity_right = inf_y / (root_y * sup_y)
            rows.append(
                {
                    "case": label,
                    "infY": as_text(inf_y),
                    "supY": as_text(sup_y),
                    "rootY": as_text(root_y),
                    "RY": as_text(contrast),
                    "oneOverRootYRY": as_text(left),
                    "infYOverRootYSupY": as_text(identity_right),
                    "oneOverSupY": as_text(right),
                    "identityResidual": as_text(abs(left - identity_right)),
                    "inequalityRatio": as_text(left / right),
                    "equalityAtMinimum": bool(root_y == inf_y and left == right),
                    "inequalityPassed": bool(left <= right),
                }
            )
    return rows


def audit() -> dict[str, object]:
    tolerance = Decimal("1e-70")

    # C_kappa is recomputed both from the zeta(4) Cauchy--Schwarz route and
    # from its simplified formula pi^2/(sqrt(45)*kappa).
    zeta_four = PI**4 / Decimal(90)
    c_kappa_unsimplified = (
        TWO / KAPPA * zeta_four.sqrt() / TWO.sqrt()
    )
    c_kappa_value = c_kappa()
    c_kappa_residual = abs(c_kappa_unsimplified - c_kappa_value)

    # The multiplier constant is likewise reconstructed from sum r^-2.
    zeta_two = PI**2 / SIX
    multiplier_from_cauchy = FOUR * K_Z**2 * zeta_two
    multiplier_value = multiplier_ratio_upper()

    optimizer_max = optimizer(THREE)
    optimizer_grid = [
        optimizer(Decimal(index) / Decimal(1000))
        for index in range(1, 10001)
    ]
    optimizer_grid_max = max(optimizer_grid)
    optimizer_grid_argmax = optimizer_grid.index(optimizer_grid_max) + 1

    lattice_rows: list[dict[str, object]] = []
    lattice_values: list[Decimal] = []
    for m_value in M_VALUES:
        factor = lattice_factor(m_value)
        lattice_values.append(factor)
        lattice_rows.append(
            {
                "M": m_value,
                "minimumKs": str(int(minimum_lattice_cost(m_value))),
                "MOverMinimumKs": as_text(factor),
                "M2TimesMOverMinimumKs": as_text(
                    Decimal(m_value) ** 2 * factor
                ),
                "upperThreeOverM2": as_text(
                    THREE / Decimal(m_value) ** 2
                ),
            }
        )
    tail_m = [Decimal(value) for value in M_VALUES[-8:]]
    lattice_tail_power = fit_power(tail_m, lattice_values[-8:])

    bounded_rows: list[dict[str, object]] = []
    bounded_tail_powers: list[Decimal] = []
    for eta in BOUNDED_ETA_VALUES:
        values = [normalized_envelope(m_value, eta) for m_value in M_VALUES]
        tail_power = fit_power(tail_m, values[-8:])
        bounded_tail_powers.append(tail_power)
        bounded_rows.append(
            {
                "eta": as_text(eta),
                "CBV": as_text(c_bv(eta)),
                "tailPowerInM": as_text(tail_power),
                "values": [
                    {"M": m_value, "envelope": as_text(value)}
                    for m_value, value in zip(M_VALUES, values, strict=True)
                ],
            }
        )

    critical_eta_power = SIX / SEVEN
    large_eta_total_power = FOUR / THREE + ONE
    critical_balance = -TWO + critical_eta_power * large_eta_total_power
    strong_rows: list[dict[str, object]] = []
    strong_values: list[Decimal] = []
    for m_value in M_VALUES:
        m = Decimal(m_value)
        eta = decimal_power(m, critical_eta_power)
        value = normalized_envelope(m_value, eta)
        strong_values.append(value)
        strong_rows.append(
            {
                "M": m_value,
                "etaEqualsMToSixSevenths": as_text(eta),
                "CBV": as_text(c_bv(eta)),
                "envelope": as_text(value),
            }
        )
    strong_tail_power = fit_power(tail_m, strong_values[-8:])

    floor_rows = floor_cancellation_rows()

    heat_coefficient = TWO * NU * D_MODULUS**2 * A_0
    retention_rows: list[dict[str, object]] = []
    negative_log_retention: list[Decimal] = []
    retention_r: list[Decimal] = []
    for frequency in RETENTION_FREQUENCIES:
        r_value = Decimal(frequency)
        exponent = heat_coefficient * r_value**2
        retention = (-exponent).exp()
        negative_log_retention.append(exponent)
        retention_r.append(r_value)
        retention_rows.append(
            {
                "R": frequency,
                "minusLogThetaI": as_text(exponent),
                "thetaI": as_text(retention),
                "log10ThetaI": as_text(-exponent / Decimal(10).ln()),
                "R8ThetaI": as_text(r_value**8 * retention),
                "minusLogThetaIOverR2": as_text(exponent / r_value**2),
            }
        )
    retention_exponent = fit_power(retention_r, negative_log_retention)

    checks = [
        check(
            "BV constant C_kappa",
            c_kappa_value > ZERO and c_kappa_residual < tolerance,
            {
                "simplified": as_text(c_kappa_value),
                "zeta4CauchyRoute": as_text(c_kappa_unsimplified),
                "residual": as_text(c_kappa_residual),
            },
            "C_kappa=pi^2/(sqrt(45)*nu*d^2) with no carrier-count factor",
        ),
        check(
            "amplitude optimizer u=3",
            optimizer_grid_argmax == 3000
            and abs(optimizer_grid_max - optimizer_max) < tolerance,
            {
                "uStar": "3",
                "analyticMaximum": as_text(optimizer_max),
                "gridMaximum": as_text(optimizer_grid_max),
                "gridArgmax": as_text(Decimal(optimizer_grid_argmax) / Decimal(1000)),
            },
            "max_{u>0} u*(1+u)^(-4/3)=3/4^(4/3) at u=3",
        ),
        check(
            "minimum lattice cost and M^-2 suppression",
            all(
                minimum_lattice_cost(m_value)
                == Decimal(sum(index * index for index in range(1, m_value + 1)))
                for m_value in M_VALUES
                if m_value <= 4097
            )
            and all(
                lattice_factor(m_value) <= THREE / Decimal(m_value) ** 2
                for m_value in M_VALUES
            )
            and abs(lattice_tail_power + TWO) < Decimal("2e-6")
            and Decimal(M_VALUES[-1]) ** 2 * lattice_values[-1]
            > Decimal("2.999999"),
            {
                "tailPower": as_text(lattice_tail_power),
                "terminalM2Factor": as_text(
                    Decimal(M_VALUES[-1]) ** 2 * lattice_values[-1]
                ),
            },
            "M/Ks<=3/M^2 and the exact factor has tail power -2",
        ),
        check(
            "bounded eta envelopes retain M^-2",
            all(abs(power + TWO) < Decimal("2e-6") for power in bounded_tail_powers),
            [as_text(power) for power in bounded_tail_powers],
            "fixed eta leaves C_BV(eta)*eta^(4/3) independent of M",
        ),
        check(
            "large-eta critical power is six sevenths",
            abs(critical_balance) < tolerance
            and abs(strong_tail_power) < Decimal("2e-5"),
            {
                "algebraicBalance": as_text(critical_balance),
                "etaPower": as_text(critical_eta_power),
                "numericalTailPower": as_text(strong_tail_power),
            },
            "-2+(6/7)*(4/3+1)=0; eta=M^(6/7) saturates the upper envelope",
        ),
        check(
            "Omega squared over Kv upper constant",
            abs(multiplier_from_cauchy - multiplier_value) < tolerance,
            {
                "twoPiSquaredKzSquaredOverThree": as_text(multiplier_value),
                "fourKzSquaredZeta2": as_text(multiplier_from_cauchy),
                "residual": as_text(abs(multiplier_from_cauchy - multiplier_value)),
            },
            "Omega^2/Kv <= 2*pi^2*Kz^2/3",
        ),
        check(
            "launch-inclusive floor cancellation identity",
            all(
                Decimal(row["identityResidual"]) == ZERO
                and bool(row["inequalityPassed"])
                for row in floor_rows
            )
            and sum(bool(row["equalityAtMinimum"]) for row in floor_rows) == 2,
            floor_rows,
            "1/(Y(root)*R_Y)=infY/(Y(root)*supY)<=1/supY, with equality at Y(root)=infY",
        ),
        check(
            "fixed-window heat retention disappears",
            abs(retention_exponent - TWO) < tolerance
            and Decimal(retention_rows[-1]["thetaI"]) < Decimal("1e-900")
            and Decimal(retention_rows[-1]["R8ThetaI"]) < Decimal("1e-850"),
            {
                "minusLogThetaTailPower": as_text(retention_exponent),
                "heatCoefficient": as_text(heat_coefficient),
                "terminalThetaI": retention_rows[-1]["thetaI"],
                "terminalR8ThetaI": retention_rows[-1]["R8ThetaI"],
            },
            "theta_I=exp(-2*nu*d^2*A0*R^2) tends to zero faster than every audited polynomial compensation",
        ),
    ]

    return {
        "release": "R0.71Z",
        "generatedAt": now(),
        "status": "passed" if all(item["passed"] for item in checks) else "failed",
        "certificateType": "high-precision algebra and asymptotic scaling audit",
        "analyticSource": "research/r071z_report-source.md",
        "claimBoundary": {
            "continuumProof": False,
            "directNumericalSimulation": False,
            "threeDimensionalTurbulenceTimeStepping": False,
            "exactRootFamilyConstruction": False,
            "navierStokesRegularityResult": False,
            "meaning": (
                "This producer checks constants, identities, and finite-grid "
                "asymptotic diagnostics used by the analytic report. The "
                "report, not this JSON, carries the continuum proof."
            ),
        },
        "arithmetic": {
            "engine": "Python standard-library Decimal",
            "contextPrecisionDigits": PRECISION_DIGITS,
            "serializedSignificantDigits": 71,
            "piConstruction": "10-step Gauss-Legendre AGM in the same Decimal context",
        },
        "parameters": {
            "nu": as_text(NU),
            "d": as_text(D_MODULUS),
            "kappa": as_text(KAPPA),
            "Kz": as_text(K_Z),
            "A0": as_text(A_0),
            "lambda0L": as_text(LAMBDA_0_L),
            "MValues": list(M_VALUES),
            "boundedEtaValues": [as_text(value) for value in BOUNDED_ETA_VALUES],
            "normalizationNote": (
                "These fixed numerical values expose constants only; the audited M-powers are parameter independent."
            ),
        },
        "BVConstant": {
            "formula": "C_kappa=pi^2/(sqrt(45)*nu*d^2)",
            "value": as_text(c_kappa_value),
            "zeta4Route": as_text(c_kappa_unsimplified),
        },
        "amplitudeOptimizer": {
            "factor": "u*(1+u)^(-4/3)",
            "uStar": "3",
            "maximum": as_text(optimizer_max),
        },
        "multiplierRatio": {
            "formula": "Omega^2/Kv <= 2*pi^2*Kz^2/3",
            "upperConstant": as_text(multiplier_value),
        },
        "lattice": {
            "formula": "Ks_min=M*(M+1)*(2*M+1)/6",
            "factor": "M/Ks_min",
            "tailPower": as_text(lattice_tail_power),
            "rows": lattice_rows,
        },
        "boundedCouplingEnvelope": {
            "formula": "optimizer_max*C_BV(eta)*(M/Ks)*eta^(4/3)*(2*pi^2*Kz^2/3)^(1/3)",
            "expectedMPower": "-2",
            "rows": bounded_rows,
        },
        "strongCouplingDiagnostic": {
            "CBVLargeEtaPower": "1",
            "etaFactorPowerIncludingCBV": "7/3",
            "criticalEtaLaw": "eta=M^(6/7)",
            "algebraicMPower": as_text(critical_balance),
            "fittedMPower": as_text(strong_tail_power),
            "interpretation": (
                "Saturation of this upper envelope is not a construction of a strong-coupling exact-root family."
            ),
            "rows": strong_rows,
        },
        "floorCancellation": {
            "identity": "1/(Y(root)*R_Y)=infY/(Y(root)*supY)<=1/supY",
            "rows": floor_rows,
        },
        "fixedWindowRetention": {
            "formula": "theta_I=exp(-2*nu*d^2*A0*R^2)",
            "minusLogThetaPowerInR": as_text(retention_exponent),
            "interpretation": (
                "Launch data do not provide a uniform positive retention factor on a fixed window excluding launch."
            ),
            "rows": retention_rows,
        },
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
