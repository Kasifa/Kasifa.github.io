#!/usr/bin/env python3
"""Fail-closed validation for the R0.72Z exact-audit figure package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

from PIL import Image
from pypdf import PdfReader


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
FIGURE_ID = "fig-r072z-os-squire-threshold"
RELEASE = "R0.72Z"
PUBLIC_DIR = ROOT / "public" / "assets" / "r072z"
WIDTH_MM = 178
HEIGHT_MM = 145
PNG_DPI = 600
EXPECTED_FIELDS = [
    "panel", "kind", "id", "series", "x", "y", "value", "alpha", "gap",
    "cAbs", "theta0", "modeN", "orientationRatio", "rhoOverGamma", "chi",
    "A_vartheta", "B_vartheta", "formula", "status", "note",
]
SOURCE_FILES = {
    "README.md", "caption.md", "command.txt", "config.json", "contract.json",
    "environment.txt", "figure-contract.md", "plot.py", "qa-protocol.md",
    "manifest-draft.json", "requirements.txt", "validate.py",
}
GENERATED_FILES = {
    "data.csv", "results.json", "validation.json", "figure.svg", "figure.pdf",
    "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "qa-report.md", "manifest.json", "SHA256SUMS",
}
REQUIRED_VISIBLE = [
    "CLOSED HIGH-GAP CLASS | COARSE CONSTANT NOT OPTIMAL",
    "g ~ |c|^(2/5) = alpha^(-2): SHARP POWER",
    "ALL-GAP PREFACTOR-ONE L2_q CONTRACTION: FALSE",
    "ABSTRACT TANGENT - NOT PHYSICAL mu=0 ROW",
    "|Lambda| PAID | Q HISTORY REQUIRED",
    "EXACT FORMULAS - NO PDE SIMULATION | LOW-GAP OS PROPAGATOR: OPEN",
    "CLAY PROBLEM: OPEN",
]


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def signed_envelope(z: float, m3: float) -> float:
    return 4.0 * m3 * z ** (-2.5)


def high_mode_scaled(n: int, d: float) -> float:
    mu = 2.0 * n * n
    return (math.exp(-d) * (2.0 * n + 1.0) * mu ** 2.5
            / (8.0 * (3.0 * n * n) ** 1.5
               * (3.0 * n * n + 2.0 * n + 1.0) ** 1.5))


def low_mode_growth(mu: float, c_abs: float) -> float:
    return c_abs / (8.0 * mu ** 1.5 * (1.0 + mu) ** 1.5) - 1.0


def tangent_ratio(alpha: float, t_block: float) -> float:
    norm = lambda d: math.exp(-2.0 * d) / 8.0 + math.exp(-8.0 * d) / 2.0
    return math.sqrt(norm(2.0 * t_block * alpha * alpha) / norm(0.0))


def embedded_font_count(reader: PdfReader) -> int:
    count = 0
    fonts = reader.pages[0]["/Resources"].get("/Font", {})
    fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
    for reference in fonts.values():
        font = reference.get_object()
        descendants = font.get("/DescendantFonts", [])
        candidates = [font]
        if descendants:
            candidates.extend(item.get_object() for item in descendants)
        for candidate in candidates:
            descriptor = candidate.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                if any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")):
                    count += 1
                    break
    return count


def validate_hash_records(manifest: dict) -> None:
    records = []
    records.extend(manifest.get("data", []))
    records.extend(manifest.get("figure", {}).get("outputs", []))
    records.extend(manifest.get("outputs", []))
    for record in records:
        path = PACKAGE / record["path"]
        if not path.is_file():
            fail(f"hashed file missing: {record['path']}")
        if path.stat().st_size != record["bytes"]:
            fail(f"byte count mismatch: {record['path']}")
        if sha256(path) != record["sha256"]:
            fail(f"hash mismatch: {record['path']}")


def validate_sums() -> None:
    seen = {}
    for line in (PACKAGE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        if not match:
            fail(f"invalid SHA256SUMS line: {line}")
        seen[match.group(2)] = match.group(1)
    expected = (SOURCE_FILES | GENERATED_FILES) - {"SHA256SUMS"}
    if set(seen) != expected:
        fail("SHA256SUMS inventory is not exact")
    for name, expected_hash in seen.items():
        if sha256(PACKAGE / name) != expected_hash:
            fail(f"SHA256SUMS mismatch: {name}")


def validate_data() -> dict:
    config = json.loads((PACKAGE / "config.json").read_text(encoding="utf-8"))
    with (PACKAGE / "data.csv").open(encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != EXPECTED_FIELDS:
            fail("data schema is not exact")
        rows = list(reader)
    a = [row for row in rows if row["panel"] == "A"]
    b = [row for row in rows if row["panel"] == "B"]
    c = [row for row in rows if row["panel"] == "C"]
    if (len(rows), len(a), len(b), len(c)) != (769, 141, 223, 405):
        fail("data row-count contract failed")
    kinds = {kind: [row for row in rows if row["kind"] == kind]
             for kind in {row["kind"] for row in rows}}
    expected_counts = {
        "signed-threshold-envelope": 61,
        "high-mode-sharpness-sequence": 80,
        "low-mode-instantaneous-growth": 162,
        "abstract-tangent-block-ratio": 61,
        "kinetic-orientation": 243,
        "history-L2-multiplier": 81,
        "history-endpoint-multiplier": 81,
    }
    if {key: len(kinds.get(key, [])) for key in expected_counts} != expected_counts:
        fail("kind row counts are not exact")
    tol = 5e-14
    m3 = float(config["panelA"]["M3"])
    d0 = float(config["panelA"]["d0"])
    for row in kinds["signed-threshold-envelope"]:
        expected = signed_envelope(float(row["x"]), m3)
        if abs(float(row["value"]) - expected) > tol * max(1.0, abs(expected)):
            fail("signed envelope mismatch")
    for row in kinds["high-mode-sharpness-sequence"]:
        if abs(float(row["value"]) - high_mode_scaled(int(row["modeN"]), d0)) > tol:
            fail("high-mode sequence mismatch")
    if abs(float(kinds["high-mode-sharpness-sequence"][-1]["value"])
           - math.sqrt(2.0) / 27.0) > 5e-4:
        fail("high-mode sequence misses its exact limit")
    for row in kinds["low-mode-instantaneous-growth"]:
        expected = low_mode_growth(float(row["gap"]), float(row["cAbs"]))
        if abs(float(row["value"]) - expected) > tol * max(1.0, abs(expected)):
            fail("low-mode growth mismatch")
    for label in {row["series"] for row in kinds["low-mode-instantaneous-growth"]}:
        values = [float(row["value"]) for row in kinds["low-mode-instantaneous-growth"]
                  if row["series"] == label]
        if not (min(values) < 0 < max(values)):
            fail(f"growth series does not cross zero: {label}")
    for row in kinds["abstract-tangent-block-ratio"]:
        expected = tangent_ratio(float(row["alpha"]), float(config["panelB"]["T"]))
        if abs(float(row["value"]) - expected) > tol:
            fail("tangent ratio mismatch")
    for row in kinds["kinetic-orientation"]:
        ratio = float(row["orientationRatio"])
        rho = float(row["rhoOverGamma"])
        expected = ratio / math.sqrt(1.0 + ratio * ratio + rho * rho)
        if abs(float(row["value"]) - expected) > tol or not 0 < expected < 1:
            fail("kinetic orientation mismatch")
    for kind in ("history-L2-multiplier", "history-endpoint-multiplier"):
        for row in kinds[kind]:
            gap, alpha, chi = map(float, (row["gap"], row["alpha"], row["chi"]))
            expected = (chi * min(1.0 / gap, float(row["A_vartheta"]) * alpha ** 2)
                        if kind == "history-L2-multiplier"
                        else chi * min(1.0 / math.sqrt(2.0 * gap),
                                       math.sqrt(float(row["B_vartheta"])) * alpha))
            if abs(float(row["value"]) - expected) > tol:
                fail("history multiplier mismatch")
    return {"rows": rows, "a": a, "b": b, "c": c}

def validate_svg() -> str:
    path = PACKAGE / "figure.svg"
    root = ET.parse(path).getroot()
    if root.attrib.get("width") != "178mm" or root.attrib.get("height") != "145mm":
        fail("SVG physical dimensions are not exact")
    if root.attrib.get("viewBox") != "0 0 1780 1450":
        fail("SVG viewBox is not exact")
    text = "\n".join(element.text or "" for element in root.iter()
                     if element.tag.endswith("text"))
    for required in REQUIRED_VISIBLE:
        if required not in text:
            fail(f"required SVG boundary missing: {required}")
    raw = path.read_text(encoding="utf-8").upper()
    for root_color in ("#285F8F", "#A6781F"):
        if root_color not in raw:
            fail(f"declared chromatic root missing: {root_color}")
    forbidden = {"#FF0000", "#00FF00", "#008000", "#D62728", "#2CA02C"}
    if any(color in raw for color in forbidden):
        fail("undeclared red/green palette found")
    return text


def validate_pdf() -> dict:
    reader = PdfReader(PACKAGE / "figure.pdf")
    if len(reader.pages) != 1:
        fail("PDF must contain exactly one page")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) * 25.4 / 72.0
    height_mm = float(page.mediabox.height) * 25.4 / 72.0
    if abs(width_mm - WIDTH_MM) > 0.02 or abs(height_mm - HEIGHT_MM) > 0.02:
        fail(f"PDF page size mismatch: {width_mm} x {height_mm} mm")
    if list(page.images):
        fail("PDF contains raster image XObjects")
    fonts = embedded_font_count(reader)
    if fonts < 2:
        fail(f"expected two embedded Arial fonts, found {fonts}")
    text = page.extract_text() or ""
    for required in REQUIRED_VISIBLE:
        if required not in text:
            fail(f"required PDF boundary missing: {required}")
    return {"widthMillimetres": width_mm, "heightMillimetres": height_mm,
            "embeddedFontCount": fonts, "rasterImageCount": 0}


def validate_pngs() -> dict:
    expected_w = round(WIDTH_MM / 25.4 * PNG_DPI)
    expected_h = round(HEIGHT_MM / 25.4 * PNG_DPI)
    with Image.open(PACKAGE / "figure.png") as image:
        if image.size != (expected_w, expected_h):
            fail(f"600-dpi PNG dimensions mismatch: {image.size}")
        dpi = image.info.get("dpi", (0.0, 0.0))
        if any(abs(float(value) - PNG_DPI) > 0.1 for value in dpi):
            fail(f"PNG dpi metadata mismatch: {dpi}")
        rgb = image.convert("RGB")
        corners = [rgb.getpixel((0, 0)), rgb.getpixel((rgb.width - 1, 0)),
                   rgb.getpixel((0, rgb.height - 1)),
                   rgb.getpixel((rgb.width - 1, rgb.height - 1))]
        if corners != [(255, 255, 255)] * 4:
            fail("outer PNG corners are not white; possible crop failure")
    preview_size = (round(WIDTH_MM / 25.4 * 300),
                    round(HEIGHT_MM / 25.4 * 300))
    with Image.open(PACKAGE / "qa-final-size.png") as image:
        if image.size != preview_size:
            fail(f"qa-final-size.png size mismatch: {image.size}")
    with Image.open(PACKAGE / "qa-pdf.png") as image:
        if any(abs(actual - expected) > 1
               for actual, expected in zip(image.size, preview_size)):
            fail(f"qa-pdf.png size mismatch: {image.size}")
    with Image.open(PACKAGE / "qa-grayscale.png") as image:
        if image.size != preview_size:
            fail("grayscale preview size mismatch")
        rgb = image.convert("RGB")
        sample_step = max(1, rgb.width // 100)
        for y in range(0, rgb.height, sample_step):
            for x in range(0, rgb.width, sample_step):
                r, g, b = rgb.getpixel((x, y))
                if not (r == g == b):
                    fail("grayscale preview contains chromatic pixels")
    return {"pixels": [expected_w, expected_h], "dpi": PNG_DPI,
            "previewPixels": list(preview_size), "cornersWhite": True}


def validate_lineage(manifest: dict) -> None:
    git = manifest["git"]
    status = manifest["status"]
    if status == "draft":
        if git["sourceCommit"] != "pending" or git["certificateCommit"] != "pending":
            fail("draft lineage must remain explicitly pending")
        return
    if status != "formal":
        fail(f"invalid manifest status: {status}")
    source = git["sourceCommit"]
    certificate = git["certificateCommit"]
    if not re.fullmatch(r"[0-9a-f]{40}", source):
        fail("formal source commit is invalid")
    if not re.fullmatch(r"[0-9a-f]{40}", certificate):
        fail("formal certificate commit is invalid")
    if source == certificate:
        fail("formal source and certificate commits must differ")
    if subprocess.run(["git", "merge-base", "--is-ancestor", source, certificate],
                      cwd=ROOT).returncode:
        fail("formal certificate commit does not descend from source commit")
    source_paths = [str(PACKAGE.relative_to(ROOT) / name) for name in SOURCE_FILES]
    if subprocess.run(["git", "diff", "--quiet", source, certificate, "--",
                       *source_paths], cwd=ROOT).returncode:
        fail("figure source changed between source and certificate commits")


def validate_publication(manifest: dict) -> None:
    publication = manifest.get("publication")
    if not isinstance(publication, dict):
        fail("publication ledger is missing")
    if publication.get("directory") != "public/assets/r072z":
        fail("publication directory mismatch")
    expected = [f"{FIGURE_ID}.{suffix}" for suffix in ("pdf", "svg", "png")]
    if publication.get("files") != expected:
        fail("publication file list mismatch")
    if manifest.get("status") != "formal":
        if publication.get("byteIdenticalToArchive") is not False:
            fail("draft publication must remain unsealed")
        return
    if publication.get("byteIdenticalToArchive") is not True:
        fail("formal publication identity is not sealed")
    for suffix in ("pdf", "svg", "png"):
        public = PUBLIC_DIR / f"{FIGURE_ID}.{suffix}"
        archive = PACKAGE / f"figure.{suffix}"
        if not public.is_file() or sha256(public) != sha256(archive):
            fail(f"public {suffix} is absent or not byte-identical")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    names = {path.name for path in PACKAGE.iterdir() if path.is_file()}
    if names != SOURCE_FILES | GENERATED_FILES:
        fail(f"package inventory is not exact: {sorted(names ^ (SOURCE_FILES | GENERATED_FILES))}")
    manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("figureId") != FIGURE_ID or manifest.get("release") != RELEASE:
        fail("figure identity or release mismatch")
    if args.require_formal and manifest.get("status") != "formal":
        fail("formal figure package required")
    validate_lineage(manifest)
    validate_publication(manifest)
    validate_hash_records(manifest)
    validate_sums()
    data = validate_data()
    svg_text = validate_svg()
    pdf = validate_pdf()
    png = validate_pngs()

    validation = json.loads((PACKAGE / "validation.json").read_text(encoding="utf-8"))
    if validation.get("status") != "passed" or not all(validation.get("checks", {}).values()):
        fail("archived validation ledger is not fully passed")
    results = json.loads((PACKAGE / "results.json").read_text(encoding="utf-8"))
    if results.get("rowCount") != 769 or results.get("deterministic") is not True:
        fail("results ledger mismatch")
    if results.get("panelC", {}).get("fittedQuantities") != []:
        fail("fitted quantities are forbidden")
    if manifest.get("claimBoundary") != json.loads(
        (PACKAGE / "contract.json").read_text(encoding="utf-8")
    )["claimBoundary"]:
        fail("claim boundary differs from the source contract")
    qa = manifest.get("qa", {})
    if qa.get("status") != "passed":
        fail("visual QA has not been sealed")
    if qa.get("visualInspectionExplicit") is not True:
        fail("visual inspection is not explicit")
    for key in (
        "finalSizeInspected", "grayscaleInspected", "labelsAndLegendsInspected",
        "scalesAndUnitsInspected", "dataCrossChecked", "fontEmbeddingInspected",
        "croppingInspected",
    ):
        if qa.get(key) is not True:
            fail(f"QA field is false: {key}")
    report = {
        "status": "passed",
        "manifestStatus": manifest["status"],
        "figureId": FIGURE_ID,
        "rows": len(data["rows"]),
        "pdf": pdf,
        "png": png,
        "visibleBoundaryCount": len(REQUIRED_VISIBLE),
        "errors": [],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
