#!/usr/bin/env python3
"""Fail-closed validation for the R0.73A exact-audit figure package."""

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
FIGURE_ID = "fig-r073a-hidden-mean-transient-spectral"
RELEASE = "R0.73A"
PUBLIC_DIR = ROOT / "public" / "assets" / "r073a"
WIDTH_MM = 178
HEIGHT_MM = 145
PNG_DPI = 600
CERTIFICATE_BOUND_TOLERANCE = 2e-8
EXPECTED_FIELDS = [
    "panel", "kind", "id", "series", "x", "y", "value", "mu", "d", "s",
    "tau", "cAbs", "J", "rawSpectralEdge", "rawNumericalAbscissa",
    "displayValue", "projection", "targetCase", "N", "sourcePath",
    "sourceSha256", "certificateId", "formula", "status", "note",
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
    "BRACKET mu->0: NONZERO IF c_mu->c0 != 0",
    "ABSTRACT TANGENT: NO HIDDEN COORDINATE",
    "FIXED Lambda (c_mu->0): UNDECIDED",
    "bracket limit (c_mu factor excluded)",
    "ANALYTIC UPPER ENVELOPE - NOT OBSERVED GAIN",
    "J start:",
    "E mu/|c|/s:",
    "FINITE GALERKIN N=40 - NOT INFINITE-DIMENSIONAL",
    "FIXED PROJECTION SUFFICIENT: FALSE IN SCREEN",
    "NO GALERKIN TAIL BOUND",
    "LOW-GAP KINETIC / BLOCH DIRECT SUM / NONLINEAR: OPEN",
    "CLAY PROBLEM: OPEN",
]
STALE_RELEASE_TOKENS = [
    "Squire payment",
    "g ~ |c|^(2/5)",
    "CLOSED HIGH-GAP CLASS",
    "ALL-GAP PREFACTOR-ONE",
    "history-L2-multiplier",
    "kinetic-orientation",
]


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def hidden_mean(mu: float, d: float) -> float:
    return (math.exp(-2.0 * d) / (8.0 * (1.0 + mu))
            + math.exp(-8.0 * d) / (8.0 * (4.0 + mu)))


def hidden_limit(d: float) -> float:
    return math.exp(-2.0 * d) / 8.0 + math.exp(-8.0 * d) / 32.0


def transient_j(s: float, d: float) -> float:
    return (7.0 / 4.0) * (math.exp(-s) - math.exp(-d)) + 0.5 * (
        math.exp(-4.0 * s) - math.exp(-4.0 * d)
    )


def transient_envelope(mu: float, c_abs: float, s: float, d: float) -> float:
    return math.exp(-mu * (d - s) + c_abs * transient_j(s, d))


def signed_log(value: float) -> float:
    return math.copysign(math.log10(1.0 + abs(value)), value) if value else 0.0


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
    if float(config["panelB"]["certificateBoundTolerance"]) != CERTIFICATE_BOUND_TOLERANCE:
        fail("certificate crosscheck tolerance differs from fixed 2e-8")
    with (PACKAGE / "data.csv").open(encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != EXPECTED_FIELDS:
            fail("data schema is not exact")
        rows = list(reader)
    a = [row for row in rows if row["panel"] == "A"]
    b = [row for row in rows if row["panel"] == "B"]
    c = [row for row in rows if row["panel"] == "C"]
    certificate = [row for row in b
                   if row["kind"] == "certified-xmu-propagator-gain"]
    if (len(rows), len(a), len(b), len(c)) != (
            851 + len(certificate), 305, 486 + len(certificate), 60):
        fail("data row-count contract failed")
    kinds = {kind: [row for row in rows if row["kind"] == kind]
             for kind in {row["kind"] for row in rows}}
    expected_counts = {
        "hidden-mean-excitation": 244,
        "abstract-limit-mismatch": 61,
        "exact-J-kernel": 243,
        "analytic-transient-envelope": 243,
        "frozen-spectral-edge": 30,
        "frozen-numerical-abscissa": 30,
    }
    if {key: len(kinds.get(key, [])) for key in expected_counts} != expected_counts:
        fail("kind row counts are not exact")
    tol = 5e-14
    for row in kinds["hidden-mean-excitation"]:
        expected = hidden_mean(float(row["mu"]), float(row["d"]))
        if abs(float(row["value"]) - expected) > tol * max(1.0, abs(expected)):
            fail("hidden mean mismatch")
    for row in kinds["abstract-limit-mismatch"]:
        expected = hidden_limit(float(row["d"]))
        if abs(float(row["value"]) - expected) > tol:
            fail("hidden singular limit mismatch")
    if abs(hidden_limit(0.0) - 5.0 / 32.0) > tol:
        fail("hidden singular limit at d=0 is wrong")
    for row in kinds["exact-J-kernel"]:
        expected = transient_j(float(row["s"]), float(row["d"]))
        if abs(float(row["value"]) - expected) > tol:
            fail("J kernel mismatch")
    for row in kinds["analytic-transient-envelope"]:
        expected = transient_envelope(float(row["mu"]), float(row["cAbs"]),
                                      float(row["s"]), float(row["d"]))
        if abs(float(row["value"]) - expected) > tol * max(1.0, abs(expected)):
            fail("analytic envelope mismatch")
        if abs(float(row["displayValue"]) - math.log10(expected)) > tol:
            fail("analytic envelope display transform mismatch")

    panel_c = config["panelC"]
    source_path = ROOT / panel_c["sourceCsv"]
    validation_path = ROOT / panel_c["validationJson"]
    if sha256(source_path) != panel_c["sourceSha256"]:
        fail("Panel C source hash differs from the source contract")
    if sha256(validation_path) != panel_c["validationSha256"]:
        fail("Panel C validation hash differs from the source contract")
    upstream = json.loads(validation_path.read_text(encoding="utf-8"))
    if upstream.get("status") != "passed" or not all(upstream.get("checks", {}).values()):
        fail("Panel C upstream validation is not fully passed")
    with source_path.open(encoding="utf-8") as stream:
        source_rows = [row for row in csv.DictReader(stream)
                       if int(row["N"]) == int(panel_c["N"])]
    if len(source_rows) != 30:
        fail("Panel C source must contain exactly 30 N=40 target rows")
    lookup = {(row["caseId"], row["projection"]): row for row in source_rows}
    if len(lookup) != 30:
        fail("Panel C source target/projection keys are not unique")
    for row in c:
        source = lookup.get((row["targetCase"], row["projection"]))
        if source is None:
            fail("Panel C plotted row has no upstream source row")
        source_field = ("spectralAbscissa" if row["kind"] == "frozen-spectral-edge"
                        else "numericalAbscissa")
        raw_field = ("rawSpectralEdge" if row["kind"] == "frozen-spectral-edge"
                     else "rawNumericalAbscissa")
        expected_raw = float(source[source_field])
        if abs(float(row[raw_field]) - expected_raw) > tol:
            fail("Panel C raw metric differs from upstream source")
        if abs(float(row["displayValue"]) - signed_log(expected_raw)) > tol:
            fail("Panel C display transform mismatch")
        if (row["N"] != "40" or row["sourcePath"] != panel_c["sourceCsv"]
                or row["sourceSha256"] != panel_c["sourceSha256"]):
            fail("Panel C provenance fields are incomplete")
    minimum_padding = float(panel_c["minimumDisplayPadding"])
    for kind in ("frozen-spectral-edge", "frozen-numerical-abscissa"):
        values = [float(row["displayValue"]) for row in kinds[kind]]
        lo, hi = map(float, panel_c["displayDomains"][kind])
        ticks = list(map(float, panel_c["displayTicks"][kind]))
        if min(values) - lo < minimum_padding or hi - max(values) < minimum_padding:
            fail(f"Panel C {kind} domain lacks required data padding")
        if 0.0 not in ticks or any(not lo <= tick <= hi for tick in ticks):
            fail(f"Panel C {kind} ticks omit zero or leave the domain")

    for row in certificate:
        if not (row["certificateId"] and float(row["value"]) > 0.0
                and row["sourcePath"] == config["panelB"]["certificateCsv"]):
            fail("certificate overlay row is incomplete")
        certificate_path = ROOT / row["sourcePath"]
        with certificate_path.open(encoding="utf-8") as stream:
            certificate_lookup = {
                source["certificateId"]: source for source in csv.DictReader(stream)
            }
        source = certificate_lookup.get(row["certificateId"])
        if source is None:
            fail("certificate overlay ID is absent from its source CSV")
        gain, bound = float(source["gain"]), float(source["bound"])
        if not (0.0 < gain <= bound + CERTIFICATE_BOUND_TOLERANCE):
            fail("certificate gain exceeds bound + fixed 2e-8 crosscheck tolerance")
    if not certificate and config["panelB"]["certificateAvailableAtSourceFreeze"]:
        fail("source contract says the absent certificate was available")
    return {"rows": rows, "a": a, "b": b, "c": c,
            "certificate": certificate}

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
    for token in STALE_RELEASE_TOKENS:
        if token in text:
            fail(f"stale R0.72Z token found in SVG: {token}")
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
    for token in STALE_RELEASE_TOKENS:
        if token in text:
            fail(f"stale R0.72Z token found in PDF: {token}")
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
    if publication.get("directory") != "public/assets/r073a":
        fail("publication directory mismatch")
    expected = [f"{FIGURE_ID}.{suffix}" for suffix in ("pdf", "svg", "png")]
    if publication.get("files") != expected:
        fail("publication file list mismatch")
    if publication.get("stem") != FIGURE_ID:
        fail("publication stem mismatch")
    assets = publication.get("assets")
    if not isinstance(assets, list) or len(assets) != 3:
        fail("publication asset ledger mismatch")
    for suffix, row in zip(("pdf", "svg", "png"), assets, strict=True):
        archive = PACKAGE / f"figure.{suffix}"
        expected_path = f"public/assets/r073a/{FIGURE_ID}.{suffix}"
        if row.get("path") != expected_path:
            fail(f"public {suffix} path mismatch")
        if row.get("bytes") != archive.stat().st_size or row.get("sha256") != sha256(archive):
            fail(f"public {suffix} ledger differs from archival master")
    if manifest.get("status") != "formal":
        if (publication.get("byteIdenticalToArchive") is not False
                or publication.get("publicCopiesComplete") is not False
                or any(row.get("byteIdenticalToMaster") is not False for row in assets)):
            fail("draft publication must remain unsealed")
        return
    if (publication.get("byteIdenticalToArchive") is not True
            or publication.get("publicCopiesComplete") is not True
            or any(row.get("byteIdenticalToMaster") is not True for row in assets)):
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
    plot_source = (PACKAGE / "plot.py").read_text(encoding="utf-8")
    for token in STALE_RELEASE_TOKENS:
        if token in plot_source:
            fail(f"stale R0.72Z token found in plot.py: {token}")
    manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("figureId") != FIGURE_ID or manifest.get("release") != RELEASE:
        fail("figure identity or release mismatch")
    if args.require_formal and manifest.get("status") != "formal":
        fail("formal figure package required")
    dependency = manifest.get("dependency", {})
    if manifest.get("status") == "formal" and (
            dependency.get("available") is not True
            or dependency.get("formalBlocked") is not False):
        fail("formal figure requires an available X_mu propagator certificate")
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
    expected_rows = 851 + len(data["certificate"])
    if results.get("rowCount") != expected_rows or results.get("deterministic") is not True:
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
