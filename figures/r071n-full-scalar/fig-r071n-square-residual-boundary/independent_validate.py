#!/usr/bin/env python3
"""Independent Decimal and archive audit for the R0.71N figure package."""

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


EXPECTED = {
    "seed 49": {
        "positiveSquare": Decimal("5023.642509952941"),
        "signedResidual": Decimal("749.9219442938775"),
        "J": Decimal("1.352354294391183"),
        "z": Decimal("0.0037338304858202916"),
    },
    "seed 5": {
        "positiveSquare": Decimal("5167.69457947911"),
        "signedResidual": Decimal("-25941.29401331811"),
        "J": Decimal("-7.371344134519265"),
        "z": Decimal("0.0019598744198175808"),
    },
}


def require(condition, label, checks):
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def decimal_close(left, right, tolerance=Decimal("2e-12")):
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
    by_key = {
        (row["series"], row["witness"]): Decimal(row["value"])
        for row in rows if row["witness"]
    }
    checks = {}

    for witness, expected in EXPECTED.items():
        for series, expected_value in expected.items():
            require(
                decimal_close(by_key[(series, witness)], expected_value),
                f"decimal_{witness}_{series}",
                checks,
            )
        total = by_key[("numeratorTotal", witness)]
        root = by_key[("normalizerRoot", witness)]
        require(
            decimal_close(
                total,
                by_key[("positiveSquare", witness)]
                + by_key[("signedResidual", witness)],
            ),
            f"decimal_{witness}_componentSum",
            checks,
        )
        require(
            decimal_close(by_key[("J", witness)], total / root),
            f"decimal_{witness}_normalization",
            checks,
        )
        require(by_key[("z", witness)] > 0, f"decimal_{witness}_positiveZ", checks)
    require(by_key[("J", "seed 49")] > 0, "decimalPositiveJ", checks)
    require(by_key[("J", "seed 5")] < 0, "decimalNegativeJ", checks)
    require(metadata["intervalCertified"] is False, "diagnosticNotInterval", checks)
    require(metadata["pdeTimeStepping"] is False, "noTimeStepping", checks)

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
    extracted = reader.pages[0].extract_text() or ""
    require("R0.71N" in extracted, "pdfTextR071N", checks)
    require("diagnostic" in extracted.lower(), "pdfTextDiagnostic", checks)

    svg_head = svg_path.read_text(encoding="utf-8")[:1200]
    require(bool(re.search(r'width="178mm"', svg_head)), "svgWidth178mm", checks)
    require(bool(re.search(r'height="118mm"', svg_head)), "svgHeight118mm", checks)

    width, height, phys = png_info(png_path)
    require(width >= 4200, "pngWidthAtLeast4200", checks)
    require(height >= 2780, "pngHeightAtLeast2780", checks)
    require(phys is not None and phys[2] == 1, "pngPhysicalUnitMetres", checks)
    require(abs(phys[0] - 23622) <= 2, "png600DpiX", checks)
    require(abs(phys[1] - 23622) <= 2, "png600DpiY", checks)

    payload = {
        "release": "R0.71N",
        "status": "pass",
        "method": (
            "separate Decimal reconstruction, pypdf page-size/text audit, "
            "and standard-library SVG/PNG binary inspection; no producer import"
        ),
        "checks": checks,
        "metrics": {
            "independentCheckCount": len(checks),
            "pdfMillimetres": f"{width_mm:.6f} by {height_mm:.6f}",
            "pngPixels": f"{width} by {height}",
            "pngPixelsPerMetre": list(phys) if phys else None,
        },
    }
    args.output.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
