#!/usr/bin/env python3
"""Validate the R0.72L formal figure package and public masters."""

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


def relerr(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def check(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {"name": name, "passed": bool(passed), "value": value, "requirement": requirement}


def load_rows() -> list[dict[str, str]]:
    with (ROOT / "data.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def ledger_values(r_value: float, p_value: float, epsilon: float) -> dict[str, float]:
    ell = 1.0 + math.log(r_value)
    u0 = epsilon ** (4.0 / 3.0) * p_value ** (4.0 / 3.0)
    w_value = epsilon ** (1.0 / 3.0) * p_value ** (1.0 / 3.0) * r_value ** (-1.0 / 3.0) * ell ** (-0.5)
    u_value = epsilon ** (7.0 / 3.0) * p_value ** (4.0 / 3.0)
    v_value = epsilon ** (1.0 / 3.0) * p_value ** (1.0 / 3.0) * r_value
    h_value = u_value / v_value
    z_value = epsilon**2 * p_value**2 * r_value ** (2.0 / 3.0) * (1.0 + epsilon) ** (-2.0 / 3.0) * (1.0 + math.log(2.0 + r_value**2 * (1.0 + epsilon)))
    return {"U0": u0, "W": w_value, "U": u_value, "H": h_value, "Z": z_value}


def main() -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    rows = load_rows()
    items: list[dict[str, Any]] = []
    required = ["figure.pdf", "figure.svg", "figure.png", "data.csv", "results.json", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "caption.md", "contract.json", "config.json", "figure-contract.md", "plot.py"]
    missing = [name for name in required if not (ROOT / name).is_file()]
    items.append(check("required_assets", not missing, missing, "all masters, data, QA, and contract assets exist"))

    width_mm = float(config["figure"]["widthMillimetres"])
    height_mm = float(config["figure"]["heightMillimetres"])
    png_dpi = int(config["figure"]["pngDpi"])
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        dpi_meta = image.info.get("dpi", (0.0, 0.0))
    expected_png = (round(width_mm / 25.4 * png_dpi), round(height_mm / 25.4 * png_dpi))
    items.append(check("png_600_dpi", all(abs(float(value) - png_dpi) < 0.02 for value in dpi_meta), dpi_meta, "PNG metadata is 600 dpi"))
    items.append(check("png_dimensions", abs(png_size[0] - expected_png[0]) <= 2 and abs(png_size[1] - expected_png[1]) <= 2, {"actual": png_size, "expected": expected_png}, "PNG pixels agree with 177.8 x 124.0 mm at 600 dpi within renderer rounding"))

    reader = PdfReader(str(ROOT / "figure.pdf"))
    page = reader.pages[0]
    pdf_mm = (float(page.mediabox.width) * 25.4 / 72.0, float(page.mediabox.height) * 25.4 / 72.0)
    items.append(check("pdf_one_page", len(reader.pages) == 1, len(reader.pages), "PDF has one page"))
    items.append(check("pdf_dimensions", abs(pdf_mm[0] - width_mm) < 0.08 and abs(pdf_mm[1] - height_mm) < 0.08, pdf_mm, "PDF is 177.8 x 124.0 mm within Matplotlib point rounding"))
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    items.append(check("svg_vector_text", "<svg" in svg and "<text" in svg and "<image" not in svg, {"hasSvg": "<svg" in svg, "hasText": "<text" in svg, "hasEmbeddedImage": "<image" in svg}, "SVG remains vector and keeps editable text"))

    qa_dpi = int(config["figure"]["qaDpi"])
    qa_expected = (round(width_mm / 25.4 * qa_dpi), round(height_mm / 25.4 * qa_dpi))
    qa_sizes: dict[str, tuple[int, int]] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(ROOT / name) as image:
            qa_sizes[name] = image.size
    items.append(check("qa_surface_dimensions", all(size == qa_expected for size in qa_sizes.values()), qa_sizes, "all QA surfaces match final print size at 180 dpi"))
    with Image.open(ROOT / "qa-grayscale.png") as image:
        gray_std = float(ImageStat.Stat(image.convert("L")).stddev[0])
    items.append(check("grayscale_contrast", gray_std > 20.0, gray_std, "grayscale surface retains substantial tonal contrast"))

    panel_a = [row for row in rows if row["panel"] == "A"]
    a_errors: list[float] = []
    for row in panel_a:
        r_value = float(row["x"])
        p_value = 1.0 if row["series"] == "p = 1" else r_value ** -0.5
        expected = p_value ** (2.0 / 3.0) * r_value ** (2.0 / 3.0) * (1.0 + math.log(r_value))
        a_errors.append(relerr(float(row["y"]), expected))
    items.append(check("panel_a_equation", max(a_errors) < 2.0e-15 and len(panel_a) == 362, {"rows": len(panel_a), "maxRelativeError": max(a_errors)}, "panel A samples equation (0.9) exactly to binary64 precision"))

    panel_b = [row for row in rows if row["panel"] == "B"]
    r_b = float(config["panels"]["B"]["R"])
    p_b = r_b ** -0.5
    k_b = float(config["panels"]["B"]["K"])
    b_errors: list[float] = []
    for row in panel_b:
        epsilon = float(row["rawValue"])
        parts = ledger_values(r_b, p_b, epsilon)
        values = {
            "first-root term": parts["U0"] / (k_b + parts["Z"]),
            "mixed-row term": parts["W"] / math.sqrt(k_b + parts["Z"]),
            "true-cubic term": parts["U"] / (k_b + max(parts["H"], parts["Z"])),
        }
        expected = sum(values.values()) if row["series"] == "three-term sum" else values[row["series"]]
        b_errors.append(relerr(float(row["y"]), expected))
    items.append(check("panel_b_equation", max(b_errors) < 2.0e-15 and len(panel_b) == 644, {"rows": len(panel_b), "maxRelativeError": max(b_errors)}, "panel B recomputes equations (0.4), (0.7), and (0.8)"))

    slopes = results["summary"]["panelCSlopesLastFour"]
    root_counts = results["summary"]["panelCRootCounts"]
    items.append(check("galerkin_linear_rows", 0.96 < float(slopes["G"]) < 1.03 and 0.96 < float(slopes["C"]) < 1.04, slopes, "finite projected G and cubic tail slopes are near one"))
    items.append(check("galerkin_bounded_mixed_row", abs(float(slopes["EQ"])) < 0.02, slopes["EQ"], "finite projected mixed-row tail slope is near zero"))
    items.append(check("galerkin_many_roots", all(left < right for left, right in zip(root_counts, root_counts[1:])) and root_counts[-1] >= 200, root_counts, "projected root counts grow monotonically and reach at least 200"))
    items.append(check("finite_not_pde", results.get("newPdeEvolution") is False and results.get("finiteProjectedOdeOnly") is True, {"newPdeEvolution": results.get("newPdeEvolution"), "finiteProjectedOdeOnly": results.get("finiteProjectedOdeOnly")}, "finite solve is explicitly a projected-ODE diagnostic"))

    ratio = float(results["summary"]["outsideOverInside"])
    items.append(check("exact_leakage_ratio", relerr(ratio, 1.0 / math.sqrt(2.0)) < 2.0e-15, ratio, "outside-to-inside norm ratio equals 1/sqrt(2)"))
    d_rows = [row for row in rows if row["panel"] == "D" and row["series"] == "omitted-shell support"]
    items.append(check("omitted_shell_support", sorted(float(row["y"]) for row in d_rows) == [-2.0, 2.0], [row["y"] for row in d_rows], "the first omitted shell is plus-or-minus 2R"))

    source_hashes = results["sourceSha256"]
    changed_sources = []
    for relative, expected in source_hashes.items():
        path = REPOSITORY / relative
        if not path.is_file() or digest(path) != expected:
            changed_sources.append(relative)
    items.append(check("source_lineage", not changed_sources, changed_sources, "all report and contract sources retain their build hashes"))
    output_hashes = results["outputSha256"]
    changed_outputs = [name for name, expected in output_hashes.items() if not (ROOT / name).is_file() or digest(ROOT / name) != expected]
    items.append(check("output_lineage", not changed_outputs, changed_outputs, "all masters and plotted data retain their build hashes"))

    publication = config["publication"]
    public_dir = REPOSITORY / publication["directory"]
    public_status: dict[str, bool] = {}
    for suffix in ("pdf", "svg", "png"):
        target = public_dir / f"{publication['stem']}.{suffix}"
        public_status[suffix] = target.is_file() and digest(target) == digest(ROOT / f"figure.{suffix}")
    items.append(check("public_byte_identity", all(public_status.values()), public_status, "public PDF, SVG, and PNG are byte-identical to masters"))

    caption = (ROOT / "caption.md").read_text(encoding="utf-8")
    boundary = str(contract["claimBoundary"])
    combined = caption + "\n" + boundary
    boundary_terms = ["not a full-lattice", "unresolved", "do not prove", "general three-dimensional Navier"]
    items.append(check("claim_boundary", all(term.lower() in combined.lower() for term in boundary_terms), boundary_terms, "caption and contract separate finite diagnostics from analytic and general-PDE claims"))
    visual = os.environ.get("R072L_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    items.append(check("visual_inspection_declared", visual, visual, "final-size, grayscale, and PDF-raster surfaces were explicitly inspected"))

    all_passed = all(item["passed"] for item in items)
    payload = {"schemaVersion": 1, "figureId": "R0.72L-1", "status": "passed" if all_passed else "failed", "allPassed": all_passed, "checkCount": len(items), "checks": items}
    (ROOT / "validation.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    failed = [item["name"] for item in items if not item["passed"]]
    qa_report = "\n".join([
        "# R0.72L figure QA report",
        "",
        f"- Automatic validation: **{'PASS' if all_passed else 'FAIL'}** ({len(items)} checks).",
        f"- Final print size: {pdf_mm[0]:.3f} x {pdf_mm[1]:.3f} mm (PDF); {png_size[0]} x {png_size[1]} px at 600 dpi (PNG).",
        f"- QA surfaces: {qa_expected[0]} x {qa_expected[1]} px at 180 dpi.",
        f"- Grayscale standard deviation: {gray_std:.3f}.",
        f"- Projected-ODE tail slopes: G={float(slopes['G']):.4f}, C={float(slopes['C']):.4f}, E_Q={float(slopes['EQ']):.4f}.",
        "- Human inspection: final-size, grayscale, and PDF-raster surfaces checked for legibility, collisions, hatching, units, and boundary language." if visual else "- Human inspection: not declared.",
        "- Claim boundary: Panel C is a projected-ODE diagnostic; Panel D prevents a full-lattice embedding; the extreme region remains unresolved.",
        f"- Failed checks: {', '.join(failed) if failed else 'none'}.",
        "",
    ])
    (ROOT / "qa-report.md").write_text(qa_report, encoding="utf-8")
    print(json.dumps({"status": payload["status"], "checks": len(items), "failed": failed}, sort_keys=True))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
