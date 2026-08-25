#!/usr/bin/env python3
"""Exact finite audit for the R0.70Y response-slope and Besov gate.

The producer checks six narrowly delimited facts:

1. the response-chord, symmetric, metric/response, wedge, and Gram identities;
2. an actual radial-frame family excluding Gram-area divisibility;
3. the scale-separation arithmetic behind the q=3 packet obstruction;
4. the two-shell filler covariance and a uniform positive top eigenvalue;
5. the exact absence of a principal eigengap in that filler family; and
6. an independent 40-mode Fourier/Parseval reconstruction of the filler work.

The finite calculations do not prove the periodic Coifman--Meyer theorem,
the Littlewood--Paley summation theorem, a principal-eigengap no-go theorem,
an enstrophy closure, a continuation theorem, or any Navier--Stokes
regularity conclusion.  Those analytic dependencies and boundaries are
stated explicitly in the accompanying report.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from itertools import product
from pathlib import Path

import sympy as sp

import r070x_exact_audit as previous


Frequency = tuple[int, int, int]


def canonical(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.expand(expression)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def scalar_payload(expression: sp.Expr) -> str:
    return str(canonical(expression))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [scalar_payload(entry) for entry in vector]


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(canonical(entry) == 0 for entry in matrix)


def outer(first: sp.Matrix, second: sp.Matrix | None = None) -> sp.Matrix:
    if second is None:
        second = first
    return first * second.T


def frobenius(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return canonical(
        sum(
            first[row, column] * second[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


def add_frequency(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def negative_frequency(frequency: Frequency) -> Frequency:
    return tuple(-entry for entry in frequency)  # type: ignore[return-value]


def frequency_square(frequency: Frequency) -> int:
    return sum(entry * entry for entry in frequency)


def scale_vector(scalar: sp.Expr, vector: sp.Matrix) -> sp.Matrix:
    return vector.applyfunc(lambda entry: canonical(scalar * entry))


e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])


# ---------------------------------------------------------------------------
# 1. Generic response-slope identities.
# ---------------------------------------------------------------------------

B_n, B_p = sp.symbols("B_n B_p", real=True)
B_q = -B_n - B_p

dn = sp.Matrix(sp.symbols("dn0:3", real=True))
dp = sp.Matrix(sp.symbols("dp0:3", real=True))
dq = sp.Matrix(sp.symbols("dq0:3", real=True))

norm_dn = canonical(dn.dot(dn))
norm_dp = canonical(dp.dot(dp))
norm_dq = canonical(dq.dot(dq))
beta_dn = norm_dn / 2
beta_dp = norm_dp / 2
beta_dq = norm_dq / 2

response_block = canonical(beta_dn * B_n + beta_dp * B_p + beta_dq * B_q)
two_leg_form = canonical(
    sp.Rational(1, 2)
    * (
        (norm_dn - norm_dq) * B_n
        + (norm_dp - norm_dq) * B_p
    )
)

cyclic_pairs = (
    (dn, dp, B_n, B_p),
    (dp, dq, B_p, B_q),
    (dq, dn, B_q, B_n),
)
symmetric_form = canonical(
    sp.Rational(1, 6)
    * sum(
        (first - second).dot(first + second)
        * (first_B - second_B)
        for first, second, first_B, second_B in cyclic_pairs
    )
)

require(canonical(response_block - two_leg_form) == 0, "two-leg chord form")
require(canonical(response_block - symmetric_form) == 0, "symmetric chord form")

x_n, x_p, K_n, K_p = sp.symbols("x_n x_p K_n K_p", real=True)
response_difference = sp.symbols("response_difference", real=True)
metric_split = canonical(
    sp.Rational(1, 2) * (x_n + x_p) * response_difference
    + sp.Rational(1, 2) * (x_n - x_p) * (K_n + K_p)
)
metric_split_residual = canonical(
    x_n * K_n
    - x_p * K_p
    - metric_split.subs(response_difference, K_n - K_p)
)
require(metric_split_residual == 0, "metric/response split")

gram_gamma, norm_square = sp.symbols(
    "gram_gamma norm_square", real=True, positive=True
)
wedge_norm_square = canonical(
    (1 - gram_gamma**2) / (norm_square * (1 + gram_gamma))
)
chord_norm_square = canonical((1 - gram_gamma) / norm_square)
wedge_norm_residual = canonical(wedge_norm_square - chord_norm_square)
require(wedge_norm_residual == 0, "wedge/chord norm identity")

A_n, A_p, A_q = sp.symbols("A_n A_p A_q", real=True)
g_xy, g_yz, g_zx = sp.symbols("g_xy g_yz g_zx", real=True)
response_gram = sp.Matrix(
    [[1, g_xy, g_zx], [g_xy, 1, g_yz], [g_zx, g_yz, 1]]
)
graph_laplacian = sp.Matrix(
    [
        [A_p + A_q, -A_q, -A_p],
        [-A_q, A_q + A_n, -A_n],
        [-A_p, -A_n, A_n + A_p],
    ]
)
gram_trace = canonical(sp.trace(graph_laplacian * response_gram) / 2)
gram_block = canonical(
    (1 - g_yz) * A_n + (1 - g_zx) * A_p + (1 - g_xy) * A_q
)
gram_trace_residual = canonical(gram_trace - gram_block)
require(gram_trace_residual == 0, "Gram trace identity")


# ---------------------------------------------------------------------------
# 2. Actual radial-frame family excluding Gram-area divisibility.
# ---------------------------------------------------------------------------

family_M = sp.symbols("M", integer=True, positive=True)
family_R2 = canonical(2 * family_M**2 + 2 * family_M + 1)
family_d = 2 * family_M + 1

family_n = sp.Matrix([1, 1, 0])
family_p = sp.Matrix([family_M, -family_M - 1, 0])
family_q = sp.Matrix([-family_M - 1, family_M, 0])
family_c = sp.Matrix([1, -1, 0])
family_a = e3
family_b = sp.Matrix([family_M, family_M + 1, 0])

family_A_n = previous.triad_leg(
    family_n, family_p, family_q, family_c, family_a, family_b
)
family_A_p = previous.triad_leg(
    family_p, family_q, family_n, family_a, family_b, family_c
)
family_A_q = previous.triad_leg(
    family_q, family_n, family_p, family_b, family_c, family_a
)
family_cyclic = canonical(
    family_n.dot(family_n) * family_A_n
    + family_p.dot(family_p) * family_A_p
    + family_q.dot(family_q) * family_A_q
)
family_block = canonical(family_A_p + family_A_q)
family_expected = canonical(-2 * family_d / family_R2)

require(matrix_is_zero(family_n + family_p + family_q), "family resonance")
require(canonical(family_n.dot(family_c)) == 0, "family n divergence")
require(canonical(family_p.dot(family_a)) == 0, "family p divergence")
require(canonical(family_q.dot(family_b)) == 0, "family q divergence")
require(canonical(family_p.dot(family_p) - family_R2) == 0, "family p radius")
require(canonical(family_q.dot(family_q) - family_R2) == 0, "family q radius")
require(canonical(family_A_n - family_d) == 0, "family A_n")
require(
    canonical(family_A_p - family_d * (1 - 2 / family_R2)) == 0,
    "family A_p",
)
require(canonical(family_A_q + family_d) == 0, "family A_q")
require(family_cyclic == 0, "family cyclic identity")
require(canonical(family_block - family_expected) == 0, "family block")
require(canonical(family_R2.subs(family_M, 4) - 32) > 0, "family separation")

K_family = (sp.Integer(0), sp.Integer(1), sp.Integer(1))
area_family = canonical(
    2 * (K_family[0] * K_family[1] + K_family[1] * K_family[2] + K_family[2] * K_family[0])
    - sum(entry**2 for entry in K_family)
)
det_family = canonical(area_family - 2 * sp.prod(K_family))
require(area_family == 0, "family affine response area")
require(det_family == 0, "family response Gram determinant")


# ---------------------------------------------------------------------------
# 3. Scale-packet separation arithmetic and sequence exponent.
# ---------------------------------------------------------------------------

packet_scale = sp.Integer(64)
packet_min_square = sp.Integer(5)
packet_max_square = sp.Integer(149)
one_top_slack = canonical(packet_scale**2 * packet_min_square - 4 * packet_max_square)
two_top_slack = canonical(packet_scale**2 - packet_max_square)

require(one_top_slack > 0, "one-top packet separation")
require(two_top_slack > 0, "two-top packet separation")
require(packet_scale == 2**6, "dyadic response shift")


# ---------------------------------------------------------------------------
# 4. Filler covariance and uniform positive top eigenvalue.
# ---------------------------------------------------------------------------

filler_m = sp.Integer(49)
filler_n = sp.Integer(197)
filler_lower_denominator = filler_m**2 + filler_n**2
filler_first_slack = canonical(filler_m**2 - 16 * packet_max_square)
filler_second_slack = canonical(filler_n**2 - 16 * filler_m**2)

require(math.gcd(int(filler_m), int(filler_n)) == 1, "filler coprimality")
require(int(filler_m) % 2 == 1 and int(filler_n) % 2 == 1, "filler parity")
require(filler_first_slack > 0, "first filler separation")
require(filler_second_slack > 0, "second filler separation")
require(filler_lower_denominator == 41210, "filler lower denominator")

Lambda, covariance_q, covariance_h = sp.symbols(
    "Lambda covariance_q covariance_h", positive=True, real=True
)
wx, wy, wz = sp.symbols("wx wy wz", real=True)
w_generic = sp.Matrix([wx, wy, wz])
filler_covariance = (
    Lambda**2 * covariance_q * outer(w_generic)
    + covariance_h * outer(e2)
)
covariance_area_square = canonical(
    (
        sp.trace(filler_covariance) ** 2
        - sp.trace(filler_covariance * filler_covariance)
    )
    / 2
)
covariance_area_expected = canonical(
    Lambda**2
    * covariance_q
    * covariance_h
    * w_generic.cross(e2).dot(w_generic.cross(e2))
)
covariance_area_residual = canonical(
    covariance_area_square - covariance_area_expected
)
require(covariance_area_residual == 0, "filler covariance area")


# ---------------------------------------------------------------------------
# 5. Explicit and asymptotic absence of a principal eigengap.
# ---------------------------------------------------------------------------

curve_A = sp.symbols("A", real=True)
curve_w = 3 * sp.sin(curve_A) * (e1 - e3)
curve_q = sp.Integer(2)
curve_substitution = {
    previous.x1: curve_A / 3,
    previous.x2: 2 * curve_A / 3,
    previous.x3: curve_A / 3,
}
curve_z_residual = canonical(
    previous.axis.dot(
        sp.Matrix(
            [
                curve_substitution[previous.x1],
                curve_substitution[previous.x2],
                curve_substitution[previous.x3],
            ]
        )
    )
)
curve_w_residual = (
    previous.w_field.subs(curve_substitution) - curve_w
).applyfunc(sp.trigsimp)
curve_q_from_frame = canonical(
    previous.covariance_scalar.subs(
        {
            previous.f1: 1,
            previous.fM: 1,
            previous.fN: 0,
        }
    )
)
curve_X = canonical(Lambda**2 * curve_q * curve_w.dot(curve_w))
curve_X_expected = canonical(36 * Lambda**2 * sp.sin(curve_A) ** 2)
require(curve_z_residual == 0, "curve axial phase")
require(matrix_is_zero(curve_w_residual), "curve old-field vector")
require(curve_q_from_frame == curve_q, "curve covariance scalar")
require(canonical(curve_X - curve_X_expected) == 0, "curve principal eigenvalue")

explicit_Lambda = sp.Rational(1, 6)
explicit_A = sp.pi / 2
explicit_x1 = explicit_A / 3
explicit_h = sp.trigsimp(
    sp.cos(filler_m * explicit_x1) ** 2
    + sp.sin(filler_n * explicit_x1) ** 2
)
explicit_X = sp.trigsimp(
    curve_X.subs({Lambda: explicit_Lambda, curve_A: explicit_A})
)
require(explicit_h == 1, "explicit filler eigenvalue")
require(explicit_X == 1, "explicit old-field eigenvalue")


# ---------------------------------------------------------------------------
# 6. Independent 40-mode filler Fourier/Parseval reconstruction.
# ---------------------------------------------------------------------------

I = sp.I
physical_kappa = previous.physical_kappa

combined_fourier: dict[Frequency, sp.Matrix] = {
    mode: scale_vector(Lambda, coefficient)
    for mode, coefficient in previous.omega_fourier.items()
}
combined_label: dict[Frequency, tuple[str, int]] = {
    mode: ("old", previous.shell_label[mode])
    for mode in previous.omega_fourier
}

filler_modes: dict[Frequency, sp.Matrix] = {
    (int(filler_m), 0, 0): e2 / 2,
    (-int(filler_m), 0, 0): e2 / 2,
    (int(filler_n), 0, 0): -I * e2 / 2,
    (-int(filler_n), 0, 0): I * e2 / 2,
}
for mode, coefficient in filler_modes.items():
    require(mode not in combined_fourier, "new filler mode")
    combined_fourier[mode] = coefficient
    combined_label[mode] = ("filler", abs(mode[0]))


def combined_response_kernel(
    first: tuple[str, int], second: tuple[str, int]
) -> sp.Expr:
    if first[0] == "old" and second[0] == "old":
        return previous.response_kernel(first[1], second[1])
    if first == second:
        return sp.Integer(0)
    return sp.Integer(1)


for mode, coefficient in combined_fourier.items():
    require(
        canonical(sp.Matrix(mode).dot(coefficient)) == 0,
        "combined Fourier divergence",
    )

combined_strain: dict[Frequency, sp.Matrix] = {}
for mode, coefficient in combined_fourier.items():
    mode_matrix = sp.Matrix(mode)
    velocity = scale_vector(
        I / frequency_square(mode), mode_matrix.cross(coefficient)
    )
    combined_strain[mode] = I / 2 * (
        outer(mode_matrix, velocity) + outer(velocity, mode_matrix)
    )

combined_defect: defaultdict[Frequency, sp.Matrix] = defaultdict(
    lambda: sp.zeros(3, 3)
)
for first_mode, second_mode in product(combined_fourier, repeat=2):
    kernel = combined_response_kernel(
        combined_label[first_mode], combined_label[second_mode]
    )
    if kernel != 0:
        combined_defect[add_frequency(first_mode, second_mode)] += (
            kernel
            * outer(combined_fourier[first_mode], combined_fourier[second_mode])
        )

combined_contributions: list[dict[str, object]] = []
combined_signed_work = sp.S.Zero
for mode, strain_coefficient in sorted(combined_strain.items()):
    defect_coefficient = combined_defect.get(
        negative_frequency(mode), sp.zeros(3, 3)
    )
    contribution = frobenius(strain_coefficient, defect_coefficient)
    combined_signed_work = canonical(combined_signed_work + contribution)
    if contribution != 0:
        combined_contributions.append(
            {
                "strainMode": list(mode),
                "strainFamily": combined_label[mode][0],
                "contribution": scalar_payload(contribution),
            }
        )

combined_expected = canonical(
    -sp.Rational(81, 32780)
    * (62 + 1639 * physical_kappa)
    * Lambda**3
)
combined_residual = canonical(combined_signed_work - combined_expected)
combined_polynomial = sp.Poly(combined_signed_work, Lambda)

gradient_square = sp.S.Zero
for mode, coefficient in combined_fourier.items():
    coefficient_norm = sum(
        sp.conjugate(entry) * entry for entry in coefficient
    )
    gradient_square += frequency_square(mode) * coefficient_norm
gradient_square = canonical(gradient_square)
gradient_expected = 1188 * Lambda**2 + 20605

require(len(combined_fourier) == 40, "40 vorticity modes")
require(len(combined_defect) == 376, "376 defect outputs")
require(combined_residual == 0, "combined Fourier signed work")
require(combined_polynomial.coeff_monomial(Lambda**2) == 0, "no quadratic mixed work")
require(combined_polynomial.coeff_monomial(Lambda) == 0, "no linear mixed work")
require(combined_polynomial.coeff_monomial(1) == 0, "no filler-only work")
require(canonical(gradient_square - gradient_expected) == 0, "combined gradient norm")


payload = {
    "release": "R0.70Y",
    "status": "response-slope-besov-and-top-eigenvalue-gate",
    "checks": {
        "responseSlopeIdentities": True,
        "radialFrameGramAreaObstruction": True,
        "scalePacketArithmetic": True,
        "fillerCovarianceTopEigenvalue": True,
        "principalEigengapBoundary": True,
        "fortyModeFourierReconstruction": True,
    },
    "responseLedger": {
        "slopeDefinition": "d_n=(V(p)-V(q))/|n| and cyclically",
        "betaDefinition": "beta_j=(1/2)*||d_j||_ell2^2",
        "weightedClosure": "|n|d_n+|p|d_p+|q|d_q=0",
        "twoLegResidual": scalar_payload(response_block - two_leg_form),
        "symmetricResidual": scalar_payload(response_block - symmetric_form),
        "metricResponseSplit": "beta_n-beta_p=((x_n+x_p)/2)<V(q),V(n)-V(p)>+((x_n-x_p)/2)(K_n+K_p)",
        "metricResponseResidual": scalar_payload(metric_split_residual),
        "wedgeNormResidual": scalar_payload(wedge_norm_residual),
        "gramTraceResidual": scalar_payload(gram_trace_residual),
        "diagnosis": "the response-difference term and inverse-square metric term are algebraically distinct",
    },
    "gramAreaFamilyLedger": {
        "parameterPremise": "integer M>=4",
        "n": vector_payload(family_n),
        "p": vector_payload(family_p),
        "q": vector_payload(family_q),
        "c": vector_payload(family_c),
        "a": vector_payload(family_a),
        "b": vector_payload(family_b),
        "radiusSquare": scalar_payload(family_R2),
        "A": [
            scalar_payload(family_A_n),
            scalar_payload(family_A_p),
            scalar_payload(family_A_q),
        ],
        "cyclicResidual": scalar_payload(family_cyclic),
        "responseK": [scalar_payload(entry) for entry in K_family],
        "affineResponseAreaSquare": scalar_payload(area_family),
        "responseGramDeterminant": scalar_payload(det_family),
        "cyclicBlock": scalar_payload(family_block),
        "cyclicBlockExpected": scalar_payload(family_expected),
        "conclusion": "neither the affine response area nor the three-response Gram determinant divides the cyclic block",
    },
    "besovLedger": {
        "theorem": "|E_S|<=C_phi*sum_j||Delta_j omega||_3^3=C_phi*||omega||_(B^0_(3,3))^3",
        "mixedTheorem": "|E_S|<=C_phi*||omega||_(B^0_(infinity,infinity))*||omega||_2^2",
        "HHLNormalizedSymbol": "M_(kJJ)=delta*Mtilde_delta with uniformly bounded normalized derivatives and delta=2^(k-J)",
        "derivativeBound": "all fixed normalized symbol derivatives are O_phi(2^(k-J))",
        "periodicKernel": "compact normalized inverse kernel has L1(T^6)=O_phi(2^(k-J)) after periodization",
        "sequenceKernel": "h_m=2^(-m)*1_(m>=L) belongs to ell1",
        "ordinaryL3Relation": "sum_j||Delta_j omega||_3^3<=C||omega||_3^3",
        "analyticDependency": "the theorem uses smooth response-vector derivative bounds, periodic kernel transference, and finite-overlap LP square-function estimates",
    },
    "sharpnessLedger": {
        "packet": "W_N=sum_(r=r0)^(r0+N-1) W(64^r x), with fixed r0 beyond the inhomogeneous low block",
        "supportRadiiSquared": [5, 110, 149],
        "scale": int(packet_scale),
        "oneTopSquaredSlack": scalar_payload(one_top_slack),
        "twoTopSquaredSlack": scalar_payload(two_top_slack),
        "responseShift": "64=2^6 shifts the dyadic response index and preserves K",
        "signedWork": "E_S(W_N)=N*E_S(W)",
        "besovGrowth": "||W_N||_(B^0_(3,q)) is comparable to N^(1/q)",
        "contradiction": "q>3 would require N<=C*N^(3/q)",
        "conclusion": "q=3 is sharp within symmetric B^0_(3,q) cubic estimates",
    },
    "fillerLedger": {
        "field": "omega_Lambda=Lambda*xi+e2*(cos(49*x1)+sin(197*x1))",
        "radiiSquared": [5, 110, 149, int(filler_m**2), int(filler_n**2)],
        "strictFactorFourSquaredSlacks": [
            scalar_payload(filler_first_slack),
            scalar_payload(filler_second_slack),
        ],
        "covariance": "Q_Lambda=Lambda^2*q*w tensor w+h*e2 tensor e2",
        "h": "cos(49*x1)^2+sin(197*x1)^2",
        "zeroSetLemma": "nearest-zero distances a,b obey 197*a+49*b>=pi/2 after frequency normalization",
        "uniformLowerBound": "h>=1/(49^2+197^2)=1/41210",
        "topEigenvalue": "lambda_1(Q_Lambda)>=1/41210 for every Lambda>0",
        "covarianceAreaResidual": scalar_payload(covariance_area_residual),
        "covarianceArea": "G_Q^2=Lambda^2*q*h*|w cross e2|^2",
        "gradientSquare": scalar_payload(gradient_square),
        "gradientSquareExpected": scalar_payload(gradient_expected),
    },
    "eigengapLedger": {
        "curve": "x(A)=(A/3,2*A/3,A/3)",
        "axialPhaseResidual": scalar_payload(curve_z_residual),
        "oldFieldResidual": vector_payload(curve_w_residual),
        "covarianceScalarFromFrame": scalar_payload(curve_q_from_frame),
        "oldEigenvalue": scalar_payload(curve_X),
        "fillerEigenvalue": "h(A/3)",
        "signChange": "for Lambda>=1, X-h is -1 at A=0 and at least 7 at A=pi/6",
        "consequence": "for every Lambda>=1 some A_Lambda has lambda_1=lambda_2>0",
        "explicitLambda": scalar_payload(explicit_Lambda),
        "explicitPoint": ["pi/6", "pi/3", "pi/6"],
        "explicitOldEigenvalue": scalar_payload(explicit_X),
        "explicitFillerEigenvalue": scalar_payload(explicit_h),
        "boundary": "no absolute or relative principal eigengap is asserted",
    },
    "fourierLedger": {
        "modeCount": len(combined_fourier),
        "defectOutputCount": len(combined_defect),
        "nonzeroSignedContributionCount": len(combined_contributions),
        "signedWork": scalar_payload(combined_signed_work),
        "signedWorkExpected": scalar_payload(combined_expected),
        "difference": scalar_payload(combined_residual),
        "LambdaPowers": {
            str(power): scalar_payload(combined_polynomial.coeff_monomial(Lambda**power))
            for power in (3, 2, 1, 0)
        },
        "oldFieldDependency": "the 36 old modes and kappa response are imported from the archived R0.70X producer",
    },
    "analyticDependencies": [
        "the complete scalar frame is real, even, radial, smooth, Parseval, dyadic, and strictly supported in 1/2<|xi|<2",
        "the B^0_(3,3) and mixed B^0_(infinity,infinity)-L2 bounds use a separate periodic Coifman--Meyer and Littlewood--Paley proof in the report",
        "the q=3 lower bound uses an auxiliary fixed smooth inhomogeneous Littlewood--Paley decomposition whose macro-scale supports are disjoint",
        "the h lower bound uses the zero-set parity lemma plus sin(y)>=2y/pi on [0,pi/2]",
        "continuity on the explicit curve supplies eigengap degeneracy for every Lambda>=1",
        "the exact Fourier producer verifies the signed-work polynomial but not any infinite-dimensional functional-analytic estimate",
    ],
    "claimBoundary": [
        "proves exact response-chord, metric/response, wedge-norm, and Gram-trace identities",
        "rules out affine response area and three-response Gram determinant as universal factors of the cyclic block",
        "supports a log-free critical B^0_(3,3) cyclic defect estimate and a B^0_(infinity,infinity)-L2 mixed estimate, conditional only on the analytic lemmas written in the report",
        "proves q=3 is sharp only within the symmetric B^0_(3,q) cubic family",
        "rules out a uniform positive top covariance eigenvalue as a repair of the old G_Q candidate",
        "does not rule out an estimate under a uniformly positive principal eigengap",
        "does not control the principal covariance stretching integral S:Q",
        "does not prove an enstrophy closure, continuation criterion, singularity, global regularity, or solve the Millennium problem",
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
