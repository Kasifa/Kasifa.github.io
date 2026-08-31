#!/usr/bin/env python3
"""Produce the R0.73Q finite heat-flow formula diagnostic."""

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
    "j",
    "N",
    "amplitude",
    "l2_norm",
    "heat_l4_l6_norm",
    "hhalf_norm",
    "expected_l2_norm",
    "expected_heat_l4_l6_norm",
    "expected_hhalf_norm",
    "n",
    "g_l4_fourth_power",
    "g_l4_norm",
    "fractional_value",
    "expected_fractional_value",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default=str(HERE / "config.json"))
    parser.add_argument("--output-dir", default=str(HERE))
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def binding(path: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def relative_error(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1e-300)
    return abs(left - right) / scale


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
        progress = {
            "elapsedSeconds": elapsed,
            "producer": "direct-fourier-heat-integral",
            "stage": stage,
            "timestampUtc": now,
            **fields,
        }
        resources = {
            "elapsedSeconds": elapsed,
            "executionHost": platform.node(),
            "gpu": "not used",
            "maximumResidentSetMiB": rss_mib(),
            "processes": 1,
            "producer": "direct-fourier-heat-integral",
            "stage": stage,
            "threadsPerProcess": 1,
            "timestampUtc": now,
        }
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(progress, sort_keys=True) + "\n")
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(resources, sort_keys=True) + "\n")


def blank_row(kind: str, index: int) -> dict[str, str]:
    row = {field: "" for field in CSV_FIELDS}
    row["record_type"] = kind
    row["sample_index"] = str(index)
    return row


def check(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    output = Path(args.output_dir).resolve()
    require(output == HERE, "output directory must be the canonical R0.73Q package")
    config = load_json(config_path)
    require(config.get("schemaVersion") == "r073q-finite-heat-flow-config-v1", "config schema drift")
    require(config.get("release") == "R0.73Q", "release drift")
    monitor = Monitor(output)
    monitor.event("producer-start")

    checks: list[dict[str, object]] = []
    rows: list[dict[str, str]] = []
    tolerance = float(config["tolerances"]["producerRelative"])
    claim = config["claimBoundary"]
    check(
        checks,
        "claim-boundary-finite-only",
        claim.get("finiteFormulaDiagnosticOnly") is True
        and claim.get("navierStokesSimulation") is False
        and claim.get("pdeEvolutionComputed") is False
        and claim.get("clayProblemSolved") is False,
    )

    moment = Fraction(1, 1)
    for odd, even in ((1, 2), (3, 4), (5, 6)):
        moment *= Fraction(odd, even)
    configured_moment = Fraction(
        int(config["trigonometricMoment"]["valueNumerator"]),
        int(config["trigonometricMoment"]["valueDenominator"]),
    )
    c6 = float(moment) ** (1.0 / 6.0)
    check(checks, "sin-sixth-moment-exact", moment == configured_moment, value=str(moment))
    check(
        checks,
        "c6-sixth-power",
        relative_error(c6**6, 5.0 / 16.0) <= tolerance,
        relativeError=relative_error(c6**6, 5.0 / 16.0),
    )

    grid = config["modeGrid"]
    minimum = int(grid["minimumExponent"])
    maximum = int(grid["maximumExponent"])
    radix = int(grid["radix"])
    amplitude_power = float(grid["amplitudePower"])
    l2_errors: list[float] = []
    heat_errors: list[float] = []
    hhalf_errors: list[float] = []
    for index, exponent in enumerate(range(minimum, maximum + 1)):
        frequency = radix**exponent
        amplitude = math.exp(amplitude_power * math.log(frequency)) if frequency > 1 else 1.0

        # Direct Fourier coefficient calculation: the two coefficients have
        # modulus amplitude/2.
        l2_norm = math.sqrt(2.0 * (amplitude / 2.0) ** 2)
        hhalf_norm = math.sqrt(2.0 * frequency * (amplitude / 2.0) ** 2)
        l6_norm = amplitude * c6
        heat_fourth_power = l6_norm**4 / (4.0 * frequency**2)
        heat_norm = heat_fourth_power**0.25

        expected_l2 = frequency**-0.25 / math.sqrt(2.0)
        expected_heat = c6 / (4.0**0.25) * frequency**-0.75
        expected_hhalf = frequency**0.25 / math.sqrt(2.0)
        l2_error = relative_error(l2_norm, expected_l2)
        heat_error = relative_error(heat_norm, expected_heat)
        hhalf_error = relative_error(hhalf_norm, expected_hhalf)
        l2_errors.append(l2_error)
        heat_errors.append(heat_error)
        hhalf_errors.append(hhalf_error)

        row = blank_row("fourier_mode", index)
        row.update({
            "j": str(exponent),
            "N": str(frequency),
            "amplitude": format(amplitude, ".17g"),
            "l2_norm": format(l2_norm, ".17g"),
            "heat_l4_l6_norm": format(heat_norm, ".17g"),
            "hhalf_norm": format(hhalf_norm, ".17g"),
            "expected_l2_norm": format(expected_l2, ".17g"),
            "expected_heat_l4_l6_norm": format(expected_heat, ".17g"),
            "expected_hhalf_norm": format(expected_hhalf, ".17g"),
        })
        rows.append(row)
        check(checks, f"mode-{exponent:02d}-frequency", frequency == 2**exponent)
        check(checks, f"mode-{exponent:02d}-l2", l2_error <= tolerance, relativeError=l2_error)
        check(checks, f"mode-{exponent:02d}-heat", heat_error <= tolerance, relativeError=heat_error)
        check(checks, f"mode-{exponent:02d}-hhalf", hhalf_error <= tolerance, relativeError=hhalf_error)
    monitor.event("fourier-mode-grid", rows=maximum - minimum + 1)

    time_values = [int(value) for value in config["timeMapNoGo"]["nValues"]]
    support_upper = float(config["timeMapNoGo"]["supportUpper"])
    prefactor_power = float(config["timeMapNoGo"]["prefactorPower"])
    require(support_upper == 0.5, "canonical time-map support drift")
    require(prefactor_power == -0.25, "canonical time-map prefactor drift")
    log_two = math.log(2.0)
    fractional_values: list[float] = []
    for index, n_value in enumerate(time_values):
        require(n_value >= 2, "time-map n must be at least two")
        log_length = float(n_value) - log_two
        prefactor = float(n_value) ** prefactor_power
        l4_fourth = prefactor**4 * log_length
        l4_norm = l4_fourth**0.25
        fractional = prefactor * log_length
        expected_l4_fourth = 1.0 - log_two / float(n_value)
        expected_fractional = (
            float(n_value) ** 0.75
            - float(n_value) ** -0.25 * log_two
        )
        fractional_values.append(fractional)
        row = blank_row("time_map_no_go", index)
        row.update({
            "n": str(n_value),
            "g_l4_fourth_power": format(l4_fourth, ".17g"),
            "g_l4_norm": format(l4_norm, ".17g"),
            "fractional_value": format(fractional, ".17g"),
            "expected_fractional_value": format(expected_fractional, ".17g"),
        })
        rows.append(row)
        check(
            checks,
            f"time-map-{n_value}-l4-canonical",
            relative_error(l4_fourth, expected_l4_fourth) <= tolerance,
            relativeError=relative_error(l4_fourth, expected_l4_fourth),
        )
        check(
            checks,
            f"time-map-{n_value}-fractional",
            relative_error(fractional, expected_fractional) <= tolerance,
            relativeError=relative_error(fractional, expected_fractional),
        )
    check(
        checks,
        "time-map-values-strictly-increase",
        all(right > left for left, right in zip(fractional_values, fractional_values[1:])),
    )
    monitor.event("time-map-no-go-grid", rows=len(time_values))

    csv_path = output / "source-data.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    environment = {
        "execution": {
            "gpu": "not used",
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "platform": platform.platform(),
        "pythonExecutable": sys.executable,
        "pythonImplementation": platform.python_implementation(),
        "pythonVersion": platform.python_version(),
        "release": "R0.73Q",
        "schemaVersion": "r073q-finite-heat-flow-environment-v1",
        "standardLibraryOnly": True,
    }
    (output / "environment.json").write_text(canonical(environment), encoding="utf-8")
    monitor.event("producer-outputs-written", rows=len(rows))

    all_pass = all(item["pass"] is True for item in checks)
    diagnostic = {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "constants": {
            "c6": c6,
            "sinSixthMoment": {"denominator": moment.denominator, "numerator": moment.numerator},
        },
        "maxRelativeErrors": {
            "hhalf": max(hhalf_errors, default=0.0),
            "heatL4L6": max(heat_errors, default=0.0),
            "l2": max(l2_errors, default=0.0),
        },
        "modeRows": maximum - minimum + 1,
        "release": "R0.73Q",
        "schemaVersion": "r073q-finite-heat-flow-diagnostic-v1",
        "sourceData": binding(csv_path),
        "timeMapRows": len(time_values),
        "totalRows": len(rows),
    }
    (output / "diagnostic.json").write_text(canonical(diagnostic), encoding="utf-8")
    monitor.event("producer-complete", allChecksPass=all_pass, checks=len(checks))
    require(all_pass, "one or more producer checks failed")
    print(canonical({
        "allChecksPass": all_pass,
        "checks": len(checks),
        "modeRows": diagnostic["modeRows"],
        "timeMapRows": diagnostic["timeMapRows"],
    }), end="")


if __name__ == "__main__":
    main()
