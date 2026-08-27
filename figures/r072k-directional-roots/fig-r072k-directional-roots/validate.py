#!/usr/bin/env python3
"""Validate the R0.72K formal figure package and public masters."""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def item(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def common_cases(payload: dict[str, Any]) -> dict[int, dict[str, Any]]:
    for key in ("commonBandCases", "cases"):
        rows = payload.get(key)
        if isinstance(rows, list) and rows and "R" in rows[0]:
            return {int(row["R"]): row for row in rows}
    ledger_rows = payload.get("ledgerCases")
    if isinstance(ledger_rows, list) and ledger_rows:
        return {
            int(row["R"]): {
                "R": int(row["R"]),
                "N": int(row["N"]),
                "exactRootAtom": float(row["exactRootLower"]),
                "directionalMeasuredUpper": float(
                    row["measuredCompleteLedgerUpper"]
                ),
                "directionalTheoremProxy": float(
                    row["analyticCompleteLedgerProxy"]
                ),
                "normalizedMeasuredCompleteUpper": float(
                    row["normalizedMeasuredCompleteUpper"]
                ),
                "normalizedTheoremCompleteProxy": float(
                    row["normalizedAnalyticCompleteProxy"]
                ),
                "exactRootResidual": float(row["exactRootResidual"]),
            }
            for row in ledger_rows
        }
    raise KeyError("certificate does not expose common-band cases")


def checks_pass(payload: dict[str, Any]) -> bool:
    checks = payload.get("checks")
    return (
        isinstance(checks, dict)
        and bool(checks)
        and all(value is True for value in checks.values())
    )


def optional_checks_pass(payload: dict[str, Any]) -> bool:
    checks = payload.get("checks")
    return checks is None or (
        isinstance(checks, dict)
        and bool(checks)
        and all(value is True for value in checks.values())
    )


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def resolve_repository_path(relative: str) -> Path:
    path = (REPOSITORY / relative).resolve()
    repository = REPOSITORY.resolve()
    if path != repository and repository not in path.parents:
        raise ValueError(f"source path escapes repository: {relative}")
    return path


def main() -> None:
    config = load(ROOT / "config.json")
    contract = load(ROOT / "contract.json")
    results = load(ROOT / "results.json")
    source_config = config["sourceCertificates"]
    producer_path = resolve_repository_path(source_config["producerResult"])
    independent_path = resolve_repository_path(source_config["independentResult"])
    crosscheck_path = resolve_repository_path(source_config["crosscheck"])
    producer = load(producer_path)
    independent = load(independent_path)
    crosscheck = load(crosscheck_path)

    rows = list(csv.DictReader((ROOT / "data.csv").open(encoding="utf-8")))
    panels = {
        panel: [row for row in rows if row["panel"] == panel]
        for panel in "ABCD"
    }
    panel_counts = {panel: len(panel_rows) for panel, panel_rows in panels.items()}
    expected_r = [int(value) for value in config["expected"]["rValues"]]
    producer_cases = common_cases(producer)
    independent_cases = common_cases(independent)

    measured_errors = [
        relative_error(
            float(producer_cases[R]["normalizedMeasuredCompleteUpper"]),
            float(independent_cases[R]["normalizedMeasuredCompleteUpper"]),
        )
        for R in expected_r
    ]
    proxy_errors = [
        relative_error(
            float(producer_cases[R]["normalizedTheoremCompleteProxy"]),
            float(independent_cases[R]["normalizedTheoremCompleteProxy"]),
        )
        for R in expected_r
    ]

    recorded_sources = results.get("sourceSha256", {})
    current_sources = {
        relative: digest(resolve_repository_path(relative))
        for relative in recorded_sources
    }
    recorded_outputs = results.get("outputSha256", {})
    current_outputs = {
        name: digest(ROOT / name)
        for name in recorded_outputs
    }

    sharpness = producer.get("sharpnessCases", [])
    sharpness_ratios = [float(row["theoremRatio"]) for row in sharpness]
    exact_sharpness = [
        1.0
        / (
            1.0
            + (
                float(row["epsilonNumerator"])
                / float(row["epsilonDenominator"])
            )
            ** 2
        )
        for row in sharpness
    ]

    pdf_reader = PdfReader(str(ROOT / "figure.pdf"))
    if len(pdf_reader.pages) != 1:
        width_mm = height_mm = float("nan")
    else:
        media_box = pdf_reader.pages[0].mediabox
        width_mm = float(media_box.width) / 72.0 * 25.4
        height_mm = float(media_box.height) / 72.0 * 25.4

    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_dpi = tuple(float(value) for value in image.info.get("dpi", (0, 0)))
    with Image.open(ROOT / "qa-final-size.png") as image:
        qa_final_size = image.size
    with Image.open(ROOT / "qa-grayscale.png") as image:
        qa_gray_size = image.size
        gray_std = float(ImageStat.Stat(image.convert("L")).stddev[0])
    with Image.open(ROOT / "qa-pdf.png") as image:
        qa_pdf_size = image.size
        pdf_std = float(ImageStat.Stat(image.convert("L")).stddev[0])

    expected_png = (
        round(
            float(config["figure"]["widthMillimetres"])
            / 25.4
            * int(config["figure"]["pngDpi"])
        ),
        round(
            float(config["figure"]["heightMillimetres"])
            / 25.4
            * int(config["figure"]["pngDpi"])
        ),
    )
    expected_qa = (
        round(
            float(config["figure"]["widthMillimetres"])
            / 25.4
            * int(config["figure"]["qaDpi"])
        ),
        round(
            float(config["figure"]["heightMillimetres"])
            / 25.4
            * int(config["figure"]["qaDpi"])
        ),
    )

    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    caption = (ROOT / "caption.md").read_text(encoding="utf-8").lower()
    boundary = contract["claimBoundary"].lower()
    public_dir = resolve_repository_path(config["publication"]["directory"])
    stem = config["publication"]["stem"]
    public_matches = {
        suffix: (public_dir / f"{stem}.{suffix}").is_file()
        and digest(ROOT / f"figure.{suffix}")
        == digest(public_dir / f"{stem}.{suffix}")
        for suffix in ("pdf", "svg", "png")
    }

    expected_panel_counts = {"A": 243, "B": 7, "C": 30, "D": 100}
    c_series = {row["series"] for row in panels["C"]}
    d_series = {row["series"] for row in panels["D"]}
    producer_measured = [
        float(producer_cases[R]["normalizedMeasuredCompleteUpper"])
        for R in expected_r
    ]
    producer_proxy = [
        float(producer_cases[R]["normalizedTheoremCompleteProxy"])
        for R in expected_r
    ]
    root_ordering = {
        route: all(
            float(cases[R]["exactRootAtom"])
            <= float(cases[R]["directionalMeasuredUpper"])
            <= float(cases[R]["directionalTheoremProxy"])
            for R in expected_r
        )
        for route, cases in (
            ("producer", producer_cases),
            ("independent", independent_cases),
        )
    }
    maximum_root_residual = max(
        max(float(producer_cases[R]["exactRootResidual"]) for R in expected_r),
        max(float(independent_cases[R]["exactRootResidual"]) for R in expected_r),
    )
    slope = float(producer["slopes"]["normalizedMeasuredCompleteUpperAll"])
    slope_range = [
        float(value)
        for value in config["expected"]["producerNormalizedSlopeRange"]
    ]

    checks = [
        item("producer_passed", producer.get("status") == "passed", producer.get("status"), "producer certificate passes"),
        item("independent_passed", independent.get("status") == "passed", independent.get("status"), "independent certificate passes"),
        item("crosscheck_passed", crosscheck.get("status") == "passed", crosscheck.get("status"), "cross-route certificate passes"),
        item("producer_checks", checks_pass(producer), producer.get("checks"), "all producer checks are true"),
        item("independent_checks", checks_pass(independent), independent.get("checks"), "all independent checks are true"),
        item("crosscheck_checks", optional_checks_pass(crosscheck), crosscheck.get("checks"), "all declared cross-route checks are true"),
        item("certificate_grids", sorted(producer_cases) == expected_r and sorted(independent_cases) == expected_r, {"producer": sorted(producer_cases), "independent": sorted(independent_cases)}, "both certificate grids match config"),
        item("no_new_pde_evolution", producer.get("config", {}).get("newPdeEvolution") is False and independent.get("config", {}).get("newPdeEvolution") is False, {"producer": producer.get("config", {}).get("newPdeEvolution"), "independent": independent.get("config", {}).get("newPdeEvolution")}, "both finite routes reuse sealed R0.72J evolutions"),
        item("source_lineage", current_sources == recorded_sources and len(recorded_sources) == 8, {"current": current_sources, "recorded": recorded_sources}, "all eight source hashes match the figure build"),
        item("output_lineage", current_outputs == recorded_outputs and set(recorded_outputs) == {"figure.pdf", "figure.svg", "figure.png", "data.csv"}, {"current": current_outputs, "recorded": recorded_outputs}, "master and data hashes match results.json"),
        item("data_rows", len(rows) == results["summary"]["rowCount"] == sum(expected_panel_counts.values()), {"actual": len(rows), "summary": results["summary"]["rowCount"]}, "data row count is complete"),
        item("panel_coverage", panel_counts == expected_panel_counts, panel_counts, "all contracted panel counts match"),
        item("panel_a_projection", sum(row["series"] == "complex trajectory" for row in panels["A"]) == 241 and sum(row["series"] == "directional projection zero" for row in panels["A"]) == 2, {row["series"]: sum(candidate["series"] == row["series"] for candidate in panels["A"]) for row in panels["A"]}, "analytic trajectory and two projection zeros are present"),
        item("sharpness_count", len(sharpness) == int(config["expected"]["sharpnessCaseCount"]), len(sharpness), "seven exact sharpness cases are present"),
        item("sharpness_formula", all(math.isclose(left, right, rel_tol=1.0e-14, abs_tol=1.0e-14) for left, right in zip(sharpness_ratios, exact_sharpness, strict=True)), sharpness_ratios, "factor-two ratios equal 1/(1+epsilon^2)"),
        item("sharpness_limit", all(right > left for left, right in zip(sharpness_ratios, sharpness_ratios[1:])) and sharpness_ratios[-1] > 0.9999, sharpness_ratios, "sharpness ratios increase to the factor-two boundary"),
        item("panel_c_series", c_series == {"exact root atom / N^2", "measured upper / N^2", "theorem proxy / N^2"}, sorted(c_series), "raw-ledger series are complete"),
        item("panel_d_series", d_series == {"measured complete upper", "theorem complete proxy", "R^-2/3 guide"}, sorted(d_series), "normalized-ledger series and guide are complete"),
        item("root_ledger_ordering", all(root_ordering.values()), root_ordering, "root atom is below measured and theorem upper ledgers"),
        item("root_residual", maximum_root_residual <= 1.0e-10, maximum_root_residual, "all inherited exact-root residuals are below 1e-10"),
        item("measured_cross_route", max(measured_errors) <= float(config["expected"]["maximumMeasuredCrossRelativeError"]), max(measured_errors), "measured producer-independent error meets config"),
        item("proxy_cross_route", max(proxy_errors) <= float(config["expected"]["maximumMeasuredCrossRelativeError"]), max(proxy_errors), "theorem-proxy producer-independent error meets config"),
        item("normalized_decay", all(right < left for left, right in zip(producer_measured, producer_measured[1:])) and all(right < left for left, right in zip(producer_proxy, producer_proxy[1:])), {"measured": producer_measured, "proxy": producer_proxy}, "both producer normalized ledgers decrease"),
        item("producer_slope", slope_range[0] <= slope <= slope_range[1], slope, "producer normalized slope is within its diagnostic range"),
        item("results_boundary", results.get("status") == "built" and results.get("newPdeEvolution") is False, {"status": results.get("status"), "newPdeEvolution": results.get("newPdeEvolution")}, "figure build performs no new PDE evolution"),
        item("pdf_geometry", len(pdf_reader.pages) == 1 and abs(width_mm - float(config["figure"]["widthMillimetres"])) < 0.06 and abs(height_mm - float(config["figure"]["heightMillimetres"])) < 0.06, {"pages": len(pdf_reader.pages), "widthMm": width_mm, "heightMm": height_mm}, "PDF reopens as one page at contracted geometry"),
        item("png_geometry", abs(png_size[0] - expected_png[0]) <= 1 and abs(png_size[1] - expected_png[1]) <= 1 and min(png_dpi) >= 599.0, {"pixels": png_size, "expected": expected_png, "dpi": png_dpi}, "PNG is 600 dpi at contracted geometry"),
        item("svg_vector", "<svg" in svg and "<path" in svg and "image/png" not in svg and "data:image" not in svg, {"bytes": len(svg.encode("utf-8"))}, "SVG is editable vector without embedded raster data"),
        item("svg_titles", all(title in svg for title in ("Complex return with no tangent zero", "Sharpness of the factor two", "Complete raw root ledger", "Physical normalized complete ledger")), "four panel titles", "SVG retains all panel titles as text"),
        item("qa_geometry", qa_final_size == qa_gray_size == qa_pdf_size == expected_qa, {"final": qa_final_size, "gray": qa_gray_size, "pdf": qa_pdf_size, "expected": expected_qa}, "final-size, grayscale, and PDF-raster QA surfaces match"),
        item("qa_contrast", gray_std > 20.0 and pdf_std > 20.0, {"grayscaleStd": gray_std, "pdfRasterStd": pdf_std}, "grayscale and PDF-raster QA retain contrast"),
        item("caption_boundary", all(phrase in caption for phrase in ("factor-two", "not a fitted universal constant", "do not enumerate all roots", "do not enumerate all roots or prove general")), caption[-700:], "caption records sharpness, fit, root-enumeration, and general-claim boundaries"),
        item("contract_boundary", all(phrase in boundary for phrase in ("not an interval proof", "root enumeration", "general navier-stokes regularity")), contract["claimBoundary"], "contract separates analytic theorem, finite evidence, and general regularity"),
        item("public_copies", all(public_matches.values()), public_matches, "public PDF, SVG, and PNG are byte-identical to masters"),
    ]

    report = {
        "schemaVersion": "r072k-figure-validation-v1",
        "status": "passed" if all(row["passed"] for row in checks) else "failed",
        "allPassed": all(row["passed"] for row in checks),
        "passedCount": sum(row["passed"] for row in checks),
        "requiredCount": len(checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    qa_lines = [
        "# R0.72K figure QA report",
        "",
        f"- Result: {'PASS' if report['allPassed'] else 'FAIL'}",
        f"- Checks: {report['passedCount']}/{report['requiredCount']}",
        f"- PDF geometry: {width_mm:.3f} x {height_mm:.3f} mm",
        f"- PNG: {png_size[0]} x {png_size[1]} px at {png_dpi[0]:.1f} dpi",
        f"- QA raster size: {qa_final_size[0]} x {qa_final_size[1]} px",
        f"- Grayscale standard deviation: {gray_std:.3f}",
        f"- PDF-raster standard deviation: {pdf_std:.3f}",
        f"- Maximum measured cross-route relative error: {max(measured_errors):.6g}",
        f"- Maximum theorem-proxy cross-route relative error: {max(proxy_errors):.6g}",
        f"- Public masters byte-identical: {all(public_matches.values())}",
        "",
        "These checks verify finite evidence, lineage, geometry, and QA surfaces. They do not add a mathematical claim or certify visual inspection by a human.",
    ]
    (ROOT / "qa-report.md").write_text(
        "\n".join(qa_lines) + "\n", encoding="utf-8"
    )
    print(json.dumps(report, indent=2, sort_keys=True))
    if not report["allPassed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
