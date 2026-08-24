#!/usr/bin/env python3
"""Exact audit for the R0.70S energy-level palinstrophy-majorant gate.

The producer certifies four finite/symbolic groups:

1. a two-frequency rotating shear that is an exact global heat solution of
   the unforced periodic Navier--Stokes equations, together with its two
   disjoint tight Littlewood--Paley blocks;
2. the exact covariance polynomial and endpoint slacks used by the analytic
   simple-gap/near-rank implications, plus a positive majorant point;
3. displayed-field pullback residuals, the Fourier multiplier-argument
   shift, and conditional scale-factor arithmetic for energy, residual,
   complete-frame commutator, direction cost, and the majorant; and
4. the exponent contradiction for A_N=N**(1/4), including the diverging
   initial enstrophy that limits the no-go claim.

All evaluated arithmetic is exact SymPy arithmetic.  The commutator entry
checks conditional scale-factor arithmetic, including the Pi_0 term in the
stated analytic lifting lemma; it does not evaluate the multiplier-dependent
base constant in closed form.  The
certificate concerns a positive coefficient-level majorant, not the signed
diffusion deficit.  It does not prove singularity or close a PDE estimate.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def matrix_is_zero(matrix: sp.Matrix) -> bool:
    return all(sp.simplify(entry) == 0 for entry in matrix)


def matrix_equal(first: sp.Matrix, second: sp.Matrix) -> bool:
    return first.shape == second.shape and matrix_is_zero(first - second)


def scalar_payload(value: sp.Expr) -> str:
    return str(sp.factor(value))


def vector_payload(vector: sp.Matrix) -> list[str]:
    return [str(sp.factor(entry)) for entry in vector]


def matrix_payload(matrix: sp.Matrix) -> list[list[str]]:
    return [
        [str(sp.factor(matrix[row, column])) for column in range(matrix.cols)]
        for row in range(matrix.rows)
    ]


def norm_squared(vector: sp.Matrix) -> sp.Expr:
    return sp.simplify((sp.conjugate(vector).T * vector)[0])


def divergence(
    vector: sp.Matrix, coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> sp.Expr:
    return sp.simplify(
        sum(sp.diff(vector[index], coordinates[index]) for index in range(3))
    )


def curl(
    vector: sp.Matrix, coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> sp.Matrix:
    x1, x2, x3 = coordinates
    return sp.Matrix(
        [
            sp.diff(vector[2], x2) - sp.diff(vector[1], x3),
            sp.diff(vector[0], x3) - sp.diff(vector[2], x1),
            sp.diff(vector[1], x1) - sp.diff(vector[0], x2),
        ]
    ).applyfunc(sp.expand)


def laplacian(
    vector: sp.Matrix, coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol]
) -> sp.Matrix:
    return sp.Matrix(
        [
            sum(sp.diff(component, coordinate, 2) for coordinate in coordinates)
            for component in vector
        ]
    ).applyfunc(sp.expand)


def advective_derivative(
    velocity: sp.Matrix,
    vector: sp.Matrix,
    coordinates: tuple[sp.Symbol, sp.Symbol, sp.Symbol],
) -> sp.Matrix:
    return sp.Matrix(
        [
            sum(
                velocity[index] * sp.diff(component, coordinates[index])
                for index in range(3)
            )
            for component in vector
        ]
    ).applyfunc(sp.simplify)


def normalized_average_1d(expression: sp.Expr, coordinate: sp.Symbol) -> sp.Expr:
    return sp.simplify(
        sp.integrate(expression, (coordinate, 0, 2 * sp.pi)) / (2 * sp.pi)
    )


# ---------------------------------------------------------------------------
# 1. Two rotating shear modes and the disjoint tight-frame ledger.
# ---------------------------------------------------------------------------

x1, x2, x3, t = sp.symbols("x1 x2 x3 t", real=True)
coordinates = (x1, x2, x3)
nu, amplitude = sp.symbols("nu A_N", positive=True, real=True)
frequency = sp.symbols("N", positive=True, integer=True)
M = sp.Integer(16)

low_decay = sp.exp(-nu * frequency**2 * t)
high_decay = sp.exp(-nu * M**2 * frequency**2 * t)
v_low = sp.Matrix(
    [0, sp.cos(frequency * x1), sp.sin(frequency * x1)]
)
w_high = sp.Matrix(
    [0, sp.sin(M * frequency * x1), sp.cos(M * frequency * x1)]
)

velocity = (
    amplitude
    / frequency
    * (-low_decay * v_low + high_decay * w_high / M**2)
)
omega_low = amplitude * low_decay * v_low
omega_high = amplitude * high_decay * w_high / M
vorticity = omega_low + omega_high

require(divergence(velocity, coordinates) == 0, "velocity divergence")
require(divergence(vorticity, coordinates) == 0, "vorticity divergence")
require(
    matrix_is_zero(curl(v_low, coordinates) + frequency * v_low),
    "low curl eigenmode",
)
require(
    matrix_is_zero(curl(w_high, coordinates) - M * frequency * w_high),
    "high curl eigenmode",
)
require(
    matrix_is_zero(sp.diff(v_low, x1, 2) + frequency**2 * v_low),
    "low Laplace eigenmode",
)
require(
    matrix_is_zero(
        sp.diff(w_high, x1, 2) + M**2 * frequency**2 * w_high
    ),
    "high Laplace eigenmode",
)
require(
    sp.simplify(sp.diff(low_decay, t) + nu * frequency**2 * low_decay)
    == 0,
    "low heat decay",
)
require(
    sp.simplify(
        sp.diff(high_decay, t)
        + nu * M**2 * frequency**2 * high_decay
    )
    == 0,
    "high heat decay",
)
curl_residual = (
    curl(velocity, coordinates) - vorticity
).applyfunc(sp.expand)
heat_residual = (
    sp.diff(velocity, t) - nu * laplacian(velocity, coordinates)
).applyfunc(sp.expand)
vorticity_heat_residual = (
    sp.diff(vorticity, t) - nu * laplacian(vorticity, coordinates)
).applyfunc(sp.expand)
require(matrix_is_zero(curl_residual), "full field curl residual")
require(matrix_is_zero(heat_residual), "full velocity heat residual")
require(
    matrix_is_zero(vorticity_heat_residual),
    "full vorticity heat residual",
)
nonlinearity = advective_derivative(velocity, velocity, coordinates)
require(matrix_is_zero(nonlinearity), "shear nonlinearity")

mean_vorticity = sp.Matrix(
    [normalized_average_1d(component, x1) for component in vorticity]
)
require(matrix_is_zero(mean_vorticity), "mean-zero vorticity")

velocity_energy_zero = normalized_average_1d(
    norm_squared(velocity.subs(t, 0)), x1
)
enstrophy_zero = normalized_average_1d(
    norm_squared(vorticity.subs(t, 0)), x1
)
expected_velocity_energy_zero = sp.factor(
    amplitude**2 / frequency**2 * (1 + M ** (-4))
)
expected_enstrophy_zero = sp.factor(amplitude**2 * (1 + M ** (-2)))
require(
    sp.simplify(velocity_energy_zero - expected_velocity_energy_zero) == 0,
    "initial kinetic energy",
)
require(
    sp.simplify(enstrophy_zero - expected_enstrophy_zero) == 0,
    "initial enstrophy",
)

# If N=2**J and the annular support is strictly 1/2<|xi|/2**j<2,
# the dyadic boundary points are excluded and each exact dyadic frequency
# activates one index only.
low_offset_set = sp.Intersection(sp.Interval.open(-1, 1), sp.S.Integers)
high_offset_set = sp.Intersection(sp.Interval.open(3, 5), sp.S.Integers)
low_active_offsets = [int(value) for value in low_offset_set]
high_active_offsets = [int(value) for value in high_offset_set]
require(low_active_offsets == [0], "low active singleton")
require(high_active_offsets == [4], "high active singleton")
require(
    set(low_active_offsets).isdisjoint(high_active_offsets),
    "disjoint active index groups",
)
# This is an analytic implication from the pinned frame hypotheses, not a
# numerical evaluation of the unspecified multiplier profile: singleton
# support reduces exact tightness sum_j |phi_j(xi)|^2=1 to one response
# square.  The implication is recorded as a premise below, not disguised as
# a tautological finite computation.

# Tight response signs disappear from the covariance outer products.
covariance = omega_low * omega_low.T + omega_high * omega_high.T


# ---------------------------------------------------------------------------
# 2. Covariance spectrum, relative gap, near-rank ratio, and I_1 positivity.
# ---------------------------------------------------------------------------

alpha = sp.simplify(amplitude * low_decay)
beta = sp.simplify(amplitude * high_decay / M)
direction_dot = sp.trigsimp((v_low.T * w_high)[0], method="fu")
require(
    sp.trigsimp(
        direction_dot - sp.sin((M + 1) * frequency * x1), method="fu"
    )
    == 0,
    "rotating-direction dot product",
)

require(
    sp.trigsimp(norm_squared(v_low), method="fu") == 1,
    "low direction unit norm",
)
require(
    sp.trigsimp(norm_squared(w_high), method="fu") == 1,
    "high direction unit norm",
)
trace_energy = sp.trigsimp(sp.trace(covariance), method="fu")
expected_trace_energy = alpha**2 + beta**2
require(
    sp.expand(trace_energy - expected_trace_energy) == 0,
    "covariance trace",
)
require(
    all(covariance[0, index] == 0 for index in range(3))
    and all(covariance[index, 0] == 0 for index in range(3)),
    "rank at most two",
)

spectral_parameter = sp.symbols("mu")
# Certify the characteristic polynomial in the invariant two-direction
# coordinates v=e1, z=d*e1+h*e2, d^2+h^2=1.  This avoids expanding the
# harmless but very large angle 17*N*x1 into degree-17 trig polynomials.
abstract_alpha, abstract_beta, abstract_d, abstract_h = sp.symbols(
    "abstract_alpha abstract_beta abstract_d abstract_h", real=True
)
abstract_v = sp.Matrix([1, 0, 0])
abstract_z = sp.Matrix([abstract_d, abstract_h, 0])
abstract_Q = (
    abstract_alpha**2 * abstract_v * abstract_v.T
    + abstract_beta**2 * abstract_z * abstract_z.T
)
abstract_characteristic = sp.expand(
    abstract_Q.charpoly(spectral_parameter).as_expr()
)
expected_characteristic = sp.expand(
    spectral_parameter
    * (
        spectral_parameter**2
        - (abstract_alpha**2 + abstract_beta**2) * spectral_parameter
        + abstract_alpha**2 * abstract_beta**2 * (1 - abstract_d**2)
    )
)
characteristic_unit_slack = sp.factor(
    abstract_characteristic - expected_characteristic
)
expected_characteristic_unit_slack = sp.factor(
    abstract_beta**2
    * spectral_parameter
    * (abstract_alpha**2 - spectral_parameter)
    * (abstract_d**2 + abstract_h**2 - 1)
)
require(
    sp.simplify(
        characteristic_unit_slack - expected_characteristic_unit_slack
    )
    == 0,
    "covariance characteristic polynomial unit-vector slack",
)
characteristic_residual = sp.factor(
    characteristic_unit_slack.subs(
        abstract_h**2, 1 - abstract_d**2
    )
)
require(characteristic_residual == 0, "covariance characteristic polynomial")

gap_squared = (
    (alpha**2 - beta**2) ** 2
    + 4 * alpha**2 * beta**2 * direction_dot**2
)
abstract_gap_squared = (
    (abstract_alpha**2 - abstract_beta**2) ** 2
    + 4 * abstract_alpha**2 * abstract_beta**2 * abstract_d**2
)
gap_square_slack = sp.factor(
    abstract_gap_squared
    - (abstract_alpha**2 - abstract_beta**2) ** 2
)
require(
    sp.simplify(
        gap_square_slack
        - 4 * abstract_alpha**2 * abstract_beta**2 * abstract_d**2
    )
    == 0,
    "gap square slack",
)

q_ratio = sp.simplify(beta**2 / alpha**2)
q_initial = sp.simplify(q_ratio.subs(t, 0))
q_log_derivative = sp.simplify(sp.diff(q_ratio, t) / q_ratio)
require(q_initial == sp.Rational(1, M**2), "initial q ratio")
require(
    q_log_derivative == -2 * nu * (M**2 - 1) * frequency**2,
    "q monotonicity exponent",
)

q = sp.symbols("q", nonnegative=True, real=True)
relative_gap_endpoint = sp.Rational(M**2 - 1, M**2 + 1)
relative_gap_slack = sp.factor(
    (1 - q) / (1 + q) - relative_gap_endpoint
)
expected_relative_gap_slack = sp.factor(
    2 * (1 - M**2 * q) / ((M**2 + 1) * (1 + q))
)
require(
    sp.simplify(relative_gap_slack - expected_relative_gap_slack) == 0,
    "relative gap endpoint slack",
)

eta_upper = sp.factor(q / (1 + q))
eta_endpoint = sp.Rational(1, M**2 + 1)
eta_endpoint_slack = sp.factor(eta_endpoint - eta_upper)
expected_eta_endpoint_slack = sp.factor(
    (1 - M**2 * q) / ((M**2 + 1) * (1 + q))
)
require(
    sp.simplify(eta_endpoint_slack - expected_eta_endpoint_slack) == 0,
    "eta endpoint slack",
)

dimensionless_gap = sp.symbols("Delta", nonnegative=True, real=True)
eta_formula_abstract = (1 + q - dimensionless_gap) / (2 * (1 + q))
eta_first_bound_slack = sp.factor(eta_upper - eta_formula_abstract)
expected_eta_first_bound_slack = sp.factor(
    (dimensionless_gap - (1 - q)) / (2 * (1 + q))
)
require(
    sp.simplify(
        eta_first_bound_slack - expected_eta_first_bound_slack
    )
    == 0,
    "eta first-bound slack formula",
)

zeta, eta_symbol = sp.symbols(
    "zeta eta_symbol", nonnegative=True, real=True
)
c_zeta = zeta / (1 - zeta)
c_zeta_derivative_residual = sp.simplify(
    sp.diff(c_zeta, zeta) - 1 / (1 - zeta) ** 2
)
eta_odds_derivative_residual = sp.simplify(
    sp.diff(eta_symbol / (1 - eta_symbol), eta_symbol)
    - 1 / (1 - eta_symbol) ** 2
)
require(c_zeta_derivative_residual == 0, "c_eta zeta monotonicity formula")
require(
    eta_odds_derivative_residual == 0,
    "eta odds monotonicity formula",
)

# At t=0,x1=0 the directions are orthogonal.  This exact point, together
# with the globally simple top gap, supplies the continuity proof of I_1>0.
sample_q = sp.Rational(1, M**2)
sample_d = sp.Integer(0)
sample_delta = sp.sqrt((1 - sample_q) ** 2 + 4 * sample_q * sample_d**2)
sample_eta = sp.simplify(
    (1 + sample_q - sample_delta) / (2 * (1 + sample_q))
)
sample_c_eta = sp.simplify(
    sp.sqrt(sample_eta)
    / (sp.sqrt(1 - sample_eta) - sp.sqrt(sample_eta))
)
require(sample_eta == sp.Rational(1, M**2 + 1), "positive-point eta")
require(sample_c_eta == sp.Rational(1, M - 1), "positive-point c_eta")

expected_gradient_density = sp.simplify(
    amplitude**2
    * frequency**2
    * (low_decay**2 + high_decay**2)
)
low_gradient_density = sp.trigsimp(
    norm_squared(sp.diff(omega_low, x1)), method="fu"
)
high_gradient_density = sp.trigsimp(
    norm_squared(sp.diff(omega_high, x1)), method="fu"
)
require(
    sp.simplify(low_gradient_density - amplitude**2 * frequency**2 * low_decay**2)
    == 0,
    "low block-gradient density",
)
require(
    sp.simplify(
        high_gradient_density - amplitude**2 * frequency**2 * high_decay**2
    )
    == 0,
    "high block-gradient density",
)
gradient_density = low_gradient_density + high_gradient_density
require(
    sp.simplify(gradient_density - expected_gradient_density) == 0,
    "block-gradient density",
)
sample_gradient_factor = sp.simplify(
    (gradient_density / (amplitude**2 * frequency**2)).subs(t, 0)
)
sample_majorant_factor = sp.simplify(sample_c_eta * sample_gradient_factor)
require(sample_gradient_factor == 2, "positive-point gradient factor")
require(
    sample_majorant_factor == sp.Rational(2, M - 1),
    "positive-point majorant factor",
)

c_eta_endpoint = sp.simplify(
    sp.sqrt(eta_endpoint)
    / (sp.sqrt(1 - eta_endpoint) - sp.sqrt(eta_endpoint))
)
require(c_eta_endpoint == sp.Rational(1, M - 1), "c_eta endpoint")
base_majorant_upper_integral = sp.simplify(
    sp.Rational(1, M - 1)
    * (sp.Rational(1, 2) / nu + sp.Rational(1, 2) / (nu * M**2))
)
require(
    base_majorant_upper_integral
    == sp.Rational(M**2 + 1, 2 * M**2 * (M - 1)) / nu,
    "finite I_1 upper bound",
)

# An exact positive sample of the projector derivative also certifies that
# the base line field is nonconstant (used only for the W_1 positivity
# ledger, not as a closed-form evaluation of W_1).
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])
line_sample = e2 * e2.T
orthogonal_sample = sp.eye(3) - line_sample
covariance_x_derivative_sample = sp.simplify(
    sp.diff(covariance, x1).subs({x1: 0, t: 0})
)
absolute_gap_sample = sp.simplify(amplitude**2 * (1 - M ** (-2)))
line_derivative_sample = sp.simplify(
    (
        orthogonal_sample * covariance_x_derivative_sample * line_sample
        + line_sample * covariance_x_derivative_sample * orthogonal_sample
    )
    / absolute_gap_sample
)
line_derivative_norm_squared = sp.simplify(
    sum(entry**2 for entry in line_derivative_sample)
)
require(
    line_derivative_norm_squared
    == 2 * frequency**2 * M**2 / (M - 1) ** 2,
    "positive projector-gradient sample",
)


# ---------------------------------------------------------------------------
# 3. Exact dyadic pullback and scale ledgers.
# ---------------------------------------------------------------------------

J, j = sp.symbols("J j", integer=True)
multiplier_argument_residual = sp.simplify(
    sp.Integer(2) ** (-j) * sp.Integer(2) ** J
    - sp.Integer(2) ** (-(j - J))
)
require(multiplier_argument_residual == 0, "dyadic multiplier index shift")
require(M == 2**4, "M dyadic separation")

test_function = 2 + 3 * sp.cos(x1) + 5 * sp.sin(2 * x1)
pullback_mean_residual = sp.simplify(
    normalized_average_1d(test_function.subs(x1, frequency * x1), x1)
    - normalized_average_1d(test_function, x1)
)
pullback_l2_residual = sp.simplify(
    normalized_average_1d(
        test_function.subs(x1, frequency * x1) ** 2, x1
    )
    - normalized_average_1d(test_function**2, x1)
)
require(pullback_mean_residual == 0, "Pi_0 covering identity sample")
require(pullback_l2_residual == 0, "normalized Haar pullback sample")

# Directly compare the displayed N-family against the N=1, A=1 base fields
# after the covering pullback and parabolic time change.
base_vorticity = vorticity.subs({frequency: 1, amplitude: 1})
base_velocity = velocity.subs({frequency: 1, amplitude: 1})
base_covariance = covariance.subs({frequency: 1, amplitude: 1})
base_pullback_substitution = {x1: frequency * x1, t: frequency**2 * t}
vorticity_pullback_residual = (
    vorticity
    - amplitude * base_vorticity.subs(base_pullback_substitution)
).applyfunc(sp.expand)
velocity_pullback_residual = (
    velocity
    - amplitude
    / frequency
    * base_velocity.subs(base_pullback_substitution)
).applyfunc(sp.expand)
covariance_pullback_residual = (
    covariance
    - amplitude**2 * base_covariance.subs(base_pullback_substitution)
).applyfunc(sp.expand)
require(
    matrix_is_zero(vorticity_pullback_residual),
    "vorticity pullback residual",
)
require(
    matrix_is_zero(velocity_pullback_residual),
    "velocity pullback residual",
)
require(
    matrix_is_zero(covariance_pullback_residual),
    "covariance pullback residual",
)

# Exact factor arithmetic after s=N^2*t.  These checks audit the scale
# exponents; Haar invariance, index-shift lifting to commutators, and spectral
# projector equivariance are separately named analytic dependencies.
time_jacobian = frequency ** (-2)
l2_time_jacobian = sp.sqrt(time_jacobian)
residual_point_factor = amplitude**2
commutator_point_factor = amplitude**2
velocity_l2_squared_factor = amplitude**2 / frequency**2
gradient_velocity_l2_squared_factor = amplitude**2
gradient_projector_linf_squared_factor = frequency**2
gradient_density_factor = amplitude**2 * frequency**2

residual_l2_factor_derived = sp.simplify(
    residual_point_factor * l2_time_jacobian
)
commutator_l2_factor_derived = sp.simplify(
    commutator_point_factor * l2_time_jacobian
)
direction_cost_factor_derived = sp.simplify(
    velocity_l2_squared_factor
    * gradient_velocity_l2_squared_factor
    * gradient_projector_linf_squared_factor
    * time_jacobian
)
majorant_factor_derived = sp.simplify(
    gradient_density_factor * time_jacobian
)
require(
    sp.simplify(residual_l2_factor_derived - amplitude**2 / frequency) == 0,
    "residual L2 scale factor",
)
require(
    sp.simplify(commutator_l2_factor_derived - amplitude**2 / frequency)
    == 0,
    "commutator L2 scale factor",
)
require(
    sp.simplify(direction_cost_factor_derived - amplitude**4 / frequency**2)
    == 0,
    "direction-cost scale factor",
)
require(
    sp.simplify(majorant_factor_derived - amplitude**2) == 0,
    "majorant scale factor",
)

C_R, C_W, I_1 = sp.symbols("C_R C_W I_1", positive=True, real=True)
C_commutator = sp.symbols(
    "C_commutator", nonnegative=True, real=True
)
residual_l2_scale = sp.factor(C_R * amplitude**2 / frequency)
commutator_l2_scale = sp.factor(C_commutator * amplitude**2 / frequency)
direction_cost_scale = sp.factor(C_W * amplitude**4 / frequency**2)
majorant_scale = sp.factor(I_1 * amplitude**2)

amplitude_choice = frequency ** sp.Rational(1, 4)
energy_sequence = sp.simplify(
    velocity_energy_zero.subs(amplitude, amplitude_choice)
)
enstrophy_sequence = sp.simplify(
    enstrophy_zero.subs(amplitude, amplitude_choice)
)
residual_sequence = sp.simplify(
    residual_l2_scale.subs(amplitude, amplitude_choice)
)
commutator_sequence = sp.simplify(
    commutator_l2_scale.subs(amplitude, amplitude_choice)
)
direction_cost_sequence = sp.simplify(
    direction_cost_scale.subs(amplitude, amplitude_choice)
)
majorant_sequence = sp.simplify(
    majorant_scale.subs(amplitude, amplitude_choice)
)

require(
    energy_sequence
    == (1 + M ** (-4)) * frequency ** sp.Rational(-3, 2),
    "energy sequence exponent",
)
require(
    enstrophy_sequence
    == (1 + M ** (-2)) * frequency ** sp.Rational(1, 2),
    "enstrophy sequence exponent",
)
require(
    residual_sequence == C_R * frequency ** sp.Rational(-1, 2),
    "residual sequence exponent",
)
require(
    commutator_sequence
    == C_commutator * frequency ** sp.Rational(-1, 2),
    "commutator sequence exponent",
)
require(
    direction_cost_sequence == C_W / frequency,
    "direction-cost sequence exponent",
)
require(
    majorant_sequence == I_1 * sp.sqrt(frequency),
    "majorant sequence exponent",
)


# ---------------------------------------------------------------------------
# 4. Deterministic result payload and the exact claim boundary.
# ---------------------------------------------------------------------------

result = {
    "release": "R0.70S",
    "status": "exact-energy-palinstrophy-majorant-audit",
    "arithmetic": (
        "exact SymPy symbolic, rational, matrix, trigonometric, Fourier-"
        "support, dyadic-scale, and exponent arithmetic"
    ),
    "checks": {
        "exactGlobalTwoModeShearAndFrameSupport": True,
        "exactCovariancePolynomialAndEndpointSlacks": True,
        "displayedPullbackResidualsAndConditionalScaleArithmetic": True,
        "conditionalNoGoExponentArithmeticAndScope": True,
    },
    "definitions": {
        "domain": "T^3=(R/(2*pi*Z))^3 with normalized Haar measure",
        "rowGradientConvention": "B_ij=partial_i u_j",
        "fixedFrequencyRatio": "M=16=2^4",
        "dyadicFrequency": "N=2^J",
        "amplitudeChoice": "A_N=N^(1/4)",
        "completeFrame": "{T_star=Pi_0} union {T_j:j in Z}",
        "frameHypotheses": (
            "phi is real, even, radial, smooth, supported in the strict "
            "annulus, and sum_j|phi(2^(-j)*xi)|^2=1 for xi!=0"
        ),
        "residual": "R_N(t)=integral_T3 r_N(x,t) dx",
        "commutatorSquare": (
            "C_P_N(t)=||[Pi_0,P_N]omega_N||_2^2+"
            "sum_j||[T_j,P_N]omega_N||_2^2"
        ),
        "directionCost": (
            "W_L_N=integral ||u_N,*||_2^2 ||grad u_N||_2^2 "
            "||grad L_N||_infinity^2 dt"
        ),
        "majorant": "I_N=integral c_(r_N/E_N)*G_N dx dt",
        "majorantCoefficient": (
            "c_eta=sqrt(eta)/(sqrt(1-eta)-sqrt(eta))"
        ),
    },
    "globalShearLedger": {
        "velocity": (
            "u_N=(A_N/N)*[-exp(-nu*N^2*t)*v_N+"
            "M^(-2)*exp(-nu*M^2*N^2*t)*w_MN]"
        ),
        "vorticity": (
            "omega_N=A_N*[exp(-nu*N^2*t)*v_N+"
            "M^(-1)*exp(-nu*M^2*N^2*t)*w_MN]"
        ),
        "velocityDivergence": "0",
        "vorticityDivergence": "0",
        "curlResidual": vector_payload(curl_residual),
        "heatEquationResidual": vector_payload(heat_residual),
        "vorticityHeatEquationResidual": vector_payload(
            vorticity_heat_residual
        ),
        "advectiveNonlinearity": vector_payload(nonlinearity),
        "pressureChoice": "p=0",
        "solutionBoundary": (
            "for every finite dyadic N and A_N>0 this is a smooth global "
            "mean-zero unforced Navier--Stokes shear heat flow"
        ),
        "initialKineticEnergy": scalar_payload(velocity_energy_zero),
        "initialEnstrophy": scalar_payload(enstrophy_zero),
        "lowActiveIndex": "J",
        "highActiveIndex": "J+4",
        "lowActiveOffsets": low_active_offsets,
        "highActiveOffsets": high_active_offsets,
        "activeIndexIntersection": "empty",
        "activeIndexDerivation": (
            "1/2<2^(J-j)<2 gives -1<J-j<1; since J-j is integer, "
            "j=J. Replacing J by J+4 gives j=J+4."
        ),
        "supportConvention": "strict annulus 1/2<|xi|/2^j<2",
        "lowResponseSquare": "1",
        "highResponseSquare": "1",
        "responseSquareDerivation": (
            "analytic consequence of the pinned strict singleton support "
            "and exact tightness sum; phi is not numerically evaluated"
        ),
        "zeroModeOfVorticity": vector_payload(mean_vorticity),
        "zeroModeLedger": (
            "Pi_0 omega_N=0, but [Pi_0,P_N]omega_N is retained in "
            "the complete commutator square"
        ),
        "tightCovariance": (
            "Q_N=omega_low tensor omega_low+omega_high tensor omega_high"
        ),
        "crossFrequencyOuterProduct": (
            "absent because the singleton active index groups are disjoint"
        ),
    },
    "covarianceSpectrumLedger": {
        "directionDotProduct": "sin(17*N*x1)",
        "Q": "alpha^2*v_N tensor v_N+beta^2*w_MN tensor w_MN",
        "traceE": "alpha^2+beta^2",
        "characteristicPolynomial": (
            "lambda*(lambda^2-E*lambda+alpha^2*beta^2*(1-d^2))"
        ),
        "characteristicResidual": scalar_payload(characteristic_residual),
        "eigenvalues": (
            "lambda_(1,2)=(E+/-sqrt((alpha^2-beta^2)^2+"
            "4*alpha^2*beta^2*d^2))/2; lambda_3=0"
        ),
        "q": scalar_payload(q_ratio),
        "qAtTimeZero": scalar_payload(q_initial),
        "qLogDerivative": scalar_payload(q_log_derivative),
        "gapSquareSlack": "4*alpha^2*beta^2*d^2",
        "gapBound": "lambda1-lambda2>=alpha^2-beta^2>0 for finite t",
        "relativeGapBound": "(lambda1-lambda2)/E>=255/257",
        "relativeGapEndpointSlack": scalar_payload(relative_gap_slack),
        "etaDefinition": "eta=r/E=lambda2/E",
        "etaFirstBound": "eta<=q/(1+q)",
        "etaFirstBoundSlackFormula": scalar_payload(
            eta_first_bound_slack
        ),
        "etaEndpointBound": "0<=eta<=1/257",
        "etaEndpointSlack": scalar_payload(eta_endpoint_slack),
        "cEtaBound": "0<=c_eta<=1/15",
        "cEtaMonotonicityLedger": {
            "substitution": "zeta=sqrt(eta/(1-eta)), c_eta=zeta/(1-zeta)",
            "dcDzetaResidual": scalar_payload(c_zeta_derivative_residual),
            "dEtaOddsResidual": scalar_payload(
                eta_odds_derivative_residual
            ),
            "status": (
                "exact derivative identities plus 0<=eta<1/2 give the "
                "analytic monotonicity implication"
            ),
        },
        "positivePoint": {
            "location": "t=0, x1=0",
            "directions": "v_N=e2 and w_MN=e3 are orthogonal",
            "eta": scalar_payload(sample_eta),
            "cEta": scalar_payload(sample_c_eta),
            "normalizedGradientDensity": scalar_payload(sample_gradient_factor),
            "normalizedMajorantIntegrand": scalar_payload(
                sample_majorant_factor
            ),
        },
        "continuityCertificate": (
            "the finite-time top gap is positive, so eta and c_eta*G are "
            "continuous near the positive point; therefore they stay "
            "positive on a positive-measure relative neighborhood and "
            "I_1(S)>0 for every S>0"
        ),
        "baseMajorantUpperIntegral": scalar_payload(
            base_majorant_upper_integral
        ),
        "baseMajorantStatus": "0<I_1(infinity)<infinity; no quadrature used",
        "gradientDensity": (
            "A_N^2*N^2*(exp(-2*nu*N^2*t)+"
            "exp(-2*nu*M^2*N^2*t))"
        ),
        "projectorDerivativeSampleNormSquared": scalar_payload(
            line_derivative_norm_squared
        ),
    },
    "dyadicScalingLedger": {
        "pullback": "S_N f(x)=f(N*x)",
        "normalizedHaar": "||S_N f||_p=||f||_p for integer N and 1<=p<=infinity",
        "finiteL2SampleResidual": scalar_payload(pullback_l2_residual),
        "zeroModeIdentity": "Pi_0(S_N f)=Pi_0(f)",
        "finiteZeroModeSampleResidual": scalar_payload(pullback_mean_residual),
        "annularIndexShift": "T_j*S_N=S_N*T_(j-J)",
        "multiplierArgumentResidual": scalar_payload(
            multiplier_argument_residual
        ),
        "displayedFieldPullbackResiduals": {
            "vorticity": vector_payload(vorticity_pullback_residual),
            "velocity": vector_payload(velocity_pullback_residual),
            "covariance": matrix_payload(covariance_pullback_residual),
        },
        "scaleFactorResiduals": {
            "residualL2": scalar_payload(
                residual_l2_factor_derived - amplitude**2 / frequency
            ),
            "commutatorL2": scalar_payload(
                commutator_l2_factor_derived - amplitude**2 / frequency
            ),
            "directionCost": scalar_payload(
                direction_cost_factor_derived - amplitude**4 / frequency**2
            ),
            "majorant": scalar_payload(
                majorant_factor_derived - amplitude**2
            ),
        },
        "analyticDependencies": [
            "normalized Haar invariance under the integer covering S_N",
            "Fourier-symbol index shift lifted from modes to the pinned frame",
            "simple-eigenvalue spectral projectors are invariant under positive scalar multiplication of Q",
            "change of variables s=N^2*t on the stated finite or infinite time intervals",
        ],
        "certificateScope": (
            "the producer checks the displayed-field pullback residuals, "
            "multiplier-argument identity, one finite Haar sample, and "
            "conditional factor arithmetic; the universal Haar, frame, "
            "commutator, and spectral-projector lifting statements are "
            "analytic report lemmas rather than consequences of the sample"
        ),
        "fieldScaling": {
            "omega": "omega_N=A_N*S_N[omega_1(.,N^2*t)]",
            "velocity": "u_N=(A_N/N)*S_N[u_1(.,N^2*t)]",
            "covariance": "Q_N=A_N^2*S_N[Q_1(.,N^2*t)]",
            "residualRatio": "eta_N=S_N[eta_1(.,N^2*t)]",
            "projectors": "L_N=S_N[L_1], P_N=S_N[P_1] at base time N^2*t",
            "gradientDensity": "G_N=A_N^2*N^2*S_N[G_1(.,N^2*t)]",
        },
        "finiteTimeIdentities": {
            "residual": (
                "||R_N||_L2(0,T)=(A_N^2/N)*"
                "||R_1||_L2(0,N^2*T)"
            ),
            "commutator": (
                "||C_P_N||_L2(0,T)=(A_N^2/N)*"
                "||C_P_1||_L2(0,N^2*T)"
            ),
            "directionCost": (
                "W_L_N(0,T)=(A_N^4/N^2)*W_L_1(0,N^2*T)"
            ),
            "majorant": "I_N(T)=A_N^2*I_1(N^2*T)",
        },
        "commutatorBlockIdentities": {
            "annular": (
                "[T_j,P_N]omega_N=A_N*S_N([T_(j-J),P_1]omega_1)"
            ),
            "zeroMode": (
                "[Pi_0,P_N]omega_N=A_N*S_N([Pi_0,P_1]omega_1)"
            ),
            "baseConstantEvaluation": (
                "the stated analytic scaling lemma includes Pi_0; the "
                "multiplier-dependent base L2 norm is not evaluated in "
                "closed form"
            ),
        },
        "infiniteHorizonConstants": {
            "R": (
                "C_R=||R_1||_L2(0,infinity); positivity and finiteness "
                "are analytic report lemmas, not numerical integration"
            ),
            "commutator": (
                "C_commutator=||C_P_1||_L2(0,infinity); finiteness is an "
                "analytic complete-frame lemma and no closed-form value is "
                "evaluated"
            ),
            "directionCost": (
                "C_W=W_L_1(0,infinity); positivity/finiteness use the "
                "certified sample plus analytic gap/decay lemmas"
            ),
            "majorant": (
                "I_1=I_1(infinity); positivity/finiteness use the exact "
                "positive point plus analytic continuity/decay"
            ),
        },
    },
    "exponentLedger": {
        "amplitude": "A_N=N^(1/4)",
        "initialKineticEnergy": scalar_payload(energy_sequence),
        "residualL2InfiniteHorizon": scalar_payload(residual_sequence),
        "commutatorL2InfiniteHorizon": scalar_payload(commutator_sequence),
        "directionCostInfiniteHorizon": scalar_payload(direction_cost_sequence),
        "majorantInfiniteHorizon": scalar_payload(majorant_sequence),
        "fixedTimeMajorantLowerBound": (
            "I_N(T)=sqrt(N)*I_1(N^2*T)>=sqrt(N)*I_1(T) for N>=1; "
            "I_1(T)>0"
        ),
        "limits": {
            "kineticEnergy": "0",
            "residualL2": "0",
            "commutatorL2": "0",
            "directionCost": "0",
            "majorant": "+infinity",
        },
        "initialEnstrophy": scalar_payload(enstrophy_sequence),
        "initialH1Boundary": (
            "initial H1^2 includes the enstrophy term and diverges like "
            "N^(1/2)"
        ),
        "uniformEtaBound": "eta_N<=1/257",
    },
    "claimBoundary": (
        "This finite certificate directly checks the displayed two-mode "
        "global shear field residuals, covariance polynomial and endpoint "
        "slacks, all-integer singleton support, field pullback residuals, "
        "Fourier multiplier argument, conditional scale/exponent arithmetic, "
        "and the exact positive majorant point. Together with the separately "
        "named analytic Haar, frame, spectral, continuity, decay, and "
        "change-of-variable lemmas, it supports a contradiction "
        "only for one function F fixed uniformly across all dyadic N and "
        "locally bounded near the zero four-tuple, with T, nu, eta0=1/257, "
        "and the pinned frame fixed. It does not assert that the signed diffusion "
        "deficit K_Q-D_P is large, does not exclude estimates depending on "
        "initial H1, enstrophy, palinstrophy, higher Sobolev norms, frequency "
        "moments, absolute covariance, or another derivative-sensitive "
        "datum, and does not prove singularity, PDE closure, continuation, "
        "global regularity, or the Millennium problem."
    ),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    payload = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(payload, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")


if __name__ == "__main__":
    main()
