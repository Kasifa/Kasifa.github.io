#!/usr/bin/env python3
"""Independent finite audit for the R0.72K complex complete-root route.

This program is deliberately downstream of only the archived R0.72J
*independent* result.  It verifies that archive against its recorded SHA-256,
then performs three calculations without importing or reading any R0.72K
producer source or output:

1. a sharp real family for the directional zero-sampling constant 2;
2. complex scalar and complex Hilbert-vector directional projections; and
3. the corrected complete-root ledgers

       E rho^2 + 2*mixedRow + 2*cubic

   and

       E rho^2 + rawMixedMoment + rawTrueCubic.

The numerical checks use only the Python standard library and binary64
arithmetic.  They corroborate finite identities; they are not interval
certificates, root enumerations, asymptotic proofs, or a Navier--Stokes
regularity theorem.
"""

from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import json
import math
import os
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterable, Sequence


AUDIT_NAME = "R0.72K independent complex complete-root audit"
SCHEMA_VERSION = 1


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_ndjson(path: Path, payload: dict[str, Any]) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(payload, sort_keys=True) + "\n")


def max_rss_mb() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(value) / (1024.0 * 1024.0)
    return float(value) / 1024.0


def resource_record(started: float, event: str) -> dict[str, Any]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "time": utc_now(),
        "event": event,
        "elapsedSeconds": time.perf_counter() - started,
        "maxRssMb": max_rss_mb(),
        "userCpuSeconds": float(usage.ru_utime),
        "systemCpuSeconds": float(usage.ru_stime),
        "pid": os.getpid(),
    }


def git_commit(repository_root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "-C", str(repository_root), "rev-parse", "HEAD"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except Exception:
        return "unavailable"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def recorded_sha256(checksum_path: Path, filename: str) -> str:
    for raw_line in checksum_path.read_text(encoding="utf-8").splitlines():
        fields = raw_line.split()
        if len(fields) < 2:
            continue
        recorded_name = fields[-1].lstrip("*")
        if recorded_name == filename:
            digest = fields[0].lower()
            if len(digest) != 64 or any(
                character not in "0123456789abcdef" for character in digest
            ):
                raise ValueError(f"invalid SHA-256 entry for {filename}")
            return digest
    raise ValueError(f"missing SHA-256 entry for {filename}")


def relative_error(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), sys.float_info.min)
    return abs(left - right) / scale


def composite_simpson(
    function: Callable[[float], float | complex],
    left: float,
    right: float,
    panels: int,
) -> float | complex:
    if left == right:
        return 0.0
    if panels <= 0 or panels % 2:
        raise ValueError("Simpson panel count must be a positive even integer")
    step = (right - left) / panels
    total = function(left) + function(right)
    total += 4.0 * sum(
        function(left + index * step) for index in range(1, panels, 2)
    )
    total += 2.0 * sum(
        function(left + index * step) for index in range(2, panels, 2)
    )
    return total * step / 3.0


def piecewise_simpson(
    function: Callable[[float], float | complex],
    breakpoints: Sequence[float],
    panels: int,
) -> float | complex:
    return sum(
        composite_simpson(function, left, right, panels)
        for left, right in zip(breakpoints[:-1], breakpoints[1:])
        if right > left
    )


def find_directional_zero(
    function: Callable[[float], float],
    left: float,
    right: float,
    grid: int,
    tolerance: float,
) -> dict[str, Any]:
    if grid < 4:
        raise ValueError("projection grid must contain at least four panels")
    previous_x = left
    previous_value = float(function(previous_x))
    if abs(previous_value) <= tolerance:
        return {
            "root": previous_x,
            "residual": abs(previous_value),
            "bracketLeft": previous_x,
            "bracketRight": previous_x,
            "iterations": 0,
        }
    bracket: tuple[float, float, float, float] | None = None
    for index in range(1, grid + 1):
        current_x = left + (right - left) * index / grid
        current_value = float(function(current_x))
        if abs(current_value) <= tolerance:
            return {
                "root": current_x,
                "residual": abs(current_value),
                "bracketLeft": current_x,
                "bracketRight": current_x,
                "iterations": 0,
            }
        if previous_value * current_value < 0.0:
            bracket = (previous_x, current_x, previous_value, current_value)
            break
        previous_x = current_x
        previous_value = current_value
    if bracket is None:
        raise RuntimeError("no directional sign change found on the sample grid")

    lo, hi, f_lo, _ = bracket
    iterations = 0
    while iterations < 100:
        mid = 0.5 * (lo + hi)
        f_mid = float(function(mid))
        iterations += 1
        if abs(f_mid) <= tolerance:
            lo = mid
            hi = mid
            break
        if mid == lo or mid == hi:
            break
        if f_lo * f_mid < 0.0:
            hi = mid
        else:
            lo = mid
            f_lo = f_mid
    candidates = [lo, hi, 0.5 * (lo + hi)]
    root = min(candidates, key=lambda value: abs(float(function(value))))
    return {
        "root": root,
        "residual": abs(float(function(root))),
        "bracketLeft": lo,
        "bracketRight": hi,
        "iterations": iterations,
    }


def log_slope(rows: Sequence[dict[str, Any]], key: str, tail: int = 0) -> float:
    selected = list(rows[-tail:]) if tail else list(rows)
    if len(selected) < 2:
        raise ValueError("at least two rows are required for a log slope")
    xs = [math.log(float(row["R"])) for row in selected]
    ys = [math.log(float(row[key])) for row in selected]
    x_mean = sum(xs) / len(xs)
    y_mean = sum(ys) / len(ys)
    denominator = sum((value - x_mean) ** 2 for value in xs)
    if denominator == 0.0:
        raise ValueError("R values must not all coincide")
    return sum(
        (x_value - x_mean) * (y_value - y_mean)
        for x_value, y_value in zip(xs, ys)
    ) / denominator


def sharpness_case(n_value: int, panels: int) -> dict[str, Any]:
    if n_value < 2:
        raise ValueError("sharpness n must be at least two")
    epsilon = 1.0 / n_value
    ramp_length = 2.0 * epsilon / (1.0 + epsilon)
    ramp_start = 1.0 - ramp_length
    ramp_slope = (1.0 + epsilon) / ramp_length
    velocity_zero = ramp_start + epsilon / ramp_slope

    def velocity(t_value: float) -> float:
        if t_value <= ramp_start:
            return -epsilon
        return -epsilon + ramp_slope * (t_value - ramp_start)

    endpoint_numerical = float(
        piecewise_simpson(velocity, [0.0, ramp_start, 1.0], panels)
    )
    weighted_numerical = float(
        piecewise_simpson(
            lambda t_value: abs(velocity(t_value)) * ramp_slope,
            [ramp_start, velocity_zero, 1.0],
            panels,
        )
    )
    weighted_exact = 0.5 * (1.0 + epsilon**2)
    endpoint_slope_squared = velocity(1.0) ** 2
    rhs_exact = 2.0 * weighted_exact
    return {
        "recordType": "sharpness",
        "caseId": f"sharp-n-{n_value}",
        "n": n_value,
        "epsilon": epsilon,
        "rampStart": ramp_start,
        "rampLength": ramp_length,
        "velocityZero": velocity_zero,
        "endpointPositionExact": 0.0,
        "endpointPositionNumerical": endpoint_numerical,
        "endpointPositionResidual": abs(endpoint_numerical),
        "endpointSlopeSquared": endpoint_slope_squared,
        "weightedIntegralExact": weighted_exact,
        "weightedIntegralNumerical": weighted_numerical,
        "weightedIntegralRelativeError": relative_error(
            weighted_numerical, weighted_exact
        ),
        "twiceWeightedIntegral": rhs_exact,
        "sharpnessRatio": endpoint_slope_squared / rhs_exact,
    }


def complex_scalar_case(
    frequency: int,
    panels: int,
    projection_grid: int,
    tolerance: float,
) -> dict[str, Any]:
    if frequency <= 0:
        raise ValueError("scalar frequency must be positive")
    omega = 2.0 * math.pi * frequency
    right = 1.0 / frequency

    def curve(t_value: float) -> complex:
        return cmath.exp(1j * omega * t_value) - 1.0

    def velocity(t_value: float) -> complex:
        return 1j * omega * cmath.exp(1j * omega * t_value)

    def acceleration(t_value: float) -> complex:
        return -(omega**2) * cmath.exp(1j * omega * t_value)

    right_velocity = velocity(right)
    norming_coefficient = right_velocity.conjugate() / abs(right_velocity)

    def directional(t_value: float) -> float:
        return float((norming_coefficient * velocity(t_value)).real)

    directional_zero = find_directional_zero(
        directional, 0.0, right, projection_grid, tolerance
    )
    directional_mean = float(composite_simpson(directional, 0.0, right, panels))
    weighted = float(
        composite_simpson(
            lambda t_value: abs(velocity(t_value))
            * abs(acceleration(t_value)),
            0.0,
            right,
            panels,
        )
    )
    endpoint_squared = abs(right_velocity) ** 2
    return {
        "recordType": "complexScalar",
        "caseId": f"complex-scalar-k-{frequency}",
        "frequency": frequency,
        "intervalRight": right,
        "curveLeftResidual": abs(curve(0.0)),
        "curveRightResidual": abs(curve(right)),
        "derivativeMinimumExact": omega,
        "normingFunctionalNorm": abs(norming_coefficient),
        "normingFunctionalEndpointValue": directional(right),
        "directionalMeanNumerical": directional_mean,
        "directionalRoot": directional_zero["root"],
        "directionalRootResidual": directional_zero["residual"],
        "directionalRootBracketLeft": directional_zero["bracketLeft"],
        "directionalRootBracketRight": directional_zero["bracketRight"],
        "directionalRootIterations": directional_zero["iterations"],
        "endpointSlopeSquared": endpoint_squared,
        "weightedIntegral": weighted,
        "twiceWeightedIntegral": 2.0 * weighted,
        "inequalityRatio": endpoint_squared / (2.0 * weighted),
    }


def complex_vector_case(
    alpha: float,
    panels: int,
    projection_grid: int,
    tolerance: float,
) -> dict[str, Any]:
    if alpha <= 0.0:
        raise ValueError("vector alpha must be positive")
    omega_one = 2.0 * math.pi
    omega_two = 4.0 * math.pi

    def curve(t_value: float) -> tuple[complex, complex]:
        return (
            cmath.exp(1j * omega_one * t_value) - 1.0,
            alpha * (cmath.exp(1j * omega_two * t_value) - 1.0),
        )

    def velocity(t_value: float) -> tuple[complex, complex]:
        return (
            1j * omega_one * cmath.exp(1j * omega_one * t_value),
            1j
            * alpha
            * omega_two
            * cmath.exp(1j * omega_two * t_value),
        )

    def acceleration(t_value: float) -> tuple[complex, complex]:
        return (
            -(omega_one**2) * cmath.exp(1j * omega_one * t_value),
            -alpha
            * omega_two**2
            * cmath.exp(1j * omega_two * t_value),
        )

    def vector_norm(vector: Iterable[complex]) -> float:
        return math.sqrt(sum(abs(component) ** 2 for component in vector))

    right_velocity = velocity(1.0)
    endpoint_norm = vector_norm(right_velocity)
    norming_coefficients = tuple(
        component.conjugate() / endpoint_norm for component in right_velocity
    )

    def directional(t_value: float) -> float:
        current_velocity = velocity(t_value)
        return float(
            sum(
                coefficient * component
                for coefficient, component in zip(
                    norming_coefficients, current_velocity
                )
            ).real
        )

    directional_zero = find_directional_zero(
        directional, 0.0, 1.0, projection_grid, tolerance
    )
    directional_mean = float(composite_simpson(directional, 0.0, 1.0, panels))
    weighted = float(
        composite_simpson(
            lambda t_value: vector_norm(velocity(t_value))
            * vector_norm(acceleration(t_value)),
            0.0,
            1.0,
            panels,
        )
    )
    endpoint_squared = endpoint_norm**2
    return {
        "recordType": "complexVector",
        "caseId": f"complex-vector-alpha-{alpha:g}",
        "alpha": alpha,
        "curveLeftResidual": vector_norm(curve(0.0)),
        "curveRightResidual": vector_norm(curve(1.0)),
        "derivativeMinimumExact": endpoint_norm,
        "normingFunctionalNorm": vector_norm(norming_coefficients),
        "normingFunctionalEndpointValue": directional(1.0),
        "directionalMeanNumerical": directional_mean,
        "directionalRoot": directional_zero["root"],
        "directionalRootResidual": directional_zero["residual"],
        "directionalRootBracketLeft": directional_zero["bracketLeft"],
        "directionalRootBracketRight": directional_zero["bracketRight"],
        "directionalRootIterations": directional_zero["iterations"],
        "endpointSlopeSquared": endpoint_squared,
        "weightedIntegral": weighted,
        "twiceWeightedIntegral": 2.0 * weighted,
        "inequalityRatio": endpoint_squared / (2.0 * weighted),
    }


def derive_ledger_case(source_row: dict[str, Any]) -> dict[str, Any]:
    required = {
        "R",
        "N",
        "launchEnergy",
        "rhoSquared",
        "mixedRow",
        "deltaIntegralAbsHB",
        "rawBvProxyFirstRoot",
        "rawBvProxyMixedMoment",
        "rawBvProxyTrueCubic",
        "rawBvProxyTargetDiagonal",
        "rawMeasuredBvUpperProxy",
        "theta",
        "referencePayment",
        "physicalCriticalAction",
        "rootH",
        "evolvedRootResidual",
    }
    missing = sorted(required.difference(source_row))
    if missing:
        raise ValueError(f"R0.72J independent row is missing fields: {missing}")

    R = int(source_row["R"])
    launch_energy = float(source_row["launchEnergy"])
    rho_squared = float(source_row["rhoSquared"])
    mixed_row = float(source_row["mixedRow"])
    cubic = float(source_row["deltaIntegralAbsHB"])
    raw_mixed_moment = float(source_row["rawBvProxyMixedMoment"])
    raw_true_cubic = float(source_row["rawBvProxyTrueCubic"])
    theta = float(source_row["theta"])
    reference_payment = float(source_row["referencePayment"])
    if R <= 0 or theta <= 0.0 or reference_payment <= 0.0:
        raise ValueError("R, theta, and referencePayment must be positive")

    first_root_payment = launch_energy * rho_squared
    measured_complete = first_root_payment + 2.0 * mixed_row + 2.0 * cubic
    analytic_complete = (
        first_root_payment + raw_mixed_moment + raw_true_cubic
    )
    exact_root_lower = float(source_row["rootH"]) ** 2

    physical_measured = theta * measured_complete
    physical_analytic = theta * analytic_complete
    physical_exact_root = theta * exact_root_lower
    normalized_measured = physical_measured / reference_payment
    normalized_analytic = physical_analytic / reference_payment
    normalized_exact_root = physical_exact_root / reference_payment
    archived_without_diagonal = float(source_row["rawMeasuredBvUpperProxy"]) - float(
        source_row["rawBvProxyTargetDiagonal"]
    )

    return {
        "recordType": "ledger",
        "caseId": f"ledger-R-{R}",
        "R": R,
        "N": int(source_row["N"]),
        "launchEnergy": launch_energy,
        "rhoSquared": rho_squared,
        "firstRootPayment": first_root_payment,
        "archivedFirstRootPayment": float(source_row["rawBvProxyFirstRoot"]),
        "firstRootRelativeError": relative_error(
            first_root_payment, float(source_row["rawBvProxyFirstRoot"])
        ),
        "mixedRow": mixed_row,
        "trueCubicRow": cubic,
        "twiceMixedRow": 2.0 * mixed_row,
        "twiceTrueCubicRow": 2.0 * cubic,
        "rawMixedMoment": raw_mixed_moment,
        "rawTrueCubic": raw_true_cubic,
        "rawTrueCubicRelativeError": relative_error(
            raw_true_cubic, 2.0 * cubic
        ),
        "measuredCompleteLedgerUpper": measured_complete,
        "analyticCompleteLedgerProxy": analytic_complete,
        "archivedProxyWithoutDiagonal": archived_without_diagonal,
        "analyticProxyLineageRelativeError": relative_error(
            analytic_complete, archived_without_diagonal
        ),
        "exactRootLower": exact_root_lower,
        "exactRootResidual": float(source_row["evolvedRootResidual"]),
        "measuredSlackOverExactRoot": measured_complete - exact_root_lower,
        "analyticSlackOverMeasured": analytic_complete - measured_complete,
        "measuredCompleteDivR2": measured_complete / R**2,
        "analyticCompleteDivR2": analytic_complete / R**2,
        "exactRootLowerDivR2": exact_root_lower / R**2,
        "theta": theta,
        "referencePayment": reference_payment,
        "physicalCriticalAction": float(source_row["physicalCriticalAction"]),
        "physicalMeasuredCompleteUpper": physical_measured,
        "physicalAnalyticCompleteProxy": physical_analytic,
        "physicalExactRootLower": physical_exact_root,
        "physicalMeasuredDivR": physical_measured / R,
        "physicalAnalyticDivR": physical_analytic / R,
        "normalizedMeasuredCompleteUpper": normalized_measured,
        "normalizedAnalyticCompleteProxy": normalized_analytic,
        "normalizedExactRootLower": normalized_exact_root,
        "normalizedMeasuredTimesR23": normalized_measured * R ** (2.0 / 3.0),
        "normalizedAnalyticTimesR23": normalized_analytic * R ** (2.0 / 3.0),
        "normalizedExactRootTimesR23": normalized_exact_root
        * R ** (2.0 / 3.0),
    }


def write_union_csv(path: Path, groups: Sequence[Sequence[dict[str, Any]]]) -> None:
    rows = [row for group in groups for row in group]
    if not rows:
        raise ValueError("at least one CSV row is required")
    preferred = ["recordType", "caseId", "R", "N"]
    all_fields = {key for row in rows for key in row}
    fieldnames = [field for field in preferred if field in all_fields]
    fieldnames.extend(sorted(all_fields.difference(fieldnames)))
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("research/certificates/r072k"),
    )
    parser.add_argument(
        "--sharpness-n-values",
        type=int,
        nargs="+",
        default=[4, 8, 16, 32, 64, 128, 256, 512, 1024],
    )
    parser.add_argument(
        "--scalar-frequencies", type=int, nargs="+", default=[1, 2, 4, 8]
    )
    parser.add_argument(
        "--vector-alphas", type=float, nargs="+", default=[0.125, 0.25, 0.5]
    )
    parser.add_argument("--quadrature-panels", type=int, default=4096)
    parser.add_argument("--projection-grid", type=int, default=4096)
    parser.add_argument("--tolerance", type=float, default=1.0e-10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.quadrature_panels <= 0 or args.quadrature_panels % 2:
        raise ValueError("quadrature-panels must be a positive even integer")
    if args.projection_grid < 4:
        raise ValueError("projection-grid must be at least four")
    if args.tolerance <= 0.0:
        raise ValueError("tolerance must be positive")
    if len(args.sharpness_n_values) < 2:
        raise ValueError("at least two sharpness n values are required")

    started = time.perf_counter()
    repository_root = Path(__file__).resolve().parents[1]
    archived_directory = repository_root / "research" / "certificates" / "r072j"
    archived_result_path = archived_directory / "independent-result.json"
    archived_checksums_path = archived_directory / "SHA256SUMS"

    output_dir = args.output_dir
    if not output_dir.is_absolute():
        output_dir = (Path.cwd() / output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    progress_path = output_dir / "independent-progress.ndjson"
    resource_path = output_dir / "independent-resource.ndjson"
    progress_path.write_text("", encoding="utf-8")
    resource_path.write_text("", encoding="utf-8")
    append_ndjson(
        progress_path,
        {"time": utc_now(), "event": "audit_start", "audit": AUDIT_NAME},
    )
    append_ndjson(resource_path, resource_record(started, "audit_start"))

    expected_archive_sha = recorded_sha256(
        archived_checksums_path, archived_result_path.name
    )
    actual_archive_sha = sha256(archived_result_path)
    if actual_archive_sha != expected_archive_sha:
        raise RuntimeError(
            "archived R0.72J independent result does not match SHA256SUMS"
        )
    archived_result = json.loads(archived_result_path.read_text(encoding="utf-8"))
    if archived_result.get("status") != "passed":
        raise RuntimeError("archived R0.72J independent audit is not passed")
    if archived_result.get("audit") != "R0.72J independent mixed-parity audit":
        raise RuntimeError("unexpected archived R0.72J audit identity")
    archived_cases = archived_result.get("cases")
    if not isinstance(archived_cases, list) or not archived_cases:
        raise RuntimeError("archived R0.72J independent cases are missing")

    lineage = {
        "sourceAudit": archived_result["audit"],
        "sourceStatus": archived_result["status"],
        "sourceGeneratedAt": archived_result.get("generatedAt", "unavailable"),
        "sourceGitCommit": archived_result.get("gitCommit", "unavailable"),
        "sourceImplementationSha256": archived_result.get("config", {}).get(
            "sourceSha256", "unavailable"
        ),
        "sourceRelativePath": "research/certificates/r072j/independent-result.json",
        "sourceChecksumRelativePath": "research/certificates/r072j/SHA256SUMS",
        "sourceExpectedSha256": expected_archive_sha,
        "sourceActualSha256": actual_archive_sha,
        "sourceSha256Verified": True,
    }
    append_ndjson(
        progress_path,
        {"time": utc_now(), "event": "r072j_lineage_verified", **lineage},
    )
    append_ndjson(resource_path, resource_record(started, "lineage_verified"))

    config = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "outputDirectory": str(output_dir),
        "sharpnessNValues": args.sharpness_n_values,
        "scalarFrequencies": args.scalar_frequencies,
        "vectorAlphas": args.vector_alphas,
        "quadraturePanels": args.quadrature_panels,
        "projectionGrid": args.projection_grid,
        "tolerance": args.tolerance,
        "arithmetic": "Python binary64; standard library only",
        "directionalFunctional": (
            "complex-linear norming functional followed by real part"
        ),
        "measuredCompleteLedger": (
            "launchEnergy*rhoSquared + 2*mixedRow + "
            "2*deltaIntegralAbsHB"
        ),
        "analyticCompleteLedgerProxy": (
            "launchEnergy*rhoSquared + rawBvProxyMixedMoment + "
            "rawBvProxyTrueCubic"
        ),
        "physicalConversion": "theta*rawLedger",
        "normalization": "physicalLedger/referencePayment",
        "producerR072KImported": False,
        "producerR072KRead": False,
        "newPdeEvolution": False,
        "sourceSha256": sha256(Path(__file__).resolve()),
        "lineage": lineage,
    }
    (output_dir / "independent-config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    append_ndjson(
        progress_path, {"time": utc_now(), "event": "config_written"}
    )

    sharpness_cases: list[dict[str, Any]] = []
    for n_value in args.sharpness_n_values:
        row = sharpness_case(n_value, args.quadrature_panels)
        sharpness_cases.append(row)
        append_ndjson(
            progress_path,
            {
                "time": utc_now(),
                "event": "sharpness_case_complete",
                "caseId": row["caseId"],
                "sharpnessRatio": row["sharpnessRatio"],
            },
        )
        append_ndjson(
            resource_path,
            resource_record(started, f"sharpness_case_{n_value}_complete"),
        )

    scalar_cases: list[dict[str, Any]] = []
    for frequency in args.scalar_frequencies:
        row = complex_scalar_case(
            frequency,
            args.quadrature_panels,
            args.projection_grid,
            args.tolerance,
        )
        scalar_cases.append(row)
        append_ndjson(
            progress_path,
            {
                "time": utc_now(),
                "event": "complex_scalar_case_complete",
                "caseId": row["caseId"],
                "directionalRootResidual": row["directionalRootResidual"],
            },
        )
        append_ndjson(
            resource_path,
            resource_record(started, f"complex_scalar_{frequency}_complete"),
        )

    vector_cases: list[dict[str, Any]] = []
    for alpha in args.vector_alphas:
        row = complex_vector_case(
            alpha,
            args.quadrature_panels,
            args.projection_grid,
            args.tolerance,
        )
        vector_cases.append(row)
        append_ndjson(
            progress_path,
            {
                "time": utc_now(),
                "event": "complex_vector_case_complete",
                "caseId": row["caseId"],
                "directionalRootResidual": row["directionalRootResidual"],
            },
        )
        append_ndjson(
            resource_path,
            resource_record(started, f"complex_vector_{alpha:g}_complete"),
        )

    ledger_cases = sorted(
        (derive_ledger_case(row) for row in archived_cases),
        key=lambda row: int(row["R"]),
    )
    for row in ledger_cases:
        append_ndjson(
            progress_path,
            {
                "time": utc_now(),
                "event": "ledger_case_complete",
                "caseId": row["caseId"],
                "measuredCompleteLedgerUpper": row[
                    "measuredCompleteLedgerUpper"
                ],
                "analyticCompleteLedgerProxy": row[
                    "analyticCompleteLedgerProxy"
                ],
            },
        )
    append_ndjson(resource_path, resource_record(started, "ledgers_complete"))

    tail = min(3, len(ledger_cases))
    slopes = {
        "measuredCompleteRawAll": log_slope(
            ledger_cases, "measuredCompleteLedgerUpper"
        ),
        "measuredCompleteRawTail": log_slope(
            ledger_cases, "measuredCompleteLedgerUpper", tail
        ),
        "analyticCompleteRawAll": log_slope(
            ledger_cases, "analyticCompleteLedgerProxy"
        ),
        "analyticCompleteRawTail": log_slope(
            ledger_cases, "analyticCompleteLedgerProxy", tail
        ),
        "physicalMeasuredAll": log_slope(
            ledger_cases, "physicalMeasuredCompleteUpper"
        ),
        "physicalAnalyticAll": log_slope(
            ledger_cases, "physicalAnalyticCompleteProxy"
        ),
        "normalizedMeasuredAll": log_slope(
            ledger_cases, "normalizedMeasuredCompleteUpper"
        ),
        "normalizedMeasuredTail": log_slope(
            ledger_cases, "normalizedMeasuredCompleteUpper", tail
        ),
        "normalizedAnalyticAll": log_slope(
            ledger_cases, "normalizedAnalyticCompleteProxy"
        ),
        "normalizedAnalyticTail": log_slope(
            ledger_cases, "normalizedAnalyticCompleteProxy", tail
        ),
    }

    sharpness_ratios = [float(row["sharpnessRatio"]) for row in sharpness_cases]
    checks = {
        "archiveSha256Verified": actual_archive_sha == expected_archive_sha,
        "archiveIndependentAuditPassed": archived_result["status"] == "passed",
        "sharpnessEndpointRootsAccurate": max(
            float(row["endpointPositionResidual"]) for row in sharpness_cases
        )
        < 50.0 * args.tolerance,
        "sharpnessWeightedIntegralsAccurate": max(
            float(row["weightedIntegralRelativeError"])
            for row in sharpness_cases
        )
        < 50.0 * args.tolerance,
        "sharpnessRatiosStrictlyIncrease": all(
            right > left
            for left, right in zip(sharpness_ratios[:-1], sharpness_ratios[1:])
        ),
        "sharpnessRatioApproachesOne": sharpness_ratios[-1] > 0.999,
        "complexScalarEndpointsAreRoots": max(
            max(
                float(row["curveLeftResidual"]),
                float(row["curveRightResidual"]),
            )
            for row in scalar_cases
        )
        < 50.0 * args.tolerance,
        "complexScalarDerivativesNeverVanish": min(
            float(row["derivativeMinimumExact"]) for row in scalar_cases
        )
        > 0.0,
        "complexScalarNormingFunctionalsUnit": max(
            abs(float(row["normingFunctionalNorm"]) - 1.0)
            for row in scalar_cases
        )
        < 50.0 * args.tolerance,
        "complexScalarNormingEndpointExact": max(
            relative_error(
                float(row["normingFunctionalEndpointValue"]),
                math.sqrt(float(row["endpointSlopeSquared"])),
            )
            for row in scalar_cases
        )
        < 50.0 * args.tolerance,
        "complexScalarDirectionalZerosRecovered": max(
            float(row["directionalRootResidual"]) for row in scalar_cases
        )
        < 50.0 * args.tolerance,
        "complexScalarDirectionalMeansVanish": max(
            abs(float(row["directionalMeanNumerical"])) for row in scalar_cases
        )
        < 100.0 * args.tolerance,
        "complexScalarBoundsHold": all(
            float(row["endpointSlopeSquared"])
            <= float(row["twiceWeightedIntegral"])
            * (1.0 + 100.0 * args.tolerance)
            for row in scalar_cases
        ),
        "complexVectorEndpointsAreRoots": max(
            max(
                float(row["curveLeftResidual"]),
                float(row["curveRightResidual"]),
            )
            for row in vector_cases
        )
        < 50.0 * args.tolerance,
        "complexVectorDerivativesNeverVanish": min(
            float(row["derivativeMinimumExact"]) for row in vector_cases
        )
        > 0.0,
        "complexVectorNormingFunctionalsUnit": max(
            abs(float(row["normingFunctionalNorm"]) - 1.0)
            for row in vector_cases
        )
        < 50.0 * args.tolerance,
        "complexVectorNormingEndpointExact": max(
            relative_error(
                float(row["normingFunctionalEndpointValue"]),
                math.sqrt(float(row["endpointSlopeSquared"])),
            )
            for row in vector_cases
        )
        < 50.0 * args.tolerance,
        "complexVectorDirectionalZerosRecovered": max(
            float(row["directionalRootResidual"]) for row in vector_cases
        )
        < 50.0 * args.tolerance,
        "complexVectorDirectionalMeansVanish": max(
            abs(float(row["directionalMeanNumerical"])) for row in vector_cases
        )
        < 100.0 * args.tolerance,
        "complexVectorBoundsHold": all(
            float(row["endpointSlopeSquared"])
            <= float(row["twiceWeightedIntegral"])
            * (1.0 + 100.0 * args.tolerance)
            for row in vector_cases
        ),
        "firstRootLineageExact": max(
            float(row["firstRootRelativeError"]) for row in ledger_cases
        )
        < 50.0 * args.tolerance,
        "trueCubicFactorTwoExact": max(
            float(row["rawTrueCubicRelativeError"]) for row in ledger_cases
        )
        < 50.0 * args.tolerance,
        "analyticProxyEqualsArchivedProxyWithoutDiagonal": max(
            float(row["analyticProxyLineageRelativeError"])
            for row in ledger_cases
        )
        < 50.0 * args.tolerance,
        "measuredCompleteBoundsExactRootRows": all(
            float(row["measuredSlackOverExactRoot"]) >= 0.0
            for row in ledger_cases
        ),
        "analyticProxyBoundsMeasuredComplete": all(
            float(row["analyticSlackOverMeasured"]) >= 0.0
            for row in ledger_cases
        ),
        "measuredRawScaleNearR2": 1.5
        < slopes["measuredCompleteRawTail"]
        < 2.4,
        "analyticRawScaleNearR2": 1.5
        < slopes["analyticCompleteRawTail"]
        < 2.4,
        "normalizedMeasuredDecays": slopes["normalizedMeasuredTail"] < -0.3,
        "normalizedAnalyticDecays": slopes["normalizedAnalyticTail"] < -0.3,
        "producerR072KUnused": True,
    }
    checks = {key: bool(value) for key, value in checks.items()}
    passed = all(checks.values())

    environment = {
        "python": sys.version,
        "platform": platform.platform(),
        "executable": sys.executable,
        "cpuCount": os.cpu_count(),
        "maxRssMb": max_rss_mb(),
        "standardLibraryOnly": True,
    }
    result = {
        "schemaVersion": SCHEMA_VERSION,
        "audit": AUDIT_NAME,
        "status": "passed" if passed else "failed",
        "generatedAt": utc_now(),
        "gitCommit": git_commit(repository_root),
        "config": config,
        "lineage": lineage,
        "environment": environment,
        "theoremUnderAudit": {
            "gapBound": (
                "sum_{j=2}^m ||X'(t_j)||^2 <= "
                "2*integral ||X'||*||X''||"
            ),
            "measuredCompleteLedger": (
                "E*rho^2 + 2*mixedRow + 2*cubic"
            ),
            "analyticCompleteLedgerProxy": (
                "E*rho^2 + rawMixedMoment + rawTrueCubic"
            ),
            "integratingFactorLoss": (
                "none: exp(-2*lambda*(t_j-x)) <= 1 on each root gap"
            ),
        },
        "slopes": slopes,
        "checks": checks,
        "sharpnessCases": sharpness_cases,
        "complexScalarCases": scalar_cases,
        "complexVectorCases": vector_cases,
        "ledgerCases": ledger_cases,
        "limitations": [
            "binary64 quadrature and zero reconstruction are not interval certificates",
            "the finite audit illustrates but does not prove the analytic directional lemma",
            "the audit reconstructs one directional zero per test curve and does not enumerate complete complex root sets",
            "only SHA-verified archived R0.72J independent rows are transformed; no new PDE evolution is performed",
            "physical conversion inherits theta, referencePayment, and the model choices of the archived R0.72J independent audit",
            "finite log-log slopes are diagnostics and not asymptotic proofs",
            "no R0.72K producer source or output is imported or read",
            "the calculation does not establish general three-dimensional Navier--Stokes regularity or resolve the Clay problem",
        ],
    }

    (output_dir / "independent-result.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_union_csv(
        output_dir / "independent-data.csv",
        [sharpness_cases, scalar_cases, vector_cases, ledger_cases],
    )
    (output_dir / "independent-environment.txt").write_text(
        "\n".join(
            [
                f"generatedAt={utc_now()}",
                f"audit={AUDIT_NAME}",
                f"python={sys.version}",
                f"platform={platform.platform()}",
                f"executable={sys.executable}",
                f"cpuCount={os.cpu_count()}",
                f"maxRssMb={max_rss_mb()}",
                "standardLibraryOnly=true",
                "producerR072KImported=false",
                "producerR072KRead=false",
                "newPdeEvolution=false",
                f"sourceR072JIndependentSha256={actual_archive_sha}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    append_ndjson(
        resource_path, resource_record(started, "artifacts_written")
    )
    append_ndjson(
        progress_path,
        {
            "time": utc_now(),
            "event": "audit_complete",
            "status": result["status"],
            "failedChecks": [key for key, value in checks.items() if not value],
            "resultSha256": sha256(output_dir / "independent-result.json"),
            "elapsedSeconds": time.perf_counter() - started,
        },
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
