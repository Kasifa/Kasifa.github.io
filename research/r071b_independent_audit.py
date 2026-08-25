#!/usr/bin/env python3
"""Independent Fourier reconstruction for R0.71B.

This checker intentionally does not import any project audit module.  It
rebuilds the strain multiplier, frame covariance convolution, full product,
resonance enumeration, and positive-output square coefficient directly from
Fourier coefficients.
"""

from __future__ import annotations

import argparse
import json
from itertools import product
from pathlib import Path

import sympy as sp


Frequency = tuple[int, int, int]


def clean(expression: sp.Expr) -> sp.Expr:
    return sp.factor(sp.cancel(sp.expand(expression)))


def need(condition: bool, label: str) -> None:
    if not condition:
        raise AssertionError(label)


def neg(frequency: Frequency) -> Frequency:
    return tuple(-entry for entry in frequency)  # type: ignore[return-value]


def add(first: Frequency, second: Frequency) -> Frequency:
    return tuple(first[index] + second[index] for index in range(3))  # type: ignore[return-value]


def square(frequency: Frequency) -> int:
    return sum(entry * entry for entry in frequency)


def outer(first: sp.Matrix, second: sp.Matrix) -> sp.Matrix:
    return first * second.T


def matrix_inner(first: sp.Matrix, second: sp.Matrix) -> sp.Expr:
    return clean(
        sum(
            first[row, column] * second[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


def cosine_modes(
    frequency: Frequency,
    coefficient: sp.Matrix,
) -> dict[Frequency, sp.Matrix]:
    return {frequency: coefficient / 2, neg(frequency): coefficient / 2}


def strain(modes: dict[Frequency, sp.Matrix]) -> dict[Frequency, sp.Matrix]:
    output: dict[Frequency, sp.Matrix] = {}
    for frequency, omega in modes.items():
        wave = sp.Matrix(frequency)
        velocity = sp.I * wave.cross(omega) / square(frequency)
        output[frequency] = (
            sp.I * (outer(wave, velocity) + outer(velocity, wave)) / 2
        ).applyfunc(clean)
    return output


def frame_gamma(first: Frequency, second: Frequency) -> sp.Integer:
    first_square = square(first)
    second_square = square(second)
    if first_square == second_square:
        return sp.Integer(1)
    high = max(first_square, second_square)
    low = min(first_square, second_square)
    if high > 16 * low:
        return sp.Integer(0)
    raise AssertionError(
        f"unresolved response pair: {first_square}, {second_square}"
    )


def convolution(
    modes: dict[Frequency, sp.Matrix],
    gamma,
) -> dict[Frequency, sp.Matrix]:
    output: dict[Frequency, sp.Matrix] = {}
    for first_frequency, first_coefficient in modes.items():
        for second_frequency, second_coefficient in modes.items():
            weight = gamma(first_frequency, second_frequency)
            if weight == 0:
                continue
            frequency = add(first_frequency, second_frequency)
            output[frequency] = output.get(frequency, sp.zeros(3, 3)) + (
                weight * outer(first_coefficient, second_coefficient)
            )
    return {
        frequency: matrix.applyfunc(clean)
        for frequency, matrix in output.items()
    }


def work(
    strain_coefficients: dict[Frequency, sp.Matrix],
    tensor_coefficients: dict[Frequency, sp.Matrix],
) -> sp.Expr:
    total = sp.Integer(0)
    for frequency, coefficient in strain_coefficients.items():
        total += matrix_inner(
            coefficient,
            tensor_coefficients.get(neg(frequency), sp.zeros(3, 3)),
        )
    return clean(total)


def resonance_count(support: set[Frequency]) -> int:
    count = 0
    for first, second in product(support, repeat=2):
        if neg(add(first, second)) in support:
            count += 1
    return count


def vector_square(vector: sp.Matrix) -> sp.Expr:
    return clean(sum(sp.conjugate(entry) * entry for entry in vector))


def matrix_square(matrix: sp.Matrix) -> sp.Expr:
    return clean(
        sum(
            sp.conjugate(matrix[row, column]) * matrix[row, column]
            for row in range(3)
            for column in range(3)
        )
    )


e1 = sp.Matrix([1, 0, 0])
e2 = sp.Matrix([0, 1, 0])
e3 = sp.Matrix([0, 0, 1])


# Same-low fan.
audit_n = 8
same_modes: dict[Frequency, sp.Matrix] = {}
same_modes.update(cosine_modes((1, 1, 0), sp.Matrix([1, -1, 0]) / sp.sqrt(2)))
same_common_expected = sp.Integer(0)

for index in range(1, audit_n + 1):
    value = 8**index
    radius_square = 2 * value**2 + 2 * value + 1
    radius = sp.sqrt(radius_square)
    p = (value, -value - 1, 0)
    q = (-value - 1, value, 0)
    a = e3 / sp.sqrt(audit_n)
    b = sp.Matrix([value, value + 1, 0]) / (radius * sp.sqrt(audit_n))
    same_modes.update(cosine_modes(p, a))
    same_modes.update(cosine_modes(q, b))
    common_symbol = clean(
        sp.sqrt(2)
        * value
        * (value + 1)
        * (2 * value + 1)
        / radius_square ** sp.Rational(3, 2)
    )
    same_common_expected += common_symbol / (4 * audit_n)

same_strain = strain(same_modes)
same_full = work(same_strain, convolution(same_modes, lambda _a, _b: 1))
same_principal = work(same_strain, convolution(same_modes, frame_gamma))
same_common = clean((same_full + same_principal) / 2)
same_chord = clean((same_full - same_principal) / 2)
need(resonance_count(set(same_modes)) == 12 * audit_n, "same-low resonances")
need(clean(same_common - same_common_expected) == 0, "same-low common work")


# Shared-high equal-radius fan.
shared_values = [16**index for index in range(1, audit_n + 1)]
shared_denominators = [1 + value**2 for value in shared_values]
shared_radius = int(sp.prod(shared_denominators))
shared_q = (shared_radius, 0, 0)
shared_low: dict[Frequency, sp.Matrix] = {}
shared_first: dict[Frequency, sp.Matrix] = {}
shared_second = cosine_modes(shared_q, e3)
shared_expected = sp.Integer(0)

for value, denominator in zip(shared_values, shared_denominators):
    n = (
        -2 * shared_radius // denominator,
        -2 * shared_radius * value // denominator,
        0,
    )
    p = (
        shared_radius * (1 - value**2) // denominator,
        2 * shared_radius * value // denominator,
        0,
    )
    c = sp.Matrix([value, -1, 0]) / sp.sqrt(denominator)
    a = sp.Matrix([-2 * value, 1 - value**2, 0]) / denominator
    shared_low.update(cosine_modes(n, c))
    shared_first.update(cosine_modes(p, a / sp.sqrt(audit_n)))
    shared_expected -= (
        sp.Rational(value, 1)
        / sp.sqrt(denominator)
        / (8 * sp.sqrt(audit_n))
    )

shared_cross: dict[Frequency, sp.Matrix] = {}
for first_frequency, first_coefficient in shared_first.items():
    for second_frequency, second_coefficient in shared_second.items():
        frequency = add(first_frequency, second_frequency)
        symmetric = (
            outer(first_coefficient, second_coefficient)
            + outer(second_coefficient, first_coefficient)
        ) / 2
        shared_cross[frequency] = shared_cross.get(
            frequency, sp.zeros(3, 3)
        ) + symmetric

shared_support = set(shared_low) | set(shared_first) | set(shared_second)
shared_work = work(strain(shared_low), shared_cross)
need(resonance_count(shared_support) == 12 * audit_n, "shared-high resonances")
need(clean(shared_work - shared_expected) == 0, "shared-high cross work")
need(
    clean(sum(vector_square(value) for value in shared_first.values()))
    == sp.Rational(1, 2),
    "shared first L2",
)
need(
    clean(sum(vector_square(value) for value in shared_second.values()))
    == sp.Rational(1, 2),
    "shared second L2",
)


# R0.71A same-covariance sign pair, rebuilt from its ten Fourier modes.
base_data = (
    ((-1, 0, -1), sp.Matrix([0, -1, 0])),
    ((-3, -3, 4), sp.Matrix([1, -1, 0]) / sp.sqrt(2)),
    ((4, 3, -3), sp.Matrix([-3, 4, 0]) / 5),
)
filler_amplitude = sp.sqrt(15 * 9985)
filler_modes: dict[Frequency, sp.Matrix] = {
    (24, 0, 0): filler_amplitude * e3 / 2,
    (-24, 0, 0): filler_amplitude * e3 / 2,
    (97, 0, 0): -sp.I * filler_amplitude * e3 / 2,
    (-97, 0, 0): sp.I * filler_amplitude * e3 / 2,
}


def r071a_modes(sign: int) -> dict[Frequency, sp.Matrix]:
    modes = dict(filler_modes)
    for frequency, coefficient in base_data:
        modes.update(cosine_modes(frequency, sign * coefficient))
    return modes


def positive_output(modes: dict[Frequency, sp.Matrix]) -> dict[str, sp.Expr]:
    strain_map = strain(modes)
    covariance_map = convolution(modes, frame_gamma)
    positive_square = sp.Integer(0)
    signed_sum = sp.Integer(0)
    nonzero_count = 0

    for frequency in sorted(strain_map):
        if not frequency > neg(frequency):
            continue
        strain_coefficient = strain_map[frequency]
        covariance_coefficient = covariance_map.get(frequency, sp.zeros(3, 3))
        output = clean(
            2
            * sp.re(
                sum(
                    sp.conjugate(strain_coefficient[row, column])
                    * covariance_coefficient[row, column]
                    for row in range(3)
                    for column in range(3)
                )
            )
        )
        signed_sum += output
        if output != 0:
            nonzero_count += 1
        if output.is_positive:
            denominator = (
                4 * square(frequency) * matrix_square(strain_coefficient)
            )
            positive_square += clean(output**2 / denominator)

    energy = clean(sum(vector_square(value) for value in modes.values()))
    return {
        "work": clean(signed_sum),
        "positiveSquare": clean(positive_square),
        "energy": energy,
        "normalized": clean(positive_square / energy),
        "nonzeroOutputCount": sp.Integer(nonzero_count),
    }


r071a_positive = positive_output(r071a_modes(1))
r071a_negative = positive_output(r071a_modes(-1))
need(r071a_positive["work"] == 3 * sp.sqrt(2) / 40, "R0.71A positive work")
need(r071a_positive["positiveSquare"] == sp.Rational(9, 800), "R0.71A positive square")
need(r071a_positive["normalized"] == sp.Rational(3, 39940400), "R0.71A positive normalized")
need(r071a_negative["work"] == -3 * sp.sqrt(2) / 40, "R0.71A negative work")
need(r071a_negative["positiveSquare"] == 0, "R0.71A negative square")


payload = {
    "release": "R0.71B",
    "status": "independent-fourier-reconstruction-passed",
    "sameLowFan": {
        "N": audit_n,
        "modeCount": len(same_modes),
        "orderedResonanceCount": resonance_count(set(same_modes)),
        "commonWorkFloat": float(same_common),
        "commonResidual": str(clean(same_common - same_common_expected)),
        "chordWorkFloat": float(same_chord),
    },
    "sharedHighFan": {
        "N": audit_n,
        "modeCount": len(shared_support),
        "orderedResonanceCount": resonance_count(shared_support),
        "crossWorkFloat": float(shared_work),
        "crossResidual": str(clean(shared_work - shared_expected)),
    },
    "r071aPositiveOutput": {
        key: str(value) for key, value in r071a_positive.items()
    },
    "r071aNegativeOutput": {
        key: str(value) for key, value in r071a_negative.items()
    },
    "claimBoundary": [
        "this checker verifies finite N=8 instances and exact R0.71A outputs",
        "the arbitrary-N fan statements still require the analytic frequency and resonance proofs in the report",
        "no Navier-Stokes evolution or continuation theorem is checked",
    ],
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    rendered = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
