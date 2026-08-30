#!/usr/bin/env python3
"""Independent shared-grid audit of the R0.73J kinetic-overlap certificate.

This file deliberately does not import the primary ODE, overlap, Chebyshev,
or certificate modules.  It checks the sealed 29 x 29 raw interval grid and
then recomputes the decisive bounds with a direct tensor DCT and a range
method different from the primary midpoint-Bernstein proof: on every cell it
evaluates the interpolant at the exact dyadic centre and adds the global
Chebyshev derivative bounds ``|T_n'| <= n^2`` times the cell radii.

The primary midpoint-Bernstein cells are also replayed, solely to audit their
serialization and margins.  They are not used by the independent Lipschitz
decision.  Both analyses still share the frozen ODE grid; this limitation and
an unexecuted direct-natural-box ODE spot-check plan are recorded explicitly.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import time
from typing import Any, Iterable, Sequence

from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GRID_SCHEMA = "r073j-kinetic-overlap-v1"
PRIMARY_SCHEMA = "r073j-kinetic-overlap-midpoint-bernstein-v2"
AUDIT_SCHEMA = "r073j-independent-overlap-shared-grid-lipschitz-v1"
OUTPUT_NAMES = ("anchor", "numerator", "rightEnergy", "leftEnergy")
GRID_SOURCE_PATHS = (
    "research/r073j_interval_core.py",
    "research/r073j_overlap_core.py",
    "research/r073j_overlap_analytic_proof.md",
    "research/r073j_chebyshev.py",
    "experiments/r073j/certify_overlap.py",
    "experiments/r073j/overlap_config.json",
    "experiments/r073j/requirements.txt",
)
ANALYSIS_SOURCE_PATHS = (
    "experiments/r073j/analyze_overlap_midpoint_bernstein.py",
)
EXPECTED_REQUIREMENT = "python-flint==0.6.0\n"
EXPECTED_CONFIG = {
    "degreeD": 28,
    "degreeLambda": 28,
    "dps": 80,
    "lambdaCenter": "17/100",
    "lambdaRadius": "3/1000",
    "lebesgueLimit": "4",
    "order": 12,
    "resourceIntervalSeconds": 30,
    "rhoD": "16",
    "rhoLambda": "16",
    "schemaVersion": GRID_SCHEMA,
    "steps": 768,
    "subdivision": {"dDepth": 3, "lambdaDepth": 4},
    "workers": 16,
}


class AuditFailure(RuntimeError):
    """A fail-closed audit error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True) + "\n"


def compact_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def atomic_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(canonical_json(value), encoding="utf-8")
    os.replace(temporary, path)


def start_log(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(compact_json(value) + "\n", encoding="utf-8")


def append_log(path: Path, value: object) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(compact_json(value) + "\n")


def emit(path: Path, event: str, **fields: object) -> None:
    append_log(path, {"time": utc_now(), "event": event, **fields})


def expect_keys(
    value: Any,
    required: Iterable[str],
    label: str,
    optional: Iterable[str] = (),
) -> dict[str, Any]:
    require(type(value) is dict, f"{label} must be a JSON object")
    required_set = set(required)
    allowed = required_set | set(optional)
    actual = set(value)
    require(not (required_set - actual),
            f"{label} missing keys: {sorted(required_set - actual)}")
    require(not (actual - allowed),
            f"{label} has unexpected keys: {sorted(actual - allowed)}")
    return value


def expect_int(value: Any, label: str, minimum: int | None = None) -> int:
    require(type(value) is int, f"{label} must be an integer (not bool)")
    if minimum is not None:
        require(value >= minimum, f"{label} must be at least {minimum}")
    return value


def expect_string(value: Any, label: str) -> str:
    require(type(value) is str and value != "", f"{label} must be nonempty text")
    return value


def parse_fraction(value: Any, label: str) -> Fraction:
    text = expect_string(value, label)
    try:
        result = Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise AuditFailure(f"{label} is not an exact rational") from error
    return result


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def arb_fraction(value: Fraction) -> arb:
    return arb(value.numerator) / value.denominator


def parse_arb(value: Any, label: str) -> arb:
    text = expect_string(value, label)
    try:
        result = arb(text)
    except Exception as error:
        raise AuditFailure(f"{label} is not a parseable Arb ball") from error
    require(result.is_finite(), f"{label} is not finite")
    return result


def parse_acb_record(value: Any, label: str) -> acb:
    record = expect_keys(value, ("real", "imag"), label)
    result = acb(
        parse_arb(record["real"], f"{label}.real"),
        parse_arb(record["imag"], f"{label}.imag"),
    )
    require(result.is_finite(), f"{label} is not finite")
    return result


def arb_text(value: arb, digits: int = 90) -> str:
    return value.str(digits, more=True)


def acb_record(value: acb) -> dict[str, str]:
    return {"real": arb_text(value.real), "imag": arb_text(value.imag)}


def choose_minimum(values: Sequence[arb], label: str) -> arb:
    require(bool(values), f"empty minimum collection: {label}")
    return min(values, key=lambda value: value.lower())


def validate_ledger(
    ledger_value: Any,
    digest_value: Any,
    expected_paths: Sequence[str],
    label: str,
) -> dict[str, Any]:
    require(type(ledger_value) is list, f"{label} must be a list")
    require(len(ledger_value) == len(expected_paths),
            f"{label} has the wrong number of entries")
    checked: list[dict[str, Any]] = []
    for index, (entry_value, expected_path) in enumerate(
        zip(ledger_value, expected_paths)
    ):
        entry = expect_keys(entry_value, ("path", "bytes", "sha256"),
                            f"{label}[{index}]")
        relative = expect_string(entry["path"], f"{label}[{index}].path")
        require(relative == expected_path, f"{label}[{index}] path/order mismatch")
        relative_path = Path(relative)
        require(not relative_path.is_absolute() and ".." not in relative_path.parts,
                f"unsafe source path in {label}: {relative}")
        absolute = (ROOT / relative_path).resolve()
        require(absolute.is_relative_to(ROOT.resolve()),
                f"source path escapes repository: {relative}")
        require(absolute.is_file(), f"source file missing: {relative}")
        file_bytes = absolute.read_bytes()
        byte_count = expect_int(entry["bytes"], f"{label}[{index}].bytes", 0)
        require(byte_count == len(file_bytes), f"byte count mismatch: {relative}")
        recorded_hash = expect_string(entry["sha256"], f"{label}[{index}].sha256")
        require(len(recorded_hash) == 64
                and all(character in "0123456789abcdef" for character in recorded_hash),
                f"invalid SHA-256 syntax: {relative}")
        require(recorded_hash == sha256_bytes(file_bytes),
                f"SHA-256 mismatch: {relative}")
        checked.append(dict(entry))
    digest = sha256_bytes(compact_json(checked).encode("ascii"))
    require(expect_string(digest_value, f"{label}Digest") == digest,
            f"{label} digest mismatch")
    return {"ledger": checked, "digest": digest}


def validate_config(config: Any) -> dict[str, Any]:
    config = expect_keys(config, EXPECTED_CONFIG.keys(), "configuration")
    require(config == EXPECTED_CONFIG,
            "configuration differs from the frozen R0.73J overlap contract")
    require((ROOT / "experiments/r073j/requirements.txt").read_text(
        encoding="utf-8") == EXPECTED_REQUIREMENT,
        "requirements.txt must exactly pin python-flint==0.6.0")
    return config


def validate_checkpoint(
    checkpoint: Any,
    config: dict[str, Any],
) -> dict[str, Any]:
    checkpoint = expect_keys(checkpoint, (
        "schemaVersion", "status", "completedAt", "sourceLedger",
        "sourceDigest", "configuration", "shape", "values",
    ), "checkpoint")
    require(checkpoint["schemaVersion"] == GRID_SCHEMA,
            "checkpoint schema mismatch")
    require(checkpoint["status"] == "grid-complete",
            "checkpoint is not a complete frozen grid")
    expect_string(checkpoint["completedAt"], "checkpoint.completedAt")
    require(checkpoint["configuration"] == config,
            "checkpoint/config mismatch")
    source = validate_ledger(
        checkpoint["sourceLedger"], checkpoint["sourceDigest"],
        GRID_SOURCE_PATHS, "checkpoint.sourceLedger",
    )
    require(checkpoint["shape"] == [29, 29], "checkpoint shape is not 29 x 29")
    records = checkpoint["values"]
    require(type(records) is list and len(records) == 841,
            "checkpoint must contain exactly 841 point records")

    grids = {
        name: [[acb(0) for _ in range(29)] for _ in range(29)]
        for name in OUTPUT_NAMES
    }
    seen: set[tuple[int, int]] = set()
    denominators: list[arb] = []
    slacks: list[arb] = []
    maximum_attempt = 0
    for record_index, item_value in enumerate(records):
        label = f"checkpoint.values[{record_index}]"
        item = expect_keys(item_value, ("dIndex", "lambdaIndex", "values", "audit"),
                           label)
        d_index = expect_int(item["dIndex"], f"{label}.dIndex", 0)
        lambda_index = expect_int(item["lambdaIndex"], f"{label}.lambdaIndex", 0)
        require(d_index < 29 and lambda_index < 29,
                f"grid index out of range at {label}")
        require((d_index, lambda_index) not in seen,
                f"duplicate grid index at {label}")
        seen.add((d_index, lambda_index))
        values = expect_keys(item["values"], OUTPUT_NAMES, f"{label}.values")
        for name in OUTPUT_NAMES:
            grids[name][d_index][lambda_index] = parse_acb_record(
                values[name], f"{label}.values.{name}"
            )
        point_audit = expect_keys(item["audit"], (
            "minimumDenominatorLower", "minimumComponentSlack",
            "maximumPicardAttempt",
        ), f"{label}.audit")
        denominator = parse_arb(point_audit["minimumDenominatorLower"],
                                f"{label}.audit.minimumDenominatorLower")
        slack = parse_arb(point_audit["minimumComponentSlack"],
                          f"{label}.audit.minimumComponentSlack")
        require(denominator.lower() > 0,
                f"nonpositive denominator audit at {label}")
        require(slack.lower() > 0, f"nonpositive Picard slack at {label}")
        attempt = expect_int(point_audit["maximumPicardAttempt"],
                             f"{label}.audit.maximumPicardAttempt", 0)
        denominators.append(denominator)
        slacks.append(slack)
        maximum_attempt = max(maximum_attempt, attempt)
    expected_lattice = {(d_index, lambda_index)
                        for d_index in range(29) for lambda_index in range(29)}
    require(seen == expected_lattice, "checkpoint index lattice is incomplete")
    return {
        "source": source,
        "grids": grids,
        "pointCount": len(records),
        "minimumDenominator": choose_minimum(denominators, "denominators"),
        "minimumSlack": choose_minimum(slacks, "Picard slacks"),
        "maximumAttempt": maximum_attempt,
    }


def chebyshev_angles(count: int) -> list[arb]:
    require(count > 0, "Chebyshev node count must be positive")
    return [(2 * index + 1) * arb.pi() / (2 * count)
            for index in range(count)]


def direct_tensor_dct(values: Sequence[Sequence[acb]]) -> list[list[acb]]:
    """Direct double DCT; no call to either staged primary transform."""
    d_count = len(values)
    require(d_count > 0, "empty DCT grid")
    lambda_count = len(values[0])
    require(lambda_count > 0 and all(len(row) == lambda_count for row in values),
            "ragged DCT grid")
    d_angles = chebyshev_angles(d_count)
    lambda_angles = chebyshev_angles(lambda_count)
    d_cosines = [[(order * angle).cos() for angle in d_angles]
                 for order in range(d_count)]
    lambda_cosines = [[(order * angle).cos() for angle in lambda_angles]
                      for order in range(lambda_count)]
    result = [[acb(0) for _ in range(lambda_count)] for _ in range(d_count)]
    for d_order in range(d_count):
        d_scale = arb(1) / d_count if d_order == 0 else arb(2) / d_count
        for lambda_order in range(lambda_count):
            lambda_scale = (arb(1) / lambda_count if lambda_order == 0
                            else arb(2) / lambda_count)
            total = acb(0)
            for d_index in range(d_count):
                subtotal = acb(0)
                for lambda_index in range(lambda_count):
                    subtotal += (
                        values[d_index][lambda_index]
                        * lambda_cosines[lambda_order][lambda_index]
                    )
                total += d_cosines[d_order][d_index] * subtotal
            result[d_order][lambda_order] = d_scale * lambda_scale * total
    return result


def one_dimensional_dct(values: Sequence[acb]) -> list[acb]:
    """Independent replay helper for the primary staged transform."""
    count = len(values)
    angles = chebyshev_angles(count)
    result: list[acb] = []
    for order in range(count):
        total = sum((value * (order * angle).cos()
                     for value, angle in zip(values, angles)), acb(0))
        total *= arb(2) / count
        if order == 0:
            total /= 2
        result.append(total)
    return result


def staged_tensor_dct_replay(
    values: Sequence[Sequence[acb]],
) -> list[list[acb]]:
    d_count = len(values)
    lambda_count = len(values[0])
    first = [one_dimensional_dct(
        [values[d_index][lambda_index] for d_index in range(d_count)]
    ) for lambda_index in range(lambda_count)]
    return [one_dimensional_dct(
        [first[lambda_index][d_order] for lambda_index in range(lambda_count)]
    ) for d_order in range(d_count)]


def chebyshev_basis_values(count: int, value: arb) -> list[arb]:
    require(count > 0, "Chebyshev basis count must be positive")
    values = [arb(1)]
    if count == 1:
        return values
    values.append(value)
    for _ in range(2, count):
        values.append(2 * value * values[-1] - values[-2])
    return values


def evaluate_tensor(
    coefficients: Sequence[Sequence[acb]],
    d_value: arb,
    lambda_value: arb,
) -> acb:
    d_basis = chebyshev_basis_values(len(coefficients), d_value)
    lambda_basis = chebyshev_basis_values(len(coefficients[0]), lambda_value)
    total = acb(0)
    for d_order, row in enumerate(coefficients):
        for lambda_order, coefficient in enumerate(row):
            total += coefficient * d_basis[d_order] * lambda_basis[lambda_order]
    return total


def verify_direct_dct(
    coefficients: Sequence[Sequence[acb]],
    values: Sequence[Sequence[acb]],
    name: str,
) -> int:
    d_nodes = [angle.cos() for angle in chebyshev_angles(len(values))]
    lambda_nodes = [angle.cos() for angle in chebyshev_angles(len(values[0]))]
    checked = 0
    for d_index, d_value in enumerate(d_nodes):
        for lambda_index, lambda_value in enumerate(lambda_nodes):
            rebuilt = evaluate_tensor(coefficients, d_value, lambda_value)
            original = values[d_index][lambda_index]
            require(rebuilt.real.contains(original.real)
                    and rebuilt.imag.contains(original.imag),
                    f"direct DCT does not contain raw {name} node "
                    f"({d_index},{lambda_index})")
            checked += 1
    return checked


def coefficients_overlap(
    left: Sequence[Sequence[acb]],
    right: Sequence[Sequence[acb]],
    name: str,
) -> None:
    require(len(left) == len(right) and len(left[0]) == len(right[0]),
            f"DCT shape mismatch for {name}")
    for d_order, (left_row, right_row) in enumerate(zip(left, right)):
        for lambda_order, (left_value, right_value) in enumerate(
            zip(left_row, right_row)
        ):
            require(left_value.real.overlaps(right_value.real)
                    and left_value.imag.overlaps(right_value.imag),
                    f"direct/staged DCT disagreement for {name} coefficient "
                    f"({d_order},{lambda_order})")


def lebesgue_bound(degree: int) -> arb:
    require(degree >= 0, "negative interpolation degree")
    return 1 + 2 * arb(degree + 1).log() / arb.pi()


def ellipse_axes(rho: arb) -> tuple[arb, arb]:
    require(rho.lower() > 1, "Bernstein ellipse radius must exceed one")
    return (rho + 1 / rho) / 2, (rho - 1 / rho) / 2


def overlap_majorant(
    minimum_lambda_real: arb,
    *,
    complex_d: bool,
    rho_d: arb,
) -> dict[str, arb]:
    require(minimum_lambda_real.lower() > 0,
            "analytic ellipse reaches Re(lambda) <= 0")
    if complex_d:
        maximum_d = arb(1) / 450
        real_semiaxis, imag_semiaxis = ellipse_axes(rho_d)
        d_real_minimum = maximum_d * (1 - real_semiaxis) / 2
        d_imag_maximum = maximum_d * imag_semiaxis / 2
        exp_one = (-d_real_minimum).exp()
        exp_four = (-4 * d_real_minimum).exp()
        imaginary_velocity = exp_one * d_imag_maximum / 2 + exp_four * d_imag_maximum
        denominator = 2 * minimum_lambda_real - imaginary_velocity
        velocity_xx = exp_one / 2 + exp_four
        velocity_x = exp_one / 2 + exp_four / 2
    else:
        d_real_minimum = arb(0)
        d_imag_maximum = arb(0)
        imaginary_velocity = arb(0)
        denominator = 2 * minimum_lambda_real
        velocity_xx = arb(3) / 2
        velocity_x = arb(1)
    require(denominator.lower() > 0, "analytic ellipse reaches a Rayleigh pole")
    potential = arb(1) / 4 + velocity_xx / denominator
    root_potential = potential.sqrt()
    fundamental = (2 * arb.pi() * root_potential).exp()
    scaled_solution = fundamental * (1 + fundamental)
    phi = scaled_solution / root_potential
    phi_x = scaled_solution
    anchor = fundamental / root_potential
    numerator = 2 * arb.pi() * velocity_xx * phi ** 2 / denominator ** 2
    right_energy = 2 * arb.pi() * (phi_x ** 2 + phi ** 2 / 4)
    left_potential = phi / denominator
    left_potential_x = (
        phi_x / denominator + phi * velocity_x / denominator ** 2
    )
    left_energy = 2 * arb.pi() * (
        left_potential_x ** 2 + left_potential ** 2 / 4
    )
    return {
        "minimumLambdaReal": minimum_lambda_real,
        "dRealMinimum": d_real_minimum,
        "dImagMaximum": d_imag_maximum,
        "imaginaryVelocityUpper": imaginary_velocity,
        "denominatorLower": denominator,
        "velocityXXUpper": velocity_xx,
        "velocityXUpper": velocity_x,
        "potentialUpper": potential,
        "fundamentalUpper": fundamental,
        "scaledSolutionUpper": scaled_solution,
        "anchor": anchor,
        "numerator": numerator,
        "rightEnergy": right_energy,
        "leftEnergy": left_energy,
    }


def interpolation_error(majorant: arb, degree: int, rho: arb) -> arb:
    require(majorant.lower() >= 0 and degree >= 0 and rho.lower() > 1,
            "invalid interpolation error input")
    return 4 * majorant * rho ** (-degree) / (rho - 1)


def independent_analytic_bounds(config: dict[str, Any]) -> dict[str, Any]:
    rho_d = arb_fraction(parse_fraction(config["rhoD"], "rhoD"))
    rho_lambda = arb_fraction(parse_fraction(config["rhoLambda"], "rhoLambda"))
    limit = arb_fraction(parse_fraction(config["lebesgueLimit"], "lebesgueLimit"))
    d_lebesgue = lebesgue_bound(config["degreeD"])
    lambda_lebesgue = lebesgue_bound(config["degreeLambda"])
    require(d_lebesgue.upper() < limit.lower(), "degree-d Lebesgue bound fails")
    require(lambda_lebesgue.upper() < limit.lower(),
            "degree-lambda Lebesgue bound fails")
    d_majorant = overlap_majorant(
        arb(167) / 1000, complex_d=True, rho_d=rho_d
    )
    lambda_axis, _ = ellipse_axes(rho_lambda)
    lambda_minimum = (
        arb_fraction(parse_fraction(config["lambdaCenter"], "lambdaCenter"))
        - arb_fraction(parse_fraction(config["lambdaRadius"], "lambdaRadius"))
        * lambda_axis
    )
    lambda_majorant = overlap_majorant(
        lambda_minimum, complex_d=False, rho_d=rho_d
    )
    errors: dict[str, arb] = {}
    for name in OUTPUT_NAMES:
        d_error = interpolation_error(
            d_majorant[name], config["degreeD"], rho_d
        )
        lambda_error = interpolation_error(
            lambda_majorant[name], config["degreeLambda"], rho_lambda
        )
        errors[name] = lambda_error + limit * d_error
    return {
        "rhoD": rho_d,
        "rhoLambda": rho_lambda,
        "dLebesgue": d_lebesgue,
        "lambdaLebesgue": lambda_lebesgue,
        "configuredLebesgueLimit": limit,
        "complexD": d_majorant,
        "complexLambda": lambda_majorant,
        "errors": errors,
    }


def inflate_complex(value: acb, error: arb) -> acb:
    require(error.lower() >= 0, "negative enclosure error")
    return acb(
        arb(value.real.mid(), value.real.rad() + error),
        arb(value.imag.mid(), value.imag.rad() + error),
    )


def derivative_majorants(
    coefficients: Sequence[Sequence[acb]],
) -> tuple[arb, arb]:
    d_derivative = arb(0)
    lambda_derivative = arb(0)
    for d_order, row in enumerate(coefficients):
        for lambda_order, coefficient in enumerate(row):
            modulus = coefficient.abs_upper()
            d_derivative += modulus * d_order ** 2
            lambda_derivative += modulus * lambda_order ** 2
    return d_derivative, lambda_derivative


def dyadic_cell(index: int, depth: int) -> tuple[Fraction, Fraction, Fraction]:
    require(depth >= 0 and 0 <= index < 2 ** depth, "invalid dyadic cell")
    count = 2 ** depth
    lower = Fraction(-1) + Fraction(2 * index, count)
    upper = Fraction(-1) + Fraction(2 * (index + 1), count)
    center = (lower + upper) / 2
    return lower, center, upper


def cell_decision(boxes: dict[str, acb], label: str) -> dict[str, arb]:
    anchor_lower = boxes["anchor"].abs_lower()
    numerator_lower = boxes["numerator"].abs_lower()
    right_lower = boxes["rightEnergy"].real.lower()
    left_lower = boxes["leftEnergy"].real.lower()
    right_upper = boxes["rightEnergy"].real.upper()
    left_upper = boxes["leftEnergy"].real.upper()
    require(anchor_lower.lower() > 0, f"anchor enclosure contains zero: {label}")
    require(numerator_lower.lower() > 0, f"numerator enclosure contains zero: {label}")
    require(right_lower.lower() > 0, f"right energy is not positive: {label}")
    require(left_lower.lower() > 0, f"left energy is not positive: {label}")
    overlap_lower = numerator_lower / (right_upper * left_upper).sqrt()
    require(overlap_lower.lower() > arb(1) / 2,
            f"normalized overlap misses one-half: {label}")
    return {
        "anchorLower": anchor_lower,
        "numeratorLower": numerator_lower,
        "rightEnergyLower": right_lower,
        "leftEnergyLower": left_lower,
        "rightEnergyUpper": right_upper,
        "leftEnergyUpper": left_upper,
        "overlapLower": overlap_lower,
        "overlapMargin": overlap_lower - arb(1) / 2,
    }


def independent_lipschitz_cover(
    coefficients_by_name: dict[str, list[list[acb]]],
    errors: dict[str, arb],
    config: dict[str, Any],
) -> dict[str, Any]:
    d_depth = config["subdivision"]["dDepth"]
    lambda_depth = config["subdivision"]["lambdaDepth"]
    derivative_bounds = {
        name: derivative_majorants(coefficients_by_name[name])
        for name in OUTPUT_NAMES
    }
    d_radius = arb(1) / (2 ** d_depth)
    lambda_radius = arb(1) / (2 ** lambda_depth)
    cells: list[dict[str, Any]] = []
    decision_balls: dict[str, list[arb]] = {
        "anchorLower": [], "numeratorLower": [], "rightEnergyLower": [],
        "leftEnergyLower": [], "overlapLower": [], "overlapMargin": [],
    }
    worst_indices: dict[str, tuple[int, int]] = {}
    for d_index in range(2 ** d_depth):
        _, d_center, _ = dyadic_cell(d_index, d_depth)
        for lambda_index in range(2 ** lambda_depth):
            _, lambda_center, _ = dyadic_cell(lambda_index, lambda_depth)
            boxes: dict[str, acb] = {}
            local_errors: dict[str, arb] = {}
            for name in OUTPUT_NAMES:
                d_derivative, lambda_derivative = derivative_bounds[name]
                local_error = (
                    d_radius * d_derivative
                    + lambda_radius * lambda_derivative
                    + errors[name]
                )
                local_errors[name] = local_error
                boxes[name] = inflate_complex(
                    evaluate_tensor(
                        coefficients_by_name[name],
                        arb_fraction(d_center),
                        arb_fraction(lambda_center),
                    ),
                    local_error,
                )
            label = f"d={d_index}/{2**d_depth},lambda={lambda_index}/{2**lambda_depth}"
            decision = cell_decision(boxes, label)
            for key in decision_balls:
                decision_balls[key].append(decision[key])
            cells.append({
                "dIndex": d_index,
                "lambdaIndex": lambda_index,
                "dDepth": d_depth,
                "lambdaDepth": lambda_depth,
                "normalizedD": {
                    "lower": fraction_text(dyadic_cell(d_index, d_depth)[0]),
                    "center": fraction_text(d_center),
                    "upper": fraction_text(dyadic_cell(d_index, d_depth)[2]),
                },
                "normalizedLambda": {
                    "lower": fraction_text(dyadic_cell(lambda_index, lambda_depth)[0]),
                    "center": fraction_text(lambda_center),
                    "upper": fraction_text(dyadic_cell(lambda_index, lambda_depth)[2]),
                },
                "boxes": {name: acb_record(boxes[name]) for name in OUTPUT_NAMES},
                "localLipschitzPlusInterpolationError": {
                    name: arb_text(local_errors[name]) for name in OUTPUT_NAMES
                },
                "anchorAbsoluteLower": arb_text(decision["anchorLower"]),
                "numeratorAbsoluteLower": arb_text(decision["numeratorLower"]),
                "rightEnergyLower": arb_text(decision["rightEnergyLower"]),
                "leftEnergyLower": arb_text(decision["leftEnergyLower"]),
                "overlapLower": arb_text(decision["overlapLower"]),
                "overlapMarginAboveOneHalf": arb_text(decision["overlapMargin"]),
            })
    minima: dict[str, arb] = {}
    for key, values in decision_balls.items():
        minimum = choose_minimum(values, key)
        minima[key] = minimum
        minimum_index = min(range(len(values)), key=lambda index: values[index].lower())
        cell = cells[minimum_index]
        worst_indices[key] = (cell["dIndex"], cell["lambdaIndex"])
    covered_area = (
        Fraction(2, 2 ** d_depth)
        * Fraction(2, 2 ** lambda_depth)
        * len(cells)
    )
    require(len(cells) == 2 ** (d_depth + lambda_depth),
            "independent dyadic cover has the wrong cell count")
    require(covered_area == 4,
            "independent dyadic cells do not cover the full normalized rectangle")
    return {
        "method": (
            "exact dyadic cell-centre evaluation of the direct-DCT tensor "
            "interpolant, inflated by h_d*sum|c_jk|j^2 + "
            "h_lambda*sum|c_jk|k^2 and the analytic tensor remainder"
        ),
        "derivativeInequality": "|T_n'(t)| <= n^2 for -1 <= t <= 1",
        "exactCoveredNormalizedArea": fraction_text(covered_area),
        "cellCount": len(cells),
        "dDepth": d_depth,
        "lambdaDepth": lambda_depth,
        "dCellRadius": arb_text(d_radius),
        "lambdaCellRadius": arb_text(lambda_radius),
        "derivativeBounds": {
            name: {
                "d": arb_text(derivative_bounds[name][0]),
                "lambda": arb_text(derivative_bounds[name][1]),
            }
            for name in OUTPUT_NAMES
        },
        "minima": {key: arb_text(value) for key, value in minima.items()},
        "worstCellIndices": {
            key: {"dIndex": index[0], "lambdaIndex": index[1]}
            for key, index in worst_indices.items()
        },
        "cells": cells,
        "_minimumBalls": minima,
        "_worstIndices": worst_indices,
    }


def chebyshev_power_basis(degree: int) -> list[list[int]]:
    result: list[list[int]] = [[1]]
    if degree >= 1:
        result.append([0, 1])
    for order in range(2, degree + 1):
        row = [0] * (order + 1)
        for index, coefficient in enumerate(result[-1]):
            row[index + 1] += 2 * coefficient
        for index, coefficient in enumerate(result[-2]):
            row[index] -= coefficient
        result.append(row)
    return result


def chebyshev_to_power(coefficients: Sequence[acb]) -> list[acb]:
    degree = len(coefficients) - 1
    basis = chebyshev_power_basis(degree)
    result = [acb(0) for _ in range(degree + 1)]
    for order, coefficient in enumerate(coefficients):
        for power, integer in enumerate(basis[order]):
            result[power] += integer * coefficient
    return result


def power_to_bernstein_minus_one_one(
    coefficients: Sequence[acb],
) -> list[acb]:
    degree = len(coefficients) - 1
    mapped = [acb(0) for _ in range(degree + 1)]
    for power, coefficient in enumerate(coefficients):
        for mapped_power in range(power + 1):
            mapped[mapped_power] += (
                coefficient * math.comb(power, mapped_power)
                * 2 ** mapped_power * (-1) ** (power - mapped_power)
            )
    result = [acb(0) for _ in range(degree + 1)]
    for bernstein_index in range(degree + 1):
        for power in range(bernstein_index + 1):
            result[bernstein_index] += (
                mapped[power] * math.comb(bernstein_index, power)
                / math.comb(degree, power)
            )
    return result


def chebyshev_to_bernstein(coefficients: Sequence[acb]) -> list[acb]:
    return power_to_bernstein_minus_one_one(chebyshev_to_power(coefficients))


def tensor_chebyshev_to_bernstein(
    coefficients: Sequence[Sequence[acb]],
) -> list[list[acb]]:
    d_count = len(coefficients)
    lambda_count = len(coefficients[0])
    after_d = [[acb(0) for _ in range(lambda_count)] for _ in range(d_count)]
    for lambda_order in range(lambda_count):
        column = chebyshev_to_bernstein(
            [coefficients[d_order][lambda_order] for d_order in range(d_count)]
        )
        for d_index in range(d_count):
            after_d[d_index][lambda_order] = column[d_index]
    return [chebyshev_to_bernstein(row) for row in after_d]


def split_bernstein_half(
    coefficients: Sequence[acb],
) -> tuple[list[acb], list[acb]]:
    row = list(coefficients)
    left = [row[0]]
    right = [row[-1]]
    while len(row) > 1:
        row = [(row[index] + row[index + 1]) / 2
               for index in range(len(row) - 1)]
        left.append(row[0])
        right.append(row[-1])
    right.reverse()
    return left, right


def split_tensor_axis(
    coefficients: Sequence[Sequence[acb]],
    axis: int,
) -> tuple[list[list[acb]], list[list[acb]]]:
    d_count = len(coefficients)
    lambda_count = len(coefficients[0])
    if axis == 1:
        left: list[list[acb]] = []
        right: list[list[acb]] = []
        for row in coefficients:
            first, second = split_bernstein_half(row)
            left.append(first)
            right.append(second)
        return left, right
    require(axis == 0, "tensor subdivision axis must be zero or one")
    left = [[acb(0) for _ in range(lambda_count)] for _ in range(d_count)]
    right = [[acb(0) for _ in range(lambda_count)] for _ in range(d_count)]
    for lambda_index in range(lambda_count):
        first, second = split_bernstein_half(
            [coefficients[d_index][lambda_index] for d_index in range(d_count)]
        )
        for d_index in range(d_count):
            left[d_index][lambda_index] = first[d_index]
            right[d_index][lambda_index] = second[d_index]
    return left, right


def subdivide_tensor(
    coefficients: Sequence[Sequence[acb]],
    d_depth: int,
    lambda_depth: int,
) -> list[tuple[int, int, list[list[acb]]]]:
    pieces: list[tuple[int, int, list[list[acb]]]] = [
        (0, 0, [list(row) for row in coefficients])
    ]
    for _ in range(d_depth):
        refined: list[tuple[int, int, list[list[acb]]]] = []
        for d_index, lambda_index, piece in pieces:
            first, second = split_tensor_axis(piece, 0)
            refined.append((2 * d_index, lambda_index, first))
            refined.append((2 * d_index + 1, lambda_index, second))
        pieces = refined
    for _ in range(lambda_depth):
        refined = []
        for d_index, lambda_index, piece in pieces:
            first, second = split_tensor_axis(piece, 1)
            refined.append((d_index, 2 * lambda_index, first))
            refined.append((d_index, 2 * lambda_index + 1, second))
        pieces = refined
    return sorted(pieces, key=lambda item: (item[0], item[1]))


def tensor_hull(coefficients: Sequence[Sequence[acb]]) -> acb:
    flattened = [value for row in coefficients for value in row]
    require(bool(flattened), "cannot hull empty Bernstein tensor")
    real = flattened[0].real
    imag = flattened[0].imag
    for value in flattened[1:]:
        real = real.union(value.real)
        imag = imag.union(value.imag)
    return acb(real, imag)


def midpoint_coefficients(
    coefficients: Sequence[Sequence[acb]],
) -> tuple[list[list[acb]], arb]:
    midpoint: list[list[acb]] = []
    residual = arb(0)
    for row in coefficients:
        midpoint_row: list[acb] = []
        for coefficient in row:
            center = acb(coefficient.real.mid(), coefficient.imag.mid())
            midpoint_row.append(center)
            residual += (coefficient - center).abs_upper()
        midpoint.append(midpoint_row)
    return midpoint, residual


def build_primary_replay(
    staged_coefficients: dict[str, list[list[acb]]],
    errors: dict[str, arb],
    config: dict[str, Any],
) -> dict[str, Any]:
    d_depth = config["subdivision"]["dDepth"]
    lambda_depth = config["subdivision"]["lambdaDepth"]
    cells_by_name: dict[str, dict[tuple[int, int], acb]] = {}
    residuals: dict[str, arb] = {}
    for name in OUTPUT_NAMES:
        midpoint, residual = midpoint_coefficients(staged_coefficients[name])
        residuals[name] = residual
        bernstein = tensor_chebyshev_to_bernstein(midpoint)
        cells_by_name[name] = {}
        for d_index, lambda_index, piece in subdivide_tensor(
            bernstein, d_depth, lambda_depth
        ):
            cells_by_name[name][(d_index, lambda_index)] = inflate_complex(
                tensor_hull(piece), errors[name] + residual
            )
    return {"cells": cells_by_name, "residuals": residuals}


def require_ball_contains(reported: arb, replayed: arb, label: str) -> None:
    require(reported.contains(replayed),
            f"reported primary ball does not contain independent replay: {label}")


def require_complex_contains(reported: acb, replayed: acb, label: str) -> None:
    require_ball_contains(reported.real, replayed.real, f"{label}.real")
    require_ball_contains(reported.imag, replayed.imag, f"{label}.imag")


def require_reported_ball_agrees(reported_value: Any, replayed: arb, label: str) -> arb:
    reported = parse_arb(reported_value, label)
    require_ball_contains(reported, replayed, label)
    return reported


def validate_prerequisite(evidence_value: Any) -> dict[str, Any]:
    evidence = expect_keys(evidence_value, (
        "path", "bytes", "sha256", "schemaVersion", "sourceDigest",
        "verifiedDecisions",
    ), "certificate.prerequisiteEvidence")
    require(evidence["path"] == "experiments/r073j/contour_certificate.json",
            "unexpected prerequisite path")
    path = ROOT / evidence["path"]
    data = path.read_bytes()
    require(expect_int(evidence["bytes"], "prerequisite.bytes", 0) == len(data),
            "prerequisite byte count mismatch")
    actual_hash = sha256_bytes(data)
    require(evidence["sha256"] == actual_hash, "prerequisite SHA-256 mismatch")
    prerequisite = json.loads(data)
    require(prerequisite.get("schemaVersion") == evidence["schemaVersion"],
            "prerequisite schema mismatch")
    require(prerequisite.get("sourceDigest") == evidence["sourceDigest"],
            "prerequisite source digest mismatch")
    require(prerequisite.get("status") == "passed",
            "prerequisite contour certificate did not pass")
    required_decisions = {
        "globalBasePositiveOrientationWinding": 1,
        "globalBoundaryNonzeroForAllD": True,
        "localBasePositiveOrientationWinding": 1,
        "localBoundaryNonzeroForAllD": True,
    }
    require(evidence["verifiedDecisions"] == required_decisions,
            "recorded prerequisite decisions mismatch")
    decisions = prerequisite.get("decisions", {})
    require(all(decisions.get(key) == value
                for key, value in required_decisions.items()),
            "live prerequisite decisions are incomplete")
    return {
        "path": evidence["path"],
        "bytes": len(data),
        "sha256": actual_hash,
        "schemaVersion": prerequisite["schemaVersion"],
        "sourceDigest": prerequisite["sourceDigest"],
        "verifiedDecisions": required_decisions,
    }


def compare_majorant_record(
    reported_value: Any,
    replayed: dict[str, arb],
    label: str,
) -> None:
    reported = expect_keys(reported_value, replayed.keys(), label)
    for key, value in replayed.items():
        require_reported_ball_agrees(reported[key], value, f"{label}.{key}")


def validate_primary_certificate(
    certificate: Any,
    checkpoint: dict[str, Any],
    config: dict[str, Any],
    checkpoint_audit: dict[str, Any],
    analytic: dict[str, Any],
    primary_replay: dict[str, Any],
) -> dict[str, Any]:
    certificate = expect_keys(certificate, (
        "schemaVersion", "status", "completedAt", "sourceLedger",
        "sourceDigest", "gridEvidence", "analysisEvidence", "configuration",
        "prerequisiteEvidence", "arithmetic", "analyticMajorants",
        "decisions", "cells",
    ), "certificate")
    require(certificate["schemaVersion"] == PRIMARY_SCHEMA,
            "primary certificate schema mismatch")
    require(certificate["status"] == "passed", "primary certificate did not pass")
    expect_string(certificate["completedAt"], "certificate.completedAt")
    require(certificate["configuration"] == config,
            "primary certificate/config mismatch")
    combined_paths = GRID_SOURCE_PATHS + ANALYSIS_SOURCE_PATHS
    combined_source = validate_ledger(
        certificate["sourceLedger"], certificate["sourceDigest"],
        combined_paths, "certificate.sourceLedger",
    )

    grid_evidence = expect_keys(certificate["gridEvidence"], (
        "checkpoint", "sourceLedger", "sourceDigest", "status",
    ), "certificate.gridEvidence")
    require(grid_evidence["checkpoint"] ==
            "experiments/r073j/overlap_grid_checkpoint.json",
            "primary grid checkpoint path mismatch")
    require(grid_evidence["sourceLedger"] == checkpoint["sourceLedger"]
            and grid_evidence["sourceDigest"] == checkpoint["sourceDigest"]
            and grid_evidence["status"] == checkpoint["status"],
            "primary grid evidence mismatch")
    analysis_evidence = expect_keys(certificate["analysisEvidence"],
                                    ("sourceLedger", "sourceDigest"),
                                    "certificate.analysisEvidence")
    analysis_source = validate_ledger(
        analysis_evidence["sourceLedger"], analysis_evidence["sourceDigest"],
        ANALYSIS_SOURCE_PATHS, "certificate.analysisEvidence.sourceLedger",
    )
    require(certificate["sourceLedger"] ==
            checkpoint["sourceLedger"] + analysis_evidence["sourceLedger"],
            "combined primary ledger is not grid ledger plus analysis ledger")

    arithmetic = expect_keys(certificate["arithmetic"], (
        "engine", "python", "pythonImplementation", "precisionDecimalDigits",
        "pointCount", "minimumRayleighDenominatorLower",
        "minimumPicardComponentSlack", "maximumPicardInflationAttempt",
    ), "certificate.arithmetic")
    require(arithmetic["pointCount"] == 841
            and arithmetic["precisionDecimalDigits"] == 80,
            "primary arithmetic grid/precision mismatch")
    require(arithmetic["maximumPicardInflationAttempt"] ==
            checkpoint_audit["maximumAttempt"],
            "primary maximum Picard attempt mismatch")
    require_reported_ball_agrees(
        arithmetic["minimumRayleighDenominatorLower"],
        checkpoint_audit["minimumDenominator"],
        "certificate.arithmetic.minimumRayleighDenominatorLower",
    )
    require_reported_ball_agrees(
        arithmetic["minimumPicardComponentSlack"],
        checkpoint_audit["minimumSlack"],
        "certificate.arithmetic.minimumPicardComponentSlack",
    )

    majorants = expect_keys(certificate["analyticMajorants"], (
        "complexD", "complexLambda", "totalInterpolationErrors",
        "coefficientResidualModulusUpper", "remainderFormula", "rangeMethod",
    ), "certificate.analyticMajorants")
    compare_majorant_record(majorants["complexD"], analytic["complexD"],
                            "certificate.analyticMajorants.complexD")
    compare_majorant_record(majorants["complexLambda"], analytic["complexLambda"],
                            "certificate.analyticMajorants.complexLambda")
    reported_errors = expect_keys(majorants["totalInterpolationErrors"],
                                  OUTPUT_NAMES,
                                  "certificate.totalInterpolationErrors")
    reported_residuals = expect_keys(majorants["coefficientResidualModulusUpper"],
                                     OUTPUT_NAMES,
                                     "certificate.coefficientResiduals")
    for name in OUTPUT_NAMES:
        require_reported_ball_agrees(
            reported_errors[name], analytic["errors"][name],
            f"certificate.totalInterpolationErrors.{name}",
        )
        require_reported_ball_agrees(
            reported_residuals[name], primary_replay["residuals"][name],
            f"certificate.coefficientResiduals.{name}",
        )
    require(majorants["remainderFormula"] ==
            "epsilon_lambda + Lambda_lambda*epsilon_d",
            "primary remainder formula mismatch")
    require("midpoint coefficients" in majorants["rangeMethod"],
            "primary range method is not the expected midpoint method")

    cells_value = certificate["cells"]
    require(type(cells_value) is list and len(cells_value) == 128,
            "primary certificate must contain 128 cells")
    seen: set[tuple[int, int]] = set()
    cell_audits: list[dict[str, Any]] = []
    primary_minima = {
        "anchor": [], "overlap": [], "rightEnergy": [], "leftEnergy": []
    }
    for cell_index, cell_value in enumerate(cells_value):
        label = f"certificate.cells[{cell_index}]"
        cell = expect_keys(cell_value, (
            "dIndex", "lambdaIndex", "dDepth", "lambdaDepth", "anchor",
            "numerator", "rightEnergy", "leftEnergy", "anchorAbsoluteLower",
            "overlapLower",
        ), label)
        d_index = expect_int(cell["dIndex"], f"{label}.dIndex", 0)
        lambda_index = expect_int(cell["lambdaIndex"], f"{label}.lambdaIndex", 0)
        require(d_index < 8 and lambda_index < 16,
                f"primary cell index out of range: {label}")
        require(cell["dDepth"] == 3 and cell["lambdaDepth"] == 4,
                f"primary cell depth mismatch: {label}")
        key = (d_index, lambda_index)
        require(key not in seen, f"duplicate primary cell {key}")
        seen.add(key)
        reported_boxes = {
            name: parse_acb_record(cell[name], f"{label}.{name}")
            for name in OUTPUT_NAMES
        }
        replayed_boxes = {
            name: primary_replay["cells"][name][key] for name in OUTPUT_NAMES
        }
        for name in OUTPUT_NAMES:
            require_complex_contains(
                reported_boxes[name], replayed_boxes[name], f"{label}.{name}"
            )
        reported_decision = cell_decision(reported_boxes, label)
        replayed_decision = cell_decision(replayed_boxes, f"primary replay {key}")
        # The serialized component boxes intentionally print their radii with
        # few significant digits, so re-deriving a sharp margin from a parsed
        # box is much coarser than the separately serialized margin.  Audit the
        # latter directly against the full-precision replay instead.
        recorded_anchor = parse_arb(
            cell["anchorAbsoluteLower"], f"{label}.anchorAbsoluteLower"
        )
        recorded_overlap = parse_arb(
            cell["overlapLower"], f"{label}.overlapLower"
        )
        require(recorded_anchor.contains(replayed_decision["anchorLower"]),
                f"recorded/replayed anchor margin mismatch: {label}")
        require(recorded_overlap.contains(replayed_decision["overlapLower"]),
                f"recorded/replayed overlap margin mismatch: {label}")
        primary_minima["anchor"].append(replayed_decision["anchorLower"])
        primary_minima["overlap"].append(replayed_decision["overlapLower"])
        primary_minima["rightEnergy"].append(replayed_decision["rightEnergyLower"])
        primary_minima["leftEnergy"].append(replayed_decision["leftEnergyLower"])
        cell_audits.append({
            "dIndex": d_index,
            "lambdaIndex": lambda_index,
            "reportedBoxesContainIndependentReplay": True,
            "reportedMarginsContainIndependentReplay": True,
            "reportedAnchorAbsoluteLower": arb_text(recorded_anchor),
            "replayedAnchorAbsoluteLower": arb_text(replayed_decision["anchorLower"]),
            "reportedOverlapLower": arb_text(recorded_overlap),
            "replayedOverlapLower": arb_text(replayed_decision["overlapLower"]),
        })
    require(seen == {(d_index, lambda_index)
                     for d_index in range(8) for lambda_index in range(16)},
            "primary cell cover is incomplete")

    decisions = expect_keys(certificate["decisions"], (
        "auxiliaryRectangleKineticQuotientAtLeastOneHalf",
        "auxiliaryRectanglePhaseAnchorNonzero", "conditionalBranchImplications",
        "minimumAnchorAbsoluteLower", "minimumKineticOverlapLower",
        "minimumLeftEnergyLower", "minimumRightEnergyLower",
    ), "certificate.decisions")
    require(decisions["auxiliaryRectangleKineticQuotientAtLeastOneHalf"] is True
            and decisions["auxiliaryRectanglePhaseAnchorNonzero"] is True,
            "primary Boolean decisions are false")
    conditional = expect_keys(decisions["conditionalBranchImplications"], (
        "conditionalOn", "kineticOverlapAtLeastOneHalfAlongBranch",
        "phaseAnchorNonzeroAlongBranch",
    ), "certificate.decisions.conditionalBranchImplications")
    require(conditional["kineticOverlapAtLeastOneHalfAlongBranch"] is True
            and conditional["phaseAnchorNonzeroAlongBranch"] is True
            and isinstance(conditional["conditionalOn"], str)
            and "J8" in conditional["conditionalOn"],
            "primary branch implication is not explicitly conditional on J8")
    reported_decision_minima = {
        "minimumAnchorAbsoluteLower": choose_minimum(primary_minima["anchor"], "primary anchor"),
        "minimumKineticOverlapLower": choose_minimum(primary_minima["overlap"], "primary overlap"),
        "minimumRightEnergyLower": choose_minimum(primary_minima["rightEnergy"], "primary right energy"),
        "minimumLeftEnergyLower": choose_minimum(primary_minima["leftEnergy"], "primary left energy"),
    }
    for key, replayed in reported_decision_minima.items():
        require_reported_ball_agrees(decisions[key], replayed,
                                     f"certificate.decisions.{key}")

    prerequisite = validate_prerequisite(certificate["prerequisiteEvidence"])
    return {
        "combinedSource": combined_source,
        "analysisSource": analysis_source,
        "prerequisite": prerequisite,
        "cellCount": len(cell_audits),
        "exactNormalizedCoverArea": "4/1",
        "allReportedBoxesContainReplay": True,
        "allReportedMarginsContainReplay": True,
        "cellAudits": cell_audits,
        "decisionMinima": {
            key: arb_text(value) for key, value in reported_decision_minima.items()
        },
    }


def physical_box(d_index: int, lambda_index: int) -> dict[str, Any]:
    d_depth = EXPECTED_CONFIG["subdivision"]["dDepth"]
    lambda_depth = EXPECTED_CONFIG["subdivision"]["lambdaDepth"]
    d_count = 2 ** d_depth
    lambda_count = 2 ** lambda_depth
    d_maximum = Fraction(1, 450)
    lambda_center = Fraction(17, 100)
    lambda_radius = Fraction(3, 1000)
    d_lower = d_maximum * Fraction(d_index, d_count)
    d_upper = d_maximum * Fraction(d_index + 1, d_count)
    lambda_lower = (
        lambda_center - lambda_radius
        + 2 * lambda_radius * Fraction(lambda_index, lambda_count)
    )
    lambda_upper = (
        lambda_center - lambda_radius
        + 2 * lambda_radius * Fraction(lambda_index + 1, lambda_count)
    )
    return {
        "dIndex": d_index,
        "lambdaIndex": lambda_index,
        "d": {"lower": fraction_text(d_lower), "upper": fraction_text(d_upper)},
        "lambda": {
            "lower": fraction_text(lambda_lower),
            "upper": fraction_text(lambda_upper),
        },
    }


def direct_ode_spot_plan(worst_indices: dict[str, tuple[int, int]]) -> dict[str, Any]:
    requested = [
        worst_indices["overlapMargin"],
        worst_indices["anchorLower"],
        (0, 0),
        (7, 15),
        (3, 7),
    ]
    unique: list[tuple[int, int]] = []
    for item in requested:
        if item not in unique:
            unique.append(item)
    return {
        "status": "not-executed-in-this-audit",
        "purpose": (
            "later test the ODE/node-generation layer that is shared by the "
            "primary and this post-processing audit"
        ),
        "method": (
            "write a separate interval Taylor integrator with no primary imports; "
            "integrate the plus/minus Rayleigh systems and four accumulated "
            "outputs directly over each listed natural (d,lambda) box, bisecting "
            "until Picard tubes and the local overlap inequality are decisive"
        ),
        "minimumNumericalContract": {
            "precisionDecimalDigits": 100,
            "TaylorOrderAtLeast": 14,
            "periodStepsAtLeast": 1024,
            "requiredCrossChecks": [
                "fresh denominator and Picard-slack audit",
                "direct anchor, numerator, right-energy and left-energy boxes",
                "agreement with the frozen grid/interpolant on overlapping points",
            ],
        },
        "naturalParameterBoxes": [physical_box(*item) for item in unique],
    }


def strip_private(value: dict[str, Any]) -> dict[str, Any]:
    return {key: item for key, item in value.items() if not key.startswith("_")}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path,
                        default=HERE / "overlap_config.json")
    parser.add_argument("--checkpoint", type=Path,
                        default=HERE / "overlap_grid_checkpoint.json")
    parser.add_argument("--certificate", type=Path,
                        default=HERE / "overlap_certificate.json")
    parser.add_argument("--output", type=Path,
                        default=HERE / "independent_overlap_validation.json")
    parser.add_argument("--log", type=Path,
                        default=HERE / "independent_overlap_validation.ndjson")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    started = time.monotonic()
    start_log(args.log, {
        "time": utc_now(),
        "event": "independent-overlap-audit-started",
        "checkpoint": str(args.checkpoint.relative_to(ROOT)),
        "certificate": str(args.certificate.relative_to(ROOT)),
    })
    try:
        config = validate_config(json.loads(args.config.read_text(encoding="utf-8")))
        ctx.dps = config["dps"]
        checkpoint = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        checkpoint_audit = validate_checkpoint(checkpoint, config)
        emit(args.log, "frozen-grid-validated", pointCount=841,
             minimumDenominatorLower=arb_text(checkpoint_audit["minimumDenominator"]),
             minimumPicardSlack=arb_text(checkpoint_audit["minimumSlack"]),
             maximumPicardAttempt=checkpoint_audit["maximumAttempt"])

        direct_coefficients: dict[str, list[list[acb]]] = {}
        staged_coefficients: dict[str, list[list[acb]]] = {}
        reconstruction_count = 0
        for name in OUTPUT_NAMES:
            direct = direct_tensor_dct(checkpoint_audit["grids"][name])
            staged = staged_tensor_dct_replay(checkpoint_audit["grids"][name])
            coefficients_overlap(direct, staged, name)
            checked = verify_direct_dct(direct, checkpoint_audit["grids"][name], name)
            reconstruction_count += checked
            direct_coefficients[name] = direct
            staged_coefficients[name] = staged
            emit(args.log, "direct-dct-output-validated", outputName=name,
                 nodeReconstructions=checked)

        analytic = independent_analytic_bounds(config)
        independent_cover = independent_lipschitz_cover(
            direct_coefficients, analytic["errors"], config
        )
        emit(args.log, "independent-lipschitz-cover-passed",
             cellCount=independent_cover["cellCount"],
             minimumAnchorAbsoluteLower=independent_cover["minima"]["anchorLower"],
             minimumKineticOverlapLower=independent_cover["minima"]["overlapLower"],
             minimumMarginAboveOneHalf=independent_cover["minima"]["overlapMargin"])

        primary_replay = build_primary_replay(
            staged_coefficients, analytic["errors"], config
        )
        certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
        primary_audit = validate_primary_certificate(
            certificate, checkpoint, config, checkpoint_audit, analytic, primary_replay
        )
        emit(args.log, "primary-midpoint-bernstein-cells-audited",
             cellCount=primary_audit["cellCount"],
             prerequisiteSha256=primary_audit["prerequisite"]["sha256"])

        # Recheck drift-prone ledgers and prerequisite after all arithmetic.
        validate_checkpoint(
            json.loads(args.checkpoint.read_text(encoding="utf-8")), config
        )
        validate_prerequisite(certificate["prerequisiteEvidence"])
        validate_ledger(
            certificate["sourceLedger"], certificate["sourceDigest"],
            GRID_SOURCE_PATHS + ANALYSIS_SOURCE_PATHS,
            "certificate.sourceLedger.finalRecheck",
        )

        source_path = Path(__file__).resolve()
        source_bytes = source_path.read_bytes()
        output = {
            "schemaVersion": AUDIT_SCHEMA,
            "status": "passed",
            "completedAt": utc_now(),
            "auditSource": {
                "path": str(source_path.relative_to(ROOT)),
                "bytes": len(source_bytes),
                "sha256": sha256_bytes(source_bytes),
            },
            "configuration": config,
            "environment": {
                "arithmetic": "python-flint Arb/Acb ball arithmetic",
                "flintVersion": getattr(__import__("flint"), "__version__", "unknown"),
                "python": platform.python_version(),
                "pythonImplementation": platform.python_implementation(),
                "platform": platform.platform(),
                "precisionDecimalDigits": config["dps"],
                "elapsedSeconds": time.monotonic() - started,
            },
            "frozenGridAudit": {
                "path": str(args.checkpoint.relative_to(ROOT)),
                "bytes": args.checkpoint.stat().st_size,
                "sha256": sha256_bytes(args.checkpoint.read_bytes()),
                "sourceLedger": checkpoint_audit["source"]["ledger"],
                "sourceDigest": checkpoint_audit["source"]["digest"],
                "shape": [29, 29],
                "pointCount": checkpoint_audit["pointCount"],
                "completeUniqueIndexLattice": True,
                "minimumRayleighDenominatorLower": arb_text(
                    checkpoint_audit["minimumDenominator"]
                ),
                "minimumPicardComponentSlack": arb_text(
                    checkpoint_audit["minimumSlack"]
                ),
                "maximumPicardInflationAttempt": checkpoint_audit["maximumAttempt"],
            },
            "directDctAudit": {
                "method": "direct four-index first-kind-root tensor DCT",
                "outputs": list(OUTPUT_NAMES),
                "rawNodeBallReconstructions": reconstruction_count,
                "expectedReconstructions": 4 * 841,
                "allRawNodeBallsContained": True,
                "allDirectCoefficientsOverlapIndependentStagedReplay": True,
            },
            "analyticAudit": {
                "degreeDLebesgueUpper": arb_text(analytic["dLebesgue"]),
                "degreeLambdaLebesgueUpper": arb_text(analytic["lambdaLebesgue"]),
                "configuredLebesgueLimit": arb_text(
                    analytic["configuredLebesgueLimit"]
                ),
                "complexD": {
                    key: arb_text(value) for key, value in analytic["complexD"].items()
                },
                "complexLambda": {
                    key: arb_text(value)
                    for key, value in analytic["complexLambda"].items()
                },
                "totalInterpolationErrors": {
                    key: arb_text(value) for key, value in analytic["errors"].items()
                },
                "remainderFormula": "epsilon_lambda + Lambda_lambda*epsilon_d",
            },
            "independentLipschitzCertificate": strip_private(independent_cover),
            "primaryCertificateAudit": primary_audit,
            "decisions": {
                "auxiliaryRectanglePhaseAnchorNonzero": True,
                "auxiliaryRectangleRightEnergyPositive": True,
                "auxiliaryRectangleLeftEnergyPositive": True,
                "auxiliaryRectangleKineticQuotientGreaterThanOneHalf": True,
                "minimumAnchorAbsoluteLower": independent_cover["minima"]["anchorLower"],
                "minimumNumeratorAbsoluteLower": independent_cover["minima"]["numeratorLower"],
                "minimumRightEnergyLower": independent_cover["minima"]["rightEnergyLower"],
                "minimumLeftEnergyLower": independent_cover["minima"]["leftEnergyLower"],
                "minimumKineticOverlapLower": independent_cover["minima"]["overlapLower"],
                "minimumStrictMarginAboveOneHalf": independent_cover["minima"]["overlapMargin"],
                "conditionalBranchImplication": {
                    "conditionalOn": (
                        "J8: for every d in [0,1/450], the unique algebraically "
                        "simple real Evans root lies in [167/1000,173/1000]"
                    ),
                    "phaseAnchorNonzeroAlongBranch": True,
                    "kineticOverlapGreaterThanOneHalfAlongBranch": True,
                },
            },
            "independenceBoundary": {
                "classification": "independent-post-processing-from-shared-raw-grid",
                "sharedInputs": [
                    "841 serialized interval ODE output records",
                    "the analytic formulas and frozen domain contract",
                ],
                "independentlyReimplemented": [
                    "strict JSON/config/source-ledger validation",
                    "direct tensor DCT and all-node reconstruction",
                    "Lebesgue, Bernstein-ellipse majorants and tensor remainder",
                    "complete dyadic centre-Lipschitz range proof",
                    "primary midpoint-Bernstein replay and per-cell margin audit",
                    "prerequisite contour-certificate hash and decision checks",
                ],
                "notIndependentlyRecomputed": [
                    "the Rayleigh/overlap interval ODE integrations at the 841 nodes",
                    "the primary node-generation and Picard/Taylor implementation",
                ],
                "limitation": (
                    "A systematic defect in the shared raw ODE grid, node mapping, "
                    "or primary interval integrator would not necessarily be detected "
                    "by this post-processing audit."
                ),
            },
            "futureDirectOdeSpotCheckPlan": direct_ode_spot_plan(
                independent_cover["_worstIndices"]
            ),
        }
        # Replace internal Arb objects by stable strings in the decision record.
        output["decisions"] = {
            key: (arb_text(value) if isinstance(value, arb) else value)
            for key, value in output["decisions"].items()
        }
        atomic_json(args.output, output)
        emit(args.log, "independent-overlap-audit-passed",
             output=str(args.output.relative_to(ROOT)),
             outputSha256=sha256_bytes(args.output.read_bytes()),
             elapsedSeconds=time.monotonic() - started,
             minimumKineticOverlapLower=output["decisions"]["minimumKineticOverlapLower"],
             minimumStrictMarginAboveOneHalf=
             output["decisions"]["minimumStrictMarginAboveOneHalf"])
        print(canonical_json({
            "status": "passed",
            "output": str(args.output.relative_to(ROOT)),
            "log": str(args.log.relative_to(ROOT)),
            "minimumKineticOverlapLower":
                output["decisions"]["minimumKineticOverlapLower"],
            "minimumStrictMarginAboveOneHalf":
                output["decisions"]["minimumStrictMarginAboveOneHalf"],
        }), end="")
    except Exception as error:
        emit(args.log, "independent-overlap-audit-failed",
             errorType=type(error).__name__, error=str(error),
             elapsedSeconds=time.monotonic() - started)
        raise


if __name__ == "__main__":
    main()
