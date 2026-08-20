#!/usr/bin/env python3
"""Exact audit for the R0.64 zero-time supercritical transfer cycle.

All transfer matrices, ranks, image restrictions, characteristic
polynomials, direct convolution checks, and scalar recurrences use Python
integer or Fraction arithmetic.  Floating-point roots are display-only.
The result obstructs a pointwise common norm; it does not decide the
Gaussian-weighted simplex integral.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import platform
import time
from fractions import Fraction
from pathlib import Path

import numpy as np


CARRIES = (-1, 0, 1)
WORD = (0, 1, 0, 0)


def state_index(target_state: int, cubic_state: int, carry: int) -> int:
    return (target_state * 8 + cubic_state) * 3 + CARRIES.index(carry)


def zero_matrix(rows: int, columns: int) -> list[list[int]]:
    return [[0 for _ in range(columns)] for _ in range(rows)]


def identity(size: int) -> list[list[int]]:
    output = zero_matrix(size, size)
    for index in range(size):
        output[index][index] = 1
    return output


def matrix_multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    rows = len(left)
    middle = len(right)
    columns = len(right[0])
    output = zero_matrix(rows, columns)
    for row in range(rows):
        for pivot in range(middle):
            coefficient = left[row][pivot]
            if coefficient == 0:
                continue
            for column, value in enumerate(right[pivot]):
                if value:
                    output[row][column] += coefficient * value
    return output


def matrix_vector(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [sum(value * vector[column] for column, value in enumerate(row)) for row in matrix]


def digit_transfer(bit: int) -> list[list[int]]:
    transfer = zero_matrix(48, 48)
    for target_state in (0, 1):
        for cubic_state in range(8):
            for parent_carry in CARRIES:
                row = state_index(target_state, cubic_state, parent_carry)
                for epsilon in range(8):
                    epsilon_a = (epsilon >> 2) & 1
                    epsilon_b = (epsilon >> 1) & 1
                    epsilon_c = epsilon & 1
                    shift = epsilon_a + epsilon_b - epsilon_c
                    child_carry = 2 * parent_carry + bit - shift
                    if child_carry not in CARRIES:
                        continue
                    parity = target_state * bit + (cubic_state & epsilon).bit_count()
                    sign = -1 if parity % 2 else 1
                    column = state_index(bit, epsilon, child_carry)
                    transfer[row][column] += sign
    return transfer


def rational_rank(matrix: list[list[int | Fraction]]) -> int:
    if not matrix:
        return 0
    work = [[Fraction(value) for value in row] for row in matrix]
    rows = len(work)
    columns = len(work[0])
    pivot_row = 0
    for column in range(columns):
        pivot = next((row for row in range(pivot_row, rows) if work[row][column]), None)
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(rows):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivot_row


def independent_columns(matrix: list[list[int]]) -> list[list[int]]:
    selected: list[list[int]] = []
    current_rank = 0
    for column in range(len(matrix[0])):
        candidate = [matrix[row][column] for row in range(len(matrix))]
        trial = selected + [candidate]
        trial_matrix = [[vector[row] for vector in trial] for row in range(len(matrix))]
        new_rank = rational_rank(trial_matrix)
        if new_rank > current_rank:
            selected.append(candidate)
            current_rank = new_rank
    return selected


def independent_rows(columns: list[list[int]]) -> list[int]:
    selected: list[int] = []
    current_rank = 0
    for row in range(len(columns[0])):
        trial = selected + [row]
        matrix = [[columns[column][index] for column in range(len(columns))] for index in trial]
        new_rank = rational_rank(matrix)
        if new_rank > current_rank:
            selected.append(row)
            current_rank = new_rank
        if current_rank == len(columns):
            return selected
    raise AssertionError("failed to select independent image rows")


def solve_square(matrix: list[list[int]], target: list[int]) -> list[Fraction]:
    size = len(matrix)
    work = [
        [Fraction(value) for value in row] + [Fraction(target[index])]
        for index, row in enumerate(matrix)
    ]
    for column in range(size):
        pivot = next((row for row in range(column, size) if work[row][column]), None)
        if pivot is None:
            raise AssertionError("singular coordinate matrix")
        work[column], work[pivot] = work[pivot], work[column]
        scale = work[column][column]
        work[column] = [value / scale for value in work[column]]
        for row in range(size):
            if row == column or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[column])
            ]
    return [work[row][-1] for row in range(size)]


def image_restriction(matrix: list[list[int]]) -> tuple[list[list[int]], int]:
    basis_columns = independent_columns(matrix)
    rank = len(basis_columns)
    rows = independent_rows(basis_columns)
    coordinate_matrix = [
        [basis_columns[column][row] for column in range(rank)] for row in rows
    ]
    restricted_columns: list[list[Fraction]] = []
    for basis in basis_columns:
        image = matrix_vector(matrix, basis)
        coordinates = solve_square(coordinate_matrix, [image[row] for row in rows])
        reconstructed = [
            sum(coordinates[column] * basis_columns[column][row] for column in range(rank))
            for row in range(len(matrix))
        ]
        if reconstructed != [Fraction(value) for value in image]:
            raise AssertionError("image coordinate reconstruction failed")
        restricted_columns.append(coordinates)
    restricted = [
        [restricted_columns[column][row] for column in range(rank)]
        for row in range(rank)
    ]
    if any(value.denominator != 1 for row in restricted for value in row):
        raise AssertionError("nonintegral image restriction")
    return [[int(value) for value in row] for row in restricted], rank


def polynomial_multiply(left: list[Fraction], right: list[Fraction]) -> list[Fraction]:
    output = [Fraction(0)] * (len(left) + len(right) - 1)
    for left_index, left_value in enumerate(left):
        for right_index, right_value in enumerate(right):
            output[left_index + right_index] += left_value * right_value
    return output


def permutation_sign(permutation: tuple[int, ...]) -> int:
    inversions = sum(
        permutation[left] > permutation[right]
        for left in range(len(permutation))
        for right in range(left + 1, len(permutation))
    )
    return -1 if inversions % 2 else 1


def characteristic_polynomial(matrix: list[list[int]]) -> list[int]:
    size = len(matrix)
    result = [Fraction(0)] * (size + 1)
    for permutation in itertools.permutations(range(size)):
        term = [Fraction(1)]
        for row, column in enumerate(permutation):
            factor = [Fraction(-matrix[row][column])]
            if row == column:
                factor.append(Fraction(1))
            term = polynomial_multiply(term, factor)
            if all(value == 0 for value in term):
                break
        sign = permutation_sign(permutation)
        for index, value in enumerate(term):
            result[index] += sign * value
    if any(value.denominator != 1 for value in result):
        raise AssertionError("nonintegral characteristic polynomial")
    return [int(value) for value in result]


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


def cubic_states(level: int) -> list[list[int]]:
    pair = rudin_shapiro_pair(level)
    states: list[list[int]] = []
    for sigma in range(8):
        first = pair[(sigma >> 2) & 1]
        second = pair[(sigma >> 1) & 1]
        third = pair[sigma & 1]
        states.append(exact_convolve(exact_convolve(first, second), list(reversed(third))))
    return states


def initial_vector() -> list[int]:
    vector = [0] * 48
    for target_state in (0, 1):
        for cubic_state in range(8):
            vector[state_index(target_state, cubic_state, 0)] = 1
    return vector


def repeated_word_target(level: int) -> tuple[list[int], int]:
    bits = [WORD[index % len(WORD)] for index in range(level)]
    target = sum(bit << index for index, bit in enumerate(bits))
    return bits, target


def direct_transfer_audit(transfers: list[list[list[int]]], max_level: int) -> list[dict[str, int]]:
    records: list[dict[str, int]] = []
    for level in range(1, max_level + 1):
        bits, target = repeated_word_target(level)
        vector = initial_vector()
        for bit in bits:
            vector = matrix_vector(transfers[bit], vector)
        pair = rudin_shapiro_pair(level)
        cubics = cubic_states(level)
        length = 1 << level
        offset = length - 1
        for target_state in (0, 1):
            target_sign = pair[target_state][target]
            for cubic_state in range(8):
                for carry in CARRIES:
                    exponent = target + carry * length
                    index = exponent + offset
                    direct = 0 if not 0 <= index < len(cubics[cubic_state]) else target_sign * cubics[cubic_state][index]
                    recursive = vector[state_index(target_state, cubic_state, carry)]
                    if direct != recursive:
                        raise AssertionError(
                            f"transfer mismatch level={level} target={target} "
                            f"state={(target_state, cubic_state, carry)}"
                        )
        records.append(
            {
                "level": level,
                "M": length,
                "target": target,
                "maximumAbsoluteState": max(abs(value) for value in vector),
            }
        )
    return records


def polynomial_trim(polynomial: list[Fraction]) -> list[Fraction]:
    output = polynomial[:]
    while len(output) > 1 and output[-1] == 0:
        output.pop()
    return output


def polynomial_divmod(
    dividend: list[Fraction], divisor: list[Fraction]
) -> tuple[list[Fraction], list[Fraction]]:
    remainder = polynomial_trim(dividend)
    divisor = polynomial_trim(divisor)
    if divisor == [0]:
        raise ZeroDivisionError
    quotient = [Fraction(0)] * max(1, len(remainder) - len(divisor) + 1)
    while len(remainder) >= len(divisor) and remainder != [0]:
        degree = len(remainder) - len(divisor)
        coefficient = remainder[-1] / divisor[-1]
        quotient[degree] += coefficient
        for index, value in enumerate(divisor):
            remainder[index + degree] -= coefficient * value
        remainder = polynomial_trim(remainder)
    return polynomial_trim(quotient), remainder


def polynomial_gcd(left: list[int], right: list[int]) -> list[Fraction]:
    a = [Fraction(value) for value in left]
    b = [Fraction(value) for value in right]
    while polynomial_trim(b) != [0]:
        _, remainder = polynomial_divmod(a, b)
        a, b = b, remainder
    a = polynomial_trim(a)
    leading = a[-1]
    return [value / leading for value in a]


def evaluate_quartic(value: int) -> int:
    return value**4 - 25 * value**3 - 120 * value**2 + 3248 * value - 8192


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-direct-level", type=int, default=10)
    arguments = parser.parse_args()
    started = time.perf_counter()

    transfers = [digit_transfer(0), digit_transfer(1)]
    transfer_ranks = [rational_rank(matrix) for matrix in transfers]
    cycle = identity(48)
    for bit in WORD:
        cycle = matrix_multiply(transfers[bit], cycle)

    restricted, cycle_rank = image_restriction(cycle)
    characteristic = characteristic_polynomial(restricted)
    expected_characteristic = [-2097152, 1093632, -142848, 688, 936, -57, 1]

    direct_records = direct_transfer_audit(transfers, arguments.max_direct_level)

    vector = initial_vector()
    cycle_values = [vector[state_index(0, 0, 0)]]
    for _ in range(15):
        vector = matrix_vector(cycle, vector)
        cycle_values.append(vector[state_index(0, 0, 0)])

    recurrence = [41, -280, -5168, 60160, -131072]
    recurrence_ok = all(
        cycle_values[index]
        == sum(
            recurrence[lag] * cycle_values[index - 1 - lag]
            for lag in range(len(recurrence))
        )
        for index in range(6, len(cycle_values))
    )
    numerator = [1, -19, -348, 5760, -24576, 32768]
    denominator = [1, -41, 280, 5168, -60160, 131072]
    generating_gcd = polynomial_gcd(numerator, denominator)

    roots = np.roots([1.0, -25.0, -120.0, 3248.0, -8192.0])
    real_roots = sorted(float(root.real) for root in roots if abs(root.imag) < 1.0e-9)
    dominant = max(real_roots)
    exponent = math.log(dominant, 16.0)

    root_intervals = [(-13, -12), (3, 4), (8, 9), (25, 26)]
    interval_sign_changes = [
        evaluate_quartic(left) * evaluate_quartic(right) < 0
        for left, right in root_intervals
    ]

    checks = {
        "digitTransferRanksAreTwelve": transfer_ranks == [12, 12],
        "cycleRankIsSix": cycle_rank == 6,
        "exactImageCharacteristicPolynomialMatches": characteristic
        == expected_characteristic,
        "directConvolutionMatchesAllFortyEightStates": len(direct_records)
        == arguments.max_direct_level,
        "quarticHasCertifiedRootInEachInterval": all(interval_sign_changes),
        "dominantCycleEigenvalueExceedsTwentyFive": 25.0 < dominant < 26.0,
        "cycleGrowthExceedsPointwiseThreshold": dominant > 16.0,
        "reachableScalarRecurrenceMatches": recurrence_ok,
        "reachableGeneratingFunctionIsReduced": generating_gcd == [Fraction(1)],
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "exact zero-time lifted-transfer obstruction to a pointwise common norm; "
            "not a proof or disproof of the heat-integrated quartic estimate"
        ),
        "checks": checks,
        "stateSpace": {
            "targetSignStates": 2,
            "cubicStates": 8,
            "carries": list(CARRIES),
            "dimension": 48,
            "digitTransferRanks": transfer_ranks,
        },
        "cycle": {
            "wordLeastSignificantBitFirst": list(WORD),
            "matrixProduct": "T0*T0*T1*T0",
            "rank": cycle_rank,
            "imageCharacteristicPolynomialAscending": characteristic,
            "fullCharacteristicPolynomial": (
                "x^42 (x-16)^2 (x^4-25x^3-120x^2+3248x-8192)"
            ),
            "quarticRootIntervals": [list(interval) for interval in root_intervals],
            "quarticValuesAtIntervalEndpoints": [
                [evaluate_quartic(left), evaluate_quartic(right)]
                for left, right in root_intervals
            ],
            "realRootsDisplayOnly": real_roots,
            "dominantEigenvalueDisplayOnly": dominant,
            "fourLevelThreshold": 16,
            "perLevelGrowthDisplayOnly": dominant ** 0.25,
        },
        "reachableTargetFamily": {
            "M": "16^r",
            "q": "2(16^r-1)/15",
            "initialValuesR0ThroughR15": cycle_values,
            "recurrenceFromR6": {
                "coefficients": recurrence,
                "meaning": "y_r=sum_j coefficients[j]*y_(r-1-j)",
            },
            "generatingNumeratorAscending": numerator,
            "generatingDenominatorAscending": denominator,
            "generatingPolynomialGcd": [int(value) for value in generating_gcd],
            "growthExponentLog16LambdaDisplayOnly": exponent,
        },
        "directAudit": {
            "exactLevelsChecked": arguments.max_direct_level,
            "records": direct_records,
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
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(arguments.output)
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

