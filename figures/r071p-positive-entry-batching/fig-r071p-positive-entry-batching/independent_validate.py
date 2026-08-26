#!/usr/bin/env python3
"""Independent data and artifact validator for the R0.71P figure package.

This file imports neither the producer, plotter, nor research audit modules.
It reconstructs the finite formulas from CSV and inspects PDF, SVG, PNG, and
QA binaries with independent libraries.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from PIL import Image, ImageChops, ImageStat
from pypdf import PdfReader


WIDTH_MM = 178.0
HEIGHT_MM = 118.0
ROOT = Path(__file__).resolve().parent


def close(left: float, right: float, tolerance: float = 2e-10) -> bool:
    return abs(left - right) <= tolerance * max(abs(left), abs(right), 1.0)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_svg_length(value: str) -> float:
    match = re.fullmatch(r"([0-9.]+)([a-zA-Z]*)", value.strip())
    if not match:
        raise ValueError(f"invalid SVG length {value!r}")
    number = float(match.group(1))
    unit = match.group(2).lower()
    if unit == "mm":
        return number
    if unit in ("pt", ""):
        return number * 25.4 / 72.0
    if unit == "in":
        return number * 25.4
    if unit == "px":
        return number * 25.4 / 96.0
    raise ValueError(f"unsupported SVG unit {unit!r}")


def require(condition: bool, label: str, checks: dict[str, bool]) -> None:
    checks[label] = bool(condition)
    if not condition:
        raise AssertionError(label)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=ROOT / "data.csv")
    parser.add_argument("--metadata", type=Path, default=ROOT / "figure-data-metadata.json")
    parser.add_argument("--output", type=Path, default=ROOT / "independent-validation.json")
    args = parser.parse_args()
    with args.data.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    exact = json.loads((ROOT / "exact-certificate.json").read_text(encoding="utf-8"))
    independent = json.loads((ROOT / "independent-certificate.json").read_text(encoding="utf-8"))
    checks: dict[str, bool] = {}

    require(exact["release"] == "R0.71P" and exact["status"] == "passed", "exactCertificatePass", checks)
    require(independent["release"] == "R0.71P" and independent["status"] == "passed", "independentCertificatePass", checks)
    require(digest(ROOT / "exact-certificate.json") == metadata["exactCertificateSha256"], "exactCertificateHash", checks)
    require(digest(ROOT / "independent-certificate.json") == metadata["independentCertificateSha256"], "independentCertificateHash", checks)
    require(len(rows) == 62, "csvRowCount", checks)

    def subset(panel: str, series: str) -> list[dict[str, str]]:
        return [row for row in rows if row["panel"] == panel and row["series"] == series]

    # Independent formula reconstruction.
    a = {(row["case"], row["component"]): float(row["value"]) for row in subset("A", "positiveAtomComparison")}
    require(close(a[("odd crossing m=1", "segmentedSoftEntry")], 1.0), "oddSegmented", checks)
    require(close(a[("odd crossing m=1", "ordinaryHardPositiveAtom")], 1.0), "oddHard", checks)
    require(close(a[("even touch m=2", "segmentedSoftEntry")], 1.0), "evenSegmented", checks)
    require(close(a[("even touch m=2", "ordinaryHardPositiveAtom")], 0.0), "evenHardZero", checks)
    require(close(a[("even touch m=2", "missingTouchMass")], 1.0), "evenGap", checks)

    b = {(row["case"], row["component"]): float(row["value"]) for row in subset("B", "cellLedger")}
    independent_entries = (9.0 / 10.0, 0.0, 49.0 / 10.0)
    independent_budgets = (1.0, 13.0 / 5.0, 5.0)
    for index in range(1, 4):
        require(close(b[(f"cell Q{index}", "entryAtom")], independent_entries[index - 1]), f"cell{index}Entry", checks)
        require(close(b[(f"cell Q{index}", "localSupportBudget")], independent_budgets[index - 1]), f"cell{index}Budget", checks)
    summary = {row["component"]: float(row["value"]) for row in subset("B", "batchSummary")}
    require(close(summary["entrySum"], sum(independent_entries)), "entryTotal", checks)
    require(close(summary["localEnergySum"], sum(independent_budgets)), "localTotal", checks)
    require(close(summary["overlapGlobalBudget"], 12.0), "overlapTotal", checks)

    c = {series: {int(row["N"]): float(row["value"]) for row in subset("C", series)} for series in ("hardEntryMass", "softEntryMass", "ordinaryTimeBudget", "CtSquareMass", "denominatorMass")}
    for frequency in (1, 2, 4, 8, 16, 32, 64):
        require(close(c["hardEntryMass"][frequency], frequency), f"hard{frequency}", checks)
        require(close(c["softEntryMass"][frequency], frequency / (1.0 + frequency**-2)), f"soft{frequency}", checks)
        require(close(c["ordinaryTimeBudget"][frequency], 2.0 * math.pi), f"dt{frequency}", checks)
        require(close(c["CtSquareMass"][frequency], math.pi), f"ct{frequency}", checks)
        require(close(c["denominatorMass"][frequency], math.pi / frequency**2), f"denom{frequency}", checks)

    d = {row["component"]: float(row["value"]) for row in subset("D", "nseMetric")}
    require(close(d["entryAtom"], 0.25), "nseAtom", checks)
    require(close(d["projectionBudget"], 0.25), "nseBudget", checks)
    require(close(d["sharpnessRatio"], 1.0), "nseSharpRatio", checks)
    require(close(d["pairing"] ** 2, d["Y0"] * d["c2"] * d["entryAtom"]), "nseTraceFormula", checks)
    require(len(subset("D", "targetMode")) == 4, "nseModeCount", checks)

    # PDF page geometry, vector resources, and embedded text.
    reader = PdfReader(ROOT / "figure.pdf")
    require(len(reader.pages) == 1, "pdfSinglePage", checks)
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) * 25.4 / 72.0
    height_mm = float(page.mediabox.height) * 25.4 / 72.0
    require(abs(width_mm - WIDTH_MM) < 0.20, "pdfWidth178mm", checks)
    require(abs(height_mm - HEIGHT_MM) < 0.20, "pdfHeight118mm", checks)
    pdf_text = page.extract_text() or ""
    for phrase, label in (
        ("Segmented/soft entry", "pdfPanelA"),
        ("Simultaneous-cell", "pdfPanelB"),
        ("Sequential entries", "pdfPanelC"),
        ("Genuine NSE", "pdfPanelD"),
        ("not NSE", "pdfAbstractBoundary"),
        ("no internal or repeated NSE faces", "pdfNseBoundary"),
    ):
        require(phrase in pdf_text, label, checks)
    resources = page.get("/Resources") or {}
    xobjects = resources.get("/XObject") or {}
    image_count = 0
    for obj in xobjects.values():
        resolved = obj.get_object()
        if resolved.get("/Subtype") == "/Image":
            image_count += 1
    require(image_count == 0, "pdfNoRasterImageObjects", checks)

    # SVG geometry, text, and declared palette.
    root = ET.parse(ROOT / "figure.svg").getroot()
    svg_width_mm = parse_svg_length(root.attrib["width"])
    svg_height_mm = parse_svg_length(root.attrib["height"])
    require(abs(svg_width_mm - WIDTH_MM) < 0.20, "svgWidth178mm", checks)
    require(abs(svg_height_mm - HEIGHT_MM) < 0.20, "svgHeight118mm", checks)
    svg_text = (ROOT / "figure.svg").read_text(encoding="utf-8")
    require("Segmented/soft entry" in svg_text, "svgTextPreserved", checks)
    require("#355c7d" in svg_text.lower(), "svgBlue", checks)
    require("#b8792b" in svg_text.lower(), "svgOchre", checks)
    require("abstract path on [0,2pi) - not NSE" in svg_text, "svgAbstractBoundary", checks)

    # PNG dimensions and declared 600 dpi.
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_dpi = image.info.get("dpi", (0.0, 0.0))
        require(abs(png_dpi[0] - 600.0) < 1.0 and abs(png_dpi[1] - 600.0) < 1.0, "pngDpiMetadata", checks)
        require(abs(png_size[0] / png_dpi[0] * 25.4 - WIDTH_MM) < 0.20, "pngWidth600dpi", checks)
        require(abs(png_size[1] / png_dpi[1] * 25.4 - HEIGHT_MM) < 0.20, "pngHeight600dpi", checks)
        require(len(image.getcolors(maxcolors=20_000_000) or []) > 128, "pngToneCount", checks)

    with Image.open(ROOT / "qa-original.png") as color_image, Image.open(ROOT / "qa-grayscale.png") as gray_image:
        require(color_image.size == (1780, 1180), "qaOriginalSize", checks)
        require(gray_image.size == (1780, 1180), "qaGrayscaleSize", checks)
        require(gray_image.mode == "L", "qaTrueGrayscale", checks)
        converted = color_image.convert("L")
        difference = ImageChops.difference(converted, gray_image)
        require(max(ImageStat.Stat(difference).extrema[0]) <= 1, "qaGrayscaleMatches", checks)
        extrema = ImageStat.Stat(gray_image).extrema[0]
        require(extrema[1] - extrema[0] > 150, "qaGrayscaleContrast", checks)

    payload = {
        "release": "R0.71P",
        "status": "passed",
        "checkCount": len(checks),
        "checks": checks,
        "artifacts": {
            "pdf": {"widthMillimetres": width_mm, "heightMillimetres": height_mm, "imageObjectCount": image_count},
            "svg": {"widthMillimetres": svg_width_mm, "heightMillimetres": svg_height_mm},
            "png": {"pixels": list(png_size), "dpi": list(png_dpi)},
        },
        "method": "independent CSV formula reconstruction; pypdf geometry/text/vector-resource audit; standard-library SVG inspection; Pillow PNG and true-grayscale checks; no producer import",
        "claimBoundary": "Artifact and finite-formula validation only; no interval arithmetic, time-stepped NSE multiple-face theorem, uniform zero count, or regularity conclusion.",
    }
    args.output.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
