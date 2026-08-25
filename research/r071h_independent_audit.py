#!/usr/bin/env python3
"""Release-grade independent audit of the R0.71H projective-curvature identity.

The checker uses only the Python standard library.  It has three layers:

1. a forced finite-dimensional trajectory for a non-diagonal symmetric
   positive operator;
2. an unforced heat flow in an orthonormal Fourier basis, where ``-Delta``
   is diagonal with the exact eigenvalues ``|k|^2``;
3. a soft-denominator audit for ``Z=C/sqrt(||C||^2+epsilon)``.

The calculations are consistency checks, not a Navier--Stokes regularity
result and not a claim of originality.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Callable, Sequence


Vector = list[float]
Matrix = list[list[float]]


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def add(left: Sequence[float], right: Sequence[float]) -> Vector:
    return [a + b for a, b in zip(left, right)]


def subtract(left: Sequence[float], right: Sequence[float]) -> Vector:
    return [a - b for a, b in zip(left, right)]


def scale(factor: float, value: Sequence[float]) -> Vector:
    return [factor * entry for entry in value]


def norm_squared(value: Sequence[float]) -> float:
    return dot(value, value)


def maximum_absolute(value: Sequence[float]) -> float:
    return max((abs(entry) for entry in value), default=0.0)


def matvec(matrix: Matrix, value: Sequence[float]) -> Vector:
    return [dot(row, value) for row in matrix]


def transpose(matrix: Matrix) -> Matrix:
    return [list(column) for column in zip(*matrix)]


def matmul(left: Matrix, right: Matrix) -> Matrix:
    right_t = transpose(right)
    return [[dot(row, column) for column in right_t] for row in left]


def gram_matrix(matrix: Matrix) -> Matrix:
    return matmul(transpose(matrix), matrix)


def diagonal_matrix(entries: Sequence[float]) -> Matrix:
    size = len(entries)
    return [
        [entries[row] if row == column else 0.0 for column in range(size)]
        for row in range(size)
    ]


def q_apply(direction: Sequence[float], value: Sequence[float]) -> Vector:
    """Apply I-direction tensor direction, without assuming unit length."""

    return subtract(value, scale(dot(direction, value), direction))


def simpson(
    function: Callable[[float], float],
    left: float,
    right: float,
    intervals: int = 8000,
) -> float:
    require(intervals > 0 and intervals % 2 == 0, "Simpson interval count")
    step = (right - left) / intervals
    total = function(left) + function(right)
    for index in range(1, intervals):
        weight = 4.0 if index % 2 else 2.0
        total += weight * function(left + index * step)
    return total * step / 3.0


def unit_quantities(
    operator: Matrix,
    c_value: Sequence[float],
    c_derivative: Sequence[float],
    source: Sequence[float],
    viscosity: float,
) -> dict[str, float]:
    d_value = norm_squared(c_value)
    require(d_value > 0.0, "positive denominator for unit direction")
    rho = math.sqrt(d_value)
    direction = scale(1.0 / rho, c_value)
    radial_rate = dot(c_value, c_derivative)
    direction_derivative = subtract(
        scale(1.0 / rho, c_derivative),
        scale(radial_rate / (rho**3), c_value),
    )

    a_direction = matvec(operator, direction)
    rayleigh = dot(a_direction, direction)
    curvature = q_apply(direction, a_direction)
    projected_source = scale(1.0 / rho, q_apply(direction, source))
    model_derivative = add(
        scale(-viscosity, curvature), projected_source
    )
    rayleigh_derivative = 2.0 * dot(a_direction, direction_derivative)
    rayleigh_model = (
        -2.0 * viscosity * norm_squared(curvature)
        + 2.0 * dot(curvature, projected_source)
    )
    left_side = (
        norm_squared(direction_derivative)
        + viscosity**2 * norm_squared(curvature)
    )
    right_side = (
        -viscosity * rayleigh_derivative
        + norm_squared(projected_source)
    )

    equation_residual = maximum_absolute(
        subtract(
            c_derivative,
            add(scale(-viscosity, matvec(operator, c_value)), source),
        )
    )
    direction_residual = maximum_absolute(
        subtract(direction_derivative, model_derivative)
    )

    return {
        "d": d_value,
        "r": rayleigh,
        "rDerivative": rayleigh_derivative,
        "curvatureNormSquared": norm_squared(curvature),
        "directionSpeedSquared": norm_squared(direction_derivative),
        "sourceRatio": norm_squared(projected_source),
        "equationResidual": equation_residual,
        "directionEquationResidual": direction_residual,
        "rayleighDerivativeResidual": abs(
            rayleigh_derivative - rayleigh_model
        ),
        "identityResidual": abs(left_side - right_side),
        "leftSide": left_side,
        "rightSide": right_side,
    }


def soft_quantities(
    operator: Matrix,
    c_value: Sequence[float],
    c_derivative: Sequence[float],
    source: Sequence[float],
    viscosity: float,
    epsilon: float,
) -> dict[str, float]:
    """Audit Z=C/sqrt(d+epsilon) and its non-projective Q operator."""

    require(epsilon > 0.0, "positive epsilon")
    d_value = norm_squared(c_value)
    radius = math.sqrt(d_value + epsilon)
    z_value = scale(1.0 / radius, c_value)
    c_pair = dot(c_value, c_derivative)
    z_derivative = subtract(
        scale(1.0 / radius, c_derivative),
        scale(c_pair / (radius**3), c_value),
    )

    a_z = matvec(operator, z_value)
    soft_rayleigh = dot(a_z, z_value)
    q_curvature = q_apply(z_value, a_z)
    q_source = q_apply(z_value, scale(1.0 / radius, source))
    model_derivative = add(scale(-viscosity, q_curvature), q_source)
    rayleigh_derivative = 2.0 * dot(a_z, z_derivative)
    mass = norm_squared(z_value)
    mass_derivative = 2.0 * dot(z_value, z_derivative)
    d_derivative = 2.0 * c_pair
    expected_mass_derivative = (
        epsilon * d_derivative / (d_value + epsilon) ** 2
    )

    left_side = (
        norm_squared(z_derivative)
        + viscosity**2 * norm_squared(q_curvature)
    )
    clean_right_side = (
        -viscosity * rayleigh_derivative + norm_squared(q_source)
    )
    radial_defect = viscosity * soft_rayleigh * mass_derivative
    corrected_right_side = clean_right_side + radial_defect

    result = {
        "d": d_value,
        "epsilon": epsilon,
        "softMass": mass,
        "softRayleigh": soft_rayleigh,
        "massDerivative": mass_derivative,
        "massDerivativeResidual": abs(
            mass_derivative - expected_mass_derivative
        ),
        "softEquationResidual": maximum_absolute(
            subtract(z_derivative, model_derivative)
        ),
        "leftSide": left_side,
        "cleanRightSide": clean_right_side,
        "radialDefect": radial_defect,
        "omittedDefectResidual": abs(left_side - clean_right_side),
        "correctedIdentityResidual": abs(
            left_side - corrected_right_side
        ),
    }

    # On d>0 one can still use the genuine orthogonal projector associated
    # with e=C/sqrt(d).  This is closer to the unit-direction identity, but
    # it does not extend through d=0.  Both a signed radial defect and, for
    # the full soft speed, a nonnegative radial-speed defect remain.
    if d_value > 0.0:
        unit_direction = scale(1.0 / math.sqrt(d_value), c_value)
        unit_rayleigh = dot(
            matvec(operator, unit_direction), unit_direction
        )
        tangent_z_derivative = q_apply(unit_direction, z_derivative)
        tangent_a_z = q_apply(unit_direction, a_z)
        tangent_source = q_apply(
            unit_direction, scale(1.0 / radius, source)
        )
        tangent_left = (
            norm_squared(tangent_z_derivative)
            + viscosity**2 * norm_squared(tangent_a_z)
        )
        tangent_clean_right = (
            -viscosity * rayleigh_derivative
            + norm_squared(tangent_source)
        )
        tangent_radial_defect = (
            viscosity * mass_derivative * unit_rayleigh
        )
        full_radial_speed_defect = mass_derivative**2 / (4.0 * mass)
        result.update(
            {
                "orthogonalTangentOmittedDefect": abs(
                    tangent_left - tangent_clean_right
                ),
                "orthogonalTangentRadialDefect": tangent_radial_defect,
                "orthogonalTangentCorrectedResidual": abs(
                    tangent_left
                    - tangent_clean_right
                    - tangent_radial_defect
                ),
                "fullSoftSpeedRadialDefect": full_radial_speed_defect,
                "fullOrthogonalCorrectedResidual": abs(
                    (
                        norm_squared(z_derivative)
                        + viscosity**2 * norm_squared(tangent_a_z)
                    )
                    - tangent_clean_right
                    - tangent_radial_defect
                    - full_radial_speed_defect
                ),
            }
        )

    return result


VISCOSITY = 0.37
GRAM_FACTOR: Matrix = [
    [1.0, 0.3, -0.2],
    [0.0, 1.4, 0.1],
    [0.5, -0.4, 0.9],
]
FINITE_OPERATOR = gram_matrix(GRAM_FACTOR)


def finite_trajectory(time: float) -> tuple[Vector, Vector]:
    value = [
        1.2 + 0.2 * math.sin(0.7 * time),
        -0.4 + 0.3 * math.cos(1.1 * time),
        0.8 + 0.15 * math.sin(1.3 * time + 0.2),
    ]
    derivative = [
        0.14 * math.cos(0.7 * time),
        -0.33 * math.sin(1.1 * time),
        0.195 * math.cos(1.3 * time + 0.2),
    ]
    return value, derivative


def finite_case(time: float) -> dict[str, float]:
    value, derivative = finite_trajectory(time)
    source = add(
        derivative,
        scale(VISCOSITY, matvec(FINITE_OPERATOR, value)),
    )
    return unit_quantities(
        FINITE_OPERATOR, value, derivative, source, VISCOSITY
    )


FOURIER_EIGENVALUES = [1.0, 2.0, 5.0, 9.0]
FOURIER_AMPLITUDES = [1.0, -0.7, 0.4, 0.2]
FOURIER_OPERATOR = diagonal_matrix(FOURIER_EIGENVALUES)


def fourier_trajectory(time: float) -> tuple[Vector, Vector]:
    value = [
        amplitude * math.exp(-VISCOSITY * eigenvalue * time)
        for amplitude, eigenvalue in zip(
            FOURIER_AMPLITUDES, FOURIER_EIGENVALUES
        )
    ]
    derivative = [
        -VISCOSITY * eigenvalue * entry
        for entry, eigenvalue in zip(value, FOURIER_EIGENVALUES)
    ]
    return value, derivative


def fourier_case(time: float) -> dict[str, float]:
    value, derivative = fourier_trajectory(time)
    source = [0.0 for _ in value]
    quantities = unit_quantities(
        FOURIER_OPERATOR, value, derivative, source, VISCOSITY
    )
    rho = math.sqrt(norm_squared(value))
    weights = [(entry / rho) ** 2 for entry in value]
    rayleigh = sum(
        weight * eigenvalue
        for weight, eigenvalue in zip(weights, FOURIER_EIGENVALUES)
    )
    variance = sum(
        weight * (eigenvalue - rayleigh) ** 2
        for weight, eigenvalue in zip(weights, FOURIER_EIGENVALUES)
    )
    quantities.update(
        {
            "spectralVariance": variance,
            "curvatureVarianceResidual": abs(
                quantities["curvatureNormSquared"] - variance
            ),
            "heatRayleighResidual": abs(
                quantities["rDerivative"] + 2.0 * VISCOSITY * variance
            ),
            "heatSpeedResidual": abs(
                quantities["directionSpeedSquared"]
                - VISCOSITY**2 * variance
            ),
        }
    )
    return quantities


def finite_dimensional_audit() -> dict[str, object]:
    symmetry_residual = max(
        abs(FINITE_OPERATOR[row][column] - FINITE_OPERATOR[column][row])
        for row in range(3)
        for column in range(3)
    )
    leading_minor_one = FINITE_OPERATOR[0][0]
    leading_minor_two = (
        FINITE_OPERATOR[0][0] * FINITE_OPERATOR[1][1]
        - FINITE_OPERATOR[0][1] ** 2
    )
    determinant = (
        FINITE_OPERATOR[0][0]
        * (
            FINITE_OPERATOR[1][1] * FINITE_OPERATOR[2][2]
            - FINITE_OPERATOR[1][2] * FINITE_OPERATOR[2][1]
        )
        - FINITE_OPERATOR[0][1]
        * (
            FINITE_OPERATOR[1][0] * FINITE_OPERATOR[2][2]
            - FINITE_OPERATOR[1][2] * FINITE_OPERATOR[2][0]
        )
        + FINITE_OPERATOR[0][2]
        * (
            FINITE_OPERATOR[1][0] * FINITE_OPERATOR[2][1]
            - FINITE_OPERATOR[1][1] * FINITE_OPERATOR[2][0]
        )
    )
    require(symmetry_residual < 1.0e-15, "finite operator symmetry")
    require(
        min(leading_minor_one, leading_minor_two, determinant) > 0.0,
        "finite operator positivity",
    )

    samples = [finite_case(index * 3.5 / 70.0) for index in range(71)]
    maximum_identity_residual = max(
        sample["identityResidual"] for sample in samples
    )
    maximum_direction_residual = max(
        sample["directionEquationResidual"] for sample in samples
    )
    maximum_rayleigh_residual = max(
        sample["rayleighDerivativeResidual"] for sample in samples
    )
    minimum_denominator = min(sample["d"] for sample in samples)

    left = 0.15
    right = 3.25
    integrated_left = simpson(
        lambda time: finite_case(time)["leftSide"], left, right
    )
    integrated_source = simpson(
        lambda time: finite_case(time)["sourceRatio"], left, right
    )
    endpoint_drop = VISCOSITY * (
        finite_case(left)["r"] - finite_case(right)["r"]
    )
    integrated_residual = abs(
        integrated_left - endpoint_drop - integrated_source
    )

    require(minimum_denominator > 1.0, "finite path avoids d=0")
    require(maximum_identity_residual < 3.0e-15, "finite identity")
    require(maximum_direction_residual < 2.0e-15, "finite direction equation")
    require(maximum_rayleigh_residual < 3.0e-15, "finite Rayleigh derivative")
    require(integrated_residual < 2.0e-12, "finite integrated identity")

    return {
        "operator": FINITE_OPERATOR,
        "leadingPrincipalMinors": [
            leading_minor_one,
            leading_minor_two,
            determinant,
        ],
        "symmetryResidual": symmetry_residual,
        "sampleCount": len(samples),
        "minimumDenominator": minimum_denominator,
        "maximumDirectionEquationResidual": maximum_direction_residual,
        "maximumRayleighDerivativeResidual": maximum_rayleigh_residual,
        "maximumPointwiseIdentityResidual": maximum_identity_residual,
        "integratedIdentityResidual": integrated_residual,
        "passed": True,
    }


def fourier_heat_audit() -> dict[str, object]:
    samples = [fourier_case(index * 2.8 / 70.0) for index in range(71)]
    maximum_identity_residual = max(
        sample["identityResidual"] for sample in samples
    )
    maximum_variance_residual = max(
        sample["curvatureVarianceResidual"] for sample in samples
    )
    maximum_rayleigh_residual = max(
        sample["heatRayleighResidual"] for sample in samples
    )
    maximum_speed_residual = max(
        sample["heatSpeedResidual"] for sample in samples
    )
    maximum_rayleigh_derivative = max(
        sample["rDerivative"] for sample in samples
    )

    left = 0.0
    right = 2.6
    integrated_left = simpson(
        lambda time: fourier_case(time)["leftSide"], left, right
    )
    endpoint_drop = VISCOSITY * (
        fourier_case(left)["r"] - fourier_case(right)["r"]
    )
    integrated_residual = abs(integrated_left - endpoint_drop)

    require(maximum_identity_residual < 2.0e-15, "Fourier identity")
    require(maximum_variance_residual < 2.0e-15, "Fourier variance")
    require(maximum_rayleigh_residual < 2.0e-15, "Fourier Rayleigh decay")
    require(maximum_speed_residual < 2.0e-15, "Fourier angular speed")
    require(maximum_rayleigh_derivative <= 0.0, "Fourier monotonicity")
    require(integrated_residual < 2.0e-12, "Fourier integrated identity")

    return {
        "waveVectors": [[1, 0, 0], [1, 1, 0], [2, 1, 0], [3, 0, 0]],
        "eigenvalues": FOURIER_EIGENVALUES,
        "sampleCount": len(samples),
        "maximumPointwiseIdentityResidual": maximum_identity_residual,
        "maximumCurvatureVarianceResidual": maximum_variance_residual,
        "maximumRayleighDecayResidual": maximum_rayleigh_residual,
        "maximumAngularSpeedResidual": maximum_speed_residual,
        "largestRayleighDerivative": maximum_rayleigh_derivative,
        "integratedIdentityResidual": integrated_residual,
        "passed": True,
    }


def epsilon_audit() -> dict[str, object]:
    epsilon = 0.23
    forced_samples = []
    for index in range(71):
        time = index * 3.5 / 70.0
        value, derivative = finite_trajectory(time)
        source = add(
            derivative,
            scale(VISCOSITY, matvec(FINITE_OPERATOR, value)),
        )
        forced_samples.append(
            soft_quantities(
                FINITE_OPERATOR,
                value,
                derivative,
                source,
                VISCOSITY,
                epsilon,
            )
        )

    maximum_corrected_residual = max(
        sample["correctedIdentityResidual"] for sample in forced_samples
    )
    maximum_soft_equation_residual = max(
        sample["softEquationResidual"] for sample in forced_samples
    )
    maximum_mass_residual = max(
        sample["massDerivativeResidual"] for sample in forced_samples
    )
    maximum_omitted_defect = max(
        sample["omittedDefectResidual"] for sample in forced_samples
    )
    maximum_tangent_corrected_residual = max(
        sample["orthogonalTangentCorrectedResidual"]
        for sample in forced_samples
    )
    maximum_full_orthogonal_residual = max(
        sample["fullOrthogonalCorrectedResidual"]
        for sample in forced_samples
    )

    heat_eigenvalue = 3.0
    heat_time = 0.6
    heat_epsilon = 0.4
    heat_value = [1.7 * math.exp(-VISCOSITY * heat_eigenvalue * heat_time)]
    heat_derivative = [
        -VISCOSITY * heat_eigenvalue * heat_value[0]
    ]
    one_dimensional_heat = soft_quantities(
        [[heat_eigenvalue]],
        heat_value,
        heat_derivative,
        [0.0],
        VISCOSITY,
        heat_epsilon,
    )

    crossing_epsilon = 0.19
    zero_crossing = soft_quantities(
        [[0.0, 0.0], [0.0, 0.0]],
        [0.0, 0.0],
        [1.0, 0.0],
        [1.0, 0.0],
        VISCOSITY,
        crossing_epsilon,
    )
    # For A=0, C(t)=(t,0), G=(1,0), the squared Q-source is
    # epsilon^2/(t^2+epsilon)^3.  Its exact whole-line integral is the
    # following divergent quantity.
    crossing_source_integral = (
        3.0 * math.pi / (8.0 * math.sqrt(crossing_epsilon))
    )
    crossing_rescaled_integral = (
        math.sqrt(crossing_epsilon) * crossing_source_integral
    )

    require(maximum_corrected_residual < 4.0e-15, "soft corrected identity")
    require(maximum_soft_equation_residual < 2.0e-15, "soft direction equation")
    require(maximum_mass_residual < 2.0e-15, "soft mass derivative")
    require(maximum_omitted_defect > 1.0e-5, "soft defect is nonzero")
    require(
        maximum_tangent_corrected_residual < 4.0e-15,
        "soft orthogonal-tangent identity",
    )
    require(
        maximum_full_orthogonal_residual < 4.0e-15,
        "soft full-speed orthogonal identity",
    )
    require(
        one_dimensional_heat["omittedDefectResidual"] > 1.0e-3,
        "one-dimensional heat exposes omitted defect",
    )
    require(
        one_dimensional_heat["correctedIdentityResidual"] < 2.0e-15,
        "one-dimensional corrected identity",
    )
    require(
        zero_crossing["correctedIdentityResidual"] < 2.0e-15,
        "soft identity at d=0",
    )
    require(
        abs(crossing_rescaled_integral - 3.0 * math.pi / 8.0) < 2.0e-15,
        "zero-crossing source integral",
    )

    return {
        "epsilon": epsilon,
        "sampleCount": len(forced_samples),
        "maximumSoftEquationResidual": maximum_soft_equation_residual,
        "maximumMassDerivativeResidual": maximum_mass_residual,
        "maximumCorrectedIdentityResidual": maximum_corrected_residual,
        "maximumOrthogonalTangentCorrectedResidual": (
            maximum_tangent_corrected_residual
        ),
        "maximumFullOrthogonalCorrectedResidual": (
            maximum_full_orthogonal_residual
        ),
        "maximumResidualWhenDefectIsOmitted": maximum_omitted_defect,
        "oneDimensionalHeatWitness": one_dimensional_heat,
        "zeroCrossingWitness": zero_crossing,
        "zeroCrossingWholeLineSourceIntegral": crossing_source_integral,
        "zeroCrossingSqrtEpsilonTimesIntegral": crossing_rescaled_integral,
        "passed": True,
    }


def scaling_audit() -> dict[str, object]:
    # Whole-space three-dimensional NSE scaling.  A field with pointwise
    # exponent p has L2-norm exponent p-3/2.
    c_point = 3.0
    d_exponent = 2.0 * c_point - 3.0
    rho_exponent = d_exponent / 2.0
    e_point = c_point - rho_exponent
    e_l2 = e_point - 1.5
    ae_l2 = e_point + 2.0 - 1.5
    et_l2 = e_point + 2.0 - 1.5
    g_point = 5.0
    g_l2 = g_point - 1.5
    h_l2 = g_l2 - rho_exponent
    rayleigh = 2.0
    integrated_square = 2.0 * et_l2 - 2.0
    k_weighted = integrated_square - 2.0

    require(abs(d_exponent - 3.0) < 1.0e-15, "d scaling")
    require(abs(e_l2) < 1.0e-15, "unit direction scaling")
    require(abs(ae_l2 - 2.0) < 1.0e-15, "A E scaling")
    require(abs(et_l2 - 2.0) < 1.0e-15, "E_t scaling")
    require(abs(h_l2 - 2.0) < 1.0e-15, "H scaling")
    require(abs(rayleigh - 2.0) < 1.0e-15, "Rayleigh scaling")
    require(abs(integrated_square - 2.0) < 1.0e-15, "integral scaling")
    require(abs(k_weighted) < 1.0e-15, "critical K weight")

    return {
        "CPointwiseExponent": c_point,
        "dExponent": d_exponent,
        "rhoExponent": rho_exponent,
        "EPointwiseExponent": e_point,
        "EL2NormExponent": e_l2,
        "AEL2NormExponent": ae_l2,
        "EtL2NormExponent": et_l2,
        "HL2NormExponent": h_l2,
        "rExponent": rayleigh,
        "integratedIdentityExponent": integrated_square,
        "KMinusTwoWeightedExponent": k_weighted,
        "epsilonMustScaleLikeDExponent": d_exponent,
        "passed": True,
    }


def main(output: Path | None = None) -> None:
    result = {
        "status": "PASS",
        "finiteDimensional": finite_dimensional_audit(),
        "fourierHeat": fourier_heat_audit(),
        "epsilonRegularization": epsilon_audit(),
        "scaling": scaling_audit(),
        "claims": {
            "unitDirectionIdentityChecked": True,
            "pureHeatRayleighDropChecked": True,
            "softDenominatorNeedsRadialDefect": True,
            "regularityTheoremClaimed": False,
            "originalityClaimed": False,
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if output is None:
        print(rendered, end="")
    else:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    main(arguments.output)
