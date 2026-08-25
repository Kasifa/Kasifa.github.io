#!/usr/bin/env python3
"""Exact finite audit for the R0.71A projector-coherence gate.

The producer checks two narrowly delimited obstructions.

1. A ten-mode real periodic vorticity pair has the same pointwise smooth
   frame covariance, an exactly constant principal projector, a strong
   eigengap, a zero scalar-frame commutator, and opposite nonzero covariance
   work.
2. The projector integration-by-parts error has an energy-level L1 estimate
   on the dimensionally critical mixed-norm line, whereas the corresponding
   L2 estimate has a one-power Navier--Stokes scaling mismatch.  A local
   divergence-free seed verifies that the trilinear functional is not
   identically zero.

The finite calculations do not prove that the critical projector condition
fails for Navier--Stokes solutions.  They rule out a coherence-only law and
one specific kinematic energy interpolation route.  They do not prove a
singularity, global regularity, or any Millennium-problem claim.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import product
from pathlib import Path

import sympy as sp

import r070z_exact_audit as previous


Frequency = tuple[int, int, int]

canonical = previous.canonical
require = previous.require
scalar_payload = previous.scalar_payload
vector_payload = previous.vector_payload
matrix_is_zero = previous.matrix_is_zero
add_frequency = previous.add_frequency
negative_frequency = previous.negative_frequency
frequency_square = previous.frequency_square
scale_vector = previous.scale_vector
outer = previous.outer
frobenius = previous.frobenius
real_cosine_modes = previous.real_cosine_modes
strain_coefficients = previous.strain_coefficients
covariance_convolution = previous.covariance_convolution
contraction_work = previous.contraction_work
separated_frame_gamma = previous.separated_frame_gamma

e1 = previous.e1
e2 = previous.e2
e3 = previous.e3
identity = previous.identity


# ---------------------------------------------------------------------------
# 1. A two-radius field entirely in the plane orthogonal to e3.
# ---------------------------------------------------------------------------

base_n: Frequency = (-1, 0, -1)
base_p: Frequency = (-3, -3, 4)
base_q: Frequency = (4, 3, -3)
base_c = sp.Matrix([0, -1, 0])
base_a = sp.Matrix([1, -1, 0]) / sp.sqrt(2)
base_b = sp.Matrix([-3, 4, 0]) / 5

require(
    add_frequency(add_frequency(base_n, base_p), base_q) == (0, 0, 0),
    "base triad resonance",
)
require(frequency_square(base_n) == 2, "base low radius")
require(frequency_square(base_p) == 34, "base first high radius")
require(frequency_square(base_q) == 34, "base second high radius")
require(34 - 16 * 2 == 2, "base strict factor-four separation")

for frequency, coefficient in (
    (base_n, base_c),
    (base_p, base_a),
    (base_q, base_b),
):
    require(
        canonical(sp.Matrix(frequency).dot(coefficient)) == 0,
        "base Fourier divergence",
    )
    require(canonical(coefficient.dot(e3)) == 0, "base planar polarization")
    require(canonical(coefficient.dot(coefficient)) == 1, "base normalization")

base_fourier: dict[Frequency, sp.Matrix] = {}
for frequency, coefficient in (
    (base_n, base_c),
    (base_p, base_a),
    (base_q, base_b),
):
    base_fourier.update(real_cosine_modes(frequency, coefficient))

base_strain = strain_coefficients(base_fourier)
base_covariance = covariance_convolution(base_fourier, separated_frame_gamma)
base_full_covariance = covariance_convolution(
    base_fourier, lambda _first, _second: sp.Integer(1)
)
base_defect_covariance = covariance_convolution(
    base_fourier,
    lambda first, second: 1 - separated_frame_gamma(first, second),
)

base_work = contraction_work(base_strain, base_covariance)
base_full_work = contraction_work(base_strain, base_full_covariance)
base_defect_work = contraction_work(base_strain, base_defect_covariance)
base_work_expected = canonical(3 * sp.sqrt(2) / 40)
base_full_expected = canonical(6 * sp.sqrt(2) / 85)
base_defect_expected = canonical(-3 * sp.sqrt(2) / 680)

require(canonical(base_work - base_work_expected) == 0, "base covariance work")
require(
    canonical(base_full_work - base_full_expected) == 0,
    "base full work",
)
require(
    canonical(base_defect_work - base_defect_expected) == 0,
    "base defect work",
)
require(
    canonical(base_full_work - base_work - base_defect_work) == 0,
    "base full-covariance-defect split",
)

for coefficient in base_covariance.values():
    require(
        all(
            canonical(coefficient[row, column]) == 0
            for row, column in (
                (0, 2),
                (1, 2),
                (2, 0),
                (2, 1),
                (2, 2),
            )
        ),
        "base covariance is supported in e3-perp",
    )

# The low response contributes at most one.  The common high response is the
# outer product of a*cos(p.x)+b*cos(q.x), whose norm is at most two.  Hence
# ||Q_base||_op <= tr(Q_base) <= 1+4=5 pointwise.
base_covariance_operator_bound = sp.Integer(5)
base_mean_energy = canonical(
    sp.Rational(1, 2)
    * sum(
        coefficient.dot(coefficient)
        for coefficient in (base_c, base_a, base_b)
    )
)
require(base_mean_energy == sp.Rational(3, 2), "base mean energy")


# ---------------------------------------------------------------------------
# 2. Orthogonal separated filler and the constant-projector sign pair.
# ---------------------------------------------------------------------------

filler_m = sp.Integer(24)
filler_n = sp.Integer(97)
filler_denominator = canonical(filler_m**2 + filler_n**2)
filler_amplitude_square = canonical(15 * filler_denominator)
filler_amplitude = sp.sqrt(filler_amplitude_square)

require(filler_denominator == 9985, "filler denominator")
require(math.gcd(int(filler_m), int(filler_n)) == 1, "filler coprimality")
require(int(filler_n) % 2 == 1, "sine frequency parity")
require(filler_m**2 - 16 * 34 == 32, "first filler separation")
require(
    filler_n**2 - 16 * filler_m**2 == 193,
    "second filler separation",
)

filler_fourier: dict[Frequency, sp.Matrix] = {
    (int(filler_m), 0, 0): scale_vector(filler_amplitude / 2, e3),
    (-int(filler_m), 0, 0): scale_vector(filler_amplitude / 2, e3),
    (int(filler_n), 0, 0): scale_vector(-sp.I * filler_amplitude / 2, e3),
    (-int(filler_n), 0, 0): scale_vector(sp.I * filler_amplitude / 2, e3),
}


def combined_modes(sign: int) -> dict[Frequency, sp.Matrix]:
    combined = {
        mode: scale_vector(sp.Integer(sign), coefficient)
        for mode, coefficient in base_fourier.items()
    }
    for mode, coefficient in filler_fourier.items():
        require(mode not in combined, "disjoint combined Fourier support")
        combined[mode] = coefficient
    return combined


combined_plus = combined_modes(1)
combined_minus = combined_modes(-1)
base_support = set(base_fourier)
filler_support = set(filler_fourier)
all_support = tuple(sorted(base_support | filler_support))

filler_resonances: list[tuple[Frequency, Frequency, Frequency]] = []
for first_mode, second_mode, third_mode in product(all_support, repeat=3):
    if not ({first_mode, second_mode, third_mode} & filler_support):
        continue
    if add_frequency(add_frequency(first_mode, second_mode), third_mode) == (
        0,
        0,
        0,
    ):
        filler_resonances.append((first_mode, second_mode, third_mode))
require(len(filler_resonances) == 0, "no filler-involving triad resonance")

combined_plus_covariance = covariance_convolution(
    combined_plus, separated_frame_gamma
)
combined_minus_covariance = covariance_convolution(
    combined_minus, separated_frame_gamma
)
combined_outputs = set(combined_plus_covariance) | set(combined_minus_covariance)
for output in combined_outputs:
    difference = (
        combined_plus_covariance.get(output, sp.zeros(3, 3))
        - combined_minus_covariance.get(output, sp.zeros(3, 3))
    ).applyfunc(canonical)
    require(matrix_is_zero(difference), "sign-pair covariance equality")

combined_plus_work = contraction_work(
    strain_coefficients(combined_plus), combined_plus_covariance
)
combined_minus_work = contraction_work(
    strain_coefficients(combined_minus), combined_minus_covariance
)
require(
    canonical(combined_plus_work - base_work_expected) == 0,
    "positive sign-pair work",
)
require(
    canonical(combined_minus_work + base_work_expected) == 0,
    "negative sign-pair work",
)

# The parity zero-set lemma from R0.70Y gives
# cos(24*x1)^2+sin(97*x1)^2 >= 1/(24^2+97^2).  Thus the e3 eigenvalue is at
# least 15, whereas the complete e3-perp block has operator norm at most 5.
filler_eigenvalue_lower = canonical(
    filler_amplitude_square / filler_denominator
)
absolute_gap_lower = canonical(
    filler_eigenvalue_lower - base_covariance_operator_bound
)
top_normalized_gap_lower = canonical(
    absolute_gap_lower / filler_eigenvalue_lower
)
trace_relative_gap_lower = canonical(
    absolute_gap_lower
    / (filler_eigenvalue_lower + base_covariance_operator_bound)
)
require(filler_eigenvalue_lower == 15, "filler eigenvalue lower")
require(absolute_gap_lower == 10, "absolute eigengap lower")
require(top_normalized_gap_lower == sp.Rational(2, 3), "top gap ratio")
require(
    trace_relative_gap_lower == sp.Rational(1, 2),
    "trace-relative gap ratio",
)

principal_projector = outer(e3)
lower_projector = identity - principal_projector
require(matrix_is_zero(principal_projector.diff(sp.Symbol("x"))), "constant P1")
require(matrix_is_zero(principal_projector**2 - principal_projector), "P1 idempotent")
require(sp.trace(principal_projector) == 1, "P1 rank one")


# ---------------------------------------------------------------------------
# 3. Exact exponent and scaling ledger for the kinematic projector error.
# ---------------------------------------------------------------------------

p = sp.symbols("p", positive=True)
q = canonical(2 * p / (p - 3))
spatial_velocity_exponent = canonical(2 * p / (p - 2))
gn_gradient_power = canonical(3 / p)
time_holder_sum = canonical(1 / q + (1 + 3 / p) / 2)
critical_projector_scaling = canonical(1 - 3 / p - 2 / q)

require(time_holder_sum == 1, "critical line gives only L1 in time")
require(critical_projector_scaling == 0, "critical projector norm scaling")

error_pointwise_scaling = sp.Integer(1)
error_l1_scaling = canonical(error_pointwise_scaling - 2)
error_l2_scaling = canonical(error_pointwise_scaling - 1)
velocity_energy_scaling = -sp.Rational(1, 2)
natural_energy_rhs_scaling = canonical(
    velocity_energy_scaling * (1 - 3 / p)
    + velocity_energy_scaling * (1 + 3 / p)
    + critical_projector_scaling
)
require(error_l1_scaling == -1, "error L1 scaling")
require(error_l2_scaling == 0, "error L2 scaling")
require(natural_energy_rhs_scaling == -1, "natural energy RHS scaling")
require(
    error_l1_scaling == natural_energy_rhs_scaling,
    "L1 estimate is scale homogeneous",
)
require(
    error_l2_scaling != natural_energy_rhs_scaling,
    "L2 estimate has one-power scaling mismatch",
)

# After the additional amplitude normalization
# u_hat_lambda=lambda^(1/2)u_lambda, both energy norms are fixed rather than
# merely small.  Since the error is quadratic in u, its Ls norm scales like
# lambda^(2-2/s).  This rules out every finite control function of the same
# three norm values for s>1, not only the natural monomial estimate.
s = sp.symbols("s", positive=True)
normalized_velocity_energy_scaling = sp.Integer(0)
normalized_gradient_energy_scaling = sp.Integer(0)
normalized_error_ls_scaling = canonical(2 - 2 / s)
normalized_error_l1_scaling = canonical(normalized_error_ls_scaling.subs(s, 1))
normalized_error_l2_scaling = canonical(normalized_error_ls_scaling.subs(s, 2))
require(normalized_error_l1_scaling == 0, "normalized error L1 scaling")
require(normalized_error_l2_scaling == 1, "normalized error L2 scaling")

# Local nonzero seed.  In a region where a compactly supported vector
# potential has no cutoff error, U=(z,0,y).  For the first variation of
# L=(cos(theta),sin(theta),0) tensor itself at theta=0, put
# F_i=U_1*d_2 U_i+U_2*d_1 U_i.  Its divergence is one in that region, so the
# compact construction psi=div(F) gives J'(0)=-integral psi^2<0.
x, y, z = sp.symbols("x y z", real=True)
local_velocity = sp.Matrix([z, 0, y])
local_divergence = canonical(
    sp.diff(local_velocity[0], x)
    + sp.diff(local_velocity[1], y)
    + sp.diff(local_velocity[2], z)
)
local_F = sp.Matrix(
    [
        canonical(
            local_velocity[0] * sp.diff(local_velocity[index], y)
            + local_velocity[1] * sp.diff(local_velocity[index], x)
        )
        for index in range(3)
    ]
)
local_F_divergence = canonical(
    sp.diff(local_F[0], x)
    + sp.diff(local_F[1], y)
    + sp.diff(local_F[2], z)
)
require(local_divergence == 0, "local seed divergence free")
require(local_F == sp.Matrix([0, 0, z]), "local first-variation vector")
require(local_F_divergence == 1, "local first variation is nonzero")

# A separate exact periodic seed confirms the trilinear functional is not an
# algebraic zero.  With theta=z and a(z)=1+delta*cos(2z), take
# U=curl(0,a(z)cos(x),0).  Normalized torus integration gives delta/2.
delta = sp.symbols("delta", real=True)
amplitude = 1 + delta * sp.cos(2 * z)
periodic_integrand = canonical(
    (-sp.diff(amplitude, z) * sp.cos(x))
    * (-amplitude * sp.cos(x))
    * (-sp.sin(2 * z))
)
periodic_seed_work = canonical(
    sp.integrate(periodic_integrand, (x, 0, 2 * sp.pi), (z, 0, 2 * sp.pi))
    / (2 * sp.pi) ** 2
)
require(periodic_seed_work == delta / 2, "periodic nonzero seed")


payload = {
    "release": "R0.71A",
    "status": "projector-coherence-method-boundary",
    "checks": {
        "planarTwoRadiusField": True,
        "constantPrincipalProjector": True,
        "sameCovarianceOppositeWork": True,
        "strongAbsoluteRelativeGap": True,
        "zeroScalarFrameCommutator": True,
        "criticalLineL1Exponent": True,
        "kinematicL2ScalingObstruction": True,
        "nonzeroCompactSeedJet": True,
        "nonzeroPeriodicSeed": True,
    },
    "constantProjectorLedger": {
        "baseField": "xi=c*cos(n.x)+a*cos(p.x)+b*cos(q.x)",
        "n": list(base_n),
        "p": list(base_p),
        "q": list(base_q),
        "c": vector_payload(base_c),
        "a": vector_payload(base_a),
        "b": vector_payload(base_b),
        "radiiSquared": [2, 34, 34, 576, 9409],
        "strictFactorFourSquaredSlacks": [2, 32, 193],
        "baseCovarianceWork": scalar_payload(base_work),
        "baseFullWork": scalar_payload(base_full_work),
        "baseDefectWork": scalar_payload(base_defect_work),
        "baseMeanEnergy": scalar_payload(base_mean_energy),
        "baseCovarianceOperatorUpper": scalar_payload(
            base_covariance_operator_bound
        ),
        "fields": "omega_(Lambda,sigma)=Lambda*(sigma*xi+sqrt(15*9985)*eta)",
        "eta": "e3*(cos(24*x1)+sin(97*x1))",
        "modeCount": len(combined_plus),
        "covarianceDifference": "zero at every Fourier output",
        "fillerInvolvingResonanceCount": len(filler_resonances),
        "principalProjector": "P1=e3 tensor e3 at every point",
        "projectorGradient": "0",
        "lowerProjectorFrameCommutator": "[T_alpha,I-P1]=0 for every scalar frame block",
        "positiveWork": scalar_payload(combined_plus_work),
        "negativeWork": scalar_payload(combined_minus_work),
        "scaledWork": "+/-(3*sqrt(2)/40)*Lambda^3",
        "transverseResidual": "integral tr((I-P1)Q)=(3/2)*Lambda^2",
        "freeAmplitudeAngle": "for omega_(A,sigma)=sigma*xi+A*eta, sin(theta)=|xi|/sqrt(|xi|^2+A^2*(cos(24*x1)+sin(97*x1))^2), independent of sigma",
        "finiteAngleLimit": "sin(theta)->0 in every finite Lp as A->infinity, while covariance work remains +/-(3*sqrt(2)/40)",
        "angleBoundary": "the limit is not L-infinity and the amplitude-weighted transverse vorticity remains xi",
    },
    "eigengapLedger": {
        "fillerLowerLemma": "cos(24*x1)^2+sin(97*x1)^2>=1/9985",
        "fillerAmplitudeSquare": scalar_payload(filler_amplitude_square),
        "fillerEigenvalueLower": scalar_payload(filler_eigenvalue_lower),
        "absoluteGap": "lambda1-lambda2>=10*Lambda^2",
        "topNormalizedGap": "(lambda1-lambda2)/lambda1>=2/3",
        "traceRelativeGap": "(lambda1-lambda2)/tr(Q)>=1/2",
        "blockStructure": "Q=Q_xi+C^2*h*e3 tensor e3 and ran(Q_xi) is contained in e3-perp",
    },
    "criticalLineLedger": {
        "range": "3<=p<=infinity, 2/q+3/p=1",
        "q": "2*p/(p-3), with q=infinity at p=3",
        "spaceHolderVelocityExponent": scalar_payload(
            spatial_velocity_exponent
        ),
        "gagliardoNirenbergGradientPower": scalar_payload(gn_gradient_power),
        "timeHolderReciprocalSum": scalar_payload(time_holder_sum),
        "positiveEstimate": "||E_L||_L1t <= C_p ||grad L||_Lq_tLp_x ||u||_Linf_tL2_x^(1-3/p) ||grad u||_L2_tL2_x^(1+3/p)",
        "projectorCriticalNormScaling": scalar_payload(
            critical_projector_scaling
        ),
        "errorL1Scaling": scalar_payload(error_l1_scaling),
        "errorL2Scaling": scalar_payload(error_l2_scaling),
        "naturalEnergyRhsScaling": scalar_payload(
            natural_energy_rhs_scaling
        ),
        "scalingConclusion": "the L1 bound is homogeneous; the analogous L2 bound loses one power under concentration",
        "sameNormSequence": "u_hat_lambda=lambda^(1/2)*u_lambda fixes both energy norms and the critical projector norm",
        "sameNormErrorLsScaling": "lambda^(2-2/s)",
        "sameNormErrorL1Scaling": scalar_payload(
            normalized_error_l1_scaling
        ),
        "sameNormErrorL2Scaling": scalar_payload(
            normalized_error_l2_scaling
        ),
        "strongConclusion": "no finite function of the three fixed norm values controls the error in Ls_t for any s>1",
        "endpointP3": "q=infinity and the energy estimate is still only L1 in time",
        "endpointPInfinity": "q=2; the product of grad-L in L2_t and grad-u in L2_t is only L1_t",
    },
    "nonzeroSeedLedger": {
        "localVelocity": vector_payload(local_velocity),
        "localVelocityDivergence": scalar_payload(local_divergence),
        "firstVariationVector": vector_payload(local_F),
        "firstVariationDivergence": scalar_payload(local_F_divergence),
        "compactification": "take U=curl(chi*(-y^2/2,0,y*z)), set F_i=U1*d2(U_i)+U2*d1(U_i), psi=div(F), and L_epsilon=ell_epsilon tensor ell_epsilon with ell_epsilon=(cos(epsilon*psi),sin(epsilon*psi),0)",
        "firstVariation": "J'(0)=-integral |div(F)|^2<0; since I_L=-J, epsilon>0 gives a nonzero positive part (I_L)_+",
        "periodicSeed": "theta=z, a(z)=1+delta*cos(2z), U=curl(0,a(z)*cos(x),0)",
        "periodicSeedWork": scalar_payload(periodic_seed_work),
    },
    "analyticDependencies": [
        "the scalar frame is the fixed real-even radial smooth Parseval frame used in R0.70P-Z",
        "strict factor-four separation makes the listed distinct-radius frame responses orthogonal",
        "the filler lower bound reuses the exact zero-set parity lemma proved in R0.70Y",
        "the pointwise base covariance bound uses only the triangle inequality and unit polarizations",
        "a constant matrix projector commutes exactly with every scalar Fourier multiplier",
        "the compact nonzero seed requires a smooth cutoff equal to one on a ball and the continuity of J(epsilon) at epsilon zero",
        "the scaling no-go is kinematic and is tested on smooth compactly supported fields, not asserted as an NSE-solution counterexample",
    ],
    "claimBoundary": [
        "proves that even an exactly constant covariance principal projector, a strong eigengap, and a zero exact scalar-frame commutator do not determine the sign or force the vanishing of covariance work",
        "shows that extra amplitude-sensitive, signed, or dynamical information is needed for this proof target; residual and weighted alignment are concrete non-exhaustive candidates",
        "shows that an unweighted finite-Lp angle to the principal line can tend to zero while covariance work stays nonzero; it does not reach L-infinity angle or weighted transverse vorticity",
        "proves the energy-level critical mixed-norm estimate for the projector integration-by-parts error in L1_t",
        "rules out every finite Ls_t control function of only the two energy norms and the critical projector norm for s>1, by an explicit nonzero seed and an amplitude-normalized concentrating sequence",
        "does not rule out a different estimate using NSE dynamics, signed cancellation, a Carleson measure, extra regularity, smallness, or the transverse residual",
        "does not prove a continuation criterion, singularity, global regularity, or solve the Millennium problem",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output is None:
        print(rendered, end="")
    else:
        arguments.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
