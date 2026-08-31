#!/usr/bin/env python3
"""Independently reconstruct the R0.73S finite formula records.

This validator never imports the producer.  Rudin--Shapiro signs are built
from the binary overlapping-11 rule, and moments are rebuilt from ordered
sum counts rather than the producer's recursive polynomial convolution.
"""

from __future__ import annotations

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
    "record_type", "family", "parameter", "modes",
    "autocorrelation_support", "difference_set_size",
    "l2_squared", "l4_fourth", "l6_sixth", "autocorrelation_l1",
    "aq_bound", "support_bound", "ratio_to_aq", "scaled_heat_proxy",
)


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
    require(isinstance(value, dict), "JSON root is not an object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def binding(path: Path) -> dict[str, object]:
    return {
        "bytes": path.stat().st_size,
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
    }


def q(value: Fraction | int) -> str:
    return str(Fraction(value))


def add_check(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


def monitor(stage: str, **fields: object) -> None:
    now = datetime.now(timezone.utc).isoformat()
    elapsed = time.monotonic() - START
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss = raw / (1024.0 * 1024.0) if sys.platform == "darwin" else raw / 1024.0
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "elapsedSeconds": elapsed,
            "stage": stage,
            "timestampUtc": now,
            "validator": "ordered-sums-binary-parity",
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
            "validator": "ordered-sums-binary-parity",
        }, sort_keys=True) + "\n")


def ordered_sum_counts(coefficients: list[int], factors: int) -> dict[int, int]:
    counts = {0: 1}
    for _ in range(factors):
        next_counts: dict[int, int] = {}
        for total, weight in counts.items():
            for index, coefficient in enumerate(coefficients):
                next_counts[total + index] = next_counts.get(total + index, 0) + weight * coefficient
        counts = next_counts
    return counts


def moment(coefficients: list[int], exponent: int) -> int:
    return sum(value * value for value in ordered_sum_counts(coefficients, exponent).values())


def pair_difference_counts(coefficients: list[int]) -> dict[int, int]:
    output: dict[int, int] = {}
    for first, first_value in enumerate(coefficients):
        for second, second_value in enumerate(coefficients):
            shift = first - second
            output[shift] = output.get(shift, 0) + first_value * second_value
    return {shift: value for shift, value in output.items() if value}


def pair_sum_counts(coefficients: list[int]) -> dict[int, int]:
    output: dict[int, int] = {}
    for first, first_value in enumerate(coefficients):
        for second, second_value in enumerate(coefficients):
            total = first + second
            output[total] = output.get(total, 0) + first_value * second_value
    return output


def coefficient_difference_size(coefficients: list[int]) -> int:
    support = {index for index, value in enumerate(coefficients) if value != 0}
    return len({left - right for left in support for right in support})


def selected_bound(coefficients: list[int], shifts: set[int]) -> tuple[int, int]:
    correlation = pair_difference_counts(coefficients)
    absolute_correlation = pair_difference_counts([abs(value) for value in coefficients])
    energy = sum(value * value for value in coefficients)
    total_majorant = sum(abs(value) for value in coefficients) ** 2
    exact_a = sum(abs(correlation.get(shift, 0)) for shift in shifts)
    exact_q = sum(correlation.get(shift, 0) ** 2 for shift in shifts)
    tail = total_majorant - sum(absolute_correlation.get(shift, 0) for shift in shifts)
    return exact_a + tail, exact_q + energy * tail


def generic_record(name: str, coefficients: list[int]) -> dict[str, object]:
    correlation = pair_difference_counts(coefficients)
    selected_a, selected_q = selected_bound(coefficients, {0, 1, -1})
    return {
        "autocorrelationL1": sum(abs(value) for value in correlation.values()),
        "autocorrelationSupport": len(correlation),
        "coefficients": coefficients,
        "differenceSet": coefficient_difference_size(coefficients),
        "fourthMoment": moment(coefficients, 2),
        "l2Squared": moment(coefficients, 1),
        "modes": sum(value != 0 for value in coefficients),
        "name": name,
        "selectedA": selected_a,
        "selectedQ": selected_q,
        "sixthMoment": moment(coefficients, 3),
    }


def independent_lift_audit(m_value: int, packet_multiplier: int, outer_multiplier: int) -> dict[str, object]:
    packet = packet_multiplier * m_value
    outer = outer_multiplier * m_value
    positive = {outer} | {outer + packet + offset for offset in range(m_value)}
    frequencies = positive | {-frequency for frequency in positive}
    positive_vector = (0j, 1 + 0j, -1j)
    negative_vector = tuple(value.conjugate() for value in positive_vector)
    vectors = {
        frequency: positive_vector if frequency > 0 else negative_vector
        for frequency in frequencies
    }
    real_conjugacy = all(
        vectors[-frequency] == tuple(value.conjugate() for value in vector)
        for frequency, vector in vectors.items()
    )
    divergence_free = all(vector[0] == 0j for vector in vectors.values())
    inner = lambda left, right: sum(
        left_value * right_value.conjugate()
        for left_value, right_value in zip(left, right)
    )
    # Enumerate the configured support directly, rather than reusing the
    # producer's interval decomposition.  Same-sign pairs survive because
    # <p,p>=2; opposite-sign pairs vanish because <p,conj(p)>=0.
    correlation_support = {
        left - right
        for left in positive
        for right in positive
    }
    cross_differences = {
        left + right
        for left in positive
        for right in positive
    }
    difference_set = correlation_support | cross_differences | {-value for value in cross_differences}
    return {
        "annulusMaxExclusive": max(abs(value) for value in frequencies) + 1,
        "annulusMin": min(abs(value) for value in frequencies),
        "autocorrelationSupport": len(correlation_support),
        "differenceSet": len(difference_set),
        "divergenceFree": divergence_free,
        "modes": len(frequencies),
        "pointwiseMagnitudePolarization": inner(positive_vector, positive_vector) == 2 and inner(positive_vector, negative_vector) == 0,
        "realConjugacy": real_conjugacy,
    }


def mixture_record(m_value: int, packet_multiplier: int, outer_multiplier: int) -> dict[str, object]:
    require(m_value >= 2, "bounded-quartic grid requires m >= 2")
    root = math.isqrt(m_value)
    require(root * root == m_value, "mixture grid drift")
    y = Fraction(1, root)
    fourth_d = Fraction(2 * m_value, 3) + Fraction(1, 3 * m_value)
    sixth_d = Fraction(11 * m_value**2, 20) + Fraction(1, 4) + Fraction(1, 5 * m_value**2)
    gamma = 1 + 2 * y + (fourth_d - 3) * y**2
    theta = (1 - y) ** 3 + 9 * (1 - y) ** 2 * y + 9 * (1 - y) * y**2 * fourth_d + y**3 * sixth_d
    lift = independent_lift_audit(m_value, packet_multiplier, outer_multiplier)
    return {
        "autocorrelationSupport": 4 * m_value - 1,
        "differenceSet": 4 * m_value - 1,
        "fourthMoment": q(gamma),
        "l2Squared": "1",
        "m": m_value,
        "modesComplex": m_value + 1,
        "realAnnulusMaxExclusive": lift["annulusMaxExclusive"],
        "realAnnulusMin": lift["annulusMin"],
        "realAutocorrelationSupport": lift["autocorrelationSupport"],
        "realDifferenceSet": lift["differenceSet"],
        "realDivergenceFree": lift["divergenceFree"],
        "realModes": lift["modes"],
        "realPointwiseMagnitudePolarization": lift["pointwiseMagnitudePolarization"],
        "realConjugacy": lift["realConjugacy"],
        "sixthMoment": q(theta),
    }


def rs_sign(index: int) -> int:
    overlapping_ones = (index & (index >> 1)).bit_count() if hasattr(int, "bit_count") else bin(index & (index >> 1)).count("1")
    return -1 if overlapping_ones % 2 else 1


def matched_record(family: str, exponent: int) -> dict[str, object]:
    m_value = 2**exponent
    coefficients = [1] * m_value if family == "D" else [rs_sign(index) for index in range(m_value)]
    rho = pair_difference_counts(coefficients)
    sigma = pair_sum_counts(coefficients)
    corr_l1 = Fraction(
        sum(abs(value) for value in rho.values()) ** 2
        + sum(abs(value) for value in sigma.values()) ** 2,
        m_value**2,
    )
    fourth_1d = moment(coefficients, 2)
    sixth_1d = moment(coefficients, 3)
    fourth = Fraction(3 * fourth_1d**2, 2 * m_value**4)
    sixth = Fraction(5 * sixth_1d**2, 2 * m_value**6)
    aq = corr_l1 * fourth
    scaled = m_value ** (-2.0 / 3.0) * float(aq) ** (1.0 / 6.0)
    return {
        "aqBound": q(aq),
        "autocorrelationL1": q(corr_l1),
        "autocorrelationSupport": len(rho) ** 2 + 2 * sum(value != 0 for value in sigma.values()) ** 2,
        "differenceSet": 3 * (2 * m_value - 1) ** 2,
        "exponent": exponent,
        "family": family,
        "fourthMoment": q(fourth),
        "m": m_value,
        "modes": 2 * m_value**2,
        "scaledHeatProxy": format(scaled, ".17g"),
        "sixthMoment": q(sixth),
        "univariateFourth": fourth_1d,
        "univariateSixth": sixth_1d,
    }


def no_go_record(depth: int) -> dict[str, object]:
    return {
        "depth": depth,
        "differenceSet": 9**depth,
        "fourthMomentBoth": 37**depth,
        "l2SquaredBoth": 5**depth,
        "modesBoth": 5**depth,
        "normRatio": format((323**depth / 311**depth) ** (1.0 / 6.0), ".17g"),
        "sixthMomentA": 311**depth,
        "sixthMomentB": 323**depth,
    }


def lacunary_product(base_coefficients: list[int], radix: int, depth: int) -> list[int]:
    polynomial = {0: 1}
    for level in range(depth):
        stride = radix**level
        next_polynomial: dict[int, int] = {}
        for exponent, coefficient in polynomial.items():
            for digit, digit_value in enumerate(base_coefficients):
                target = exponent + digit * stride
                next_polynomial[target] = next_polynomial.get(target, 0) + coefficient * digit_value
        polynomial = next_polynomial
    size = max(polynomial) + 1
    return [polynomial.get(index, 0) for index in range(size)]


def main() -> None:
    config_path = HERE / "config.json"
    diagnostic_path = HERE / "diagnostic.json"
    source_path = HERE / "source-data.csv"
    config = load_json(config_path)
    diagnostic = load_json(diagnostic_path)
    monitor("independent-start")
    checks: list[dict[str, object]] = []
    add_check(checks, "config-schema", config.get("schemaVersion") == "r073s-quadratic-autocorrelation-config-v1")
    add_check(checks, "diagnostic-pass", diagnostic.get("allChecksPass") is True)
    add_check(checks, "claim-boundary", diagnostic.get("claimBoundary") == config.get("claimBoundary"))

    generic = [
        generic_record(name, [int(value) for value in raw])
        for name, raw in config["genericSequences"].items()
    ]
    packet_multiplier = int(config["mixtureFamily"]["packetCarrierMultiplier"])
    outer_multiplier = int(config["mixtureFamily"]["outerCarrierMultiplier"])
    mixtures = [
        mixture_record(int(value), packet_multiplier, outer_multiplier)
        for value in config["mixtureFamily"]["mValues"]
    ]
    matched = [
        matched_record(family, exponent)
        for exponent in range(
            int(config["matchedFamily"]["minimumExponent"]),
            int(config["matchedFamily"]["maximumExponent"]) + 1,
        )
        for family in ("D", "RS")
    ]
    no_go = [
        no_go_record(depth)
        for depth in range(1, int(config["rieszNoGo"]["maximumDepth"]) + 1)
    ]
    records = {"generic": generic, "matched": matched, "mixtures": mixtures, "rieszNoGo": no_go}
    record_digest = hashlib.sha256(compact(records)).hexdigest()
    add_check(checks, "records-exact", records == diagnostic.get("records"))
    add_check(checks, "records-digest", record_digest == diagnostic.get("recordsSha256"))

    for record in mixtures:
        m_value = int(record["m"])
        add_check(checks, f"mixture-m{m_value}-carrier-separation-independent", packet_multiplier * m_value > 2 * (m_value - 1))
        add_check(checks, f"mixture-m{m_value}-lift-real-independent", record["realConjugacy"] is True)
        add_check(checks, f"mixture-m{m_value}-lift-divergence-independent", record["realDivergenceFree"] is True)
        add_check(checks, f"mixture-m{m_value}-lift-polarization-independent", record["realPointwiseMagnitudePolarization"] is True)
        add_check(checks, f"mixture-m{m_value}-lift-counts-independent", record["realModes"] == 2 * m_value + 2 and record["realAutocorrelationSupport"] == 4 * m_value - 1 and record["realDifferenceSet"] == 10 * m_value - 1)
        add_check(checks, f"mixture-m{m_value}-lift-annulus-independent", record["realAnnulusMin"] == 32 * m_value and record["realAnnulusMaxExclusive"] == 36 * m_value)

    base_a = [1, -1, -1, -1, 1]
    base_b = [1, -1, -1, -1, -1]
    add_check(checks, "base-direct-moments-A", [moment(base_a, p) for p in (1, 2, 3)] == [5, 37, 311])
    add_check(checks, "base-direct-moments-B", [moment(base_b, p) for p in (1, 2, 3)] == [5, 37, 323])
    radix = int(config["rieszNoGo"]["base"])
    for depth in (2, 3):
        product_a = lacunary_product(base_a, radix, depth)
        product_b = lacunary_product(base_b, radix, depth)
        add_check(checks, f"riesz-depth-{depth}-support", [index for index, value in enumerate(product_a) if value] == [index for index, value in enumerate(product_b) if value])
        add_check(checks, f"riesz-depth-{depth}-magnitudes", [abs(value) for value in product_a] == [abs(value) for value in product_b])
        add_check(checks, f"riesz-depth-{depth}-moments-A", [moment(product_a, p) for p in (1, 2, 3)] == [5**depth, 37**depth, 311**depth])
        add_check(checks, f"riesz-depth-{depth}-moments-B", [moment(product_b, p) for p in (1, 2, 3)] == [5**depth, 37**depth, 323**depth])

    with source_path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        add_check(checks, "source-schema", tuple(reader.fieldnames or ()) == CSV_FIELDS)
        rows = list(reader)
    add_check(checks, "source-row-count", len(rows) == diagnostic.get("rowCount"))
    add_check(checks, "source-binding", diagnostic.get("sourceDataBinding") == binding(source_path))

    all_pass = all(item["pass"] for item in checks)
    result = {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": config["claimBoundary"],
        "inputBindings": {
            "config": binding(config_path),
            "diagnostic": binding(diagnostic_path),
            "sourceData": binding(source_path),
        },
        "recordsSha256": record_digest,
        "release": "R0.73S",
        "rowCount": len(rows),
        "schemaVersion": "r073s-quadratic-autocorrelation-independent-validation-v1",
    }
    output_path = HERE / "independent_validation.json"
    output_path.write_text(canonical(result), encoding="utf-8")
    monitor("independent-complete", allChecksPass=all_pass, checks=len(checks))
    require(all_pass, "one or more independent checks failed")
    print(canonical({
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "recordsSha256": record_digest,
        "rowCount": len(rows),
    }), end="")


if __name__ == "__main__":
    main()
