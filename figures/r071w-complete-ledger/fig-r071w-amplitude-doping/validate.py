#!/usr/bin/env python3
"""Independently validate the R0.71W amplitude-doping figure package."""

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
    record = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        **payload,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def fit_power(q_values: list[float], values: list[float]) -> float:
    slope, _ = np.polyfit(
        np.log(np.asarray(q_values, dtype=float)),
        np.log(np.asarray(values, dtype=float)),
        1,
    )
    return float(slope)


def close(left: float, right: float, tolerance: float = 2.0e-12) -> bool:
    return math.isclose(left, right, rel_tol=tolerance, abs_tol=tolerance)


def load_ndjson(path: Path) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"invalid {path.name} line {line_number}: {exc}") from exc
        if not isinstance(record, dict) or not record.get("timestamp"):
            raise RuntimeError(f"invalid {path.name} record at line {line_number}")
        records.append(record)
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    checks: list[dict[str, object]] = []

    def check(name: str, condition: bool, detail: object) -> None:
        checks.append({"name": name, "passed": bool(condition), "detail": detail})

    config = json.loads(arguments.config.read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    data_json = json.loads((ROOT / "data.json").read_text(encoding="utf-8"))
    metadata = json.loads(
        (ROOT / "figure-data-metadata.json").read_text(encoding="utf-8")
    )
    source_payloads: dict[str, dict[str, object]] = {}
    source_paths: dict[str, Path] = {}
    for label, relative in config["sourceCertificates"].items():
        path = REPOSITORY / relative
        source_paths[label] = path
        source_payloads[label] = json.loads(path.read_text(encoding="utf-8"))

    check(
        "source/certificate provenance is a full commit hash",
        bool(re.fullmatch(r"[0-9a-f]{40}", config["sourceCertificateCommit"])),
        config["sourceCertificateCommit"],
    )
    check(
        "all source certificates pass",
        all(
            payload.get("status") == "passed"
            or payload.get("passed") is True
            for payload in source_payloads.values()
        ),
        {label: payload.get("status") for label, payload in source_payloads.items()},
    )
    check(
        "source hashes match extraction metadata",
        all(
            next(
                record
                for record in metadata["sourceCertificates"]
                if record["label"] == label
            )["sha256"]
            == sha256(path)
            for label, path in source_paths.items()
        ),
        {label: sha256(path) for label, path in source_paths.items()},
    )

    with (ROOT / "data.csv").open(encoding="utf-8") as stream:
        csv_rows = list(csv.DictReader(stream))
    check(
        "CSV/JSON row counts agree",
        len(csv_rows) == data_json["rowCount"] == metadata["rowCount"] == 31,
        {
            "csv": len(csv_rows),
            "json": data_json["rowCount"],
            "metadata": metadata["rowCount"],
        },
    )
    check(
        "CSV and JSON rows are lossless",
        all(
            csv_row["panel"] == json_row["panel"]
            and csv_row["series"] == json_row["series"]
            and int(csv_row["q"]) == int(json_row["q"])
            and float(csv_row["x"]) == float(json_row["x"])
            and float(csv_row["y"]) == float(json_row["y"])
            and all(
                csv_row[field] == str(json_row[field])
                for field in ("unit", "formula", "evidenceClass", "source", "note")
            )
            for csv_row, json_row in zip(csv_rows, data_json["rows"], strict=True)
        ),
        "all 31 plotting rows compared field by field",
    )
    check(
        "data metadata hashes are current",
        metadata["configSha256"] == sha256(arguments.config)
        and metadata["dataCsvSha256"] == sha256(ROOT / "data.csv")
        and metadata["dataJsonSha256"] == sha256(ROOT / "data.json")
        and metadata["resultsSha256"] == sha256(ROOT / "results.json"),
        "config, CSV, JSON, and results digests",
    )

    index = {
        (row["panel"], row["series"], int(row["q"]), float(row["x"])): float(
            row["y"]
        )
        for row in csv_rows
    }
    primary_ledger = source_payloads["primary"]["checks"]["amplitudeDopedLedger"]
    independent_ledger = source_payloads["independent"]["checks"][
        "independentAmplitudeLedger"
    ]
    analytic_errors: list[float] = []
    cross_errors: list[float] = []
    for primary_row, independent_row in zip(
        primary_ledger["rows"], independent_ledger["rows"], strict=True
    ):
        q_value = int(primary_row["q"])
        analytic_errors.append(
            abs(
                index[("A", "atom over complete-ledger proxy", q_value, float(q_value))]
                - float(primary_row["atomToCompleteLedgerProxy"])
            )
        )
        for field in (
            "atomToCompleteLedgerProxy",
            "completeLedgerProxy",
            "leadingAtomProxy",
            "rotationalChargeUpper",
        ):
            left = float(primary_row[field])
            right = float(independent_row[field])
            cross_errors.append(abs(left - right) / max(abs(left), abs(right), 1.0e-300))
    check(
        "Panel A reproduces every certified analytic value",
        max(analytic_errors, default=0.0) == 0.0,
        {"maximumAbsoluteError": max(analytic_errors, default=0.0)},
    )
    check(
        "primary and independent analytic ledgers agree",
        max(cross_errors, default=0.0) < 2.0e-12,
        {"maximumRelativeDifference": max(cross_errors, default=0.0)},
    )

    truncated = source_payloads["truncatedCoset"]
    nonlinear_errors: list[float] = []
    root_residuals: list[float] = []
    for case in truncated["mainContinuation"]:
        q_value = int(case["q"])
        nonlinear_errors.extend(
            [
                abs(
                    index[("B", "nonlinear truncated atom proxy", q_value, float(q_value))]
                    - float(case["secondRootAtomProxy"])
                ),
                abs(
                    index[("B", "full retained H^-1 rotational charge", q_value, float(q_value))]
                    - float(case["retainedCosetHminus1LChargeUpperBound"])
                ),
                abs(
                    index[("C", "normalized second-root slope", q_value, float(q_value))]
                    - float(case["normalizedRootSlopes"][1])
                ),
            ]
        )
        root_residuals.append(float(case["rootSolve"]["maximumRootResidual"]))
    check(
        "Panels B-C reproduce every retained-coset value",
        max(nonlinear_errors, default=0.0) == 0.0,
        {"maximumAbsoluteError": max(nonlinear_errors, default=0.0)},
    )
    check(
        "nonlinear roots close and remain transverse",
        max(root_residuals) < 1.0e-9
        and min(
            float(case["normalizedRootSlopes"][1])
            for case in truncated["mainContinuation"]
        )
        > 0.15,
        {
            "maximumRootResidual": max(root_residuals),
            "minimumSecondRootSlopeOverA2": min(
                float(case["normalizedRootSlopes"][1])
                for case in truncated["mainContinuation"]
            ),
        },
    )
    check(
        "the plotted rotational charge is full retained-coset plus tail",
        all(
            float(case["retainedCosetHminus1LChargeUpperBound"])
            >= float(case["retainedCosetHminus1LCharge"])
            for case in truncated["mainContinuation"]
        ),
        "upper-bound field used; no target-only substitution",
    )

    truncation_errors: list[float] = []
    for case in truncated["truncationAudit"]:
        radius = int(case["truncationRadius"])
        expected = float(case["comparisonToR40"]["secondRootSlopeRelativeDifference"])
        actual = index[
            (
                "C-inset",
                "slope relative difference versus R=40",
                int(case["q"]),
                float(radius),
            )
        ]
        truncation_errors.append(abs(actual - expected))
    check(
        "q=1024 truncation audit is reproduced",
        max(truncation_errors, default=0.0) == 0.0,
        {"maximumAbsoluteError": max(truncation_errors, default=0.0)},
    )
    check(
        "q=1024 slope is radius-stable at recorded radii",
        max(
            float(case["comparisonToR40"]["secondRootSlopeRelativeDifference"])
            for case in truncated["truncationAudit"]
        )
        < 1.0e-12,
        {
            str(case["truncationRadius"]): case["comparisonToR40"][
                "secondRootSlopeRelativeDifference"
            ]
            for case in truncated["truncationAudit"]
        },
    )

    analytic_q = [float(row["q"]) for row in primary_ledger["rows"]]
    analytic_ratio = [
        float(row["atomToCompleteLedgerProxy"]) for row in primary_ledger["rows"]
    ]
    nonlinear_q = [float(case["q"]) for case in truncated["mainContinuation"]]
    nonlinear_atom = [
        float(case["secondRootAtomProxy"]) for case in truncated["mainContinuation"]
    ]
    nonlinear_charge = [
        float(case["retainedCosetHminus1LChargeUpperBound"])
        for case in truncated["mainContinuation"]
    ]
    independent_powers = {
        "analyticAtomToCompleteLedgerTailFour": fit_power(
            analytic_q[-4:], analytic_ratio[-4:]
        ),
        "nonlinearAtomProxy": fit_power(nonlinear_q, nonlinear_atom),
        "nonlinearRotationalCharge": fit_power(nonlinear_q, nonlinear_charge),
    }
    check(
        "independent fitted powers reproduce producer fits",
        close(
            independent_powers["analyticAtomToCompleteLedgerTailFour"],
            results["derivedFigureFits"]["analyticAtomToCompleteLedger"]["power"],
        )
        and close(
            independent_powers["nonlinearAtomProxy"],
            results["derivedFigureFits"]["nonlinearAtomProxy"]["power"],
        )
        and close(
            independent_powers["nonlinearRotationalCharge"],
            results["derivedFigureFits"]["nonlinearRotationalCharge"]["power"],
        ),
        independent_powers,
    )
    check(
        "observed powers match the displayed +1/+1/-1 guides",
        abs(independent_powers["analyticAtomToCompleteLedgerTailFour"] - 1.0) < 0.01
        and abs(independent_powers["nonlinearAtomProxy"] - 1.0) < 0.01
        and abs(independent_powers["nonlinearRotationalCharge"] + 1.0) < 0.01,
        independent_powers,
    )

    figure_config = config["figure"]
    expected_width = round(
        round(float(figure_config["widthMillimetres"]) / 25.4, 2)
        * int(figure_config["pngDpi"])
    )
    expected_height = round(
        round(float(figure_config["heightMillimetres"]) / 25.4, 2)
        * int(figure_config["pngDpi"])
    )
    with Image.open(ROOT / "figure.png") as image:
        png_pixels = [image.width, image.height]
        png_dpi = image.info.get("dpi", (0.0, 0.0))
    check(
        "archival PNG is final-size 600 dpi",
        abs(png_pixels[0] - expected_width) <= 3
        and abs(png_pixels[1] - expected_height) <= 3
        and min(png_dpi) >= 599.0,
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

    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        raise FileNotFoundError("pdfinfo is required for independent PDF validation")
    pdf_report = subprocess.run(
        [pdfinfo, str(ROOT / "figure.pdf")],
        check=True,
        text=True,
        capture_output=True,
    ).stdout
    page_match = re.search(r"^Pages:\s+(\d+)$", pdf_report, re.MULTILINE)
    size_match = re.search(
        r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", pdf_report, re.MULTILINE
    )
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
        "manual color/grayscale/PDF QA is complete",
        "PENDING" not in qa_report
        and all(
            token in qa_report
            for token in (
                "Panel A ratio",
                "Panel B atom",
                "Panel C normalized slope",
                "non-color line-style",
                "PDF-specific clipping",
            )
        ),
        "qa-report.md",
    )
    caption = (ROOT / "caption.md").read_text(encoding="utf-8").lower()
    check(
        "caption states the evidence boundary",
        "computation corroboration only" in caption
        and "not dns" in caption
        and "continuum" in caption
        and "retained" in caption,
        "caption.md",
    )
    boundary_text = str(contract["claimBoundary"]).lower()
    check(
        "contract forbids continuum and DNS overclaim",
        "not dns" in boundary_text
        and "does not prove spectral-truncation convergence" in boundary_text
        and "does not prove" in boundary_text
        and "implicit-function theorem" in boundary_text,
        contract["claimBoundary"],
    )

    progress = load_ndjson(ROOT / "progress.ndjson")
    resources = load_ndjson(ROOT / "resource-log.ndjson")
    stages = {str(record.get("stage")) for record in progress}
    check(
        "progress and resource monitoring are populated",
        {"producer-start", "producer-complete", "plot-start", "plot-complete", "qa-start", "qa-complete"}.issubset(stages)
        and len(resources) >= 3,
        {"progressRecords": len(progress), "resourceRecords": len(resources), "stages": sorted(stages)},
    )

    elapsed = time.perf_counter() - started
    failed = [item for item in checks if not item["passed"]]
    payload = {
        "status": "passed" if not failed else "failed",
        "method": (
            "Matplotlib-independent certificate/data reconstruction, independent "
            "log-log refits, Poppler page audit, SVG/XML audit, and Pillow raster audit"
        ),
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        "wallSeconds": elapsed,
        "checkCount": len(checks),
        "failedCheckCount": len(failed),
        "independentPowers": independent_powers,
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(
        ROOT / "progress.ndjson",
        {
            "stage": "validation-complete",
            "status": payload["status"],
            "checkCount": len(checks),
            "elapsedSeconds": elapsed,
        },
    )
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
    print(json.dumps(payload, indent=2))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
