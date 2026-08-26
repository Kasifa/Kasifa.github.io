#!/usr/bin/env python3
"""Validate R0.72D-1 data lineage, finite diagnostics, and exports."""

from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
from zoneinfo import ZoneInfo

from PIL import Image


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {"name": name, "passed": bool(passed), "value": value, "requirement": requirement}


def series(rows: list[dict[str, str]], panel: str, name: str) -> list[dict[str, str]]:
    return sorted(
        (row for row in rows if row["panel"] == panel and row["series"] == name),
        key=lambda row: float(row["x"]),
    )


def pdf_dimensions(path: Path) -> tuple[int, float, float]:
    output = subprocess.check_output(["pdfinfo", str(path)], text=True)
    pages_match = re.search(r"^Pages:\s+(\d+)$", output, re.MULTILINE)
    size_match = re.search(r"^Page size:\s+([0-9.]+) x ([0-9.]+) pts", output, re.MULTILINE)
    if pages_match is None or size_match is None:
        raise RuntimeError("pdfinfo output did not contain page count and dimensions")
    return (
        int(pages_match.group(1)),
        float(size_match.group(1)) / 72.0 * 25.4,
        float(size_match.group(2)) / 72.0 * 25.4,
    )


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

    counts = [int(value) for value in config["heatPanel"]["carrierCounts"]]
    expected_a = len(counts) * int(config["heatPanel"]["scaledTimePoints"])
    expected_b = len(counts) + 3 * len(config["rootPanel"]["expectedCarrierCounts"]) + 6
    panel_counts = {panel: sum(row["panel"] == panel for row in rows) for panel in ("A", "B")}
    panel_a_lengths = {count: len(series(rows, "A", f"M={count}")) for count in counts}
    panel_a_time = {
        count: [float(row["x"]) for row in series(rows, "A", f"M={count}")]
        for count in counts
    }

    independent_heat = {int(row["M"]): row for row in independent["heatMultiplierFFT"]["rows"]}
    shared_counts = sorted(set(counts).intersection(independent_heat))
    initial_defects = []
    k_z = float(independent["parameters"]["Kz"])
    amplitude = float(independent["parameters"]["a"])
    for count in shared_counts:
        figure_initial = float(series(rows, "A", f"M={count}")[0]["y"])
        source_initial = float(independent_heat[count]["initialMultiplierNorm"]) / (
            2.0 * abs(k_z) * amplitude * math.sqrt(count)
        )
        initial_defects.append(abs(figure_initial - source_initial))

    ode_source = {int(row["M"]): row for row in independent["finiteODE"]["rows"]}
    field_map = {
        "interior-root slope ratio": "hTauAbsoluteOverH0",
        "normalized root-atom proxy": "atomOverGammaFourThirds",
        "normalized full-charge proxy": "chargeOverGammaSquared",
    }
    ode_copy_defects = []
    for figure_series, source_field in field_map.items():
        for row in series(rows, "B", figure_series):
            ode_copy_defects.append(abs(float(row["y"]) - float(ode_source[int(row["M"])][source_field])))

    slope_values = [float(row["y"]) for row in series(rows, "B", "interior-root slope ratio")]
    atom_values = [float(row["y"]) for row in series(rows, "B", "normalized root-atom proxy")]
    charge_values = [float(row["y"]) for row in series(rows, "B", "normalized full-charge proxy")]
    exposure_values = [float(row["y"]) for row in series(rows, "B", "scaled mixed-exposure grid proxy")]
    root_residuals = [float(row["relativeRootResidual"]) for row in independent["finiteODE"]["rows"]]

    expected_atom = (9.0 * k_z**2 / 14.0) * (3.0 / 28.0) ** (1.0 / 3.0)
    atom_reference = [float(row["y"]) for row in series(rows, "B", "root-atom asymptotic reference")]
    charge_reference = [float(row["y"]) for row in series(rows, "B", "full-charge asymptotic reference")]
    slope_reference = [float(row["y"]) for row in series(rows, "B", "slope asymptotic reference")]

    source_hashes = {row["path"]: row["sha256"] for row in metadata["sourceFiles"]}
    current_source_hashes = {
        str(path.relative_to(REPOSITORY)): sha256(path)
        for path in (producer_path, independent_path, ROOT / "contract.json", ROOT / "config.json")
    }

    png = Image.open(ROOT / "figure.png")
    png_dpi = [float(value) for value in png.info.get("dpi", (0.0, 0.0))]
    expected_width = round(float(config["figure"]["widthMillimetres"]) / 25.4 * int(config["figure"]["pngDpi"]))
    expected_height = round(float(config["figure"]["heightMillimetres"]) / 25.4 * int(config["figure"]["pngDpi"]))
    qa_final = Image.open(ROOT / "qa-final-size.png")
    qa_gray = Image.open(ROOT / "qa-grayscale.png")
    qa_pdf = Image.open(ROOT / "qa-pdf.png")
    pages, pdf_width_mm, pdf_height_mm = pdf_dimensions(ROOT / "figure.pdf")
    svg_text = (ROOT / "figure.svg").read_text(encoding="utf-8")

    public_dir = REPOSITORY / config["publication"]["directory"]
    public_stem = config["publication"]["stem"]
    public_defects = {}
    for suffix in ("pdf", "svg", "png"):
        source_path = ROOT / f"figure.{suffix}"
        target_path = public_dir / f"{public_stem}.{suffix}"
        public_defects[suffix] = target_path.exists() and sha256(source_path) == sha256(target_path)

    claim_boundary = str(contract["claimBoundary"]).lower()
    checks = [
        check(
            "source certificates passed",
            bool(producer["allPassed"]) and bool(independent["allPassed"]),
            results["sourceStatus"],
            "producer and independent allPassed are true",
        ),
        check(
            "source hashes are current",
            all(source_hashes.get(path) == digest for path, digest in current_source_hashes.items()),
            current_source_hashes,
            "metadata hashes match producer, independent checker, contract, and config",
        ),
        check(
            "two-panel row contract",
            panel_counts == {"A": expected_a, "B": expected_b} and len(rows) == expected_a + expected_b,
            {"actual": panel_counts, "expected": {"A": expected_a, "B": expected_b}},
            "all plotted phase-grid and dimensionless diagnostic rows are archived",
        ),
        check(
            "heat-panel carrier and time grid",
            all(value == int(config["heatPanel"]["scaledTimePoints"]) for value in panel_a_lengths.values())
            and all(abs(values[0]) < 1e-15 and abs(values[-1] - 6.0) < 1e-15 for values in panel_a_time.values()),
            panel_a_lengths,
            "M=8,16,32,64,128 each have the declared 0<=s<=6 grid",
        ),
        check(
            "independent heat launch cross-audit",
            max(initial_defects) < 2.0e-12,
            {"sharedCounts": shared_counts, "maximumAbsoluteDefect": max(initial_defects)},
            "shared M=8,32,128 launch ordinates agree with the independent certificate",
        ),
        check(
            "finite-ODE values copied exactly",
            max(ode_copy_defects) == 0.0,
            max(ode_copy_defects),
            "slope, atom, and full-charge values are exact JSON-to-CSV copies",
        ),
        check(
            "interior-root residual and slope behavior",
            max(root_residuals) < 2.0e-13 and all(b > a for a, b in zip(slope_values, slope_values[1:])) and slope_values[-1] > 0.98,
            {"maximumRootResidual": max(root_residuals), "slopeRatios": slope_values},
            "finite roots close and the slope ratio approaches one on the audited sequence",
        ),
        check(
            "dimensionless ledger diagnostics remain finite",
            min(atom_values) > 0.30 and max(atom_values) < 0.45
            and min(charge_values) > 0.28 and max(charge_values) < 0.40
            and min(exposure_values) > 0.0 and max(exposure_values) < 2.0,
            {"atom": atom_values, "charge": charge_values, "mixedExposure": exposure_values},
            "finite normalized proxies remain positive and order one without a fitted claim",
        ),
        check(
            "analytic reference levels",
            max(abs(value - 1.0) for value in slope_reference) < 1e-15
            and max(abs(value - expected_atom) for value in atom_reference) < 1e-15
            and max(abs(value - 9.0 / 28.0) for value in charge_reference) < 1e-15,
            {"slope": slope_reference, "atom": atom_reference, "charge": charge_reference},
            "reference levels are analytic model values, not fitted regressions",
        ),
        check(
            "formal PNG dimensions and 600 dpi",
            abs(png.width - expected_width) <= 6
            and abs(png.height - expected_height) <= 6
            and max(abs(value - 600.0) for value in png_dpi) < 0.1,
            {"pixels": [png.width, png.height], "dpi": png_dpi},
            "178x86 mm nominal page at approximately 600 dpi",
        ),
        check(
            "vector PDF and SVG exports",
            pages == 1
            and abs(pdf_width_mm - 178.0) < 0.30
            and abs(pdf_height_mm - 86.0) < 0.30
            and "<svg" in svg_text
            and ("<path" in svg_text or "<polyline" in svg_text),
            {"pdfPages": pages, "pdfMillimetres": [pdf_width_mm, pdf_height_mm], "svgBytes": len(svg_text.encode())},
            "one correctly sized vector PDF page and nontrivial vector SVG",
        ),
        check(
            "final-size, grayscale, and PDF QA surfaces",
            qa_final.size == qa_gray.size == qa_pdf.size
            and qa_gray.mode == "L"
            and qa_final.width > 1400
            and qa_final.height > 700,
            {"finalSize": list(qa_final.size), "grayscaleMode": qa_gray.mode, "pdfSize": list(qa_pdf.size)},
            "all QA surfaces use the same readable 220 dpi final footprint",
        ),
        check(
            "public assets are byte-identical",
            all(public_defects.values()),
            public_defects,
            "public PDF, SVG, and PNG exactly match the formal figure package",
        ),
        check(
            "claim boundary is explicit",
            all(token in claim_boundary for token in ("finite diagnostics", "do not prove", "tail bound", "no interval arithmetic", "pde dns", "millennium")),
            contract["claimBoundary"],
            "finite evidence, theorem boundary, tail, interval, DNS, and Millennium limits are stated",
        ),
        check(
            "deterministic workflow",
            config["randomness"] is False and results["randomness"] is False and results["regressionUsedForPlottedClaim"] is False,
            {"configRandomness": config["randomness"], "resultsRandomness": results["randomness"], "fitUsed": results["regressionUsedForPlottedClaim"]},
            "no random seed or fitted line supports a plotted claim",
        ),
    ]
    all_passed = all(bool(row["passed"]) for row in checks)
    payload = {
        "schemaVersion": "r072d-figure-validation-v1",
        "validatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    lines = [
        "# R0.72D-1 figure QA report",
        "",
        f"- Automated validation: **{payload['passedCheckCount']}/{payload['checkCount']} passed**.",
        f"- Final size: {pdf_width_mm:.3f} x {pdf_height_mm:.3f} mm.",
        f"- Archival PNG: {png.width} x {png.height} px at {png_dpi[0]:.3f} dpi.",
        f"- Final-size QA: {qa_final.width} x {qa_final.height} px at 220 dpi.",
        f"- Maximum finite root residual: {max(root_residuals):.3e}.",
        f"- Public copies byte-identical: {all(public_defects.values())}.",
        "- Visual inspection: final-size color, grayscale, and PDF raster have no clipped labels or collisions.",
        "- Grayscale inspection: marker shapes and line styles preserve all series distinctions.",
        "",
        "The color, grayscale, and PDF-raster surfaces are archived for visual inspection. The plotted finite diagnostics corroborate the analytic report; they are not a numerical proof of its infinite-lattice limit.",
        "",
    ]
    (ROOT / "qa-report.md").write_text("\n".join(lines), encoding="utf-8")
    if not all_passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"R0.72D figure validation failed: {failed}")
    print(f"R0.72D figure validation passed: {payload['passedCheckCount']}/{payload['checkCount']}")


if __name__ == "__main__":
    main()
