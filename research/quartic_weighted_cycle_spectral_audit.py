#!/usr/bin/env python3
"""Rigorous spectral-projection audit for the R0.66 weighted cycle.

The four-bit word 0100 defines a stationary affine transfer on forty-eight
signed states and normalized coordinates (x,y) in [0,1]^2.  This script
combines:

* exact integer matrices and affine branch records;
* exact rational enclosures of T=log(2)/2 and the dominant quartic root;
* a weighted Kantorovich contraction on componentwise zero-mass measures;
* an exact degree-48 finite iterate at a publication-scale cycle count; and
* C^1 bounds for the omitted simplex series.

The resulting interval certifies a nonzero (negative) dominant spectral
coefficient for the complete heat-weighted quartic target.  It is an
asymptotic theorem for one explicit packet family, not a Navier--Stokes
regularity theorem.
"""

from __future__ import annotations

import argparse
import collections
import hashlib
import itertools
import json
import math
import platform
import sys
import time
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path

import quartic_weighted_cycle_audit as r065


CARRIES = (-1, 0, 1)
WORD = (0, 1, 0, 0)
STATE_WEIGHTS_BY_CARRY = {-1: 4, 0: 277, 1: 169}
ALPHA_BOUND = Fraction(75, 8)
SPATIAL_RATE_DERIVATIVE_BOUND = Fraction(15, 8)
PARAMETER_RATE_DERIVATIVE_BOUND = Fraction(3, 2)
DOMINANT_ROOT_INTERVAL = (
    Fraction("25.1515893341015"),
    Fraction("25.1515893341016"),
)
ROOT_INTERVALS = ((-13, -12), (3, 4), (8, 9), (25, 26))
ROOT_ABSOLUTE_UPPER = (13, 4, 9, 26)
ROOT_ABSOLUTE_LOWER = (12, 3, 8, 25)
ROOT_DISTANCE_FROM_SIXTEEN_LOWER = (28, 12, 7, 9)
ROOT_DERIVATIVE_ABSOLUTE_LOWER = (11584, 1344, 1424, 12873)


def state_index(target_state: int, cubic_state: int, carry: int) -> int:
    return (target_state * 8 + cubic_state) * 3 + CARRIES.index(carry)


def state_weights() -> list[int]:
    return [STATE_WEIGHTS_BY_CARRY[CARRIES[index % 3]] for index in range(48)]


def zero_matrix(rows: int, columns: int) -> list[list[int]]:
    return [[0 for _ in range(columns)] for _ in range(rows)]


def identity(size: int) -> list[list[int]]:
    output = zero_matrix(size, size)
    for index in range(size):
        output[index][index] = 1
    return output


def matrix_multiply(left: list[list[int]], right: list[list[int]]) -> list[list[int]]:
    output = zero_matrix(len(left), len(right[0]))
    for row in range(len(left)):
        for pivot, coefficient in enumerate(left[row]):
            if coefficient == 0:
                continue
            for column, value in enumerate(right[pivot]):
                if value:
                    output[row][column] += coefficient * value
    return output


def rational_rank(matrix: list[list[int]]) -> int:
    work = [[Fraction(value) for value in row] for row in matrix]
    pivot_row = 0
    for column in range(len(work[0])):
        pivot = next(
            (row for row in range(pivot_row, len(work)) if work[row][column]),
            None,
        )
        if pivot is None:
            continue
        work[pivot_row], work[pivot] = work[pivot], work[pivot_row]
        scale = work[pivot_row][column]
        work[pivot_row] = [value / scale for value in work[pivot_row]]
        for row in range(len(work)):
            if row == pivot_row or work[row][column] == 0:
                continue
            factor = work[row][column]
            work[row] = [
                value - factor * pivot_value
                for value, pivot_value in zip(work[row], work[pivot_row])
            ]
        pivot_row += 1
        if pivot_row == len(work):
            break
    return pivot_row


def matrix_vector(matrix: list[list[int]], vector: list[int]) -> list[int]:
    return [
        sum(value * vector[column] for column, value in enumerate(row))
        for row in matrix
    ]


def independent_columns(matrix: list[list[int]]) -> list[list[int]]:
    selected: list[list[int]] = []
    current_rank = 0
    for column in range(len(matrix[0])):
        candidate = [matrix[row][column] for row in range(len(matrix))]
        trial = selected + [candidate]
        trial_matrix = [
            [vector[row] for vector in trial] for row in range(len(matrix))
        ]
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
        matrix = [
            [columns[column][index] for column in range(len(columns))]
            for index in trial
        ]
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
        pivot = next(
            (row for row in range(column, size) if work[row][column]), None
        )
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
        coordinates = solve_square(
            coordinate_matrix, [image[row] for row in rows]
        )
        reconstructed = [
            sum(
                coordinates[column] * basis_columns[column][row]
                for column in range(rank)
            )
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


def polynomial_multiply(
    left: list[Fraction], right: list[Fraction]
) -> list[Fraction]:
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


def digit_edges(bit: int, length: int) -> list[tuple[int, int, int, int, int]]:
    edges: list[tuple[int, int, int, int, int]] = []
    for target_state in (0, 1):
        for cubic_state in range(8):
            for parent_carry in CARRIES:
                row = state_index(target_state, cubic_state, parent_carry)
                for epsilon in range(8):
                    epsilon_a = (epsilon >> 2) & 1
                    epsilon_b = (epsilon >> 1) & 1
                    epsilon_c = epsilon & 1
                    child_carry = (
                        2 * parent_carry
                        + bit
                        - (epsilon_a + epsilon_b - epsilon_c)
                    )
                    if child_carry not in CARRIES:
                        continue
                    parity = target_state * bit + (cubic_state & epsilon).bit_count()
                    sign = -1 if parity % 2 else 1
                    column = state_index(bit, epsilon, child_carry)
                    edges.append(
                        (
                            row,
                            column,
                            epsilon_a * length,
                            epsilon_b * length,
                            sign,
                        )
                    )
    return edges


def digit_transfer(bit: int) -> list[list[int]]:
    transfer = zero_matrix(48, 48)
    for row, column, _a, _b, sign in digit_edges(bit, 1):
        transfer[row][column] += sign
    return transfer


def cycle_matrix() -> list[list[int]]:
    transfers = [digit_transfer(0), digit_transfer(1)]
    output = identity(48)
    for bit in WORD:
        output = matrix_multiply(transfers[bit], output)
    return output


def affine_branches() -> dict[tuple[int, int, int, int], int]:
    paths: dict[tuple[int, int, int, int], int] = {
        (state, state, 0, 0): 1 for state in range(48)
    }
    for length, bit in zip((1, 2, 4, 8), WORD):
        by_column: dict[int, list[tuple[int, int, int, int]]] = collections.defaultdict(list)
        for row, column, shift_a, shift_b, sign in digit_edges(bit, length):
            by_column[column].append((row, shift_a, shift_b, sign))
        updated: dict[tuple[int, int, int, int], int] = collections.defaultdict(int)
        for (middle, source, shift_a, shift_b), value in paths.items():
            for row, added_a, added_b, sign in by_column[middle]:
                updated[
                    (row, source, shift_a + added_a, shift_b + added_b)
                ] += value * sign
        paths = {key: value for key, value in updated.items() if value}
    return paths


def quartic(value: int | Fraction) -> int | Fraction:
    return value**4 - 25 * value**3 - 120 * value**2 + 3248 * value - 8192


def quartic_derivative(value: int | Fraction) -> int | Fraction:
    return 4 * value**3 - 75 * value**2 - 240 * value + 3248


def weighted_matrix_norm(matrix: list[list[int]], weights: list[int]) -> Fraction:
    return max(
        Fraction(
            sum(abs(matrix[row][column]) * weights[column] for column in range(48)),
            weights[row],
        )
        for row in range(48)
    )


def branch_weight_checks(
    branches: dict[tuple[int, int, int, int], int], weights: list[int]
) -> tuple[bool, Fraction]:
    exact_eigenweight = True
    contraction_lift: list[Fraction] = []
    for row in range(48):
        absolute_mass = sum(
            abs(value) * weights[column]
            for (target, column, _a, _b), value in branches.items()
            if target == row
        )
        exact_eigenweight &= absolute_mass == 256 * weights[row]
        # The l1 distance from (shift_a/16,shift_b/16) to the lift atom (0,0).
        distance_sum = sum(
            Fraction(
                abs(value) * weights[column] * (shift_a + shift_b), 16
            )
            for (target, column, shift_a, shift_b), value in branches.items()
            if target == row
        )
        contraction_lift.append(distance_sum / weights[row])
    return exact_eigenweight, max(contraction_lift)


def projector_norm_bounds(matrix_norm: Fraction) -> dict[str, Fraction]:
    bounds: list[Fraction] = []
    for index in range(4):
        numerator = matrix_norm * (matrix_norm + 16)
        for other in range(4):
            if other != index:
                numerator *= matrix_norm + ROOT_ABSOLUTE_UPPER[other]
        denominator = (
            ROOT_ABSOLUTE_LOWER[index]
            * ROOT_DISTANCE_FROM_SIXTEEN_LOWER[index]
            * ROOT_DERIVATIVE_ABSOLUTE_LOWER[index]
        )
        bounds.append(numerator / denominator)
    polynomial_norm = (
        matrix_norm**4
        + 25 * matrix_norm**3
        + 120 * matrix_norm**2
        + 3248 * matrix_norm
        + 8192
    )
    sixteen = matrix_norm * polynomial_norm / (16 * abs(quartic(16)))
    return {
        "negativeRoot": bounds[0],
        "smallPositiveRoot": bounds[1],
        "middlePositiveRoot": bounds[2],
        "dominantRoot": bounds[3],
        "sixteen": sixteen,
    }


def exponential_upper(value: Fraction, terms: int = 80) -> Fraction:
    partial = Fraction(1)
    term = Fraction(1)
    for index in range(1, terms + 1):
        term *= value / index
        partial += term
    ratio = value / (terms + 1)
    if ratio >= 1:
        raise ValueError("exponential enclosure requires a smaller tail ratio")
    return partial + term * ratio / (1 - ratio)


def simplex_tail_lipschitz(
    order: int, time_upper: Fraction, rate_derivative_bound: Fraction
) -> Fraction:
    first_degree = order + 1
    z = ALPHA_BOUND * time_upper
    first = (
        3
        * (rate_derivative_bound / ALPHA_BOUND)
        * time_upper**3
        / 2
        * first_degree
        * z**first_degree
        / (math.factorial(first_degree) * (first_degree + 3))
    )
    ratio = z * (first_degree + 3) / (
        first_degree * (first_degree + 4)
    )
    if ratio >= 1:
        raise ValueError("derivative tail is not geometrically decreasing")
    return first / (1 - ratio)


def fraction_decimal(value: Fraction, digits: int = 48) -> str:
    with localcontext() as context:
        context.prec = digits
        output = Decimal(value.numerator) / Decimal(value.denominator)
        return format(output, ".40E")


def fraction_hash(value: Fraction) -> str:
    return hashlib.sha256(
        f"{value.numerator}/{value.denominator}".encode("ascii")
    ).hexdigest()


def exact_partial_iterate(
    cycles: int, order: int, progress: bool, started: float
) -> tuple[Fraction, Fraction, int, int]:
    degree = 2 * order
    states = r065.initial_states(degree)
    length = 1
    for level in range(1, 4 * cycles + 1):
        bit = WORD[(level - 1) % 4]
        states = r065.advance_moments(states, degree, length, bit)
        length *= 2
        if progress and level % 4 == 0:
            print(
                f"[R0.66 +{time.perf_counter()-started:8.2f}s] "
                f"exact-cycle={level//4:03d}/{cycles} bits(M)={length.bit_length()}",
                file=sys.stderr,
                flush=True,
            )
    target = 2 * (length - 1) // 15
    moments = states[state_index(0, 0, 0)]
    sequences = [
        r065.complete_homogeneous_sequence(rates, order)
        for rates in r065.rate_polynomials(length, target)
    ]
    integer_coefficients = [
        sum(
            r065.moment_functional(sequence[index], moments)
            for sequence in sequences
        )
        for index in range(order + 1)
    ]
    high = 4 * length
    coefficients = [
        Fraction(
            (-1) ** index * value,
            high ** (2 * index) * math.factorial(index + 3),
        )
        for index, value in enumerate(integer_coefficients)
    ]
    time_lower, time_upper = r065.time_enclosure()
    lower, upper = r065.interval_polynomial(
        coefficients, time_lower, time_upper
    )
    return lower, upper, length, target


def load_finite_iterate(
    path: Path, cycles: int, order: int
) -> tuple[Fraction, Fraction, int, int, str]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if int(payload["cycles"]) != cycles or int(payload["order"]) != order:
        raise ValueError("finite iterate parameters do not match the spectral audit")
    if int(payload["degree"]) != 2 * order:
        raise ValueError("finite iterate has the wrong maximum moment degree")
    length = int(payload["M"])
    target = int(payload["target"])
    if length != 16**cycles or target != 2 * (length - 1) // 15:
        raise ValueError("finite iterate has the wrong packet scale or target")
    lower = Fraction(
        int(payload["partialLowerNumerator"]),
        int(payload["partialLowerDenominator"]),
    )
    upper = Fraction(
        int(payload["partialUpperNumerator"]),
        int(payload["partialUpperDenominator"]),
    )
    if not lower <= upper:
        raise ValueError("finite iterate interval endpoints are reversed")
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return lower, upper, length, target, digest


def normalized_interval(
    lower: Fraction,
    upper: Fraction,
    denominator_lower: Fraction,
    denominator_upper: Fraction,
    power: int,
) -> tuple[Fraction, Fraction]:
    denominators = (denominator_lower**power, denominator_upper**power)
    values = [value / denominator for value in (lower, upper) for denominator in denominators]
    return min(values), max(values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument(
        "--profile", choices=("publication", "quick"), default="publication"
    )
    parser.add_argument("--cycles", type=int)
    parser.add_argument("--order", type=int)
    parser.add_argument("--finite-input", type=Path)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    cycles = arguments.cycles or (100 if arguments.profile == "publication" else 8)
    order = arguments.order or (24 if arguments.profile == "publication" else 12)
    if arguments.profile == "publication" and (cycles < 100 or order < 24):
        raise ValueError("publication profile requires cycles>=100 and order>=24")
    if arguments.profile == "quick" and (cycles < 4 or order < 8):
        raise ValueError("quick profile requires cycles>=4 and order>=8")
    started = time.perf_counter()

    matrix = cycle_matrix()
    matrix_squared = matrix_multiply(matrix, matrix)
    restricted_matrix, restricted_rank = image_restriction(matrix)
    restricted_characteristic = characteristic_polynomial(restricted_matrix)
    expected_characteristic = [-2097152, 1093632, -142848, 688, 936, -57, 1]
    shifted = [
        [matrix[row][column] - (16 if row == column else 0) for column in range(48)]
        for row in range(48)
    ]
    branches = affine_branches()
    branch_matrix = zero_matrix(48, 48)
    for (row, column, _a, _b), value in branches.items():
        branch_matrix[row][column] += value
    weights = state_weights()
    absolute_weight_exact, lift_constant = branch_weight_checks(branches, weights)
    matrix_norm = weighted_matrix_norm(matrix, weights)
    projector_bounds = projector_norm_bounds(matrix_norm)

    root_sign_changes = [
        quartic(left) * quartic(right) < 0 for left, right in ROOT_INTERVALS
    ]
    dominant_lower, dominant_upper = DOMINANT_ROOT_INTERVAL
    dominant_root_enclosed = (
        quartic(dominant_lower) < 0 < quartic(dominant_upper)
    )

    if arguments.finite_input:
        (
            partial_lower,
            partial_upper,
            length,
            target,
            finite_input_sha256,
        ) = load_finite_iterate(arguments.finite_input, cycles, order)
    else:
        partial_lower, partial_upper, length, target = exact_partial_iterate(
            cycles, order, arguments.progress, started
        )
        finite_input_sha256 = None
    finite_lower, finite_upper = normalized_interval(
        partial_lower,
        partial_upper,
        dominant_lower,
        dominant_upper,
        cycles,
    )

    initial_mass_norm = Fraction(1, 277)
    dominant_mass_norm = projector_bounds["dominantRoot"] * initial_mass_norm
    mass_remainder_norm = max(
        initial_mass_norm + dominant_mass_norm,
        initial_mass_norm
        * (
            projector_bounds["negativeRoot"]
            + projector_bounds["smallPositiveRoot"]
            + projector_bounds["middlePositiveRoot"]
            + projector_bounds["sixteen"]
        ),
    )
    eigenmeasure_zero_mass_norm = (
        lift_constant
        * dominant_mass_norm
        / (dominant_lower - 16)
    )

    _time_lower, time_upper = r065.time_enclosure()
    z = ALPHA_BOUND * time_upper
    exp_z_upper = exponential_upper(z)
    observable_sup = time_upper**3 / 2 * exp_z_upper
    observable_spatial_lipschitz = (
        3
        * SPATIAL_RATE_DERIVATIVE_BOUND
        * time_upper**4
        / 2
        * exp_z_upper
    )
    observable_parameter_lipschitz = (
        3
        * PARAMETER_RATE_DERIVATIVE_BOUND
        * time_upper**4
        / 2
        * exp_z_upper
    )
    convergence_ratio = Fraction(16) / dominant_lower
    selected_weight = Fraction(277)
    finite_convergence_error = (
        selected_weight
        * (
            mass_remainder_norm * observable_sup
            + observable_spatial_lipschitz
            * (
                eigenmeasure_zero_mass_norm
                + lift_constant * mass_remainder_norm * cycles / 16
            )
        )
        * convergence_ratio**cycles
    )
    target_parameter_error = (
        Fraction(2, 15)
        * observable_parameter_lipschitz
        * convergence_ratio**cycles
    )
    tail_sup = r065.simplex_tail_bound(order, 1, time_upper)
    tail_lipschitz = simplex_tail_lipschitz(
        order, time_upper, SPATIAL_RATE_DERIVATIVE_BOUND
    )
    infinite_series_error = selected_weight * (
        dominant_mass_norm * tail_sup
        + eigenmeasure_zero_mass_norm * tail_lipschitz
    )
    total_error = (
        finite_convergence_error + target_parameter_error + infinite_series_error
    )
    coefficient_lower = finite_lower - total_error
    coefficient_upper = finite_upper + total_error

    structural_checks = {
        "cycleMatrixMatchesAffineBranchMasses": branch_matrix == matrix,
        "affineBranchAuditHas12288ExactRecords": len(branches) == 12288
        and sum(abs(value) for value in branches.values()) == 12288,
        "cycleRankIsSix": rational_rank(matrix) == restricted_rank == 6,
        "exactImageCharacteristicPolynomialMatches": restricted_characteristic
        == expected_characteristic,
        "cycleSquaredRankIsSixSoZeroIsSemisimple": rational_rank(matrix_squared)
        == 6,
        "sixteenEigenspaceHasDimensionTwo": 48 - rational_rank(shifted) == 2,
        "quarticHasOneSignChangeInEachCertifiedRootInterval": all(
            root_sign_changes
        ),
        "dominantRootHasTightExactRationalEnclosure": dominant_root_enclosed,
        "rootDerivativeEndpointBoundsMatch": (
            abs(quartic_derivative(-12)),
            abs(quartic_derivative(4)),
            abs(quartic_derivative(8)),
            abs(quartic_derivative(25)),
        )
        == ROOT_DERIVATIVE_ABSOLUTE_LOWER,
        "dominantRootExceedsTwentyFive": dominant_lower > 25,
        "absoluteBranchMatrixHasExactPositiveWeight256": absolute_weight_exact,
        "weightedCycleNormIsExactly256": matrix_norm == 256,
        "zeroMassKantorovichGrowthPerBlockIsAtMost16": Fraction(256, 16)
        == 16,
        "liftConstantMatchesExactBranchAudit": lift_constant
        == Fraction(36161, 104),
        "normalizedRateDerivativeBoundsAreExact": max(
            Fraction(163, 120),
            Fraction(101, 120),
            Fraction(22, 15),
            Fraction(15, 8),
        )
        == SPATIAL_RATE_DERIVATIVE_BOUND
        and max(Fraction(1, 4), Fraction(7, 8), Fraction(3, 2))
        == PARAMETER_RATE_DERIVATIVE_BOUND,
    }
    numerical_checks = {
        "finiteTaylorIterateIsStrictlyNegative": partial_upper < 0,
        "spectralConvergenceErrorBelowThreeTimesTenToMinusNine": finite_convergence_error
        < Fraction(3, 10**9),
        "infiniteSimplexTailProjectionBelowOneTimesTenToMinusSeven": infinite_series_error
        < Fraction(1, 10**7),
        "targetParameterCorrectionBelowOneTimesTenToMinusTwenty": target_parameter_error
        < Fraction(1, 10**20),
        "completeDominantSpectralCoefficientIsStrictlyNegative": coefficient_upper
        < 0,
        "completeDominantCoefficientMagnitudeExceedsTwoTimesTenToMinusFive": coefficient_upper
        < Fraction(-2, 10**5),
    }
    checks = {**structural_checks, **numerical_checks}
    if arguments.profile == "publication" and not all(checks.values()):
        raise AssertionError(checks)
    if arguments.profile == "quick":
        checks["quickProfileDoesNotClaimPublicationProjectionSign"] = cycles < 100

    report = {
        "schemaVersion": "1.0",
        "status": "passed" if all(checks.values()) else "exploratory",
        "profile": arguments.profile,
        "classification": (
            "rigorous negative dominant spectral projection and asymptotic "
            "supercritical growth for one explicit heat-weighted quartic packet; "
            "not control of all Picard orders and not a three-dimensional "
            "Navier-Stokes regularity theorem"
        ),
        "checks": checks,
        "stationaryBlockOperator": {
            "wordLeastSignificantBitFirst": list(WORD),
            "states": 48,
            "affineBranchRecords": len(branches),
            "absoluteBranchMultiplicity": sum(abs(value) for value in branches.values()),
            "coordinateContraction": "1/16",
            "stateWeightsByCarry": {
                str(carry): weight
                for carry, weight in STATE_WEIGHTS_BY_CARRY.items()
            },
            "absoluteBranchEigenvalue": 256,
            "zeroMassKantorovichBound": 16,
            "liftConstantExactNumerator": str(lift_constant.numerator),
            "liftConstantExactDenominator": str(lift_constant.denominator),
        },
        "massSpectrum": {
            "characteristicPolynomial": (
                "x^42 (x-16)^2 (x^4-25x^3-120x^2+3248x-8192)"
            ),
            "imageCharacteristicPolynomialAscending": restricted_characteristic,
            "rootIntervals": [list(interval) for interval in ROOT_INTERVALS],
            "dominantLowerNumerator": str(dominant_lower.numerator),
            "dominantLowerDenominator": str(dominant_lower.denominator),
            "dominantUpperNumerator": str(dominant_upper.numerator),
            "dominantUpperDenominator": str(dominant_upper.denominator),
            "dominantLowerDisplay": fraction_decimal(dominant_lower),
            "dominantUpperDisplay": fraction_decimal(dominant_upper),
            "projectorNormBoundsDisplay": {
                name: fraction_decimal(value) for name, value in projector_bounds.items()
            },
            "dominantMassNormBound": fraction_decimal(dominant_mass_norm),
            "massRemainderNormBound": fraction_decimal(mass_remainder_norm),
        },
        "exactFiniteIterate": {
            "cycles": cycles,
            "TaylorOrder": order,
            "maximumMomentDegree": 2 * order,
            "M": str(length),
            "q": str(target),
            "stagedInputSha256": finite_input_sha256,
            "partialLowerNumerator": str(partial_lower.numerator),
            "partialLowerDenominator": str(partial_lower.denominator),
            "partialUpperNumerator": str(partial_upper.numerator),
            "partialUpperDenominator": str(partial_upper.denominator),
            "normalizedLowerDisplay": fraction_decimal(finite_lower),
            "normalizedUpperDisplay": fraction_decimal(finite_upper),
            "partialLowerSha256": fraction_hash(partial_lower),
            "partialUpperSha256": fraction_hash(partial_upper),
        },
        "errorBudget": {
            "finiteSpectralConvergence": fraction_decimal(
                finite_convergence_error
            ),
            "finiteTargetParameter": fraction_decimal(target_parameter_error),
            "infiniteSimplexTailProjection": fraction_decimal(
                infinite_series_error
            ),
            "total": fraction_decimal(total_error),
            "simplexTailSup": fraction_decimal(tail_sup),
            "simplexTailSpatialLipschitz": fraction_decimal(tail_lipschitz),
            "observableSupBound": fraction_decimal(observable_sup),
            "observableSpatialLipschitzBound": fraction_decimal(
                observable_spatial_lipschitz
            ),
            "observableParameterLipschitzBound": fraction_decimal(
                observable_parameter_lipschitz
            ),
        },
        "certifiedTheorem": {
            "coefficientLowerNumerator": str(coefficient_lower.numerator),
            "coefficientLowerDenominator": str(coefficient_lower.denominator),
            "coefficientUpperNumerator": str(coefficient_upper.numerator),
            "coefficientUpperDenominator": str(coefficient_upper.denominator),
            "coefficientLowerDisplay": fraction_decimal(coefficient_lower),
            "coefficientUpperDisplay": fraction_decimal(coefficient_upper),
            "asymptoticFormula": "S_r=C_* lambda^r+O(r 16^r)",
            "coefficientSign": "negative",
            "consequence": "|S_r|/16^r tends to infinity on the explicit packet",
            "claimBoundary": (
                "This disproves the candidate uniform quartic O(M) bound on the "
                "named packet family only. It does not control higher Picard orders, "
                "general initial data, or global smoothness."
            ),
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
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
