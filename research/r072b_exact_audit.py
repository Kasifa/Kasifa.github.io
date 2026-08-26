#!/usr/bin/env python3
"""Producer audit for the R0.72B target-row coherence theorem.

The analytic proof belongs in ``research/r072b_report-source.md``.  This
program reconstructs the theorem constants and scaling laws from raw
parameters at high precision.  It also performs deterministic quadrature for
representative heat-decaying profiles and evaluates three Bessel-family
comparison indicators.  Floating-point output corroborates the algebra; it
is not interval arithmetic and is not a continuum proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time

import mpmath as mp


MP_DIGITS = 80
mp.mp.dps = MP_DIGITS

NU = mp.mpf("1")
D_MODULUS = mp.mpf("1")
K_Z = mp.mpf("1")
KAPPA = NU * D_MODULUS**2
RHO_ROOT_NEIGHBORHOOD = mp.mpf("0.35")
M_VALUES = tuple(2**power for power in range(0, 21))
EXPOSURE_M_VALUES = (1, 2, 4, 8, 16, 32, 64)
BESSEL_R_VALUES = (8, 16, 32, 64, 128, 256, 512)
EXPOSURE_LENGTH = mp.mpf("2")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--progress-log", type=Path)
    parser.add_argument("--resource-log", type=Path)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def emit(message: str) -> None:
    print(f"[{utc_now()}] {message}", file=sys.stderr, flush=True)


def append_json(path: Path | None, payload: dict[str, object]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def progress(path: Path | None, stage: str, **fields: object) -> None:
    append_json(path, {"timestampUtc": utc_now(), "stage": stage, **fields})


def resource_snapshot(
    path: Path | None, stage: str, started: float, **fields: object
) -> None:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_json(
        path,
        {
            "timestampUtc": utc_now(),
            "stage": stage,
            "elapsedSeconds": time.perf_counter() - started,
            "userCpuSeconds": usage.ru_utime,
            "systemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
            "logicalCpuCount": os.cpu_count(),
            **fields,
        },
    )


def mtext(value: mp.mpf, digits: int = 40) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def as_float(value: mp.mpf) -> float:
    return float(value)


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def regression_power(xs: list[mp.mpf], ys: list[mp.mpf]) -> mp.mpf:
    log_x = [mp.log(value) for value in xs]
    log_y = [mp.log(value) for value in ys]
    mean_x = mp.fsum(log_x) / len(log_x)
    mean_y = mp.fsum(log_y) / len(log_y)
    numerator = mp.fsum(
        (x_value - mean_x) * (y_value - mean_y)
        for x_value, y_value in zip(log_x, log_y, strict=True)
    )
    denominator = mp.fsum((x_value - mean_x) ** 2 for x_value in log_x)
    return numerator / denominator


def constants_ledger() -> dict[str, object]:
    c_kappa = mp.pi**2 / (mp.sqrt(45) * KAPPA)
    c_cross = mp.sqrt(c_kappa / (2 * KAPPA))

    # The pointwise row estimate has prefactor
    # 6 sqrt(2 nu) d |Kz|.  Cauchy--Schwarz then uses
    # int A^2 = rho_A^2/(4 kappa Kz^2) and int E <= M/2.
    # Dividing by rho_A sqrt(M) leaves exactly 3.
    q_ratio = (
        6
        * mp.sqrt(2 * NU)
        * D_MODULUS
        * abs(K_Z)
        * mp.sqrt(1 / (4 * KAPPA * K_Z**2))
        * mp.sqrt(mp.mpf("0.5"))
    )
    return {
        "Ckappa": mtext(c_kappa),
        "Ccross": mtext(c_cross),
        "CcrossIdentityResidual": mtext(abs(2 * KAPPA * c_cross**2 - c_kappa)),
        "qRhoCauchyConstant": mtext(q_ratio),
        "qRhoConstantResidualFromThree": mtext(abs(q_ratio - 3)),
        "formulas": {
            "rhoSquared": "2*Kz^2*sum_l |z_l|^2 exp(-2*kappa*r_l^2*A0)",
            "Ccross": "sqrt(Ckappa/(2*kappa))",
            "qRho": "integral_I |QF|/(rho_A*sqrt(M)) <= 3",
            "mixedExposure": "integral_I rho(x)||V(x)|| dx/(rho_A*Omega)",
        },
    }


def phase_boundary_rows() -> list[dict[str, object]]:
    beta_values = (
        Fraction(0),
        Fraction(1, 2),
        Fraction(1),
        Fraction(3, 2),
        Fraction(2),
        Fraction(5, 2),
        Fraction(3),
        Fraction(4),
    )
    rows: list[dict[str, object]] = []
    for beta in beta_values:
        old = min(Fraction(3, 2), (Fraction(6) + 3 * beta) / 7)
        participation = min(Fraction(9, 4), (Fraction(9) + 3 * beta) / 7)
        coherent = min(Fraction(5, 2), (Fraction(10) + 3 * beta) / 7)
        rows.append(
            {
                "beta": float(beta),
                "oldMMinus2": float(old),
                "oldExact": str(old),
                "targetParticipationMMinus3": float(participation),
                "targetParticipationExact": str(participation),
                "coherentMMinusTenThirds": float(coherent),
                "coherentExact": str(coherent),
            }
        )
    return rows


def equal_carrier_rows() -> tuple[list[dict[str, object]], mp.mpf]:
    rows: list[dict[str, object]] = []
    prefactors: list[mp.mpf] = []
    for m_value in M_VALUES:
        m = mp.mpf(m_value)
        ks_integer = m_value * (m_value + 1) * (2 * m_value + 1) // 6
        ks = mp.mpf(ks_integer)
        omega = 2 * abs(K_Z) * m
        rho_squared = 2 * K_Z**2 * m
        chi = rho_squared / omega**2
        omega_squared_over_kv = omega**2 / ks
        normalized_prefactor = (
            (m / ks) * chi * mp.root(omega_squared_over_kv, 3)
        )
        prefactors.append(normalized_prefactor)
        rows.append(
            {
                "M": m_value,
                "Ks": ks_integer,
                "Kv": ks_integer,
                "Omega": mtext(omega),
                "rhoSquared": mtext(rho_squared),
                "chi": mtext(chi),
                "twoMChi": mtext(2 * m * chi),
                "OmegaSquaredOverKv": mtext(omega_squared_over_kv),
                "M times OmegaSquaredOverKv": mtext(
                    m * omega_squared_over_kv
                ),
                "normalizedGeometricPrefactor": mtext(normalized_prefactor),
                "MToTenThirdsTimesPrefactor": mtext(
                    m ** (mp.mpf(10) / 3) * normalized_prefactor
                ),
                "newRootFactorOverOldRootFactor": mtext(chi),
            }
        )
    tail_power = regression_power(
        [mp.mpf(value) for value in M_VALUES[-7:]], prefactors[-7:]
    )
    return rows, tail_power


def comparable_carrier_rows() -> tuple[list[dict[str, object]], mp.mpf]:
    """Audit one non-equal positive family with a uniform amplitude ratio."""

    lower = mp.mpf("0.75")
    upper = mp.mpf("1.25")
    rows: list[dict[str, object]] = []
    prefactors: list[mp.mpf] = []
    for m_value in M_VALUES[1:]:
        # Every audited M is even. Odd radii carry the upper weight and even
        # radii carry the lower weight.
        half = m_value // 2
        ks_integer = m_value * (m_value + 1) * (2 * m_value + 1) // 6
        even_square_sum = 4 * half * (half + 1) * (2 * half + 1) // 6
        odd_square_sum = ks_integer - even_square_sum
        m = mp.mpf(m_value)
        sum_z = mp.mpf(half) * (lower + upper)
        sum_z_square = mp.mpf(half) * (lower**2 + upper**2)
        kv = upper**2 * odd_square_sum + lower**2 * even_square_sum
        omega = 2 * abs(K_Z) * sum_z
        rho_squared = 2 * K_Z**2 * sum_z_square
        chi = rho_squared / omega**2
        omega_squared_over_kv = omega**2 / kv
        prefactor = (
            (m / ks_integer) * chi * mp.root(omega_squared_over_kv, 3)
        )
        prefactors.append(prefactor)
        chi_upper = (upper / lower) ** 2 / (2 * m)
        multiplier_upper = 12 * K_Z**2 * (upper / lower) ** 2 / m
        rows.append(
            {
                "M": m_value,
                "lowerAmplitude": mtext(lower),
                "upperAmplitude": mtext(upper),
                "chi": mtext(chi),
                "chiUpper": mtext(chi_upper),
                "chiOverUpper": mtext(chi / chi_upper),
                "OmegaSquaredOverKv": mtext(omega_squared_over_kv),
                "OmegaSquaredOverKvUpper": mtext(multiplier_upper),
                "multiplierRatioOverUpper": mtext(
                    omega_squared_over_kv / multiplier_upper
                ),
                "normalizedGeometricPrefactor": mtext(prefactor),
                "MToTenThirdsTimesPrefactor": mtext(
                    m ** (mp.mpf(10) / 3) * prefactor
                ),
            }
        )
    tail_power = regression_power(
        [mp.mpf(value) for value in M_VALUES[-7:]], prefactors[-7:]
    )
    return rows, tail_power


def mixed_exposure_rows(c_cross: mp.mpf) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    split_points = [
        mp.mpf("0"),
        mp.mpf("0.0005"),
        mp.mpf("0.002"),
        mp.mpf("0.01"),
        mp.mpf("0.05"),
        mp.mpf("0.25"),
        EXPOSURE_LENGTH,
    ]
    for m_value in EXPOSURE_M_VALUES:
        rho_a = mp.sqrt(2 * K_Z**2 * m_value)
        omega = 2 * abs(K_Z) * m_value

        def rho(time_value: mp.mpf) -> mp.mpf:
            return mp.sqrt(
                2
                * K_Z**2
                * mp.fsum(
                    mp.exp(-2 * KAPPA * radius**2 * time_value)
                    for radius in range(1, m_value + 1)
                )
            )

        def multiplier_norm(time_value: mp.mpf) -> mp.mpf:
            return 2 * abs(K_Z) * mp.fsum(
                mp.exp(-KAPPA * radius**2 * time_value)
                for radius in range(1, m_value + 1)
            )

        integral = mp.quad(
            lambda value: rho(value) * multiplier_norm(value), split_points
        )
        ell_cross = integral / (rho_a * omega)
        upper = min(EXPOSURE_LENGTH, c_cross)
        rho_square_integral = mp.fsum(
            K_Z**2 / (KAPPA * radius**2)
            for radius in range(1, m_value + 1)
        )
        rho_square_bound = rho_a**2 / (2 * KAPPA)
        rows.append(
            {
                "M": m_value,
                "L": mtext(EXPOSURE_LENGTH),
                "rhoA": mtext(rho_a),
                "Omega": mtext(omega),
                "mixedIntegral": mtext(integral),
                "ellCross": mtext(ell_cross),
                "minLAndCcross": mtext(upper),
                "ellCrossOverBound": mtext(ell_cross / upper),
                "rhoSquareIntegral": mtext(rho_square_integral),
                "rhoSquareHalfLineBound": mtext(rho_square_bound),
                "rhoSquareIntegralOverBound": mtext(
                    rho_square_integral / rho_square_bound
                ),
            }
        )
    return rows


def bessel_comparison_rows() -> tuple[list[dict[str, object]], dict[str, str]]:
    rows: list[dict[str, object]] = []
    theta_values: list[mp.mpf] = []
    xi_values: list[mp.mpf] = []
    energy_values: list[mp.mpf] = []
    for r_value in BESSEL_R_VALUES:
        r = mp.mpf(r_value)
        last_zero = mp.besseljzero(1, r_value)
        terminal_tau = last_zero / 2 + RHO_ROOT_NEIGHBORHOOD
        delta = r**4
        layer = terminal_tau / delta
        frozen_ed_rate = r**2 / mp.log(r) ** 2
        theta = layer * frozen_ed_rate
        # Stable form of L - (1-exp(-L)).
        heat_freezing = 2 * delta * (layer + mp.expm1(-layer))
        heat_freezing_upper = delta * layer**2
        energy_loss = (
            4 * terminal_tau
            + 4 * terminal_tau**2
            + mp.mpf(8) * terminal_tau**3 / 3
        ) / delta
        theta_values.append(theta)
        xi_values.append(heat_freezing)
        energy_values.append(energy_loss)
        rows.append(
            {
                "R": r_value,
                "lastJ1Zero": mtext(last_zero),
                "terminalTau": mtext(terminal_tau),
                "layerLength": mtext(layer),
                "frozenEnhancedDissipationRate": mtext(frozen_ed_rate),
                "ThetaLayerTimesFrozenRate": mtext(theta),
                "RLogSquaredRTimesTheta": mtext(r * mp.log(r) ** 2 * theta),
                "heatFreezingXi": mtext(heat_freezing),
                "heatFreezingUpper": mtext(heat_freezing_upper),
                "XiOverUpper": mtext(heat_freezing / heat_freezing_upper),
                "R2TimesXi": mtext(r**2 * heat_freezing),
                "energyLossUpper": mtext(energy_loss),
                "RTimesEnergyLossUpper": mtext(r * energy_loss),
            }
        )
    tail_r = [mp.mpf(value) for value in BESSEL_R_VALUES[-4:]]
    powers = {
        "ThetaTailPower": mtext(regression_power(tail_r, theta_values[-4:])),
        "XiTailPower": mtext(regression_power(tail_r, xi_values[-4:])),
        "energyLossTailPower": mtext(
            regression_power(tail_r, energy_values[-4:])
        ),
    }
    return rows, powers


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    emit("R0.72B producer audit started")
    progress(args.progress_log, "producer-start", mpDigits=MP_DIGITS)
    resource_snapshot(args.resource_log, "producer-start", started)

    constants = constants_ledger()
    c_cross = mp.mpf(constants["Ccross"])
    emit("constant identities and q_rho payment complete")
    progress(args.progress_log, "constants-complete")

    phases = phase_boundary_rows()
    equal_rows, equal_tail_power = equal_carrier_rows()
    comparable_rows, comparable_tail_power = comparable_carrier_rows()
    emit(
        "phase and equal-carrier ledgers complete: fitted prefactor power "
        f"{float(equal_tail_power):.8f}; comparable {float(comparable_tail_power):.8f}"
    )
    progress(
        args.progress_log,
        "scaling-ledger-complete",
        fittedPower=float(equal_tail_power),
        comparableFittedPower=float(comparable_tail_power),
    )

    exposure_rows = mixed_exposure_rows(c_cross)
    emit("mixed-exposure quadrature complete")
    progress(
        args.progress_log,
        "mixed-exposure-complete",
        rowCount=len(exposure_rows),
    )
    resource_snapshot(args.resource_log, "mixed-exposure-complete", started)

    bessel_rows, bessel_powers = bessel_comparison_rows()
    emit("Bessel and enhanced-dissipation comparison ledger complete")
    progress(
        args.progress_log,
        "bessel-comparison-complete",
        rowCount=len(bessel_rows),
    )

    phase_zero = phases[0]
    phase_cap = next(row for row in phases if row["beta"] == 2.5)
    exposure_pass = all(
        mp.mpf(row["ellCross"]) <= mp.mpf(row["minLAndCcross"])
        + mp.mpf("1e-60")
        for row in exposure_rows
    )
    rho_integral_pass = all(
        mp.mpf(row["rhoSquareIntegralOverBound"]) <= 1 + mp.mpf("1e-60")
        for row in exposure_rows
    )
    bessel_xi_pass = all(
        mp.mpf(row["heatFreezingXi"])
        <= mp.mpf(row["heatFreezingUpper"]) + mp.mpf("1e-60")
        for row in bessel_rows
    )
    bessel_metric_sequences = [
        [mp.mpf(row[key]) for row in bessel_rows]
        for key in (
            "ThetaLayerTimesFrozenRate",
            "heatFreezingXi",
            "energyLossUpper",
        )
    ]
    bessel_metrics_decrease = all(
        later < earlier
        for values in bessel_metric_sequences
        for earlier, later in zip(values[:-1], values[1:], strict=True)
    )
    checks = [
        check(
            "mixed-exposure constant identity",
            mp.mpf(constants["CcrossIdentityResidual"]) < mp.mpf("1e-70"),
            constants["CcrossIdentityResidual"],
            "2*kappa*Ccross^2=Ckappa",
        ),
        check(
            "dissipation-paired target-row payment",
            mp.mpf(constants["qRhoConstantResidualFromThree"]) < mp.mpf("1e-70"),
            constants["qRhoCauchyConstant"],
            "integral |QF| <= 3*rho_A*sqrt(M)",
        ),
        check(
            "representative mixed exposure obeys both bounds",
            exposure_pass and rho_integral_pass,
            {
                "maximumEllCrossOverBound": max(
                    float(row["ellCrossOverBound"]) for row in exposure_rows
                ),
                "maximumRhoSquareIntegralOverBound": max(
                    float(row["rhoSquareIntegralOverBound"])
                    for row in exposure_rows
                ),
            },
            "ell_cross<=min(L,Ccross) and integral rho^2<=rho_A^2/(2*kappa)",
        ),
        check(
            "equal-carrier target participation identity",
            max(abs(mp.mpf(row["twoMChi"]) - 1) for row in equal_rows)
            < mp.mpf("1e-70"),
            equal_rows[-1]["chi"],
            "chi=rho_A^2/Omega^2=1/(2M) for r_l=l,z_l=1",
        ),
        check(
            "coherent normalized prefactor has M^-10/3 tail",
            abs(equal_tail_power + mp.mpf(10) / 3) < mp.mpf("0.001"),
            mtext(equal_tail_power),
            "(M/Ks)*chi*(Omega^2/Kv)^(1/3) has asymptotic power -10/3",
        ),
        check(
            "comparable positive amplitudes retain M^-10/3",
            abs(comparable_tail_power + mp.mpf(10) / 3) < mp.mpf("0.001")
            and max(mp.mpf(row["chiOverUpper"]) for row in comparable_rows) <= 1
            and max(
                mp.mpf(row["multiplierRatioOverUpper"])
                for row in comparable_rows
            )
            <= 1,
            {
                "fittedTailPower": mtext(comparable_tail_power),
                "maximumChiOverUpper": mtext(
                    max(mp.mpf(row["chiOverUpper"]) for row in comparable_rows)
                ),
                "maximumMultiplierRatioOverUpper": mtext(
                    max(
                        mp.mpf(row["multiplierRatioOverUpper"])
                        for row in comparable_rows
                    )
                ),
            },
            "uniform same-sign amplitudes bounded above and below give chi=O(M^-1), Omega^2/Kv=O(M^-1), and total M^-10/3",
        ),
        check(
            "coherent phase boundary endpoints",
            abs(phase_zero["coherentMMinusTenThirds"] - 10 / 7) < 1e-15
            and abs(phase_cap["coherentMMinusTenThirds"] - 5 / 2) < 1e-15,
            {
                "fixedLayer": phase_zero["coherentExact"],
                "capAtBetaFiveHalves": phase_cap["coherentExact"],
            },
            "alpha<min(5/2,(10+3*beta)/7)",
        ),
        check(
            "Bessel heat-freezing inequality",
            bessel_xi_pass,
            max(float(row["XiOverUpper"]) for row in bessel_rows),
            "2*R^4*[L-(1-exp(-L))] <= R^4*L^2",
        ),
        check(
            "Bessel pre-dissipation indicators decay",
            bessel_metrics_decrease,
            {
                "terminalTheta": bessel_rows[-1]["ThetaLayerTimesFrozenRate"],
                "terminalXi": bessel_rows[-1]["heatFreezingXi"],
                "terminalEnergyLossUpper": bessel_rows[-1]["energyLossUpper"],
                "tailPowers": bessel_powers,
            },
            "Theta_R, Xi_R, and the analytic energy-loss upper bound decrease",
        ),
    ]

    all_passed = all(bool(row["passed"]) for row in checks)
    payload = {
        "schemaVersion": "r072b-target-row-coherence-producer-v1",
        "release": "R0.72B",
        "generatedAtUtc": utc_now(),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "arithmetic": {
            "engine": "mpmath arbitrary precision",
            "decimalDigits": MP_DIGITS,
            "intervalArithmetic": False,
            "role": "high-precision algebra and deterministic quadrature corroboration",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "mpmath": mp.__version__,
        },
        "parameters": {
            "nu": mtext(NU),
            "d": mtext(D_MODULUS),
            "kappa": mtext(KAPPA),
            "Kz": mtext(K_Z),
            "A0": 0,
            "equalCarrierRule": "r_l=l and z_l=1",
            "MValues": list(M_VALUES),
            "exposureLength": mtext(EXPOSURE_LENGTH),
            "besselRValues": list(BESSEL_R_VALUES),
            "besselRootNeighborhood": mtext(RHO_ROOT_NEIGHBORHOOD),
            "randomness": False,
        },
        "analyticLedger": {
            "completeRootBound": (
                "G_all^ex <= exp(2*lambda0*L)*M*rho_A^2*"
                "[1+q_rho,I+eta*ell_cross(I)]"
            ),
            "normalizedBound": (
                "C*nu^-2*exp(2*lambda0*L)*(M/Ks)*eta^(4/3)*"
                "chi*(Omega^2/Kv)^(1/3)*[1+q+eta*ell_cross]"
            ),
            "chi": "rho_A^2/Omega^2",
            "equalCarrierMPower": "-10/3",
            "phaseBoundary": "alpha<min(5/2,(10+3*beta)/7)",
        },
        "constants": constants,
        "phaseBoundary": phases,
        "equalCarrierLedger": {
            "fittedTailPower": mtext(equal_tail_power),
            "expectedPower": "-10/3",
            "rows": equal_rows,
        },
        "comparableAmplitudeLedger": {
            "family": "z_l=1.25 on odd l and z_l=0.75 on even l",
            "uniformEnvelope": {
                "chiUpper": "(c_plus/c_minus)^2/(2M)",
                "OmegaSquaredOverKvUpper": "12*Kz^2*(c_plus/c_minus)^2/M",
            },
            "fittedTailPower": mtext(comparable_tail_power),
            "expectedPower": "-10/3",
            "rows": comparable_rows,
        },
        "mixedExposure": {
            "role": "non-rigorous high-precision quadrature corroboration of analytic Cauchy bounds",
            "rows": exposure_rows,
        },
        "besselNoGo": {
            "definitions": {
                "Theta": "L_R*Gamma_fr,R with Gamma_fr,R=R^2/(log R)^2",
                "Xi": "2*R^4*[L_R-(1-exp(-L_R))]",
                "energyLossUpper": "[4*T_R+4*T_R^2+(8/3)*T_R^3]/R^4",
            },
            "tailPowers": bessel_powers,
            "rows": bessel_rows,
            "enhancedDissipationScope": (
                "A positive burn-in can estimate only the remaining tail ledger. "
                "It does not erase slope mass accumulated before burn-in."
            ),
        },
        "checks": checks,
        "scope": {
            "analyticProofInJson": False,
            "intervalArithmetic": False,
            "finiteMatrixDNS": False,
            "provesNSERegularity": False,
            "constructsNormalizedLowerFamily": False,
            "note": (
                "The certificate checks identities, constants, asymptotic diagnostics, "
                "and representative quadrature. The report carries the analytic proof."
            ),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }
    if not all_passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"producer checks failed: {failed}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    progress(
        args.progress_log,
        "producer-complete",
        allPassed=all_passed,
        elapsedSeconds=payload["elapsedSeconds"],
    )
    resource_snapshot(
        args.resource_log,
        "producer-complete",
        started,
        allPassed=all_passed,
    )
    emit(f"R0.72B producer audit passed in {payload['elapsedSeconds']:.2f}s")


if __name__ == "__main__":
    main()
