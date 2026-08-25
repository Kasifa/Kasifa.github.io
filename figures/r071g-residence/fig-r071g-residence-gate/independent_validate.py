#!/usr/bin/env python3
"""Compare the figure data with the independent adaptive audit and file QA."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from pathlib import Path

from PIL import Image


PDFINFO = Path(
    "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo"
)


def require(condition: bool, label: str, checks: dict[str, bool]):
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path("../../../research/certificates/r071g/independent-result.json"),
    )
    parser.add_argument(
        "--output", type=Path, default=Path("independent-validation.json")
    )
    args = parser.parse_args()
    certificate = json.loads(args.certificate.read_text(encoding="utf-8"))
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    figure_sign = {
        float(row["mu"]): float(row["theta"])
        for row in rows
        if row["recordType"] == "signExit"
    }
    figure_q = {
        (float(row["mu"]), float(row["level"])): float(row["theta"])
        for row in rows
        if row["recordType"] == "qExit"
    }

    checks: dict[str, bool] = {}
    require(certificate["version"] == "R0.71G-independent", "certificateVersion", checks)
    require(certificate["status"] == "pass", "certificatePass", checks)
    require(all(certificate["checks"].values()), "certificateChecks", checks)
    maximum_sign_difference = 0.0
    maximum_q_difference = 0.0
    maximum_radius_difference = 0.0
    for case in certificate["chainCases"]:
        mu = float(case["mu"])
        adaptive = case["radius18"]
        maximum_sign_difference = max(
            maximum_sign_difference,
            abs(figure_sign[mu] - float(adaptive["firstSignExit"])),
        )
        for level in (0.5, 0.1, 0.01):
            maximum_q_difference = max(
                maximum_q_difference,
                abs(
                    figure_q[(mu, level)]
                    - float(adaptive["relativeQExit"][str(level)])
                ),
            )
        maximum_radius_difference = max(
            maximum_radius_difference, float(case["maximumEventDifference"])
        )
    require(maximum_sign_difference < 5.0e-8, "fixedVsAdaptiveSign", checks)
    require(maximum_q_difference < 1.5e-7, "fixedVsAdaptiveRelative", checks)
    require(maximum_radius_difference < 4.0e-14, "adaptiveRadiusAgreement", checks)

    pdf = Path("figure.pdf").read_bytes()
    svg = Path("figure.svg").read_text(encoding="utf-8")
    require(pdf.startswith(b"%PDF"), "pdfHeader", checks)
    require("<svg" in svg, "svgRoot", checks)
    require(len(pdf) > 20_000, "pdfSize", checks)
    require(len(svg) > 50_000, "svgSize", checks)

    with Image.open("figure.png") as image:
        require(image.size == (4204, 2551), "pngPixels", checks)
    with Image.open("qa-original.png") as image:
        require(image.size == (1780, 1080), "qaOriginalPixels", checks)
    with Image.open("qa-grayscale.png") as image:
        require(image.size == (1780, 1080), "qaGrayscalePixels", checks)

    pdf_info = subprocess.run(
        [str(PDFINFO), "figure.pdf"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    require("Pages:           1" in pdf_info, "onePagePdf", checks)
    match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", pdf_info)
    require(match is not None, "pdfPageSizePresent", checks)
    width_mm = float(match.group(1)) * 25.4 / 72.0
    height_mm = float(match.group(2)) * 25.4 / 72.0
    require(abs(width_mm - 178.0) < 0.02, "pdfWidth", checks)
    require(abs(height_mm - 108.0) < 0.02, "pdfHeight", checks)

    payload = {
        "release": "R0.71G-independent-figure",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "maximumFixedVsAdaptiveSignDifference": maximum_sign_difference,
            "maximumFixedVsAdaptiveRelativeDifference": maximum_q_difference,
            "maximumAdaptiveRadiusEventDifference": maximum_radius_difference,
            "pdfWidthMillimetres": width_mm,
            "pdfHeightMillimetres": height_mm,
        },
        "claimBoundary": (
            "Compares two finite numerical methods and validates archival formats. It does not prove the analytic arbitrary-duration theorem or a general occupation bound."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
