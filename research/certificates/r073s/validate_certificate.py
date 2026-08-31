#!/usr/bin/env python3
"""Structurally validate the R0.73S quadratic-autocorrelation package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from fractions import Fraction
import hashlib
import json
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


def matches_binding(record: object, path: Path) -> bool:
    return isinstance(record, dict) and record == binding(path)


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
            "validator": "structural-package",
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
            "validator": "structural-package",
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
    add_check(checks, "config-schema", config.get("schemaVersion") == "r073s-quadratic-autocorrelation-config-v1")
    add_check(checks, "diagnostic-schema", diagnostic.get("schemaVersion") == "r073s-quadratic-autocorrelation-diagnostic-v1")
    add_check(checks, "independent-schema", independent.get("schemaVersion") == "r073s-quadratic-autocorrelation-independent-validation-v1")
    add_check(checks, "certificate-schema", certificate.get("schemaVersion") == "r073s-quadratic-autocorrelation-certificate-v1")
    add_check(checks, "environment-schema", environment.get("schemaVersion") == "r073s-quadratic-autocorrelation-environment-v1")
    add_check(checks, "all-prerequisites", diagnostic.get("allChecksPass") is True and independent.get("allChecksPass") is True and certificate.get("allPrerequisiteChecksPass") is True)
    add_check(checks, "records-digest", diagnostic.get("recordsSha256") == independent.get("recordsSha256") == certificate.get("recordsSha256"))
    add_check(checks, "claim-boundary-exact", diagnostic.get("claimBoundary") == independent.get("claimBoundary") == certificate.get("claimBoundary") == claim)
    add_check(
        checks,
        "claim-boundary-no-overreach",
        claim.get("arithmeticComplexityLowerBound") is False
        and claim.get("heatFlowIntegralComputed") is False
        and claim.get("navierStokesSimulation") is False
        and claim.get("continuumPdeProofCertified") is False
        and claim.get("clayProblemSolved") is False
        and claim.get("predeclaredStrictSubsetNoGo") is True
        and claim.get("universalRuntimeLowerBound") is False,
    )
    add_check(checks, "environment-standard-library", environment.get("standardLibraryOnly") is True)
    add_check(checks, "environment-no-gpu", environment.get("execution", {}).get("gpu") == "not used")

    add_check(checks, "diagnostic-config-binding", matches_binding(diagnostic.get("inputBindings", {}).get("config"), paths["config.json"]))
    independent_bindings = independent.get("inputBindings", {})
    add_check(checks, "independent-config-binding", matches_binding(independent_bindings.get("config"), paths["config.json"]))
    add_check(checks, "independent-diagnostic-binding", matches_binding(independent_bindings.get("diagnostic"), paths["diagnostic.json"]))
    add_check(checks, "independent-source-binding", matches_binding(independent_bindings.get("sourceData"), paths["source-data.csv"]))
    certificate_bindings = certificate.get("evidenceBindings", {})
    for key, filename in (
        ("config", "config.json"),
        ("diagnostic", "diagnostic.json"),
        ("environment", "environment.json"),
        ("independentValidation", "independent_validation.json"),
        ("sourceData", "source-data.csv"),
    ):
        add_check(checks, f"certificate-{key}-binding", matches_binding(certificate_bindings.get(key), paths[filename]))

    with paths["source-data.csv"].open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        add_check(checks, "source-schema", tuple(reader.fieldnames or ()) == CSV_FIELDS)
        rows = list(reader)
    add_check(checks, "row-count-cross-layer", len(rows) == diagnostic.get("rowCount") == independent.get("rowCount") == certificate.get("rowCount"))
    add_check(checks, "check-count-bindings", diagnostic.get("checkCount") == certificate.get("primaryCheckCount") and independent.get("checkCount") == certificate.get("independentCheckCount"))

    for index, row in enumerate(rows):
        record_type = row["record_type"]
        parameter = int(row["parameter"])
        modes = int(row["modes"])
        autocorrelation_support = int(row["autocorrelation_support"]) if row["autocorrelation_support"] else None
        difference_set = int(row["difference_set_size"]) if row["difference_set_size"] else None
        l2 = Fraction(row["l2_squared"])
        fourth = Fraction(row["l4_fourth"])
        sixth = Fraction(row["l6_sixth"])
        support_bound = Fraction(row["support_bound"])
        add_check(checks, f"row-{index:02d}-positive", modes > 0 and l2 > 0 and fourth > 0 and sixth > 0)
        add_check(checks, f"row-{index:02d}-difference-set-present", difference_set is not None and difference_set > 0)
        add_check(
            checks,
            f"row-{index:02d}-support-kind",
            (record_type == "riesz_product_no_go" and autocorrelation_support is None)
            or (
                record_type != "riesz_product_no_go"
                and autocorrelation_support is not None
                and 0 < autocorrelation_support <= int(difference_set or 0)
            ),
        )
        add_check(checks, f"row-{index:02d}-support-bound", sixth <= support_bound and support_bound == modes * l2 * fourth)
        if row["aq_bound"]:
            corr_l1 = Fraction(row["autocorrelation_l1"])
            aq = Fraction(row["aq_bound"])
            add_check(
                checks,
                f"row-{index:02d}-aq-relations",
                autocorrelation_support is not None
                and sixth <= aq <= support_bound
                and aq == corr_l1 * fourth
                and corr_l1 * corr_l1 <= autocorrelation_support * fourth,
            )
        else:
            add_check(checks, f"row-{index:02d}-aq-blank-contract", row["autocorrelation_l1"] == "" and row["ratio_to_aq"] == "")

        if record_type == "asymptotically_fixed_quartic_spike":
            add_check(
                checks,
                f"row-{index:02d}-bounded-quartic-supports",
                parameter >= 2
                and modes == parameter + 1
                and autocorrelation_support == difference_set == 4 * parameter - 1
                and sixth * sixth <= int(autocorrelation_support or 0) * fourth**3,
            )
        elif record_type == "matched_r073r":
            m_value = 2**parameter
            add_check(
                checks,
                f"row-{index:02d}-matched-supports",
                modes == 2 * m_value * m_value
                and difference_set == 3 * (2 * m_value - 1) ** 2,
            )
        elif record_type == "riesz_product_no_go":
            add_check(
                checks,
                f"row-{index:02d}-riesz-difference-set",
                modes == 5**parameter and difference_set == 9**parameter,
            )
        else:
            add_check(checks, f"row-{index:02d}-generic-supports", record_type == "generic_sequence")

    no_go_rows = [row for row in rows if row["record_type"] == "riesz_product_no_go"]
    for offset in range(0, len(no_go_rows), 2):
        left, right = no_go_rows[offset], no_go_rows[offset + 1]
        add_check(
            checks,
            f"riesz-pair-{offset // 2 + 1}",
            left["family"] == "A" and right["family"] == "B"
            and left["parameter"] == right["parameter"]
            and left["modes"] == right["modes"]
            and left["l2_squared"] == right["l2_squared"]
            and left["l4_fourth"] == right["l4_fourth"]
            and Fraction(right["l6_sixth"]) > Fraction(left["l6_sixth"]),
        )

    all_pass = all(item["pass"] for item in checks)
    return {
        "allChecksPass": all_pass,
        "checkCount": len(checks),
        "checks": checks,
        "claimBoundary": claim,
        "inputBindings": {name: binding(path) for name, path in paths.items()},
        "release": "R0.73S",
        "rowCount": len(rows),
        "schemaVersion": "r073s-quadratic-autocorrelation-validation-v1",
    }


def main() -> None:
    args = parse_args()
    result = build_validation()
    output = HERE / "validation.json"
    result_text = canonical(result)
    if args.verify_only:
        require(output.is_file() and not output.is_symlink(), "missing regular validation.json")
        require(output.read_text(encoding="utf-8") == result_text, "validation.json is stale or inconsistent")
    else:
        output.write_text(result_text, encoding="utf-8")
        monitor("validation-complete", allChecksPass=result["allChecksPass"], checks=result["checkCount"])
    require(result["allChecksPass"] is True, "one or more structural checks failed")
    print(canonical({
        "allChecksPass": result["allChecksPass"],
        "checkCount": result["checkCount"],
        "rows": result["rowCount"],
        "verifyOnly": args.verify_only,
    }), end="")


if __name__ == "__main__":
    main()
