#!/usr/bin/env python3
"""Independent binary64 audit for the R0.71Y operator-sampling theorem.

This program imports neither r071y_exact_audit.py nor its JSON. It constructs
finite shift generators directly, checks skew-adjointness and dissipativity,
tests the root-coordinate slope inequality, and independently recomputes the
optimized lattice envelope. Finite matrices corroborate the analytic proof;
they are not DNS or a construction of growing exact roots.
"""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
from scipy.linalg import expm


NU = 0.02
D_MODULUS = 8.0
K_Y = 1.0
K_Z = 1.0
A_0 = 0.05
Q_VALUE = 64.0
N_VALUES = (1, 2, 4, 8)
RNG_SEED = 71071


def now() -> str:
    return datetime.now(ZoneInfo("Asia/Shanghai")).isoformat(timespec="seconds")


def shift_pair(radius: int, step: int) -> np.ndarray:
    size = 2 * radius + 1
    matrix = np.zeros((size, size), dtype=np.complex128)
    for column in range(size):
        for row in (column - step, column + step):
            if 0 <= row < size:
                matrix[row, column] += 1.0
    return matrix


def shear_generator(
    radius: int,
    multipliers: np.ndarray,
    coefficients: np.ndarray,
    scaled_time: float,
) -> np.ndarray:
    matrix = np.zeros((2 * radius + 1, 2 * radius + 1), dtype=np.complex128)
    for multiplier, coefficient in zip(multipliers, coefficients, strict=True):
        heat = np.exp(-NU * D_MODULUS**2 * multiplier**2 * scaled_time)
        matrix += coefficient * heat * shift_pair(radius, int(multiplier))
    return -1j * K_Z * matrix


def diffusion_generator(radius: int) -> np.ndarray:
    indices = np.arange(-radius, radius + 1, dtype=float)
    diagonal = -NU * (
        (D_MODULUS * indices + K_Y / Q_VALUE) ** 2
        + (K_Z / Q_VALUE) ** 2
    )
    return np.diag(diagonal.astype(np.complex128))


def optimizer_maximum() -> float:
    return 3.0 / 4.0 ** (4.0 / 3.0)


def minimum_lattice_cost(n_value: int) -> float:
    m_value = 2 * n_value + 1
    return float(sum(index * index for index in range(1, m_value + 1)))


def lattice_factor(n_value: int) -> float:
    m_value = 2 * n_value + 1
    return n_value * m_value / minimum_lattice_cost(n_value)


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def audit() -> dict[str, object]:
    rng = np.random.default_rng(RNG_SEED)
    rows = []
    max_skew_defect = 0.0
    max_slope_ratio = 0.0
    max_multiplier_ratio = 0.0
    max_weighted_l1_ratio = 0.0
    max_envelope_ratio = 0.0
    max_lattice_ratio = 0.0
    max_contraction_ratio = 0.0
    max_dissipative_real_part = -np.inf
    max_separated_ratio = 0.0

    for n_value in N_VALUES:
        m_value = 2 * n_value + 1
        multipliers = np.arange(1, m_value + 1, dtype=float)
        coefficients = rng.normal(size=m_value)
        radius = 4 * m_value
        shear = shear_generator(radius, multipliers, coefficients, A_0)
        diffusion = diffusion_generator(radius)
        operator_norm = float(np.linalg.norm(shear, ord=2))
        skew_defect = float(
            np.linalg.norm(shear + shear.conj().T, ord=2)
            / max(operator_norm, np.finfo(float).tiny)
        )
        max_skew_defect = max(max_skew_defect, skew_defect)

        vector = rng.normal(size=2 * radius + 1) + 1j * rng.normal(
            size=2 * radius + 1
        )
        vector[radius] = 0.0
        vector_norm = float(np.linalg.norm(vector))
        amplitude = 0.037
        root_slope = abs(amplitude * (shear @ vector)[radius])
        slope_bound = amplitude * operator_norm * vector_norm
        slope_ratio = float(root_slope / slope_bound)
        max_slope_ratio = max(max_slope_ratio, slope_ratio)

        generator = diffusion + amplitude * shear
        real_part = float(np.vdot(vector, generator @ vector).real)
        max_dissipative_real_part = max(max_dissipative_real_part, real_part)
        evolved = expm(0.01 * generator) @ vector
        contraction_ratio = float(np.linalg.norm(evolved) / vector_norm)
        max_contraction_ratio = max(max_contraction_ratio, contraction_ratio)

        heat = np.exp(-NU * D_MODULUS**2 * multipliers**2 * A_0)
        l1_upper = 2.0 * abs(K_Z) * float(np.sum(np.abs(coefficients) * heat))
        multiplier_ratio = operator_norm / l1_upper
        max_multiplier_ratio = max(max_multiplier_ratio, multiplier_ratio)

        weighted_energy = float(
            np.sum(multipliers**2 * np.abs(coefficients) ** 2)
        )
        unheated_l1 = float(np.sum(np.abs(coefficients)))
        weighted_l1_bound = np.sqrt(weighted_energy) * np.sqrt(
            np.sum(1.0 / multipliers**2)
        )
        weighted_l1_ratio = unheated_l1 / weighted_l1_bound
        max_weighted_l1_ratio = max(max_weighted_l1_ratio, weighted_l1_ratio)

        ks_value = minimum_lattice_cost(n_value)
        s_value = float(np.exp(rng.normal()))
        p_value = float(np.exp(rng.normal()))
        q_value = 128.0
        energy = s_value**2 * ks_value + p_value**2 * weighted_energy
        raw = (
            n_value
            * m_value
            * s_value**2
            * p_value**2
            * operator_norm**2
            / (q_value ** (8.0 / 3.0) * energy ** (4.0 / 3.0))
        )
        optimized = (
            n_value
            * m_value
            * optimizer_maximum()
            * (p_value / q_value**2) ** (4.0 / 3.0)
            * operator_norm**2
            / (ks_value * weighted_energy ** (1.0 / 3.0))
        )
        envelope_ratio = raw / optimized
        max_envelope_ratio = max(max_envelope_ratio, envelope_ratio)

        lattice_ratio = lattice_factor(n_value) / (3.0 / (4.0 * n_value))
        max_lattice_ratio = max(max_lattice_ratio, lattice_ratio)
        rows.append(
            {
                "N": n_value,
                "M": m_value,
                "matrixDimension": 2 * radius + 1,
                "operatorNorm": operator_norm,
                "skewDefect": skew_defect,
                "slopeRatio": slope_ratio,
                "contractionRatio": contraction_ratio,
                "multiplierL1Ratio": multiplier_ratio,
                "weightedL1Ratio": weighted_l1_ratio,
                "optimizedEnvelopeRatio": envelope_ratio,
                "latticeBoundRatio": lattice_ratio,
            }
        )

        gap = 0.03
        weighted_at_left = float(
            np.sum(
                np.abs(coefficients) ** 2
                * np.exp(
                    -2.0
                    * NU
                    * D_MODULUS**2
                    * multipliers**2
                    * A_0
                )
            )
        )
        exact_sampled_mass = 0.0
        for root_index in range(1, n_value + 1):
            root_time = A_0 + root_index * gap
            root_shear = shear_generator(
                radius, multipliers, coefficients, root_time
            )
            root_vector = rng.normal(size=2 * radius + 1) + 1j * rng.normal(
                size=2 * radius + 1
            )
            root_vector[radius] = 0.0
            root_vector *= np.sqrt(m_value) / max(
                np.linalg.norm(root_vector), np.finfo(float).tiny
            )
            exact_sampled_mass += abs((root_shear @ root_vector)[radius]) ** 2
        separated_bound = (
            2.0
            * K_Z**2
            * m_value
            * weighted_at_left
            / (2.0 * NU * D_MODULUS**2 * gap)
        )
        separated_ratio = float(exact_sampled_mass / separated_bound)
        max_separated_ratio = max(max_separated_ratio, separated_ratio)
        rows[-1]["separatedSampleRatio"] = separated_ratio

    single_mode_rows = []
    for multiplier in (1, 2, 4, 8, 16, 32):
        heat_ratio = np.exp(
            -NU * D_MODULUS**2 * float(multiplier**2) * A_0
        )
        single_mode_rows.append(
            {
                "r": multiplier,
                "heatWeightedOverUnweighted": float(heat_ratio),
            }
        )

    determinant_rows = []
    max_determinant_relative_error = 0.0
    min_inverse_bound_ratio = np.inf
    b_rate = 2.0 * NU * D_MODULUS**2
    for n_value in (2, 3, 4, 5, 6):
        gap = 0.01
        roots = np.arange(1, n_value + 1, dtype=float) * gap
        rates = np.arange(2, n_value + 2, dtype=float)
        nodes = np.exp(-b_rate * gap * rates**2)
        matrix = np.empty((n_value, n_value), dtype=float)
        for row, root_time in enumerate(roots):
            matrix[row, :] = (
                1.0 - np.exp(-b_rate * rates**2 * root_time)
            ) / (b_rate * rates**2)
        determinant_direct = abs(float(np.linalg.det(matrix)))
        determinant_factor = float(
            np.prod((1.0 - nodes) / (b_rate * rates**2))
            * np.prod(
                [
                    abs(nodes[right] - nodes[left])
                    for left in range(n_value)
                    for right in range(left + 1, n_value)
                ]
            )
        )
        relative_error = abs(determinant_direct - determinant_factor) / max(
            determinant_factor, np.finfo(float).tiny
        )
        inverse_norm = float(np.linalg.norm(np.linalg.inv(matrix), ord=2))
        r_max = float(n_value + 1)
        inverse_lower = gap ** -1 * (
            b_rate * gap * r_max**2
        ) ** (-(n_value - 1) / 2.0)
        bound_ratio = inverse_norm / inverse_lower
        max_determinant_relative_error = max(
            max_determinant_relative_error, relative_error
        )
        min_inverse_bound_ratio = min(min_inverse_bound_ratio, bound_ratio)
        determinant_rows.append(
            {
                "N": n_value,
                "determinantDirect": determinant_direct,
                "determinantFactor": determinant_factor,
                "relativeError": relative_error,
                "inverseNorm": inverse_norm,
                "inverseLower": inverse_lower,
                "boundRatio": bound_ratio,
            }
        )

    checks = [
        check(
            "finite shear generators are skew-adjoint",
            max_skew_defect < 1e-14,
            max_skew_defect,
            "||V+V*||/||V|| < 1e-14",
        ),
        check(
            "root-coordinate slope inequality",
            max_slope_ratio <= 1.0 + 1e-13,
            max_slope_ratio,
            "|P0 V F| <= ||V|| ||F|| when F0=0",
        ),
        check(
            "combined generator is dissipative",
            max_dissipative_real_part <= 1e-10,
            max_dissipative_real_part,
            "Re <(D+aV)F,F> <= 0",
        ),
        check(
            "finite semigroup is contractive",
            max_contraction_ratio <= 1.0 + 1e-12,
            max_contraction_ratio,
            "||exp(t(D+aV))F|| <= ||F||",
        ),
        check(
            "multiplier norm obeys l1 bound",
            max_multiplier_ratio <= 1.0 + 1e-12,
            max_multiplier_ratio,
            "||V(A0)|| <= 2|Kz| sum |z_l| exp(-c r_l^2 A0)",
        ),
        check(
            "weighted Cauchy bound",
            max_weighted_l1_ratio <= 1.0 + 1e-12,
            max_weighted_l1_ratio,
            "sum |z_l| <= sqrt(Kv) sqrt(sum r_l^-2)",
        ),
        check(
            "amplitude optimizer upper envelope",
            max_envelope_ratio <= 1.0 + 1e-12,
            max_envelope_ratio,
            "raw amplitude factor is below its u=3 optimum",
        ),
        check(
            "integer lattice suppression",
            max_lattice_ratio <= 1.0 + 1e-12,
            max_lattice_ratio,
            "NM/Ks <= 3/(4N)",
        ),
        check(
            "exact separated sampled-slope inequality",
            max_separated_ratio <= 1.0 + 1e-12,
            max_separated_ratio,
            "sum |P0 V(tau_m) F(tau_m)|^2 <= 2 Kz^2 M W^2/(b h)",
        ),
        check(
            "equal-grid determinant factorization",
            max_determinant_relative_error < 1e-7,
            {
                "maxRelativeError": max_determinant_relative_error,
                "rows": determinant_rows,
            },
            "det M equals the cumulative-Vandermonde-diagonal product",
        ),
        check(
            "equal-grid inverse lower bound",
            min_inverse_bound_ratio >= 1.0 - 1e-10,
            min_inverse_bound_ratio,
            "||M^-1||_2 >= h^-1*(b*h*rmax^2)^(-(N-1)/2)",
        ),
        check(
            "heat-weighted correction is decisive",
            single_mode_rows[-1]["heatWeightedOverUnweighted"] < 1e-25,
            single_mode_rows,
            "the observation-layer norm cannot lower-bound unweighted coefficient l2",
        ),
    ]

    return {
        "release": "R0.71Y",
        "generatedAt": now(),
        "status": "passed" if all(item["passed"] for item in checks) else "failed",
        "seed": RNG_SEED,
        "meaning": (
            "Independent finite-matrix corroboration of skew contraction, "
            "root-slope sampling, and optimized lattice algebra. No exact-root "
            "construction, DNS, universal endpoint theorem, or regularity "
            "result is claimed."
        ),
        "rows": rows,
        "equalGridRows": determinant_rows,
        "singleModeCorrection": single_mode_rows,
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
