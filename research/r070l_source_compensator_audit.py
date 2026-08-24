#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70L source-compensator gate.

The producer checks the filtered strain algebra, the quadratic source/shape
combination, and a smooth periodic initial-face pair with identical local
strain and identical normalized global vorticity covariance but opposite
time derivatives of their source/shape correlation.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


Mode = tuple[int, int, int]
Series = dict[Mode, sp.Expr]


def clean(series: Series) -> Series:
    result: Series = {}
    for mode, coefficient in series.items():
        simplified = sp.simplify(coefficient)
        if simplified != 0:
            result[mode] = simplified
    return result


def add(*series_list: Series) -> Series:
    result: Series = {}
    for series in series_list:
        for mode, coefficient in series.items():
            result[mode] = result.get(mode, sp.Integer(0)) + coefficient
    return clean(result)


def scale(series: Series, factor: sp.Expr | int) -> Series:
    return clean({mode: factor * value for mode, value in series.items()})


def derivative(series: Series, axis: int) -> Series:
    return clean(
        {
            mode: sp.I * mode[axis] * coefficient
            for mode, coefficient in series.items()
        }
    )


def laplacian(series: Series) -> Series:
    return clean(
        {
            mode: -sum(component**2 for component in mode) * coefficient
            for mode, coefficient in series.items()
        }
    )


def multiply(first: Series, second: Series) -> Series:
    result: Series = {}
    for left_mode, left_value in first.items():
        for right_mode, right_value in second.items():
            mode = tuple(
                left_mode[index] + right_mode[index] for index in range(3)
            )
            result[mode] = (
                result.get(mode, sp.Integer(0)) + left_value * right_value
            )
    return clean(result)


def value_at_origin(series: Series) -> sp.Expr:
    return sp.simplify(sum(series.values(), sp.Integer(0)))


def mean_product(first: Series, second: Series) -> sp.Expr:
    return sp.simplify(
        sum(
            coefficient * second.get(tuple(-entry for entry in mode), 0)
            for mode, coefficient in first.items()
        )
    )


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def dev(matrix: sp.Matrix) -> sp.Matrix:
    return sp.simplify(matrix - sp.trace(matrix) * sp.eye(3) / 3)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def psi_base() -> Series:
    # -sin(x) sin(y)=(cos(x+y)-cos(x-y))/2.
    quarter = sp.Rational(1, 4)
    return {
        (1, 1, 0): quarter,
        (-1, -1, 0): quarter,
        (1, -1, 0): -quarter,
        (-1, 1, 0): -quarter,
    }


def psi_perturbation(m: int, n: int) -> Series:
    # (1-cos(mx))(1-cos(ny)).
    result: Series = {
        (0, 0, 0): sp.Integer(1),
        (m, 0, 0): -sp.Rational(1, 2),
        (-m, 0, 0): -sp.Rational(1, 2),
        (0, n, 0): -sp.Rational(1, 2),
        (0, -n, 0): -sp.Rational(1, 2),
    }
    for sign_x in (-1, 1):
        for sign_y in (-1, 1):
            result[(sign_x * m, sign_y * n, 0)] = sp.Rational(1, 4)
    return result


def velocity(perturbation: tuple[int, int], amplitude: sp.Expr, carrier: sp.Expr) -> list[Series]:
    psi = add(psi_base(), scale(psi_perturbation(*perturbation), amplitude))
    u1 = scale(derivative(psi, 1), -1)
    u2 = derivative(psi, 0)
    shear = {
        (0, 0, 1): carrier / 2,
        (0, 0, -1): carrier / 2,
        (0, 0, 0): -carrier,
    }
    return [u1, add(u2, shear), {}]


def gradient_series(velocity_series: list[Series]) -> list[list[Series]]:
    return [
        [derivative(velocity_series[i], j) for j in range(3)]
        for i in range(3)
    ]


def curl_series(velocity_series: list[Series]) -> list[Series]:
    return [
        add(derivative(velocity_series[2], 1), scale(derivative(velocity_series[1], 2), -1)),
        add(derivative(velocity_series[0], 2), scale(derivative(velocity_series[2], 0), -1)),
        add(derivative(velocity_series[1], 0), scale(derivative(velocity_series[0], 1), -1)),
    ]


def pressure_source(gradient: list[list[Series]]) -> Series:
    terms: list[Series] = []
    for i in range(3):
        for j in range(3):
            terms.append(multiply(gradient[i][j], gradient[j][i]))
    return add(*terms)


def pressure_hessian(source: Series) -> sp.Matrix:
    hessian = sp.zeros(3)
    for mode, coefficient in source.items():
        norm_square = sum(component**2 for component in mode)
        if norm_square == 0:
            continue
        for i in range(3):
            for j in range(3):
                hessian[i, j] -= (
                    sp.Rational(mode[i] * mode[j], norm_square) * coefficient
                )
    return hessian.applyfunc(sp.simplify)


def origin_matrix(matrix_series: list[list[Series]]) -> sp.Matrix:
    return sp.Matrix(
        [
            [value_at_origin(matrix_series[i][j]) for j in range(3)]
            for i in range(3)
        ]
    )


def covariance(vorticity: list[Series]) -> sp.Matrix:
    return sp.Matrix(
        [
            [mean_product(vorticity[i], vorticity[j]) for j in range(3)]
            for i in range(3)
        ]
    ).applyfunc(sp.simplify)


def vorticity_time_derivative(
    velocity_series: list[Series],
    vorticity: list[Series],
    viscosity: sp.Expr,
) -> list[Series]:
    result: list[Series] = []
    for i in range(3):
        transport: list[Series] = []
        stretching: list[Series] = []
        for axis in range(3):
            transport.append(
                multiply(velocity_series[axis], derivative(vorticity[i], axis))
            )
            stretching.append(
                multiply(vorticity[axis], derivative(velocity_series[i], axis))
            )
        result.append(
            add(
                scale(add(*transport), -1),
                add(*stretching),
                scale(laplacian(vorticity[i]), viscosity),
            )
        )
    return result


def covariance_derivative(
    vorticity: list[Series], vorticity_derivative: list[Series]
) -> sp.Matrix:
    return sp.Matrix(
        [
            [
                sp.simplify(
                    mean_product(vorticity_derivative[i], vorticity[j])
                    + mean_product(vorticity[i], vorticity_derivative[j])
                )
                for j in range(3)
            ]
            for i in range(3)
        ]
    )


# ---------------------------------------------------------------------------
# Exact matrix algebra for the resolved strain equation and q ledger.
# ---------------------------------------------------------------------------
s11, s22, s12, s13, s23 = sp.symbols(
    "s11 s22 s12 s13 s23", real=True
)
wx, wy, wz = sp.symbols("wx wy wz", real=True)
r11, r22, r12, r13, r23 = sp.symbols(
    "r11 r22 r12 r13 r23", real=True
)

sigma = sp.Matrix(
    [
        [s11, s12, s13],
        [s12, s22, s23],
        [s13, s23, -s11 - s22],
    ]
)
rotation = sp.Matrix(
    [
        [0, -wz / 2, wy / 2],
        [wz / 2, 0, -wx / 2],
        [-wy / 2, wx / 2, 0],
    ]
)
omega = sp.Matrix([wx, wy, wz])
shape = sp.Matrix(
    [
        [r11, r12, r13],
        [r12, r22, r23],
        [r13, r23, 1 - r11 - r22],
    ]
)
anisotropy = sp.simplify(shape - sp.eye(3) / 3)
correlation = sp.simplify(sp.trace(sigma * anisotropy))

sym_gradient_square = sp.simplify(
    ((sigma + rotation) ** 2 + ((sigma + rotation) ** 2).T) / 2
)
rotation_square_expected = sp.simplify(
    (omega * omega.T - omega.dot(omega) * sp.eye(3)) / 4
)
combined_quadratic = sp.simplify(
    -sp.trace(dev(sigma**2) * anisotropy)
    + 2 * (sp.trace(shape * sigma**2) - correlation**2)
)
combined_quadratic_expected = sp.simplify(
    sp.trace(anisotropy * sigma**2)
    + sp.Rational(2, 3) * sp.trace(sigma**2)
    - 2 * correlation**2
)

axis_sigma = sp.diag(sp.Rational(-1, 2), sp.Rational(-1, 2), 1)
axis_rank = sp.diag(0, 0, 1)
axis_iso = sp.eye(3) / 3

strain_algebra_checks = {
    "symmetricGradientSquareSplits": matrix_is_zero(
        sym_gradient_square - sigma**2 - rotation**2
    ),
    "rotationSquareMatchesVorticityDyad": matrix_is_zero(
        rotation**2 - rotation_square_expected
    ),
    "combinedQuadraticIdentity": sp.simplify(
        combined_quadratic - combined_quadratic_expected
    )
    == 0,
    "combinedQuadraticCanBeNegative": sp.simplify(
        combined_quadratic.subs(
            {
                s11: -sp.Rational(1, 2),
                s22: -sp.Rational(1, 2),
                s12: 0,
                s13: 0,
                s23: 0,
                r11: 0,
                r22: 0,
                r12: 0,
                r13: 0,
                r23: 0,
            }
        )
        + sp.Rational(1, 2)
    )
    == 0,
    "combinedQuadraticCanBePositive": sp.simplify(
        (
            -sp.trace(dev(axis_sigma**2) * (axis_iso - sp.eye(3) / 3))
            + 2
            * (
                sp.trace(axis_iso * axis_sigma**2)
                - sp.trace(axis_sigma * axis_iso) ** 2
            )
        )
        - 1
    )
    == 0,
}


# ---------------------------------------------------------------------------
# Explicit periodic initial-face pair.
# ---------------------------------------------------------------------------
amplitude = sp.Integer(2)
viscosity = sp.Integer(1)
carrier = sp.sqrt(120)
expected_sigma = sp.diag(1, -1, 0)
expected_shape = sp.diag(sp.Rational(1, 2), 0, sp.Rational(1, 2))
expected_anisotropy = expected_shape - sp.eye(3) / 3

witnesses: dict[str, dict[str, object]] = {}
witness_checks: dict[str, bool] = {}
comparison_records: dict[str, dict[str, sp.Expr | sp.Matrix]] = {}

for label, perturbation in {"minus": (1, 2), "plus": (2, 1)}.items():
    u = velocity(perturbation, amplitude, carrier)
    gradient = gradient_series(u)
    gradient_zero = origin_matrix(gradient)
    strain_zero = sp.simplify((gradient_zero + gradient_zero.T) / 2)
    omega_series = curl_series(u)
    omega_zero = sp.Matrix([value_at_origin(component) for component in omega_series])
    q_pressure = pressure_source(gradient)
    hessian = pressure_hessian(q_pressure)
    kinetic_energy_twice = sp.simplify(
        sum(mean_product(component, component) for component in u)
    )
    q_matrix = covariance(omega_series)
    energy = sp.simplify(sp.trace(q_matrix))
    shape_zero = sp.simplify(q_matrix / energy)
    anisotropy_zero = sp.simplify(shape_zero - sp.eye(3) / 3)

    omega_t = vorticity_time_derivative(u, omega_series, viscosity)
    q_matrix_t = covariance_derivative(omega_series, omega_t)
    energy_t = sp.simplify(sp.trace(q_matrix_t))
    anisotropy_t = sp.simplify(
        q_matrix_t / energy - q_matrix * energy_t / energy**2
    )

    laplace_strain = origin_matrix(
        [
            [
                laplacian(
                    scale(
                        add(gradient[i][j], gradient[j][i]),
                        sp.Rational(1, 2),
                    )
                )
                for j in range(3)
            ]
            for i in range(3)
        ]
    )
    sigma_material_t = sp.simplify(
        -((gradient_zero**2 + (gradient_zero**2).T) / 2)
        - hessian
        + viscosity * laplace_strain
    )
    source_shape_correlation = sp.simplify(
        sp.trace(strain_zero * anisotropy_zero)
    )
    correlation_t = sp.simplify(
        sp.trace(sigma_material_t * anisotropy_zero)
        + sp.trace(strain_zero * anisotropy_t)
    )
    pressure_pairing = sp.simplify(sp.trace(hessian * anisotropy_zero))
    local_gradient_pairing = sp.simplify(
        -sp.trace(
            ((gradient_zero**2 + (gradient_zero**2).T) / 2)
            * anisotropy_zero
        )
    )
    viscous_pairing = sp.simplify(
        viscosity * sp.trace(laplace_strain * anisotropy_zero)
    )
    shape_derivative_pairing = sp.simplify(
        sp.trace(strain_zero * anisotropy_t)
    )

    expected_h11 = (
        -1 - sp.Rational(216, 85)
        if label == "minus"
        else -1 + sp.Rational(216, 85)
    )
    expected_correlation_t = (
        sp.Rational(3901, 2040)
        if label == "minus"
        else -sp.Rational(1283, 2040)
    )

    witness_checks.update(
        {
            f"{label}VelocityIsDivergenceFree": all(
                sp.simplify(
                    sum(
                        mode[i] * coefficient[i] for i in range(3)
                    )
                )
                == 0
                for mode, coefficient in {
                    mode: sp.Matrix(
                        [component.get(mode, 0) for component in u]
                    )
                    for mode in set().union(*(component.keys() for component in u))
                }.items()
            ),
            f"{label}VelocityVanishesAtOrigin": all(
                value_at_origin(component) == 0 for component in u
            ),
            f"{label}LocalStrainIsCommon": matrix_is_zero(
                strain_zero - expected_sigma
            ),
            f"{label}LocalVorticityVanishes": matrix_is_zero(
                omega_zero
            ),
            f"{label}ShapeIsCommon": matrix_is_zero(
                shape_zero - expected_shape
            ),
            f"{label}PressureH11": sp.simplify(
                hessian[0, 0] - expected_h11
            )
            == 0,
            f"{label}PressureHasNoCarrierCrossSource": all(
                mode[2] == 0 for mode in q_pressure
            ),
            f"{label}CorrelationIsOneHalf": source_shape_correlation
            == sp.Rational(1, 2),
            f"{label}CorrelationDerivativeHasCertifiedSign": sp.simplify(
                correlation_t - expected_correlation_t
            )
            == 0,
            f"{label}LocalGradientContribution": local_gradient_pairing
            == sp.Rational(1, 6),
            f"{label}ViscousSourceContribution": viscous_pairing == -1,
            f"{label}ShapeDerivativeContribution": shape_derivative_pairing
            == sp.Rational(197, 120),
        }
    )

    comparison_records[label] = {
        "covariance": q_matrix,
        "localGradient": local_gradient_pairing,
        "viscosity": viscous_pairing,
        "shapeDerivative": shape_derivative_pairing,
        "pressure": -pressure_pairing,
        "velocityNormSquare": kinetic_energy_twice,
    }

    witnesses[label] = {
        "perturbation": list(perturbation),
        "velocityGradientAtOrigin": [
            [str(entry) for entry in row] for row in gradient_zero.tolist()
        ],
        "vorticityAtOrigin": [str(entry) for entry in omega_zero],
        "vorticityCovariancePerUnitVolume": [
            [str(entry) for entry in row] for row in q_matrix.tolist()
        ],
        "velocityNormSquarePerUnitVolume": str(kinetic_energy_twice),
        "normalizedShape": [
            [str(entry) for entry in row] for row in shape_zero.tolist()
        ],
        "pressureHessianAtOrigin": [
            [str(entry) for entry in row] for row in hessian.tolist()
        ],
        "pressurePairingHColonB": str(pressure_pairing),
        "derivativeLedger": {
            "localGradient": str(local_gradient_pairing),
            "viscousSource": str(viscous_pairing),
            "pressure": str(-pressure_pairing),
            "shapeDerivative": str(shape_derivative_pairing),
        },
        "sigmaColonB": str(source_shape_correlation),
        "sigmaColonBdot": str(sp.trace(strain_zero * anisotropy_t)),
        "materialSigmaDotColonB": str(
            sp.trace(sigma_material_t * anisotropy_zero)
        ),
        "materialDerivativeOfSigmaColonB": str(correlation_t),
    }

witness_checks.update(
    {
        "pairHasIdenticalCovariance": matrix_is_zero(
            comparison_records["minus"]["covariance"]
            - comparison_records["plus"]["covariance"]
        ),
        "pairHasIdenticalLocalGradientContribution": comparison_records[
            "minus"
        ]["localGradient"]
        == comparison_records["plus"]["localGradient"],
        "pairHasIdenticalViscousSourceContribution": comparison_records[
            "minus"
        ]["viscosity"]
        == comparison_records["plus"]["viscosity"],
        "pairHasIdenticalShapeDerivativeContribution": comparison_records[
            "minus"
        ]["shapeDerivative"]
        == comparison_records["plus"]["shapeDerivative"],
        "pairHasIdenticalKineticEnergy": comparison_records["minus"][
            "velocityNormSquare"
        ]
        == comparison_records["plus"]["velocityNormSquare"],
        "onlyPressureContributionSwitchesInQdotLedger": sp.simplify(
            comparison_records["minus"]["pressure"]
            - comparison_records["plus"]["pressure"]
            - (sp.Rational(3901, 2040) + sp.Rational(1283, 2040))
        )
        == 0,
    }
)


# The exterior pressure-Hessian realization from R0.70J changes the center
# pressure tensor while leaving the buffered core velocity and vorticity
# ledger fixed.  The finite-dimensional duality below is the algebraic part
# of the resulting local-functional no-go theorem.
d11, d22, d12, d13, d23 = sp.symbols(
    "d11 d22 d12 d13 d23", real=True
)
functional_sigma_gradient = sp.Matrix(
    [
        [d11, d12, d13],
        [d12, d22, d23],
        [d13, d23, -d11 - d22],
    ]
)
pressure_plus = functional_sigma_gradient
pressure_minus = -functional_sigma_gradient
pressure_duality_checks = {
    "functionalGradientIsTraceFree": sp.trace(functional_sigma_gradient) == 0,
    "oppositePressureChoicesGiveOppositeDerivatives": sp.simplify(
        -sp.trace(functional_sigma_gradient * pressure_plus)
        + sp.trace(functional_sigma_gradient * pressure_minus)
    )
    == -2 * sp.trace(functional_sigma_gradient**2),
    "nonzeroGradientHasStrictPressureDirection": sp.trace(
        functional_sigma_gradient**2
    ).subs({d11: 1, d22: -1, d12: 0, d13: 0, d23: 0})
    > 0,
}


# ---------------------------------------------------------------------------
# Auxiliary two-mode Beltrami filter split.
# ---------------------------------------------------------------------------
x_coordinate, z_coordinate = sp.symbols("x_coordinate z_coordinate", real=True)
wave_number = sp.symbols("wave_number", positive=True, integer=True)
filter_multiplier = sp.symbols("filter_multiplier", real=True)
split_amplitude = sp.symbols("split_amplitude", real=True)

beltrami_velocity = sp.Matrix(
    [
        sp.sin(wave_number * z_coordinate),
        sp.sin(wave_number * x_coordinate)
        + sp.cos(wave_number * z_coordinate),
        sp.cos(wave_number * x_coordinate),
    ]
)
beltrami_curl = sp.Matrix(
    [
        -sp.diff(beltrami_velocity[1], z_coordinate),
        sp.diff(beltrami_velocity[0], z_coordinate)
        - sp.diff(beltrami_velocity[2], x_coordinate),
        sp.diff(beltrami_velocity[1], x_coordinate),
    ]
)
beltrami_laplacian = beltrami_velocity.applyfunc(
    lambda entry: sp.diff(entry, x_coordinate, 2)
    + sp.diff(entry, z_coordinate, 2)
)
beltrami_nonlinearity = sp.simplify(
    beltrami_velocity[0] * beltrami_velocity.diff(x_coordinate)
    + beltrami_velocity[2] * beltrami_velocity.diff(z_coordinate)
)
beltrami_head = (
    1
    + sp.sin(wave_number * x_coordinate)
    * sp.cos(wave_number * z_coordinate)
)
beltrami_head_gradient = sp.Matrix(
    [
        sp.diff(beltrami_head, x_coordinate),
        0,
        sp.diff(beltrami_head, z_coordinate),
    ]
)
pressure_filter_share = -filter_multiplier * split_amplitude
sgs_filter_share = -(1 - filter_multiplier) * split_amplitude

beltrami_filter_checks = {
    "curlEigenfield": matrix_is_zero(
        beltrami_curl - wave_number * beltrami_velocity
    ),
    "laplacianEigenfield": matrix_is_zero(
        beltrami_laplacian + wave_number**2 * beltrami_velocity
    ),
    "nonlinearityIsGradient": matrix_is_zero(
        beltrami_nonlinearity - beltrami_head_gradient
    ),
    "pressureAndSgsSumIsFilterIndependent": sp.simplify(
        pressure_filter_share + sgs_filter_share + split_amplitude
    )
    == 0,
    "identityFilterPlacesShareInPressure": (
        pressure_filter_share.subs(filter_multiplier, 1) == -split_amplitude
        and sgs_filter_share.subs(filter_multiplier, 1) == 0
    ),
    "zeroMixedModePlacesShareInSgs": (
        pressure_filter_share.subs(filter_multiplier, 0) == 0
        and sgs_filter_share.subs(filter_multiplier, 0) == -split_amplitude
    ),
}


all_groups = {
    "strainAlgebra": strain_algebra_checks,
    "periodicInitialFacePair": witness_checks,
    "pressureDuality": pressure_duality_checks,
    "beltramiFilterSplit": beltrami_filter_checks,
}
for group_name, group in all_groups.items():
    for check_name, value in group.items():
        require(bool(value), f"{group_name}.{check_name}")
        group[check_name] = bool(value)


payload = {
    "release": "R0.70L",
    "status": "exact-source-evolution-compensator-obstruction-audit",
    "arithmetic": "exact SymPy Fourier, matrix, polynomial, and rational arithmetic",
    "checks": {name: all(values.values()) for name, values in all_groups.items()},
    "checkDetails": all_groups,
    "resolvedStrainEquation": {
        "filteredMomentum": "D_U U=-grad(P)+nu*Delta(U)-div(tau)",
        "source": "Sigma(t)=S(U)(X(t),t), Xdot=U(X(t),t)",
        "evolution": "SigmaDot=-dev(Sigma**2)-dev(W**2)-dev(Hess(P))+nu*Delta(S)-dev(sym(grad(div(tau))))",
        "rotationSquare": "dev(W**2)=dev(Omega tensor Omega)/4",
    },
    "correlationLedger": {
        "shape": "R=Q/tr(Q), B=R-I/3",
        "correlation": "q=Sigma:B",
        "combinedLocalQuadratic": "B:Sigma**2+(2/3)*abs(Sigma)**2-2*q**2",
        "sign": "both signs occur before pressure, viscosity, SGS, cutoff, and covariance-residual terms",
    },
    "periodicWitness": {
        "streamFunctions": "psi_minus=-sin(x)sin(y)+2(1-cos(x))(1-cos(2y)); psi_plus=-sin(x)sin(y)+2(1-cos(2x))(1-cos(y))",
        "velocity": "u=(-partial_y psi, partial_x psi+sqrt(120)*(cos(z)-1), 0)",
        "commonLocalData": "u(0)=0, Sigma(0)=diag(1,-1,0), omega(0)=0",
        "commonShape": "R=diag(1/2,0,1/2), B=diag(1/6,-1/3,1/6), q=1/2",
        "viscosity": "nu=1",
        "oppositeDerivatives": "qdot_minus=3901/2040>0; qdot_plus=-1283/2040<0",
        "mechanism": "the pressure Hessian orientation switches while the normalized covariance and its instantaneous nonpressure ledger remain matched",
        "records": witnesses,
    },
    "localFunctionalNoGo": {
        "statement": "for a C1 instantaneous scalar Phi(Sigma,B), arbitrary STF center pressure variation contributes -D_Sigma Phi:H; a universal sign under the support-separated R0.70J pressure realization forces D_Sigma Phi=0",
        "scope": "smooth initial-face data with a buffered core and compact exterior pressure packets; it excludes only nontrivial instantaneous local source dependence",
        "survivingOptions": "nonlocal pressure information, spatial integration, time history, or adjacent-scale sums",
    },
    "beltramiFilterSplit": {
        "velocity": "v_N=(sin(N*z),sin(N*x)+cos(N*z),cos(N*x))",
        "identities": "curl(v_N)=N*v_N, Delta(v_N)=-N**2*v_N, and (v_N dot grad)v_N=grad(1+sin(N*x)*cos(N*z))",
        "pressureShare": "-theta*C",
        "sgsShare": "-(1-theta)*C",
        "invariantCombinedShare": "-C",
        "interpretation": "pressure and SGS shares depend on the filter convention even when their sum is exact",
    },
    "claimBoundary": {
        "proved": "the exact resolved-strain ledger, the indefinite combined quadratic, the explicit periodic opposite-sign pair, and the finite-dimensional pressure duality used by the local-functional no-go theorem",
        "analyticInput": "the compact support-separated realization of arbitrary STF center pressure Hessians proved and certified in R0.70J",
        "notClaimed": "a sign for a nonlocal or time-integrated compensator, a Leray-to-critical estimate, blow-up, global regularity, or a Millennium solution",
    },
}

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--output")
arguments = parser.parse_args()
rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
if arguments.output:
    Path(arguments.output).write_text(rendered, encoding="utf-8")
else:
    print(rendered, end="")
