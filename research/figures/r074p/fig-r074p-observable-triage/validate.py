#!/usr/bin/env python3
"""Independently validate and freeze the R0.74P figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import math
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
REPO = HERE.parents[3]
QUICKLOOK = Path("/usr/bin/qlmanage")


def locate_pdftoppm() -> Path:
    override = os.environ.get("R074P_DEPENDENCIES_ROOT")
    candidates = []
    if override:
        candidates.append(Path(override).expanduser().resolve() / "bin/override/pdftoppm")
    for parent in Path(sys.executable).resolve().parents:
        candidates.append(parent / "bin/override/pdftoppm")
    path_command = shutil.which("pdftoppm")
    if path_command:
        candidates.append(Path(path_command).resolve())
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError("pdftoppm; set R074P_DEPENDENCIES_ROOT or add pdftoppm to PATH")


PDFTOPPM = locate_pdftoppm()

EXTERNAL_BINDINGS = [
    REPO / "research/r074p_problem_freeze.md",
    REPO / "research/r074p_temporal_observable_triage.md",
    REPO / "research/r074p_temporal_clock_certificate.json",
    REPO / "research/r074p_temporal_clock_certificate_report.md",
    REPO / "scripts/r074p_temporal_clock_certificate.py",
    REPO / "scripts/r074p_temporal_clock_certificate_independent.rb",
    REPO / "research/r074p_certificate_independent_audit.md",
    REPO / "research/r074p_main_independent_audit.md",
    REPO / "research/r074p_gap_matrix.md",
    REPO / "research/r074p_primary_literature_boundary.md",
    REPO / "research/r074p_primary_literature_independent_audit.md",
    REPO / "research/r074p_bilingual_dictionary.md",
    REPO / "research/r074p_report-source.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def render_pdf(dpi: int, output: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="r074p-qa-pdf-") as temp_dir:
        prefix = Path(temp_dir) / "page"
        subprocess.run(
            [
                str(PDFTOPPM),
                "-png",
                "-singlefile",
                "-r",
                str(dpi),
                str(HERE / "figure.pdf"),
                str(prefix),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        image = Image.open(prefix.with_suffix(".png"))
        image.save(output, dpi=(dpi, dpi))


def check_source_data(config: dict, checks: list[dict]) -> tuple[int, int]:
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    panel_a = [row for row in rows if row["panel"] == "A"]
    panel_b = [row for row in rows if row["panel"] == "B"]
    checks.append({"id": "source_row_counts", "pass": len(panel_a) == 147 and len(panel_b) == 5})
    checks.append({"id": "source_unique_ids", "pass": len({row["item_id"] for row in rows}) == len(rows)})

    series_config = {row["id"]: row for row in config["carleson_series"]}
    panel_a_ok = True
    for row in panel_a:
        series = series_config[row["series_id"]]
        beta = Fraction(series["beta_numerator"], series["beta_denominator"])
        x_value = Fraction(row["log10_K"])
        expected = -beta * x_value
        panel_a_ok &= Fraction(row["log10_decay_term"]) == expected
        panel_a_ok &= row["sigma_or_beta_exact"] == f"{beta.numerator}/{beta.denominator}"
        panel_a_ok &= row["claim_type"] == "PROVED_RATE_ONLY"
        panel_a_ok &= "additive log10 C suppressed" in row["classification"]
    checks.append({"id": "panel_a_exact_formula_147_of_147", "pass": panel_a_ok})

    expected_b = {
        "window_sigma_1_4": ("<=", Fraction(-1, 4), "misses target"),
        "window_sigma_1_2": ("<=", Fraction(-1, 2), "misses target"),
        "window_sigma_ge_1": ("<=", Fraction(-1, 1), "misses target"),
        "matched_target_component": ("=", Fraction(0, 1), "detects target"),
        "strong_target_lower": (">=", Fraction(640, 43), "overpays"),
    }
    panel_b_ok = True
    for row in panel_b:
        relation, rate, classification = expected_b[row["item_id"]]
        panel_b_ok &= row["relation"] == relation
        panel_b_ok &= Fraction(row["rate_exact"]) == rate
        panel_b_ok &= math.isclose(float(row["rate_decimal"]), float(rate), rel_tol=0.0, abs_tol=5e-12)
        panel_b_ok &= row["classification"] == classification
    checks.append({"id": "panel_b_exact_ledger_5_of_5", "pass": panel_b_ok})
    return len(panel_a), len(panel_b)


def check_certificate(checks: list[dict]) -> str:
    path = REPO / "research/r074p_temporal_clock_certificate.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    cert = {row["id"]: Fraction(row["left"]) for row in payload["checks"]}
    expected = {
        "m_exact": Fraction(43, 423360),
        "K_exponential_rate": Fraction(43, 635040),
        "strong_exponential_penalty": Fraction(4, 3969),
    }
    checks.append({"id": "certificate_52_all_pass", "pass": len(payload["checks"]) == 52 and all(row["pass"] for row in payload["checks"])})
    checks.append({"id": "certificate_exact_inputs", "pass": all(cert[key] == value for key, value in expected.items())})
    checks.append(
        {
            "id": "strong_rate_independent_ratio",
            "pass": cert["strong_exponential_penalty"] / cert["K_exponential_rate"] == Fraction(640, 43),
        }
    )
    return sha256(path)


def check_geometry(config: dict, checks: list[dict]) -> list[int]:
    expected_w = round(config["width_mm"] / 25.4 * config["dpi"])
    expected_h = round(config["height_mm"] / 25.4 * config["dpi"])
    with Image.open(HERE / "figure.png") as image:
        actual = list(image.size)
        checks.append({"id": "png_mode_rgb", "pass": image.mode in {"RGB", "RGBA"}})
    checks.append(
        {
            "id": "png_600dpi_dimensions",
            "pass": abs(actual[0] - expected_w) <= 1 and abs(actual[1] - expected_h) <= 1,
            "actual": actual,
            "expected": [expected_w, expected_h],
        }
    )

    reader = PdfReader(str(HERE / "figure.pdf"))
    page = reader.pages[0]
    pdf_w = float(page.mediabox.width)
    pdf_h = float(page.mediabox.height)
    expected_pdf_w = config["width_mm"] / 25.4 * 72.0
    expected_pdf_h = config["height_mm"] / 25.4 * 72.0
    checks.append({"id": "pdf_one_page", "pass": len(reader.pages) == 1})
    checks.append(
        {
            "id": "pdf_page_geometry",
            "pass": abs(pdf_w - expected_pdf_w) < 0.02 and abs(pdf_h - expected_pdf_h) < 0.02,
            "actual_points": [pdf_w, pdf_h],
        }
    )

    root = ET.parse(HERE / "figure.svg").getroot()
    svg_width_attr = root.attrib["width"]
    svg_height_attr = root.attrib["height"]
    view_box = [float(value) for value in root.attrib["viewBox"].split()]
    checks.append(
        {
            "id": "svg_physical_geometry_and_units",
            "pass": (
                svg_width_attr == f"{config['width_mm']}mm"
                and svg_height_attr == f"{config['height_mm']}mm"
                and abs(view_box[2] - round(expected_pdf_w)) <= 1
                and abs(view_box[3] - round(expected_pdf_h)) <= 1
            ),
            "physical_size": [svg_width_attr, svg_height_attr],
            "view_box": view_box,
        }
    )
    return actual


def check_required_language(checks: list[dict]) -> None:
    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    required_svg = [
        "Temporal observables: miss, detect, or overpay?",
        "analytic bounds, not simulation",
        "NOT CLAY",
        "PROVED:",
        "additive log10 C suppressed",
        "OPEN: no full upper bound for Y2(sf).",
        "Target component only",
        "overpays",
    ]
    required_caption = [
        "decay-rate",
        "additive",
        "target component",
        "no upper bound for the full",
        "no simulation",
        "Clay conclusion",
    ]
    checks.append({"id": "svg_required_boundary_language", "pass": all(value in svg for value in required_svg)})
    checks.append({"id": "caption_required_boundary_language", "pass": all(value in caption for value in required_caption)})
    font_sizes = [float(value) for value in re.findall(r"font-size: ([0-9.]+)px", svg)]
    checks.append(
        {
            "id": "svg_final_size_text_minimum_5pt",
            "pass": bool(font_sizes) and min(font_sizes) >= 5.0,
            "minimum_font_size": min(font_sizes) if font_sizes else None,
        }
    )
    checks.append(
        {
            "id": "svg_fonts_embedded",
            "pass": svg.count("data:font/ttf;base64,") == 2 and "R074P-Regular" in svg and "R074P-Bold" in svg,
        }
    )
    requirements = (HERE / "requirements.txt").read_text(encoding="utf-8")
    checks.append({"id": "validator_dependencies_frozen", "pass": "pypdf==6.10.0" in requirements})


def make_qa_derivatives(config: dict, checks: list[dict]) -> None:
    render_pdf(config["dpi"], HERE / "qa-pdf-render.png")
    render_pdf(300, HERE / "qa-final-size.png")
    with Image.open(HERE / "figure.png") as master, Image.open(HERE / "qa-pdf-render.png") as rerender:
        same_size = master.size == rerender.size
        same_pixels = same_size and ImageChops.difference(master.convert("RGB"), rerender.convert("RGB")).getbbox() is None
        checks.append({"id": "independent_pdf_raster_matches_master", "pass": same_pixels})
        ImageOps.grayscale(master).save(HERE / "qa-grayscale.png", dpi=(config["dpi"], config["dpi"]))

    quicklook_ok = False
    with tempfile.TemporaryDirectory(prefix="r074p-qa-svg-") as temp_dir:
        completed = subprocess.run(
            [str(QUICKLOOK), "-t", "-s", "1800", "-o", temp_dir, str(HERE / "figure.svg")],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        candidates = sorted(Path(temp_dir).glob("*.png"))
        if completed.returncode == 0 and candidates:
            shutil.copy2(candidates[0], HERE / "qa-svg-quicklook.png")
            quicklook_ok = True
    checks.append({"id": "svg_independent_quicklook", "pass": quicklook_ok})


def write_layout_bounds() -> None:
    write_json(
        HERE / "layout-bounds.json",
        {
            "schema": "r074p-observable-triage-layout-v1",
            "canvas_points": [504.5669291338583, 283.46456692913387],
            "panel_a_points": [14, 22, 292, 225.46456692913387],
            "panel_b_points": [313, 22, 177.5669291338583, 225.46456692913387],
            "minimum_intended_font_points": 5.0,
            "final_width_mm": 178,
            "final_height_mm": 100,
            "meaning_not_color_only": ["solid/dash/dot", "direct labels", "verdict text", "rate symbols"],
            "svg_physical_units": ["178mm", "100mm"],
            "svg_font_policy": "DejaVu Sans regular and bold embedded as data fonts",
        },
    )


def freeze_manifest(validation: dict) -> None:
    excluded = {"manifest.json", "SHA256SUMS"}
    package_files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name not in excluded)
    artifact_records = [
        {"path": path.name, "bytes": path.stat().st_size, "sha256": sha256(path)} for path in package_files
    ]
    external_records = [
        {
            "path": str(path.relative_to(REPO)),
            "bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
        for path in EXTERNAL_BINDINGS
    ]
    manifest = {
        "schema": "r074p-observable-triage-manifest-v1",
        "figure_id": "fig-r074p-observable-triage",
        "claim_boundary": "PROVED analytic comparison; FINITE rendering; OPEN full square-function upper; NOT CLAY",
        "validation_pass": validation["pass"],
        "artifacts": artifact_records,
        "external_bindings": external_records,
        "sha256sums_scope": "all package files except SHA256SUMS",
    }
    write_json(HERE / "manifest.json", manifest)

    sum_files = sorted(path for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    lines = [f"{sha256(path)}  {path.name}" for path in sum_files]
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    checks: list[dict] = []
    panel_a_rows, panel_b_rows = check_source_data(config, checks)
    certificate_hash = check_certificate(checks)
    pixel_size = check_geometry(config, checks)
    check_required_language(checks)
    make_qa_derivatives(config, checks)
    write_layout_bounds()

    checks.append({"id": "required_external_bindings_present", "pass": all(path.is_file() for path in EXTERNAL_BINDINGS)})
    validation = {
        "schema": "r074p-observable-triage-validation-v1",
        "pass": all(row["pass"] for row in checks),
        "checks": checks,
        "check_count": len(checks),
        "panel_a_rows": panel_a_rows,
        "panel_b_rows": panel_b_rows,
        "pixel_size": pixel_size,
        "certificate_sha256": certificate_hash,
        "boundary": "The figure verifies an analytic exact-family comparison only; NOT CLAY.",
    }
    write_json(HERE / "validation.json", validation)

    report_lines = [
        "# R0.74P figure QA report",
        "",
        f"Overall result: **{'PASS' if validation['pass'] else 'FAIL'}**",
        "",
        f"- Exact source rows: {panel_a_rows} Panel A + {panel_b_rows} Panel B.",
        f"- 600 dpi master dimensions: {pixel_size[0]} x {pixel_size[1]} pixels.",
        "- PDF and SVG geometry independently checked at 178 mm x 100 mm.",
        "- PDF re-render compared pixel-for-pixel with the archived PNG master.",
        "- Final-size, grayscale, and independent SVG Quick Look derivatives created.",
        "- Required PROVED / OPEN / target-component / NOT CLAY language found.",
        "",
        "Visual inspection remains a human/agent QA step; this script does not infer readability from pixels.",
        "",
        "## Check ledger",
        "",
    ]
    report_lines.extend(f"- {'PASS' if row['pass'] else 'FAIL'} — `{row['id']}`" for row in checks)
    (HERE / "qa-report.md").write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    freeze_manifest(validation)
    print(json.dumps(validation, indent=2, sort_keys=True))
    if not validation["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
