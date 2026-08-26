#!/usr/bin/env python3
"""Validate R0.72C-1 identities, certificate links, and exported assets."""

from __future__ import annotations

import csv
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path
from zoneinfo import ZoneInfo

from PIL import Image
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]
TIMEZONE = ZoneInfo("Asia/Shanghai")


def load_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def sum_of_squares(count: int) -> int:
    return count * (count + 1) * (2 * count + 1) // 6


def coherent_prefactor(count: int) -> float:
    carrier_sum = sum_of_squares(count)
    return (
        2.0 ** (-1.0 / 3.0)
        * count ** (2.0 / 3.0)
        * carrier_sum ** (-4.0 / 3.0)
    )


def rudin_shapiro_prefactor(count: int) -> float:
    return 0.5 * (count / sum_of_squares(count)) ** (4.0 / 3.0)


def relative_defect(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def series_rows(
    rows: list[dict[str, str]], panel: str, series: str
) -> list[dict[str, str]]:
    return sorted(
        [row for row in rows if row["panel"] == panel and row["series"] == series],
        key=lambda row: float(row["x"]),
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

    coherent = series_rows(rows, "A", "coherent exact launch")
    rudin_shapiro = series_rows(rows, "A", "Rudin-Shapiro exact launch")
    coherent_reference = series_rows(
        rows, "A", "coherent asymptotic reference"
    )
    rudin_shapiro_reference = series_rows(
        rows, "A", "Rudin-Shapiro asymptotic reference"
    )
    coherent_boundary = series_rows(rows, "B", "coherent exact launch")
    arbitrary_boundary = series_rows(rows, "B", "arbitrary-phase exact launch")
    fixed_boundary = series_rows(rows, "B", "fixed-positive-time tail")

    configured_generations = [int(value) for value in config["carrierGenerations"]]
    configured_counts = [1 << generation for generation in configured_generations]
    coherent_counts = [int(float(row["x"])) for row in coherent]
    rs_counts = [int(float(row["x"])) for row in rudin_shapiro]
    formula_defects = [
        relative_defect(float(row["y"]), coherent_prefactor(int(float(row["x"]))))
        for row in coherent
    ] + [
        relative_defect(
            float(row["y"]), rudin_shapiro_prefactor(int(float(row["x"])))
        )
        for row in rudin_shapiro
    ]
    coherent_constant = (81.0 / 2.0) ** (1.0 / 3.0)
    rs_constant = 3.0 ** (4.0 / 3.0) / 2.0
    reference_defects = [
        relative_defect(
            float(row["y"]),
            coherent_constant * int(float(row["x"])) ** (-10.0 / 3.0),
        )
        for row in coherent_reference
    ] + [
        relative_defect(
            float(row["y"]),
            rs_constant * int(float(row["x"])) ** (-8.0 / 3.0),
        )
        for row in rudin_shapiro_reference
    ]

    boundary_defects: list[float] = []
    for source_rows, formula in (
        (coherent_boundary, lambda beta: min(2.5, (10.0 + 3.0 * beta) / 7.0)),
        (arbitrary_boundary, lambda beta: min(2.0, (8.0 + 3.0 * beta) / 7.0)),
        (fixed_boundary, lambda beta: min(2.25, (9.0 + 3.0 * beta) / 7.0)),
    ):
        boundary_defects.extend(
            relative_defect(float(row["y"]), formula(float(row["x"])))
            for row in source_rows
        )
    nested_defect = max(
        max(0.0, float(arbitrary["y"]) - float(fixed["y"]))
        + max(0.0, float(fixed["y"]) - float(coherent_row["y"]))
        for coherent_row, arbitrary, fixed in zip(
            coherent_boundary, arbitrary_boundary, fixed_boundary, strict=True
        )
    )

    producer_rows = producer["rudinShapiro"]["oddGenerationExactFamily"]["rows"]
    producer_defect = max(
        relative_defect(
            float(row["Phi"]), rudin_shapiro_prefactor(int(row["M"]))
        )
        for row in producer_rows
    )
    independent_rows = independent["rudinShapiro"]["rows"]
    independent_defect = 0.0
    for row in independent_rows:
        count = int(row["M"])
        inferred_kz = math.sqrt(float(row["rhoSquared"]) / (2.0 * count))
        normalized = float(row["normalizedGeometricPrefactor"]) / inferred_kz ** (
            2.0 / 3.0
        )
        independent_defect = max(
            independent_defect,
            relative_defect(normalized, rudin_shapiro_prefactor(count)),
        )

    png = Image.open(ROOT / "figure.png")
    png_dpi = png.info.get("dpi", (0.0, 0.0))
    expected_width = round(
        float(config["figure"]["widthMillimetres"]) / 25.4 * 600
    )
    expected_height = round(
        float(config["figure"]["heightMillimetres"]) / 25.4 * 600
    )
    qa_original = Image.open(ROOT / "qa-original.png")
    qa_gray = Image.open(ROOT / "qa-grayscale.png")
    qa_pdf = Image.open(ROOT / "qa-pdf.png")

    reader = PdfReader(ROOT / "figure.pdf")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) / 72.0 * 25.4
    height_mm = float(page.mediabox.height) / 72.0 * 25.4

    panel_counts = {
        panel: sum(row["panel"] == panel for row in rows) for panel in ("A", "B")
    }
    endpoint_values = {
        "coherentBetaZero": float(coherent_boundary[0]["y"]),
        "arbitraryBetaZero": float(arbitrary_boundary[0]["y"]),
        "fixedBetaZero": float(fixed_boundary[0]["y"]),
        "coherentCap": max(float(row["y"]) for row in coherent_boundary),
        "arbitraryCap": max(float(row["y"]) for row in arbitrary_boundary),
        "fixedCap": max(float(row["y"]) for row in fixed_boundary),
    }
    source_hashes = {
        row["path"]: row["sha256"] for row in metadata["sourceFiles"]
    }
    claim_boundary = str(contract["claimBoundary"]).lower()

    checks = [
        check(
            "source certificates passed",
            bool(producer["allPassed"]) and bool(independent["allPassed"]),
            results["sourceStatus"],
            "producer and independent allPassed are true",
        ),
        check(
            "certificate hashes are current",
            source_hashes[str(producer_path.relative_to(REPOSITORY))]
            == sha256(producer_path)
            and source_hashes[str(independent_path.relative_to(REPOSITORY))]
            == sha256(independent_path),
            source_hashes,
            "figure-data metadata hashes match both archived source certificates",
        ),
        check(
            "two-panel data contract",
            panel_counts == {"A": 40, "B": 483},
            panel_counts,
            "Panel A has four ten-point analytic series and Panel B has three 161-point boundaries",
        ),
        check(
            "odd-generation carrier grid",
            coherent_counts == configured_counts
            and rs_counts == configured_counts
            and configured_generations == list(range(1, 20, 2)),
            {"generations": configured_generations, "counts": configured_counts},
            "n=1,3,...,19 and M=2^n appear once in each exact family",
        ),
        check(
            "exact prefactor formulas",
            max(formula_defects) < 3.0e-15,
            max(formula_defects),
            "coherent and Rudin-Shapiro CSV values match their exact finite-M formulas",
        ),
        check(
            "analytic slope references",
            max(reference_defects) < 3.0e-15,
            max(reference_defects),
            "reference curves are the stated -10/3 and -8/3 power laws, not regressions",
        ),
        check(
            "producer exact-family agreement",
            producer_defect < 3.0e-15,
            producer_defect,
            "all producer odd-generation rows agree with the Kz=1 closed formula",
        ),
        check(
            "independent exact-family agreement",
            independent_defect < 3.0e-15,
            independent_defect,
            "all independent rows agree after removing their independently chosen Kz^(2/3) scale",
        ),
        check(
            "phase boundary formulas and nesting",
            max(boundary_defects) < 3.0e-15 and nested_defect == 0.0,
            {
                "maximumFormulaDefect": max(boundary_defects),
                "nestingViolation": nested_defect,
            },
            "the three strict sufficient boundaries match their formulas and remain ordered",
        ),
        check(
            "phase boundary endpoints",
            abs(endpoint_values["coherentBetaZero"] - 10.0 / 7.0) < 2.0e-15
            and abs(endpoint_values["arbitraryBetaZero"] - 8.0 / 7.0) < 2.0e-15
            and abs(endpoint_values["fixedBetaZero"] - 9.0 / 7.0) < 2.0e-15
            and abs(endpoint_values["coherentCap"] - 2.5) < 2.0e-15
            and abs(endpoint_values["arbitraryCap"] - 2.0) < 2.0e-15
            and abs(endpoint_values["fixedCap"] - 2.25) < 2.0e-15,
            endpoint_values,
            "beta=0 endpoints and saturation caps are exact",
        ),
        check(
            "deterministic analytic data only",
            config["randomness"] is False
            and results["randomness"] is False
            and results["regressionOrFittedMaximumUsed"] is False,
            {
                "configRandomness": config["randomness"],
                "resultsRandomness": results["randomness"],
                "fitUsed": results["regressionOrFittedMaximumUsed"],
            },
            "no random sample, regression, or fitted maximum enters the plotted claim",
        ),
        check(
            "formal PNG dimensions and resolution",
            abs(png.width - expected_width) <= 6
            and abs(png.height - expected_height) <= 6
            and abs(float(png_dpi[0]) - 600.0) < 0.1
            and abs(float(png_dpi[1]) - 600.0) < 0.1,
            {"pixels": [png.width, png.height], "dpi": list(png_dpi)},
            "178x86 mm nominal size at 600 dpi within Matplotlib quantization",
        ),
        check(
            "PDF has one correctly sized page",
            len(reader.pages) == 1
            and abs(width_mm - 178.0) < 0.30
            and abs(height_mm - 86.0) < 0.30,
            {"pages": len(reader.pages), "millimetres": [width_mm, height_mm]},
            "one nominal 178x86 mm page within Matplotlib quantization",
        ),
        check(
            "vector and QA assets are present",
            (ROOT / "figure.svg").stat().st_size > 10000
            and qa_original.size == qa_gray.size
            and abs(qa_pdf.width - qa_original.width) <= 2
            and abs(qa_pdf.height - qa_original.height) <= 2,
            {
                "svgBytes": (ROOT / "figure.svg").stat().st_size,
                "qaOriginal": list(qa_original.size),
                "qaGrayscale": list(qa_gray.size),
                "qaPdf": list(qa_pdf.size),
            },
            "SVG is nontrivial and color, grayscale, and PDF QA surfaces share final size",
        ),
        check(
            "claim boundary is explicit",
            all(
                token in claim_boundary
                for token in (
                    "algebraic",
                    "root-ledger saturation",
                    "sufficient strict regions",
                    "remaining tail",
                    "no dns",
                    "general navier-stokes endpoint",
                )
            ),
            contract["claimBoundary"],
            "algebraic sharpness, sufficiency, tail-only burn-in, DNS, and endpoint limits are stated",
        ),
    ]
    all_passed = all(bool(row["passed"]) for row in checks)
    payload = {
        "schemaVersion": "r072c-figure-validation-v1",
        "validatedAt": datetime.now(TIMEZONE).isoformat(timespec="seconds"),
        "allPassed": all_passed,
        "checkCount": len(checks),
        "passedCheckCount": sum(bool(row["passed"]) for row in checks),
        "checks": checks,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    if not all_passed:
        failed = [row["name"] for row in checks if not row["passed"]]
        raise AssertionError(f"figure validation failed: {failed}")
    print(f"figure validation passed: {payload['passedCheckCount']}/{payload['checkCount']}")


if __name__ == "__main__":
    main()
