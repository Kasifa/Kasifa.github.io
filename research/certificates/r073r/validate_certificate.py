#!/usr/bin/env python3
"""Structurally validate the R0.73R matched-phase certificate."""

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
    "record_type", "sample_index", "r", "m", "N", "family",
    "support_size", "coefficient_magnitude_squared", "l2_squared",
    "univariate_l6_sixth", "field_l6_sixth", "field_l6_norm",
    "hhalf_squared", "hhalf_norm", "annular_heat_proxy", "alpha",
    "scaled_l2_norm", "scaled_hhalf_norm", "scaled_annular_heat_proxy",
    "support_sha256", "magnitude_sha256",
    "signed_coefficient_sha256",
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
        "bytes": path.stat().st_size,
        "path": path.resolve().relative_to(ROOT).as_posix(),
        "sha256": sha256(path),
    }


def matches_binding(record: object, path: Path) -> bool:
    return isinstance(record, dict) and record == binding(path)


def relative_error(left: float, right: float) -> float:
    scale = max(abs(left), abs(right), 1e-300)
    return abs(left - right) / scale


def add_check(checks: list[dict[str, object]], check_id: str, passed: bool, **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})


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
            "validator": "structural-exact-relations",
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
            "validator": "structural-exact-relations",
        }, sort_keys=True) + "\n")


def build_validation() -> dict[str, object]:
    paths = {
        name: HERE / name
        for name in (
            "config.json", "diagnostic.json", "environment.json",
            "independent_validation.json", "certificate.json", "source-data.csv",
        )
    }
    for path in paths.values():
        require(path.is_file() and not path.is_symlink(), "missing regular input: " + str(path))
    config = load_json(paths["config.json"])
    diagnostic = load_json(paths["diagnostic.json"])
    environment = load_json(paths["environment.json"])
    independent = load_json(paths["independent_validation.json"])
    certificate = load_json(paths["certificate.json"])
    checks: list[dict[str, object]] = []
    claim = config["claimBoundary"]
    tolerance = float(config["tolerances"]["structuralRelative"])

    add_check(checks, "config-schema", config.get("schemaVersion") == "r073r-matched-phase-shell-config-v1")
    add_check(checks, "diagnostic-schema", diagnostic.get("schemaVersion") == "r073r-matched-phase-shell-diagnostic-v1")
    add_check(checks, "independent-schema", independent.get("schemaVersion") == "r073r-matched-phase-shell-independent-validation-v1")
    add_check(checks, "certificate-schema", certificate.get("schemaVersion") == "r073r-matched-phase-shell-certificate-v1")
    add_check(checks, "environment-schema", environment.get("schemaVersion") == "r073r-matched-phase-shell-environment-v1")
    add_check(checks, "primary-pass", diagnostic.get("allChecksPass") is True)
    add_check(checks, "independent-pass", independent.get("allChecksPass") is True)
    add_check(checks, "certificate-prerequisites", certificate.get("allPrerequisiteChecksPass") is True)
    add_check(
        checks,
        "claim-boundary-exact",
        diagnostic.get("claimBoundary") == claim
        and independent.get("claimBoundary") == claim
        and certificate.get("claimBoundary") == claim,
    )
    add_check(
        checks,
        "claim-boundary-no-overreach",
        claim.get("heatFlowIntegralComputed") is False
        and claim.get("intervalArithmeticUsed") is False
        and claim.get("annularHeatProxyIsExactHeatNorm") is False
        and claim.get("navierStokesSimulation") is False
        and claim.get("continuumPdeProofCertified") is False
        and claim.get("clayProblemSolved") is False,
    )
    add_check(checks, "environment-standard-library", environment.get("standardLibraryOnly") is True)
    add_check(checks, "environment-no-gpu", environment.get("execution", {}).get("gpu") == "not used")

    add_check(checks, "diagnostic-config-binding", matches_binding(diagnostic.get("inputBindings", {}).get("config"), paths["config.json"]))
    add_check(checks, "diagnostic-source-binding", matches_binding(diagnostic.get("sourceDataBinding"), paths["source-data.csv"]))
    independent_bindings = independent.get("inputBindings", {})
    add_check(checks, "independent-config-binding", matches_binding(independent_bindings.get("config"), paths["config.json"]))
    add_check(checks, "independent-diagnostic-binding", matches_binding(independent_bindings.get("diagnostic"), paths["diagnostic.json"]))
    add_check(checks, "independent-source-binding", matches_binding(independent_bindings.get("sourceData"), paths["source-data.csv"]))
    certificate_bindings = certificate.get("evidenceBindings", {})
    for key, filename in (
        ("config", "config.json"),
        ("diagnostic", "diagnostic.json"),
        ("independentValidation", "independent_validation.json"),
        ("sourceData", "source-data.csv"),
    ):
        add_check(checks, f"certificate-{key}-binding", matches_binding(certificate_bindings.get(key), paths[filename]))

    with paths["source-data.csv"].open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        add_check(checks, "source-data-schema", tuple(reader.fieldnames or ()) == CSV_FIELDS)
        rows = list(reader)
    expected_rows = 2 * (
        int(config["familyGrid"]["maximumExponent"])
        - int(config["familyGrid"]["minimumExponent"])
        + 1
    )
    add_check(checks, "source-data-row-count", len(rows) == expected_rows)
    add_check(checks, "cross-layer-row-count", diagnostic.get("rowCount") == independent.get("rowCount") == certificate.get("rowCount") == len(rows))
    add_check(checks, "primary-check-count", certificate.get("primaryCheckCount") == diagnostic.get("checkCount"))
    add_check(checks, "independent-check-count", certificate.get("independentCheckCount") == independent.get("checkCount"))
    add_check(
        checks,
        "theoretical-scaling-ledger-bound",
        certificate.get("theoreticalScalingExponentsInM")
        == diagnostic.get("theoreticalScalingExponentsInM"),
    )

    for row_index, row in enumerate(rows):
        m_value = int(row["m"])
        carrier = int(row["N"])
        family = row["family"]
        univariate_sixth = Fraction(row["univariate_l6_sixth"])
        field_sixth = Fraction(row["field_l6_sixth"])
        expected_field = Fraction(5 * univariate_sixth**2, 2 * m_value**6)
        exact_pass = (
            row["record_type"] == "matched_phase_family"
            and family in {"D", "RS"}
            and carrier == int(config["familyGrid"]["carrierMultiplier"]) * m_value
            and int(row["support_size"]) == 2 * m_value * m_value
            and Fraction(row["coefficient_magnitude_squared"]) == Fraction(1, 2 * m_value * m_value)
            and Fraction(row["l2_squared"]) == 1
            and field_sixth == expected_field
        )
        add_check(checks, f"row-{row_index:02d}-exact-relations", exact_pass)
        if family == "D":
            formula = Fraction(11 * m_value**5 + 5 * m_value**3 + 4 * m_value, 20)
            add_check(checks, f"row-{row_index:02d}-dirichlet-formula", univariate_sixth == formula)
        else:
            add_check(checks, f"row-{row_index:02d}-rs-l6-bounds", Fraction(1, 1) <= field_sixth <= Fraction(40, 1))
        l6_value = float(field_sixth) ** (1.0 / 6.0)
        hhalf_value = math.sqrt(float(row["hhalf_squared"]))
        alpha = math.sqrt(carrier) * m_value ** (-2.0 / 3.0)
        proxy = l6_value / math.sqrt(carrier)
        float_error = max(
            relative_error(float(row["field_l6_norm"]), l6_value),
            relative_error(float(row["hhalf_norm"]), hhalf_value),
            relative_error(float(row["annular_heat_proxy"]), proxy),
            relative_error(float(row["alpha"]), alpha),
            relative_error(float(row["scaled_l2_norm"]), alpha),
            relative_error(float(row["scaled_hhalf_norm"]), alpha * hhalf_value),
            relative_error(float(row["scaled_annular_heat_proxy"]), alpha * proxy),
        )
        add_check(checks, f"row-{row_index:02d}-float-relations", float_error <= tolerance, maximumRelativeError=float_error)
        hash_pass = all(
            len(row[field]) == 64 and all(character in "0123456789abcdef" for character in row[field])
            for field in ("support_sha256", "magnitude_sha256", "signed_coefficient_sha256")
        )
        add_check(checks, f"row-{row_index:02d}-hash-format", hash_pass)

    for pair_index in range(0, len(rows), 2):
        d_row = rows[pair_index]
        rs_row = rows[pair_index + 1]
        m_value = int(d_row["m"])
        add_check(
            checks,
            f"m-{m_value}-pair-order",
            d_row["family"] == "D" and rs_row["family"] == "RS" and d_row["m"] == rs_row["m"],
        )
        add_check(
            checks,
            f"m-{m_value}-matched-quadratic-data",
            d_row["support_sha256"] == rs_row["support_sha256"]
            and d_row["magnitude_sha256"] == rs_row["magnitude_sha256"]
            and d_row["l2_squared"] == rs_row["l2_squared"]
            and d_row["hhalf_squared"] == rs_row["hhalf_squared"],
        )
        signatures_equal = (
            d_row["signed_coefficient_sha256"] == rs_row["signed_coefficient_sha256"]
        )
        add_check(
            checks,
            f"m-{m_value}-phase-signature-pattern",
            signatures_equal if m_value <= 2 else not signatures_equal,
        )

    all_pass = all(item["pass"] for item in checks)
    return {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "inputBindings": {name: binding(path) for name, path in paths.items()},
        "release": "R0.73R",
        "rowCount": len(rows),
        "schemaVersion": "r073r-matched-phase-shell-structural-validation-v1",
    }


def main() -> None:
    args = parse_args()
    output = HERE / "validation.json"
    result = build_validation()
    require(result["allChecksPass"] is True, "one or more structural checks failed")
    text = canonical(result)
    if args.verify_only:
        require(output.is_file() and not output.is_symlink(), "missing regular validation.json")
        require(output.read_text(encoding="utf-8") == text, "validation.json is stale or inconsistent")
    else:
        output.write_text(text, encoding="utf-8")
        append_monitor("structural-validation-complete", checks=result["checkCount"], rows=result["rowCount"])
    print(canonical({
        "allChecksPass": True,
        "checks": result["checkCount"],
        "rows": result["rowCount"],
        "verifyOnly": args.verify_only,
    }), end="")


if __name__ == "__main__":
    main()
