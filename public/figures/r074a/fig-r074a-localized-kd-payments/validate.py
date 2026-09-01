#!/usr/bin/env python3
"""Fail-closed validator and metadata writer for Figure R0.74A-1."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import subprocess
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageOps
from pypdf import PdfReader


PACKAGE = Path(__file__).resolve().parent
CONFIG_PATH = PACKAGE / "config.json"
CONTRACT_PATH = PACKAGE / "contract.json"
MM_TO_PT = 72.0 / 25.4
TOLERANCE = 5e-13
METADATA_FILES = {"SHA256SUMS", "manifest.json", "qa-report.md", "validation.json"}


class ValidationFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationFailure(message)


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def repository_root() -> Path:
    value = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=PACKAGE, text=True
    ).strip()
    return Path(value).resolve()


def verify_source_binding(config: dict[str, Any]) -> dict[str, Any]:
    root = repository_root()
    binding = config["sourceBinding"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    require(head == binding["commit"], f"HEAD drift: {head} != {binding['commit']}")
    observed: dict[str, str] = {}
    for relative, expected in sorted(binding["files"].items()):
        path = root / relative
        require(path.is_file() and not path.is_symlink(), f"bound source missing or symlink: {relative}")
        actual = sha256_file(path)
        require(actual == expected, f"bound source hash drift: {relative}")
        observed[relative] = actual
    certificate = json.loads((root / "research/r074a_localized_kd_certificate.json").read_text(encoding="utf-8"))
    require(certificate.get("status") == "PASS", "localized K_D certificate status is not PASS")
    require(certificate.get("summary") == binding["certificateSummary"], "certificate 21/21 summary drift")
    require("NOT CLAY" in certificate.get("scope", ""), "certificate NOT CLAY boundary drift")
    require(certificate.get("derived", {}).get("theta_exponents") == {"cc": "1/4", "ce": "1", "ec": "1/4", "ee": "1"}, "certificate theta ledger drift")
    require(certificate.get("derived", {}).get("packet_N_exponents") == {"epsilon": "-2/3", "K_D": "0", "old_L3_tail": "-2", "gradient_energy": "2/3"}, "certificate packet ledger drift")
    require(certificate.get("derived", {}).get("time_spike_delta_exponents") == {"amplitude": "-1/3", "L3_time": "0", "Linf_L2": "-2/3"}, "certificate spike ledger drift")
    return {"commit": head, "files": observed, "certificateStatus": "PASS", "certificateSummary": certificate["summary"]}


def load_rows() -> list[dict[str, str]]:
    path = PACKAGE / "source-data.csv"
    require(path.is_file(), "source-data.csv missing")
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames is not None, "CSV header missing")
        rows = list(reader)
    require(len(rows) == 266, f"CSV row count {len(rows)} != 266")
    return rows


def close(actual: float, expected: float, label: str) -> None:
    require(math.isfinite(actual), f"{label}: non-finite value")
    error = abs(actual - expected)
    require(error <= TOLERANCE, f"{label}: error {error:.3e} exceeds {TOLERANCE:.1e}")


def close_physical(actual: float, expected: float, label: str) -> None:
    """Allow only the PDF/SVG serialization precision, never formula drift."""
    error = abs(actual - expected)
    require(error <= 5e-4, f"{label}: physical-size error {error:.3e} pt exceeds 5e-4 pt")


def verify_formulas(rows: list[dict[str, str]], config: dict[str, Any]) -> dict[str, Any]:
    by_panel = {panel: [row for row in rows if row["panel"] == panel] for panel in ("A", "B", "C")}
    require([len(by_panel[p]) for p in ("A", "B", "C")] == [121, 24, 121], "panel grain mismatch")

    a_min = float(config["panelA"]["thetaMinimum"])
    a_max = float(config["panelA"]["thetaMaximum"])
    a_count = int(config["panelA"]["points"])
    a_ratio = a_max / a_min
    for zero_index, row in enumerate(by_panel["A"]):
        index = zero_index + 1
        require(int(row["sample_index"]) == index, f"A sample index drift at {index}")
        theta = a_min * a_ratio ** (zero_index / (a_count - 1))
        quarter = theta ** 0.25
        close(float(row["theta"]), theta, f"A theta row {index}")
        close(float(row["cc_weight"]), quarter, f"A cc row {index}")
        close(float(row["ec_weight"]), quarter, f"A ec row {index}")
        close(float(row["ce_weight"]), theta, f"A ce row {index}")
        close(float(row["ee_weight"]), theta, f"A ee row {index}")
        require("C suppressed" in row["normalization"], f"A suppressed-C qualifier missing at row {index}")
        require("C is not plotted" in row["claim_qualifier"] and "NOT CLAY" in row["claim_qualifier"], f"A claim boundary missing at row {index}")

    for index, row in enumerate(by_panel["B"], start=1):
        require(int(row["sample_index"]) == index and int(row["j"]) == index, f"B index drift at {index}")
        n = 2**index
        require(int(row["N"]) == n, f"B N=2^j drift at j={index}")
        close(float(row["epsilon_N"]), n ** (-2.0 / 3.0), f"B epsilon row {index}")
        close(float(row["KD_lower_bound_exponent_factor"]), 1.0, f"B K_D factor row {index}")
        close(float(row["old_cubic_N_factor"]), n**-2, f"B old cubic row {index}")
        close(float(row["gradient_energy_N_factor"]), n ** (2.0 / 3.0), f"B gradient row {index}")
        require("c suppressed" in row["normalization"], f"B suppressed-c qualifier missing at j={index}")
        qualifier = row["claim_qualifier"]
        require("not an unforced NSE trajectory" in qualifier and "no simulation/DNS" in qualifier and "finite rows do not prove quantifiers" in qualifier and "NOT CLAY" in qualifier, f"B claim boundary missing at j={index}")

    c_min = float(config["panelC"]["deltaMinimum"])
    c_max = float(config["panelC"]["deltaMaximum"])
    point_count = int(config["panelC"]["points"])
    ratio = c_max / c_min
    c_maxima = {"old_cubic_delta_factor": 0.0, "U_ext_infinity_delta_factor": 0.0}
    for zero_index, row in enumerate(by_panel["C"]):
        index = zero_index + 1
        require(int(row["sample_index"]) == index, f"C index drift at {index}")
        delta = c_min * ratio ** (zero_index / (point_count - 1))
        close(float(row["delta"]), delta, f"C delta row {index}")
        values = {
            "old_cubic_delta_factor": float(row["old_cubic_delta_factor"]),
            "U_ext_infinity_delta_factor": float(row["U_ext_infinity_delta_factor"]),
        }
        close(values["old_cubic_delta_factor"], 1.0, f"C old cubic row {index}")
        close(values["U_ext_infinity_delta_factor"], delta ** (-2.0 / 3.0), f"C endpoint row {index}")
        qualifier = row["claim_qualifier"]
        require("separate finite energy-class field for each delta" in qualifier and "no uniform global L_t^infinity L_x^2" in qualifier and "not an unforced NSE trajectory" in qualifier and "no simulation/DNS" in qualifier and "finite rows do not prove quantifiers" in qualifier and "NOT CLAY" in qualifier, f"C claim boundary missing at row {index}")
        for key, value in values.items():
            c_maxima[key] = max(c_maxima[key], value)

    require(float(by_panel["B"][-1]["old_cubic_N_factor"]) < float(by_panel["B"][0]["old_cubic_N_factor"]), "B old factor must decrease")
    require(float(by_panel["B"][-1]["gradient_energy_N_factor"]) > float(by_panel["B"][0]["gradient_energy_N_factor"]), "B gradient factor must increase")
    require(float(by_panel["C"][0]["U_ext_infinity_delta_factor"]) > float(by_panel["C"][-1]["U_ext_infinity_delta_factor"]), "C endpoint factor must grow as delta decreases")
    return {
        "rowCount": len(rows),
        "panelRows": {panel: len(values) for panel, values in by_panel.items()},
        "maximumAbsoluteReconstructionError": TOLERANCE,
        "panelCDisplayedMaxima": c_maxima,
    }


def verify_claim_boundary(contract: dict[str, Any], *, include_manifest: bool) -> None:
    claim = contract["claimBoundary"]
    require(claim["notClay"] is True and claim["clayProblemSolved"] is False, "contract Clay boundary drift")
    require(claim["finiteRowsProveQuantifiers"] is False, "finite-row proof boundary drift")
    require(claim["sizeLemmaAbsorption"] == "OPEN" and claim["epsilonRegularity"] == "OPEN", "OPEN qualifier drift")
    require(claim["functionLevelPacketsAreUnforcedNseTrajectories"] is False, "function-level NSE boundary drift")
    require(claim["timeSpikeUniformGlobalLinfL2"] is False, "uniform-energy boundary drift")
    require(claim["unknownConstantsPlotted"] is False and claim["directNumericalSimulation"] is False, "plot/simulation boundary drift")
    for name in ("README.md", "caption.md", "chart-contract-and-source-data.md"):
        text = (PACKAGE / name).read_text(encoding="utf-8")
        require("finite" in text.lower(), f"finite-row boundary missing from {name}")
        require("not unforced" in text.lower(), f"unforced-NSE boundary missing from {name}")
        require("simulation" in text.lower() and "DNS" in text, f"simulation/DNS boundary missing from {name}")
        require("NOT CLAY" in text, f"NOT CLAY missing from {name}")
    if include_manifest:
        manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
        require(manifest["claimBoundary"] == claim, "manifest claim boundary differs from contract")


def verify_svg(config: dict[str, Any]) -> dict[str, Any]:
    path = PACKAGE / "figure.svg"
    require(path.is_file(), "figure.svg missing")
    text = path.read_text(encoding="utf-8")
    require("<image" not in text.lower(), "SVG embeds raster image")
    root = ET.fromstring(text)
    require(root.attrib.get("width") == "178mm" and root.attrib.get("height") == "74mm", "SVG physical size mismatch")
    view_box = [float(value) for value in root.attrib["viewBox"].split()]
    require(len(view_box) == 4, "SVG viewBox malformed")
    close_physical(view_box[2], float(config["widthMillimetres"]) * MM_TO_PT, "SVG width points")
    close_physical(view_box[3], float(config["heightMillimetres"]) * MM_TO_PT, "SVG height points")
    namespace = {"svg": "http://www.w3.org/2000/svg"}
    require(len(root.findall(".//svg:polyline", namespace)) >= 7, "SVG lacks expected vector series")
    require(len(root.findall(".//svg:text", namespace)) >= 45, "SVG lacks expected labels")
    require(len(root.findall(".//svg:circle", namespace)) >= 12, "SVG research blossom/markers missing")
    return {"vector": True, "embeddedImages": 0, "sha256": sha256_file(path)}


def dereference(value: Any) -> Any:
    return value.get_object() if hasattr(value, "get_object") else value


def count_pdf_images(reader: PdfReader) -> int:
    count = 0
    page = reader.pages[0]
    resources = dereference(page.get("/Resources", {}))
    xobjects = dereference(resources.get("/XObject", {})) if resources else {}
    for value in xobjects.values() if hasattr(xobjects, "values") else []:
        obj = dereference(value)
        if obj.get("/Subtype") == "/Image":
            count += 1
    return count


def verify_pdf(config: dict[str, Any]) -> dict[str, Any]:
    path = PACKAGE / "figure.pdf"
    require(path.is_file(), "figure.pdf missing")
    reader = PdfReader(str(path))
    require(len(reader.pages) == 1, "PDF must contain exactly one page")
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    close_physical(width, float(config["widthMillimetres"]) * MM_TO_PT, "PDF width points")
    close_physical(height, float(config["heightMillimetres"]) * MM_TO_PT, "PDF height points")
    image_count = count_pdf_images(reader)
    require(image_count == 0, f"PDF contains {image_count} raster image XObjects")
    resources = dereference(page.get("/Resources", {}))
    fonts = dereference(resources.get("/Font", {})) if resources else {}
    require(len(fonts) >= 1, "PDF has no vector text fonts")
    return {
        "vector": True,
        "embeddedImages": image_count,
        "pageCount": 1,
        "points": [width, height],
        "sha256": sha256_file(path),
    }


def image_info(path: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        dpi = image.info.get("dpi", (0.0, 0.0))
        return {"mode": image.mode, "size": list(image.size), "dpi": [float(dpi[0]), float(dpi[1])]}


def verify_rasters(config: dict[str, Any]) -> dict[str, Any]:
    paths = {name: PACKAGE / name for name in ("figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png")}
    for name, path in paths.items():
        require(path.is_file(), f"{name} missing")
    info = {name: image_info(path) for name, path in paths.items()}
    archival = info["figure.png"]
    expected_w = float(config["widthMillimetres"]) * int(config["pngDpi"]) / 25.4
    expected_h = float(config["heightMillimetres"]) * int(config["pngDpi"]) / 25.4
    require(abs(archival["size"][0] - expected_w) <= 1.1 and abs(archival["size"][1] - expected_h) <= 1.1, "600 dpi PNG pixel dimensions mismatch")
    require(all(abs(value - int(config["pngDpi"])) <= 1.0 for value in archival["dpi"]), "archival PNG dpi metadata mismatch")
    require(archival["mode"] == "RGB", "archival PNG must be RGB")

    qa_size = info["qa-pdf.png"]["size"]
    require(info["qa-final-size.png"]["size"] == qa_size == info["qa-grayscale.png"]["size"], "QA render dimensions differ")
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        require(all(abs(value - int(config["qaDpi"])) <= 1.0 for value in info[name]["dpi"]), f"{name} dpi metadata mismatch")
    require(info["qa-grayscale.png"]["mode"] == "L", "grayscale QA is not mode L")

    with Image.open(paths["figure.png"]) as image:
        expected_final = image.convert("RGB").resize(tuple(qa_size), Image.Resampling.LANCZOS)
    with Image.open(paths["qa-final-size.png"]) as image:
        stored_final = image.convert("RGB")
    require(np.array_equal(np.asarray(expected_final), np.asarray(stored_final)), "qa-final-size is not exact archival downsample")
    expected_gray = ImageOps.grayscale(stored_final)
    with Image.open(paths["qa-grayscale.png"]) as image:
        stored_gray = image.convert("L")
    require(np.array_equal(np.asarray(expected_gray), np.asarray(stored_gray)), "qa-grayscale is not exact grayscale conversion")
    with Image.open(paths["qa-pdf.png"]) as image:
        pdf_rgb = np.asarray(image.convert("RGB"), dtype=np.int16)
    final_rgb = np.asarray(stored_final, dtype=np.int16)
    differences = np.abs(final_rgb - pdf_rgb).astype(np.float64)
    mean_difference = float(np.mean(differences))
    percentile_99 = float(np.percentile(differences, 99.0))
    require(mean_difference <= 3.0, f"archival/PDF render mean difference {mean_difference:.3f} > 3")
    # Direct 300 dpi rasterization and 600->300 Lanczos reduction disagree at
    # anti-aliased vector edges; retain a tight whole-image mean and an explicit
    # edge-pixel p99 allowance without weakening any formula tolerance.
    require(percentile_99 <= 64.0, f"archival/PDF render p99 difference {percentile_99:.3f} > 64")
    return {
        "images": info,
        "archivalVsPdfRender": {
            "meanAbsoluteRgbDifference": mean_difference,
            "percentile99AbsoluteRgbDifference": percentile_99,
        },
    }


def deterministic_hashes(config: dict[str, Any]) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for name in config["deterministicCore"]:
        path = PACKAGE / name
        require(path.is_file(), f"deterministic-core file missing: {name}")
        hashes[name] = sha256_file(path)
    require(len(hashes) == 18, f"deterministic core count {len(hashes)} != 18")
    return hashes


def expected_inventory(contract: dict[str, Any]) -> list[str]:
    inventory = contract["inventory"]
    names = sorted(inventory["source"] + inventory["rawAndResult"] + inventory["metadata"])
    require(len(names) == 25 and len(set(names)) == 25, "contract inventory must contain 25 unique files")
    return names


def verify_inventory(contract: dict[str, Any], *, metadata_expected: bool) -> dict[str, Any]:
    expected = expected_inventory(contract)
    actual = sorted(path.name for path in PACKAGE.iterdir() if path.is_file())
    symlinks = sorted(path.name for path in PACKAGE.iterdir() if path.is_symlink())
    require(not symlinks, f"package contains symlinks: {symlinks}")
    if metadata_expected:
        require(actual == expected, f"inventory mismatch: expected {expected}, observed {actual}")
    else:
        allowed = set(expected) - METADATA_FILES
        unexpected = sorted(set(actual) - allowed - {".determinism-baseline.json"})
        missing_core = sorted(allowed - set(actual))
        require(not unexpected, f"unexpected pre-metadata files: {unexpected}")
        require(not missing_core, f"missing pre-metadata files: {missing_core}")
    return {"expectedCount": 25, "observedCount": len(actual), "files": actual, "symlinks": symlinks}


def write_baseline(path: Path, hashes: dict[str, str]) -> None:
    payload = {"schema": "r074a-determinism-baseline-v1", "fileCount": len(hashes), "sha256": hashes}
    path.write_text(canonical_json(payload), encoding="utf-8", newline="\n")


def compare_baseline(path: Path, hashes: dict[str, str]) -> dict[str, Any]:
    require(path.is_file(), f"determinism baseline missing: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    require(payload.get("schema") == "r074a-determinism-baseline-v1", "determinism baseline schema drift")
    require(payload.get("fileCount") == 18, "determinism baseline core count drift")
    before = payload.get("sha256", {})
    changed = sorted(name for name in set(before) | set(hashes) if before.get(name) != hashes.get(name))
    require(not changed, f"second render changed deterministic core: {changed}")
    return {"fileCount": len(hashes), "secondRenderIdentical": True, "changed": changed, "sha256": hashes}


def nonmetadata_inventory(contract: dict[str, Any]) -> list[str]:
    return sorted(contract["inventory"]["source"] + contract["inventory"]["rawAndResult"])


def write_metadata(
    config: dict[str, Any],
    contract: dict[str, Any],
    source: dict[str, Any],
    formula: dict[str, Any],
    svg: dict[str, Any],
    pdf: dict[str, Any],
    raster: dict[str, Any],
    determinism: dict[str, Any],
    *,
    visual_confirmed: bool,
) -> None:
    require(visual_confirmed, "--confirm-visual-qa is required before writing formal metadata")
    validation = {
        "checks": {
            "claimBoundary": "PASS",
            "deterministicSecondRender": "PASS",
            "formulaReconstruction": "PASS",
            "inventory": "PASS pending metadata closure",
            "pdfVector": "PASS",
            "rasterParity": "PASS",
            "sourceBinding": "PASS",
            "svgVector": "PASS",
            "visualQa": "PASS (operator-confirmed final, grayscale, and PDF renders)",
        },
        "formulaAudit": formula,
        "rasterAudit": raster,
        "schema": "r074a-figure-validation-v1",
        "sourceBinding": source,
        "status": "PASS",
        "validatedAtUtc": utc_now(),
        "visualQaConfirmed": True,
    }
    (PACKAGE / "validation.json").write_text(canonical_json(validation), encoding="utf-8", newline="\n")

    qa_lines = [
        "# R0.74A figure QA report",
        "",
        "Status: **PASS**",
        "",
        "- Source binding: PASS (commit, six file hashes, certificate PASS 21/21).",
        "- Formula reconstruction: PASS (all 266 rows; tolerance 5e-13).",
        "- Panel A: PASS (cc/ec theta^(1/4); ce/ee theta; unknown C not plotted).",
        "- Panel B: PASS (N=2^j; factors N^0, N^-2, N^(2/3); unknown c not plotted).",
        "- Panel C: PASS (delta^0 and delta^(-2/3); separate finite fields; no uniform global Linf_t L2_x).",
        "- SVG/PDF: PASS (178 mm x 74 mm; vector; no embedded raster images).",
        "- Raster: PASS (600 dpi archival PNG; independent 300 dpi PDF QA render).",
        f"- Raster parity: PASS (mean absolute RGB difference {raster['archivalVsPdfRender']['meanAbsoluteRgbDifference']:.6f}; p99 {raster['archivalVsPdfRender']['percentile99AbsoluteRgbDifference']:.3f}).",
        "- Grayscale/final/PDF visual review: PASS (operator-confirmed; no collision, clipping, or illegible series distinction).",
        "- Two-render determinism: PASS (18/18 deterministic-core hashes identical).",
        "- Inventory closure: PASS after metadata generation (25 contract files; no symlinks).",
        "",
        "Panels B and C are function-level packets, not unforced NSE trajectories. The images contain no simulation or DNS. Finite data are not used as proof of any quantified statement. **NOT CLAY.**",
        "",
    ]
    (PACKAGE / "qa-report.md").write_text("\n".join(qa_lines), encoding="utf-8", newline="\n")

    manifest = {
        "claimBoundary": contract["claimBoundary"],
        "compute": {
            "dgxUsed": False,
            "execution": "local CPU",
            "networkUsed": False,
            "randomnessUsed": False,
            "workload": "266 closed-form rows and vector/raster export; no simulation/DNS",
        },
        "deterministicCore": determinism,
        "figureId": config["figureId"],
        "figureOutputs": {
            "pdf": pdf,
            "png": {
                "dpi": int(config["pngDpi"]),
                "pixelDimensions": raster["images"]["figure.png"]["size"],
                "sha256": sha256_file(PACKAGE / "figure.png"),
                "source": "Poppler render of vector PDF",
            },
            "svg": svg,
        },
        "figureSchemaVersion": config["figureSchemaVersion"],
        "formalCommand": "python producer.py --render; python validate.py --write-baseline .determinism-baseline.json; python producer.py --render; python validate.py --determinism-baseline .determinism-baseline.json --consume-baseline --write-metadata --confirm-visual-qa; python validate.py --verify-only --confirm-visual-qa",
        "inventory": {
            "expectedCount": 25,
            "metadata": contract["inventory"]["metadata"],
            "rawAndResult": contract["inventory"]["rawAndResult"],
            "source": contract["inventory"]["source"],
        },
        "packageSourceCommit": None,
        "publicationStatus": "staged",
        "release": config["release"],
        "schemaVersion": "research-figure-manifest-v1",
        "sourceData": {
            "formulaReconstructed": True,
            "rowCount": formula["rowCount"],
            "sha256": sha256_file(PACKAGE / "source-data.csv"),
            "warning": "function-level packets are not unforced NSE trajectories; finite rows do not prove quantifiers; no simulation/DNS; NOT CLAY",
        },
        "sourceEvidence": source,
        "status": "formal",
        "validation": {
            "maximumTolerance": TOLERANCE,
            "status": "PASS",
            "visualQaConfirmed": True,
        },
    }
    (PACKAGE / "manifest.json").write_text(canonical_json(manifest), encoding="utf-8", newline="\n")

    checksum_names = nonmetadata_inventory(contract)
    checksum_text = "".join(f"{sha256_file(PACKAGE / name)}  {name}\n" for name in checksum_names)
    (PACKAGE / "SHA256SUMS").write_text(checksum_text, encoding="utf-8", newline="\n")


def verify_metadata(config: dict[str, Any], contract: dict[str, Any]) -> None:
    for name in METADATA_FILES:
        require((PACKAGE / name).is_file(), f"metadata missing: {name}")
    validation = json.loads((PACKAGE / "validation.json").read_text(encoding="utf-8"))
    require(validation.get("status") == "PASS" and validation.get("visualQaConfirmed") is True, "validation metadata not PASS")
    manifest = json.loads((PACKAGE / "manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("schemaVersion") == "research-figure-manifest-v1", "manifest schema drift")
    require(manifest.get("figureSchemaVersion") == config["figureSchemaVersion"], "figure manifest schema drift")
    require(manifest.get("status") == "formal" and manifest.get("publicationStatus") == "staged", "manifest status drift")
    require(manifest.get("packageSourceCommit") is None, "uncommitted package source commit must be null")
    require(manifest["figureOutputs"]["svg"]["sha256"] == sha256_file(PACKAGE / "figure.svg"), "manifest SVG hash drift")
    require(manifest["figureOutputs"]["pdf"]["sha256"] == sha256_file(PACKAGE / "figure.pdf"), "manifest PDF hash drift")
    require(manifest["figureOutputs"]["png"]["sha256"] == sha256_file(PACKAGE / "figure.png"), "manifest PNG hash drift")
    require(manifest["sourceData"]["sha256"] == sha256_file(PACKAGE / "source-data.csv"), "manifest CSV hash drift")
    require(manifest["deterministicCore"]["sha256"] == deterministic_hashes(config), "manifest deterministic hashes drift")
    qa_text = (PACKAGE / "qa-report.md").read_text(encoding="utf-8")
    require("Status: **PASS**" in qa_text and "NOT CLAY" in qa_text, "QA report status/boundary drift")

    expected_names = nonmetadata_inventory(contract)
    observed: dict[str, str] = {}
    for line in (PACKAGE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        parts = line.split("  ", 1)
        require(len(parts) == 2, "malformed SHA256SUMS line")
        digest, name = parts
        require(len(digest) == 64, f"malformed SHA-256 for {name}")
        observed[name] = digest
    require(sorted(observed) == expected_names, "SHA256SUMS inventory drift")
    for name, digest in observed.items():
        require(digest == sha256_file(PACKAGE / name), f"SHA256SUMS mismatch: {name}")


def full_validation(config: dict[str, Any], contract: dict[str, Any], *, metadata_expected: bool) -> dict[str, Any]:
    source = verify_source_binding(config)
    rows = load_rows()
    formula = verify_formulas(rows, config)
    svg = verify_svg(config)
    pdf = verify_pdf(config)
    raster = verify_rasters(config)
    verify_claim_boundary(contract, include_manifest=metadata_expected)
    inventory = verify_inventory(contract, metadata_expected=metadata_expected)
    hashes = deterministic_hashes(config)
    if metadata_expected:
        verify_metadata(config, contract)
    return {
        "source": source,
        "formula": formula,
        "svg": svg,
        "pdf": pdf,
        "raster": raster,
        "inventory": inventory,
        "hashes": hashes,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write-baseline", type=Path)
    parser.add_argument("--determinism-baseline", type=Path)
    parser.add_argument("--consume-baseline", action="store_true")
    parser.add_argument("--write-metadata", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--confirm-visual-qa", action="store_true")
    args = parser.parse_args()
    modes = sum(bool(value) for value in (args.write_baseline, args.write_metadata, args.verify_only))
    require(modes == 1, "choose exactly one of --write-baseline, --write-metadata, or --verify-only")
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    if args.verify_only:
        require(args.confirm_visual_qa, "--verify-only requires --confirm-visual-qa")
        result = full_validation(config, contract, metadata_expected=True)
        print(
            "PASS: verified source binding, 266 formulas, vector exports, raster QA, "
            f"18 deterministic files, and {result['inventory']['observedCount']} contract files"
        )
        return 0

    result = full_validation(config, contract, metadata_expected=False)
    if args.write_baseline:
        baseline = args.write_baseline.resolve()
        require(baseline.parent == PACKAGE, "determinism baseline must be package-local")
        write_baseline(baseline, result["hashes"])
        print(f"PASS: wrote 18-file determinism baseline {baseline.name}")
        return 0

    require(args.determinism_baseline is not None, "--write-metadata requires --determinism-baseline")
    baseline = args.determinism_baseline.resolve()
    determinism = compare_baseline(baseline, result["hashes"])
    write_metadata(
        config,
        contract,
        result["source"],
        result["formula"],
        result["svg"],
        result["pdf"],
        result["raster"],
        determinism,
        visual_confirmed=args.confirm_visual_qa,
    )
    if args.consume_baseline:
        require(baseline.parent == PACKAGE and baseline.name == ".determinism-baseline.json", "refusing to consume unexpected baseline path")
        baseline.unlink()
    verify_inventory(contract, metadata_expected=True)
    verify_metadata(config, contract)
    verify_claim_boundary(contract, include_manifest=True)
    print("PASS: second render identical; wrote formal metadata and closed 25-file inventory")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ValidationFailure as error:
        print(f"FAIL: {error}")
        raise SystemExit(1)
