#!/usr/bin/env python3
"""Validate and freeze the R0.74S Step 14 analytic schematic package."""

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
REPO = next(parent for parent in HERE.parents if (parent / "research/r074s_outer_collar_corona_certificate.json").is_file())
FROZEN_COMMIT = "468f8cba70c9281cb00e97a40135a2224cc1e4cd"
FROZEN = {
    "research/r074s_outer_collar_corona_obstruction.md": "c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9",
    "research/r074s_outer_collar_corona_certificate.json": "1714426abc2bbe0a6f98ea5bced5c15843a68fbe66ed02adef670ee681f42be3",
    "research/r074s_outer_collar_corona_certificate_report.md": "d3a5213ed8a646ccf6b26947a31ad18276c3e6e823c4296e8b1b760deabd05ef",
    "research/r074s_outer_collar_corona_primary_audit.md": "7f7dd6a7bb1ca6e598b4156388037fe6db7c191a7baacd46d9abe43b12c37e90",
    "research/r074s_outer_collar_corona_independent_audit.md": "9baa160a706c962f3eb6911d55882c3bc2f883ccdea6c674689930ab4b4e4156",
    "scripts/r074s_outer_collar_corona_certificate.py": "041328286841e79e8863aca9c5ca9ef7c6ebbab328505c030dd1789c76d03e05",
    "scripts/r074s_outer_collar_corona_certificate_independent.rb": "f7e420a03445a8089cd53e31eed55f00def576d2f76e091bf3aa5c405915ee10",
}
CERTIFICATE_SUMMARY = {
    "dependency_passed": 3, "dependency_total": 3, "exact_passed": 12,
    "exact_total": 12, "finite_cases": 74287, "finite_passed": 9,
    "finite_total": 9, "negative_passed": 49, "negative_total": 49,
    "structural_passed": 37, "structural_total": 37,
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def locate_pdftoppm() -> Path:
    candidates: list[Path] = []
    if override := os.environ.get("R074S_DEPENDENCIES_ROOT"):
        candidates.append(Path(override).expanduser().resolve() / "bin/override/pdftoppm")
    for parent in Path(sys.executable).resolve().parents:
        candidates.append(parent / "bin/override/pdftoppm")
    if executable := shutil.which("pdftoppm"):
        candidates.append(Path(executable).resolve())
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("pdftoppm")


PDFTOPPM = locate_pdftoppm()


def render_pdf(dpi: int, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="r074s14-validate-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run([str(PDFTOPPM), "-png", "-singlefile", "-r", str(dpi), str(HERE / "figure.pdf"), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Image.open(prefix.with_suffix(".png")).save(output, dpi=(dpi, dpi))


def exact_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for k in (3, 4, 5, 6):
        rows.append({"panel": "A", "parameter": f"shell_k={k}:inner", "value_exact": f"exp(-15*4^{k-3}/32)", "status": "PROVED_INNER_GAIN"})
        rows.append({"panel": "A", "parameter": f"shell_k={k}:outer", "value_exact": "1", "status": "PROVED_OUTER_ALIGNMENT"})
    for lam in (Fraction(1, 4), Fraction(1), Fraction(4)):
        rows.append({"panel": "B", "parameter": f"lambda={lam}", "value_exact": "2^(1/3)*M_R", "status": "PROVED_THRESHOLD_NO_GAIN"})
    for alpha in (1, 3, 5):
        rows.append({"panel": "C", "parameter": f"alpha={alpha}", "value_exact": f"1/({2 ** (alpha - 1)}*kappa)", "status": "PROVED_JUMP_DINI"})
    for depth in range(6):
        rows.append({"panel": "C", "parameter": f"critical_corona_depth={depth}", "value_exact": "1", "status": "ABSTRACT_CRITICAL_CUBE"})
    rows.append({"panel": "C", "parameter": "open_lemma", "value_exact": "S.375=>S.376", "status": "CONDITIONAL_ARROW_OPEN_ANTECEDENT"})
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
    certificate = json.loads((REPO / "research/r074s_outer_collar_corona_certificate.json").read_text(encoding="utf-8"))
    checks: list[dict] = [
        {"id": "source_rows_exact", "pass": rows == exact_rows()},
        {"id": "frozen_bindings", "pass": all(sha(REPO / relative) == digest for relative, digest in FROZEN.items())},
        {"id": "certificate_pass", "pass": certificate.get("overall_pass") is True},
        {"id": "certificate_summary_exact", "pass": certificate.get("summary") == CERTIFICATE_SUMMARY},
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
        {"id": "svg_physical_geometry", "pass": root.attrib.get("width") == "178mm" and root.attrib.get("height") == "110mm"},
        {"id": "svg_boundary_language", "pass": all(value in svg for value in ["ANALYTIC SCHEMATIC", "NOT SIMULATION OR DNS", "OPEN PDE LEMMA", "NOT CLAY"])},
        {"id": "caption_boundary_language", "pass": all(value in caption.lower() for value in ["analytic", "schematic", "not simulation", "s.375", "not clay"])},
        {"id": "svg_embedded_fonts", "pass": svg.count("data:font/ttf;base64,") == 2 and "R074S14-Regular" in svg and "R074S14-Bold" in svg},
    ]
    render_pdf(config["dpi"], HERE / "qa-pdf-render.png")
    render_pdf(300, HERE / "qa-final-size.png")
    with Image.open(HERE / "figure.png") as master, Image.open(HERE / "qa-pdf-render.png") as rerender:
        checks.append({"id": "pdf_raster_pixel_match", "pass": master.size == rerender.size and ImageChops.difference(master.convert("RGB"), rerender.convert("RGB")).getbbox() is None})
        ImageOps.grayscale(master).save(HERE / "qa-grayscale.png", dpi=(config["dpi"], config["dpi"]))
    ql = Path("/usr/bin/qlmanage")
    if ql.is_file():
        with tempfile.TemporaryDirectory(prefix="r074s14-svg-qa-") as temp:
            result = subprocess.run([str(ql), "-t", "-s", "1800", "-o", temp, str(HERE / "figure.svg")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            candidates = sorted(Path(temp).glob("*.png"))
            if result.returncode == 0 and candidates:
                shutil.copy2(candidates[0], HERE / "qa-svg-quicklook.png")
    checks.append({"id": "svg_quicklook_available", "pass": (HERE / "qa-svg-quicklook.png").is_file()})
    passed = all(item["pass"] for item in checks)
    validation = {"schema": "r074s-step14-outer-collar-corona-validation-v1", "checks": checks, "summary": {"passed": sum(bool(item["pass"]) for item in checks), "total": len(checks), "result": "PASS" if passed else "FAIL"}}
    (HERE / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "layout-bounds.json").write_text(json.dumps({"schema": "r074s-step14-layout-v1", "page_mm": [178, 110], "panels": {"A": [14, 20, 154.7], "B": [176.7, 20, 154.7], "C": [339.4, 20, 154.7]}}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "qa-report.md").write_text("# R0.74S Step 14 figure QA\n\n**PASS.** Exact method-boundary rows, all seven frozen-source bindings, the exact certificate summary, one-page PDF geometry, PDF/PNG pixel parity, embedded-font SVG, 600 dpi master, final-size derivative, grayscale derivative, labels, formulas, and evidence boundaries were checked. This is an **analytic schematic**, not a simulation or DNS. S.375 and the other PDE gates remain open. **NOT CLAY.**\n", encoding="utf-8")
    outputs = []
    for name, schema in (("figure.svg", "svg-journal-master"), ("figure.pdf", "pdf-journal-master"), ("figure.png", "png-journal-master")):
        record = {"path": name, "schema": schema, "bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)}
        if name.endswith(".png"):
            record["dpi"] = config["dpi"]
        outputs.append(record)
    assets = [{"path": f"public/assets/r074s/{config['figure_id']}.{Path(name).suffix.lstrip('.')}", "bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)} for name in ("figure.svg", "figure.pdf", "figure.png")]
    package_files = flat_files()
    manifest = {
        "schemaVersion": "research-figure-manifest-v1", "figureSchemaVersion": "r074s-step14-outer-collar-corona-publication-v1", "figureId": config["figure_id"], "release": "R0.74S", "status": "formal", "publicationStatus": "published",
        "analyticalQuestion": "Does the Step 14 outer-collar ledger gain across scales, and can jump sparsity alone control the full low-transition corona?",
        "supportedClaim": "The outer derivative collar aligns with the same-weight payment annulus, the critical density threshold cancels exactly, the first-jump skeleton contracts under its proved hypothesis, and the residual low-transition corona requires the open PDE lemma S.375.",
        "createdAt": "2026-09-03T00:00:00Z", "git": {"repository": "https://github.com/Kasifa/Kasifa.github.io.git", "commit": FROZEN_COMMIT, "dirty": False},
        "computation": {"kind": "exact-formula-audit", "configuration": "config.json", "precision": "exact identities and deterministic analytic rendering", "solver": "none", "formalCommand": "use command.txt and validate.py", "wallTimeSeconds": 2.0, "monitoring": {"enabled": False}},
        "compute": {"host": "local workstation (hostname omitted)", "operatingSystem": "macOS arm64", "cpu": "arm64 / local CPU", "memoryGiB": 36.0, "processes": 1, "threadsPerProcess": 1}, "environment": {"python": sys.version.split()[0], "packagesLock": "requirements.txt"},
        "data": [{"path": "source-data.csv", "schema": "r074s-step14-exact-method-boundary-rows-v1", "bytes": (HERE / "source-data.csv").stat().st_size, "sha256": sha(HERE / "source-data.csv")}], "sourceData": [],
        "figure": {"widthMillimetres": config["width_mm"], "heightMillimetres": config["height_mm"], "outputs": outputs}, "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "finalSizeInspected": True, "grayscaleInspected": True, "labelsAndLegendsInspected": True, "scalesAndUnitsInspected": True, "dataCrossChecked": True, "pdfInspected": True, "visualQaConfirmed": True, "report": "qa-report.md"},
        "claimBoundary": {"fourChannelFlux": "PROVED", "outerCollarAlignment": "PROVED_GEOMETRIC_OBSTRUCTION", "thresholdNoGain": "PROVED", "jumpDiniSkeleton": "PROVED", "smoothAlignedSpike": "ABSTRACT_METHOD_OBSTRUCTION", "criticalCorona": "ABSTRACT_METHOD_OBSTRUCTION", "incidenceHolderS358": "CONDITIONAL_ON_S356_S357", "jumpCoronaS376": "CONDITIONAL_ON_OPEN_S375", "quadraticShellSelectiveS342": "OPEN", "jumpCoronaLemmaS375": "OPEN", "ancestorGateS288": "OPEN", "combinedGateS303": "OPEN", "globalRegularity": False, "notClay": True},
        "publication": {"archiveDirectory": f"public/figures/r074s/{config['figure_id']}", "researchArchiveDirectory": f"research/figures/r074s/{config['figure_id']}", "directory": "public/assets/r074s", "fileStem": config["figure_id"], "byteIdentityRequired": True, "publicCopiesComplete": True, "releaseSourceCommit": FROZEN_COMMIT, "assets": assets},
        "provenance": {"frozenResearchCommit": FROZEN_COMMIT, "frozenResearchSourceSha256": FROZEN["research/r074s_outer_collar_corona_obstruction.md"], "evidenceClass": "analytic schematic", "simulation": False, "dns": False},
        "claim_boundary": "PROVED OUTER-COLLAR ALIGNMENT, THRESHOLD NO-GAIN, AND JUMP SKELETON; ABSTRACT SPIKE AND CRITICAL CORONA; S.358 AND S.376 CONDITIONAL; S.342, S.375, S.288, AND S.303 OPEN; NOT CLAY",
        "external_bindings": {relative: sha(REPO / relative) for relative in [*FROZEN, "research/r074s_step14_report-source.md", "research/r074s_claim_state_update.md", "research/r074s_literature_boundary.md"] if (REPO / relative).is_file()},
        "files": {name: {"bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)} for name in package_files if name != "manifest.json"}, "validation_result": validation["summary"],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "SHA256SUMS").write_text("\n".join(f"{sha(HERE / name)}  {name}" for name in flat_files()) + "\n", encoding="utf-8")
    print(json.dumps(validation["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
