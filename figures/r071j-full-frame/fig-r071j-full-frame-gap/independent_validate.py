#!/usr/bin/env python3
"""Independent Decimal and archival audit for the R0.71J figure.

The arithmetic path uses only the Python standard library and does not import
the producer, NumPy, Matplotlib, SymPy, or Pillow.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import struct
import subprocess
import tempfile
from decimal import Decimal, getcontext
from pathlib import Path


getcontext().prec = 80
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


def absolute(value: Decimal) -> Decimal:
    return value.copy_abs()


def exponential(power: int, theta: Decimal) -> Decimal:
    return (-Decimal(power) * theta).exp()


def profiles(theta: Decimal) -> tuple[Decimal, Decimal, Decimal, Decimal, Decimal, Decimal]:
    b_zero = Decimal(4) * (exponential(34, theta) - exponential(52, theta))
    d_zero = (
        Decimal(32) * exponential(32, theta)
        + Decimal(1156) * exponential(34, theta)
        + Decimal(50) * exponential(50, theta)
        + Decimal(2704) * exponential(52, theta)
    )
    y_zero = (
        Decimal(2) * exponential(2, theta)
        + Decimal(2) * exponential(32, theta)
        + Decimal(68) * exponential(34, theta)
        + Decimal(2) * exponential(50, theta)
        + Decimal(104) * exponential(52, theta)
    )
    f_zero_square = (
        Decimal(4) * exponential(34, theta)
        + Decimal(192) * exponential(36, theta)
        + Decimal(4) * exponential(52, theta)
        + Decimal(300) * exponential(54, theta)
    )
    if b_zero == 0:
        return b_zero, d_zero, y_zero, f_zero_square, Decimal(0), Decimal(0)
    b_prime = Decimal(4) * (
        -Decimal(34) * exponential(34, theta)
        + Decimal(52) * exponential(52, theta)
    )
    d_prime = -(
        Decimal(32 * 32) * exponential(32, theta)
        + Decimal(34 * 1156) * exponential(34, theta)
        + Decimal(50 * 50) * exponential(50, theta)
        + Decimal(52 * 2704) * exponential(52, theta)
    )
    y_prime = -(
        Decimal(2 * 2) * exponential(2, theta)
        + Decimal(32 * 2) * exponential(32, theta)
        + Decimal(34 * 68) * exponential(34, theta)
        + Decimal(50 * 2) * exponential(50, theta)
        + Decimal(52 * 104) * exponential(52, theta)
    )
    a_zero = b_zero * b_zero / (d_zero * y_zero)
    a_prime = a_zero * (
        Decimal(2) * b_prime / b_zero - d_prime / d_zero - y_prime / y_zero
    )
    return b_zero, d_zero, y_zero, f_zero_square, a_zero, a_prime


def a_star_exact() -> Decimal:
    logarithm_two = Decimal(2).ln()
    root_one = (logarithm_two / Decimal(9)).exp()
    root_seven = (Decimal(7) * logarithm_two / Decimal(9)).exp()
    return Decimal(4) / (
        Decimal(57)
        * (root_one + Decimal(44))
        * (Decimal(3) * root_one + Decimal(4) * root_seven + Decimal(120))
    )


def png_info(path: Path) -> tuple[int, int, tuple[int, int] | None]:
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise AssertionError(f"not PNG: {path}")
    width, height = struct.unpack(">II", payload[16:24])
    offset = 8
    density: tuple[int, int] | None = None
    while offset + 12 <= len(payload):
        length = struct.unpack(">I", payload[offset : offset + 4])[0]
        kind = payload[offset + 4 : offset + 8]
        data = payload[offset + 8 : offset + 8 + length]
        if kind == b"pHYs" and length == 9 and data[8] == 1:
            density = struct.unpack(">II", data[:8])
        offset += 12 + length
        if kind == b"IEND":
            break
    return width, height, density


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output", type=Path, default=Path("independent-validation.json"))
    args = parser.parse_args()
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    for selected in grouped.values():
        selected.sort(key=lambda row: (Decimal(row["x"]), row["category"]))

    checks: dict[str, bool] = {}
    expected_series = {
        ("A", "positiveCreation"),
        ("A", "timeDerivative"),
        ("A", "viscousMass"),
        ("A", "negativeDefect"),
        ("B", "Bnormalized"),
        ("B", "Dnormalized"),
        ("B", "Ynormalized"),
        ("B", "anormalized"),
        ("C", "Zlower"),
        ("C", "Hupper"),
        ("C", "ratioOverK2"),
        ("D", "Bgroup"),
        ("D", "F2group"),
        ("D", "dgroup"),
        ("D", "frameRadius"),
    }
    require(len(rows) == 856, "independentRowCount", checks)
    require(set(grouped) == expected_series, "independentSeriesSet", checks)
    maximum_formula_error = Decimal(0)
    maximum_relative_error = Decimal(0)
    maximum_sampling_error = Decimal(0)
    maximum_balance_error = Decimal(0)

    theta_star = Decimal(2).ln() / Decimal(18)
    b_star, _, _, _, a_profile_star, a_prime_star = profiles(theta_star)
    a_star = a_star_exact()
    maximum_balance_error = max(maximum_balance_error, absolute(a_profile_star - a_star))
    source_star = (a_prime_star + Decimal(32) * a_profile_star) / Decimal(2)
    expected_a = {
        "positiveCreation": Decimal(2) * max(source_star, Decimal(0)),
        "timeDerivative": a_prime_star,
        "viscousMass": Decimal(32) * a_profile_star,
        "negativeDefect": Decimal(2) * max(-source_star, Decimal(0)),
    }
    for series, expected in expected_a.items():
        row = grouped[("A", series)][0]
        value = Decimal(row["value"])
        maximum_sampling_error = max(maximum_sampling_error, absolute(Decimal(row["x"]) - theta_star))
        maximum_formula_error = max(maximum_formula_error, absolute(value - expected))
        if expected != 0:
            maximum_relative_error = max(maximum_relative_error, absolute(value - expected) / absolute(expected))
    lhs = Decimal(grouped[("A", "positiveCreation")][0]["value"])
    rhs = sum(
        (Decimal(grouped[("A", series)][0]["value"]) for series in ("timeDerivative", "viscousMass", "negativeDefect")),
        Decimal(0),
    )
    maximum_balance_error = max(maximum_balance_error, absolute(lhs - rhs))
    require(source_star > 0, "independentPositiveSource", checks)
    require(Decimal(grouped[("A", "negativeDefect")][0]["value"]) == 0, "independentZeroNegativeDefect", checks)

    for index in range(201):
        theta_expected = Decimal(index) / Decimal(500)
        b_zero, d_zero, y_zero, _, a_zero, _ = profiles(theta_expected)
        expected_b = {
            "Bnormalized": b_zero / b_star,
            "Dnormalized": d_zero / Decimal(3942),
            "Ynormalized": y_zero / Decimal(178),
            "anormalized": a_zero / a_star,
        }
        for series, expected in expected_b.items():
            row = grouped[("B", series)][index]
            theta = Decimal(row["x"])
            value = Decimal(row["value"])
            maximum_sampling_error = max(maximum_sampling_error, absolute(theta - theta_expected))
            error = absolute(value - expected)
            maximum_formula_error = max(maximum_formula_error, error)
            if expected != 0:
                maximum_relative_error = max(maximum_relative_error, error / absolute(expected))
    require(Decimal(grouped[("B", "Bnormalized")][0]["value"]) == 0, "independentBEntryZero", checks)
    require(Decimal(grouped[("B", "anormalized")][0]["value"]) == 0, "independentaEntryZero", checks)
    require(max(Decimal(row["value"]) for row in grouped[("B", "anormalized")]) > 4, "independentInteriorPulse", checks)

    logarithm_two = Decimal(2).ln()
    gap = Decimal(1) - (-logarithm_two / Decimal(9)).exp()
    ratio_constant = a_star / (Decimal(32) * gap)
    normalized_ratio_values: list[Decimal] = []
    for index, exponent in enumerate(range(3, 14)):
        frequency = Decimal(2) ** exponent
        expected_c = {
            "Zlower": a_star / (Decimal(64) * frequency**2),
            "Hupper": gap / (Decimal(2) * frequency**4),
            "ratioOverK2": ratio_constant,
        }
        for series, expected in expected_c.items():
            row = grouped[("C", series)][index]
            value = Decimal(row["value"])
            maximum_sampling_error = max(maximum_sampling_error, absolute(Decimal(row["x"]) - frequency))
            error = absolute(value - expected)
            maximum_formula_error = max(maximum_formula_error, error)
            maximum_relative_error = max(maximum_relative_error, error / absolute(expected))
        z_value = Decimal(grouped[("C", "Zlower")][index]["value"])
        h_value = Decimal(grouped[("C", "Hupper")][index]["value"])
        normalized_ratio_values.append(z_value / h_value / frequency**2)
    maximum_balance_error = max(
        maximum_balance_error,
        max(normalized_ratio_values) - min(normalized_ratio_values),
        max(absolute(value - ratio_constant) for value in normalized_ratio_values),
    )

    expected_ledger = {
        "Bgroup": [Decimal(36), Decimal(-36), Decimal(0)],
        "F2group": [Decimal(328), Decimal(8), Decimal(164)],
        "dgroup": [Decimal(82), Decimal(3860), Decimal(0)],
    }
    for series, expected in expected_ledger.items():
        actual = [Decimal(row["value"]) for row in grouped[("D", series)]]
        require(actual == expected, f"independentLedger_{series}", checks)
    require(sum(expected_ledger["Bgroup"], Decimal(0)) == 0, "independentInitialBCancellation", checks)
    require(sum(expected_ledger["F2group"], Decimal(0)) == 500, "independentInitialF2Total", checks)
    require(sum(expected_ledger["dgroup"], Decimal(0)) == 3942, "independentInitialDTotal", checks)
    radii: list[Decimal] = []
    for row in grouped[("D", "frameRadius")]:
        group = int(Decimal(row["x"]))
        channel = int(row["category"].split("=")[1])
        expected = Decimal(group * group + channel * channel).sqrt() / Decimal(4)
        value = Decimal(row["value"])
        radii.append(value)
        maximum_formula_error = max(maximum_formula_error, absolute(value - expected))
    require(min(radii) >= 1, "independentFlatTopLower", checks)
    require(max(radii) <= Decimal(2).sqrt(), "independentFlatTopUpper", checks)

    require(maximum_sampling_error <= Decimal("2e-16"), "decimalSamplingGrid", checks)
    require(maximum_formula_error < Decimal("3e-15"), "decimalFormulaAgreement", checks)
    require(maximum_relative_error < Decimal("5e-15"), "decimalRelativeAgreement", checks)
    require(maximum_balance_error < Decimal("3e-18"), "independentExactBalances", checks)

    pdf = Path("figure.pdf").read_bytes()
    svg = Path("figure.svg").read_text(encoding="utf-8")
    require(pdf.startswith(b"%PDF"), "pdfHeader", checks)
    require("<svg" in svg, "svgRoot", checks)
    require(len(pdf) > 20_000, "pdfMinimumSize", checks)
    require(len(svg) > 50_000, "svgMinimumSize", checks)
    png_width, png_height, png_density = png_info(Path("figure.png"))
    require(abs(png_width - 4205) <= 1, "pngWidth600dpi", checks)
    require(abs(png_height - 2646) <= 1, "pngHeight600dpi", checks)
    require(png_density is not None and 23000 <= png_density[0] <= 24000, "pngDensity600dpi", checks)
    qa_width, qa_height, _ = png_info(Path("qa-original.png"))
    gray_width, gray_height, _ = png_info(Path("qa-grayscale.png"))
    require((qa_width, qa_height) == (1780, 1120), "qaOriginalPixels", checks)
    require((gray_width, gray_height) == (1780, 1120), "qaGrayscalePixels", checks)

    require(PDFINFO.is_file(), "pdfInfoAvailable", checks)
    require(PDFTOPPM.is_file(), "pdfRasterizerAvailable", checks)
    pdf_info = subprocess.run([str(PDFINFO), "figure.pdf"], check=True, capture_output=True, text=True).stdout
    require("Pages:           1" in pdf_info, "onePagePdf", checks)
    match = re.search(r"Page size:\s+([0-9.]+) x ([0-9.]+) pts", pdf_info)
    require(match is not None, "pdfPageSizePresent", checks)
    width_mm = float(match.group(1)) * 25.4 / 72.0
    height_mm = float(match.group(2)) * 25.4 / 72.0
    require(abs(width_mm - 178.0) < 0.02, "pdfWidth178mm", checks)
    require(abs(height_mm - 112.0) < 0.02, "pdfHeight112mm", checks)
    with tempfile.TemporaryDirectory(prefix="r071j-pdf-qa-") as temporary:
        stem = Path(temporary) / "render"
        subprocess.run(
            [str(PDFTOPPM), "-singlefile", "-png", "-r", "180", "figure.pdf", str(stem)],
            check=True,
            capture_output=True,
        )
        pdf_raster_width, pdf_raster_height, _ = png_info(stem.with_suffix(".png"))
        require(pdf_raster_width > 1200 and pdf_raster_height > 750, "pdfRasterized", checks)

    payload = {
        "release": "R0.71J-independent-figure",
        "status": "pass",
        "method": "independent Python-standard-library Decimal path; no producer import",
        "checks": checks,
        "metrics": {
            "maximumDecimalFormulaError": str(maximum_formula_error),
            "maximumDecimalRelativeError": str(maximum_relative_error),
            "maximumSamplingGridError": str(maximum_sampling_error),
            "maximumExactBalanceError": str(maximum_balance_error),
            "thetaStar": str(theta_star),
            "AStar": str(a_star),
            "ratioOverK2Nu1": str(ratio_constant),
            "modeLedgerTotals": {"B": "0", "F2": "500", "d": "3942"},
            "frameRadiusRange": [str(min(radii)), str(max(radii))],
            "pdfWidthMillimetres": width_mm,
            "pdfHeightMillimetres": height_mm,
            "pngPixels": [png_width, png_height],
            "pdfRasterPixelsAt180Dpi": [pdf_raster_width, pdf_raster_height],
        },
        "claimBoundary": (
            "Independent formula and archive validation for the parent-only broad "
            "frame, global cell, and heat-height-zero calculation. This is not DNS, "
            "a finite-K trajectory, a matched-cell estimate, a face-paid BV no-go, "
            "or a regularity or singularity conclusion."
        ),
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
