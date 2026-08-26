#!/usr/bin/env python3
"""Independent binary64 audit for the R0.71X one-third boundary.

This program is deliberately self-contained.  It imports no R0.71W/R0.71X
producer, reads no producer JSON, and uses only the Python standard library.
Starting from the pinned raw Fourier parameters, it independently rebuilds

* the limiting response interpolation, prescribed-root residuals, slopes,
  nonzero limiting tail, and the finite ECT zero-budget ledger;
* finite-q tangent-ledger proxies for the initial H1 data size, selected atom,
  and deterministic full-frequency rotational upper bound;
* the exact algebraic factor J / D^(1/3) = delta^(4/3) times a uniformly
  dimensionless coefficient;
* the fixed-delta beta < 1/3, beta = 1/3, beta > 1/3 trichotomy.

The finite calculation corroborates powers and algebra only.  It does not
prove the uniform infinite-lattice IFT, continuum roots, nonlinear enstrophy
bounds, a theorem for every triangular 2.5D solution, or Navier--Stokes
regularity.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from typing import Callable, Iterable


# Raw parameters, repeated here rather than imported from another audit.
NU = 0.02
MODULUS = 8
K_Y = 1
K_Z = 1
BACKGROUND_FREQUENCY = 4
BACKGROUND_MULTIPLIER = 1.0 / BACKGROUND_FREQUENCY
N_ROOTS = 2
MODE_RATIOS = (1, 2, 3, 4, 5)
SCALED_ROOTS = (0.1, 0.2)
SCALED_WINDOW_LEFT = 0.05
PHYSICAL_WINDOW_LENGTH = 0.5
DELTA_STAR = 1.0 / 64.0
Q_VALUES = tuple(2**power for power in (12, 14, 16, 18, 20, 22))
DELTA_DECAY_POWERS = (0.0, 0.25, 0.5, 0.75)
BETA_VALUES = (0.25, 1.0 / 3.0, 0.4)

# The finite proxy fixes the harmless target multiplier factor
# 2 |m_*(k_*)|^2 / kappa_*^2 to two, i.e. |m_*| = kappa_* = 1.
ATOM_FACTOR = 2.0

ROOT_RESIDUAL_TOLERANCE = 2.0e-13
SIMPLE_SLOPE_TOLERANCE = 5.0e-2
TAIL_TOLERANCE = 5.0e-2
DETERMINANT_TOLERANCE = 1.0e-6
POWER_TOLERANCE = 3.0e-2
FACTORIZATION_TOLERANCE = 5.0e-13


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def solve_linear(matrix: list[list[float]], rhs: list[float]) -> list[float]:
    """Solve a dense real system by independent partial-pivot elimination."""

    size = len(rhs)
    if len(matrix) != size or any(len(row) != size for row in matrix):
        raise ValueError("matrix must be square and match rhs")
    augmented = [list(row) + [value] for row, value in zip(matrix, rhs)]
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(augmented[row][column]))
        if abs(augmented[pivot][column]) <= 1.0e-300:
            raise ArithmeticError("singular response matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        pivot_value = augmented[column][column]
        for index in range(column, size + 1):
            augmented[column][index] /= pivot_value
        for row in range(size):
            if row == column:
                continue
            factor = augmented[row][column]
            for index in range(column, size + 1):
                augmented[row][index] -= factor * augmented[column][index]
    return [augmented[row][-1] for row in range(size)]


def determinant(matrix: list[list[float]]) -> float:
    work = [list(row) for row in matrix]
    size = len(work)
    sign = 1.0
    product = 1.0
    for column in range(size):
        pivot = max(range(column, size), key=lambda row: abs(work[row][column]))
        if work[pivot][column] == 0.0:
            return 0.0
        if pivot != column:
            work[column], work[pivot] = work[pivot], work[column]
            sign *= -1.0
        pivot_value = work[column][column]
        product *= pivot_value
        for row in range(column + 1, size):
            factor = work[row][column] / pivot_value
            for index in range(column + 1, size):
                work[row][index] -= factor * work[column][index]
    return sign * product


def limiting_rate(mode_ratio: int) -> float:
    return 2.0 * NU * MODULUS**2 * mode_ratio**2


def limiting_response(mode_ratio: int, scaled_time: float) -> float:
    rate = limiting_rate(mode_ratio)
    return -math.expm1(-rate * scaled_time) / rate


def limiting_response_derivative(mode_ratio: int, scaled_time: float) -> float:
    return math.exp(-limiting_rate(mode_ratio) * scaled_time)


def finite_response(q_value: int, mode_ratio: int, scaled_time: float) -> float:
    mode = MODULUS * mode_ratio * q_value
    beta = 2.0 * NU * mode * (mode - K_Y)
    mu = NU * (K_Y**2 + K_Z**2)
    physical_time = scaled_time / q_value**2
    return (
        math.exp(-mu * physical_time)
        * (-math.expm1(-beta * physical_time))
        / beta
    )


def finite_response_derivative(
    q_value: int, mode_ratio: int, scaled_time: float
) -> float:
    mode = MODULUS * mode_ratio * q_value
    beta = 2.0 * NU * mode * (mode - K_Y)
    mu = NU * (K_Y**2 + K_Z**2)
    physical_time = scaled_time / q_value**2
    return (
        -mu * math.exp(-mu * physical_time) / beta
        + (mu + beta) * math.exp(-(mu + beta) * physical_time) / beta
    )


def interpolation_coefficients(
    response: Callable[[int, float], float]
) -> tuple[list[float], list[list[float]], float]:
    """Fix c_1=1 and solve the N-by-N real response block."""

    active_ratios = MODE_RATIOS[: N_ROOTS + 1]
    matrix = [
        [response(active_ratios[column], time) for column in range(1, N_ROOTS + 1)]
        for time in SCALED_ROOTS
    ]
    rhs = [-response(active_ratios[0], time) for time in SCALED_ROOTS]
    free = solve_linear(matrix, rhs)
    coefficients = [1.0, *free, *([0.0] * N_ROOTS)]
    return coefficients, matrix, determinant(matrix)


def limiting_ledger() -> dict[str, object]:
    coefficients, matrix, block_determinant = interpolation_coefficients(
        limiting_response
    )
    real_coefficients = coefficients[: N_ROOTS + 1]
    active_ratios = MODE_RATIOS[: N_ROOTS + 1]
    residuals = [
        K_Z
        * math.fsum(
            coefficient * limiting_response(ratio, time)
            for coefficient, ratio in zip(real_coefficients, active_ratios)
        )
        for time in SCALED_ROOTS
    ]
    slopes = [
        K_Z
        * math.fsum(
            coefficient * limiting_response_derivative(ratio, time)
            for coefficient, ratio in zip(real_coefficients, active_ratios)
        )
        for time in SCALED_ROOTS
    ]
    tail = K_Z * math.fsum(
        coefficient / limiting_rate(ratio)
        for coefficient, ratio in zip(real_coefficients, active_ratios)
    )
    return {
        "coefficients": coefficients,
        "responseEvaluationMatrix": matrix,
        "responseBlockDeterminant": block_determinant,
        "rootResiduals": residuals,
        "maximumRootResidual": max(abs(value) for value in residuals),
        "rootSlopes": slopes,
        "minimumAbsoluteRootSlope": min(abs(value) for value in slopes),
        "limitingTail": tail,
        "ectZeroBudget": {
            "responseDimension": N_ROOTS + 1,
            "maximumPositiveZeros": N_ROOTS,
            "prescribedPositiveZeros": len(SCALED_ROOTS),
            "budgetSaturated": len(SCALED_ROOTS) == N_ROOTS,
            "allPrescribedRootsSimple": all(
                abs(value) >= SIMPLE_SLOPE_TOLERANCE for value in slopes
            ),
            "meaning": (
                "A nonzero combination of M limiting responses has at most "
                "M-1 positive zeros.  The constructed M=3 combination uses "
                "the full two-zero budget; the nonzero slopes rule out "
                "multiplicity at either prescribed root."
            ),
        },
    }


def finite_coefficients(q_value: int) -> list[float]:
    def response(mode_ratio: int, scaled_time: float) -> float:
        return finite_response(q_value, mode_ratio, scaled_time)

    coefficients, _, _ = interpolation_coefficients(response)
    return coefficients


def loglog_fit(q_values: Iterable[int], values: Iterable[float]) -> dict[str, float]:
    x_values = [math.log(float(value)) for value in q_values]
    y_values = [math.log(float(value)) for value in values]
    x_mean = math.fsum(x_values) / len(x_values)
    y_mean = math.fsum(y_values) / len(y_values)
    covariance = math.fsum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(x_values, y_values)
    )
    variance = math.fsum((x_value - x_mean) ** 2 for x_value in x_values)
    slope = covariance / variance
    intercept = y_mean - slope * x_mean
    residual_square = math.fsum(
        (y_value - (slope * x_value + intercept)) ** 2
        for x_value, y_value in zip(x_values, y_values)
    )
    total_square = math.fsum((y_value - y_mean) ** 2 for y_value in y_values)
    return {
        "power": slope,
        "logCoefficient": intercept,
        "rSquared": 1.0 - residual_square / total_square if total_square else 1.0,
    }


def leading_enstrophy(
    q_value: int,
    amplitude: float,
    coefficients: list[float],
    physical_time: float,
) -> float:
    modes = [MODULUS * ratio * q_value for ratio in MODE_RATIOS]
    scalar_rates = [(K_Y - mode) ** 2 + K_Z**2 for mode in modes]
    background = amplitude * q_value * BACKGROUND_MULTIPLIER
    scalar = 2.0 * amplitude**2 * math.fsum(
        rate * math.exp(-2.0 * NU * rate * physical_time)
        for rate in scalar_rates
    )
    shear = 2.0 * amplitude**2 * math.fsum(
        mode**2
        * coefficient**2
        * math.exp(-2.0 * NU * mode**2 * physical_time)
        for mode, coefficient in zip(modes, coefficients)
    )
    background_part = (
        2.0
        * BACKGROUND_FREQUENCY**2
        * background**2
        * math.exp(
            -2.0 * NU * BACKGROUND_FREQUENCY**2 * physical_time
        )
    )
    return scalar + shear + background_part


def exact_tangent_initial_data(
    q_value: int, amplitude: float, coefficients: list[float]
) -> float:
    """Exact normalized-Haar H1 size of the finite tangent datum."""

    modes = [MODULUS * ratio * q_value for ratio in MODE_RATIOS]
    scalar = 2.0 * amplitude**2 * math.fsum(
        1.0 + (K_Y - mode) ** 2 + K_Z**2 for mode in modes
    )
    shear = 2.0 * amplitude**2 * math.fsum(
        coefficient**2 * (1.0 + mode**2)
        for coefficient, mode in zip(coefficients, modes)
    )
    background = amplitude * q_value * BACKGROUND_MULTIPLIER
    background_part = 2.0 * background**2 * (
        1.0 + BACKGROUND_FREQUENCY**2
    )
    return scalar + shear + background_part


def rotational_charge_upper(
    q_value: int, amplitude: float, coefficients: list[float]
) -> float:
    modes = [MODULUS * ratio * q_value for ratio in MODE_RATIOS]
    integral_v_infinity_squared = 4.0 * amplitude**2 * math.fsum(
        abs(coefficients[left] * coefficients[right])
        / (NU * (modes[left] ** 2 + modes[right] ** 2))
        for left in range(len(modes))
        for right in range(len(modes))
    )
    scalar_z_energy_upper = (
        2.0 * K_Z**2 * amplitude**2 * len(MODE_RATIOS)
    )
    background = amplitude * q_value * BACKGROUND_MULTIPLIER
    right_time = SCALED_WINDOW_LEFT / q_value**2 + PHYSICAL_WINDOW_LENGTH
    background_floor = (
        2.0
        * BACKGROUND_FREQUENCY**2
        * background**2
        * math.exp(
            -2.0 * NU * BACKGROUND_FREQUENCY**2 * right_time
        )
    )
    return (
        integral_v_infinity_squared
        * scalar_z_energy_upper
        / background_floor
        / PHYSICAL_WINDOW_LENGTH
    )


def evaluate_case(q_value: int, delta_decay_power: float) -> dict[str, object]:
    delta = DELTA_STAR * q_value ** (-delta_decay_power)
    amplitude = delta * q_value**2
    coefficients = finite_coefficients(q_value)
    root_residuals: list[float] = []
    normalized_slopes: list[float] = []
    atoms: list[float] = []
    root_enstrophies: list[float] = []
    for scaled_time in SCALED_ROOTS:
        residual = K_Z * math.fsum(
            coefficient * finite_response(q_value, ratio, scaled_time)
            for coefficient, ratio in zip(
                coefficients[: N_ROOTS + 1], MODE_RATIOS[: N_ROOTS + 1]
            )
        )
        normalized_slope = abs(
            K_Z
            * math.fsum(
                coefficient
                * finite_response_derivative(q_value, ratio, scaled_time)
                for coefficient, ratio in zip(
                    coefficients[: N_ROOTS + 1],
                    MODE_RATIOS[: N_ROOTS + 1],
                )
            )
        )
        root_time = scaled_time / q_value**2
        enstrophy = leading_enstrophy(
            q_value, amplitude, coefficients, root_time
        )
        physical_slope = amplitude**2 * normalized_slope
        atom = ATOM_FACTOR * physical_slope**2 / enstrophy
        root_residuals.append(residual)
        normalized_slopes.append(normalized_slope)
        root_enstrophies.append(enstrophy)
        atoms.append(atom)

    initial_data = exact_tangent_initial_data(q_value, amplitude, coefficients)
    selected_atom = atoms[1]
    endpoint_ratio = selected_atom / initial_data ** (1.0 / 3.0)
    endpoint_coefficient = endpoint_ratio / delta ** (4.0 / 3.0)
    selected_normalized_enstrophy = root_enstrophies[1] / (
        amplitude**2 * q_value**2
    )
    normalized_initial_data = initial_data / (amplitude**2 * q_value**2)
    algebraic_endpoint_coefficient = (
        ATOM_FACTOR
        * normalized_slopes[1] ** 2
        / (
            selected_normalized_enstrophy
            * normalized_initial_data ** (1.0 / 3.0)
        )
    )
    factorization_relative_error = abs(
        endpoint_coefficient - algebraic_endpoint_coefficient
    ) / max(abs(endpoint_coefficient), abs(algebraic_endpoint_coefficient), 1.0e-300)

    left_time = SCALED_WINDOW_LEFT / q_value**2
    right_time = left_time + PHYSICAL_WINDOW_LENGTH
    left_enstrophy = leading_enstrophy(
        q_value, amplitude, coefficients, left_time
    )
    right_enstrophy = leading_enstrophy(
        q_value, amplitude, coefficients, right_time
    )
    charge_upper = rotational_charge_upper(q_value, amplitude, coefficients)
    enstrophy_ratio = left_enstrophy / right_enstrophy
    complete_ledger_proxy = enstrophy_ratio * (NU**2 + charge_upper)

    return {
        "q": q_value,
        "deltaDecayPower": delta_decay_power,
        "delta": delta,
        "amplitude": amplitude,
        "coefficients": coefficients,
        "rootResiduals": root_residuals,
        "maximumRootResidual": max(abs(value) for value in root_residuals),
        "normalizedRootSlopes": normalized_slopes,
        "minimumNormalizedRootSlope": min(normalized_slopes),
        "rootEnstrophy": root_enstrophies,
        "selectedSecondRootAtom": selected_atom,
        "initialDataD": initial_data,
        "DNormalized": normalized_initial_data,
        "selectedRootYNormalized": selected_normalized_enstrophy,
        "rotationalChargeUpper": charge_upper,
        "leadingEnstrophyRatio": enstrophy_ratio,
        "completeLedgerProxy": complete_ledger_proxy,
        "atomToCompleteLedgerProxy": selected_atom / complete_ledger_proxy,
        "endpointRatio": endpoint_ratio,
        "deltaFourThirds": delta ** (4.0 / 3.0),
        "endpointCoefficient": endpoint_coefficient,
        "endpointCoefficientFromNormalizedFactors": algebraic_endpoint_coefficient,
        "endpointFactorizationRelativeError": factorization_relative_error,
    }


def expected_powers(delta_decay_power: float) -> dict[str, float]:
    gamma = delta_decay_power
    return {
        "delta": -gamma,
        "amplitude": 2.0 - gamma,
        "initialDataD": 6.0 - 2.0 * gamma,
        "selectedSecondRootAtom": 2.0 - 2.0 * gamma,
        "rotationalChargeUpper": -2.0 * gamma,
        "endpointRatio": -4.0 * gamma / 3.0,
        "endpointCoefficient": 0.0,
    }


def amplitude_law_audit(delta_decay_power: float) -> dict[str, object]:
    rows = [evaluate_case(q_value, delta_decay_power) for q_value in Q_VALUES]
    expected = expected_powers(delta_decay_power)
    fitted: dict[str, dict[str, float]] = {}
    for field in expected:
        fitted[field] = loglog_fit(
            Q_VALUES, [float(row[field]) for row in rows]
        )
        fitted[field]["expectedPower"] = expected[field]
        fitted[field]["absolutePowerError"] = abs(
            fitted[field]["power"] - expected[field]
        )
    passed = (
        all(item["absolutePowerError"] <= POWER_TOLERANCE for item in fitted.values())
        and max(float(row["maximumRootResidual"]) for row in rows)
        <= ROOT_RESIDUAL_TOLERANCE
        and min(float(row["minimumNormalizedRootSlope"]) for row in rows)
        >= SIMPLE_SLOPE_TOLERANCE
        and max(float(row["endpointFactorizationRelativeError"]) for row in rows)
        <= FACTORIZATION_TOLERANCE
    )
    return {
        "deltaLaw": f"delta_q = {DELTA_STAR} * q^(-{delta_decay_power})",
        "deltaDecayPower": delta_decay_power,
        "expectedPowers": expected,
        "fittedPowers": fitted,
        "rows": rows,
        "passed": passed,
    }


def beta_trichotomy(fixed_delta_rows: list[dict[str, object]]) -> dict[str, object]:
    entries: list[dict[str, object]] = []
    for beta in BETA_VALUES:
        ratios = [
            float(row["selectedSecondRootAtom"])
            / float(row["initialDataD"]) ** beta
            for row in fixed_delta_rows
        ]
        fitted = loglog_fit(Q_VALUES, ratios)
        expected_power = 2.0 - 6.0 * beta
        if beta < 1.0 / 3.0 - 1.0e-12:
            expected_class = "divergent"
            observed_class = "divergent" if fitted["power"] > 0.0 else "not divergent"
        elif beta > 1.0 / 3.0 + 1.0e-12:
            expected_class = "vanishing"
            observed_class = "vanishing" if fitted["power"] < 0.0 else "not vanishing"
        else:
            expected_class = "critical"
            observed_class = (
                "critical"
                if abs(fitted["power"]) <= POWER_TOLERANCE
                else "not critical"
            )
        entries.append(
            {
                "beta": beta,
                "expectedClass": expected_class,
                "observedClass": observed_class,
                "expectedPower": expected_power,
                "fittedPower": fitted["power"],
                "absolutePowerError": abs(fitted["power"] - expected_power),
                "rSquared": fitted["rSquared"],
                "firstRatio": ratios[0],
                "lastRatio": ratios[-1],
                "passed": (
                    observed_class == expected_class
                    and abs(fitted["power"] - expected_power) <= POWER_TOLERANCE
                ),
            }
        )
    return {
        "entries": entries,
        "passed": all(bool(entry["passed"]) for entry in entries),
        "meaning": (
            "At fixed small delta, J has q-power 2 and D has q-power 6. "
            "Therefore J/D^beta diverges for beta<1/3, is scale-critical "
            "at beta=1/3, and vanishes for beta>1/3."
        ),
    }


def make_check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def audit() -> dict[str, object]:
    limiting = limiting_ledger()
    amplitude_laws = [
        amplitude_law_audit(decay_power)
        for decay_power in DELTA_DECAY_POWERS
    ]
    fixed_delta = next(
        law for law in amplitude_laws if law["deltaDecayPower"] == 0.0
    )
    trichotomy = beta_trichotomy(fixed_delta["rows"])
    maximum_factorization_error = max(
        float(row["endpointFactorizationRelativeError"])
        for law in amplitude_laws
        for row in law["rows"]
    )
    checks = [
        make_check(
            "limiting prescribed roots close",
            float(limiting["maximumRootResidual"]) <= ROOT_RESIDUAL_TOLERANCE,
            limiting["maximumRootResidual"],
            f"maximum absolute residual <= {ROOT_RESIDUAL_TOLERANCE}",
        ),
        make_check(
            "limiting response block invertible",
            abs(float(limiting["responseBlockDeterminant"]))
            >= DETERMINANT_TOLERANCE,
            limiting["responseBlockDeterminant"],
            f"absolute determinant >= {DETERMINANT_TOLERANCE}",
        ),
        make_check(
            "limiting prescribed roots simple",
            float(limiting["minimumAbsoluteRootSlope"])
            >= SIMPLE_SLOPE_TOLERANCE,
            limiting["minimumAbsoluteRootSlope"],
            f"minimum absolute slope >= {SIMPLE_SLOPE_TOLERANCE}",
        ),
        make_check(
            "limiting tail nonzero",
            abs(float(limiting["limitingTail"])) >= TAIL_TOLERANCE,
            limiting["limitingTail"],
            f"absolute limiting tail >= {TAIL_TOLERANCE}",
        ),
        make_check(
            "ECT positive-zero budget saturated",
            bool(limiting["ectZeroBudget"]["budgetSaturated"])
            and bool(limiting["ectZeroBudget"]["allPrescribedRootsSimple"]),
            limiting["ectZeroBudget"],
            "two prescribed simple positive roots use the M-1=2 budget",
        ),
        make_check(
            "all amplitude-law power ledgers close",
            all(bool(law["passed"]) for law in amplitude_laws),
            {
                str(law["deltaDecayPower"]): {
                    field: fit["absolutePowerError"]
                    for field, fit in law["fittedPowers"].items()
                }
                for law in amplitude_laws
            },
            f"every absolute fitted-power error <= {POWER_TOLERANCE}",
        ),
        make_check(
            "delta four-thirds factorization closes",
            maximum_factorization_error <= FACTORIZATION_TOLERANCE,
            maximum_factorization_error,
            f"maximum relative algebra error <= {FACTORIZATION_TOLERANCE}",
        ),
        make_check(
            "beta one-third trichotomy closes",
            bool(trichotomy["passed"]),
            trichotomy["entries"],
            "beta<1/3 divergent, beta=1/3 critical, beta>1/3 vanishing",
        ),
    ]
    status = "passed" if all(bool(check["passed"]) for check in checks) else "failed"
    return {
        "release": "R0.71X",
        "audit": "independent binary64 endpoint-boundary reconstruction",
        "status": status,
        "generatedAt": utc_now(),
        "method": {
            "language": "Python standard library only",
            "arithmetic": "IEEE-754 binary64",
            "linearSolve": "self-contained partial-pivot Gaussian elimination",
            "producerImports": False,
            "producerJsonReads": False,
            "randomness": "none",
        },
        "parameters": {
            "viscosity": NU,
            "modulus": MODULUS,
            "target": [K_Y, K_Z],
            "backgroundFrequency": BACKGROUND_FREQUENCY,
            "backgroundMultiplier": BACKGROUND_MULTIPLIER,
            "rootCount": N_ROOTS,
            "modeRatios": list(MODE_RATIOS),
            "scaledRoots": list(SCALED_ROOTS),
            "scaledWindowLeft": SCALED_WINDOW_LEFT,
            "physicalWindowLength": PHYSICAL_WINDOW_LENGTH,
            "fixedSmallDelta": DELTA_STAR,
            "qValues": list(Q_VALUES),
            "deltaDecayPowers": list(DELTA_DECAY_POWERS),
            "betaValues": list(BETA_VALUES),
            "atomProxyFactor": ATOM_FACTOR,
        },
        "limitingResponse": limiting,
        "amplitudeLawAudits": amplitude_laws,
        "betaTrichotomy": trichotomy,
        "checks": checks,
        "claimBoundary": (
            "This independent finite tangent-ledger calculation checks the "
            "limiting interpolation, root/slopes/tail, exact initial-data "
            "formula, D/J/rotational powers, delta^(4/3) factorization, and "
            "beta trichotomy for the fixed-geometry small-coupling branch. "
            "It does not prove the uniform continuum IFT or nonlinear PDE "
            "bounds, does not extend the endpoint payment to every triangular "
            "2.5D solution or arbitrary 3D solution, and makes no Navier--Stokes "
            "regularity, novelty, or priority claim."
        ),
    }


def main() -> None:
    args = parse_args()
    payload = audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"output": str(args.output), "status": payload["status"]}))
    if payload["status"] != "passed":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
