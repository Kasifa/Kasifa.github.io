#!/usr/bin/env python3
"""R0.25 boundary-face polarization-channel audit.

The R0.24 minimal-face recurrence reaches the R0.22 sharp labels while its
generated operator gain stays of order one at N=2 and N=3.  This audit
isolates the structural quantity that would have to be controlled for all N.

For a charged cone mode, decompose its normalized coefficient into the unit
sharp mode S (zero longitudinal jet) and the unit longitudinal mode L.  On
the sharp label pair a_N,b_N, the four symmetrized channels SS, SL, LS, and
LL have respective sizes O(N^2), O(N), O(N), and O(1).  An elementary bound
then shows that sigma_A,sigma_B=O(N^-1) is sufficient for a uniformly bounded
generated gain.  The only second-order term is the SS coefficient product.

The all-N decay of the generated sharp coordinates is not proved here.  A
two-precision MPFR recurrence extends the numerical probe to N=4 and N=5,
checks N=2 and N=3 against the exact R0.24 certificate, and records the root
split distributions.  These finite computations are evidence, not an
asymptotic theorem or a Navier--Stokes regularity result.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import platform
import sys
import time
from typing import Iterable

import gmpy2

import boundary_face_sharpness_audit as face
import generated_subspace_sharpness_audit as base


Real = gmpy2.mpfr
RealVector = tuple[Real, Real, Real, Real]
RealField = dict[base.Label, RealVector]

DEFAULT_PARAMETERS = (2, 3, 4, 5)
DEFAULT_PRECISIONS = (160, 224)
R024_CERTIFICATE = Path(
    "research/certificates/r024/boundary-face-sharpness.json"
)


def progress(enabled: bool, started: float, message: str) -> None:
    if enabled:
        elapsed = time.perf_counter() - started
        print(f"[R0.25 +{elapsed:8.2f}s] {message}", file=sys.stderr, flush=True)


def real(value: base.Rational | int) -> Real:
    return Real(value)


def vector_add(left: RealVector, right: RealVector) -> RealVector:
    return tuple(left[index] + right[index] for index in range(4))  # type: ignore[return-value]


def vector_scale(value: Real, vector: RealVector) -> RealVector:
    return tuple(value * component for component in vector)  # type: ignore[return-value]


def vector_subtract(left: RealVector, right: RealVector) -> RealVector:
    return tuple(left[index] - right[index] for index in range(4))  # type: ignore[return-value]


def real_dot(left: Iterable[Real], right: Iterable[Real]) -> Real:
    zero = Real(0)
    return sum((a * b for a, b in zip(left, right, strict=True)), start=zero)


def euclidean_norm(vector: Iterable[Real]) -> Real:
    return gmpy2.sqrt(real_dot(vector, vector))


def mode_norm(vector: RealVector) -> Real:
    return euclidean_norm(vector[:3]) + abs(vector[3])


def decimal_string(value: Real) -> str:
    digits = max(20, int(gmpy2.get_context().precision * math.log10(2)) - 5)
    return format(value, f".{digits}g")


def embed_quadratic(value: base.Quadratic, generator: Real) -> Real:
    return real(value[0]) + real(value[1]) * generator


def embedded_initial_field(
    center: dict[str, base.Rational],
    radicand: base.Rational,
) -> RealField:
    generator = gmpy2.sqrt(real(radicand))
    return {
        label: tuple(embed_quadratic(component, generator) for component in coefficient)  # type: ignore[misc]
        for label, coefficient in face.boundary_initial_field(center, radicand).items()
    }


def real_offset(label: base.Label) -> tuple[Real, Real, Real]:
    return tuple(real(component) for component in base.offset(label))  # type: ignore[return-value]


def real_cone_bilinear(
    left_label: base.Label,
    left: RealVector,
    right_label: base.Label,
    right: RealVector,
) -> tuple[base.Label, RealVector]:
    output_label = base.label_add(left_label, right_label)
    right_offset = real_offset(right_label)
    output_offset = real_offset(output_label)
    right_charge = real(base.charge(right_label))
    output_charge = real(base.charge(output_label))
    scalar = real_dot(right_offset, left[:3]) + right_charge * left[3]
    zero = Real(0)

    if output_charge != 0:
        transverse = tuple(scalar * component for component in right[:3])
        longitudinal = -real_dot(output_offset, transverse) / output_charge
        return output_label, transverse + (longitudinal,)  # type: ignore[return-value]

    offset_squared = real_dot(output_offset, output_offset)
    if offset_squared == 0:
        return output_label, (zero, zero, zero, zero)
    offset_component = real_dot(output_offset, right[:3])
    projected = tuple(
        right[index]
        - output_offset[index] * offset_component / offset_squared
        for index in range(3)
    )
    transverse = tuple(scalar * component for component in projected)
    return output_label, transverse + (scalar * right[3],)  # type: ignore[return-value]


def monochromatic_corner(label: base.Label, leaf_count: int) -> bool:
    """The four corners require identical leaves, whose self-interaction is zero."""

    return (
        label[1] == -leaf_count
        and abs(label[0]) == leaf_count
        and abs(label[2]) == leaf_count
    )


def real_boundary_taylor(
    center: dict[str, base.Rational],
    radicand: base.Rational,
    maximum_order: int,
    precision_bits: int,
    show_progress: bool,
    started: float,
) -> tuple[list[RealField], list[dict[str, object]]]:
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = precision_bits
    try:
        coefficients = [embedded_initial_field(center, radicand)]
        summaries: list[dict[str, object]] = [
            {
                "timeOrder": 0,
                "leafCount": 1,
                "supportSize": 4,
                "orderedInteractions": 0,
                "stageSeconds": 0.0,
            }
        ]
        for next_order in range(1, maximum_order + 1):
            stage_started = time.perf_counter()
            output: RealField = {}
            interaction_count = 0
            scale = -Real(1) / next_order
            for left_order in range(next_order):
                right_order = next_order - 1 - left_order
                for left_label, left in coefficients[left_order].items():
                    for right_label, right in coefficients[right_order].items():
                        interaction_count += 1
                        output_label, value = real_cone_bilinear(
                            left_label, left, right_label, right
                        )
                        updated = vector_add(
                            output.get(
                                output_label,
                                (Real(0), Real(0), Real(0), Real(0)),
                            ),
                            vector_scale(scale, value),
                        )
                        output[output_label] = updated

            leaf_count = next_order + 1
            for label in tuple(output):
                if monochromatic_corner(label, leaf_count):
                    output.pop(label)
            stage_seconds = time.perf_counter() - stage_started
            coefficients.append(output)
            summaries.append(
                {
                    "timeOrder": next_order,
                    "leafCount": leaf_count,
                    "supportSize": len(output),
                    "orderedInteractions": interaction_count,
                    "stageSeconds": stage_seconds,
                }
            )
            progress(
                show_progress,
                started,
                f"precision {precision_bits:3d}, order {next_order:2d}: "
                f"support {len(output):3d}, interactions {interaction_count:7d}, "
                f"stage {stage_seconds:.2f}s",
            )
        return coefficients, summaries
    finally:
        context.precision = previous_precision


def polarization_basis(label: base.Label) -> tuple[RealVector, RealVector]:
    beta = real_offset(label)
    charge = real(base.charge(label))
    if charge == 0:
        raise ValueError(f"the polarization basis requires nonzero charge: {label}")
    beta_norm = euclidean_norm(beta)
    direction_cross_beta = (
        beta[2] - beta[1],
        beta[0] - beta[2],
        beta[1] - beta[0],
    )
    sharp_norm = euclidean_norm(direction_cross_beta)
    sharp: RealVector = tuple(
        component / sharp_norm for component in direction_cross_beta
    ) + (Real(0),)  # type: ignore[assignment]

    denominator = Real(1) + beta_norm / abs(charge)
    longitudinal: RealVector = tuple(
        component / (beta_norm * denominator) for component in beta
    ) + (-beta_norm / (charge * denominator),)  # type: ignore[assignment]
    return sharp, longitudinal


def normalized_coordinates(
    label: base.Label,
    coefficient: RealVector,
) -> tuple[Real, Real, RealVector]:
    coefficient_norm = mode_norm(coefficient)
    normalized = vector_scale(Real(1) / coefficient_norm, coefficient)
    sharp, longitudinal = polarization_basis(label)
    sigma = real_dot(normalized[:3], sharp[:3])
    lam = normalized[3] / longitudinal[3]
    reconstruction = vector_add(
        vector_scale(sigma, sharp), vector_scale(lam, longitudinal)
    )
    reconstruction_error = mode_norm(vector_subtract(normalized, reconstruction))
    if reconstruction_error > gmpy2.exp2(-gmpy2.get_context().precision // 2):
        raise AssertionError(
            f"polarization reconstruction failed at {label}: {reconstruction_error}"
        )
    return sigma, lam, normalized


def symmetrized(
    left_label: base.Label,
    left: RealVector,
    right_label: base.Label,
    right: RealVector,
) -> RealVector:
    _, left_right = real_cone_bilinear(
        left_label, left, right_label, right
    )
    _, right_left = real_cone_bilinear(
        right_label, right, left_label, left
    )
    return vector_add(left_right, right_left)


def root_split_record(
    target: base.Label,
    order: int,
    coefficients: list[RealField],
) -> dict[str, object]:
    full = coefficients[order][target]
    full_norm = mode_norm(full)
    records = []
    for left_order in range(order):
        right_order = order - 1 - left_order
        contribution: RealVector = (Real(0), Real(0), Real(0), Real(0))
        for left_label, left in coefficients[left_order].items():
            right_label = tuple(
                target[index] - left_label[index] for index in range(3)
            )
            right = coefficients[right_order].get(right_label)  # type: ignore[arg-type]
            if right is None:
                continue
            _, value = real_cone_bilinear(
                left_label, left, right_label, right  # type: ignore[arg-type]
            )
            contribution = vector_add(
                contribution, vector_scale(-Real(1) / order, value)
            )
        records.append(
            {
                "leftLeafCount": left_order + 1,
                "rightLeafCount": right_order + 1,
                "modeNormOverFull": float(mode_norm(contribution) / full_norm),
            }
        )
    triangle_ratio = sum(record["modeNormOverFull"] for record in records)
    dominant = max(records, key=lambda record: record["modeNormOverFull"])
    return {
        "triangleSumOverFull": triangle_ratio,
        "cancellationRatio": 1.0 / triangle_ratio,
        "dominantSplit": dominant,
        "splits": records,
    }


def parameter_record(
    parameter: int,
    coefficients: list[RealField],
) -> dict[str, object]:
    left_label, right_label, output_label = base.sharp_labels(parameter)
    left_order = base.radius(left_label) - 1
    right_order = base.radius(right_label) - 1
    output_order = base.radius(output_label) - 1
    left = coefficients[left_order][left_label]
    right = coefficients[right_order][right_label]
    full_output = coefficients[output_order][output_label]
    sigma_left, lambda_left, normalized_left = normalized_coordinates(
        left_label, left
    )
    sigma_right, lambda_right, normalized_right = normalized_coordinates(
        right_label, right
    )
    sharp_left, longitudinal_left = polarization_basis(left_label)
    sharp_right, longitudinal_right = polarization_basis(right_label)

    channel_specifications = (
        ("sharpSharp", sigma_left * sigma_right, sharp_left, sharp_right),
        ("sharpLongitudinal", sigma_left * lambda_right, sharp_left, longitudinal_right),
        ("longitudinalSharp", lambda_left * sigma_right, longitudinal_left, sharp_right),
        (
            "longitudinalLongitudinal",
            lambda_left * lambda_right,
            longitudinal_left,
            longitudinal_right,
        ),
    )
    channel_records: dict[str, object] = {}
    channel_sum: RealVector = (Real(0), Real(0), Real(0), Real(0))
    channel_triangle = Real(0)
    for name, coordinate_product, left_basis, right_basis in channel_specifications:
        raw_output = symmetrized(
            left_label, left_basis, right_label, right_basis
        )
        contribution = vector_scale(coordinate_product, raw_output)
        contribution_norm = mode_norm(contribution)
        channel_sum = vector_add(channel_sum, contribution)
        channel_triangle += contribution_norm
        channel_records[name] = {
            "coordinateProduct": float(coordinate_product),
            "rawOperatorGain": float(mode_norm(raw_output)),
            "contributionModeNorm": float(contribution_norm),
        }

    generated = symmetrized(
        left_label, normalized_left, right_label, normalized_right
    )
    generated_gain = mode_norm(generated)
    identity_error = mode_norm(vector_subtract(generated, channel_sum))
    actual_root_operator = symmetrized(left_label, left, right_label, right)
    root_contribution = vector_scale(
        -Real(1) / output_order, actual_root_operator
    )
    root_share = mode_norm(root_contribution) / mode_norm(full_output)
    sharp_gain = mode_norm(
        symmetrized(left_label, sharp_left, right_label, sharp_right)
    )

    return {
        "parameter": parameter,
        "labels": {
            "left": list(left_label),
            "right": list(right_label),
            "output": list(output_label),
        },
        "orders": {
            "left": left_order,
            "right": right_order,
            "output": output_order,
        },
        "normalizedCoordinates": {
            "left": {
                "sigma": float(sigma_left),
                "lambda": float(lambda_left),
                "NAbsSigma": float(parameter * abs(sigma_left)),
            },
            "right": {
                "sigma": float(sigma_right),
                "lambda": float(lambda_right),
                "NAbsSigma": float(parameter * abs(sigma_right)),
            },
            "N2AbsSigmaProduct": float(
                parameter * parameter * abs(sigma_left * sigma_right)
            ),
        },
        "channels": channel_records,
        "channelReconstructionError": float(identity_error),
        "channelTriangleModeNorm": float(channel_triangle),
        "generatedSymmetrizedOperatorGain": float(generated_gain),
        "generatedToSharpGainRatio": float(generated_gain / sharp_gain),
        "generatedGainOverRadiusProduct": float(
            generated_gain
            / (base.radius(left_label) * base.radius(right_label))
        ),
        "channelCancellationRatio": float(generated_gain / channel_triangle),
        "rootContributionToFullOutputModeNorm": float(root_share),
        "highPrecisionQuantities": {
            "generatedGain": decimal_string(generated_gain),
            "leftSigma": decimal_string(sigma_left),
            "rightSigma": decimal_string(sigma_right),
            "rootShare": decimal_string(root_share),
        },
        "rootSplits": {
            "left": root_split_record(left_label, left_order, coefficients),
            "right": root_split_record(right_label, right_order, coefficients),
        },
    }


def exact_geometry_checks(parameters: Iterable[int]) -> list[dict[str, object]]:
    records = []
    direction = (base.Rational(1),) * 3
    for parameter in parameters:
        left, right, output = base.sharp_labels(parameter)
        beta_left = base.offset(left)
        beta_right = base.offset(right)
        beta_output = base.offset(output)
        determinant = base.rational_dot(
            beta_right, base.rational_cross(direction, beta_left)
        )
        left_squared = base.rational_dot(beta_left, beta_left)
        right_squared = base.rational_dot(beta_right, beta_right)
        mixed_dot = base.rational_dot(beta_left, beta_right)
        records.append(
            {
                "parameter": parameter,
                "chargesCorrect": (
                    base.charge(left) == base.Rational(1, 6)
                    and base.charge(right) == base.Rational(1, 6)
                    and base.charge(output) == base.Rational(1, 3)
                ),
                "offsetAddition": tuple(
                    beta_left[index] + beta_right[index] for index in range(3)
                )
                == beta_output,
                "leftSquaredNormIdentity": left_squared
                == 6 * parameter * parameter
                - 2 * parameter
                + base.Rational(2, 3),
                "rightSquaredNormIdentity": right_squared
                == 6 * parameter * parameter
                - 4 * parameter
                + base.Rational(2, 3),
                "mixedDotIdentity": mixed_dot
                == 3 * parameter * parameter - base.Rational(1, 3),
                "determinantIdentity": determinant
                == -(3 * parameter - 1) ** 2,
            }
        )
    return records


def channel_geometry_record(parameter: int) -> dict[str, float]:
    left, right, _ = base.sharp_labels(parameter)
    sharp_left, longitudinal_left = polarization_basis(left)
    sharp_right, longitudinal_right = polarization_basis(right)
    return {
        "parameter": parameter,
        "sharpSharp": float(
            mode_norm(symmetrized(left, sharp_left, right, sharp_right))
        ),
        "sharpLongitudinal": float(
            mode_norm(symmetrized(left, sharp_left, right, longitudinal_right))
        ),
        "longitudinalSharp": float(
            mode_norm(symmetrized(left, longitudinal_left, right, sharp_right))
        ),
        "longitudinalLongitudinal": float(
            mode_norm(
                symmetrized(left, longitudinal_left, right, longitudinal_right)
            )
        ),
    }


def precision_run(
    parameters: tuple[int, ...],
    precision_bits: int,
    center: dict[str, base.Rational],
    radicand: base.Rational,
    show_progress: bool,
    started: float,
) -> dict[str, object]:
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = precision_bits
    try:
        maximum_order = max(
            base.radius(base.sharp_labels(n)[2]) - 1 for n in parameters
        )
        coefficients, support = real_boundary_taylor(
            center,
            radicand,
            maximum_order,
            precision_bits,
            show_progress,
            started,
        )
        records = {
            f"N{parameter}": parameter_record(parameter, coefficients)
            for parameter in parameters
        }
        progress(
            show_progress,
            started,
            f"precision {precision_bits}: completed N={parameters[0]}..{parameters[-1]}",
        )
        return {
            "precisionBits": precision_bits,
            "maximumTimeOrder": maximum_order,
            "support": support,
            "parameters": records,
        }
    finally:
        context.precision = previous_precision


def relative_difference(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), sys.float_info.min)


def audit(
    parameters: tuple[int, ...],
    precisions: tuple[int, ...],
    show_progress: bool,
) -> dict[str, object]:
    started = time.perf_counter()
    if len(precisions) != 2 or precisions[0] >= precisions[1]:
        raise ValueError("provide exactly two increasing MPFR precisions")
    center, root_radius, root_hash = base.load_root_center()
    pump_norm_squared = base.Rational(1) + center["p"] * center["p"] / 12
    catalyst_norm_squared = base.Rational(1) + center["q"] * center["q"] / 3
    radicand = center["x"] * pump_norm_squared / (4 * catalyst_norm_squared)

    runs = [
        precision_run(
            parameters,
            precision,
            center,
            radicand,
            show_progress,
            started,
        )
        for precision in precisions
    ]
    low, high = runs
    stability = {}
    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = precisions[-1]
    try:
        for parameter in parameters:
            key = f"N{parameter}"
            low_record = low["parameters"][key]
            high_record = high["parameters"][key]
            low_quantities = low_record["highPrecisionQuantities"]
            high_quantities = high_record["highPrecisionQuantities"]
            stability[key] = {}
            for name in low_quantities:
                left_value = Real(low_quantities[name])
                right_value = Real(high_quantities[name])
                denominator = max(
                    abs(left_value), abs(right_value), gmpy2.exp2(-1000)
                )
                stability[key][name] = float(
                    abs(left_value - right_value) / denominator
                )
    finally:
        context.precision = previous_precision

    certificate = json.loads(R024_CERTIFICATE.read_text())
    exact_comparison = {}
    for parameter in (2, 3):
        key = f"N{parameter}"
        exact_gain = certificate["parameterAudits"][key]["comparison"][
            "generatedSymmetrizedOperatorGain"
        ]
        exact_root_share = certificate["parameterAudits"][key]["comparison"][
            "rootContributionToFullOutputModeNorm"
        ]
        computed_gain = high["parameters"][key][
            "generatedSymmetrizedOperatorGain"
        ]
        computed_root_share = high["parameters"][key][
            "rootContributionToFullOutputModeNorm"
        ]
        exact_comparison[key] = {
            "R024ExactGain": exact_gain,
            "MPFRGain": computed_gain,
            "gainRelativeDifference": relative_difference(
                exact_gain, computed_gain
            ),
            "R024ExactRootShare": exact_root_share,
            "MPFRRootShare": computed_root_share,
            "rootShareRelativeDifference": relative_difference(
                exact_root_share, computed_root_share
            ),
        }

    context = gmpy2.get_context()
    previous_precision = context.precision
    context.precision = precisions[-1]
    try:
        channel_samples = [
            channel_geometry_record(parameter)
            for parameter in (*parameters, 1000, 10000)
        ]
    finally:
        context.precision = previous_precision

    return {
        "scope": {
            "result": "polarization-channel reduction of the minimal boundary face",
            "proved": [
                "every charged boundary coefficient has a unique normalized sharp-longitudinal decomposition",
                "the SS, SL, LS, and LL channels scale as N^2, N, N, and 1 on the R0.22 label family",
                "O(N^-1) bounds for both generated sharp coordinates are sufficient for a bounded generated gain",
            ],
            "notProved": [
                "the generated sharp coordinates are O(N^-1) for all N",
                "an all-N generated-gain bound",
                "one-radius analytic closure",
                "a Navier--Stokes regularity or singularity result",
            ],
        },
        "decomposition": {
            "modeNorm": "M(w,ell)=|w|+|ell|",
            "sharpBasis": "S_m=((d cross beta_m)/(sqrt(3)|beta_m|),0)",
            "longitudinalBasis": (
                "L_m=(beta_m/(|beta_m|(1+6|beta_m|)),"
                "-6|beta_m|/(1+6|beta_m|))"
            ),
            "normalizedCoefficient": "U_m/M(U_m)=sigma_m S_m+lambda_m L_m",
            "lambdaBound": "|lambda_m| <= 1+1/(12N) <= 25/24 for the sharp inputs, N>=2",
        },
        "catalystParity": {
            "faceGenerators": {
                "pump": ["(1,-1,1)", "(-1,-1,-1)"],
                "catalyst": ["(1,-1,-1)", "(-1,-1,1)"],
            },
            "identity": (
                "the catalyst leaf count C satisfies "
                "C congruent to (m_1-m_3)/2 modulo 2"
            ),
            "fieldLine": (
                "U_L(m) lies in Q when (m_1-m_3)/2 is even and in tQ "
                "when it is odd, because t^2 is rational"
            ),
            "sharpFamilyParities": {
                "aN": "N-1 modulo 2",
                "bN": "N modulo 2",
                "output": "1 modulo 2",
            },
        },
        "exactSharpPairGeometry": {
            "betaA": "(N-2/3,-2N+1/3,N+1/3)",
            "betaB": "(-N+1/3,-N+1/3,2N-2/3)",
            "betaASquared": "6N^2-2N+2/3",
            "betaBSquared": "6N^2-4N+2/3",
            "betaADotBetaB": "3N^2-1/3",
            "mixedDeterminant": "beta_B dot (d cross beta_A)=-(3N-1)^2",
            "checks": exact_geometry_checks((*parameters, 8, 13, 21)),
        },
        "channelHierarchy": {
            "asymptoticLimits": {
                "sharpSharpOverN2": 27.0,
                "sharpLongitudinalOverN": 3.0 / (2.0 * math.sqrt(2.0)),
                "longitudinalSharpOverN": 3.0 / (2.0 * math.sqrt(2.0)),
                "longitudinalLongitudinal": 0.125,
            },
            "elementaryBoundsForNAtLeast2": {
                "sharpSharp": "<=44 N^2",
                "sharpLongitudinal": "<=7 N",
                "longitudinalSharp": "<=7 N",
                "longitudinalLongitudinal": "<=1",
            },
            "conditionalGainBound": (
                "G_N <= 44N^2|sigma_A sigma_B|"
                "+7N(|sigma_A lambda_B|+|lambda_A sigma_B|)"
                "+|lambda_A lambda_B|"
            ),
            "samples": channel_samples,
        },
        "precisionRuns": runs,
        "precisionStability": stability,
        "R024ExactRegression": exact_comparison,
        "root": {
            "center": {key: str(value) for key, value in center.items()},
            "boxRadius": str(root_radius),
            "certificateSha256": root_hash,
        },
        "quadraticFieldRadicand": str(radicand),
        "environment": {
            "python": platform.python_version(),
            "gmpy2": gmpy2.version(),
            "mpfr": gmpy2.mpfr_version(),
            "platform": platform.platform(),
        },
        "git": base.git_source_state(),
        "wallSeconds": time.perf_counter() - started,
    }


def validate(result: dict[str, object]) -> None:
    for record in result["exactSharpPairGeometry"]["checks"]:
        assert all(value is True for key, value in record.items() if key != "parameter")

    high = result["precisionRuns"][-1]["parameters"]
    expected_ranges = {
        "N2": (0.3045, 0.3047),
        "N3": (0.3614, 0.3617),
        "N4": (0.4214, 0.4219),
        "N5": (0.2355, 0.2361),
    }
    for key, (lower, upper) in expected_ranges.items():
        gain = high[key]["generatedSymmetrizedOperatorGain"]
        assert lower < gain < upper
        coordinates = high[key]["normalizedCoordinates"]
        assert coordinates["left"]["NAbsSigma"] < 0.25
        assert coordinates["right"]["NAbsSigma"] < 0.25
        assert coordinates["N2AbsSigmaProduct"] < 0.025
        assert high[key]["channelReconstructionError"] < 1.0e-30

    for record in result["R024ExactRegression"].values():
        assert record["gainRelativeDifference"] < 2.0e-15
        assert record["rootShareRelativeDifference"] < 2.0e-14
    for record in result["precisionStability"].values():
        assert max(record.values()) < 1.0e-38

    samples = result["channelHierarchy"]["samples"]
    for sample in samples:
        parameter = sample["parameter"]
        assert sample["sharpSharp"] <= 44 * parameter * parameter
        assert sample["sharpLongitudinal"] <= 7 * parameter
        assert sample["longitudinalSharp"] <= 7 * parameter
        assert sample["longitudinalLongitudinal"] <= 1
    last = samples[-1]
    limits = result["channelHierarchy"]["asymptoticLimits"]
    assert abs(last["sharpSharp"] / 10000**2 - limits["sharpSharpOverN2"]) < 0.01
    assert (
        abs(
            last["sharpLongitudinal"] / 10000
            - limits["sharpLongitudinalOverN"]
        )
        < 0.001
    )
    assert abs(last["longitudinalLongitudinal"] - 0.125) < 0.0001


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--parameters", nargs="+", type=int, default=list(DEFAULT_PARAMETERS)
    )
    parser.add_argument(
        "--precisions", nargs="+", type=int, default=list(DEFAULT_PRECISIONS)
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--pretty", action="store_true")
    parser.add_argument("--progress", action="store_true")
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()
    parameters = tuple(arguments.parameters)
    precisions = tuple(arguments.precisions)
    if parameters != DEFAULT_PARAMETERS:
        parser.error("the certified audit currently requires parameters 2 3 4 5")
    if min(precisions) < 96:
        parser.error("each MPFR precision must be at least 96 bits")
    result = audit(parameters, precisions, arguments.progress)
    if arguments.check:
        validate(result)
    serialized = json.dumps(
        result,
        ensure_ascii=False,
        indent=2 if arguments.pretty else None,
        sort_keys=True,
    )
    if arguments.output:
        arguments.output.parent.mkdir(parents=True, exist_ok=True)
        arguments.output.write_text(serialized + "\n")
    print(serialized)


if __name__ == "__main__":
    main()
