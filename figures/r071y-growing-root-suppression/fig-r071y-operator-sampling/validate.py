#!/usr/bin/env python3
"""Independently validate the R0.71Y operator-sampling figure package."""

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


def lattice_cost(n_value: int) -> float:
    m_value = 2 * n_value + 1
    return float(m_value * (m_value + 1) * (2 * m_value + 1) / 6)


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

    commit = str(config["sourceCertificateCommit"])
    check(
        "source/certificate provenance is a full commit hash",
        bool(re.fullmatch(r"[0-9a-f]{40}", commit)),
        commit,
    )
    committed_source_hashes: dict[str, str] = {}
    for label, relative in config["sourceCertificates"].items():
        committed_bytes = subprocess.run(
            ["git", "show", f"{commit}:{relative}"],
            cwd=REPOSITORY,
            check=True,
            capture_output=True,
        ).stdout
        committed_source_hashes[label] = hashlib.sha256(committed_bytes).hexdigest()
    check(
        "source certificates exactly match the recorded commit",
        all(committed_source_hashes[label] == sha256(path) for label, path in source_paths.items()),
        committed_source_hashes,
    )
    check(
        "all source certificates and every recorded source check pass",
        all(source.get("status") == "passed" and source.get("release") == config["release"] for source in sources.values())
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
        len(csv_rows) == data_json["rowCount"] == metadata["rowCount"] == 110,
        {"csv": len(csv_rows), "json": data_json["rowCount"], "metadata": metadata["rowCount"]},
    )
    string_fields = ("panel", "series", "unit", "formula", "evidenceClass", "source", "note")
    numeric_fields = ("h", "deltaObs", "x", "y", "rawValue", "referenceValue")
    check(
        "CSV and JSON rows are lossless",
        all(
            int(csv_row["N"]) == int(json_row["N"])
            and int(csv_row["M"]) == int(json_row["M"])
            and all(csv_row[field] == str(json_row[field]) for field in string_fields)
            and all(float(csv_row[field]) == float(json_row[field]) for field in numeric_fields)
            for csv_row, json_row in zip(csv_rows, data_json["rows"], strict=True)
        ),
        "all 110 rows compared field by field",
    )
    check(
        "data metadata hashes are current",
        metadata["configSha256"] == sha256(args.config)
        and metadata["contractSha256"] == sha256(ROOT / "contract.json")
        and metadata["dataCsvSha256"] == sha256(ROOT / "data.csv")
        and metadata["dataJsonSha256"] == sha256(ROOT / "data.json")
        and metadata["resultsSha256"] == sha256(ROOT / "results.json"),
        "config, contract, CSV, JSON, and results digests",
    )
    index = {(row["panel"], row["series"], int(row["N"])): row for row in csv_rows}

    primary = sources["primary"]
    independent = sources["independent"]
    n_values = [int(value) for value in primary["parameters"]["NValues"]]
    panel_a_errors: list[float] = []
    for n_value in n_values:
        m_value = 2 * n_value + 1
        ks_value = lattice_cost(n_value)
        exact = n_value * m_value / ks_value
        upper = 3.0 / (4.0 * n_value)
        for series, expected, reference in (
            ("exact minimum-lattice factor NM/Ks", exact, upper),
            ("analytic upper bound 3/(4N)", upper, exact),
        ):
            row = index[("A", series, n_value)]
            panel_a_errors.extend(
                [
                    abs(float(row["rawValue"]) - expected),
                    abs(float(row["y"]) - expected),
                    abs(float(row["referenceValue"]) - reference),
                ]
            )
    check(
        "Panel A independently reproduces the exact lattice identity and bound",
        max(panel_a_errors, default=0.0) < 2.0e-16,
        {"maximumAbsoluteError": max(panel_a_errors, default=0.0)},
    )

    fixed_delta = float(config["fixedDeltaObs"])
    source_envelope = next(row for row in primary["envelopeRows"] if float(row["deltaObs"]) == fixed_delta)
    source_envelope_index = {int(row["N"]): float(row["upperEnvelope"]) for row in source_envelope["values"]}
    b_rate = 2.0 * float(primary["parameters"]["nu"]) * float(primary["parameters"]["d"]) ** 2
    fixed_gap = float(config["fixedGap"])
    raw_series: dict[str, list[float]] = {
        "no separation; fixed delta_obs=1/8": [],
        "separated; fixed h=0.05": [],
        "separated; h=N^-1": [],
    }
    for n_value in n_values:
        m_value = 2 * n_value + 1
        ks_value = lattice_cost(n_value)
        raw_series["no separation; fixed delta_obs=1/8"].append(source_envelope_index[n_value])
        raw_series["separated; fixed h=0.05"].append(m_value / (b_rate * fixed_gap * ks_value))
        raw_series["separated; h=N^-1"].append(m_value / (b_rate * (1.0 / n_value) * ks_value))
    panel_b_errors: list[float] = []
    for series, values in raw_series.items():
        reference = values[0]
        for n_value, expected in zip(n_values, values, strict=True):
            row = index[("B", series, n_value)]
            panel_b_errors.extend(
                [
                    abs(float(row["rawValue"]) - expected),
                    abs(float(row["referenceValue"]) - reference),
                    abs(float(row["y"]) - expected / reference),
                ]
            )
    check(
        "Panel B independently reconstructs every normalized theorem envelope",
        max(panel_b_errors, default=0.0) < 2.0e-16,
        {"maximumAbsoluteError": max(panel_b_errors, default=0.0)},
    )

    independent_powers = {
        "latticeFactor": fit_power(n_values[-6:], [n * (2 * n + 1) / lattice_cost(n) for n in n_values[-6:]]),
        "noSeparationFixedDeltaObs": fit_power(n_values[-6:], raw_series["no separation; fixed delta_obs=1/8"][-6:]),
        "separatedFixedGap": fit_power(n_values[-6:], raw_series["separated; fixed h=0.05"][-6:]),
        "separatedQuasiuniformGap": fit_power(n_values[-6:], raw_series["separated; h=N^-1"][-6:]),
    }
    check(
        "independent fitted powers reproduce producer and source fits",
        all(close(value, results["derivedFigureFits"][key]["power"]) for key, value in independent_powers.items())
        and all(close(value, results["sourceFitValues"][key]) for key, value in independent_powers.items()),
        independent_powers,
    )
    check(
        "theorem-envelope powers are N^-1, N^-2, and N^-1",
        abs(independent_powers["latticeFactor"] + 1.0) < 0.002
        and abs(independent_powers["noSeparationFixedDeltaObs"] + 1.0) < 0.002
        and abs(independent_powers["separatedFixedGap"] + 2.0) < 0.002
        and abs(independent_powers["separatedQuasiuniformGap"] + 1.0) < 0.002,
        independent_powers,
    )
    coincidence_errors = [
        abs(
            float(index[("B", "no separation; fixed delta_obs=1/8", n_value)]["y"])
            - float(index[("B", "separated; h=N^-1", n_value)]["y"])
        )
        for n_value in n_values
    ]
    check(
        "normalized no-separation and h=N^-1 laws coincide exactly",
        max(coincidence_errors, default=0.0) < 2.0e-15,
        {"maximumAbsoluteDifference": max(coincidence_errors, default=0.0)},
    )

    panel_c_errors: list[float] = []
    inverse_logs: list[float] = []
    for n_value in config["equalGridNValues"]:
        n_value = int(n_value)
        gap = n_value ** -3.0
        base = b_rate * gap * (n_value + 1.0) ** 2
        expected_log = -math.log10(gap) - 0.5 * (n_value - 1) * math.log10(base)
        row = index[("C", "equal-grid inverse lower bound; h=N^-3", n_value)]
        panel_c_errors.extend(
            [
                abs(float(row["h"]) - gap),
                abs(float(row["referenceValue"]) - base),
                abs(float(row["y"]) - expected_log),
                abs(math.log10(float(row["rawValue"])) - expected_log),
            ]
        )
        inverse_logs.append(float(row["y"]))
    check(
        "Panel C independently reconstructs the determinant-based inverse lower bound",
        max(panel_c_errors, default=0.0) < 2.0e-14,
        {"maximumAbsoluteError": max(panel_c_errors, default=0.0)},
    )
    check(
        "equal-grid h=N^-3 lower bound grows through more than 47 decades",
        all(right > left for left, right in zip(inverse_logs, inverse_logs[1:]))
        and inverse_logs[-1] - inverse_logs[0] > 47.0,
        {"first": inverse_logs[0], "last": inverse_logs[-1], "increase": inverse_logs[-1] - inverse_logs[0]},
    )

    independent_index = {int(row["N"]): row for row in independent["rows"]}
    independent_lattice_errors = []
    for n_value, source_row in independent_index.items():
        expected = (n_value * (2 * n_value + 1) / lattice_cost(n_value)) / (3.0 / (4.0 * n_value))
        independent_lattice_errors.append(abs(float(source_row["latticeBoundRatio"]) - expected))
    check(
        "independent finite matrices corroborate contraction, sampling, and lattice algebra",
        all(bool(item["passed"]) for item in independent["checks"])
        and max(independent_lattice_errors, default=0.0) < 2.0e-15
        and min(float(row["boundRatio"]) for row in independent["equalGridRows"]) > 1.0,
        {
            "checks": len(independent["checks"]),
            "maximumLatticeAbsoluteError": max(independent_lattice_errors, default=0.0),
            "minimumEqualGridBoundRatio": min(float(row["boundRatio"]) for row in independent["equalGridRows"]),
        },
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
    check(
        "SVG colors stay inside the declared palette",
        used_hex.issubset(declared_colors),
        {"used": sorted(used_hex), "declared": sorted(declared_colors)},
    )
    check(
        "SVG retains the visible neutral title and evidence caveat",
        "growing-root operator-sampling bounds" in svg_text
        and "analytic/certificate envelopes" in svg_text
        and "not dns" in svg_text,
        "figure.svg text layer",
    )

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
        and all(
            token in qa_report
            for token in (
                "Panel A exact lattice",
                "Panel B three theorem-envelope",
                "Panel C log10 inverse",
                "analytic/certificate-envelope",
                "non-color line-style",
                "PDF-specific clipping",
            )
        ),
        "qa-report.md",
    )
    caption = " ".join((ROOT / "caption.md").read_text(encoding="utf-8").lower().split())
    check(
        "caption states every material evidence boundary",
        "analytic/certificate envelopes" in caption
        and "not simulated" in caption
        and "not an upper bound" in caption
        and "unit carrier phases" in caption
        and "enstrophy floors" in caption
        and "neither construct" in caption
        and "not dns" in caption
        and "no universal endpoint" in caption
        and "regularity" in caption,
        "caption.md",
    )
    boundary = str(contract["claimBoundary"]).lower()
    check(
        "contract forbids construction, all-root, IFT-radius, DNS, endpoint, and regularity overclaim",
        all(
            token in boundary
            for token in (
                "not a simulated trajectory",
                "selected-root",
                "do not construct",
                "count every nonlinear root",
                "not an upper bound",
                "not dns",
                "no universal endpoint",
                "regularity",
            )
        ),
        contract["claimBoundary"],
    )

    progress_records = load_ndjson(ROOT / "progress.ndjson")
    resource_records = load_ndjson(ROOT / "resource-log.ndjson")
    check(
        "progress and resource monitoring logs are populated",
        len(progress_records) >= 32
        and len(resource_records) >= 3
        and any(record.get("stage") == "producer-complete" for record in progress_records)
        and any(record.get("stage") == "plot-complete" for record in progress_records)
        and any(record.get("stage") == "qa-complete" for record in progress_records),
        {"progressRecords": len(progress_records), "resourceRecords": len(resource_records)},
    )

    elapsed = time.perf_counter() - started
    passed = all(item["passed"] for item in checks)
    payload = {
        "release": config["release"],
        "figureId": config["figureId"],
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "status": "passed" if passed else "failed",
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(item["passed"]) for item in checks),
        "method": "independent source-commit verification, exact source-to-CSV reconstruction, independent power fits, determinant-bound reconstruction, output-format checks, and recorded manual final-size QA",
        "independentPowers": independent_powers,
        "checks": checks,
        "wallSeconds": elapsed,
    }
    (ROOT / "validation.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    append_log(ROOT / "progress.ndjson", {"stage": "validation-complete", "passed": passed, "checkCount": len(checks), "elapsedSeconds": elapsed})
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
    print(json.dumps(payload, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
