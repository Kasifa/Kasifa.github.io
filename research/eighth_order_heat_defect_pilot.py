#!/usr/bin/env python3
"""R0.68B-2c pilot for a sharpened degree-ten heat-defect bound.

The degree-eight centred jet from R0.68B-2b is numerically stable, but its
zero-eight-jet defect is too large for the first global derivative majorants.
This script raises the spatial jet to degree ten and exploits a new exact
compression of the six-dimensional affine shifts.

For a fixed free shift e in {0,...,15}^6, only the sixteen four-bit strings of
the dependent seventh carrier remain.  After carry admissibility and Fourier
signs are imposed, these sixteen branches aggregate into a fourteen-component
integer signature indexed by the dependent least-significant bit and the
seven possible input carries.  Across one fixed free least-significant-bit
pattern, the 8^6 upper-bit combinations collapse to about seven hundred
"distance shell + signature" classes.

The output is still exploratory:

* dominant moments and heat coefficients use binary64 arithmetic;
* the observable defect is aggregated exactly at the combinatorial level,
  but its coefficients come from the binary64 moment lift;
* the eleventh-derivative majorant is complete only for the six pure
  multiindices, not for all 4,368 mixed multiindices.

It is therefore not a sign theorem and not a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
import collections
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy

import eighth_order_cycle_audit as r068
import eighth_order_heat_jet_pilot as jet


VARIABLES = 6
CENTER = 0.5
THETA = 2 / 15
DEFAULT_DEGREE = 10
DEFAULT_HEAT_ORDER = 64
OBSERVABLE_STATE = r068.state_index(0, 0, 0)
UPPER_COMBINATIONS = 8**VARIABLES
FREE_SHIFT_COUNT = 16**VARIABLES
MAXIMUM_DISTANCE = 45 / 16
EXACT_CARRY_WEIGHTS = (
    64,
    24_137_121,
    904_780_185,
    3_769_909_270,
    3_049_493_910,
    448_102_641,
    4_826_809,
)


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.68B-2c defect pilot +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def carry_digit_matrix(bit: int) -> np.ndarray:
    matrix = np.zeros((len(r068.CARRIES), len(r068.CARRIES)), dtype=object)
    for row, parent in enumerate(r068.CARRIES):
        for positive_ones in range(r068.POSITIVE_CARRIERS + 1):
            for negative_ones in range(r068.NEGATIVE_CARRIERS + 1):
                signed_shift = positive_ones - negative_ones
                child = 2 * parent + bit - signed_shift
                if child not in r068.CARRIES:
                    continue
                multiplicity = math.comb(
                    r068.POSITIVE_CARRIERS, positive_ones
                ) * math.comb(r068.NEGATIVE_CARRIERS, negative_ones)
                matrix[row, r068.CARRIES.index(child)] += multiplicity
    return matrix


def exact_absolute_carry_data() -> tuple[np.ndarray, dict[str, object]]:
    digit = {bit: carry_digit_matrix(bit) for bit in (0, 1)}
    cycle = np.eye(len(r068.CARRIES), dtype=object)
    for bit in r068.WORD:
        cycle = digit[bit] @ cycle
    weights = np.array(EXACT_CARRY_WEIGHTS, dtype=object)
    eigenvalue = 16**VARIABLES
    image = cycle @ weights
    if list(image) != [eigenvalue * value for value in weights]:
        raise AssertionError("the proposed absolute carry weight is not exact")
    return cycle, {
        "cycleMatrix": [[int(value) for value in row] for row in cycle],
        "positiveCarryWeight": list(EXACT_CARRY_WEIGHTS),
        "eigenvalue": eigenvalue,
        "checks": {
            "weightIsStrictlyPositive": all(value > 0 for value in weights),
            "weightIsExactRightEigenvector": True,
            "eigenvalueEqualsSixFreeBitsPerDigit": eigenvalue == 16**6,
        },
    }


def state_weights() -> np.ndarray:
    return np.array(
        [
            weight
            for _target in (0, 1)
            for _septic in range(r068.SIGN_STATES)
            for weight in EXACT_CARRY_WEIGHTS
        ],
        dtype=float,
    )


def upper_digit_table() -> np.ndarray:
    values = np.arange(UPPER_COMBINATIONS, dtype=np.uint32)
    return np.stack(
        [((values >> (3 * coordinate)) & 7).astype(np.int8) for coordinate in range(VARIABLES)],
        axis=1,
    )


def free_lsb_epsilon(lsb_code: int) -> int:
    return sum(
        ((lsb_code >> coordinate) & 1)
        << (r068.CARRIER_COUNT - 1 - coordinate)
        for coordinate in range(VARIABLES)
    )


def signature_table(
    lsb_code: int, upper: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return the distance shell and fourteen-component signature at every shift."""
    lsb = np.array(
        [(lsb_code >> coordinate) & 1 for coordinate in range(VARIABLES)],
        dtype=np.int8,
    )
    shifts = 2 * upper + lsb
    bit1 = np.broadcast_to(lsb, (len(upper), VARIABLES))
    bit2 = upper & 1
    bit3 = (upper >> 1) & 1
    bit4 = (upper >> 2) & 1
    free_signed_shifts = [
        bits[:, : r068.POSITIVE_CARRIERS].sum(axis=1).astype(np.int8)
        - bits[:, r068.POSITIVE_CARRIERS :].sum(axis=1).astype(np.int8)
        for bits in (bit1, bit2, bit3, bit4)
    ]
    free_parity = (
        (bit4 * bit3 + bit3 * bit2 + bit2 * bit1).sum(axis=1) & 1
    ).astype(np.int8)
    signatures = np.zeros((len(upper), 2 * len(r068.CARRIES)), dtype=np.int8)

    # word=(0,1,0,0), read from least to most significant bit.
    for dependent_shift in range(16):
        dependent_bits = [
            (dependent_shift >> bit_index) & 1 for bit_index in range(4)
        ]
        signed_shifts = [
            free_signed_shifts[index] - dependent_bits[index]
            for index in range(4)
        ]
        carry3 = -signed_shifts[3]
        carry2 = 2 * carry3 - signed_shifts[2]
        carry1 = 2 * carry2 + 1 - signed_shifts[1]
        input_carry = 2 * carry1 - signed_shifts[0]
        valid = (
            (np.abs(carry3) <= r068.POSITIVE_CARRIERS - 1)
            & (np.abs(carry2) <= r068.POSITIVE_CARRIERS - 1)
            & (np.abs(carry1) <= r068.POSITIVE_CARRIERS - 1)
            & (np.abs(input_carry) <= r068.POSITIVE_CARRIERS - 1)
        )
        dependent_parity = (
            dependent_bits[3] * dependent_bits[2]
            + dependent_bits[2] * dependent_bits[1]
            + dependent_bits[1] * dependent_bits[0]
        ) & 1
        parity = free_parity ^ dependent_parity
        columns = (
            dependent_bits[0] * len(r068.CARRIES)
            + input_carry
            - r068.CARRIES[0]
        )
        rows = np.flatnonzero(valid)
        np.add.at(
            signatures,
            (rows, columns[rows]),
            np.where(parity[rows], -1, 1).astype(np.int8),
        )

    shells = np.abs(2 * shifts.astype(np.int16) - 15).sum(axis=1).astype(np.int8)
    return shells, signatures


def explicit_cycle_signature(
    free_shift: tuple[int, ...], transfers: list[object]
) -> np.ndarray:
    """Independent sparse-matrix check of one fourteen-component signature."""
    output = np.zeros(2 * len(r068.CARRIES), dtype=np.int64)
    free_bits = [
        tuple((value >> bit_index) & 1 for value in free_shift)
        for bit_index in range(4)
    ]
    final_row = OBSERVABLE_STATE
    for dependent_shift in range(16):
        dependent_bits = [
            (dependent_shift >> bit_index) & 1 for bit_index in range(4)
        ]
        epsilons = []
        for bit_index in range(4):
            digits = free_bits[bit_index] + (dependent_bits[bit_index],)
            epsilons.append(
                sum(
                    value << (r068.CARRIER_COUNT - 1 - coordinate)
                    for coordinate, value in enumerate(digits)
                )
            )
        carries = [0]
        coefficient = 1
        row = final_row
        for reverse_index in range(3, -1, -1):
            bit = r068.WORD[reverse_index]
            epsilon = epsilons[reverse_index]
            digits = tuple(
                (epsilon >> shift) & 1
                for shift in range(r068.CARRIER_COUNT - 1, -1, -1)
            )
            signed_shift = sum(digits[: r068.POSITIVE_CARRIERS]) - sum(
                digits[r068.POSITIVE_CARRIERS :]
            )
            child_carry = 2 * carries[-1] + bit - signed_shift
            if child_carry not in r068.CARRIES:
                coefficient = 0
                break
            column = r068.state_index(bit, epsilon, child_carry)
            coefficient *= int(transfers[bit][row, column])
            row = column
            carries.append(child_carry)
        if coefficient:
            input_carry = carries[-1]
            column = (
                dependent_bits[0] * len(r068.CARRIES)
                + input_carry
                - r068.CARRIES[0]
            )
            output[column] += coefficient
    return output


def signature_cross_checks(
    upper: np.ndarray, transfers: list[object]
) -> list[dict[str, object]]:
    records = []
    samples = (
        (0, 0),
        (0, 12345),
        (7, 54321),
        (21, 100000),
        (42, 200000),
        (63, UPPER_COMBINATIONS - 1),
    )
    for lsb_code, upper_index in samples:
        _shells, signatures = signature_table(lsb_code, upper[upper_index : upper_index + 1])
        lsb = tuple((lsb_code >> coordinate) & 1 for coordinate in range(VARIABLES))
        free_shift = tuple(
            2 * int(upper[upper_index, coordinate]) + lsb[coordinate]
            for coordinate in range(VARIABLES)
        )
        explicit = explicit_cycle_signature(free_shift, transfers)
        agrees = np.array_equal(signatures[0].astype(np.int64), explicit)
        if not agrees:
            raise AssertionError(f"signature check failed at {free_shift}")
        records.append(
            {
                "freeShift": list(free_shift),
                "nonzeros": int(np.count_nonzero(explicit)),
                "agreesWithSparseCycleEntries": agrees,
            }
        )
    return records


def channel_factor(alpha: tuple[int, ...], degree: int) -> float:
    return 1 / (
        math.prod(math.factorial(value) for value in alpha) * 16**degree
    )


def unaggregated_weighted_bound(
    degree: int,
    indices: list[tuple[int, ...]],
    centered: np.ndarray,
    transfers: list[object],
) -> tuple[np.ndarray, dict[str, object]]:
    absolute_transfers = []
    for transfer in transfers:
        absolute = transfer.copy().astype(float)
        absolute.data = np.abs(absolute.data)
        absolute_transfers.append(absolute)
    absolute_cycle = r068.cycle_matrix(absolute_transfers).astype(float)
    transported = absolute_cycle @ np.abs(centered).T
    bounds = np.zeros(r068.DIMENSION)
    for current_degree in range(degree + 1):
        selected = [
            index
            for index, alpha in enumerate(indices)
            if sum(alpha) == current_degree
        ]
        factors = np.array(
            [
                channel_factor(indices[index], current_degree)
                * MAXIMUM_DISTANCE ** (degree + 1 - current_degree)
                / math.factorial(degree + 1 - current_degree)
                for index in selected
            ]
        )
        bounds += transported[:, selected] @ factors
    weights = state_weights()
    weighted = bounds / weights
    return bounds, {
        "observable": float(bounds[OBSERVABLE_STATE]),
        "weightedMaximum": float(np.max(weighted)),
        "weightedMaximumState": int(np.argmax(weighted)),
        "method": (
            "Discard all same-shift cancellation, replace every six-dimensional "
            "distance by 45/16, and apply the exact absolute cycle."
        ),
    }


def observable_signature_bound(
    degree: int,
    indices: list[tuple[int, ...]],
    centered: np.ndarray,
    upper: np.ndarray,
    lsb_groups: int,
    report_progress: bool,
    started: float,
) -> tuple[float, dict[str, object]]:
    degree_indices = [
        [
            index
            for index, alpha in enumerate(indices)
            if sum(alpha) == current_degree
        ]
        for current_degree in range(degree + 1)
    ]
    factors = [
        np.array(
            [channel_factor(indices[index], current_degree) for index in selected]
        )
        for current_degree, selected in enumerate(degree_indices)
    ]
    by_degree = np.zeros(degree + 1)
    class_count = 0
    nonzero_shift_count = 0
    maximum_signature_entry = 0
    processed_shifts = 0
    for lsb_code in range(lsb_groups):
        shells, signatures = signature_table(lsb_code, upper)
        keyed = np.concatenate([shells[:, None], signatures], axis=1)
        unique, multiplicities = np.unique(keyed, axis=0, return_counts=True)
        class_count += len(unique)
        nonzero = np.any(unique[:, 1:] != 0, axis=1)
        nonzero_shift_count += int(multiplicities[nonzero].sum())
        maximum_signature_entry = max(
            maximum_signature_entry, int(np.max(np.abs(unique[:, 1:])))
        )
        processed_shifts += int(multiplicities.sum())

        epsilon = free_lsb_epsilon(lsb_code)
        states = [
            r068.state_index(0, epsilon + dependent_lsb, carry)
            for dependent_lsb in (0, 1)
            for carry in r068.CARRIES
        ]
        signature_values = unique[:, 1:].astype(float)
        distances = unique[:, 0].astype(float) / 32
        for current_degree, selected in enumerate(degree_indices):
            aggregated = np.abs(
                signature_values @ centered[selected][:, states].T
            )
            channel_sum = aggregated @ factors[current_degree]
            by_degree[current_degree] += np.dot(
                multiplicities,
                channel_sum
                * distances ** (degree + 1 - current_degree)
                / math.factorial(degree + 1 - current_degree),
            )
        if (lsb_code + 1) % 8 == 0 or lsb_code + 1 == lsb_groups:
            progress(
                report_progress,
                started,
                "signature compression",
                groups=f"{lsb_code + 1}/{lsb_groups}",
                classes=class_count,
                partial=f"{float(by_degree.sum()):.12g}",
            )
    return float(by_degree.sum()), {
        "byJetDegree": [float(value) for value in by_degree],
        "signatureClasses": class_count,
        "processedFreeShifts": processed_shifts,
        "nonzeroFreeShifts": nonzero_shift_count,
        "maximumAbsoluteSignatureEntry": maximum_signature_entry,
        "lsbGroups": lsb_groups,
        "fullFreeShiftCount": FREE_SHIFT_COUNT,
        "distanceShellUnit": "1/32",
        "signatureCoordinates": (
            "dependent least-significant bit (2) times input carry (7)"
        ),
    }


Poly = dict[tuple[int, ...], float]
TimePoly = dict[tuple[int, ...], float]


def poly_add(*values: Poly) -> Poly:
    output: collections.defaultdict[tuple[int, ...], float] = (
        collections.defaultdict(float)
    )
    for value in values:
        for alpha, coefficient in value.items():
            output[alpha] += coefficient
    return {alpha: coefficient for alpha, coefficient in output.items() if coefficient}


def poly_scale(value: Poly, scalar: float) -> Poly:
    return {alpha: scalar * coefficient for alpha, coefficient in value.items()}


def poly_multiply(left: Poly, right: Poly) -> Poly:
    output: collections.defaultdict[tuple[int, ...], float] = (
        collections.defaultdict(float)
    )
    for left_alpha, left_value in left.items():
        for right_alpha, right_value in right.items():
            output[
                tuple(
                    left_alpha[index] + right_alpha[index]
                    for index in range(VARIABLES)
                )
            ] += left_value * right_value
    return dict(output)


def poly_linear(constant: float, coefficients: list[float]) -> Poly:
    output: Poly = {(0,) * VARIABLES: constant}
    for coordinate, coefficient in enumerate(coefficients):
        if coefficient:
            alpha = [0] * VARIABLES
            alpha[coordinate] = 1
            output[tuple(alpha)] = coefficient
    return output


def poly_derivative(value: Poly, coordinate: int) -> Poly:
    output: collections.defaultdict[tuple[int, ...], float] = (
        collections.defaultdict(float)
    )
    for alpha, coefficient in value.items():
        if alpha[coordinate]:
            beta = list(alpha)
            beta[coordinate] -= 1
            output[tuple(beta)] += coefficient * alpha[coordinate]
    return dict(output)


def poly_cube_supremum(value: Poly) -> float:
    return max(
        abs(
            sum(
                coefficient
                * math.prod(
                    point[coordinate] ** alpha[coordinate]
                    for coordinate in range(VARIABLES)
                )
                for alpha, coefficient in value.items()
            )
        )
        for point in itertools.product((0, 1), repeat=VARIABLES)
    )


def rate_polynomials(word: tuple[int, ...]) -> list[Poly]:
    variables = [
        poly_linear(
            CENTER,
            [1.0 if other == coordinate else 0.0 for other in range(VARIABLES)],
        )
        for coordinate in range(VARIABLES)
    ]
    one = poly_linear(1.0, [0.0] * VARIABLES)
    dependent = poly_add(
        variables[0],
        variables[1],
        variables[2],
        variables[3],
        poly_scale(variables[4], -1),
        poly_scale(variables[5], -1),
        poly_linear(-THETA, [0.0] * VARIABLES),
    )
    magnitudes = [
        poly_add(one, poly_scale(variables[index], 0.25))
        for index in range(VARIABLES)
    ] + [poly_add(one, poly_scale(dependent, 0.25))]
    positives = iter(magnitudes[:4])
    negatives = iter(magnitudes[4:])
    carriers = [
        next(positives) if sign > 0 else poly_scale(next(negatives), -1)
        for sign in word
    ]
    current = poly_linear(-(1 + THETA / 4), [0.0] * VARIABLES)
    suffix = poly_add(*(poly_multiply(value, value) for value in carriers))
    rates = []
    for carrier in carriers:
        rates.append(poly_add(poly_multiply(current, current), suffix))
        suffix = poly_add(
            suffix, poly_scale(poly_multiply(carrier, carrier), -1)
        )
        current = poly_add(current, carrier)
    return rates


def time_multiply(left: TimePoly, right: TimePoly) -> TimePoly:
    output: collections.defaultdict[tuple[int, ...], float] = (
        collections.defaultdict(float)
    )
    for left_alpha, left_value in left.items():
        for right_alpha, right_value in right.items():
            output[
                tuple(left_alpha[index] + right_alpha[index] for index in range(7))
            ] += left_value * right_value
    return dict(output)


def time_power(linear_coefficients: list[float], exponent: int) -> TimePoly:
    output: TimePoly = {(0,) * 7: 1.0}
    linear = {
        tuple(1 if other == coordinate else 0 for other in range(7)): coefficient
        for coordinate, coefficient in enumerate(linear_coefficients)
        if coefficient
    }
    for _ in range(exponent):
        output = time_multiply(output, linear)
    return output


def simplex_integral(value: TimePoly, time_value: float) -> float:
    return sum(
        coefficient
        * time_value ** (sum(alpha) + 7)
        * math.prod(math.factorial(exponent) for exponent in alpha)
        / math.factorial(sum(alpha) + 7)
        for alpha, coefficient in value.items()
    )


def pure_derivative_majorants(
    derivative_order: int,
    time_value: float,
    report_progress: bool,
    started: float,
) -> tuple[list[float], dict[str, object]]:
    totals = [0.0] * VARIABLES
    wordwise_maxima = []
    records = []
    for word_index, word in enumerate(jet.shuffle_words()):
        rates = rate_polynomials(word)
        word_values = []
        for coordinate in range(VARIABLES):
            first = [
                poly_cube_supremum(poly_derivative(rate, coordinate))
                for rate in rates
            ]
            second = [
                poly_cube_supremum(
                    poly_derivative(poly_derivative(rate, coordinate), coordinate)
                )
                for rate in rates
            ]
            first_powers = {
                exponent: time_power(first, exponent)
                for exponent in range(1, derivative_order + 1, 2)
            }
            second_powers = {
                exponent: time_power(second, exponent)
                for exponent in range(derivative_order // 2 + 1)
            }
            value = 0.0
            for pairs in range(derivative_order // 2 + 1):
                singles = derivative_order - 2 * pairs
                coefficient = math.factorial(derivative_order) / (
                    math.factorial(singles)
                    * math.factorial(pairs)
                    * 2**pairs
                )
                value += coefficient * simplex_integral(
                    time_multiply(
                        first_powers[singles], second_powers[pairs]
                    ),
                    time_value,
                )
            totals[coordinate] += value
            word_values.append(value)
        word_maximum = max(word_values)
        wordwise_maxima.append(word_maximum)
        records.append(
            {
                "word": list(word),
                "pureBounds": word_values,
                "maximum": word_maximum,
                "maximumCoordinate": int(np.argmax(word_values)),
            }
        )
        progress(
            report_progress,
            started,
            "pure derivative majorants",
            shuffle=f"{word_index + 1}/{len(jet.shuffle_words())}",
            maximum=f"{word_maximum:.12e}",
        )
    return totals, {
        "derivativeOrder": derivative_order,
        "pureMultiindexBounds": totals,
        "maximumPureBound": max(totals),
        "maximumPureCoordinate": int(np.argmax(totals)),
        "sumOfWordwisePureMaxima": sum(wordwise_maxima),
        "perShuffle": records,
        "scope": (
            "all six pure derivatives only; mixed multiindices are not certified"
        ),
        "method": (
            "Use exact seven-simplex monomial integrals. For each rate and "
            "coordinate, bound the affine first derivative on cube vertices and "
            "use the constant pure second derivative in the Hermite pairing sum."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-degree", type=int, default=DEFAULT_DEGREE)
    parser.add_argument("--heat-order", type=int, default=DEFAULT_HEAT_ORDER)
    parser.add_argument("--lsb-groups", type=int, default=64)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if not 0 <= arguments.max_degree <= 10:
        raise ValueError("max-degree must lie between zero and ten")
    if not 1 <= arguments.lsb_groups <= 64:
        raise ValueError("lsb-groups must lie between one and sixty-four")
    if arguments.heat_order < 32:
        raise ValueError("heat-order must be at least 32")
    started = time.perf_counter()

    progress(arguments.progress, started, "constructing exact carry data")
    _carry_cycle, carry_metadata = exact_absolute_carry_data()
    transfers = [r068.signed_digit_transfer(0), r068.signed_digit_transfer(1)]
    cycle = r068.cycle_matrix(transfers).astype(float)
    groups = {bit: jet.digit_edge_groups(bit) for bit in (0, 1)}
    subset_matrices = {
        bit: jet.subset_transfer_matrices(groups[bit]) for bit in (0, 1)
    }
    dominant_root = max(
        root.real
        for root in np.roots(r068.SCALED_QUARTIC)
        if abs(root.imag) < 1.0e-7
    )
    mass, mass_record = jet.reachable_dominant_mass(cycle, dominant_root)

    progress(arguments.progress, started, "lifting dominant moments")
    indices, raw_moments, moment_records = jet.dominant_moments(
        arguments.max_degree,
        cycle,
        dominant_root,
        mass,
        subset_matrices,
        arguments.progress,
        started,
    )
    centered = jet.centered_moments(indices, raw_moments)

    progress(arguments.progress, started, "evaluating heat jet and next derivative")
    time_value = math.log(2) / 2
    heat_indices, heat_coefficients = jet.heat_taylor_coefficients(
        arguments.max_degree + 1, arguments.heat_order, time_value
    )
    if heat_indices[: len(indices)] != indices:
        raise AssertionError("moment and heat multiindex orders disagree")
    heat_jet = float(
        sum(
            centered[index, OBSERVABLE_STATE] * heat_coefficients[index]
            for index in range(len(indices))
        )
    )
    derivative_indices = [
        index
        for index, alpha in enumerate(heat_indices)
        if sum(alpha) == arguments.max_degree + 1
    ]
    center_derivatives = [
        abs(heat_coefficients[index])
        * math.prod(math.factorial(value) for value in heat_indices[index])
        for index in derivative_indices
    ]
    center_maximum_index = derivative_indices[int(np.argmax(center_derivatives))]

    unaggregated, unaggregated_metadata = unaggregated_weighted_bound(
        arguments.max_degree, indices, centered, transfers
    )
    upper = upper_digit_table()
    cross_checks = signature_cross_checks(upper, transfers)
    progress(arguments.progress, started, "aggregating shift signatures")
    observable_defect, signature_metadata = observable_signature_bound(
        arguments.max_degree,
        indices,
        centered,
        upper,
        arguments.lsb_groups,
        arguments.progress,
        started,
    )

    progress(arguments.progress, started, "bounding pure next derivatives")
    pure_bounds, derivative_metadata = pure_derivative_majorants(
        arguments.max_degree + 1,
        time_value,
        arguments.progress,
        started,
    )

    weights = state_weights()
    contraction = 16 ** (VARIABLES - arguments.max_degree - 1)
    resolvent_ratio = contraction / dominant_root
    resolvent_observable = (
        observable_defect / dominant_root
        + weights[OBSERVABLE_STATE]
        * unaggregated_metadata["weightedMaximum"]
        / dominant_root
        * resolvent_ratio
        / (1 - resolvent_ratio)
    )
    required_derivative = abs(heat_jet) / resolvent_observable
    pure_correction = (
        resolvent_observable * derivative_metadata["maximumPureBound"]
    )
    wordwise_pure_correction = (
        resolvent_observable
        * derivative_metadata["sumOfWordwisePureMaxima"]
    )

    full_run = (
        arguments.max_degree == DEFAULT_DEGREE
        and arguments.lsb_groups == 64
        and arguments.heat_order == DEFAULT_HEAT_ORDER
    )
    checks = {
        "exactAbsoluteCarryWeightPasses": all(carry_metadata["checks"].values()),
        "signatureSpotChecksPass": all(
            record["agreesWithSparseCycleEntries"] for record in cross_checks
        ),
        "allMomentResidualsAreSmall": all(
            record["relativeLinearResidual"] < 1.0e-10
            for record in moment_records
        ),
        "signatureEntriesAreZeroOrUnit": (
            signature_metadata["maximumAbsoluteSignatureEntry"] <= 1
        ),
        "fullRunProcessesEveryFreeShift": (
            not full_run
            or signature_metadata["processedFreeShifts"] == FREE_SHIFT_COUNT
        ),
        "degreeTenHeatJetAgreesWithDegreeEightPilot": (
            not full_run or abs(heat_jet + 1.4923824320396173e-8) < 3.0e-18
        ),
        "pureDerivativeBoundIsBelowRequiredThreshold": (
            derivative_metadata["maximumPureBound"] < required_derivative
        ),
        "wordwisePureMaximumSumIsBelowRequiredThreshold": (
            derivative_metadata["sumOfWordwisePureMaxima"] < required_derivative
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "exploratory-passed",
        "classification": (
            "binary64 degree-ten shift-defect and pure-eleventh-derivative "
            "pilot for the dominant eighth-order heat projection; all mixed "
            "eleventh derivatives remain uncertified"
        ),
        "checks": {key: bool(value) for key, value in checks.items()},
        "parameters": {
            "jetDegree": arguments.max_degree,
            "derivativeOrder": arguments.max_degree + 1,
            "spatialVariables": VARIABLES,
            "channelsPerState": len(indices),
            "totalMomentCoordinates": len(indices) * r068.DIMENSION,
            "heatTaylorOrder": arguments.heat_order,
            "heatTime": "log(2)/2",
            "lsbGroups": arguments.lsb_groups,
            "fullRun": full_run,
        },
        "dominantRoot": dominant_root,
        "massProjection": mass_record,
        "momentLift": moment_records,
        "absoluteCarry": carry_metadata,
        "heatJet": {
            "value": heat_jet,
            "nextDerivativeAtCenterMaximum": max(center_derivatives),
            "nextDerivativeAtCenterMultiindex": list(
                heat_indices[center_maximum_index]
            ),
            "nextDerivativeAtCenterSum": sum(center_derivatives),
        },
        "signatureCompression": {
            **signature_metadata,
            "spotChecks": cross_checks,
        },
        "defect": {
            "observableAggregated": observable_defect,
            "unaggregated": unaggregated_metadata,
        },
        "resolvent": {
            "remainderContraction": contraction,
            "ratioToDominantRoot": resolvent_ratio,
            "observableUpper": resolvent_observable,
        },
        "pureDerivativeMajorants": derivative_metadata,
        "gapDiagnostics": {
            "requiredGlobalDerivativeUpper": required_derivative,
            "pureCorrectionUpper": pure_correction,
            "wordwisePureMaximumCorrectionUpper": wordwise_pure_correction,
            "heatJetMagnitude": abs(heat_jet),
        },
        "limitations": [
            "The moment lift and heat coefficients use binary64 arithmetic.",
            "The observable defect is not yet enclosed by outward-rounded interval arithmetic.",
            "Only the six pure eleventh derivatives are bounded completely.",
            "All 4,368 mixed eleventh-derivative multiindices remain to be certified or dominated analytically.",
            "No strict sign theorem is claimed.",
            "No claim is made about all Picard orders or general 3D Navier-Stokes regularity.",
        ],
        "provenance": {"sourceCommit": arguments.source_commit},
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized)
    progress(
        arguments.progress,
        started,
        "complete",
        defect=f"{observable_defect:.12g}",
        required=f"{required_derivative:.12e}",
    )
    sys.stdout.write(serialized)


if __name__ == "__main__":
    main()
