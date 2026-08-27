#!/usr/bin/env python3
"""Validate the R0.72J formal figure package and public copies."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat

try:
    from pypdf import PdfReader
except ModuleNotFoundError:
    bundled = sorted(
        Path.home().glob(
            ".cache/codex-runtimes/codex-primary-runtime/dependencies/"
            "python/lib/python*/site-packages"
        )
    )
    if not bundled:
        raise
    sys.path.insert(0, str(bundled[-1]))
    from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def item(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def pdf_geometry(path: Path) -> tuple[int, float, float]:
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    pages = re.search(r"^Pages:\s+(\d+)$", output, re.MULTILINE)
    size = re.search(
        r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts",
        output,
        re.MULTILINE,
    )
    if pages is None or size is None:
        raise RuntimeError("pdfinfo did not expose page geometry")
    return (
        int(pages.group(1)),
        float(size.group(1)) / 72.0 * 25.4,
        float(size.group(2)) / 72.0 * 25.4,
    )


def values(
    panels: dict[str, list[dict[str, str]]],
    panel: str,
    series: str,
    route: str,
) -> list[float]:
    selected = [
        row
        for row in panels[panel]
        if row["series"] == series and row["route"] == route
    ]
    selected.sort(key=lambda row: float(row["x"]))
    return [float(row["y"]) for row in selected]


def main() -> None:
    config = load(ROOT / "config.json")
    contract = load(ROOT / "contract.json")
    results = load(ROOT / "results.json")
    metadata = load(ROOT / "figure-data-metadata.json")
    sources = config["sourceCertificates"]
    producer = load(REPOSITORY / sources["producerResult"])
    independent = load(REPOSITORY / sources["independentResult"])
    crosscheck = load(REPOSITORY / sources["crosscheck"])
    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    panels = {
        panel: [row for row in rows if row["panel"] == panel]
        for panel in "ABCD"
    }
    expected_r = [int(value) for value in config["expected"]["rValues"]]
    producer_cases = {int(case["R"]): case for case in producer["cases"]}
    independent_cases = {int(case["R"]): case for case in independent["cases"]}

    source_paths = [REPOSITORY / row["path"] for row in metadata["sourceFiles"]]
    current_sources = {
        str(path.relative_to(REPOSITORY)): digest(path) for path in source_paths
    }
    recorded_sources = {
        row["path"]: row["sha256"] for row in metadata["sourceFiles"]
    }

    pages, width_mm, height_mm = pdf_geometry(ROOT / "figure.pdf")
    reader = PdfReader(ROOT / "figure.pdf")
    pypdf_pages = len(reader.pages)
    media = reader.pages[0].mediabox
    pypdf_width_mm = float(media.width) / 72.0 * 25.4
    pypdf_height_mm = float(media.height) / 72.0 * 25.4
    png = Image.open(ROOT / "figure.png")
    dpi = tuple(float(value) for value in png.info.get("dpi", (0.0, 0.0)))
    expected_width = round(
        config["figure"]["widthMillimetres"]
        / 25.4
        * config["figure"]["pngDpi"]
    )
    expected_height = round(
        config["figure"]["heightMillimetres"]
        / 25.4
        * config["figure"]["pngDpi"]
    )
    qa_final = Image.open(ROOT / "qa-final-size.png")
    qa_gray = Image.open(ROOT / "qa-grayscale.png")
    qa_pdf = Image.open(ROOT / "qa-pdf.png")
    gray_std = float(ImageStat.Stat(qa_gray).stddev[0])
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    caption = (ROOT / "caption.md").read_text(encoding="utf-8").lower()
    claim = contract["claimBoundary"].lower()

    signed_triples = values(panels, "B", "signed triples T_R", "exact")
    aligned_b0 = values(panels, "B", "aligned |b(0)|", "exact")
    raw_producer = values(panels, "C", "true raw cubic", "producer")
    raw_independent = values(panels, "C", "true raw cubic", "independent")
    normalized_producer = values(
        panels, "D", "physical normalized true cubic", "producer"
    )
    normalized_independent = values(
        panels, "D", "physical normalized true cubic", "independent"
    )
    analytic_reference = values(
        panels,
        "D",
        "R^-4/9 (1+log R)^-2/3",
        "analytic theorem reference",
    )
    analytic_rows = [
        row
        for row in panels["D"]
        if row["route"] == "analytic theorem reference"
    ]
    producer_root_max = max(
        float(case["evolvedRootResidual"]) for case in producer_cases.values()
    )
    independent_root_max = max(
        float(case["evolvedRootResidual"]) for case in independent_cases.values()
    )
    raw_slope = float(producer["slopes"]["rawTrueCubicTail"])
    normalized_slope = float(producer["slopes"]["normalizedTrueCubicTail"])
    raw_range = config["expected"]["rawTailSlopeRange"]
    normalized_range = config["expected"]["normalizedTailSlopeRange"]
    expected_analytic_reference = [
        float(row["x"]) ** (-4.0 / 9.0)
        * (1.0 + math.log(float(row["x"]))) ** (-2.0 / 3.0)
        for row in analytic_rows
    ]

    public_dir = REPOSITORY / config["publication"]["directory"]
    public_stem = config["publication"]["stem"]
    public_paths = {
        suffix: public_dir / f"{public_stem}.{suffix}"
        for suffix in ("pdf", "svg", "png")
    }
    public_matches = {
        suffix: path.exists() and digest(path) == digest(ROOT / f"figure.{suffix}")
        for suffix, path in public_paths.items()
    }

    exact_triple_formula = [3.0 * R * (R + 1) for R in expected_r]
    exact_b0_formula = [value / (2.0**0.5) for value in exact_triple_formula]
    panel_counts = {key: len(value) for key, value in panels.items()}
    checks = [
        item("producer_passed", producer["status"] == "passed", producer["status"], "producer status is passed"),
        item("producer_checks", all(producer["checks"].values()), producer["checks"], "all producer checks pass"),
        item("independent_passed", independent["status"] == "passed", independent["status"], "independent status is passed"),
        item("independent_checks", all(independent["checks"].values()), independent["checks"], "all independent checks pass"),
        item("crosscheck_passed", crosscheck["status"] == "passed", crosscheck["status"], "cross-route audit passes"),
        item("r_grid", sorted(producer_cases) == expected_r and sorted(independent_cases) == expected_r, {"producer": sorted(producer_cases), "independent": sorted(independent_cases)}, "both certificate grids match the contract"),
        item("producer_root_residual", producer_root_max <= config["expected"]["maximumProducerRootResidual"], producer_root_max, "producer complex-root residuals meet the contract"),
        item("independent_root_residual", independent_root_max <= config["expected"]["maximumIndependentRootResidual"], independent_root_max, "independent complex-root residuals meet the contract"),
        item("source_lineage", current_sources == recorded_sources, {"current": current_sources, "recorded": recorded_sources}, "source hashes match"),
        item("data_rows", len(rows) == metadata["rowCount"] == results["summary"]["rowCount"], {"rows": len(rows), "metadata": metadata["rowCount"], "summary": results["summary"]["rowCount"]}, "data row counts agree"),
        item("panel_coverage", all(panel_counts[key] > 0 for key in "ABCD"), panel_counts, "all four panels have data"),
        item("graph_examples", panel_counts["A"] == 3 and {row["series"] for row in panels["A"]} == {"{2,6} / gcd 2 -> {1,3}", "{1,4}", "S_R={R,...,3R-1}"}, [row["series"] for row in panels["A"]], "all classification examples are present"),
        item("signed_triangle_formula", all(abs(left - right) < 1.0e-12 for left, right in zip(signed_triples, exact_triple_formula, strict=True)), signed_triples, "T_R=3R(R+1) exactly"),
        item("aligned_b0_formula", all(abs(left - right) / right < 1.0e-14 for left, right in zip(aligned_b0, exact_b0_formula, strict=True)), aligned_b0, "aligned |b(0)|=T_R/sqrt(2)"),
        item("raw_route_overlay", len(raw_producer) == len(raw_independent) == len(expected_r), {"producer": raw_producer, "independent": raw_independent}, "both raw-cubic routes are plotted"),
        item("normalized_route_overlay", len(normalized_producer) == len(normalized_independent) == len(expected_r), {"producer": normalized_producer, "independent": normalized_independent}, "both normalized routes are plotted"),
        item("true_cubic_crosscheck", crosscheck["maximumRelativeErrors"]["deltaIntegralAbsHB"] <= config["expected"]["maximumTrueCubicCrossRelativeError"], crosscheck["maximumRelativeErrors"]["deltaIntegralAbsHB"], "true cubic cross-route error meets the contract"),
        item("raw_cubic_increases", all(right > left for left, right in zip(raw_producer, raw_producer[1:])), raw_producer, "raw true cubic increases"),
        item("normalized_cubic_decreases", all(right < left for left, right in zip(normalized_producer, normalized_producer[1:])), normalized_producer, "normalized true cubic decreases"),
        item("raw_tail_slope", raw_range[0] <= raw_slope <= raw_range[1], raw_slope, "raw tail slope is consistent with order R^2"),
        item("normalized_tail_slope", normalized_range[0] <= normalized_slope <= normalized_range[1], normalized_slope, "normalized tail slope is consistent with decay"),
        item(
            "analytic_reference_unfitted",
            len(analytic_reference) == 64
            and all(
                abs(value - expected) <= 1.0e-14 * max(1.0, abs(expected))
                for value, expected in zip(
                    analytic_reference,
                    expected_analytic_reference,
                    strict=True,
                )
            )
            and all(
                "not plotted" in row["auxiliary"]
                and "not fitted" in row["auxiliary"]
                and row["source"] == "research/r072j_report-source.md"
                for row in analytic_rows
            ),
            {
                "rows": len(analytic_reference),
                "first": analytic_reference[0],
                "last": analytic_reference[-1],
                "source": sorted({row["source"] for row in analytic_rows}),
            },
            "R^-4/9(1+log R)^-2/3 is retained only as an unfitted theorem-rate reference from the R0.72J report",
        ),
        item("ode_not_recomputed", metadata["odeRecomputed"] is False, metadata["odeRecomputed"], "figure build reads sealed certificates only"),
        item("result_summary", results["allRequiredSourceChecksPassed"] is True, results["summary"], "result summary records passing sources"),
        item("pdf_geometry", pages == 1 and abs(width_mm - 177.8) < 0.06 and abs(height_mm - 130.0) < 0.06, {"pages": pages, "widthMm": width_mm, "heightMm": height_mm}, "pdfinfo reports contracted one-page geometry"),
        item("pypdf_reopen", pypdf_pages == 1 and abs(pypdf_width_mm - 177.8) < 0.06 and abs(pypdf_height_mm - 130.0) < 0.06, {"pages": pypdf_pages, "widthMm": pypdf_width_mm, "heightMm": pypdf_height_mm}, "pypdf reopens the final PDF with contracted geometry"),
        item("png_geometry", abs(png.size[0] - expected_width) <= 1 and abs(png.size[1] - expected_height) <= 1 and min(dpi) >= 599.0, {"pixels": png.size, "expected": [expected_width, expected_height], "dpi": dpi}, "PNG is 600 dpi at contracted size"),
        item("svg_vector", "<svg" in svg and "<path" in svg and "image/png" not in svg, {"bytes": len(svg.encode("utf-8"))}, "SVG is vector without embedded PNG"),
        item("svg_titles", all(text in svg for text in ("Gcd-reduced carrier graph", "Exact triangle coefficient", "True raw cubic", "Physical normalization")), "panel titles found", "editable SVG retains panel titles as text"),
        item("qa_surfaces", qa_final.size == qa_gray.size == qa_pdf.size and min(qa_final.size) > 500, {"final": qa_final.size, "gray": qa_gray.size, "pdf": qa_pdf.size}, "QA surfaces share final aspect ratio"),
        item("grayscale_contrast", gray_std > 20.0, gray_std, "grayscale QA retains contrast"),
        item("caption_boundary", all(term in caption for term in ("one exact complex root", "does not enumerate complete roots", "1+log r", "not as a fit", "does not prove")), caption[-520:], "caption states the corrected theorem rate plus root, fit, and general-claim boundaries"),
        item("claim_boundary", all(term in claim for term in ("one complex root only", "does not enumerate complete roots", "does not prove")), contract["claimBoundary"], "contract states the mathematical boundary"),
        item("public_copies", all(public_matches.values()), public_matches, "public PDF, SVG, and PNG are byte-identical to masters"),
    ]
    report = {
        "schemaVersion": "r072j-figure-validation-v1",
        "allPassed": all(row["passed"] for row in checks),
        "passedCount": sum(row["passed"] for row in checks),
        "requiredCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# R0.72J figure QA report",
        "",
        f"- Result: {'PASS' if report['allPassed'] else 'FAIL'}",
        f"- Checks: {report['passedCount']}/{report['requiredCount']}",
        f"- PDF geometry: {width_mm:.3f} x {height_mm:.3f} mm",
        f"- PNG: {png.size[0]} x {png.size[1]} px at {dpi[0]:.1f} dpi",
        f"- Grayscale standard deviation: {gray_std:.3f}",
        f"- Raw cubic tail slope: {raw_slope:.6f}",
        f"- Normalized cubic tail slope: {normalized_slope:.6f}",
        f"- Maximum raw-cubic cross-route relative error: {crosscheck['maximumRelativeErrors']['deltaIntegralAbsHB']:.6g}",
        f"- Public masters byte-identical: {all(public_matches.values())}",
        "",
        "The QA verifies finite evidence and layout. It does not certify complete roots or a general Navier-Stokes theorem.",
    ]
    (ROOT / "qa-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["allPassed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
