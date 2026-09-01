#!/usr/bin/env python3
"""Fail-closed validation and prepublication seal for the R0.73W figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import sys
from typing import Any
import xml.etree.ElementTree as ET


def bootstrap() -> None:
    for index, value in enumerate(sys.argv):
        if value == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if value.startswith("--deps="):
            sys.path.insert(0, str(Path(value.split("=", 1)[1]).resolve()))
            return


bootstrap()

from PIL import Image, ImageChops, ImageOps  # type: ignore  # noqa: E402
from pypdf import PdfReader  # type: ignore  # noqa: E402
import pypdfium2 as pdfium  # type: ignore  # noqa: E402

from plot import (  # type: ignore  # noqa: E402
    CSV_FIELDS,
    EXPECTED_PACKAGES,
    absorption_coefficient,
    absorption_stationary_point,
    canonical,
    generate_rows,
    load_json,
    package_versions,
    sha256,
    verify_inputs,
)


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FIGURE_ID = "fig-r073w-signed-production"
REPOSITORY_URL = "https://github.com/Kasifa/Kasifa.github.io.git"
SOURCE_FILES = {
    "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt",
    "config.json", "contract.json", "plot.py", "qa-protocol.md", "requirements.txt",
    "validate.py",
}
RAW_FILES = {
    "source-data.csv", "figure.pdf", "figure.svg", "figure.png",
    "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "environment.json",
    "results.json", "progress.ndjson", "resource-log.ndjson",
}
METADATA_FILES = {"validation.json", "manifest.json", "qa-report.md", "SHA256SUMS"}
PACKAGE_FILES = SOURCE_FILES | RAW_FILES | METADATA_FILES
BOUND_FILES = SOURCE_FILES | RAW_FILES
NUMERIC_TOLERANCE = 5e-15


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--confirm-visual-qa", action="store_true")
    parser.add_argument("--figure-source-commit", default="")
    parser.add_argument("--verify-only", action="store_true")
    return parser.parse_args()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def add(checks: list[dict[str, object]], check_id: str, passed: bool,
        **details: object) -> None:
    checks.append({"id": check_id, "pass": bool(passed), **details})
    require(bool(passed), "check failed: " + check_id)


def record(path: Path, schema: str | None = None,
           relative: str | None = None) -> dict[str, object]:
    result: dict[str, object] = {
        "bytes": path.stat().st_size,
        "path": relative if relative is not None else path.name,
        "sha256": sha256(path),
    }
    if schema:
        result["schema"] = schema
    return result


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open("r", encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        return list(reader.fieldnames or []), list(reader)


def read_ndjson(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        value = json.loads(line)
        require(isinstance(value, dict), "NDJSON row is not an object: " + path.name)
        rows.append(value)
    require(bool(rows), "empty NDJSON: " + path.name)
    return rows


def source_rows_close(actual: list[dict[str, str]],
                      expected: list[dict[str, str]]) -> bool:
    if len(actual) != len(expected):
        return False
    for actual_row, expected_row in zip(actual, expected, strict=True):
        if actual_row.keys() != expected_row.keys():
            return False
        for field in actual_row:
            if field not in {"x", "y"}:
                if actual_row[field] != expected_row[field]:
                    return False
                continue
            try:
                left = float(actual_row[field])
                right = float(expected_row[field])
            except ValueError:
                return False
            if not (math.isfinite(left) and math.isfinite(right)
                    and abs(left - right) <= NUMERIC_TOLERANCE):
                return False
    return True


def check_pdf_fonts(page: Any) -> dict[str, object]:
    resources = page.get("/Resources")
    if resources is None:
        return {"fontReferenceCount": 0, "embeddedFontCount": 0,
                "allReferencedFontsEmbedded": False, "fonts": []}
    resources = resources.get_object()
    fonts_object = resources.get("/Font", {})
    fonts_object = fonts_object.get_object() if hasattr(fonts_object, "get_object") else fonts_object
    rows: list[dict[str, object]] = []
    for resource_name, reference in fonts_object.items():
        font = reference.get_object()
        descriptors: list[Any] = []
        descriptor = font.get("/FontDescriptor")
        if descriptor is not None:
            descriptors.append(descriptor.get_object())
        descendants = font.get("/DescendantFonts")
        if descendants is not None:
            for descendant_ref in descendants:
                descendant = descendant_ref.get_object()
                child_descriptor = descendant.get("/FontDescriptor")
                if child_descriptor is not None:
                    descriptors.append(child_descriptor.get_object())
        embedded = any(any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3"))
                       for descriptor in descriptors)
        rows.append({
            "baseFont": str(font.get("/BaseFont", "")),
            "embedded": embedded,
            "resource": str(resource_name),
            "subtype": str(font.get("/Subtype", "")),
        })
    return {
        "allReferencedFontsEmbedded": bool(rows) and all(row["embedded"] for row in rows),
        "embeddedFontCount": sum(bool(row["embedded"]) for row in rows),
        "fontReferenceCount": len(rows),
        "fonts": rows,
    }


def render_pdf_qa(path: Path, maximum_width: int) -> Image.Image:
    document = pdfium.PdfDocument(str(path))
    require(len(document) == 1, "PDF raster source is not one page")
    page = document[0]
    width_points, _ = page.get_size()
    bitmap = page.render(scale=maximum_width / float(width_points))
    image = bitmap.to_pil().convert("RGB")
    page.close()
    document.close()
    return image


def inspect_outputs(config: dict[str, Any], checks: list[dict[str, object]]) -> dict[str, Any]:
    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    dpi = int(config["pngDpi"])
    # Matplotlib's Agg canvas truncates the nonintegral physical-size product.
    expected_pixels = [int(width_mm / 25.4 * dpi), int(height_mm / 25.4 * dpi)]

    with Image.open(HERE / "figure.png") as image_open:
        png_info = dict(image_open.info)
        image = image_open.convert("RGB")
        png_pixels = [image.width, image.height]
        reported_dpi = png_info.get("dpi", (0.0, 0.0))
        add(checks, "png-pixel-dimensions", png_pixels == expected_pixels,
            actual=png_pixels, expected=expected_pixels)
        add(checks, "png-600-dpi-metadata",
            len(reported_dpi) == 2
            and abs(float(reported_dpi[0]) - dpi) < 0.1
            and abs(float(reported_dpi[1]) - dpi) < 0.1,
            actual=list(reported_dpi), expected=dpi)
        qa_width = min(int(config["qaMaximumWidthPixels"]), image.width)
        qa_height = round(image.height * qa_width / image.width)
        expected_final = image.resize((qa_width, qa_height), Image.Resampling.LANCZOS)
    with Image.open(HERE / "qa-final-size.png") as stored_open:
        stored_final = stored_open.convert("RGB")
    add(checks, "qa-final-size-exact",
        stored_final.size == expected_final.size
        and ImageChops.difference(stored_final, expected_final).getbbox() is None,
        pixels=list(stored_final.size))
    expected_gray = ImageOps.grayscale(expected_final).convert("RGB")
    with Image.open(HERE / "qa-grayscale.png") as stored_open:
        stored_gray = stored_open.convert("RGB")
    add(checks, "qa-grayscale-exact",
        stored_gray.size == expected_gray.size
        and ImageChops.difference(stored_gray, expected_gray).getbbox() is None,
        pixels=list(stored_gray.size))

    pdf_reader = PdfReader(str(HERE / "figure.pdf"))
    add(checks, "pdf-one-page", len(pdf_reader.pages) == 1, pages=len(pdf_reader.pages))
    page = pdf_reader.pages[0]
    media_width = float(page.mediabox.width)
    media_height = float(page.mediabox.height)
    expected_points = [width_mm / 25.4 * 72.0, height_mm / 25.4 * 72.0]
    add(checks, "pdf-mediabox",
        abs(media_width - expected_points[0]) < 0.02
        and abs(media_height - expected_points[1]) < 0.02,
        actualPoints=[media_width, media_height], expectedPoints=expected_points)
    font_report = check_pdf_fonts(page)
    add(checks, "pdf-font-references", font_report["fontReferenceCount"] >= 1,
        fontReferenceCount=font_report["fontReferenceCount"])
    add(checks, "pdf-fonts-embedded", bool(font_report["allReferencedFontsEmbedded"]),
        embeddedFontCount=font_report["embeddedFontCount"],
        fontReferenceCount=font_report["fontReferenceCount"])

    fresh_pdf = render_pdf_qa(HERE / "figure.pdf", int(config["qaMaximumWidthPixels"]))
    with Image.open(HERE / "qa-pdf.png") as stored_open:
        stored_pdf = stored_open.convert("RGB")
    add(checks, "qa-pdf-independent-raster-exact",
        stored_pdf.size == fresh_pdf.size
        and ImageChops.difference(stored_pdf, fresh_pdf).getbbox() is None,
        pixels=list(stored_pdf.size))

    svg_path = HERE / "figure.svg"
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_root = ET.fromstring(svg_text)
    view_box = [float(value) for value in svg_root.attrib["viewBox"].split()]
    add(checks, "svg-viewbox",
        len(view_box) == 4 and abs(view_box[2] - expected_points[0]) < 0.02
        and abs(view_box[3] - expected_points[1]) < 0.02,
        actual=view_box, expected=[0.0, 0.0, *expected_points])
    remote_links = []
    for element in svg_root.iter():
        for key, value in element.attrib.items():
            if key.endswith("href") and re.match(r"https?://", value):
                remote_links.append(value)
    add(checks, "svg-no-remote-links", not remote_links, remoteLinks=remote_links)
    blossom_ids = ["research-blossom-center"] + [f"research-blossom-petal-{i}" for i in range(1, 6)]
    add(checks, "locked-research-blossom",
        all(f'id="{token}"' in svg_text for token in blossom_ids),
        ids=blossom_ids, placement=[0.966, 0.957])
    add(checks, "visible-claim-boundary-tokens",
        all(token in svg_text for token in ("NOT DATA", "NOT CLAY", "R0.73W")),
        tokens=["NOT DATA", "NOT CLAY", "R0.73W"])

    palette_values = {value.lower() for value in config["palette"].values()}
    colors = {value.lower() for value in re.findall(r"#[0-9a-fA-F]{6}", svg_text)}
    unexpected_chromatic = []
    for color in sorted(colors - palette_values):
        red, green, blue = int(color[1:3], 16), int(color[3:5], 16), int(color[5:7], 16)
        if not (red == green == blue):
            unexpected_chromatic.append(color)
    add(checks, "two-root-palette", not unexpected_chromatic
        and config["palette"]["blue"].lower() in colors
        and config["palette"]["orange"].lower() in colors,
        colors=sorted(colors), unexpectedChromatic=unexpected_chromatic)

    return {
        "dimensions": {
            "millimetres": [width_mm, height_mm],
            "pdfPoints": [media_width, media_height],
            "pngPixels": png_pixels,
            "pngReportedDpi": list(reported_dpi),
            "qaFinalSizePixels": list(stored_final.size),
            "qaPdfPixels": list(stored_pdf.size),
        },
        "pdf": {"pages": len(pdf_reader.pages), **font_report},
        "svg": {"colors": sorted(colors), "researchBlossomIds": blossom_ids,
                "viewBox": view_box},
    }


def core_validation(visual_confirmed: bool) -> tuple[list[dict[str, object]], dict[str, Any]]:
    checks: list[dict[str, object]] = []
    entries = list(HERE.iterdir())
    actual_files = {path.name for path in entries if path.is_file()}
    add(checks, "source-inventory", len(SOURCE_FILES) == 10,
        sourceFiles=sorted(SOURCE_FILES))
    add(checks, "raw-inventory", len(RAW_FILES) == 11, rawFiles=sorted(RAW_FILES))
    add(checks, "no-unexpected-package-files", actual_files <= PACKAGE_FILES,
        unexpected=sorted(actual_files - PACKAGE_FILES))
    add(checks, "no-subdirectories-or-special-entries", all(path.is_file() for path in entries))
    add(checks, "source-and-raw-files-present", (SOURCE_FILES | RAW_FILES) <= actual_files,
        missing=sorted((SOURCE_FILES | RAW_FILES) - actual_files))

    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")
    add(checks, "figure-id", config.get("figureId") == FIGURE_ID
        and contract.get("figureId") == FIGURE_ID)
    add(checks, "dependency-versions", package_versions() == EXPECTED_PACKAGES,
        actual=package_versions(), expected=EXPECTED_PACKAGES)
    primary, independent, rank_three = verify_inputs(contract)
    add(checks, "certificate-two-path-common-core",
        primary["commonCore"] == independent["commonCore"],
        commonCoreSha256=contract["certificate"]["commonCoreSha256"])
    add(checks, "certificate-final-commit-bound",
        contract["certificate"]["sealState"] == "SEALED_COMMIT_BOUND",
        sourceCommit=contract["certificate"]["sourceCommit"],
        certificatePackageCommit=contract["certificate"]["certificatePackageCommit"])
    add(checks, "rank-three-witness", rank_three["field"]["frequencyRank"] == 3
        and rank_three["field"]["divergenceFree"] is True)
    add(checks, "production-certificate-formula",
        rank_three["signedProduction"]["factored"] == "1/4*q^2*(1-q^2)")
    add(checks, "production-parity-certificate",
        rank_three["parity"]["productionOdd"] is True
        and rank_three["parity"]["stressEven"] is True
        and rank_three["parity"]["gradientDefectEven"] is True)
    add(checks, "absorption-certificate-formula",
        rank_three["absorptionRatio"]["cancelledFormula"]
        == "A*q^2/(2*nu*(13+12*q^2+10*q^4+4*q^6))"
        and rank_three["absorptionRatio"]["qToOneCoefficient"] == "1/(78*nu)")

    fields, rows = read_csv(HERE / "source-data.csv")
    expected_rows = generate_rows(config)
    add(checks, "source-data-schema", fields == CSV_FIELDS, actual=fields)
    add(checks, "source-data-row-count", len(rows) == len(expected_rows), rows=len(rows))
    add(checks, "source-data-reconstruction", source_rows_close(rows, expected_rows),
        numericTolerance=NUMERIC_TOLERANCE)
    panel_counts = {panel: sum(row["panel"] == panel for row in rows)
                    for panel in ("A", "B", "C", "D")}
    add(checks, "source-data-panel-inventory",
        panel_counts == results["panelRowCounts"], panelCounts=panel_counts)

    endpoints = [row for row in rows if row["panel"] == "A"
                 and row["series"] == "payment-endpoint"]
    nu = float(config["panelA"]["nuDrawing"])
    characteristic_values = [float(row["y"]) + nu * float(row["x"]) for row in endpoints]
    add(checks, "panel-a-one-characteristic", len(endpoints) == 2
        and max(characteristic_values) - min(characteristic_values) < 1e-14,
        characteristicValues=characteristic_values)
    add(checks, "panel-a-payment-sign",
        all("E_initial-E_final" in row["formula"] for row in endpoints)
        and all("periodic or boundary-decaying" in row["normalization"] for row in endpoints))

    b_rows = [row for row in rows if row["panel"] == "B"]
    panel_b_values_pass = all(abs(float(row["y"]) - float(row["x"]) **
                                  (-0.25 if row["series"] == "fixed-scale-upper" else 0.75))
                              <= NUMERIC_TOLERANCE for row in b_rows)
    add(checks, "panel-b-closed-shapes", panel_b_values_pass)
    add(checks, "panel-b-not-data-boundary", all(
        row["evidence_class"] == "analytic-upper-bound-shape-not-data"
        and "not observations" in row["note"] for row in b_rows))

    c_plus = [row for row in rows if row["panel"] == "C" and row["series"] == "plus-R"]
    c_minus = [row for row in rows if row["panel"] == "C" and row["series"] == "minus-R"]
    add(checks, "panel-c-parity-pair", len(c_plus) == len(c_minus)
        and all(left["x"] == right["x"]
                and abs(float(left["y"]) + float(right["y"])) <= NUMERIC_TOLERANCE
                for left, right in zip(c_plus, c_minus, strict=True)))
    extrema = [row for row in rows if row["panel"] == "C"
               and row["series"] == "exact-extremum"]
    add(checks, "panel-c-exact-extrema", len(extrema) == 2
        and all(abs(float(row["x"]) - 0.5 * math.log(2.0)) <= NUMERIC_TOLERANCE
                for row in extrema)
        and sorted(round(float(row["y"]), 12) for row in extrema)
        == [-0.0625, 0.0625])

    d_rows = [row for row in rows if row["panel"] == "D"
              and row["series"] == "absorption-coefficient"]
    add(checks, "panel-d-closed-form", all(
        abs(float(row["y"]) - absorption_coefficient(float(row["x"])))
        <= NUMERIC_TOLERANCE for row in d_rows))
    d_landmarks = [row for row in rows if row["panel"] == "D"
                   and row["series"] == "exact-landmark"]
    endpoint = next(row for row in d_landmarks if row["record"] == "zero-scale-limit")
    add(checks, "panel-d-one-over-78", float(endpoint["x"]) == 0.0
        and abs(float(endpoint["y"]) - 1.0 / 78.0) <= NUMERIC_TOLERANCE)
    stationary_s, stationary_z, stationary_y = absorption_stationary_point()
    add(checks, "panel-d-interior-maximum",
        0.0 < stationary_s < float(config["panelD"]["sMaximum"])
        and abs(8.0 * stationary_z ** 3 + 10.0 * stationary_z ** 2 - 13.0) < 2e-14
        and stationary_y > 1.0 / 78.0,
        s=stationary_s, z=stationary_z, coefficient=stationary_y)

    add(checks, "renderer-artist-bounds", results["render"]["artistBoundsPass"] is True
        and results["render"]["artistBoundsFailures"] == [])
    output_report = inspect_outputs(config, checks)

    progress = read_ndjson(HERE / "progress.ndjson")
    resource_rows = read_ndjson(HERE / "resource-log.ndjson")
    add(checks, "progress-log", progress[0]["event"] == "start"
        and any(row["event"] == "render-complete" for row in progress),
        events=[row["event"] for row in progress])
    add(checks, "resource-log", len(resource_rows) == 1
        and resource_rows[0]["processes"] == 1
        and resource_rows[0]["threadsPerProcess"] == 1)
    add(checks, "environment-scope",
        environment["execution"]["dgxUsed"] is False
        and environment["execution"]["gpu"] == "not used"
        and environment["execution"]["network"] == "not used"
        and environment["execution"]["ordinaryTranslationPath"] == "LOCAL_DIRECT_NO_DGX")
    add(checks, "claim-boundary-flags",
        contract["claimBoundary"]["navierStokesSimulation"] is False
        and contract["claimBoundary"]["fittedScalingLaw"] is False
        and contract["claimBoundary"]["globalRegularityEstablished"] is False
        and contract["claimBoundary"]["clayProblemSolved"] is False)
    add(checks, "visual-qa-confirmed", visual_confirmed,
        assets=["figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"],
        inspectedFor=["clipping", "labels", "legends", "scales", "blossom", "grayscale"])
    return checks, {
        "config": config,
        "contract": contract,
        "environment": environment,
        "output": output_report,
        "progress": progress,
        "results": results,
    }


def git_text(args: list[str]) -> str:
    completed = subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                               text=True, check=False)
    require(completed.returncode == 0, "git command failed: " + " ".join(args))
    return completed.stdout.strip()


def figure_source_bindings(commit: str) -> list[dict[str, object]]:
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            "figure source commit must be full lowercase 40-hex")
    exists = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=ROOT,
        capture_output=True, check=False,
    )
    require(exists.returncode == 0, "figure source commit does not resolve")
    bindings: list[dict[str, object]] = []
    scoped_paths: list[str] = []
    for name in sorted(BOUND_FILES):
        path = HERE / name
        repository_path = path.relative_to(ROOT).as_posix()
        payload = path.read_bytes()
        committed = subprocess.run(
            ["git", "cat-file", "blob", commit + ":" + repository_path],
            cwd=ROOT, capture_output=True, check=False,
        )
        require(committed.returncode == 0,
                "figure source blob absent from commit: " + repository_path)
        require(committed.stdout == payload,
                "figure source blob differs from current bytes: " + repository_path)
        object_id = git_text(["rev-parse", commit + ":" + repository_path])
        require(re.fullmatch(r"[0-9a-f]{40,64}", object_id) is not None,
                "invalid figure source blob object id: " + repository_path)
        bindings.append({
            "bytes": len(payload),
            "gitBlobObjectId": object_id,
            "path": repository_path,
            "sha256": hashlib.sha256(payload).hexdigest(),
            "sourceClass": "immutable-figure-source-or-raw-artifact",
        })
        scoped_paths.append(repository_path)
    require(len(bindings) == 21, "figure source binding inventory drift")
    status = subprocess.run(
        ["git", "status", "--porcelain=v1", "--untracked-files=all", "--",
         *scoped_paths], cwd=ROOT, capture_output=True, check=False,
    )
    require(status.returncode == 0, "figure source scoped git status failed")
    require(not status.stdout, "figure source/raw bound scope is dirty")
    return bindings


def write_seal(
    checks: list[dict[str, object]], diagnostics: dict[str, Any],
    figure_source_commit: str | None = None,
    figure_bindings: list[dict[str, object]] | None = None,
) -> None:
    final_source_seal = figure_source_commit is not None
    figure_bindings = figure_bindings or []
    seal_state = ("formal-figure-source-seal" if final_source_seal
                  else "HASH_BOUND_PREPUBLICATION_ARTIFACT")
    report_status = ("FORMAL FIGURE-SOURCE SEAL" if final_source_seal
                     else "HASH-BOUND PREPUBLICATION ARTIFACT")
    created = utc_now()
    validation = {
        "schemaVersion": "r073w-signed-production-validation-v1",
        "figureId": FIGURE_ID,
        "status": "PASS",
        "sealState": seal_state,
        "figureSourceCommit": figure_source_commit,
        "figureSourceCommitAssigned": final_source_seal,
        "createdUtc": created,
        "passed": len(checks),
        "required": len(checks),
        "checksPassed": len(checks),
        "checksRequired": len(checks),
        "visualQaConfirmed": True,
        "checks": checks,
        "pdfInspection": diagnostics["output"]["pdf"],
        "dimensions": diagnostics["output"]["dimensions"],
        "svgInspection": diagnostics["output"]["svg"],
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")

    pdf = diagnostics["output"]["pdf"]
    dimensions = diagnostics["output"]["dimensions"]
    report = f"""# R0.73W formal-figure QA report

**Status:** PASS — {report_status}

**Checks:** {len(checks)}/{len(checks)}

The audited heat-plane identity, the two analytic energy-class envelopes, and
the sealed two-path rank-three certificate all passed fail-closed source
verification.  `source-data.csv` was reconstructed in full; every formula and
categorical field passed and all renderer coordinates were within
`{NUMERIC_TOLERANCE:.0e}` of their deterministic closed-form reconstruction.

SVG, PDF, and 600 dpi PNG integrity passed at
{dimensions['millimetres'][0]:.0f} mm by {dimensions['millimetres'][1]:.0f} mm.
The PDF has {pdf['pages']} page, MediaBox
{dimensions['pdfPoints'][0]:.6f} by {dimensions['pdfPoints'][1]:.6f} pt,
{pdf['fontReferenceCount']} referenced font resource(s), and
{pdf['embeddedFontCount']} embedded font resource(s); every referenced font
passed the embedded-font descriptor check.  The independently regenerated PDF
raster is {dimensions['qaPdfPixels'][0]} by {dimensions['qaPdfPixels'][1]}
pixels and is pixel-identical to `qa-pdf.png`.

Final-size, grayscale, and PDF rasters were inspected for clipped or colliding
panel titles, subtitles, equations, curve labels, annotations, ticks, legends,
axis labels, and the footer.  No clipping was observed.  Filled/open markers
and solid/dashed strokes preserve all comparisons in grayscale.  The locked
five-petal research blossom is present at the established data-free top-right
token and does not overlap the R0.73W header.

Panel B is visibly and structurally labelled as analytic upper-bound shapes,
not data.  Panel D retains the small interior maximum and separately marks the
exact `1/78` zero-scale endpoint.  No DNS, fit, generic-turbulence, singularity,
regularity, global-regularity, or Clay claim is made.

The finite certificate is commit-bound (`{diagnostics['contract']['certificate']['sourceCommit']}`
and `{diagnostics['contract']['certificate']['certificatePackageCommit']}`).
{"The 21 figure source/raw artifacts are byte-identical to immutable commit `" + figure_source_commit + "`, and their scoped Git status is clean; this is the formal figure-source seal." if final_source_seal else "The new figure sources/raw artifacts are not yet commit-bound, so this remains truthfully a hash-bound prepublication artifact rather than an immutable figure-source seal."}
`ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX`; `dgxUsed=false`; `NOT CLAY`.
"""
    (HERE / "qa-report.md").write_text(report, encoding="utf-8")

    environment = diagnostics["environment"]
    contract = diagnostics["contract"]
    progress = diagnostics["progress"]
    wall_time = max(float(row.get("elapsedSeconds", 0.0)) for row in progress)
    current_commit = git_text(["rev-parse", "HEAD"])
    scoped_status = git_text(["status", "--porcelain=v1", "--untracked-files=all", "--",
                              str(HERE.relative_to(ROOT))])
    manifest_data_names = [
        "source-data.csv", "results.json", "environment.json", "progress.ndjson",
        "resource-log.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
        "validation.json", "qa-report.md",
    ]
    source_data = []
    for entry in contract["analyticSources"]:
        source_data.append(record(ROOT / entry["path"],
                                  "hash-bound-audited-analytic-source", entry["path"]))
    certificate = contract["certificate"]
    for relative, schema in (
        (certificate["primaryPath"], "sealed-primary-exact-certificate"),
        (certificate["independentPath"], "sealed-independent-exact-certificate"),
        (certificate["manifestPath"], "sealed-commit-bound-certificate-manifest"),
    ):
        source_data.append(record(ROOT / relative, schema, relative))
    if final_source_seal:
        git_block = {
            "repository": REPOSITORY_URL,
            "sourceCommit": figure_source_commit,
            "certificateCommit": certificate["certificatePackageCommit"],
            "certificateSourceCommit": certificate["sourceCommit"],
            "dirtyAtCertifiedRun": False,
            "dirtyScope": [item["path"] for item in figure_bindings],
            "figureSourceCommit": figure_source_commit,
            "sourceCommitMeaning": "immutable commit containing byte-identical figure source and raw artifacts",
        }
    else:
        git_block = {
            "repository": REPOSITORY_URL,
            "commit": current_commit,
            "dirty": True,
            "scopedStatus": scoped_status,
            "certificateSourceCommit": certificate["sourceCommit"],
            "certificatePackageCommit": certificate["certificatePackageCommit"],
        }
    manifest = {
        "schemaVersion": "research-figure-manifest-v1",
        "figureSchemaVersion": "r073w-signed-production-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73W",
        "status": "formal" if final_source_seal else "draft",
        "publicationStatus": "staged" if final_source_seal else "prepublication",
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedClaim"],
        "createdAt": created,
        "git": git_block,
        "computation": {
            "kind": "exact-formula-audit",
            "configuration": "config.json",
            "precision": "exact certificate formulas; IEEE-754 binary64 renderer coordinates",
            "solver": "none",
            "formalCommand": "python plot.py --render-preseal; python validate.py --confirm-visual-qa; python validate.py --figure-source-commit <full-40-hex> --confirm-visual-qa; python validate.py --verify-only",
            "wallTimeSeconds": wall_time,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": ["elapsedSeconds", "event", "maximumResidentSetSizeRaw"],
            },
        },
        "compute": {
            "host": environment["execution"]["host"],
            "operatingSystem": environment["execution"]["operatingSystem"],
            "cpu": environment["execution"]["cpu"],
            "memoryGiB": environment["execution"]["memoryGiB"],
            "processes": environment["execution"]["processes"],
            "threadsPerProcess": environment["execution"]["threadsPerProcess"],
            "gpu": "not used",
            "network": "not used",
            "dgxUsed": False,
            "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        },
        "environment": {
            "python": environment["execution"]["python"],
            "packagesLock": "requirements.txt",
            "packages": environment["packages"],
        },
        "data": [record(HERE / name, "r073w-figure-package-file-v1")
                 for name in manifest_data_names],
        "sourceData": source_data,
        "figure": {
            "widthMillimetres": diagnostics["config"]["widthMillimetres"],
            "heightMillimetres": diagnostics["config"]["heightMillimetres"],
            "outputs": [
                record(HERE / "figure.svg", "svg-journal-master"),
                record(HERE / "figure.pdf", "one-page-pdf-journal-master"),
                {**record(HERE / "figure.png", "png-journal-master"), "dpi": 600},
            ],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "validationChecks": len(checks),
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "pdfRasterInspected": True,
            "pdfFontsEmbedded": True,
            "researchBlossomInspected": True,
            "artistBoundsGuardPassed": True,
            "report": "qa-report.md",
        },
        "seal": {
            "state": seal_state,
            "certificateCommitBound": True,
            "certificateSourceCommit": certificate["sourceCommit"],
            "certificatePackageCommit": certificate["certificatePackageCommit"],
            "figureSourceBindings": figure_bindings,
            "figureSourceCommit": figure_source_commit,
            "figureSourceCommitAssigned": final_source_seal,
            "requiresFigureSourceCommitFinalReseal": not final_source_seal,
            "requiresParentFigureSourceCommitFinalReseal": not final_source_seal,
        },
        "claimBoundary": contract["claimBoundary"],
        "ordinaryTranslationPath": "LOCAL_DIRECT_NO_DGX",
        "dgxUsed": False,
        "notClay": True,
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")

    sum_files = sorted(path for path in HERE.iterdir()
                       if path.is_file() and path.name != "SHA256SUMS")
    with (HERE / "SHA256SUMS").open("w", encoding="utf-8") as stream:
        for path in sum_files:
            stream.write(f"{sha256(path)}  {path.name}\n")


def verify_seal(
    expected_checks: list[dict[str, object]],
    expected_figure_bindings: list[dict[str, object]] | None = None,
) -> dict[str, object]:
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    expected_figure_bindings = expected_figure_bindings or []
    require(validation.get("status") == "PASS"
            and validation.get("visualQaConfirmed") is True,
            "stored validation is not a visually confirmed pass")
    require(manifest.get("schemaVersion") == "research-figure-manifest-v1"
            and manifest.get("figureSchemaVersion")
            == "r073w-signed-production-manifest-v1"
            and manifest.get("figureId") == FIGURE_ID
            and manifest.get("release") == "R0.73W",
            "manifest schema or identity drift")
    require(validation.get("checksPassed") == len(expected_checks)
            and validation.get("checksRequired") == len(expected_checks)
            and validation.get("passed") == len(expected_checks)
            and validation.get("required") == len(expected_checks)
            and validation.get("checks") == expected_checks,
            "validation check reconstruction drift")
    require(manifest.get("qa", {}).get("validationChecks")
            == validation.get("required"),
            "manifest QA validation-count drift")
    seal = manifest.get("seal", {})
    assigned = seal.get("figureSourceCommitAssigned") is True
    expected_state = ("formal-figure-source-seal" if assigned
                      else "HASH_BOUND_PREPUBLICATION_ARTIFACT")
    require(seal.get("state") == expected_state, "manifest seal state drift")
    require(validation.get("sealState") == expected_state,
            "validation seal state drift")
    if assigned:
        figure_source_commit = seal.get("figureSourceCommit")
        require(isinstance(figure_source_commit, str),
                "assigned figure source commit is not a string")
        require(manifest.get("status") == "formal"
                and manifest.get("publicationStatus") == "staged",
                "formal manifest publication state drift")
        require(seal.get("requiresParentFigureSourceCommitFinalReseal") is False
                and seal.get("requiresFigureSourceCommitFinalReseal") is False,
                "formal reseal boundary drift")
        require(seal.get("figureSourceBindings") == expected_figure_bindings,
                "figure source bindings drift")
        require(manifest.get("git", {}).get("sourceCommit") == figure_source_commit
                and manifest.get("git", {}).get("dirtyAtCertifiedRun") is False,
                "formal git source boundary drift")
    else:
        require(manifest.get("status") == "draft"
                and manifest.get("publicationStatus") == "prepublication",
                "prepublication manifest state drift")
        require(seal.get("requiresParentFigureSourceCommitFinalReseal") is True
                and seal.get("requiresFigureSourceCommitFinalReseal") is True,
                "prepublication reseal boundary drift")
    hash_records = list(manifest.get("data", []))
    hash_records.extend(manifest.get("figure", {}).get("outputs", []))
    for item in hash_records:
        path = HERE / item["path"]
        require(path.is_file() and sha256(path) == item["sha256"],
                "manifest-bound file drift: " + item["path"])
    for item in manifest.get("sourceData", []):
        path = ROOT / item["path"]
        require(path.is_file() and sha256(path) == item["sha256"],
                "manifest source-data drift: " + item["path"])

    expected_names = sorted(path.name for path in HERE.iterdir()
                            if path.is_file() and path.name != "SHA256SUMS")
    parsed: dict[str, str] = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        require(name not in parsed, "duplicate SHA256SUMS entry: " + name)
        parsed[name] = digest
    require(sorted(parsed) == expected_names, "SHA256SUMS inventory drift")
    for name, expected in parsed.items():
        require(sha256(HERE / name) == expected, "SHA256SUMS mismatch: " + name)
    return {
        "figureSourceBindings": len(expected_figure_bindings),
        "figureSourceCommitAssigned": assigned,
        "manifestHashRecords": len(hash_records),
        "sha256SumsEntries": len(parsed),
        "sourceDataBindings": len(manifest.get("sourceData", [])),
    }


def main() -> int:
    args = parse_args()
    require(not (args.verify_only and args.figure_source_commit),
            "--verify-only reads the stored seal; do not pass --figure-source-commit")
    stored_visual = False
    if args.verify_only and (HERE / "validation.json").is_file():
        stored_visual = load_json(HERE / "validation.json").get("visualQaConfirmed") is True
    checks, diagnostics = core_validation(args.confirm_visual_qa or stored_visual)
    if args.verify_only:
        stored_manifest = load_json(HERE / "manifest.json")
        stored_seal = stored_manifest.get("seal", {})
        stored_bindings: list[dict[str, object]] = []
        if stored_seal.get("figureSourceCommitAssigned") is True:
            stored_commit = stored_seal.get("figureSourceCommit")
            require(isinstance(stored_commit, str),
                    "stored figure source commit is not a string")
            stored_bindings = figure_source_bindings(stored_commit)
            add(checks, "figure-source-commit-bound", len(stored_bindings) == 21,
                commit=stored_commit, boundFiles=len(stored_bindings))
            add(checks, "figure-source-blob-byte-identity", True,
                blobObjectIds=[item["gitBlobObjectId"] for item in stored_bindings])
            add(checks, "figure-source-bound-scope-clean", True,
                paths=[item["path"] for item in stored_bindings])
        seal_report = verify_seal(checks, stored_bindings)
        print(json.dumps({
            "checks": len(checks),
            "figureId": FIGURE_ID,
            "mode": "verify-only",
            "seal": seal_report,
            "status": "PASS",
        }, indent=2, sort_keys=True))
        return 0
    require(args.confirm_visual_qa,
            "write-seal requires --confirm-visual-qa after inspecting all QA rasters")
    figure_source_commit = args.figure_source_commit or None
    bindings: list[dict[str, object]] = []
    if figure_source_commit is not None:
        bindings = figure_source_bindings(figure_source_commit)
        add(checks, "figure-source-commit-bound", len(bindings) == 21,
            commit=figure_source_commit, boundFiles=len(bindings))
        add(checks, "figure-source-blob-byte-identity", True,
            blobObjectIds=[item["gitBlobObjectId"] for item in bindings])
        add(checks, "figure-source-bound-scope-clean", True,
            paths=[item["path"] for item in bindings])
    write_seal(checks, diagnostics, figure_source_commit, bindings)
    seal_report = verify_seal(checks, bindings)
    print(json.dumps({
        "checks": len(checks),
        "figureSourceCommit": figure_source_commit,
        "figureId": FIGURE_ID,
        "mode": "write-seal",
        "pdf": diagnostics["output"]["pdf"],
        "seal": seal_report,
        "status": "PASS",
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
