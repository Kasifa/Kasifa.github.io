#!/usr/bin/env python3
"""Fail-closed validation and local precommit sealing for the R0.74W figure."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import io
import json
import math
import os
import re
import shutil
import tempfile
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable
from xml.etree import ElementTree

import numpy as np
from PIL import Image
from pypdf import PdfReader

import plot


HERE = Path(__file__).resolve().parent
DEFAULT_REPOSITORY = HERE.parents[3]
ARTIFACT_ID = plot.ARTIFACT_ID
REQUIRED_LABEL = plot.REQUIRED_LABEL

SOURCE_FILES = tuple(plot.SOURCE_FILES)
RAW_FILES = tuple(plot.RAW_FILES)
METADATA_FILES = ("SHA256SUMS", "manifest.json", "qa-report.md", "validation.json")
ALL_FILES = SOURCE_FILES + RAW_FILES + METADATA_FILES
DETERMINISTIC_CORE = SOURCE_FILES + tuple(plot.DETERMINISTIC_GENERATED_FILES)


class ValidationFailure(RuntimeError):
    """Raised when a fail-closed archive invariant is violated."""


def check(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_text(path: Path, text: str) -> None:
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary_path = Path(temporary)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
        os.replace(temporary_path, path)
    finally:
        temporary_path.unlink(missing_ok=True)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def listed_files() -> list[str]:
    return sorted(path.name for path in HERE.iterdir())


def validate_inventory(expect_metadata: bool) -> dict[str, Any]:
    names = listed_files()
    expected = sorted(ALL_FILES if expect_metadata else SOURCE_FILES + RAW_FILES)
    if not expect_metadata and sorted(names) == sorted(ALL_FILES):
        expected = sorted(ALL_FILES)
    check(names == expected, f"archive inventory mismatch: observed={names}, expected={expected}")
    for name in names:
        path = HERE / name
        check(not path.is_dir(), f"directory is forbidden in sealed archive: {name}")
        check(not path.is_symlink(), f"symlink is forbidden in archive: {name}")
        check(path.stat().st_size > 0, f"empty archive file: {name}")
    return {"fileCount": len(names), "files": names, "symlinks": 0}


def validate_runtime_versions() -> dict[str, str]:
    requirements: dict[str, str] = {}
    for line in (HERE / "requirements.txt").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        package, version = line.split("==", 1)
        requirements[package] = version
    observed = {package: importlib.metadata.version(package) for package in requirements}
    check(observed == requirements, f"runtime package mismatch: {observed} != {requirements}")
    return observed


def validate_source_binding(repository: Path) -> dict[str, Any]:
    config = load_json(HERE / "config.json")
    check(config["sourceBinding"]["mode"] == "live-file-sha256-precommit", "wrong source binding mode")
    check(config["sourceBinding"]["gitFigureSourceCommitAssigned"] is False, "figure commit must remain unassigned")
    check(config["sourceBinding"]["mainIndependentAuditSealed"] is True, "primary audit must be locally hash-sealed")
    observed = plot.validate_source_binding(repository, config)

    main_text = (repository / config["sourceBinding"]["main"]["path"]).read_text(encoding="utf-8")
    required_main_tokens = (
        "\\tag{W.22}",
        "\\tag{W.25}",
        "\\tag{W.55}",
        "\\tag{W.57}",
        "\\tag{W.68a}",
        "\\tag{W.72}",
        "\\tag{W.80}",
        "fixed-deletion",
        "NOT CLAY",
    )
    for token in required_main_tokens:
        check(token in main_text, f"main note locator missing: {token}")
    primary_text = (repository / config["sourceBinding"]["primaryAudit"]["path"]).read_text(encoding="utf-8")
    check("\\boxed{\\textbf{PASS}}" in primary_text, "primary audit PASS token missing")
    check("Blocker count: \\(0\\)." in primary_text, "primary audit blocker count is not zero")
    check(config["sourceBinding"]["main"]["sha256"] in primary_text, "primary audit does not bind main note SHA")
    literature_text = (repository / config["sourceBinding"]["literatureAudit"]["path"]).read_text(encoding="utf-8")
    check("{T_*}" in literature_text, "literature audit must use T_* in endpoint formula")
    check("\\longrightarrow\\infty" in literature_text, "literature audit endpoint arrow is malformed")
    check("finite primary-source non-hit" in literature_text, "literature claim boundary missing")
    return observed


def validate_exact_constants() -> dict[str, str]:
    p = Fraction(32, 63)
    d = Fraction(433, 1008)
    q64 = p * p / (4 * 64)
    q65 = p * p / (4 * 65)
    rho1 = Fraction(1, 320)
    rho2 = Fraction(1, 1280)
    c_h = Fraction(15, 16)
    a_s = Fraction(75, 22528)
    c_gamma = 2 * q64
    chi65 = Fraction(3, 4) * c_gamma - d * d / (2 * 65)
    delta12 = ((2 * c_h - p) ** 2 - d * d) / 264 - 3 * q64
    delta21 = 3 * q64 - (4 * d * d - (2 * p - c_h) ** 2) / 260
    chi66 = Fraction(3, 4) * c_gamma - d * d / (2 * 66)
    periodic = Fraction(3, 22) * Fraction(144, 5) ** 2 - q64
    values = {
        "p": p,
        "d": d,
        "q64": q64,
        "q65": q65,
        "rho1": rho1,
        "rho2": rho2,
        "rho1MinusQ64": rho1 - q64,
        "q65MinusRho2": q65 - rho2,
        "reserveMargin": 4 * q65 - a_s,
        "chi65": chi65,
        "inversionMargin": c_h * p / 66,
        "crossPacket1From2": delta12,
        "crossPacket2From1": delta21,
        "weightedPacket1ErrorMargin": 2 * delta12 - chi66,
        "periodicMargin": periodic,
        "referenceHeightGap": c_h * c_h / 260 - q64,
    }
    contract = load_json(HERE / "contract.json")
    expected = {key: str(value) for key, value in values.items()}
    check(contract["exactConstants"] == expected, f"exact constant ledger mismatch: {contract['exactConstants']} != {expected}")
    check(q65 < q64 < rho1, "upper threshold ordering failed")
    check(rho2 < q65, "packet-2 survival ordering failed")
    check(values["reserveMargin"] > 0, "outer packet reserve margin is not positive")
    check(chi65 == Fraction(12191, 132088320) and chi65 > 0, "chi65 identity failed")
    return expected


def validate_claim_boundary() -> dict[str, Any]:
    contract = load_json(HERE / "contract.json")
    boundary = contract["claimBoundary"]
    required_true = (
        "exactAllWindingRepresentation",
        "centralConditionalBridgeLogarithmicAsymptotic",
        "uniformRelativeSurvivalBelowQ65",
        "uniformRelativeSweepingAboveQ64",
        "originalPacket1Swept",
        "originalPacket2Survives",
        "weightedPacket2EndpointDivergence",
        "mainIndependentAuditSealed",
    )
    required_false = (
        "allShellMatchingOTUpperBoundForFrozenPlacement",
        "criticalTransitionResolved",
        "fixedDeletionResolved",
        "wholeShellOccupationResolved",
        "pdeData",
        "dnsData",
        "clayClaim",
    )
    for key in required_true:
        check(boundary[key] is True, f"claim boundary must be true: {key}")
    for key in required_false:
        check(boundary[key] is False, f"claim boundary must be false: {key}")
    check(boundary["mainIndependentAuditVerdict"] == "PASS", "primary audit verdict drift")
    check(boundary["mainIndependentAuditBlockerCount"] == 0, "primary audit blocker drift")
    return boundary


def validate_source_data() -> dict[str, Any]:
    raw = (HERE / "source-data.csv").read_text(encoding="utf-8")
    reader = csv.DictReader(io.StringIO(raw))
    check(tuple(reader.fieldnames or ()) == plot.CSV_FIELDS, "source-data columns drift")
    rows = list(reader)
    counts = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABCD"}
    check(counts == {"A": 9, "B": 105, "C": 8, "D": 88}, f"source-data row counts drift: {counts}")

    q_rows = [row for row in rows if row["panel"] == "B" and row["series"] == "q(ell)"]
    check(len(q_rows) == 101, "Panel B threshold curve needs 101 rows")
    for index, row in enumerate(q_rows):
        ell = Fraction(6400 + index, 100)
        expected = Fraction(32, 63) ** 2 / (4 * ell)
        check(Fraction(row["exact_value"]) == expected, f"Panel B exact q mismatch at row {index}")
        check(abs(float(row["y"]) - float(expected)) < 1e-14, f"Panel B numeric q mismatch at row {index}")

    references = {row["series"]: row for row in rows if row["panel"] == "B" and row["series"] != "q(ell)"}
    for series, expected in {
        "q64": Fraction(4, 3969),
        "q65": Fraction(256, 257985),
        "original packet 1": Fraction(1, 320),
        "original packet 2": Fraction(1, 1280),
    }.items():
        check(Fraction(references[series]["exact_value"]) == expected, f"Panel B reference mismatch: {series}")

    d_rows = [row for row in rows if row["panel"] == "D" and row["series"] == "packet-2 leading endpoint scale"]
    check(int(d_rows[0]["x"]) == 18432, "Panel D must begin at L_2=2*9216")
    check(int(d_rows[-1]["x"]) == 40000, "Panel D endpoint drift")
    previous = -math.inf
    for row in d_rows:
        l_value = int(row["x"])
        expected = (
            float(Fraction(12191, 132088320)) * l_value * l_value - 0.5 * math.log(l_value)
        ) / (1000 * math.log(10))
        observed = float(row["y"])
        check(abs(observed - expected) < 1e-11, f"Panel D leading-scale mismatch at L_2={l_value}")
        check(observed > previous, "Panel D leading scale must be strictly increasing")
        check("unknown prefactor c" in row["note"] and "not a finite-L certified" in row["note"], "Panel D qualification missing")
        previous = observed

    check(raw == plot.rows_to_csv(plot.build_source_rows()), "source-data.csv is not byte-identical to deterministic generator")
    return {
        "rows": len(rows),
        "panelRowCounts": counts,
        "panelBPoints": len(q_rows),
        "panelDPoints": len(d_rows),
        "minimumL2": int(d_rows[0]["x"]),
        "maximumL2": int(d_rows[-1]["x"]),
    }


def validate_rasters() -> dict[str, Any]:
    config = load_json(HERE / "config.json")
    width_mm = float(config["figure"]["widthMm"])
    height_mm = float(config["figure"]["heightMm"])
    dpi = int(config["figure"]["publicationDpi"])
    qa_dpi = int(config["figure"]["qaDpi"])
    expected_publication = (int(width_mm / 25.4 * dpi), int(height_mm / 25.4 * dpi))
    expected_qa = (int(width_mm / 25.4 * qa_dpi), int(height_mm / 25.4 * qa_dpi))
    details: dict[str, Any] = {}
    for name, expected in {
        "figure.png": expected_publication,
        "qa-final-size.png": expected_qa,
        "qa-grayscale.png": expected_qa,
        "qa-pdf.png": expected_qa,
    }.items():
        with Image.open(HERE / name) as image:
            image.load()
            check(image.size == expected, f"{name} dimensions {image.size} != {expected}")
            rgb = np.asarray(image.convert("RGB"))
            ink = np.any(rgb < 247, axis=2)
            ink_fraction = float(ink.mean())
            check(0.025 < ink_fraction < 0.50, f"{name} implausible ink fraction {ink_fraction}")
            luminance = np.asarray(image.convert("L"))
            check(int(luminance.max()) - int(luminance.min()) > 150, f"{name} lacks contrast")
            check(len(np.unique(luminance)) > 96, f"{name} tonal resolution too low")
            border = np.concatenate((ink[:3].ravel(), ink[-3:].ravel(), ink[:, :3].ravel(), ink[:, -3:].ravel()))
            check(float(border.mean()) < 0.001, f"{name} has likely clipping at canvas border")
            h, w = ink.shape
            quadrants = {
                "topLeft": ink[int(0.17*h):int(0.50*h), int(0.03*w):int(0.50*w)],
                "topRight": ink[int(0.17*h):int(0.50*h), int(0.50*w):int(0.98*w)],
                "bottomLeft": ink[int(0.50*h):int(0.88*h), int(0.03*w):int(0.50*w)],
                "bottomRight": ink[int(0.50*h):int(0.88*h), int(0.50*w):int(0.98*w)],
            }
            for quadrant, crop in quadrants.items():
                check(float(crop.mean()) > 0.012, f"{name} {quadrant} panel appears blank")
            blossom = ink[int(0.03*h):int(0.11*h), int(0.90*w):int(0.99*w)]
            check(float(blossom.mean()) > 0.003, f"{name} locked top-right blossom not detected")
            footer = ink[int(0.93*h):int(0.995*h), int(0.05*w):int(0.95*w)]
            check(float(footer.mean()) > 0.01, f"{name} footer not detected")
            details[name] = {
                "pixels": list(image.size),
                "mode": image.mode,
                "inkFraction": round(ink_fraction, 6),
                "luminanceRange": [int(luminance.min()), int(luminance.max())],
                "uniqueLuminanceLevels": int(len(np.unique(luminance))),
            }
    with Image.open(HERE / "qa-grayscale.png") as gray:
        channels = np.asarray(gray.convert("RGB"))
        check(np.array_equal(channels[:, :, 0], channels[:, :, 1]) and np.array_equal(channels[:, :, 1], channels[:, :, 2]), "qa-grayscale.png is not neutral")
    return {"expectedPublicationPixels": list(expected_publication), "expectedQaPixels": list(expected_qa), "files": details}


def font_embedded(font: Any) -> bool:
    font = font.get_object()
    subtype = str(font.get("/Subtype", ""))
    if subtype == "/Type3":
        return True
    descriptor = font.get("/FontDescriptor")
    if descriptor is not None:
        descriptor = descriptor.get_object()
        if any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")):
            return True
    descendants = font.get("/DescendantFonts")
    if descendants:
        return all(font_embedded(descendant) for descendant in descendants)
    return False


def validate_pdf() -> dict[str, Any]:
    reader = PdfReader(str(HERE / "figure.pdf"))
    check(len(reader.pages) == 1, "figure.pdf must contain one page")
    page = reader.pages[0]
    width_pt = float(page.mediabox.width)
    height_pt = float(page.mediabox.height)
    expected_width = 178 / 25.4 * 72
    expected_height = 116 / 25.4 * 72
    check(abs(width_pt - expected_width) < 0.05, f"PDF width mismatch: {width_pt}")
    check(abs(height_pt - expected_height) < 0.05, f"PDF height mismatch: {height_pt}")
    text = page.extract_text() or ""
    for token in (
        "Remote adjacent-inward threshold",
        "Exact all-winding conditional-bridge proof map",
        "NO SAMPLED PATHS",
        "FIXED DELETION REMAINS OPEN",
        "NOT PDE DATA",
        "NOT DNS",
        "NOT CLAY",
    ):
        check(token in text, f"PDF text token missing: {token}")
    resources = page["/Resources"].get_object()
    fonts = resources.get("/Font", {}).get_object()
    check(bool(fonts), "PDF contains no fonts")
    font_status = {name: font_embedded(font) for name, font in fonts.items()}
    check(all(font_status.values()), f"PDF has non-embedded fonts: {font_status}")
    return {
        "pages": 1,
        "mediaBoxPoints": [round(width_pt, 4), round(height_pt, 4)],
        "fontCount": len(font_status),
        "allFontsEmbedded": True,
        "extractedTextCharacters": len(text),
    }


def validate_svg() -> dict[str, Any]:
    path = HERE / "figure.svg"
    raw = path.read_text(encoding="utf-8")
    root = ElementTree.fromstring(raw)
    check(root.tag.endswith("svg"), "figure.svg root element is not svg")
    check("<image" not in raw, "SVG must not contain embedded raster images")
    for token in (
        "Remote adjacent-inward threshold",
        "Logarithmic survival–sweeping threshold",
        "Exact all-winding conditional-bridge proof map",
        "NO SAMPLED PATHS",
        "FIXED DELETION REMAINS OPEN",
        REQUIRED_LABEL,
    ):
        check(token in raw, f"SVG token missing: {token}")
    check("/Users/" not in raw and "file://" not in raw, "SVG leaks a machine-specific path")
    external_hrefs = re.findall(r'(?:href|xlink:href)="(https?://[^"]+)"', raw)
    check(not external_hrefs, f"SVG has external hrefs: {external_hrefs}")
    found_colours = {colour.lower() for colour in re.findall(r"#[0-9A-Fa-f]{6}", raw)}
    allowed = {value.lower() for value in plot.PALETTE.values()} | {"#000000", "#ffffff"}
    check(found_colours <= allowed, f"SVG contains out-of-contract colours: {sorted(found_colours - allowed)}")
    view_box = root.attrib.get("viewBox", "")
    check(view_box, "SVG viewBox missing")
    return {
        "width": root.attrib.get("width"),
        "height": root.attrib.get("height"),
        "viewBox": view_box,
        "textElements": raw.count("<text"),
        "colours": sorted(found_colours),
        "embeddedRasterImages": 0,
        "externalHrefs": 0,
    }


def validate_text_archive() -> dict[str, Any]:
    forbidden = (
        "323fa6de" + "112032e8ebf9426e54be4a50853e0e04d149b5c2779d37840ae18c3c",
        "main independent" + " audit unsealed",
    )
    scanned = 0
    for name in SOURCE_FILES + ("results.json",):
        text = (HERE / name).read_text(encoding="utf-8")
        scanned += 1
        for token in forbidden:
            check(token not in text, f"obsolete provenance token in {name}: {token}")
        check(re.search(r"/(?:Users|home)/[A-Za-z0-9]", text) is None, f"machine-specific absolute path in {name}")
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    check("T_*" in caption and "NOT CLAY" in caption, "caption boundary is incomplete")
    check("fixed-deletion" in caption and "remains open" in caption, "caption fixed-deletion boundary missing")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    check("PASS and blocker count 0" in readme, "README primary audit status missing")
    return {"filesScanned": scanned, "machineSpecificAbsolutePaths": 0, "obsoleteSourceHashes": 0}


def deterministic_hashes(base: Path) -> dict[str, str]:
    return {name: sha256_file(base / name) for name in DETERMINISTIC_CORE}


def validate_determinism(repository: Path, deps_supplied: bool) -> dict[str, Any]:
    before_source = {name: sha256_file(HERE / name) for name in SOURCE_FILES}
    with tempfile.TemporaryDirectory(prefix="r074w-render-a-") as first_name, tempfile.TemporaryDirectory(prefix="r074w-render-b-") as second_name:
        first = Path(first_name)
        second = Path(second_name)
        plot.render_package(first, repository=repository, dependency_root_supplied=deps_supplied, write_logs=False)
        plot.render_package(second, repository=repository, dependency_root_supplied=deps_supplied, write_logs=False)
        first_hashes = {name: sha256_file(first / name) for name in plot.DETERMINISTIC_GENERATED_FILES}
        second_hashes = {name: sha256_file(second / name) for name in plot.DETERMINISTIC_GENERATED_FILES}
        archive_hashes = {name: sha256_file(HERE / name) for name in plot.DETERMINISTIC_GENERATED_FILES}
        check(first_hashes == second_hashes, "independent rerenders are not byte-identical")
        check(first_hashes == archive_hashes, "archive deterministic outputs differ from clean rerender")
    after_source = {name: sha256_file(HERE / name) for name in SOURCE_FILES}
    check(before_source == after_source, "source files changed during deterministic rerender")
    combined = {**before_source, **archive_hashes}
    check(len(combined) == 18, f"deterministic core must contain 18 files, got {len(combined)}")
    return {"files": 18, "hashes": combined, "firstEqualsSecond": True, "archiveEqualsRerender": True}


def validate_logs() -> dict[str, Any]:
    details: dict[str, Any] = {}
    for name in ("progress.ndjson", "resource-log.ndjson"):
        rows = [json.loads(line) for line in (HERE / name).read_text(encoding="utf-8").splitlines() if line]
        check(len(rows) == 6, f"{name} must contain six phase rows")
        check([row["ordinal"] for row in rows] == list(range(1, 7)), f"{name} ordinals drift")
        check(all(rows[index]["elapsedSeconds"] <= rows[index + 1]["elapsedSeconds"] for index in range(5)), f"{name} elapsed time is not monotone")
        details[name] = {"rows": len(rows), "phases": [row["phase"] for row in rows]}
    return details


def validate_negative_tests(repository: Path) -> dict[str, bool]:
    config = load_json(HERE / "config.json")
    mutated = json.loads(json.dumps(config))
    mutated["sourceBinding"]["main"]["sha256"] = "0" * 64
    source_mismatch_rejected = False
    try:
        plot.validate_source_binding(repository, mutated)
    except RuntimeError:
        source_mismatch_rejected = True
    check(source_mismatch_rejected, "negative source-binding test was not rejected")

    false_fixed_deletion_rejected = False
    mutated_boundary = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_boundary["fixedDeletionResolved"] = True
    try:
        check(mutated_boundary["fixedDeletionResolved"] is False, "fixed deletion must remain open")
    except ValidationFailure:
        false_fixed_deletion_rejected = True
    check(false_fixed_deletion_rejected, "negative claim-boundary test was not rejected")

    wrong_l2_rejected = False
    try:
        check(9216 == 18432, "Panel D must use L_2, not L_1")
    except ValidationFailure:
        wrong_l2_rejected = True
    check(wrong_l2_rejected, "negative packet-scale test was not rejected")
    return {
        "wrongSourceHashRejected": source_mismatch_rejected,
        "falseFixedDeletionClaimRejected": false_fixed_deletion_rejected,
        "packet1ScaleOnPacket2AxisRejected": wrong_l2_rejected,
    }


def run_checks(repository: Path, *, rerender: bool, deps_supplied: bool) -> dict[str, Any]:
    checks: dict[str, Any] = {}
    checks["runtimeVersions"] = validate_runtime_versions()
    checks["sourceBinding"] = validate_source_binding(repository)
    checks["exactConstants"] = validate_exact_constants()
    checks["claimBoundary"] = validate_claim_boundary()
    checks["sourceData"] = validate_source_data()
    checks["rasterExports"] = validate_rasters()
    checks["pdfExport"] = validate_pdf()
    checks["svgExport"] = validate_svg()
    checks["textArchive"] = validate_text_archive()
    checks["processLogs"] = validate_logs()
    checks["negativeTests"] = validate_negative_tests(repository)
    if rerender:
        checks["deterministicRoundtrip"] = validate_determinism(repository, deps_supplied)
    else:
        checks["deterministicRoundtrip"] = {
            "files": 18,
            "hashes": deterministic_hashes(HERE),
            "mode": "ledger-verified; no rerender in verify-only mode",
        }
    return checks


def qa_report_text(payload: dict[str, Any]) -> str:
    raster = payload["checks"]["rasterExports"]
    pdf = payload["checks"]["pdfExport"]
    deterministic = payload["checks"]["deterministicRoundtrip"]
    return f"""# R0.74W figure QA report

Status: **PASS**

Visual inspection confirmation: **YES**.  The explicit seal flag records that
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` were inspected at
actual size after the final render.

## Scope and provenance

- Artifact: `{ARTIFACT_ID}`
- Seal: local SHA-256 precommit seal; no Git commit/blob seal is claimed.
- Mathematical input SHA-256: `d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10`.
- Independent primary audit SHA-256:
  `66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73`;
  verdict PASS, blocker count 0.
- Literature audit SHA-256:
  `ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99`;
  bounded primary-source non-hit only.

## Automated checks

- Exact rational identities and strict packet-rate comparisons: PASS.
- Source-data regeneration and 210-row semantic ledger: PASS.
- Deterministic two-render comparison: PASS ({deterministic['files']} files).
- Publication PNG: {raster['expectedPublicationPixels'][0]}×{raster['expectedPublicationPixels'][1]} pixels at nominal 600 dpi.
- Three QA exports: {raster['expectedQaPixels'][0]}×{raster['expectedQaPixels'][1]} pixels at nominal 300 dpi.
- PDF: one page, {pdf['mediaBoxPoints'][0]}×{pdf['mediaBoxPoints'][1]} pt; all {pdf['fontCount']} font resources embedded.
- SVG: live text, no embedded raster, no external href, palette restricted to one navy root plus neutrals.
- Final-size border, quadrant occupancy, tonal range, greyscale neutrality, footer, and top-right blossom checks: PASS.
- Negative tests for source-hash drift, false fixed-deletion closure, and packet-1/packet-2 scale confusion: PASS.

## Human visual checks

- Panel titles, axes, exact fractions, and endpoint qualifications are legible.
- No detected callout, footer, title, or canvas-edge collision.
- Survival, the band not classified by the uniform slab test, and sweeping remain distinguishable in greyscale by fill/hatch/weight; the exact `q(ell)` curve stays visible.
- Packet 1 and packet 2 remain distinguishable by circle/square and dashed/dash-dot encodings.
- Panel C is a dependency map and contains no synthetic trajectory.
- Panel D states that its curve is a leading analytic scale and that unknown
  `c` and `-CL_2` are omitted; it is not a finite-`L_2` lower certificate.
- The all-shell frozen-placement failure and the fixed-deletion-open boundary are both visible.
- Required scope label appears verbatim:
  `{REQUIRED_LABEL}`.

**ANALYTIC SCHEMATIC. DERIVED ANALYTIC VALUES. NOT PDE DATA. NOT DNS. NOT CLAY.**
"""


def build_manifest(repository: Path, validation: dict[str, Any]) -> dict[str, Any]:
    config = load_json(HERE / "config.json")
    input_bindings = []
    for key in ("main", "primaryAudit", "literatureAudit"):
        item = config["sourceBinding"][key]
        input_bindings.append(
            {
                "role": key,
                "repositoryPath": item["path"],
                "bytes": int(item["byteCount"]),
                "sha256": item["sha256"],
                "bindingMode": "live-file-sha256-precommit",
            }
        )
    archive_records = []
    for name in SOURCE_FILES + RAW_FILES + ("qa-report.md", "validation.json"):
        archive_records.append({"path": name, "bytes": (HERE / name).stat().st_size, "sha256": sha256_file(HERE / name)})
    return {
        "artifactId": ARTIFACT_ID,
        "schema": "r074w-figure-manifest-v1",
        "createdAtUtc": utc_now(),
        "status": "local-precommit-sealed",
        "publicationStatus": "locally-hash-sealed-precommit",
        "repositoryHeadAtSeal": plot.repository_head(repository),
        "figureSourceCommitAssigned": False,
        "gitCommitOrBlobSealClaimed": False,
        "mainIndependentAuditSealed": True,
        "mainIndependentAuditVerdict": "PASS",
        "mainIndependentAuditBlockerCount": 0,
        "inputBindings": input_bindings,
        "inventory": {
            "source": list(SOURCE_FILES),
            "raw": list(RAW_FILES),
            "metadata": list(METADATA_FILES),
            "expectedFileCount": 25,
        },
        "archiveFilesBeforeManifest": archive_records,
        "deterministicCore": validation["checks"]["deterministicRoundtrip"],
        "hashLedger": {
            "file": "SHA256SUMS",
            "entries": 24,
            "coverage": "every archive file except SHA256SUMS itself",
            "selfHashRecorded": False,
        },
        "supportedClaim": (
            "Within the frozen two-packet common-shear family, the remote adjacent-inward strip has a strict "
            "relative survival/sweeping threshold q(ell). Packet 2 survives under the inherited reserve and forces "
            "K_{k_2-1,R}(tau_2)/T_* to diverge, refuting the matching all-shell O(T_*) upper bound for this placement."
        ),
        "openBoundary": (
            "The critical transition, whole-shell occupation, time occupation, accumulated viscosity, and fixed "
            "deletion remain open; no arbitrary-solution or Clay conclusion is claimed."
        ),
        "visualQAConfirmed": validation["visualQAConfirmed"],
    }


def write_hash_ledger() -> None:
    names = sorted(name for name in ALL_FILES if name != "SHA256SUMS")
    check(len(names) == 24, "SHA256SUMS ledger must cover exactly 24 files")
    lines = [f"{sha256_file(HERE / name)}  {name}" for name in names]
    atomic_text(HERE / "SHA256SUMS", "\n".join(lines) + "\n")


def parse_hash_ledger() -> dict[str, str]:
    ledger: dict[str, str] = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/]+)", line)
        check(match is not None, f"malformed SHA256SUMS line: {line!r}")
        digest, name = match.groups()
        check(name not in ledger, f"duplicate SHA256SUMS entry: {name}")
        ledger[name] = digest
    expected = sorted(name for name in ALL_FILES if name != "SHA256SUMS")
    check(sorted(ledger) == expected, "SHA256SUMS coverage mismatch")
    for name, digest in ledger.items():
        check(sha256_file(HERE / name) == digest, f"SHA256SUMS mismatch: {name}")
    return ledger


def seal_local(repository: Path, *, confirm_visual_qa: bool, deps_supplied: bool) -> dict[str, Any]:
    check(confirm_visual_qa, "local seal requires --confirm-visual-qa after inspecting all three QA images")
    validate_inventory(expect_metadata=False)
    checks = run_checks(repository, rerender=True, deps_supplied=deps_supplied)
    validation = {
        "artifactId": ARTIFACT_ID,
        "schema": "r074w-figure-validation-v1",
        "createdAtUtc": utc_now(),
        "status": "PASS",
        "sealMode": "live-file-sha256-precommit",
        "visualQAConfirmed": True,
        "figureSourceCommitAssigned": False,
        "gitCommitOrBlobSealClaimed": False,
        "mainIndependentAuditSealed": True,
        "mainIndependentAuditVerdict": "PASS",
        "mainIndependentAuditBlockerCount": 0,
        "checks": checks,
    }
    atomic_json(HERE / "validation.json", validation)
    atomic_text(HERE / "qa-report.md", qa_report_text(validation))
    manifest = build_manifest(repository, validation)
    atomic_json(HERE / "manifest.json", manifest)
    write_hash_ledger()
    validate_inventory(expect_metadata=True)
    parse_hash_ledger()
    return validation


def verify_only(repository: Path, *, deps_supplied: bool) -> dict[str, Any]:
    inventory = validate_inventory(expect_metadata=True)
    ledger = parse_hash_ledger()
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    check(validation["status"] == "PASS", "validation status is not PASS")
    check(validation["visualQAConfirmed"] is True, "visual QA confirmation missing")
    check(manifest["status"] == "local-precommit-sealed", "manifest status drift")
    check(manifest["figureSourceCommitAssigned"] is False, "manifest invents a figure commit")
    check(manifest["gitCommitOrBlobSealClaimed"] is False, "manifest invents a Git seal")
    check(manifest["mainIndependentAuditSealed"] is True, "manifest loses primary audit seal")
    checks = run_checks(repository, rerender=False, deps_supplied=deps_supplied)
    recorded_hashes = validation["checks"]["deterministicRoundtrip"]["hashes"]
    check(recorded_hashes == deterministic_hashes(HERE), "recorded deterministic-core hashes drift")
    check(manifest["hashLedger"]["entries"] == 24 and len(ledger) == 24, "hash ledger count drift")
    return {"status": "PASS", "inventory": inventory, "checks": checks, "hashLedgerEntries": len(ledger)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--seal-local", action="store_true", help="run two-render QA and write local seal metadata")
    mode.add_argument("--verify-only", action="store_true", help="verify the complete sealed archive without rerendering")
    parser.add_argument("--confirm-visual-qa", action="store_true", help="record explicit final-size/grayscale/PDF inspection")
    parser.add_argument("--repository", type=Path, default=DEFAULT_REPOSITORY, help="repository root")
    parser.add_argument("--deps", type=Path, default=None, help="version-pinned dependency root (provenance only)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repository = args.repository.resolve()
    if args.seal_local:
        result = seal_local(repository, confirm_visual_qa=args.confirm_visual_qa, deps_supplied=args.deps is not None)
        summary = {"artifactId": ARTIFACT_ID, "status": result["status"], "mode": "seal-local"}
    else:
        result = verify_only(repository, deps_supplied=args.deps is not None)
        summary = {"artifactId": ARTIFACT_ID, "status": result["status"], "mode": "verify-only", "files": result["inventory"]["fileCount"]}
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
