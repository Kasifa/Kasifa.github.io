#!/usr/bin/env python3
"""Exact finite audit for the R0.70I temporal-Hardy obstruction.

The producer checks finite rational instances of the geometric time kernel,
the alpha=1/4 weighted-L2 threshold, heat and Navier--Stokes scaling ledgers,
the forced outer-scale exponent, fixed-low mixed-scale exponents, and the
isotropic/trace-free contraction.  It is an algebraic regression producer.

It does not turn the finite kernel samples into a proof for arbitrary chain
length, realize an arbitrary scalar enstrophy profile as a Navier--Stokes
trajectory, or construct a common-positive-top Navier--Stokes obstruction.
"""

from __future__ import annotations

import json

import sympy as sp


def exact_le(left: sp.Expr, right: sp.Expr) -> bool:
    """Return an exact comparison for the rational/algebraic cases below."""

    return bool(sp.simplify(left - right) <= 0)


# ---------------------------------------------------------------------------
# Finite temporal-Hardy kernel
# ---------------------------------------------------------------------------

rho_values = (sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(2, 5))
kernel_checks: dict[str, bool] = {}
kernel_records: dict[str, dict[str, object]] = {}
kernel_case_count = 0

for rho in rho_values:
    rho_key = f"rho{rho.p}_{rho.q}"
    geometric_constant = sp.simplify(1 / (1 - rho))
    representative: dict[str, object] = {}

    for final_index in range(0, 9):
        # A finite chain has moments k=0,...,K, interior increments
        # k=0,...,K-1, and the separate fine Abel endpoint at k=K.
        radii = [sp.simplify(rho**index) for index in range(final_index + 1)]
        inverse_radii = [sp.simplify(1 / value) for value in radii]

        # On r_(j+1)^2 <= s < r_j^2, overlap indices are 0,...,j-1
        # and the unique slab index is j.  The rational sample
        # s=r_j*r_(j+1) lies strictly inside this interval.
        for shell_index in range(final_index):
            sample_s = sp.simplify(
                radii[shell_index] * radii[shell_index + 1]
            )
            overlap_indices = [
                index
                for index in range(final_index)
                if sample_s < radii[index + 1] ** 2
            ]
            slab_indices = [
                index
                for index in range(final_index)
                if radii[index + 1] ** 2
                <= sample_s
                < radii[index] ** 2
            ]
            fine_endpoint_active = sample_s < radii[final_index] ** 2
            kernel_value = sp.simplify(
                sum(inverse_radii[index] for index in overlap_indices)
                + sum(inverse_radii[index] for index in slab_indices)
                + (
                    inverse_radii[final_index]
                    if fine_endpoint_active
                    else sp.Integer(0)
                )
            )
            expected_value = sp.simplify(
                sum(inverse_radii[index] for index in range(shell_index + 1))
            )
            key = (
                f"{rho_key}K{final_index}Shell{shell_index}"
            )
            kernel_checks[f"{key}OverlapSet"] = overlap_indices == list(
                range(shell_index)
            )
            kernel_checks[f"{key}SlabSet"] = slab_indices == [shell_index]
            kernel_checks[f"{key}FineEndpointInactive"] = not fine_endpoint_active
            kernel_checks[f"{key}Value"] = kernel_value == expected_value
            # These two rational inequalities are equivalent to
            # G_K(s) <= C_rho*min(r_K^(-1),s^(-1/2)).
            kernel_checks[f"{key}FiniteCap"] = exact_le(
                kernel_value,
                geometric_constant * inverse_radii[final_index],
            )
            kernel_checks[f"{key}HardyCap"] = exact_le(
                kernel_value**2 * sample_s,
                geometric_constant**2,
            )
            kernel_case_count += 1

        # Fine tail: all overlap terms survive, no slab is present, and the
        # finite cap r_K^(-1) replaces the divergent s^(-1/2) endpoint.
        fine_s = sp.simplify(radii[final_index] ** 2 / 2)
        fine_overlap = [
            index
            for index in range(final_index)
            if fine_s < radii[index + 1] ** 2
        ]
        fine_slabs = [
            index
            for index in range(final_index)
            if radii[index + 1] ** 2 <= fine_s < radii[index] ** 2
        ]
        fine_endpoint_active = fine_s < radii[final_index] ** 2
        fine_kernel = sp.simplify(
            sum(inverse_radii[index] for index in fine_overlap)
            + sum(inverse_radii[index] for index in fine_slabs)
            + (
                inverse_radii[final_index]
                if fine_endpoint_active
                else sp.Integer(0)
            )
        )
        fine_expected = sp.simplify(
            sum(inverse_radii[index] for index in range(final_index + 1))
        )
        fine_key = f"{rho_key}K{final_index}FineTail"
        kernel_checks[f"{fine_key}OverlapSet"] = fine_overlap == list(
            range(final_index)
        )
        kernel_checks[f"{fine_key}NoSlab"] = fine_slabs == []
        kernel_checks[f"{fine_key}EndpointActive"] = fine_endpoint_active
        kernel_checks[f"{fine_key}Value"] = fine_kernel == fine_expected
        kernel_checks[f"{fine_key}FiniteCap"] = exact_le(
            fine_kernel,
            geometric_constant * inverse_radii[final_index],
        )
        kernel_checks[f"{fine_key}HardyCap"] = exact_le(
            fine_kernel**2 * fine_s,
            geometric_constant**2,
        )
        kernel_case_count += 1

        # At the measure-zero boundary s=r_K^2, the fine endpoint turns off.
        # For K>=1 the last interior overlap is replaced by its slab term.
        endpoint_s = radii[final_index] ** 2
        endpoint_overlap = [
            index
            for index in range(final_index)
            if endpoint_s < radii[index + 1] ** 2
        ]
        endpoint_slabs = [
            index
            for index in range(final_index)
            if radii[index + 1] ** 2
            <= endpoint_s
            < radii[index] ** 2
        ]
        endpoint_active = endpoint_s < radii[final_index] ** 2
        endpoint_kernel = sp.simplify(
            sum(inverse_radii[index] for index in endpoint_overlap)
            + sum(inverse_radii[index] for index in endpoint_slabs)
            + (
                inverse_radii[final_index]
                if endpoint_active
                else sp.Integer(0)
            )
        )
        endpoint_expected = sp.simplify(
            sum(inverse_radii[index] for index in range(final_index))
        )
        endpoint_key = f"{rho_key}K{final_index}FineEndpoint"
        kernel_checks[f"{endpoint_key}OverlapSet"] = endpoint_overlap == list(
            range(max(final_index - 1, 0))
        )
        expected_endpoint_slabs = (
            [final_index - 1] if final_index >= 1 else []
        )
        kernel_checks[f"{endpoint_key}TerminalSlab"] = (
            endpoint_slabs == expected_endpoint_slabs
        )
        kernel_checks[f"{endpoint_key}EndpointInactive"] = not endpoint_active
        kernel_checks[f"{endpoint_key}Value"] = (
            endpoint_kernel == endpoint_expected
        )
        kernel_checks[f"{endpoint_key}FiniteCap"] = exact_le(
            endpoint_kernel,
            geometric_constant * inverse_radii[final_index],
        )
        kernel_checks[f"{endpoint_key}HardyCap"] = exact_le(
            endpoint_kernel**2 * endpoint_s,
            geometric_constant**2,
        )
        kernel_case_count += 1

        if final_index == 8:
            representative = {
                "K": final_index,
                "rKInverse": sp.sstr(inverse_radii[final_index]),
                "rKSquared": sp.sstr(radii[final_index] ** 2),
                "fineTailSample": sp.sstr(fine_s),
                "fineTailKernel": sp.sstr(fine_kernel),
                "fineEndpointContribution": sp.sstr(
                    inverse_radii[final_index]
                ),
                "kernelAtMeasureZeroBoundary": sp.sstr(endpoint_kernel),
            }

    kernel_records[rho_key] = {
        "rho": sp.sstr(rho),
        "uniformGeometricConstant": sp.sstr(geometric_constant),
        "representativeK8": representative,
    }


# The overlap difference contains m_k and rho^n*m_(k+1).  If
# |m_j| <= C*r_j*f, their two squared majorants have relative factors
# 1 and rho^(2n+2), respectively.
overlap_factor_checks: dict[str, bool] = {}
overlap_factor_records: dict[str, str] = {}
for rho in rho_values:
    for degree in (0, 1):
        fine_factor = sp.simplify(
            rho ** (2 * degree) * (rho**2)
        )
        expected = rho ** (2 * degree + 2)
        key = f"rho{rho.p}_{rho.q}Degree{degree}"
        overlap_factor_checks[key] = fine_factor == expected
        overlap_factor_records[key] = sp.sstr(fine_factor)


# ---------------------------------------------------------------------------
# The alpha=1/4 temporal-Hardy threshold
# ---------------------------------------------------------------------------

alpha = sp.symbols("alpha", real=True)
weighted_power = sp.Rational(1, 2) + 2 * alpha
critical_alpha = sp.solve(sp.Eq(weighted_power, 1), alpha)[0]

alpha_samples = (
    sp.Rational(0),
    sp.Rational(1, 8),
    sp.Rational(1, 4),
    sp.Rational(1, 3),
    sp.Rational(3, 4),
)
threshold_records: dict[str, dict[str, object]] = {}
threshold_checks: dict[str, bool] = {}
for alpha_value in alpha_samples:
    exponent_value = sp.simplify(weighted_power.subs(alpha, alpha_value))
    weighted_integrable = bool(exponent_value < 1)
    leray_l1_integrable = bool(alpha_value < 1)
    key = f"alpha{alpha_value.p}_{alpha_value.q}"
    threshold_records[key] = {
        "alpha": sp.sstr(alpha_value),
        "weightedExponent": sp.sstr(exponent_value),
        "weightedL2Integrable": weighted_integrable,
        "scalarLerayL1Integrable": leray_l1_integrable,
    }
    threshold_checks[key] = weighted_integrable == bool(
        alpha_value < sp.Rational(1, 4)
    )


# ---------------------------------------------------------------------------
# Heat and Navier--Stokes scaling
# ---------------------------------------------------------------------------

A, r, n = sp.symbols("A r n", positive=True)
heat_energy = A**2 * r**3
heat_dissipation = A**2 * r**3
heat_moment = A**2 * r ** (n + 1)
heat_critical_moment = sp.simplify(r ** (1 - n) * heat_moment)
heat_target = sp.simplify(r**-3 * heat_critical_moment**2 * r**2)

heat_scaling_checks = {
    "energy": heat_energy == A**2 * r**3,
    "integratedEnstrophy": heat_dissipation == A**2 * r**3,
    "degree0Moment": heat_moment.subs(n, 0) == A**2 * r,
    "degree1Moment": heat_moment.subs(n, 1) == A**2 * r**2,
    "criticalMomentIndependentOfDegree": heat_critical_moment == A**2 * r**2,
    "targetIndependentOfDegree": heat_target == A**4 * r**3,
}

fixed_energy_amplitude = r ** sp.Rational(-3, 2)
fixed_energy_records = {
    "amplitude": "r^(-3/2)",
    "energyScale": sp.sstr(
        sp.simplify(heat_energy.subs(A, fixed_energy_amplitude))
    ),
    "dissipationScale": sp.sstr(
        sp.simplify(heat_dissipation.subs(A, fixed_energy_amplitude))
    ),
    "criticalMomentScale": sp.sstr(
        sp.simplify(heat_critical_moment.subs(A, fixed_energy_amplitude))
    ),
    "targetScale": sp.sstr(
        sp.simplify(heat_target.subs(A, fixed_energy_amplitude))
    ),
}
fixed_energy_heat_check = (
    sp.simplify(heat_energy.subs(A, fixed_energy_amplitude)) == 1
    and sp.simplify(heat_dissipation.subs(A, fixed_energy_amplitude)) == 1
    and sp.simplify(heat_target.subs(A, fixed_energy_amplitude)) == r**-3
)

a = sp.symbols("a", positive=True)
nse_amplitude = a / r
nse_energy = sp.simplify(heat_energy.subs(A, nse_amplitude))
nse_dissipation = sp.simplify(heat_dissipation.subs(A, nse_amplitude))
nse_critical_moment = sp.simplify(
    heat_critical_moment.subs(A, nse_amplitude)
)
nse_target = sp.simplify(heat_target.subs(A, nse_amplitude))
nse_outer_energy_square = sp.simplify(r**-3 * nse_energy**2)

nse_scaling_checks = {
    "energyIsRA2": nse_energy == r * a**2,
    "dissipationIsRA2": nse_dissipation == r * a**2,
    "criticalMomentIsA2": nse_critical_moment == a**2,
    "targetIsRMinus1A4": nse_target == r**-1 * a**4,
    "outerScaleEnergySquareMatches": nse_outer_energy_square == nse_target,
}


# ---------------------------------------------------------------------------
# General homogeneous right-hand side
# ---------------------------------------------------------------------------

p, q, gamma = sp.symbols("p q gamma", real=True)
rhs_scale_exponent = p + q - gamma
gamma_solution = sp.solve(sp.Eq(rhs_scale_exponent, -1), gamma)[0]

rhs_samples = (
    (sp.Integer(1), sp.Integer(0)),
    (sp.Integer(0), sp.Integer(1)),
    (sp.Integer(2), sp.Integer(0)),
    (sp.Integer(1), sp.Integer(1)),
    (sp.Integer(0), sp.Integer(2)),
    (sp.Rational(1, 2), sp.Rational(1, 2)),
)
rhs_checks: dict[str, bool] = {}
rhs_records: dict[str, dict[str, str]] = {}
for p_value, q_value in rhs_samples:
    gamma_value = sp.simplify(gamma_solution.subs({p: p_value, q: q_value}))
    resulting_exponent = sp.simplify(
        rhs_scale_exponent.subs(
            {p: p_value, q: q_value, gamma: gamma_value}
        )
    )
    key = f"p{sp.sstr(p_value)}q{sp.sstr(q_value)}"
    rhs_checks[key] = resulting_exponent == -1
    rhs_records[key] = {
        "p": sp.sstr(p_value),
        "q": sp.sstr(q_value),
        "forcedGamma": sp.sstr(gamma_value),
        "resultingScaleExponent": sp.sstr(resulting_exponent),
    }


# ---------------------------------------------------------------------------
# Frozen-low/annular same-index scale ledger and isotropic contraction
# ---------------------------------------------------------------------------

cutoff_weight_exponent = sp.Integer(-1)
support_l2_exponent = sp.Rational(3, 2)
current_band_curl_exponent = sp.Integer(-1)

# Equation (6.3) of the report: the cutoff weight, the square root of its
# support volume, and B_k=curl(V_k) give r_k^(-1/2).  This is exactly the
# half-weight paired with sum r_k^(-1)|c_k|^2.
mixed_current_band_exponent = sp.simplify(
    cutoff_weight_exponent
    + support_l2_exponent
    + current_band_curl_exponent
)
source_half_weight_exponent = sp.Rational(-1, 2)
frozen_vorticity_bernstein_exponent = sp.Rational(-3, 2)
mixed_outer_exponent = frozen_vorticity_bernstein_exponent

# Frozen low--low ledger, corresponding to (6.7)--(6.9):
#   r_k^(-1)*|supp| = r_k^2,
#   r_k^2 = r_k^(-1/2)*r_k^(5/2),
#   sum r_k^5 has square-root scale r_0^(5/2),
#   ||L_0||_infty^2 contributes r_0^(-5), and
#   the L_t^2-to-L_t^1 interval factor contributes r_0.
low_low_spatial_exponent = sp.simplify(cutoff_weight_exponent + 3)
low_low_cauchy_companion_exponent = sp.simplify(
    low_low_spatial_exponent - source_half_weight_exponent
)
low_low_geometric_square_exponent = sp.simplify(
    2 * low_low_cauchy_companion_exponent
)
low_velocity_bernstein_exponent = sp.Rational(-5, 2)
outer_interval_sqrt_exponent = sp.Integer(1)
low_low_outer_exponent = sp.simplify(
    low_low_cauchy_companion_exponent
    + 2 * low_velocity_bernstein_exponent
    + outer_interval_sqrt_exponent
)

mixed_scale_checks = {
    "cutoffSupportBandGivesRMinusHalf": (
        mixed_current_band_exponent == sp.Rational(-1, 2)
    ),
    "currentBandMatchesSourceHalfWeight": (
        mixed_current_band_exponent == source_half_weight_exponent
    ),
    "frozenVorticityBernsteinIsR0MinusThreeHalves": (
        frozen_vorticity_bernstein_exponent == sp.Rational(-3, 2)
    ),
    "mixedFinalOuterExponentIsMinusThreeHalves": (
        mixed_outer_exponent == sp.Rational(-3, 2)
    ),
    "lowLowSpatialWeightIsR2": low_low_spatial_exponent == 2,
    "lowLowCauchyCompanionIsRFiveHalves": (
        low_low_cauchy_companion_exponent == sp.Rational(5, 2)
    ),
    "lowLowGeometricSquareIsR5": low_low_geometric_square_exponent == 5,
    "lowVelocityBernsteinIsR0MinusFiveHalves": (
        low_velocity_bernstein_exponent == sp.Rational(-5, 2)
    ),
    "outerIntervalSquareRootIsR0": outer_interval_sqrt_exponent == 1,
    "lowLowFinalOuterExponentIsMinusThreeHalves": (
        low_low_outer_exponent == sp.Rational(-3, 2)
    ),
}

s11, s22, s12, s13, s23, isotropic_weight = sp.symbols(
    "s11 s22 s12 s13 s23 isotropic_weight", real=True
)
trace_free_strain = sp.Matrix(
    [
        [s11, s12, s13],
        [s12, s22, s23],
        [s13, s23, -s11 - s22],
    ]
)
isotropic_moment = isotropic_weight * sp.eye(3)
isotropic_contraction = sp.simplify(
    sum(
        trace_free_strain[row, column] * isotropic_moment[row, column]
        for row in range(3)
        for column in range(3)
    )
)
anisotropic_witness = sp.diag(1, 0, 0)
anisotropic_contraction = sp.simplify(
    sum(
        trace_free_strain[row, column] * anisotropic_witness[row, column]
        for row in range(3)
        for column in range(3)
    )
)

isotropic_checks = {
    "strainIsTraceFree": sp.trace(trace_free_strain) == 0,
    "isotropicContractionVanishes": isotropic_contraction == 0,
    "anisotropicContractionNotIdenticallyZero": anisotropic_contraction == s11,
}


checks = {
    "finiteKernelPiecewiseLedger": all(kernel_checks.values()),
    "finiteKernelMinBound": all(kernel_checks.values()),
    "overlapFineFactors": all(overlap_factor_checks.values()),
    "alphaQuarterThreshold": critical_alpha == sp.Rational(1, 4),
    "alphaThresholdSamples": all(threshold_checks.values()),
    "heatScalingLedger": all(heat_scaling_checks.values()),
    "fixedEnergyHeatTargetIsRMinus3": fixed_energy_heat_check,
    "nseInitialBoundaryScaling": all(nse_scaling_checks.values()),
    "generalRhsForcedGamma": gamma_solution == p + q + 1,
    "generalRhsSamples": all(rhs_checks.values()),
    "frozenLowMixedScaleLedger": all(mixed_scale_checks.values()),
    "isotropicTraceFreeContraction": all(isotropic_checks.values()),
}

if not all(checks.values()):
    raise AssertionError({key: value for key, value in checks.items() if not value})


result = {
    "release": "R0.70I",
    "status": "exact-finite-temporal-hardy-scaling-audit",
    "temporalHardyKernel": {
        "definition": (
            "G_K(s)=sum_{k=0}^{K-1} r_k^(-1)1_{s<r_(k+1)^2} "
            "+sum_{k=0}^{K-1} r_k^(-1)1_{r_(k+1)^2<=s<r_k^2} "
            "+r_K^(-1)1_{s<r_K^2}"
        ),
        "majorant": "G_K(s)<=C_rho*min(r_K^(-1),s^(-1/2))",
        "uniformConstant": "C_rho=1/(1-rho)",
        "ratios": [sp.sstr(value) for value in rho_values],
        "KRange": "0,...,8",
        "finiteRegionCasesChecked": kernel_case_count,
        "records": kernel_records,
        "overlapFineSquaredFactors": overlap_factor_records,
        "analyticBoundary": (
            "the producer samples every shell, the strict fine tail, and the "
            "fine endpoint for K<=8; the all-K geometric proof is not a finite "
            "regression claim"
        ),
    },
    "temporalThreshold": {
        "profile": "f(t0-s)=s^(-alpha)",
        "weightedIntegrandPower": "s^(-(1/2+2*alpha))",
        "criticalAlpha": sp.sstr(critical_alpha),
        "atCriticality": "1/2+2*(1/4)=1, hence logarithmic divergence",
        "lerayBoundary": (
            "alpha<1 gives scalar L1 integrability, while the weighted "
            "core majorant requires alpha<1/4"
        ),
        "samples": threshold_records,
    },
    "heatScaling": {
        "ansatz": "u^(A,r)(x,t)=A*v(x/r,t/r^2)",
        "energy": "A^2*r^3",
        "integratedEnstrophy": "A^2*r^3",
        "degreeNMoment": "A^2*r^(n+1)",
        "criticalMoment": "A^2*r^2",
        "coreTarget": "A^4*r^3",
        "fixedEnergyInitialLayer": fixed_energy_records,
        "equationBoundary": (
            "A=r^(-3/2) is a linear heat/Stokes scaling and is not the "
            "Navier--Stokes invariant amplitude"
        ),
    },
    "nseScaling": {
        "ansatz": "u^(a,r)(x,t)=r^(-1)*v^a(x/r,t/r^2)",
        "outerRadiusAndTop": "r_0=r and t_0=r^2",
        "energy": sp.sstr(nse_energy),
        "integratedEnstrophy": sp.sstr(nse_dissipation),
        "criticalMoment": sp.sstr(nse_critical_moment),
        "coreTarget": sp.sstr(nse_target),
        "outerScaleEnergySquare": sp.sstr(nse_outer_energy_square),
        "amplitudeBoundary": (
            "the exact producer checks exponents; the analytic small-amplitude "
            "lower bound T[v^a]>=c*a^4 requires a nondegenerate base moment"
        ),
    },
    "generalHomogeneousRhs": {
        "candidate": "r_0^(-gamma)*E^p*D^q",
        "nseScaleExponent": "p+q-gamma",
        "targetScaleExponent": "-1",
        "forcedGamma": "p+q+1",
        "samples": rhs_records,
    },
    "frozenLowMixedScale": {
        "currentBandLedger": {
            "cutoffWeight": "r_k^(-1)",
            "supportSquareRoot": "r_k^(3/2)",
            "curlBand": "||B_k||_2 <= r_k^(-1)||V_k||_2",
            "combined": f"r_k^({sp.sstr(mixed_current_band_exponent)})",
            "sourceHalfWeight": "r_k^(-1/2)|c_k|",
            "frozenVorticityBernstein": "r_0^(-3/2)||omega||_2",
            "finalOuterPower": sp.sstr(mixed_outer_exponent),
        },
        "lowLowLedger": {
            "spatialWeight": f"r_k^{sp.sstr(low_low_spatial_exponent)}",
            "cauchyCompanion": (
                f"r_k^({sp.sstr(low_low_cauchy_companion_exponent)})"
            ),
            "geometricSquareSum": (
                f"sum r_k^{sp.sstr(low_low_geometric_square_exponent)}"
            ),
            "geometricSquareRootOuterPower": sp.sstr(
                low_low_cauchy_companion_exponent
            ),
            "lowVelocityBernstein": "r_0^(-5/2)||u||_2",
            "lowVelocityBernsteinSquaredPower": "-5",
            "timeIntervalSquareRootPower": sp.sstr(
                outer_interval_sqrt_exponent
            ),
            "finalOuterPower": sp.sstr(low_low_outer_exponent),
        },
        "interpretation": (
            "both the frozen-low/annular same-index ledger and frozen low--low absolute "
            "estimates close with the report's outer factor r_0^(-3/2)"
        ),
        "scopeBoundary": (
            "only the outer frozen low L_0=P_(<=c/r_0)omega is covered; the "
            "producer checks the same-index exponent, while the report's full "
            "lower-triangular array uses the analytic r_k/r_j geometric "
            "convolution; the moving-low sum is excluded; physical cutoffs "
            "are retained and window indicators only reduce the absolute integral"
        ),
    },
    "isotropicTraceFree": {
        "contraction": sp.sstr(isotropic_contraction),
        "identity": "(q*I):S=q*trace(S)=0 for trace-free S",
        "anisotropicBoundary": (
            "trace freedom cancels only the isotropic tensor; the witness "
            "diag(1,0,0) contracts to s11 and need not vanish"
        ),
    },
    "checks": checks,
    "claimBoundary": {
        "finiteRegression": (
            "the kernel computation is exact for rho in {1/2,1/3,2/5}, "
            "K=0,...,8, and rational representatives of every shell, fine "
            "tail, and fine endpoint; it is not an all-K computer proof"
        ),
        "initialBoundary": (
            "the Navier--Stokes scaling ledger uses r_0=r, t_0=r^2 and "
            "therefore follows a family whose terminal time collapses to the "
            "initial face as r tends to zero"
        ),
        "notNseCommonTop": (
            "neither the fixed-energy heat scaling nor the small-amplitude "
            "Navier--Stokes initial-layer scaling constructs concentration "
            "along one unforced Leray/Navier--Stokes solution trajectory at "
            "one fixed positive terminal time uniformly separated from its "
            "initial face; the NSE family members all start at t=0 but have "
            "different rescaled data and solutions, with tops t_0=r^2 tending "
            "to zero"
        ),
        "notComputerProved": (
            "the all-scale Hardy bound, the full lower-triangular LP convolution, "
            "realization of the scalar power-law profile by a Navier--Stokes "
            "solution, the Kato expansion and nondegenerate base-moment lower "
            "bound, or nonlinear persistence"
        ),
        "notClaimed": (
            "a common-positive-top counterexample, singularity formation, "
            "large-data regularity, theorem nonexistence, or a Millennium solution"
        ),
    },
}

print(json.dumps(result, indent=2, sort_keys=True))
