#!/usr/bin/env python3
"""Exact finite/symbolic audit for the R0.70V response-distance gate.

The producer checks six narrowly scoped groups:

1. finite-dimensional Gram chord/area identities;
2. the two-shell exact-rank full-tensor counterexample;
3. the strain-projected homogeneous H^{-1} constants and equality anchor;
4. the R0.70U projected-defect critical-order subtotal;
5. the exact divergence-free triad-area identity; and
6. the algebraic expansion used in the narrow radial-band proof.

The infinite Parseval-frame reconstruction, arbitrary-cutoff radial Lipschitz
bound, mode-count-independent operator estimate, shell summation, and every
Navier--Stokes continuation statement are analytic arguments in the report.
They are not inferred from this finite certificate.  Nothing here proves an
enstrophy closure, singularity, global regularity, or a solution of the
Millennium problem.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def canonical(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.expand(expression)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def outer(first: sp.Matrix, second: sp.Matrix | None = None) -> sp.Matrix:
    if second is None:
        second = first
    return first * second.T


def contract(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return canonical(
        sum(
            (first[row, column] * second[row, column] for row in range(3) for column in range(3)),
            sp.S.Zero,
        )
    )


def squared_norm(vector: sp.Matrix) -> sp.Expr:
    return canonical(vector.dot(vector))


def frobenius_squared(matrix: sp.Matrix) -> sp.Expr:
    return canonical(
        sum((entry**2 for entry in matrix), sp.S.Zero)
    )


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(canonical(entry) == 0 for entry in matrix)


def scalar_payload(expression: sp.Expr) -> str:
    return str(canonical(expression))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [scalar_payload(entry) for entry in vector]


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [scalar_payload(matrix[row, column]) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])


# ---------------------------------------------------------------------------
# 1. Gram chord and response-area algebra.
# ---------------------------------------------------------------------------

x_symbols = sp.symbols("x0:3", real=True)
y_symbols = sp.symbols("y0:3", real=True)
x_response = sp.Matrix(x_symbols)
y_response = sp.Matrix(y_symbols)

norm_x = squared_norm(x_response)
norm_y = squared_norm(y_response)
gamma_xy = canonical(x_response.dot(y_response))
distance_squared = squared_norm(x_response - y_response)
kernel_unconstrained = canonical(1 - gamma_xy)
unit_constraint_remainder = canonical(
    kernel_unconstrained
    - distance_squared / 2
    - ((1 - norm_x) + (1 - norm_y)) / 2
)

wedge_square = canonical(
    sum(
        (
            x_response[first] * y_response[second]
            - x_response[second] * y_response[first]
        )
        ** 2
        for first in range(3)
        for second in range(first + 1, 3)
    )
)
wedge_lagrange_residual = canonical(
    wedge_square - (norm_x * norm_y - gamma_xy**2)
)

gamma = sp.symbols("gamma", real=True)
d = canonical(1 - gamma)
kappa = canonical(1 - gamma**2)
chord_area_residual = canonical(kappa - d * (1 + gamma))
ratio_square_residual = canonical(
    d**2 - kappa * (1 - gamma) / (1 + gamma)
)
gamma_plus_d = canonical(d.subs(gamma, 1))
gamma_plus_kappa = canonical(kappa.subs(gamma, 1))
gamma_minus_d = canonical(d.subs(gamma, -1))
gamma_minus_kappa = canonical(kappa.subs(gamma, -1))

require(unit_constraint_remainder == 0, "unit-response chord identity")
require(wedge_lagrange_residual == 0, "response wedge Lagrange identity")
require(chord_area_residual == 0, "chord-area factorization")
require(ratio_square_residual == 0, "chord-area ratio square")
require(gamma_plus_d == 0 and gamma_plus_kappa == 0, "gamma=1 endpoint")
require(gamma_minus_d == 2 and gamma_minus_kappa == 0, "gamma=-1 endpoint")


# ---------------------------------------------------------------------------
# 2. Two-shell exact-rank full-tensor counterexample.
# ---------------------------------------------------------------------------

A, B, N = sp.symbols("A B N", nonzero=True, real=True)
x = sp.symbols("x", real=True)

trigonometric_residual = sp.simplify(
    sp.expand_trig(
        2 * sp.cos(x) * sp.cos(4 * x) - sp.cos(3 * x) - sp.cos(5 * x)
    )
)
require(trigonometric_residual == 0, "two-shell product-to-sum")

E33 = outer(e3)
D3 = A * B / 2 * E33
D5 = A * B / 2 * E33
hdot_minus_one_squared = canonical(
    2 * frobenius_squared(D3) / (3 * N) ** 2
    + 2 * frobenius_squared(D5) / (5 * N) ** 2
)
hdot_minus_one_expected = canonical(17 * A**2 * B**2 / (225 * N**2))
require(
    canonical(hdot_minus_one_squared - hdot_minus_one_expected) == 0,
    "two-shell homogeneous H^-1 norm",
)

projected_D3 = e1.cross(D3 * e1)
projected_D5 = e1.cross(D5 * e1)
two_shell_projected_defect = canonical(
    2 * squared_norm(projected_D3) / (3 * N) ** 2
    + 2 * squared_norm(projected_D5) / (5 * N) ** 2
)
require(two_shell_projected_defect == 0, "two-shell strain projection null")

s12 = sp.symbols("s12", real=True)
shear_strain = s12 * (outer(e1, e2) + outer(e2, e1))
two_shell_tensor = sp.symbols("d33", real=True) * E33
two_shell_contraction = contract(shear_strain, two_shell_tensor)
require(two_shell_contraction == 0, "two-shell shear contraction null")


# ---------------------------------------------------------------------------
# 3. Strain projection, Frobenius constant, and simultaneous equality anchor.
# ---------------------------------------------------------------------------

d11, d22, d33, d12, d13, d23 = sp.symbols(
    "d11 d22 d33 d12 d13 d23", real=True
)
generic_symmetric = sp.Matrix(
    [
        [d11, d12, d13],
        [d12, d22, d23],
        [d13, d23, d33],
    ]
)
generic_projection_square = squared_norm(e1.cross(generic_symmetric * e1))
generic_frobenius_square = frobenius_squared(generic_symmetric)
projection_slack = canonical(
    generic_frobenius_square - 2 * generic_projection_square
)
projection_slack_expected = canonical(d11**2 + d22**2 + d33**2 + 2 * d23**2)
require(
    canonical(projection_slack - projection_slack_expected) == 0,
    "ambient symmetric Frobenius constant",
)

sym13 = outer(e1, e3) + outer(e3, e1)
omega_plus = e2 / 2
omega_minus = e2 / 2
D_plus = -sym13 / 2
D_minus = -sym13 / 2
S_plus = -sym13 / 4
S_minus = -sym13 / 4

anchor_work = canonical(contract(S_plus, D_minus) + contract(S_minus, D_plus))
anchor_palinstrophy = canonical(squared_norm(omega_plus) + squared_norm(omega_minus))
anchor_projected = canonical(
    squared_norm(e1.cross(D_plus * e1))
    + squared_norm(e1.cross(D_minus * e1))
)
anchor_hdot_minus_one = canonical(
    frobenius_squared(D_plus) + frobenius_squared(D_minus)
)

require(anchor_work == sp.Rational(1, 2), "ambient work equality anchor")
require(anchor_palinstrophy == sp.Rational(1, 2), "ambient palinstrophy anchor")
require(anchor_projected == sp.Rational(1, 2), "ambient projected anchor")
require(anchor_hdot_minus_one == 1, "ambient homogeneous H^-1 anchor")
require(
    canonical(anchor_work**2 - anchor_palinstrophy * anchor_projected) == 0,
    "Cauchy equality anchor",
)
require(
    canonical(anchor_projected - anchor_hdot_minus_one / 2) == 0,
    "Frobenius equality anchor",
)


# ---------------------------------------------------------------------------
# 4. R0.70U projected critical subtotal and exact defect factorization.
# ---------------------------------------------------------------------------

m = sp.symbols("m", integer=True, positive=True)
delta, epsilon = sp.symbols("delta epsilon", real=True)
a_pythagorean = m**2 - 1
b_pythagorean = 2 * m
K_pythagorean = m**2 + 1
unit_k = sp.Matrix([a_pythagorean, b_pythagorean, 0]) / K_pythagorean
U_D_at_k = delta / 4 * (outer(e3, e2) + outer(e2, e3))
U_output_k_subtotal = canonical(
    2
    * squared_norm(unit_k.cross(U_D_at_k * unit_k))
    / K_pythagorean**2
)
U_output_k_expected = canonical(
    delta**2 * m**2 / (2 * (m**2 + 1) ** 4)
)
require(
    canonical(U_output_k_subtotal - U_output_k_expected) == 0,
    "R0.70U projected +/-k subtotal",
)

w_symbols = sp.symbols("w0:3", real=True)
h_symbols = sp.symbols("h0:3", real=True)
w = sp.Matrix(w_symbols)
h_vector = sp.Matrix(h_symbols)
physical_tensor = outer(w + epsilon * h_vector)
frame_tensor = (
    outer(w)
    + epsilon * gamma * (outer(w, h_vector) + outer(h_vector, w))
    + epsilon**2 * outer(h_vector)
)
expected_frame_defect = epsilon * (1 - gamma) * (
    outer(w, h_vector) + outer(h_vector, w)
)
frame_defect_residual = (
    physical_tensor - frame_tensor - expected_frame_defect
).applyfunc(canonical)
require(matrix_is_zero(frame_defect_residual), "R0.70U exact frame defect")

theta = sp.symbols("theta", real=True)
residual_ratio_power = canonical(1 - 2 * theta)


# ---------------------------------------------------------------------------
# 5. Exact divergence-free triad-area identity.
# ---------------------------------------------------------------------------

nmag = sp.symbols("nmag", positive=True, real=True)
kx, ky, kz = sp.symbols("kx ky kz", real=True)
au0, au1, au2 = sp.symbols("au0 au1 au2", real=True)
bu0, bu1, bu2 = sp.symbols("bu0 bu1 bu2", real=True)
c2, c3 = sp.symbols("c2 c3", real=True)

n_vector = nmag * e1
k_vector = sp.Matrix([kx, ky, kz])
l_vector = -n_vector - k_vector
a_vector = k_vector.cross(sp.Matrix([au0, au1, au2]))
b_vector = l_vector.cross(sp.Matrix([bu0, bu1, bu2]))
c_vector = sp.Matrix([0, c2, c3])
z_vector = e1.cross(c_vector)
strain_c = -(outer(e1, z_vector) + outer(z_vector, e1)) / 2
polarized_pair = outer(a_vector, b_vector) + outer(b_vector, a_vector)
triad_left = contract(strain_c, polarized_pair)
triad_right = canonical(
    (l_vector - k_vector).cross(z_vector).dot(a_vector.cross(b_vector))
    / nmag
)
triad_identity_residual = canonical(triad_left - triad_right)

require(canonical(k_vector.dot(a_vector)) == 0, "triad k divergence")
require(canonical(l_vector.dot(b_vector)) == 0, "triad l divergence")
require(canonical(n_vector.dot(c_vector)) == 0, "triad n divergence")
require(triad_identity_residual == 0, "exact triad-area identity")

space_dimension = sp.Integer(3)
vorticity_scaling_degree = sp.Integer(2)
defect_scaling_degree = 2 * vorticity_scaling_degree
whole_space_X_degree = canonical(
    2 * defect_scaling_degree - 2 - space_dimension
)
whole_space_area_degree = canonical(
    2 * defect_scaling_degree - space_dimension
)
fixed_torus_X_degree = canonical(2 * defect_scaling_degree - 2)
fixed_torus_area_degree = canonical(2 * defect_scaling_degree)
whole_space_degree_gap = canonical(
    whole_space_area_degree - whole_space_X_degree
)
fixed_torus_degree_gap = canonical(
    fixed_torus_area_degree - fixed_torus_X_degree
)
require(whole_space_X_degree == 3, "whole-space X scaling degree")
require(whole_space_area_degree == 5, "whole-space area scaling degree")
require(whole_space_degree_gap == 2, "whole-space scaling gap")
require(fixed_torus_X_degree == 6, "fixed-torus X scaling degree")
require(fixed_torus_area_degree == 8, "fixed-torus area scaling degree")
require(fixed_torus_degree_gap == 2, "fixed-torus scaling gap")


# ---------------------------------------------------------------------------
# 6. Narrow-band algebraic expansion and unit-sphere quadratic gain.
# ---------------------------------------------------------------------------

c0, c1 = sp.symbols("c0 c1", real=True)
omega_symbols = sp.symbols("omega0:3", real=True)
err0_symbols = sp.symbols("err0_0:3", real=True)
err1_symbols = sp.symbols("err1_0:3", real=True)
omega_vector = sp.Matrix(omega_symbols)
error0 = sp.Matrix(err0_symbols)
error1 = sp.Matrix(err1_symbols)
g_vector = c0 * error0 + c1 * error1

expanded_Q = (
    outer(c0 * omega_vector + error0)
    + outer(c1 * omega_vector + error1)
)
narrow_defect = outer(omega_vector) - expanded_Q
narrow_expected = (
    -outer(omega_vector, g_vector)
    - outer(g_vector, omega_vector)
    - outer(error0)
    - outer(error1)
)
narrow_constraint_residual = (
    narrow_defect
    - narrow_expected
    - (1 - c0**2 - c1**2) * outer(omega_vector)
).applyfunc(canonical)
require(matrix_is_zero(narrow_constraint_residual), "narrow-band expansion")

response_gamma = sp.symbols("response_gamma", real=True)
response_distance_square = canonical(2 - 2 * response_gamma)
g_symbol = canonical(response_gamma - 1)
unit_sphere_quadratic_residual = canonical(
    g_symbol + response_distance_square / 2
)
require(unit_sphere_quadratic_residual == 0, "unit-sphere quadratic g symbol")


payload = {
    "release": "R0.70V",
    "status": "response-distance-and-strain-projection-exact-audit",
    "checks": {
        "gramChordArea": True,
        "twoShellExactRank": True,
        "strainProjection": True,
        "uFamilyCriticalSubtotal": True,
        "triadAreaIdentity": True,
        "narrowBandAlgebra": True,
    },
    "gramLedger": {
        "unitConstraintRemainder": scalar_payload(unit_constraint_remainder),
        "wedgeLagrangeResidual": scalar_payload(wedge_lagrange_residual),
        "chordAreaResidual": scalar_payload(chord_area_residual),
        "ratioSquareResidual": scalar_payload(ratio_square_residual),
        "ratioPremise": "-1<gamma<1; the quotient is not defined at either endpoint",
        "gammaPlusEndpoint": {
            "d": scalar_payload(gamma_plus_d),
            "kappa": scalar_payload(gamma_plus_kappa),
            "reading": "0/0 ratio is undefined; the frame-defect pair itself vanishes",
        },
        "gammaMinusEndpoint": {
            "d": scalar_payload(gamma_minus_d),
            "kappa": scalar_payload(gamma_minus_kappa),
            "reading": "response chord is nonzero while covariance area vanishes",
        },
        "kernel": "1 - gamma = (1/2)||V(p)-V(q)||_ell2^2 for unit responses",
        "area": "1 - gamma^2 = sum_{alpha<beta}|Vp_alpha Vq_beta - Vp_beta Vq_alpha|^2",
        "antiCorrelationBoundary": "1+gamma>=sigma>0 is required to bound chord by response area",
    },
    "twoShellLedger": {
        "field": "omega=e3*(A*cos(N*x1)+B*cos(4*N*x1))",
        "responseSupport": "strict annular support makes the radius-N and radius-4N index sets disjoint",
        "covariance": "Q=e3 tensor e3*(A^2*cos(N*x1)^2+B^2*cos(4*N*x1)^2)",
        "topGapBoundary": "cos(N*x1)=0 implies cos(4*N*x1)=1, so Q is globally positive rank one",
        "residual": "r identically 0",
        "trigonometricResidual": scalar_payload(trigonometric_residual),
        "defect": "A*B*(cos(3*N*x1)+cos(5*N*x1))*e3 tensor e3",
        "hdotMinusOneSquared": scalar_payload(hdot_minus_one_squared),
        "hdotMinusOneExpected": scalar_payload(hdot_minus_one_expected),
        "strainProjection": scalar_payload(two_shell_projected_defect),
        "shearContraction": scalar_payload(two_shell_contraction),
    },
    "strainLedger": {
        "projectionSquare": scalar_payload(generic_projection_square),
        "frobeniusMinusTwiceProjection": scalar_payload(projection_slack),
        "expectedNonnegativeSlack": scalar_payload(projection_slack_expected),
        "ambientEqualityField": "omega=e2*cos(x1), D=-cos(x1)*(e1 tensor e3+e3 tensor e1)",
        "workAbsolute": scalar_payload(anchor_work),
        "palinstrophy": scalar_payload(anchor_palinstrophy),
        "projectedDefect": scalar_payload(anchor_projected),
        "hdotMinusOneFrobenius": scalar_payload(anchor_hdot_minus_one),
        "cauchyEqualityResidual": scalar_payload(
            anchor_work**2 - anchor_palinstrophy * anchor_projected
        ),
        "frobeniusEqualityResidual": scalar_payload(
            anchor_projected - anchor_hdot_minus_one / 2
        ),
        "sharpnessScope": "ambient symmetric tensor class only; not certified inside D=D_cross(omega)",
    },
    "criticalLedger": {
        "parameterPremise": "inherits the locked R0.70U integer m>=2, fixed A>delta>0, and |gamma|<=3/4 family",
        "exactFrameDefectResidual": matrix_payload(frame_defect_residual),
        "uPlusMinusKSubtotal": scalar_payload(U_output_k_subtotal),
        "uPlusMinusKExpected": scalar_payload(U_output_k_expected),
        "uProjectedReading": "X_epsilon>=epsilon^2*(1-gamma)^2*delta^2*m^2/[2*(m^2+1)^4]",
        "orders": {
            "r": "epsilon^2",
            "X": "epsilon^2",
            "sqrtX": "abs(epsilon)",
            "signedWork": "epsilon",
        },
        "ordersSource": "X is checked here from the exact defect and positive +/-k subtotal; r and signedWork are inherited from the locked R0.70U theorem",
        "residualThetaRatioPower": scalar_payload(residual_ratio_power),
    },
    "triadLedger": {
        "frequencyConstraint": "n+k+l=0",
        "divergenceResiduals": [
            scalar_payload(k_vector.dot(a_vector)),
            scalar_payload(l_vector.dot(b_vector)),
            scalar_payload(n_vector.dot(c_vector)),
        ],
        "identityResidual": scalar_payload(triad_identity_residual),
        "identity": "S_c:(a tensor b+b tensor a)=[(l-k)x(nu_n x c)] dot (a x b)/|n|",
        "pairwiseBound": "absolute value <=[(|k|+|l|)/|n|]*|c|*|a x b|",
        "responseWeightedConstant": "K(k,l)(|k|+|l|)/|k+l| <= 2+2*M_phi",
        "areaWeightedBoundary": "with 1+Gamma>=sigma, coefficient <=sqrt(2)*(1+M_phi)/sqrt(sigma)",
    },
    "scalingLedger": {
        "premise": "dyadic mu=2^J, so the pinned homogeneous frame changes only by an index shift",
        "wholeSpaceXDegree": scalar_payload(whole_space_X_degree),
        "wholeSpaceAreaIntegralDegree": scalar_payload(
            whole_space_area_degree
        ),
        "wholeSpaceDegreeGap": scalar_payload(whole_space_degree_gap),
        "fixedTorusXDegree": scalar_payload(fixed_torus_X_degree),
        "fixedTorusAreaIntegralDegree": scalar_payload(
            fixed_torus_area_degree
        ),
        "fixedTorusDegreeGap": scalar_payload(fixed_torus_degree_gap),
        "reading": "the raw X-to-covariance-area comparator is two inverse-frequency degrees short",
    },
    "narrowBandLedger": {
        "expansionConstraintResidual": matrix_payload(narrow_constraint_residual),
        "unitSphereQuadraticResidual": scalar_payload(
            unit_sphere_quadratic_residual
        ),
        "operatorReading": "sum||e_alpha||_2^2<=beta^2||omega||_2^2 and ||g||_2<=beta^2||omega||_2/2",
        "finalAnalyticConstant": "min(2,2*M_phi^2*delta^2)*||omega||_2^2",
    },
    "analyticDependencies": [
        "the star=Pi_0 block is retained when the complete frame acts on omega tensor omega",
        "infinite-frame reconstruction and the L2-to-L1 passage are analytic, not finite symbolic checks",
        "the radial log-Lipschitz bound uses a smooth real-even radial exact tight cutoff",
        "the global simple top gap in the two-shell sample uses the analytic fact that the two cosines never vanish together",
        "the U-family X subtotal proves positivity but does not calculate every nonnegative output contribution",
        "the response-weighted triad constants use scalar inequalities in the report and are not optimized here",
        "no vector-valued shell summation or time-integrated estimate is certified",
    ],
    "claimBoundary": [
        "proves no estimate X_cross<=C*r",
        "proves no a priori time integrability of X_cross",
        "does not control the principal covariance stretching integral S:Q",
        "does not propagate narrow radial support or covariance rank",
        "does not prove an enstrophy closure or continuation criterion",
        "does not prove a singularity, unconditional global regularity, or solve the Millennium problem",
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
