#!/usr/bin/env python3
"""Rejected binary64 precision baseline for the R0.68B-2f moment lift.

The exact dominant-root and mass intervals from R0.68B-2e are used as the
degree-zero input.  Higher raw moments are represented by a binary64 centre
and a nonnegative binary64 radius.  Every sparse product has integer or
dyadic coefficients that are exactly representable in binary64.  Standard
dot-product gamma bounds, enlarged by an explicit arithmetic guard, propagate
the radii through the four digit steps.

For degree one, residuals are converted to solution errors with

    ||(16 nu I-C)^(-1)||_2
        <= 1 / (16 nu_- - sqrt(||C^T C||_infinity)).

For degrees two through ten, the stronger scalar factor gives strict
infinity-norm diagonal dominance:

    ||(16^d nu I-C)^(-1)||_infinity
        <= 1 / (16^d nu_- - ||C||_infinity).

This implementation is retained as a reproducible negative control: its
componentwise radii become too wide after the four signed-digit transports.
The formal route therefore uses the separate guarded binary128 engine.  This
file is not a successful certificate and is not a Navier--Stokes regularity
result.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path

import numpy as np
import scipy
from scipy.sparse import csr_matrix

import eighth_order_cycle_audit as cycle_audit
import eighth_order_dominant_mass_exact_audit as mass_audit
import eighth_order_heat_jet_pilot as pilot


MAXIMUM_DEGREE = 10
DEFAULT_BASELINE_DEGREE = 4
ROOT_BISECTIONS = 192
UNIT_ROUNDOFF = 2.0**-53
ARITHMETIC_GUARD = 1.0 + 2.0**-48
NORM_GUARD = 1.0 + 2.0**-40
EXPECTED_CYCLE_INFINITY_NORM = 123_028
EXPECTED_CYCLE_ONE_NORM = 212_804
EXPECTED_NORMAL_INFINITY_NORM = 2_024_341_504


def progress(enabled: bool, started: float, stage: str, **details: object) -> None:
    if not enabled:
        return
    fields = " ".join(f"{key}={value}" for key, value in details.items())
    print(
        f"[R0.68B-2f moment interval +{time.perf_counter() - started:8.2f}s] "
        f"{stage}{(' ' + fields) if fields else ''}",
        file=sys.stderr,
        flush=True,
    )


def fraction_down(value: Fraction) -> float:
    """Largest convenient binary64 value known not to exceed a rational."""
    output = float(value)
    if Fraction.from_float(output) > value:
        output = math.nextafter(output, -math.inf)
    return output


def fraction_up(value: Fraction) -> float:
    """Smallest convenient binary64 value known not to lie below a rational."""
    output = float(value)
    if Fraction.from_float(output) < value:
        output = math.nextafter(output, math.inf)
    return output


def guarded_up(values: np.ndarray | float) -> np.ndarray | float:
    """Inflate positive binary64 bounds beyond the local arithmetic roundoff."""
    array = np.asarray(values, dtype=float)
    guarded = array * ARITHMETIC_GUARD
    guarded = np.where(
        guarded > 0,
        np.nextafter(guarded, math.inf),
        guarded,
    )
    if np.isscalar(values):
        return float(guarded)
    return guarded


def gamma_bound(dot_terms: int) -> float:
    """Upward binary64 bound for a dot product with at most dot_terms entries.

    Two elementary roundings per entry are allowed.  This is deliberately
    wider than the usual gamma_n dot-product estimate.
    """
    if dot_terms <= 0:
        return 0.0
    operations = 2 * dot_terms
    numerator = operations * UNIT_ROUNDOFF
    if numerator >= 1:
        raise OverflowError("dot-product gamma bound is not finite")
    return math.nextafter(numerator / (1 - numerator), math.inf)


def absolute_matrix(matrix: csr_matrix) -> csr_matrix:
    output = matrix.copy().astype(float)
    output.data = np.abs(output.data)
    return output


def assert_exact_binary_coefficients(matrix: csr_matrix, label: str) -> None:
    if not np.all(np.isfinite(matrix.data)):
        raise AssertionError(f"{label} has non-finite coefficients")
    if not np.all(matrix.data == np.rint(matrix.data)):
        raise AssertionError(f"{label} has noninteger coefficients")
    if matrix.data.size and float(np.max(np.abs(matrix.data))) >= 2.0**53:
        raise AssertionError(f"{label} has coefficients beyond exact binary64 integers")


def sparse_product_enclosure(
    matrix: csr_matrix,
    absolute: csr_matrix,
    centre: np.ndarray,
    radius: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Enclose matrix times a rectangular interval array.

    centre and radius have shape (matrix.shape[1], right_hand_sides).
    """
    if centre.shape != radius.shape or centre.shape[0] != matrix.shape[1]:
        raise ValueError("sparse enclosure shape mismatch")
    maximum_terms = int(np.max(np.diff(matrix.indptr), initial=0))
    gamma = gamma_bound(maximum_terms)
    output_centre = matrix @ centre
    absolute_centre_sum = absolute @ np.abs(centre)
    radius_sum = absolute @ radius
    output_radius = guarded_up(
        (radius_sum + gamma * absolute_centre_sum) / (1 - gamma)
    )
    if np.any(output_radius < 0) or not np.all(np.isfinite(output_radius)):
        raise AssertionError("invalid sparse-product radius")
    return output_centre, output_radius


def channel_addition_enclosure(
    centres: list[np.ndarray],
    radii: list[np.ndarray],
) -> tuple[np.ndarray, np.ndarray]:
    if not centres:
        raise ValueError("at least one channel contribution is required")
    output = np.zeros_like(centres[0])
    absolute_sum = np.zeros_like(centres[0])
    radius_sum = np.zeros_like(centres[0])
    for centre, radius in zip(centres, radii, strict=True):
        output += centre
        absolute_sum += np.abs(centre)
        radius_sum += radius
    gamma = gamma_bound(len(centres))
    output_radius = guarded_up(
        (radius_sum + gamma * absolute_sum) / (1 - gamma)
    )
    return output, output_radius


def enclosed_digit_step(
    centres: np.ndarray,
    radii: np.ndarray,
    subset_matrices: list[csr_matrix],
    subset_absolute: list[csr_matrix],
    operators: list[tuple[np.ndarray, csr_matrix] | None],
) -> tuple[np.ndarray, np.ndarray]:
    term_centres: list[np.ndarray] = []
    term_radii: list[np.ndarray] = []
    for mask, record in enumerate(operators):
        if record is None:
            continue
        sources, channel = record
        assert_exact_binary_coefficients(channel, f"channel operator mask {mask}")
        channel_absolute = absolute_matrix(channel)
        transported_centre, transported_radius = sparse_product_enclosure(
            subset_matrices[mask],
            subset_absolute[mask],
            centres[sources].T,
            radii[sources].T,
        )
        term_centre, term_radius = sparse_product_enclosure(
            channel,
            channel_absolute,
            transported_centre.T,
            transported_radius.T,
        )
        term_centres.append(term_centre)
        term_radii.append(term_radius)
    return channel_addition_enclosure(term_centres, term_radii)


def enclosed_raw_cycle(
    centres: np.ndarray,
    radii: np.ndarray,
    indices: list[tuple[int, ...]],
    subset_matrices: dict[int, list[csr_matrix]],
    subset_absolute: dict[int, list[csr_matrix]],
    report_progress: bool,
    started: float,
) -> tuple[np.ndarray, np.ndarray]:
    output_centre = centres
    output_radius = radii
    for digit_index, (length, bit) in enumerate(
        zip((1, 2, 4, 8), cycle_audit.WORD, strict=True),
        1,
    ):
        operators = pilot.channel_translation_operators(indices, length)
        output_centre, output_radius = enclosed_digit_step(
            output_centre,
            output_radius,
            subset_matrices[bit],
            subset_absolute[bit],
            operators,
        )
        progress(
            report_progress,
            started,
            "enclosed digit step",
            digit=f"{digit_index}/4",
            length=length,
            bit=bit,
            maximum_radius=f"{float(np.max(output_radius)):.3e}",
        )
    return output_centre, output_radius


def cycle_norms(cycle: csr_matrix) -> dict[str, int | float]:
    integer_cycle = cycle.astype(np.int64)
    row_sum = np.asarray(abs(integer_cycle).sum(axis=1)).ravel()
    column_sum = np.asarray(abs(integer_cycle).sum(axis=0)).ravel()
    normal = integer_cycle.T @ integer_cycle
    normal_row_sum = np.asarray(abs(normal).sum(axis=1)).ravel()
    infinity_norm = int(row_sum.max())
    one_norm = int(column_sum.max())
    normal_infinity_norm = int(normal_row_sum.max())
    if (
        infinity_norm != EXPECTED_CYCLE_INFINITY_NORM
        or one_norm != EXPECTED_CYCLE_ONE_NORM
        or normal_infinity_norm != EXPECTED_NORMAL_INFINITY_NORM
    ):
        raise AssertionError(
            {
                "infinity": infinity_norm,
                "one": one_norm,
                "normalInfinity": normal_infinity_norm,
            }
        )
    two_norm_upper = math.nextafter(
        math.sqrt(normal_infinity_norm),
        math.inf,
    )
    return {
        "infinityNorm": infinity_norm,
        "oneNorm": one_norm,
        "normalInfinityNorm": normal_infinity_norm,
        "twoNormUpper": two_norm_upper,
    }


def exact_initial_intervals(
    report_progress: bool,
    started: float,
) -> tuple[
    tuple[Fraction, Fraction],
    np.ndarray,
    np.ndarray,
    dict[str, object],
]:
    root_interval, _root_values = mass_audit.refined_root_interval(
        ROOT_BISECTIONS
    )
    lowers, uppers, metadata = mass_audit.dominant_mass_intervals(
        root_interval,
        report_progress=report_progress,
        started=started,
    )
    centres = np.empty(cycle_audit.DIMENSION)
    radii = np.empty(cycle_audit.DIMENSION)
    for state, (lower, upper) in enumerate(zip(lowers, uppers, strict=True)):
        midpoint = (lower + upper) / 2
        centre = float(midpoint)
        centre_fraction = Fraction.from_float(centre)
        radius = max(centre_fraction - lower, upper - centre_fraction)
        centres[state] = centre
        radii[state] = fraction_up(radius)
    return root_interval, centres, radii, {
        **metadata,
        "rootBisections": ROOT_BISECTIONS,
        "maximumStoredBinary64Radius": float(np.max(radii)),
    }


def scalar_interval(
    degree: int,
    root_interval: tuple[Fraction, Fraction],
) -> tuple[float, float, float, float]:
    lower = 16**degree * root_interval[0]
    upper = 16**degree * root_interval[1]
    midpoint = (lower + upper) / 2
    centre = float(midpoint)
    centre_fraction = Fraction.from_float(centre)
    radius = max(centre_fraction - lower, upper - centre_fraction)
    return centre, fraction_up(radius), fraction_down(lower), fraction_up(upper)


def residual_enclosure(
    right_centre: np.ndarray,
    right_radius: np.ndarray,
    solution: np.ndarray,
    cycle: csr_matrix,
    cycle_absolute: csr_matrix,
    scalar_centre: float,
    scalar_radius: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Enclose b-(sI-C)x for channel-major b and x arrays."""
    cycle_centre, cycle_radius = sparse_product_enclosure(
        cycle,
        cycle_absolute,
        solution.T,
        np.zeros_like(solution.T),
    )
    scalar_product = scalar_centre * solution.T
    one_gamma = gamma_bound(1)
    scalar_rounding = guarded_up(
        one_gamma * np.abs(scalar_product) / (1 - one_gamma)
        + scalar_radius * np.abs(solution.T)
    )
    residual_centre = right_centre.T - scalar_product + cycle_centre
    addition_gamma = gamma_bound(3)
    addition_absolute = (
        np.abs(right_centre.T)
        + np.abs(scalar_product)
        + np.abs(cycle_centre)
    )
    residual_radius = guarded_up(
        right_radius.T
        + scalar_rounding
        + cycle_radius
        + addition_gamma * addition_absolute / (1 - addition_gamma)
    )
    return residual_centre.T, residual_radius.T


def solution_error_radii(
    degree: int,
    residual_centre: np.ndarray,
    residual_radius: np.ndarray,
    scalar_lower: float,
    norms: dict[str, int | float],
) -> tuple[np.ndarray, dict[str, object]]:
    absolute_residual = np.abs(residual_centre) + residual_radius
    channel_radii = np.empty(len(residual_centre))
    if degree == 1:
        denominator = scalar_lower - float(norms["twoNormUpper"])
        if not denominator > 0:
            raise AssertionError("degree-one two-norm denominator is not positive")
        for channel, values in enumerate(absolute_residual):
            norm = float(np.linalg.norm(values)) * NORM_GUARD
            norm = math.nextafter(norm, math.inf)
            channel_radii[channel] = guarded_up(norm / denominator)
        method = "Euclidean residual with exact C^T C row-sum bound"
        residual_norm = "two"
    else:
        denominator = scalar_lower - int(norms["infinityNorm"])
        if not denominator > 0:
            raise AssertionError("infinity-norm denominator is not positive")
        maxima = np.max(absolute_residual, axis=1)
        channel_radii[:] = guarded_up(maxima / denominator)
        method = "infinity residual with strict diagonal dominance"
        residual_norm = "infinity"
    return channel_radii, {
        "method": method,
        "residualNorm": residual_norm,
        "resolventDenominatorLower": denominator,
        "maximumAbsoluteResidualBound": float(np.max(absolute_residual)),
        "maximumChannelRadius": float(np.max(channel_radii)),
        "maximumChannelRadiusIndex": int(np.argmax(channel_radii)),
    }


def centering_operator(
    indices: list[tuple[int, ...]],
) -> csr_matrix:
    index_map = {alpha: index for index, alpha in enumerate(indices)}
    rows: list[int] = []
    columns: list[int] = []
    values: list[float] = []
    for target, alpha in enumerate(indices):
        for beta in np.ndindex(*(value + 1 for value in alpha)):
            coefficient = 1.0
            for coordinate in range(pilot.VARIABLES):
                coefficient *= (
                    math.comb(alpha[coordinate], beta[coordinate])
                    * (-pilot.CENTER)
                    ** (alpha[coordinate] - beta[coordinate])
                )
            rows.append(target)
            columns.append(index_map[tuple(beta)])
            values.append(coefficient)
    operator = csr_matrix(
        (np.array(values), (np.array(rows), np.array(columns))),
        shape=(len(indices), len(indices)),
    )
    operator.sum_duplicates()
    operator.eliminate_zeros()
    return operator


def array_sha256(values: np.ndarray) -> str:
    canonical = np.ascontiguousarray(values.astype("<f8", copy=False))
    return hashlib.sha256(canonical.tobytes()).hexdigest()


def enclosed_moments(
    maximum_degree: int,
    report_progress: bool,
    started: float,
) -> tuple[
    list[tuple[int, ...]],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
    dict[str, object],
]:
    transfers = [
        cycle_audit.signed_digit_transfer(0),
        cycle_audit.signed_digit_transfer(1),
    ]
    cycle = cycle_audit.cycle_matrix(transfers).astype(float)
    assert_exact_binary_coefficients(cycle, "signed cycle")
    cycle_absolute = absolute_matrix(cycle)
    norms = cycle_norms(cycle)
    groups = {bit: pilot.digit_edge_groups(bit) for bit in (0, 1)}
    subset_matrices = {
        bit: pilot.subset_transfer_matrices(groups[bit]) for bit in (0, 1)
    }
    for bit in (0, 1):
        for mask, matrix in enumerate(subset_matrices[bit]):
            assert_exact_binary_coefficients(
                matrix,
                f"subset matrix bit {bit} mask {mask}",
            )
    subset_absolute = {
        bit: [absolute_matrix(matrix) for matrix in subset_matrices[bit]]
        for bit in (0, 1)
    }

    root_interval, mass_centre, mass_radius, mass_metadata = (
        exact_initial_intervals(report_progress, started)
    )
    old_indices: list[tuple[int, ...]] = []
    old_centres = np.empty((0, cycle_audit.DIMENSION))
    old_radii = np.empty((0, cycle_audit.DIMENSION))
    degree_records: list[dict[str, object]] = []

    for degree in range(maximum_degree + 1):
        indices = pilot.multiindices(degree)
        index_map = {alpha: index for index, alpha in enumerate(indices)}
        centres = np.zeros((len(indices), cycle_audit.DIMENSION))
        radii = np.zeros_like(centres)
        if degree == 0:
            centres[0] = mass_centre
            radii[0] = mass_radius
            record = {
                "degree": 0,
                "cumulativeChannels": 1,
                "homogeneousChannels": 1,
                "maximumAbsoluteCentre": float(np.max(np.abs(centres))),
                "maximumRadius": float(np.max(radii)),
                "maximumRelativeRadius": float(
                    np.max(radii / np.maximum(np.abs(centres), 1.0e-300))
                ),
                "method": "exact rational dominant-mass intervals stored as binary64 enclosures",
            }
        else:
            for old_index, alpha in enumerate(old_indices):
                target = index_map[alpha]
                centres[target] = old_centres[old_index]
                radii[target] = old_radii[old_index]
            transported_centre, transported_radius = enclosed_raw_cycle(
                centres,
                radii,
                indices,
                subset_matrices,
                subset_absolute,
                report_progress,
                started,
            )
            current = np.array(
                [
                    index
                    for index, alpha in enumerate(indices)
                    if sum(alpha) == degree
                ],
                dtype=np.int32,
            )
            scalar_centre, scalar_radius, scalar_lower, scalar_upper = (
                scalar_interval(degree, root_interval)
            )
            solution, terms, _binary_residual = pilot.neumann_solve(
                cycle,
                scalar_centre,
                transported_centre[current].T,
                tolerance=1.0e-18,
                maximum_terms=160,
            )
            centres[current] = solution.T
            residual_centre, residual_radius = residual_enclosure(
                transported_centre[current],
                transported_radius[current],
                centres[current],
                cycle,
                cycle_absolute,
                scalar_centre,
                scalar_radius,
            )
            channel_radii, error_record = solution_error_radii(
                degree,
                residual_centre,
                residual_radius,
                scalar_lower,
                norms,
            )
            radii[current] = channel_radii[:, None]
            record = {
                "degree": degree,
                "cumulativeChannels": len(indices),
                "homogeneousChannels": len(current),
                "neumannTerms": terms,
                "scalarCentre": scalar_centre,
                "scalarRadius": scalar_radius,
                "scalarLower": scalar_lower,
                "scalarUpper": scalar_upper,
                "maximumAbsoluteCentre": float(
                    np.max(np.abs(centres[current]))
                ),
                "maximumRadius": float(np.max(radii[current])),
                "maximumRelativeRadius": float(
                    np.max(
                        radii[current]
                        / np.maximum(np.abs(centres[current]), 1.0e-300)
                    )
                ),
                **error_record,
            }
        degree_records.append(record)
        progress(
            report_progress,
            started,
            "degree enclosed",
            degree=degree,
            channels=len(indices),
            maximum_radius=f"{record['maximumRadius']:.3e}",
            relative=f"{record['maximumRelativeRadius']:.3e}",
        )
        old_indices, old_centres, old_radii = indices, centres, radii

    operator = centering_operator(old_indices)
    if not np.all(np.isfinite(operator.data)):
        raise AssertionError("centering operator is not finite")
    centred_centre, centred_radius = sparse_product_enclosure(
        operator,
        absolute_matrix(operator),
        old_centres,
        old_radii,
    )
    summary = {
        "cycleNorms": norms,
        "dominantRoot": {
            "lower": f"{root_interval[0].numerator}/{root_interval[0].denominator}",
            "upper": f"{root_interval[1].numerator}/{root_interval[1].denominator}",
            "lowerDecimal": fraction_down(root_interval[0]),
            "upperDecimal": fraction_up(root_interval[1]),
        },
        "dominantMass": mass_metadata,
        "degrees": degree_records,
        "centredMoments": {
            "maximumAbsoluteCentre": float(np.max(np.abs(centred_centre))),
            "maximumRadius": float(np.max(centred_radius)),
            "observableMaximumRadius": float(
                np.max(centred_radius[:, pilot.OBSERVABLE_STATE])
            ),
            "rawCentreSha256": array_sha256(old_centres),
            "rawRadiusSha256": array_sha256(old_radii),
            "centredCentreSha256": array_sha256(centred_centre),
            "centredRadiusSha256": array_sha256(centred_radius),
            "canonicalArrayFormat": (
                "C-contiguous little-endian IEEE-754 binary64, channel-major then state"
            ),
        },
    }
    return (
        old_indices,
        old_centres,
        old_radii,
        centred_centre,
        centred_radius,
        summary,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument(
        "--max-degree",
        type=int,
        default=DEFAULT_BASELINE_DEGREE,
        help="degree four already demonstrates loss of useful precision",
    )
    parser.add_argument("--source-commit", default="uncommitted")
    parser.add_argument("--progress", action="store_true")
    arguments = parser.parse_args()
    if not 0 <= arguments.max_degree <= MAXIMUM_DEGREE:
        raise ValueError("max-degree must lie between zero and ten")
    started = time.perf_counter()
    (
        indices,
        raw_centre,
        raw_radius,
        centred_centre,
        centred_radius,
        summary,
    ) = enclosed_moments(
        arguments.max_degree,
        arguments.progress,
        started,
    )
    checks = {
        "allRadiiAreFiniteAndNonnegative": bool(
            np.all(np.isfinite(raw_radius))
            and np.all(raw_radius >= 0)
            and np.all(np.isfinite(centred_radius))
            and np.all(centred_radius >= 0)
        ),
        "allCentresAreFinite": bool(
            np.all(np.isfinite(raw_centre))
            and np.all(np.isfinite(centred_centre))
        ),
        "cycleNormsMatchExactIntegerAudit": (
            summary["cycleNorms"]["infinityNorm"]
            == EXPECTED_CYCLE_INFINITY_NORM
            and summary["cycleNorms"]["normalInfinityNorm"]
            == EXPECTED_NORMAL_INFINITY_NORM
        ),
        "dominantMassVectorHashMatchesR068B2e": (
            summary["dominantMass"]["canonicalIntervalVectorSha256"]
            == "bf424dfb3c9ce85d1e47d2270b329f6cb4af51e32e665663949d6c53cf6f0e53"
        ),
        "allDegreesArePresent": len(summary["degrees"]) == arguments.max_degree + 1,
        "allPositiveDegreeResolventDenominatorsArePositive": all(
            record.get("resolventDenominatorLower", 1) > 0
            for record in summary["degrees"]
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)
    precision_sufficient = bool(
        arguments.max_degree == MAXIMUM_DEGREE
        and summary["centredMoments"]["maximumRadius"] <= 1.0e-18
    )
    report = {
        "schemaVersion": "1.0",
        "status": (
            "precision-baseline-passed"
            if precision_sufficient
            else "precision-baseline-rejected"
        ),
        "classification": (
            "binary64 centre-radius negative control for the dominant "
            f"degree-{arguments.max_degree} moment lift; this is not the "
            "formal binary128 certificate"
        ),
        "precisionSufficientForHeatStage": precision_sufficient,
        "checks": checks,
        "parameters": {
            "maximumDegree": arguments.max_degree,
            "spatialVariables": pilot.VARIABLES,
            "channelsPerState": len(indices),
            "stateDimension": cycle_audit.DIMENSION,
            "totalRawMomentCoordinates": int(raw_centre.size),
            "rootBisections": ROOT_BISECTIONS,
            "unitRoundoff": UNIT_ROUNDOFF,
            "arithmeticGuard": ARITHMETIC_GUARD,
            "normGuard": NORM_GUARD,
        },
        "enclosure": summary,
        "provenance": {
            "sourceCommit": arguments.source_commit,
            "dominantMassCertificateCommit": (
                "c24abb94584f7b9e76b28191f5b1c6426c41dbb5"
            ),
        },
        "runtime": {
            "elapsedSeconds": time.perf_counter() - started,
            "python": platform.python_version(),
            "numpy": np.__version__,
            "scipy": scipy.__version__,
            "platform": platform.platform(),
        },
        "limitations": [
            "The heat Taylor coefficients are not enclosed in this certificate.",
            "The signature-compressed observable defect is not enclosed here.",
            "No final eighth-order heat sign is claimed by this component alone.",
            "No claim is made about general 3D Navier-Stokes regularity.",
        ],
    }
    serialized = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(serialized)
    sys.stdout.write(serialized)
    progress(
        arguments.progress,
        started,
        "complete",
        degree=arguments.max_degree,
        maximum_radius=(
            f"{summary['centredMoments']['maximumRadius']:.3e}"
        ),
    )


if __name__ == "__main__":
    main()
