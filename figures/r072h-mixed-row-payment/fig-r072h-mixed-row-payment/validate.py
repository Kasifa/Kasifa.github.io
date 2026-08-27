#!/usr/bin/env python3
"""Validate the R0.72H formal figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


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


def main() -> None:
    config = load(ROOT / "config.json")
    contract = load(ROOT / "contract.json")
    results = load(ROOT / "results.json")
    metadata = load(ROOT / "figure-data-metadata.json")
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load(producer_path)
    independent = load(independent_path)
    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    panels = {panel: [row for row in rows if row["panel"] == panel] for panel in "ABC"}
    expected_m = config["expected"]["mValues"]
    producer_m = [int(row["M"]) for row in producer["cases"]]
    independent_m = [int(row["M"]) for row in independent["cases"]]
    current_sources = {
        str(path.relative_to(REPOSITORY)): digest(path)
        for path in (
            producer_path,
            independent_path,
            ROOT / "config.json",
            ROOT / "contract.json",
        )
    }
    recorded_sources = {
        row["path"]: row["sha256"] for row in metadata["sourceFiles"]
    }
    pages, width_mm, height_mm = pdf_geometry(ROOT / "figure.pdf")
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
    public = REPOSITORY / config["publication"]["directory"]
    stem = config["publication"]["stem"]
    public_equal = {
        suffix: digest(ROOT / f"figure.{suffix}")
        == digest(public / f"{stem}.{suffix}")
        for suffix in ("pdf", "svg", "png")
    }
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    envelope_y = [float(row["y"]) for row in panels["A"]]
    action_rows = [
        row for row in panels["C"] if row["series"] == "action-only quotient"
    ]
    action_values = [float(row["y"]) for row in action_rows]
    moment_values = [
        float(row["y"])
        for row in panels["C"]
        if row["series"] == "moment-resolved ratio"
    ]
    caption = (ROOT / "caption.md").read_text(encoding="utf-8").lower()
    claim = contract["claimBoundary"].lower()

    checks = [
        item("producer_passed", producer["status"] == "passed", producer["status"], "producer status is passed"),
        item("independent_passed", independent["status"] == "passed", independent["status"], "independent status is passed"),
        item("producer_checks", all(producer["checks"].values()), producer["checks"], "every producer check passes"),
        item("independent_checks", all(independent["checks"].values()), independent["checks"], "every independent check passes"),
        item("m_grids", producer_m == expected_m and independent_m == expected_m, {"producer": producer_m, "independent": independent_m}, "both M grids match the contract"),
        item("cross_route", independent["maxProducerRelativeError"] <= config["expected"]["maximumCrossRouteRelativeError"], independent["maxProducerRelativeError"], "cross-route relative error is within contract"),
        item("root_residual", max(row["evolvedRootResidual"] for row in producer["cases"]) <= config["expected"]["maximumRootResidual"], max(row["evolvedRootResidual"] for row in producer["cases"]), "all evolved root residuals are within contract"),
        item("data_rows", len(rows) == 129, {"actual": len(rows), "expected": 129}, "data.csv contains all contracted rows"),
        item("panel_coverage", {key: len(value) for key, value in panels.items()} == {"A": 84, "B": 30, "C": 15}, {key: len(value) for key, value in panels.items()}, "all panel counts match"),
        item("source_lineage", current_sources == recorded_sources, {"current": current_sources, "recorded": recorded_sources}, "source hashes match"),
        item("envelope_bounds", min(envelope_y) > 0.3 and max(envelope_y) < 2.0, {"min": min(envelope_y), "max": max(envelope_y)}, "finite envelope ratio stays within analytic comparison bounds"),
        item("action_only_growth", all(right > left for left, right in zip(action_values, action_values[1:])), action_values, "action-only quotient grows across the sweep"),
        item("moment_ratio_stable", max(moment_values) / min(moment_values) < 1.10, moment_values, "moment-resolved ratio remains stable"),
        item("result_summary", results["allRequiredSourceChecksPassed"] is True and results["summary"]["rowCount"] == len(rows), results["summary"], "result summary matches data"),
        item("pdf_geometry", pages == 1 and abs(width_mm - 177.8) < 0.06 and abs(height_mm - 96.0) < 0.06, {"pages": pages, "widthMm": width_mm, "heightMm": height_mm}, "one-page PDF has contracted size"),
        item(
            "png_geometry",
            abs(png.size[0] - expected_width) <= 1
            and abs(png.size[1] - expected_height) <= 1
            and min(dpi) >= 599.0,
            {"pixels": png.size, "expected": [expected_width, expected_height], "dpi": dpi},
            "PNG is 600 dpi within one raster pixel of the contracted size",
        ),
        item("svg_vector", "<svg" in svg and "<path" in svg and "image/png" not in svg, {"bytes": len(svg)}, "SVG is vector and contains no embedded PNG"),
        item("public_assets", all(public_equal.values()), public_equal, "public figure copies are byte-identical"),
        item("qa_surfaces", qa_final.size == qa_gray.size == qa_pdf.size and min(qa_final.size) > 500, {"final": qa_final.size, "gray": qa_gray.size, "pdf": qa_pdf.size}, "final-size, grayscale, and PDF QA surfaces match"),
        item("grayscale_contrast", gray_std > 20.0, gray_std, "grayscale QA retains contrast"),
        item("caption_boundary", all(term in caption for term in ("finite", "do not", "navier")), caption[-280:], "caption separates diagnostics from general claims"),
        item("claim_boundary", all(term in claim for term in ("triangular", "does not prove", "regularity")), contract["claimBoundary"], "contract states the mathematical boundary"),
    ]
    report = {
        "schemaVersion": "r072h-figure-validation-v1",
        "allPassed": all(row["passed"] for row in checks),
        "passedCount": sum(row["passed"] for row in checks),
        "requiredCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# R0.72H figure QA report",
        "",
        f"- Result: {'PASS' if report['allPassed'] else 'FAIL'}",
        f"- Checks: {report['passedCount']}/{report['requiredCount']}",
        f"- PDF geometry: {width_mm:.3f} x {height_mm:.3f} mm",
        f"- PNG: {png.size[0]} x {png.size[1]} px at {dpi[0]:.1f} dpi",
        f"- Grayscale standard deviation: {gray_std:.3f}",
        f"- Cross-route maximum relative error: {independent['maxProducerRelativeError']:.3e}",
        "",
        "The QA report verifies package integrity and legibility. It does not add a mathematical claim.",
    ]
    (ROOT / "qa-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["allPassed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
