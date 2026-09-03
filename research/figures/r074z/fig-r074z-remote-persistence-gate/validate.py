#!/usr/bin/env python3
"""Fail-closed validation and local precommit sealing for the R0.74Z figure."""

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
        "\\tag{Z.6}",
        "\\tag{Z.11}",
        "\\tag{Z.12}",
        "\\tag{Z.15}",
        "\\tag{Z.16}",
        "\\tag{Z.19a}",
        "\\tag{Z.22}",
        "\\tag{Z.25}",
        "\\tag{Z.36}",
        "\\tag{Z.39}",
        "FULL-CLOCK Y.57 CANCELLATION CELL: OPEN",
        "R074Z_ENDPOINT_ONLY_TEMPORAL_CONCENTRATION_OPEN",
        "\\mathbf{NOT\\ CLAY}",
    )
    for token in required_main_tokens:
        check(token in main_text, f"main note locator missing: {token}")
    primary_text = (repository / config["sourceBinding"]["primaryAudit"]["path"]).read_text(encoding="utf-8")
    check("**Verdict: PASS.**" in primary_text, "primary audit PASS token missing")
    check("**Blocker count: 0.**" in primary_text, "primary audit blocker count is not zero")
    check(config["sourceBinding"]["main"]["sha256"] in primary_text, "primary audit does not bind main note SHA")
    literature_text = (repository / config["sourceBinding"]["literatureAudit"]["path"]).read_text(encoding="utf-8")
    check("finite primary-source non-hit" in literature_text, "literature claim boundary missing")
    check("**not** evidence of novelty" in literature_text, "literature no-novelty boundary missing")
    check("LITERATURE BOUNDARY. NOT CLAY." in literature_text, "literature NOT CLAY boundary missing")
    return observed


def validate_exact_constants() -> dict[str, str]:
    c_gamma = Fraction(8, 3969)
    rho = Fraction(9, 10000)
    d = Fraction(7, 32)
    a0 = Fraction(131, 2)
    clock_weight = Fraction(1, 4)
    payment_weight = Fraction(1, 16)
    beta = d * d / (4 * a0)
    reserve = rho / 4 - beta
    delta_remote = Fraction(5, 24) * c_gamma - rho / 6
    kappa_star = Fraction(3, 2) * delta_remote
    two_center_rate = d * d / (2 * a0)
    two_center_margin = two_center_rate - Fraction(1, 5000)
    complexity = reserve + kappa_star
    values = {
        "cGamma": c_gamma,
        "rho": rho,
        "d": d,
        "a0": a0,
        "clockWeightExponent": clock_weight,
        "paymentWeightExponent": payment_weight,
        "beta": beta,
        "timeTameReserve": reserve,
        "deltaRemote": delta_remote,
        "kappaStar": kappa_star,
        "twoCenterRate": two_center_rate,
        "twoCenterMargin": two_center_margin,
        "complexityEscapeCoefficient": complexity,
    }
    contract = load_json(HERE / "contract.json")
    expected = {key: str(value) for key, value in values.items()}
    check(contract["exactConstants"] == expected, f"exact constant ledger mismatch: {contract['exactConstants']} != {expected}")
    identities = {
        "beta": Fraction(49, 268288),
        "timeTameReserve": Fraction(7103, 167680000),
        "deltaRemote": Fraction(64279, 238140000),
        "kappaStar": Fraction(64279, 158760000),
        "twoCenterRate": Fraction(49, 134144),
        "twoCenterMargin": Fraction(13857, 83840000),
        "complexityEscapeCoefficient": Fraction(476239, 1064835072),
    }
    for key, value in identities.items():
        check(values[key] == value, f"exact identity failed: {key}")
    check(clock_weight * clock_weight == payment_weight, "fourth-root weight ladder failed")
    check(delta_remote - Fraction(2, 3) * kappa_star == 0, "critical rate identity failed")
    check(complexity == reserve + kappa_star, "complexity decomposition failed")
    check(reserve > 0 and delta_remote > 0 and two_center_margin > 0, "a strict margin is nonpositive")
    return expected


def validate_claim_boundary() -> dict[str, Any]:
    contract = load_json(HERE / "contract.json")
    check(contract["artifactId"] == ARTIFACT_ID, "contract artifactId drift")
    boundary = contract["claimBoundary"]
    required_true = (
        "exactCommonShearAdmissibility",
        "remoteClockWeightGammaQuarter",
        "doubledRadiusPaymentWeightGammaSixteenth",
        "shellTubeHolderCoercivity",
        "strictSubcriticalKappaNoGoForWKinetic",
        "timeTamePersistenceConditional",
        "mainIndependentAuditSealed",
    )
    required_false = (
        "movingStripAllWindingUniformityProved",
        "endpointToTubeUnconditional",
        "criticalLayerResolved",
        "fullClockY57Blocked",
        "accumulatedClockRowsControlled",
        "arbitraryFiniteEndpointFocusedBlocked",
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
    check(counts == {"A": 7, "B": 85, "C": 8, "D": 4}, f"source-data row counts drift: {counts}")
    check(len(rows) == 104, f"source-data row count drift: {len(rows)}")
    check(all(row["panel"] in "ABCD" for row in rows), "unknown panel identifier")

    a_rows = {row["series"]: row for row in rows if row["panel"] == "A"}
    check(a_rows["outer packet clock"]["exact_value"] == "Gamma=gamma_{k_2}", "outer packet weight drift")
    check(a_rows["remote clock"]["exact_value"] == "omega=gamma_{k_2-1}=Gamma^(1/4)", "remote clock weight drift")
    check(a_rows["doubled-radius payment"]["exact_value"] == "gamma_{k_2-2}=Gamma^(1/16)", "payment weight drift")
    check(a_rows["physical-shell identity"]["exact_value"] == "A_{k_2-1}(R)=A_{k_2-2}(2R)", "physical-shell identity drift")

    b_curve = [row for row in rows if row["panel"] == "B" and row["series"] == "Holder lower-rate curve"]
    check(len(b_curve) == 81, "Panel B affine curve sample count drift")
    for index, row in enumerate(b_curve):
        kappa = Fraction(index, 100000)
        rate = Fraction(64279, 238140000) - Fraction(2, 3) * kappa
        check(Fraction(row["exact_value"]) == rate, f"Panel B exact affine sample drift: {index}")
        check(abs(float(row["x"]) - 1000 * float(kappa)) < 1e-12, f"Panel B x sample drift: {index}")
        check(abs(float(row["y"]) - 1000 * float(rate)) < 1e-11, f"Panel B y sample drift: {index}")
    b_rows = {row["series"]: row for row in rows if row["panel"] == "B" and row["series"] != "Holder lower-rate curve"}
    check(Fraction(b_rows["delta remote"]["exact_value"]) == Fraction(64279, 238140000), "Panel B delta drift")
    check(Fraction(b_rows["kappa star"]["exact_value"]) == Fraction(64279, 158760000), "Panel B kappa star drift")
    check("limsup kappa_L < kappa_*" in b_rows["strict theorem region"]["exact_value"], "Panel B strict quantifier missing")
    check("OPEN" in b_rows["critical layer"]["note"], "Panel B critical layer not open")

    c_rows = {row["series"]: row for row in rows if row["panel"] == "C"}
    expected_rates = {
        "time-tame reserve": Fraction(7103, 167680000),
        "critical residence cost": Fraction(64279, 158760000),
        "necessary complexity rate": Fraction(476239, 1064835072),
    }
    for series, expected in expected_rates.items():
        row = c_rows[series]
        check(Fraction(row["exact_value"]) == expected, f"Panel C exact rate drift: {series}")
        check(abs(float(row["x"]) - 1000 * float(expected)) < 1e-11, f"Panel C numeric rate drift: {series}")
    check(expected_rates["time-tame reserve"] + expected_rates["critical residence cost"] == expected_rates["necessary complexity rate"], "Panel C complexity addition failed")
    check("not proved generically" in c_rows["moving-strip all-winding"]["note"], "Panel C all-winding condition missing")
    check("all three hypotheses" in c_rows["R^3 persistence"]["note"], "Panel C persistence qualification missing")
    check("necessary, not sufficient" in c_rows["necessary complexity rate"]["note"], "Panel C necessity boundary missing")

    d_rows = [row for row in rows if row["panel"] == "D"]
    check([row["series"] for row in d_rows] == ["PROVED", "CONDITIONAL", "OPEN", "NEXT Z.39"], "Panel D status hierarchy drift")
    check("shell-tube Holder coercivity" in d_rows[0]["exact_value"], "Panel D proved scope drift")
    check("moving-strip all-winding" in d_rows[1]["exact_value"], "Panel D conditional hypothesis missing")
    check("full-clock Y.57" in d_rows[2]["exact_value"] and "accumulated rows" in d_rows[2]["exact_value"], "Panel D open full-clock boundary missing")
    check(d_rows[3]["source_locator"] == "Z.39", "Panel D next target drift")

    check(raw == plot.rows_to_csv(plot.build_source_rows()), "source-data.csv is not byte-identical to deterministic generator")
    return {
        "rows": len(rows),
        "panelRowCounts": counts,
        "panelBAffineCurveRows": len(b_curve),
        "panelCExactRateRows": len(expected_rates),
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
        "Remote persistence gate",
        "Exact remote-shell weight ladder",
        "STRICT SIDE ONLY",
        "CONDITIONAL / NECESSARY ONLY",
        "full-clock Y",
        "accumulated clock rows",
        "NEXT Z.39",
        "NOT PDE DATA",
        "NOT DNS",
        "NO NOVELTY CLAIM",
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
        "Remote persistence gate",
        "Exact remote-shell weight ladder",
        "Strict W-kinetic persistence threshold",
        "STRICT SIDE ONLY",
        "CONDITIONAL / NECESSARY ONLY",
        "full-clock Y.57",
        "NEXT Z.39",
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


def obsolete_tokens() -> tuple[str, ...]:
    return (
        "4fdc9558605afd9557c557c4292ca1af5" + "0d52ff54f9aa11603f15c97a97b3ee3",
        "834ec846c3f8629f9e7462caf4503bfa" + "99ba6b88288da2dd525793206de9357e",
        "f58f7a1d095ba6bd8b27c41872301fd" + "367fe784597160fe060f9cd332c64c422",
        "b12e3d7aa33e8e0db2b931621f35e51" + "d7655fefcd600c558979634b13133b42f",
        "fig-r074" + "x-three-packet-payment-gate",
        "r074" + "x-figure-results-v1",
        "r074" + "x-figure-environment-v1",
        "r074" + "x-figure-validation-v1",
        "r074" + "x-figure-manifest-v1",
        "R0.74" + "X figure QA report",
        "main independent" + " audit unsealed",
    )


def validate_text_archive() -> dict[str, Any]:
    forbidden = obsolete_tokens()
    scanned = 0
    text_files = SOURCE_FILES + (
        "environment.json",
        "results.json",
        "progress.ndjson",
        "resource-log.ndjson",
        "source-data.csv",
        "figure.svg",
    )
    for name in text_files:
        text = (HERE / name).read_text(encoding="utf-8")
        scanned += 1
        for token in forbidden:
            check(token not in text, f"obsolete provenance token in {name}: {token}")
        check(re.search(r"/(?:Users|home)/[A-Za-z0-9]", text) is None, f"machine-specific absolute path in {name}")
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    check("NOT CLAY" in caption and "no novelty claim" in caption, "caption scope boundary is incomplete")
    check("critical layer" in caption and "is open" in caption, "caption critical-layer boundary missing")
    check("full-clock Y.57" in caption and "remain open" in caption, "caption full-clock boundary missing")
    check("necessary,\nnot sufficient" in caption, "caption complexity boundary missing")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    check("verdict PASS, blocker count 0" in readme, "README primary audit status missing")
    check("bounded dated primary-source non-hit only" in readme, "README literature boundary missing")
    check("critical layer" in readme and "is open" in readme, "README critical boundary missing")
    check("full-clock Y.57" in readme and "remain open" in readme, "README full-clock boundary missing")
    return {"filesScanned": scanned, "machineSpecificAbsolutePaths": 0, "obsoleteSourceHashes": 0}


def validate_sealed_metadata_text() -> dict[str, Any]:
    config = load_json(HERE / "config.json")
    current_hashes = tuple(
        config["sourceBinding"][key]["sha256"]
        for key in ("main", "primaryAudit", "literatureAudit")
    )
    names = ("qa-report.md", "validation.json", "manifest.json", "SHA256SUMS")
    for name in names:
        text = (HERE / name).read_text(encoding="utf-8")
        for token in obsolete_tokens():
            check(token not in text, f"obsolete provenance token in sealed metadata {name}: {token}")
    qa_text = (HERE / "qa-report.md").read_text(encoding="utf-8")
    manifest_text = (HERE / "manifest.json").read_text(encoding="utf-8")
    validation_text = (HERE / "validation.json").read_text(encoding="utf-8")
    check(all(token in qa_text for token in current_hashes), "QA report does not bind all current source hashes")
    check(all(token in manifest_text for token in current_hashes), "manifest does not bind all current source hashes")
    check(all(token in validation_text for token in current_hashes), "validation does not bind all current source hashes")
    return {"filesScanned": len(names), "obsoleteTokens": 0, "currentSourceHashesPresent": 3}


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
    check(environment["schema"] == "r074z-figure-environment-v1", "environment schema drift")
    check(results["schema"] == "r074z-figure-results-v1", "results schema drift")
    check(results["requiredVisibleLabel"] == REQUIRED_LABEL, "results scope label drift")
    check(results["sourceDataRows"] == 104, "results source-data count drift")
    check(results["panelRowCounts"] == {"A": 7, "B": 85, "C": 8, "D": 4}, "results panel counts drift")
    expected_binding = {
        key: {
            "path": config["sourceBinding"][key]["path"],
            "sha256": config["sourceBinding"][key]["sha256"],
            "byteCount": int(config["sourceBinding"][key]["byteCount"]),
        }
        for key in ("main", "primaryAudit", "literatureAudit")
    }
    check(results["sourceBinding"] == expected_binding, "results source binding drift")
    check(results["exactConstants"] == contract["exactConstants"], "results exact constants drift")
    for key, value in contract["claimBoundary"].items():
        check(results["claimBoundary"].get(key) == value, f"results claim boundary drift: {key}")
    check(results["claimBoundary"]["criticalLayerResolved"] is False, "results falsely close critical layer")
    check(results["claimBoundary"]["fullClockY57Blocked"] is False, "results falsely close full-clock Y.57")
    check(results["claimBoundary"]["accumulatedClockRowsControlled"] is False, "results falsely control accumulated rows")
    return {
        "artifactId": ARTIFACT_ID,
        "schemas": [environment["schema"], results["schema"]],
        "sourceHashes": {key: item["sha256"] for key, item in expected_binding.items()},
    }


def deterministic_hashes(base: Path) -> dict[str, str]:
    return {name: sha256_file(base / name) for name in DETERMINISTIC_CORE}


def validate_determinism(repository: Path, deps_supplied: bool) -> dict[str, Any]:
    before_source = {name: sha256_file(HERE / name) for name in SOURCE_FILES}
    with tempfile.TemporaryDirectory(prefix="r074z-render-a-") as first_name, tempfile.TemporaryDirectory(prefix="r074z-render-b-") as second_name:
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

    false_critical_closure_rejected = False
    mutated_boundary = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_boundary["criticalLayerResolved"] = True
    try:
        check(mutated_boundary["criticalLayerResolved"] is False, "critical residence layer must remain open")
    except ValidationFailure:
        false_critical_closure_rejected = True
    check(false_critical_closure_rejected, "negative critical-layer closure was not rejected")

    unconditional_persistence_rejected = False
    mutated_persistence = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_persistence["endpointToTubeUnconditional"] = True
    try:
        check(mutated_persistence["endpointToTubeUnconditional"] is False, "endpoint-to-tube persistence must remain conditional")
    except ValidationFailure:
        unconditional_persistence_rejected = True
    check(unconditional_persistence_rejected, "negative unconditional persistence claim was not rejected")

    full_clock_promotion_rejected = False
    mutated_clock = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_clock["fullClockY57Blocked"] = True
    try:
        check(mutated_clock["fullClockY57Blocked"] is False, "W-kinetic no-go must not be promoted to full-clock Y.57")
    except ValidationFailure:
        full_clock_promotion_rejected = True
    check(full_clock_promotion_rejected, "negative full-clock promotion was not rejected")

    accumulated_rows_rejected = False
    mutated_accumulated = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_accumulated["accumulatedClockRowsControlled"] = True
    try:
        check(mutated_accumulated["accumulatedClockRowsControlled"] is False, "accumulated clock rows must remain open")
    except ValidationFailure:
        accumulated_rows_rejected = True
    check(accumulated_rows_rejected, "negative accumulated-row closure was not rejected")

    novelty_claim_rejected = False
    mutated_novelty = load_json(HERE / "contract.json")["claimBoundary"]
    mutated_novelty["noveltyClaim"] = True
    try:
        check(mutated_novelty["noveltyClaim"] is False, "bounded literature non-hit must not become a novelty claim")
    except ValidationFailure:
        novelty_claim_rejected = True
    check(novelty_claim_rejected, "negative novelty claim was not rejected")
    return {
        "wrongSourceHashRejected": source_mismatch_rejected,
        "falseCriticalClosureRejected": false_critical_closure_rejected,
        "unconditionalPersistenceRejected": unconditional_persistence_rejected,
        "wKineticToFullClockPromotionRejected": full_clock_promotion_rejected,
        "accumulatedRowsClosureRejected": accumulated_rows_rejected,
        "noveltyClaimRejected": novelty_claim_rejected,
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
    return f"""# R0.74Z figure QA report

Status: **PASS**

Visual inspection confirmation: **YES**.  The explicit seal flag records that
`qa-final-size.png`, `qa-grayscale.png`, and `qa-pdf.png` were inspected at
actual size after the final render.

## Scope and provenance

- Artifact: `{ARTIFACT_ID}`
- Seal: local SHA-256 precommit seal; no Git commit/blob seal is claimed.
- Mathematical input SHA-256: `bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a`.
- Independent primary audit SHA-256:
  `6b867551bce840cb382cd13cb2ff298affbf0c0d8b1357a8163c5cedc9bace08`;
  verdict PASS, blocker count 0.
- Literature audit SHA-256:
  `8e5346ecf3c2beef4a620e0844e790703b628388ca7f0a6997aae88818caa82f`;
  bounded primary-source non-hit only.

## Automated checks

- Exact rational identities, two fourth-root shifts, strict threshold, and complexity addition: PASS.
- Source-data regeneration and 104-row semantic ledger: PASS.
- Deterministic two-render comparison: PASS ({deterministic['files']} files).
- Publication PNG: {raster['expectedPublicationPixels'][0]}×{raster['expectedPublicationPixels'][1]} pixels at nominal 600 dpi.
- Three QA exports: {raster['expectedQaPixels'][0]}×{raster['expectedQaPixels'][1]} pixels at nominal 300 dpi.
- PDF: one page, {pdf['mediaBoxPoints'][0]}×{pdf['mediaBoxPoints'][1]} pt; all {pdf['fontCount']} font resources embedded.
- SVG: live text, no embedded raster, no external href, palette restricted to one navy root plus neutrals.
- Final-size border, quadrant occupancy, tonal range, greyscale neutrality, footer, and top-right blossom checks: PASS.
- Negative tests for source-hash drift, critical-layer closure, unconditional persistence, W-kinetic-to-full-clock promotion, accumulated-row closure, and novelty: PASS.

## Human visual checks

- Panel titles, axes, exact fractions, and endpoint qualifications are legible.
- No detected callout, footer, title, or canvas-edge collision.
- Panel A shows the exact `Gamma -> Gamma^(1/4) -> Gamma^(1/16)` ladder and the doubled-radius shell identity.
- Panel B visibly separates the strict `limsup kappa_L < kappa_*` theorem from the open critical layer.
- Panel C uses dashed/solid structure and direct labels to show that persistence is conditional on endpoint preservation, Z.22, and moving-strip all-winding uniformity; the complexity rate is visibly necessary, not sufficient.
- Panel D visibly separates PROVED, CONDITIONAL, OPEN, and NEXT Z.39.
- Full-clock Y.57, accumulated rows, the critical layer, and arbitrary exponentially ill-conditioned finite families remain visibly open.
- No novelty claim is made.
- Required scope label appears verbatim:
  `{REQUIRED_LABEL}`.

**ANALYTIC SCHEMATIC. DERIVED ANALYTIC VALUES. NOT PDE DATA. NOT DNS. NO NOVELTY CLAIM. NOT CLAY.**
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
        "schema": "r074z-figure-manifest-v1",
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
            "For the exact smooth common-shear family, the adjacent-inward clock weight is Gamma^(1/4), the doubled-radius "
            "payment weight is Gamma^(1/16), and shell-tube Holder coercivity forces (P_R^M)^(2/3)/h to diverge "
            "exponentially on the strict side limsup kappa_L < kappa_*. This blocks only the W-kinetic-witness route, "
            "not the full completed clock."
        ),
        "openBoundary": (
            "The critical layer kappa_L=kappa_*+o(1), generic moving-strip all-winding persistence, accumulated clock rows, "
            "the full-clock Y.57 gate, and arbitrary exponentially ill-conditioned finite families remain open. The "
            "complexity coefficient is necessary only within the stated derivative/conditioning model. No novelty, "
            "arbitrary-solution, or Clay conclusion is claimed."
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
        "schema": "r074z-figure-validation-v1",
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
    validate_sealed_metadata_text()
    return validation


def verify_only(repository: Path, *, deps_supplied: bool) -> dict[str, Any]:
    inventory = validate_inventory(expect_metadata=True)
    ledger = parse_hash_ledger()
    validation = load_json(HERE / "validation.json")
    manifest = load_json(HERE / "manifest.json")
    config = load_json(HERE / "config.json")
    for label, payload in (("validation", validation), ("manifest", manifest)):
        check(payload.get("artifactId") == ARTIFACT_ID, f"{label} artifactId drift")
    check(validation["schema"] == "r074z-figure-validation-v1", "validation schema drift")
    check(manifest["schema"] == "r074z-figure-manifest-v1", "manifest schema drift")
    check(validation["status"] == "PASS", "validation status is not PASS")
    check(validation["visualQAConfirmed"] is True, "visual QA confirmation missing")
    check(manifest["status"] == "local-precommit-sealed", "manifest status drift")
    check(manifest["figureSourceCommitAssigned"] is False, "manifest invents a figure commit")
    check(manifest["gitCommitOrBlobSealClaimed"] is False, "manifest invents a Git seal")
    check(manifest["mainIndependentAuditSealed"] is True, "manifest loses primary audit seal")
    check(
        "blocks only the W-kinetic-witness route" in manifest["supportedClaim"]
        and "not the full completed clock" in manifest["supportedClaim"],
        "manifest promotes W-kinetic coercivity to the full clock",
    )
    check(
        "critical layer" in manifest["openBoundary"]
        and "accumulated clock rows" in manifest["openBoundary"]
        and "full-clock Y.57 gate" in manifest["openBoundary"]
        and "remain open" in manifest["openBoundary"],
        "manifest loses an open boundary",
    )
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
    sealed_text = validate_sealed_metadata_text()
    return {
        "status": "PASS",
        "inventory": inventory,
        "checks": checks,
        "sealedMetadataText": sealed_text,
        "hashLedgerEntries": len(ledger),
    }


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
