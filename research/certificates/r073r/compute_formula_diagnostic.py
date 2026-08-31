#!/usr/bin/env python3
"""Produce the R0.73R matched-phase finite Fourier diagnostic."""

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
from typing import Any, Iterable


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
    parser.add_argument("--output-dir", default=str(HERE))
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
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hash_object(value: object) -> str:
    return hashlib.sha256(compact(value)).hexdigest()


def binding(path: Path) -> dict[str, object]:
    return {
        "bytes": path.stat().st_size,
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
    }


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rss_mib() -> float:
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return raw / (1024.0 * 1024.0) if sys.platform == "darwin" else raw / 1024.0


class Monitor:
    def __init__(self, output: Path) -> None:
        self.progress = output / "progress.ndjson"
        self.resources = output / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        now = utc_now()
        elapsed = time.monotonic() - START
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "elapsedSeconds": elapsed,
                "producer": "recursive-polynomial-convolution",
                "stage": stage,
                "timestampUtc": now,
                **fields,
            }, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({
                "elapsedSeconds": elapsed,
                "executionHost": platform.node(),
                "gpu": "not used",
                "maximumResidentSetMiB": rss_mib(),
                "processes": 1,
                "producer": "recursive-polynomial-convolution",
                "stage": stage,
                "threadsPerProcess": 1,
                "timestampUtc": now,
            }, sort_keys=True) + "\n")


def check(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


def convolve(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a_value in enumerate(left):
        for j, b_value in enumerate(right):
            result[i + j] += a_value * b_value
    return result


def sixth_moment(coefficients: list[int]) -> int:
    cube = convolve(convolve(coefficients, coefficients), coefficients)
    return sum(value * value for value in cube)


def rudin_shapiro_pair(exponent: int) -> tuple[list[int], list[int]]:
    p_values = [1]
    q_values = [1]
    for _ in range(exponent):
        old_p = p_values
        old_q = q_values
        p_values = old_p + old_q
        q_values = old_p + [-value for value in old_q]
    return p_values, q_values


def combined_autocorrelation(p_values: list[int], q_values: list[int], lag: int) -> int:
    total = 0
    length = len(p_values)
    for index in range(length):
        shifted = index + lag
        if 0 <= shifted < length:
            total += p_values[shifted] * p_values[index]
            total += q_values[shifted] * q_values[index]
    return total


def support_records(m_value: int, carrier: int, coefficients: list[int]) -> tuple[list[list[object]], list[list[object]], list[list[object]]]:
    magnitude = str(Fraction(1, 2 * m_value * m_value))
    support: list[list[object]] = []
    magnitudes: list[list[object]] = []
    signed: list[list[object]] = []
    for q_value, q_sign in enumerate(coefficients):
        for s_value, s_sign in enumerate(coefficients):
            sign = q_sign * s_sign
            for orientation in (1, -1):
                site = [orientation * (carrier + q_value), orientation * s_value, 0]
                support.append(site)
                magnitudes.append([*site, magnitude])
                signed.append([*site, sign])
    support.sort()
    magnitudes.sort()
    signed.sort()
    return support, magnitudes, signed


def hhalf_squared(m_value: int, carrier: int) -> float:
    radial_sum = 0.0
    for q_value in range(m_value):
        for s_value in range(m_value):
            radial_sum += math.hypot(carrier + q_value, s_value)
    return radial_sum / float(m_value * m_value)


def blank_row(index: int) -> dict[str, str]:
    row = {field: "" for field in CSV_FIELDS}
    row["record_type"] = "matched_phase_family"
    row["sample_index"] = str(index)
    return row


def endpoint_slope(values: Iterable[tuple[int, float]]) -> float:
    pairs = list(values)
    first_m, first_value = pairs[0]
    last_m, last_value = pairs[-1]
    return math.log(last_value / first_value) / math.log(last_m / first_m)


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    output = Path(args.output_dir).resolve()
    require(output == HERE, "output directory must be the canonical R0.73R package")
    config = load_json(config_path)
    require(config.get("schemaVersion") == "r073r-matched-phase-shell-config-v1", "config schema drift")
    require(config.get("release") == "R0.73R", "release drift")
    monitor = Monitor(output)
    monitor.event("producer-start")

    checks: list[dict[str, object]] = []
    rows: list[dict[str, str]] = []
    comparisons: list[dict[str, object]] = []
    claim = config["claimBoundary"]
    check(
        checks,
        "claim-boundary-finite-only",
        claim.get("finiteFormulaDiagnosticOnly") is True
        and claim.get("heatFlowIntegralComputed") is False
        and claim.get("intervalArithmeticUsed") is False
        and claim.get("annularHeatProxyIsExactHeatNorm") is False
        and claim.get("navierStokesSimulation") is False
        and claim.get("clayProblemSolved") is False,
    )

    grid = config["familyGrid"]
    minimum = int(grid["minimumExponent"])
    maximum = int(grid["maximumExponent"])
    radix = int(grid["radix"])
    carrier_multiplier = int(grid["carrierMultiplier"])
    require(radix == 2, "Rudin--Shapiro grid radix must be two")
    require(carrier_multiplier >= 8, "carrier no-alias margin drift")
    family_series: dict[str, dict[str, list[tuple[int, float]]]] = {
        "D": {"proxy": [], "scaledProxy": []},
        "RS": {"proxy": [], "scaledProxy": []},
    }
    ratio_series: list[tuple[int, float]] = []

    for exponent in range(minimum, maximum + 1):
        m_value = radix**exponent
        carrier = carrier_multiplier * m_value
        p_values, q_values = rudin_shapiro_pair(exponent)
        d_values = [1] * m_value
        check(checks, f"m-{m_value}-rs-length", len(p_values) == m_value and len(q_values) == m_value)
        check(checks, f"m-{m_value}-rs-signs", set(p_values + q_values) <= {-1, 1})
        check(checks, f"m-{m_value}-carrier-separation", carrier > 6 * (m_value - 1))

        energy_values = {
            lag: combined_autocorrelation(p_values, q_values, lag)
            for lag in range(-(m_value - 1), m_value)
        }
        energy_pass = all(
            value == (2 * m_value if lag == 0 else 0)
            for lag, value in energy_values.items()
        )
        check(checks, f"m-{m_value}-rs-energy-identity", energy_pass)

        family_outputs: dict[str, dict[str, object]] = {}
        for family, coefficients in (("D", d_values), ("RS", p_values)):
            support, magnitudes, signed = support_records(m_value, carrier, coefficients)
            support_size = len(support)
            coefficient_magnitude_squared = Fraction(1, 2 * m_value * m_value)
            l2_square = coefficient_magnitude_squared * support_size
            univariate_sixth = sixth_moment(coefficients)
            field_sixth = Fraction(5 * univariate_sixth * univariate_sixth, 2 * m_value**6)
            field_l6 = float(field_sixth) ** (1.0 / 6.0)
            hhalf_square = hhalf_squared(m_value, carrier)
            hhalf_norm = math.sqrt(hhalf_square)
            proxy = field_l6 / math.sqrt(carrier)
            alpha = math.sqrt(carrier) * m_value ** (-2.0 / 3.0)
            scaled_proxy = alpha * proxy
            support_hash = hash_object(support)
            magnitude_hash = hash_object(magnitudes)
            signed_hash = hash_object(signed)

            check(checks, f"m-{m_value}-{family}-support-size", support_size == 2 * m_value * m_value)
            check(checks, f"m-{m_value}-{family}-l2-exact", l2_square == 1, value=str(l2_square))
            check(checks, f"m-{m_value}-{family}-sixth-positive", field_sixth > 0)
            if family == "D":
                formula = Fraction(11 * m_value**5 + 5 * m_value**3 + 4 * m_value, 20)
                check(
                    checks,
                    f"m-{m_value}-dirichlet-sixth-formula",
                    univariate_sixth == formula,
                    direct=str(univariate_sixth),
                    formula=str(formula),
                )
            else:
                check(
                    checks,
                    f"m-{m_value}-rs-field-l6-bounds",
                    Fraction(1, 1) <= field_sixth <= Fraction(40, 1),
                    value=str(field_sixth),
                )

            row = blank_row(len(rows))
            row.update({
                "r": str(exponent),
                "m": str(m_value),
                "N": str(carrier),
                "family": family,
                "support_size": str(support_size),
                "coefficient_magnitude_squared": str(coefficient_magnitude_squared),
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
                "scaled_annular_heat_proxy": format(scaled_proxy, ".17g"),
                "support_sha256": support_hash,
                "magnitude_sha256": magnitude_hash,
                "signed_coefficient_sha256": signed_hash,
            })
            rows.append(row)
            family_series[family]["proxy"].append((m_value, proxy))
            family_series[family]["scaledProxy"].append((m_value, scaled_proxy))
            family_outputs[family] = {
                "fieldL6Norm": field_l6,
                "hhalfSquared": hhalf_square,
                "magnitudeSha256": magnitude_hash,
                "signedCoefficientSha256": signed_hash,
                "supportSha256": support_hash,
            }

        matched = (
            family_outputs["D"]["supportSha256"] == family_outputs["RS"]["supportSha256"]
            and family_outputs["D"]["magnitudeSha256"] == family_outputs["RS"]["magnitudeSha256"]
            and family_outputs["D"]["hhalfSquared"] == family_outputs["RS"]["hhalfSquared"]
        )
        signatures_equal = (
            family_outputs["D"]["signedCoefficientSha256"]
            == family_outputs["RS"]["signedCoefficientSha256"]
        )
        signed_pattern_expected = signatures_equal if m_value <= 2 else not signatures_equal
        check(checks, f"m-{m_value}-matched-support-magnitude", matched)
        check(checks, f"m-{m_value}-phase-signature-pattern", signed_pattern_expected)
        ratio = float(family_outputs["D"]["fieldL6Norm"]) / float(family_outputs["RS"]["fieldL6Norm"])
        ratio_series.append((m_value, ratio))
        comparisons.append({
            "N": carrier,
            "l6RatioDOverRS": ratio,
            "m": m_value,
            "matchedHhalf": True,
            "matchedL2": True,
            "matchedMagnitudes": True,
            "matchedSupport": True,
        })
        monitor.event("family-complete", m=m_value, rows=len(rows))

    csv_path = output / "source-data.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    slopes = {
        "DAnnularHeatProxy": endpoint_slope(family_series["D"]["proxy"]),
        "DScaledAnnularHeatProxy": endpoint_slope(family_series["D"]["scaledProxy"]),
        "L6RatioDOverRS": endpoint_slope(ratio_series),
        "RSAnnularHeatProxy": endpoint_slope(family_series["RS"]["proxy"]),
        "RSScaledAnnularHeatProxy": endpoint_slope(family_series["RS"]["scaledProxy"]),
    }
    check(checks, "all-primary-checks-pass", all(item["pass"] for item in checks))

    environment = {
        "execution": {"gpu": "not used", "processes": 1, "threadsPerProcess": 1},
        "platform": platform.platform(),
        "pythonExecutable": sys.executable,
        "pythonImplementation": platform.python_implementation(),
        "pythonVersion": platform.python_version(),
        "release": "R0.73R",
        "schemaVersion": "r073r-matched-phase-shell-environment-v1",
        "standardLibraryOnly": True,
    }
    environment_path = output / "environment.json"
    environment_path.write_text(canonical(environment), encoding="utf-8")
    monitor.event("producer-outputs-written", checks=len(checks), rows=len(rows))

    all_pass = all(item["pass"] for item in checks)
    diagnostic = {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "comparisons": comparisons,
        "exactStatements": {
            "coefficientMagnitudeSquared": "1/(2*m^2)",
            "dirichletUnivariateL6Sixth": "(11*m^5+5*m^3+4*m)/20",
            "fieldL2Squared": "1",
            "fieldL6Sixth": "5*S_R^2/(2*m^6)",
            "supportSize": "2*m^2",
        },
        "inputBindings": {"config": binding(config_path)},
        "release": "R0.73R",
        "rowCount": len(rows),
        "scalingEndpointSlopes": slopes,
        "theoreticalScalingExponentsInM": {
            "DAnnularHeatProxy": "1/6",
            "DFieldL6": "2/3",
            "DOverRSL6Ratio": "2/3",
            "RSAnnularHeatProxy": "-1/2",
            "RSFieldL6": "0 (two-sided bounded)",
            "alpha": "-1/6",
            "commonHhalf": "1/2",
            "scaledDAnnularHeatProxy": "0",
            "scaledHhalf": "1/3",
            "scaledRSAnnularHeatProxy": "-2/3"
        },
        "schemaVersion": "r073r-matched-phase-shell-diagnostic-v1",
        "sourceDataBinding": binding(csv_path),
    }
    diagnostic_path = output / "diagnostic.json"
    diagnostic_path.write_text(canonical(diagnostic), encoding="utf-8")
    require(all_pass, "one or more primary checks failed")
    print(canonical({
        "allChecksPass": True,
        "checks": len(checks),
        "rows": len(rows),
        "scalingEndpointSlopes": slopes,
    }), end="")


if __name__ == "__main__":
    main()
