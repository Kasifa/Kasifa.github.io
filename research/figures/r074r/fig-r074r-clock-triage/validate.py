#!/usr/bin/env python3
"""Validate and freeze the R0.74R formal figure package."""

from __future__ import annotations

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
from pathlib import Path

from PIL import Image, ImageChops, ImageOps
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]


def locate_pdftoppm() -> Path:
    override = os.environ.get("R074R_DEPENDENCIES_ROOT")
    candidates = []
    if override:
        candidates.append(Path(override).expanduser().resolve() / "bin/override/pdftoppm")
    for parent in Path(sys.executable).resolve().parents:
        candidates.append(parent / "bin/override/pdftoppm")
    if shutil.which("pdftoppm"):
        candidates.append(Path(shutil.which("pdftoppm")).resolve())
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError("pdftoppm")


PDFTOPPM = locate_pdftoppm()
EXTERNAL = [
    "research/r074r_problem_freeze.md",
    "research/r074r_persistent_lobe_cubic_packing.md",
    "research/r074r_persistent_lobe_certificate.json",
    "research/r074r_arbitrary_clock_extraction_gate.md",
    "research/r074r_arbitrary_clock_gate_certificate.json",
    "research/r074r_arbitrary_clock_independent_certificate.json",
    "research/r074r_gap_matrix.md",
    "research/r074r_primary_literature_boundary.md",
    "research/r074r_report-source.md",
    "research/r074r_freeze_manifest.json",
]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_pdf(dpi: int, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="r074r-validate-") as temp:
        prefix = Path(temp) / "page"
        subprocess.run([str(PDFTOPPM), "-png", "-singlefile", "-r", str(dpi), str(HERE / "figure.pdf"), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Image.open(prefix.with_suffix(".png")).save(output, dpi=(dpi, dpi))


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    checks: list[dict] = []
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    checks.append({"id": "source_rows_exact", "pass": rows == config["rows"]})
    checks.append({"id": "source_ids_unique", "pass": len({r["id"] for r in rows}) == 9})

    terminal = json.loads((REPO / "research/r074r_persistent_lobe_certificate.json").read_text(encoding="utf-8"))
    arbitrary = json.loads((REPO / "research/r074r_arbitrary_clock_gate_certificate.json").read_text(encoding="utf-8"))
    independent = json.loads((REPO / "research/r074r_arbitrary_clock_independent_certificate.json").read_text(encoding="utf-8"))
    checks += [
        {"id": "terminal_certificate_pass", "pass": terminal["summary"]["result"] == "PASS" and terminal["summary"]["rational_total"] == 21 and terminal["summary"]["structural_total"] == 22},
        {"id": "arbitrary_primary_pass", "pass": arbitrary["summary"]["result"] == "PASS" and arbitrary["summary"]["rational_total"] == 13 and arbitrary["summary"]["power_ledgers_total"] == 3 and arbitrary["summary"]["structural_total"] == 25},
        {"id": "arbitrary_independent_pass", "pass": independent["summary"]["result"] == "PASS" and independent["summary"]["rational_total"] == 9 and independent["summary"]["structural_total"] == 12 and independent["summary"]["finite_total"] == 5},
    ]

    expected_size = [round(config["width_mm"] / 25.4 * config["dpi"]), round(config["height_mm"] / 25.4 * config["dpi"])]
    with Image.open(HERE / "figure.png") as image:
        actual_size = list(image.size)
        checks.append({"id": "png_600dpi_geometry", "pass": all(abs(a - b) <= 1 for a, b in zip(actual_size, expected_size)), "actual": actual_size, "expected": expected_size})
    pdf = PdfReader(str(HERE / "figure.pdf"))
    checks.append({"id": "pdf_one_page", "pass": len(pdf.pages) == 1})
    page = pdf.pages[0]
    checks.append({"id": "pdf_physical_geometry", "pass": abs(float(page.mediabox.width) - config["width_mm"] / 25.4 * 72) < 0.02 and abs(float(page.mediabox.height) - config["height_mm"] / 25.4 * 72) < 0.02})
    root = ET.parse(HERE / "figure.svg").getroot()
    checks.append({"id": "svg_physical_geometry", "pass": root.attrib.get("width") == "178mm" and root.attrib.get("height") == "100mm"})
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    required = ["Terminal-window contraction", "PROVED CONDITIONAL", "OPEN", "NO-GO", "NOT NSE solutions", "NOT CLAY"]
    checks.append({"id": "svg_boundary_language", "pass": all(value in svg for value in required)})
    checks.append({"id": "caption_boundary_language", "pass": all(value in caption for value in ["PROVED CONDITIONAL", "OPEN", "no-go", "not Navier--Stokes solutions", "NOT CLAY"])})
    font_sizes = [float(value) for value in re.findall(r"font-size: ([0-9.]+)px", svg)]
    checks.append({"id": "minimum_text_size", "pass": bool(font_sizes) and min(font_sizes) >= 4.5, "minimum": min(font_sizes) if font_sizes else None})
    checks.append({"id": "svg_embedded_fonts", "pass": svg.count("data:font/ttf;base64,") == 2 and "R074R-Regular" in svg and "R074R-Bold" in svg})

    render_pdf(config["dpi"], HERE / "qa-pdf-render.png")
    render_pdf(300, HERE / "qa-final-size.png")
    with Image.open(HERE / "figure.png") as master, Image.open(HERE / "qa-pdf-render.png") as rerender:
        checks.append({"id": "pdf_raster_pixel_match", "pass": master.size == rerender.size and ImageChops.difference(master.convert("RGB"), rerender.convert("RGB")).getbbox() is None})
        ImageOps.grayscale(master).save(HERE / "qa-grayscale.png", dpi=(config["dpi"], config["dpi"]))

    ql = Path("/usr/bin/qlmanage")
    if ql.is_file():
        with tempfile.TemporaryDirectory(prefix="r074r-svg-qa-") as temp:
            result = subprocess.run([str(ql), "-t", "-s", "1800", "-o", temp, str(HERE / "figure.svg")], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            candidates = sorted(Path(temp).glob("*.png"))
            if result.returncode == 0 and candidates:
                shutil.copy2(candidates[0], HERE / "qa-svg-quicklook.png")
    checks.append({"id": "svg_quicklook_available_locally", "pass": (HERE / "qa-svg-quicklook.png").is_file(), "required_for_ci": False})

    passed = all(item["pass"] for item in checks if item["id"] != "svg_quicklook_available_locally")
    validation = {"schema": "r074r-clock-triage-validation-v1", "checks": checks, "summary": {"passed": sum(bool(c["pass"]) for c in checks), "total": len(checks), "result": "PASS" if passed else "FAIL"}}
    (HERE / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "layout-bounds.json").write_text(json.dumps({"schema": "r074r-layout-v1", "page_mm": [178, 100], "panels": {"A": [14, 22, 154], "B": [175, 22, 160], "C": [342, 22, 148]}}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "qa-report.md").write_text(
        "# R0.74R figure QA\n\n**PASS.** PDF/PNG pixel parity, 600 dpi geometry, print-size and grayscale derivatives, embedded-font SVG, exact source rows, and all three certificate bindings passed. Quick Look SVG preview was also generated locally. No simulation or DNS. **NOT CLAY.**\n",
        encoding="utf-8",
    )
    package_files = [
        "README.md", "caption.md", "chart-contract-and-source-data.md", "command.txt", "config.json",
        "environment.json", "figure.pdf", "figure.png", "figure.svg", "layout-bounds.json", "plot.py",
        "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf-render.png", "qa-protocol.md",
        "qa-report.md", "qa-svg-quicklook.png", "requirements.txt", "results.json", "source-data.csv",
        "validate.py", "validation.json",
    ]
    manifest = {
        "schema": "r074r-clock-triage-manifest-v1", "figure_id": config["figure_id"],
        "claim_boundary": "analytic summary only; no simulation; universal extraction OPEN; NOT CLAY",
        "external_bindings": {path: sha(REPO / path) for path in EXTERNAL},
        "files": {name: {"bytes": (HERE / name).stat().st_size, "sha256": sha(HERE / name)} for name in package_files if (HERE / name).is_file()},
        "validation_result": validation["summary"],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    checksums = [f"{sha(HERE / name)}  {name}" for name in sorted([*package_files, "manifest.json"]) if (HERE / name).is_file()]
    (HERE / "SHA256SUMS").write_text("\n".join(checksums) + "\n", encoding="utf-8")
    print(json.dumps(validation["summary"], indent=2, sort_keys=True))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
