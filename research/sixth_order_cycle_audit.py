#!/usr/bin/env python3
"""Exact R0.67 audit for the sixth-order periodic target at zero heat time.

The audit derives the 320-state five-carrier transfer, restricts its four-bit
cycle to the exact 36-dimensional image, computes the characteristic
polynomial over the integers, and proves that the reachable scalar sees the
dominant root.  It also records the C^2 absolute-transfer threshold needed by
the later heat-weighted problem.

This is not a certificate for the complete five-simplex heat observable.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import json
import math
import platform
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import numpy as np


CARRIES = (-2, -1, 0, 1, 2)
WORD = (0, 1, 0, 0)
DIMENSION = 320
IMAGE_DIMENSION = 36
MODULAR_PRIMES = (1_000_003, 1_000_033)

R066_QUARTIC = [1, -25, -120, 3248, -8192]
SCALED_QUARTIC = [1, -400, -30_720, 13_303_808, -536_870_912]
DEGREE_TEN = [
    1,
    -425,
    27_640,
    2_986_608,
    1_690_933_248,
    -861_945_266_176,
    79_733_131_837_440,
    19_372_471_463_444_480,
    -3_646_484_134_030_737_408,
    212_882_902_585_989_660_672,
    -495_756_246_980_944_199_680,
]
POSITIVE_CARRY_WEIGHT = [16, 83_441, 631_131, 471_851, 28_561]
EXPECTED_ABSOLUTE_CARRY_MATRIX = [
    [15, 5, 1, 0, 0],
    [7240, 5960, 4840, 3876, 3060],
    [37_390, 36_170, 34_690, 32_980, 31_076],
    [20_176, 22_400, 24_640, 26_860, 29_020],
    [715, 1001, 1365, 1820, 2380],
]


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.67 sixth +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def state_index(target_state: int, quintic_state: int, carry: int) -> int:
    return (target_state * 32 + quintic_state) * 5 + CARRIES.index(carry)


def signed_digit_transfer(bit: int, *, absolute: bool = False) -> np.ndarray:
    transfer = np.zeros((DIMENSION, DIMENSION), dtype=np.int64)
    for target_state in (0, 1):
        for quintic_state in range(32):
            for parent_carry in CARRIES:
                row = state_index(target_state, quintic_state, parent_carry)
                for epsilon in range(32):
                    digits = tuple((epsilon >> shift) & 1 for shift in (4, 3, 2, 1, 0))
                    signed_shift = sum(digits[:3]) - sum(digits[3:])
                    child_carry = 2 * parent_carry + bit - signed_shift
                    if child_carry not in CARRIES:
                        continue
                    parity = target_state * bit + (quintic_state & epsilon).bit_count()
                    sign = 1 if absolute or parity % 2 == 0 else -1
                    column = state_index(bit, epsilon, child_carry)
                    transfer[row, column] += sign
    return transfer


def cycle_matrix(transfers: list[np.ndarray]) -> np.ndarray:
    cycle = np.eye(DIMENSION, dtype=np.int64)
    for bit in WORD:
        cycle = transfers[bit] @ cycle
    return cycle


def modular_pivots(matrix: np.ndarray, prime: int) -> list[int]:
    work = np.remainder(matrix, prime).astype(np.int64).copy()
    rows, columns = work.shape
    pivot_row = 0
    pivots: list[int] = []
    for column in range(columns):
        candidates = np.flatnonzero(work[pivot_row:, column])
        if not candidates.size:
            continue
        selected = pivot_row + int(candidates[0])
        work[[pivot_row, selected]] = work[[selected, pivot_row]]
        inverse = pow(int(work[pivot_row, column]), -1, prime)
        work[pivot_row] = (work[pivot_row] * inverse) % prime
        if pivot_row + 1 < rows:
            factors = work[pivot_row + 1 :, column].copy()
            nonzero = np.flatnonzero(factors)
            if nonzero.size:
                affected = pivot_row + 1 + nonzero
                work[affected] = (
                    work[affected] - factors[nonzero, None] * work[pivot_row]
                ) % prime
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivots


def modular_rank(matrix: np.ndarray, prime: int) -> int:
    return len(modular_pivots(matrix, prime))


def solve_square_multiple(
    left: list[list[int]], right: list[list[int]]
) -> list[list[Fraction]]:
    size = len(left)
    augmented = [
        [Fraction(value) for value in left[row]]
        + [Fraction(value) for value in right[row]]
        for row in range(size)
    ]
    for column in range(size):
        pivot = next(
            (row for row in range(column, size) if augmented[row][column]),
            None,
        )
        if pivot is None:
            raise AssertionError("singular image coordinate matrix")
        augmented[column], augmented[pivot] = augmented[pivot], augmented[column]
        scale = augmented[column][column]
        augmented[column] = [value / scale for value in augmented[column]]
        for row in range(size):
            if row == column or augmented[row][column] == 0:
                continue
            factor = augmented[row][column]
            augmented[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(augmented[row], augmented[column])
            ]
    return [row[size:] for row in augmented]


def image_restriction(cycle: np.ndarray) -> tuple[np.ndarray, dict[str, object]]:
    columns = modular_pivots(cycle, MODULAR_PRIMES[0])
    if len(columns) != IMAGE_DIMENSION:
        raise AssertionError(f"unexpected image rank {len(columns)}")
    basis = cycle[:, columns]
    rows = modular_pivots(basis.T, MODULAR_PRIMES[0])
    if len(rows) != IMAGE_DIMENSION:
        raise AssertionError("failed to select image coordinates")
    coordinate = basis[rows, :].tolist()
    image = (cycle @ basis)[rows, :].tolist()
    rational = solve_square_multiple(coordinate, image)
    if any(value.denominator != 1 for row in rational for value in row):
        raise AssertionError("nonintegral image restriction")
    restricted = np.array(
        [[int(value) for value in row] for row in rational], dtype=np.int64
    )
    if not np.array_equal(basis @ restricted, cycle @ basis):
        raise AssertionError("image restriction reconstruction failed")
    return restricted, {
        "basisColumns": columns,
        "coordinateRows": rows,
        "coordinateDeterminantNonzeroModulo": {
            str(prime): modular_rank(basis[rows, :], prime) == IMAGE_DIMENSION
            for prime in MODULAR_PRIMES
        },
    }


def int_matrix_multiply(
    left: list[list[int]], right: list[list[int]]
) -> list[list[int]]:
    size = len(left)
    output = [[0] * size for _ in range(size)]
    for row in range(size):
        for pivot, coefficient in enumerate(left[row]):
            if coefficient == 0:
                continue
            for column, value in enumerate(right[pivot]):
                if value:
                    output[row][column] += coefficient * value
    return output


def characteristic_polynomial(matrix: np.ndarray) -> list[int]:
    source = [[int(value) for value in row] for row in matrix.tolist()]
    size = len(source)
    auxiliary = [[int(row == column) for column in range(size)] for row in range(size)]
    coefficients = [1]
    for degree in range(1, size + 1):
        product = int_matrix_multiply(source, auxiliary)
        trace = sum(product[index][index] for index in range(size))
        if trace % degree:
            raise AssertionError("Faddeev--LeVerrier coefficient is not integral")
        coefficient = -trace // degree
        coefficients.append(coefficient)
        for index in range(size):
            product[index][index] += coefficient
        auxiliary = product
    if any(auxiliary[row][column] for row in range(size) for column in range(size)):
        raise AssertionError("Cayley--Hamilton residual is nonzero")
    return coefficients


def polynomial_multiply(left: list[int], right: list[int]) -> list[int]:
    output = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            output[left_index + right_index] += left_value * right_value
    return output


def polynomial_power(polynomial: list[int], exponent: int) -> list[int]:
    output = [1]
    for _ in range(exponent):
        output = polynomial_multiply(output, polynomial)
    return output


def expected_image_characteristic() -> list[int]:
    output = polynomial_power([1, 0], 5)
    output = polynomial_multiply(output, polynomial_power([1, -256], 5))
    output = polynomial_multiply(output, polynomial_power(SCALED_QUARTIC, 4))
    return polynomial_multiply(output, DEGREE_TEN)


def evaluate_matrix_polynomial_mod(
    coefficients: list[int], matrix: np.ndarray, prime: int
) -> np.ndarray:
    size = len(matrix)
    source = matrix % prime
    output = np.zeros_like(source)
    identity = np.eye(size, dtype=np.int64)
    for coefficient in coefficients:
        output = (output @ source + (coefficient % prime) * identity) % prime
    return output


def evaluate_polynomial(coefficients: list[int], value: int | Fraction) -> int | Fraction:
    result: int | Fraction = 0
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def rudin_shapiro_pair(level: int) -> tuple[list[int], list[int]]:
    p = [1]
    q = [1]
    for _ in range(level):
        p, q = p + q, p + [-value for value in q]
    return p, q


def exact_convolve(left: list[int], right: list[int]) -> list[int]:
    output = [0] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            output[left_index + right_index] += left_value * right_value
    return output


def quintic_states(level: int) -> list[list[int]]:
    pair = rudin_shapiro_pair(level)
    states: list[list[int]] = []
    for sigma in range(32):
        factors = [pair[(sigma >> shift) & 1] for shift in (4, 3, 2, 1, 0)]
        factors[3] = list(reversed(factors[3]))
        factors[4] = list(reversed(factors[4]))
        value = factors[0]
        for factor in factors[1:]:
            value = exact_convolve(value, factor)
        states.append(value)
    return states


def initial_vector() -> np.ndarray:
    vector = np.zeros(DIMENSION, dtype=np.int64)
    for target_state in (0, 1):
        for quintic_state in range(32):
            vector[state_index(target_state, quintic_state, 0)] = 1
    return vector


def repeated_word_target(level: int) -> tuple[list[int], int]:
    bits = [WORD[index % 4] for index in range(level)]
    return bits, sum(bit << index for index, bit in enumerate(bits))


def direct_transfer_audit(
    transfers: list[np.ndarray], maximum_level: int
) -> list[dict[str, int]]:
    records: list[dict[str, int]] = []
    for level in range(1, maximum_level + 1):
        bits, target = repeated_word_target(level)
        vector = initial_vector()
        for bit in bits:
            vector = transfers[bit] @ vector
        pair = rudin_shapiro_pair(level)
        quintics = quintic_states(level)
        length = 1 << level
        offset = 2 * (length - 1)
        for target_state in (0, 1):
            target_sign = pair[target_state][target]
            for quintic_state in range(32):
                for carry in CARRIES:
                    exponent = target + carry * length
                    array_index = exponent + offset
                    direct = (
                        0
                        if not 0 <= array_index < len(quintics[quintic_state])
                        else target_sign * quintics[quintic_state][array_index]
                    )
                    recursive = int(vector[state_index(target_state, quintic_state, carry)])
                    if direct != recursive:
                        raise AssertionError(
                            "five-carrier transfer mismatch "
                            f"level={level} state={(target_state, quintic_state, carry)}"
                        )
        records.append(
            {
                "level": level,
                "M": length,
                "target": target,
                "maximumAbsoluteState": int(np.max(np.abs(vector))),
            }
        )
    return records


def exact_scalar_sequence(cycle: np.ndarray, terms: int) -> list[int]:
    sparse_rows = [
        [(column, int(value)) for column, value in enumerate(row) if value]
        for row in cycle.tolist()
    ]
    vector = [int(value) for value in initial_vector()]
    output: list[int] = []
    observable = state_index(0, 0, 0)
    for _ in range(terms):
        output.append(vector[observable])
        vector = [
            sum(coefficient * vector[column] for column, coefficient in row)
            for row in sparse_rows
        ]
    return output


def polynomial_trim(polynomial: list[Fraction]) -> list[Fraction]:
    result = polynomial[:]
    while len(result) > 1 and result[-1] == 0:
        result.pop()
    return result


def polynomial_divmod(
    dividend: list[Fraction], divisor: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    remainder = polynomial_trim(dividend)
    divisor = polynomial_trim(divisor)
    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and remainder != [0]:
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree] += coefficient
        for index, value in enumerate(divisor):
            remainder[index + degree] -= coefficient * value
        remainder = polynomial_trim(remainder)
    return polynomial_trim(quotient), remainder


def polynomial_gcd(
    left: list[int | Fraction], right: list[int | Fraction]
) -> list[Fraction]:
    a = [Fraction(value) for value in left]
    b = [Fraction(value) for value in right]
    while polynomial_trim(b) != [0]:
        _, remainder = polynomial_divmod(a, b)
        a, b = b, remainder
    a = polynomial_trim(a)
    leading = a[-1]
    return [value / leading for value in a]


def reachable_generating_data(sequence: list[int]) -> dict[str, object]:
    recurrence = polynomial_multiply(
        polynomial_multiply([1, -256], SCALED_QUARTIC), DEGREE_TEN
    )
    if len(recurrence) != 16:
        raise AssertionError("unexpected reachable recurrence degree")
    residuals = [
        sum(recurrence[index] * sequence[n - index] for index in range(16))
        for n in range(15, len(sequence))
    ]
    numerator = [
        sum(recurrence[index] * sequence[degree - index] for index in range(degree + 1))
        for degree in range(16)
    ]
    gcd = polynomial_gcd(recurrence, numerator)
    return {
        "recurrenceCharacteristicDescending": recurrence,
        "recurrenceResidualAtR15": residuals[0],
        "recurrenceResidualsFromR16AreZero": all(value == 0 for value in residuals[1:]),
        "generatingDenominatorAscending": recurrence,
        "generatingNumeratorAscending": numerator,
        "generatingGcdAscending": [
            int(value) if value.denominator == 1 else str(value) for value in gcd
        ],
    }


def interval_multiply(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    values = (
        left[0] * right[0],
        left[0] * right[1],
        left[1] * right[0],
        left[1] * right[1],
    )
    return min(values), max(values)


def interval_horner(
    coefficients: list[int], interval: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    result = (Fraction(coefficients[0]), Fraction(coefficients[0]))
    for coefficient in coefficients[1:]:
        product = interval_multiply(result, interval)
        result = product[0] + coefficient, product[1] + coefficient
    return result


def interval_divide_negative(
    negative_numerator: tuple[Fraction, Fraction],
    negative_denominator: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    if not (
        negative_numerator[1] < 0
        and negative_denominator[1] < 0
    ):
        raise AssertionError("projection sign enclosure lost negativity")
    candidates = [
        -negative_numerator[i] / negative_denominator[j]
        for i in (0, 1)
        for j in (0, 1)
    ]
    return min(candidates), max(candidates)


def decimal_display(value: Fraction, digits: int = 24) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def dominant_projection_interval(
    generating: dict[str, object]
) -> dict[str, object]:
    lower = Fraction(402_425_429_345_624, 10**12)
    upper = Fraction(4_024_254_293_456_256, 10**13)
    root_interval = (lower, upper)
    numerator = [int(value) for value in generating["generatingNumeratorAscending"]]
    recurrence = [
        int(value) for value in generating["generatingDenominatorAscending"]
    ]
    numerator_reversed = numerator
    derivative_reversed = [
        index * recurrence[index] for index in range(1, len(recurrence))
    ]
    numerator_interval = interval_horner(numerator_reversed, root_interval)
    derivative_interval = interval_horner(derivative_reversed, root_interval)
    coefficient_interval = interval_divide_negative(
        numerator_interval, derivative_interval
    )
    return {
        "dominantRootLower": str(lower),
        "dominantRootUpper": str(upper),
        "scaledQuarticAtLower": str(evaluate_polynomial(SCALED_QUARTIC, lower)),
        "scaledQuarticAtUpper": str(evaluate_polynomial(SCALED_QUARTIC, upper)),
        "projectionNumeratorInterval": [str(value) for value in numerator_interval],
        "projectionDenominatorInterval": [str(value) for value in derivative_interval],
        "coefficientLower": str(coefficient_interval[0]),
        "coefficientUpper": str(coefficient_interval[1]),
        "coefficientLowerDisplay": decimal_display(coefficient_interval[0]),
        "coefficientUpperDisplay": decimal_display(coefficient_interval[1]),
        "coefficientIsNegative": coefficient_interval[1] < 0,
    }


def schur_disk_certificate(coefficients: list[int], radius: int) -> list[dict[str, object]]:
    degree = len(coefficients) - 1
    current = [
        coefficient * radius ** (degree - index)
        for index, coefficient in enumerate(coefficients)
    ]
    records: list[dict[str, object]] = []
    while len(current) > 1:
        leading = current[0]
        constant = current[-1]
        strict = abs(leading) > abs(constant)
        records.append(
            {
                "degree": len(current) - 1,
                "leadingAbs": str(abs(leading)),
                "constantAbs": str(abs(constant)),
                "strictSchurInequality": strict,
                "coefficientSha256": hashlib.sha256(
                    json.dumps(current, separators=(",", ":")).encode()
                ).hexdigest(),
            }
        )
        if not strict:
            raise AssertionError("Schur transform failed")
        reversed_coefficients = list(reversed(current))
        transformed = [
            leading * value - constant * reverse
            for value, reverse in zip(current, reversed_coefficients)
        ][:-1]
        divisor = functools.reduce(
            math.gcd, (abs(value) for value in transformed if value)
        )
        current = [value // divisor for value in transformed]
        if current[0] < 0:
            current = [-value for value in current]
    return records


def absolute_carry_audit() -> dict[str, object]:
    absolute_cycle = cycle_matrix(
        [signed_digit_transfer(0, absolute=True), signed_digit_transfer(1, absolute=True)]
    )
    carry_matrix: list[list[int]] = []
    for parent_carry in CARRIES:
        row = state_index(0, 0, parent_carry)
        carry_matrix.append(
            [
                int(
                    absolute_cycle[
                        row,
                        [
                            state_index(target_state, quintic_state, child_carry)
                            for target_state in (0, 1)
                            for quintic_state in range(32)
                        ],
                    ].sum()
                )
                for child_carry in CARRIES
            ]
        )
    for target_state in (0, 1):
        for quintic_state in range(32):
            for row_index, parent_carry in enumerate(CARRIES):
                row = state_index(target_state, quintic_state, parent_carry)
                aggregate = [
                    int(
                        absolute_cycle[
                            row,
                            [
                                state_index(child_target, child_quintic, child_carry)
                                for child_target in (0, 1)
                                for child_quintic in range(32)
                            ],
                        ].sum()
                    )
                    for child_carry in CARRIES
                ]
                if aggregate != carry_matrix[row_index]:
                    raise AssertionError("absolute carry aggregation depends on sign state")
    image = [
        sum(carry_matrix[row][column] * POSITIVE_CARRY_WEIGHT[column] for column in range(5))
        for row in range(5)
    ]
    expected = [65_536 * value for value in POSITIVE_CARRY_WEIGHT]
    return {
        "carryMatrix": carry_matrix,
        "positiveCarryWeight": POSITIVE_CARRY_WEIGHT,
        "weightedImage": image,
        "eigenvalue": 65_536,
        "secondDerivativeSpatialContraction": "1/16^2",
        "C2ZeroAffineThreshold": 256,
        "checks": {
            "carryMatrixMatches": carry_matrix == EXPECTED_ABSOLUTE_CARRY_MATRIX,
            "positiveWeightEigenvectorIsExact": image == expected,
            "C2ThresholdIsBelowDominantRootLower": Fraction(256) < Fraction(
                402_425_429_345_624, 10**12
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-direct-level", type=int, default=7)
    parser.add_argument("--sequence-terms", type=int, default=40)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    progress(arguments.progress, started, "building signed digit transfers")
    transfers = [signed_digit_transfer(0), signed_digit_transfer(1)]
    cycle = cycle_matrix(transfers)
    digit_ranks = {
        str(prime): [modular_rank(transfer, prime) for transfer in transfers]
        for prime in MODULAR_PRIMES
    }
    cycle_ranks = {
        str(prime): [
            modular_rank(cycle, prime),
            modular_rank(cycle @ cycle, prime),
            modular_rank(cycle @ cycle @ cycle, prime),
        ]
        for prime in MODULAR_PRIMES
    }

    progress(arguments.progress, started, "restricting exact image")
    restricted, image_metadata = image_restriction(cycle)
    characteristic = characteristic_polynomial(restricted)
    expected_characteristic = expected_image_characteristic()

    primary_nullities: dict[str, dict[str, int]] = {}
    identity = np.eye(IMAGE_DIMENSION, dtype=np.int64)
    for prime in MODULAR_PRIMES:
        primary_nullities[str(prime)] = {
            "zero": IMAGE_DIMENSION - modular_rank(restricted, prime),
            "twoFiftySix": IMAGE_DIMENSION
            - modular_rank(restricted - 256 * identity, prime),
            "scaledQuartic": IMAGE_DIMENSION
            - modular_rank(
                evaluate_matrix_polynomial_mod(SCALED_QUARTIC, restricted, prime),
                prime,
            ),
            "degreeTen": IMAGE_DIMENSION
            - modular_rank(
                evaluate_matrix_polynomial_mod(DEGREE_TEN, restricted, prime),
                prime,
            ),
        }

    progress(arguments.progress, started, "checking direct five-carrier convolutions")
    direct = direct_transfer_audit(transfers, arguments.max_direct_level)

    progress(arguments.progress, started, "isolating reachable scalar")
    sequence = exact_scalar_sequence(cycle, arguments.sequence_terms)
    generating = reachable_generating_data(sequence)
    projection = dominant_projection_interval(generating)

    broad_root_intervals = [(-208, -192), (48, 64), (128, 144), (400, 416)]
    broad_root_signs = [
        [
            int(evaluate_polynomial(SCALED_QUARTIC, lower)),
            int(evaluate_polynomial(SCALED_QUARTIC, upper)),
        ]
        for lower, upper in broad_root_intervals
    ]
    schur = schur_disk_certificate(DEGREE_TEN, 300)
    absolute = absolute_carry_audit()

    scaled_identity = [
        R066_QUARTIC[index] * 16**index
        for index in range(len(R066_QUARTIC))
    ]
    checks = {
        "stateDimensionIsTwoTimesThirtyTwoTimesFive": DIMENSION == 2 * 32 * 5,
        "digitRanksAreEightyOverTwoPrimes": all(
            ranks == [80, 80] for ranks in digit_ranks.values()
        ),
        "cycleRanksAreThirtySixThenThirtyOne": all(
            ranks == [36, 31, 31] for ranks in cycle_ranks.values()
        ),
        "imageRestrictionIsIntegral": restricted.dtype == np.int64,
        "imageCharacteristicPolynomialMatchesFactorization": characteristic
        == expected_characteristic,
        "primaryNullitiesMatchAlgebraicMultiplicities": all(
            nullities
            == {"zero": 5, "twoFiftySix": 5, "scaledQuartic": 16, "degreeTen": 10}
            for nullities in primary_nullities.values()
        ),
        "directConvolutionMatchesAllThreeHundredTwentyStates": len(direct)
        == arguments.max_direct_level,
        "reachableRecurrenceStartsAfterOneTransient": bool(
            generating["recurrenceResidualAtR15"]
        )
        and bool(generating["recurrenceResidualsFromR16AreZero"]),
        "reachableGeneratingFunctionIsReduced": generating[
            "generatingGcdAscending"
        ]
        == [1],
        "scaledQuarticIsSixteenRescalingOfR066Polynomial": scaled_identity
        == SCALED_QUARTIC,
        "scaledQuarticHasFourSeparatedRealRoots": all(
            left * right < 0 for left, right in broad_root_signs
        ),
        "degreeTenFactorIsStrictlyInsideRadiusThreeHundred": all(
            record["strictSchurInequality"] for record in schur
        ),
        "dominantProjectionCoefficientIsStrictlyNegative": bool(
            projection["coefficientIsNegative"]
        ),
        "absoluteCarryWeightAndC2ThresholdAreExact": all(
            absolute["checks"].values()
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "exact zero-time sixth-order five-carrier transfer theorem and "
            "C2 remainder ingredient; not a certificate for the complete "
            "five-simplex heat observable or the full Picard series"
        ),
        "checks": checks,
        "pathFormula": {
            "signPattern": "A+B+C-D-E=Q",
            "positiveCarriers": 3,
            "negativeCarriers": 2,
            "timeOrderSignPlacements": 10,
            "fourFreeCarrierIndices": True,
            "sixthFourierPrefactor": "-i m^5 exp(-m^2 t_H) H^-10",
            "normalizedRatio": (
                "A^6 G6/(A^2 G2)=(epsilon^4/L^4) R6, "
                "R6=L^4 m^4 S6/(H^6 S2)"
            ),
        },
        "stateSpace": {
            "targetSignStates": 2,
            "quinticSignStates": 32,
            "carries": list(CARRIES),
            "dimension": DIMENSION,
            "digitRanksByPrime": digit_ranks,
        },
        "cycle": {
            "wordLeastSignificantBitFirst": list(WORD),
            "rankThenSquareThenCubeByPrime": cycle_ranks,
            "imageDimension": IMAGE_DIMENSION,
            "imageRestrictionMetadata": image_metadata,
            "imageCharacteristicPolynomialDescending": characteristic,
            "imageCharacteristicFactorization": (
                "x^5 (x-256)^5 "
                "(x^4-400x^3-30720x^2+13303808x-536870912)^4 "
                "(x^10-425x^9+27640x^8+2986608x^7+1690933248x^6"
                "-861945266176x^5+79733131837440x^4"
                "+19372471463444480x^3-3646484134030737408x^2"
                "+212882902585989660672x-495756246980944199680)"
            ),
            "fullCharacteristicFactorization": (
                "x^289 (x-256)^5 "
                "(x^4-400x^3-30720x^2+13303808x-536870912)^4 "
                "(degree-ten factor)"
            ),
            "primaryNullitiesByPrime": primary_nullities,
            "scaledQuarticRootIntervals": [
                list(interval) for interval in broad_root_intervals
            ],
            "scaledQuarticEndpointValues": broad_root_signs,
            "degreeTenSchurRadius": 300,
            "degreeTenSchurCertificate": schur,
            "dominantRoot": (
                "mu is the unique root in (400,416) of the scaled quartic; "
                "mu=16 lambda from R0.66"
            ),
        },
        "reachableTargetFamily": {
            "M": "16^r",
            "q": "2(16^r-1)/15",
            "initialValues": sequence,
            **generating,
            "dominantProjection": projection,
            "asymptotic": (
                "Y_r=C6,0 mu^r+O(300^r), "
                "C6,0 is in the recorded strict negative interval"
            ),
            "criticalSixthThreshold": "M_r^2=256^r",
            "consequence": "|Y_r|/M_r^2 tends to infinity",
        },
        "absoluteTransfer": absolute,
        "directAudit": {
            "exactLevelsChecked": arguments.max_direct_level,
            "records": direct,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "randomness": False,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
    temporary.write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(arguments.output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
