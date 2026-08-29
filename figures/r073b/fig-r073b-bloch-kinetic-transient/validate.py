#!/usr/bin/env python3
"""Independent fail-closed validator for the R0.73B journal figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import xml.etree.ElementTree as ET

from PIL import Image
from pypdf import PdfReader


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
FIGURE_ID = "fig-r073b-bloch-kinetic-transient"
RELEASE = "R0.73B"
WIDTH_MM = 178
HEIGHT_MM = 150
PNG_DPI = 600
EXPECTED_FIELDS = [
    "panel", "kind", "id", "series", "x", "y", "value", "mu",
    "Lambda", "p", "a", "norm", "N", "start", "end", "gain",
    "finiteGain", "triangularGain", "energyEnvelope",
    "observedExponent", "predictedExponent", "sourcePath",
    "sourceSha256", "sourceRowId", "formula", "status", "note",
]
SOURCE_FILES = {
    "README.md", "caption.md", "command.txt", "config.json", "contract.json",
    "environment.txt", "figure-contract.md", "manifest-draft.json", "plot.py",
    "qa-protocol.md", "requirements.txt", "validate.py",
}
GENERATED_FILES = {
    "data.csv", "results.json", "validation.json", "figure.svg", "figure.pdf",
    "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "qa-report.md", "manifest.json", "SHA256SUMS",
}
REQUIRED_VISIBLE = [
    "FINITE N=10 DIAGNOSTICS - NO GALERKIN TAIL",
    "ANALYTIC ENERGY ENVELOPE - UPPER BOUND",
    "ANALYTIC ONLY - NO TRUNCATED OPERATOR NORM",
    "BLOCK PREDICTION (a/2-p)_+",
    "EXACT MAXIMUM TRANSIENT: NOT CLAIMED",
    "rho_0(0) = 1/4",
    "0.188106... is an integrated log coefficient, not a gain",
    "A2 DIRECT SUM / NONLINEAR / CLAY: OPEN",
]
STALE_OR_FORBIDDEN = [
    "Clay problem: solved", "GALERKIN TAIL: PROVED",
    "EXACT MAXIMUM TRANSIENT: PROVED", "R0.73A |",
]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def close(left: float, right: float, tolerance: float = 5e-13) -> bool:
    return abs(left - right) <= tolerance * max(1.0, abs(left), abs(right))


def heat_shear_k(start: float, end: float) -> float:
    return (0.5 * (math.exp(-start) - math.exp(-end))
            + 0.125 * (math.exp(-4.0 * start) - math.exp(-4.0 * end)))


def energy_envelope(mu: float, lam: float, start: float, end: float) -> float:
    return math.exp(-mu * (end - start) + abs(lam) * heat_shear_k(start, end) / 2.0)


def triangular_gain(lam: float, start: float, end: float) -> float:
    tau = end - start
    d1, d2 = math.exp(-tau), math.exp(-4.0 * tau)
    z1 = lam * tau * math.exp(-end) / 4.0
    z2 = lam * tau * math.exp(-4.0 * end) / 4.0
    matrix = [
        [1.0, 0.0, 0.0, 0.0, 0.0],
        [z2, d2, 0.0, 0.0, 0.0],
        [z1, 0.0, d1, 0.0, 0.0],
        [-z1, 0.0, 0.0, d1, 0.0],
        [-z2, 0.0, 0.0, 0.0, d2],
    ]
    gram = [[sum(matrix[k][i] * matrix[k][j] for k in range(5))
             for j in range(5)] for i in range(5)]
    vector = [1.0, -0.3, 0.7, -0.9, 0.2]
    for _ in range(260):
        product = [sum(gram[i][j] * vector[j] for j in range(5))
                   for i in range(5)]
        length = math.sqrt(sum(value * value for value in product))
        vector = [value / length for value in product]
    eigenvalue = sum(vector[i] * gram[i][j] * vector[j]
                     for i in range(5) for j in range(5))
    return math.sqrt(eigenvalue)


def embedded_font_count(reader: PdfReader) -> int:
    count = 0
    fonts = reader.pages[0]["/Resources"].get("/Font", {})
    fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
    for reference in fonts.values():
        font = reference.get_object()
        candidates = [font]
        descendants = font.get("/DescendantFonts", [])
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


def validate_inventory(manifest: dict) -> None:
    require(set(path.name for path in PACKAGE.iterdir() if path.is_file())
            == SOURCE_FILES | GENERATED_FILES,
            "package top-level inventory is not exact")
    seen: dict[str, str] = {}
    for line in (PACKAGE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, f"malformed SHA256SUMS line: {line}")
        seen[match.group(2)] = match.group(1)
    expected = (SOURCE_FILES | GENERATED_FILES) - {"SHA256SUMS"}
    require(set(seen) == expected, "SHA256SUMS inventory is not exact")
    for name, digest in seen.items():
        require(sha256(PACKAGE / name) == digest, f"SHA256SUMS mismatch: {name}")

    records = manifest.get("outputs", [])
    records += manifest.get("figure", {}).get("outputs", [])
    for record in records:
        path = PACKAGE / record["path"]
        require(path.is_file(), f"manifest output missing: {record['path']}")
        require(path.stat().st_size == record["bytes"],
                f"manifest byte mismatch: {record['path']}")
        require(sha256(path) == record["sha256"],
                f"manifest hash mismatch: {record['path']}")


def validate_upstream(manifest: dict) -> dict[str, Path]:
    config = read_json(PACKAGE / "config.json")
    paths = {key: ROOT / value for key, value in config["upstream"].items()}
    require(set(manifest["upstream"]) == set(paths), "manifest upstream keys changed")
    for key, path in paths.items():
        record = manifest["upstream"][key]
        require(path.is_file() and record["path"] == str(path.relative_to(ROOT)),
                f"upstream path mismatch: {key}")
        require(path.stat().st_size == record["bytes"] and sha256(path) == record["sha256"],
                f"upstream hash mismatch: {key}")
    experiment = read_json(paths["experimentValidation"])
    certificate = read_json(paths["certificate"])
    cert_validation = read_json(paths["certificateValidation"])
    require(experiment.get("status") == "passed" and all(experiment.get("checks", {}).values()),
            "experiment validation no longer fully passes")
    require(certificate.get("release") == RELEASE,
            "certificate release changed")
    require(cert_validation.get("status") == "passed" and all(cert_validation.get("checks", {}).values()),
            "certificate validation no longer fully passes")
    require(certificate["claimBoundary"]["GalerkinTailBoundProved"] is False
            and certificate["claimBoundary"]["nonlinearNavierStokesProved"] is False,
            "certificate negative boundary changed")
    return paths


def validate_data(paths: dict[str, Path]) -> dict[str, list[dict[str, str]]]:
    with (PACKAGE / "data.csv").open(encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == EXPECTED_FIELDS, "data.csv schema is not exact")
        rows = list(reader)
    panels = {letter: [row for row in rows if row["panel"] == letter]
              for letter in "ABCD"}
    require(len(rows) == 364, "data.csv must contain exactly 364 rows")
    require({key: len(value) for key, value in panels.items()}
            == {"A": 39, "B": 12, "C": 183, "D": 130},
            "panel row counts changed")
    for row in rows:
        source = ROOT / row["sourcePath"]
        require(source.is_file() and sha256(source) == row["sourceSha256"],
                f"row source hash mismatch: {row['id']}")
        value = float(row["value"])
        require(math.isfinite(value), f"non-finite plotted value: {row['id']}")

    # Panel A exact source reconciliation.
    with paths["mainRows"].open(encoding="utf-8") as stream:
        main_rows = list(csv.DictReader(stream))
    with paths["targetedRows"].open(encoding="utf-8") as stream:
        targeted_rows = list(csv.DictReader(stream))
    require(len(main_rows) == 1960 and len(targeted_rows) == 245,
            "upstream row counts changed")
    main_lookup = {(row["caseId"] + ":" + row["norm"]): row for row in main_rows}
    for series in {row["series"] for row in panels["A"]}:
        subset = [row for row in panels["A"] if row["series"] == series]
        require(len(subset) == 13 and len({row["mu"] for row in subset}) == 13,
                f"Panel A distinct-mu contract failed: {series}")
    for row in panels["A"]:
        if row["sourcePath"].endswith("weighted_propagator_rows.csv"):
            source = main_lookup.get(row["sourceRowId"])
            require(source is not None and close(float(source["gain"]), float(row["gain"]), 2e-15),
                    f"Panel A main row mismatch: {row['id']}")
        else:
            line_number = int(row["sourceRowId"].split("-")[-1])
            source = targeted_rows[line_number - 2]
            require(close(float(source["gain"]), float(row["gain"]), 2e-15)
                    and close(float(source["mu"]), float(row["mu"]), 2e-15),
                    f"Panel A targeted row mismatch: {row['id']}")
        require(row["status"] == "FINITE N=10 diagnostic" and row["N"] == "10",
                "Panel A finite boundary missing")

    # Panel B independent analytic and finite reconciliation.
    validation = read_json(paths["experimentValidation"])
    limit_lookup = {float(row["Lambda"]): row for row in validation["fixedLambdaKineticLimits"]}
    for lam in (0.25, 1.0, 4.0, 16.0):
        subset = [row for row in panels["B"] if close(float(row["Lambda"]), lam)]
        require(len(subset) == 3, f"Panel B triplet missing: Lambda={lam:g}")
        finite = next(row for row in subset if row["kind"] == "finite-kinetic-gain")
        limit = next(row for row in subset if row["kind"] == "triangular-limit-gain")
        envelope = next(row for row in subset if row["kind"] == "analytic-energy-envelope")
        source = limit_lookup[lam]
        expected_limit = triangular_gain(lam, 0.0, 0.75)
        expected_envelope = energy_envelope(1e-8, lam, 0.0, 0.75)
        require(close(float(finite["value"]), float(source["finiteGain"]), 2e-15),
                "Panel B finite gain differs from validation")
        require(close(float(limit["value"]), expected_limit, 3e-13),
                "Panel B triangular gain recomputation failed")
        require(close(float(envelope["value"]), expected_envelope, 5e-14),
                "Panel B energy envelope recomputation failed")
        require(abs(float(finite["value"]) - expected_limit) / expected_limit <= 8e-9,
                "Panel B finite/limit difference exceeds contract")
        require(float(finite["value"]) <= float(envelope["value"]),
                "Panel B finite gain exceeds analytic envelope")

    # Panel C exact analytic rows; no numerical source is accepted.
    c_kinds = {
        "elementary-shear-upper": lambda mu: 0.5,
        "carrier-block-upper": lambda mu: min(0.5,
            (math.sqrt(mu / (1.0 + mu))
             + math.sqrt(mu / (1.0 + mu) + 0.25)) / 2.0),
        "exact-low-gap-coefficient": lambda mu: 0.25,
    }
    for kind, formula in c_kinds.items():
        subset = [row for row in panels["C"] if row["kind"] == kind]
        require(len(subset) == 61 and len({row["mu"] for row in subset}) == 61,
                f"Panel C row count failed: {kind}")
        for row in subset:
            expected = formula(float(row["mu"]))
            require(close(float(row["value"]), expected, 5e-14),
                    f"Panel C formula mismatch: {row['id']}")

    # Panel D formula and observed-fit reconciliation.
    fit_lookup = {(float(row["p"]), row["norm"]): row
                  for row in validation["asymptoticFits"]}
    predictions = [row for row in panels["D"] if row["kind"] == "analytic-block-prediction"]
    observed = [row for row in panels["D"] if row["kind"] == "observed-finite-exponent"]
    require(len(predictions) == 122 and len(observed) == 8,
            "Panel D row counts changed")
    for row in predictions:
        expected = max(float(row["a"]) / 2.0 - float(row["p"]), 0.0)
        require(close(float(row["value"]), expected, 5e-14),
                f"Panel D prediction mismatch: {row['id']}")
    for row in observed:
        source = fit_lookup.get((float(row["p"]), row["norm"]))
        expected = max(float(row["a"]) / 2.0 - float(row["p"]), 0.0)
        require(source is not None
                and close(float(row["observedExponent"]),
                          float(source["observedDivergenceExponent"]), 2e-15),
                f"Panel D observed fit mismatch: {row['id']}")
        require(abs(float(row["observedExponent"]) - expected) <= 2e-5,
                f"Panel D observed fit misses prediction: {row['id']}")
        require(row["status"] == "FINITE N=10 diagnostic" and row["N"] == "10",
                "Panel D finite boundary missing")
    return {"rows": rows, **panels}


def validate_svg(stage: str) -> str:
    root = ET.parse(PACKAGE / "figure.svg").getroot()
    require(root.attrib.get("width") == "178mm"
            and root.attrib.get("height") == "150mm"
            and root.attrib.get("viewBox") == "0 0 1780 1500",
            "SVG physical dimensions changed")
    text = "\n".join(element.text or "" for element in root.iter()
                     if element.tag.endswith("text"))
    for value in REQUIRED_VISIBLE:
        require(value in text, f"required SVG text missing: {value}")
    lineage = ("FORMAL - CERTIFICATE COMMIT LINEAGE SEALED" if stage == "formal"
               else "DRAFT - FORMAL CERTIFICATE LINEAGE PENDING")
    require(lineage in text, "SVG lineage stage missing")
    for value in STALE_OR_FORBIDDEN:
        require(value not in text, f"stale or forbidden SVG token: {value}")
    raw = (PACKAGE / "figure.svg").read_text(encoding="utf-8").upper()
    colors = set(re.findall(r"#[0-9A-F]{6}", raw))
    allowed = {"#20262D", "#5D6670", "#8A939D", "#D9DEE3", "#FFFFFF",
               "#F5F7F8", "#285F8F", "#DDEAF4", "#A6781F", "#F3E8CB"}
    require(colors <= allowed and "#285F8F" in colors and "#A6781F" in colors,
            f"SVG palette differs from declared two-root palette: {sorted(colors - allowed)}")
    return text


def validate_pdf(stage: str) -> dict:
    reader = PdfReader(PACKAGE / "figure.pdf")
    require(len(reader.pages) == 1, "PDF must have one page")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) * 25.4 / 72.0
    height_mm = float(page.mediabox.height) * 25.4 / 72.0
    require(abs(width_mm - WIDTH_MM) <= 0.02 and abs(height_mm - HEIGHT_MM) <= 0.02,
            "PDF physical dimensions changed")
    require(len(list(page.images)) == 0, "PDF contains raster image XObjects")
    fonts = embedded_font_count(reader)
    require(fonts >= 2, f"PDF embeds fewer than two fonts: {fonts}")
    text = page.extract_text() or ""
    for value in REQUIRED_VISIBLE:
        require(value in text, f"required PDF text missing: {value}")
    lineage = ("FORMAL - CERTIFICATE COMMIT LINEAGE SEALED" if stage == "formal"
               else "DRAFT - FORMAL CERTIFICATE LINEAGE PENDING")
    require(lineage in text, "PDF lineage stage missing")
    return {"pages": 1, "widthMillimetres": width_mm,
            "heightMillimetres": height_mm, "embeddedFontCount": fonts,
            "rasterImageCount": 0}


def validate_pngs() -> dict:
    expected = [round(WIDTH_MM / 25.4 * PNG_DPI),
                round(HEIGHT_MM / 25.4 * PNG_DPI)]
    with Image.open(PACKAGE / "figure.png") as image:
        require([image.width, image.height] == expected,
                "PNG pixel dimensions changed")
        dpi = image.info.get("dpi", (0.0, 0.0))
        require(all(abs(float(value) - PNG_DPI) <= 0.1 for value in dpi),
                "PNG 600-dpi metadata missing")
        rgb = image.convert("RGB")
        corners = [rgb.getpixel((0, 0)), rgb.getpixel((rgb.width - 1, 0)),
                   rgb.getpixel((0, rgb.height - 1)),
                   rgb.getpixel((rgb.width - 1, rgb.height - 1))]
        require(corners == [(255, 255, 255)] * 4, "PNG outer corners are not white")
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(PACKAGE / name) as image:
            require(image.width > 2000 and image.height > 1700,
                    f"QA preview is too small: {name}")
            require(image.getbbox() is not None, f"QA preview is blank: {name}")
    return {"pixels": expected, "dpi": list(dpi), "cornersWhite": True}


def main() -> int:
    manifest = read_json(PACKAGE / "manifest.json")
    validation = read_json(PACKAGE / "validation.json")
    results = read_json(PACKAGE / "results.json")
    require(manifest.get("figureId") == FIGURE_ID and manifest.get("release") == RELEASE,
            "manifest identity mismatch")
    require(manifest.get("status") in ("draft", "formal"), "manifest stage invalid")
    stage = manifest["status"]
    require(validation.get("status") == "passed" and validation.get("stage") == stage
            and all(validation.get("checks", {}).values()),
            "producer validation is not fully passed")
    require(results.get("rowCount") == 364 and results.get("deterministic") is True,
            "results summary changed")
    validate_inventory(manifest)
    paths = validate_upstream(manifest)
    data = validate_data(paths)
    svg_text = validate_svg(stage)
    pdf = validate_pdf(stage)
    png = validate_pngs()

    if stage == "draft":
        require(manifest["lineage"]["formalBlocked"] is True
                and manifest["publication"]["allowed"] is False,
                "draft manifest incorrectly permits publication")
        require("DRAFT - FORMAL CERTIFICATE LINEAGE PENDING" in svg_text,
                "draft boundary missing")
    else:
        certificate = read_json(paths["certificate"])
        certificate_validation = read_json(paths["certificateValidation"])
        certificate_manifest = read_json(paths["certificateManifest"])
        require(manifest["lineage"]["formalBlocked"] is False
                and manifest["publication"]["allowed"] is True,
                "formal manifest does not permit publication")
        require(re.fullmatch(r"[0-9a-f]{40}", manifest["lineage"]["sourceCommit"])
                and re.fullmatch(r"[0-9a-f]{40}", manifest["lineage"]["certificateCommit"])
                and manifest["lineage"]["sourceCommit"] != manifest["lineage"]["certificateCommit"],
                "formal lineage commits are invalid")
        require(certificate.get("certificateStage") == "formal"
                and certificate.get("sourceCommit") == manifest["lineage"]["sourceCommit"],
                "formal figure is not bound to the formal certificate source commit")
        require(certificate_validation.get("stage") == "formal"
                and certificate_manifest.get("status") == "formal",
                "formal certificate validation or manifest stage is missing")
        require({row.get("commit") for row in certificate_manifest.get("sourceBindings", [])}
                == {manifest["lineage"]["sourceCommit"]},
                "formal certificate source bindings are not commit-sealed")

    output = {
        "schemaVersion": 1,
        "figureId": FIGURE_ID,
        "release": RELEASE,
        "status": "passed",
        "stage": stage,
        "rowCount": len(data["rows"]),
        "checks": {
            "inventoryAndHashes": True,
            "upstreamBindings": True,
            "rowCountsAndProvenance": True,
            "panelAThirteenPointSeries": True,
            "panelBTriangularAndEnvelopeRecompute": True,
            "panelCAnalyticFormulaRecompute": True,
            "panelDExponentRecompute": True,
            "visibleClaimBoundaries": True,
            "twoRootPalette": True,
            "pdfVectorAndFonts": True,
            "png600Dpi": True,
            "qaPreviewsPresent": True,
            "lineageStage": True,
        },
        "pdf": pdf,
        "png": png,
        "claimBoundary": {
            "finiteN10Only": True,
            "galerkinTailBound": False,
            "exactMaximumTransientGain": False,
            "nonlinearNavierStokes": False,
            "clayMillenniumProblemSolved": False,
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True) + "\n", end="")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise
