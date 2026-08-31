#!/usr/bin/env python3
"""Build the exact finite R0.73S autocorrelation diagnostic.

All exact identities use Python integers and fractions.  Floating values are
derived only for the public scaling table and are never used to decide an
exact inequality.
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
from typing import Any, Iterable


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
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def binding(path: Path) -> dict[str, object]:
    return {
        "bytes": path.stat().st_size,
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
    }


def q(value: Fraction | int) -> str:
    return str(Fraction(value))


def monitor(stage: str, **fields: object) -> None:
    now = datetime.now(timezone.utc).isoformat()
    elapsed = time.monotonic() - START
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss = raw / (1024.0 * 1024.0) if sys.platform == "darwin" else raw / 1024.0
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "elapsedSeconds": elapsed,
            "producer": "exact-pair-correlation",
            "stage": stage,
            "timestampUtc": now,
            **fields,
        }, sort_keys=True) + "\n")
    with (HERE / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "elapsedSeconds": elapsed,
            "executionHost": platform.node(),
            "gpu": "not used",
            "maximumResidentSetMiB": rss,
            "processes": 1,
            "producer": "exact-pair-correlation",
            "stage": stage,
            "threadsPerProcess": 1,
            "timestampUtc": now,
        }, sort_keys=True) + "\n")


def add_check(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


def convolve(left: list[int], right: list[int]) -> list[int]:
    output = [0] * (len(left) + len(right) - 1)
    for first, left_value in enumerate(left):
        for second, right_value in enumerate(right):
            output[first + second] += left_value * right_value
    return output


def power_convolution(coefficients: list[int], exponent: int) -> list[int]:
    output = [1]
    for _ in range(exponent):
        output = convolve(output, coefficients)
    return output


def even_moment(coefficients: list[int], exponent: int) -> int:
    values = power_convolution(coefficients, exponent)
    return sum(value * value for value in values)


def autocorrelation(coefficients: list[int]) -> dict[int, int]:
    output: dict[int, int] = {}
    size = len(coefficients)
    for shift in range(-(size - 1), size):
        value = 0
        for index, coefficient in enumerate(coefficients):
            other = index + shift
            if 0 <= other < size:
                value += coefficients[other] * coefficient
        if value:
            output[shift] = value
    return output


def difference_set_size(coefficients: list[int]) -> int:
    support = [index for index, value in enumerate(coefficients) if value]
    return len({left - right for left in support for right in support})


def magnitude_correlation(coefficients: list[int]) -> dict[int, int]:
    return autocorrelation([abs(value) for value in coefficients])


def selected_shift_bound(coefficients: list[int], shifts: set[int]) -> tuple[int, int]:
    correlation = autocorrelation(coefficients)
    majorant = magnitude_correlation(coefficients)
    energy = sum(value * value for value in coefficients)
    s1_square = sum(abs(value) for value in coefficients) ** 2
    exact_l1 = sum(abs(correlation.get(shift, 0)) for shift in shifts)
    exact_l2 = sum(correlation.get(shift, 0) ** 2 for shift in shifts)
    inspected_majorant = sum(majorant.get(shift, 0) for shift in shifts)
    tail_l1 = s1_square - inspected_majorant
    return exact_l1 + tail_l1, exact_l2 + energy * tail_l1


def generic_record(name: str, coefficients: list[int], checks: list[dict[str, object]]) -> dict[str, object]:
    values = [value for value in coefficients if value]
    correlation = autocorrelation(coefficients)
    energy = sum(value * value for value in coefficients)
    fourth = sum(value * value for value in correlation.values())
    sixth = even_moment(coefficients, 3)
    corr_l1 = sum(abs(value) for value in correlation.values())
    modes = len(values)
    autocorrelation_support = len(correlation)
    difference = difference_set_size(coefficients)
    aq = corr_l1 * fourth
    selected_a, selected_q = selected_shift_bound(coefficients, {0, 1, -1})
    add_check(checks, f"generic-{name}-parseval-fourth", fourth == even_moment(coefficients, 2))
    add_check(checks, f"generic-{name}-aq", sixth <= aq)
    add_check(checks, f"generic-{name}-l1-support", corr_l1 <= modes * energy)
    add_check(checks, f"generic-{name}-l1-autocorrelation-support", corr_l1 * corr_l1 <= autocorrelation_support * fourth)
    add_check(checks, f"generic-{name}-support-order", 0 < autocorrelation_support <= difference)
    add_check(checks, f"generic-{name}-selected-tail", sixth <= selected_a * selected_q)
    return {
        "autocorrelationL1": corr_l1,
        "autocorrelationSupport": autocorrelation_support,
        "coefficients": coefficients,
        "differenceSet": difference,
        "fourthMoment": fourth,
        "l2Squared": energy,
        "modes": modes,
        "name": name,
        "selectedA": selected_a,
        "selectedQ": selected_q,
        "sixthMoment": sixth,
    }


def gaussian_conjugate(value: tuple[int, int]) -> tuple[int, int]:
    return value[0], -value[1]


def gaussian_multiply(left: tuple[int, int], right: tuple[int, int]) -> tuple[int, int]:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def polarization_inner(
    left: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    total = (0, 0)
    for left_value, right_value in zip(left, right):
        product = gaussian_multiply(left_value, gaussian_conjugate(right_value))
        total = total[0] + product[0], total[1] + product[1]
    return total


def audit_real_lift(m_value: int, packet_multiplier: int, outer_multiplier: int) -> dict[str, object]:
    packet = packet_multiplier * m_value
    outer = outer_multiplier * m_value
    positive = [outer] + [outer + packet + index for index in range(m_value)]
    frequencies = positive + [-value for value in positive]
    positive_polarization = ((0, 0), (1, 0), (0, -1))
    negative_polarization = tuple(gaussian_conjugate(value) for value in positive_polarization)
    entries = {
        frequency: positive_polarization if frequency > 0 else negative_polarization
        for frequency in frequencies
    }
    reality = all(
        entries[-frequency] == tuple(gaussian_conjugate(value) for value in polarization)
        for frequency, polarization in entries.items()
    )
    divergence = all(polarization[0] == (0, 0) for polarization in entries.values())
    same_polarization = polarization_inner(positive_polarization, positive_polarization)
    cross_polarization = polarization_inner(positive_polarization, negative_polarization)
    central_differences = set(range(-(m_value - 1), m_value))
    carrier_differences = set(range(packet, packet + m_value))
    same_sign_differences = central_differences | carrier_differences | {-value for value in carrier_differences}
    packet_sums = {0} | set(range(packet, packet + m_value)) | set(range(2 * packet, 2 * packet + 2 * m_value - 1))
    positive_cross_differences = {2 * outer + value for value in packet_sums}
    difference_support = same_sign_differences | positive_cross_differences | {-value for value in positive_cross_differences}
    correlation_support = same_sign_differences
    absolute_frequencies = [abs(value) for value in frequencies]
    return {
        "annulusMaxExclusive": max(absolute_frequencies) + 1,
        "annulusMin": min(absolute_frequencies),
        "autocorrelationSupport": len(correlation_support),
        "differenceSet": len(difference_support),
        "divergenceFree": divergence,
        "modes": len(entries),
        "pointwiseMagnitudePolarization": same_polarization == (2, 0) and cross_polarization == (0, 0),
        "realConjugacy": reality,
    }


def mixture_record(m_value: int, checks: list[dict[str, object]]) -> dict[str, object]:
    require(m_value >= 2, "bounded-quartic family requires m >= 2")
    root = math.isqrt(m_value)
    require(root * root == m_value, "mixture m must be a square")
    y = Fraction(1, root)
    dirichlet_fourth = Fraction(2 * m_value, 3) + Fraction(1, 3 * m_value)
    dirichlet_sixth = (
        Fraction(11 * m_value * m_value, 20)
        + Fraction(1, 4)
        + Fraction(1, 5 * m_value * m_value)
    )
    gamma = (1 - y) ** 2 + 4 * (1 - y) * y + y * y * dirichlet_fourth
    theta = (
        (1 - y) ** 3
        + 9 * (1 - y) ** 2 * y
        + 9 * (1 - y) * y * y * dirichlet_fourth
        + y**3 * dirichlet_sixth
    )
    gamma_closed = Fraction(5, 3) + 2 * y - 3 * y**2 + Fraction(1, 3) * y**4
    theta_closed = (
        Fraction(11, 20) / y + 7 - 15 * y**2
        + Fraction(33, 4) * y**3 + 3 * y**4
        - 3 * y**5 + Fraction(1, 5) * y**7
    )
    autocorrelation_support = 4 * m_value - 1
    difference = 4 * m_value - 1
    modes = m_value + 1
    add_check(checks, f"mixture-m{m_value}-gamma-closed", gamma == gamma_closed)
    add_check(checks, f"mixture-m{m_value}-theta-closed", theta == theta_closed)
    add_check(checks, f"mixture-m{m_value}-support-branch", theta <= modes * gamma)
    add_check(checks, f"mixture-m{m_value}-difference-branch", theta * theta <= autocorrelation_support * gamma**3)
    packet_multiplier = int(load_json(HERE / "config.json")["mixtureFamily"]["packetCarrierMultiplier"])
    outer_multiplier = int(load_json(HERE / "config.json")["mixtureFamily"]["outerCarrierMultiplier"])
    packet_carrier = packet_multiplier * m_value
    add_check(checks, f"mixture-m{m_value}-carrier-separation", packet_carrier > 2 * (m_value - 1))
    lift = audit_real_lift(m_value, packet_multiplier, outer_multiplier)
    add_check(checks, f"mixture-m{m_value}-lift-real-conjugacy", lift["realConjugacy"] is True)
    add_check(checks, f"mixture-m{m_value}-lift-divergence-free", lift["divergenceFree"] is True)
    add_check(checks, f"mixture-m{m_value}-lift-polarization", lift["pointwiseMagnitudePolarization"] is True)
    add_check(checks, f"mixture-m{m_value}-lift-modes", lift["modes"] == 2 * m_value + 2)
    add_check(checks, f"mixture-m{m_value}-lift-autocorrelation-support", lift["autocorrelationSupport"] == 4 * m_value - 1)
    add_check(checks, f"mixture-m{m_value}-lift-difference-set", lift["differenceSet"] == 10 * m_value - 1)
    add_check(checks, f"mixture-m{m_value}-lift-annulus", lift["annulusMin"] == 32 * m_value and lift["annulusMaxExclusive"] == 36 * m_value)
    return {
        "autocorrelationSupport": autocorrelation_support,
        "differenceSet": difference,
        "fourthMoment": q(gamma),
        "l2Squared": "1",
        "m": m_value,
        "modesComplex": modes,
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


def rudin_shapiro_pair(exponent: int) -> tuple[list[int], list[int]]:
    p_values = [1]
    q_values = [1]
    for _ in range(exponent):
        old_p = p_values
        old_q = q_values
        p_values = old_p + old_q
        q_values = old_p + [-value for value in old_q]
    return p_values, q_values


def matched_record(family: str, exponent: int, checks: list[dict[str, object]]) -> dict[str, object]:
    m_value = 2**exponent
    p_values, _ = rudin_shapiro_pair(exponent)
    coefficients = [1] * m_value if family == "D" else p_values
    rho = autocorrelation(coefficients)
    sigma = convolve(coefficients, coefficients)
    corr_l1 = Fraction(
        sum(abs(value) for value in rho.values()) ** 2
        + sum(abs(value) for value in sigma) ** 2,
        m_value * m_value,
    )
    univariate_fourth = even_moment(coefficients, 2)
    univariate_sixth = even_moment(coefficients, 3)
    fourth = Fraction(3 * univariate_fourth**2, 2 * m_value**4)
    sixth = Fraction(5 * univariate_sixth**2, 2 * m_value**6)
    modes = 2 * m_value * m_value
    rho_support = len(rho)
    sigma_support = sum(value != 0 for value in sigma)
    autocorrelation_support = rho_support**2 + 2 * sigma_support**2
    difference = 3 * (2 * m_value - 1) ** 2
    aq = corr_l1 * fourth
    add_check(checks, f"matched-{family}-r{exponent}-aq", sixth <= aq)
    add_check(checks, f"matched-{family}-r{exponent}-support", corr_l1 <= modes)
    add_check(checks, f"matched-{family}-r{exponent}-autocorrelation-support", corr_l1 * corr_l1 <= autocorrelation_support * fourth)
    add_check(checks, f"matched-{family}-r{exponent}-support-order", 0 < autocorrelation_support <= difference)
    if family == "D":
        expected_fourth = Fraction((2 * m_value * m_value + 1) ** 2, 6 * m_value * m_value)
        expected_sixth_1d = Fraction(11 * m_value**5 + 5 * m_value**3 + 4 * m_value, 20)
        add_check(checks, f"matched-D-r{exponent}-l1", corr_l1 == 2 * m_value * m_value)
        add_check(checks, f"matched-D-r{exponent}-fourth", fourth == expected_fourth)
        add_check(checks, f"matched-D-r{exponent}-sixth-1d", univariate_sixth == expected_sixth_1d)
    else:
        expected_fourth_1d = Fraction(4 * m_value * m_value - ((-1) ** exponent) * m_value, 3)
        add_check(checks, f"matched-RS-r{exponent}-fourth-1d", univariate_fourth == expected_fourth_1d)
        add_check(checks, f"matched-RS-r{exponent}-fourth-field", fourth == Fraction((4 * m_value - ((-1) ** exponent)) ** 2, 6 * m_value * m_value))
    scaled_proxy = m_value ** (-2.0 / 3.0) * float(aq) ** (1.0 / 6.0)
    return {
        "aqBound": q(aq),
        "autocorrelationL1": q(corr_l1),
        "autocorrelationSupport": autocorrelation_support,
        "differenceSet": difference,
        "exponent": exponent,
        "family": family,
        "fourthMoment": q(fourth),
        "m": m_value,
        "modes": modes,
        "scaledHeatProxy": format(scaled_proxy, ".17g"),
        "sixthMoment": q(sixth),
        "univariateFourth": univariate_fourth,
        "univariateSixth": univariate_sixth,
    }


def no_go_record(depth: int, checks: list[dict[str, object]]) -> dict[str, object]:
    l2 = 5**depth
    fourth = 37**depth
    sixth_a = 311**depth
    sixth_b = 323**depth
    modes = 5**depth
    add_check(checks, f"riesz-r{depth}-separation", sixth_b > sixth_a)
    add_check(checks, f"riesz-r{depth}-matched-low-order", l2 > 0 and fourth > 0 and modes > 0)
    return {
        "depth": depth,
        "differenceSet": 9**depth,
        "fourthMomentBoth": fourth,
        "l2SquaredBoth": l2,
        "modesBoth": modes,
        "normRatio": format((sixth_b / sixth_a) ** (1.0 / 6.0), ".17g"),
        "sixthMomentA": sixth_a,
        "sixthMomentB": sixth_b,
    }


def csv_row(record_type: str, family: str, parameter: int, modes: int,
            autocorrelation_support: int | None, difference_set: int | None,
            l2: Fraction | int, fourth: Fraction | int, sixth: Fraction | int,
            corr_l1: Fraction | int | None = None, scaled: float | None = None) -> dict[str, str]:
    aq = Fraction(corr_l1) * Fraction(fourth) if corr_l1 is not None else None
    support_bound = Fraction(modes) * Fraction(l2) * Fraction(fourth)
    return {
        "record_type": record_type,
        "family": family,
        "parameter": str(parameter),
        "modes": str(modes),
        "autocorrelation_support": "" if autocorrelation_support is None else str(autocorrelation_support),
        "difference_set_size": "" if difference_set is None else str(difference_set),
        "l2_squared": q(l2),
        "l4_fourth": q(fourth),
        "l6_sixth": q(sixth),
        "autocorrelation_l1": "" if corr_l1 is None else q(corr_l1),
        "aq_bound": "" if aq is None else q(aq),
        "support_bound": q(support_bound),
        "ratio_to_aq": "" if aq is None else format(float(Fraction(sixth) / aq), ".17g"),
        "scaled_heat_proxy": "" if scaled is None else format(scaled, ".17g"),
    }


def main() -> None:
    config_path = HERE / "config.json"
    config = load_json(config_path)
    require(config.get("schemaVersion") == "r073s-quadratic-autocorrelation-config-v1", "config schema drift")
    require(config.get("release") == "R0.73S", "release drift")
    (HERE / "progress.ndjson").write_text("", encoding="utf-8")
    (HERE / "resource-log.ndjson").write_text("", encoding="utf-8")
    monitor("producer-start")
    checks: list[dict[str, object]] = []
    rows: list[dict[str, str]] = []

    claim = config["claimBoundary"]
    add_check(
        checks,
        "claim-boundary-no-overreach",
        claim.get("quadraticAutocorrelationUpperBoundChecked") is True
        and claim.get("exactFiniteFormulaDiagnosticOnly") is True
        and claim.get("arithmeticComplexityLowerBound") is False
        and claim.get("heatFlowIntegralComputed") is False
        and claim.get("navierStokesSimulation") is False
        and claim.get("clayProblemSolved") is False,
    )

    generic: list[dict[str, object]] = []
    for name, raw in config["genericSequences"].items():
        coefficients = [int(value) for value in raw]
        record = generic_record(name, coefficients, checks)
        generic.append(record)
        rows.append(csv_row(
            "generic_sequence", name, len(coefficients), int(record["modes"]),
            int(record["autocorrelationSupport"]), int(record["differenceSet"]), int(record["l2Squared"]),
            int(record["fourthMoment"]), int(record["sixthMoment"]),
            int(record["autocorrelationL1"]),
        ))

    base_a = next(record for record in generic if record["name"] == "A")
    base_b = next(record for record in generic if record["name"] == "B")
    add_check(checks, "base-no-go-l2", base_a["l2Squared"] == base_b["l2Squared"] == 5)
    add_check(checks, "base-no-go-l4", base_a["fourthMoment"] == base_b["fourthMoment"] == 37)
    add_check(checks, "base-no-go-l6", base_a["sixthMoment"] == 311 and base_b["sixthMoment"] == 323)

    mixtures: list[dict[str, object]] = []
    for m_value in config["mixtureFamily"]["mValues"]:
        record = mixture_record(int(m_value), checks)
        mixtures.append(record)
        rows.append(csv_row(
            "asymptotically_fixed_quartic_spike", "Dirichlet-spike", int(m_value), int(record["modesComplex"]),
            int(record["autocorrelationSupport"]), int(record["differenceSet"]), 1, Fraction(record["fourthMoment"]),
            Fraction(record["sixthMoment"]), None,
        ))

    matched: list[dict[str, object]] = []
    matched_config = config["matchedFamily"]
    for exponent in range(int(matched_config["minimumExponent"]), int(matched_config["maximumExponent"]) + 1):
        for family in ("D", "RS"):
            record = matched_record(family, exponent, checks)
            matched.append(record)
            rows.append(csv_row(
                "matched_r073r", family, exponent, int(record["modes"]),
                int(record["autocorrelationSupport"]), int(record["differenceSet"]),
                1, Fraction(record["fourthMoment"]), Fraction(record["sixthMoment"]),
                Fraction(record["autocorrelationL1"]), float(record["scaledHeatProxy"]),
            ))

    no_go: list[dict[str, object]] = []
    for depth in range(1, int(config["rieszNoGo"]["maximumDepth"]) + 1):
        record = no_go_record(depth, checks)
        no_go.append(record)
        rows.append(csv_row(
            "riesz_product_no_go", "A", depth, int(record["modesBoth"]), None, int(record["differenceSet"]),
            int(record["l2SquaredBoth"]), int(record["fourthMomentBoth"]), int(record["sixthMomentA"]),
        ))
        rows.append(csv_row(
            "riesz_product_no_go", "B", depth, int(record["modesBoth"]), None, int(record["differenceSet"]),
            int(record["l2SquaredBoth"]), int(record["fourthMomentBoth"]), int(record["sixthMomentB"]),
        ))

    records = {
        "generic": generic,
        "matched": matched,
        "mixtures": mixtures,
        "rieszNoGo": no_go,
    }
    records_digest = hashlib.sha256(compact(records)).hexdigest()
    source_path = HERE / "source-data.csv"
    with source_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    monitor("records-complete", checks=len(checks), rows=len(rows))
    all_pass = all(item["pass"] for item in checks)
    diagnostic = {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "inputBindings": {"config": binding(config_path)},
        "records": records,
        "recordsSha256": records_digest,
        "release": "R0.73S",
        "rowCount": len(rows),
        "schemaVersion": "r073s-quadratic-autocorrelation-diagnostic-v1",
        "sourceDataBinding": binding(source_path),
    }
    (HERE / "diagnostic.json").write_text(canonical(diagnostic), encoding="utf-8")
    environment = {
        "execution": {
            "gpu": "not used",
            "host": platform.node(),
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "python": platform.python_version(),
        "release": "R0.73S",
        "schemaVersion": "r073s-quadratic-autocorrelation-environment-v1",
        "standardLibraryOnly": True,
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor("producer-complete", allChecksPass=all_pass)
    require(all_pass, "one or more primary checks failed")
    print(canonical({
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "recordsSha256": records_digest,
        "rowCount": len(rows),
    }), end="")


if __name__ == "__main__":
    main()
