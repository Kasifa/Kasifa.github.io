#!/usr/bin/env python3
"""Independently rebuild the R0.73R matched-phase shell formulas.

This validator does not import or execute the producer.  Rudin--Shapiro signs
come from the binary overlapping-11 rule, and sixth moments come from a direct
ordered-triple enumeration rather than polynomial convolution.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import platform
import resource
import sys
import time
from typing import Any


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
START = time.monotonic()
CSV_FIELDS = (
    "record_type",
    "sample_index",
    "r",
    "m",
    "N",
    "family",
    "support_size",
    "coefficient_magnitude_squared",
    "l2_squared",
    "univariate_l6_sixth",
    "field_l6_sixth",
    "field_l6_norm",
    "hhalf_squared",
    "hhalf_norm",
    "annular_heat_proxy",
    "alpha",
    "scaled_l2_norm",
    "scaled_hhalf_norm",
    "scaled_annular_heat_proxy",
    "support_sha256",
    "magnitude_sha256",
    "signed_coefficient_sha256",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--reference", default=str(HERE / "diagnostic.json"))
    parser.add_argument("--source-data", default=str(HERE / "source-data.csv"))
    parser.add_argument("--output", default=str(HERE / "independent_validation.json"))
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def compact(value: object) -> bytes:
    return json.dumps(value, separators=(",", ":"), sort_keys=True).encode("utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict[str, Any]:
    require(path.is_file() and not path.is_symlink(), "missing regular JSON: " + str(path))
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), "JSON root is not an object: " + str(path))
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def hash_object(value: object) -> str:
    return hashlib.sha256(compact(value)).hexdigest()


def binding(path: Path) -> dict[str, object]:
    return {
        "bytes": path.stat().st_size,
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
    }


def relative_error(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1e-300)
    return abs(left - right) / scale


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_monitor(stage: str, **fields: object) -> None:
    now = utc_now()
    elapsed = time.monotonic() - START
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss = raw / (1024.0 * 1024.0) if sys.platform == "darwin" else raw / 1024.0
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "elapsedSeconds": elapsed,
            "stage": stage,
            "timestampUtc": now,
            "validator": "binary-parity-direct-triples",
            **fields,
        }, sort_keys=True) + "\n")
    with (HERE / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "elapsedSeconds": elapsed,
            "executionHost": platform.node(),
            "gpu": "not used",
            "maximumResidentSetMiB": rss,
            "processes": 1,
            "stage": stage,
            "threadsPerProcess": 1,
            "timestampUtc": now,
            "validator": "binary-parity-direct-triples",
        }, sort_keys=True) + "\n")


def add_check(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


def rs_sign(index: int) -> int:
    overlapping_pairs = index & (index >> 1)
    return -1 if bin(overlapping_pairs).count("1") % 2 else 1


def rs_coefficients(m_value: int) -> list[int]:
    return [rs_sign(index) for index in range(m_value)]


def rs_q_coefficients(p_values: list[int]) -> list[int]:
    if len(p_values) == 1:
        return [1]
    half = len(p_values) // 2
    return [value if index < half else -value for index, value in enumerate(p_values)]


def direct_sixth_moment(coefficients: list[int]) -> int:
    length = len(coefficients)
    triple_coefficients = [0] * (3 * length - 2)
    for first in range(length):
        for second in range(length):
            pair = coefficients[first] * coefficients[second]
            for third in range(length):
                triple_coefficients[first + second + third] += pair * coefficients[third]
    return sum(value * value for value in triple_coefficients)


def combined_autocorrelation(p_values: list[int], q_values: list[int], lag: int) -> int:
    total = 0
    for first, (p_value, q_value) in enumerate(zip(p_values, q_values)):
        second = first + lag
        if 0 <= second < len(p_values):
            total += p_values[second] * p_value + q_values[second] * q_value
    return total


def support_records(m_value: int, carrier: int, coefficients: list[int]) -> tuple[list[list[object]], list[list[object]], list[list[object]]]:
    magnitude = str(Fraction(1, 2 * m_value * m_value))
    support: list[list[object]] = []
    magnitudes: list[list[object]] = []
    signed: list[list[object]] = []
    for orientation in (-1, 1):
        for first in range(m_value):
            for second in range(m_value):
                site = [orientation * (carrier + first), orientation * second, 0]
                support.append(site)
                magnitudes.append(site + [magnitude])
                signed.append(site + [coefficients[first] * coefficients[second]])
    return sorted(support), sorted(magnitudes), sorted(signed)


def rebuild_row(index: int, exponent: int, family: str, carrier_multiplier: int) -> dict[str, str]:
    m_value = 2**exponent
    carrier = carrier_multiplier * m_value
    coefficients = [1] * m_value if family == "D" else rs_coefficients(m_value)
    support, magnitudes, signed = support_records(m_value, carrier, coefficients)
    support_size = len(support)
    magnitude_square = Fraction(1, 2 * m_value * m_value)
    l2_square = magnitude_square * support_size
    univariate_sixth = direct_sixth_moment(coefficients)

    # Independent derivation of the carrier factor: only the three-H and
    # three-conjugate-H term survives.  Its coefficient is C(6,3)/2^6,
    # while (sqrt(2)/m)^6 is 8/m^6.
    real_part_factor = Fraction(math.comb(6, 3), 2**6)
    amplitude_sixth = Fraction(8, m_value**6)
    field_sixth = real_part_factor * amplitude_sixth * univariate_sixth**2
    field_l6 = float(field_sixth) ** (1.0 / 6.0)
    radial_sum = math.fsum(
        math.sqrt((carrier + first) ** 2 + second**2)
        for first in range(m_value)
        for second in range(m_value)
    )
    hhalf_square = radial_sum / float(m_value * m_value)
    hhalf_norm = math.sqrt(hhalf_square)
    proxy = field_l6 / math.sqrt(carrier)
    alpha = math.sqrt(carrier) / (m_value ** (2.0 / 3.0))

    return {
        "record_type": "matched_phase_family",
        "sample_index": str(index),
        "r": str(exponent),
        "m": str(m_value),
        "N": str(carrier),
        "family": family,
        "support_size": str(support_size),
        "coefficient_magnitude_squared": str(magnitude_square),
        "l2_squared": str(l2_square),
        "univariate_l6_sixth": str(univariate_sixth),
        "field_l6_sixth": str(field_sixth),
        "field_l6_norm": format(field_l6, ".17g"),
        "hhalf_squared": format(hhalf_square, ".17g"),
        "hhalf_norm": format(hhalf_norm, ".17g"),
        "annular_heat_proxy": format(proxy, ".17g"),
        "alpha": format(alpha, ".17g"),
        "scaled_l2_norm": format(alpha, ".17g"),
        "scaled_hhalf_norm": format(alpha * hhalf_norm, ".17g"),
        "scaled_annular_heat_proxy": format(alpha * proxy, ".17g"),
        "support_sha256": hash_object(support),
        "magnitude_sha256": hash_object(magnitudes),
        "signed_coefficient_sha256": hash_object(signed),
    }


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    reference_path = Path(args.reference).resolve()
    source_path = Path(args.source_data).resolve()
    output_path = Path(args.output).resolve()
    require(output_path == HERE / "independent_validation.json", "output path drift")
    config = load_json(config_path)
    reference = load_json(reference_path)
    require(config.get("schemaVersion") == "r073r-matched-phase-shell-config-v1", "config schema drift")
    require(reference.get("schemaVersion") == "r073r-matched-phase-shell-diagnostic-v1", "reference schema drift")
    require(reference.get("allChecksPass") is True, "primary diagnostic did not pass")
    append_monitor("independent-start")

    with source_path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "source-data schema drift")
        actual_rows = list(reader)

    grid = config["familyGrid"]
    minimum = int(grid["minimumExponent"])
    maximum = int(grid["maximumExponent"])
    multiplier = int(grid["carrierMultiplier"])
    expected_rows: list[dict[str, str]] = []
    for exponent in range(minimum, maximum + 1):
        for family in ("D", "RS"):
            expected_rows.append(rebuild_row(len(expected_rows), exponent, family, multiplier))
    require(len(actual_rows) == len(expected_rows), "source-data row-count drift")

    tolerance = float(config["tolerances"]["independentRelative"])
    exact_fields = {
        "record_type", "sample_index", "r", "m", "N", "family",
        "support_size", "coefficient_magnitude_squared", "l2_squared",
        "univariate_l6_sixth", "field_l6_sixth", "support_sha256",
        "magnitude_sha256", "signed_coefficient_sha256",
    }
    float_fields = set(CSV_FIELDS) - exact_fields
    checks: list[dict[str, object]] = []
    add_check(checks, "claim-boundary-exact", reference.get("claimBoundary") == config["claimBoundary"])
    maximum_error = 0.0

    for row_index, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        exact_pass = all(actual[field] == expected[field] for field in exact_fields)
        add_check(checks, f"row-{row_index:02d}-exact-fields", exact_pass)
        row_error = max(
            relative_error(float(actual[field]), float(expected[field]))
            for field in float_fields
        )
        maximum_error = max(maximum_error, row_error)
        add_check(
            checks,
            f"row-{row_index:02d}-float-fields",
            row_error <= tolerance,
            maximumRelativeError=row_error,
        )

    for exponent in range(minimum, maximum + 1):
        m_value = 2**exponent
        p_values = rs_coefficients(m_value)
        q_values = rs_q_coefficients(p_values)
        energy_pass = all(
            combined_autocorrelation(p_values, q_values, lag)
            == (2 * m_value if lag == 0 else 0)
            for lag in range(-(m_value - 1), m_value)
        )
        add_check(checks, f"m-{m_value}-independent-rs-energy", energy_pass)
        dirichlet_direct = direct_sixth_moment([1] * m_value)
        dirichlet_formula = Fraction(11 * m_value**5 + 5 * m_value**3 + 4 * m_value, 20)
        add_check(
            checks,
            f"m-{m_value}-independent-dirichlet-formula",
            dirichlet_direct == dirichlet_formula,
            direct=str(dirichlet_direct),
            formula=str(dirichlet_formula),
        )

    for pair_index in range(0, len(expected_rows), 2):
        d_row = expected_rows[pair_index]
        rs_row = expected_rows[pair_index + 1]
        m_value = int(d_row["m"])
        add_check(
            checks,
            f"m-{m_value}-independent-matched-support-magnitude",
            d_row["support_sha256"] == rs_row["support_sha256"]
            and d_row["magnitude_sha256"] == rs_row["magnitude_sha256"]
            and d_row["l2_squared"] == rs_row["l2_squared"] == "1"
            and d_row["hhalf_squared"] == rs_row["hhalf_squared"],
        )
        signatures_equal = (
            d_row["signed_coefficient_sha256"] == rs_row["signed_coefficient_sha256"]
        )
        add_check(
            checks,
            f"m-{m_value}-independent-phase-signature-pattern",
            signatures_equal if m_value <= 2 else not signatures_equal,
        )

    all_pass = all(item["pass"] for item in checks)
    append_monitor("independent-complete", checks=len(checks), rows=len(expected_rows))
    result = {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": config["claimBoundary"],
        "independentMethod": {
            "carrierMoment": "central binomial term and exact amplitude sixth power",
            "rudinShapiroSigns": "parity of overlapping 11 blocks in the binary index",
            "sixthMoment": "direct enumeration of ordered coefficient triples",
            "sourceImportsProducer": False,
        },
        "inputBindings": {
            "config": binding(config_path),
            "diagnostic": binding(reference_path),
            "sourceData": binding(source_path),
        },
        "maximumRelativeError": maximum_error,
        "release": "R0.73R",
        "rowCount": len(expected_rows),
        "schemaVersion": "r073r-matched-phase-shell-independent-validation-v1",
    }
    output_path.write_text(canonical(result), encoding="utf-8")
    require(all_pass, "one or more independent checks failed")
    print(canonical({
        "allChecksPass": True,
        "checks": len(checks),
        "maximumRelativeError": maximum_error,
        "rows": len(expected_rows),
    }), end="")


if __name__ == "__main__":
    main()
