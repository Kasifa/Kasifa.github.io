#!/usr/bin/env python3
"""Validate the R0.72I formal figure package."""

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


def values(
    panels: dict[str, list[dict[str, str]]], panel: str, series: str, route: str
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
    producer_csv_path = REPOSITORY / sources["producerCsv"]
    producer_result_path = REPOSITORY / sources["producerResult"]
    producer = load(producer_result_path)
    with producer_csv_path.open(encoding="utf-8") as handle:
        producer_rows = list(csv.DictReader(handle))
    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    panels = {
        panel: [row for row in rows if row["panel"] == panel]
        for panel in "ABCD"
    }
    expected_m = config["expected"]["mValues"]
    producer_m = [int(float(row["M"])) for row in producer_rows]

    source_paths = [
        REPOSITORY / row["path"] for row in metadata["sourceFiles"]
    ]
    current_sources = {
        str(path.relative_to(REPOSITORY)): digest(path) for path in source_paths
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
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    caption = (ROOT / "caption.md").read_text(encoding="utf-8").lower()
    claim = contract["claimBoundary"].lower()

    generic_term = values(panels, "A", "generic B term", "producer")
    first_term = values(panels, "A", "initial trace", "producer")
    mixed_term = values(panels, "A", "mixed moment", "producer")
    generic_over_measured = values(
        panels,
        "B",
        "generic bound / measured cubic exposure",
        "producer",
    )
    measured_bv = values(panels, "C", "measured BV upper", "producer")
    exact_root = values(panels, "C", "one exact-root atom", "producer")
    numeric_envelope = values(
        panels, "D", "numeric coupling envelope", "numeric maximization"
    )
    analytic_envelope = values(
        panels, "D", "analytic M^(-4/9) log^(-2/3)", "analytic"
    )
    envelope_error = max(
        abs(left - right) / right
        for left, right in zip(numeric_envelope, analytic_envelope, strict=True)
    )
    independent_rows = [row for row in rows if row["route"] == "independent"]
    independent_csv_exists = (REPOSITORY / sources["independentCsv"]).exists()
    independent_consistent = (not independent_csv_exists and not independent_rows) or (
        independent_csv_exists and bool(independent_rows)
    )
    root_residual = max(float(row["evolvedRootResidual"]) for row in producer_rows)
    root_rescaled = [float(row["exactRootRatioRescaled"]) for row in producer_rows]

    checks = [
        item("producer_passed", producer["status"] == "passed", producer["status"], "producer status is passed"),
        item("producer_checks", all(producer["checks"].values()), producer["checks"], "every producer check passes"),
        item("m_grid", producer_m == expected_m, producer_m, "producer M grid matches the contract"),
        item("root_residual", root_residual <= config["expected"]["maximumRootResidual"], root_residual, "all exact-root residuals satisfy the contract"),
        item("root_rescaled_spread", max(root_rescaled) / min(root_rescaled) <= config["expected"]["maximumRootRescaledSpread"], root_rescaled, "rescaled exact-root ratio is stable"),
        item("source_lineage", current_sources == recorded_sources, {"current": current_sources, "recorded": recorded_sources}, "source hashes match"),
        item("data_rows", len(rows) == metadata["rowCount"] == results["summary"]["rowCount"], {"rows": len(rows), "metadata": metadata["rowCount"], "summary": results["summary"]["rowCount"]}, "data row counts agree"),
        item("panel_coverage", all(len(panels[key]) > 0 for key in "ABCD"), {key: len(value) for key, value in panels.items()}, "all four panels have data"),
        item("independent_overlay_contract", independent_consistent, {"csvExists": independent_csv_exists, "plottedRows": len(independent_rows)}, "independent data are overlaid exactly when present"),
        item("generic_B_growth", all(right > left for left, right in zip(generic_term, generic_term[1:])), generic_term, "generic B ratio grows across M"),
        item("generic_B_crosses_payment", generic_term[-1] > 1.0 and generic_term[0] < 1.0, generic_term, "generic B term crosses the unit payment"),
        item("other_terms_decay", all(right < left for left, right in zip(first_term, first_term[1:])) and all(right < left for left, right in zip(mixed_term, mixed_term[1:])), {"first": first_term, "mixed": mixed_term}, "initial and mixed terms decrease"),
        item("parity_gap_growth", all(right > left for left, right in zip(generic_over_measured, generic_over_measured[1:])), generic_over_measured, "generic-to-measured cubic gap grows"),
        item("measured_BV_decay", all(right < left for left, right in zip(measured_bv, measured_bv[1:])), measured_bv, "measured BV ledger decreases"),
        item("exact_root_finite", all(value > 0.0 and value < 0.01 for value in exact_root), exact_root, "exact-root atoms remain finite and small"),
        item("coupling_envelope_match", envelope_error < 0.0001, envelope_error, "numeric coupling maximization matches the analytic envelope"),
        item("coupling_envelope_decay", all(right < left for left, right in zip(numeric_envelope, numeric_envelope[1:])), [numeric_envelope[0], numeric_envelope[-1]], "optimized coupling envelope decreases"),
        item("result_summary", results["allRequiredSourceChecksPassed"] is True, results["summary"], "result summary records passing sources"),
        item("pdf_geometry", pages == 1 and abs(width_mm - 177.8) < 0.06 and abs(height_mm - 130.0) < 0.06, {"pages": pages, "widthMm": width_mm, "heightMm": height_mm}, "one-page PDF has contracted geometry"),
        item("png_geometry", abs(png.size[0] - expected_width) <= 1 and abs(png.size[1] - expected_height) <= 1 and min(dpi) >= 599.0, {"pixels": png.size, "expected": [expected_width, expected_height], "dpi": dpi}, "PNG is 600 dpi at contracted size"),
        item("svg_vector", "<svg" in svg and "<path" in svg and "image/png" not in svg, {"bytes": len(svg.encode("utf-8"))}, "SVG is vector without embedded PNG"),
        item("qa_surfaces", qa_final.size == qa_gray.size == qa_pdf.size and min(qa_final.size) > 500, {"final": qa_final.size, "gray": qa_gray.size, "pdf": qa_pdf.size}, "QA surfaces share final aspect ratio"),
        item("grayscale_contrast", gray_std > 20.0, gray_std, "grayscale QA retains contrast"),
        item("caption_boundary", all(term in caption for term in ("not growth", "not an enumeration", "do not prove")), caption[-420:], "caption separates upper bounds, measured ledgers, and general claims"),
        item("claim_boundary", all(term in claim for term in ("triangular", "not a growing physical", "does not prove")), contract["claimBoundary"], "contract states the mathematical boundary"),
        item("local_only_publication", config["publication"]["requirePublicCopiesDuringPackageBuild"] is False, config["publication"], "package build requires no writes outside its directory"),
    ]
    report = {
        "schemaVersion": "r072i-figure-validation-v1",
        "allPassed": all(row["passed"] for row in checks),
        "passedCount": sum(row["passed"] for row in checks),
        "requiredCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# R0.72I figure QA report",
        "",
        f"- Result: {'PASS' if report['allPassed'] else 'FAIL'}",
        f"- Checks: {report['passedCount']}/{report['requiredCount']}",
        f"- PDF geometry: {width_mm:.3f} x {height_mm:.3f} mm",
        f"- PNG: {png.size[0]} x {png.size[1]} px at {dpi[0]:.1f} dpi",
        f"- Grayscale standard deviation: {gray_std:.3f}",
        f"- Generic B ratio at M={expected_m[-1]}: {generic_term[-1]:.6g}",
        f"- Generic/measured cubic ratio at M={expected_m[-1]}: {generic_over_measured[-1]:.6g}",
        f"- Independent overlay: {metadata['independentOverlay']}",
        "",
        "The QA verifies package integrity and legibility. It does not turn the generic upper-bound loss into a physical counterexample.",
    ]
    (ROOT / "qa-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["allPassed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
