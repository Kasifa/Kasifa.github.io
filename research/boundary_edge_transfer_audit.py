#!/usr/bin/env python3
"""R0.26 edge/one-defect reduction and three-leaf transfer audit.

R0.25 reduced the sharp boundary-family estimate to decay of two normalized
sharp coordinates.  This script identifies a smaller exact recurrence behind
those two coefficients.

The b_N coefficient is generated only by the edge pair P_-, C_+.  The a_N
coefficient contains exactly one leaf off the opposite P_+, C_- edge, so it
is the sum of two first variations of that edge recurrence.  These statements
follow from leaf-count arithmetic and hold for every N.

Adding N -> N+1 appends the unique three-leaf blocks 2 P_+ + C_- and
2 P_- + C_+.  Expanding the Taylor recurrence through three consecutive
one-leaf attachments gives an exact two-dimensional transfer operator plus a
signed remainder.  The numerical part evaluates the reduced recurrence at
two MPFR precisions and audits that split.

The finite calculation does not prove an all-N polarization bound or a
Navier--Stokes regularity theorem.
"""

from __future__ import annotations

import argparse
import itertools
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from typing import Iterable

import gmpy2

import boundary_face_channel_audit as channel
import generated_subspace_sharpness_audit as base


Real = gmpy2.mpfr
RealVector = tuple[Real, Real, Real, Real]
RealFieldByCount = dict[int, RealVector]
GradedRealField = list[RealFieldByCount]

P_PLUS: base.Label = (1, -1, 1)
C_PLUS: base.Label = (1, -1, -1)
P_MINUS: base.Label = (-1, -1, -1)
C_MINUS: base.Label = (-1, -1, 1)

A_BLOCK = (P_PLUS, P_PLUS, C_MINUS)
B_BLOCK = (P_MINUS, P_MINUS, C_PLUS)
R025_CERTIFICATE = Path(
    "research/certificates/r025/boundary-face-channels.json"
)
DEFAULT_PRECISIONS = (160, 224)
ZERO_VECTOR: RealVector = (Real(0), Real(0), Real(0), Real(0))


def progress(enabled: bool, started: float, message: str) -> None:
    if enabled:
        elapsed = time.perf_counter() - started
        print(f"[R0.26 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)


def git_source_state() -> dict[str, object]:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip()
    dirty = bool(
        subprocess.check_output(["git", "status", "--porcelain"], text=True).strip()
    )
    return {"commit": commit, "dirty": dirty}


def atomic_json_write(path: Path, payload: dict[str, object], pretty: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + f".tmp-{os.getpid()}")
    with temporary.open("w", encoding="utf-8") as target:
        json.dump(
            payload,
            target,
            ensure_ascii=False,
            indent=2 if pretty else None,
            sort_keys=True,
        )
        target.write("\n")
        target.flush()
        os.fsync(target.fileno())
    os.replace(temporary, path)


def vector_sum(vectors: Iterable[RealVector]) -> RealVector:
    result = ZERO_VECTOR
    for vector in vectors:
        result = channel.vector_add(result, vector)
    return result


def linear_label(
    first: base.Label,
    first_count: int,
    second: base.Label,
    second_count: int,
) -> base.Label:
    return tuple(
        first_count * first[index] + second_count * second[index]
        for index in range(3)
    )  # type: ignore[return-value]


def edge_label(
    pump: base.Label,
    catalyst: base.Label,
    leaf_count: int,
    catalyst_count: int,
) -> base.Label:
    return linear_label(
        pump,
        leaf_count - catalyst_count,
        catalyst,
        catalyst_count,
    )


def variation_label(
    pump: base.Label,
    catalyst: base.Label,
    defect: base.Label,
    leaf_count: int,
    catalyst_count: int,
) -> base.Label:
    edge_part = edge_label(
        pump,
        catalyst,
        leaf_count - 1,
        catalyst_count,
    )
    return base.label_add(edge_part, defect)


def real_constraint(label: base.Label, coefficient: RealVector) -> Real:
    beta = channel.real_offset(label)
    return (
        Real(base.charge(label)) * coefficient[3]
        + channel.real_dot(beta, coefficient[:3])
    )


def assert_constrained(label: base.Label, coefficient: RealVector) -> None:
    residual = abs(real_constraint(label, coefficient))
    scale = max(Real(1), channel.mode_norm(coefficient))
    tolerance = gmpy2.exp2(-gmpy2.get_context().precision // 2) * scale
    if residual > tolerance:
        raise AssertionError(
            f"constraint residual {residual} exceeds {tolerance} at {label}"
        )


def edge_recurrence(
    pump: base.Label,
    catalyst: base.Label,
    initial: channel.RealField,
    maximum_leaf_count: int,
    show_progress: bool,
    started: float,
    name: str,
) -> GradedRealField:
    """Pure two-generator edge coefficients, indexed by catalyst count."""

    fields: GradedRealField = [
        {} for _ in range(maximum_leaf_count + 1)
    ]
    fields[1] = {0: initial[pump], 1: initial[catalyst]}

    for leaf_count in range(2, maximum_leaf_count + 1):
        output: RealFieldByCount = {}
        scale = -Real(1) / (leaf_count - 1)
        interactions = 0
        for left_leaf_count in range(1, leaf_count):
            right_leaf_count = leaf_count - left_leaf_count
            for left_count, left in fields[left_leaf_count].items():
                left_label = edge_label(
                    pump, catalyst, left_leaf_count, left_count
                )
                for right_count, right in fields[right_leaf_count].items():
                    right_label = edge_label(
                        pump, catalyst, right_leaf_count, right_count
                    )
                    _, value = channel.real_cone_bilinear(
                        left_label, left, right_label, right
                    )
                    count = left_count + right_count
                    output[count] = channel.vector_add(
                        output.get(count, ZERO_VECTOR),
                        channel.vector_scale(scale, value),
                    )
                    interactions += 1
        # A monochromatic Fourier mode has zero self-interaction exactly.
        # Remove both corners explicitly instead of retaining MPFR roundoff.
        output.pop(0, None)
        output.pop(leaf_count, None)
        fields[leaf_count] = {
            count: coefficient
            for count, coefficient in output.items()
            if channel.mode_norm(coefficient) != 0
        }
        if leaf_count % 10 == 0 or leaf_count == maximum_leaf_count:
            progress(
                show_progress,
                started,
                f"{name}: leaves {leaf_count:2d}, states "
                f"{len(fields[leaf_count]):2d}, interactions {interactions:6d}",
            )
    return fields


def first_variation_recurrence(
    pump: base.Label,
    catalyst: base.Label,
    defect: base.Label,
    initial: channel.RealField,
    edge: GradedRealField,
    maximum_leaf_count: int,
    show_progress: bool,
    started: float,
    name: str,
) -> GradedRealField:
    """Coefficients with exactly one defect leaf off a two-generator edge."""

    fields: GradedRealField = [
        {} for _ in range(maximum_leaf_count + 1)
    ]
    fields[1] = {0: initial[defect]}

    for leaf_count in range(2, maximum_leaf_count + 1):
        output: RealFieldByCount = {}
        scale = -Real(1) / (leaf_count - 1)
        interactions = 0
        for edge_leaf_count in range(1, leaf_count):
            variation_leaf_count = leaf_count - edge_leaf_count
            for edge_count, edge_value in edge[edge_leaf_count].items():
                edge_mode = edge_label(
                    pump, catalyst, edge_leaf_count, edge_count
                )
                for variation_count, variation_value in fields[
                    variation_leaf_count
                ].items():
                    variation_mode = variation_label(
                        pump,
                        catalyst,
                        defect,
                        variation_leaf_count,
                        variation_count,
                    )
                    _, edge_variation = channel.real_cone_bilinear(
                        edge_mode,
                        edge_value,
                        variation_mode,
                        variation_value,
                    )
                    _, variation_edge = channel.real_cone_bilinear(
                        variation_mode,
                        variation_value,
                        edge_mode,
                        edge_value,
                    )
                    count = edge_count + variation_count
                    output[count] = channel.vector_add(
                        output.get(count, ZERO_VECTOR),
                        channel.vector_scale(
                            scale,
                            channel.vector_add(
                                edge_variation, variation_edge
                            ),
                        ),
                    )
                    interactions += 2
        fields[leaf_count] = {
            count: coefficient
            for count, coefficient in output.items()
            if channel.mode_norm(coefficient) != 0
        }
        if leaf_count % 10 == 0 or leaf_count == maximum_leaf_count:
            progress(
                show_progress,
                started,
                f"{name}: leaves {leaf_count:2d}, states "
                f"{len(fields[leaf_count]):2d}, interactions {interactions:6d}",
            )
    return fields


def unique_permutations(block: tuple[base.Label, ...]) -> list[tuple[base.Label, ...]]:
    return sorted(set(itertools.permutations(block)))


def attach_one_leaf(
    target_label: base.Label,
    leaf_label: base.Label,
    parent: RealVector,
    target_leaf_count: int,
    initial: channel.RealField,
) -> RealVector:
    """The sum of the two root orientations with one initial leaf."""

    parent_label = tuple(
        target_label[index] - leaf_label[index] for index in range(3)
    )
    _, leaf_parent = channel.real_cone_bilinear(
        leaf_label,
        initial[leaf_label],
        parent_label,  # type: ignore[arg-type]
        parent,
    )
    _, parent_leaf = channel.real_cone_bilinear(
        parent_label,  # type: ignore[arg-type]
        parent,
        leaf_label,
        initial[leaf_label],
    )
    return channel.vector_scale(
        -Real(1) / (target_leaf_count - 1),
        channel.vector_add(leaf_parent, parent_leaf),
    )


def three_leaf_transfer(
    source_label: base.Label,
    source: RealVector,
    source_leaf_count: int,
    block: tuple[base.Label, base.Label, base.Label],
    initial: channel.RealField,
) -> tuple[base.Label, RealVector]:
    """Compose every distinct ordering of a three-leaf one-leaf block."""

    total = ZERO_VECTOR
    final_label: base.Label | None = None
    for path in unique_permutations(block):
        coefficient = source
        label = source_label
        leaf_count = source_leaf_count
        for leaf_label in path:
            label = base.label_add(label, leaf_label)
            leaf_count += 1
            coefficient = attach_one_leaf(
                label,
                leaf_label,
                coefficient,
                leaf_count,
                initial,
            )
        if final_label is None:
            final_label = label
        elif label != final_label:
            raise AssertionError("three-leaf paths have inconsistent endpoints")
        total = channel.vector_add(total, coefficient)
    if final_label is None:
        raise AssertionError("empty three-leaf block")
    return final_label, total


def raw_coordinates(
    label: base.Label,
    coefficient: RealVector,
) -> tuple[Real, Real]:
    sharp, longitudinal = channel.polarization_basis(label)
    sharp_coordinate = channel.real_dot(coefficient[:3], sharp[:3])
    longitudinal_coordinate = coefficient[3] / longitudinal[3]
    return sharp_coordinate, longitudinal_coordinate


def transfer_matrix(
    source_label: base.Label,
    target_label: base.Label,
    source_leaf_count: int,
    block: tuple[base.Label, base.Label, base.Label],
    initial: channel.RealField,
) -> tuple[tuple[Real, Real], tuple[Real, Real]]:
    source_sharp, source_longitudinal = channel.polarization_basis(source_label)
    sharp_target, sharp_output = three_leaf_transfer(
        source_label,
        source_sharp,
        source_leaf_count,
        block,
        initial,
    )
    longitudinal_target, longitudinal_output = three_leaf_transfer(
        source_label,
        source_longitudinal,
        source_leaf_count,
        block,
        initial,
    )
    if sharp_target != target_label or longitudinal_target != target_label:
        raise AssertionError("transfer matrix endpoint mismatch")
    sharp_column = raw_coordinates(target_label, sharp_output)
    longitudinal_column = raw_coordinates(target_label, longitudinal_output)
    return (
        (sharp_column[0], longitudinal_column[0]),
        (sharp_column[1], longitudinal_column[1]),
    )


def endpoint_coefficients(
    parameter: int,
    negative_edge: GradedRealField,
    positive_variation_pump: GradedRealField,
    positive_variation_catalyst: GradedRealField,
) -> tuple[RealVector, RealVector]:
    a_leaf_count = 3 * parameter
    b_leaf_count = 3 * parameter - 1
    a_coefficient = channel.vector_add(
        positive_variation_pump[a_leaf_count][parameter - 1],
        positive_variation_catalyst[a_leaf_count][parameter],
    )
    b_coefficient = negative_edge[b_leaf_count][parameter]
    return a_coefficient, b_coefficient


def ratio_or_none(numerator: Real, denominator: Real) -> float | None:
    if denominator == 0:
        return None
    return float(numerator / denominator)


def matrix_record(
    matrix: tuple[tuple[Real, Real], tuple[Real, Real]]
) -> list[list[float]]:
    return [[float(value) for value in row] for row in matrix]


def endpoint_record(
    parameter: int,
    left: RealVector,
    right: RealVector,
) -> dict[str, object]:
    left_label, right_label, _ = base.sharp_labels(parameter)
    left_sigma, left_lambda, normalized_left = channel.normalized_coordinates(
        left_label, left
    )
    right_sigma, right_lambda, normalized_right = channel.normalized_coordinates(
        right_label, right
    )
    generated = channel.symmetrized(
        left_label, normalized_left, right_label, normalized_right
    )
    sharp_left, _ = channel.polarization_basis(left_label)
    sharp_right, _ = channel.polarization_basis(right_label)
    sharp_benchmark = channel.mode_norm(
        channel.symmetrized(
            left_label, sharp_left, right_label, sharp_right
        )
    )
    generated_gain = channel.mode_norm(generated)
    return {
        "parameter": parameter,
        "left": {
            "sigma": float(left_sigma),
            "lambda": float(left_lambda),
            "NAbsSigma": float(parameter * abs(left_sigma)),
            "modeNorm": float(channel.mode_norm(left)),
            "highPrecisionSigma": channel.decimal_string(left_sigma),
        },
        "right": {
            "sigma": float(right_sigma),
            "lambda": float(right_lambda),
            "NAbsSigma": float(parameter * abs(right_sigma)),
            "modeNorm": float(channel.mode_norm(right)),
            "highPrecisionSigma": channel.decimal_string(right_sigma),
        },
        "generatedGain": float(generated_gain),
        "highPrecisionGeneratedGain": channel.decimal_string(generated_gain),
        "generatedToSharpGainRatio": float(
            generated_gain / sharp_benchmark
        ),
    }


def transfer_record(
    family: str,
    parameter: int,
    source: RealVector,
    target: RealVector,
    initial: channel.RealField,
) -> dict[str, object]:
    index = 0 if family == "a" else 1
    block = A_BLOCK if family == "a" else B_BLOCK
    source_label = base.sharp_labels(parameter)[index]
    target_label = base.sharp_labels(parameter + 1)[index]
    source_leaf_count = base.radius(source_label)
    reached_label, predicted = three_leaf_transfer(
        source_label,
        source,
        source_leaf_count,
        block,
        initial,
    )
    if reached_label != target_label:
        raise AssertionError(f"{family}-family transfer endpoint mismatch")
    remainder = channel.vector_subtract(target, predicted)
    reconstruction_error = channel.mode_norm(
        channel.vector_subtract(
            target, channel.vector_add(predicted, remainder)
        )
    )
    matrix = transfer_matrix(
        source_label,
        target_label,
        source_leaf_count,
        block,
        initial,
    )
    full_sharp, full_longitudinal = raw_coordinates(target_label, target)
    predicted_sharp, predicted_longitudinal = raw_coordinates(
        target_label, predicted
    )
    remainder_sharp, remainder_longitudinal = raw_coordinates(
        target_label, remainder
    )
    predicted_norm = channel.mode_norm(predicted)
    remainder_norm = channel.mode_norm(remainder)
    target_norm = channel.mode_norm(target)
    return {
        "fromParameter": parameter,
        "toParameter": parameter + 1,
        "matrix": matrix_record(matrix),
        "predictedModeNormOverFull": float(predicted_norm / target_norm),
        "remainderModeNormOverFull": float(remainder_norm / target_norm),
        "signedSplitCancellationRatio": float(
            target_norm / (predicted_norm + remainder_norm)
        ),
        "predictedSharpOverFullSharp": ratio_or_none(
            predicted_sharp, full_sharp
        ),
        "remainderSharpOverFullSharp": ratio_or_none(
            remainder_sharp, full_sharp
        ),
        "predictedLongitudinalOverFullLongitudinal": ratio_or_none(
            predicted_longitudinal, full_longitudinal
        ),
        "remainderLongitudinalOverFullLongitudinal": ratio_or_none(
            remainder_longitudinal, full_longitudinal
        ),
        "reconstructionRelativeError": float(
            reconstruction_error / target_norm
        ),
    }


def load_r025_reference() -> dict[str, object]:
    payload = json.loads(R025_CERTIFICATE.read_text())
    return payload["precisionRuns"][-1]["parameters"]


def relative_difference(left: Real | float, right: Real | float) -> float:
    left_real = Real(left)
    right_real = Real(right)
    denominator = max(abs(left_real), abs(right_real), Real(1e-300))
    return float(abs(left_real - right_real) / denominator)


def run_precision(
    precision_bits: int,
    maximum_parameter: int,
    show_progress: bool,
    started: float,
) -> dict[str, object]:
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = precision_bits
    try:
        center, _, _ = base.load_root_center()
        p_value, q_value, x_value = (
            center[name] for name in ("p", "q", "x")
        )
        pump_norm_squared = base.Rational(1) + p_value * p_value / 12
        catalyst_norm_squared = base.Rational(1) + q_value * q_value / 3
        exact_radicand = x_value * pump_norm_squared / (
            4 * catalyst_norm_squared
        )
        radicand = Real(exact_radicand)
        initial = channel.embedded_initial_field(center, exact_radicand)
        maximum_leaf_count = 3 * maximum_parameter
        progress(
            show_progress,
            started,
            f"precision {precision_bits}: building negative edge",
        )
        negative_edge = edge_recurrence(
            P_MINUS,
            C_PLUS,
            initial,
            maximum_leaf_count,
            show_progress,
            started,
            f"{precision_bits}-bit negative edge",
        )
        progress(
            show_progress,
            started,
            f"precision {precision_bits}: building positive edge",
        )
        positive_edge = edge_recurrence(
            P_PLUS,
            C_MINUS,
            initial,
            maximum_leaf_count,
            show_progress,
            started,
            f"{precision_bits}-bit positive edge",
        )
        variation_pump = first_variation_recurrence(
            P_PLUS,
            C_MINUS,
            P_MINUS,
            initial,
            positive_edge,
            maximum_leaf_count,
            show_progress,
            started,
            f"{precision_bits}-bit P- variation",
        )
        variation_catalyst = first_variation_recurrence(
            P_PLUS,
            C_MINUS,
            C_PLUS,
            initial,
            positive_edge,
            maximum_leaf_count,
            show_progress,
            started,
            f"{precision_bits}-bit C+ variation",
        )

        coefficients: dict[int, tuple[RealVector, RealVector]] = {}
        endpoint_records: list[dict[str, object]] = []
        for parameter in range(2, maximum_parameter + 1):
            left, right = endpoint_coefficients(
                parameter,
                negative_edge,
                variation_pump,
                variation_catalyst,
            )
            left_label, right_label, _ = base.sharp_labels(parameter)
            assert_constrained(left_label, left)
            assert_constrained(right_label, right)
            coefficients[parameter] = (left, right)
            endpoint_records.append(
                endpoint_record(parameter, left, right)
            )

        transfer_records = {"a": [], "b": []}
        for parameter in range(2, maximum_parameter):
            left, right = coefficients[parameter]
            next_left, next_right = coefficients[parameter + 1]
            transfer_records["a"].append(
                transfer_record(
                    "a", parameter, left, next_left, initial
                )
            )
            transfer_records["b"].append(
                transfer_record(
                    "b", parameter, right, next_right, initial
                )
            )

        asymptotic_parameter = 1_000_000
        generator = gmpy2.sqrt(radicand)
        asymptotic_matrices: dict[str, object] = {}
        for family, index, block, expected in (
            (
                "a",
                0,
                A_BLOCK,
                ((-24 * generator, Real(0)), (Real(0), -24 * generator)),
            ),
            (
                "b",
                1,
                B_BLOCK,
                ((-24 * generator, Real(0)), (Real(0), 16 * generator)),
            ),
        ):
            source_label = base.sharp_labels(asymptotic_parameter)[index]
            target_label = base.sharp_labels(asymptotic_parameter + 1)[index]
            matrix = transfer_matrix(
                source_label,
                target_label,
                base.radius(source_label),
                block,
                initial,
            )
            maximum_error = max(
                abs(matrix[row][column] - expected[row][column])
                for row in range(2)
                for column in range(2)
            )
            asymptotic_matrices[family] = {
                "probeParameter": asymptotic_parameter,
                "matrix": matrix_record(matrix),
                "claimedLimit": matrix_record(expected),
                "maximumAbsoluteProbeError": float(maximum_error),
            }

        progress(
            show_progress,
            started,
            f"precision {precision_bits}: completed endpoints and transfers",
        )
        return {
            "precisionBits": precision_bits,
            "quadraticGenerator": float(generator),
            "quadraticGeneratorHighPrecision": channel.decimal_string(generator),
            "endpoints": endpoint_records,
            "transfers": transfer_records,
            "asymptoticMatrices": asymptotic_matrices,
        }
    finally:
        context.precision = previous_precision


def endpoint_map(run: dict[str, object]) -> dict[int, dict[str, object]]:
    return {
        record["parameter"]: record
        for record in run["endpoints"]
    }


def validate_payload(
    runs: list[dict[str, object]],
    maximum_parameter: int,
) -> dict[str, object]:
    reference = load_r025_reference()
    high = endpoint_map(runs[-1])
    regression: dict[str, object] = {}
    for parameter in range(2, min(5, maximum_parameter) + 1):
        current = high[parameter]
        old = reference[f"N{parameter}"]["normalizedCoordinates"]
        left_difference = relative_difference(
            current["left"]["sigma"], old["left"]["sigma"]
        )
        right_difference = relative_difference(
            current["right"]["sigma"], old["right"]["sigma"]
        )
        if max(left_difference, right_difference) > 2e-14:
            raise AssertionError(
                f"R0.25 endpoint regression failed at N={parameter}"
            )
        regression[f"N{parameter}"] = {
            "leftSigmaRelativeDifference": left_difference,
            "rightSigmaRelativeDifference": right_difference,
        }

    stability: dict[str, object] = {}
    if len(runs) >= 2:
        context = gmpy2.get_context()
        previous_precision = context.precision
        context.precision = max(run["precisionBits"] for run in runs) + 32
        try:
            low = endpoint_map(runs[-2])
            maximum_difference = 0.0
            for parameter in range(2, maximum_parameter + 1):
                differences: dict[str, float] = {}
                for family in ("left", "right"):
                    difference = relative_difference(
                        low[parameter][family]["highPrecisionSigma"],
                        high[parameter][family]["highPrecisionSigma"],
                    )
                    differences[f"{family}Sigma"] = difference
                    maximum_difference = max(maximum_difference, difference)
                differences["generatedGain"] = relative_difference(
                    low[parameter]["highPrecisionGeneratedGain"],
                    high[parameter]["highPrecisionGeneratedGain"],
                )
                maximum_difference = max(
                    maximum_difference, differences["generatedGain"]
                )
                stability[f"N{parameter}"] = differences
            stability["maximumRelativeDifference"] = maximum_difference
            if maximum_difference > 1e-35:
                raise AssertionError(
                    f"precision stability failed: {maximum_difference}"
                )
        finally:
            context.precision = previous_precision

    all_transfers = [
        record
        for family in ("a", "b")
        for record in runs[-1]["transfers"][family]
    ]
    maximum_reconstruction_error = max(
        record["reconstructionRelativeError"] for record in all_transfers
    )
    if maximum_reconstruction_error > 1e-35:
        raise AssertionError(
            "three-leaf transfer reconstruction lost precision"
        )

    b_lower_left = max(
        abs(record["matrix"][1][0])
        for record in runs[-1]["transfers"]["b"]
    )
    if b_lower_left > 1e-35:
        raise AssertionError(
            f"negative-edge transfer is not triangular: {b_lower_left}"
        )

    asymptotic_probe_error = max(
        record["maximumAbsoluteProbeError"]
        for record in runs[-1]["asymptoticMatrices"].values()
    )
    if asymptotic_probe_error > 1e-3:
        raise AssertionError(
            f"transfer limit probe failed: {asymptotic_probe_error}"
        )

    maximum_n_sigma = 0.0
    maximum_n_sigma_location = ""
    first_above_r025_window = None
    first_above_one = None
    for parameter in range(2, maximum_parameter + 1):
        for family in ("left", "right"):
            value = high[parameter][family]["NAbsSigma"]
            if value > maximum_n_sigma:
                maximum_n_sigma = value
                maximum_n_sigma_location = f"N{parameter}:{family}"
            if value > 0.214 and first_above_r025_window is None:
                first_above_r025_window = f"N{parameter}:{family}"
            if value > 1 and first_above_one is None:
                first_above_one = f"N{parameter}:{family}"

    return {
        "R025Regression": regression,
        "precisionStability": stability,
        "maximumTransferReconstructionRelativeError": (
            maximum_reconstruction_error
        ),
        "negativeEdgeMaximumLowerLeftMatrixEntry": b_lower_left,
        "asymptoticProbeMaximumAbsoluteError": asymptotic_probe_error,
        "finiteWindow": {
            "maximumNAbsSigma": maximum_n_sigma,
            "maximumNAbsSigmaLocation": maximum_n_sigma_location,
            "firstAboveR025ObservedMaximum": first_above_r025_window,
            "firstAboveOne": first_above_one,
            "interpretation": (
                (
                    "the N=2..5 observed maximum 0.214 is exceeded; "
                    if first_above_r025_window is not None
                    else "the N=2..5 observed maximum 0.214 is not exceeded; "
                )
                + "this finite window neither proves nor disproves an "
                "all-N O(1/N) bound"
            ),
        },
    }


def build_payload(
    maximum_parameter: int,
    precisions: tuple[int, ...],
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    runs = [
        run_precision(
            precision,
            maximum_parameter,
            show_progress,
            started,
        )
        for precision in precisions
    ]
    checks = validate_payload(runs, maximum_parameter)
    generator = runs[-1]["quadraticGenerator"]
    return {
        "scope": {
            "result": (
                "exact edge/one-defect reduction and exact three-leaf "
                "transfer-plus-remainder identity"
            ),
            "maximumParameter": maximum_parameter,
            "limitations": [
                "the transfer remainder is evaluated only on a finite parameter window",
                "no all-N sharp-coordinate bound is proved",
                "no Navier-Stokes regularity conclusion is claimed",
            ],
        },
        "leafCountArithmetic": {
            "generators": {
                "PPlus": list(P_PLUS),
                "CPlus": list(C_PLUS),
                "PMinus": list(P_MINUS),
                "CMinus": list(C_MINUS),
            },
            "bN": {
                "label": "(-N+1,-3N+1,-3N+1)",
                "uniqueCounts": {
                    "PMinus": "2N-1",
                    "CPlus": "N",
                    "PPlus": "0",
                    "CMinus": "0",
                },
                "consequence": "b_N is an exact two-generator edge coefficient",
            },
            "aN": {
                "label": "(N,-3N,3N-2)",
                "countSectors": [
                    {
                        "PPlus": "2N",
                        "CMinus": "N-1",
                        "PMinus": "1",
                        "CPlus": "0",
                    },
                    {
                        "PPlus": "2N-1",
                        "CMinus": "N",
                        "PMinus": "0",
                        "CPlus": "1",
                    },
                ],
                "consequence": (
                    "a_N is the sum of two exact first variations of the "
                    "PPlus/CMinus edge"
                ),
            },
            "parameterIncrements": {
                "a": "a_(N+1)-a_N=2PPlus+CMinus",
                "b": "b_(N+1)-b_N=2PMinus+CPlus",
                "catalystParity": "each three-leaf block flips catalyst parity",
            },
        },
        "threeLeafIdentity": {
            "attachment": (
                "A_(m,g)^L(v)=-(B(u_g,v)+B(v,u_g))/(L-1)"
            ),
            "transfer": (
                "T_N is the sum of the three distinct compositions of the "
                "one-leaf attachments for the block 2P+C"
            ),
            "remainder": (
                "U_(N+1)=T_N U_N+R_N; after three substitutions R_N is "
                "exactly the signed sum of terms containing at least one "
                "non-one-leaf root split"
            ),
            "dimension": (
                "the divergence constraint leaves two polarization "
                "coordinates at every charged endpoint"
            ),
        },
        "transferLimits": {
            "generator": generator,
            "aMatrix": "[[-24t,0],[0,-24t]]",
            "bMatrix": "[[-24t,0],[0,16t]]",
            "spectralRadii": {
                "a": 24 * generator,
                "b": 24 * generator,
            },
            "conclusion": (
                "the isolated three-leaf transfer is expansive, not "
                "contractive; any normalized sharp decay must use the "
                "signed bulk remainder and denominator growth"
            ),
        },
        "runs": runs,
        "checks": checks,
        "environment": {
            "python": platform.python_version(),
            "platform": platform.platform(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
        },
        "git": git_source_state(),
        "wallSeconds": time.perf_counter() - started,
    }


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--max-parameter",
        type=int,
        default=20,
        help="largest sharp-family parameter (default: 20)",
    )
    parser.add_argument(
        "--precisions",
        type=int,
        nargs="+",
        default=list(DEFAULT_PRECISIONS),
        help="MPFR precision levels in bits",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument(
        "--check",
        action="store_true",
        help="run assertions (assertions also run before every output)",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if arguments.max_parameter < 5:
        raise SystemExit("--max-parameter must be at least 5")
    if len(arguments.precisions) < 2:
        raise SystemExit("at least two precision levels are required")
    precisions = tuple(sorted(set(arguments.precisions)))
    payload = build_payload(
        arguments.max_parameter,
        precisions,
        arguments.progress,
    )
    if arguments.output is not None:
        atomic_json_write(arguments.output, payload, arguments.pretty)
    else:
        json.dump(
            payload,
            sys.stdout,
            ensure_ascii=False,
            indent=2 if arguments.pretty else None,
            sort_keys=True,
        )
        sys.stdout.write("\n")


if __name__ == "__main__":
    main()
