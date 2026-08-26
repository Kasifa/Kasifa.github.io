#!/usr/bin/env python3
"""Extract the R0.71W amplitude-doping journal-figure data.

The three source certificates are read-only inputs.  This producer does not
rerun or modify the high-precision or retained-coset calculations.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import resource
import time
from zoneinfo import ZoneInfo

import numpy as np


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")
FIELDS = (
    "panel",
    "series",
    "q",
    "x",
    "y",
    "unit",
    "formula",
    "evidenceClass",
    "source",
    "note",
)


def timestamp() -> str:
    return datetime.now(TIMEZONE).isoformat(timespec="milliseconds")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_ndjson(path: Path, payload: dict[str, object]) -> None:
    payload = {"timestamp": timestamp(), **payload}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(payload, sort_keys=True) + "\n")


def resource_record(stage: str, started: float, **details: object) -> dict[str, object]:
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return {
        "stage": stage,
        "elapsedSeconds": time.perf_counter() - started,
        "pid": os.getpid(),
        "logicalCpuCount": os.cpu_count(),
        "loadAverage1m5m15m": list(os.getloadavg()),
        "processUserCpuSeconds": usage.ru_utime,
        "processSystemCpuSeconds": usage.ru_stime,
        "maximumResidentSetRaw": usage.ru_maxrss,
        **details,
    }


def load_source(config: dict[str, object], key: str) -> tuple[Path, dict[str, object]]:
    relative = Path(config["sourceCertificates"][key])
    path = REPOSITORY / relative
    if not path.is_file():
        raise FileNotFoundError(f"source certificate is missing: {relative}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    passed = payload.get("status") == "passed" or payload.get("passed") is True
    if not passed:
        raise RuntimeError(f"source certificate did not pass: {relative}")
    return path, payload


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), np.finfo(float).tiny)


def add_row(
    rows: list[dict[str, object]],
    panel: str,
    series: str,
    q_value: int,
    x_value: float,
    y_value: float,
    unit: str,
    formula: str,
    evidence_class: str,
    source: str,
    note: str,
) -> None:
    if not np.isfinite(y_value) or y_value < 0.0:
        raise ValueError(f"invalid plot value for {panel}/{series}: {y_value}")
    rows.append(
        {
            "panel": panel,
            "series": series,
            "q": q_value,
            "x": x_value,
            "y": y_value,
            "unit": unit,
            "formula": formula,
            "evidenceClass": evidence_class,
            "source": source,
            "note": note,
        }
    )


def fit_power(q_values: list[int], values: list[float]) -> dict[str, float]:
    x_values = np.log(np.asarray(q_values, dtype=float))
    y_values = np.log(np.asarray(values, dtype=float))
    slope, intercept = np.polyfit(x_values, y_values, 1)
    fitted = slope * x_values + intercept
    residual = y_values - fitted
    total = y_values - np.mean(y_values)
    denominator = float(np.dot(total, total))
    return {
        "power": float(slope),
        "logCoefficient": float(intercept),
        "rSquared": (
            1.0 - float(np.dot(residual, residual)) / denominator
            if denominator > 0.0
            else 1.0
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    (ROOT / "progress.ndjson").write_text("", encoding="utf-8")
    (ROOT / "resource-log.ndjson").write_text("", encoding="utf-8")
    append_ndjson(ROOT / "progress.ndjson", {"stage": "producer-start"})

    config = json.loads(arguments.config.read_text(encoding="utf-8"))
    primary_path, primary = load_source(config, "primary")
    independent_path, independent = load_source(config, "independent")
    truncated_path, truncated = load_source(config, "truncatedCoset")
    for payload, label in (
        (primary, "primary"),
        (independent, "independent"),
    ):
        if payload.get("release") != config["release"]:
            raise RuntimeError(f"{label} release does not match config")

    primary_ledger = primary["checks"]["amplitudeDopedLedger"]
    independent_ledger = independent["checks"]["independentAmplitudeLedger"]
    if not primary_ledger["passed"] or not independent_ledger["passed"]:
        raise RuntimeError("the analytic amplitude-doped ledgers must pass")
    primary_rows = primary_ledger["rows"]
    independent_rows = independent_ledger["rows"]
    if [int(row["q"]) for row in primary_rows] != config["analyticQValues"]:
        raise RuntimeError("primary analytic q grid differs from config")
    if [int(row["q"]) for row in independent_rows] != config["analyticQValues"]:
        raise RuntimeError("independent analytic q grid differs from config")

    analytic_crosscheck_maximum = 0.0
    for left, right in zip(primary_rows, independent_rows, strict=True):
        for field in (
            "atomToCompleteLedgerProxy",
            "leadingAtomProxy",
            "rotationalChargeUpper",
            "completeLedgerProxy",
        ):
            analytic_crosscheck_maximum = max(
                analytic_crosscheck_maximum,
                relative_error(float(left[field]), float(right[field])),
            )
    if analytic_crosscheck_maximum > 2.0e-12:
        raise RuntimeError(
            "primary/independent analytic ledgers differ by "
            f"{analytic_crosscheck_maximum:.3e}"
        )

    main_cases = truncated["mainContinuation"]
    if [int(case["q"]) for case in main_cases] != config["nonlinearQValues"]:
        raise RuntimeError("truncated-coset q grid differs from config")
    if not truncated["passed"] or not all(
        bool(check["passed"]) for check in truncated["checks"]
    ):
        raise RuntimeError("truncated-coset certificate did not pass every check")

    rows: list[dict[str, object]] = []
    for source_row in primary_rows:
        q_value = int(source_row["q"])
        add_row(
            rows,
            "A",
            "atom over complete-ledger proxy",
            q_value,
            q_value,
            float(source_row["atomToCompleteLedgerProxy"]),
            "dimensionless",
            "leadingAtomProxy/completeLedgerProxy",
            "primary high-precision certificate",
            str(primary_path.relative_to(REPOSITORY)),
            "leading asymptotic certificate proxy; not the nonlinear truncation",
        )
        append_ndjson(
            ROOT / "progress.ndjson",
            {
                "stage": "analytic-case-extracted",
                "q": q_value,
                "atomToCompleteLedgerProxy": source_row[
                    "atomToCompleteLedgerProxy"
                ],
            },
        )

    for case in main_cases:
        q_value = int(case["q"])
        add_row(
            rows,
            "B",
            "nonlinear truncated atom proxy",
            q_value,
            q_value,
            float(case["secondRootAtomProxy"]),
            "dimensionless proxy",
            "2 |a_t(t_2)|^2 / Y(t_2)",
            "finite nonlinear retained-coset corroboration",
            str(truncated_path.relative_to(REPOSITORY)),
            "second prescribed root; R=40",
        )
        add_row(
            rows,
            "B",
            "full retained H^-1 rotational charge",
            q_value,
            q_value,
            float(case["retainedCosetHminus1LChargeUpperBound"]),
            "dimensionless proxy",
            "integral ||L||_{H^-1,retained}^2/Y dt plus time-tail upper bound",
            "finite nonlinear retained-coset corroboration",
            str(truncated_path.relative_to(REPOSITORY)),
            "all retained convolution modes; R=40; not target-only",
        )
        add_row(
            rows,
            "C",
            "normalized second-root slope",
            q_value,
            q_value,
            float(case["normalizedRootSlopes"][1]),
            "dimensionless",
            "|a_t(t_2)|/A_q^2",
            "finite nonlinear retained-coset corroboration",
            str(truncated_path.relative_to(REPOSITORY)),
            "second prescribed root; R=40",
        )
        append_ndjson(
            ROOT / "progress.ndjson",
            {
                "stage": "truncated-case-extracted",
                "q": q_value,
                "rootResidual": case["rootSolve"]["maximumRootResidual"],
                "atomProxy": case["secondRootAtomProxy"],
                "rotationalCharge": case[
                    "retainedCosetHminus1LChargeUpperBound"
                ],
                "normalizedSlope": case["normalizedRootSlopes"][1],
            },
        )

    truncation_rows = truncated["truncationAudit"]
    for case in truncation_rows:
        radius = int(case["truncationRadius"])
        add_row(
            rows,
            "C-inset",
            "slope relative difference versus R=40",
            int(case["q"]),
            radius,
            float(case["comparisonToR40"]["secondRootSlopeRelativeDifference"]),
            "relative difference",
            "abs(s_R-s_40)/max(abs(s_R),abs(s_40))",
            "finite nonlinear truncation audit",
            str(truncated_path.relative_to(REPOSITORY)),
            "q=1024; R=40 is the reference and is not replotted as a zero on log scale",
        )

    analytic_q = [int(row["q"]) for row in primary_rows]
    analytic_ratio = [float(row["atomToCompleteLedgerProxy"]) for row in primary_rows]
    nonlinear_q = [int(case["q"]) for case in main_cases]
    nonlinear_atom = [float(case["secondRootAtomProxy"]) for case in main_cases]
    nonlinear_charge = [
        float(case["retainedCosetHminus1LChargeUpperBound"])
        for case in main_cases
    ]
    derived_fits = {
        "analyticAtomToCompleteLedger": fit_power(analytic_q[-4:], analytic_ratio[-4:]),
        "nonlinearAtomProxy": fit_power(nonlinear_q, nonlinear_atom),
        "nonlinearRotationalCharge": fit_power(nonlinear_q, nonlinear_charge),
    }
    source_records = []
    for label, path, payload in (
        ("primary", primary_path, primary),
        ("independent", independent_path, independent),
        ("truncatedCoset", truncated_path, truncated),
    ):
        source_records.append(
            {
                "label": label,
                "location": str(path.parent.relative_to(REPOSITORY)),
                "fileName": path.name,
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
                "status": payload.get("status"),
                "extractionCommand": (
                    "python figures/r071w-complete-ledger/"
                    "fig-r071w-amplitude-doping/produce_data.py --config "
                    "figures/r071w-complete-ledger/fig-r071w-amplitude-doping/config.json"
                ),
            }
        )

    elapsed = time.perf_counter() - started
    results = {
        "status": "passed",
        "release": config["release"],
        "figureId": config["figureId"],
        "generatedAt": timestamp(),
        "wallSeconds": elapsed,
        "sourceCertificates": source_records,
        "analytic": {
            "rows": primary_rows,
            "primaryFittedPowers": primary_ledger["fittedPowers"],
            "independentFittedPowers": independent_ledger["fittedPowers"],
            "maximumPrimaryIndependentRelativeDifference": analytic_crosscheck_maximum,
        },
        "truncatedCoset": {
            "mainContinuation": main_cases,
            "truncationAudit": truncation_rows,
            "certificatePowerFits": truncated["powerFits"],
            "certificateChecks": truncated["checks"],
        },
        "derivedFigureFits": derived_fits,
        "claimBoundary": json.loads((ROOT / "contract.json").read_text())["claimBoundary"],
    }
    (ROOT / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    "x": format(float(row["x"]), ".17g"),
                    "y": format(float(row["y"]), ".17g"),
                }
            )
    data_payload = {
        "schema": list(FIELDS),
        "rowCount": len(rows),
        "rows": rows,
        "evidenceClasses": {
            "A": "primary high-precision certificate, independently cross-checked",
            "B": "finite nonlinear retained-coset corroboration",
            "C": "finite nonlinear retained-coset and truncation corroboration",
        },
    }
    (ROOT / "data.json").write_text(
        json.dumps(data_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    metadata = {
        "figureId": config["figureId"],
        "release": config["release"],
        "rowCount": len(rows),
        "schema": list(FIELDS),
        "configSha256": sha256(arguments.config),
        "dataCsvSha256": sha256(ROOT / "data.csv"),
        "dataJsonSha256": sha256(ROOT / "data.json"),
        "resultsSha256": sha256(ROOT / "results.json"),
        "sourceCertificates": source_records,
        "evidenceMap": {
            "A": "certified leading atom divided by complete-ledger proxy",
            "B": "nonlinear finite-coset atom and all-retained-mode rotational charge",
            "C": "nonlinear root slope and q=1024 truncation audit",
        },
        "claimBoundary": results["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    append_ndjson(
        ROOT / "progress.ndjson",
        {"stage": "producer-complete", "rowCount": len(rows), "elapsedSeconds": elapsed},
    )
    append_ndjson(
        ROOT / "resource-log.ndjson",
        resource_record("producer-complete", started, rowCount=len(rows)),
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "rows": len(rows),
                "analyticCrosscheckMaximum": analytic_crosscheck_maximum,
                "derivedFits": derived_fits,
                "elapsedSeconds": elapsed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
