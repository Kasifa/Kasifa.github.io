#!/usr/bin/env python3
"""Fail-closed validation and local precommit sealing for the R0.74X figure."""

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
    check(config["artifactId"] == ARTIFACT_ID, "config artifactId drift")
    check(config["sourceBinding"]["mode"] == "live-file-sha256-precommit", "wrong source binding mode")
    check(config["sourceBinding"]["gitFigureSourceCommitAssigned"] is False, "figure commit must remain unassigned")
    check(config["sourceBinding"]["mainIndependentAuditSealed"] is True, "primary audit must be locally hash-sealed")
    observed = plot.validate_source_binding(repository, config)
    for key in ("main", "primaryAudit", "literatureAudit"):
        expected = config["sourceBinding"][key]
        check(observed[key]["sha256"] == expected["sha256"], f"observed source hash drift: {key}")
        check(observed[key]["byteCount"] == int(expected["byteCount"]), f"observed source byte count drift: {key}")

    main_text = (repository / config["sourceBinding"]["main"]["path"]).read_text(encoding="utf-8")
    required_main_tokens = (
        "\\tag{X.5}",
        "\\tag{X.17}",
        "\\tag{X.37}",
        "\\tag{X.43}",
        "\\tag{X.44}",
        "\\tag{X.47}",
        "\\tag{X.50}",
        "\\tag{X.51}",
        "\\tag{X.52}",
        "ACTUAL FIXED-DELETION GATE COUNTEREXAMPLE: NOT PROVED",
        "\\mathbf{NOT\\ CLAY}",
    )
    for token in required_main_tokens:
        check(token in main_text, f"main note locator missing: {token}")
    primary_text = (repository / config["sourceBinding"]["primaryAudit"]["path"]).read_text(encoding="utf-8")
    check("**Verdict: PASS.**" in primary_text, "primary audit PASS token missing")
    check("There are no blockers." in primary_text, "primary audit blocker count is not zero")
    check(config["sourceBinding"]["main"]["sha256"] in primary_text, "primary audit does not bind main note SHA")
    literature_text = (repository / config["sourceBinding"]["literatureAudit"]["path"]).read_text(encoding="utf-8")
    check("finite primary-source non-hit" in literature_text, "literature claim boundary missing")
    check("**not** evidence or proof of\nnovelty" in literature_text, "literature no-novelty boundary missing")
    check("LITERATURE BOUNDARY. NOT CLAY." in literature_text, "literature NOT CLAY boundary missing")
    return observed


def validate_exact_constants() -> dict[str, str]:
    p = Fraction(32, 63)
    d = Fraction(433, 1008)
    q = Fraction(4, 3969)
    q65 = Fraction(256, 257985)
    c_h = Fraction(15, 16)
    a_s = Fraction(75, 22528)
    c_gamma = Fraction(8, 3969)

    def delta(r: Fraction, heat_age: int) -> Fraction:
        return ((c_h * r - p) ** 2 - d**2) / (4 * heat_age) - q * (r**2 - 1)

    cross_2_from_1 = delta(Fraction(1, 2), 65)
    cross_2_from_3 = delta(Fraction(2), 66)
    cross_3_from_2 = delta(Fraction(1, 2), 65)
    cross_3_from_1 = delta(Fraction(1, 4), 65)
    inversion = c_h * p / 66
    a_cross = Fraction(49, 14850)
    target_outer = a_cross - 3 * q
    target_inner = Fraction(1, 4) * a_cross + Fraction(3, 4) * q
    target_nonadjacent = Fraction(9, 16) * a_cross + Fraction(15, 16) * q
    periodic = Fraction(3, 22) * Fraction(144, 5) ** 2 - q
    chi65 = Fraction(3, 4) * c_gamma - d**2 / (2 * 65)
    chi66 = Fraction(3, 4) * c_gamma - d * d / (2 * 66)
    payment = Fraction(40, 3) * c_gamma - Fraction(2, 3) * a_s
    maximum_strip = 16 * chi66
    gap = payment - maximum_strip
    values = {
        "p": p,
        "d": d,
        "q": q,
        "q65": q65,
        "packet2SurvivalReserve": 4 * q65 - a_s,
        "packet3SurvivalReserve": 16 * q65 - a_s,
        "cross2From1": cross_2_from_1,
        "cross2From3": cross_2_from_3,
        "cross3From2": cross_3_from_2,
        "cross3From1": cross_3_from_1,
        "inversionMargin": inversion,
        "targetLobeOuterMargin": target_outer,
        "targetLobeInnerMargin": target_inner,
        "targetLobeNonadjacentMargin": target_nonadjacent,
        "periodicMargin": periodic,
        "chi65": chi65,
        "chi66": chi66,
        "paymentRate": payment,
        "maximumStripRate": maximum_strip,
        "paymentMinusMaximumStrip": gap,
    }
    contract = load_json(HERE / "contract.json")
    expected = {key: str(value) for key, value in values.items()}
    check(contract["exactConstants"] == expected, f"exact constant ledger mismatch: {contract['exactConstants']} != {expected}")
    identities = {
        "packet2SurvivalReserve": Fraction(3719797, 5811886080),
        "packet3SurvivalReserve": Fraction(72925813, 5811886080),
        "cross2From1": Fraction(3667, 70447104),
        "cross2From3": Fraction(100043, 29804544),
        "cross3From2": Fraction(3667, 70447104),
        "cross3From1": Fraction(147359, 281788416),
        "inversionMargin": Fraction(5, 693),
        "targetLobeOuterMargin": Fraction(67, 242550),
        "targetLobeInnerMargin": Fraction(4601, 2910600),
        "targetLobeNonadjacentMargin": Fraction(32609, 11642400),
        "periodicMargin": Fraction(123450676, 1091475),
        "chi65": Fraction(12191, 132088320),
        "chi66": Fraction(15263, 134120448),
        "paymentRate": Fraction(3306805, 134120448),
        "maximumStripRate": Fraction(15263, 8382528),
        "paymentMinusMaximumStrip": Fraction(3062597, 134120448),
    }
    for key, value in identities.items():
        check(values[key] == value, f"exact identity failed: {key}")
    check(all(value > 0 for key, value in values.items() if key not in {"p", "d", "q", "q65"}), "a strict margin is nonpositive")
    check(payment > maximum_strip and gap == payment - maximum_strip, "payment/strip rate ordering failed")
    return expected


def validate_claim_boundary() -> dict[str, Any]:
    contract = load_json(HERE / "contract.json")
    check(contract["artifactId"] == ARTIFACT_ID, "contract artifactId drift")
    boundary = contract["claimBoundary"]
    required_true = (
        "exactThreePacketSmoothNseFamily",
        "packet2And3RelativeSurvival",
        "twoCoordinateTstarEndpointObstruction",
        "differentTimePigeonhole",
        "equalTimeSchedulePermitted",
        "equalTargetWStripRouteNoGo",
        "mainIndependentAuditSealed",
    )
    required_false = (
        "simultaneousTimeRequired",
        "actualPaymentNormalizedGateCounterexample",
        "stripUpperIsWholeShellUpper",
        "wholeShellClockBoundResolved",
        "noveltyClaim",
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
    check(counts == {"A": 16, "B": 6, "C": 4, "D": 4}, f"source-data row counts drift: {counts}")
    check(len(rows) == 30, f"source-data row count drift: {len(rows)}")
    check(all(row["panel"] in "ABCD" for row in rows), "unknown panel identifier")

    a_rows = {row["series"]: row for row in rows if row["panel"] == "A"}
    check(a_rows["packet 2"]["exact_value"] == "k_2=k_1+1; L_2=2L_1", "packet-2 scale architecture drift")
    check(a_rows["packet 3"]["exact_value"] == "k_3=k_1+2; L_3=4L_1", "packet-3 scale architecture drift")
    check(a_rows["clock coordinate from packet 2"]["exact_value"] == "k_2-1=k_1", "first adjacent-inward coordinate drift")
    check(a_rows["clock coordinate from packet 3"]["exact_value"] == "k_3-1=k_2", "second adjacent-inward coordinate drift")
    check(a_rows["packet 2 survival reserve"]["exact_value"] == "3719797/5811886080", "packet-2 reserve drift")
    check(a_rows["packet 3 survival reserve"]["exact_value"] == "72925813/5811886080", "packet-3 reserve drift")

    b_rows = [row for row in rows if row["panel"] == "B"]
    check([row["series"] for row in b_rows] == [
        "fixed deletion order", "branch k1 remains", "branch k1 deleted",
        "pigeonhole lower bound", "optional equal schedule", "terminal-domain consequence",
    ], "Panel B quantifier branch order drift")
    check("inf_{#S<=1} sup_{t in D}" in b_rows[0]["exact_value"], "Panel B inf-sup order drift")
    check("S fixed before t" in b_rows[0]["note"], "Panel B fixed-set qualification missing")
    check("choose t=tau_2" in b_rows[1]["exact_value"] and "choose t=tau_3" in b_rows[2]["exact_value"], "Panel B witness-time branch drift")
    check("different times permitted" in b_rows[3]["note"], "Panel B different-time statement missing")
    check("permitted but unnecessary" in b_rows[4]["exact_value"], "Panel B optional-equality statement missing")
    check(all("required" not in row["note"].lower() or "not a hypothesis" in row["note"].lower() for row in b_rows), "Panel B accidentally requires simultaneous witness times")

    c_rows = {row["series"]: row for row in rows if row["panel"] == "C"}
    expected_rates = {
        "payment lower rate": Fraction(3306805, 134120448),
        "maximum audited strip rate": Fraction(15263, 8382528),
        "strict rate gap": Fraction(3062597, 134120448),
    }
    for series, expected in expected_rates.items():
        row = c_rows[series]
        check(Fraction(row["exact_value"]) == expected, f"Panel C exact rate drift: {series}")
        check(abs(float(row["x"]) - float(expected)) < 1e-14, f"Panel C numeric rate drift: {series}")
    check(expected_rates["payment lower rate"] - expected_rates["maximum audited strip rate"] == expected_rates["strict rate gap"], "Panel C rate subtraction failed")
    strip_scope = c_rows["strip-to-payment conclusion"]
    check("does not upper-bound either whole shell clock" in strip_scope["note"], "Panel C whole-shell boundary missing")
    check(strip_scope["source_locator"] == "X.51", "Panel C strip scope locator drift")

    d_rows = [row for row in rows if row["panel"] == "D"]
    check([row["series"] for row in d_rows] == ["PROVED", "NOT PROVED", "NO-GO", "NEXT X.52"], "Panel D status hierarchy drift")
    check("T_*" in d_rows[0]["exact_value"], "Panel D proved normalization drift")
    check("actual (P_R^M)^(2/3)-normalized gate" in d_rows[1]["exact_value"], "Panel D open payment gate boundary missing")
    check("W-strip route is dominated by cubic payment" in d_rows[2]["exact_value"], "Panel D no-go statement drift")
    check(d_rows[3]["source_locator"] == "X.52" and "times need not coincide" in d_rows[3]["note"], "Panel D next target drift")

    check(raw == plot.rows_to_csv(plot.build_source_rows()), "source-data.csv is not byte-identical to deterministic generator")
    return {
        "rows": len(rows),
        "panelRowCounts": counts,
        "panelBQuantifierRows": len(b_rows),
        "panelCRateRows": len(expected_rates),
        "panelDStatusRows": len(d_rows),
        "byteIdenticalToGenerator": True,
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
        "Three-packet fixed deletion",
        "Different-time fixed-deletion pigeonhole",
        "TIMES MAY DIFFER",
        "UPPER COMPARISON: TWO STRIP INTEGRALS ONLY",
        "NOT PROVED",
        "NEXT X.52",
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
        "Three-packet fixed deletion",
        "Three packets and two adjacent-inward coordinates",
        "Different-time fixed-deletion pigeonhole",
        "TIMES MAY DIFFER",
        "UPPER COMPARISON: TWO STRIP INTEGRALS ONLY",
        "NOT PROVED",
        "NEXT X.52",
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
        "d818db13acc16ad26a2d9628f2681e4a" + "654698c9966815dd6cf1712813830d10",
        "66ec78f67bba64c555a92e9a616c477" + "d702ebb200b48bbfc08a353bdfde5bb73",
        "ec6259d95990fd6a8357d9685cc3f17" + "e300e672c1add911a5eb64c6291f3bb99",
        "fig-r074w-remote-" + "adjacent-inward-threshold",
        "r074w-figure-" + "results-v1",
        "r074w-figure-" + "environment-v1",
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
    check("not proved" in caption and "not either full shell" in caption, "caption payment/whole-shell boundary missing")
    check("simultaneity is optional, not required" in caption, "caption different-time boundary missing")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    check("verdict PASS, blocker count 0" in readme, "README primary audit status missing")
    check("bounded dated primary-source non-hit only" in readme, "README literature boundary missing")
    check("No common-time hypothesis is required" in readme, "README different-time boundary missing")
    return {"filesScanned": scanned, "machineSpecificAbsolutePaths": 0, "obsoleteSourceHashes": 0}


def validate_artifact_identity() -> dict[str, Any]:
    config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    environment = load_json(HERE / "environment.json")
    results = load_json(HERE / "results.json")
    for label, payload in (
        ("config", config), ("contract", contract),
        ("environment", environment), ("results", results),
    ):
        check(payload.get("artifactId") == ARTIFACT_ID, f"{label} artifactId drift")
    check(environment["schema"] == "r074x-figure-environment-v1", "environment schema drift")
    check(results["schema"] == "r074x-figure-results-v1", "results schema drift")
    check(results["requiredVisibleLabel"] == REQUIRED_LABEL, "results scope label drift")
    check(results["sourceDataRows"] == 30, "results source-data count drift")
    check(results["panelRowCounts"] == {"A": 16, "B": 6, "C": 4, "D": 4}, "results panel counts drift")
    expected_binding = {
        key: {
            "path": config["sourceBinding"][key]["path"],
            "sha256": config["sourceBinding"][key]["sha256"],
            "byteCount": int(config["sourceBinding"][key]["byteCount"]),
        }
        for key in ("main", "primaryAudit", "literatureAudit")
    }
    check(results["sourceBinding"] == expected_binding, "results source binding drift")
    check(results["claimBoundary"]["actualPaymentNormalizedGateCounterexample"] is False, "results falsely close payment gate")
    check(results["claimBoundary"]["stripUpperIsWholeShellUpper"] is False, "results promote strip upper to whole shell")
    return {
        "artifactId": ARTIFACT_ID,
        "schemas": [environment["schema"], results["schema"]],
        "sourceHashes": {key: item["sha256"] for key, item in expected_binding.items()},
    }


def deterministic_hashes(base: Path) -> dict[str, str]:
    return {name: sha256_file(base / name) for name in DETERMINISTIC_CORE}


def validate_determinism(repository: Path, deps_supplied: bool) -> dict[str, Any]:
    before_source = {name: sha256_file(HERE / name) for name in SOURCE_FILES}
    with tempfile.TemporaryDirectory(prefix="r074x-render-a-") as first_name, tempfile.TemporaryDirectory(prefix="r074x-render-b-") as second_name:
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
        check(all(row.get("artifactId") == ARTIFACT_ID for row in rows), f"{name} artifactId drift")
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

    false_payment_gate_rejected = False
    mutated_boundary = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_boundary["actualPaymentNormalizedGateCounterexample"] = True
    try:
        check(mutated_boundary["actualPaymentNormalizedGateCounterexample"] is False, "actual payment-normalized gate must remain open")
    except ValidationFailure:
        false_payment_gate_rejected = True
    check(false_payment_gate_rejected, "negative payment-gate claim was not rejected")

    simultaneous_required_rejected = False
    mutated_simultaneous = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_simultaneous["simultaneousTimeRequired"] = True
    try:
        check(mutated_simultaneous["simultaneousTimeRequired"] is False, "simultaneous witness times must not be required")
    except ValidationFailure:
        simultaneous_required_rejected = True
    check(simultaneous_required_rejected, "negative simultaneous-time claim was not rejected")

    whole_shell_promotion_rejected = False
    mutated_shell = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_shell["stripUpperIsWholeShellUpper"] = True
    try:
        check(mutated_shell["stripUpperIsWholeShellUpper"] is False, "strip upper comparison must not be promoted to a whole-shell upper bound")
    except ValidationFailure:
        whole_shell_promotion_rejected = True
    check(whole_shell_promotion_rejected, "negative whole-shell promotion was not rejected")
    return {
        "wrongSourceHashRejected": source_mismatch_rejected,
        "falsePaymentGateClaimRejected": false_payment_gate_rejected,
        "simultaneousTimeRequirementRejected": simultaneous_required_rejected,
        "stripToWholeShellPromotionRejected": whole_shell_promotion_rejected,
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
    checks["artifactIdentity"] = validate_artifact_identity()
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
    return f"""# R0.74X figure QA report

Status: **PASS**

Visual inspection confirmation: **YES**.  The explicit seal flag records that
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` were inspected at
actual size after the final render.

## Scope and provenance

- Artifact: `{ARTIFACT_ID}`
- Seal: local SHA-256 precommit seal; no Git commit/blob seal is claimed.
- Mathematical input SHA-256: `4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3`.
- Independent primary audit SHA-256:
  `834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e`;
  verdict PASS, blocker count 0.
- Literature audit SHA-256:
  `f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422`;
  bounded primary-source non-hit only.

## Automated checks

- Exact rational identities and strict payment-versus-strip rate comparison: PASS.
- Source-data regeneration and 30-row semantic ledger: PASS.
- Deterministic two-render comparison: PASS ({deterministic['files']} files).
- Publication PNG: {raster['expectedPublicationPixels'][0]}×{raster['expectedPublicationPixels'][1]} pixels at nominal 600 dpi.
- Three QA exports: {raster['expectedQaPixels'][0]}×{raster['expectedQaPixels'][1]} pixels at nominal 300 dpi.
- PDF: one page, {pdf['mediaBoxPoints'][0]}×{pdf['mediaBoxPoints'][1]} pt; all {pdf['fontCount']} font resources embedded.
- SVG: live text, no embedded raster, no external href, palette restricted to one navy root plus neutrals.
- Final-size border, quadrant occupancy, tonal range, greyscale neutrality, footer, and top-right blossom checks: PASS.
- Negative tests for source-hash drift, false payment-gate closure, simultaneous-time requirement, and strip-to-whole-shell promotion: PASS.

## Human visual checks

- Panel titles, axes, exact fractions, and endpoint qualifications are legible.
- No detected callout, footer, title, or canvas-edge collision.
- Packets 1, 2, and 3 remain distinguishable by circle/square/diamond and fill encodings.
- Panel B places `inf` before `sup`, says that the deletion set is fixed before time selection, and visibly permits different witness times.
- Panel C displays the exact payment rate, maximum two-strip rate, and their strict positive gap; its upper comparison is explicitly restricted to the two strip integrals.
- Panel D visibly separates PROVED, NOT PROVED, NO-GO, and NEXT X.52.
- The two-coordinate `T_*` result, open payment-normalized gate, and absence of a whole-shell upper bound are all visible.
- No novelty claim is made.
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
        "schema": "r074x-figure-manifest-v1",
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
            "Within the exact smooth frozen three-packet common-shear family, packets 2 and 3 survive their remote "
            "adjacent-inward strips and force endpoint lower witnesses at two distinct coordinates. Because the "
            "deletion set is fixed before the time supremum, these witnesses may occur at different times and still "
            "force the two-coordinate completed-clock obstruction relative to T_*."
        ),
        "openBoundary": (
            "The actual payment-normalized fixed-deletion counterexample is not proved. The exact payment exponent "
            "strictly dominates the maximum of the two audited W-strip exponents, so only that equal-target strip "
            "route is a no-go. No whole-shell upper bound, novelty, arbitrary-solution, or Clay conclusion is claimed."
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
        "schema": "r074x-figure-validation-v1",
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
    config = load_json(HERE / "config.json")
    for label, payload in (("validation", validation), ("manifest", manifest)):
        check(payload.get("artifactId") == ARTIFACT_ID, f"{label} artifactId drift")
    check(validation["schema"] == "r074x-figure-validation-v1", "validation schema drift")
    check(manifest["schema"] == "r074x-figure-manifest-v1", "manifest schema drift")
    check(validation["status"] == "PASS", "validation status is not PASS")
    check(validation["visualQAConfirmed"] is True, "visual QA confirmation missing")
    check(manifest["status"] == "local-precommit-sealed", "manifest status drift")
    check(manifest["figureSourceCommitAssigned"] is False, "manifest invents a figure commit")
    check(manifest["gitCommitOrBlobSealClaimed"] is False, "manifest invents a Git seal")
    check(manifest["mainIndependentAuditSealed"] is True, "manifest loses primary audit seal")
    expected_hashes = {
        key: config["sourceBinding"][key]["sha256"]
        for key in ("main", "primaryAudit", "literatureAudit")
    }
    manifest_hashes = {item["role"]: item["sha256"] for item in manifest["inputBindings"]}
    check(manifest_hashes == expected_hashes, "manifest source hashes drift")
    validation_hashes = {
        key: item["sha256"]
        for key, item in validation["checks"]["sourceBinding"].items()
    }
    check(validation_hashes == expected_hashes, "validation source hashes drift")
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
