#!/usr/bin/env python3
"""Independently validate the R0.71Z figure data, exports, and QA record."""

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
from zoneinfo import ZoneInfo

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def close(left: float, right: float, tolerance: float = 5.0e-13) -> bool:
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def fit_power(x_values: list[float], y_values: list[float]) -> float:
    return float(np.polyfit(np.log(np.asarray(x_values)), np.log(np.asarray(y_values)), 1)[0])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    metadata = json.loads((ROOT / "figure-data-metadata.json").read_text(encoding="utf-8"))
    with (ROOT / "data.csv").open(encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))

    checks: list[dict[str, object]] = []

    def check(name: str, passed: bool, value: object) -> None:
        checks.append({"name": name, "passed": bool(passed), "value": value})

    primary_path = REPOSITORY / Path(config["sourceCertificates"]["primary"])
    independent_path = REPOSITORY / Path(config["sourceCertificates"]["independent"])
    primary = json.loads(primary_path.read_text(encoding="utf-8"))
    independent = json.loads(independent_path.read_text(encoding="utf-8"))
    check(
        "primary certificate remains fully passed",
        primary.get("status") == "passed" and all(bool(item.get("passed")) for item in primary.get("checks", [])),
        {"status": primary.get("status"), "checkCount": len(primary.get("checks", []))},
    )
    check(
        "independent certificate remains fully passed",
        independent.get("passed") is True and all(bool(item.get("passed")) for item in independent.get("checks", [])),
        {"passed": independent.get("passed"), "checkCount": len(independent.get("checks", []))},
    )
    recorded_sources = {item["path"]: item for item in metadata["sourceCertificates"]}
    source_hash_errors = []
    for relative in [*config["sourceCertificates"].values(), *config["analyticSources"]]:
        path = REPOSITORY / Path(relative)
        source_hash_errors.append(0 if recorded_sources[relative]["sha256"] == sha256(path) else 1)
    check("all source hashes remain exact", not any(source_hash_errors), {"mismatches": sum(source_hash_errors)})

    check(
        "data and result hashes match metadata",
        metadata["dataCsvSha256"] == sha256(ROOT / "data.csv")
        and metadata["dataJsonSha256"] == sha256(ROOT / "data.json")
        and metadata["resultsSha256"] == sha256(ROOT / "results.json"),
        {
            "dataCsv": sha256(ROOT / "data.csv"),
            "dataJson": sha256(ROOT / "data.json"),
            "results": sha256(ROOT / "results.json"),
        },
    )
    check("row count is complete", len(rows) == 274 == int(metadata["rowCount"]), {"rowCount": len(rows)})

    index = {(row["panel"], row["series"], float(row["x"])): row for row in rows}
    m_values = [int(value) for value in results["parameters"]["MValues"]]
    formula_errors: list[float] = []
    for m_value in m_values:
        ks = m_value * (m_value + 1) * (2 * m_value + 1) / 6.0
        exact = m_value / ks
        upper = 3.0 / m_value**2
        formula_errors.extend(
            [
                abs(float(index[("A", "exact minimum-lattice factor M/Ks", float(m_value))]["y"]) - exact),
                abs(float(index[("A", "analytic upper bound 3/M^2", float(m_value))]["y"]) - upper),
            ]
        )
    check("Panel A independently reconstructs every lattice row", max(formula_errors, default=0.0) < 2.0e-16, {"maximumAbsoluteError": max(formula_errors, default=0.0)})

    b_complete = [index[("B", "complete-root BV envelope; eta=1", float(m))] for m in m_values]
    b_selected = [index[("B", "prior selected-root envelope; N=(M-1)/2", float(m))] for m in m_values]
    relation_errors = [
        abs(float(selected["rawValue"]) - ((m - 1) / 2) * float(complete["rawValue"]))
        / max(float(selected["rawValue"]), np.finfo(float).tiny)
        for m, complete, selected in zip(m_values, b_complete, b_selected, strict=True)
    ]
    check("Panel B prior comparator differs by exactly N", max(relation_errors, default=0.0) < 3.0e-15, {"maximumRelativeError": max(relation_errors, default=0.0)})

    independent_powers = {
        "latticeMOverKs": fit_power(m_values[-8:], [float(index[("A", "exact minimum-lattice factor M/Ks", float(m))]["rawValue"]) for m in m_values[-8:]]),
        "completeRootBoundedEta": fit_power(m_values[-8:], [float(index[("B", "complete-root BV envelope; eta=1", float(m))]["rawValue"]) for m in m_values[-8:]]),
        "selectedRootBoundedEta": fit_power(m_values[-8:], [float(index[("B", "prior selected-root envelope; N=(M-1)/2", float(m))]["rawValue"]) for m in m_values[-8:]]),
        "etaBounded": fit_power(m_values[-8:], [float(index[("C", "bounded eta=1", float(m))]["rawValue"]) for m in m_values[-8:]]),
        "etaMOneHalf": fit_power(m_values[-8:], [float(index[("C", "eta=M^(1/2)", float(m))]["rawValue"]) for m in m_values[-8:]]),
        "etaMSixSevenths": fit_power(m_values[-8:], [float(index[("C", "eta=M^(6/7)", float(m))]["rawValue"]) for m in m_values[-8:]]),
    }
    check(
        "independent fitted powers reproduce producer fits",
        all(close(value, float(results["derivedFigureFits"][key]["power"]), 2.0e-12) for key, value in independent_powers.items()),
        independent_powers,
    )
    power_requirements = (
        abs(independent_powers["latticeMOverKs"] + 2.0) < 2.0e-5
        and abs(independent_powers["completeRootBoundedEta"] + 2.0) < 2.0e-5
        and abs(independent_powers["selectedRootBoundedEta"] + 1.0) < 2.0e-5
        and abs(independent_powers["etaBounded"] + 2.0) < 2.0e-5
        and abs(independent_powers["etaMOneHalf"] + 5.0 / 6.0) < 3.0e-4
        and abs(independent_powers["etaMSixSevenths"]) < 2.0e-5
    )
    check("Panels A-C have the declared asymptotic powers", power_requirements, independent_powers)

    heat_coefficient = float(results["parameters"]["heatCoefficient"])
    retention_errors = []
    launch_errors = []
    for r_value in range(1, int(config["retentionMaximumR"]) + 1):
        fixed = float(index[("D", "fixed-window exact heat retention", float(r_value))]["rawValue"])
        launch = float(index[("D", "launch-inclusive retention", float(r_value))]["rawValue"])
        retention_errors.append(abs(-math.log(fixed) / r_value**2 - heat_coefficient))
        launch_errors.append(abs(launch - 1.0))
    check(
        "Panel D independently reconstructs fixed and launch-inclusive retention",
        max(retention_errors, default=0.0) < 2.0e-14 and max(launch_errors, default=0.0) == 0.0,
        {"maximumHeatCoefficientError": max(retention_errors, default=0.0), "maximumLaunchError": max(launch_errors, default=0.0)},
    )

    required_outputs = ["figure.pdf", "figure.svg", "figure.png", "qa-original.png", "qa-grayscale.png", "qa-pdf.png", "qa-report.md"]
    missing = [name for name in required_outputs if not (ROOT / name).is_file()]
    check("all formal outputs and QA assets exist", not missing, {"missing": missing})

    figure_config = config["figure"]
    expected_width = round(round(float(figure_config["widthMillimetres"]) / 25.4, 2) * int(figure_config["pngDpi"]))
    expected_height = round(round(float(figure_config["heightMillimetres"]) / 25.4, 2) * int(figure_config["pngDpi"]))
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_dpi = image.info.get("dpi", (0.0, 0.0))
    check(
        "archival PNG is 600 dpi at the declared print size",
        abs(png_size[0] - expected_width) <= 2 and abs(png_size[1] - expected_height) <= 2 and min(png_dpi) >= 599.0,
        {"pixels": list(png_size), "dpi": list(png_dpi), "expectedPixels": [expected_width, expected_height]},
    )

    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        raise FileNotFoundError("pdfinfo is required for independent PDF page validation")
    pdf_info_text = subprocess.run(
        [pdfinfo, str(ROOT / "figure.pdf")],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    pages_match = re.search(r"^Pages:\s+(\d+)$", pdf_info_text, re.MULTILINE)
    size_match = re.search(r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", pdf_info_text, re.MULTILINE)
    if pages_match is None or size_match is None:
        raise RuntimeError("pdfinfo did not report page count and physical size")
    page_count = int(pages_match.group(1))
    width_mm = float(size_match.group(1)) / 72.0 * 25.4
    height_mm = float(size_match.group(2)) / 72.0 * 25.4
    check(
        "PDF is one page at the declared physical size",
        page_count == 1
        and abs(width_mm - float(figure_config["widthMillimetres"])) < 0.15
        and abs(height_mm - float(figure_config["heightMillimetres"])) < 0.15,
        {"pageCount": page_count, "widthMillimetres": width_mm, "heightMillimetres": height_mm},
    )

    svg_text = (ROOT / "figure.svg").read_text(encoding="utf-8")
    declared_colors = ["#355c7d", "#b8792b", "#252422", "#77736c", "#d8d3c8", "#fbf9f4"]
    default_colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    check(
        "SVG uses the declared palette and no plotting-library defaults",
        all(color in svg_text.lower() for color in declared_colors[:5])
        and not any(color in svg_text.lower() for color in default_colors),
        {"declaredColorsFound": [color for color in declared_colors if color in svg_text.lower()]},
    )
    check(
        "SVG contains all panel labels and evidence boundaries",
        all(token in svg_text for token in ["A   Exact", "B   Complete", "C   Observation", "D   Fixed-window", "no DNS", "No universal endpoint"]),
        {"tokens": ["A", "B", "C", "D", "no DNS", "No universal endpoint"]},
    )

    qa_text = (ROOT / "qa-report.md").read_text(encoding="utf-8")
    pending = bool(re.search(r": PENDING", qa_text))
    check("manual final-size and grayscale QA is recorded as PASS", not pending and "inspection: PASS" in qa_text, {"pending": pending})

    passed = all(bool(item["passed"]) for item in checks)
    validation = {
        "release": config["release"],
        "figureId": config["figureId"],
        "status": "passed" if passed else "failed",
        "method": "independent binary64 reconstruction, source-hash verification, Poppler page inspection, raster metadata checks, SVG policy checks, and manual-QA record audit",
        "checkCount": len(checks),
        "checks": checks,
        "independentPowers": independent_powers,
        "wallSeconds": time.perf_counter() - started,
    }
    (ROOT / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    event_time = datetime.now(TIMEZONE).isoformat(timespec="milliseconds")
    with (ROOT / "progress.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps(
                {
                    "timestamp": event_time,
                    "stage": "validation-complete",
                    "status": validation["status"],
                    "checkCount": len(checks),
                    "elapsedSeconds": validation["wallSeconds"],
                },
                sort_keys=True,
            )
            + "\n"
        )
    usage = resource.getrusage(resource.RUSAGE_SELF)
    with (ROOT / "resource-log.ndjson").open("a", encoding="utf-8") as stream:
        stream.write(
            json.dumps(
                {
                    "timestamp": event_time,
                    "stage": "validation-complete",
                    "elapsedSeconds": validation["wallSeconds"],
                    "pid": os.getpid(),
                    "processUserCpuSeconds": usage.ru_utime,
                    "processSystemCpuSeconds": usage.ru_stime,
                    "maximumResidentSetRaw": usage.ru_maxrss,
                },
                sort_keys=True,
            )
            + "\n"
        )
    if not passed:
        failed = [item["name"] for item in checks if not item["passed"]]
        raise SystemExit(f"validation failed: {failed}")
    print(json.dumps({"status": "passed", "checks": len(checks), "independentPowers": independent_powers, "wallSeconds": validation["wallSeconds"]}, indent=2))


if __name__ == "__main__":
    main()
