#!/usr/bin/env python3
"""Validate R0.72F-1 lineage, finite diagnostics, and exports."""

from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from typing import Any
from zoneinfo import ZoneInfo

from PIL import Image, ImageStat


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(
    name: str, passed: bool, value: object, requirement: str
) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def series(
    rows: list[dict[str, str]], panel: str, name: str
) -> list[dict[str, str]]:
    return sorted(
        (item for item in rows if item["panel"] == panel and item["series"] == name),
        key=lambda item: float(item["x"]),
    )


def pdf_dimensions(path: Path) -> tuple[int, float, float]:
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    pages_match = re.search(r"^Pages:\s+(\d+)$", output, re.MULTILINE)
    size_match = re.search(
        r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", output, re.MULTILINE
    )
    if pages_match is None or size_match is None:
        raise RuntimeError("pdfinfo output did not contain page count and dimensions")
    return (
        int(pages_match.group(1)),
        float(size_match.group(1)) / 72.0 * 25.4,
        float(size_match.group(2)) / 72.0 * 25.4,
    )


def maximum(values: list[float]) -> float:
    if not values:
        raise RuntimeError("empty comparison")
    return max(values)


def main() -> None:
    config = load_json(ROOT / "config.json")
    contract = load_json(ROOT / "contract.json")
    results = load_json(ROOT / "results.json")
    metadata = load_json(ROOT / "figure-data-metadata.json")
    producer_path = REPOSITORY / config["sourceCertificates"]["producer"]
    independent_path = REPOSITORY / config["sourceCertificates"]["independent"]
    producer = load_json(producer_path)
    independent = load_json(independent_path)
    with (ROOT / "data.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    expected_deltas = [int(value) for value in config["expected"]["deltas"]]
    expected_counts = {"A": 10, "B": 18, "C": 3}
    panel_counts = {
        panel: sum(item["panel"] == panel for item in rows)
        for panel in ("A", "B", "C")
    }
    producer_source = {
        int(item["delta"]): item for item in producer["weightedActionRows"]
    }
    independent_source = {
        int(item["delta"]): item for item in independent["weightedActionRows"]
    }

    copy_defects: list[float] = []
    for item in series(rows, "B", "producer critical-log normalization"):
        delta = int(float(item["x"]))
        source = producer_source[delta]
        raw = float(source["actions"]["critical-log"])
        normalized = raw * delta ** (2.0 / 3.0) / math.log(delta)
        copy_defects.extend(
            (abs(float(item["rawValue"]) - raw), abs(float(item["y"]) - normalized))
        )
    for item in series(rows, "B", "independent critical-log normalization"):
        delta = int(float(item["x"]))
        source = independent_source[delta]
        raw = float(source["actions"]["critical-log"])
        normalized = raw * delta ** (2.0 / 3.0) / math.log(delta)
        copy_defects.extend(
            (abs(float(item["rawValue"]) - raw), abs(float(item["y"]) - normalized))
        )
    for item in series(rows, "B", "producer plain-to-critical annotation"):
        delta = int(float(item["x"]))
        source = producer_source[delta]
        plain = float(source["actions"]["plain-one-third"])
        ratio = plain / float(source["actions"]["critical-log"])
        copy_defects.extend(
            (abs(float(item["rawValue"]) - plain), abs(float(item["y"]) - ratio))
        )

    metadata_hashes = {item["path"]: item["sha256"] for item in metadata["sourceFiles"]}
    source_paths = (
        producer_path,
        independent_path,
        ROOT / "contract.json",
        ROOT / "config.json",
    )
    current_hashes = {
        str(path.relative_to(REPOSITORY)): sha256(path) for path in source_paths
    }
    producer_grid = [
        int(float(item["x"]))
        for item in series(rows, "B", "producer critical-log normalization")
    ]
    independent_grid = [
        int(float(item["x"]))
        for item in series(rows, "B", "independent critical-log normalization")
    ]
    plain_grid = [
        int(float(item["x"]))
        for item in series(rows, "B", "producer plain-to-critical annotation")
    ]

    producer_values = [
        float(item["y"])
        for item in series(rows, "B", "producer critical-log normalization")
    ]
    independent_values = [
        float(item["y"])
        for item in series(rows, "B", "independent critical-log normalization")
    ]
    plain_ratios = [
        float(item["y"])
        for item in series(rows, "B", "producer plain-to-critical annotation")
    ]
    relative_gaps = [
        abs(left - right) / max(abs(left), abs(right))
        for left, right in zip(producer_values, independent_values, strict=True)
    ]
    producer_refinement = max(
        float(item["fineCoarseRelativeDifferences"]["critical-log"])
        for item in producer["weightedActionRows"]
    )
    independent_quadrature = max(
        float(item["quadratureRelativeDefects"]["critical-log"])
        for item in independent["weightedActionRows"]
    )
    producer_l2 = next(
        item["value"]
        for item in producer["checks"]
        if item["name"] == "critical_weight_l2_identity"
    )

    vertices = producer["frontier"]["vertices"]
    vertex_map = {item["name"]: item for item in vertices}
    root_row = next(item for item in rows if item["series"] == "root-weight")
    frontier_exact = (
        len(vertices) == 3
        and all(item["onDeclaredBoundary"] for item in vertices)
        and vertex_map["critical-log-action"]["beta"] == "1/3"
        and vertex_map["critical-log-action"]["gamma"] == 1
        and vertex_map["explicit-coupling"]["c"] == "1/3"
        and vertex_map["root-weight"]["alpha"] == "4/9"
        and "changes LHS" in root_row["note"]
    )

    png = Image.open(ROOT / "figure.png")
    png_dpi = [float(value) for value in png.info.get("dpi", (0.0, 0.0))]
    expected_width = round(
        float(config["figure"]["widthMillimetres"])
        / 25.4
        * int(config["figure"]["pngDpi"])
    )
    expected_height = round(
        float(config["figure"]["heightMillimetres"])
        / 25.4
        * int(config["figure"]["pngDpi"])
    )
    qa_final = Image.open(ROOT / "qa-final-size.png")
    qa_gray = Image.open(ROOT / "qa-grayscale.png")
    qa_pdf = Image.open(ROOT / "qa-pdf.png")
    grayscale_stddev = float(ImageStat.Stat(qa_gray).stddev[0])
    pages, pdf_width_mm, pdf_height_mm = pdf_dimensions(ROOT / "figure.pdf")
    svg_text = (ROOT / "figure.svg").read_text(encoding="utf-8")

    public_dir = REPOSITORY / config["publication"]["directory"]
    public_stem = config["publication"]["stem"]
    public_matches = {
        suffix: (
            (public_dir / f"{public_stem}.{suffix}").exists()
            and sha256(ROOT / f"figure.{suffix}")
            == sha256(public_dir / f"{public_stem}.{suffix}")
        )
        for suffix in ("pdf", "svg", "png")
    }

    boundary = str(contract["claimBoundary"]).lower()
    cjk_in_svg = bool(re.search(r"[\u3400-\u9fff]", svg_text))
    checks = [
        check(
            "source certificates passed and independent",
            bool(
                producer["allRequiredChecksPassed"]
                and independent["allRequiredChecksPassed"]
                and not independent["scope"]["importsProducer"]
                and not independent["scope"]["readsProducerOutput"]
            ),
            results["sourceStatus"],
            "both certificates passed and the independent audit imports no producer output",
        ),
        check(
            "source hashes are current",
            all(metadata_hashes.get(path) == digest for path, digest in current_hashes.items()),
            current_hashes,
            "metadata hashes match both certificates, contract, and config",
        ),
        check(
            "three-panel row contract",
            panel_counts == expected_counts and len(rows) == 31,
            {"actual": panel_counts, "expected": expected_counts, "rows": len(rows)},
            "all analytic, numerical, and frontier rows are archived",
        ),
        check(
            "shared dyadic grids",
            producer_grid == independent_grid == plain_grid == expected_deltas,
            {
                "producer": producer_grid,
                "independent": independent_grid,
                "plainAnnotation": plain_grid,
            },
            "both solvers and the plain-endpoint annotation use delta=16,...,512",
        ),
        check(
            "certificate values copied exactly",
            maximum(copy_defects) == 0.0,
            maximum(copy_defects),
            "raw Q values and derived normalizations reproduce their source rows exactly",
        ),
        check(
            "critical normalization bounded",
            min(producer_values) > 0.0
            and min(independent_values) > 0.0
            and max(producer_values) / min(producer_values) < 1.10
            and max(independent_values) / min(independent_values) < 1.10,
            {
                "producer": producer_values,
                "independent": independent_values,
                "producerSpread": max(producer_values) / min(producer_values),
                "independentSpread": max(independent_values) / min(independent_values),
            },
            "Q_* delta^(2/3)/log(delta) remains within a 1.10 finite spread",
        ),
        check(
            "producer-independent agreement",
            maximum(relative_gaps) < 5.0e-4
            and abs(
                maximum(relative_gaps)
                - float(results["panels"]["B"]["maximumRelativeCrossAuditGap"])
            )
            < 1.0e-16,
            maximum(relative_gaps),
            "the two finite routes agree to less than 5e-4 relatively",
        ),
        check(
            "discretization diagnostics",
            producer_refinement < 1.5e-3 and independent_quadrature < 1.0e-8,
            {
                "producerFineCoarse": producer_refinement,
                "independentQuadrature": independent_quadrature,
            },
            "producer refinement and independent quadrature defects stay below declared limits",
        ),
        check(
            "plain endpoint contrast",
            all(later < earlier for earlier, later in zip(plain_ratios[:-1], plain_ratios[1:], strict=True))
            and 0.20 < plain_ratios[0] < 0.22
            and 0.13 < plain_ratios[-1] < 0.15,
            plain_ratios,
            "Q_(1/3,0)/Q_* decreases across the shared finite grid",
        ),
        check(
            "critical weight L2 identity",
            float(producer_l2) == 75.0
            and float(independent["criticalWeightL2"]["value"]) == 75.0
            and float(independent["criticalWeightL2"]["exactTarget"]) == 75.0,
            {
                "producer": producer_l2,
                "independent": independent["criticalWeightL2"],
            },
            "both routes record the exact critical-weight L2 square 75",
        ),
        check(
            "two-screen analytic window",
            results["panels"]["A"]["admissibleInterior"]
            == "1/3 < beta < 1/2, gamma >= 0"
            and results["panels"]["A"]["includedEndpointRay"]
            == "beta=1/3, gamma>=1"
            and results["panels"]["A"]["excludedEnergyBoundary"]
            == "beta=1/2 for gamma>=0",
            results["panels"]["A"],
            "the plot distinguishes the open interior, included log endpoint, and excluded energy boundary",
        ),
        check(
            "frontier vertices exact and distinct",
            frontier_exact and results["panels"]["C"]["rootAtomChangesLHS"] is True,
            vertices,
            "the three rational vertices are exact and the root-atom vertex changes the LHS",
        ),
        check(
            "formal PNG dimensions and 600 dpi",
            abs(png.width - expected_width) <= 6
            and abs(png.height - expected_height) <= 6
            and max(abs(value - 600.0) for value in png_dpi) < 0.1,
            {"pixels": [png.width, png.height], "dpi": png_dpi},
            "178x94 mm nominal page at approximately 600 dpi",
        ),
        check(
            "vector PDF and SVG exports",
            pages == 1
            and abs(pdf_width_mm - 178.0) < 0.30
            and abs(pdf_height_mm - 94.0) < 0.30
            and "<svg" in svg_text
            and ("<path" in svg_text or "<polyline" in svg_text)
            and "CHANGES LHS" in svg_text,
            {
                "pdfPages": pages,
                "pdfMillimetres": [pdf_width_mm, pdf_height_mm],
                "svgBytes": len(svg_text.encode()),
            },
            "one correctly sized vector PDF page and nontrivial labelled SVG",
        ),
        check(
            "final-size, grayscale, and PDF QA surfaces",
            qa_final.size == qa_gray.size == qa_pdf.size
            and qa_gray.mode == "L"
            and qa_final.width > 1500
            and qa_final.height > 790
            and grayscale_stddev > 20.0,
            {
                "finalSize": list(qa_final.size),
                "grayscaleMode": qa_gray.mode,
                "pdfSize": list(qa_pdf.size),
                "grayscaleStddev": grayscale_stddev,
            },
            "all QA surfaces share a readable 220 dpi final footprint with nontrivial contrast",
        ),
        check(
            "public assets are byte-identical",
            all(public_matches.values()),
            public_matches,
            "public PDF, SVG, and PNG exactly match the formal package",
        ),
        check(
            "claim boundary is explicit",
            all(
                token in boundary
                for token in (
                    "selected-root",
                    "finite binary64",
                    "do not prove",
                    "complete-root",
                    "restart",
                    "r_y",
                    "regularity",
                    "millennium",
                    "changes the left-hand-side",
                )
            ),
            contract["claimBoundary"],
            "selected/complete-root, analytic, and Millennium boundaries are stated",
        ),
        check(
            "English-only visible figure text",
            not cjk_in_svg,
            {"cjkInSvg": cjk_in_svg},
            "the formal SVG contains no CJK figure text",
        ),
        check(
            "deterministic workflow",
            config["randomness"] is False
            and results["randomness"] is False
            and results["regressionUsedForPlottedClaim"] is False
            and results["finiteFitsAreDiagnostics"] is True,
            {
                "configRandomness": config["randomness"],
                "resultsRandomness": results["randomness"],
                "fitUsedForClaim": results["regressionUsedForPlottedClaim"],
                "finiteFitsAreDiagnostics": results["finiteFitsAreDiagnostics"],
            },
            "no random seed or fitted line supplies a plotted theorem claim",
        ),
    ]

    all_passed = all(bool(item["passed"]) for item in checks)
    validation_path = ROOT / "validation.json"
    previous: dict[str, Any] = {}
    if validation_path.exists():
        try:
            previous = load_json(validation_path)
        except (json.JSONDecodeError, OSError):
            previous = {}
    validated_at = (
        previous.get("validatedAt")
        if previous.get("checks") == checks and previous.get("allPassed") == all_passed
        else datetime.now(TIMEZONE).isoformat(timespec="seconds")
    )
    payload = {
        "schemaVersion": "r072f-figure-validation-v1",
        "validatedAt": validated_at,
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(item["passed"]) for item in checks),
        "checks": checks,
    }
    validation_path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    lines = [
        "# R0.72F-1 figure QA report",
        "",
        f"- Automated validation: **{payload['passedCheckCount']}/{payload['checkCount']} passed**.",
        f"- Final size: {pdf_width_mm:.3f} x {pdf_height_mm:.3f} mm.",
        f"- Archival PNG: {png.width} x {png.height} px at {png_dpi[0]:.3f} dpi.",
        f"- Final-size QA: {qa_final.width} x {qa_final.height} px at 220 dpi.",
        f"- Maximum source-copy defect: {maximum(copy_defects):.3e}.",
        f"- Maximum producer/independent critical-normalization gap: {maximum(relative_gaps):.3e} relative.",
        f"- Critical-normalization finite spreads: {max(producer_values)/min(producer_values):.6f} (producer), {max(independent_values)/min(independent_values):.6f} (independent).",
        f"- Plain-to-critical ratio: {plain_ratios[0]:.6f} to {plain_ratios[-1]:.6f}.",
        "- Root-atom vertex is explicitly labelled as changing the LHS.",
        f"- Public copies byte-identical: {all(public_matches.values())}.",
        "- Visual inspection surface: final-size color, grayscale, and PDF raster.",
        "- Grayscale encoding: hatch, line style, marker fill, and marker shape preserve distinctions.",
        "",
        "The archived surfaces are finite numerical diagnostics plus exact analytic schematics. They do not provide complete-root or Navier-Stokes regularity control.",
        "",
    ]
    (ROOT / "qa-report.md").write_text("\n".join(lines), encoding="utf-8")
    if not all_passed:
        failed = [item["name"] for item in checks if not item["passed"]]
        raise AssertionError(f"R0.72F figure validation failed: {failed}")
    print(
        f"R0.72F figure validation passed: {payload['passedCheckCount']}/{payload['checkCount']}"
    )


if __name__ == "__main__":
    main()
