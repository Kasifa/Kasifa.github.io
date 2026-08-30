#!/usr/bin/env python3
"""Fail-closed validation for the formal R0.73J journal figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, getcontext
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import socket
import subprocess
import sys


def _bootstrap_dependencies() -> None:
    for index, argument in enumerate(sys.argv):
        if argument == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if argument.startswith("--deps="):
            sys.path.insert(0, str(Path(argument.split("=", 1)[1]).resolve()))
            return


_bootstrap_dependencies()

from PIL import Image, ImageChops, __version__ as pillow_version
from pypdf import PdfReader, __version__ as pypdf_version


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
FIGURE_ID = "fig-r073j-continuum-branch-certificate"
CONTOUR_PATH = REPOSITORY / "experiments/r073j/contour_certificate.json"
OVERLAP_PATH = REPOSITORY / "experiments/r073j/overlap_certificate.json"
CONTOUR_CONFIG_PATH = REPOSITORY / "experiments/r073j/config.json"
OVERLAP_CONFIG_PATH = REPOSITORY / "experiments/r073j/overlap_config.json"
SOURCE_FILES = {
    "README.md", "caption.md", "command.txt", "config.json", "contract.json",
    "plot.py", "qa-protocol.md", "requirements.txt", "validate.py",
}
GENERATED_FILES = {
    "source-data.csv", "figure.pdf", "figure.svg", "figure.png",
    "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    "environment.json", "results.json", "validation.json", "manifest.json",
    "progress.ndjson", "resource-log.ndjson", "qa-report.md", "SHA256SUMS",
}
BALL_RE = re.compile(
    r"^\[?\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    r"(?:\s*\+/-\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?))?"
    r"\s*\]?$"
)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    if not path.is_file() or path.is_symlink():
        raise RuntimeError(f"required regular file is absent: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def ball_parts(text: str) -> tuple[Decimal, Decimal, Decimal]:
    match = BALL_RE.fullmatch(text.strip())
    if not match:
        raise RuntimeError(f"unsupported interval string: {text!r}")
    midpoint = Decimal(match.group(1))
    radius = Decimal(match.group(2) or "0")
    require(radius >= 0, f"negative interval radius: {text}")
    return midpoint, radius, midpoint - radius


def file_record(path: Path) -> dict[str, object]:
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def input_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def verify_inventory_before_qa() -> None:
    required = SOURCE_FILES | {
        "source-data.csv", "figure.pdf", "figure.svg", "figure.png",
        "environment.json", "results.json", "progress.ndjson",
        "resource-log.ndjson", "qa-report.md",
    }
    for name in sorted(required):
        path = HERE / name
        require(path.is_file() and not path.is_symlink(),
                f"required regular package file is absent: {name}")


def verify_contract(config: dict, contract: dict, results: dict) -> None:
    require(
        config.get("figureId") == contract.get("figureId") == results.get("figureId")
        == FIGURE_ID,
        "figure identity drift",
    )
    require(config.get("widthMillimetres") == 178.0, "width contract drift")
    require(config.get("heightMillimetres") == 104.0, "height contract drift")
    require(config.get("pngDpi") == 600, "PNG resolution contract drift")
    require(contract.get("release") == "R0.73J", "release identity drift")
    require(contract.get("evidenceClass") == "validated-continuum-interval-certificate",
            "evidence-class drift")
    policy = contract.get("palettePolicy", {})
    require(policy.get("policy") == "hard two-root cap", "palette policy drift")
    require(policy.get("chromaticRoots") == [
        config["palette"]["blue"], config["palette"]["orange"]
    ], "chromatic roots do not match the frozen palette")
    require(contract.get("researchBlossom", {}).get("lockedAnchor") ==
            "top-right-header", "research blossom anchor drift")
    require(contract.get("researchBlossom", {}).get("petalCount") == 5,
            "research blossom petal count drift")
    boundary = contract.get("claimBoundary", {})
    for key in (
        "formalValidatedCertificateFigure",
        "continuumSpectralBranchCountCertified",
        "kineticOverlapThresholdCertified",
    ):
        require(boundary.get(key) is True, "missing supported boundary: " + key)
    for key in (
        "viscousBranchCertified",
        "adiabaticRemainderCertified",
        "transverseThreeDimensionalClosureCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    ):
        require(boundary.get(key) is False, "escaped claim boundary: " + key)
    require(results.get("claimBoundary") == boundary, "result boundary drift")


def verify_input_bindings(results: dict) -> tuple[dict, dict]:
    expected_paths = (
        CONTOUR_PATH, OVERLAP_PATH, CONTOUR_CONFIG_PATH, OVERLAP_CONFIG_PATH
    )
    expected = [input_record(path) for path in expected_paths]
    require(results.get("inputBindings") == expected, "input SHA-256 binding drift")
    contour = load_json(CONTOUR_PATH)
    overlap = load_json(OVERLAP_PATH)
    require(contour.get("status") == "passed", "contour certificate is not passed")
    require(overlap.get("status") == "passed", "overlap certificate is not passed")
    require(contour.get("configuration") == load_json(CONTOUR_CONFIG_PATH),
            "contour certificate/configuration mismatch")
    require(overlap.get("configuration") == load_json(OVERLAP_CONFIG_PATH),
            "overlap certificate/configuration mismatch")
    return contour, overlap


def verify_source_data(contour: dict, overlap: dict, results: dict) -> dict[str, object]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    require(len(rows) == 192, "source-data.csv must contain 192 rows")
    contour_rows = [row for row in rows if row.get("record_type") == "contour_panel"]
    overlap_rows = [row for row in rows if row.get("record_type") == "overlap_cell"]
    require(len(contour_rows) == 64, "source data does not contain 64 contour rows")
    require(len(overlap_rows) == 128, "source data does not contain 128 overlap rows")
    require(len({row["record_id"] for row in rows}) == 192,
            "source-data record identifiers are not unique")
    require([int(row["order_index"]) for row in rows] == list(range(1, 193)),
            "source-data order ledger drift")

    contour_hash = sha256(CONTOUR_PATH)
    overlap_hash = sha256(OVERLAP_PATH)
    contour_relative = str(CONTOUR_PATH.relative_to(REPOSITORY))
    overlap_relative = str(OVERLAP_PATH.relative_to(REPOSITORY))
    certificate_panels = contour["panels"]
    require([row["record_id"] for row in contour_rows] ==
            [panel["id"] for panel in certificate_panels],
            "contour panel order or identity drift")
    for row, panel in zip(contour_rows, certificate_panels):
        require(row["bound_raw"] == panel["minimumAbsoluteLower"],
                "contour raw bound drift: " + row["record_id"])
        midpoint, radius, lower = ball_parts(row["bound_raw"])
        require(Decimal(row["bound_midpoint"]) == midpoint,
                "contour midpoint drift: " + row["record_id"])
        require(Decimal(row["bound_radius"]) == radius,
                "contour radius drift: " + row["record_id"])
        require(Decimal(row["bound_lower_endpoint"]) == lower,
                "contour lower endpoint drift: " + row["record_id"])
        require(lower > 0 and Decimal(row["strict_margin"]) == lower,
                "nonpositive contour bound: " + row["record_id"])
        require(row["upstream_path"] == contour_relative and
                row["upstream_sha256"] == contour_hash,
                "contour provenance drift: " + row["record_id"])
    require(sum(row["family"] == "global" for row in contour_rows) == 56,
            "global contour count drift")
    require(sum(row["family"] == "local" for row in contour_rows) == 8,
            "local contour count drift")

    certificate_cells = sorted(
        overlap["cells"], key=lambda cell: (cell["dIndex"], cell["lambdaIndex"])
    )
    for row, cell in zip(overlap_rows, certificate_cells):
        require(int(row["d_index"]) == int(cell["dIndex"]) and
                int(row["lambda_index"]) == int(cell["lambdaIndex"]),
                "overlap cell identity drift: " + row["record_id"])
        require(row["bound_raw"] == cell["overlapLower"],
                "overlap raw bound drift: " + row["record_id"])
        midpoint, radius, lower = ball_parts(row["bound_raw"])
        require(Decimal(row["bound_midpoint"]) == midpoint,
                "overlap midpoint drift: " + row["record_id"])
        require(Decimal(row["bound_radius"]) == radius,
                "overlap radius drift: " + row["record_id"])
        require(Decimal(row["bound_lower_endpoint"]) == lower,
                "overlap lower endpoint drift: " + row["record_id"])
        require(Decimal(row["threshold"]) == Decimal("0.5"),
                "overlap threshold drift: " + row["record_id"])
        require(lower > Decimal("0.5"),
                "overlap cell does not strictly exceed one half: " + row["record_id"])
        require(Decimal(row["strict_margin"]) == lower - Decimal("0.5"),
                "overlap margin drift: " + row["record_id"])
        require(row["upstream_path"] == overlap_relative and
                row["upstream_sha256"] == overlap_hash,
                "overlap provenance drift: " + row["record_id"])

    grid = {(int(row["d_index"]), int(row["lambda_index"])) for row in overlap_rows}
    require(grid == {(j, k) for j in range(8) for k in range(16)},
            "overlap dyadic grid is incomplete")
    global_rows = [row for row in contour_rows if row["family"] == "global"]
    local_rows = [row for row in contour_rows if row["family"] == "local"]
    global_min_row = min(global_rows, key=lambda row: Decimal(row["bound_midpoint"]))
    local_min_row = min(local_rows, key=lambda row: Decimal(row["bound_midpoint"]))
    overlap_min_row = min(overlap_rows, key=lambda row: Decimal(row["bound_midpoint"]))
    require(global_min_row["bound_raw"] ==
            contour["decisions"]["globalMinimumAbsoluteLower"],
            "global minimum does not match the certificate decision")
    require(local_min_row["bound_raw"] ==
            contour["decisions"]["localMinimumAbsoluteLower"],
            "local minimum does not match the certificate decision")
    require(overlap_min_row["bound_raw"] ==
            overlap["decisions"]["minimumKineticOverlapLower"],
            "overlap minimum does not match the certificate decision")
    require(contour["decisions"]["globalBasePositiveOrientationWinding"] == 1 and
            contour["decisions"]["localBasePositiveOrientationWinding"] == 1,
            "one or both exact base windings differ from one")
    require(contour["decisions"]["globalBoundaryNonzeroForAllD"] is True and
            contour["decisions"]["localBoundaryNonzeroForAllD"] is True,
            "one or both contour families lack uniform nonzero certification")
    require(overlap["decisions"][
        "auxiliaryRectangleKineticQuotientAtLeastOneHalf"
    ] is True, "overlap certificate decision is not true")

    decisions = results.get("decisions", {})
    require(decisions.get("globalMinimumAbsoluteLowerRaw") ==
            global_min_row["bound_raw"], "results global minimum drift")
    require(decisions.get("localMinimumAbsoluteLowerRaw") ==
            local_min_row["bound_raw"], "results local minimum drift")
    require(decisions.get("minimumKineticOverlapLowerRaw") ==
            overlap_min_row["bound_raw"], "results overlap minimum drift")
    require(decisions.get("globalMinimumId") == global_min_row["record_id"],
            "results global minimum identifier drift")
    require(decisions.get("localMinimumId") == local_min_row["record_id"],
            "results local minimum identifier drift")
    require(decisions.get("overlapMinimumCell") == {
        "dIndex": int(overlap_min_row["d_index"]),
        "lambdaIndex": int(overlap_min_row["lambda_index"]),
    }, "results overlap minimum cell drift")
    return {
        "rowCount": len(rows),
        "contourPanelCount": len(contour_rows),
        "overlapCellCount": len(overlap_rows),
        "globalMinimumId": global_min_row["record_id"],
        "globalMinimum": str(ball_parts(global_min_row["bound_raw"])[0]),
        "localMinimumId": local_min_row["record_id"],
        "localMinimum": str(ball_parts(local_min_row["bound_raw"])[0]),
        "overlapMinimumCell": {
            "dIndex": int(overlap_min_row["d_index"]),
            "lambdaIndex": int(overlap_min_row["lambda_index"]),
        },
        "overlapMinimum": str(ball_parts(overlap_min_row["bound_raw"])[0]),
    }


def pdf_image_count(page: object) -> int:
    visited: set[tuple[int, int]] = set()

    def walk(resources: object) -> int:
        if resources is None:
            return 0
        resources_object = resources.get_object() if hasattr(resources, "get_object") else resources
        xobjects = resources_object.get("/XObject")
        if xobjects is None:
            return 0
        xobjects_object = xobjects.get_object()
        count = 0
        for reference in xobjects_object.values():
            identifier = getattr(reference, "idnum", None)
            generation = getattr(reference, "generation", 0)
            key = (identifier, generation)
            if identifier is not None and key in visited:
                continue
            if identifier is not None:
                visited.add(key)
            item = reference.get_object()
            subtype = str(item.get("/Subtype"))
            if subtype == "/Image":
                count += 1
            elif subtype == "/Form":
                count += walk(item.get("/Resources"))
        return count

    return walk(page.get("/Resources"))


def verify_master_formats(config: dict) -> dict[str, object]:
    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    dpi = int(config["pngDpi"])
    # Matplotlib converts the physical canvas to an integer raster by flooring
    # the two pixel counts.  The vector masters retain the exact millimetres.
    expected_pixels = (
        int(width_mm / 25.4 * dpi), int(height_mm / 25.4 * dpi)
    )
    with Image.open(HERE / "figure.png") as image:
        png_size = image.size
        png_dpi = image.info.get("dpi", (0.0, 0.0))
        require(png_size == expected_pixels,
                f"600 dpi PNG dimensions drift: {png_size} != {expected_pixels}")
        require(all(abs(float(value) - dpi) < 0.2 for value in png_dpi),
                f"PNG density metadata drift: {png_dpi}")
        require(image.mode in {"RGB", "RGBA"}, "master PNG color mode drift")

    reader = PdfReader(HERE / "figure.pdf")
    require(len(reader.pages) == 1, "figure PDF must have exactly one page")
    page = reader.pages[0]
    pdf_points = (float(page.mediabox.width), float(page.mediabox.height))
    expected_points = (width_mm / 25.4 * 72.0, height_mm / 25.4 * 72.0)
    require(all(abs(actual - expected) < 0.12 for actual, expected in
                zip(pdf_points, expected_points)),
            f"PDF physical dimensions drift: {pdf_points} != {expected_points}")
    require(pdf_image_count(page) == 0, "PDF contains a raster image XObject")
    pdf_text = page.extract_text() or ""
    for token in (
        "Validated periodic", "Spectral-domain geometry",
        "Uniform contour-panel bounds", "Kinetic left",
        "no viscous, 3D", "Clay conclusion",
    ):
        require(token in pdf_text, "PDF text missing: " + token)

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require(re.search(r"<image\b", svg, re.IGNORECASE) is None,
            "SVG unexpectedly contains a raster image")
    for token in (
        "Spectral-domain geometry", "Uniform contour-panel bounds",
        "Kinetic left", "global: 56 panels", "local: 8 panels",
        "research-blossom-petal-1", "research-blossom-petal-5",
        "research-blossom-center", "stroke-dasharray",
    ):
        require(token in svg, "SVG vector/text encoding missing: " + token)
    for root in (config["palette"]["blue"], config["palette"]["orange"]):
        require(root.lower() in svg.lower(), "SVG palette root missing: " + root)
    for forbidden in ("#1f77b4", "#d62728", "#2ca02c", "#9467bd"):
        require(forbidden not in svg.lower(), "default palette color leaked: " + forbidden)
    return {
        "pdfPoints": list(pdf_points),
        "expectedPdfPoints": list(expected_points),
        "pdfImageXObjects": 0,
        "pngPixels": list(png_size),
        "pngDpiMetadata": [float(value) for value in png_dpi],
        "svgRasterImages": 0,
        "vectorPdf": True,
        "vectorSvg": True,
    }


def prepare_qa_surfaces(config: dict) -> dict[str, object]:
    qa_dpi = int(config["qaDpi"])
    target = (
        round(float(config["widthMillimetres"]) / 25.4 * qa_dpi),
        round(float(config["heightMillimetres"]) / 25.4 * qa_dpi),
    )
    with Image.open(HERE / "figure.png") as master:
        final = master.convert("RGB").resize(target, Image.Resampling.LANCZOS)
        final.save(HERE / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
        final.convert("L").save(HERE / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))

    pdftoppm = shutil.which("pdftoppm")
    require(pdftoppm is not None, "pdftoppm is unavailable on PATH")
    output_base = HERE / "qa-pdf"
    subprocess.run(
        [
            pdftoppm, "-png", "-r", str(qa_dpi), "-f", "1", "-l", "1",
            "-singlefile", str(HERE / "figure.pdf"), str(output_base),
        ],
        check=True, text=True, capture_output=True,
    )
    require((HERE / "qa-pdf.png").is_file(), "Poppler PDF raster is absent")

    def image_record(name: str) -> dict[str, object]:
        with Image.open(HERE / name) as image:
            return {
                "path": name,
                "pixels": list(image.size),
                "mode": image.mode,
                "sha256": sha256(HERE / name),
            }

    final_record = image_record("qa-final-size.png")
    gray_record = image_record("qa-grayscale.png")
    pdf_record = image_record("qa-pdf.png")
    require(tuple(final_record["pixels"]) == target, "final-size QA dimensions drift")
    require(tuple(gray_record["pixels"]) == target, "grayscale QA dimensions drift")
    require(gray_record["mode"] == "L", "grayscale QA surface is not single-channel")
    require(all(abs(actual - expected) <= 1 for actual, expected in
                zip(pdf_record["pixels"], target)),
            "PDF raster dimensions are inconsistent with 180 dpi physical size")

    with Image.open(HERE / "qa-final-size.png") as image:
        rgb = image.convert("RGB")
        white = Image.new("RGB", rgb.size, (255, 255, 255))
        bbox = ImageChops.difference(rgb, white).getbbox()
        require(bbox is not None, "final-size QA surface is blank")
        require(bbox[0] > 0 and bbox[1] > 0 and bbox[2] < rgb.width and bbox[3] < rgb.height,
                f"visible content touches a page edge: {bbox}")
    with Image.open(HERE / "qa-grayscale.png") as image:
        extrema = image.getextrema()
        require(extrema[0] < 70 and extrema[1] > 245,
                f"grayscale contrast is insufficient: {extrema}")

    return {
        "qaDpi": qa_dpi,
        "expectedPixels": list(target),
        "finalSize": final_record,
        "grayscale": gray_record,
        "pdfRaster": pdf_record,
        "popplerExecutable": pdftoppm,
        "popplerVersion": subprocess.run(
            [pdftoppm, "-v"], text=True, capture_output=True, check=False
        ).stderr.splitlines()[0],
        "contentBoundingBox": list(bbox),
        "grayscaleExtrema": list(extrema),
    }


def qa_report_is_passed() -> bool:
    text = (HERE / "qa-report.md").read_text(encoding="utf-8")
    return re.search(r"\*\*Status:\*\*\s*passed\b", text, re.IGNORECASE) is not None


def write_pending_qa_report(
    data_summary: dict[str, object],
    format_summary: dict[str, object],
    qa_summary: dict[str, object],
) -> None:
    if qa_report_is_passed():
        return
    (HERE / "qa-report.md").write_text(
        "# R0.73J figure QA report\n\n"
        "**Status:** pending manual visual inspection.\n\n"
        "Automated certificate and export checks passed. The final formal pass still "
        "requires direct inspection of `figure.png`, `qa-final-size.png`, "
        "`qa-grayscale.png`, and `qa-pdf.png`.\n\n"
        "Automated facts:\n\n"
        f"- source rows: {data_summary['rowCount']} = 64 contour panels + "
        f"{data_summary['overlapCellCount']} overlap cells;\n"
        f"- global minimum: {data_summary['globalMinimum']} "
        f"({data_summary['globalMinimumId']});\n"
        f"- local minimum: {data_summary['localMinimum']} "
        f"({data_summary['localMinimumId']});\n"
        f"- overlap minimum: {data_summary['overlapMinimum']} at "
        f"d-index {data_summary['overlapMinimumCell']['dIndex']}, lambda-index "
        f"{data_summary['overlapMinimumCell']['lambdaIndex']};\n"
        f"- PDF page: {format_summary['pdfPoints'][0]:.6f} by "
        f"{format_summary['pdfPoints'][1]:.6f} points;\n"
        f"- 600 dpi PNG: {format_summary['pngPixels'][0]} by "
        f"{format_summary['pngPixels'][1]} pixels;\n"
        f"- final-size QA: {qa_summary['finalSize']['pixels'][0]} by "
        f"{qa_summary['finalSize']['pixels'][1]} pixels at "
        f"{qa_summary['qaDpi']} dpi;\n"
        "- PDF/SVG raster-image count: zero.\n\n"
        "Manual inspection checklist:\n\n"
        "- original 600 dpi PNG: pending;\n"
        "- final-size raster: pending;\n"
        "- grayscale distinctions: pending;\n"
        "- independently rasterized PDF: pending;\n"
        "- labels, inset, annotation attachment, blossom anchor, and claim boundary: pending.\n",
        encoding="utf-8",
    )


def update_environment(qa_summary: dict[str, object]) -> dict:
    environment = load_json(HERE / "environment.json")
    packages = environment.setdefault("packages", {})
    packages["Pillow"] = pillow_version
    packages["pypdf"] = pypdf_version
    environment["poppler"] = {
        "version": qa_summary["popplerVersion"],
        "executable": qa_summary["popplerExecutable"],
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")
    return environment


def git_metadata() -> dict[str, object]:
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True
    ).strip()
    dirty = bool(subprocess.check_output(
        ["git", "status", "--porcelain"], cwd=REPOSITORY, text=True
    ).strip())
    remote = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=REPOSITORY,
        text=True, capture_output=True, check=False,
    ).stdout.strip()
    return {
        "repository": remote or "Kasifa/Kasifa.github.io",
        "baseCommit": head,
        "workingTreeDirtyAtRender": dirty,
        "workingTreeBoundByInputAndPackageHashes": True,
        "publicationCommitAssigned": False,
    }


def build_manifest(
    config: dict,
    contract: dict,
    results: dict,
    environment: dict,
    validation: dict,
    qa_summary: dict[str, object],
    formal: bool,
) -> dict:
    output_records = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        record = file_record(HERE / name)
        if name == "figure.png":
            record["dpi"] = 600
            record["pixels"] = validation["formats"]["pngPixels"]
        output_records.append(record)
    data_schemas = {
        "source-data.csv": (
            "192 losslessly extracted certificate records: 64 contour panels "
            "and 128 overlap cells"
        ),
        "results.json": "plotted values, input bindings, decisions, and claim boundary",
        "validation.json": "certificate, vector-format, dimension, and QA checks",
        "environment.json": "runtime, dependency, host, and Poppler metadata",
        "progress.ndjson": "timestamped deterministic render stages",
        "resource-log.ndjson": "per-stage process, thread, memory, and GPU record",
    }
    data = []
    for name, schema in data_schemas.items():
        record = file_record(HERE / name)
        record["schema"] = schema
        data.append(record)
    qa_records = [file_record(HERE / name) for name in (
        "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-report.md"
    )]
    package_files = sorted(
        path for path in HERE.iterdir()
        if path.is_file() and path.name not in {"manifest.json", "SHA256SUMS"}
    )
    return {
        "schemaVersion": "r073j-continuum-branch-figure-manifest-v1",
        "release": "R0.73J",
        "figureId": FIGURE_ID,
        "status": "formal" if formal else "draft",
        "publicationStatus": "prepublication",
        "createdAt": results["renderedAt"],
        "validatedAt": datetime.now(timezone.utc).isoformat(),
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedTakeaway"],
        "git": git_metadata(),
        "computation": {
            "kind": "data-analysis",
            "configuration": "config.json",
            "precision": (
                "outward-rounded interval-certificate strings are copied losslessly; "
                "binary64 is used only to position vector presentation marks"
            ),
            "solver": (
                "no new spectral solve; direct extraction from passed R0.73J contour "
                "and overlap certificates"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": results["wallTimeSeconds"],
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "timestamp", "elapsedSeconds", "stage", "rows", "pid",
                    "processes", "threadsPerProcess", "maximumResidentSetMiB", "gpu",
                ],
            },
        },
        "compute": {
            "host": environment.get("host", socket.gethostname()),
            "operatingSystem": environment.get("operatingSystem", platform.platform()),
            "cpu": environment.get("processor") or environment.get("architecture"),
            "memoryGiB": environment.get("memoryGiB", "not sampled"),
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used; static certificate rendering is local CPU work",
        },
        "environment": {
            "python": environment["python"],
            "packagesLock": "requirements.txt",
            **environment.get("packages", {}),
            "poppler": environment["poppler"]["version"],
        },
        "data": data,
        "sourceData": results["inputBindings"],
        "figure": {
            "profile": "journal-double-column",
            "script": "plot.py",
            "widthMillimetres": 178.0,
            "heightMillimetres": 104.0,
            "pngDpi": 600,
            "layout": "three-panel geometry, ordered margins, and dyadic overlap matrix",
            "outputs": output_records,
        },
        "caption": {"english": "caption.md"},
        "masters": ["figure.pdf", "figure.svg", "figure.png"],
        "qa": {
            "status": "passed" if formal else "pending-manual-inspection",
            "visualInspectionExplicit": formal,
            "finalSizeInspected": formal,
            "grayscaleInspected": formal,
            "labelsAndLegendsInspected": formal,
            "scalesAndUnitsInspected": formal,
            "dataCrossChecked": True,
            "finalSize": "qa-final-size.png",
            "grayscale": "qa-grayscale.png",
            "pdfRaster": "qa-pdf.png",
            "report": "qa-report.md",
            "records": qa_records,
            "qaDpi": qa_summary["qaDpi"],
        },
        "files": [file_record(path) for path in package_files],
        "inputBindings": results["inputBindings"],
        "claimBoundary": contract["claimBoundary"],
        "conditionalStatement": results["conditionalStatement"],
    }


def write_sha256_ledger() -> None:
    names = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in names),
        encoding="utf-8",
    )


def verify_sha256_ledger() -> None:
    lines = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    seen: list[str] = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", line)
        require(match is not None, "malformed SHA256SUMS row: " + line)
        expected, name = match.groups()
        path = HERE / name
        require(path.is_file() and not path.is_symlink(),
                "SHA256SUMS target is absent or not regular: " + name)
        require(sha256(path) == expected, "SHA256SUMS drift: " + name)
        seen.append(name)
    actual = sorted(
        path.name for path in HERE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    require(seen == sorted(set(seen)) == actual,
            "SHA256SUMS must cover every flat regular file exactly once")
    require(set(actual) == (SOURCE_FILES | GENERATED_FILES) - {"SHA256SUMS"},
            "formal package contains an unexpected or missing regular file")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", type=Path)
    parser.add_argument("--require-formal", action="store_true")
    args = parser.parse_args()
    getcontext().prec = 120
    verify_inventory_before_qa()
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    verify_contract(config, contract, results)
    contour, overlap = verify_input_bindings(results)
    data_summary = verify_source_data(contour, overlap, results)
    format_summary = verify_master_formats(config)
    qa_summary = prepare_qa_surfaces(config)
    write_pending_qa_report(data_summary, format_summary, qa_summary)
    manual_passed = qa_report_is_passed()
    environment = update_environment(qa_summary)

    automatic_checks = {
        "inventoryComplete": True,
        "claimBoundaryFailClosed": True,
        "inputHashesBound": True,
        "all64ContourPanelsMatched": True,
        "all128OverlapCellsMatched": True,
        "certificateMinimaMatched": True,
        "bothBaseWindingsEqualOne": True,
        "allContourBoundsStrictlyPositive": True,
        "allOverlapBoundsStrictlyAboveOneHalf": True,
        "physicalDimensionsPassed": True,
        "png600DpiPassed": True,
        "pdfVectorPassed": True,
        "svgVectorPassed": True,
        "hardTwoRootPalettePassed": True,
        "nonColorDistinctionsEncoded": True,
        "researchBlossomTopRightEncoded": True,
        "qaSurfacesPrepared": True,
    }
    validation = {
        "schemaVersion": "r073j-continuum-branch-figure-validation-v1",
        "status": "passed" if manual_passed else "pending-manual-inspection",
        "automaticStatus": "passed" if all(automatic_checks.values()) else "failed",
        "checks": {
            **automatic_checks,
            "manualVisualInspectionPassed": manual_passed,
        },
        "data": data_summary,
        "formats": format_summary,
        "qa": qa_summary,
        "claimBoundary": contract["claimBoundary"],
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    manifest = build_manifest(
        config, contract, results, environment, validation, qa_summary, manual_passed
    )
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    write_sha256_ledger()
    verify_sha256_ledger()

    if args.require_formal:
        require(manual_passed,
                "manual visual QA is still pending; inspect all QA surfaces and "
                "set qa-report.md Status to passed before the formal rerun")
        require(validation["status"] == "passed" and
                all(validation["checks"].values()),
                "formal validation checks are not all passed")
        require(manifest["status"] == "formal" and
                manifest["qa"]["status"] == "passed",
                "formal manifest state is incomplete")
    print(canonical({
        "status": validation["status"],
        "figureId": FIGURE_ID,
        "sourceRows": data_summary["rowCount"],
        "globalMinimum": data_summary["globalMinimum"],
        "localMinimum": data_summary["localMinimum"],
        "overlapMinimum": data_summary["overlapMinimum"],
        "pdfPoints": format_summary["pdfPoints"],
        "pngPixels": format_summary["pngPixels"],
        "qaFinalSizePixels": qa_summary["finalSize"]["pixels"],
        "qaPdfPixels": qa_summary["pdfRaster"]["pixels"],
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
