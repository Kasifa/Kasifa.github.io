#!/usr/bin/env python3
"""Exact symbolic audit for the R0.70K normalized-anisotropy gate.

The producer checks finite algebra only.  Analytic positivity uses the stated
positive-semidefinite hypothesis, and the Burgers-vortex PDE boundary is kept
explicit in the JSON claim ledger.
"""

from __future__ import annotations

import json

import sympy as sp


def dev(matrix: sp.Matrix) -> sp.Matrix:
    return sp.simplify(matrix - sp.trace(matrix) * sp.eye(3) / 3)


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


# ---------------------------------------------------------------------------
# General symmetric trace-free source and trace-one covariance.
# ---------------------------------------------------------------------------
s11, s22, s12, s13, s23 = sp.symbols("s11 s22 s12 s13 s23", real=True)
source = sp.Matrix(
    [
        [s11, s12, s13],
        [s12, s22, s23],
        [s13, s23, -s11 - s22],
    ]
)

r11, r22, r12, r13, r23 = sp.symbols(
    "r11 r22 r12 r13 r23", real=True
)
shape = sp.Matrix(
    [
        [r11, r12, r13],
        [r12, r22, r23],
        [r13, r23, 1 - r11 - r22],
    ]
)
anisotropy = sp.simplify(shape - sp.eye(3) / 3)

energy, scalar_rate = sp.symbols("energy scalar_rate", nonzero=True, real=True)
raw_covariance = energy * shape

f11, f22, f33, f12, f13, f23 = sp.symbols(
    "f11 f22 f33 f12 f13 f23", real=True
)
general_flux = sp.Matrix(
    [
        [f11, f12, f13],
        [f12, f22, f23],
        [f13, f23, f33],
    ]
)

master_shape_derivative = sp.simplify(
    dev(general_flux) / energy
    - anisotropy * sp.trace(general_flux) / energy
)
amplitude_flux = scalar_rate * raw_covariance
amplitude_shape_derivative = sp.simplify(
    dev(amplitude_flux) / energy
    - anisotropy * sp.trace(amplitude_flux) / energy
)

correlation = sp.simplify(sp.trace(source * shape))
source_flux = sp.simplify(source * raw_covariance + raw_covariance * source)
source_shape_derivative_master = sp.simplify(
    dev(source_flux) / energy
    - anisotropy * sp.trace(source_flux) / energy
)
source_shape_derivative = sp.simplify(
    source * shape + shape * source - 2 * correlation * shape
)
correlation_source_derivative = sp.simplify(
    sp.trace(source * source_shape_derivative)
)
source_variance = sp.simplify(
    sp.trace(shape * source * source) - correlation**2
)
variance_square = sp.simplify(
    sp.trace(shape * (source - correlation * sp.eye(3)) ** 2)
)

normalization_checks = {
    "sourceIsSymmetric": source == source.T,
    "sourceIsTraceFree": sp.trace(source) == 0,
    "shapeIsSymmetric": shape == shape.T,
    "shapeHasUnitTrace": sp.simplify(sp.trace(shape) - 1) == 0,
    "anisotropyIsTraceFree": sp.simplify(sp.trace(anisotropy)) == 0,
    "masterDerivativeIsTraceFree": sp.simplify(
        sp.trace(master_shape_derivative)
    )
    == 0,
    "scalarAmplitudeChangeCancels": matrix_is_zero(amplitude_shape_derivative),
}

variance_checks = {
    "sourceProductionMatchesMaster": matrix_is_zero(
        source_shape_derivative_master - source_shape_derivative
    ),
    "correlationDerivativeIsTwiceVariance": sp.simplify(
        correlation_source_derivative - 2 * source_variance
    )
    == 0,
    "varianceHasCenteredSquareForm": sp.simplify(
        source_variance - variance_square
    )
    == 0,
}


# ---------------------------------------------------------------------------
# Axisymmetric frozen-source model.
# ---------------------------------------------------------------------------
p = sp.symbols("p", real=True)
axis_source = sp.diag(sp.Rational(-1, 2), sp.Rational(-1, 2), 1)
axis_shape = sp.diag((1 - p) / 2, (1 - p) / 2, p)
axis_anisotropy = sp.simplify(axis_shape - sp.eye(3) / 3)
axis_correlation = sp.simplify(sp.trace(axis_source * axis_shape))
axis_variance = sp.simplify(
    sp.trace(axis_shape * axis_source * axis_source) - axis_correlation**2
)
axis_production = sp.simplify(2 * axis_variance)
axis_anisotropy_square = sp.simplify(sp.trace(axis_anisotropy**2))

x, p0 = sp.symbols("x p0", positive=True)
p_solution = sp.simplify(p0 * x / (1 - p0 + p0 * x))
p_solution_time_derivative = sp.simplify(3 * x * sp.diff(p_solution, x))
isotropic_p = sp.simplify(p_solution.subs(p0, sp.Rational(1, 3)))
isotropic_q = sp.simplify(axis_correlation.subs(p, isotropic_p))
isotropic_q_time_derivative = sp.simplify(3 * x * sp.diff(isotropic_q, x))
isotropic_production = sp.simplify(axis_production.subs(p, isotropic_p))
isotropic_anisotropy_square = sp.simplify(
    axis_anisotropy_square.subs(p, isotropic_p)
)

axis_checks = {
    "correlationFormula": sp.simplify(axis_correlation - (3 * p - 1) / 2)
    == 0,
    "varianceFormula": sp.simplify(
        axis_variance - sp.Rational(9, 4) * p * (1 - p)
    )
    == 0,
    "productionAsCorrelationPolynomial": sp.simplify(
        axis_production - (1 + 2 * axis_correlation) * (1 - axis_correlation)
    )
    == 0,
    "probabilitySolvesReplicator": sp.simplify(
        p_solution_time_derivative - 3 * p_solution * (1 - p_solution)
    )
    == 0,
    "isotropicSolutionFormula": sp.simplify(
        isotropic_q - (x - 1) / (x + 2)
    )
    == 0,
    "isotropicCorrelationSolvesVarianceOde": sp.simplify(
        isotropic_q_time_derivative - isotropic_production
    )
    == 0,
    "axisAnisotropyNormFormula": sp.simplify(
        axis_anisotropy_square - sp.Rational(2, 3) * axis_correlation**2
    )
    == 0,
    "compressivePlaneIsStationary": sp.simplify(axis_production.subs(p, 0))
    == 0,
    "extensionalAxisIsStationary": sp.simplify(axis_production.subs(p, 1)) == 0,
}


# ---------------------------------------------------------------------------
# Realizability bounds for a positive-semidefinite, trace-one covariance.
# ---------------------------------------------------------------------------
p1, p2 = sp.symbols("p1 p2", nonnegative=True)
p3 = 1 - p1 - p2
probability_anisotropy_square = sp.simplify(
    (p1 - sp.Rational(1, 3)) ** 2
    + (p2 - sp.Rational(1, 3)) ** 2
    + (p3 - sp.Rational(1, 3)) ** 2
)
probability_square_identity = sp.simplify(
    probability_anisotropy_square - (p1**2 + p2**2 + p3**2 - sp.Rational(1, 3))
)

rank_one_shape = sp.diag(0, 0, 1)
rank_one_anisotropy = rank_one_shape - sp.eye(3) / 3
plane_shape = sp.diag(sp.Rational(1, 2), sp.Rational(1, 2), 0)
plane_anisotropy = plane_shape - sp.eye(3) / 3

realizability_checks = {
    "anisotropySquareIdentity": probability_square_identity == 0,
    "isotropicNormIsZero": probability_anisotropy_square.subs(
        {p1: sp.Rational(1, 3), p2: sp.Rational(1, 3)}
    )
    == 0,
    "rankOneSharpNorm": sp.trace(rank_one_anisotropy**2) == sp.Rational(2, 3),
    "twoComponentNorm": sp.trace(plane_anisotropy**2) == sp.Rational(1, 6),
    "rankOneSourceCorrelation": sp.trace(axis_source * rank_one_anisotropy) == 1,
    "planeSourceCorrelation": sp.trace(axis_source * plane_anisotropy)
    == sp.Rational(-1, 2),
}


# ---------------------------------------------------------------------------
# Burgers-vortex scalar balance and axial geometry.
# ---------------------------------------------------------------------------
radius, gamma, viscosity, omega_peak = sp.symbols(
    "radius gamma viscosity omega_peak", positive=True
)
gaussian = sp.exp(-gamma * radius**2 / (4 * viscosity))
burgers_omega = omega_peak * gaussian
radial_velocity = -gamma * radius / 2
radial_laplacian = sp.simplify(
    sp.diff(burgers_omega, radius, 2)
    + sp.diff(burgers_omega, radius) / radius
)
burgers_balance_residual = sp.simplify(
    radial_velocity * sp.diff(burgers_omega, radius)
    - gamma * burgers_omega
    - viscosity * radial_laplacian
)
azimuthal_velocity = sp.simplify(
    2
    * viscosity
    * omega_peak
    * (1 - gaussian)
    / (gamma * radius)
)
curl_from_swirl = sp.simplify(
    sp.diff(radius * azimuthal_velocity, radius) / radius
)

burgers_shape = rank_one_shape
burgers_anisotropy = rank_one_anisotropy
burgers_source = gamma * axis_source
burgers_correlation = sp.simplify(
    sp.trace(burgers_source * burgers_anisotropy)
)
burgers_variance = sp.simplify(
    sp.trace(burgers_shape * burgers_source**2) - burgers_correlation**2
)

burgers_checks = {
    "stationaryAxialVorticityBalance": burgers_balance_residual == 0,
    "swirlCurlRecoversGaussianVorticity": sp.simplify(
        curl_from_swirl - burgers_omega
    )
    == 0,
    "filteredAxialShapeIsRankOne": burgers_shape == sp.diag(0, 0, 1),
    "normalizedAnisotropyIsMaximal": sp.trace(burgers_anisotropy**2)
    == sp.Rational(2, 3),
    "sourceCorrelationIsPositive": burgers_correlation == gamma,
    "frozenSourceVarianceVanishesOnEigenstate": burgers_variance == 0,
}


# ---------------------------------------------------------------------------
# Exact periodic Navier--Stokes shear witness: normalized diffusion has no
# universal sign even when the nonlinear term vanishes identically.
# ---------------------------------------------------------------------------
z, time = sp.symbols("z time", real=True)
amplitude_a, amplitude_b = sp.symbols(
    "amplitude_a amplitude_b", positive=True
)
shear_velocity = sp.Matrix(
    [
        amplitude_b
        * sp.exp(-4 * viscosity * time)
        * sp.sin(2 * z)
        / 2,
        -amplitude_a * sp.exp(-viscosity * time) * sp.sin(z),
        0,
    ]
)
shear_vorticity = sp.Matrix(
    [
        -sp.diff(shear_velocity[1], z),
        sp.diff(shear_velocity[0], z),
        0,
    ]
)
shear_heat_residual = sp.simplify(
    sp.diff(shear_velocity, time)
    - viscosity * shear_velocity.diff(z, 2)
)

mode_one_weight = amplitude_a**2 * sp.exp(-2 * viscosity * time)
mode_two_weight = amplitude_b**2 * sp.exp(-8 * viscosity * time)
shear_probability = sp.simplify(
    mode_one_weight / (mode_one_weight + mode_two_weight)
)
shear_shape = sp.diag(shear_probability, 1 - shear_probability, 0)
shear_anisotropy = sp.simplify(shear_shape - sp.eye(3) / 3)
shear_anisotropy_square = sp.simplify(sp.trace(shear_anisotropy**2))
shear_probability_derivative = sp.simplify(sp.diff(shear_probability, time))
shear_anisotropy_square_derivative = sp.simplify(
    sp.diff(shear_anisotropy_square, time)
)
shear_expected_derivative = sp.simplify(
    12
    * viscosity
    * shear_probability
    * (1 - shear_probability)
    * (2 * shear_probability - 1)
)
shear_derivative_at_zero = sp.simplify(
    shear_anisotropy_square_derivative.subs(time, 0)
)

shear_checks = {
    "velocitySolvesHeatEquation": matrix_is_zero(shear_heat_residual),
    "nonlinearityVanishesBecauseOnlyZDependenceAndZeroVerticalVelocity": shear_velocity[2]
    == 0,
    "vorticityFormula": matrix_is_zero(
        shear_vorticity
        - sp.Matrix(
            [
                amplitude_a * sp.exp(-viscosity * time) * sp.cos(z),
                amplitude_b * sp.exp(-4 * viscosity * time) * sp.cos(2 * z),
                0,
            ]
        )
    ),
    "probabilityReplicator": sp.simplify(
        shear_probability_derivative
        - 6 * viscosity * shear_probability * (1 - shear_probability)
    )
    == 0,
    "anisotropyNormFormula": sp.simplify(
        shear_anisotropy_square
        - (
            2 * shear_probability**2
            - 2 * shear_probability
            + sp.Rational(2, 3)
        )
    )
    == 0,
    "anisotropyDerivativeFormula": sp.simplify(
        shear_anisotropy_square_derivative - shear_expected_derivative
    )
    == 0,
    "positiveWitnessAtPFourFifths": sp.simplify(
        shear_derivative_at_zero.subs(
            amplitude_a**2, 4 * amplitude_b**2
        )
        - sp.Rational(144, 125) * viscosity
    )
    == 0,
    "negativeWitnessAtPOneFifth": sp.simplify(
        shear_derivative_at_zero.subs(
            amplitude_b**2, 4 * amplitude_a**2
        )
        + sp.Rational(144, 125) * viscosity
    )
    == 0,
}


# ---------------------------------------------------------------------------
# Navier--Stokes scaling and amplitude homogeneity ledgers.
# ---------------------------------------------------------------------------
scaling_ledger = {
    "velocity": "r**(-1)",
    "vorticity": "r**(-2)",
    "localizedRawCovarianceQ": "r**(-1)",
    "localizedEnstrophyTraceE": "r**(-1)",
    "rawDeviatoricMomentA": "r**(-1)",
    "normalizedShapeR": "1",
    "normalizedAnisotropyB": "1",
    "sourceStrainSigma": "r**(-2)",
    "sourceCorrelationSigmaColonB": "r**(-2)",
    "dimensionlessCorrelationR2SigmaColonB": "1",
    "criticalMoment_rQ": "1",
    "instantaneousRawPairingSigmaColonA": "r**(-3)",
    "parabolicWindowRawPairing": "r**(-1)",
}

homogeneity_ledger = {
    "sourceFunctionalSigma[epsilon*u]": "epsilon*Sigma[u]",
    "rawCovarianceQ[epsilon*u]": "epsilon**2*Q[u]",
    "normalizedAnisotropyB[epsilon*u]": "B[u]",
    "normalizedCorrelationK[epsilon*u]": "epsilon*K[u]",
    "rawCubicWorkJ[epsilon*u]": "epsilon**3*J[u]",
}


all_groups = {
    "normalization": normalization_checks,
    "sourceVariance": variance_checks,
    "axisymmetricModel": axis_checks,
    "realizability": realizability_checks,
    "burgersVortex": burgers_checks,
    "periodicShear": shear_checks,
}
for group_name, group in all_groups.items():
    for check_name, value in group.items():
        require(bool(value), f"{group_name}.{check_name}")


payload = {
    "release": "R0.70K",
    "status": "exact-normalized-anisotropy-evolution-audit",
    "arithmetic": "exact SymPy polynomial, rational, matrix, and exponential differentiation",
    "checks": {name: all(values.values()) for name, values in all_groups.items()},
    "checkDetails": all_groups,
    "masterIdentity": {
        "rawCovariance": "Q=int chi Omega tensor Omega",
        "enstrophyTrace": "E=tr(Q)>0",
        "rawDeviatoricMoment": "A=dev(Q)",
        "normalizedShape": "R=Q/E",
        "normalizedAnisotropy": "B=Q/E-I/3=A/E",
        "evolution": "dB/dt=(dev(F)-B*tr(F))/E where F=dQ/dt",
        "amplitudeCancellation": "F=lambda*Q implies dB/dt=0",
    },
    "frozenSourceVarianceLaw": {
        "sourceFlux": "F_S=Sigma*Q+Q*Sigma",
        "shapeEquation": "dR/dt=Sigma*R+R*Sigma-2*(Sigma:R)*R",
        "correlation": "q=Sigma:B=Sigma:R",
        "correlationDerivative": "dq/dt=2*(tr(R*Sigma**2)-q**2)",
        "centeredSquare": "tr(R*(Sigma-q*I)**2)",
        "sign": "nonnegative for R positive semidefinite with trace one",
        "equality": "the support of R lies in one eigenspace of Sigma",
    },
    "axisymmetricModel": {
        "source": "diag(-1/2,-1/2,1)",
        "shape": "diag((1-p)/2,(1-p)/2,p)",
        "correlation": "(3*p-1)/2",
        "variance": "9*p*(1-p)/4",
        "production": "9*p*(1-p)/2=(1+2*q)*(1-q)",
        "replicatorEquation": "dp/dt=3*p*(1-p)",
        "isotropicInitialCorrelation": "q(t)=(exp(3*t)-1)/(exp(3*t)+2)",
        "isotropicInitialAnisotropyNormSquare": "2*q(t)**2/3",
        "limit": "q(t) increases from 0 to 1 and B approaches the rank-one vertex",
    },
    "realizability": {
        "eigenvalueBounds": "-1/3 <= eigenvalue(B) <= 2/3",
        "normBound": "0 <= tr(B**2) <= 2/3",
        "sharpState": "R=e3 tensor e3",
        "sourceCorrelationBounds": "lambda_min(Sigma) <= Sigma:B <= lambda_max(Sigma)",
        "frobeniusBound": "abs(Sigma:B) <= sqrt(2/3)*abs(Sigma)_F",
        "interpretation": "energy gives bounded shape but no small anisotropy defect",
    },
    "burgersVortex": {
        "backgroundStrain": "gamma*diag(-1/2,-1/2,1)",
        "vorticity": "omega_peak*exp(-gamma*rho**2/(4*nu))*e3",
        "swirl": "2*nu*omega_peak*(1-exp(-gamma*rho**2/(4*nu)))/(gamma*rho)",
        "normalizedShape": "e3 tensor e3",
        "normalizedAnisotropy": "diag(-1/3,-1/3,2/3)",
        "anisotropyNormSquare": "2/3",
        "sourceCorrelation": "gamma>0",
        "rawResolvedStretchingTrace": "2*gamma*E>0",
        "balance": "stationarity forces transport, viscosity, and subfilter/cutoff terms to balance the positive raw stretching in the complete filtered identity",
        "boundary": "exact self-consistent stationary NSE solution but not a Leray finite-energy field because the background strain grows linearly and the tube is axial",
    },
    "periodicShear": {
        "velocity": "(B*exp(-4*nu*t)*sin(2*z)/2,-A*exp(-nu*t)*sin(z),0)",
        "vorticity": "(A*exp(-nu*t)*cos(z),B*exp(-4*nu*t)*cos(2*z),0)",
        "nonlinearity": "zero identically, so this is an exact periodic Navier-Stokes heat solution",
        "shape": "diag(p,1-p,0)",
        "probability": "p=A**2*exp(-2*nu*t)/(A**2*exp(-2*nu*t)+B**2*exp(-8*nu*t))",
        "anisotropyNormSquare": "2*p**2-2*p+2/3",
        "anisotropyNormDerivative": "12*nu*p*(1-p)*(2*p-1)",
        "oppositeSigns": "+144*nu/125 at p=4/5 and -144*nu/125 at p=1/5",
        "conclusion": "after trace normalization, viscous evolution alone has no universal sign for anisotropy magnitude",
    },
    "scalingLedger": scaling_ledger,
    "homogeneityLedger": homogeneity_ledger,
    "claimBoundary": {
        "proved": "the normalized covariance identity, the frozen-source variance law, the exact axisymmetric replicator solution, sharp realizability examples, the Burgers scalar vorticity balance, the exact periodic two-mode shear sign pair, and scaling/homogeneity ledgers",
        "analyticNotComputerProved": "positive-semidefinite covariance positivity, the full filtered tensor identity from integration by parts, the complete three-dimensional Burgers velocity-pressure verification, small-data NSE continuity, and completeness of the literature search",
        "notClaimed": "an energy-only bound for the raw core magnitude, a favorable sign for source evolution or pressure, a fixed-positive-terminal-time finite-energy cascade, blow-up, global regularity, or a Millennium solution",
    },
}

print(json.dumps(payload, indent=2, sort_keys=True))
