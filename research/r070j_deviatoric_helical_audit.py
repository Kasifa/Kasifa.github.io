#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70J deviatoric-helical gate.

The producer verifies the finite tensor identities used in the R0.70J
report: the STF/deviatoric contraction, the helical projector and real-mode
symbol, a pointwise-positive Beltrami witness, signed versus positive angular
averages, a finite same-shell example, compact-core homotopy identities, and
the critical source/core scale ledger.

It does not computer-prove smooth cutoff support buffers, Littlewood--Paley
pseudolocal error bounds, literature completeness, persistence at one fixed
positive terminal time, or any Navier--Stokes regularity theorem.
"""

from __future__ import annotations

import json

import sympy as sp


x1, x2, x3, time = sp.symbols("x1 x2 x3 time", real=True)
theta, kappa, nu = sp.symbols("theta kappa nu", real=True, positive=True)
a, b, c, d, e = sp.symbols("a b c d e", real=True)
w1, w2, w3 = sp.symbols("w1 w2 w3", real=True)
coordinates = sp.Matrix([x1, x2, x3])
e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])


def divergence(field: sp.Matrix) -> sp.Expr:
    """Three-dimensional divergence in the fixed spatial coordinates."""

    return sp.simplify(
        sum(sp.diff(field[index], coordinates[index]) for index in range(3))
    )


def curl(field: sp.Matrix) -> sp.Matrix:
    """Three-dimensional curl in the fixed spatial coordinates."""

    return sp.Matrix(
        [
            sp.diff(field[2], x2) - sp.diff(field[1], x3),
            sp.diff(field[0], x3) - sp.diff(field[2], x1),
            sp.diff(field[1], x1) - sp.diff(field[0], x2),
        ]
    ).applyfunc(sp.simplify)


def strain(field: sp.Matrix) -> sp.Matrix:
    """Symmetric velocity gradient."""

    jacobian = field.jacobian(coordinates)
    return ((jacobian + jacobian.T) / 2).applyfunc(sp.simplify)


def laplacian(field: sp.Matrix) -> sp.Matrix:
    """Componentwise spatial Laplacian."""

    return field.applyfunc(
        lambda value: sp.simplify(
            sum(sp.diff(value, variable, 2) for variable in coordinates)
        )
    )


def matrix_contraction(left: sp.Matrix, right: sp.Matrix) -> sp.Expr:
    """Frobenius contraction of two 3 by 3 matrices."""

    return sp.simplify(sum(left[i, j] * right[i, j] for i in range(3) for j in range(3)))


# ---------------------------------------------------------------------------
# General STF and helical identities
# ---------------------------------------------------------------------------

generic_stf = sp.Matrix(
    [
        [a, b, c],
        [b, d, e],
        [c, e, -a - d],
    ]
)
w = sp.Matrix([w1, w2, w3])
deviatoric_square = w * w.T - (w.dot(w) / 3) * sp.eye(3)
stf_dev_difference = sp.simplify(
    matrix_contraction(generic_stf, deviatoric_square)
    - (w.T * generic_stf * w)[0]
)

helical_records: dict[str, dict[str, str]] = {}
helical_checks: dict[str, bool] = {}
real_mode_formula_checks: dict[str, bool] = {}

for helicity in (-1, 1):
    h = (e1 + sp.I * helicity * e2) / sp.sqrt(2)
    eigenvector_residual = (
        sp.I * e3.cross(h) - helicity * h
    ).applyfunc(sp.simplify)
    projector_contraction = sp.simplify(
        (sp.conjugate(h).T * generic_stf * h)[0]
    )
    spin_two_contraction = sp.simplify((h.T * generic_stf * h)[0])

    real_mode = sp.sqrt(2) * sp.Matrix(
        [sp.cos(theta), -helicity * sp.sin(theta), 0]
    )
    real_contraction = sp.expand_trig(
        sp.simplify((real_mode.T * generic_stf * real_mode)[0])
    )
    expected_real_contraction = (
        a
        + d
        + (a - d) * sp.cos(2 * theta)
        - 2 * helicity * b * sp.sin(2 * theta)
    )
    real_formula_residual = sp.trigsimp(
        sp.expand_trig(real_contraction - expected_real_contraction)
    )

    key = "positive" if helicity == 1 else "negative"
    helical_records[key] = {
        "basis": sp.sstr(h),
        "projectorContraction": sp.sstr(projector_contraction),
        "spinTwoContraction": sp.sstr(spin_two_contraction),
        "realModeContraction": sp.sstr(expected_real_contraction),
    }
    helical_checks[f"{key}HelicalEigenvector"] = (
        eigenvector_residual == sp.zeros(3, 1)
    )
    helical_checks[f"{key}ProjectorContraction"] = (
        sp.simplify(projector_contraction + (e3.T * generic_stf * e3)[0] / 2)
        == 0
    )
    helical_checks[f"{key}SpinTwoContraction"] = (
        sp.simplify(
            spin_two_contraction
            - (a - d + 2 * sp.I * helicity * b) / 2
        )
        == 0
    )
    real_mode_formula_checks[f"{key}RealModeFormula"] = (
        real_formula_residual == 0
    )


# ---------------------------------------------------------------------------
# Pointwise-positive Beltrami witness and angular ledgers
# ---------------------------------------------------------------------------

S0 = sp.diag(sp.Rational(1, 2), sp.Rational(1, 2), -1)
helicity_symbol = sp.symbols("helicity_symbol", integer=True)

positive_mode_checks: dict[str, bool] = {}
positive_mode_records: dict[str, str] = {}
for helicity in (-1, 1):
    phase = kappa * x3
    omega_mode = sp.sqrt(2) * sp.Matrix(
        [sp.cos(phase), -helicity * sp.sin(phase), 0]
    )
    velocity_mode = omega_mode / (helicity * kappa)
    helical_vector_potential = omega_mode / kappa**2
    coupling = sp.trigsimp((omega_mode.T * S0 * omega_mode)[0])
    self_stretching = sp.trigsimp(
        (omega_mode.T * strain(velocity_mode) * omega_mode)[0]
    )
    key = "positive" if helicity == 1 else "negative"
    positive_mode_checks[f"{key}BeltramiCurl"] = (
        (curl(omega_mode) - helicity * kappa * omega_mode).applyfunc(sp.trigsimp)
        == sp.zeros(3, 1)
    )
    positive_mode_checks[f"{key}VelocityVorticity"] = (
        (curl(velocity_mode) - omega_mode).applyfunc(sp.trigsimp)
        == sp.zeros(3, 1)
    )
    positive_mode_checks[f"{key}VectorPotentialRecoversVelocity"] = (
        (curl(helical_vector_potential) - velocity_mode).applyfunc(
            sp.trigsimp
        )
        == sp.zeros(3, 1)
    )
    positive_mode_checks[f"{key}PointwiseCoupling"] = coupling == 1
    positive_mode_checks[f"{key}SelfStretchingZero"] = self_stretching == 0
    positive_mode_records[f"{key}Coupling"] = sp.sstr(coupling)
    positive_mode_records[f"{key}SelfStretching"] = sp.sstr(self_stretching)

z = sp.symbols("z", real=True)
quadrupole = (3 * z**2 - 1) / 2
sphere_signed_average = sp.simplify(
    sp.Rational(1, 2) * sp.integrate(quadrupole, (z, -1, 1))
)
sphere_positive_average = sp.simplify(
    sp.integrate(quadrupole, (z, 1 / sp.sqrt(3), 1))
)
great_circle_average = sp.simplify((e3.T * S0 * e3)[0] / 2)

xi_one = e3
xi_two = sp.Matrix([sp.Rational(3, 5), 0, sp.Rational(4, 5)])
xi_two_quadratic = sp.simplify((xi_two.T * S0 * xi_two)[0])
same_shell_pairing = sp.simplify(
    -(xi_one.T * S0 * xi_one)[0] - (xi_two.T * S0 * xi_two)[0]
)
axis_symbols = [sp.simplify(-(axis.T * S0 * axis)[0]) for axis in (e1, e2, e3)]

angular_checks = {
    "sphereSignedAverageZero": sphere_signed_average == 0,
    "spherePositivePartNonzero": sphere_positive_average == sp.sqrt(3) / 9,
    "greatCircleAverageNonzero": great_circle_average == -sp.Rational(1, 2),
    "sameShellSecondDirection": xi_two_quadratic == -sp.Rational(23, 50),
    "sameShellTwoModePositive": same_shell_pairing == sp.Rational(73, 50),
    "threeAxisSignedDesign": sum(axis_symbols) == 0,
    "threeAxisPositivePartSurvives": sum(max(value, 0) for value in axis_symbols) == 1,
}


# ---------------------------------------------------------------------------
# Harmonic jet, compact-core homotopies, and a genuine periodic NSE mode
# ---------------------------------------------------------------------------

harmonic_potential = x1**2 / 4 + x2**2 / 4 - x3**2 / 2
external_velocity = S0 * coordinates
external_homotopy = -sp.Rational(1, 3) * coordinates.cross(external_velocity)
constant_core_velocity = sp.Rational(1, 2) * e1.cross(coordinates)
constant_core_homotopy = (
    -sp.Rational(1, 3) * coordinates.cross(constant_core_velocity)
)

base_wave = sp.Matrix([sp.sin(x3), sp.cos(x3), 0])
periodic_nse_mode = sp.exp(-nu * time) * base_wave
transport = sp.Matrix(
    [
        sum(
            periodic_nse_mode[j] * sp.diff(periodic_nse_mode[i], coordinates[j])
            for j in range(3)
        )
        for i in range(3)
    ]
).applyfunc(sp.simplify)
periodic_nse_residual = (
    periodic_nse_mode.diff(time) + transport - nu * laplacian(periodic_nse_mode)
).applyfunc(sp.simplify)

realization_checks = {
    "harmonicQuadratic": sp.simplify(sum(sp.diff(harmonic_potential, variable, 2) for variable in coordinates)) == 0,
    "harmonicHessianIsS0": sp.hessian(harmonic_potential, coordinates) == S0,
    "externalVelocityDivergenceFree": divergence(external_velocity) == 0,
    "externalVelocityCurlFree": curl(external_velocity) == sp.zeros(3, 1),
    "externalHomotopyRecoversVelocity": curl(external_homotopy) == external_velocity,
    "externalCoreStrainIsS0": strain(external_velocity) == S0,
    "constantCoreVelocityDivergenceFree": divergence(constant_core_velocity) == 0,
    "constantCoreHomotopyRecoversVelocity": (
        curl(constant_core_homotopy) == constant_core_velocity
    ),
    "constantCoreVorticityE1": curl(constant_core_velocity) == e1,
    "constantCoreStrainZero": (
        strain(constant_core_velocity) == sp.zeros(3)
    ),
    "periodicModeDivergenceFree": divergence(periodic_nse_mode) == 0,
    "periodicModeBeltrami": curl(periodic_nse_mode) == periodic_nse_mode,
    "periodicModeNonlinearityZero": transport == sp.zeros(3, 1),
    "periodicModeNseResidualZero": periodic_nse_residual == sp.zeros(3, 1),
}


# ---------------------------------------------------------------------------
# Exact critical scale ledger
# ---------------------------------------------------------------------------

r, Lambda, amplitude = sp.symbols("r Lambda amplitude", positive=True)
R = Lambda * r
source_strain_scale = amplitude * R**-2
core_vorticity_scale = amplitude * r**-2
core_volume_scale = r**3
time_window_scale = r**2
moment_scale = sp.simplify(core_volume_scale * core_vorticity_scale**2)
critical_moment_scale = sp.simplify(r * moment_scale)
source_coordinate_scale = sp.simplify(r**2 * source_strain_scale)
core_dual_coordinate_scale = sp.simplify(r**-2 * critical_moment_scale)
normalized_pairing_scale = sp.simplify(
    source_coordinate_scale * core_dual_coordinate_scale * time_window_scale
)
source_square_norm_scale = sp.simplify(
    r**-1 * source_coordinate_scale**2 * time_window_scale
)
core_dual_square_norm_scale = sp.simplify(
    r * core_dual_coordinate_scale**2 * time_window_scale
)
cauchy_product_scale = sp.simplify(
    sp.sqrt(source_square_norm_scale * core_dual_square_norm_scale)
)
carrier_energy_scale = sp.simplify(amplitude**2 * r**-2 * r**3)
carrier_window_dissipation_scale = sp.simplify(
    amplitude**2 * r**-4 * r**3 * time_window_scale
)
leray_normalized_amplitude = r**-sp.Rational(1, 2)
leray_source_square_scale = sp.simplify(
    source_square_norm_scale.subs(
        amplitude, leray_normalized_amplitude
    )
)
leray_core_dual_square_scale = sp.simplify(
    core_dual_square_norm_scale.subs(
        amplitude, leray_normalized_amplitude
    )
)
leray_pairing_scale = sp.simplify(
    normalized_pairing_scale.subs(
        amplitude, leray_normalized_amplitude
    )
)
leray_energy_scale = sp.simplify(
    carrier_energy_scale.subs(amplitude, leray_normalized_amplitude)
)
leray_dissipation_scale = sp.simplify(
    carrier_window_dissipation_scale.subs(
        amplitude, leray_normalized_amplitude
    )
)

scale_checks = {
    "zerothMomentScale": moment_scale == amplitude**2 / r,
    "criticalMomentScaleInvariant": critical_moment_scale == amplitude**2,
    "sourceCoordinateScale": (
        source_coordinate_scale == amplitude / Lambda**2
    ),
    "coreDualCoordinateScale": (
        core_dual_coordinate_scale == amplitude**2 / r**2
    ),
    "normalizedPairingScaleInvariant": (
        normalized_pairing_scale == amplitude**3 / Lambda**2
    ),
    "sourceSquareNormScale": (
        source_square_norm_scale == amplitude**2 * r / Lambda**4
    ),
    "coreDualSquareNormScale": (
        core_dual_square_norm_scale == amplitude**4 / r
    ),
    "cauchyProductMatchesPairingScale": (
        cauchy_product_scale == amplitude**3 / Lambda**2
    ),
    "carrierEnergyScale": carrier_energy_scale == amplitude**2 * r,
    "carrierWindowDissipationScale": (
        carrier_window_dissipation_scale == amplitude**2 * r
    ),
    "lerayNormalizedSourceSquareScale": (
        leray_source_square_scale == Lambda**-4
    ),
    "lerayNormalizedCoreDualSquareScale": (
        leray_core_dual_square_scale == r**-3
    ),
    "lerayNormalizedPairingScale": (
        leray_pairing_scale
        == r**-sp.Rational(3, 2) / Lambda**2
    ),
    "lerayNormalizedEnergyScale": leray_energy_scale == 1,
    "lerayNormalizedWindowDissipationScale": (
        leray_dissipation_scale == 1
    ),
}


check_groups = {
    "stfAndHelical": {
        "stfDevIdentity": stf_dev_difference == 0,
        **helical_checks,
        **real_mode_formula_checks,
    },
    "positiveBeltrami": positive_mode_checks,
    "angularAverages": angular_checks,
    "realizationAndNseMode": realization_checks,
    "criticalScaleLedger": scale_checks,
}

checks = {
    group_name: all(group_checks.values())
    for group_name, group_checks in check_groups.items()
}

if not all(checks.values()):
    failures = {
        group_name: [name for name, passed in group_checks.items() if not passed]
        for group_name, group_checks in check_groups.items()
        if not all(group_checks.values())
    }
    raise AssertionError(f"failed exact checks: {failures}")

result = {
    "status": "exact-symbolic-deviatoric-helical-audit",
    "release": "R0.70J",
    "arithmetic": "exact SymPy polynomial, trigonometric, and rational arithmetic",
    "helicalSymbol": {
        "phaseAveragedKernel": "K_S(xi)=-xi^T*S*xi",
        "helicityDependence": "none",
        "frequencyParity": "even under xi -> -xi",
        "records": helical_records,
    },
    "pointwisePositiveWitness": {
        "sourceTensor": [[sp.sstr(value) for value in row] for row in S0.tolist()],
        "waveDirection": "e3",
        "vorticity": "sqrt(2)*(e1*cos(theta)-sigma*e2*sin(theta))",
        "coupling": "1 pointwise for sigma=+1 and sigma=-1",
        "physicalCutoffConsequence": "integral chi*q equals integral chi for every nonnegative chi",
        "records": positive_mode_records,
    },
    "angularLedger": {
        "quadrupoleForS0": "(3*z^2-1)/2",
        "normalizedSphereSignedAverage": sp.sstr(sphere_signed_average),
        "normalizedSpherePositivePartAverage": sp.sstr(sphere_positive_average),
        "greatCircleAverageNormalE3": sp.sstr(great_circle_average),
        "sameShellDirections": ["(0,0,1)", "(3/5,0,4/5)"],
        "sameShellSecondQuadraticForm": sp.sstr(xi_two_quadratic),
        "sameShellPairing": sp.sstr(same_shell_pairing),
        "threeAxisSymbols": [sp.sstr(value) for value in axis_symbols],
    },
    "compactCoreAlgebra": {
        "harmonicPotential": sp.sstr(harmonic_potential),
        "externalVelocity": [sp.sstr(value) for value in external_velocity],
        "homotopyPotential": [sp.sstr(value) for value in external_homotopy],
        "constantCoreVelocity": [
            sp.sstr(value) for value in constant_core_velocity
        ],
        "constantCoreHomotopyPotential": [
            sp.sstr(value) for value in constant_core_homotopy
        ],
        "constantCoreVorticity": [
            sp.sstr(value) for value in curl(constant_core_velocity)
        ],
        "localizationRule": "curl[-zeta*x cross (S0*x)/3] equals S0*x where zeta=1",
        "supportBoundary": "vorticity created by derivatives of zeta remains in the transition annulus",
    },
    "periodicNseWitness": {
        "velocity": "exp(-nu*t)*(sin(x3),cos(x3),0)",
        "curl": "u",
        "nonlinearity": "0",
        "pressure": "constant",
        "boundary": "the selected external STF tensor is not this mode's self-generated pressure Hessian",
    },
    "criticalScaleLedger": {
        "outerToCoreRatio": "R=Lambda*r",
        "commonVelocityAmplitude": sp.sstr(amplitude),
        "sourceStrain": sp.sstr(source_strain_scale),
        "coreVorticity": sp.sstr(core_vorticity_scale),
        "zerothMoment": sp.sstr(moment_scale),
        "criticalMoment": sp.sstr(critical_moment_scale),
        "sourceCoordinate": sp.sstr(source_coordinate_scale),
        "coreDualCoordinate": sp.sstr(core_dual_coordinate_scale),
        "normalizedSpacetimePairing": sp.sstr(normalized_pairing_scale),
        "sourceSquareNorm": sp.sstr(source_square_norm_scale),
        "coreDualSquareNorm": sp.sstr(core_dual_square_norm_scale),
        "cauchyProduct": sp.sstr(cauchy_product_scale),
        "velocityEnergy": sp.sstr(carrier_energy_scale),
        "windowDissipation": sp.sstr(carrier_window_dissipation_scale),
        "lerayNormalizedAmplitude": sp.sstr(leray_normalized_amplitude),
        "lerayNormalizedSourceSquareNorm": sp.sstr(
            leray_source_square_scale
        ),
        "lerayNormalizedCoreDualSquareNorm": sp.sstr(
            leray_core_dual_square_scale
        ),
        "lerayNormalizedPairing": sp.sstr(leray_pairing_scale),
        "lerayNormalizedVelocityEnergy": sp.sstr(leray_energy_scale),
        "lerayNormalizedWindowDissipation": sp.sstr(
            leray_dissipation_scale
        ),
    },
    "checks": checks,
    "checkDetails": check_groups,
    "claimBoundary": {
        "proved": (
            "finite tensor and helical identities, exact angular examples, "
            "compact-core polynomial identities, one periodic NSE mode, and "
            "the critical monomial scale ledger"
        ),
        "notComputerProved": (
            "smooth cutoff support buffers, strict annular LP localization of "
            "a compact packet, the small-data theorem and continuity/sign "
            "persistence of the fixed functional J, or completeness of the "
            "literature search"
        ),
        "notClaimed": (
            "a universal equation-correlated noncancellation, a fixed-positive-"
            "terminal-time cascade, blow-up, global regularity, or a Millennium solution"
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
