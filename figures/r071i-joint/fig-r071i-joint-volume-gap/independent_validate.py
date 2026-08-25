#!/usr/bin/env python3
"""Independent Decimal and archival audit for the R0.71I formal figure."""

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


getcontext().prec = 70
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


def nse_profiles(theta: Decimal) -> tuple[Decimal, Decimal]:
    one = Decimal(1)
    two = Decimal(2)
    x = (-Decimal(10) * theta).exp()
    q_scaled = Decimal(4) * x * (one - x) ** 2 / (one + x)
    y_scaled = (
        two * (-two * theta).exp()
        + two * (-Decimal(8) * theta).exp()
        + two * (-Decimal(18) * theta).exp()
        + Decimal(4) / Decimal(5) * (-Decimal(10) * theta).exp()
        + two / Decimal(5) * (-Decimal(20) * theta).exp()
    )
    f_scaled = Decimal(4) * (
        (-Decimal(10) * theta).exp() + (-Decimal(20) * theta).exp()
    )
    return q_scaled / y_scaled, f_scaled / y_scaled


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
    require(len(rows) == 567, "independentRowCount", checks)
    require(
        set(grouped)
        == {
            ("A", "commonHeatPulse"),
            ("A", "pulsePeak"),
            ("B", "traceVolumeRatio"),
            ("C", "A0"),
            ("C", "G0"),
            ("C", "positiveTestPoint"),
            ("D", "aggregateCoefficient"),
            ("D", "refreshEndpoint"),
        },
        "independentSeriesSet",
        checks,
    )
    maximum_decimal_formula_error = Decimal(0)
    maximum_ratio_relative_error = Decimal(0)
    maximum_sampling_error = Decimal(0)
    maximum_exact_balance_error = Decimal(0)

    pulse_values: list[Decimal] = []
    for index, row in enumerate(grouped[("A", "commonHeatPulse")]):
        expected_tau = Decimal(3) * Decimal(index) / Decimal(150)
        tau = Decimal(row["x"])
        x = (-Decimal(2) * tau).exp()
        expected = x * (Decimal(1) - x) ** 2 / (
            Decimal(2) * (Decimal(1) + x)
        )
        value = Decimal(row["value"])
        maximum_sampling_error = max(
            maximum_sampling_error, decimal_abs(tau - expected_tau)
        )
        maximum_decimal_formula_error = max(
            maximum_decimal_formula_error, decimal_abs(value - expected)
        )
        pulse_values.append(value)
    require(pulse_values[0] == 0, "independentCommonHeatEntryZero", checks)

    sqrt17 = Decimal(17).sqrt()
    x_star = (sqrt17 - Decimal(3)) / Decimal(4)
    tau_star = -x_star.ln() / Decimal(2)
    q_star = (Decimal(71) - Decimal(17) * sqrt17) / Decimal(16)
    peak_row = grouped[("A", "pulsePeak")][0]
    maximum_decimal_formula_error = max(
        maximum_decimal_formula_error,
        decimal_abs(Decimal(peak_row["x"]) - tau_star),
        decimal_abs(Decimal(peak_row["value"]) - q_star),
    )
    require(q_star > max(pulse_values), "independentExactPulsePeak", checks)
    require(
        decimal_abs(Decimal(2) * q_star - (Decimal(71) - Decimal(17) * sqrt17) / Decimal(8))
        < Decimal("1e-65"),
        "independentPulseTVIdentity",
        checks,
    )

    ratio_constant = (Decimal(71) - Decimal(17) * sqrt17) / Decimal(3)
    for index, row in enumerate(grouped[("B", "traceVolumeRatio")]):
        expected_frequency = Decimal(2) ** index
        frequency = Decimal(row["x"])
        expected = ratio_constant * frequency * frequency
        value = Decimal(row["value"])
        maximum_sampling_error = max(
            maximum_sampling_error, decimal_abs(frequency - expected_frequency)
        )
        maximum_decimal_formula_error = max(
            maximum_decimal_formula_error, decimal_abs(value - expected)
        )
        maximum_ratio_relative_error = max(
            maximum_ratio_relative_error,
            decimal_abs(value - expected) / expected,
        )
        maximum_exact_balance_error = max(
            maximum_exact_balance_error,
            decimal_abs(value / (frequency * frequency) - ratio_constant),
        )

    a_values: list[Decimal] = []
    g_values: list[Decimal] = []
    for index in range(151):
        expected_theta = Decimal(3) * Decimal(index) / Decimal(750)
        a_row = grouped[("C", "A0")][index]
        g_row = grouped[("C", "G0")][index]
        theta = Decimal(a_row["x"])
        g_theta = Decimal(g_row["x"])
        expected_a, expected_g = nse_profiles(theta)
        a_value = Decimal(a_row["value"])
        g_value = Decimal(g_row["value"])
        maximum_sampling_error = max(
            maximum_sampling_error,
            decimal_abs(theta - expected_theta),
            decimal_abs(g_theta - expected_theta),
        )
        maximum_decimal_formula_error = max(
            maximum_decimal_formula_error,
            decimal_abs(a_value - expected_a),
            decimal_abs(g_value - expected_g),
        )
        a_values.append(a_value)
        g_values.append(g_value)
    require(a_values[0] == 0, "independentNseEntryZero", checks)
    require(max(a_values) > Decimal("0.18"), "independentNsePulsePositive", checks)
    require(
        decimal_abs(g_values[0] - Decimal(10) / Decimal(9)) < Decimal("2e-16"),
        "independentNseInitialG0",
        checks,
    )
    require(
        all(left > right for left, right in zip(g_values, g_values[1:])),
        "independentNseG0Decreases",
        checks,
    )

    test_row = grouped[("C", "positiveTestPoint")][0]
    theta_test = Decimal(2).ln() / Decimal(10)
    expected_test, _ = nse_profiles(theta_test)
    maximum_decimal_formula_error = max(
        maximum_decimal_formula_error,
        decimal_abs(Decimal(test_row["x"]) - theta_test),
        decimal_abs(Decimal(test_row["value"]) - expected_test),
    )
    require(expected_test > 0, "independentNseExactTestPositive", checks)

    aggregate_values: list[Decimal] = []
    for index, row in enumerate(grouped[("D", "aggregateCoefficient")]):
        expected_delta = Decimal(index) / Decimal(100)
        delta = Decimal(row["x"])
        expected = Decimal(1) / (Decimal(3) * delta * delta + Decimal(4))
        value = Decimal(row["value"])
        maximum_sampling_error = max(
            maximum_sampling_error, decimal_abs(delta - expected_delta)
        )
        maximum_decimal_formula_error = max(
            maximum_decimal_formula_error, decimal_abs(value - expected)
        )
        aggregate_values.append(value)
    require(
        all(left > right for left, right in zip(aggregate_values, aggregate_values[1:])),
        "independentRefreshCurveDecreases",
        checks,
    )
    endpoints = grouped[("D", "refreshEndpoint")]
    left_endpoint = Decimal(endpoints[0]["value"])
    right_endpoint = Decimal(endpoints[1]["value"])
    maximum_decimal_formula_error = max(
        maximum_decimal_formula_error,
        decimal_abs(left_endpoint - Decimal(1) / Decimal(4)),
        decimal_abs(right_endpoint - Decimal(1) / Decimal(7)),
    )
    maximum_exact_balance_error = max(
        maximum_exact_balance_error,
        decimal_abs(left_endpoint - right_endpoint - Decimal(3) / Decimal(28)),
    )

    require(maximum_sampling_error <= Decimal("2e-16"), "decimalSamplingGrid", checks)
    require(
        maximum_decimal_formula_error < Decimal("2e-12"),
        "decimalFormulaAgreement",
        checks,
    )
    require(
        maximum_ratio_relative_error < Decimal("2e-16"),
        "decimalRatioRelativeAgreement",
        checks,
    )
    require(
        maximum_exact_balance_error < Decimal("3e-15"),
        "independentExactBalances",
        checks,
    )

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

    with tempfile.TemporaryDirectory(prefix="r071i-pdf-qa-") as temporary:
        stem = Path(temporary) / "render"
        subprocess.run(
            [str(PDFTOPPM), "-singlefile", "-png", "-r", "180", "figure.pdf", str(stem)],
            check=True,
            capture_output=True,
        )
        with Image.open(stem.with_suffix(".png")) as image:
            pdf_raster_pixels = image.size
            require(
                image.size[0] > 1200 and image.size[1] > 700,
                "pdfRasterized",
                checks,
            )

    payload = {
        "release": "R0.71I-independent-figure",
        "status": "pass",
        "checks": checks,
        "metrics": {
            "maximumDecimalFormulaError": str(maximum_decimal_formula_error),
            "maximumRatioRelativeError": str(maximum_ratio_relative_error),
            "maximumSamplingGridError": str(maximum_sampling_error),
            "maximumExactBalanceError": str(maximum_exact_balance_error),
            "commonHeatExactPeak": str(q_star),
            "commonHeatRatioConstantNu1": str(ratio_constant),
            "nseMaximumA0OnGrid": str(max(a_values)),
            "nseInitialG0": str(g_values[0]),
            "refreshGap": str(left_endpoint - right_endpoint),
            "pdfWidthMillimetres": width_mm,
            "pdfHeightMillimetres": height_mm,
            "pngPixels": list(png_pixels),
            "pdfRasterPixelsAt180Dpi": list(pdf_raster_pixels),
        },
        "claimBoundary": (
            "Independent Decimal recomputation and file-format validation only. "
            "Panels A-B are abstract common heat; panel C is a fixed-window "
            "K-to-infinity profile of a global-smooth 2D3C NSE family for one "
            "smooth radial two-ring multiplier. This is not a full face-paid BV "
            "no-go, a broad-frame theorem, DNS, or a regularity conclusion."
        ),
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
