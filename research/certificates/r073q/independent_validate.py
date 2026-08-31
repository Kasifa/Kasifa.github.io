#!/usr/bin/env python3
"""Independently recalculate the R0.73Q finite heat-flow formulas.

This program does not import or execute the primary calculation.  It rebuilds
the grid from integer indices, obtains the sixth trigonometric moment from a
central binomial coefficient, and uses the two Fourier coefficients of sine.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
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
    parser.add_argument("--reference", default=str(HERE / "diagnostic.json"))
    parser.add_argument("--source-data", default=str(HERE / "source-data.csv"))
    parser.add_argument("--output", default=str(HERE / "independent_validation.json"))
    return parser.parse_args()


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


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


def binding(path: Path) -> dict[str, object]:
    return {
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "bytes": path.stat().st_size,
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
    progress = {
        "elapsedSeconds": elapsed,
        "stage": stage,
        "timestampUtc": now,
        "validator": "independent-binomial-fourier",
        **fields,
    }
    resources = {
        "elapsedSeconds": elapsed,
        "executionHost": platform.node(),
        "gpu": "not used",
        "maximumResidentSetMiB": rss,
        "processes": 1,
        "stage": stage,
        "threadsPerProcess": 1,
        "timestampUtc": now,
        "validator": "independent-binomial-fourier",
    }
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(progress, sort_keys=True) + "\n")
    with (HERE / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(resources, sort_keys=True) + "\n")


def add_check(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


def main() -> None:
    args = parse_args()
    config_path = Path(args.config).resolve()
    reference_path = Path(args.reference).resolve()
    source_path = Path(args.source_data).resolve()
    output_path = Path(args.output).resolve()
    require(output_path == HERE / "independent_validation.json", "output path drift")
    config = load_json(config_path)
    reference = load_json(reference_path)
    require(config.get("schemaVersion") == "r073q-finite-heat-flow-config-v1", "config schema drift")
    require(reference.get("schemaVersion") == "r073q-finite-heat-flow-diagnostic-v1", "reference schema drift")
    require(reference.get("allChecksPass") is True, "primary diagnostic did not pass")
    append_monitor("independent-start")

    with source_path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "source-data schema drift")
        rows = list(reader)
    mode_rows = [row for row in rows if row["record_type"] == "fourier_mode"]
    time_rows = [row for row in rows if row["record_type"] == "time_map_no_go"]
    require(len(rows) == len(mode_rows) + len(time_rows), "unknown source-data row kind")

    tolerance = float(config["tolerances"]["independentRelative"])
    checks: list[dict[str, object]] = []
    errors = {"amplitude": [], "c6": [], "fractional": [], "hhalf": [], "heat": [], "l2": [], "l4": []}
    claim = config["claimBoundary"]
    add_check(checks, "claim-boundary-exact", reference.get("claimBoundary") == claim)

    # Independent sixth moment: E(sin^(2m)) = C(2m,m)/4^m.
    moment = math.comb(6, 3) / 4.0**3
    configured_moment = (
        int(config["trigonometricMoment"]["valueNumerator"])
        / int(config["trigonometricMoment"]["valueDenominator"])
    )
    independent_c6 = moment ** (1.0 / 6.0)
    errors["c6"].append(relative_error(moment, configured_moment))
    errors["c6"].append(relative_error(independent_c6, float(reference["constants"]["c6"])))
    add_check(
        checks,
        "central-binomial-sixth-moment",
        max(errors["c6"]) <= tolerance,
        moment=moment,
        relativeError=max(errors["c6"]),
    )

    grid = config["modeGrid"]
    exponents = list(range(int(grid["minimumExponent"]), int(grid["maximumExponent"]) + 1))
    require(len(mode_rows) == len(exponents), "mode row-count drift")
    for index, (row, exponent) in enumerate(zip(mode_rows, exponents)):
        frequency = 1 << exponent
        amplitude = 2.0 ** (-exponent / 4.0)
        coefficient_modulus_squared = (amplitude / 2.0) ** 2
        l2 = math.sqrt(2.0 * coefficient_modulus_squared)
        hhalf = math.sqrt(2.0 * frequency * coefficient_modulus_squared)
        l6 = amplitude * independent_c6
        heat = (l6**4 * (1.0 / (4.0 * frequency**2))) ** 0.25

        require(int(row["sample_index"]) == index, "mode sample-index drift")
        require(int(row["j"]) == exponent, "mode exponent drift")
        require(int(row["N"]) == frequency, "mode frequency drift")
        observed = {
            "amplitude": float(row["amplitude"]),
            "l2": float(row["l2_norm"]),
            "heat": float(row["heat_l4_l6_norm"]),
            "hhalf": float(row["hhalf_norm"]),
        }
        expected = {"amplitude": amplitude, "l2": l2, "heat": heat, "hhalf": hhalf}
        for name in expected:
            errors[name].append(relative_error(observed[name], expected[name]))
        add_check(
            checks,
            f"mode-{exponent:02d}-independent-reconstruction",
            max(relative_error(observed[name], expected[name]) for name in expected) <= tolerance,
        )

    n_values = [int(value) for value in config["timeMapNoGo"]["nValues"]]
    support_upper = float(config["timeMapNoGo"]["supportUpper"])
    prefactor_power = float(config["timeMapNoGo"]["prefactorPower"])
    require(support_upper == 0.5, "canonical time-map support drift")
    require(prefactor_power == -0.25, "canonical time-map prefactor drift")
    require(len(time_rows) == len(n_values), "time-map row-count drift")
    reconstructed_fractional: list[float] = []
    for index, (row, n_value) in enumerate(zip(time_rows, n_values)):
        require(int(row["sample_index"]) == index, "time-map sample-index drift")
        require(int(row["n"]) == n_value, "time-map n drift")
        # Set r=1-s.  The canonical support exp(-n)<r<1/2 has
        # integral(dr/r)=n+log(1/2).  This path is coded independently of
        # the primary direct-formula calculation.
        interval_log_measure = float(n_value) + math.log(support_upper)
        normalizer = math.exp(prefactor_power * math.log(float(n_value)))
        l4_fourth = normalizer**4 * interval_log_measure
        l4_norm = l4_fourth**0.25
        fractional = normalizer * interval_log_measure
        reconstructed_fractional.append(fractional)
        l4_error = max(
            relative_error(float(row["g_l4_fourth_power"]), l4_fourth),
            relative_error(float(row["g_l4_norm"]), l4_norm),
        )
        fractional_error = relative_error(float(row["fractional_value"]), fractional)
        errors["l4"].append(l4_error)
        errors["fractional"].append(fractional_error)
        add_check(
            checks,
            f"time-map-{n_value}-independent-reconstruction",
            max(l4_error, fractional_error) <= tolerance,
            fractionalRelativeError=fractional_error,
            l4RelativeError=l4_error,
        )
    add_check(
        checks,
        "time-map-independent-growth",
        all(right > left for left, right in zip(reconstructed_fractional, reconstructed_fractional[1:])),
    )

    all_errors = [item for values in errors.values() for item in values]
    all_pass = all(item["pass"] is True for item in checks) and max(all_errors, default=0.0) <= tolerance
    result = {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "independence": {
            "callsPrimaryProducer": False,
            "importsPrimaryProducer": False,
            "method": "central-binomial moment, integer-index grid, two Fourier coefficients",
        },
        "maxRelativeError": max(all_errors, default=0.0),
        "referenceDiagnostic": binding(reference_path),
        "release": "R0.73Q",
        "schemaVersion": "r073q-finite-heat-flow-independent-validation-v1",
        "sourceData": binding(source_path),
        "validatedModeRows": len(mode_rows),
        "validatedTimeMapRows": len(time_rows),
    }
    output_path.write_text(canonical(result), encoding="utf-8")
    append_monitor("independent-complete", allChecksPass=all_pass, checks=len(checks))
    require(all_pass, "one or more independent checks failed")
    print(canonical({
        "allChecksPass": all_pass,
        "checks": len(checks),
        "maxRelativeError": result["maxRelativeError"],
    }), end="")


if __name__ == "__main__":
    main()
