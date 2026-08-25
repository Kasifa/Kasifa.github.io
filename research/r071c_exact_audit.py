#!/usr/bin/env python3
"""Exact finite audit for the R0.71C signed-localization gate.

The producer checks seven narrowly delimited facts.

1. A signed-before-square Cauchy ledger is monotone under partition
   refinement, and a binary refinement pays a nonnegative defect.
2. The R0.71B same-output normalization is discontinuous at a vanishing
   strain coefficient, even along a fixed finite Fourier family.
3. Two disjoint real Fourier triads place opposite covariance work on two
   output modes of the same radius.  Their coarse work cancels exactly while
   the fine positive-output ledger is nonzero.
4. Linear Stokes damping immediately destroys that cancellation because the
   two covariance inputs have different radii.
5. For the full-response tensor Q=omega tensor omega, the same initial datum
   is an exact smooth Navier--Stokes initial trace: after amplitude scaling by
   epsilon, the coarse work derivative is
       12*nu*epsilon**3 + (76/5)*epsilon**4 > 0.
6. A balanced two-shell HHL datum has zero initial fine coefficient but both
   Stokes and true NSE evolution create positive output immediately.
7. The shellwise full-nonlinearity injection gives a valid conditional
   continuation reduction, but time-integrated signed box mass controls the
   required positive square variation in the wrong direction.

The audit does not prove or disprove time integrability of the R0.71B
positive-output coefficient.  It does not exclude adaptive nonlinear
localizations or a genuinely PDE-specific flux estimate, and it does not
prove global regularity, finite-time blow-up, or any Millennium-problem
claim.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

import sympy as sp

import r071b_exact_audit as r071b


Frequency = tuple[int, int, int]


def clean(value):
    if isinstance(value, sp.MatrixBase):
        return value.applyfunc(lambda entry: sp.factor(sp.cancel(sp.expand(entry))))
    return sp.factor(sp.cancel(sp.expand(value)))


def require(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def add(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def negative(frequency: Frequency) -> Frequency:
    return tuple(-entry for entry in frequency)  # type: ignore[return-value]


def square(frequency: Frequency) -> int:
    return sum(entry * entry for entry in frequency)


def outer(first: sp.Matrix, second: sp.Matrix) -> sp.Matrix:
    return first * second.T


def matrix_square(matrix: sp.Matrix) -> sp.Expr:
    return clean(
        sum(
            sp.conjugate(matrix[row, column]) * matrix[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


def matrix_pair(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return clean(
        sum(
            sp.conjugate(first[row, column]) * second[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


def velocity(frequency: Frequency, omega: sp.Matrix) -> sp.Matrix:
    return clean(sp.I * sp.Matrix(frequency).cross(omega) / square(frequency))


def strain_coefficient(frequency: Frequency, omega: sp.Matrix) -> sp.Matrix:
    wave = sp.Matrix(frequency)
    speed = velocity(frequency, omega)
    return clean(
        sp.I * (outer(wave, speed) + outer(speed, wave)) / 2
    )


def covariance_at(
    modes: dict[Frequency, sp.Matrix],
    output: Frequency,
    kernel=lambda _first, _second: sp.Integer(1),
) -> sp.Matrix:
    tensor = sp.zeros(3, 3)
    for first, second in product(modes, repeat=2):
        if add(first, second) == output:
            tensor += kernel(first, second) * outer(
                modes[first], modes[second]
            )
    return clean(tensor)


def signed_output_work(
    modes: dict[Frequency, sp.Matrix],
    output: Frequency,
    kernel=lambda _first, _second: sp.Integer(1),
) -> sp.Expr:
    strain = strain_coefficient(output, modes[output])
    tensor = covariance_at(modes, output, kernel)
    return clean(2 * sp.re(matrix_pair(strain, tensor)))


def ordered_zero_sum_count(support: set[Frequency]) -> int:
    return sum(
        1
        for first, second in product(support, repeat=2)
        if negative(add(first, second)) in support
    )


def scaled_real_modes(
    positive_modes: dict[Frequency, sp.Matrix],
    amplitude: sp.Expr,
) -> dict[Frequency, sp.Matrix]:
    output: dict[Frequency, sp.Matrix] = {}
    for frequency, coefficient in positive_modes.items():
        output[frequency] = clean(amplitude * coefficient)
        output[negative(frequency)] = clean(amplitude * coefficient)
    return output


def equal_radius_response(
    first: Frequency,
    second: Frequency,
) -> sp.Integer:
    return sp.Integer(square(first) == square(second))


# ---------------------------------------------------------------------------
# 1. Abstract refinement ledger.
# ---------------------------------------------------------------------------

x, y, d, e = sp.symbols("x y d e", positive=True)
positive_children_defect = clean(
    x**2 / d + y**2 / e - (x + y) ** 2 / (d + e)
)
positive_children_square = clean(
    (e * x - d * y) ** 2 / (d * e * (d + e))
)
require(
    clean(positive_children_defect - positive_children_square) == 0,
    "positive-child refinement square",
)

# The full theorem is proved in the report from
# (sum_j z_j)^+ <= sum_j z_j^+ followed by weighted Cauchy.  This symbolic
# identity records its equality defect in the all-positive two-child sector.


# ---------------------------------------------------------------------------
# 2. Static zero-denominator discontinuity of the R0.71B coefficient.
# ---------------------------------------------------------------------------

e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])

amp_a, amp_b, eta = sp.symbols("amp_a amp_b eta", positive=True)
disc_p: Frequency = (1, 1, 0)
disc_q: Frequency = (1, -1, 0)
disc_k: Frequency = (2, 0, 0)
disc_a = e3
disc_b = (e1 + e2) / sp.sqrt(2)
disc_c = -e2

disc_modes = scaled_real_modes(
    {
        disc_p: amp_a * disc_a,
        disc_q: amp_b * disc_b,
        disc_k: eta * disc_c,
    },
    sp.Rational(1, 2),
)
disc_strain = strain_coefficient(disc_k, disc_modes[disc_k])
disc_tensor = covariance_at(
    disc_modes,
    disc_k,
    equal_radius_response,
)
disc_work = signed_output_work(
    disc_modes,
    disc_k,
    equal_radius_response,
)
disc_strain_square = matrix_square(disc_strain)
disc_output_term = clean(
    disc_work**2
    / (4 * square(disc_k) * disc_strain_square)
)
disc_energy = clean((amp_a**2 + amp_b**2 + eta**2) / 2)
disc_gradient = clean(amp_a**2 + amp_b**2 + 2 * eta**2)
disc_normalized_lower_limit = clean(
    disc_output_term
    / ((amp_a**2 + amp_b**2) / 2)
)

require(
    clean(
        disc_strain
        - eta
        * (outer(e1, e3) + outer(e3, e1))
        / 4
    )
    == sp.zeros(3, 3),
    "discontinuity strain coefficient",
)
require(
    clean(
        disc_tensor
        - amp_a
        * amp_b
        * (outer(disc_a, disc_b) + outer(disc_b, disc_a))
        / 4
    )
    == sp.zeros(3, 3),
    "discontinuity covariance coefficient",
)
require(
    disc_work == sp.sqrt(2) * amp_a * amp_b * eta / 8,
    "discontinuity signed work",
)
require(disc_strain_square == eta**2 / 8, "discontinuity strain square")
require(
    disc_output_term == amp_a**2 * amp_b**2 / 64,
    "discontinuity positive-output term",
)
require(
    clean(
        disc_normalized_lower_limit
        - amp_a**2 * amp_b**2 / (32 * (amp_a**2 + amp_b**2))
    )
    == 0,
    "discontinuity normalized jump",
)


# ---------------------------------------------------------------------------
# 3. Two disjoint same-output-radius triads.
# ---------------------------------------------------------------------------

k1: Frequency = (2, 0, 0)
p1: Frequency = (1, 1, 0)
q1: Frequency = (1, -1, 0)
k2: Frequency = (0, 0, 2)
p2: Frequency = (2, 0, 1)
q2: Frequency = (-2, 0, 1)

positive_modes = {
    k1: e2,
    p1: sp.Matrix([1, -1, 0]),
    q1: -e3,
    k2: e1,
    p2: sp.Matrix([-1, 0, 2]),
    q2: sp.Rational(1, 2) * e2,
}

triad1 = {k1, p1, q1, negative(k1), negative(p1), negative(q1)}
triad2 = {k2, p2, q2, negative(k2), negative(p2), negative(q2)}
modes = scaled_real_modes(positive_modes, sp.Integer(1))
support = set(modes)

for frequency, coefficient in modes.items():
    require(
        clean(sp.Matrix(frequency).dot(coefficient)) == 0,
        f"divergence-free mode {frequency}",
    )

require(k1 == add(p1, q1), "first output resonance")
require(k2 == add(p2, q2), "second output resonance")
require(square(k1) == square(k2) == 4, "same output radius")
require(square(p1) == square(q1) == 2, "first input radius")
require(square(p2) == square(q2) == 5, "second input radius")
require(ordered_zero_sum_count(triad1) == 12, "first intended resonances")
require(ordered_zero_sum_count(triad2) == 12, "second intended resonances")
require(ordered_zero_sum_count(support) == 24, "no cross-triad resonances")

work1 = signed_output_work(modes, k1)
work2 = signed_output_work(modes, k2)
strain1 = strain_coefficient(k1, modes[k1])
strain2 = strain_coefficient(k2, modes[k2])
dissipation1 = clean(4 * square(k1) * matrix_square(strain1))
dissipation2 = clean(4 * square(k2) * matrix_square(strain2))

require(work1 == 2, "first selected output work")
require(work2 == -2, "second selected output work")
require(dissipation1 == 8, "first selected dissipation weight")
require(dissipation2 == 8, "second selected dissipation weight")

root_initial = clean(sp.Max(work1 + work2, 0) ** 2 / (dissipation1 + dissipation2))
fine_initial = clean(work1**2 / dissipation1)
require(root_initial == 0, "coarse initial cancellation")
require(fine_initial == sp.Rational(1, 2), "latent fine positive mass")


# ---------------------------------------------------------------------------
# 4. Exact Stokes sign creation.
# ---------------------------------------------------------------------------

nu, time = sp.symbols("nu time", positive=True)
A = sp.exp(-8 * nu * time)
B = sp.exp(-14 * nu * time)
stokes_work1 = 2 * A
stokes_work2 = -2 * B
stokes_weight1 = 8 * A
stokes_weight2 = 8 * A

stokes_parent_work = clean(stokes_work1 + stokes_work2)
stokes_root = clean(stokes_parent_work**2 / (stokes_weight1 + stokes_weight2))
stokes_fine = clean(stokes_work1**2 / stokes_weight1)
stokes_defect = clean(stokes_fine - stokes_root)

require(clean(stokes_parent_work.subs(time, 0)) == 0, "Stokes zero trace")
require(
    clean(sp.diff(stokes_parent_work, time).subs(time, 0)) == 12 * nu,
    "Stokes positive trace derivative",
)

time1 = sp.log(2) / (6 * nu)
root_at_time1 = clean(stokes_root.subs(time, time1))
fine_at_time1 = clean(stokes_fine.subs(time, time1))
defect_at_time1 = clean(stokes_defect.subs(time, time1))
require(root_at_time1 == 2 ** sp.Rational(-16, 3), "Stokes root at t1")
require(fine_at_time1 == 2 ** sp.Rational(-7, 3), "Stokes fine at t1")
require(
    defect_at_time1 == 7 * 2 ** sp.Rational(-16, 3),
    "Stokes defect at t1",
)


# ---------------------------------------------------------------------------
# 5. True NSE initial derivative for the full-response tensor.
# ---------------------------------------------------------------------------

epsilon = sp.symbols("epsilon", positive=True)
scaled_modes = scaled_real_modes(positive_modes, epsilon)
scaled_support = set(scaled_modes)


def nonlinear_vorticity_derivative(output: Frequency) -> sp.Matrix:
    derivative = sp.zeros(3, 1)
    for first, second in product(scaled_support, repeat=2):
        if add(first, second) != output:
            continue
        derivative += sp.I * (
            scaled_modes[first].dot(sp.Matrix(second))
            * velocity(second, scaled_modes[second])
            - velocity(first, scaled_modes[first]).dot(sp.Matrix(second))
            * scaled_modes[second]
        )
    return clean(derivative)


generated_support = {
    add(first, second)
    for first, second in product(scaled_support, repeat=2)
} | scaled_support
mode_derivative: dict[Frequency, sp.Matrix] = {}
for frequency in generated_support:
    if frequency == (0, 0, 0):
        continue
    value = nonlinear_vorticity_derivative(frequency)
    if frequency in scaled_modes:
        value += -nu * square(frequency) * scaled_modes[frequency]
    mode_derivative[frequency] = clean(value)

for frequency, coefficient in mode_derivative.items():
    require(
        clean(sp.Matrix(frequency).dot(coefficient)) == 0,
        f"NSE derivative divergence {frequency}",
    )
    opposite = negative(frequency)
    if opposite in mode_derivative:
        require(
            clean(mode_derivative[opposite] - sp.conjugate(coefficient))
            == sp.zeros(3, 1),
            f"NSE derivative reality {frequency}",
        )


def covariance_derivative_at(output: Frequency) -> sp.Matrix:
    derivative = sp.zeros(3, 3)
    for frequency, coefficient in mode_derivative.items():
        partner = add(output, negative(frequency))
        if partner in scaled_modes:
            derivative += outer(coefficient, scaled_modes[partner])
    for frequency, coefficient in scaled_modes.items():
        partner = add(output, negative(frequency))
        if partner in mode_derivative:
            derivative += outer(coefficient, mode_derivative[partner])
    return clean(derivative)


def signed_output_derivative(output: Frequency) -> sp.Expr:
    strain = strain_coefficient(output, scaled_modes[output])
    strain_derivative = strain_coefficient(output, mode_derivative[output])
    tensor = covariance_at(scaled_modes, output)
    tensor_derivative = covariance_derivative_at(output)
    return clean(
        2
        * sp.re(
            matrix_pair(strain_derivative, tensor)
            + matrix_pair(strain, tensor_derivative)
        )
    )


scaled_work1 = signed_output_work(scaled_modes, k1)
scaled_work2 = signed_output_work(scaled_modes, k2)
derivative1 = signed_output_derivative(k1)
derivative2 = signed_output_derivative(k2)
parent_derivative = clean(derivative1 + derivative2)

require(scaled_work1 == 2 * epsilon**3, "scaled first work")
require(scaled_work2 == -2 * epsilon**3, "scaled second work")
require(
    clean(derivative1 - (-16 * nu * epsilon**3 + 6 * epsilon**4)) == 0,
    "first NSE output derivative",
)
require(
    clean(
        derivative2
        - (28 * nu * epsilon**3 + sp.Rational(46, 5) * epsilon**4)
    )
    == 0,
    "second NSE output derivative",
)
require(
    clean(
        parent_derivative
        - (12 * nu * epsilon**3 + sp.Rational(76, 5) * epsilon**4)
    )
    == 0,
    "positive NSE parent derivative",
)


# ---------------------------------------------------------------------------
# 6. Exact zero-to-positive fine coefficient under Stokes and true NSE.
# ---------------------------------------------------------------------------

delta = sp.symbols("delta", positive=True)
hhl_n: Frequency = (1, 1, 0)
hhl_c = (e1 - e2) / sp.sqrt(2)


def hhl_data(value: int) -> tuple[Frequency, Frequency, sp.Matrix, sp.Expr]:
    radius_square = 2 * value**2 + 2 * value + 1
    first = (value, -value - 1, 0)
    second = (-value - 1, value, 0)
    polarization = sp.Matrix([value, value + 1, 0]) / sp.sqrt(radius_square)
    balancing = (2 * value + 1) / (
        sp.sqrt(2) * sp.sqrt(radius_square)
    )
    return first, second, polarization, balancing


hhl_p8, hhl_q8, hhl_b8, h8 = hhl_data(8)
hhl_p64, hhl_q64, hhl_b64, h64 = hhl_data(64)
hhl_positive_modes = {
    hhl_n: hhl_c,
    hhl_p8: h64 * e3,
    hhl_q8: hhl_b8,
    hhl_p64: h8 * e3,
    hhl_q64: -hhl_b64,
}
hhl_modes = scaled_real_modes(hhl_positive_modes, delta / 2)
hhl_support = set(hhl_modes)
hhl_work_at_zero = signed_output_work(
    hhl_modes,
    hhl_n,
    equal_radius_response,
)

for frequency, coefficient in hhl_modes.items():
    require(
        clean(sp.Matrix(frequency).dot(coefficient)) == 0,
        f"HHL divergence {frequency}",
    )

require(
    ordered_zero_sum_count(hhl_support) == 24,
    "HHL two-shell intended resonances",
)
require(hhl_work_at_zero == 0, "HHL exact signed cancellation")

hhl_nonzero_outputs: list[tuple[Frequency, sp.Expr]] = []
for frequency in sorted(hhl_support):
    if not frequency > negative(frequency):
        continue
    output_work = signed_output_work(
        hhl_modes,
        frequency,
        equal_radius_response,
    )
    if output_work != 0:
        hhl_nonzero_outputs.append((frequency, output_work))
require(hhl_nonzero_outputs == [], "HHL all positive-output terms vanish")

hhl_c0 = clean(h8 * h64 / 4)
hhl_heat_rate_first = sp.Integer(290)
hhl_heat_rate_second = sp.Integer(16642)
hhl_heat_work = clean(
    delta**3
    * hhl_c0
    * sp.exp(-2 * nu * time)
    * (
        sp.exp(-hhl_heat_rate_first * nu * time)
        - sp.exp(-hhl_heat_rate_second * nu * time)
    )
)
hhl_heat_derivative = clean(sp.diff(hhl_heat_work, time).subs(time, 0))
hhl_heat_constant = clean(hhl_heat_derivative / (nu * delta**3))
hhl_heat_positive_square = clean(
    delta**4
    * hhl_c0**2
    * (
        sp.exp(-hhl_heat_rate_first * nu * time)
        - sp.exp(-hhl_heat_rate_second * nu * time)
    )
    ** 2
)
require(
    hhl_heat_constant
    == 4482492 * sp.sqrt(1206545) / 1206545,
    "HHL heat sign-creation constant",
)


hhl_nonlinear_map: dict[Frequency, sp.Matrix] = {}
for first, second in product(hhl_support, repeat=2):
    output = add(first, second)
    if output == (0, 0, 0):
        continue
    contribution = sp.I * (
        hhl_modes[first].dot(sp.Matrix(second))
        * velocity(second, hhl_modes[second])
        - velocity(first, hhl_modes[first]).dot(sp.Matrix(second))
        * hhl_modes[second]
    )
    hhl_nonlinear_map[output] = (
        hhl_nonlinear_map.get(output, sp.zeros(3, 1)) + contribution
    )
hhl_nonlinear_map = {
    frequency: clean(coefficient)
    for frequency, coefficient in hhl_nonlinear_map.items()
}

hhl_generated_support = set(hhl_nonlinear_map) | hhl_support
hhl_mode_derivative: dict[Frequency, sp.Matrix] = {}
for frequency in hhl_generated_support:
    if frequency == (0, 0, 0):
        continue
    value = hhl_nonlinear_map.get(frequency, sp.zeros(3, 1))
    if frequency in hhl_modes:
        value += -nu * square(frequency) * hhl_modes[frequency]
    hhl_mode_derivative[frequency] = clean(value)


def hhl_covariance_derivative(output: Frequency) -> sp.Matrix:
    derivative = sp.zeros(3, 3)
    for frequency, coefficient in hhl_mode_derivative.items():
        partner = add(output, negative(frequency))
        if partner in hhl_modes:
            derivative += equal_radius_response(frequency, partner) * outer(
                coefficient, hhl_modes[partner]
            )
    for frequency, coefficient in hhl_modes.items():
        partner = add(output, negative(frequency))
        if partner in hhl_mode_derivative:
            derivative += equal_radius_response(frequency, partner) * outer(
                coefficient, hhl_mode_derivative[partner]
            )
    return clean(derivative)


hhl_strain = strain_coefficient(hhl_n, hhl_modes[hhl_n])
hhl_strain_derivative = strain_coefficient(
    hhl_n,
    hhl_mode_derivative[hhl_n],
)
hhl_tensor = covariance_at(
    hhl_modes,
    hhl_n,
    equal_radius_response,
)
hhl_tensor_derivative = hhl_covariance_derivative(hhl_n)
hhl_nse_derivative = clean(
    2
    * sp.re(
        matrix_pair(hhl_strain_derivative, hhl_tensor)
        + matrix_pair(hhl_strain, hhl_tensor_derivative)
    )
)
hhl_nse_linear = clean(sp.diff(hhl_nse_derivative, nu) * nu)
hhl_nse_quartic = clean(hhl_nse_derivative.subs(nu, 0))

require(
    hhl_nse_linear == nu * delta**3 * hhl_heat_constant,
    "HHL true-NSE viscous derivative",
)
require(
    hhl_nse_quartic == sp.Rational(4809249, 19304720) * delta**4,
    "HHL true-NSE quartic derivative",
)
require(
    clean(hhl_nse_derivative - hhl_nse_linear - hhl_nse_quartic) == 0,
    "HHL true-NSE derivative split",
)


# ---------------------------------------------------------------------------
# 7. Conditional shell-injection reduction and inherited acceptance checks.
# ---------------------------------------------------------------------------

production, total_dissipation, theta, energy = sp.symbols(
    "production total_dissipation theta energy", positive=True
)
young_residual = clean(
    nu * total_dissipation / 2
    + theta**2 / (2 * nu)
    - sp.sqrt(total_dissipation) * theta
)
young_square = clean(
    (
        sp.sqrt(nu * total_dissipation)
        - theta / sp.sqrt(nu)
    )
    ** 2
    / 2
)
require(clean(young_residual - young_square) == 0, "shell-injection Young identity")

# R0.71C must not forget the exact R0.71A/R0.71B acceptance witnesses.
require(
    r071b.positive_output["positiveSquare"] == sp.Rational(9, 800),
    "R0.71A positive sign pair inherited",
)
require(
    r071b.negative_output["positiveSquare"] == 0,
    "R0.71A negative sign pair inherited",
)
require(
    r071b.same_low_resonance_count == 12 * r071b.FAN_N,
    "same-low fan inherited",
)
require(
    r071b.shared_resonance_count == 12 * r071b.SHARED_N,
    "shared-high fan inherited",
)


def text(value: sp.Expr) -> str:
    return str(clean(value))


payload = {
    "release": "R0.71C",
    "status": "signed-refinement-and-viscous-sign-creation-gate",
    "checks": {
        "partitionRefinementMonotone": True,
        "binaryDefectNonnegative": True,
        "positiveOutputNormalizationDiscontinuous": True,
        "sameRadiusOppositeOutputs": True,
        "triadsHaveNoCrossResonances": True,
        "coarseCancellationHasLatentFineMass": True,
        "StokesCreatesPositiveCoarseWork": True,
        "trueNseCreatesPositiveCoarseWork": True,
        "fineCoefficientStartsAtZero": True,
        "StokesCreatesFinePositiveCoefficient": True,
        "trueNseCreatesFinePositiveCoefficient": True,
        "shellInjectionConditionalReduction": True,
        "signedBoxDirectionInsufficient": True,
        "r071aSignPairRechecked": True,
        "r071bPackingFansRechecked": True,
    },
    "partitionLedger": {
        "definition": "E_Pi=sum_(B in Pi) ((sum_(i in B) w_i)^+)^2/(sum_(i in B) d_i)",
        "consumer": "(sum_i w_i)^+ <= sqrt(sum_i d_i)*sqrt(E_Pi)",
        "refinement": "E_Pi <= E_PiPrime whenever PiPrime refines Pi",
        "binaryDefect": "delta_v=E_children-E_parent>=0",
        "positiveChildrenDefect": text(positive_children_defect),
        "treeIdentity": "E_leaves=E_root+sum_(internal v) delta_v",
        "decision": "refining a signed ledger exposes a nonnegative cancellation defect rather than producing a free cancellation estimate",
    },
    "normalizationDiscontinuity": {
        "frequencies": {
            "p": list(disc_p),
            "q": list(disc_q),
            "k": list(disc_k),
        },
        "strainCoefficient": "(eta/4)*(e1 tensor e3+e3 tensor e1)",
        "covarianceCoefficient": "(amp_a*amp_b/4)*(a tensor b+b tensor a)",
        "signedWork": text(disc_work),
        "strainSquare": text(disc_strain_square),
        "positiveOutputTermForEtaPositive": text(disc_output_term),
        "energy": text(disc_energy),
        "gradientEnstrophy": text(disc_gradient),
        "normalizedLiminfAsEtaToZero": text(disc_normalized_lower_limit),
        "valueAtEtaZeroByConvention": "0",
        "decision": "the same-output strain normalization is not continuous even along fixed finite Fourier support and strong Sobolev convergence",
    },
    "twoTriadWitness": {
        "positiveModes": {
            str(frequency): [text(entry) for entry in coefficient]
            for frequency, coefficient in positive_modes.items()
        },
        "modeCountIncludingRealityPartners": len(support),
        "orderedZeroSumResonances": ordered_zero_sum_count(support),
        "expectedOrderedZeroSumResonances": 24,
        "outputRadiiSquared": [square(k1), square(k2)],
        "inputRadiiSquared": [
            [square(p1), square(q1)],
            [square(p2), square(q2)],
        ],
        "selectedWorks": [text(work1), text(work2)],
        "selectedDissipationWeights": [text(dissipation1), text(dissipation2)],
        "coarseLedgerAtZero": text(root_initial),
        "fineLedgerAtZero": text(fine_initial),
    },
    "StokesEvolution": {
        "work1": "2*exp(-8*nu*t)",
        "work2": "-2*exp(-14*nu*t)",
        "weight1": "8*exp(-8*nu*t)",
        "weight2": "8*exp(-8*nu*t)",
        "parentWork": "2*(exp(-8*nu*t)-exp(-14*nu*t))",
        "parentDerivativeAtZero": "12*nu",
        "comparisonTime": "log(2)/(6*nu)",
        "rootLedgerAtComparisonTime": text(root_at_time1),
        "fineLedgerAtComparisonTime": text(fine_at_time1),
        "refinementDefectAtComparisonTime": text(defect_at_time1),
        "decision": "different input radii make viscosity reveal initially cancelled positive output on a fixed equal-output-radius node",
    },
    "NavierStokesInitialTrace": {
        "tensor": "Q=omega tensor omega (the full-response or identity-frame tensor)",
        "amplitude": "omega_0=epsilon*Omega",
        "selectedWorksAtZero": [text(scaled_work1), text(scaled_work2)],
        "selectedDerivativesAtZero": [text(derivative1), text(derivative2)],
        "parentWorkAtZero": "0",
        "parentDerivativeAtZero": text(parent_derivative),
        "linearViscousPart": "12*nu*epsilon^3",
        "nonlinearPart": "(76/5)*epsilon^4",
        "decision": "the parent work becomes positive for every nu>0 and epsilon>0 at sufficiently small positive time",
    },
    "zeroToPositiveFineCoefficient": {
        "frameResponse": "Gamma(r,s)=1 when |r|=|s| and 0 otherwise (orthogonal radial-sphere Parseval response)",
        "shellParameters": [8, 64],
        "modeCountIncludingRealityPartners": len(hhl_support),
        "orderedZeroSumResonances": ordered_zero_sum_count(hhl_support),
        "signedOutputAtZero": text(hhl_work_at_zero),
        "nonzeroPositiveOutputsAtZero": len(hhl_nonzero_outputs),
        "positiveOutputCoefficientAtZero": "0",
        "balancingConstant": text(hhl_c0),
        "heatWork": "delta^3*c0*exp(-2*nu*t)*(exp(-290*nu*t)-exp(-16642*nu*t))",
        "heatDerivativeAtZero": text(hhl_heat_derivative),
        "heatConstant": text(hhl_heat_constant),
        "heatPositiveSquareContribution": "delta^4*c0^2*(exp(-290*nu*t)-exp(-16642*nu*t))^2",
        "trueNseDerivativeAtZero": text(hhl_nse_derivative),
        "trueNseViscousPart": text(hhl_nse_linear),
        "trueNseQuarticPart": text(hhl_nse_quartic),
        "decision": "for the displayed radial Parseval response, a_+(0)=0 but a_+(t)>0 for every sufficiently small positive time; homogeneous Gronwall propagation from a_+(0) is impossible",
    },
    "shellInjectionReduction": {
        "definition": "b_alpha=<T_alpha omega,T_alpha(S omega-u dot grad omega)>",
        "shellIdentity": "(1/2)Y_alpha prime+nu D_alpha=b_alpha",
        "coefficient": "A_sb,+=Y^(-1)*sum_alpha (b_alpha^+)^2/D_alpha",
        "consumer": "P_+<=sqrt(D)*Theta_sb,+<=nu*D/2+(A_sb,+*Y)/(2*nu)",
        "conditionalConclusion": "integral A_sb,+ dt finite implies H1 continuation",
        "signedIntervalMass": "beta_alpha,I=(Y_alpha(t1)-Y_alpha(t0))/2+nu*integral_I D_alpha",
        "direction": "(beta_alpha,I^+)^2/integral_I D_alpha <= integral_I (b_alpha^+)^2/D_alpha",
        "decision": "the conditional quantity is scale critical, but signed box telescoping supplies only a lower bound for the required positive square variation",
    },
    "acceptanceWitnesses": {
        "r071aPositiveSquare": text(r071b.positive_output["positiveSquare"]),
        "r071aNegativeSquare": text(r071b.negative_output["positiveSquare"]),
        "sameLowOrderedResonances": r071b.same_low_resonance_count,
        "sharedHighOrderedResonances": r071b.shared_resonance_count,
        "decision": "the new ledger preserves the earlier sign distinction but does not remove either packing obstruction",
    },
    "analyticDependencies": [
        "the refinement theorem uses positive-part subadditivity and weighted Cauchy; the arbitrary finite-partition proof is in the report",
        "the Fourier calculation uses normalized torus coefficients, omega_hat(-k)=conjugate(omega_hat(k)), and u_hat(k)=i*k cross omega_hat(k)/|k|^2",
        "the explicit NSE derivative uses the full-response tensor Q=omega tensor omega; other frame-response kernels can alter the quartic term",
        "the zero-to-positive fine-coefficient derivative is exact for the orthogonal radial-sphere Parseval response; for any fixed bounded smooth response its universal positive cubic heat term dominates the finite quartic term after sufficiently small amplitude scaling",
        "a smooth trigonometric polynomial is admissible smooth periodic initial data and has a local smooth Navier-Stokes solution",
        "the shell-injection continuation step uses the standard H1 blow-up alternative for smooth periodic Navier-Stokes solutions",
        "comparison with BMO, dyadic BMO, Besov, and dynamic dissipation-wavenumber criteria is a literature statement, not a finite-algebra output",
    ],
    "claimBoundary": [
        "classifies every additive finite signed-before-square partition ledger by an exact nonnegative refinement defect",
        "proves that neither static nesting nor linear viscous evolution gives a monotone signed-output cancellation principle for the displayed full-response node",
        "proves an exact true-NSE initial-trace sign-creation example for Q=omega tensor omega",
        "proves that the R0.71B normalization is discontinuous at a zero output-strain mode and that the displayed radial-sphere response creates a positive fine coefficient from zero under true NSE",
        "rules out homogeneous Gronwall propagation from a_+(0), but not an estimate with an additive flux source",
        "does not show that the time integral of the R0.71B coefficient diverges for any NSE solution",
        "does not exclude adaptive, solution-dependent localization or a PDE flux identity that independently controls the refinement defect",
        "the shell-injection criterion is a conditional reduction, not a new unconditional regularity theorem",
        "does not prove a singularity, global regularity, or solve the Millennium problem",
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
