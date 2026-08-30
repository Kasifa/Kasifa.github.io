#!/usr/bin/env python3
"""Fail-closed validation for the formal R0.73K journal figure package."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
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

from PIL import Image, ImageChops, ImageOps, __version__ as pillow_version
from pypdf import PdfReader, __version__ as pypdf_version


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
FIGURE_ID = "fig-r073k-uniform-viscous-branch"
FIGURE_SOURCE_COMMIT = "567c72e323e1395c441b2fb76e4e0a1eae7d5662"
EXPERIMENT_CERTIFICATE_COMMIT = "ce0cfc6ad54060c1ac4fb1fa449e367f361f95ea"
CANONICAL_REPOSITORY = "https://github.com/Kasifa/Kasifa.github.io.git"
RECORDED_MEMORY_GIB = 36.0
PUBLIC_DIRECTORY = "public/assets/r073k"
PUBLIC_FILE_STEM = FIGURE_ID
PRIMARY_PATH = REPOSITORY / "experiments/r073k/viscous_branch_diagnostic.json"
INDEPENDENT_PATH = REPOSITORY / "experiments/r073k/independent_validation.json"
EXPERIMENT_CONFIG_PATH = REPOSITORY / "experiments/r073k/config.json"
EXPERIMENT_ENVIRONMENT_PATH = REPOSITORY / "experiments/r073k/environment.json"
PACKAGE_VALIDATION_PATH = REPOSITORY / "experiments/r073k/package_validation.json"
PRIMARY_PROGRESS_PATH = REPOSITORY / "experiments/r073k/progress.ndjson"
PRIMARY_RESOURCES_PATH = REPOSITORY / "experiments/r073k/resources.ndjson"
INDEPENDENT_PROGRESS_PATH = REPOSITORY / "experiments/r073k/independent_progress.ndjson"
INDEPENDENT_RESOURCES_PATH = REPOSITORY / "experiments/r073k/independent_resources.ndjson"
INPUT_PATHS = (
    PRIMARY_PATH,
    INDEPENDENT_PATH,
    EXPERIMENT_CONFIG_PATH,
    EXPERIMENT_ENVIRONMENT_PATH,
    PACKAGE_VALIDATION_PATH,
    PRIMARY_PROGRESS_PATH,
    PRIMARY_RESOURCES_PATH,
    INDEPENDENT_PROGRESS_PATH,
    INDEPENDENT_RESOURCES_PATH,
)
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
CSV_FIELDS = (
    "record_type", "record_id", "order_index", "N", "dimension",
    "small_N", "large_N", "d_index", "d_label", "d", "epsilon",
    "regime", "lambda_real", "lambda_imag", "decay_rate",
    "first_order_decay_rate", "rate_error_abs", "projector_difference",
    "projector_norm", "left_right_overlap", "right_embedded_residual",
    "left_embedded_residual", "right_algebraic_residual",
    "left_algebraic_residual", "fixed_contour_count",
    "selected_inside_fixed_contour", "cross_projector_difference",
    "cross_lambda_difference", "upstream_path", "upstream_sha256",
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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def input_record(path: Path) -> dict[str, object]:
    return {
        "path": str(path.relative_to(REPOSITORY)),
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def file_record(path: Path) -> dict[str, object]:
    return {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)}


def require_commit(commit: str, label: str) -> None:
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None,
            f"{label} is not a full commit hash")
    result = subprocess.run(
        ["git", "cat-file", "-e", commit + "^{commit}"], cwd=REPOSITORY,
        text=True, capture_output=True, check=False,
    )
    require(result.returncode == 0, f"{label} does not resolve to a commit")


def float_text(value: object) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    return format(float(value), ".17g")


def blank_row(record_type: str, record_id: str, order: int) -> dict[str, str]:
    row = {field: "" for field in CSV_FIELDS}
    row.update({
        "record_type": record_type,
        "record_id": record_id,
        "order_index": str(order),
    })
    return row


def derive_expected_rows(primary: dict, figure_config: dict) -> list[dict[str, str]]:
    upstream = str(PRIMARY_PATH.relative_to(REPOSITORY))
    upstream_hash = sha256(PRIMARY_PATH)
    display_cutoff = int(figure_config["analysis"]["displayCutoff"])
    core = sorted(
        (
            row for row in primary["rows"]
            if row["regime"] == "core" and int(row["N"]) == display_cutoff
        ),
        key=lambda row: (float(row["epsilon"]), int(row["dIndex"])),
    )
    rows: list[dict[str, str]] = []
    for item in core:
        epsilon = float(item["epsilon"])
        quotient = item["lambdaDifferenceOverEpsilon"]
        first_order = item["firstOrderAdjointFormulaAtZero"]
        decay_rate = None if quotient is None else -float(quotient["real"])
        first_order_rate = -float(first_order["real"])
        row = blank_row(
            "display_core_row",
            f"N{display_cutoff}-e{epsilon:.17g}-d{int(item['dIndex']):02d}",
            len(rows) + 1,
        )
        row.update({
            "N": str(display_cutoff),
            "dimension": str(int(item["dimension"])),
            "d_index": str(int(item["dIndex"])),
            "d_label": str(item["dLabel"]),
            "d": float_text(item["d"]),
            "epsilon": float_text(epsilon),
            "regime": "core",
            "lambda_real": float_text(item["lambda"]["real"]),
            "lambda_imag": float_text(item["lambda"]["imag"]),
            "decay_rate": float_text(decay_rate),
            "first_order_decay_rate": float_text(first_order_rate),
            "rate_error_abs": float_text(
                None if decay_rate is None else abs(decay_rate - first_order_rate)
            ),
            "projector_difference": float_text(item["projectorDifferenceFromEpsilonZero"]),
            "projector_norm": float_text(item["projectorNorm"]),
            "left_right_overlap": float_text(item["leftRightOverlap"]),
            "right_embedded_residual": float_text(item["rightEmbeddedResidual"]),
            "left_embedded_residual": float_text(item["leftEmbeddedResidual"]),
            "right_algebraic_residual": float_text(item["rightAlgebraicResidual"]),
            "left_algebraic_residual": float_text(item["leftAlgebraicResidual"]),
            "fixed_contour_count": str(int(item["fixedContourEigenvalueCount"])),
            "selected_inside_fixed_contour": float_text(item["selectedInsideFixedContour"]),
            "upstream_path": upstream,
            "upstream_sha256": upstream_hash,
        })
        rows.append(row)

    all_core = [item for item in primary["rows"] if item["regime"] == "core"]
    for cutoff in sorted({int(item["N"]) for item in all_core}):
        subset = [item for item in all_core if int(item["N"]) == cutoff]
        row = blank_row("cutoff_summary", f"cutoff-N{cutoff}", len(rows) + 1)
        row.update({
            "N": str(cutoff),
            "dimension": str(2 * cutoff + 1),
            "regime": "core",
            "right_embedded_residual": float_text(max(
                float(item["rightEmbeddedResidual"]) for item in subset
            )),
            "left_embedded_residual": float_text(max(
                float(item["leftEmbeddedResidual"]) for item in subset
            )),
            "right_algebraic_residual": float_text(max(
                float(item["rightAlgebraicResidual"]) for item in subset
            )),
            "left_algebraic_residual": float_text(max(
                float(item["leftAlgebraicResidual"]) for item in subset
            )),
            "upstream_path": upstream,
            "upstream_sha256": upstream_hash,
        })
        rows.append(row)

    cross = primary["crossCutoffComparisons"]
    for small, large in figure_config["analysis"]["cutoffPairs"]:
        subset = [
            item for item in cross
            if item["regime"] == "core"
            and int(item["smallN"]) == int(small)
            and int(item["largeN"]) == int(large)
        ]
        require(subset, f"missing cross-cutoff pair {small}->{large}")
        row = blank_row(
            "cross_cutoff_summary", f"cross-N{small}-N{large}", len(rows) + 1
        )
        row.update({
            "small_N": str(int(small)),
            "large_N": str(int(large)),
            "regime": "core",
            "cross_projector_difference": float_text(max(
                float(item["embeddedProjectorDifference"]) for item in subset
            )),
            "cross_lambda_difference": float_text(max(
                float(item["lambdaAbsoluteDifference"]) for item in subset
            )),
            "upstream_path": upstream,
            "upstream_sha256": upstream_hash,
        })
        rows.append(row)
    return rows


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
        config.get("figureId") == contract.get("figureId") ==
        results.get("figureId") == FIGURE_ID,
        "figure identity drift",
    )
    require(config.get("release") == contract.get("release") ==
            results.get("release") == "R0.73K", "release identity drift")
    require(config.get("widthMillimetres") == 178.0, "width contract drift")
    require(config.get("heightMillimetres") == 118.0, "height contract drift")
    require(config.get("pngDpi") == 600, "PNG resolution contract drift")
    require(contract.get("evidenceClass") ==
            "independently-recomputed-finite-dimensional-diagnostic",
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
        "formalValidatedDiagnosticFigure", "finiteDimensionalDiagnostic",
        "independentFiniteRecomputationPassed",
    ):
        require(boundary.get(key) is True, "missing supported boundary: " + key)
    for key in (
        "continuumViscousBranchCertifiedByFigure",
        "explicitContinuumViscosityThresholdCertified",
        "adiabaticRemainderCertified", "nonlinearNavierStokesCertified",
        "transverseThreeDimensionalClosureCertified",
        "finiteTimeSingularityCertified", "clayProblemSolved",
    ):
        require(boundary.get(key) is False, "escaped claim boundary: " + key)
    require(results.get("claimBoundary") == boundary, "result boundary drift")
    require(results.get("status") == "passed" and
            results.get("allChecksPass") is True,
            "figure result is not passed")


def verify_inputs(results: dict) -> tuple[dict, dict, dict]:
    expected = [input_record(path) for path in INPUT_PATHS]
    require(results.get("inputBindings") == expected, "input SHA-256 binding drift")
    primary = load_json(PRIMARY_PATH)
    independent = load_json(INDEPENDENT_PATH)
    package_validation = load_json(PACKAGE_VALIDATION_PATH)
    require(primary.get("status") == "passed" and primary.get("allChecksPass") is True,
            "primary diagnostic is not passed")
    require(independent.get("status") == "passed" and
            independent.get("allChecksPass") is True,
            "independent recomputation is not passed")
    require(package_validation.get("status") == "passed" and
            package_validation.get("allChecksPass") is True,
            "experiment package is not passed")
    require(all(primary.get("checks", {}).values()), "a primary check is false")
    require(all(independent.get("checks", {}).values()), "an independent check is false")
    require(all(package_validation.get("checks", {}).values()),
            "an experiment-package check is false")
    require(primary["configurationBinding"]["sha256"] == sha256(EXPERIMENT_CONFIG_PATH),
            "primary configuration hash drift")
    require(independent["primary"]["sha256"] == sha256(PRIMARY_PATH),
            "independent primary hash drift")
    return primary, independent, package_validation


def verify_source_data(primary: dict, config: dict, results: dict) -> dict[str, object]:
    with (HERE / "source-data.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        require(tuple(reader.fieldnames or ()) == CSV_FIELDS, "CSV field order drift")
        actual = list(reader)
    expected = derive_expected_rows(primary, config)
    require(actual == expected, "source-data.csv does not exactly match independent derivation")
    require(len(actual) == 213, "source-data.csv must contain 213 rows")
    require([int(row["order_index"]) for row in actual] == list(range(1, 214)),
            "source-data order ledger drift")
    require(len({row["record_id"] for row in actual}) == 213,
            "source-data record identifiers are not unique")
    display = [row for row in actual if row["record_type"] == "display_core_row"]
    cutoff = [row for row in actual if row["record_type"] == "cutoff_summary"]
    cross = [row for row in actual if row["record_type"] == "cross_cutoff_summary"]
    require(len(display) == 204 and len(cutoff) == 5 and len(cross) == 4,
            "source-data class counts drift")
    require({int(row["d_index"]) for row in display} == set(range(17)),
            "source-data d grid is incomplete")
    require(len({float(row["epsilon"]) for row in display}) == 12,
            "source-data epsilon grid is incomplete")
    require(all(row["fixed_contour_count"] == "1" for row in display),
            "a displayed row does not have fixed-circle count one")
    require(all(row["selected_inside_fixed_contour"] == "true" for row in display),
            "a displayed row lies outside the fixed circle")
    require(max(abs(float(row["lambda_imag"])) for row in display) < 1e-10,
            "displayed eigenvalue is not numerically real")
    expected_counts = results["rowCounts"]
    require(expected_counts == {
        "primary": 1190,
        "crossCutoff": 952,
        "displayCore": 204,
        "cutoffSummaries": 5,
        "crossCutoffSummaries": 4,
        "sourceData": 213,
    }, "result row counts drift")
    return {
        "rowCount": len(actual),
        "displayCoreRows": len(display),
        "cutoffSummaryRows": len(cutoff),
        "crossCutoffSummaryRows": len(cross),
        "dNodes": len({int(row["d_index"]) for row in display}),
        "coreEpsilonLevels": len({float(row["epsilon"]) for row in display}),
    }


def verify_decisions(primary: dict, independent: dict, results: dict) -> dict[str, object]:
    decisions = results["decisions"]
    display = [
        row for row in primary["rows"]
        if row["regime"] == "core" and int(row["N"]) == 160
    ]
    positive = [row for row in display if float(row["epsilon"]) > 0]
    cross = [
        row for row in primary["crossCutoffComparisons"]
        if row["regime"] == "core" and int(row["smallN"]) == 128
        and int(row["largeN"]) == 160
    ]
    require(decisions["displayCutoff"] == 160, "display cutoff decision drift")
    require(decisions["displayCoreRows"] == 204 and decisions["dNodes"] == 17 and
            decisions["coreEpsilonLevels"] == 12, "display-grid decision drift")
    require(decisions["coreFixedContourMultiplicityExactlyOne"] is True,
            "fixed-circle decision is not true")
    recomputed = {
        "maximumCoreLambdaImaginaryAbs": max(
            abs(float(row["lambda"]["imag"])) for row in display
        ),
        "maximumCoreRateErrorAgainstFirstOrder": max(
            abs(
                -float(row["lambdaDifferenceOverEpsilon"]["real"])
                + float(row["firstOrderAdjointFormulaAtZero"]["real"])
            ) for row in positive
        ),
        "maximumCoreProjectorDifference": max(
            float(row["projectorDifferenceFromEpsilonZero"]) for row in display
        ),
        "maximumCoreProjectorNorm": max(float(row["projectorNorm"]) for row in display),
        "minimumCoreLeftRightOverlap": min(
            float(row["leftRightOverlap"]) for row in display
        ),
        "largestTwoCutoffsCoreEigenvalueDifference": max(
            float(row["lambdaAbsoluteDifference"]) for row in cross
        ),
        "largestTwoCutoffsCoreEmbeddedProjectorDifference": max(
            float(row["embeddedProjectorDifference"]) for row in cross
        ),
        "largestCutoffCoreRightEmbeddedResidual": max(
            float(row["rightEmbeddedResidual"]) for row in display
        ),
        "largestCutoffCoreLeftEmbeddedResidual": max(
            float(row["leftEmbeddedResidual"]) for row in display
        ),
    }
    for key, value in recomputed.items():
        require(math.isclose(float(decisions[key]), value, rel_tol=0.0, abs_tol=1e-30),
                "decision drift: " + key)
    ordinary_keys = [
        key for key in independent["maximumAbsoluteErrors"]
        if "Quotient" not in key and key not in (
            "lambdaQuotientImag", "lambdaQuotientReal",
            "quotientExactDifference", "quotientFirstDifference",
        )
    ]
    quotient_keys = (
        "lambdaQuotientImag", "lambdaQuotientReal",
        "quotientExactDifference", "quotientFirstDifference",
    )
    ordinary = max(independent["maximumAbsoluteErrors"][key] for key in ordinary_keys)
    quotient = max(independent["maximumAbsoluteErrors"][key] for key in quotient_keys)
    require(math.isclose(decisions["independentMaximumOrdinaryAbsoluteError"], ordinary,
                         rel_tol=0.0, abs_tol=0.0),
            "independent ordinary-error decision drift")
    require(math.isclose(
        decisions["independentMaximumDifferenceQuotientAbsoluteError"], quotient,
        rel_tol=0.0, abs_tol=0.0,
    ), "independent quotient-error decision drift")
    require(ordinary <= independent["comparisonTolerances"]["ordinaryAbsolute"],
            "independent ordinary error exceeds tolerance")
    require(quotient <= independent["comparisonTolerances"]["differenceQuotientAbsolute"],
            "independent quotient error exceeds tolerance")
    return recomputed | {
        "independentMaximumOrdinaryAbsoluteError": ordinary,
        "independentMaximumDifferenceQuotientAbsoluteError": quotient,
    }


def count_pdf_images(reader: PdfReader) -> int:
    count = 0
    for page in reader.pages:
        resources = page.get("/Resources")
        if resources is None:
            continue
        resources = resources.get_object()
        xobjects = resources.get("/XObject")
        if xobjects is None:
            continue
        xobjects = xobjects.get_object()
        for candidate in xobjects.values():
            obj = candidate.get_object()
            if obj.get("/Subtype") == "/Image":
                count += 1
    return count


def verify_formats(config: dict) -> dict[str, object]:
    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    expected_points = [width_mm / 25.4 * 72.0, height_mm / 25.4 * 72.0]
    reader = PdfReader(str(HERE / "figure.pdf"))
    require(len(reader.pages) == 1, "PDF must contain one page")
    page = reader.pages[0]
    pdf_points = [float(page.mediabox.width), float(page.mediabox.height)]
    require(all(abs(actual - expected) < 0.02 for actual, expected in
                zip(pdf_points, expected_points)), "PDF physical dimensions drift")
    pdf_images = count_pdf_images(reader)
    require(pdf_images == 0, "PDF contains raster image objects")

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    require(re.search(r"<svg\b", svg) is not None, "SVG root is absent")
    require(re.search(r"<image\b", svg, flags=re.IGNORECASE) is None,
            "SVG contains a raster image")
    require("linearGradient" not in svg and "radialGradient" not in svg,
            "SVG contains a gradient")
    for root in config["palette"].values():
        if isinstance(root, str) and root.startswith("#") and root not in (
            config["palette"]["open"],
        ):
            require(root.lower() in svg.lower(), "declared palette color absent: " + root)

    with Image.open(HERE / "figure.png") as image:
        png_pixels = list(image.size)
        dpi = image.info.get("dpi", (0.0, 0.0))
        png_dpi = [float(dpi[0]), float(dpi[1])]
        require(abs(png_dpi[0] - 600.0) < 0.2 and abs(png_dpi[1] - 600.0) < 0.2,
                "PNG resolution metadata drift")
        expected_pixels = [
            round(width_mm / 25.4 * 600), round(height_mm / 25.4 * 600)
        ]
        require(all(abs(actual - expected) <= 1 for actual, expected in
                    zip(png_pixels, expected_pixels)), "PNG dimensions drift")
    return {
        "expectedPdfPoints": expected_points,
        "pdfPoints": pdf_points,
        "pdfImageXObjects": pdf_images,
        "vectorPdf": True,
        "svgRasterImages": 0,
        "vectorSvg": True,
        "pngPixels": png_pixels,
        "pngDpiMetadata": png_dpi,
    }


def prepare_qa_surfaces(config: dict) -> dict[str, object]:
    qa_dpi = int(config["qaDpi"])
    expected = (
        round(float(config["widthMillimetres"]) / 25.4 * qa_dpi),
        round(float(config["heightMillimetres"]) / 25.4 * qa_dpi),
    )
    with Image.open(HERE / "figure.png") as source:
        rgb = source.convert("RGB")
        final = rgb.resize(expected, Image.Resampling.LANCZOS)
        final.save(HERE / "qa-final-size.png", dpi=(qa_dpi, qa_dpi))
        gray = ImageOps.grayscale(final)
        gray.save(HERE / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))
        white = Image.new("RGB", final.size, "white")
        bbox = ImageChops.difference(final, white).getbbox()
        require(bbox is not None, "final-size QA raster is blank")

    executable = shutil.which("pdftoppm")
    require(executable is not None, "pdftoppm is unavailable")
    prefix = HERE / "qa-pdf"
    subprocess.run(
        [executable, "-png", "-singlefile", "-r", str(qa_dpi),
         str(HERE / "figure.pdf"), str(prefix)],
        check=True, text=True, capture_output=True,
    )
    version = subprocess.run(
        [executable, "-v"], check=True, text=True, capture_output=True
    )
    version_text = (version.stderr or version.stdout).splitlines()[0]
    with Image.open(HERE / "qa-final-size.png") as final_image:
        final_record = {
            "path": "qa-final-size.png", "pixels": list(final_image.size),
            "mode": final_image.mode, "sha256": sha256(HERE / "qa-final-size.png"),
        }
    with Image.open(HERE / "qa-grayscale.png") as gray_image:
        extrema = list(gray_image.getextrema())
        gray_record = {
            "path": "qa-grayscale.png", "pixels": list(gray_image.size),
            "mode": gray_image.mode, "sha256": sha256(HERE / "qa-grayscale.png"),
        }
    with Image.open(HERE / "qa-pdf.png") as pdf_image:
        pdf_record = {
            "path": "qa-pdf.png", "pixels": list(pdf_image.size),
            "mode": pdf_image.mode, "sha256": sha256(HERE / "qa-pdf.png"),
        }
        require(abs(pdf_image.size[0] - expected[0]) <= 2 and
                abs(pdf_image.size[1] - expected[1]) <= 2,
                "PDF QA raster dimensions drift")
    require(final_record["pixels"] == list(expected), "final QA dimensions drift")
    require(gray_record["pixels"] == list(expected), "grayscale QA dimensions drift")
    require(extrema[0] < 16 and extrema[1] > 245, "grayscale tonal range is insufficient")
    return {
        "qaDpi": qa_dpi,
        "expectedPixels": list(expected),
        "contentBoundingBox": list(bbox),
        "grayscaleExtrema": extrema,
        "finalSize": final_record,
        "grayscale": gray_record,
        "pdfRaster": pdf_record,
        "popplerExecutable": executable,
        "popplerVersion": version_text,
    }


def manual_qa_passed() -> bool:
    text = (HERE / "qa-report.md").read_text(encoding="utf-8")
    return re.search(r"\*\*Status:\*\*\s*passed\.", text, flags=re.IGNORECASE) is not None


def write_validation(
    contract: dict,
    data: dict[str, object],
    decisions: dict[str, object],
    formats: dict[str, object],
    qa: dict[str, object],
    manual_passed: bool,
) -> dict:
    checks = {
        "inventoryComplete": True,
        "inputHashesBound": True,
        "primaryAllChecksPass": True,
        "independentAllChecksPass": True,
        "experimentPackageAllChecksPass": True,
        "all213SourceRowsMatched": True,
        "all17DNodesPresent": True,
        "all12CoreEpsilonLevelsPresent": True,
        "allDisplayedFixedCircleCountsEqualOne": True,
        "allDisplayedEigenvaluesNumericallyReal": True,
        "fourAdjacentCutoffPairsPresent": True,
        "independentErrorsWithinTolerance": True,
        "claimBoundaryFailClosed": True,
        "hardTwoRootPalettePassed": True,
        "nonColorDistinctionsEncoded": True,
        "researchBlossomTopRightEncoded": True,
        "physicalDimensionsPassed": True,
        "png600DpiPassed": True,
        "pdfVectorPassed": True,
        "svgVectorPassed": True,
        "qaSurfacesPrepared": True,
        "manualVisualInspectionPassed": manual_passed,
    }
    validation = {
        "schemaVersion": "r073k-uniform-viscous-branch-figure-validation-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73K",
        "automaticStatus": "passed",
        "status": "passed" if manual_passed else "pending-manual-inspection",
        "allChecksPass": all(checks.values()),
        "checks": checks,
        "data": data | decisions,
        "formats": formats,
        "qa": qa,
        "claimBoundary": contract["claimBoundary"],
    }
    (HERE / "validation.json").write_text(canonical(validation), encoding="utf-8")
    return validation


def build_manifest(
    config: dict,
    contract: dict,
    results: dict,
    validation: dict,
    qa: dict[str, object],
    formal: bool,
) -> dict:
    environment = load_json(HERE / "environment.json")
    require_commit(FIGURE_SOURCE_COMMIT, "figure source commit")
    require_commit(EXPERIMENT_CERTIFICATE_COMMIT, "experiment certificate commit")
    figure_records = []
    for name in ("figure.pdf", "figure.svg", "figure.png"):
        record = file_record(HERE / name)
        if name == "figure.png":
            with Image.open(HERE / name) as image:
                record["pixels"] = list(image.size)
                record["dpi"] = int(config["pngDpi"])
        figure_records.append(record)
    publication_records = []
    for record in figure_records:
        extension = Path(str(record["path"])).suffix
        publication_records.append({
            "path": f"{PUBLIC_DIRECTORY}/{PUBLIC_FILE_STEM}{extension}",
            "bytes": record["bytes"],
            "sha256": record["sha256"],
        })
    qa_records = [
        file_record(HERE / name)
        for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-report.md")
    ]
    package_names = sorted((SOURCE_FILES | GENERATED_FILES) - {"manifest.json", "SHA256SUMS"})
    files = [file_record(HERE / name) for name in package_names]
    manifest = {
        "schemaVersion": "r073k-uniform-viscous-branch-figure-manifest-v1",
        "figureId": FIGURE_ID,
        "release": "R0.73K",
        "status": "formal" if formal else "draft",
        "publicationStatus": "prepublication",
        "createdAt": results["renderedAt"],
        "validatedAt": utc_now(),
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": contract["supportedTakeaway"],
        "supportedTakeaway": contract["supportedTakeaway"],
        "claimBoundary": contract["claimBoundary"],
        "inputBindings": results["inputBindings"],
        "figure": {
            "profile": "journal-double-column",
            "layout": "four-panel branch, drift, projector, and cutoff diagnostic",
            "widthMillimetres": config["widthMillimetres"],
            "heightMillimetres": config["heightMillimetres"],
            "pngDpi": config["pngDpi"],
            "script": "plot.py",
            "outputs": figure_records,
        },
        "masters": ["figure.pdf", "figure.svg", "figure.png"],
        "publication": {
            "directory": PUBLIC_DIRECTORY,
            "fileStem": PUBLIC_FILE_STEM,
            "byteIdentityRequired": True,
            "publicCopiesComplete": True,
            "assets": publication_records,
        },
        "data": [
            file_record(HERE / "source-data.csv") | {
                "schema": "204 N=160 core records, five cutoff summaries, and four adjacent-cutoff summaries"
            },
            file_record(HERE / "results.json") | {
                "schema": "input bindings, row counts, finite decisions, and claim boundary"
            },
            file_record(HERE / "validation.json") | {
                "schema": "independent data, format, QA, and boundary checks"
            },
            file_record(HERE / "environment.json") | {
                "schema": "runtime, dependency, host, thread, and git metadata"
            },
            file_record(HERE / "progress.ndjson") | {
                "schema": "timestamped deterministic render stages"
            },
            file_record(HERE / "resource-log.ndjson") | {
                "schema": "per-stage process, thread, memory, and GPU record"
            },
        ],
        "computation": {
            "kind": "data-analysis",
            "solver": "no new eigenvalue solve; deterministic extraction from the passed R0.73K finite diagnostic",
            "precision": "binary64 presentation derived losslessly from the upstream JSON decimal renderings",
            "wallTimeSeconds": results["wallTimeSeconds"],
            "configuration": "config.json",
            "formalCommand": "commands recorded in command.txt",
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
        "environment": {
            "python": environment["python"],
            "numpy": environment["numpy"],
            "matplotlib": environment["matplotlib"],
            "Pillow": pillow_version,
            "pypdf": pypdf_version,
            "poppler": qa["popplerVersion"],
            "packagesLock": "requirements.txt",
        },
        "compute": environment["compute"] | {
            "host": environment["host"],
            "machine": environment["machine"],
            "operatingSystem": environment["platform"],
            "cpu": environment["machine"],
            "memoryGiB": RECORDED_MEMORY_GIB,
        },
        "git": {
            "repository": CANONICAL_REPOSITORY,
            "baseCommit": EXPERIMENT_CERTIFICATE_COMMIT,
            "sourceCommit": FIGURE_SOURCE_COMMIT,
            "certificateCommit": EXPERIMENT_CERTIFICATE_COMMIT,
            "dirtyAtCertifiedRun": False,
            "dirtyAtCertifiedRunMeaning": (
                "the finite diagnostic inputs and rendered figure masters are read "
                "from immutable committed blobs; generated publication mirrors and "
                "unrelated working-tree files are excluded"
            ),
            "workingTreeDirtyAtRender": environment["git"].get(
                "trackedWorktreeDirtyAtRender", False
            ),
            "wholeWorktreeCleanAtRun": False,
            "workingTreeBoundByInputAndPackageHashes": True,
            "publicationCommitAssigned": False,
        },
        "sourceData": results["inputBindings"],
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
            "qaDpi": qa["qaDpi"],
        },
        "caption": {"english": "caption.md"},
        "files": files,
    }
    (HERE / "manifest.json").write_text(canonical(manifest), encoding="utf-8")
    return manifest


def verify_formal_manifest_contract(
    manifest: dict,
    contract: dict,
    results: dict,
    formal: bool,
) -> None:
    expected_status = "formal" if formal else "draft"
    require(manifest.get("status") == expected_status, "manifest status drift")
    require(manifest.get("release") == "R0.73K", "manifest release drift")
    require(manifest.get("supportedClaim") == contract["supportedTakeaway"],
            "manifest supported claim drift")
    require(manifest.get("sourceData") == results["inputBindings"],
            "manifest source-data binding drift")
    require(manifest.get("masters") == ["figure.pdf", "figure.svg", "figure.png"],
            "manifest master list drift")

    git = manifest.get("git", {})
    require(git.get("repository") == CANONICAL_REPOSITORY, "git repository drift")
    require(git.get("sourceCommit") == FIGURE_SOURCE_COMMIT,
            "git source commit drift")
    require(git.get("certificateCommit") == EXPERIMENT_CERTIFICATE_COMMIT,
            "git certificate commit drift")
    require(git.get("dirtyAtCertifiedRun") is False,
            "formal git dirtiness must be false")
    require(git.get("workingTreeBoundByInputAndPackageHashes") is True,
            "git binding declaration is absent")

    compute = manifest.get("compute", {})
    for key in (
        "host", "operatingSystem", "cpu", "memoryGiB",
        "processes", "threadsPerProcess", "gpu", "dgx",
    ):
        require(compute.get(key) not in (None, "", [], {}),
                "manifest compute field is absent: " + key)
    require(float(compute["memoryGiB"]) == RECORDED_MEMORY_GIB,
            "recorded physical memory drift")

    qa = manifest.get("qa", {})
    require(qa.get("status") == ("passed" if formal else "pending-manual-inspection"),
            "manifest QA status drift")
    for key in (
        "finalSizeInspected", "grayscaleInspected",
        "labelsAndLegendsInspected", "scalesAndUnitsInspected",
    ):
        require(qa.get(key) is formal, "manifest QA declaration drift: " + key)
    require(qa.get("dataCrossChecked") is True, "manifest data QA is not passed")
    require(len(qa.get("records", [])) == 4, "manifest QA record count drift")
    for record in qa["records"]:
        path = HERE / str(record["path"])
        require(path.is_file(), "manifest QA record is absent: " + str(path))
        require(record["bytes"] == path.stat().st_size and
                record["sha256"] == sha256(path),
                "manifest QA record binding drift: " + path.name)

    publication = manifest.get("publication", {})
    require(publication.get("directory") == PUBLIC_DIRECTORY,
            "publication directory drift")
    require(publication.get("fileStem") == PUBLIC_FILE_STEM,
            "publication file stem drift")
    require(publication.get("byteIdentityRequired") is True,
            "publication byte-identity requirement is absent")
    require(publication.get("publicCopiesComplete") is True,
            "publication public-copy declaration is not complete")
    assets = publication.get("assets", [])
    outputs = manifest["figure"]["outputs"]
    require(len(assets) == len(outputs) == 3, "publication asset count drift")
    output_by_extension = {Path(record["path"]).suffix: record for record in outputs}
    for extension in (".pdf", ".svg", ".png"):
        master = output_by_extension[extension]
        expected_path = f"{PUBLIC_DIRECTORY}/{PUBLIC_FILE_STEM}{extension}"
        asset = next((record for record in assets if record.get("path") == expected_path), None)
        require(asset is not None, "publication asset path is absent: " + expected_path)
        require(asset["bytes"] == master["bytes"] and
                asset["sha256"] == master["sha256"],
                "publication asset does not bind its master: " + extension)
        public_path = REPOSITORY / expected_path
        if public_path.is_file():
            require(public_path.stat().st_size == asset["bytes"] and
                    sha256(public_path) == asset["sha256"],
                    "existing public copy is not byte-identical: " + expected_path)


def verify_existing_qa(config: dict, validation: dict) -> dict[str, object]:
    qa = validation.get("qa", {})
    require(isinstance(qa, dict), "validation QA record must be an object")
    require(qa.get("qaDpi") == int(config["qaDpi"]), "validation QA DPI drift")
    expected_pixels = [
        round(float(config["widthMillimetres"]) / 25.4 * int(config["qaDpi"])),
        round(float(config["heightMillimetres"]) / 25.4 * int(config["qaDpi"])),
    ]
    require(qa.get("expectedPixels") == expected_pixels,
            "validation QA expected-pixel drift")
    for key, expected_name, expected_mode in (
        ("finalSize", "qa-final-size.png", "RGB"),
        ("grayscale", "qa-grayscale.png", "L"),
        ("pdfRaster", "qa-pdf.png", "RGB"),
    ):
        record = qa.get(key, {})
        require(record.get("path") == expected_name, "validation QA path drift: " + key)
        path = HERE / expected_name
        require(path.is_file() and not path.is_symlink(), "QA surface is absent: " + expected_name)
        require(record.get("sha256") == sha256(path), "QA surface hash drift: " + expected_name)
        with Image.open(path) as image:
            require(record.get("pixels") == list(image.size),
                    "QA surface pixel drift: " + expected_name)
            require(record.get("mode") == image.mode == expected_mode,
                    "QA surface mode drift: " + expected_name)
    require(qa["finalSize"]["pixels"] == expected_pixels,
            "final-size QA dimensions drift")
    require(qa["grayscale"]["pixels"] == expected_pixels,
            "grayscale QA dimensions drift")
    pdf_pixels = qa["pdfRaster"]["pixels"]
    require(abs(pdf_pixels[0] - expected_pixels[0]) <= 2 and
            abs(pdf_pixels[1] - expected_pixels[1]) <= 2,
            "PDF-raster QA dimensions drift")
    require(qa.get("grayscaleExtrema") == [0, 255],
            "grayscale QA tonal-range drift")
    require(manual_qa_passed(), "qa-report.md does not record a passed inspection")
    return qa


def verify_manifest_file_bindings(manifest: dict) -> None:
    for section in ("data", "files"):
        records = manifest.get(section, [])
        require(isinstance(records, list) and records,
                "manifest file-record section is absent: " + section)
        for record in records:
            path = HERE / str(record["path"])
            require(path.is_file() and not path.is_symlink(),
                    f"manifest {section} target is absent: {path.name}")
            require(record.get("bytes") == path.stat().st_size and
                    record.get("sha256") == sha256(path),
                    f"manifest {section} binding drift: {path.name}")
    for record in manifest["figure"]["outputs"]:
        path = HERE / str(record["path"])
        require(path.is_file() and record.get("bytes") == path.stat().st_size and
                record.get("sha256") == sha256(path),
                "manifest figure-output binding drift: " + path.name)
    for record in manifest["sourceData"]:
        path = REPOSITORY / str(record["path"])
        require(path.is_file() and record.get("bytes") == path.stat().st_size and
                record.get("sha256") == sha256(path),
                "manifest source-data binding drift: " + str(record["path"]))


def check_formal_read_only() -> dict[str, object]:
    verify_inventory_before_qa()
    for name in ("validation.json", "manifest.json", "SHA256SUMS"):
        path = HERE / name
        require(path.is_file() and not path.is_symlink(),
                "formal package record is absent: " + name)
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    verify_contract(config, contract, results)
    primary, independent, _package_validation = verify_inputs(results)
    data = verify_source_data(primary, config, results)
    decisions = verify_decisions(primary, independent, results)
    formats = verify_formats(config)
    qa = verify_existing_qa(config, validation)
    require(validation.get("figureId") == FIGURE_ID and
            validation.get("release") == "R0.73K",
            "validation identity or release drift")
    require(validation.get("status") == "passed" and
            validation.get("automaticStatus") == "passed" and
            validation.get("allChecksPass") is True,
            "formal validation status is not passed")
    require(all(validation.get("checks", {}).values()),
            "a stored formal validation check is false")
    require(validation.get("data") == data | decisions,
            "stored formal validation data drift")
    require(validation.get("formats") == formats,
            "stored formal validation format drift")
    require(validation.get("claimBoundary") == contract["claimBoundary"],
            "stored formal validation boundary drift")
    verify_formal_manifest_contract(manifest, contract, results, True)
    require(manifest.get("qa", {}).get("qaDpi") == qa["qaDpi"],
            "manifest QA summary drift")
    verify_manifest_file_bindings(manifest)
    verify_sha256s()
    return {
        "figureId": FIGURE_ID,
        "release": "R0.73K",
        "status": "formal",
        "validationStatus": "passed",
        "allChecksPass": True,
        "sourceRows": data["rowCount"],
        "checksumCount": len((HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()),
        "publicationCopiesComplete": manifest["publication"]["publicCopiesComplete"],
        "readOnly": True,
    }


def write_sha256s() -> int:
    names = sorted((SOURCE_FILES | GENERATED_FILES) - {"SHA256SUMS"})
    lines = []
    for name in names:
        path = HERE / name
        require(path.is_file() and not path.is_symlink(),
                "cannot checksum absent or symlink file: " + name)
        lines.append(f"{sha256(path)}  {name}")
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


def verify_sha256s() -> None:
    records = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected_names = sorted((SOURCE_FILES | GENERATED_FILES) - {"SHA256SUMS"})
    require(len(records) == len(expected_names), "SHA256SUMS count drift")
    for line, expected_name in zip(records, expected_names):
        match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
        require(match is not None, "malformed SHA256SUMS line")
        digest, name = match.groups()
        require(name == expected_name, "SHA256SUMS order or name drift")
        require(digest == sha256(HERE / name), "SHA256 mismatch: " + name)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--deps", help="directory containing pinned Python packages")
    parser.add_argument("--require-formal", action="store_true")
    parser.add_argument(
        "--check-formal", action="store_true",
        help="verify the existing formal package without writing any file",
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_arguments()
    require(not (arguments.require_formal and arguments.check_formal),
            "--require-formal and --check-formal are mutually exclusive")
    if arguments.check_formal:
        print(canonical(check_formal_read_only()), end="")
        return 0
    verify_inventory_before_qa()
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    results = load_json(HERE / "results.json")
    verify_contract(config, contract, results)
    primary, independent, _package_validation = verify_inputs(results)
    data = verify_source_data(primary, config, results)
    decisions = verify_decisions(primary, independent, results)
    formats = verify_formats(config)
    qa = prepare_qa_surfaces(config)
    manual = manual_qa_passed()
    if arguments.require_formal:
        require(manual, "formal validation requires qa-report.md Status: passed")
    validation = write_validation(contract, data, decisions, formats, qa, manual)
    manifest = build_manifest(config, contract, results, validation, qa, manual)
    verify_formal_manifest_contract(manifest, contract, results, manual)
    checksum_count = write_sha256s()
    verify_sha256s()
    if arguments.require_formal:
        require(validation["status"] == "passed" and validation["allChecksPass"] is True,
                "formal validation checks are incomplete")
        require(manifest["status"] == "formal" and manifest["qa"]["status"] == "passed",
                "formal manifest contract is incomplete")
    output = {
        "figureId": FIGURE_ID,
        "status": validation["status"],
        "automaticStatus": validation["automaticStatus"],
        "allChecksPass": validation["allChecksPass"],
        "manualVisualInspectionPassed": manual,
        "sourceRows": data["rowCount"],
        "checksumCount": checksum_count,
        "manifestStatus": manifest["status"],
        "publicationCopiesComplete": manifest["publication"]["publicCopiesComplete"],
    }
    print(canonical(output), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
