#!/usr/bin/env python3
"""Independent Decimal and archival audit for the R0.71H formal figure."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import tempfile
from decimal import Decimal, getcontext
from pathlib import Path

from PIL import Image


getcontext().prec = 60
PDFINFO = Path(
    "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo"
)
PDFTOPPM = Path(
    "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdftoppm"
)


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def decimal_abs(value: Decimal) -> Decimal:
    return value.copy_abs()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--output", type=Path, default=Path("independent-validation.json")
    )
    args = parser.parse_args()

    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    for selected in grouped.values():
        selected.sort(key=lambda row: Decimal(row["x"]))

    checks: dict[str, bool] = {}
    require(len(rows) == 391, "independentRowCount", checks)
    maximum_decimal_formula_error = Decimal(0)
    maximum_sampling_error = Decimal(0)
    maximum_balance_error = Decimal(0)

    heat_names = (
        "rayleighPayment",
        "angularIntegral",
        "curvatureIntegral",
        "identitySum",
    )
    for index in range(61):
        expected_time = Decimal(index) / Decimal(40)
        values: dict[str, Decimal] = {}
        for name in heat_names:
            row = grouped[("A", name)][index]
            x = Decimal(row["x"])
            maximum_sampling_error = max(
                maximum_sampling_error, decimal_abs(x - expected_time)
            )
            z = (-Decimal(6) * x).exp()
            payment = Decimal("2.5") - (Decimal(1) + Decimal(4) * z) / (
                Decimal(1) + z
            )
            expected = {
                "rayleighPayment": payment,
                "angularIntegral": payment / Decimal(2),
                "curvatureIntegral": payment / Decimal(2),
                "identitySum": payment,
            }[name]
            values[name] = Decimal(row["value"])
            maximum_decimal_formula_error = max(
                maximum_decimal_formula_error,
                decimal_abs(values[name] - expected),
            )
        maximum_balance_error = max(
            maximum_balance_error,
            decimal_abs(values["identitySum"] - values["rayleighPayment"]),
            decimal_abs(
                values["identitySum"]
                - values["angularIntegral"]
                - values["curvatureIntegral"]
            ),
        )

    for index in range(9):
        frequency = Decimal(2) ** index
        angular_row = grouped[("B", "angularSpeed")][index]
        source_row = grouped[("B", "sourceDensity")][index]
        k = Decimal(angular_row["x"])
        require(k == frequency, f"panelBFrequency{index}", checks)
        amplitude = Decimal(1) / k
        angular_expected = amplitude * k * k / Decimal(2)
        source_expected = (
            amplitude
            * amplitude
            * (Decimal(3) + Decimal(2) * amplitude) ** 2
            * k
            * k
            / Decimal(4)
        )
        maximum_decimal_formula_error = max(
            maximum_decimal_formula_error,
            decimal_abs(Decimal(angular_row["value"]) - angular_expected),
            decimal_abs(Decimal(source_row["value"]) - source_expected),
        )

    for index in range(51):
        expected_delta = Decimal(index) / Decimal(50)
        rayleigh_row = grouped[("C", "rayleighQuotient")][index]
        source_row = grouped[("C", "projectiveSource")][index]
        delta = Decimal(rayleigh_row["x"])
        maximum_sampling_error = max(
            maximum_sampling_error, decimal_abs(delta - expected_delta)
        )
        square = delta * delta
        denominator = Decimal(3) * square + Decimal(4)
        rayleigh_expected = Decimal(2) * (
            Decimal(3) * square + Decimal(2)
        ) / denominator
        source_expected = Decimal(12) * square / (denominator * denominator)
        maximum_decimal_formula_error = max(
            maximum_decimal_formula_error,
            decimal_abs(Decimal(rayleigh_row["value"]) - rayleigh_expected),
            decimal_abs(Decimal(source_row["value"]) - source_expected),
        )

    for index in range(9):
        frequency = Decimal(2) ** index
        known_row = grouped[("D", "knownHeatWeight")][index]
        required_row = grouped[("D", "directRequiredWeight")][index]
        ratio_row = grouped[("D", "gapRatio")][index]
        k = Decimal(known_row["x"])
        require(k == frequency, f"panelDFrequency{index}", checks)
        known = Decimal(1) / (k * k)
        required = Decimal(1)
        ratio = k * k
        maximum_decimal_formula_error = max(
            maximum_decimal_formula_error,
            decimal_abs(Decimal(known_row["value"]) - known),
            decimal_abs(Decimal(required_row["value"]) - required),
            decimal_abs(Decimal(ratio_row["value"]) - ratio),
        )
        maximum_balance_error = max(
            maximum_balance_error,
            decimal_abs(
                Decimal(required_row["value"])
                / Decimal(known_row["value"])
                - Decimal(ratio_row["value"])
            ),
        )

    require(maximum_sampling_error <= Decimal("1e-16"), "decimalSamplingGrid", checks)
    require(maximum_decimal_formula_error < Decimal("3e-15"), "decimalFormulaAgreement", checks)
    require(maximum_balance_error < Decimal("2e-13"), "independentExactBalances", checks)

    pdf = Path("figure.pdf").read_bytes()
    svg = Path("figure.svg").read_text(encoding="utf-8")
    require(pdf.startswith(b"%PDF"), "pdfHeader", checks)
    require("<svg" in svg, "svgRoot", checks)
    require(len(pdf) > 20_000, "pdfMinimumSize", checks)
    require(len(svg) > 50_000, "svgMinimumSize", checks)

    with Image.open("figure.png") as image:
        png_pixels = image.size
        require(abs(image.size[0] - 4205) <= 1, "pngWidth600dpi", checks)
        require(abs(image.size[1] - 2551) <= 1, "pngHeight600dpi", checks)
    with Image.open("qa-original.png") as image:
        require(image.size == (1780, 1080), "qaOriginalPixels", checks)
    with Image.open("qa-grayscale.png") as image:
        require(image.size == (1780, 1080), "qaGrayscalePixels", checks)

    pdf_info = subprocess.run(
        [str(PDFINFO), "figure.pdf"], check=True, capture_output=True, text=True
    ).stdout
    require("Pages:           1" in pdf_info, "onePagePdf", checks)
    match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", pdf_info)
    require(match is not None, "pdfPageSizePresent", checks)
    width_mm = float(match.group(1)) * 25.4 / 72.0
    height_mm = float(match.group(2)) * 25.4 / 72.0
    require(abs(width_mm - 178.0) < 0.02, "pdfWidth178mm", checks)
    require(abs(height_mm - 108.0) < 0.02, "pdfHeight108mm", checks)

    with tempfile.TemporaryDirectory(prefix="r071h-pdf-qa-") as temporary:
        stem = Path(temporary) / "render"
        subprocess.run(
            [str(PDFTOPPM), "-singlefile", "-png", "-r", "180", "figure.pdf", str(stem)],
            check=True,
            capture_output=True,
        )
        with Image.open(stem.with_suffix(".png")) as image:
            pdf_raster_pixels = image.size
            require(image.size[0] > 1200 and image.size[1] > 700, "pdfRasterized", checks)

    payload = {
        "release": "R0.71H-independent-figure",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "maximumDecimalFormulaError": str(maximum_decimal_formula_error),
            "maximumSamplingGridError": str(maximum_sampling_error),
            "maximumExactBalanceError": str(maximum_balance_error),
            "pdfWidthMillimetres": width_mm,
            "pdfHeightMillimetres": height_mm,
            "pngPixels": list(png_pixels),
            "pdfRasterPixelsAt180Dpi": list(pdf_raster_pixels),
        },
        "claimBoundary": (
            "Independent Decimal recomputation and file-format validation only; no DNS, "
            "general NSE estimate, regularity theorem, singularity claim, or originality claim."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
