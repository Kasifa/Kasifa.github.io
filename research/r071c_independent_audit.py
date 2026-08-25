#!/usr/bin/env python3
"""Independent exact audit for the R0.71C signed-output obstruction.

This checker deliberately imports no project audit module.  It rebuilds the
partition ledger, the finite Fourier field, the full Fourier vorticity
nonlinearity, the derivative of the full-response covariance, and the scalar
signed-interval obstruction from their definitions.

All deciding arithmetic is exact SymPy arithmetic.  In particular, Q'(k)
includes nonlinear modes created outside the initial support; omitting those
modes gives the wrong quartic coefficient.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path
from typing import Callable, Iterable

import sympy as sp


Frequency = tuple[int, int, int]
Block = tuple[int, ...]
Response = Callable[[Frequency, Frequency], sp.Expr]


def clean(expression: sp.Expr) -> sp.Expr:
    """Put an exact scalar expression in a stable simplified form."""

    return sp.factor(sp.cancel(sp.expand(expression)))


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def add(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def subtract(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] - second[index] for index in range(3))  # type: ignore[return-value]


def negate(frequency: Frequency) -> Frequency:
    return tuple(-entry for entry in frequency)  # type: ignore[return-value]


def frequency_square(frequency: Frequency) -> int:
    return sum(entry * entry for entry in frequency)


def outer(first: sp.Matrix, second: sp.Matrix) -> sp.Matrix:
    return first * second.T


def matrix_inner_conjugate(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return clean(
        sum(
            sp.conjugate(first[row, column]) * second[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


def positive_part(value: sp.Expr) -> sp.Expr:
    """Positive part for an exact real number, not a symbolic variable."""

    need(value.is_real is not False, "positive part received a non-real value")
    if value.is_nonnegative:
        return value
    if value.is_negative:
        return sp.Integer(0)
    raise AssertionError(f"undecidable sign in exact positive part: {value}")


def as_text(value: object) -> str:
    if isinstance(value, sp.Basic):
        return sp.sstr(clean(value))
    return str(value)


def ledger(
    partition: Iterable[Block],
    works: list[sp.Expr],
    weights: list[sp.Expr],
) -> sp.Expr:
    total = sp.Integer(0)
    for block in partition:
        block_work = clean(sum(works[index] for index in block))
        block_weight = clean(sum(weights[index] for index in block))
        need(block_weight.is_positive is True, "ledger weight must be positive")
        total += positive_part(block_work) ** 2 / block_weight
    return clean(total)


def partition_audit() -> dict[str, object]:
    """Check refinement, defect decomposition, telescoping, and the consumer."""

    child_left, child_right = sp.symbols("a b", nonnegative=True)
    weight_left, weight_right = sp.symbols("d e", positive=True)
    balance_defect = clean(
        child_left**2 / weight_left
        + child_right**2 / weight_right
        - (child_left + child_right) ** 2 / (weight_left + weight_right)
    )
    balance_square = clean(
        (weight_right * child_left - weight_left * child_right) ** 2
        / (weight_left * weight_right * (weight_left + weight_right))
    )
    need(clean(balance_defect - balance_square) == 0, "balance square identity")

    # Exact piecewise regression of the arbitrary-sign decomposition
    # delta = balance defect + cancellation loss.
    checked_cases = 0
    for left_work in range(-3, 4):
        for right_work in range(-3, 4):
            for left_weight in range(1, 5):
                for right_weight in range(1, 5):
                    x = sp.Integer(left_work)
                    y = sp.Integer(right_work)
                    d = sp.Integer(left_weight)
                    e = sp.Integer(right_weight)
                    a = positive_part(x)
                    b = positive_part(y)
                    c = positive_part(x + y)
                    exact_defect = clean(a**2 / d + b**2 / e - c**2 / (d + e))
                    decomposed = clean(
                        (e * a - d * b) ** 2 / (d * e * (d + e))
                        + ((a + b) ** 2 - c**2) / (d + e)
                    )
                    need(clean(exact_defect - decomposed) == 0, "piecewise defect identity")
                    need(exact_defect.is_nonnegative is True, "negative refinement defect")
                    checked_cases += 1

    works = [sp.Integer(3), sp.Integer(-5), sp.Integer(7), sp.Integer(-1)]
    weights = [sp.Integer(2), sp.Integer(3), sp.Integer(5), sp.Integer(7)]
    leaves = ((0,), (1,), (2,), (3,))
    middle = ((0, 1), (2, 3))
    root = ((0, 1, 2, 3),)
    energy_leaves = ledger(leaves, works, weights)
    energy_middle = ledger(middle, works, weights)
    energy_root = ledger(root, works, weights)
    lower_defect = clean(energy_leaves - energy_middle)
    upper_defect = clean(energy_middle - energy_root)
    need(energy_root <= energy_middle <= energy_leaves, "refinement monotonicity example")
    need(
        clean(energy_leaves - energy_root - lower_defect - upper_defect) == 0,
        "binary telescoping identity",
    )

    total_work_positive = positive_part(sum(works))
    total_weight = sum(weights)
    consumer_residual = clean(
        total_weight * energy_middle - total_work_positive**2
    )
    need(consumer_residual.is_nonnegative is True, "partition consumer")

    return {
        "definition": "E_Pi=sum_B (W_B^+)^2/D_B",
        "twoPositiveChildrenDefect": as_text(balance_square),
        "arbitrarySignDecomposition": (
            "delta=(e*a-d*b)^2/(d*e*(d+e))"
            "+((a+b)^2-((x+y)^+)^2)/(d+e), a=x^+, b=y^+"
        ),
        "exactPiecewiseCasesChecked": checked_cases,
        "example": {
            "works": [as_text(value) for value in works],
            "weights": [as_text(value) for value in weights],
            "rootEnergy": as_text(energy_root),
            "middleEnergy": as_text(energy_middle),
            "leafEnergy": as_text(energy_leaves),
            "lowerDefect": as_text(lower_defect),
            "upperDefect": as_text(upper_defect),
            "telescopingResidual": "0",
            "consumerResidual": as_text(consumer_residual),
        },
        "provedAlgebraically": [
            "refinement can only increase E_Pi",
            "E_leaves=E_root+sum_internal_delta with every delta nonnegative",
            "(sum_i w_i)^+ <= sqrt(sum_i d_i)*sqrt(E_Pi)",
        ],
    }


def velocity(frequency: Frequency, omega: sp.Matrix) -> sp.Matrix:
    square = frequency_square(frequency)
    need(square > 0, "velocity requested at zero frequency")
    wave = sp.Matrix(frequency)
    return (sp.I * wave.cross(omega) / square).applyfunc(clean)


def strain(frequency: Frequency, omega: sp.Matrix) -> sp.Matrix:
    wave = sp.Matrix(frequency)
    flow = velocity(frequency, omega)
    return (
        sp.I * (outer(wave, flow) + outer(flow, wave)) / 2
    ).applyfunc(clean)


def response_covariance(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
    response: Response,
) -> sp.Matrix:
    result = sp.zeros(3, 3)
    for first_frequency, first_coefficient in modes.items():
        second_frequency = subtract(output, first_frequency)
        if second_frequency in modes:
            result += response(first_frequency, second_frequency) * outer(
                first_coefficient,
                modes[second_frequency],
            )
    return result.applyfunc(clean)


def full_response(_first: Frequency, _second: Frequency) -> sp.Integer:
    return sp.Integer(1)


def radial_sphere_response(first: Frequency, second: Frequency) -> sp.Integer:
    return sp.Integer(frequency_square(first) == frequency_square(second))


def full_covariance(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
) -> sp.Matrix:
    return response_covariance(output, modes, full_response)


def response_output_work(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
    response: Response,
) -> sp.Expr:
    return clean(
        2
        * sp.re(
            matrix_inner_conjugate(
                strain(output, modes[output]),
                response_covariance(output, modes, response),
            )
        )
    )


def output_work(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
) -> sp.Expr:
    return response_output_work(output, modes, full_response)


def dissipation_weight(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
) -> sp.Expr:
    strain_coefficient = strain(output, modes[output])
    strain_square = matrix_inner_conjugate(strain_coefficient, strain_coefficient)
    return clean(4 * frequency_square(output) * strain_square)


def add_cosine_mode(
    modes: dict[Frequency, sp.Matrix],
    frequency: Frequency,
    amplitude: sp.Matrix,
) -> None:
    positive_coefficient = amplitude / 2
    negative_coefficient = amplitude.applyfunc(sp.conjugate) / 2
    modes[frequency] = (
        modes.get(frequency, sp.zeros(3, 1)) + positive_coefficient
    ).applyfunc(clean)
    negative_frequency = negate(frequency)
    modes[negative_frequency] = (
        modes.get(negative_frequency, sp.zeros(3, 1))
        + negative_coefficient
    ).applyfunc(clean)


def is_positive_representative(frequency: Frequency) -> bool:
    for entry in frequency:
        if entry:
            return entry > 0
    raise AssertionError("zero frequency has no signed representative")


def vector_square(vector: sp.Matrix) -> sp.Expr:
    return clean(sum(sp.conjugate(entry) * entry for entry in vector))


def nonlinear_vorticity_rhs(
    modes: dict[Frequency, sp.Matrix],
) -> dict[Frequency, sp.Matrix]:
    """Return N_hat for N=(omega.grad)u-(u.grad)omega.

    The implementation follows

      N_k = i sum_{p+q=k} [(omega_p.q) u_q - (u_p.q) omega_q].

    It returns every nonzero generated mode, not merely the initial support.
    """

    result: dict[Frequency, sp.Matrix] = {}
    for first_frequency, first_omega in modes.items():
        first_velocity = velocity(first_frequency, first_omega)
        for second_frequency, second_omega in modes.items():
            output = add(first_frequency, second_frequency)
            if output == (0, 0, 0):
                continue
            second_velocity = velocity(second_frequency, second_omega)
            second_wave = sp.Matrix(second_frequency)
            contribution = sp.I * (
                first_omega.dot(second_wave) * second_velocity
                - first_velocity.dot(second_wave) * second_omega
            )
            result[output] = result.get(output, sp.zeros(3, 1)) + contribution

    cleaned: dict[Frequency, sp.Matrix] = {}
    for frequency, coefficient in result.items():
        exact = coefficient.applyfunc(clean)
        if exact != sp.zeros(3, 1):
            cleaned[frequency] = exact
    return cleaned


def response_covariance_derivative(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
    mode_derivative: dict[Frequency, sp.Matrix],
    response: Response,
) -> sp.Matrix:
    """Differentiate a fixed-response covariance over all generated modes."""

    result = sp.zeros(3, 3)
    for first_frequency, first_derivative in mode_derivative.items():
        second_frequency = subtract(output, first_frequency)
        if second_frequency in modes:
            result += response(first_frequency, second_frequency) * outer(
                first_derivative,
                modes[second_frequency],
            )
    for first_frequency, first_omega in modes.items():
        second_frequency = subtract(output, first_frequency)
        if second_frequency in mode_derivative:
            result += response(first_frequency, second_frequency) * outer(
                first_omega,
                mode_derivative[second_frequency],
            )
    return result.applyfunc(clean)


def covariance_derivative(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
    mode_derivative: dict[Frequency, sp.Matrix],
) -> sp.Matrix:
    return response_covariance_derivative(
        output,
        modes,
        mode_derivative,
        full_response,
    )


def response_output_work_derivative(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
    mode_derivative: dict[Frequency, sp.Matrix],
    response: Response,
) -> sp.Expr:
    strain_now = strain(output, modes[output])
    strain_derivative = strain(
        output,
        mode_derivative.get(output, sp.zeros(3, 1)),
    )
    covariance_now = response_covariance(output, modes, response)
    covariance_rate = response_covariance_derivative(
        output,
        modes,
        mode_derivative,
        response,
    )
    return clean(
        2
        * sp.re(
            matrix_inner_conjugate(strain_derivative, covariance_now)
            + matrix_inner_conjugate(strain_now, covariance_rate)
        )
    )


def output_work_derivative(
    output: Frequency,
    modes: dict[Frequency, sp.Matrix],
    mode_derivative: dict[Frequency, sp.Matrix],
) -> sp.Expr:
    return response_output_work_derivative(
        output,
        modes,
        mode_derivative,
        full_response,
    )


def fourier_audit() -> dict[str, object]:
    half = sp.Rational(1, 2)
    named_frequencies: dict[str, Frequency] = {
        "k1": (2, 0, 0),
        "p1": (1, 1, 0),
        "q1": (1, -1, 0),
        "k2": (0, 0, 2),
        "p2": (2, 0, 1),
        "q2": (-2, 0, 1),
    }
    named_coefficients = {
        "k1": sp.Matrix((0, 1, 0)),
        "p1": sp.Matrix((1, -1, 0)),
        "q1": sp.Matrix((0, 0, -1)),
        "k2": sp.Matrix((1, 0, 0)),
        "p2": sp.Matrix((-1, 0, 2)),
        "q2": sp.Matrix((0, half, 0)),
    }

    modes = {
        named_frequencies[name]: coefficient
        for name, coefficient in named_coefficients.items()
    }
    for frequency, coefficient in list(modes.items()):
        modes[negate(frequency)] = coefficient

    need(len(modes) == 12, "twelve signed support modes")
    for frequency, coefficient in modes.items():
        need(sp.Matrix(frequency).dot(coefficient) == 0, f"divergence at {frequency}")
        need(modes[negate(frequency)] == sp.conjugate(coefficient), "reality condition")

    support = set(modes)
    resonances: list[tuple[Frequency, Frequency, Frequency]] = []
    for first, second in product(support, repeat=2):
        third = negate(add(first, second))
        if third in support:
            resonances.append((first, second, third))

    first_group = {
        named_frequencies[name] for name in ("k1", "p1", "q1")
    }
    first_group |= {negate(frequency) for frequency in first_group}
    second_group = support - first_group
    mixed_resonances = [
        resonance
        for resonance in resonances
        if not (
            set(resonance) <= first_group
            or set(resonance) <= second_group
        )
    ]
    need(len(resonances) == 24, "twenty-four ordered zero-sum resonances")
    need(not mixed_resonances, "no cross-triad zero-sum resonance")

    k1 = named_frequencies["k1"]
    k2 = named_frequencies["k2"]
    need(frequency_square(k1) == frequency_square(k2) == 4, "equal output shell")
    work1 = output_work(k1, modes)
    work2 = output_work(k2, modes)
    weight1 = dissipation_weight(k1, modes)
    weight2 = dissipation_weight(k2, modes)
    need(work1 == 2 and work2 == -2, "initial output works")
    need(weight1 == 8 and weight2 == 8, "initial dissipation weights")

    viscosity = sp.symbols("nu", positive=True)
    linear_derivative = {
        frequency: -viscosity * frequency_square(frequency) * coefficient
        for frequency, coefficient in modes.items()
    }
    linear_work_rate1 = output_work_derivative(k1, modes, linear_derivative)
    linear_work_rate2 = output_work_derivative(k2, modes, linear_derivative)
    need(linear_work_rate1 == -16 * viscosity, "first Stokes derivative")
    need(linear_work_rate2 == 28 * viscosity, "second Stokes derivative")
    need(
        clean(linear_work_rate1 + linear_work_rate2) == 12 * viscosity,
        "parent Stokes derivative",
    )

    # At t1=log(2)/(6 nu), r=exp(-8 nu t1)=2^(-4/3), while
    # exp(-14 nu t1)=r/2.
    radius_factor = 2 ** (-sp.Rational(4, 3))
    t1_work1 = clean(2 * radius_factor)
    t1_work2 = clean(-radius_factor)
    t1_weight = clean(8 * radius_factor)
    initial_parent_energy = clean(positive_part(work1 + work2) ** 2 / (weight1 + weight2))
    initial_leaf_energy = clean(
        positive_part(work1) ** 2 / weight1
        + positive_part(work2) ** 2 / weight2
    )
    t1_parent_energy = clean(
        positive_part(t1_work1 + t1_work2) ** 2 / (2 * t1_weight)
    )
    t1_leaf_energy = clean(
        positive_part(t1_work1) ** 2 / t1_weight
        + positive_part(t1_work2) ** 2 / t1_weight
    )
    t1_defect = clean(t1_leaf_energy - t1_parent_energy)
    need(initial_parent_energy == 0, "initial parent ledger")
    need(initial_leaf_energy == sp.Rational(1, 2), "initial leaf ledger")
    need(
        clean(t1_parent_energy - 2 ** (-sp.Rational(16, 3))) == 0,
        "t1 parent ledger",
    )
    need(
        clean(t1_leaf_energy - 2 ** (-sp.Rational(7, 3))) == 0,
        "t1 leaf ledger",
    )
    need(
        clean(t1_defect - 7 * 2 ** (-sp.Rational(16, 3))) == 0,
        "t1 refinement defect",
    )

    nonlinear_derivative = nonlinear_vorticity_rhs(modes)
    need(len(nonlinear_derivative) == 50, "full nonlinear generated support")
    for frequency, coefficient in nonlinear_derivative.items():
        need(
            sp.Matrix(frequency).dot(coefficient) == 0,
            f"nonlinear divergence at {frequency}",
        )
        need(
            nonlinear_derivative.get(negate(frequency))
            == sp.conjugate(coefficient),
            f"nonlinear reality at {frequency}",
        )

    nonlinear_work_rate1 = output_work_derivative(k1, modes, nonlinear_derivative)
    nonlinear_work_rate2 = output_work_derivative(k2, modes, nonlinear_derivative)
    nonlinear_parent_rate = clean(nonlinear_work_rate1 + nonlinear_work_rate2)
    need(nonlinear_work_rate1 == 6, "first quartic work derivative")
    need(nonlinear_work_rate2 == sp.Rational(46, 5), "second quartic work derivative")
    need(nonlinear_parent_rate == sp.Rational(76, 5), "quartic parent derivative")

    epsilon = sp.symbols("epsilon", positive=True)
    scaled_parent_rate = clean(
        12 * viscosity * epsilon**3
        + nonlinear_parent_rate * epsilon**4
    )
    need(
        clean(
            scaled_parent_rate
            - 12 * viscosity * epsilon**3
            - sp.Rational(76, 5) * epsilon**4
        )
        == 0,
        "scaled NSE derivative",
    )

    # A second check does not use the differentiated-work helper.  Form the
    # complete first-order Fourier polynomial omega+h*omega_dot, rebuild Q and
    # S, and differentiate the resulting parent work with respect to h.
    increment = sp.symbols("h", real=True)
    perturbed_modes: dict[Frequency, sp.Matrix] = {}
    all_frequencies = set(modes) | set(nonlinear_derivative)
    for frequency in all_frequencies:
        base = modes.get(frequency, sp.zeros(3, 1))
        linear_rate = linear_derivative.get(frequency, sp.zeros(3, 1))
        nonlinear_rate = nonlinear_derivative.get(frequency, sp.zeros(3, 1))
        perturbed_modes[frequency] = (
            epsilon * base
            + increment
            * (epsilon * linear_rate + epsilon**2 * nonlinear_rate)
        ).applyfunc(clean)
    direct_parent_polynomial = clean(
        output_work(k1, perturbed_modes) + output_work(k2, perturbed_modes)
    )
    direct_parent_rate = clean(
        sp.diff(direct_parent_polynomial, increment).subs(increment, 0)
    )
    need(
        clean(direct_parent_rate - scaled_parent_rate) == 0,
        "direct first-order Fourier reconstruction",
    )

    return {
        "field": {
            "signedSupportSize": len(modes),
            "allModesDivergenceFree": True,
            "realFourierField": True,
            "orderedZeroSumResonances": len(resonances),
            "crossTriadResonances": len(mixed_resonances),
            "equalOutputRadiusSquared": 4,
        },
        "initialOutputLedger": {
            "wK1": as_text(work1),
            "wK2": as_text(work2),
            "dK1": as_text(weight1),
            "dK2": as_text(weight2),
            "parentEnergy": as_text(initial_parent_energy),
            "leafEnergy": as_text(initial_leaf_energy),
            "refinementDefect": as_text(initial_leaf_energy - initial_parent_energy),
        },
        "stokes": {
            "w1(t)": "2*exp(-8*nu*t)",
            "w2(t)": "-2*exp(-14*nu*t)",
            "parentWork(t)": "2*exp(-8*nu*t)*(1-exp(-6*nu*t)) > 0 for t>0",
            "parentDerivativeAtZero": as_text(12 * viscosity),
            "t1": "log(2)/(6*nu)",
            "t1ParentEnergy": "2^(-16/3)",
            "t1LeafEnergy": "2^(-7/3)",
            "t1RefinementDefect": "7*2^(-16/3)",
        },
        "navierStokesDerivative": {
            "nonlinearGeneratedModes": len(nonlinear_derivative),
            "outsideInitialSupportIncludedInQdot": True,
            "quarticRateK1": as_text(nonlinear_work_rate1),
            "quarticRateK2": as_text(nonlinear_work_rate2),
            "quarticParentRate": as_text(nonlinear_parent_rate),
            "scaledParentRate": as_text(scaled_parent_rate),
            "directFirstOrderReconstruction": as_text(direct_parent_rate),
            "directReconstructionResidual": "0",
            "strictlyPositiveFor": "nu>0 and epsilon>0",
        },
    }


def normalization_discontinuity_audit() -> dict[str, object]:
    """Check the exact three-mode discontinuity in the normalized output."""

    amplitude_a, amplitude_b, eta = sp.symbols("A B eta", positive=True)
    p = (1, 1, 0)
    q = (1, -1, 0)
    k = (2, 0, 0)
    polarization_a = sp.Matrix((0, 0, 1))
    polarization_b = sp.Matrix((1, 1, 0)) / sp.sqrt(2)
    polarization_c = sp.Matrix((0, -1, 0))

    modes: dict[Frequency, sp.Matrix] = {}
    add_cosine_mode(modes, p, amplitude_a * polarization_a)
    add_cosine_mode(modes, q, amplitude_b * polarization_b)
    add_cosine_mode(modes, k, eta * polarization_c)
    for frequency, coefficient in modes.items():
        need(sp.Matrix(frequency).dot(coefficient) == 0, "three-mode divergence")

    representatives = sorted(
        frequency for frequency in modes if is_positive_representative(frequency)
    )
    works = {
        frequency: response_output_work(
            frequency,
            modes,
            radial_sphere_response,
        )
        for frequency in representatives
    }
    expected_work = sp.sqrt(2) * amplitude_a * amplitude_b * eta / 8
    need(clean(works[k] - expected_work) == 0, "three-mode output work")
    need(works[p] == 0 and works[q] == 0, "three-mode other output works")

    output_strain = strain(k, modes[k])
    strain_square = matrix_inner_conjugate(output_strain, output_strain)
    expected_strain_square = eta**2 / 8
    need(
        clean(strain_square - expected_strain_square) == 0,
        "three-mode output strain square",
    )
    output_denominator = dissipation_weight(k, modes)
    output_term = clean(expected_work**2 / output_denominator)
    expected_output_term = amplitude_a**2 * amplitude_b**2 / 64
    need(
        clean(output_term - expected_output_term) == 0,
        "three-mode positive-output quotient",
    )

    total_enstrophy = clean(sum(vector_square(value) for value in modes.values()))
    expected_enstrophy = (
        amplitude_a**2 + amplitude_b**2 + eta**2
    ) / 2
    need(
        clean(total_enstrophy - expected_enstrophy) == 0,
        "three-mode enstrophy",
    )
    normalized_coefficient = clean(output_term / total_enstrophy)
    normalized_limit = clean(sp.limit(normalized_coefficient, eta, 0, dir="+"))
    expected_limit = clean(
        amplitude_a**2
        * amplitude_b**2
        / (32 * (amplitude_a**2 + amplitude_b**2))
    )
    need(
        clean(normalized_limit - expected_limit) == 0,
        "three-mode normalized liminf",
    )

    zero_modes: dict[Frequency, sp.Matrix] = {}
    add_cosine_mode(zero_modes, p, amplitude_a * polarization_a)
    add_cosine_mode(zero_modes, q, amplitude_b * polarization_b)
    zero_works = {
        frequency: response_output_work(
            frequency,
            zero_modes,
            radial_sphere_response,
        )
        for frequency in zero_modes
        if is_positive_representative(frequency)
    }
    need(all(value == 0 for value in zero_works.values()), "eta-zero works")

    return {
        "frequencies": {
            "p": str(p),
            "q": str(q),
            "k": str(k),
        },
        "response": "Gamma(r,s)=1 when |r|^2=|s|^2, otherwise 0",
        "outputWork": as_text(works[k]),
        "outputStrainSquare": as_text(strain_square),
        "outputDenominator": as_text(output_denominator),
        "positiveOutputTerm": as_text(output_term),
        "totalEnstrophy": as_text(total_enstrophy),
        "normalizedCoefficientForEtaPositive": as_text(normalized_coefficient),
        "normalizedLiminf": as_text(normalized_limit),
        "normalizedValueAtEtaZero": "0",
        "otherOutputWorks": {
            str(frequency): as_text(value)
            for frequency, value in works.items()
            if frequency != k
        },
        "claim": (
            "the zero-denominator convention makes the normalized "
            "positive-output coefficient discontinuous at eta=0"
        ),
    }


def balanced_hhl_audit() -> dict[str, object]:
    """Check the M=8,64 balanced HHL heat and NSE sign creation."""

    n = (1, 1, 0)
    low_polarization = sp.Matrix((1, -1, 0)) / sp.sqrt(2)
    vertical_polarization = sp.Matrix((0, 0, 1))

    def radius_square(value: int) -> int:
        return 2 * value**2 + 2 * value + 1

    def p_mode(value: int) -> Frequency:
        return (value, -value - 1, 0)

    def q_mode(value: int) -> Frequency:
        return (-value - 1, value, 0)

    def q_polarization(value: int) -> sp.Matrix:
        return sp.Matrix((value, value + 1, 0)) / sp.sqrt(
            radius_square(value)
        )

    def low_leg(value: int) -> sp.Expr:
        return clean(
            sp.Rational(2 * value + 1)
            / (sp.sqrt(2) * sp.sqrt(radius_square(value)))
        )

    first_value = 8
    second_value = 64
    first_radius_square = radius_square(first_value)
    second_radius_square = radius_square(second_value)
    need(first_radius_square == 145, "M=8 radius")
    need(second_radius_square == 8321, "M=64 radius")
    need(
        first_radius_square * second_radius_square == 1_206_545,
        "HHL radical",
    )

    h8 = low_leg(first_value)
    h64 = low_leg(second_value)
    modes: dict[Frequency, sp.Matrix] = {}
    add_cosine_mode(modes, n, low_polarization)
    add_cosine_mode(
        modes,
        p_mode(first_value),
        h64 * vertical_polarization,
    )
    add_cosine_mode(
        modes,
        q_mode(first_value),
        q_polarization(first_value),
    )
    add_cosine_mode(
        modes,
        p_mode(second_value),
        h8 * vertical_polarization,
    )
    add_cosine_mode(
        modes,
        q_mode(second_value),
        -q_polarization(second_value),
    )

    need(len(modes) == 10, "balanced HHL signed support")
    for frequency, coefficient in modes.items():
        need(sp.Matrix(frequency).dot(coefficient) == 0, "balanced HHL divergence")
        need(
            modes[negate(frequency)] == sp.conjugate(coefficient),
            "balanced HHL reality",
        )

    support = set(modes)
    resonance_count = sum(
        1
        for first, second in product(support, repeat=2)
        if negate(add(first, second)) in support
    )
    need(resonance_count == 24, "balanced HHL resonances")

    representatives = sorted(
        frequency for frequency in support if is_positive_representative(frequency)
    )
    initial_works = {
        frequency: response_output_work(
            frequency,
            modes,
            radial_sphere_response,
        )
        for frequency in representatives
    }
    need(all(value == 0 for value in initial_works.values()), "all initial HHL works")

    viscosity, time = sp.symbols("nu t", positive=True)
    delta = sp.symbols("delta", positive=True)
    heat_modes = {
        frequency: (
            sp.exp(-viscosity * frequency_square(frequency) * time)
            * coefficient
        )
        for frequency, coefficient in modes.items()
    }
    # Avoid generic polynomial factorization on exponentials.  The raw exact
    # sum has only the four ordered high-high pairs that reach n.
    heat_covariance = sp.zeros(3, 3)
    heat_pair_count = 0
    for first_frequency, first_coefficient in heat_modes.items():
        second_frequency = subtract(n, first_frequency)
        if (
            second_frequency in heat_modes
            and radial_sphere_response(first_frequency, second_frequency) == 1
        ):
            heat_covariance += outer(
                first_coefficient,
                heat_modes[second_frequency],
            )
            heat_pair_count += 1
    need(heat_pair_count == 4, "balanced HHL heat target pairs")
    heat_strain = strain(n, heat_modes[n])
    heat_work = sp.simplify(
        2
        * sum(
            sp.conjugate(heat_strain[row, column])
            * heat_covariance[row, column]
            for row in range(3)
            for column in range(3)
        )
    )
    cancellation_amplitude = clean(h8 * h64 / 4)
    expected_heat_work = cancellation_amplitude * sp.exp(-2 * viscosity * time) * (
        sp.exp(-2 * first_radius_square * viscosity * time)
        - sp.exp(-2 * second_radius_square * viscosity * time)
    )
    need(
        sp.simplify(heat_work - expected_heat_work) == 0,
        "balanced HHL heat work",
    )
    heat_dissipation_weight = dissipation_weight(n, heat_modes)
    need(
        sp.simplify(
            heat_dissipation_weight - sp.exp(-4 * viscosity * time)
        )
        == 0,
        "balanced HHL heat output weight",
    )
    scaled_heat_positive_term = sp.powsimp(
        delta**4
        * (expected_heat_work**2 / sp.exp(-4 * viscosity * time)),
        force=True,
    )
    expected_heat_positive_term = (
        delta**4
        * cancellation_amplitude**2
        * (
            sp.exp(-2 * first_radius_square * viscosity * time)
            - sp.exp(-2 * second_radius_square * viscosity * time)
        )
        ** 2
    )
    need(
        sp.simplify(scaled_heat_positive_term - expected_heat_positive_term)
        == 0,
        "balanced HHL heat positive-output term",
    )
    heat_work_rate = clean(sp.diff(heat_work, time).subs(time, 0))
    expected_heat_rate = clean(
        sp.Rational(4_482_492, 1_206_545)
        * sp.sqrt(1_206_545)
        * viscosity
    )
    need(clean(heat_work_rate - expected_heat_rate) == 0, "HHL heat rate")

    nonlinear_derivative = nonlinear_vorticity_rhs(modes)
    outside_generated = set(nonlinear_derivative) - support
    need(len(nonlinear_derivative) == 24, "balanced HHL generated support")
    need(len(outside_generated) == 18, "balanced HHL outside generated support")
    for frequency, coefficient in nonlinear_derivative.items():
        need(
            sp.Matrix(frequency).dot(coefficient) == 0,
            "balanced HHL nonlinear divergence",
        )
        need(
            nonlinear_derivative.get(negate(frequency))
            == sp.conjugate(coefficient),
            "balanced HHL nonlinear reality",
        )

    surviving_outside_terms = 0
    for first_frequency in nonlinear_derivative:
        second_frequency = subtract(n, first_frequency)
        if (
            first_frequency in outside_generated
            and second_frequency in modes
            and radial_sphere_response(first_frequency, second_frequency) == 1
        ):
            surviving_outside_terms += 1
    for first_frequency in modes:
        second_frequency = subtract(n, first_frequency)
        if (
            second_frequency in outside_generated
            and radial_sphere_response(first_frequency, second_frequency) == 1
        ):
            surviving_outside_terms += 1
    need(
        surviving_outside_terms == 0,
        "sphere response removes outside-support target Qdot pairs",
    )

    linear_derivative = {
        frequency: -viscosity * frequency_square(frequency) * coefficient
        for frequency, coefficient in modes.items()
    }
    linear_target_rate = response_output_work_derivative(
        n,
        modes,
        linear_derivative,
        radial_sphere_response,
    )
    nonlinear_target_rate = response_output_work_derivative(
        n,
        modes,
        nonlinear_derivative,
        radial_sphere_response,
    )
    expected_quartic_rate = sp.Rational(4_809_249, 19_304_720)
    need(
        clean(linear_target_rate - expected_heat_rate) == 0,
        "balanced HHL linear target rate",
    )
    need(
        clean(nonlinear_target_rate - expected_quartic_rate) == 0,
        "balanced HHL quartic target rate",
    )

    scaled_target_rate = clean(
        delta**3 * linear_target_rate
        + delta**4 * nonlinear_target_rate
    )
    expected_scaled_rate = clean(
        sp.Rational(2193, 19_304_720)
        * delta**3
        * (
            2193 * delta
            + 32704 * sp.sqrt(1_206_545) * viscosity
        )
    )
    need(
        clean(scaled_target_rate - expected_scaled_rate) == 0,
        "balanced HHL scaled NSE rate",
    )

    other_target_rates = {}
    for frequency in representatives:
        if frequency == n:
            continue
        rate = response_output_work_derivative(
            frequency,
            modes,
            nonlinear_derivative,
            radial_sphere_response,
        )
        other_target_rates[frequency] = rate
    need(
        all(value == 0 for value in other_target_rates.values()),
        "balanced HHL other quartic output rates",
    )

    # Rebuild the target's complete first-order polynomial independently of
    # the differentiated covariance routine.  Generated-generated pairs are
    # O(h^2) and cannot affect the requested derivative, so enumerate exactly
    # the equal-radius pairs with at least one nonzero base coefficient.
    increment = sp.symbols("h", real=True)
    all_frequencies = support | set(nonlinear_derivative)
    target_pairs: list[tuple[Frequency, Frequency]] = []
    for first_frequency in all_frequencies:
        second_frequency = subtract(n, first_frequency)
        if (
            second_frequency in all_frequencies
            and (first_frequency in support or second_frequency in support)
            and radial_sphere_response(first_frequency, second_frequency) == 1
        ):
            target_pairs.append((first_frequency, second_frequency))
    need(len(target_pairs) == 4, "balanced HHL target first-order pairs")

    def first_order_mode(frequency: Frequency) -> sp.Matrix:
        base = modes.get(frequency, sp.zeros(3, 1))
        linear_rate = linear_derivative.get(frequency, sp.zeros(3, 1))
        nonlinear_rate = nonlinear_derivative.get(frequency, sp.zeros(3, 1))
        return (
            delta * base
            + increment
            * (delta * linear_rate + delta**2 * nonlinear_rate)
        )

    direct_strain = strain(n, first_order_mode(n))
    direct_covariance = sp.zeros(3, 3)
    for first_frequency, second_frequency in target_pairs:
        direct_covariance += outer(
            first_order_mode(first_frequency),
            first_order_mode(second_frequency),
        )
    direct_work_polynomial = 2 * sum(
        sp.conjugate(direct_strain[row, column])
        * direct_covariance[row, column]
        for row in range(3)
        for column in range(3)
    )
    direct_target_rate = clean(
        sp.diff(direct_work_polynomial, increment).subs(increment, 0)
    )
    need(
        clean(direct_target_rate - expected_scaled_rate) == 0,
        "balanced HHL direct first-order reconstruction",
    )

    return {
        "parameters": {
            "M1": first_value,
            "M2": second_value,
            "radiusSquaredM1": first_radius_square,
            "radiusSquaredM2": second_radius_square,
            "radicalSquare": first_radius_square * second_radius_square,
            "h8": as_text(h8),
            "h64": as_text(h64),
            "c0": as_text(cancellation_amplitude),
        },
        "response": "Gamma(r,s)=1 when |r|^2=|s|^2, otherwise 0",
        "support": {
            "initialSignedModes": len(modes),
            "orderedZeroSumResonances": resonance_count,
            "allInitialOutputWorksZero": True,
            "initialPositiveOutputCount": 0,
            "initialOutputWorks": {
                str(frequency): as_text(value)
                for frequency, value in initial_works.items()
            },
        },
        "heat": {
            "targetWork": (
                "delta^3*c0*exp(-2*nu*t)*"
                "(exp(-290*nu*t)-exp(-16642*nu*t))"
            ),
            "targetPositiveOutputTerm": (
                "delta^4*c0^2*"
                "(exp(-290*nu*t)-exp(-16642*nu*t))^2"
            ),
            "targetDerivativeAtZeroWithoutDelta": as_text(heat_work_rate),
            "orderedPairsContributingToTarget": heat_pair_count,
            "strictlyPositiveFor": "delta>0, nu>0, t>0",
        },
        "navierStokes": {
            "nonlinearGeneratedModes": len(nonlinear_derivative),
            "generatedModesOutsideInitialSupport": len(outside_generated),
            "outsideGeneratedPairsSurvivingTargetSphereResponse": (
                surviving_outside_terms
            ),
            "targetFirstOrderOrderedPairs": len(target_pairs),
            "linearTargetRateWithoutDelta": as_text(linear_target_rate),
            "quarticTargetRate": as_text(nonlinear_target_rate),
            "scaledTargetRate": as_text(scaled_target_rate),
            "expectedFactoredRate": (
                "2193*delta^3*(2193*delta+32704*sqrt(1206545)*nu)"
                "/19304720"
            ),
            "otherInitialSupportQuarticRates": {
                str(frequency): as_text(value)
                for frequency, value in other_target_rates.items()
            },
            "directFirstOrderReconstruction": as_text(direct_target_rate),
            "directReconstructionResidual": "0",
            "strictlyPositiveFor": "delta>0 and nu>0",
        },
        "claim": (
            "a fixed exact-radius Parseval response has zero positive output "
            "at t=0 but creates positive low-output work immediately"
        ),
    }


def shell_and_interval_audit() -> dict[str, object]:
    """Audit the shellwise conditional consumer and reverse-Cauchy boundary."""

    viscosity, dissipation, theta = sp.symbols(
        "nu D Theta", positive=True
    )
    young_residual = clean(
        viscosity * dissipation / 2
        + theta**2 / (2 * viscosity)
        - sp.sqrt(dissipation) * theta
    )
    expected_square = clean(
        (
            sp.sqrt(viscosity * dissipation)
            - theta / sp.sqrt(viscosity)
        )
        ** 2
        / 2
    )
    need(clean(young_residual - expected_square) == 0, "shell Young square")

    # Abstract one-shell path on I=[0,2*pi].  It exactly satisfies
    # b_N=Y_N'/2+D_N for nu=kappa=1, while its integrated ledger data stay
    # fixed.  This is deliberately not asserted to be an NSE trajectory.
    integer_frequency = sp.symbols("N", integer=True, positive=True)
    interval_length = 2 * sp.pi
    integrated_energy = interval_length
    integrated_dissipation = interval_length
    signed_mass = interval_length
    box_quotient = clean(signed_mass**2 / integrated_dissipation)
    consumer_lower_bound = clean(sp.pi * integer_frequency**2 / 144)
    need(box_quotient == 2 * sp.pi, "fixed signed box quotient")

    test_frequency = sp.Integer(18)
    need(
        (consumer_lower_bound.subs(integer_frequency, test_frequency) - box_quotient).is_positive
        is True,
        "reverse-Cauchy separation at N=18",
    )

    return {
        "shellQuantity": {
            "nonlinearity": "N(u,omega)=S*omega-u.grad(omega)=curl(u cross omega)",
            "injection": "b_alpha=<T_alpha omega,T_alpha N(u,omega)>",
            "shellIdentity": "(1/2)Y_alpha'+nu*D_alpha=b_alpha",
            "parsevalTotals": [
                "sum_alpha Y_alpha=||omega||_2^2=Y",
                "sum_alpha D_alpha=||grad omega||_2^2=D",
                "sum_alpha b_alpha=<omega,S omega>=P",
            ],
            "thetaSquared": "sum_{D_alpha>0}(b_alpha^+)^2/D_alpha",
            "criticalCoefficient": "A_sb,+=Theta_sb,+^2/Y",
            "consumer": "P_+<=sqrt(D)*Theta_sb,+",
            "youngSquareResidual": as_text(young_residual),
            "differentialInequality": "Y'+nu*D<=nu^(-1)*A_sb,+*Y",
            "conditionalContinuation": "integral_0^T A_sb,+(t)dt<infinity",
            "scalingExponents": {
                "Y": 1,
                "D": 3,
                "bAlpha": 3,
                "thetaSquared": 3,
                "A_sb,+": 2,
                "dt": -2,
            },
        },
        "signedIntervalObstruction": {
            "path": "Y_N=1+(1/2)sin(Nt), D_N=Y_N, b_N=(1/2)Y_N'+D_N",
            "interval": "[0,2*pi] with integer N",
            "integralY": as_text(integrated_energy),
            "integralD": as_text(integrated_dissipation),
            "signedMass": as_text(signed_mass),
            "signedBoxQuotient": as_text(box_quotient),
            "consumerLowerBound": as_text(consumer_lower_bound),
            "lowerBoundReason": (
                "on {cos(Nt)>=1/2}, measure=2*pi/3, "
                "b_N^+>=N/8 and D_N<=3/2"
            ),
            "direction": (
                "(integral_I b_alpha)^+^2/integral_I D_alpha "
                "<= integral_I (b_alpha^+)^2/D_alpha"
            ),
            "notAnNSECounterexample": True,
        },
    }


def build_certificate() -> dict[str, object]:
    partition = partition_audit()
    fourier = fourier_audit()
    normalization_discontinuity = normalization_discontinuity_audit()
    balanced_hhl = balanced_hhl_audit()
    shell = shell_and_interval_audit()
    return {
        "version": "R0.71C-independent",
        "arithmetic": "exact SymPy rationals and symbolic identities",
        "partition": partition,
        "fourier": fourier,
        "normalizationDiscontinuity": normalization_discontinuity,
        "balancedHHL": balanced_hhl,
        "shell": shell,
        "claimBoundary": {
            "proved": [
                "finite signed-before-square partition ledgers are monotone under refinement",
                "their binary refinement loss telescopes as a sum of nonnegative defects",
                (
                    "the stated full-response output parent has zero work at t=0 "
                    "and positive work immediately under Stokes flow"
                ),
                (
                    "the same smooth finite Fourier datum has "
                    "W'(0)=12*nu*epsilon^3+(76/5)*epsilon^4>0 under true NSE"
                ),
                (
                    "integrability of the complete shell-injection coefficient "
                    "A_sb,+ is a conditional continuation criterion"
                ),
                "signed interval masses give only a lower bound for the required positive square variation",
                (
                    "the same-output strain normalization is discontinuous "
                    "at a zero output strain coefficient"
                ),
                (
                    "the balanced M=8,64 HHL datum has zero initial positive "
                    "output but creates positive work under heat and true NSE"
                ),
            ],
            "notProved": [
                "failure of every adaptive or PDE-specific localization",
                "failure of a localization whose flux identity controls the refinement defects",
                (
                    "failure of every regularized denominator that remains "
                    "comparable to the same-output strain weight"
                ),
                "unconditional time integrability of A_sb,+ or of the R0.71B coefficient a_+",
                "realizability of the abstract oscillatory one-shell path by Navier-Stokes",
                "regularity or blow-up for the three-dimensional Navier-Stokes problem",
            ],
            "scope": "full-response fixed-output-node no-go plus a conditional shellwise reduction",
        },
        "status": "pass",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    certificate = build_certificate()
    serialized = json.dumps(certificate, indent=2, sort_keys=True, ensure_ascii=False)
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n", encoding="utf-8")
    print(serialized)


if __name__ == "__main__":
    main()
