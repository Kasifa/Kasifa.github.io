#!/usr/bin/env python3
"""Independently validate the R0.72A-1 figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import time
from zoneinfo import ZoneInfo

from PIL import Image
from scipy.special import j0, jn_zeros


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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

    def check(name: str, passed: bool, value: object, requirement: str) -> None:
        checks.append(
            {
                "name": name,
                "passed": bool(passed),
                "value": value,
                "requirement": requirement,
            }
        )

    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = json.loads(producer_path.read_text(encoding="utf-8"))
    independent = json.loads(independent_path.read_text(encoding="utf-8"))
    check(
        "source_certificates_pass",
        bool(producer["allPassed"]) and bool(independent["allPassed"]),
        {"producer": producer["allPassed"], "independent": independent["allPassed"]},
        "both source certificates remain fully passed",
    )

    recorded_sources = {record["path"]: record["sha256"] for record in metadata["sourceFiles"]}
    source_hashes = {
        str(path.relative_to(REPOSITORY)): sha256(path)
        for path in (producer_path, independent_path)
    }
    check(
        "source_hashes",
        source_hashes == recorded_sources,
        source_hashes,
        "source certificate hashes match figure metadata exactly",
    )
    data_hashes = {name: sha256(ROOT / name) for name in ("data.csv", "data.json", "results.json")}
    check(
        "data_hashes",
        data_hashes == metadata["dataFiles"],
        data_hashes,
        "data and result hashes match metadata exactly",
    )
    check(
        "row_count",
        len(rows) == int(metadata["rowCount"]) == int(results["rowCount"]) == 402,
        len(rows),
        "all 402 declared figure rows are present",
    )

    a_rows = [row for row in rows if row["panel"] == "A"]
    a_errors = []
    for row in a_rows:
        beta = float(row["x"])
        if row["series"] == "certified boundary":
            expected = min(1.5, (6.0 + 3.0 * beta) / 7.0)
        elif row["series"] == "local exposure constraint":
            expected = (6.0 + 3.0 * beta) / 7.0
        else:
            expected = 1.5
        a_errors.append(abs(float(row["y"]) - expected))
    check(
        "phase_formula",
        max(a_errors, default=0.0) < 2.0e-15,
        max(a_errors, default=0.0),
        "Panel A independently reconstructs every exponent row",
    )

    bessel_rows = {
        int(float(row["x"])): float(row["y"])
        for row in rows
        if row["panel"] == "B" and row["series"] == "frozen Bessel sum"
    }
    bessel_errors = []
    for r_value, plotted in bessel_rows.items():
        expected = float(4.0 * sum(float(j0(value)) ** 2 for value in jn_zeros(1, r_value)))
        bessel_errors.append(abs(plotted - expected))
    check(
        "bessel_formula",
        max(bessel_errors, default=0.0) < 2.0e-14,
        max(bessel_errors, default=0.0),
        "Panel B independently reconstructs all Bessel sums",
    )

    cross = results["crossAudit"]
    check(
        "cross_audit_mass",
        max(float(row["massDifference"]) for row in cross) < 4.0e-10,
        max(float(row["massDifference"]) for row in cross),
        "producer and independent masses agree below 4e-10",
    )
    check(
        "cross_audit_roots",
        max(float(row["maximumRootDifference"]) for row in cross) < 4.0e-9,
        max(float(row["maximumRootDifference"]) for row in cross),
        "producer and independent roots agree below 4e-9",
    )
    check(
        "log_coefficient",
        abs(float(results["bessel"]["leadingCoefficient"]) - 8.0 / math.pi**2) < 2.0e-16,
        results["bessel"]["leadingCoefficient"],
        "leading coefficient is exactly reconstructed as 8/pi^2",
    )

    producer_by_r = {int(row["R"]): row for row in producer["finiteLattice"]}
    c_displacement_errors = []
    for row in rows:
        if row["panel"] == "C" and row["series"] == "maximum root displacement":
            r_value = int(float(row["x"]))
            source = producer_by_r[r_value]
            expected = float(source["maximumRootShift"]) / float(source["delta"])
            c_displacement_errors.append(abs(float(row["y"]) - expected))
    check(
        "physical_root_displacement",
        len(c_displacement_errors) == len(producer_by_r)
        and max(c_displacement_errors, default=1.0) < 2.0e-22,
        max(c_displacement_errors, default=None),
        "Panel C converts rescaled tau root shifts to physical x displacement",
    )

    required = [
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "qa-original.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "qa-report.md",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    check("formal_outputs", not missing, missing, "all formal and QA outputs exist")

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
        png_size = image.size
        png_dpi = image.info.get("dpi", (0.0, 0.0))
    check(
        "png_dimensions",
        abs(png_size[0] - expected_width) <= 2
        and abs(png_size[1] - expected_height) <= 2
        and min(png_dpi) >= 599.0,
        {"pixels": png_size, "dpi": png_dpi, "expected": [expected_width, expected_height]},
        "archival PNG is 600 dpi at the declared print dimensions",
    )

    pdfinfo = shutil.which("pdfinfo")
    if pdfinfo is None:
        raise FileNotFoundError("pdfinfo is required")
    info = subprocess.run(
        [pdfinfo, str(ROOT / "figure.pdf")], check=True, capture_output=True, text=True
    ).stdout
    pages = re.search(r"^Pages:\s+(\d+)$", info, re.MULTILINE)
    size = re.search(r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", info, re.MULTILINE)
    if pages is None or size is None:
        raise RuntimeError("pdfinfo did not return page geometry")
    width_mm = float(size.group(1)) / 72.0 * 25.4
    height_mm = float(size.group(2)) / 72.0 * 25.4
    check(
        "pdf_geometry",
        int(pages.group(1)) == 1
        and abs(width_mm - float(figure_config["widthMillimetres"])) < 0.18
        and abs(height_mm - float(figure_config["heightMillimetres"])) < 0.18,
        {"pages": int(pages.group(1)), "widthMm": width_mm, "heightMm": height_mm},
        "PDF is one page at the declared physical dimensions",
    )

    svg = (ROOT / "figure.svg").read_text(encoding="utf-8").lower()
    palette = config["palette"]
    default_colors = ("#1f77b4", "#ff7f0e", "#2ca02c", "#d62728")
    check(
        "svg_palette",
        all(value.lower() in svg for value in palette.values())
        and not any(value in svg for value in default_colors),
        {key: value.lower() in svg for key, value in palette.items()},
        "SVG contains the declared palette and no Matplotlib defaults",
    )
    tokens = (
        "a   power-law certificate",
        "b   exact-root mass",
        "c   shrinking scales",
        "physical $x$ length",
        "no dns",
        "do not establish nonlinear normalized divergence",
    )
    check(
        "svg_labels",
        all(token in svg for token in tokens),
        {token: token in svg for token in tokens},
        "SVG contains panel labels and the evidence boundary",
    )

    qa_report = (ROOT / "qa-report.md").read_text(encoding="utf-8")
    check(
        "manual_qa",
        "PENDING" not in qa_report and qa_report.count("PASS") >= 5,
        {"pending": "PENDING" in qa_report, "passCount": qa_report.count("PASS")},
        "manual color, grayscale, PDF, clipping, and claim-boundary QA are all PASS",
    )

    passed = all(bool(row["passed"]) for row in checks)
    payload = {
        "schemaVersion": "r072a-figure-validation-v1",
        "generatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "status": "passed" if passed else "failed",
        "checkCount": len(checks),
        "checks": checks,
        "elapsedSeconds": time.perf_counter() - started,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if not passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise SystemExit(f"validation failed: {failed}")
    print(json.dumps({"status": "passed", "checks": len(checks)}, indent=2))


if __name__ == "__main__":
    main()
