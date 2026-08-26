#!/usr/bin/env python3
"""Producer audit for the R0.72C physical-phase carrier theorem.

The analytic proof belongs in ``research/r072c_report-source.md``.  This
program independently reconstructs the finite algebra behind that proof:
the failure of a naive complexification, the conjugate-paired skew identity,
the joint phase inequality, the three heat-participation regimes, the phase
boundaries, and the two sharp algebraic families.  All transcendental
calculations use high-precision ``mpmath`` arithmetic.  The output is a
corroborating certificate, not interval arithmetic or an NSE regularity
proof.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import json
import os
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Iterable

import mpmath as mp


MP_DIGITS = 90
mp.mp.dps = MP_DIGITS

K_Z = mp.mpf("1")
KAPPA = mp.mpf("1")
FIXED_T = mp.mpf("0.01")
H_M_VALUES = tuple(2**power for power in range(5, 13))
RS_GENERATIONS = tuple(range(0, 14))
ODD_RS_GENERATIONS = tuple(range(1, 14, 2))
FIXED_A_M_VALUES = tuple(2**power for power in range(4, 14))


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


def mtext(value: mp.mpf | mp.mpc, digits: int = 45) -> str:
    return mp.nstr(value, digits, strip_zeros=False)


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def max_matrix_abs(matrix: mp.matrix) -> mp.mpf:
    return max(abs(matrix[row, column]) for row in range(matrix.rows) for column in range(matrix.cols))


def adjoint(matrix: mp.matrix) -> mp.matrix:
    return matrix.transpose_conj()


def vector_inner(left: mp.matrix, right: mp.matrix) -> mp.mpc:
    return (adjoint(left) * right)[0]


def shift_matrices(radius: int) -> tuple[mp.matrix, mp.matrix]:
    dimension = 2 * radius + 1
    forward = mp.zeros(dimension)
    for index in range(dimension - 1):
        forward[index + 1, index] = 1
    backward = forward.transpose()
    return forward, backward


def complex_model_ledger() -> dict[str, object]:
    """Rebuild the naive counterexample and the physical skew pairing."""

    radius = 2
    forward, backward = shift_matrices(radius)
    adjacency = forward + backward
    imaginary_unit = mp.mpc(0, 1)

    naive_coefficient = imaginary_unit
    naive = -imaginary_unit * naive_coefficient * adjacency
    naive_skew_defect = max_matrix_abs(adjoint(naive) + naive)

    state = mp.zeros(2 * radius + 1, 1)
    state[radius, 0] = 1 / mp.sqrt(2)
    state[radius + 1, 0] = 1 / mp.sqrt(2)
    state_norm_defect = abs(vector_inner(state, state) - 1)
    naive_expectation = mp.re(vector_inner(state, naive * state))

    lambda_zero = mp.mpf("1")
    lambda_one = mp.mpf("3")
    delta = mp.mpf("3")
    half_energy_derivative = (
        -(lambda_zero + lambda_one) / 2 + delta * naive_expectation
    )

    physical_coefficient = mp.mpc("0.6", "0.8")
    paired = -imaginary_unit * (
        physical_coefficient * forward
        + mp.conj(physical_coefficient) * backward
    )
    paired_skew_defect = max_matrix_abs(adjoint(paired) + paired)
    paired_energy_coupling = abs(mp.re(vector_inner(state, paired * state)))

    theta = mp.mpf("0.731")
    multiplier = -imaginary_unit * (
        physical_coefficient * mp.e ** (imaginary_unit * theta)
        + mp.conj(physical_coefficient) * mp.e ** (-imaginary_unit * theta)
    )
    multiplier_real_part = abs(mp.re(multiplier))

    return {
        "dimension": 2 * radius + 1,
        "naiveCoefficient": "i",
        "naiveSkewDefect": mtext(naive_skew_defect),
        "stateNormDefect": mtext(state_norm_defect),
        "naiveCouplingExpectation": mtext(naive_expectation),
        "lambda0": mtext(lambda_zero),
        "lambda1": mtext(lambda_one),
        "delta": mtext(delta),
        "halfEnergyDerivative": mtext(half_energy_derivative),
        "physicalCoefficient": {
            "real": mtext(mp.re(physical_coefficient)),
            "imaginary": mtext(mp.im(physical_coefficient)),
        },
        "pairedSkewDefect": mtext(paired_skew_defect),
        "pairedEnergyCoupling": mtext(paired_energy_coupling),
        "sampleMultiplierRealPart": mtext(multiplier_real_part),
    }


def joint_inequality_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rho = mp.mpf("1.75")
    carrier_moment = mp.mpf("13.5")
    for multiplier_ratio in (
        mp.mpf("1"),
        mp.mpf("1.125"),
        mp.mpf("1.5"),
        mp.mpf("2"),
        mp.mpf("5"),
    ):
        omega = multiplier_ratio * rho
        chi = rho**2 / omega**2
        left = chi * mp.root(omega**2 / carrier_moment, 3)
        right = mp.root(rho**2 / carrier_moment, 3)
        ratio = left / right
        exact_ratio = multiplier_ratio ** (-mp.mpf(4) / 3)
        rows.append(
            {
                "OmegaOverRho": mtext(multiplier_ratio),
                "chi": mtext(chi),
                "jointLeft": mtext(left),
                "phaseFreeRight": mtext(right),
                "leftOverRight": mtext(ratio),
                "expectedRatio": mtext(exact_ratio),
                "identityResidual": mtext(abs(ratio - exact_ratio)),
            }
        )
    return rows


def heat_sum(m_value: int, t_value: mp.mpf) -> mp.mpf:
    return mp.fsum(
        mp.exp(-2 * t_value * index**2)
        for index in range(1, m_value + 1)
    )


def single_heat_sum(m_value: int, t_value: mp.mpf) -> mp.mpf:
    return mp.fsum(
        mp.exp(-t_value * index**2)
        for index in range(1, m_value + 1)
    )


def infinite_single_heat_sum(t_value: mp.mpf) -> mp.mpf:
    total = mp.mpf("0")
    index = 1
    threshold = mp.mpf(10) ** (-(MP_DIGITS - 15))
    while True:
        term = mp.exp(-t_value * index**2)
        total += term
        if term < threshold:
            return total
        index += 1


def heat_scale_ledger() -> dict[str, object]:
    subcarrier: list[dict[str, object]] = []
    critical: list[dict[str, object]] = []
    effective: list[dict[str, object]] = []
    critical_c = mp.mpf("0.75")
    critical_limit = mp.quad(
        lambda value: mp.exp(-2 * critical_c * value**2), [0, 1]
    )
    theta_constant = mp.sqrt(mp.pi) / (2 * mp.sqrt(2))

    for m_value in H_M_VALUES:
        m = mp.mpf(m_value)

        t_sub = m ** (-3)
        h_sub = heat_sum(m_value, t_sub)
        subcarrier.append(
            {
                "M": m_value,
                "t": mtext(t_sub),
                "tM2": mtext(t_sub * m**2),
                "H": mtext(h_sub),
                "HOverM": mtext(h_sub / m),
                "defectFromOne": mtext(abs(h_sub / m - 1)),
            }
        )

        t_critical = critical_c / m**2
        h_critical = heat_sum(m_value, t_critical)
        critical.append(
            {
                "M": m_value,
                "c": mtext(critical_c),
                "t": mtext(t_critical),
                "HOverM": mtext(h_critical / m),
                "riemannLimit": mtext(critical_limit),
                "absoluteDefect": mtext(abs(h_critical / m - critical_limit)),
            }
        )

        t_effective = m ** (-mp.mpf(3) / 2)
        h_effective = heat_sum(m_value, t_effective)
        normalized = h_effective * mp.sqrt(t_effective)
        effective.append(
            {
                "M": m_value,
                "t": mtext(t_effective),
                "tM2": mtext(t_effective * m**2),
                "H": mtext(h_effective),
                "sqrtTtimesH": mtext(normalized),
                "thetaLimit": mtext(theta_constant),
                "absoluteDefect": mtext(abs(normalized - theta_constant)),
            }
        )

    return {
        "definition": "H_M(t)=sum_(j=1)^M exp(-2*t*j^2)",
        "subcarrier": {
            "rule": "t_M=M^-3, so t_M*M^2 -> 0",
            "rows": subcarrier,
        },
        "critical": {
            "rule": "t_M=c/M^2 with c=3/4",
            "limit": "integral_0^1 exp(-2*c*s^2) ds",
            "rows": critical,
        },
        "effectiveCarrier": {
            "rule": "t_M=M^-3/2, so t_M->0 and t_M*M^2->infinity",
            "limit": "sqrt(t_M)*H_M(t_M) -> sqrt(pi)/(2*sqrt(2))",
            "rows": effective,
        },
    }


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def phase_boundary_ledger() -> list[dict[str, object]]:
    regimes = (
        ("exact-launch-phase-uniform", Fraction(8, 3), "sigma>=2"),
        ("transition-sigma-one", Fraction(17, 6), "sigma=1"),
        ("fixed-positive-layer", Fraction(3), "sigma=0"),
    )
    beta_values = (
        Fraction(0),
        Fraction(1, 2),
        Fraction(1),
        Fraction(2),
        Fraction(9, 4),
        Fraction(3),
    )
    rows: list[dict[str, object]] = []
    for name, power, scale in regimes:
        cap = 3 * power / 4
        for beta in beta_values:
            exposure = (3 * power + 3 * beta) / 7
            certified = min(cap, exposure)
            rows.append(
                {
                    "regime": name,
                    "scale": scale,
                    "p": fraction_text(power),
                    "beta": fraction_text(beta),
                    "constantTermBoundary": fraction_text(cap),
                    "localExposureBoundary": fraction_text(exposure),
                    "certifiedAlphaBoundary": fraction_text(certified),
                    "certifiedAlphaBoundaryDecimal": float(certified),
                }
            )
    return rows


def rudin_shapiro_coefficients(generation: int) -> tuple[list[int], list[int]]:
    p_coefficients = [1]
    q_coefficients = [1]
    for _ in range(generation):
        old_p = p_coefficients
        old_q = q_coefficients
        p_coefficients = old_p + old_q
        q_coefficients = old_p + [-value for value in old_q]
    return p_coefficients, q_coefficients


def binary_eleven_sign(index: int) -> int:
    return -1 if (index & (index >> 1)).bit_count() % 2 else 1


def polynomial_value(coefficients: Iterable[int], value: mp.mpc) -> mp.mpc:
    result = mp.mpc(0)
    for coefficient in reversed(list(coefficients)):
        result = result * value + coefficient
    return result


def rudin_shapiro_ledger() -> dict[str, object]:
    coefficient_rows: list[dict[str, object]] = []
    maximum_identity_residual = mp.mpf("0")
    sample_angles = (
        mp.mpf("0"),
        mp.pi / 17,
        mp.pi / 7,
        mp.pi / 3,
        mp.mpf("1.731"),
    )

    for generation in RS_GENERATIONS:
        p_coefficients, q_coefficients = rudin_shapiro_coefficients(generation)
        expected = [binary_eleven_sign(index) for index in range(2**generation)]
        binary_match = p_coefficients == expected
        generation_residual = mp.mpf("0")
        for angle in sample_angles:
            point = mp.e ** (mp.j * angle)
            p_value = polynomial_value(p_coefficients, point)
            q_value = polynomial_value(q_coefficients, point)
            residual = abs(abs(p_value) ** 2 + abs(q_value) ** 2 - 2 ** (generation + 1))
            generation_residual = max(generation_residual, residual)
        maximum_identity_residual = max(
            maximum_identity_residual, generation_residual
        )
        coefficient_rows.append(
            {
                "generation": generation,
                "M": 2**generation,
                "binaryElevenMatch": binary_match,
                "allCoefficientsAreSigns": all(
                    abs(value) == 1 for value in p_coefficients + q_coefficients
                ),
                "PAtOne": sum(p_coefficients),
                "QAtOne": sum(q_coefficients),
                "maximumParallelogramResidual": mtext(generation_residual),
            }
        )

    odd_rows: list[dict[str, object]] = []
    prefactors: list[mp.mpf] = []
    m_values: list[mp.mpf] = []
    for generation in ODD_RS_GENERATIONS:
        p_coefficients, _ = rudin_shapiro_coefficients(generation)
        m_value = 2**generation
        m = mp.mpf(m_value)
        carrier_sum = mp.mpf(m_value * (m_value + 1) * (2 * m_value + 1) // 6)
        p_at_one = mp.mpf(sum(p_coefficients))
        exact_endpoint = mp.sqrt(2 * m)
        omega_lower = 2 * abs(K_Z) * p_at_one
        omega_upper = 2 * abs(K_Z) * mp.sqrt(2 * m)
        rho_squared = 2 * K_Z**2 * m
        chi = rho_squared / omega_upper**2
        prefactor = (
            (m / carrier_sum)
            * chi
            * mp.root(omega_upper**2 / carrier_sum, 3)
        )
        closed_prefactor = (
            abs(K_Z) ** (mp.mpf(2) / 3)
            / 2
            * (m / carrier_sum) ** (mp.mpf(4) / 3)
        )
        prefactors.append(prefactor)
        m_values.append(m)
        odd_rows.append(
            {
                "generation": generation,
                "M": m_value,
                "PAtOne": mtext(p_at_one),
                "sqrtTwoM": mtext(exact_endpoint),
                "endpointResidual": mtext(abs(p_at_one - exact_endpoint)),
                "OmegaLowerAtThetaZero": mtext(omega_lower),
                "OmegaUpperFromRudinShapiro": mtext(omega_upper),
                "OmegaIdentityResidual": mtext(abs(omega_lower - omega_upper)),
                "rhoSquared": mtext(rho_squared),
                "chi": mtext(chi),
                "Phi": mtext(prefactor),
                "closedPhi": mtext(closed_prefactor),
                "PhiIdentityResidual": mtext(abs(prefactor - closed_prefactor)),
                "MToEightThirdsTimesPhi": mtext(
                    m ** (mp.mpf(8) / 3) * prefactor
                ),
            }
        )

    # Odd generations multiply M by four.  The last three exact rows already
    # isolate the S_M=M^3/3+O(M^2) correction to within the declared gate.
    tail_power = regression_power(m_values[-3:], prefactors[-3:])
    asymptotic_constant = (
        mp.mpf("0.5") * 3 ** (mp.mpf(4) / 3) * abs(K_Z) ** (mp.mpf(2) / 3)
    )
    return {
        "recursion": {
            "Pnext": "P_n + z^(2^n) Q_n",
            "Qnext": "P_n - z^(2^n) Q_n",
            "binaryRule": "epsilon_j=(-1)^(number of overlapping 11 blocks in binary j)",
            "rows": coefficient_rows,
            "maximumParallelogramResidual": mtext(maximum_identity_residual),
        },
        "oddGenerationExactFamily": {
            "rule": "M=2^n with odd n, r_l=l, w_l=epsilon_(l-1)",
            "expectedPower": "-8/3",
            "fittedTailPower": mtext(tail_power),
            "asymptoticScaledConstant": mtext(asymptotic_constant),
            "rows": odd_rows,
        },
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
    denominator = mp.fsum((value - mean_x) ** 2 for value in log_x)
    return numerator / denominator


def fixed_positive_ledger() -> dict[str, object]:
    rows: list[dict[str, object]] = []
    prefactors: list[mp.mpf] = []
    m_values: list[mp.mpf] = []
    for m_value in FIXED_A_M_VALUES:
        m = mp.mpf(m_value)
        carrier_sum = mp.mpf(m_value * (m_value + 1) * (2 * m_value + 1) // 6)
        h_sum = single_heat_sum(m_value, FIXED_T)
        j_sum = heat_sum(m_value, FIXED_T)
        omega = 2 * abs(K_Z) * h_sum
        rho_squared = 2 * K_Z**2 * j_sum
        chi = rho_squared / omega**2
        direct = (
            (m / carrier_sum)
            * chi
            * mp.root(omega**2 / carrier_sum, 3)
        )
        closed = (
            2 ** (-mp.mpf(1) / 3)
            * abs(K_Z) ** (mp.mpf(2) / 3)
            * m
            * j_sum
            / (carrier_sum ** (mp.mpf(4) / 3) * h_sum ** (mp.mpf(4) / 3))
        )
        prefactors.append(direct)
        m_values.append(m)
        rows.append(
            {
                "M": m_value,
                "t": mtext(FIXED_T),
                "H": mtext(h_sum),
                "J": mtext(j_sum),
                "Omega": mtext(omega),
                "rhoSquared": mtext(rho_squared),
                "chi": mtext(chi),
                "Phi": mtext(direct),
                "closedPhi": mtext(closed),
                "formulaResidual": mtext(abs(direct - closed)),
                "M3TimesPhi": mtext(m**3 * direct),
            }
        )

    h_infinite = infinite_single_heat_sum(FIXED_T)
    j_infinite = infinite_single_heat_sum(2 * FIXED_T)
    scaled_limit = (
        2 ** (-mp.mpf(1) / 3)
        * 3 ** (mp.mpf(4) / 3)
        * abs(K_Z) ** (mp.mpf(2) / 3)
        * j_infinite
        / h_infinite ** (mp.mpf(4) / 3)
    )
    tail_power = regression_power(m_values[-5:], prefactors[-5:])
    return {
        "rule": "fixed t=kappa*A=0.01, r_l=l, w_l=1",
        "expectedPower": "-3",
        "fittedTailPower": mtext(tail_power),
        "HInfinite": mtext(h_infinite),
        "JInfinite": mtext(j_infinite),
        "asymptoticM3TimesPhi": mtext(scaled_limit),
        "rows": rows,
    }


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    emit("R0.72C producer audit started")
    progress(args.progress_log, "producer-start", mpDigits=MP_DIGITS)
    resource_snapshot(args.resource_log, "producer-start", started)

    complex_models = complex_model_ledger()
    emit("naive and conjugate-paired complex models reconstructed")
    progress(args.progress_log, "complex-models-complete")

    joint_rows = joint_inequality_rows()
    heat_scales = heat_scale_ledger()
    phase_boundaries = phase_boundary_ledger()
    emit("joint inequality, heat scales, and phase boundaries complete")
    progress(args.progress_log, "phase-free-ledger-complete")
    resource_snapshot(args.resource_log, "phase-free-ledger-complete", started)

    rudin_shapiro = rudin_shapiro_ledger()
    fixed_positive = fixed_positive_ledger()
    emit("Rudin-Shapiro and fixed-positive sharpness ledgers complete")
    progress(args.progress_log, "sharpness-ledgers-complete")

    sub_rows = heat_scales["subcarrier"]["rows"]
    critical_rows = heat_scales["critical"]["rows"]
    effective_rows = heat_scales["effectiveCarrier"]["rows"]
    recursion_rows = rudin_shapiro["recursion"]["rows"]
    odd_rows = rudin_shapiro["oddGenerationExactFamily"]["rows"]
    fixed_rows = fixed_positive["rows"]

    exact_boundary_zero = next(
        row
        for row in phase_boundaries
        if row["regime"] == "exact-launch-phase-uniform" and row["beta"] == "0"
    )
    exact_boundary_cap = next(
        row
        for row in phase_boundaries
        if row["regime"] == "exact-launch-phase-uniform" and row["beta"] == "2"
    )
    fixed_boundary_zero = next(
        row
        for row in phase_boundaries
        if row["regime"] == "fixed-positive-layer" and row["beta"] == "0"
    )
    fixed_boundary_cap = next(
        row
        for row in phase_boundaries
        if row["regime"] == "fixed-positive-layer" and row["beta"] == "9/4"
    )

    checks = [
        check(
            "naive complexification breaks the energy identity",
            mp.mpf(complex_models["naiveSkewDefect"]) == 2
            and mp.mpf(complex_models["halfEnergyDerivative"]) > 0
            and mp.mpf(complex_models["stateNormDefect"]) < mp.mpf("1e-80"),
            {
                "skewDefect": complex_models["naiveSkewDefect"],
                "halfEnergyDerivative": complex_models["halfEnergyDerivative"],
            },
            "z=i makes -i*z*(T_1+T_-1) self-adjoint and admits positive energy growth",
        ),
        check(
            "conjugate pairing is skew-adjoint",
            mp.mpf(complex_models["pairedSkewDefect"]) < mp.mpf("1e-80")
            and mp.mpf(complex_models["pairedEnergyCoupling"]) < mp.mpf("1e-80")
            and mp.mpf(complex_models["sampleMultiplierRealPart"]) < mp.mpf("1e-80"),
            {
                "skewDefect": complex_models["pairedSkewDefect"],
                "energyCoupling": complex_models["pairedEnergyCoupling"],
                "multiplierRealPart": complex_models["sampleMultiplierRealPart"],
            },
            "-i*(w*T_r+conj(w)*T_-r) is skew-adjoint and has a purely imaginary multiplier",
        ),
        check(
            "joint phase inequality closes",
            all(
                mp.mpf(row["leftOverRight"]) <= 1
                and mp.mpf(row["identityResidual"]) < mp.mpf("1e-80")
                for row in joint_rows
            ),
            mtext(max(mp.mpf(row["leftOverRight"]) for row in joint_rows)),
            "chi*(Omega^2/Kv)^(1/3) <= (rho^2/Kv)^(1/3)",
        ),
        check(
            "sub-carrier heat scale tends to M",
            mp.mpf(sub_rows[-1]["defectFromOne"]) < mp.mpf("0.001")
            and all(
                mp.mpf(later["defectFromOne"]) < mp.mpf(earlier["defectFromOne"])
                for earlier, later in zip(sub_rows[:-1], sub_rows[1:], strict=True)
            ),
            sub_rows[-1],
            "t_M*M^2->0 implies H_M(t_M)/M->1",
        ),
        check(
            "critical heat scale has the Riemann limit",
            mp.mpf(critical_rows[-1]["absoluteDefect"]) < mp.mpf("0.001")
            and all(
                mp.mpf(later["absoluteDefect"]) < mp.mpf(earlier["absoluteDefect"])
                for earlier, later in zip(critical_rows[:-1], critical_rows[1:], strict=True)
            ),
            critical_rows[-1],
            "t_M*M^2->c implies H_M/M->integral_0^1 exp(-2*c*s^2) ds",
        ),
        check(
            "effective-carrier heat scale has the theta limit",
            mp.mpf(effective_rows[-1]["absoluteDefect"]) < mp.mpf("0.002")
            and all(
                mp.mpf(later["absoluteDefect"]) < mp.mpf(earlier["absoluteDefect"])
                for earlier, later in zip(effective_rows[:-1], effective_rows[1:], strict=True)
            ),
            effective_rows[-1],
            "t_M->0 and t_M*M^2->infinity imply sqrt(t_M)*H_M->sqrt(pi)/(2*sqrt(2))",
        ),
        check(
            "phase boundary endpoints are exact",
            exact_boundary_zero["certifiedAlphaBoundary"] == "8/7"
            and exact_boundary_cap["certifiedAlphaBoundary"] == "2"
            and fixed_boundary_zero["certifiedAlphaBoundary"] == "9/7"
            and fixed_boundary_cap["certifiedAlphaBoundary"] == "9/4",
            {
                "exactBetaZero": exact_boundary_zero["certifiedAlphaBoundary"],
                "exactCap": exact_boundary_cap["certifiedAlphaBoundary"],
                "fixedBetaZero": fixed_boundary_zero["certifiedAlphaBoundary"],
                "fixedCap": fixed_boundary_cap["certifiedAlphaBoundary"],
            },
            "alpha<min(3p/4,(3p+3beta)/7) for p=8/3 and p=3",
        ),
        check(
            "Rudin-Shapiro recursion equals the binary-eleven rule",
            all(
                bool(row["binaryElevenMatch"])
                and bool(row["allCoefficientsAreSigns"])
                for row in recursion_rows
            ),
            {"generationCount": len(recursion_rows), "terminalM": recursion_rows[-1]["M"]},
            "recursive P_n coefficients equal (-1)^(overlapping binary 11 count)",
        ),
        check(
            "Rudin-Shapiro parallelogram identity",
            mp.mpf(rudin_shapiro["recursion"]["maximumParallelogramResidual"])
            < mp.mpf("1e-75"),
            rudin_shapiro["recursion"]["maximumParallelogramResidual"],
            "|P_n(z)|^2+|Q_n(z)|^2=2^(n+1) on the unit circle",
        ),
        check(
            "odd Rudin-Shapiro generations have exact Omega and chi",
            all(
                mp.mpf(row["endpointResidual"]) < mp.mpf("1e-80")
                and mp.mpf(row["OmegaIdentityResidual"]) < mp.mpf("1e-80")
                and abs(mp.mpf(row["chi"]) - mp.mpf("0.25")) < mp.mpf("1e-80")
                for row in odd_rows
            ),
            odd_rows[-1],
            "odd n gives P_n(1)=sqrt(2M), Omega=2|Kz|sqrt(2M), and chi=1/4",
        ),
        check(
            "Rudin-Shapiro sharp prefactor has power minus eight-thirds",
            all(mp.mpf(row["PhiIdentityResidual"]) < mp.mpf("1e-80") for row in odd_rows)
            and abs(
                mp.mpf(rudin_shapiro["oddGenerationExactFamily"]["fittedTailPower"])
                + mp.mpf(8) / 3
            )
            < mp.mpf("0.002"),
            {
                "fittedPower": rudin_shapiro["oddGenerationExactFamily"]["fittedTailPower"],
                "terminalScaledPhi": odd_rows[-1]["MToEightThirdsTimesPhi"],
            },
            "Phi=(|Kz|^(2/3)/2)*(M/S_M)^(4/3)=Theta(M^-8/3)",
        ),
        check(
            "fixed-positive same-sign formula has power minus three",
            all(mp.mpf(row["formulaResidual"]) < mp.mpf("1e-80") for row in fixed_rows)
            and abs(mp.mpf(fixed_positive["fittedTailPower"]) + 3) < mp.mpf("0.002")
            and abs(
                mp.mpf(fixed_rows[-1]["M3TimesPhi"])
                - mp.mpf(fixed_positive["asymptoticM3TimesPhi"])
            )
            < mp.mpf("0.001"),
            {
                "fittedPower": fixed_positive["fittedTailPower"],
                "terminalScaledPhi": fixed_rows[-1]["M3TimesPhi"],
                "limit": fixed_positive["asymptoticM3TimesPhi"],
            },
            "Phi=2^(-1/3)|Kz|^(2/3) M J/(S_M^(4/3) H^(4/3))=Theta(M^-3)",
        ),
    ]

    all_passed = all(bool(row["passed"]) for row in checks)
    payload = {
        "schemaVersion": "r072c-physical-phase-producer-v1",
        "release": "R0.72C",
        "generatedAtUtc": utc_now(),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "arithmetic": {
            "engine": "mpmath arbitrary precision",
            "decimalDigits": MP_DIGITS,
            "intervalArithmetic": False,
            "role": "high-precision finite algebra and asymptotic corroboration",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "mpmath": mp.__version__,
        },
        "parameters": {
            "Kz": mtext(K_Z),
            "kappa": mtext(KAPPA),
            "fixedT": mtext(FIXED_T),
            "heatMValues": list(H_M_VALUES),
            "rudinShapiroGenerations": list(RS_GENERATIONS),
            "oddRudinShapiroGenerations": list(ODD_RS_GENERATIONS),
            "fixedAMValues": list(FIXED_A_M_VALUES),
            "randomness": False,
        },
        "analyticLedger": {
            "physicalPairing": "-i*Kz*[w_l*T_(r_l)+conj(w_l)*T_(-r_l)]",
            "jointInequality": "chi*(Omega^2/Kv)^(1/3)<=(rho_A^2/Kv)^(1/3)",
            "uniformPrefactor": "Phi_A,M<=C*M^-3*H_M(A0)^(1/3)",
            "exactLaunchPower": "-8/3",
            "fixedPositivePower": "-3",
            "exactLaunchPhaseBoundary": "alpha<min(2,(8+3*beta)/7)",
            "fixedPositivePhaseBoundary": "alpha<min(9/4,(9+3*beta)/7)",
        },
        "complexModels": complex_models,
        "jointInequality": {"rows": joint_rows},
        "heatParticipation": heat_scales,
        "phaseBoundaries": phase_boundaries,
        "rudinShapiro": rudin_shapiro,
        "fixedPositiveSharpness": fixed_positive,
        "checks": checks,
        "scope": {
            "analyticProofInJson": False,
            "intervalArithmetic": False,
            "finiteMatrixDNS": False,
            "provesNSERegularity": False,
            "constructsNormalizedLowerFamily": False,
            "note": (
                "The report carries the analytic proof. This certificate checks "
                "finite identities, exact sharpness formulas, and deterministic "
                "high-precision asymptotic diagnostics."
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
        checkCount=len(checks),
        elapsedSeconds=payload["elapsedSeconds"],
    )
    resource_snapshot(
        args.resource_log,
        "producer-complete",
        started,
        allPassed=all_passed,
        checkCount=len(checks),
    )
    emit(f"R0.72C producer audit passed in {payload['elapsedSeconds']:.2f}s")


if __name__ == "__main__":
    main()
