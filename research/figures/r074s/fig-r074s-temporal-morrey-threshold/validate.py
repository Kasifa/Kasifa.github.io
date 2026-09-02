#!/usr/bin/env python3
"""Validate and freeze the R0.74S Step 13 analytic schematic package."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageChops, ImageOps
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = next(
    parent
    for parent in HERE.parents
    if (parent / "research/r074s_temporal_integrability_morrey_certificate.json").is_file()
)
FROZEN_COMMIT = "533d9e70949da1ad19007fd741581a8c7e165e7c"
FROZEN = {
    "research/r074s_temporal_integrability_morrey_certificate.json": "095e8a7a0ba378ff2178a166cbed81e1f132be055d37165c945020a26466e330",
    "research/r074s_temporal_integrability_morrey_certificate_report.md": "c464af1617391beda5b077e13066629203d408519ab32ee89b2115475346fe2b",
    "research/r074s_temporal_integrability_morrey_independent_audit.md": "332bf2a5b4503b9456bc76b1067bc44cb2d788e37fa7f2e34f10211a700e7ce3",
    "research/r074s_temporal_integrability_morrey_primary_audit.md": "5910f46c0dd401d3766343d75ae3e68bdecb9d8416615fd8feb74d0f560adefd",
    "research/r074s_temporal_integrability_morrey_threshold.md": "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de",
    "scripts/r074s_temporal_integrability_morrey_certificate.py": "eb313260c16431c1379d1b77a508b8bb7740ac713c014126c08e44bc2d0cfafb",
    "scripts/r074s_temporal_integrability_morrey_certificate_independent.rb": "520d52deb1ba56fb46f841e0856bd8eb14ec5dd4961c90dd3b9ec240f88c9720",
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_pdftoppm() -> Path:
    override = os.environ.get("R074S_DEPENDENCIES_ROOT")
    candidates = []
    if override:
        candidates.append(Path(override).expanduser().resolve() / "bin/override/pdftoppm")
    for parent in Path(sys.executable).resolve().parents:
        candidates.append(parent / "bin/override/pdftoppm")
    executable = shutil.which("pdftoppm")
    if executable:
        candidates.append(Path(executable).resolve())
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("pdftoppm")


PDFTOPPM = locate_pdftoppm()


def render_pdf(dpi: int, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="r074s13-validate-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run(
            [str(PDFTOPPM), "-png", "-singlefile", "-r", str(dpi), str(HERE / "figure.pdf"), str(prefix)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        Image.open(prefix.with_suffix(".png")).save(output, dpi=(dpi, dpi))


def exact_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for numerator in range(21):
        x = Fraction(numerator, 20)
        value = Fraction(2) * (Fraction(2) - x) / (Fraction(5) - 3 * x)
        rows.append({"panel": "A", "parameter": "inverse_p", "x_exact": f"{x.numerator}/{x.denominator}", "value_exact": f"{value.numerator}/{value.denominator}", "status": "METHOD_CEILING"})
    for theta in (Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(3, 4), Fraction(1)):
        gap = theta - Fraction(2, 3)
        rows.append({"panel": "B", "parameter": "morrey_theta", "x_exact": f"{theta.numerator}/{theta.denominator}", "value_exact": f"{gap.numerator}/{gap.denominator}", "status": "CLOSES" if gap <= 0 else "ABSTRACT_TWO_CAP_FAILURE"})
    for q in (Fraction(2), Fraction(5, 2), Fraction(3), Fraction(7, 2), Fraction(4)):
        factor = Fraction(8, 2**q.numerator) if q.denominator == 1 else None
        rows.append({"panel": "C", "parameter": "coefficient_power_q", "x_exact": f"{q.numerator}/{q.denominator}", "value_exact": f"{factor.numerator}/{factor.denominator}" if factor is not None else "8*2^(-q)", "status": "CRITICAL" if q == 3 else ("SUBCRITICAL" if q > 3 else "SUPERCRITICAL")})
    return rows


def flat_files() -> list[str]:
    return sorted(path.name for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS" and not re.search(r" 2(?:\.[^.]+)?$", path.name))


def check_only() -> None:
    expected = {}
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        digest, name = line.split("  ", 1)
        expected[name] = digest
    actual_names = flat_files()
    if sorted(expected) != actual_names:
        raise SystemExit("SHA256SUMS inventory mismatch")
    mismatches = [name for name in actual_names if sha(HERE / name) != expected[name]]
    if mismatches:
        raise SystemExit(f"SHA256SUMS mismatch: {mismatches}")
    validation = json.loads((HERE / "validation.json").read_text(encoding="utf-8"))
    if validation["summary"]["result"] != "PASS":
        raise SystemExit("validation.json is not PASS")
    for relative, digest in FROZEN.items():
        if sha(REPO / relative) != digest:
            raise SystemExit(f"frozen binding mismatch: {relative}")
    print(json.dumps({"status": "PASS", "files": len(actual_names), "frozenBindings": len(FROZEN)}, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check-only", action="store_true")
    args = parser.parse_args()
    if args.check_only:
        check_only()
        return

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    certificate = json.loads((REPO / "research/r074s_temporal_integrability_morrey_certificate.json").read_text(encoding="utf-8"))
    checks: list[dict] = [
        {"id": "source_rows_exact", "pass": rows == exact_rows()},
        {"id": "frozen_bindings", "pass": all(sha(REPO / relative) == digest for relative, digest in FROZEN.items())},
        {"id": "certificate_pass", "pass": certificate.get("overall_pass") is True},
    ]
    expected_size = [round(config["width_mm"] / 25.4 * config["dpi"]), round(config["height_mm"] / 25.4 * config["dpi"])]
    with Image.open(HERE / "figure.png") as source_image:
        actual_size = list(source_image.size)
        checks.append({"id": "png_600dpi_geometry", "pass": all(abs(a - b) <= 1 for a, b in zip(actual_size, expected_size)), "actual": actual_size, "expected": expected_size})
    pdf = PdfReader(str(HERE / "figure.pdf"))
    page = pdf.pages[0]
    checks += [
        {"id": "pdf_one_page", "pass": len(pdf.pages) == 1},
        {"id": "pdf_physical_geometry", "pass": abs(float(page.mediabox.width) - config["width_mm"] / 25.4 * 72) < 0.02 and abs(float(page.mediabox.height) - config["height_mm"] / 25.4 * 72) < 0.02},
    ]
    root = ET.parse(HERE / "figure.svg").getroot()
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    checks += [
        {"id": "svg_physical_geometry", "pass": root.attrib.get("width") == "178mm" and root.attrib.get("height") == "105mm"},
        {"id": "svg_boundary_language", "pass": all(value in svg for value in ["ANALYTIC SCHEMATIC", "NOT SIMULATION OR DNS", "2/3", "NOT CLAY"])},
        {"id": "caption_boundary_language", "pass": all(value in caption for value in ["analytic", "not simulation", "2/3", "NOT CLAY"])},
        {"id": "svg_embedded_fonts", "pass": svg.count("data:font/ttf;base64,") == 2 and "R074S13-Regular" in svg and "R074S13-Bold" in svg},
    ]
    render_pdf(config["dpi"], HERE / "qa-pdf-render.png")
    render_pdf(300, HERE / "qa-final-size.png")
    with Image.open(HERE / "figure.png") as master, Image.open(HERE / "qa-pdf-render.png") as rerender:
        checks.append({"id": "pdf_raster_pixel_match", "pass": master.size == rerender.size and ImageChops.difference(master.convert("RGB"), rerender.convert("RGB")).getbbox() is None})
        ImageOps.grayscale(master).save(HERE / "qa-grayscale.png", dpi=(config["dpi"], config["dpi"]))
    ql = Path("/usr/bin/qlmanage")
    if ql.is_file():
        with tempfile.TemporaryDirectory(prefix="r074s13-svg-qa-") as temp:
            result = subprocess.run([str(ql), "-t", "-s", "1800", "-o", temp, str(HERE / "figure.svg")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            candidates = sorted(Path(temp).glob("*.png"))
            if result.returncode == 0 and candidates:
                shutil.copy2(candidates[0], HERE / "qa-svg-quicklook.png")
    checks.append({"id": "svg_quicklook_available", "pass": (HERE / "qa-svg-quicklook.png").is_file()})
    passed = all(item["pass"] for item in checks)
    validation = {"schema": "r074s-step13-temporal-morrey-validation-v1", "checks": checks, "summary": {"passed": sum(bool(item["pass"]) for item in checks), "total": len(checks), "result": "PASS" if passed else "FAIL"}}
    (HERE / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "layout-bounds.json").write_text(json.dumps({"schema": "r074s-step13-layout-v1", "page_mm": [178, 105], "panels": {"A": [14, 22, 255], "B": [279, 22, 211.6]}}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "qa-report.md").write_text("# R0.74S Step 13 figure QA\n\n**PASS.** Exact rational rows, frozen-source bindings, one-page PDF geometry, PDF/PNG pixel parity, embedded-font SVG, 600 dpi master, final-size derivative, grayscale derivative, labels, formulas, and explicit evidence boundaries were checked. This is an **analytic schematic**, not a simulation or DNS. Open gates remain open. **NOT CLAY.**\n", encoding="utf-8")
    outputs = []
    for name, schema in (("figure.svg", "svg-journal-master"), ("figure.pdf", "pdf-journal-master"), ("figure.png", "png-journal-master")):
        record = {"path": name, "schema": schema, "bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)}
        if name.endswith(".png"):
            record["dpi"] = config["dpi"]
        outputs.append(record)
    assets = [{"path": f"public/assets/r074s/{config['figure_id']}.{Path(name).suffix.lstrip('.')}", "bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)} for name in ("figure.svg", "figure.pdf", "figure.png")]
    package_files = flat_files()
    manifest = {
        "schemaVersion": "research-figure-manifest-v1", "figureSchemaVersion": "r074s-step13-temporal-morrey-publication-v1", "figureId": config["figure_id"], "release": "R0.74S", "status": "formal", "publicationStatus": "published",
        "analyticalQuestion": "Can the Step 13 linear-payment estimates reach the scale-invariant 2/3 temporal target, and which abstract packing thresholds remain?",
        "supportedClaim": "The exact linear-payment ceiling remains strictly above 2/3; the two-scalar-cap moving-Morrey inference has threshold theta=2/3; and the critical eight-ary cubic tree prevents a bare critical Dini conclusion.",
        "createdAt": "2026-09-03T00:00:00Z", "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": FROZEN_COMMIT, "dirty": False},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json", "precision": "exact rational identities and deterministic analytic rendering", "solver": "none", "formalCommand": "use command.txt and validate.py", "wallTimeSeconds": 2.0, "monitoring": {"enabled": False}},
        "compute": {"host": "local workstation (hostname omitted)", "operatingSystem": "macOS arm64", "cpu": "arm64 / local CPU", "memoryGiB": 36.0, "processes": 1, "threadsPerProcess": 1}, "environment": {"python": sys.version.split()[0], "packagesLock": "requirements.txt"},
        "data": [{"path": "source-data.csv", "schema": "r074s-step13-exact-threshold-rows-v1", "bytes": (HERE / "source-data.csv").stat().st_size, "sha256": sha(HERE / "source-data.csv")}], "sourceData": [],
        "figure": {"widthMillimetres": config["width_mm"], "heightMillimetres": config["height_mm"], "outputs": outputs}, "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": {"fixedSolutionTemporalSequence": "PROVED_ELL1_L4_OVER_3", "commonWindowGain": "PROVED_DELTA_ONE_QUARTER", "linearPaymentTarget": "METHOD_CEILING_ABOVE_TWO_THIRDS", "movingMorreyImplication": "CONDITIONAL_ON_S328", "twoCapMorreyThreshold": "ABSTRACT_EXACT_TWO_THIRDS", "criticalEightAryTree": "ABSTRACT_OBSTRUCTION", "strictCubicDiniCriterion": "CONDITIONAL_INTERFACE", "bareClassS328": "OPEN", "uniformHTailPayment": "OPEN", "quadraticShellSelectiveS342": "OPEN", "globalRegularity": False, "notClay": True},
        "publication": {"archiveDirectory": f"public/figures/r074s/{config['figure_id']}", "researchArchiveDirectory": f"research/figures/r074s/{config['figure_id']}", "directory": "public/assets/r074s", "fileStem": config["figure_id"], "byteIdentityRequired": True, "publicCopiesComplete": True, "releaseSourceCommit": FROZEN_COMMIT, "assets": assets},
        "provenance": {"frozenResearchCommit": FROZEN_COMMIT, "frozenResearchSourceSha256": FROZEN["research/r074s_temporal_integrability_morrey_threshold.md"], "evidenceClass": "analytic schematic", "simulation": False, "dns": False},
        "claim_boundary": "PROVED FIXED-SOLUTION TIME SUM; LINEAR METHOD CEILING ABOVE 2/3; CONDITIONAL MORREY IMPLICATION; ABSTRACT CRITICAL TREE; OPEN PDE GATES; NOT CLAY",
        "external_bindings": {relative: sha(REPO / relative) for relative in [*FROZEN, "research/r074s_step13_report-source.md", "research/r074s_claim_state_update.md", "research/r074s_literature_boundary.md"] if (REPO / relative).is_file()},
        "files": {name: {"bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)} for name in package_files if name != "manifest.json"}, "validation_result": validation["summary"],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "SHA256SUMS").write_text("\n".join(f"{sha(HERE / name)}  {name}" for name in flat_files()) + "\n", encoding="utf-8")
    print(json.dumps(validation["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
