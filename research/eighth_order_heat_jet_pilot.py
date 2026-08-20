#!/usr/bin/env python3
"""Exploratory finite-jet pilot for the R0.68B-2b heat projection.

The seven-carrier constraint has six free normalized coordinates.  This
script constructs their affine moment lift over the exact 1792-state cycle,
selects the reachable dominant mass component by normalized power iteration,
and pairs the lifted moments with the complete 35-shuffle seven-simplex heat
observable.

The digit transport is factorized by the support of each translation
multiindex.  There are only 2^6 subset transfer matrices, rather than one
dense channel transform for every one of the 128 carrier-bit patterns.

This file is a numerical architecture and convergence pilot.  It does not
bound the zero-jet defect, the ninth derivatives, or the final dominant heat
projection, and it is not a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
import itertools
import json
import math
import platform
import sys
import time
from pathlib import Path

import numpy as np
import scipy
from scipy.sparse import csr_matrix

import eighth_order_cycle_audit as r068


VARIABLES = 6
CENTER = 0.5
THETA = 2 / 15
DEFAULT_DEGREE = 4
DEFAULT_HEAT_ORDER = 64
OBSERVABLE_STATE = r068.state_index(0, 0, 0)


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.68B-2b heat jet pilot +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def multiindices(maximum_degree: int) -> list[tuple[int, ...]]:
    return [
        alpha
        for degree in range(maximum_degree + 1)
        for alpha in itertools.product(range(degree + 1), repeat=VARIABLES)
        if sum(alpha) == degree
    ]


def digit_edge_groups(
    bit: int,
) -> list[tuple[int, np.ndarray, np.ndarray, np.ndarray]]:
    groups: list[tuple[int, np.ndarray, np.ndarray, np.ndarray]] = []
    for epsilon in range(1 << r068.CARRIER_COUNT):
        digits = tuple(
            (epsilon >> shift) & 1
            for shift in range(r068.CARRIER_COUNT - 1, -1, -1)
        )
        free_mask = sum(digits[index] << index for index in range(VARIABLES))
        rows: list[int] = []
        columns: list[int] = []
        signs: list[int] = []
        signed_shift = sum(digits[:4]) - sum(digits[4:])
        for target_state in (0, 1):
            for septic_state in range(r068.SIGN_STATES):
                for parent_carry in r068.CARRIES:
                    child_carry = 2 * parent_carry + bit - signed_shift
                    if child_carry not in r068.CARRIES:
                        continue
                    rows.append(
                        r068.state_index(target_state, septic_state, parent_carry)
                    )
                    columns.append(r068.state_index(bit, epsilon, child_carry))
                    parity = (
                        target_state * bit
                        + (septic_state & epsilon).bit_count()
                    )
                    signs.append(-1 if parity % 2 else 1)
        if len(rows) != len(set(rows)):
            raise AssertionError("one epsilon group must map every row at most once")
        groups.append(
            (
                free_mask,
                np.array(rows, dtype=np.int32),
                np.array(columns, dtype=np.int32),
                np.array(signs, dtype=float),
            )
        )
    return groups


def subset_transfer_matrices(
    groups: list[tuple[int, np.ndarray, np.ndarray, np.ndarray]],
) -> list[csr_matrix]:
    row_buckets: list[list[np.ndarray]] = [[] for _ in range(1 << VARIABLES)]
    column_buckets: list[list[np.ndarray]] = [[] for _ in range(1 << VARIABLES)]
    value_buckets: list[list[np.ndarray]] = [[] for _ in range(1 << VARIABLES)]
    for pattern, rows, columns, signs in groups:
        subset = pattern
        while True:
            row_buckets[subset].append(rows)
            column_buckets[subset].append(columns)
            value_buckets[subset].append(signs)
            if subset == 0:
                break
            subset = (subset - 1) & pattern
    output: list[csr_matrix] = []
    for mask in range(1 << VARIABLES):
        rows = np.concatenate(row_buckets[mask])
        columns = np.concatenate(column_buckets[mask])
        values = np.concatenate(value_buckets[mask])
        matrix = csr_matrix(
            (values, (rows, columns)),
            shape=(r068.DIMENSION, r068.DIMENSION),
        )
        matrix.sum_duplicates()
        matrix.eliminate_zeros()
        output.append(matrix)
    return output


def channel_translation_operators(
    indices: list[tuple[int, ...]], length: int
) -> list[tuple[np.ndarray, csr_matrix] | None]:
    index_map = {alpha: index for index, alpha in enumerate(indices)}
    pairs: list[list[tuple[int, int, float]]] = [
        [] for _ in range(1 << VARIABLES)
    ]
    for target, alpha in enumerate(indices):
        for beta in itertools.product(*(range(value + 1) for value in alpha)):
            gamma = tuple(alpha[index] - beta[index] for index in range(VARIABLES))
            mask = sum(
                int(gamma[index] > 0) << index for index in range(VARIABLES)
            )
            coefficient = 1
            for coordinate in range(VARIABLES):
                coefficient *= (
                    math.comb(alpha[coordinate], beta[coordinate])
                    * length ** gamma[coordinate]
                )
            pairs[mask].append((target, index_map[beta], float(coefficient)))

    output: list[tuple[np.ndarray, csr_matrix] | None] = []
    for records in pairs:
        if not records:
            output.append(None)
            continue
        sources = np.array(sorted({source for _target, source, _value in records}))
        source_map = {int(source): index for index, source in enumerate(sources)}
        operator = csr_matrix(
            (
                np.array([value for _target, _source, value in records]),
                (
                    np.array([target for target, _source, _value in records]),
                    np.array(
                        [source_map[source] for _target, source, _value in records]
                    ),
                ),
            ),
            shape=(len(indices), len(sources)),
        )
        output.append((sources, operator))
    return output


def digit_moment_step(
    moments: np.ndarray,
    subset_matrices: list[csr_matrix],
    operators: list[tuple[np.ndarray, csr_matrix] | None],
) -> np.ndarray:
    output = np.zeros_like(moments)
    for mask, record in enumerate(operators):
        if record is None:
            continue
        sources, channel_operator = record
        transported = subset_matrices[mask] @ moments[sources].T
        output += channel_operator @ transported.T
    return output


def raw_moment_cycle(
    moments: np.ndarray,
    indices: list[tuple[int, ...]],
    subset_matrices: dict[int, list[csr_matrix]],
) -> np.ndarray:
    output = moments
    for length, bit in zip((1, 2, 4, 8), r068.WORD):
        operators = channel_translation_operators(indices, length)
        output = digit_moment_step(output, subset_matrices[bit], operators)
    return output


def reachable_dominant_mass(
    cycle: csr_matrix, dominant_root: float, iterations: int = 220
) -> tuple[np.ndarray, dict[str, float | int]]:
    vector = r068.initial_vector().astype(float)
    for _ in range(iterations):
        vector = cycle @ vector / dominant_root
    residual = cycle @ vector - dominant_root * vector
    return vector, {
        "iterations": iterations,
        "observable": float(vector[OBSERVABLE_STATE]),
        "maximumEigenResidual": float(np.max(np.abs(residual))),
    }


def neumann_solve(
    cycle: csr_matrix,
    scalar: float,
    right_hand_side: np.ndarray,
    tolerance: float = 1.0e-17,
    maximum_terms: int = 100,
) -> tuple[np.ndarray, int, float]:
    term = right_hand_side / scalar
    solution = term.copy()
    terms = 1
    while terms < maximum_terms:
        term = cycle @ term / scalar
        solution += term
        terms += 1
        if float(np.max(np.abs(term))) < tolerance:
            break
    residual = scalar * solution - cycle @ solution - right_hand_side
    relative = float(np.max(np.abs(residual))) / max(
        1.0, float(np.max(np.abs(right_hand_side)))
    )
    return solution, terms, relative


def dominant_moments(
    maximum_degree: int,
    cycle: csr_matrix,
    dominant_root: float,
    mass: np.ndarray,
    subset_matrices: dict[int, list[csr_matrix]],
    report_progress: bool,
    started: float,
) -> tuple[list[tuple[int, ...]], np.ndarray, list[dict[str, object]]]:
    old_indices: list[tuple[int, ...]] = []
    old_moments = np.empty((0, r068.DIMENSION))
    records: list[dict[str, object]] = []
    for degree in range(maximum_degree + 1):
        indices = multiindices(degree)
        index_map = {alpha: index for index, alpha in enumerate(indices)}
        moments = np.zeros((len(indices), r068.DIMENSION))
        if degree == 0:
            moments[0] = mass
            terms = 0
            relative_residual = 0.0
        else:
            for old_index, alpha in enumerate(old_indices):
                moments[index_map[alpha]] = old_moments[old_index]
            transported = raw_moment_cycle(moments, indices, subset_matrices)
            current = [
                index for index, alpha in enumerate(indices) if sum(alpha) == degree
            ]
            scalar = 16**degree * dominant_root
            solution, terms, relative_residual = neumann_solve(
                cycle, scalar, transported[current].T
            )
            moments[current] = solution.T
        records.append(
            {
                "degree": degree,
                "cumulativeChannels": len(indices),
                "homogeneousChannels": math.comb(degree + VARIABLES - 1, VARIABLES - 1),
                "neumannTerms": terms,
                "relativeLinearResidual": relative_residual,
                "maximumAbsoluteMomentAtDegree": float(
                    np.max(
                        np.abs(
                            moments[
                                [
                                    index
                                    for index, alpha in enumerate(indices)
                                    if sum(alpha) == degree
                                ]
                            ]
                        )
                    )
                ),
            }
        )
        progress(
            report_progress,
            started,
            "moment lift",
            degree=degree,
            channels=len(indices),
            terms=terms,
            residual=f"{relative_residual:.3e}",
        )
        old_indices, old_moments = indices, moments
    return old_indices, old_moments, records


def centered_moments(
    indices: list[tuple[int, ...]], raw_moments: np.ndarray
) -> np.ndarray:
    output = np.zeros_like(raw_moments)
    index_map = {alpha: index for index, alpha in enumerate(indices)}
    for target, alpha in enumerate(indices):
        for beta in itertools.product(*(range(value + 1) for value in alpha)):
            coefficient = 1.0
            for coordinate in range(VARIABLES):
                coefficient *= (
                    math.comb(alpha[coordinate], beta[coordinate])
                    * (-CENTER) ** (alpha[coordinate] - beta[coordinate])
                )
            output[target] += coefficient * raw_moments[index_map[beta]]
    return output


def shuffle_words() -> list[tuple[int, ...]]:
    output = []
    for positive_positions in itertools.combinations(range(7), 4):
        positive = set(positive_positions)
        output.append(
            tuple(1 if index in positive else -1 for index in range(7))
        )
    return output


def heat_taylor_coefficients(
    maximum_degree: int, series_order: int, time_value: float
) -> tuple[list[tuple[int, ...]], np.ndarray]:
    """Return coefficients in y=x-c, already including alpha!^-1."""
    indices = multiindices(maximum_degree)
    index_map = {alpha: index for index, alpha in enumerate(indices)}

    def constant(value: float = 0.0) -> np.ndarray:
        output = np.zeros(len(indices))
        output[0] = value
        return output

    def variable(coordinate: int) -> np.ndarray:
        output = constant(CENTER)
        alpha = [0] * VARIABLES
        alpha[coordinate] = 1
        output[index_map[tuple(alpha)]] = 1.0
        return output

    def add(*values: np.ndarray) -> np.ndarray:
        return sum(values, np.zeros(len(indices)))

    def multiply_sparse(left: np.ndarray, right: np.ndarray) -> np.ndarray:
        output = np.zeros(len(indices))
        for left_index in np.flatnonzero(left):
            for right_index in np.flatnonzero(right):
                alpha = tuple(
                    indices[left_index][coordinate]
                    + indices[right_index][coordinate]
                    for coordinate in range(VARIABLES)
                )
                if sum(alpha) <= maximum_degree:
                    output[index_map[alpha]] += (
                        left[left_index] * right[right_index]
                    )
        return output

    def rate_maps(rate: np.ndarray) -> list[tuple[float, np.ndarray, np.ndarray]]:
        output = []
        for rate_index in np.flatnonzero(rate):
            beta = indices[rate_index]
            sources: list[int] = []
            targets: list[int] = []
            for source, alpha in enumerate(indices):
                target = tuple(
                    alpha[coordinate] + beta[coordinate]
                    for coordinate in range(VARIABLES)
                )
                if sum(target) <= maximum_degree:
                    sources.append(source)
                    targets.append(index_map[target])
            output.append(
                (
                    float(rate[rate_index]),
                    np.array(sources, dtype=np.int32),
                    np.array(targets, dtype=np.int32),
                )
            )
        return output

    def multiply_rate(
        value: np.ndarray, maps: list[tuple[float, np.ndarray, np.ndarray]]
    ) -> np.ndarray:
        output = np.zeros_like(value)
        for coefficient, sources, targets in maps:
            output[targets] += coefficient * value[sources]
        return output

    x = [variable(index) for index in range(VARIABLES)]
    one = constant(1.0)
    dependent = add(
        x[0], x[1], x[2], x[3], -x[4], -x[5], constant(-THETA)
    )
    magnitudes = [add(one, x[index] / 4) for index in range(VARIABLES)] + [
        add(one, dependent / 4)
    ]
    observable = constant()
    for word in shuffle_words():
        positives = iter(magnitudes[:4])
        negatives = iter(magnitudes[4:])
        carriers = [
            next(positives) if sign > 0 else -next(negatives)
            for sign in word
        ]
        current = constant(-(1 + THETA / 4))
        suffix = sum(
            (multiply_sparse(value, value) for value in carriers), constant()
        )
        rates: list[np.ndarray] = []
        for carrier in carriers:
            rates.append(add(multiply_sparse(current, current), suffix))
            suffix = add(suffix, -multiply_sparse(carrier, carrier))
            current = add(current, carrier)

        homogeneous = [constant(1.0)] + [
            constant() for _ in range(series_order)
        ]
        for rate in rates:
            maps = rate_maps(rate)
            for order in range(1, series_order + 1):
                homogeneous[order] += multiply_rate(
                    homogeneous[order - 1], maps
                )
        for order, value in enumerate(homogeneous):
            observable += (
                (-1) ** order
                * time_value ** (order + 7)
                / math.factorial(order + 7)
                * value
            )
    return indices, observable


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--max-degree", type=int, default=DEFAULT_DEGREE)
    parser.add_argument("--heat-order", type=int, default=DEFAULT_HEAT_ORDER)
    parser.add_argument("--source-commit")
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if not 0 <= arguments.max_degree <= 8:
        raise ValueError("max-degree must lie between zero and eight")
    if arguments.heat_order < 32:
        raise ValueError("heat-order must be at least 32")
    started = time.perf_counter()

    progress(arguments.progress, started, "constructing digit subset transfers")
    transfers = [r068.signed_digit_transfer(0), r068.signed_digit_transfer(1)]
    cycle = r068.cycle_matrix(transfers).astype(float)
    groups = {bit: digit_edge_groups(bit) for bit in (0, 1)}
    subset_matrices = {
        bit: subset_transfer_matrices(groups[bit]) for bit in (0, 1)
    }
    dominant_root = max(
        root.real
        for root in np.roots(r068.SCALED_QUARTIC)
        if abs(root.imag) < 1.0e-7
    )
    mass, mass_record = reachable_dominant_mass(cycle, dominant_root)

    indices, raw_moments, moment_records = dominant_moments(
        arguments.max_degree,
        cycle,
        dominant_root,
        mass,
        subset_matrices,
        arguments.progress,
        started,
    )
    centered = centered_moments(indices, raw_moments)

    progress(arguments.progress, started, "evaluating complete 35-shuffle heat jet")
    time_value = math.log(2) / 2
    heat_indices, heat_coefficients = heat_taylor_coefficients(
        arguments.max_degree, arguments.heat_order, time_value
    )
    short_indices, short_coefficients = heat_taylor_coefficients(
        arguments.max_degree, arguments.heat_order - 16, time_value
    )
    if heat_indices != indices or short_indices != indices:
        raise AssertionError("moment and heat multiindex orders disagree")
    order_difference = float(
        np.max(np.abs(heat_coefficients - short_coefficients))
    )
    partial_jets = []
    for degree in range(arguments.max_degree + 1):
        value = float(
            sum(
                centered[index, OBSERVABLE_STATE] * heat_coefficients[index]
                for index, alpha in enumerate(indices)
                if sum(alpha) <= degree
            )
        )
        partial_jets.append({"degree": degree, "value": value})

    checks = {
        "subsetZeroMatricesMatchDigitTransfers": all(
            np.max(
                np.abs(
                    (subset_matrices[bit][0] - transfers[bit].astype(float)).data
                )
            )
            < 1.0e-12
            if (subset_matrices[bit][0] - transfers[bit].astype(float)).nnz
            else True
            for bit in (0, 1)
        ),
        "reachableMassMatchesR068B1Interval": (
            -0.02612679363405570
            < mass_record["observable"]
            < -0.02612679362708268
        ),
        "massEigenResidualIsSmall": mass_record["maximumEigenResidual"]
        < 1.0e-9,
        "allMomentLinearResidualsAreSmall": all(
            record["relativeLinearResidual"] < 1.0e-10
            for record in moment_records
        ),
        "heatTaylorOrdersAgree": order_difference < 1.0e-14,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    report = {
        "schemaVersion": "1.0",
        "status": "exploratory-passed",
        "classification": (
            "binary64 convergence and architecture pilot for the dominant "
            "eighth-order 35-shuffle heat projection; no defect, ninth-derivative, "
            "or final sign certificate is claimed"
        ),
        "checks": {key: bool(value) for key, value in checks.items()},
        "parameters": {
            "maximumJetDegree": arguments.max_degree,
            "spatialVariables": VARIABLES,
            "channelsPerState": len(indices),
            "totalMomentCoordinates": len(indices) * r068.DIMENSION,
            "heatTaylorOrder": arguments.heat_order,
            "heatTime": "log(2)/2",
            "thetaLimit": "2/15",
            "shuffleCount": len(shuffle_words()),
        },
        "transfer": {
            "stateDimension": r068.DIMENSION,
            "cycleNonzeros": int(cycle.nnz),
            "subsetCount": 1 << VARIABLES,
            "subsetNonzerosByBit": {
                str(bit): [int(matrix.nnz) for matrix in subset_matrices[bit]]
                for bit in (0, 1)
            },
        },
        "dominantRoot": dominant_root,
        "massProjection": mass_record,
        "momentLift": moment_records,
        "heatJet": {
            "partialByDegree": partial_jets,
            "heatOrderCrossCheckMaximumDifference": order_difference,
            "finalPilotValue": partial_jets[-1]["value"],
        },
        "limitations": [
            "The maximum pilot degree may be below the required degree eight.",
            "The affine-shift defect and its resolvent are not bounded here.",
            "The global ninth derivative of the full heat observable is not bounded here.",
            "No claim is made about all Picard orders or 3D Navier-Stokes regularity.",
        ],
        "provenance": {"sourceCommit": arguments.source_commit},
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
        },
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized)
    progress(
        arguments.progress,
        started,
        "complete",
        degree=arguments.max_degree,
        value=f"{partial_jets[-1]['value']:.12e}",
    )
    sys.stdout.write(serialized)


if __name__ == "__main__":
    main()
