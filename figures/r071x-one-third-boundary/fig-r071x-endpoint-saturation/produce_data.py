#!/usr/bin/env python3
"""Extract the R0.71X endpoint-saturation journal-figure data.

The three configured certificate JSON files are the only scientific inputs.
This script does not rerun or modify any certificate calculation.
"""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
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
    "delta",
    "x",
    "y",
    "rawValue",
    "referenceValue",
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
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": timestamp(), **payload}, sort_keys=True) + "\n")


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
    if not (payload.get("status") == "passed" or payload.get("passed") is True):
        raise RuntimeError(f"source certificate did not pass: {relative}")
    return path, payload


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), np.finfo(float).tiny)


def fit_power(x_values: list[float], y_values: list[float]) -> dict[str, float]:
    x = np.log(np.asarray(x_values, dtype=float))
    y = np.log(np.asarray(y_values, dtype=float))
    slope, intercept = np.polyfit(x, y, 1)
    fitted = slope * x + intercept
    residual = y - fitted
    total = y - np.mean(y)
    denominator = float(np.dot(total, total))
    return {
        "power": float(slope),
        "logCoefficient": float(intercept),
        "rSquared": 1.0 - float(np.dot(residual, residual)) / denominator if denominator else 1.0,
    }


def add_row(
    rows: list[dict[str, object]],
    *,
    panel: str,
    series: str,
    q: int,
    delta: float,
    x: float,
    y: float,
    raw_value: float,
    reference_value: float,
    unit: str,
    formula: str,
    evidence_class: str,
    source: str,
    note: str,
) -> None:
    values = (x, y, raw_value, reference_value)
    if not all(math.isfinite(value) for value in values) or x <= 0.0 or y <= 0.0:
        raise ValueError(f"invalid positive plot row for {panel}/{series}: {values}")
    rows.append(
        {
            "panel": panel,
            "series": series,
            "q": q,
            "delta": delta,
            "x": x,
            "y": y,
            "rawValue": raw_value,
            "referenceValue": reference_value,
            "unit": unit,
            "formula": formula,
            "evidenceClass": evidence_class,
            "source": source,
            "note": note,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    (ROOT / "progress.ndjson").write_text("", encoding="utf-8")
    (ROOT / "resource-log.ndjson").write_text("", encoding="utf-8")
    append_ndjson(ROOT / "progress.ndjson", {"stage": "producer-start"})

    config = json.loads(args.config.read_text(encoding="utf-8"))
    primary_path, primary = load_source(config, "primary")
    independent_path, independent = load_source(config, "independent")
    truncated_path, truncated = load_source(config, "truncatedCoset")
    if independent.get("release") != config["release"]:
        raise RuntimeError("independent certificate release does not match config")
    if not str(primary.get("release", "")).startswith(config["release"]):
        raise RuntimeError("primary certificate release does not match config")
    if not all(bool(check["passed"]) for source in (primary, independent, truncated) for check in source["checks"]):
        raise RuntimeError("at least one source-certificate check did not pass")

    fixed_delta = float(config["fixedDelta"])
    primary_fixed = primary["fixedDeltaRows"]
    nonlinear = truncated["mainContinuation"]
    delta_rows = primary["deltaCollapse"]["rows"]
    truncation_rows = truncated["truncationAudit"]
    if [int(case["q"]) for case in nonlinear] != config["nonlinearQValues"]:
        raise RuntimeError("nonlinear q grid differs from config")
    if any(float(case["delta"]) != fixed_delta for case in nonlinear):
        raise RuntimeError("nonlinear fixed delta differs from config")
    if [float(row["delta"]) for row in delta_rows] != config["deltaSweep"]:
        raise RuntimeError("delta sweep differs from config")
    if any(int(row["q"]) != int(config["deltaSweepQ"]) for row in delta_rows):
        raise RuntimeError("delta-sweep q differs from config")
    if [int(case["truncationRadius"]) for case in truncation_rows] != config["truncationAudit"]["radii"]:
        raise RuntimeError("truncation-radius grid differs from config")

    # Cross-check the limiting algebra through two independent implementations.
    primary_coefficients = [float(value) for value in primary["limitingInterpolation"]["coefficients"]]
    independent_coefficients = [float(value) for value in independent["limitingResponse"]["coefficients"][:3]]
    primary_slopes = [abs(float(value)) for value in primary["limitingInterpolation"]["rootSlopes"]]
    independent_slopes = [abs(float(value)) for value in independent["limitingResponse"]["rootSlopes"]]
    crosscheck_errors = [
        relative_error(left, right)
        for left, right in zip(primary_coefficients + primary_slopes, independent_coefficients + independent_slopes, strict=True)
    ]
    crosscheck_errors.append(
        relative_error(float(primary["limitingInterpolation"]["tailLimit"]), float(independent["limitingResponse"]["limitingTail"]))
    )
    maximum_crosscheck_error = max(crosscheck_errors)
    if maximum_crosscheck_error > 2.0e-14:
        raise RuntimeError(f"primary/independent limiting algebra differs by {maximum_crosscheck_error:.3e}")

    rows: list[dict[str, object]] = []
    truncated_source = str(truncated_path.relative_to(REPOSITORY))
    primary_source = str(primary_path.relative_to(REPOSITORY))

    # Panel A: comparable indexed powers, with raw values retained per row.
    d_reference = float(nonlinear[0]["initialData"]["D"])
    atom_reference = float(nonlinear[0]["completePrescribedAtomProxySum"])
    for case in nonlinear:
        q_value = int(case["q"])
        d_value = float(case["initialData"]["D"])
        atom_value = float(case["completePrescribedAtomProxySum"])
        add_row(
            rows,
            panel="A",
            series="initial-data D indexed to q=256",
            q=q_value,
            delta=fixed_delta,
            x=q_value,
            y=d_value / d_reference,
            raw_value=d_value,
            reference_value=d_reference,
            unit="index (q=256 equals 1)",
            formula="D_q/D_256",
            evidence_class="finite nonlinear retained-coset corroboration",
            source=truncated_source,
            note="R=40; finite retained Fourier coset; raw D retained in rawValue",
        )
        add_row(
            rows,
            panel="A",
            series="complete prescribed atomProxy sum indexed to q=256",
            q=q_value,
            delta=fixed_delta,
            x=q_value,
            y=atom_value / atom_reference,
            raw_value=atom_value,
            reference_value=atom_reference,
            unit="index (q=256 equals 1)",
            formula="atomProxySum_q/atomProxySum_256",
            evidence_class="finite nonlinear retained-coset corroboration",
            source=truncated_source,
            note="sum over the two prescribed roots; atomProxy is not multiplier-locked J_*",
        )
        append_ndjson(
            ROOT / "progress.ndjson",
            {"stage": "fixed-delta-case-extracted", "q": q_value, "D": d_value, "atomProxySum": atom_value},
        )

    # Panel B: keep the high-precision and retained-coset layers distinct.
    for source_row in primary_fixed:
        q_value = int(source_row["q"])
        for series, field, formula, note in (
            (
                "high-precision endpoint atom-proxy ratio",
                "atomOverDataOneThird",
                "leadingAtomProxy/D^(1/3)",
                "tangent/high-precision algebra; atomProxy is not multiplier-locked J_*",
            ),
            (
                "high-precision complete-ledger-normalized proxy",
                "atomOverDataOneThirdLedger",
                "leadingAtomProxy/(D^(1/3) completeLedgerProxy)",
                "complete-ledger-normalized analytic proxy; not the finite retained charge",
            ),
        ):
            value = float(source_row[field])
            add_row(
                rows,
                panel="B",
                series=series,
                q=q_value,
                delta=float(source_row["delta"]),
                x=q_value,
                y=value,
                raw_value=value,
                reference_value=1.0,
                unit="dimensionless proxy",
                formula=formula,
                evidence_class="primary high-precision algebra certificate",
                source=primary_source,
                note=note,
            )
    for case in nonlinear:
        q_value = int(case["q"])
        for series, field, formula, note in (
            (
                "finite-coset endpoint atomProxy ratio",
                "completePrescribedAtomProxySumOverDOneThird",
                "completePrescribedAtomProxySum/D^(1/3)",
                "R=40 finite retained-coset corroboration; atomProxy is not J_*",
            ),
            (
                "full retained rotational-charge upper bound",
                "retainedFullCosetHminus1LChargeUpperBound",
                "integral ||L||^2_H^-1,retained/Y dt plus time-tail upper bound",
                "all retained convolution modes; distinct from complete-ledger-normalized proxy",
            ),
        ):
            value = float(case[field])
            add_row(
                rows,
                panel="B",
                series=series,
                q=q_value,
                delta=float(case["delta"]),
                x=q_value,
                y=value,
                raw_value=value,
                reference_value=1.0,
                unit="dimensionless proxy",
                formula=formula,
                evidence_class="finite nonlinear retained-coset corroboration",
                source=truncated_source,
                note=note,
            )

    # Panel C: high-precision delta sweep and the retained-coset radius audit.
    for source_row in delta_rows:
        value = float(source_row["atomOverDataOneThird"])
        add_row(
            rows,
            panel="C",
            series="high-precision delta endpoint collapse",
            q=int(source_row["q"]),
            delta=float(source_row["delta"]),
            x=float(source_row["delta"]),
            y=value,
            raw_value=value,
            reference_value=1.0,
            unit="dimensionless proxy",
            formula="leadingAtomProxy/D^(1/3)",
            evidence_class="primary high-precision algebra certificate",
            source=primary_source,
            note="q=2048 delta sweep; atomProxy is not multiplier-locked J_*",
        )
    truncation_fields = (
        "atomProxySumRelativeDifference",
        "endpointCoefficientRelativeDifference",
        "initialDRelativeDifference",
        "retainedChargeRelativeDifference",
    )
    for case in truncation_rows:
        comparison = case["comparisonToR40"]
        maximum_relative = max(float(comparison[field]) for field in truncation_fields)
        radius = int(case["truncationRadius"])
        add_row(
            rows,
            panel="C-inset",
            series="maximum retained-observable relative difference versus R=40",
            q=int(case["q"]),
            delta=float(case["delta"]),
            x=radius,
            y=maximum_relative,
            raw_value=maximum_relative,
            reference_value=40.0,
            unit="relative difference",
            formula="max relative difference across atomProxy sum, endpoint coefficient, D, and retained charge",
            evidence_class="finite nonlinear truncation audit",
            source=truncated_source,
            note="q=1024; R=40 reference; maximumZDifference excluded because it is absolute",
        )

    derived_fits = {
        "fixedDeltaInitialDataD": fit_power(
            [float(case["q"]) for case in nonlinear],
            [float(case["initialData"]["D"]) for case in nonlinear],
        ),
        "fixedDeltaCompletePrescribedAtomProxySum": fit_power(
            [float(case["q"]) for case in nonlinear],
            [float(case["completePrescribedAtomProxySum"]) for case in nonlinear],
        ),
        "finiteCosetEndpointAtomProxyRatio": fit_power(
            [float(case["q"]) for case in nonlinear],
            [float(case["completePrescribedAtomProxySumOverDOneThird"]) for case in nonlinear],
        ),
        "fullRetainedRotationalChargeUpper": fit_power(
            [float(case["q"]) for case in nonlinear],
            [float(case["retainedFullCosetHminus1LChargeUpperBound"]) for case in nonlinear],
        ),
        "deltaEndpointCollapse": fit_power(
            [float(row["delta"]) for row in delta_rows],
            [float(row["atomOverDataOneThird"]) for row in delta_rows],
        ),
    }
    no_extra_root_cases = sum(
        bool(case["noExtraRootCorroboration"]["noExtraRealRootScanPassed"])
        and bool(case["noExtraRootCorroboration"]["integratingFactor"]["tailProxyPassed"])
        for case in nonlinear
    )
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
                "extractionCommand": "python figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/produce_data.py --config figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/config.json",
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
        "primary": {
            "fittedQPowers": primary["fittedQPowers"],
            "fixedDeltaRows": primary_fixed,
            "deltaCollapse": primary["deltaCollapse"],
        },
        "independent": {
            "limitingResponse": independent["limitingResponse"],
            "fixedDeltaAudit": next(audit for audit in independent["amplitudeLawAudits"] if float(audit["deltaDecayPower"]) == 0.0),
            "maximumLimitingAlgebraRelativeDifference": maximum_crosscheck_error,
        },
        "truncatedCoset": {
            "mainContinuation": nonlinear,
            "truncationAudit": truncation_rows,
            "certificatePowerFits": truncated["powerFits"],
            "noExtraRootAndTailCasesPassed": no_extra_root_cases,
            "caseCount": len(nonlinear),
        },
        "derivedFigureFits": derived_fits,
        "claimBoundary": json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))["claimBoundary"],
    }
    (ROOT / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with (ROOT / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(
                {
                    **row,
                    **{field: format(float(row[field]), ".17g") for field in ("delta", "x", "y", "rawValue", "referenceValue")},
                }
            )
    data_payload = {
        "schema": list(FIELDS),
        "rowCount": len(rows),
        "rows": rows,
        "evidenceClasses": {
            "A": "finite nonlinear retained-coset power corroboration",
            "B": "high-precision algebra and finite retained-coset layers kept separate",
            "C": "high-precision delta sweep with finite retained-coset truncation inset",
        },
    }
    (ROOT / "data.json").write_text(json.dumps(data_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    metadata = {
        "figureId": config["figureId"],
        "release": config["release"],
        "rowCount": len(rows),
        "schema": list(FIELDS),
        "configSha256": sha256(args.config),
        "dataCsvSha256": sha256(ROOT / "data.csv"),
        "dataJsonSha256": sha256(ROOT / "data.json"),
        "resultsSha256": sha256(ROOT / "results.json"),
        "sourceCertificates": source_records,
        "evidenceMap": {
            "A": "indexed finite retained-coset D and complete prescribed atomProxy sum; raw values retained",
            "B": "two high-precision endpoint proxies and two separate finite retained-coset diagnostics",
            "C": "high-precision delta collapse and finite retained-coset truncation comparison",
        },
        "claimBoundary": results["claimBoundary"],
    }
    (ROOT / "figure-data-metadata.json").write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_ndjson(ROOT / "progress.ndjson", {"stage": "producer-complete", "rowCount": len(rows), "elapsedSeconds": elapsed})
    append_ndjson(ROOT / "resource-log.ndjson", resource_record("producer-complete", started, rowCount=len(rows)))
    print(
        json.dumps(
            {
                "status": "passed",
                "rows": len(rows),
                "limitingCrosscheckMaximum": maximum_crosscheck_error,
                "derivedFits": derived_fits,
                "noExtraRootAndTailCases": f"{no_extra_root_cases}/{len(nonlinear)}",
                "elapsedSeconds": elapsed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
