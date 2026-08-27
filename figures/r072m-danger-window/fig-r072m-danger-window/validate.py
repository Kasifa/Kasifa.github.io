#!/usr/bin/env python3
"""Validate the R0.72M formal figure package and public masters."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def check(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "value": value, "requirement": requirement}


def relerr(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def main() -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    with (ROOT / "data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    items: list[dict[str, Any]] = []
    required = [
        "README.md", "caption.md", "figure-contract.md", "contract.json", "config.json",
        "plot.py", "qa_images.py", "publish_assets.py", "build_manifest.py", "figure.pdf",
        "figure.svg", "figure.png", "data.csv", "results.json", "qa-final-size.png",
        "qa-grayscale.png", "qa-pdf.png", "progress.ndjson", "resource-log.ndjson",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    items.append(check("required_assets", not missing, missing, "all masters, data, QA, and archive sources exist"))

    width_mm = float(config["figure"]["widthMillimetres"]); height_mm = float(config["figure"]["heightMillimetres"])
    png_dpi = int(config["figure"]["pngDpi"])
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size; dpi_meta = image.info.get("dpi", (0.0, 0.0))
    expected_png = (round(width_mm / 25.4 * png_dpi), round(height_mm / 25.4 * png_dpi))
    items.append(check("png_600_dpi", all(abs(float(value) - png_dpi) < 0.02 for value in dpi_meta), dpi_meta, "PNG metadata is 600 dpi"))
    items.append(check("png_dimensions", all(abs(left - right) <= 2 for left, right in zip(png_size, expected_png)), {"actual": png_size, "expected": expected_png}, "PNG pixels match final size at 600 dpi"))
    reader = PdfReader(str(ROOT / "figure.pdf")); page = reader.pages[0]
    pdf_mm = (float(page.mediabox.width) * 25.4 / 72.0, float(page.mediabox.height) * 25.4 / 72.0)
    items.append(check("pdf_one_page", len(reader.pages) == 1, len(reader.pages), "PDF has one page"))
    items.append(check("pdf_dimensions", abs(pdf_mm[0] - width_mm) < 0.08 and abs(pdf_mm[1] - height_mm) < 0.08, pdf_mm, "PDF matches 177.8 x 124.0 mm"))
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    items.append(check("svg_vector_text", "<svg" in svg and "<text" in svg and "<image" not in svg, {"svg": "<svg" in svg, "text": "<text" in svg, "image": "<image" in svg}, "SVG is vector and keeps editable text"))

    qa_dpi = int(config["figure"]["qaDpi"]); qa_expected = (round(width_mm / 25.4 * qa_dpi), round(height_mm / 25.4 * qa_dpi))
    qa_sizes: dict[str, tuple[int, int]] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(ROOT / name) as image:
            qa_sizes[name] = image.size
    items.append(check("qa_dimensions", all(size == qa_expected for size in qa_sizes.values()), qa_sizes, "QA surfaces match final print size at 180 dpi"))
    with Image.open(ROOT / "qa-grayscale.png") as image:
        gray_std = float(ImageStat.Stat(image.convert("L")).stddev[0])
    items.append(check("grayscale_contrast", gray_std > 20.0, gray_std, "grayscale surface retains contrast"))

    panel_a = [row for row in rows if row["panel"] == "A"]
    errors_a = []
    for row in panel_a:
        kappa = float(row["series"].split("=")[1]); r_value = float(row["x"])
        errors_a.append(relerr(float(row["y"]), min(r_value, 1.0) / (kappa + r_value)))
    items.append(check("panel_a_formula", len(panel_a) == 3 * int(config["panels"]["A"]["samples"]) and max(errors_a) < 2.0e-15, {"rows": len(panel_a), "maxRelativeError": max(errors_a)}, "Panel A samples the exact scalar formula"))
    panel_b = [row for row in rows if row["panel"] == "B"]
    formulas = {
        "K/U": lambda sigma: sigma ** (-1.0 / 3.0),
        "x/H": lambda sigma: sigma ** (-2.0 / 3.0) * math.log(sigma),
        "Vx/K": lambda sigma: sigma ** (-1.0 / 3.0) * math.log(sigma),
    }
    errors_b = [relerr(float(row["y"]), formulas[row["series"]](float(row["x"]))) for row in panel_b]
    items.append(check("panel_b_formula", len(panel_b) == 3 * int(config["panels"]["B"]["samples"]) and max(errors_b) < 2.0e-15, {"rows": len(panel_b), "maxRelativeError": max(errors_b)}, "Panel B samples the fixed-geometry exponent ledger"))

    cert = REPOSITORY / config["certificateDirectory"]
    cross = json.loads((cert / "crosscheck.json").read_text(encoding="utf-8"))
    items.append(check("certificate_crosscheck", cross.get("status") == "passed", cross.get("status"), "producer and independent certificate crosscheck passes"))
    frozen = [row for row in rows if row["panel"] == "C"]
    target = 16.0 / math.pi**2
    final_errors = {series: relerr(float(sorted((row for row in frozen if row["series"] == series), key=lambda row: float(row["x"]))[-1]["y"]), target) for series in ("producer", "independent")}
    items.append(check("frozen_constant_trend", all(error < 0.14 for error in final_errors.values()), final_errors, "largest finite frozen ratios lie within 14 percent of 16/pi^2"))
    diagnostic = [row for row in rows if row["panel"] == "D"]
    items.append(check("dissipative_two_routes", len(diagnostic) == 8 and {row["series"] for row in diagnostic} == {"FFT split", "Cayley split"}, {"rows": len(diagnostic), "series": sorted({row["series"] for row in diagnostic})}, "Panel D contains two four-case finite diagnostic routes"))

    changed_sources = [relative for relative, expected in results["sourceSha256"].items() if not (REPOSITORY / relative).is_file() or digest(REPOSITORY / relative) != expected]
    changed_outputs = [name for name, expected in results["outputSha256"].items() if not (ROOT / name).is_file() or digest(ROOT / name) != expected]
    items.append(check("source_lineage", not changed_sources, changed_sources, "all source hashes retain build lineage"))
    items.append(check("output_lineage", not changed_outputs, changed_outputs, "all figure outputs retain build hashes"))
    publication = config["publication"]; public_dir = REPOSITORY / publication["directory"]
    identity = {suffix: (public_dir / f"{publication['stem']}.{suffix}").is_file() and digest(public_dir / f"{publication['stem']}.{suffix}") == digest(ROOT / f"figure.{suffix}") for suffix in ("pdf", "svg", "png")}
    items.append(check("public_byte_identity", all(identity.values()), identity, "public masters are byte-identical"))
    combined = (ROOT / "caption.md").read_text(encoding="utf-8") + "\n" + str(contract["claimBoundary"])
    boundary_terms = ["diagnostic only", "not the dissipative", "do not prove", "general three-dimensional"]
    items.append(check("claim_boundary", all(term.lower() in combined.lower() for term in boundary_terms), boundary_terms, "caption and contract separate proof from diagnostics and the Clay problem"))
    visual = os.environ.get("R072M_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    items.append(check("visual_inspection_declared", visual, visual, "final-size, grayscale, and PDF raster were explicitly inspected"))

    all_passed = all(item["passed"] for item in items)
    payload = {"schemaVersion": 1, "figureId": "R0.72M-1", "status": "passed" if all_passed else "failed", "allPassed": all_passed, "checkCount": len(items), "checks": items}
    (ROOT / "validation.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failed = [item["name"] for item in items if not item["passed"]]
    (ROOT / "qa-report.md").write_text("\n".join([
        "# R0.72M figure QA report", "", f"- Automatic validation: **{'PASS' if all_passed else 'FAIL'}** ({len(items)} checks).",
        f"- Final print size: {pdf_mm[0]:.3f} x {pdf_mm[1]:.3f} mm; PNG {png_size[0]} x {png_size[1]} px at 600 dpi.",
        f"- QA surfaces: {qa_expected[0]} x {qa_expected[1]} px at 180 dpi; grayscale standard deviation {gray_std:.3f}.",
        "- Human inspection: final-size, grayscale, and PDF-raster surfaces checked for legibility and collisions." if visual else "- Human inspection: not declared.",
        "- Claim boundary: Panel D is a finite dissipative diagnostic; the continuum dissipative estimate and Clay problem remain open.",
        f"- Failed checks: {', '.join(failed) if failed else 'none'}.", "",
    ]), encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(items), "failed": failed}, sort_keys=True))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
