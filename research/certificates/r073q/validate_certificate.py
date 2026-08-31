#!/usr/bin/env python3
"""Fail-closed structural validation for the R0.73Q certificate."""

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
SOURCE_FILES = (
    "README.md",
    "assemble_certificate.py",
    "command.txt",
    "compute_formula_diagnostic.py",
    "config.json",
    "independent_validate.py",
    "requirements.txt",
    "seal_package.py",
    "validate_certificate.py",
)
PRESEAL_OUTPUTS = (
    "certificate.json",
    "diagnostic.json",
    "environment.json",
    "independent_validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "source-data.csv",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-only", action="store_true")
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


def append_monitor(stage: str, **fields: object) -> None:
    now = datetime.now(timezone.utc).isoformat()
    elapsed = time.monotonic() - START
    raw = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss = raw / (1024.0 * 1024.0) if sys.platform == "darwin" else raw / 1024.0
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({
            "elapsedSeconds": elapsed,
            "stage": stage,
            "timestampUtc": now,
            "validator": "structural-fail-closed",
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
            "validator": "structural-fail-closed",
        }, sort_keys=True) + "\n")


def add(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


def build_validation() -> dict[str, object]:
    config = load_json(HERE / "config.json")
    diagnostic = load_json(HERE / "diagnostic.json")
    independent = load_json(HERE / "independent_validation.json")
    certificate = load_json(HERE / "certificate.json")
    environment = load_json(HERE / "environment.json")
    checks: list[dict[str, object]] = []

    add(checks, "config-schema", config.get("schemaVersion") == "r073q-finite-heat-flow-config-v1")
    add(checks, "diagnostic-schema", diagnostic.get("schemaVersion") == "r073q-finite-heat-flow-diagnostic-v1")
    add(checks, "independent-schema", independent.get("schemaVersion") == "r073q-finite-heat-flow-independent-validation-v1")
    add(checks, "certificate-schema", certificate.get("schemaVersion") == "r073q-finite-heat-flow-certificate-v1")
    add(checks, "environment-schema", environment.get("schemaVersion") == "r073q-finite-heat-flow-environment-v1")
    add(checks, "primary-pass", diagnostic.get("allChecksPass") is True)
    add(checks, "independent-pass", independent.get("allChecksPass") is True)
    add(checks, "certificate-pass", certificate.get("allPrerequisiteChecksPass") is True)

    claim = config["claimBoundary"]
    add(
        checks,
        "claim-boundary-all-layers",
        diagnostic.get("claimBoundary") == claim
        and independent.get("claimBoundary") == claim
        and certificate.get("claimBoundary") == claim,
    )
    add(
        checks,
        "claim-boundary-negative-claims",
        claim.get("finiteFormulaDiagnosticOnly") is True
        and claim.get("navierStokesSimulation") is False
        and claim.get("continuumFixedPointCertified") is False
        and claim.get("globalRegularityEstablished") is False
        and claim.get("clayProblemSolved") is False,
    )

    for name in SOURCE_FILES + PRESEAL_OUTPUTS:
        path = HERE / name
        add(checks, "regular-file-" + name, path.is_file() and not path.is_symlink())

    producer_text = (HERE / "compute_formula_diagnostic.py").read_text(encoding="utf-8")
    independent_text = (HERE / "independent_validate.py").read_text(encoding="utf-8")
    add(checks, "producer-does-not-call-independent", "independent_validate" not in producer_text)
    add(checks, "independent-does-not-call-producer", "compute_formula_diagnostic" not in independent_text)
    add(checks, "standard-library-declaration", "external Python packages: none" in (HERE / "requirements.txt").read_text(encoding="utf-8"))

    with (HERE / "source-data.csv").open("r", encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    modes = [row for row in rows if row["record_type"] == "fourier_mode"]
    time_rows = [row for row in rows if row["record_type"] == "time_map_no_go"]
    expected_modes = int(config["modeGrid"]["maximumExponent"]) - int(config["modeGrid"]["minimumExponent"]) + 1
    expected_times = len(config["timeMapNoGo"]["nValues"])
    add(checks, "mode-row-count", len(modes) == expected_modes, observed=len(modes), expected=expected_modes)
    add(checks, "time-row-count", len(time_rows) == expected_times, observed=len(time_rows), expected=expected_times)
    add(checks, "only-known-row-kinds", len(rows) == len(modes) + len(time_rows))

    c6 = float(diagnostic["constants"]["c6"])
    tolerance = float(config["tolerances"]["structuralRelative"])
    add(checks, "c6-value", math.isclose(c6**6, 5.0 / 16.0, rel_tol=tolerance, abs_tol=0.0))
    first = modes[0]
    last = modes[-1]
    add(checks, "mode-grid-first", int(first["j"]) == 0 and int(first["N"]) == 1)
    add(checks, "mode-grid-last", int(last["j"]) == 24 and int(last["N"]) == 2**24)
    add(
        checks,
        "mode-asymptotic-directions",
        float(last["l2_norm"]) < float(first["l2_norm"])
        and float(last["heat_l4_l6_norm"]) < float(first["heat_l4_l6_norm"])
        and float(last["hhalf_norm"]) > float(first["hhalf_norm"]),
    )
    add(
        checks,
        "time-map-canonical-family-and-unbounded-direction",
        float(time_rows[-1]["fractional_value"]) > float(time_rows[0]["fractional_value"])
        and all(
            math.isclose(
                float(row["g_l4_fourth_power"]),
                1.0 - math.log(2.0) / float(row["n"]),
                rel_tol=tolerance,
                abs_tol=0.0,
            )
            and math.isclose(
                float(row["fractional_value"]),
                float(row["n"]) ** 0.75
                - float(row["n"]) ** -0.25 * math.log(2.0),
                rel_tol=tolerance,
                abs_tol=0.0,
            )
            for row in time_rows
        ),
    )

    add(
        checks,
        "certificate-count-bindings",
        int(certificate["primaryCheckCount"]) == int(diagnostic["checkCount"])
        and int(certificate["independentCheckCount"]) == int(independent["checkCount"]),
    )
    add(checks, "monitor-progress-nonempty", (HERE / "progress.ndjson").stat().st_size > 0)
    add(checks, "monitor-resource-nonempty", (HERE / "resource-log.ndjson").stat().st_size > 0)

    all_pass = all(item["pass"] is True for item in checks)
    return {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "evidenceBindings": {
            "certificate": binding(HERE / "certificate.json"),
            "config": binding(HERE / "config.json"),
            "diagnostic": binding(HERE / "diagnostic.json"),
            "independentValidation": binding(HERE / "independent_validation.json"),
            "sourceData": binding(HERE / "source-data.csv"),
        },
        "release": "R0.73Q",
        "schemaVersion": "r073q-finite-heat-flow-structural-validation-v1",
    }


def verify_seal_inventory_if_present() -> None:
    manifest_path = HERE / "manifest.json"
    sums_path = HERE / "SHA256SUMS"
    if not manifest_path.exists() and not sums_path.exists():
        return
    require(manifest_path.is_file() and sums_path.is_file(), "partial seal inventory")
    manifest = load_json(manifest_path)
    inventory = manifest.get("inventory")
    require(isinstance(inventory, dict), "manifest inventory missing")
    require(int(inventory["packageFileCount"]) == 19, "manifest package-file count drift")
    lines = [line for line in sums_path.read_text(encoding="utf-8").splitlines() if line]
    require(len(lines) == 18, "SHA256SUMS line-count drift")


def main() -> None:
    args = parse_args()
    output = HERE / "validation.json"
    if not args.verify_only:
        append_monitor("structural-validation-start")
    expected = build_validation()
    require(expected["allChecksPass"] is True, "one or more structural checks failed")
    if args.verify_only:
        actual = load_json(output)
        require(actual == expected, "validation.json is stale or inconsistent")
        verify_seal_inventory_if_present()
    else:
        output.write_text(canonical(expected), encoding="utf-8")
    print(canonical({
        "allChecksPass": True,
        "checks": expected["checkCount"],
        "verifyOnly": args.verify_only,
    }), end="")


if __name__ == "__main__":
    main()
