#!/usr/bin/env python3
"""Exact algebra audit for the R0.70H core-moment variation gate.

The script checks the critical normalization of the zeroth and first core
moments, the covariant summation-by-parts identity, the exact scale and nested
time-window ledgers, the filtered local-enstrophy identity, and the finite-N
constant-core pressure test inherited from R0.70F.

It does not prove a parabolic Carleson estimate for Leray solutions, extend an
initial-face family to one common positive terminal time, or establish a
Navier--Stokes regularity theorem.
"""

from __future__ import annotations

import json

import sympy as sp


def geometric_sum(ratio: sp.Expr, count: int) -> sp.Expr:
    return sp.simplify(sum(ratio**index for index in range(count)))


def squared_norm(vector: sp.Matrix) -> sp.Expr:
    return sp.simplify(sum(entry**2 for entry in vector))


# ---------------------------------------------------------------------------
# Critical normalization and covariant Abel identity
# ---------------------------------------------------------------------------

r, coefficient, time_moment = sp.symbols(
    "r coefficient time_moment", positive=True
)
degree = sp.symbols("degree", integer=True, nonnegative=True)

# A degree-n jet has size r^(-n-2).  The instantaneous critical moment has
# size r^(n-1), while its time integral has size r^(n+1).
instantaneous_normalized_work = sp.simplify(
    r**3
    * (r ** (-(degree + 2)) * coefficient)
    * (r ** (degree - 1) * time_moment)
)
spacetime_normalized_work = sp.simplify(
    r * (r ** (-(degree + 2)) * coefficient) * (r ** (degree + 1) * time_moment)
)

covariant_abel_checks: dict[str, bool] = {}
for power in (2, 3):
    for length in range(1, 10):
        rho_value = sp.Rational(2, 7)
        lam_value = rho_value**power
        cumulative = [
            sp.Rational((index + 1) * (index + 4), index + 3)
            for index in range(length + 1)
        ]
        moments = [
            sp.Rational((index + 2) * (3 * index + 5), index + 5)
            for index in range(length)
        ]
        direct = sum(
            (cumulative[index + 1] - lam_value * cumulative[index])
            * moments[index]
            for index in range(length)
        )
        transformed = (
            cumulative[-1] * moments[-1]
            - lam_value * cumulative[0] * moments[0]
            + sum(
                cumulative[index + 1]
                * (moments[index] - lam_value * moments[index + 1])
                for index in range(length - 1)
            )
        )
        covariant_abel_checks[f"degree{power - 2}Length{length}"] = (
            sp.simplify(direct - transformed) == 0
        )

# Generic finite-chain regressions with nonconstant lambda values catch the
# rho-index shift that a constant-ratio test cannot see.
variable_abel_checks: dict[str, bool] = {}
for length in range(1, 7):
    c_values = sp.symbols(f"c0:{length + 1}")
    m_values = sp.symbols(f"m0:{length}")
    lambda_values = sp.symbols(f"lambda1:{length + 1}")
    direct = sum(
        (c_values[index + 1] - lambda_values[index] * c_values[index])
        * m_values[index]
        for index in range(length)
    )
    transformed = (
        c_values[-1] * m_values[-1]
        - lambda_values[0] * c_values[0] * m_values[0]
        + sum(
            c_values[index + 1]
            * (m_values[index] - lambda_values[index + 1] * m_values[index + 1])
            for index in range(length - 1)
        )
    )
    variable_abel_checks[f"length{length}"] = sp.expand(direct - transformed) == 0

weighted_shift_records: dict[str, str] = {}
weighted_shift_checks: dict[str, bool] = {}
for rho_value in (sp.Rational(1, 2), sp.Rational(1, 4), sp.Rational(2, 5)):
    for n_value in (0, 1):
        shift_norm = sp.sqrt(1 / rho_value)
        transport = rho_value ** (n_value + 2)
        neumann_ratio = sp.simplify(transport * shift_norm)
        key = f"rho{sp.sstr(rho_value)}Degree{n_value}"
        weighted_shift_records[key] = sp.sstr(neumann_ratio)
        weighted_shift_checks[key] = bool(neumann_ratio < 1)


# ---------------------------------------------------------------------------
# Exact adjacent-scale ledger
# ---------------------------------------------------------------------------

rho, base_moment = sp.symbols("rho base_moment", positive=True)
cutoff_change = sp.symbols("cutoff_change", real=True)
field, field_change = sp.symbols("field field_change", real=True)

scale_ledgers: dict[str, bool] = {}
for n_value in (0, 1):
    normalization = rho ** (1 - n_value)
    old_moment = base_moment
    field_quadratic_change = sp.expand(
        (field + field_change) ** 2 - field**2
    )
    direct = sp.expand(
        normalization
        * (base_moment + cutoff_change + field_quadratic_change)
        - old_moment
    )
    ledger = sp.expand(
        (normalization - 1) * old_moment
        + normalization * cutoff_change
        + normalization * (2 * field * field_change + field_change**2)
    )
    scale_ledgers[f"degree{n_value}"] = sp.simplify(direct - ledger) == 0


# ---------------------------------------------------------------------------
# Exact nested time-window ledger
# ---------------------------------------------------------------------------

fine_inverse_time, coarse_inverse_time = sp.symbols(
    "fine_inverse_time coarse_inverse_time", positive=True
)
fine_old, fine_change, discarded_old = sp.symbols(
    "fine_old fine_change discarded_old", real=True
)

window_direct = sp.expand(
    fine_inverse_time * (fine_old + fine_change)
    - coarse_inverse_time * (fine_old + discarded_old)
)
window_ledger = sp.expand(
    fine_inverse_time * fine_change
    + (fine_inverse_time - coarse_inverse_time) * fine_old
    - coarse_inverse_time * discarded_old
)

# The actual spacetime work uses N_k=r_k^(-2) 1_(I_k) m_k.  On the fine
# overlap, lambda_(k+1) N_(k+1) therefore carries rho^n, not rho^(n+2).
spacetime_overlap_checks = {
    f"degree{n_value}": sp.simplify(
        rho ** (n_value + 2) * (rho * r) ** -2
        - rho**n_value * r**-2
    )
    == 0
    for n_value in (0, 1)
}
dual_weight_check = sp.simplify(r * (r**-2) ** 2 - r**-3) == 0

radius_ratios = [sp.Rational(1, 2), sp.Rational(2, 5), sp.Rational(1, 3)]
radius_values = [sp.Integer(1)]
for ratio_value in radius_ratios:
    radius_values.append(sp.simplify(radius_values[-1] * ratio_value))
radius_index_checks: dict[str, bool] = {}
for n_value in (0, 1):
    for k_value in range(1, len(radius_values)):
        lam_from_radii = sp.simplify(
            (radius_values[k_value] / radius_values[k_value - 1])
            ** (n_value + 2)
        )
        radius_index_checks[f"degree{n_value}Lambda{k_value}"] = (
            lam_from_radii == radius_ratios[k_value - 1] ** (n_value + 2)
        )
    for k_value in range(len(radius_ratios) - 1):
        lambda_next = radius_ratios[k_value] ** (n_value + 2)
        overlap_factor = sp.simplify(
            lambda_next
            * radius_values[k_value + 1] ** -2
            / radius_values[k_value] ** -2
        )
        radius_index_checks[f"degree{n_value}Overlap{k_value}"] = (
            overlap_factor == radius_ratios[k_value] ** n_value
        )


# ---------------------------------------------------------------------------
# Filtered local-enstrophy identity, checked as a pointwise divergence law
# ---------------------------------------------------------------------------

x1, x2, x3 = sp.symbols("x1 x2 x3", real=True)
coordinates = (x1, x2, x3)
nu = sp.symbols("nu", positive=True)

U = sp.Matrix([-x2 * x3, x1 * x3, 0])
Omega = sp.Matrix([-x1, -x2, 2 * x3])
C = sp.Matrix(
    [
        [x1 * x2, x2 * x3, x3 * x1],
        [x1**2, x2**2, x3**2],
        [x2 + x3, x3 + x1, x1 + x2],
    ]
)

divergence_u = sp.simplify(
    sum(sp.diff(U[index], coordinates[index]) for index in range(3))
)
divergence_omega = sp.simplify(
    sum(sp.diff(Omega[index], coordinates[index]) for index in range(3))
)
curl_u = sp.Matrix(
    [
        sp.diff(U[2], x2) - sp.diff(U[1], x3),
        sp.diff(U[0], x3) - sp.diff(U[2], x1),
        sp.diff(U[1], x1) - sp.diff(U[0], x2),
    ]
).applyfunc(sp.simplify)


def gradient(expression: sp.Expr) -> sp.Matrix:
    return sp.Matrix([sp.diff(expression, variable) for variable in coordinates])


def laplacian(expression: sp.Expr) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(expression, variable, 2) for variable in coordinates)
    )


def divergence(vector: sp.Matrix) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(vector[index], coordinates[index]) for index in range(3))
    )


dt_omega = sp.Matrix(
    [
        -sum(U[a] * sp.diff(Omega[i], coordinates[a]) for a in range(3))
        + sum(Omega[a] * sp.diff(U[i], coordinates[a]) for a in range(3))
        + nu * laplacian(Omega[i])
        + sum(sp.diff(C[a, i], coordinates[a]) for a in range(3))
        for i in range(3)
    ]
)

omega_squared = squared_norm(Omega)
gradient_omega_squared = sp.simplify(
    sum(
        sp.diff(Omega[i], coordinates[a]) ** 2
        for i in range(3)
        for a in range(3)
    )
)
stretching = sp.simplify(
    sum(
        Omega[i] * Omega[a] * sp.diff(U[i], coordinates[a])
        for i in range(3)
        for a in range(3)
    )
)
commutator_contraction = sp.simplify(
    sum(C[a, i] * sp.diff(Omega[i], coordinates[a]) for a in range(3) for i in range(3))
)
commutator_flux = sp.Matrix(
    [2 * sum(Omega[i] * C[a, i] for i in range(3)) for a in range(3)]
)

local_enstrophy_direct = sp.simplify(2 * Omega.dot(dt_omega))
local_enstrophy_ledger = sp.simplify(
    -divergence(U * omega_squared)
    + 2 * stretching
    + nu * laplacian(omega_squared)
    - 2 * nu * gradient_omega_squared
    + divergence(commutator_flux)
    - 2 * commutator_contraction
)

phi0 = 1 + x1**2 + 2 * x2**2 + 3 * x3**2
phi1 = x1 * phi0


def integrated_weight_ledger_residual(phi: sp.Expr) -> sp.Expr:
    """Residual after integration by parts, represented modulo divergence."""

    direct_density = sp.expand(phi * local_enstrophy_direct)
    ledger_density = sp.expand(
        U.dot(gradient(phi)) * omega_squared
        + 2 * phi * stretching
        + nu * laplacian(phi) * omega_squared
        - 2 * nu * phi * gradient_omega_squared
        - 2
        * sum(
            C[a, i] * sp.diff(phi * Omega[i], coordinates[a])
            for a in range(3)
            for i in range(3)
        )
    )
    boundary_flux = sp.Matrix(
        [
            -phi * U[a] * omega_squared
            + nu * (phi * sp.diff(omega_squared, coordinates[a]) - sp.diff(phi, coordinates[a]) * omega_squared)
            + phi * commutator_flux[a]
            for a in range(3)
        ]
    )
    return sp.simplify(direct_density - ledger_density - divergence(boundary_flux))


# ---------------------------------------------------------------------------
# Exact finite-N constant-core pressure test
# ---------------------------------------------------------------------------

pressure_checks: dict[str, bool] = {}
pressure_records: dict[str, dict[str, str]] = {}

for lambda_base in (2, 4, 8):
    Lambda = sp.Integer(lambda_base)
    rho_active = Lambda ** -2
    q = sp.simplify(rho_active**2)
    for jet_degree in (0, 1):
        transport = sp.simplify(rho_active ** (jet_degree + 2))
        lower_bound = sp.simplify(1 - transport / (1 - q) ** 2)
        for count in range(2, 13):
            b_values = [
                sp.simplify((1 - q**index) / (1 - q))
                for index in range(1, count + 1)
            ]
            ordinary = [
                sp.simplify(b_values[index + 1] ** 2 - b_values[index] ** 2)
                for index in range(count - 1)
            ]
            covariant = [
                sp.simplify(b_values[index] ** 2 - transport * b_values[index + 1] ** 2)
                for index in range(count - 1)
            ]
            source_cumulative = [
                sp.Integer(0),
                *[
                    sp.simplify((1 - transport**index) / (1 - transport))
                    for index in range(1, count + 1)
                ],
            ]
            direct_work = sp.simplify(sum(value**2 for value in b_values))
            abel_work = sp.simplify(
                source_cumulative[count] * b_values[-1] ** 2
                + sum(
                    source_cumulative[index + 1] * covariant[index]
                    for index in range(count - 1)
                )
            )
            key = f"Lambda{lambda_base}Degree{jet_degree}Count{count}"
            pressure_checks[key] = (
                sp.simplify(sum(ordinary) - (b_values[-1] ** 2 - 1)) == 0
                and all(value > 0 for value in covariant)
                and all(sp.simplify(value - lower_bound) >= 0 for value in covariant)
                and sp.simplify(direct_work - abel_work) == 0
            )

        infinite_ordinary_variation = sp.simplify((1 - q) ** -2 - 1)
        asymptotic_covariant = sp.simplify((1 - transport) / (1 - q) ** 2)
        pressure_records[f"Lambda{lambda_base}Degree{jet_degree}"] = {
            "activeRatio": sp.sstr(rho_active),
            "coreRecurrenceRatio": sp.sstr(q),
            "sourceTransportFactor": sp.sstr(transport),
            "ordinaryVariationLimit": sp.sstr(infinite_ordinary_variation),
            "covariantIncrementLowerBound": sp.sstr(lower_bound),
            "covariantIncrementLimit": sp.sstr(asymptotic_covariant),
        }


# Component scale-weight geometric series, with profile norms and cross terms
# deliberately suppressed.  These are not full-field energy computations.
component_scale_records: dict[str, str] = {}
for lambda_base in (2, 4, 8):
    Lambda = sp.Integer(lambda_base)
    ratio = Lambda ** -2
    finite_count = 12
    finite_energy_weight = sp.simplify(
        sum((1 + Lambda**-1) * ratio**index for index in range(1, finite_count + 1))
    )
    infinite_energy_weight = sp.simplify(
        (1 + Lambda**-1) * ratio / (1 - ratio)
    )
    component_scale_records[f"Lambda{lambda_base}"] = (
        f"finite={sp.sstr(finite_energy_weight)}; "
        f"uniformUpper={sp.sstr(infinite_energy_weight)}"
    )


checks = {
    "instantaneousCriticalWorkNormalization": (
        instantaneous_normalized_work == coefficient * time_moment
    ),
    "spacetimeDimensionalNormalization": (
        spacetime_normalized_work == coefficient * time_moment
    ),
    "covariantAbelFiniteChains": all(covariant_abel_checks.values()),
    "variableCoefficientAbelRegressions": all(variable_abel_checks.values()),
    "weightedSourceShiftInvertible": all(weighted_shift_checks.values()),
    "zerothScaleLedger": scale_ledgers["degree0"],
    "firstScaleLedger": scale_ledgers["degree1"],
    "nestedWindowLedger": sp.simplify(window_direct - window_ledger) == 0,
    "spacetimeOverlapFactors": all(spacetime_overlap_checks.values()),
    "spacetimeDualWeightIsRMinus3": dual_weight_check,
    "nonconstantRadiusIndexMap": all(radius_index_checks.values()),
    "testVelocityDivergenceFree": divergence_u == 0,
    "testVorticityDivergenceFree": divergence_omega == 0,
    "testVorticityEqualsCurlVelocity": curl_u == Omega,
    "filteredLocalEnstrophyPointwise": sp.simplify(
        local_enstrophy_direct - local_enstrophy_ledger
    )
    == 0,
    "zerothWeightedMomentEvolution": integrated_weight_ledger_residual(phi0) == 0,
    "firstWeightedMomentEvolution": integrated_weight_ledger_residual(phi1) == 0,
    "constantCoreFiniteChains": all(pressure_checks.values()),
}

if not all(checks.values()):
    raise AssertionError({key: value for key, value in checks.items() if not value})


result = {
    "release": "R0.70H",
    "status": "exact-symbolic-regression-audit",
    "criticalMoments": {
        "instantaneousDegreeN": "m_k^(n)=r_k^(1-n)*M_k^(n)",
        "parabolicDegreeN": "mbar_k^(n)=r_k^(-2)*integral_(I_k) m_k^(n)(t) dt",
        "instantaneousWork": "r_k^3*P_k^(n):M_k^(n)=c_k^(n):m_k^(n)",
        "spacetimeWork": (
            "r_k*integral P_k^(n)(t):M_k^(n)(t) dt "
            "=r_k^(-2)*integral c_k^(n)(t):m_k^(n)(t) dt"
        ),
        "timeCoefficientBoundary": (
            "c_k(t) cannot be factored from the time integral without time constancy"
        ),
        "sourceTransport": "h_k^(n)=c_k^(n)-rho_(k-1)^(n+2)*c_(k-1)^(n)",
        "instantaneousPairingIncrement": "m_k^(n)-rho_k^(n+2)*m_(k+1)^(n)",
        "spacetimeCoordinate": "N_k^(n)=r_k^(-2)*1_(I_k)*m_k^(n)",
        "spacetimeOverlapIncrement": "r_k^(-2)*(m_k^(n)-rho_k^n*m_(k+1)^(n))",
    },
    "exactLedgers": {
        "scale": (
            "scalar-contraction regression for normalization dilation + signed "
            "cutoff-shell change + two bilinear filter-change terms + quadratic term"
        ),
        "timeWindow": (
            "conditional scalar ledger: fine-window field change + averaging-factor "
            "dilation - discarded coarse slab"
        ),
        "finiteCovariantAbelCases": len(covariant_abel_checks),
        "genericVariableCoefficientAbelCases": len(variable_abel_checks),
        "spacetimeOverlapFactors": {"degree0": "1", "degree1": "rho_k"},
        "spacetimeDualWeight": "r_k*(r_k^(-2))^2=r_k^(-3)",
        "nonconstantRadiusIndexCases": len(radius_index_checks),
        "weightedShiftNeumannRatios": weighted_shift_records,
    },
    "momentEvolution": {
        "regressionScope": (
            "pointwise divergence identity for one polynomial divergence-free "
            "velocity/vorticity pair with Omega=curl(U); weights are noncompact "
            "polynomials and no boundary integral is asserted"
        ),
        "traceStretchingTerm": "2*integral phi*S(U):Omega tensor Omega",
        "transportBoundary": "integral (U dot grad phi)*|Omega|^2",
        "viscousTerms": (
            "nu*integral Delta(phi)*|Omega|^2 "
            "- 2*nu*integral phi*|grad Omega|^2"
        ),
        "commutatorTerm": "-2*integral C_ai*partial_a(phi*Omega_i)",
    },
    "constantCorePressureTest": {
        "sampleScope": "Lambda in {2,4,8}; N in {2,...,12}; algebra only",
        "geometryChecked": False,
        "profile": "b_n=(1-q^n)/(1-q), q=Lambda^(-4)",
        "zerothCriticalMoment": "C_0*b_n^2*(e1 tensor e1)",
        "firstCriticalMoment": "C_1*b_n^2*(e1 tensor e1 tensor e1)",
        "ordinaryVariation": (
            "the report proves from the closed formula C_s*(b_N^2-1) that it is bounded; "
            "the producer performs finite regressions"
        ),
        "covariantL1AndSquareMass": (
            "the report derives linear growth from a positive analytic lower bound; "
            "the producer performs finite regressions"
        ),
        "records": pressure_records,
        "finiteCasesChecked": len(pressure_checks),
    },
    "sampledComponentScaleWeights": component_scale_records,
    "checks": checks,
    "claimBoundary": {
        "proved": (
            "exact finite symbolic regressions for critical normalization, covariant "
            "summation by parts, scale/window ledgers, one pointwise polynomial local-"
            "enstrophy divergence identity, and finite initial-face recurrence algebra"
        ),
        "notComputerProved": (
            "the general-index proofs written in the report, the filter multiplier "
            "hypothesis, compact support geometry inherited from R0.70F, a Leray-class "
            "local enstrophy Carleson bound, or nonlinear time persistence"
        ),
        "notClaimed": (
            "a common-positive-terminal-time counterexample, a singular solution, "
            "large-data regularity, or a Millennium solution"
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
