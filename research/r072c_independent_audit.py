#!/usr/bin/env python3
"""Independent binary64 audit for the R0.72C phase-sensitive gate.

The program imports no producer module and reads no producer result.  It
reconstructs the conjugate-paired finite shear matrix, a deliberately invalid
naive complex extension, the target row, representative heat multipliers, and
two asymptotic ledgers from raw parameters.  Rudin--Shapiro coefficients are
built twice: once by the P/Q recursion and once from overlapping binary pairs.

All floating-point calculations use IEEE-754 binary64.  Dense grids, FFT
samples, finite matrices, and log regressions are corroborating computations;
they are not interval arithmetic, a proof for every generation, a proof of an
infinite lattice theorem, or a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import platform
import resource
import sys
import time

import numpy as np
from scipy.integrate import quad


# Raw parameters are deliberately local to this independent program.
NU = 0.03
D_MODULUS = 4.0
K_Y = 0.8
K_Z = 1.25
Q_VALUE = 48.0
KAPPA = NU * D_MODULUS**2
DELTA_NAIVE = 10.0
MATRIX_RADIUS = 20
MATRIX_DIMENSION = 2 * MATRIX_RADIUS + 1
TARGET_INDEX = MATRIX_RADIUS
MULTIPLIERS = np.array([1, 3, 6, 9], dtype=int)
MAGNITUDES = np.array([0.80, 1.05, 0.90, 1.20], dtype=float)
PHASES = np.array([0.20, 1.10, -0.70, 2.30], dtype=float)
COMPLEX_COEFFICIENTS = MAGNITUDES * np.exp(1j * PHASES)
REPRESENTATIVE_A0 = 0.04
REPRESENTATIVE_WINDOW = 0.30
ANGLE_GRID_SIZE = 1 << 15
RS_ODD_GENERATIONS = tuple(range(3, 20, 2))
RS_FFT_GENERATION = 11
FIXED_T = 0.036
FIXED_A_M_VALUES = tuple(2**power for power in range(4, 21))


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


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def shift(step: int) -> np.ndarray:
    """Return the truncated shift T_step e_j=e_(j+step)."""
    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    for column in range(MATRIX_DIMENSION):
        row = column + step
        if 0 <= row < MATRIX_DIMENSION:
            matrix[row, column] = 1.0
    return matrix


POSITIVE_SHIFTS = tuple(shift(int(step)) for step in MULTIPLIERS)
NEGATIVE_SHIFTS = tuple(shift(-int(step)) for step in MULTIPLIERS)


def heated_coefficients(time_value: float) -> np.ndarray:
    weights = np.exp(
        -KAPPA * MULTIPLIERS.astype(float) ** 2 * time_value
    )
    return COMPLEX_COEFFICIENTS * weights


def conjugate_paired_shear(time_value: float) -> np.ndarray:
    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    for coefficient, positive, negative in zip(
        heated_coefficients(time_value),
        POSITIVE_SHIFTS,
        NEGATIVE_SHIFTS,
        strict=True,
    ):
        matrix += coefficient * positive + coefficient.conjugate() * negative
    return -1j * K_Z * matrix


def conjugate_paired_shear_derivative(time_value: float) -> np.ndarray:
    matrix = np.zeros((MATRIX_DIMENSION, MATRIX_DIMENSION), dtype=np.complex128)
    for multiplier, coefficient, positive, negative in zip(
        MULTIPLIERS,
        heated_coefficients(time_value),
        POSITIVE_SHIFTS,
        NEGATIVE_SHIFTS,
        strict=True,
    ):
        factor = -KAPPA * float(multiplier) ** 2
        matrix += factor * (
            coefficient * positive + coefficient.conjugate() * negative
        )
    return -1j * K_Z * matrix


def diffusion_data() -> tuple[np.ndarray, np.ndarray]:
    indices = np.arange(-MATRIX_RADIUS, MATRIX_RADIUS + 1, dtype=float)
    lambdas = NU * (
        (D_MODULUS * indices + K_Y / Q_VALUE) ** 2
        + (K_Z / Q_VALUE) ** 2
    )
    return np.diag(-lambdas.astype(np.complex128)), lambdas


DIFFUSION, LAMBDAS = diffusion_data()
LAMBDA_0 = float(LAMBDAS[TARGET_INDEX])


def matrix_structure_audit() -> dict[str, object]:
    shear = conjugate_paired_shear(REPRESENTATIVE_A0)
    scale = max(float(np.linalg.norm(shear)), np.finfo(float).tiny)
    skew_defect = float(np.linalg.norm(shear + shear.conj().T) / scale)

    step = 1
    positive = shift(step)
    negative = shift(-step)
    naive = -1j * K_Z * 1j * (positive + negative)
    naive_scale = max(float(np.linalg.norm(naive)), np.finfo(float).tiny)
    naive_skew_defect = float(
        np.linalg.norm(naive + naive.conj().T) / naive_scale
    )
    naive_hermitian_defect = float(
        np.linalg.norm(naive - naive.conj().T) / naive_scale
    )

    witness = np.zeros(MATRIX_DIMENSION, dtype=np.complex128)
    witness[TARGET_INDEX] = 1.0 / math.sqrt(2.0)
    witness[TARGET_INDEX + 1] = 1.0 / math.sqrt(2.0)
    coupling_form = float(np.vdot(witness, naive @ witness).real)
    energy_derivative = float(
        np.vdot(
            witness, (DIFFUSION + DELTA_NAIVE * naive) @ witness
        ).real
    )

    target_row = shear[TARGET_INDEX, :]
    matrix_rho = float(np.linalg.norm(target_row))
    weights = np.exp(
        -KAPPA
        * MULTIPLIERS.astype(float) ** 2
        * REPRESENTATIVE_A0
    )
    analytic_rho = math.sqrt(
        2.0 * K_Z**2 * float(np.sum(MAGNITUDES**2 * weights**2))
    )
    row_relative_defect = abs(matrix_rho - analytic_rho) / analytic_rho

    identity = np.eye(MATRIX_DIMENSION, dtype=np.complex128)
    q_matrix = conjugate_paired_shear_derivative(REPRESENTATIVE_A0) + shear @ (
        DIFFUSION + LAMBDA_0 * identity
    )
    q_row = q_matrix[TARGET_INDEX, :]
    matrix_q_norm_square = float(np.vdot(q_row, q_row).real)
    manual_q_norm_square = 0.0
    coefficient_ratios: list[float] = []
    for multiplier, coefficient, weight in zip(
        MULTIPLIERS, COMPLEX_COEFFICIENTS, weights, strict=True
    ):
        minus_index = TARGET_INDEX - int(multiplier)
        plus_index = TARGET_INDEX + int(multiplier)
        factor_minus = (
            -KAPPA * float(multiplier) ** 2
            - float(LAMBDAS[minus_index])
            + LAMBDA_0
        )
        factor_plus = (
            -KAPPA * float(multiplier) ** 2
            - float(LAMBDAS[plus_index])
            + LAMBDA_0
        )
        amplitude_square = abs(coefficient) ** 2 * weight**2
        manual_q_norm_square += (
            K_Z**2
            * amplitude_square
            * (factor_minus**2 + factor_plus**2)
        )
        denominator = 3.0 * NU * D_MODULUS**2 * float(multiplier) ** 2
        coefficient_ratios.extend(
            [abs(factor_minus) / denominator, abs(factor_plus) / denominator]
        )
    q_row_relative_defect = abs(
        matrix_q_norm_square - manual_q_norm_square
    ) / manual_q_norm_square

    return {
        "conjugatePairedSkewDefect": skew_defect,
        "naiveComplexSkewDefect": naive_skew_defect,
        "naiveComplexHermitianDefect": naive_hermitian_defect,
        "naiveWitnessCouplingForm": coupling_form,
        "naiveWitnessEnergyDerivative": energy_derivative,
        "rhoFromMatrixRow": matrix_rho,
        "rhoFromParsevalFormula": analytic_rho,
        "rhoRelativeDefect": row_relative_defect,
        "qRowNormSquareFromMatrix": matrix_q_norm_square,
        "qRowNormSquareFromCoefficientModuli": manual_q_norm_square,
        "qRowRelativeDefect": q_row_relative_defect,
        "maximumQCoefficientRatio": max(coefficient_ratios),
    }


ANGLE_GRID = 2.0 * math.pi * np.arange(ANGLE_GRID_SIZE) / ANGLE_GRID_SIZE
ANGLE_BASIS = np.exp(1j * np.outer(ANGLE_GRID, MULTIPLIERS))


def multiplier_grid_norm(time_value: float) -> float:
    polynomial = ANGLE_BASIS @ heated_coefficients(time_value)
    return 2.0 * abs(K_Z) * float(np.max(np.abs(polynomial.real)))


def rho_value(time_value: float) -> float:
    weights = np.exp(
        -KAPPA * MULTIPLIERS.astype(float) ** 2 * time_value
    )
    return math.sqrt(
        2.0 * K_Z**2 * float(np.sum(MAGNITUDES**2 * weights**2))
    )


def heat_grid_audit() -> dict[str, object]:
    offsets = np.array([0.0, 0.01, 0.03, 0.07, 0.15, 0.30, 0.60])
    times = REPRESENTATIVE_A0 + offsets
    norms = [multiplier_grid_norm(float(value)) for value in times]
    rho_a = rho_value(REPRESENTATIVE_A0)
    omega_a = norms[0]
    ell_integral, quadrature_error = quad(
        lambda value: rho_value(value) * multiplier_grid_norm(value),
        REPRESENTATIVE_A0,
        REPRESENTATIVE_A0 + REPRESENTATIVE_WINDOW,
        epsabs=2.0e-10,
        epsrel=2.0e-9,
        limit=80,
    )
    ell_cross = ell_integral / (rho_a * omega_a)
    c_kappa = math.pi**2 / (math.sqrt(45.0) * KAPPA)
    c_cross = math.sqrt(c_kappa / (2.0 * KAPPA))
    return {
        "times": times.tolist(),
        "gridNorms": norms,
        "maximumLaterOverInitial": max(norms[1:]) / norms[0],
        "rhoA": rho_a,
        "omegaAFromGrid": omega_a,
        "chiAFromGrid": rho_a**2 / omega_a**2,
        "ellCrossFromGridQuadrature": ell_cross,
        "quadratureAbsoluteErrorEstimate": quadrature_error,
        "windowLength": REPRESENTATIVE_WINDOW,
        "Ckappa": c_kappa,
        "Ccross": c_cross,
        "mixedConstantIdentityDefect": abs(
            2.0 * KAPPA * c_cross**2 - c_kappa
        ),
    }


def rudin_shapiro_recursive(generation: int) -> tuple[np.ndarray, np.ndarray]:
    p = np.array([1], dtype=np.int8)
    q = np.array([1], dtype=np.int8)
    for _ in range(generation):
        p, q = np.concatenate((p, q)), np.concatenate((p, -q))
    return p, q


def rudin_shapiro_binary(generation: int) -> np.ndarray:
    count = 1 << generation
    values = np.empty(count, dtype=np.int8)
    for index in range(count):
        overlapping_pairs = (index & (index >> 1)).bit_count()
        values[index] = -1 if overlapping_pairs % 2 else 1
    return values


def sum_of_squares(count: int) -> int:
    return count * (count + 1) * (2 * count + 1) // 6


def rudin_shapiro_audit() -> tuple[list[dict[str, object]], dict[str, object]]:
    rows: list[dict[str, object]] = []
    all_paths_equal = True
    all_odd_sums_exact = True
    all_norm_identities_exact = True
    for generation in RS_ODD_GENERATIONS:
        p, q = rudin_shapiro_recursive(generation)
        binary = rudin_shapiro_binary(generation)
        count = int(p.size)
        paths_equal = bool(np.array_equal(p, binary))
        p_sum = int(np.sum(p, dtype=np.int64))
        q_sum = int(np.sum(q, dtype=np.int64))
        expected_sum_square = 2 * count
        odd_sum_exact = p_sum**2 == expected_sum_square and q_sum == 0
        p_integer = p.astype(np.int64)
        q_integer = q.astype(np.int64)
        coefficient_energy_exact = (
            int(np.vdot(p_integer, p_integer)) == count
            and int(np.vdot(q_integer, q_integer)) == count
        )
        all_paths_equal = all_paths_equal and paths_equal
        all_odd_sums_exact = all_odd_sums_exact and odd_sum_exact
        all_norm_identities_exact = (
            all_norm_identities_exact and coefficient_energy_exact
        )

        k_s = sum_of_squares(count)
        rho_squared = 2.0 * K_Z**2 * count
        omega_squared = 8.0 * K_Z**2 * count
        chi = rho_squared / omega_squared
        normalized_prefactor = (
            count / k_s
            * chi
            * (omega_squared / k_s) ** (1.0 / 3.0)
        )
        rows.append(
            {
                "generation": generation,
                "M": count,
                "recursiveEqualsBinaryPath": paths_equal,
                "coefficientEnergyExact": coefficient_energy_exact,
                "sumP": p_sum,
                "sumQ": q_sum,
                "sumPSquaredOver2M": p_sum**2 / expected_sum_square,
                "rhoSquared": rho_squared,
                "omegaSquared": omega_squared,
                "chi": chi,
                "Ks": k_s,
                "Kv": k_s,
                "normalizedGeometricPrefactor": normalized_prefactor,
                "MToEightThirdsTimesPrefactor": (
                    count ** (8.0 / 3.0) * normalized_prefactor
                ),
            }
        )

    tail = rows[-5:]
    fitted_power = float(
        np.polyfit(
            np.log([float(row["M"]) for row in tail]),
            np.log(
                [
                    float(row["normalizedGeometricPrefactor"])
                    for row in tail
                ]
            ),
            1,
        )[0]
    )

    fft_p, fft_q = rudin_shapiro_recursive(RS_FFT_GENERATION)
    count = int(fft_p.size)
    fft_size = 1 << math.ceil(math.log2(8 * (count + 1)))
    p_coefficients = np.zeros(fft_size, dtype=np.complex128)
    q_coefficients = np.zeros(fft_size, dtype=np.complex128)
    p_coefficients[1 : count + 1] = fft_p
    q_coefficients[1 : count + 1] = fft_q
    p_values = np.fft.ifft(p_coefficients) * fft_size
    q_values = np.fft.ifft(q_coefficients) * fft_size
    sampled_identity_defect = float(
        np.max(np.abs(np.abs(p_values) ** 2 + np.abs(q_values) ** 2 - 2 * count))
    )
    sampled_complex_max = float(np.max(np.abs(p_values)))
    sampled_real_max = float(np.max(np.abs(p_values.real)))
    fft_summary = {
        "generation": RS_FFT_GENERATION,
        "M": count,
        "fftGridSize": fft_size,
        "sampledPQIdentityAbsoluteDefect": sampled_identity_defect,
        "sampledComplexMaxOverSqrt2M": sampled_complex_max
        / math.sqrt(2.0 * count),
        "sampledRealMaxOverSqrt2M": sampled_real_max
        / math.sqrt(2.0 * count),
        "allRecursiveBinaryPathsEqual": all_paths_equal,
        "allOddGenerationSumsExact": all_odd_sums_exact,
        "allCoefficientEnergiesExact": all_norm_identities_exact,
        "fittedTailPower": fitted_power,
        "expectedPower": -8.0 / 3.0,
    }
    return rows, fft_summary


def fixed_positive_layer_audit() -> tuple[list[dict[str, object]], float]:
    rows: list[dict[str, object]] = []
    for count in FIXED_A_M_VALUES:
        indices = np.arange(1, count + 1, dtype=float)
        heat_sum = float(np.sum(np.exp(-FIXED_T * indices**2)))
        heat_square_sum = float(np.sum(np.exp(-2.0 * FIXED_T * indices**2)))
        k_s = sum_of_squares(count)
        rho_squared = 2.0 * K_Z**2 * heat_square_sum
        omega_squared = 4.0 * K_Z**2 * heat_sum**2
        chi = rho_squared / omega_squared
        normalized_prefactor = (
            count / k_s
            * chi
            * (omega_squared / k_s) ** (1.0 / 3.0)
        )
        rows.append(
            {
                "M": count,
                "tEqualsKappaA0": FIXED_T,
                "heatL1": heat_sum,
                "heatL2Squared": heat_square_sum,
                "rhoSquared": rho_squared,
                "omegaSquared": omega_squared,
                "chi": chi,
                "Ks": k_s,
                "Kv": k_s,
                "normalizedGeometricPrefactor": normalized_prefactor,
                "MToThirdTimesPrefactor": count**3 * normalized_prefactor,
            }
        )
    tail = rows[-6:]
    fitted_power = float(
        np.polyfit(
            np.log([float(row["M"]) for row in tail]),
            np.log(
                [
                    float(row["normalizedGeometricPrefactor"])
                    for row in tail
                ]
            ),
            1,
        )[0]
    )
    return rows, fitted_power


def phase_boundary(exponent: float, beta: float) -> float:
    return min(3.0 * exponent / 4.0, (3.0 * exponent + 3.0 * beta) / 7.0)


def phase_boundary_audit() -> list[dict[str, float]]:
    rows: list[dict[str, float]] = []
    for beta in (0.0, 1.0, 2.0, 2.25, 3.0):
        rows.append(
            {
                "beta": beta,
                "exactLaunchArbitraryPhase": phase_boundary(8.0 / 3.0, beta),
                "fixedPositiveLayer": phase_boundary(3.0, beta),
                "coherentExactLaunchReference": phase_boundary(
                    10.0 / 3.0, beta
                ),
            }
        )
    return rows


def main() -> None:
    args = parse_args()
    started = time.perf_counter()
    emit("R0.72C independent phase audit started")
    progress(args.progress_log, "independent-started")
    resource_snapshot(args.resource_log, "independent-started", started)

    matrix = matrix_structure_audit()
    emit("conjugate-paired and naive-complex matrix checks complete")
    progress(args.progress_log, "matrix-structure-complete")

    heat = heat_grid_audit()
    emit("representative heat-grid and mixed-exposure checks complete")
    progress(
        args.progress_log,
        "heat-grid-complete",
        maximumLaterOverInitial=heat["maximumLaterOverInitial"],
    )

    rs_rows, rs_summary = rudin_shapiro_audit()
    emit(
        "independent Rudin-Shapiro paths complete: "
        f"tail power {rs_summary['fittedTailPower']:.8f}"
    )
    progress(
        args.progress_log,
        "rudin-shapiro-complete",
        fittedPower=rs_summary["fittedTailPower"],
    )

    fixed_rows, fixed_power = fixed_positive_layer_audit()
    emit(f"fixed-positive-layer scaling complete: tail power {fixed_power:.8f}")
    progress(
        args.progress_log,
        "fixed-positive-layer-complete",
        fittedPower=fixed_power,
    )

    boundaries = phase_boundary_audit()
    exact_beta_zero = boundaries[0]["exactLaunchArbitraryPhase"]
    fixed_beta_zero = boundaries[0]["fixedPositiveLayer"]
    exact_beta_two = next(
        row["exactLaunchArbitraryPhase"]
        for row in boundaries
        if row["beta"] == 2.0
    )
    fixed_beta_two_quarter = next(
        row["fixedPositiveLayer"]
        for row in boundaries
        if row["beta"] == 2.25
    )

    checks = [
        check(
            "conjugate-paired finite matrix is skew-adjoint",
            matrix["conjugatePairedSkewDefect"] < 3.0e-15,
            matrix["conjugatePairedSkewDefect"],
            "||V+V*||/||V|| < 3e-15",
        ),
        check(
            "naive complex extension destroys contraction structure",
            matrix["naiveComplexSkewDefect"] > 1.0
            and matrix["naiveComplexHermitianDefect"] < 3.0e-15
            and matrix["naiveWitnessEnergyDerivative"] > 0.0,
            {
                "skewDefect": matrix["naiveComplexSkewDefect"],
                "hermitianDefect": matrix["naiveComplexHermitianDefect"],
                "witnessEnergyDerivative": matrix[
                    "naiveWitnessEnergyDerivative"
                ],
            },
            (
                "z=i makes the old same-coefficient pair Hermitian and "
                "admits positive energy growth"
            ),
        ),
        check(
            "conjugate-paired target row equals Parseval rho",
            matrix["rhoRelativeDefect"] < 3.0e-15,
            matrix["rhoRelativeDefect"],
            "relative target-row defect < 3e-15",
        ),
        check(
            "Q-row coefficient moduli survive conjugate pairing",
            matrix["qRowRelativeDefect"] < 5.0e-15
            and matrix["maximumQCoefficientRatio"] <= 1.0 + 3.0e-15,
            {
                "relativeDefect": matrix["qRowRelativeDefect"],
                "maximumCoefficientRatio": matrix[
                    "maximumQCoefficientRatio"
                ],
            },
            (
                "matrix Q row matches the modulus formula and each coefficient "
                "obeys the 3 nu d^2 r^2 envelope"
            ),
        ),
        check(
            "representative heat multiplier contracts on the direct grid",
            heat["maximumLaterOverInitial"] <= 1.0 + 2.0e-13,
            heat["maximumLaterOverInitial"],
            "all later sampled L-infinity norms do not exceed the A0 grid norm",
        ),
        check(
            "representative mixed exposure obeys both declared bounds",
            heat["ellCrossFromGridQuadrature"]
            <= min(heat["windowLength"], heat["Ccross"]) + 2.0e-9
            and heat["mixedConstantIdentityDefect"] < 2.0e-15,
            {
                "ellCross": heat["ellCrossFromGridQuadrature"],
                "bound": min(heat["windowLength"], heat["Ccross"]),
                "constantIdentityDefect": heat[
                    "mixedConstantIdentityDefect"
                ],
            },
            "ell_cross<=min(L,C_cross) and 2*kappa*C_cross^2=C_kappa",
        ),
        check(
            "Rudin-Shapiro recursion agrees with the binary path",
            bool(rs_summary["allRecursiveBinaryPathsEqual"]),
            bool(rs_summary["allRecursiveBinaryPathsEqual"]),
            "all audited odd generations agree coefficient by coefficient",
        ),
        check(
            "odd Rudin-Shapiro generations attain the exact launch endpoint",
            bool(rs_summary["allOddGenerationSumsExact"])
            and bool(rs_summary["allCoefficientEnergiesExact"])
            and abs(rs_summary["sampledRealMaxOverSqrt2M"] - 1.0) < 2.0e-13
            and rs_summary["sampledPQIdentityAbsoluteDefect"] < 2.0e-9,
            {
                "allOddSumsExact": rs_summary[
                    "allOddGenerationSumsExact"
                ],
                "sampledRealMaxOverSqrt2M": rs_summary[
                    "sampledRealMaxOverSqrt2M"
                ],
                "sampledPQIdentityDefect": rs_summary[
                    "sampledPQIdentityAbsoluteDefect"
                ],
            },
            "P_n(1)^2=2M, Q_n(1)=0, and sampled |P|^2+|Q|^2=2M",
        ),
        check(
            "Rudin-Shapiro geometric prefactor has the M^-8/3 tail",
            abs(float(rs_summary["fittedTailPower"]) + 8.0 / 3.0) < 2.5e-4,
            rs_summary["fittedTailPower"],
            "binary64 tail fit is within 2.5e-4 of -8/3",
        ),
        check(
            "fixed positive layer has the M^-3 tail",
            abs(fixed_power + 3.0) < 3.0e-5,
            fixed_power,
            "binary64 tail fit is within 3e-5 of -3",
        ),
        check(
            "phase-boundary endpoints match the joint exponents",
            abs(exact_beta_zero - 8.0 / 7.0) < 2.0e-15
            and abs(exact_beta_two - 2.0) < 2.0e-15
            and abs(fixed_beta_zero - 9.0 / 7.0) < 2.0e-15
            and abs(fixed_beta_two_quarter - 9.0 / 4.0) < 2.0e-15,
            {
                "exactLaunchBeta0": exact_beta_zero,
                "exactLaunchBeta2": exact_beta_two,
                "fixedLayerBeta0": fixed_beta_zero,
                "fixedLayerBeta9Over4": fixed_beta_two_quarter,
            },
            "p=8/3 gives min(2,(8+3 beta)/7); p=3 gives min(9/4,(9+3 beta)/7)",
        ),
    ]
    all_passed = all(bool(row["passed"]) for row in checks)

    payload = {
        "schemaVersion": "r072c-phase-sensitive-independent-v1",
        "release": "R0.72C",
        "generatedAtUtc": utc_now(),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "independence": {
            "importsProducer": False,
            "readsProducerResult": False,
            "rawParametersRepeatedLocally": True,
            "rudinShapiroSecondPath": "overlapping binary 11-pair parity",
        },
        "arithmetic": {
            "format": "IEEE-754 binary64",
            "intervalArithmetic": False,
            "linearAlgebra": "NumPy complex128 finite matrices",
            "multiplierNorm": "direct uniform angle grid",
            "polynomialAudit": "NumPy FFT samples plus exact integer recursions",
            "quadrature": "SciPy adaptive QUADPACK over grid-evaluated norms",
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
        },
        "parameters": {
            "nu": NU,
            "d": D_MODULUS,
            "kappa": KAPPA,
            "Ky": K_Y,
            "Kz": K_Z,
            "q": Q_VALUE,
            "representativeA0": REPRESENTATIVE_A0,
            "representativeWindow": REPRESENTATIVE_WINDOW,
            "multipliers": MULTIPLIERS.tolist(),
            "magnitudes": MAGNITUDES.tolist(),
            "phases": PHASES.tolist(),
            "matrixRadius": MATRIX_RADIUS,
            "matrixDimension": MATRIX_DIMENSION,
            "angleGridSize": ANGLE_GRID_SIZE,
            "fixedTEqualsKappaA0": FIXED_T,
            "randomness": False,
        },
        "matrixStructure": matrix,
        "heatGrid": heat,
        "rudinShapiro": {
            "summary": rs_summary,
            "rows": rs_rows,
            "exactFamilyFormula": (
                "Phi_M=(|Kz|^(2/3)/2)*(M/Ks)^(4/3) for odd generations"
            ),
        },
        "fixedPositiveLayer": {
            "fittedTailPower": fixed_power,
            "expectedPower": -3.0,
            "rows": fixed_rows,
        },
        "phaseBoundary": boundaries,
        "checks": checks,
        "scope": {
            "intervalArithmetic": False,
            "provesAllGenerations": False,
            "provesInfiniteLattice": False,
            "provesCompleteRootLowerBound": False,
            "provesNSERegularity": False,
            "note": (
                "Finite matrices, sampled multiplier grids, FFT values, and "
                "binary64 regressions corroborate the analytic identities only."
            ),
        },
        "elapsedSeconds": time.perf_counter() - started,
    }

    if not all_passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"independent checks failed: {failed}")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    progress(
        args.progress_log,
        "independent-complete",
        allPassed=all_passed,
        checkCount=len(checks),
        elapsedSeconds=payload["elapsedSeconds"],
    )
    resource_snapshot(
        args.resource_log,
        "independent-complete",
        started,
        allPassed=all_passed,
    )
    emit(
        f"R0.72C independent audit passed {len(checks)}/{len(checks)} "
        f"in {payload['elapsedSeconds']:.2f}s"
    )


if __name__ == "__main__":
    main()
