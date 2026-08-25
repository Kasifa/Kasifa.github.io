#!/usr/bin/env python3
"""Independent Decimal and archive audit for the R0.71O figure package."""

from __future__ import annotations

import argparse
import csv
import json
import re
import struct
from decimal import Decimal, getcontext
from pathlib import Path

from pypdf import PdfReader


getcontext().prec = 80
PI = Decimal("3.1415926535897932384626433832795028841971693993751")


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def decimal_close(
    left: Decimal, right: Decimal, tolerance: Decimal = Decimal("3e-12")
) -> bool:
    return abs(left - right) <= tolerance * max(abs(left), abs(right), Decimal(1))


def png_info(path: Path):
    payload = path.read_bytes()
    if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
        raise AssertionError("not PNG")
    width, height = struct.unpack(">II", payload[16:24])
    position = 8
    pixels_per_metre = None
    while position + 12 <= len(payload):
        length = struct.unpack(">I", payload[position : position + 4])[0]
        chunk_type = payload[position + 4 : position + 8]
        chunk = payload[position + 8 : position + 8 + length]
        if chunk_type == b"pHYs" and len(chunk) == 9:
            x_ppm, y_ppm, unit = struct.unpack(">IIB", chunk)
            pixels_per_metre = (x_ppm, y_ppm, unit)
        position += 12 + length
    return width, height, pixels_per_metre


def nearest_profile(rows, case: str, target: Decimal) -> Decimal:
    selected = [row for row in rows if row["case"] == case]
    row = min(selected, key=lambda item: abs(Decimal(item["x"]) - target))
    if abs(Decimal(row["x"]) - target) > Decimal("1e-12"):
        raise AssertionError(f"profile point {case} x={target} missing")
    return Decimal(row["value"])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument(
        "--metadata", type=Path, default=Path("figure-data-metadata.json")
    )
    parser.add_argument(
        "--output", type=Path, default=Path("independent-validation.json")
    )
    args = parser.parse_args()
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    grouped: dict[tuple[str, str], list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    checks: dict[str, bool] = {}

    require(len(rows) == 531, "rowCount531", checks)
    require(metadata["release"] == "R0.71O", "metadataRelease", checks)
    require(metadata["pdeTimeStepping"] is False, "noTimeStepping", checks)
    require(metadata["dns"] is False, "notDNS", checks)
    require(metadata["intervalCertified"] is False, "notIntervalCertified", checks)

    profiles = grouped[("A", "softProfile")]
    require(
        decimal_close(
            nearest_profile(profiles, "odd m=1, b>0", Decimal("-1")),
            Decimal(0),
        ),
        "oddLeftProfileZero",
        checks,
    )
    require(
        decimal_close(
            nearest_profile(profiles, "odd m=1, b>0", Decimal("1")),
            Decimal("0.5"),
        ),
        "oddRightProfileHalf",
        checks,
    )
    require(
        decimal_close(
            nearest_profile(profiles, "even m=2, b>0", Decimal("-1")),
            Decimal("0.5"),
        )
        and decimal_close(
            nearest_profile(profiles, "even m=2, b>0", Decimal("1")),
            Decimal("0.5"),
        ),
        "evenSymmetricProfileHalf",
        checks,
    )

    ledger = {
        (row["case"], row["component"]): Decimal(row["value"])
        for row in grouped[("B", "faceLedger")]
    }
    for case in ("odd m=1", "even m=2"):
        a_plus = ledger[(case, "Aplus")]
        a_minus = ledger[(case, "Aminus")]
        signed = ledger[(case, "signedAtom")]
        hard = ledger[(case, "hardBVJump")]
        jordan = ledger[(case, "relaxedJordan")]
        defect = ledger[(case, "relaxationDefect")]
        require(signed == a_plus - a_minus, f"decimalSigned_{case}", checks)
        require(hard == abs(a_plus - a_minus), f"decimalHardBV_{case}", checks)
        require(jordan == a_plus + a_minus, f"decimalJordan_{case}", checks)
        require(defect == jordan - hard, f"decimalDefect_{case}", checks)
    require(ledger[("odd m=1", "signedAtom")] == Decimal(1), "oddSignedOne", checks)
    require(ledger[("even m=2", "signedAtom")] == Decimal(0), "evenSignedZero", checks)
    require(ledger[("even m=2", "relaxedJordan")] == Decimal(2), "evenJordanTwo", checks)

    c_values = {
        (row["series"], int(row["N"])): Decimal(row["value"])
        for key in (("C", "softFaceTV"), ("C", "denominatorMass"), ("C", "CtSquareMass"))
        for row in grouped[key]
    }
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        n = Decimal(frequency)
        expected_tv = Decimal(2) * n**3 / (n**2 + Decimal(1))
        expected_d = PI / n**2
        require(
            decimal_close(c_values[("softFaceTV", frequency)], expected_tv),
            f"decimalFaceTV_N{frequency}",
            checks,
        )
        require(
            decimal_close(c_values[("denominatorMass", frequency)], expected_d),
            f"decimalDenominator_N{frequency}",
            checks,
        )
        require(
            decimal_close(c_values[("CtSquareMass", frequency)], PI),
            f"decimalCtMass_N{frequency}",
            checks,
        )

    modes = {
        (int(Decimal(row["x"])), int(Decimal(row["y"])), row["component"])
        for row in grouped[("D", "targetMode")]
    }
    require(len(modes) == 4, "independentFourModes", checks)
    require({(x, y) for x, y, _ in modes} == {(-1, -1), (-1, 1), (1, -1), (1, 1)}, "independentModeLocations", checks)
    require(all(component in {"0,0,I/4", "0,0,-I/4"} for _, _, component in modes), "independentModeCoefficients", checks)
    metrics = {
        row["component"]: Decimal(row["value"])
        for row in grouped[("D", "nseMetric")]
    }
    require(metrics["targetModeCount"] == Decimal(4), "decimalModeCount", checks)
    require(metrics["Y0"] == Decimal(1), "decimalY0", checks)
    require(metrics["F2"] == Decimal("0.25"), "decimalF2", checks)
    require(metrics["G2"] == Decimal("0.5"), "decimalG2", checks)
    require(metrics["Ct2"] == Decimal(1), "decimalCt2", checks)
    require(metrics["Bt"] == Decimal("0.5"), "decimalBt", checks)
    require(metrics["rightTrace"] == Decimal("0.25"), "decimalRightTrace", checks)

    pdf_path = Path("figure.pdf")
    svg_path = Path("figure.svg")
    png_path = Path("figure.png")
    require(pdf_path.read_bytes().startswith(b"%PDF"), "pdfSignature", checks)
    require(svg_path.read_bytes().startswith(b"<?xml"), "svgSignature", checks)
    reader = PdfReader(str(pdf_path))
    require(len(reader.pages) == 1, "pdfOnePage", checks)
    box = reader.pages[0].mediabox
    width_mm = float(box.width) * 25.4 / 72.0
    height_mm = float(box.height) * 25.4 / 72.0
    require(abs(width_mm - 178.0) < 0.05, "pdfWidth178mm", checks)
    require(abs(height_mm - 118.0) < 0.05, "pdfHeight118mm", checks)
    extracted = (reader.pages[0].extract_text() or "").lower()
    require("r0.71o" in extracted, "pdfTextR071O", checks)
    require("abstract smooth hilbert path" in extracted, "pdfTextAbstractBoundary", checks)
    require("initial jet only" in extracted, "pdfTextInitialJetBoundary", checks)
    require("regularity" in extracted, "pdfTextRegularityBoundary", checks)

    svg_head = svg_path.read_text(encoding="utf-8")[:1400]
    require(bool(re.search(r'width="178mm"', svg_head)), "svgWidth178mm", checks)
    require(bool(re.search(r'height="118mm"', svg_head)), "svgHeight118mm", checks)

    width, height, phys = png_info(png_path)
    require(width >= 4200, "pngWidthAtLeast4200", checks)
    require(height >= 2780, "pngHeightAtLeast2780", checks)
    require(phys is not None and phys[2] == 1, "pngPhysicalUnitMetres", checks)
    require(abs(phys[0] - 23622) <= 2, "png600DpiX", checks)
    require(abs(phys[1] - 23622) <= 2, "png600DpiY", checks)
    qa_width, qa_height, _ = png_info(Path("qa-original.png"))
    gray_width, gray_height, _ = png_info(Path("qa-grayscale.png"))
    require((qa_width, qa_height) == (1780, 1180), "qaOriginalFinalSize", checks)
    require((gray_width, gray_height) == (1780, 1180), "qaGrayscaleFinalSize", checks)

    payload = {
        "release": "R0.71O",
        "status": "pass",
        "method": (
            "separate Decimal reconstruction of profile, face-ledger, "
            "oscillatory, and NSE-jet values; pypdf page-size/text audit; "
            "standard-library SVG/PNG binary inspection; no producer import"
        ),
        "checks": checks,
        "metrics": {
            "independentCheckCount": len(checks),
            "pdfMillimetres": f"{width_mm:.6f} by {height_mm:.6f}",
            "pngPixels": f"{width} by {height}",
            "pngPixelsPerMetre": list(phys) if phys else None,
            "N64FaceTV": str(c_values[("softFaceTV", 64)]),
            "N64DenominatorMass": str(c_values[("denominatorMass", 64)]),
            "nseRightEntryTrace": str(metrics["rightTrace"]),
        },
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
