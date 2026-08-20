#!/usr/bin/env python3
"""Exact R0.68B-1 audit for the zero-time eighth-order target cycle.

The audit builds the 1792-state seven-carrier signed transfer, proves exact
ranks over Q, restricts the repeated-0100 cycle to its 204-dimensional image,
and computes the image characteristic polynomial over Q.  It independently
checks the reachable scalar by exact seven-fold convolution and by an exact
vector recurrence after one transient.

This is a fixed-order, zero-time algebraic theorem.  It is not a certificate
for the complete heat-weighted seven-simplex observable, the full Picard
series, or three-dimensional Navier--Stokes regularity.

Formal dependencies are pinned in ``requirements-r068b.txt``.
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
import scipy
from scipy.sparse import csr_matrix, eye
import sympy
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


POSITIVE_CARRIERS = 4
NEGATIVE_CARRIERS = 3
CARRIER_COUNT = POSITIVE_CARRIERS + NEGATIVE_CARRIERS
SIGN_STATES = 1 << CARRIER_COUNT
CARRIES = tuple(range(-NEGATIVE_CARRIERS, POSITIVE_CARRIERS))
WORD = (0, 1, 0, 0)
DIMENSION = 2 * SIGN_STATES * len(CARRIES)
IMAGE_DIMENSION = 204
STABLE_IMAGE_DIMENSION = 148
MODULAR_PRIMES = (1_000_003, 1_000_033)

R066_QUARTIC = [1, -25, -120, 3248, -8192]
R067_DEGREE_TEN = [
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

SCALED_QUARTIC = [
    1,
    -6_400,
    -7_864_320,
    54_492_397_568,
    -35_184_372_088_832,
]
SCALED_DEGREE_TEN = [
    1,
    -6_800,
    7_075_840,
    12_233_146_368,
    110_817_001_340_928,
    -903_815_119_425_765_376,
    1_337_699_975_193_207_767_040,
    5_200_258_211_136_706_319_482_880,
    -15_661_530_101_044_897_826_123_808_768,
    14_629_201_671_750_070_726_086_038_126_592,
    -545_089_758_098_138_642_643_582_378_311_680,
]
DEGREE_EIGHTEEN = [
    1,
    -6_969,
    -2_590_744,
    139_397_444_912,
    -426_297_237_954_560,
    65_541_085_313_761_280,
    1_817_561_819_293_822_222_336,
    -12_923_427_431_300_516_632_592_384,
    72_083_289_706_196_062_643_987_415_040,
    -147_173_596_220_605_159_573_753_471_959_040,
    -29_101_569_723_662_770_535_965_645_510_541_312,
    382_197_970_754_416_550_433_344_819_302_481_526_784,
    -749_472_734_550_488_533_458_838_292_284_403_557_072_896,
    2_161_494_797_667_240_625_211_172_063_217_942_790_211_108_864,
    3_167_861_340_246_684_172_706_078_559_046_764_091_092_737_458_176,
    -9_714_642_251_431_883_530_476_110_829_655_218_596_491_783_122_714_624,
    -5_562_654_259_926_397_846_713_126_171_648_909_197_020_814_256_315_039_744,
    -320_199_342_064_115_143_523_122_610_176_213_995_501_458_910_461_684_613_120,
    93_468_964_114_928_862_759_328_348_387_927_361_466_359_102_381_601_325_056_000,
]

DOMINANT_ROOT_INTERVAL = (
    Fraction("25.1515893341015") * 256,
    Fraction("25.1515893341016") * 256,
)
REMAINDER_RADIUS = 4_800


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.68B-1 eighth +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def state_index(target_state: int, septic_state: int, carry: int) -> int:
    return (
        (target_state * SIGN_STATES + septic_state) * len(CARRIES)
        + CARRIES.index(carry)
    )


def signed_shifts() -> list[int]:
    output: list[int] = []
    for epsilon in range(SIGN_STATES):
        digits = tuple(
            (epsilon >> shift) & 1
            for shift in range(CARRIER_COUNT - 1, -1, -1)
        )
        output.append(
            sum(digits[:POSITIVE_CARRIERS])
            - sum(digits[POSITIVE_CARRIERS:])
        )
    return output


def signed_digit_transfer(bit: int) -> csr_matrix:
    shifts = signed_shifts()
    rows: list[int] = []
    columns: list[int] = []
    values: list[int] = []
    for target_state in (0, 1):
        for septic_state in range(SIGN_STATES):
            for parent_carry in CARRIES:
                row = state_index(target_state, septic_state, parent_carry)
                for epsilon, signed_shift in enumerate(shifts):
                    child_carry = 2 * parent_carry + bit - signed_shift
                    if child_carry not in CARRIES:
                        continue
                    parity = (
                        target_state * bit
                        + (septic_state & epsilon).bit_count()
                    )
                    rows.append(row)
                    columns.append(state_index(bit, epsilon, child_carry))
                    values.append(-1 if parity % 2 else 1)
    return csr_matrix(
        (
            np.array(values, dtype=np.int64),
            (np.array(rows, dtype=np.int32), np.array(columns, dtype=np.int32)),
        ),
        shape=(DIMENSION, DIMENSION),
        dtype=np.int64,
    )


def cycle_matrix(transfers: list[csr_matrix]) -> csr_matrix:
    cycle = eye(DIMENSION, dtype=np.int64, format="csr")
    for bit in WORD:
        cycle = transfers[bit] @ cycle
        cycle.eliminate_zeros()
    return cycle


def exact_domain_rank(matrix: csr_matrix) -> int:
    dense = matrix.toarray()
    domain = DomainMatrix.from_list_sympy(
        dense.shape[0], dense.shape[1], dense.tolist()
    )
    return domain.rank()


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
            factors = work[pivot_row + 1 :, column]
            nonzero = np.flatnonzero(factors)
            if nonzero.size:
                affected = pivot_row + 1 + nonzero
                work[affected] = (
                    work[affected]
                    - factors[nonzero, None] * work[pivot_row]
                ) % prime
        pivots.append(column)
        pivot_row += 1
        if pivot_row == rows:
            break
    return pivots


def modular_rank(matrix: np.ndarray, prime: int) -> int:
    return len(modular_pivots(matrix, prime))


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
    output = polynomial_power([1, 0], IMAGE_DIMENSION - STABLE_IMAGE_DIMENSION)
    output = polynomial_multiply(output, polynomial_power([1, -4096], 14))
    output = polynomial_multiply(output, polynomial_power(SCALED_QUARTIC, 14))
    output = polynomial_multiply(output, polynomial_power(SCALED_DEGREE_TEN, 6))
    return polynomial_multiply(output, DEGREE_EIGHTEEN)


def reachable_polynomial() -> list[int]:
    output = polynomial_multiply([1, -4096], SCALED_QUARTIC)
    output = polynomial_multiply(output, SCALED_DEGREE_TEN)
    return polynomial_multiply(output, DEGREE_EIGHTEEN)


def image_characteristic(
    cycle: csr_matrix, dense_cycle: np.ndarray
) -> tuple[list[int], dict[str, object]]:
    basis_columns = modular_pivots(dense_cycle, MODULAR_PRIMES[0])
    if len(basis_columns) != IMAGE_DIMENSION:
        raise AssertionError(f"unexpected image rank {len(basis_columns)}")
    basis = dense_cycle[:, basis_columns]
    coordinate_rows = modular_pivots(basis.T, MODULAR_PRIMES[0])
    if len(coordinate_rows) != IMAGE_DIMENSION:
        raise AssertionError("failed to select image coordinate rows")

    coordinate = basis[coordinate_rows, :]
    image = (cycle @ basis)[coordinate_rows, :]
    coordinate_domain = DomainMatrix.from_list_sympy(
        IMAGE_DIMENSION, IMAGE_DIMENSION, coordinate.tolist()
    )
    image_domain = DomainMatrix.from_list_sympy(
        IMAGE_DIMENSION, IMAGE_DIMENSION, image.tolist()
    )
    numerator, denominator = coordinate_domain.solve_den(
        image_domain, method="rref"
    )
    restriction = numerator.to_field().scalarmul(QQ(1, int(denominator)))
    characteristic_raw = restriction.charpoly()
    if any(value.denominator != 1 for value in characteristic_raw):
        raise AssertionError("nonintegral image characteristic polynomial")
    characteristic = [int(value) for value in characteristic_raw]
    return characteristic, {
        "basisColumns": basis_columns,
        "coordinateRows": coordinate_rows,
        "coordinateDenominatorBits": int(denominator).bit_length(),
        "coordinateDenominatorSha256": hashlib.sha256(
            str(int(denominator)).encode()
        ).hexdigest(),
        "coordinateDeterminantNonzeroModulo": {
            str(prime): modular_rank(coordinate, prime) == IMAGE_DIMENSION
            for prime in MODULAR_PRIMES
        },
    }


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


def septic_states(level: int) -> list[list[int]]:
    pair = rudin_shapiro_pair(level)
    states: list[list[int]] = []
    for sigma in range(SIGN_STATES):
        factors = [
            pair[(sigma >> shift) & 1]
            for shift in range(CARRIER_COUNT - 1, -1, -1)
        ]
        for index in range(POSITIVE_CARRIERS, CARRIER_COUNT):
            factors[index] = list(reversed(factors[index]))
        value = factors[0]
        for factor in factors[1:]:
            value = exact_convolve(value, factor)
        states.append(value)
    return states


def initial_vector(dtype: object = np.int64) -> np.ndarray:
    vector = np.zeros(DIMENSION, dtype=dtype)
    for target_state in (0, 1):
        for septic_state in range(SIGN_STATES):
            vector[state_index(target_state, septic_state, 0)] = 1
    return vector


def repeated_word_target(level: int) -> tuple[list[int], int]:
    bits = [WORD[index % len(WORD)] for index in range(level)]
    return bits, sum(bit << index for index, bit in enumerate(bits))


def direct_transfer_audit(
    transfers: list[csr_matrix], maximum_level: int
) -> list[dict[str, int]]:
    records: list[dict[str, int]] = []
    for level in range(1, maximum_level + 1):
        bits, target = repeated_word_target(level)
        vector = initial_vector()
        for bit in bits:
            vector = transfers[bit] @ vector
        pair = rudin_shapiro_pair(level)
        septics = septic_states(level)
        length = 1 << level
        offset = NEGATIVE_CARRIERS * (length - 1)
        for target_state in (0, 1):
            target_sign = pair[target_state][target]
            for septic_state in range(SIGN_STATES):
                for carry in CARRIES:
                    exponent = target + carry * length
                    array_index = exponent + offset
                    direct = (
                        0
                        if not 0 <= array_index < len(septics[septic_state])
                        else target_sign * septics[septic_state][array_index]
                    )
                    recursive = int(
                        vector[state_index(target_state, septic_state, carry)]
                    )
                    if direct != recursive:
                        raise AssertionError(
                            "seven-carrier transfer mismatch "
                            f"level={level} "
                            f"state={(target_state, septic_state, carry)}"
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


def exact_transfer_rows(
    transfer: csr_matrix,
) -> list[tuple[list[int], list[int]]]:
    rows: list[tuple[list[int], list[int]]] = []
    for row in range(DIMENSION):
        start, end = transfer.indptr[row], transfer.indptr[row + 1]
        positive: list[int] = []
        negative: list[int] = []
        for column, value in zip(
            transfer.indices[start:end], transfer.data[start:end]
        ):
            (positive if value == 1 else negative).append(int(column))
        rows.append((positive, negative))
    return rows


def apply_exact_transfer(
    rows: list[tuple[list[int], list[int]]], vector: list[int]
) -> list[int]:
    return [
        sum(vector[column] for column in positive)
        - sum(vector[column] for column in negative)
        for positive, negative in rows
    ]


def apply_exact_cycle(
    rows: list[list[tuple[list[int], list[int]]]], vector: list[int]
) -> list[int]:
    for bit in WORD:
        vector = apply_exact_transfer(rows[bit], vector)
    return vector


def exact_reachable_data(
    transfers: list[csr_matrix], sequence_terms: int
) -> dict[str, object]:
    recurrence = reachable_polynomial()
    degree = len(recurrence) - 1
    if sequence_terms < 2 * degree + 2:
        raise ValueError(
            f"sequence terms must be at least {2 * degree + 2}"
        )
    rows = [exact_transfer_rows(transfer) for transfer in transfers]
    vector = [int(value) for value in initial_vector(dtype=object)]
    vectors = [vector]
    for _ in range(sequence_terms - 1):
        vector = apply_exact_cycle(rows, vector)
        vectors.append(vector)
    observable = state_index(0, 0, 0)
    sequence = [vector[observable] for vector in vectors]

    residual_at_degree = sequence[degree] + sum(
        recurrence[index] * sequence[degree - index]
        for index in range(1, degree + 1)
    )
    residuals_after_transient = [
        sequence[n]
        + sum(
            recurrence[index] * sequence[n - index]
            for index in range(1, degree + 1)
        )
        for n in range(degree + 1, sequence_terms)
    ]
    vector_residual = [
        vectors[degree + 1][state]
        + sum(
            recurrence[index] * vectors[degree + 1 - index][state]
            for index in range(1, degree + 1)
        )
        for state in range(DIMENSION)
    ]
    numerator = [
        sum(
            recurrence[index] * sequence[power - index]
            for index in range(power + 1)
        )
        for power in range(degree + 1)
    ]
    variable = sympy.symbols("x")
    gcd = sympy.gcd(
        sympy.Poly.from_list(recurrence, variable, domain=sympy.ZZ),
        sympy.Poly.from_list(numerator, variable, domain=sympy.ZZ),
    )
    return {
        "initialValues": sequence,
        "recurrenceCharacteristicDescending": recurrence,
        "recurrenceDegree": degree,
        "recurrenceResidualAtR33": residual_at_degree,
        "recurrenceResidualsFromR34AreZero": all(
            value == 0 for value in residuals_after_transient
        ),
        "vectorRecurrenceFromR34IsExact": not any(vector_residual),
        "generatingDenominatorAscending": recurrence,
        "generatingNumeratorAscending": numerator,
        "generatingGcdAscending": [int(value) for value in gcd.all_coeffs()],
    }


def interval_multiply(
    left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]
) -> tuple[Fraction, Fraction]:
    values = tuple(
        left[left_index] * right[right_index]
        for left_index in (0, 1)
        for right_index in (0, 1)
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


def decimal_display(value: Fraction, digits: int = 30) -> str:
    with localcontext() as context:
        context.prec = digits
        return str(Decimal(value.numerator) / Decimal(value.denominator))


def evaluate_polynomial(
    coefficients: list[int], value: int | Fraction
) -> int | Fraction:
    result: int | Fraction = 0
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def dominant_projection_interval(reachable: dict[str, object]) -> dict[str, object]:
    recurrence = [
        int(value)
        for value in reachable["recurrenceCharacteristicDescending"]
    ]
    numerator = [
        int(value) for value in reachable["generatingNumeratorAscending"]
    ]
    root_interval = DOMINANT_ROOT_INTERVAL
    numerator_interval = interval_horner(numerator, root_interval)
    derivative_interval = interval_horner(
        [index * recurrence[index] for index in range(1, len(recurrence))],
        root_interval,
    )
    if not (
        numerator_interval[1] < 0 and derivative_interval[1] < 0
    ):
        raise AssertionError("dominant projection interval lost its sign")
    candidates = tuple(
        -numerator_interval[numerator_index]
        / derivative_interval[derivative_index]
        for numerator_index in (0, 1)
        for derivative_index in (0, 1)
    )
    coefficient_interval = min(candidates), max(candidates)
    return {
        "dominantRootLower": str(root_interval[0]),
        "dominantRootUpper": str(root_interval[1]),
        "dominantRootLowerDisplay": decimal_display(root_interval[0]),
        "dominantRootUpperDisplay": decimal_display(root_interval[1]),
        "scaledQuarticAtLower": str(
            evaluate_polynomial(SCALED_QUARTIC, root_interval[0])
        ),
        "scaledQuarticAtUpper": str(
            evaluate_polynomial(SCALED_QUARTIC, root_interval[1])
        ),
        "projectionNumeratorInterval": [
            str(value) for value in numerator_interval
        ],
        "projectionDenominatorInterval": [
            str(value) for value in derivative_interval
        ],
        "coefficientLower": str(coefficient_interval[0]),
        "coefficientUpper": str(coefficient_interval[1]),
        "coefficientLowerDisplay": decimal_display(coefficient_interval[0]),
        "coefficientUpperDisplay": decimal_display(coefficient_interval[1]),
        "coefficientIsStrictlyNegative": coefficient_interval[1] < 0,
    }


def schur_disk_certificate(
    coefficients: list[int], radius: int
) -> list[dict[str, object]]:
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--max-direct-level", type=int, default=6)
    parser.add_argument("--sequence-terms", type=int, default=82)
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()

    progress(arguments.progress, started, "building signed digit transfers")
    transfers = [signed_digit_transfer(0), signed_digit_transfer(1)]
    digit_exact_ranks = [exact_domain_rank(transfer) for transfer in transfers]

    progress(arguments.progress, started, "building repeated four-bit cycle")
    cycle = cycle_matrix(transfers)
    cycle_squared = cycle @ cycle
    cycle_squared.eliminate_zeros()
    cycle_cubed = cycle_squared @ cycle
    cycle_cubed.eliminate_zeros()

    progress(arguments.progress, started, "computing exact rational ranks", power=1)
    cycle_rank = exact_domain_rank(cycle)
    progress(arguments.progress, started, "computing exact rational ranks", power=2)
    cycle_squared_rank = exact_domain_rank(cycle_squared)
    progress(arguments.progress, started, "computing exact rational ranks", power=3)
    cycle_cubed_rank = exact_domain_rank(cycle_cubed)

    dense_cycle = cycle.toarray()
    dense_squared = cycle_squared.toarray()
    dense_cubed = cycle_cubed.toarray()
    modular_ranks = {
        str(prime): [
            modular_rank(dense_cycle, prime),
            modular_rank(dense_squared, prime),
            modular_rank(dense_cubed, prime),
        ]
        for prime in MODULAR_PRIMES
    }

    progress(arguments.progress, started, "restricting exact image", dimension=cycle_rank)
    characteristic, image_metadata = image_characteristic(cycle, dense_cycle)
    expected_characteristic = expected_image_characteristic()

    progress(arguments.progress, started, "checking direct seven-carrier convolutions")
    direct = direct_transfer_audit(transfers, arguments.max_direct_level)

    progress(arguments.progress, started, "isolating exact reachable scalar")
    reachable = exact_reachable_data(transfers, arguments.sequence_terms)
    projection = dominant_projection_interval(reachable)
    degree_ten_schur = schur_disk_certificate(
        SCALED_DEGREE_TEN, REMAINDER_RADIUS
    )
    degree_eighteen_schur = schur_disk_certificate(
        DEGREE_EIGHTEEN, REMAINDER_RADIUS
    )

    quartic_scaling = [
        R066_QUARTIC[index] * 256**index
        for index in range(len(R066_QUARTIC))
    ]
    degree_ten_scaling = [
        R067_DEGREE_TEN[index] * 16**index
        for index in range(len(R067_DEGREE_TEN))
    ]
    critical_rate_upper = Fraction(256, 25**2)
    checks = {
        "stateDimensionIsTwoTimesOneTwentyEightTimesSeven": (
            DIMENSION == 2 * 128 * 7
        ),
        "digitTransfersHaveExactRankFourFortyEight": (
            digit_exact_ranks == [448, 448]
        ),
        "cycleExactRanksAreTwoZeroFourThenOneFourEight": (
            [cycle_rank, cycle_squared_rank, cycle_cubed_rank]
            == [IMAGE_DIMENSION, STABLE_IMAGE_DIMENSION, STABLE_IMAGE_DIMENSION]
        ),
        "cycleModularRanksConfirmTwoIndependentPrimes": all(
            ranks == [IMAGE_DIMENSION, STABLE_IMAGE_DIMENSION, STABLE_IMAGE_DIMENSION]
            for ranks in modular_ranks.values()
        ),
        "imageCoordinatesAreNonsingularOverTwoPrimes": all(
            image_metadata["coordinateDeterminantNonzeroModulo"].values()
        ),
        "imageCharacteristicHasDegreeTwoZeroFour": (
            len(characteristic) == IMAGE_DIMENSION + 1
        ),
        "imageCharacteristicMatchesExactFactorization": (
            characteristic == expected_characteristic
        ),
        "quarticIsTwoFiftySixRescalingOfR066": (
            quartic_scaling == SCALED_QUARTIC
        ),
        "degreeTenIsSixteenRescalingOfR067": (
            degree_ten_scaling == SCALED_DEGREE_TEN
        ),
        "directConvolutionMatchesAllStates": (
            len(direct) == arguments.max_direct_level
        ),
        "reachableVectorRecurrenceStartsAfterOneTransient": (
            bool(reachable["recurrenceResidualAtR33"])
            and bool(reachable["recurrenceResidualsFromR34AreZero"])
            and bool(reachable["vectorRecurrenceFromR34IsExact"])
        ),
        "reachableGeneratingFunctionIsReduced": (
            reachable["generatingGcdAscending"] == [1]
        ),
        "dominantQuarticRootIsStrictlyBracketed": (
            Fraction(projection["scaledQuarticAtLower"]) < 0
            < Fraction(projection["scaledQuarticAtUpper"])
        ),
        "degreeTenRootsAreStrictlyInsideRadiusFourThousandEightHundred": all(
            record["strictSchurInequality"] for record in degree_ten_schur
        ),
        "degreeEighteenRootsAreStrictlyInsideRadiusFourThousandEightHundred": all(
            record["strictSchurInequality"] for record in degree_eighteen_schur
        ),
        "dominantProjectionCoefficientIsStrictlyNegative": bool(
            projection["coefficientIsStrictlyNegative"]
        ),
        "quarticCriticalEighthProbeRateIsBelowFortyOneHundredths": (
            critical_rate_upper < Fraction(41, 100)
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    characteristic_sha = hashlib.sha256(
        json.dumps(characteristic, separators=(",", ":")).encode()
    ).hexdigest()
    report = {
        "schemaVersion": "1.0",
        "status": "passed",
        "classification": (
            "exact zero-time eighth-order seven-carrier spectrum and reachable "
            "projection theorem for one invariant-shear packet; not a certificate "
            "for the complete heat-weighted seven-simplex observable, the full "
            "Picard series, or three-dimensional Navier--Stokes regularity"
        ),
        "checks": checks,
        "pathFormula": {
            "signPattern": "A+B+C+D-E-F-G=Q",
            "positiveCarriers": POSITIVE_CARRIERS,
            "negativeCarriers": NEGATIVE_CARRIERS,
            "timeOrderSignPlacements": 35,
            "sixFreeCarrierIndices": True,
            "eighthFourierPrefactor": "i m^7 exp(-m^2 t_H) H^-14",
            "normalizedRatio": (
                "A^8 G8/(A^2 G2)=-(epsilon^6/L^6) R8, "
                "R8=L^6 m^6 S8/(H^9 S2)"
            ),
        },
        "stateSpace": {
            "targetSignStates": 2,
            "septicSignStates": SIGN_STATES,
            "carries": list(CARRIES),
            "dimension": DIMENSION,
            "digitNonzeros": [int(transfer.nnz) for transfer in transfers],
            "digitExactRanks": digit_exact_ranks,
        },
        "cycle": {
            "wordLeastSignificantBitFirst": list(WORD),
            "nonzerosByPower": [
                int(cycle.nnz),
                int(cycle_squared.nnz),
                int(cycle_cubed.nnz),
            ],
            "exactRanksByPower": [
                cycle_rank,
                cycle_squared_rank,
                cycle_cubed_rank,
            ],
            "modularRanksByPrime": modular_ranks,
            "imageDimension": IMAGE_DIMENSION,
            "stableImageDimension": STABLE_IMAGE_DIMENSION,
            "imageRestrictionMetadata": image_metadata,
            "imageCharacteristicPolynomialDescending": characteristic,
            "imageCharacteristicSha256": characteristic_sha,
            "imageCharacteristicFactorization": (
                "x^56 (x-4096)^14 q4_256(x)^14 "
                "q10_16(x)^6 q18(x)"
            ),
            "fullCharacteristicFactorization": (
                "x^1588 times the image characteristic polynomial"
            ),
            "scaledQuartic": SCALED_QUARTIC,
            "scaledDegreeTen": SCALED_DEGREE_TEN,
            "degreeEighteen": DEGREE_EIGHTEEN,
            "dominantRoot": (
                "nu is the unique root outside |x|<=4800; "
                "nu=256 lambda from R0.66"
            ),
            "remainderRadius": REMAINDER_RADIUS,
            "degreeTenSchurCertificate": degree_ten_schur,
            "degreeEighteenSchurCertificate": degree_eighteen_schur,
        },
        "reachableTargetFamily": {
            "M": "16^r",
            "q": "2(16^r-1)/15",
            **reachable,
            "dominantProjection": projection,
            "asymptotic": (
                "Y8_r=C8,0 nu^r+O(4800^r), with the strict negative "
                "C8,0 interval recorded here"
            ),
            "zeroTimeSpatialThreshold": "M_r^3=4096^r",
            "quarticCriticalAmplitudeProbeRate": "256/lambda^2",
            "coarseCertifiedProbeRateUpper": str(critical_rate_upper),
            "heatBoundary": (
                "the complete seven-simplex heat projection is not evaluated"
            ),
        },
        "directAudit": {
            "exactLevelsChecked": arguments.max_direct_level,
            "records": direct,
        },
        "provenance": {
            "sourceCommit": arguments.source_commit,
            "script": "research/eighth_order_cycle_audit.py",
            "requirements": "research/requirements-r068b.txt",
            "randomness": False,
        },
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "sympy": sympy.__version__,
        },
        "wallSeconds": time.perf_counter() - started,
    }
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(report, indent=2, sort_keys=True) + "\n"
    temporary = arguments.output.with_suffix(arguments.output.suffix + ".tmp")
    temporary.write_text(payload, encoding="utf-8")
    temporary.replace(arguments.output)
    print(payload, end="")


if __name__ == "__main__":
    main()
