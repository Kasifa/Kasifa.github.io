#!/usr/bin/env python3
"""Independent post-processing audit for the R0.73J contour certificate.

This program intentionally does *not* import the primary interval ODE core,
Chebyshev helpers, or release driver.  It reads their frozen raw grid and
certificate, validates provenance and completeness, and independently
reimplements:

* the two-dimensional first-kind-root Chebyshev transform (as a direct DCT);
* reverse-order (d then s) interval Clenshaw range evaluation on exact
  dyadic covers, independently of the primary s-then-d implementation;
* the analytic ellipse majorants and interpolation remainders;
* base-curve homotopy boxes; and
* exact rational polygon winding.

This is deliberately described as independent *post-processing from a shared
raw grid*.  It neither recomputes the interval monodromy values nor proves that
the serialized values were evaluated at the declared nodes.  The JSON report
records that limitation and a deterministic, unexecuted natural-box spot-check
plan.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import platform
from typing import Any, Iterable, Sequence

import flint
from flint import acb, arb, ctx


ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
GRID_SCHEMA_VERSION = "r073j-parameter-uniform-contours-v1"
CERTIFICATE_SCHEMA_VERSION = "r073j-parameter-uniform-contours-clenshaw-v2"
AUDIT_SCHEMA = "r073j-independent-shared-grid-postprocessing-clenshaw-v2"
GRID_SOURCE_PATHS = (
    "research/r073j_interval_core.py",
    "research/r073j_chebyshev.py",
    "experiments/r073j/certify_contours.py",
    "experiments/r073j/config.json",
    "experiments/r073j/requirements.txt",
)
ANALYSIS_SOURCE_PATHS = ("experiments/r073j/analyze_contours_clenshaw.py",)
CERTIFICATE_SOURCE_PATHS = GRID_SOURCE_PATHS + ANALYSIS_SOURCE_PATHS
EXPECTED_REQUIREMENT = "python-flint==0.6.0\n"
MAX_EXTRA_DYADIC_DEPTH = 4


class AuditFailure(RuntimeError):
    """A fail-closed validation error with a stable human-readable message."""


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
    require(type(value) is str and value != "", f"{label} must be a nonempty string")
    return value


def parse_fraction(value: Any, label: str) -> Fraction:
    text = expect_string(value, label)
    try:
        result = Fraction(text)
    except (ValueError, ZeroDivisionError) as error:
        raise AuditFailure(f"{label} is not an exact rational: {text!r}") from error
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


def balls_overlap(left: arb, right: arb) -> bool:
    return left.overlaps(right)


def complexes_overlap(left: acb, right: acb) -> bool:
    return left.real.overlaps(right.real) and left.imag.overlaps(right.imag)


def require_ball_agreement(reported: Any, computed: arb, label: str) -> arb:
    parsed = parse_arb(reported, label)
    require(balls_overlap(parsed, computed),
            f"{label} does not overlap the independently recomputed ball")
    return parsed


def choose_minimum(values: Sequence[arb], label: str) -> arb:
    require(bool(values), f"empty minimum collection: {label}")
    # Ordering lower endpoints is unambiguous and conservative even if two
    # enclosing balls overlap.  Every decision separately requires positivity.
    return min(values, key=lambda value: value.lower())


def validate_configuration(config: Any) -> dict[str, Any]:
    config = expect_keys(config, (
        "schemaVersion", "dps", "order", "degreeD", "rhoD", "rhoS",
        "lebesgueLimit", "workers", "resourceIntervalSeconds", "global", "local",
    ), "configuration")
    require(config["schemaVersion"] == GRID_SCHEMA_VERSION,
            "configuration schemaVersion mismatch")
    dps = expect_int(config["dps"], "configuration.dps", 50)
    order = expect_int(config["order"], "configuration.order", 2)
    degree_d = expect_int(config["degreeD"], "configuration.degreeD", 1)
    expect_int(config["workers"], "configuration.workers", 1)
    expect_int(config["resourceIntervalSeconds"],
               "configuration.resourceIntervalSeconds", 1)
    rho_d = parse_fraction(config["rhoD"], "configuration.rhoD")
    rho_s = parse_fraction(config["rhoS"], "configuration.rhoS")
    lebesgue = parse_fraction(config["lebesgueLimit"],
                              "configuration.lebesgueLimit")
    require(rho_d > 1 and rho_s > 1, "both Bernstein ellipse radii must exceed one")
    require(lebesgue > 0, "Lebesgue limit must be positive")

    global_config = expect_keys(config["global"], (
        "boundary", "degreeS", "steps", "horizontalPanelsPerEdge",
        "verticalPanelsPerEdge", "subdivision",
    ), "configuration.global")
    boundary = expect_keys(global_config["boundary"], ("left", "outer"),
                           "configuration.global.boundary")
    left = parse_fraction(boundary["left"], "configuration.global.boundary.left")
    outer = parse_fraction(boundary["outer"], "configuration.global.boundary.outer")
    require(0 < left < outer, "global boundary must satisfy 0 < left < outer")
    global_degree = expect_int(global_config["degreeS"],
                               "configuration.global.degreeS", 1)
    global_steps = expect_int(global_config["steps"],
                              "configuration.global.steps", 1)
    expect_int(global_config["horizontalPanelsPerEdge"],
               "configuration.global.horizontalPanelsPerEdge", 1)
    expect_int(global_config["verticalPanelsPerEdge"],
               "configuration.global.verticalPanelsPerEdge", 1)
    global_subdivision = expect_keys(global_config["subdivision"],
                                     ("dDepth", "sDepth"),
                                     "configuration.global.subdivision")
    expect_int(global_subdivision["dDepth"],
               "configuration.global.subdivision.dDepth", 0)
    expect_int(global_subdivision["sDepth"],
               "configuration.global.subdivision.sDepth", 0)

    local_config = expect_keys(config["local"], (
        "degreeS", "steps", "panels", "subdivision",
    ), "configuration.local")
    local_degree = expect_int(local_config["degreeS"],
                              "configuration.local.degreeS", 1)
    local_steps = expect_int(local_config["steps"],
                             "configuration.local.steps", 1)
    expect_int(local_config["panels"], "configuration.local.panels", 3)
    local_subdivision = expect_keys(local_config["subdivision"],
                                    ("dDepth", "sDepth"),
                                    "configuration.local.subdivision")
    expect_int(local_subdivision["dDepth"],
               "configuration.local.subdivision.dDepth", 0)
    expect_int(local_subdivision["sDepth"],
               "configuration.local.subdivision.sDepth", 0)

    require(order < global_steps and order < local_steps,
            "Taylor order must be smaller than both step counts")
    require(degree_d < 100 and global_degree < 100 and local_degree < 100,
            "unexpectedly large degree; audit code requires explicit review")
    require(dps >= 2 * order,
            "configured precision is unexpectedly small relative to Taylor order")
    return config


def line_panel(
    config: dict[str, Any],
    panel_id: str,
    edge: str,
    center_real: Fraction,
    center_imag: Fraction,
    half_real: Fraction,
    half_imag: Fraction,
) -> dict[str, Any]:
    return {
        "id": panel_id,
        "family": "global",
        "kind": "line",
        "edge": edge,
        "centerReal": fraction_text(center_real),
        "centerImag": fraction_text(center_imag),
        "halfReal": fraction_text(half_real),
        "halfImag": fraction_text(half_imag),
        "degreeS": config["global"]["degreeS"],
        "steps": config["global"]["steps"],
    }


def independent_panel_definitions(config: dict[str, Any]) -> list[dict[str, Any]]:
    """Derive the positively oriented contours without calling primary code."""
    left = Fraction(config["global"]["boundary"]["left"])
    outer = Fraction(config["global"]["boundary"]["outer"])
    horizontal_count = config["global"]["horizontalPanelsPerEdge"]
    vertical_count = config["global"]["verticalPanelsPerEdge"]
    dx = (outer - left) / horizontal_count
    dy = 2 * outer / vertical_count
    result: list[dict[str, Any]] = []

    for index in range(horizontal_count):
        x = left + Fraction(2 * index + 1, 2) * dx
        result.append(line_panel(config, f"G-bottom-{index:02d}", "bottom",
                                 x, -outer, dx / 2, Fraction(0)))
    for index in range(vertical_count):
        y = -outer + Fraction(2 * index + 1, 2) * dy
        result.append(line_panel(config, f"G-right-{index:02d}", "right",
                                 outer, y, Fraction(0), dy / 2))
    for index in range(horizontal_count):
        x = outer - Fraction(2 * index + 1, 2) * dx
        result.append(line_panel(config, f"G-top-{index:02d}", "top",
                                 x, outer, -dx / 2, Fraction(0)))
    for index in range(vertical_count):
        y = outer - Fraction(2 * index + 1, 2) * dy
        result.append(line_panel(config, f"G-left-{index:02d}", "left",
                                 left, y, Fraction(0), -dy / 2))

    local_count = config["local"]["panels"]
    for index in range(local_count):
        result.append({
            "id": f"L-circle-{index:02d}",
            "family": "local",
            "kind": "circle",
            "thetaCenterPi": fraction_text(Fraction(2 * index + 1, local_count)),
            "thetaHalfPi": fraction_text(Fraction(1, local_count)),
            "degreeS": config["local"]["degreeS"],
            "steps": config["local"]["steps"],
        })
    return result


def validate_source_ledger(
    ledger_value: Any,
    digest_value: Any,
    expected_paths: Sequence[str] = GRID_SOURCE_PATHS,
    label: str = "sourceLedger",
) -> dict[str, Any]:
    require(type(ledger_value) is list, "sourceLedger must be a list")
    require(len(ledger_value) == len(expected_paths),
            f"{label} has the wrong number of entries")
    validated: list[dict[str, Any]] = []
    for index, (entry_value, expected_relative) in enumerate(
        zip(ledger_value, expected_paths)
    ):
        entry = expect_keys(entry_value, ("path", "bytes", "sha256"),
                            f"{label}[{index}]")
        relative = expect_string(entry["path"], f"{label}[{index}].path")
        require(relative == expected_relative,
                f"{label}[{index}] path/order mismatch")
        path_object = Path(relative)
        require(not path_object.is_absolute() and ".." not in path_object.parts,
                f"unsafe sourceLedger path: {relative}")
        absolute = (ROOT / path_object).resolve()
        require(absolute.is_relative_to(ROOT.resolve()),
                f"sourceLedger path escapes repository: {relative}")
        require(absolute.is_file(), f"sourceLedger file missing: {relative}")
        byte_count = expect_int(entry["bytes"], f"{label}[{index}].bytes", 0)
        file_bytes = absolute.read_bytes()
        require(byte_count == len(file_bytes),
                f"sourceLedger byte count mismatch: {relative}")
        digest = expect_string(entry["sha256"], f"{label}[{index}].sha256")
        require(len(digest) == 64 and all(char in "0123456789abcdef" for char in digest),
                f"invalid SHA-256 syntax for {relative}")
        require(digest == sha256_bytes(file_bytes),
                f"sourceLedger SHA-256 mismatch: {relative}")
        validated.append(dict(entry))

    if "experiments/r073j/requirements.txt" in expected_paths:
        requirements = (ROOT / "experiments/r073j/requirements.txt").read_text(
            encoding="utf-8"
        )
        require(requirements == EXPECTED_REQUIREMENT,
                "requirements.txt must exactly pin python-flint==0.6.0")
    calculated = sha256_bytes(compact_json(validated).encode("ascii"))
    digest = expect_string(digest_value, f"{label}Digest")
    require(digest == calculated,
            f"digest does not match canonical {label}")
    return {"ledger": validated, "digest": calculated}


def validate_checkpoint(
    checkpoint: Any,
    config: dict[str, Any],
    panels: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    checkpoint = expect_keys(checkpoint, (
        "schemaVersion", "status", "createdAt", "updatedAt", "sourceLedger",
        "sourceDigest", "configuration", "panels",
    ), "checkpoint")
    require(checkpoint["schemaVersion"] == GRID_SCHEMA_VERSION,
            "checkpoint schemaVersion mismatch")
    require(checkpoint["status"] in ("grids-complete", "passed"),
            "checkpoint is not complete; independent audit refuses partial grids")
    require(checkpoint["configuration"] == config,
            "checkpoint configuration differs byte-semantically from config.json")
    source = validate_source_ledger(checkpoint["sourceLedger"],
                                    checkpoint["sourceDigest"])
    records = checkpoint["panels"]
    require(type(records) is dict, "checkpoint.panels must be an object")
    expected_ids = [panel["id"] for panel in panels]
    require(set(records) == set(expected_ids),
            "checkpoint panel set is incomplete or contains extras")

    grids: dict[str, list[list[acb]]] = {}
    audit_denominators: list[arb] = []
    audit_slacks: list[arb] = []
    maximum_attempt = 0
    total_points = 0
    for panel in panels:
        panel_id = panel["id"]
        record = expect_keys(records[panel_id], ("definition", "shape", "values"),
                             f"checkpoint.panels.{panel_id}")
        require(record["definition"] == panel,
                f"checkpoint definition mismatch for {panel_id}")
        expected_shape = [config["degreeD"] + 1, panel["degreeS"] + 1]
        require(record["shape"] == expected_shape,
                f"checkpoint shape mismatch for {panel_id}")
        values = record["values"]
        require(type(values) is list, f"checkpoint values must be a list for {panel_id}")
        require(len(values) == expected_shape[0] * expected_shape[1],
                f"checkpoint point count mismatch for {panel_id}")
        grid = [[acb(0) for _ in range(expected_shape[1])]
                for _ in range(expected_shape[0])]
        seen: set[tuple[int, int]] = set()
        for entry_index, entry_value in enumerate(values):
            label = f"checkpoint.panels.{panel_id}.values[{entry_index}]"
            entry = expect_keys(entry_value,
                                ("panelId", "dIndex", "sIndex", "evans", "audit"),
                                label)
            require(entry["panelId"] == panel_id, f"{label}.panelId mismatch")
            d_index = expect_int(entry["dIndex"], f"{label}.dIndex", 0)
            s_index = expect_int(entry["sIndex"], f"{label}.sIndex", 0)
            require(d_index < expected_shape[0] and s_index < expected_shape[1],
                    f"{label} grid index out of range")
            require((d_index, s_index) not in seen,
                    f"duplicate checkpoint grid index {panel_id}:{d_index},{s_index}")
            seen.add((d_index, s_index))
            grid[d_index][s_index] = parse_acb_record(entry["evans"], f"{label}.evans")

            point_audit = expect_keys(entry["audit"], (
                "minimumDenominatorLower", "minimumComponentSlack",
                "maximumPicardAttempt", "steps",
            ), f"{label}.audit")
            denominator = parse_arb(point_audit["minimumDenominatorLower"],
                                    f"{label}.audit.minimumDenominatorLower")
            slack = parse_arb(point_audit["minimumComponentSlack"],
                              f"{label}.audit.minimumComponentSlack")
            require(denominator.lower() > 0,
                    f"nonpositive Rayleigh denominator audit at {label}")
            require(slack.lower() > 0,
                    f"nonpositive Picard component slack at {label}")
            attempt = expect_int(point_audit["maximumPicardAttempt"],
                                 f"{label}.audit.maximumPicardAttempt", 0)
            steps = expect_int(point_audit["steps"], f"{label}.audit.steps", 1)
            require(steps == panel["steps"], f"step count mismatch at {label}")
            audit_denominators.append(denominator)
            audit_slacks.append(slack)
            maximum_attempt = max(maximum_attempt, attempt)
        require(len(seen) == expected_shape[0] * expected_shape[1],
                f"incomplete index lattice for {panel_id}")
        grids[panel_id] = grid
        total_points += len(values)

    return {
        "source": source,
        "grids": grids,
        "pointCount": total_points,
        "minimumDenominator": choose_minimum(audit_denominators, "denominators"),
        "minimumSlack": choose_minimum(audit_slacks, "Picard slacks"),
        "maximumAttempt": maximum_attempt,
    }


def chebyshev_angles(count: int) -> list[arb]:
    return [(2 * index + 1) * arb.pi() / (2 * count) for index in range(count)]


def direct_tensor_dct(values: Sequence[Sequence[acb]]) -> list[list[acb]]:
    """Direct double DCT, intentionally unlike the primary staged transform."""
    d_count = len(values)
    require(d_count > 0, "empty tensor grid")
    s_count = len(values[0])
    require(s_count > 0 and all(len(row) == s_count for row in values),
            "ragged tensor grid")
    d_angles = chebyshev_angles(d_count)
    s_angles = chebyshev_angles(s_count)
    d_cosines = [[(order * angle).cos() for angle in d_angles]
                 for order in range(d_count)]
    s_cosines = [[(order * angle).cos() for angle in s_angles]
                 for order in range(s_count)]
    result = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
    for d_order in range(d_count):
        d_scale = arb(1) / d_count if d_order == 0 else arb(2) / d_count
        for s_order in range(s_count):
            s_scale = arb(1) / s_count if s_order == 0 else arb(2) / s_count
            total = acb(0)
            for d_index in range(d_count):
                subtotal = acb(0)
                for s_index in range(s_count):
                    subtotal += values[d_index][s_index] * s_cosines[s_order][s_index]
                total += d_cosines[d_order][d_index] * subtotal
            result[d_order][s_order] = d_scale * s_scale * total
    return result


def chebyshev_basis_values(count: int, value: arb) -> list[arb]:
    require(count > 0, "Chebyshev basis count must be positive")
    result = [arb(1)]
    if count == 1:
        return result
    result.append(value)
    for _ in range(2, count):
        result.append(2 * value * result[-1] - result[-2])
    return result


def evaluate_tensor_chebyshev(
    coefficients: Sequence[Sequence[acb]],
    d_value: arb,
    s_value: arb,
) -> acb:
    d_basis = chebyshev_basis_values(len(coefficients), d_value)
    s_basis = chebyshev_basis_values(len(coefficients[0]), s_value)
    total = acb(0)
    for d_index, row in enumerate(coefficients):
        for s_index, coefficient in enumerate(row):
            total += coefficient * d_basis[d_index] * s_basis[s_index]
    return total


def verify_dct_interpolates_grid(
    coefficients: Sequence[Sequence[acb]],
    values: Sequence[Sequence[acb]],
    panel_id: str,
) -> None:
    d_nodes = [angle.cos() for angle in chebyshev_angles(len(values))]
    s_nodes = [angle.cos() for angle in chebyshev_angles(len(values[0]))]
    for d_index, d_value in enumerate(d_nodes):
        for s_index, s_value in enumerate(s_nodes):
            rebuilt = evaluate_tensor_chebyshev(coefficients, d_value, s_value)
            original = values[d_index][s_index]
            require(rebuilt.real.contains(original.real)
                    and rebuilt.imag.contains(original.imag),
                    f"direct DCT reconstruction does not contain raw ball at "
                    f"{panel_id}:{d_index},{s_index}")


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


def scale_by_fraction(value: acb, factor: Fraction) -> acb:
    return value * factor.numerator / factor.denominator


def power_minus_one_one_to_bernstein(coefficients: Sequence[acb]) -> list[acb]:
    """Convert p(t), t=2u-1, to exact-degree Bernstein coefficients."""
    degree = len(coefficients) - 1
    mapped = [acb(0) for _ in range(degree + 1)]
    for power, coefficient in enumerate(coefficients):
        for mapped_power in range(power + 1):
            integer = (math.comb(power, mapped_power) * (2 ** mapped_power)
                       * ((-1) ** (power - mapped_power)))
            mapped[mapped_power] += integer * coefficient
    result = [acb(0) for _ in range(degree + 1)]
    for bernstein_index in range(degree + 1):
        for power in range(bernstein_index + 1):
            factor = Fraction(math.comb(bernstein_index, power),
                              math.comb(degree, power))
            result[bernstein_index] += scale_by_fraction(mapped[power], factor)
    return result


def chebyshev_to_bernstein(coefficients: Sequence[acb]) -> list[acb]:
    return power_minus_one_one_to_bernstein(chebyshev_to_power(coefficients))


def tensor_chebyshev_to_bernstein(
    coefficients: Sequence[Sequence[acb]],
) -> list[list[acb]]:
    d_count = len(coefficients)
    s_count = len(coefficients[0])
    after_d = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
    for s_index in range(s_count):
        column = chebyshev_to_bernstein(
            [coefficients[d_index][s_index] for d_index in range(d_count)]
        )
        for d_index in range(d_count):
            after_d[d_index][s_index] = column[d_index]
    return [chebyshev_to_bernstein(row) for row in after_d]


def de_casteljau_value(coefficients: Sequence[acb], parameter: arb) -> acb:
    row = list(coefficients)
    while len(row) > 1:
        row = [(1 - parameter) * row[index] + parameter * row[index + 1]
               for index in range(len(row) - 1)]
    return row[0]


def evaluate_tensor_bernstein(
    coefficients: Sequence[Sequence[acb]],
    d_parameter: arb,
    s_parameter: arb,
) -> acb:
    along_s = [de_casteljau_value(row, s_parameter) for row in coefficients]
    return de_casteljau_value(along_s, d_parameter)


def verify_bernstein_conversion(
    chebyshev: Sequence[Sequence[acb]],
    bernstein: Sequence[Sequence[acb]],
    panel_id: str,
) -> None:
    for t_value in (arb(-1), arb(0), arb(1)):
        for s_value in (arb(-1), arb(0), arb(1)):
            cheb_value = evaluate_tensor_chebyshev(chebyshev, t_value, s_value)
            bern_value = evaluate_tensor_bernstein(
                bernstein, (t_value + 1) / 2, (s_value + 1) / 2
            )
            require(complexes_overlap(cheb_value, bern_value),
                    f"Chebyshev/Bernstein cross-check failed for {panel_id} "
                    f"at ({t_value},{s_value})")


def split_bernstein_half(coefficients: Sequence[acb]) -> tuple[list[acb], list[acb]]:
    triangle = [list(coefficients)]
    while len(triangle[-1]) > 1:
        previous = triangle[-1]
        triangle.append([(previous[index] + previous[index + 1]) / 2
                         for index in range(len(previous) - 1)])
    left = [row[0] for row in triangle]
    right = [row[-1] for row in reversed(triangle)]
    return left, right


def split_tensor_axis(
    coefficients: Sequence[Sequence[acb]], axis: int
) -> tuple[list[list[acb]], list[list[acb]]]:
    d_count = len(coefficients)
    s_count = len(coefficients[0])
    if axis == 1:
        left: list[list[acb]] = []
        right: list[list[acb]] = []
        for row in coefficients:
            first, second = split_bernstein_half(row)
            left.append(first)
            right.append(second)
        return left, right
    require(axis == 0, "tensor split axis must be zero or one")
    left = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
    right = [[acb(0) for _ in range(s_count)] for _ in range(d_count)]
    for s_index in range(s_count):
        first, second = split_bernstein_half(
            [coefficients[d_index][s_index] for d_index in range(d_count)]
        )
        for d_index in range(d_count):
            left[d_index][s_index] = first[d_index]
            right[d_index][s_index] = second[d_index]
    return left, right


def subdivide_tensor(
    coefficients: Sequence[Sequence[acb]], d_depth: int, s_depth: int
) -> list[tuple[int, int, list[list[acb]]]]:
    pieces: list[tuple[int, int, list[list[acb]]]] = [
        (0, 0, [list(row) for row in coefficients])
    ]
    for _ in range(d_depth):
        refined: list[tuple[int, int, list[list[acb]]]] = []
        for d_index, s_index, piece in pieces:
            first, second = split_tensor_axis(piece, 0)
            refined.append((2 * d_index, s_index, first))
            refined.append((2 * d_index + 1, s_index, second))
        pieces = refined
    for _ in range(s_depth):
        refined = []
        for d_index, s_index, piece in pieces:
            first, second = split_tensor_axis(piece, 1)
            refined.append((d_index, 2 * s_index, first))
            refined.append((d_index, 2 * s_index + 1, second))
        pieces = refined
    return sorted(pieces, key=lambda item: (item[0], item[1]))


def subdivide_curve(coefficients: Sequence[acb], depth: int) -> list[list[acb]]:
    pieces = [list(coefficients)]
    for _ in range(depth):
        refined: list[list[acb]] = []
        for piece in pieces:
            refined.extend(split_bernstein_half(piece))
        pieces = refined
    return pieces


def complex_hull(values: Sequence[acb]) -> acb:
    require(bool(values), "cannot hull an empty complex collection")
    real = values[0].real
    imag = values[0].imag
    for value in values[1:]:
        real = real.union(value.real)
        imag = imag.union(value.imag)
    return acb(real, imag)


def tensor_hull(values: Sequence[Sequence[acb]]) -> acb:
    return complex_hull([value for row in values for value in row])


def inflate_complex(value: acb, error: arb) -> acb:
    require(error.lower() >= 0, "negative interpolation error")
    return acb(
        arb(value.real.mid(), value.real.rad() + error),
        arb(value.imag.mid(), value.imag.rad() + error),
    )


def ellipse_axes(rho: arb) -> tuple[arb, arb]:
    return (rho + 1 / rho) / 2, (rho - 1 / rho) / 2


def real_path_minimum(panel: dict[str, Any]) -> arb:
    if panel["kind"] == "circle":
        return arb(167) / 1000
    center = arb_fraction(Fraction(panel["centerReal"]))
    half = arb_fraction(abs(Fraction(panel["halfReal"])))
    return center - half


def ellipse_path_minimum(panel: dict[str, Any], rho: arb) -> arb:
    major, minor = ellipse_axes(rho)
    if panel["kind"] == "line":
        return (
            arb_fraction(Fraction(panel["centerReal"]))
            - arb_fraction(abs(Fraction(panel["halfReal"]))) * major
            - arb_fraction(abs(Fraction(panel["halfImag"]))) * minor
        )
    theta_half = arb.pi() * arb_fraction(abs(Fraction(panel["thetaHalfPi"])))
    return arb(17) / 100 - arb(3) / 1000 * (theta_half * minor).exp()


def real_d_majorant(minimum_lambda_real: arb) -> dict[str, arb]:
    require(minimum_lambda_real.lower() > 0,
            "parameter ellipse reaches Re(lambda) <= 0")
    denominator = 2 * minimum_lambda_real
    velocity_xx = arb(3) / 2
    potential = arb(1) / 4 + velocity_xx / denominator
    evans = 2 + 2 * (2 * arb.pi() * potential.sqrt()).exp()
    return {
        "minimumLambdaReal": minimum_lambda_real,
        "denominatorLower": denominator,
        "velocityXXUpper": velocity_xx,
        "potentialUpper": potential,
        "evansUpper": evans,
    }


def complex_d_majorant(minimum_lambda_real: arb, rho: arb) -> dict[str, arb]:
    require(minimum_lambda_real.lower() > 0 and rho.lower() > 1,
            "invalid complex-d majorant inputs")
    maximum_d = arb(1) / 450
    major, minor = ellipse_axes(rho)
    d_real_minimum = maximum_d * (1 - major) / 2
    d_real_maximum = maximum_d * (1 + major) / 2
    d_imag_maximum = maximum_d * minor / 2
    exponential_one = (-d_real_minimum).exp()
    exponential_four = (-4 * d_real_minimum).exp()
    imaginary_velocity = (exponential_one * d_imag_maximum / 2
                          + exponential_four * d_imag_maximum)
    denominator = 2 * minimum_lambda_real - imaginary_velocity
    require(denominator.lower() > 0, "complex-d ellipse reaches a Rayleigh pole")
    velocity_xx = exponential_one / 2 + exponential_four
    potential = arb(1) / 4 + velocity_xx / denominator
    evans = 2 + 2 * (2 * arb.pi() * potential.sqrt()).exp()
    return {
        "dRealMinimum": d_real_minimum,
        "dRealMaximum": d_real_maximum,
        "dImagMaximum": d_imag_maximum,
        "imaginaryVelocityUpper": imaginary_velocity,
        "minimumLambdaReal": minimum_lambda_real,
        "denominatorLower": denominator,
        "velocityXXUpper": velocity_xx,
        "potentialUpper": potential,
        "evansUpper": evans,
    }


def interpolation_error(majorant: arb, degree: int, rho: arb) -> arb:
    require(majorant.lower() >= 0 and rho.lower() > 1 and degree >= 0,
            "invalid interpolation-error inputs")
    return 4 * majorant * rho ** (-degree) / (rho - 1)


def lebesgue_bound(degree: int) -> arb:
    require(degree >= 0, "negative Chebyshev degree")
    return 1 + 2 * arb(degree + 1).log() / arb.pi()


def dyadic_bounds(index: int, depth: int) -> tuple[Fraction, Fraction]:
    require(depth >= 0 and 0 <= index < 2 ** depth, "invalid dyadic cell")
    denominator = 2 ** depth
    return (
        Fraction(-1) + Fraction(2 * index, denominator),
        Fraction(-1) + Fraction(2 * (index + 1), denominator),
    )


def dyadic_interval(index: int, depth: int) -> arb:
    lower, upper = dyadic_bounds(index, depth)
    return arb_fraction(lower).union(arb_fraction(upper))


def dyadic_point(index: int, depth: int) -> arb:
    require(depth >= 0 and 0 <= index <= 2 ** depth,
            "invalid dyadic endpoint")
    return arb_fraction(Fraction(-1) + Fraction(2 * index, 2 ** depth))


def interval_clenshaw(coefficients: Sequence[acb], parameter: arb) -> acb:
    """Outward-rounded Clenshaw for c_0 + sum_{k>=1} c_k T_k.

    The final expression matches the DCT convention used by
    :func:`direct_tensor_dct`; in particular c_0 is not doubled.
    """
    require(bool(coefficients), "empty interval-Clenshaw coefficient list")
    if len(coefficients) == 1:
        return coefficients[0]
    next_one = acb(0)
    next_two = acb(0)
    for order in range(len(coefficients) - 1, 0, -1):
        current = 2 * parameter * next_one - next_two + coefficients[order]
        next_two, next_one = next_one, current
    return coefficients[0] + parameter * next_one - next_two


def reverse_tensor_interval_clenshaw(
    coefficients: Sequence[Sequence[acb]],
    d_box: arb,
    s_box: arb,
) -> acb:
    """Evaluate d first and s second, opposite to the primary implementation."""
    require(bool(coefficients) and bool(coefficients[0]),
            "empty tensor coefficient array")
    s_count = len(coefficients[0])
    require(all(len(row) == s_count for row in coefficients),
            "ragged tensor coefficient array")
    d_evaluated = [
        interval_clenshaw(
            [coefficients[d_order][s_order]
             for d_order in range(len(coefficients))],
            d_box,
        )
        for s_order in range(s_count)
    ]
    return interval_clenshaw(d_evaluated, s_box)


def forward_tensor_interval_clenshaw_for_reaudit(
    coefficients: Sequence[Sequence[acb]],
    d_box: arb,
    s_box: arb,
) -> acb:
    """Recompute primary s-then-d boxes only for margin/serialization audit."""
    s_evaluated = [interval_clenshaw(row, s_box) for row in coefficients]
    return interval_clenshaw(s_evaluated, d_box)


def verify_reverse_clenshaw_points(
    coefficients: Sequence[Sequence[acb]], panel_id: str
) -> None:
    for d_value in (arb(-1), arb(0), arb(1)):
        for s_value in (arb(-1), arb(0), arb(1)):
            direct = evaluate_tensor_chebyshev(coefficients, d_value, s_value)
            reverse = reverse_tensor_interval_clenshaw(
                coefficients, d_value, s_value
            )
            require(complexes_overlap(direct, reverse),
                    f"direct/reverse-Clenshaw point check failed for {panel_id}")


def restricted_d_minus_one(
    coefficients: Sequence[Sequence[acb]],
) -> list[acb]:
    """Use T_k(-1)=(-1)^k without the primary restriction evaluator."""
    return [
        sum(
            (((-1) ** d_order) * coefficients[d_order][s_order]
             for d_order in range(len(coefficients))),
            acb(0),
        )
        for s_order in range(len(coefficients[0]))
    ]


def adaptive_reverse_clenshaw_cover(
    coefficients: Sequence[Sequence[acb]],
    tensor_error: arb,
    initial_d_depth: int,
    initial_s_depth: int,
    panel_id: str,
) -> dict[str, Any]:
    """Certify a complete dyadic cover, refining only inconclusive leaves."""
    leaves: list[dict[str, Any]] = []
    maximum_extra = 0

    def visit(
        d_index: int,
        d_depth: int,
        s_index: int,
        s_depth: int,
        extra: int,
    ) -> None:
        nonlocal maximum_extra
        image = inflate_complex(
            reverse_tensor_interval_clenshaw(
                coefficients,
                dyadic_interval(d_index, d_depth),
                dyadic_interval(s_index, s_depth),
            ),
            tensor_error,
        )
        lower = image.abs_lower()
        if lower.lower() > 0:
            maximum_extra = max(maximum_extra, extra)
            leaves.append({
                "dDepth": d_depth,
                "dIndex": d_index,
                "sDepth": s_depth,
                "sIndex": s_index,
                "image": image,
                "lower": lower,
            })
            return
        require(extra < MAX_EXTRA_DYADIC_DEPTH,
                f"reverse Clenshaw remains inconclusive for {panel_id} at "
                f"d={d_index}/{2**d_depth}, s={s_index}/{2**s_depth}")
        for d_child in (2 * d_index, 2 * d_index + 1):
            for s_child in (2 * s_index, 2 * s_index + 1):
                visit(d_child, d_depth + 1, s_child, s_depth + 1, extra + 1)

    for d_index in range(2 ** initial_d_depth):
        for s_index in range(2 ** initial_s_depth):
            visit(d_index, initial_d_depth, s_index, initial_s_depth, 0)

    keys = {(leaf["dDepth"], leaf["dIndex"],
             leaf["sDepth"], leaf["sIndex"]) for leaf in leaves}
    require(len(keys) == len(leaves), f"duplicate adaptive leaf for {panel_id}")
    covered_area = sum(
        (Fraction(2, 2 ** leaf["dDepth"])
         * Fraction(2, 2 ** leaf["sDepth"]))
        for leaf in leaves
    )
    require(covered_area == 4,
            f"adaptive dyadic leaves do not have full area for {panel_id}")
    return {
        "leaves": leaves,
        "minimum": choose_minimum([leaf["lower"] for leaf in leaves], panel_id),
        "maximumExtraDepth": maximum_extra,
        "exactCoveredArea": fraction_text(covered_area),
    }


def fixed_base_cells(
    panel: dict[str, Any],
    restricted: Sequence[acb],
    tensor_error: arb,
    s_depth: int,
) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for cell_index in range(2 ** s_depth):
        image = inflate_complex(
            interval_clenshaw(restricted, dyadic_interval(cell_index, s_depth)),
            tensor_error,
        )
        require(image.abs_lower().lower() > 0,
                f"independent base curve box contains zero: "
                f"{panel['id']} s={cell_index}")
        result.append({
            "panelId": panel["id"],
            "cellIndex": cell_index,
            "sDepth": s_depth,
            "image": image,
            "startBall": interval_clenshaw(
                restricted, dyadic_point(cell_index, s_depth)
            ),
            "endBall": interval_clenshaw(
                restricted, dyadic_point(cell_index + 1, s_depth)
            ),
        })
    return result


def independent_panel_analysis(
    config: dict[str, Any],
    panel: dict[str, Any],
    values: Sequence[Sequence[acb]],
) -> dict[str, Any]:
    coefficients = direct_tensor_dct(values)
    verify_dct_interpolates_grid(coefficients, values, panel["id"])
    verify_reverse_clenshaw_points(coefficients, panel["id"])

    rho_d = arb_fraction(Fraction(config["rhoD"]))
    rho_s = arb_fraction(Fraction(config["rhoS"]))
    lebesgue_limit = arb_fraction(Fraction(config["lebesgueLimit"]))
    d_lebesgue = lebesgue_bound(config["degreeD"])
    s_lebesgue = lebesgue_bound(panel["degreeS"])
    require(d_lebesgue.upper() < lebesgue_limit.lower(),
            "degree-d Lebesgue bound is not below configured limit")
    require(s_lebesgue.upper() < lebesgue_limit.lower(),
            f"degree-s Lebesgue bound is not below limit for {panel['id']}")

    real_minimum = real_path_minimum(panel)
    ellipse_minimum = ellipse_path_minimum(panel, rho_s)
    d_majorant = complex_d_majorant(real_minimum, rho_d)
    s_majorant = real_d_majorant(ellipse_minimum)
    d_error = interpolation_error(d_majorant["evansUpper"],
                                  config["degreeD"], rho_d)
    s_error = interpolation_error(s_majorant["evansUpper"],
                                  panel["degreeS"], rho_s)
    tensor_error = s_error + lebesgue_limit * d_error
    subdivision = config[panel["family"]]["subdivision"]
    cover = adaptive_reverse_clenshaw_cover(
        coefficients,
        tensor_error,
        subdivision["dDepth"],
        subdivision["sDepth"],
        panel["id"],
    )
    primary_order_fixed: dict[tuple[int, int, int, int], dict[str, Any]] = {}
    for d_index in range(2 ** subdivision["dDepth"]):
        for s_index in range(2 ** subdivision["sDepth"]):
            image = inflate_complex(
                forward_tensor_interval_clenshaw_for_reaudit(
                    coefficients,
                    dyadic_interval(d_index, subdivision["dDepth"]),
                    dyadic_interval(s_index, subdivision["sDepth"]),
                ),
                tensor_error,
            )
            lower = image.abs_lower()
            require(lower.lower() > 0,
                    f"independently replayed primary-order box contains zero: "
                    f"{panel['id']} d={d_index} s={s_index}")
            primary_order_fixed[(
                subdivision["dDepth"], d_index,
                subdivision["sDepth"], s_index,
            )] = {"image": image, "lower": lower}
    restricted = restricted_d_minus_one(coefficients)
    base_cells = fixed_base_cells(
        panel, restricted, tensor_error, subdivision["sDepth"]
    )

    return {
        "panel": panel,
        "coefficients": coefficients,
        "realMinimum": real_minimum,
        "ellipseMinimum": ellipse_minimum,
        "dMajorant": d_majorant,
        "sMajorant": s_majorant,
        "dError": d_error,
        "sError": s_error,
        "tensorError": tensor_error,
        "lebesgue": s_lebesgue,
        "cellLeaves": cover["leaves"],
        "minimum": cover["minimum"],
        "maximumExtraDepth": cover["maximumExtraDepth"],
        "exactCoveredArea": cover["exactCoveredArea"],
        "initialDDepth": subdivision["dDepth"],
        "initialSDepth": subdivision["sDepth"],
        "primaryOrderFixed": primary_order_fixed,
        "baseCells": base_cells,
    }


def decimal_fraction(text_value: Any, label: str) -> Fraction:
    text = expect_string(text_value, label)
    try:
        decimal = Decimal(text)
    except InvalidOperation as error:
        raise AuditFailure(f"{label} is not a finite decimal rational") from error
    require(decimal.is_finite(), f"{label} is not finite")
    return Fraction(decimal)


def vertex_fraction(value: Any, label: str) -> tuple[Fraction, Fraction]:
    record = expect_keys(value, ("real", "imag"), label)
    return (decimal_fraction(record["real"], f"{label}.real"),
            decimal_fraction(record["imag"], f"{label}.imag"))


def rational_candidate(value: acb, label: str) -> dict[str, str]:
    """Choose a finite decimal point and prove that its Arb ball contains it."""
    for digits in (60, 90, 130, 180):
        real_text = value.real.mid().str(digits, radius=False, more=True)
        imag_text = value.imag.mid().str(digits, radius=False, more=True)
        try:
            real_fraction = Fraction(Decimal(real_text))
            imag_fraction = Fraction(Decimal(imag_text))
        except (InvalidOperation, ValueError):
            continue
        candidate = acb(arb(real_text), arb(imag_text))
        if value.real.contains(candidate.real) and value.imag.contains(candidate.imag):
            return {"real": real_text, "imag": imag_text}
    raise AuditFailure(f"failed to choose an exact decimal candidate inside {label}")


def point_acb(vertex: Any, label: str) -> acb:
    x, y = vertex_fraction(vertex, label)
    return acb(arb_fraction(x), arb_fraction(y))


def hull_with_points(image: acb, vertices: Sequence[Any], label: str) -> acb:
    real = image.real
    imag = image.imag
    for index, vertex in enumerate(vertices):
        point = point_acb(vertex, f"{label}.vertices[{index}]")
        real = real.union(point.real)
        imag = imag.union(point.imag)
    return acb(real, imag)


def axis_half_plane(value: acb) -> dict[str, str] | None:
    if value.real.lower() > 0:
        return {"axis": "real", "sign": "+", "margin": arb_text(value.real.lower())}
    if value.real.upper() < 0:
        return {"axis": "real", "sign": "-", "margin": arb_text(-value.real.upper())}
    if value.imag.lower() > 0:
        return {"axis": "imag", "sign": "+", "margin": arb_text(value.imag.lower())}
    if value.imag.upper() < 0:
        return {"axis": "imag", "sign": "-", "margin": arb_text(-value.imag.upper())}
    return None


def exact_polygon_winding(
    vertices_value: Any,
    label: str,
    forced_rotation: int | None = None,
) -> dict[str, int]:
    require(type(vertices_value) is list and len(vertices_value) >= 3,
            f"{label} must contain at least three vertices")
    vertices = [vertex_fraction(value, f"{label}[{index}]")
                for index, value in enumerate(vertices_value)]
    require(all(not (x == 0 and y == 0) for x, y in vertices),
            f"{label} contains the origin as a vertex")
    for index, (first, second) in enumerate(
        zip(vertices, vertices[1:] + vertices[:1])
    ):
        x1, y1 = first
        x2, y2 = second
        determinant = x1 * y2 - x2 * y1
        if determinant == 0 and x1 * x2 <= 0 and y1 * y2 <= 0:
            raise AuditFailure(f"{label} edge {index} passes through the origin")

    rotation: int | None = None
    transformed: list[tuple[Fraction, Fraction]] = []
    candidates = (range(257) if forced_rotation is None else (forced_rotation,))
    for candidate in candidates:
        trial = [(x - candidate * y, candidate * x + y) for x, y in vertices]
        if all(y != 0 for _, y in trial):
            rotation = candidate
            transformed = trial
            break
    require(rotation is not None,
            f"failed to select an exact rational ray rotation for {label}")

    winding = 0
    for first, second in zip(transformed, transformed[1:] + transformed[:1]):
        x1, y1 = first
        x2, y2 = second
        determinant = x1 * y2 - x2 * y1
        if y1 <= 0 < y2 and determinant > 0:
            winding += 1
        elif y2 <= 0 < y1 and determinant < 0:
            winding -= 1
    return {"rotationImaginaryMultiplier": int(rotation), "winding": winding}


def independent_base_polygon(
    family: str, base_cells: Sequence[dict[str, Any]]
) -> dict[str, Any]:
    require(bool(base_cells), f"no independently reconstructed {family} base cells")
    vertices = [rational_candidate(base_cells[0]["startBall"],
                                   f"{family} base start")]
    vertices.extend(rational_candidate(cell["endBall"],
                                       f"{family} base cell {index} end")
                    for index, cell in enumerate(base_cells[:-1]))
    homotopy_lowers: list[arb] = []
    for index, cell in enumerate(base_cells):
        endpoints = (vertices[index], vertices[(index + 1) % len(vertices)])
        box = hull_with_points(cell["image"], endpoints,
                               f"independent {family} base cell {index}")
        require(axis_half_plane(box) is not None,
                f"independent {family} base homotopy box contains zero "
                f"at cell {index}")
        homotopy_lowers.append(box.abs_lower())
    winding = exact_polygon_winding(vertices,
                                    f"independentPolygons.{family}.vertices")
    require(winding["winding"] == 1,
            f"independent exact polygon winding is not one: {winding}")
    return {
        "vertices": vertices,
        "winding": winding,
        "minimum": choose_minimum(homotopy_lowers,
                                  f"independent {family} homotopy"),
        "cellCount": len(base_cells),
    }


def validate_majorant_record(
    record_value: Any,
    computed: dict[str, arb],
    label: str,
) -> None:
    record = expect_keys(record_value, tuple(computed), label)
    for key, value in computed.items():
        require_ball_agreement(record[key], value, f"{label}.{key}")


def validate_primary_cell_box(value: Any, label: str) -> tuple[acb, arb, arb]:
    record = expect_keys(value, (
        "dIndex", "sIndex", "dDepth", "sDepth", "box", "absoluteLower",
    ), label)
    expect_int(record["dIndex"], f"{label}.dIndex", 0)
    expect_int(record["sIndex"], f"{label}.sIndex", 0)
    expect_int(record["dDepth"], f"{label}.dDepth", 0)
    expect_int(record["sDepth"], f"{label}.sDepth", 0)
    box = parse_acb_record(record["box"], f"{label}.box")
    recomputed = box.abs_lower()
    reported = parse_arb(record["absoluteLower"], f"{label}.absoluteLower")
    require(recomputed.lower() > 0 and reported.lower() > 0,
            f"primary cell decision is not strictly positive at {label}")
    return box, recomputed, reported


def validate_primary_panel(
    primary_value: Any,
    independent: dict[str, Any],
    label: str,
) -> dict[str, Any]:
    primary = expect_keys(primary_value, (
        "id", "family", "definition", "realPathMinimumLambdaReal",
        "ellipseMinimumLambdaReal", "dMajorant", "sMajorant",
        "dInterpolationError", "sInterpolationError", "tensorInterpolationError",
        "lebesgueBound", "minimumAbsoluteLower", "cells",
    ), label)
    panel = independent["panel"]
    require(primary["id"] == panel["id"] and primary["family"] == panel["family"],
            f"primary panel identity mismatch at {label}")
    require(primary["definition"] == panel,
            f"primary panel definition mismatch at {label}")
    require_ball_agreement(primary["realPathMinimumLambdaReal"],
                           independent["realMinimum"],
                           f"{label}.realPathMinimumLambdaReal")
    require_ball_agreement(primary["ellipseMinimumLambdaReal"],
                           independent["ellipseMinimum"],
                           f"{label}.ellipseMinimumLambdaReal")
    validate_majorant_record(primary["dMajorant"], independent["dMajorant"],
                             f"{label}.dMajorant")
    validate_majorant_record(primary["sMajorant"], independent["sMajorant"],
                             f"{label}.sMajorant")
    require_ball_agreement(primary["dInterpolationError"], independent["dError"],
                           f"{label}.dInterpolationError")
    require_ball_agreement(primary["sInterpolationError"], independent["sError"],
                           f"{label}.sInterpolationError")
    require_ball_agreement(primary["tensorInterpolationError"],
                           independent["tensorError"],
                           f"{label}.tensorInterpolationError")
    require_ball_agreement(primary["lebesgueBound"], independent["lebesgue"],
                           f"{label}.lebesgueBound")

    cells_value = primary["cells"]
    require(type(cells_value) is list, f"{label}.cells must be a list")
    d_depth = independent["initialDDepth"]
    s_depth = independent["initialSDepth"]
    expected_indices = {
        (d_depth, d_index, s_depth, s_index)
        for d_index in range(2 ** d_depth)
        for s_index in range(2 ** s_depth)
    }
    require(len(cells_value) == len(expected_indices),
            f"primary cell count mismatch at {label}")
    seen: set[tuple[int, int, int, int]] = set()
    primary_lowers: list[arb] = []
    for index, cell_value in enumerate(cells_value):
        cell_label = f"{label}.cells[{index}]"
        cell_record = expect_keys(cell_value,
                                  ("dIndex", "sIndex", "dDepth", "sDepth",
                                   "box", "absoluteLower"),
                                  cell_label)
        key = (
            expect_int(cell_record["dDepth"], f"{cell_label}.dDepth", 0),
            expect_int(cell_record["dIndex"], f"{cell_label}.dIndex", 0),
            expect_int(cell_record["sDepth"], f"{cell_label}.sDepth", 0),
            expect_int(cell_record["sIndex"], f"{cell_label}.sIndex", 0),
        )
        require(key in expected_indices and key not in seen,
                f"wrong or duplicate primary cell index {panel['id']}:{key}")
        seen.add(key)
        serialized_box, _, reported = validate_primary_cell_box(
            cell_record, cell_label
        )
        replay = independent["primaryOrderFixed"][key]
        require(serialized_box.real.contains(replay["image"].real)
                and serialized_box.imag.contains(replay["image"].imag),
                f"serialized primary box does not contain independent "
                f"primary-order replay: {panel['id']}:{key}")
        primary_lowers.append(reported)
    require(seen == expected_indices, f"primary cell lattice mismatch at {label}")
    primary_minimum = choose_minimum(primary_lowers, f"primary {panel['id']} cells")
    reported_minimum = require_ball_agreement(primary["minimumAbsoluteLower"],
                                              primary_minimum,
                                              f"{label}.minimumAbsoluteLower")
    require(reported_minimum.lower() > 0,
            f"primary panel minimum is not positive at {label}")
    return {"primaryMinimum": primary_minimum, "cellCount": len(cells_value)}


def validate_recorded_witness(value: Any, box: acb, label: str) -> None:
    witness = expect_keys(value, ("axis", "sign", "margin"), label)
    require(witness["axis"] in ("real", "imag"), f"invalid axis at {label}")
    require(witness["sign"] in ("+", "-"), f"invalid sign at {label}")
    coordinate = box.real if witness["axis"] == "real" else box.imag
    if witness["sign"] == "+":
        require(coordinate.lower() > 0, f"false positive half-plane witness at {label}")
        actual = coordinate.lower()
    else:
        require(coordinate.upper() < 0, f"false negative half-plane witness at {label}")
        actual = -coordinate.upper()
    margin = parse_arb(witness["margin"], f"{label}.margin")
    require(actual.lower() > 0 and margin.lower() > 0,
            f"nonpositive recorded witness margin at {label}")


def validate_primary_polygon(
    family: str,
    polygon_value: Any,
    base_cells: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    polygon = expect_keys(polygon_value, (
        "rotationImaginaryMultiplier", "winding", "vertexCount", "vertices", "cells",
        "homotopyMinimumAbsoluteLower",
    ), f"certificate.exactPolygons.{family}")
    vertices = polygon["vertices"]
    require(type(vertices) is list,
            f"certificate.exactPolygons.{family}.vertices must be a list")
    vertex_count = expect_int(polygon["vertexCount"],
                              f"certificate.exactPolygons.{family}.vertexCount", 3)
    require(vertex_count == len(vertices) == len(base_cells),
            f"primary {family} polygon vertex/base-cell count mismatch")
    for index, vertex in enumerate(vertices):
        point = point_acb(
            vertex, f"certificate.exactPolygons.{family}.vertices[{index}]"
        )
        anchor_ball = (base_cells[0]["startBall"] if index == 0
                       else base_cells[index - 1]["endBall"])
        require(anchor_ball.real.contains(point.real)
                and anchor_ball.imag.contains(point.imag),
                f"primary {family} vertex {index} is not inside independently "
                "rebuilt anchor")

    recorded_rotation = expect_int(polygon["rotationImaginaryMultiplier"],
                                   f"certificate.exactPolygons.{family}."
                                   "rotationImaginaryMultiplier", 0)
    recorded_winding = expect_int(polygon["winding"],
                                  f"certificate.exactPolygons.{family}.winding")
    require(recorded_rotation <= 256, "primary exact polygon rotation is out of range")
    exact = exact_polygon_winding(
        vertices, f"certificate.exactPolygons.{family}.vertices"
    )
    recorded_ray = exact_polygon_winding(
        vertices, f"certificate.exactPolygons.{family}.vertices(recorded ray)",
        forced_rotation=recorded_rotation,
    )
    require(recorded_winding == exact["winding"] == recorded_ray["winding"] == 1,
            f"primary exact rational winding is not one: recorded={recorded_winding}, "
            f"recomputed={exact['winding']}, recordedRay={recorded_ray['winding']}")

    cells_value = polygon["cells"]
    require(type(cells_value) is list and len(cells_value) == len(base_cells),
            "primary winding-cell list is incomplete")
    primary_lowers: list[arb] = []
    independent_lowers: list[arb] = []
    for index, (cell_value, independent_cell) in enumerate(zip(cells_value, base_cells)):
        label = f"certificate.exactPolygons.{family}.cells[{index}]"
        cell = expect_keys(cell_value, (
            "index", "panelId", "cellIndex", "imageWithChord",
            "absoluteLower", "halfPlaneWitness",
        ), label)
        require(expect_int(cell["index"], f"{label}.index", 0) == index,
                f"primary winding-cell index mismatch at {index}")
        require(cell["panelId"] == independent_cell["panelId"]
                and cell["cellIndex"] == independent_cell["cellIndex"],
                f"primary winding-cell provenance mismatch at {index}")
        box = parse_acb_record(cell["imageWithChord"], f"{label}.imageWithChord")
        lower = box.abs_lower()
        reported = parse_arb(cell["absoluteLower"], f"{label}.absoluteLower")
        require(lower.lower() > 0 and reported.lower() > 0,
                f"primary homotopy box contains zero at {index}")
        validate_recorded_witness(cell["halfPlaneWitness"], box,
                                  f"{label}.halfPlaneWitness")
        endpoints = (vertices[index], vertices[(index + 1) % len(vertices)])
        for endpoint_index, endpoint in enumerate(endpoints):
            point = point_acb(endpoint, f"{label}.endpoint[{endpoint_index}]")
            require(box.real.contains(point.real) and box.imag.contains(point.imag),
                    f"primary homotopy box omits polygon endpoint at cell {index}")
        primary_lowers.append(reported)

        independent_box = hull_with_points(independent_cell["image"], endpoints,
                                           f"independent-primary homotopy {index}")
        require(axis_half_plane(independent_box) is not None,
                f"independent curve-to-primary-polygon homotopy contains zero "
                f"at cell {index}")
        independent_lower = independent_box.abs_lower()
        require(independent_lower.lower() > 0,
                f"independent homotopy margin is nonpositive at cell {index}")
        independent_lowers.append(independent_lower)

    primary_minimum = choose_minimum(
        primary_lowers, f"primary {family} homotopy cells"
    )
    reported_minimum = require_ball_agreement(
        polygon["homotopyMinimumAbsoluteLower"],
        primary_minimum,
        f"certificate.exactPolygons.{family}.homotopyMinimumAbsoluteLower",
    )
    require(reported_minimum.lower() > 0,
            f"primary {family} polygon minimum is not positive")
    return {
        "winding": exact["winding"],
        "rotation": exact["rotationImaginaryMultiplier"],
        "primaryMinimum": primary_minimum,
        "independentToPrimaryMinimum": choose_minimum(
            independent_lowers, "independent-to-primary homotopy cells"
        ),
        "cellCount": len(cells_value),
    }


def validate_primary_certificate(
    certificate: Any,
    config: dict[str, Any],
    checkpoint: dict[str, Any],
    checkpoint_audit: dict[str, Any],
    panels: Sequence[dict[str, Any]],
    analyses: Sequence[dict[str, Any]],
    base_cells: dict[str, Sequence[dict[str, Any]]],
) -> dict[str, Any]:
    certificate = expect_keys(certificate, (
        "schemaVersion", "status", "completedAt", "sourceLedger", "sourceDigest",
        "configuration", "arithmetic", "interpolation", "decisions",
        "exactPolygons", "panels", "gridEvidence", "analysisEvidence",
    ), "certificate")
    require(certificate["schemaVersion"] == CERTIFICATE_SCHEMA_VERSION,
            "certificate schemaVersion mismatch")
    require(certificate["status"] == "passed", "primary certificate status is not passed")
    require(certificate["configuration"] == config == checkpoint["configuration"],
            "certificate/config/checkpoint configuration mismatch")
    certificate_source = validate_source_ledger(
        certificate["sourceLedger"], certificate["sourceDigest"],
        CERTIFICATE_SOURCE_PATHS, "certificate.sourceLedger",
    )
    grid_evidence = expect_keys(certificate["gridEvidence"], (
        "checkpoint", "sourceLedger", "sourceDigest", "status",
    ), "certificate.gridEvidence")
    require(grid_evidence["checkpoint"] ==
            "experiments/r073j/contour_grid_checkpoint.json",
            "certificate grid checkpoint path mismatch")
    require(grid_evidence["sourceLedger"] == checkpoint["sourceLedger"]
            and grid_evidence["sourceDigest"] == checkpoint["sourceDigest"]
            and grid_evidence["status"] == checkpoint["status"],
            "certificate grid evidence differs from frozen checkpoint")
    analysis_evidence = expect_keys(certificate["analysisEvidence"],
                                    ("sourceLedger", "sourceDigest"),
                                    "certificate.analysisEvidence")
    analysis_source = validate_source_ledger(
        analysis_evidence["sourceLedger"], analysis_evidence["sourceDigest"],
        ANALYSIS_SOURCE_PATHS, "certificate.analysisEvidence.sourceLedger",
    )
    require(certificate_source["ledger"] ==
            list(checkpoint["sourceLedger"]) + analysis_source["ledger"],
            "combined certificate ledger is not grid ledger plus analysis ledger")

    arithmetic = expect_keys(certificate["arithmetic"], (
        "engine", "python", "pythonImplementation", "precisionDecimalDigits",
        "odePointCount", "minimumRayleighDenominatorLower",
        "minimumPicardComponentSlack", "maximumPicardInflationAttempt",
    ), "certificate.arithmetic")
    require(expect_int(arithmetic["precisionDecimalDigits"],
                       "certificate.arithmetic.precisionDecimalDigits", 1)
            == config["dps"], "certificate precision does not match configuration")
    require(expect_int(arithmetic["odePointCount"],
                       "certificate.arithmetic.odePointCount", 1)
            == checkpoint_audit["pointCount"], "certificate ODE point count mismatch")
    require_ball_agreement(arithmetic["minimumRayleighDenominatorLower"],
                           checkpoint_audit["minimumDenominator"],
                           "certificate.arithmetic.minimumRayleighDenominatorLower")
    require_ball_agreement(arithmetic["minimumPicardComponentSlack"],
                           checkpoint_audit["minimumSlack"],
                           "certificate.arithmetic.minimumPicardComponentSlack")
    require(expect_int(arithmetic["maximumPicardInflationAttempt"],
                       "certificate.arithmetic.maximumPicardInflationAttempt", 0)
            == checkpoint_audit["maximumAttempt"],
            "certificate maximum Picard attempt mismatch")

    interpolation = expect_keys(certificate["interpolation"], (
        "nodes", "remainderFormula", "tensorDecomposition", "lebesgueLimit",
        "degreeDLebesgueBound", "rangeMethod",
    ), "certificate.interpolation")
    require(interpolation["rangeMethod"] ==
            "direct outward-rounded interval Clenshaw on a complete dyadic real-box cover",
            "primary range method is not the frozen Clenshaw-v2 method")
    require(interpolation["lebesgueLimit"] == config["lebesgueLimit"],
            "certificate Lebesgue limit mismatch")
    require_ball_agreement(interpolation["degreeDLebesgueBound"],
                           lebesgue_bound(config["degreeD"]),
                           "certificate.interpolation.degreeDLebesgueBound")

    primary_panels = certificate["panels"]
    require(type(primary_panels) is list and len(primary_panels) == len(panels),
            "certificate panel list is incomplete")
    primary_global: list[arb] = []
    primary_local: list[arb] = []
    for index, (primary_panel, panel, analysis) in enumerate(
        zip(primary_panels, panels, analyses)
    ):
        require(primary_panel.get("id") == panel["id"],
                f"certificate panel order mismatch at index {index}")
        summary = validate_primary_panel(primary_panel, analysis,
                                         f"certificate.panels[{index}]")
        (primary_global if panel["family"] == "global" else primary_local).append(
            summary["primaryMinimum"]
        )
    require(primary_global and primary_local,
            "certificate must include both global and local panels")
    global_minimum = choose_minimum(primary_global, "primary global panels")
    local_minimum = choose_minimum(primary_local, "primary local panels")

    exact_polygons = expect_keys(certificate["exactPolygons"],
                                 ("global", "local"),
                                 "certificate.exactPolygons")
    polygons = {
        family: validate_primary_polygon(
            family, exact_polygons[family], base_cells[family]
        )
        for family in ("global", "local")
    }
    decisions = expect_keys(certificate["decisions"], (
        "globalBoundaryNonzeroForAllD", "globalMinimumAbsoluteLower",
        "localBoundaryNonzeroForAllD", "localMinimumAbsoluteLower",
        "globalBasePositiveOrientationWinding",
        "globalBaseHomotopyMinimumAbsoluteLower",
        "localBasePositiveOrientationWinding",
        "localBaseHomotopyMinimumAbsoluteLower",
    ), "certificate.decisions")
    require(decisions["globalBoundaryNonzeroForAllD"] is True,
            "primary global nonvanishing decision is not true")
    require(decisions["localBoundaryNonzeroForAllD"] is True,
            "primary local nonvanishing decision is not true")
    for family in ("global", "local"):
        key = f"{family}BasePositiveOrientationWinding"
        require(expect_int(decisions[key], f"certificate.decisions.{key}") == 1,
                f"primary {family} base winding decision is not one")
    global_reported = require_ball_agreement(decisions["globalMinimumAbsoluteLower"],
                                             global_minimum,
                                             "certificate.decisions.globalMinimumAbsoluteLower")
    local_reported = require_ball_agreement(decisions["localMinimumAbsoluteLower"],
                                            local_minimum,
                                            "certificate.decisions.localMinimumAbsoluteLower")
    homotopy_reported = {
        family: require_ball_agreement(
            decisions[f"{family}BaseHomotopyMinimumAbsoluteLower"],
            polygons[family]["primaryMinimum"],
            f"certificate.decisions.{family}BaseHomotopyMinimumAbsoluteLower",
        )
        for family in ("global", "local")
    }
    require(global_reported.lower() > 0 and local_reported.lower() > 0
            and all(value.lower() > 0 for value in homotopy_reported.values()),
            "at least one primary decision margin is not strictly positive")
    return {
        "globalMinimum": global_minimum,
        "localMinimum": local_minimum,
        "polygons": polygons,
        "source": certificate_source,
    }


def natural_box_spot_check_design(
    config: dict[str, Any], source_digest: str
) -> dict[str, Any]:
    """Return a deterministic independent recomputation design; do not run it."""
    left = Fraction(config["global"]["boundary"]["left"])
    outer = Fraction(config["global"]["boundary"]["outer"])
    maximum_d = Fraction(1, 450)
    global_imaginary_centers = [fraction_text(Fraction(k, 4) * outer)
                                for k in range(-4, 5)]
    d_centers = ["0/1", fraction_text(maximum_d / 2), fraction_text(maximum_d)]
    local_angles = [fraction_text(Fraction(k, 4)) for k in range(8)]
    deterministic_selectors = []
    for index in range(32):
        block = hashlib.sha256(
            f"{source_digest}:natural-box:{index}".encode("ascii")
        ).digest()
        deterministic_selectors.append({
            "ordinal": index,
            "panelSelector": int.from_bytes(block[0:4], "big"),
            "dCellSelector": int.from_bytes(block[4:8], "big"),
            "sCellSelector": int.from_bytes(block[8:12], "big"),
        })
    return {
        "status": "design-only-not-executed",
        "purpose": (
            "algorithmically distinct corroboration by integrating directly over "
            "small physical (d, lambda) boxes, without Chebyshev reconstruction"
        ),
        "independenceRequirements": [
            "new direct interval monodromy implementation with no primary imports",
            "Taylor order 14, 120 decimal digits",
            "2048 steps on global boxes and 1024 steps on local boxes",
            "fresh Picard tube and normalized Taylor remainder checks for every step",
            "record denominator lower bounds and componentwise tube slack",
        ],
        "mandatoryGlobalLeftBoxes": {
            "lambdaReal": fraction_text(left),
            "lambdaImaginaryCenters": global_imaginary_centers,
            "imaginaryHalfWidth": fraction_text(outer / (2 ** 14)),
            "dCenters": d_centers,
            "dHalfWidthBeforeEndpointClipping": fraction_text(maximum_d / (2 ** 16)),
            "boxCount": 27,
        },
        "mandatoryLocalCircleBoxes": {
            "thetaCentersInUnitsOfPi": local_angles,
            "thetaHalfWidthInUnitsOfPi": fraction_text(Fraction(1, 2 ** 14)),
            "dCenters": d_centers,
            "dHalfWidthBeforeEndpointClipping": fraction_text(maximum_d / (2 ** 16)),
            "boxCount": 24,
        },
        "hashSelectedPrimarySubdivisionBoxes": {
            "selectionSeed": source_digest,
            "count": 32,
            "selectors": deterministic_selectors,
            "mappingRule": (
                "reduce selectors modulo the ordered panel count and that panel's "
                "configured dyadic d/s cell counts"
            ),
        },
        "totalBoxes": 83,
        "maximumValidatedOdeSteps": 145408,
        "conservativeResourceEstimate": {
            "cpuWallTime": "5-30 minutes with 16 CPU workers; 0.5-3 CPU-hours",
            "peakMemory": "below 4 GiB if workers serialize only final boxes",
            "gpuOrDgx": (
                "Arb is CPU arbitrary-precision arithmetic; DGX GPU use is not expected "
                "to help unless a separately audited GPU interval kernel is written"
            ),
        },
        "acceptance": (
            "every direct natural-box Evans enclosure and every Picard audit margin "
            "is strictly separated from zero"
        ),
        "interpretation": (
            "success is corroborative only; 83 spot boxes do not cover either full "
            "contour and cannot replace the uniform certificate"
        ),
    }


def limitation_record() -> dict[str, Any]:
    return {
        "classification": "independent-postprocessing-from-shared-raw-grid",
        "independentlyReimplemented": [
            "configuration, source-ledger, and full tensor-grid validation",
            "direct two-dimensional Chebyshev DCT and node reconstruction check",
            "reverse-order d-then-s interval Clenshaw on complete exact dyadic covers",
            "ellipse majorants, Lebesgue bounds, and interpolation remainders",
            "all primary range-box and decision-margin reductions",
            "curve-to-polygon homotopy and exact rational winding",
        ],
        "notIndependentlyEstablished": [
            "the interval monodromy/Picard/Taylor computation that produced raw Evans balls",
            "that each serialized raw Evans ball was evaluated at its declared (d,s) node",
            "the mathematical implementation inside the primary ODE source",
        ],
        "consequence": (
            "this audit can detect post-processing, provenance, completeness, margin, "
            "homotopy, and winding errors, but shared raw values prevent it from being a "
            "fully independent numerical proof"
        ),
    }


def run_audit(
    config_path: Path,
    checkpoint_path: Path,
    certificate_path: Path,
    audit_dps: int | None,
) -> dict[str, Any]:
    require(config_path.is_file(), f"configuration file missing: {config_path}")
    require(checkpoint_path.is_file(), f"checkpoint file missing: {checkpoint_path}")
    require(certificate_path.is_file(), f"primary certificate file missing: {certificate_path}")
    config_bytes = config_path.read_bytes()
    checkpoint_bytes = checkpoint_path.read_bytes()
    certificate_bytes = certificate_path.read_bytes()
    auditor_path = Path(__file__).resolve()
    auditor_bytes = auditor_path.read_bytes()
    require(getattr(flint, "__version__", None) == "0.6.0",
            "runtime python-flint version is not the frozen 0.6.0")
    config = validate_configuration(json.loads(config_bytes.decode("utf-8")))
    precision = audit_dps if audit_dps is not None else max(100, config["dps"] + 20)
    require(type(precision) is int and precision >= config["dps"] + 10,
            "independent audit precision must be at least primary dps + 10")
    ctx.dps = precision
    panels = independent_panel_definitions(config)
    checkpoint = json.loads(checkpoint_bytes.decode("utf-8"))
    checkpoint_audit = validate_checkpoint(checkpoint, config, panels)

    analyses: list[dict[str, Any]] = []
    base_cells: dict[str, list[dict[str, Any]]] = {"global": [], "local": []}
    for panel in panels:
        analysis = independent_panel_analysis(
            config, panel, checkpoint_audit["grids"][panel["id"]]
        )
        analyses.append(analysis)
        base_cells[panel["family"]].extend(analysis["baseCells"])
    independent_global = choose_minimum(
        [analysis["minimum"] for analysis in analyses
         if analysis["panel"]["family"] == "global"],
        "independent global panels",
    )
    independent_local = choose_minimum(
        [analysis["minimum"] for analysis in analyses
         if analysis["panel"]["family"] == "local"],
        "independent local panels",
    )
    independent_polygons = {
        family: independent_base_polygon(family, base_cells[family])
        for family in ("global", "local")
    }

    certificate = json.loads(certificate_bytes.decode("utf-8"))
    primary = validate_primary_certificate(
        certificate, config, checkpoint, checkpoint_audit,
        panels, analyses, base_cells,
    )
    # Refuse a mixed-time audit if any large input or primary source changed
    # while post-processing was in progress.
    require(config_path.read_bytes() == config_bytes,
            "configuration changed during independent audit")
    require(checkpoint_path.read_bytes() == checkpoint_bytes,
            "checkpoint changed during independent audit")
    require(certificate_path.read_bytes() == certificate_bytes,
            "primary certificate changed during independent audit")
    require(auditor_path.read_bytes() == auditor_bytes,
            "independent auditor source changed during its own run")
    validate_source_ledger(checkpoint["sourceLedger"], checkpoint["sourceDigest"])
    validate_source_ledger(
        certificate["sourceLedger"], certificate["sourceDigest"],
        CERTIFICATE_SOURCE_PATHS, "certificate.sourceLedger",
    )
    panel_summaries = [{
        "id": analysis["panel"]["id"],
        "family": analysis["panel"]["family"],
        "cellCount": len(analysis["cellLeaves"]),
        "minimumAbsoluteLower": arb_text(analysis["minimum"]),
        "tensorInterpolationError": arb_text(analysis["tensorError"]),
        "dctGridContainmentChecked": True,
        "rangeMethod": "independent reverse-order d-then-s interval Clenshaw",
        "reverseClenshawCrossCheckPoints": 9,
        "maximumExtraDyadicDepth": analysis["maximumExtraDepth"],
        "exactCoveredNormalizedArea": analysis["exactCoveredArea"],
    } for analysis in analyses]
    result = {
        "schemaVersion": AUDIT_SCHEMA,
        "status": "passed",
        "completedAt": utc_now(),
        "classification": "independent-postprocessing-from-shared-raw-grid",
        "sourceDigest": primary["source"]["digest"],
        "inputDigests": {
            "configurationSha256": sha256_bytes(config_bytes),
            "checkpointSha256": sha256_bytes(checkpoint_bytes),
            "primaryCertificateSha256": sha256_bytes(certificate_bytes),
            "independentAuditorSha256": sha256_bytes(auditor_bytes),
        },
        "environment": {
            "python": platform.python_version(),
            "pythonImplementation": platform.python_implementation(),
            "arithmetic": "python-flint Arb/Acb ball arithmetic",
            "pythonFlintVersion": flint.__version__,
            "auditPrecisionDecimalDigits": precision,
        },
        "validatedInput": {
            "panelCount": len(panels),
            "rawGridPointCount": checkpoint_audit["pointCount"],
            "minimumRayleighDenominatorLower": arb_text(
                checkpoint_audit["minimumDenominator"]
            ),
            "minimumPicardComponentSlack": arb_text(checkpoint_audit["minimumSlack"]),
            "maximumPicardInflationAttempt": checkpoint_audit["maximumAttempt"],
            "sourceLedgerCurrentAndComplete": True,
            "configCheckpointCertificateIdentical": True,
            "gridIndexLatticesComplete": True,
        },
        "independentDecisions": {
            "globalBoundaryNonzeroForAllD": True,
            "globalMinimumAbsoluteLower": arb_text(independent_global),
            "localBoundaryNonzeroForAllD": True,
            "localMinimumAbsoluteLower": arb_text(independent_local),
            "globalBasePositiveOrientationWinding":
                independent_polygons["global"]["winding"]["winding"],
            "globalBaseHomotopyMinimumAbsoluteLower": arb_text(
                independent_polygons["global"]["minimum"]
            ),
            "localBasePositiveOrientationWinding":
                independent_polygons["local"]["winding"]["winding"],
            "localBaseHomotopyMinimumAbsoluteLower": arb_text(
                independent_polygons["local"]["minimum"]
            ),
        },
        "primaryDecisionReaudit": {
            "allSerializedBoxesRemainStrictlyNonzero": True,
            "allPrimaryOrderCellsIndependentlyReplayedAndContainedBySerializedBoxes": True,
            "globalMinimumAbsoluteLower": arb_text(primary["globalMinimum"]),
            "localMinimumAbsoluteLower": arb_text(primary["localMinimum"]),
            "globalBasePositiveOrientationWinding":
                primary["polygons"]["global"]["winding"],
            "globalBaseHomotopyMinimumAbsoluteLower": arb_text(
                primary["polygons"]["global"]["primaryMinimum"]
            ),
            "globalIndependentCurveToPrimaryPolygonMinimumAbsoluteLower": arb_text(
                primary["polygons"]["global"]["independentToPrimaryMinimum"]
            ),
            "localBasePositiveOrientationWinding":
                primary["polygons"]["local"]["winding"],
            "localBaseHomotopyMinimumAbsoluteLower": arb_text(
                primary["polygons"]["local"]["primaryMinimum"]
            ),
            "localIndependentCurveToPrimaryPolygonMinimumAbsoluteLower": arb_text(
                primary["polygons"]["local"]["independentToPrimaryMinimum"]
            ),
        },
        "panels": panel_summaries,
        "limitations": limitation_record(),
        "naturalBoxSpotCheck": natural_box_spot_check_design(
            config, checkpoint_audit["source"]["digest"]
        ),
    }
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HERE / "config.json")
    parser.add_argument("--checkpoint", type=Path,
                        default=HERE / "contour_grid_checkpoint.json")
    parser.add_argument("--primary-certificate", type=Path,
                        default=HERE / "contour_certificate.json")
    parser.add_argument("--output", type=Path,
                        default=HERE / "independent_validation.json")
    parser.add_argument(
        "--audit-dps", type=int, default=None,
        help="audit precision; default is max(100, primary dps + 20)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        result = run_audit(
            args.config.resolve(), args.checkpoint.resolve(),
            args.primary_certificate.resolve(), args.audit_dps,
        )
    except Exception as error:
        failure = {
            "schemaVersion": AUDIT_SCHEMA,
            "status": "failed",
            "completedAt": utc_now(),
            "errorType": type(error).__name__,
            "error": str(error),
            "limitations": limitation_record(),
            "naturalBoxSpotCheck": {
                "status": "not-generated-because-input-validation-failed",
                "interpretation": "no recomputation was attempted",
            },
        }
        atomic_json(args.output.resolve(), failure)
        print(canonical_json(failure), end="")
        raise SystemExit(1)
    atomic_json(args.output.resolve(), result)
    print(canonical_json({
        "status": result["status"],
        "output": str(args.output.resolve()),
        "classification": result["classification"],
        "independentDecisions": result["independentDecisions"],
        "primaryDecisionReaudit": result["primaryDecisionReaudit"],
    }), end="")


if __name__ == "__main__":
    main()
