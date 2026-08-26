#!/usr/bin/env python3
"""Independently validate the R0.71X endpoint-saturation figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
import os
from pathlib import Path
import re
import resource
import shutil
import subprocess
import time
import xml.etree.ElementTree as ET
from zoneinfo import ZoneInfo

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def append_log(path: Path, payload: dict[str, object]) -> None:
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps({"timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"), **payload}, sort_keys=True) + "\n")


def fit_power(x_values: list[float], y_values: list[float]) -> float:
    slope, _ = np.polyfit(np.log(np.asarray(x_values, dtype=float)), np.log(np.asarray(y_values, dtype=float)), 1)
    return float(slope)


def close(left: float, right: float, tolerance: float = 2.0e-12) -> bool:
    return math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)


def load_ndjson(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid {path.name} line {number}: {exc}") from exc
        if not isinstance(record, dict) or not record.get("timestamp"):
            raise RuntimeError(f"invalid {path.name} record at line {number}")
        records.append(record)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    config = json.loads(args.config.read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    data_json = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    sources: dict[str, dict[str, object]] = {}
    source_paths: dict[str, Path] = {}
    for label, relative in config["sourceCertificates"].items():
        path = REPOSITORY / relative
        source_paths[label] = path
        sources[label] = json.loads(path.read_text(encoding="utf-8"))

    check(
        "source/certificate provenance is a full commit hash",
        bool(re.fullmatch(r"[0-9a-f]{40}", config["sourceCertificateCommit"])),
        config["sourceCertificateCommit"],
    )
    check(
        "all source certificates and every recorded source check pass",
        all(source.get("status") == "passed" or source.get("passed") is True for source in sources.values())
        and all(bool(item["passed"]) for source in sources.values() for item in source["checks"]),
        {label: {"status": source.get("status"), "checks": len(source["checks"])} for label, source in sources.items()},
    )
    check(
        "source hashes match extraction metadata",
        all(
            next(record for record in metadata["sourceCertificates"] if record["label"] == label)["sha256"] == sha256(path)
            for label, path in source_paths.items()
        ),
        {label: sha256(path) for label, path in source_paths.items()},
    )

    with (ROOT / "data.csv").open(encoding="utf-8") as stream:
        csv_rows = list(csv.DictReader(stream))
    check(
        "CSV/JSON row counts agree",
        len(csv_rows) == data_json["rowCount"] == metadata["rowCount"] == 42,
        {"csv": len(csv_rows), "json": data_json["rowCount"], "metadata": metadata["rowCount"]},
    )
    string_fields = ("panel", "series", "unit", "formula", "evidenceClass", "source", "note")
    numeric_fields = ("delta", "x", "y", "rawValue", "referenceValue")
    check(
        "CSV and JSON rows are lossless",
        all(
            int(csv_row["q"]) == int(json_row["q"])
            and all(csv_row[field] == str(json_row[field]) for field in string_fields)
            and all(float(csv_row[field]) == float(json_row[field]) for field in numeric_fields)
            for csv_row, json_row in zip(csv_rows, data_json["rows"], strict=True)
        ),
        "all 42 rows compared field by field",
    )
    check(
        "data metadata hashes are current",
        metadata["configSha256"] == sha256(args.config)
        and metadata["dataCsvSha256"] == sha256(ROOT / "data.csv")
        and metadata["dataJsonSha256"] == sha256(ROOT / "data.json")
        and metadata["resultsSha256"] == sha256(ROOT / "results.json"),
        "config, CSV, JSON, and results digests",
    )
    index = {
        (row["panel"], row["series"], int(row["q"]), float(row["x"])): row
        for row in csv_rows
    }

    primary = sources["primary"]
    independent = sources["independent"]
    truncated = sources["truncatedCoset"]
    primary_coefficients = [float(value) for value in primary["limitingInterpolation"]["coefficients"]]
    independent_coefficients = [float(value) for value in independent["limitingResponse"]["coefficients"][:3]]
    primary_slopes = [abs(float(value)) for value in primary["limitingInterpolation"]["rootSlopes"]]
    independent_slopes = [abs(float(value)) for value in independent["limitingResponse"]["rootSlopes"]]
    cross_errors = [abs(left - right) / max(abs(left), abs(right), 1.0e-300) for left, right in zip(primary_coefficients + primary_slopes, independent_coefficients + independent_slopes, strict=True)]
    cross_errors.append(
        abs(float(primary["limitingInterpolation"]["tailLimit"]) - float(independent["limitingResponse"]["limitingTail"]))
        / max(abs(float(primary["limitingInterpolation"]["tailLimit"])), abs(float(independent["limitingResponse"]["limitingTail"])))
    )
    check(
        "primary and independent limiting algebra agree",
        max(cross_errors) < 2.0e-14 and close(max(cross_errors), results["independent"]["maximumLimitingAlgebraRelativeDifference"]),
        {"maximumRelativeDifference": max(cross_errors)},
    )

    nonlinear = truncated["mainContinuation"]
    d_reference = float(nonlinear[0]["initialData"]["D"])
    atom_reference = float(nonlinear[0]["completePrescribedAtomProxySum"])
    panel_a_errors: list[float] = []
    for case in nonlinear:
        q = int(case["q"])
        expected_pairs = (
            ("initial-data D indexed to q=256", float(case["initialData"]["D"]), d_reference),
            ("complete prescribed atomProxy sum indexed to q=256", float(case["completePrescribedAtomProxySum"]), atom_reference),
        )
        for series, raw, reference in expected_pairs:
            row = index[("A", series, q, float(q))]
            panel_a_errors.extend(
                [
                    abs(float(row["rawValue"]) - raw),
                    abs(float(row["referenceValue"]) - reference),
                    abs(float(row["y"]) - raw / reference),
                ]
            )
    check("Panel A reproduces raw and indexed retained-coset values", max(panel_a_errors, default=0.0) == 0.0, {"maximumAbsoluteError": max(panel_a_errors, default=0.0)})

    panel_b_errors: list[float] = []
    for source_row in primary["fixedDeltaRows"]:
        q = int(source_row["q"])
        for series, field in (
            ("high-precision endpoint atom-proxy ratio", "atomOverDataOneThird"),
            ("high-precision complete-ledger-normalized proxy", "atomOverDataOneThirdLedger"),
        ):
            panel_b_errors.append(abs(float(index[("B", series, q, float(q))]["y"]) - float(source_row[field])))
    for case in nonlinear:
        q = int(case["q"])
        for series, field in (
            ("finite-coset endpoint atomProxy ratio", "completePrescribedAtomProxySumOverDOneThird"),
            ("full retained rotational-charge upper bound", "retainedFullCosetHminus1LChargeUpperBound"),
        ):
            panel_b_errors.append(abs(float(index[("B", series, q, float(q))]["y"]) - float(case[field])))
    check("Panel B reproduces every analytic and retained-coset evidence layer", max(panel_b_errors, default=0.0) == 0.0, {"maximumAbsoluteError": max(panel_b_errors, default=0.0)})

    panel_c_errors: list[float] = []
    for source_row in primary["deltaCollapse"]["rows"]:
        delta = float(source_row["delta"])
        row = index[("C", "high-precision delta endpoint collapse", int(source_row["q"]), delta)]
        panel_c_errors.append(abs(float(row["y"]) - float(source_row["atomOverDataOneThird"])))
    truncation_fields = (
        "atomProxySumRelativeDifference",
        "endpointCoefficientRelativeDifference",
        "initialDRelativeDifference",
        "retainedChargeRelativeDifference",
    )
    truncation_values: list[float] = []
    for case in truncated["truncationAudit"]:
        radius = int(case["truncationRadius"])
        expected = max(float(case["comparisonToR40"][field]) for field in truncation_fields)
        actual = float(index[("C-inset", "maximum retained-observable relative difference versus R=40", int(case["q"]), float(radius))]["y"])
        panel_c_errors.append(abs(actual - expected))
        truncation_values.append(actual)
    check("Panel C reproduces the delta sweep and truncation inset", max(panel_c_errors, default=0.0) == 0.0, {"maximumAbsoluteError": max(panel_c_errors, default=0.0)})

    independent_powers = {
        "fixedDeltaInitialDataD": fit_power([float(case["q"]) for case in nonlinear], [float(case["initialData"]["D"]) for case in nonlinear]),
        "fixedDeltaCompletePrescribedAtomProxySum": fit_power([float(case["q"]) for case in nonlinear], [float(case["completePrescribedAtomProxySum"]) for case in nonlinear]),
        "finiteCosetEndpointAtomProxyRatio": fit_power([float(case["q"]) for case in nonlinear], [float(case["completePrescribedAtomProxySumOverDOneThird"]) for case in nonlinear]),
        "fullRetainedRotationalChargeUpper": fit_power([float(case["q"]) for case in nonlinear], [float(case["retainedFullCosetHminus1LChargeUpperBound"]) for case in nonlinear]),
        "deltaEndpointCollapse": fit_power([float(row["delta"]) for row in primary["deltaCollapse"]["rows"]], [float(row["atomOverDataOneThird"]) for row in primary["deltaCollapse"]["rows"]]),
    }
    check(
        "independent fitted powers reproduce producer fits",
        all(close(value, results["derivedFigureFits"][key]["power"]) for key, value in independent_powers.items()),
        independent_powers,
    )
    check(
        "observed powers match q^6, q^2, q^0, and delta^(4/3)",
        abs(independent_powers["fixedDeltaInitialDataD"] - 6.0) < 0.002
        and abs(independent_powers["fixedDeltaCompletePrescribedAtomProxySum"] - 2.0) < 0.002
        and abs(independent_powers["finiteCosetEndpointAtomProxyRatio"]) < 0.002
        and abs(independent_powers["fullRetainedRotationalChargeUpper"]) < 0.002
        and abs(independent_powers["deltaEndpointCollapse"] - 4.0 / 3.0) < 2.0e-12,
        independent_powers,
    )
    check(
        "finite retained-coset roots, no-extra-root scans, and tail diagnostics pass",
        len(nonlinear) == 5
        and all(case["rootSolve"]["success"] for case in nonlinear)
        and max(float(case["rootSolve"]["maximumDimensionlessRootResidual"]) for case in nonlinear) < 1.0e-10
        and min(float(case["minimumTheta"]) for case in nonlinear) > 0.15
        and all(case["noExtraRootCorroboration"]["noExtraRealRootScanPassed"] for case in nonlinear)
        and all(case["noExtraRootCorroboration"]["integratingFactor"]["tailProxyPassed"] for case in nonlinear),
        {"cases": len(nonlinear), "passed": results["truncatedCoset"]["noExtraRootAndTailCasesPassed"]},
    )
    check(
        "retained observables are truncation-stable at recorded radii",
        max(truncation_values) < 5.0e-12,
        {str(case["truncationRadius"]): value for case, value in zip(truncated["truncationAudit"], truncation_values, strict=True)},
    )
    check(
        "full retained charge upper field is used without target-only substitution",
        all(float(case["retainedFullCosetHminus1LChargeUpperBound"]) >= float(case["retainedFullCosetHminus1LCharge"]) for case in nonlinear),
        "all retained convolution modes plus stored tail upper bound",
    )

    figure_config = config["figure"]
    expected_width = round(round(float(figure_config["widthMillimetres"]) / 25.4, 2) * int(figure_config["pngDpi"]))
    expected_height = round(round(float(figure_config["heightMillimetres"]) / 25.4, 2) * int(figure_config["pngDpi"]))
    with Image.open(ROOT / "figure.png") as image:
        png_pixels = [image.width, image.height]
        png_dpi = image.info.get("dpi", (0.0, 0.0))
    check(
        "archival PNG is final-size 600 dpi",
        abs(png_pixels[0] - expected_width) <= 3 and abs(png_pixels[1] - expected_height) <= 3 and min(png_dpi) >= 599.0,
        {"pixels": png_pixels, "dpi": png_dpi},
    )
    svg_root = ET.parse(ROOT / "figure.svg").getroot()
    svg_width = svg_root.attrib.get("width", "")
    svg_height = svg_root.attrib.get("height", "")
    check(
        "SVG has the declared physical page size",
        svg_width.endswith("pt")
        and svg_height.endswith("pt")
        and abs(float(svg_width[:-2]) * 25.4 / 72.0 - float(figure_config["widthMillimetres"])) < 0.5
        and abs(float(svg_height[:-2]) * 25.4 / 72.0 - float(figure_config["heightMillimetres"])) < 0.5,
        {"width": svg_width, "height": svg_height},
    )
    svg_text = (ROOT / "figure.svg").read_text(encoding="utf-8").lower()
    declared_colors = {value.lower() for value in contract["palette"].values()}
    used_hex = set(re.findall(r"#[0-9a-f]{6}", svg_text))
    check("SVG colors stay inside the declared palette", used_hex.issubset(declared_colors), {"used": sorted(used_hex), "declared": sorted(declared_colors)})

    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        raise FileNotFoundError("pdfinfo is required for independent PDF validation")
    pdf_report = subprocess.run([pdfinfo, str(ROOT / "figure.pdf")], check=True, text=True, capture_output=True).stdout
    page_match = re.search(r"^Pages:\s+(\d+)$", pdf_report, re.MULTILINE)
    size_match = re.search(r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", pdf_report, re.MULTILINE)
    pdf_width_mm = float(size_match.group(1)) * 25.4 / 72.0 if size_match else 0.0
    pdf_height_mm = float(size_match.group(2)) * 25.4 / 72.0 if size_match else 0.0
    check(
        "PDF is one page at the declared physical size",
        page_match is not None
        and int(page_match.group(1)) == 1
        and abs(pdf_width_mm - float(figure_config["widthMillimetres"])) < 0.5
        and abs(pdf_height_mm - float(figure_config["heightMillimetres"])) < 0.5,
        {"pages": page_match.group(1) if page_match else None, "millimetres": [pdf_width_mm, pdf_height_mm]},
    )

    qa_report = (ROOT / "qa-report.md").read_text(encoding="utf-8")
    check(
        "manual color, grayscale, and PDF QA is complete",
        "PENDING" not in qa_report
        and all(token in qa_report for token in ("Panel A indexed", "Panel B four", "Panel C delta", "atomProxy-not-J_*", "non-color line-style", "PDF-specific clipping")),
        "qa-report.md",
    )
    caption = " ".join((ROOT / "caption.md").read_text(encoding="utf-8").lower().split())
    check(
        "caption states every material evidence boundary",
        "atomproxy is not" in caption
        and "not dns" in caption
        and "does not prove spectral convergence" in caption
        and "delta=1/128" in caption
        and "has not been" in caption
        and "no universal" in caption
        and "regularity" in caption,
        "caption.md",
    )
    boundary = str(contract["claimBoundary"]).lower()
    check(
        "contract forbids J_*, continuum-radius, DNS, and regularity overclaim",
        "not the multiplier-locked j_*" in boundary
        and "not dns" in boundary
        and "delta=1/128 has not been proved" in boundary
        and "no universal" in boundary
        and "no navier-stokes regularity" in boundary,
        contract["claimBoundary"],
    )
    progress = load_ndjson(ROOT / "progress.ndjson")
    resource_log = load_ndjson(ROOT / "resource-log.ndjson")
    check(
        "progress and resource monitoring logs are populated",
        any(record.get("stage") == "producer-complete" for record in progress)
        and any(record.get("stage") == "plot-complete" for record in progress)
        and any(record.get("stage") == "qa-complete" for record in progress)
        and len(resource_log) >= 3,
        {"progressRecords": len(progress), "resourceRecords": len(resource_log)},
    )

    elapsed = time.perf_counter() - started
    append_log(ROOT / "progress.ndjson", {"stage": "validation-complete", "passed": sum(bool(item["passed"]) for item in checks), "total": len(checks), "elapsedSeconds": elapsed})
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(
        ROOT / "resource-log.ndjson",
        {
            "stage": "validation-complete",
            "elapsedSeconds": elapsed,
            "pid": os.getpid(),
            "processUserCpuSeconds": usage.ru_utime,
            "processSystemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
        },
    )
    passed = all(bool(item["passed"]) for item in checks)
    payload = {
        "status": "passed" if passed else "failed",
        "release": config["release"],
        "figureId": config["figureId"],
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "method": "independent source-to-CSV reconstruction, independent log-log regressions, output-format checks, PDF/SVG/raster checks, and recorded manual final-size QA",
        "wallSeconds": elapsed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(item["passed"]) for item in checks),
        "independentPowers": independent_powers,
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
