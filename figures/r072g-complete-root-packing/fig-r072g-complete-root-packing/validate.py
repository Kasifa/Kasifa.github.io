#!/usr/bin/env python3
"""Validate the R0.72G formal figure package with 19 required checks."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, value, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def pdf_info(path: Path) -> tuple[int, float, float]:
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    pages = re.search(r"^Pages:\s+(\d+)$", output, re.MULTILINE)
    size = re.search(
        r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", output, re.MULTILINE
    )
    if pages is None or size is None:
        raise RuntimeError("pdfinfo did not expose page count and size")
    return (
        int(pages.group(1)),
        float(size.group(1)) / 72 * 25.4,
        float(size.group(2)) / 72 * 25.4,
    )


def main() -> None:
    config = load(ROOT / "config.json")
    contract = load(ROOT / "contract.json")
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load(producer_path)
    independent = load(independent_path)
    results = load(ROOT / "results.json")
    metadata = load(ROOT / "figure-data-metadata.json")
    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    producer_by_r = {int(row["R"]): row for row in producer["rows"]}
    independent_by_r = {int(row["R"]): row for row in independent["rows"]}
    common = sorted(set(producer_by_r) & set(independent_by_r))
    gaps = [
        abs(
            float(producer_by_r[r]["completeSlopeMass"])
            - float(independent_by_r[r]["completeSlopeMass"])
        )
        / max(
            abs(float(producer_by_r[r]["completeSlopeMass"])),
            abs(float(independent_by_r[r]["completeSlopeMass"])),
        )
        for r in common
    ]
    root_counts_equal = all(
        int(producer_by_r[r]["rootCount"]) == int(independent_by_r[r]["rootCount"])
        for r in common
    )
    source_hashes = {row["path"]: row["sha256"] for row in metadata["sourceFiles"]}
    current_hashes = {
        str(path.relative_to(REPOSITORY)): digest(path)
        for path in (
            producer_path,
            independent_path,
            ROOT / "contract.json",
            ROOT / "config.json",
        )
    }
    data_panels = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABC"}
    pages, pdf_width, pdf_height = pdf_info(ROOT / "figure.pdf")
    png = Image.open(ROOT / "figure.png")
    dpi = tuple(float(value) for value in png.info.get("dpi", (0, 0)))
    expected_width = round(config["figure"]["widthMillimetres"] / 25.4 * config["figure"]["pngDpi"])
    expected_height = round(config["figure"]["heightMillimetres"] / 25.4 * config["figure"]["pngDpi"])
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
    producer_checks = {row["name"]: row for row in producer["checks"]}
    independent_checks = {row["name"]: row for row in independent["checks"]}
    expected_rows = 3 * len(producer["rows"]) + len(independent["rows"]) + len(producer["rows"]) + len(producer["rows"])
    expected_rows += int(results["summary"]["positiveDyadicPacketCount"])
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    claim_boundary = contract["claimBoundary"].lower()

    checks = [
        check("producer_passed", producer.get("allRequiredChecksPassed") is True, producer.get("allRequiredChecksPassed"), "producer certificate passes"),
        check("independent_passed", independent.get("allRequiredChecksPassed") is True, independent.get("allRequiredChecksPassed"), "independent certificate passes"),
        check("producer_grid", list(producer_by_r) == config["expected"]["producerR"], list(producer_by_r), "producer R grid matches contract"),
        check("independent_grid", list(independent_by_r) == config["expected"]["independentR"], list(independent_by_r), "independent R grid matches contract"),
        check("common_root_counts", root_counts_equal, {r: [producer_by_r[r]["rootCount"], independent_by_r[r]["rootCount"]] for r in common}, "common root counts agree exactly"),
        check("cross_solver_mass", max(gaps) <= config["expected"]["maximumCommonRelativeMassGap"], max(gaps), "common mass gap <= 2e-6"),
        check("producer_pressure", producer_checks["step_pressure"]["passed"] and producer_checks["radius_pressure"]["passed"] and producer_checks["horizon_mass_tail"]["passed"], {key: producer_checks[key]["value"] for key in ("step_pressure", "radius_pressure", "horizon_mass_tail")}, "producer step, largest-radius, and horizon pressure pass"),
        check("independent_pressure", independent_checks["step_pressure"]["passed"] and independent_checks["radius_pressure"]["passed"] and independent_checks["horizon_mass_tail"]["passed"], {key: independent_checks[key]["value"] for key in ("step_pressure", "radius_pressure", "horizon_mass_tail")}, "independent step, radius, and horizon pressure pass"),
        check("diagnostic_log_slope", abs(float(producer["logFit"]["slopeAgainstLogDelta"]) - 4 / math.pi**2) / (4 / math.pi**2) < 0.02, producer["logFit"], "finite producer log slope is within 2 percent of diagnostic guide"),
        check("selected_contained", all(float(row["completeSlopeMass"]) >= float(row["selectedSlopeMass"]) > 0 for row in producer["rows"]), min(float(row["selectedToCompleteMassRatio"]) for row in producer["rows"]), "complete mass contains selected mass"),
        check("data_row_count", len(rows) == expected_rows and all(data_panels[panel] > 0 for panel in "ABC"), {"actual": len(rows), "expected": expected_rows, "panels": data_panels}, "data.csv has every contracted row and panel"),
        check("data_lineage", source_hashes == current_hashes, {"recorded": source_hashes, "current": current_hashes}, "source hashes match certificates and contract"),
        check("pdf_geometry", pages == 1 and abs(pdf_width - 177.8) < 0.05 and abs(pdf_height - 97.79) < 0.05, {"pages": pages, "widthMm": pdf_width, "heightMm": pdf_height}, "one-page 177.8 x 97.79 mm PDF"),
        check("png_geometry", png.size == (expected_width, expected_height) and min(dpi) >= 599.0, {"pixels": png.size, "dpi": dpi}, "600 dpi PNG at contracted size"),
        check("svg_vector", "<svg" in svg and "<path" in svg and "image/png" not in svg, {"bytes": len(svg)}, "SVG contains vector paths and no embedded PNG"),
        check("public_copies", all(public_equal.values()), public_equal, "public copies are byte-identical"),
        check("qa_surfaces", qa_final.size == qa_gray.size == qa_pdf.size and min(qa_final.size) > 500, {"final": qa_final.size, "gray": qa_gray.size, "pdf": qa_pdf.size}, "final-size, grayscale, and PDF QA surfaces match"),
        check("grayscale_legibility", gray_std > 20.0, gray_std, "grayscale surface retains contrast"),
        check("claim_boundary", all(term in claim_boundary for term in ("one-carrier", "binary64", "does not prove", "regularity")) and results["allRequiredSourceChecksPassed"] is True, contract["claimBoundary"], "contract separates theorem, diagnostics, and NSE boundary"),
    ]
    report = {
        "schemaVersion": "r072g-figure-validation-v1",
        "allPassed": all(row["passed"] for row in checks),
        "passedCount": sum(row["passed"] for row in checks),
        "requiredCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["allPassed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
