#!/usr/bin/env python3
"""Validate R0.72B-1 data identities and exported figure assets."""

from __future__ import annotations

import csv
from datetime import datetime
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


def check(name: str, passed: bool, value: object, requirement: str) -> dict[str, object]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def main() -> None:
    config = load_json(ROOT / "config.json")
    contract = load_json(ROOT / "contract.json")
    results = load_json(ROOT / "results.json")
    producer = load_json(REPOSITORY / config["sourceCertificates"]["producer"])
    independent = load_json(REPOSITORY / config["sourceCertificates"]["independent"])
    with (ROOT / "data.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))

    panel_counts = {
        panel: sum(row["panel"] == panel for row in rows) for panel in ("A", "B", "C")
    }
    producer_equal = {
        int(row["M"]): row for row in producer["equalCarrierLedger"]["rows"]
    }
    independent_equal = {
        int(row["M"]): row for row in independent["equalCarrierLedger"]["rows"]
    }
    common_m = sorted(set(producer_equal) & set(independent_equal))
    maximum_prefactor_defect = max(
        abs(
            float(producer_equal[m_value]["normalizedGeometricPrefactor"])
            - float(independent_equal[m_value]["normalizedGeometricPrefactor"])
        )
        / max(
            abs(float(producer_equal[m_value]["normalizedGeometricPrefactor"])),
            1.0e-300,
        )
        for m_value in common_m
    )

    producer_bessel = {
        int(row["R"]): row for row in producer["besselNoGo"]["rows"]
    }
    independent_bessel = {
        int(row["R"]): row for row in independent["besselNoGo"]["rows"]
    }
    common_r = sorted(set(producer_bessel) & set(independent_bessel))
    maximum_bessel_defect = max(
        abs(
            float(producer_bessel[r_value][producer_key])
            - float(independent_bessel[r_value][independent_key])
        )
        / max(abs(float(producer_bessel[r_value][producer_key])), 1.0e-300)
        for r_value in common_r
        for producer_key, independent_key in (
            ("ThetaLayerTimesFrozenRate", "Theta"),
            ("heatFreezingXi", "Xi"),
            ("energyLossUpper", "energyLossUpper"),
        )
    )

    png = Image.open(ROOT / "figure.png")
    png_dpi = png.info.get("dpi", (0.0, 0.0))
    expected_width = round(float(config["figure"]["widthMillimetres"]) / 25.4 * 600)
    expected_height = round(float(config["figure"]["heightMillimetres"]) / 25.4 * 600)
    qa_original = Image.open(ROOT / "qa-original.png")
    qa_gray = Image.open(ROOT / "qa-grayscale.png")
    qa_pdf = Image.open(ROOT / "qa-pdf.png")

    reader = PdfReader(ROOT / "figure.pdf")
    page = reader.pages[0]
    width_mm = float(page.mediabox.width) / 72.0 * 25.4
    height_mm = float(page.mediabox.height) / 72.0 * 25.4

    panel_a = [row for row in rows if row["panel"] == "A"]
    coherent_zero = next(
        float(row["y"])
        for row in panel_a
        if row["series"] == "coherent M^-10/3" and float(row["x"]) == 0.0
    )
    coherent_cap = max(
        float(row["y"])
        for row in panel_a
        if row["series"] == "coherent M^-10/3"
    )
    checks = [
        check(
            "source certificates passed",
            bool(producer["allPassed"]) and bool(independent["allPassed"]),
            results["sourceStatus"],
            "producer and independent allPassed are true",
        ),
        check(
            "three panel data contract",
            panel_counts["A"] >= 3 * 100 and panel_counts["B"] >= 3 * 15 and panel_counts["C"] >= 3 * 7,
            panel_counts,
            "dense phase curves and at least three audited series in panels B and C",
        ),
        check(
            "coherent phase endpoints",
            abs(coherent_zero - 10.0 / 7.0) < 2.0e-15
            and abs(coherent_cap - 2.5) < 2.0e-15,
            {"fixedLayer": coherent_zero, "cap": coherent_cap},
            "fixed-layer boundary is 10/7 and terminal cap is 5/2",
        ),
        check(
            "independent equal-carrier agreement",
            maximum_prefactor_defect < 5.0e-15,
            maximum_prefactor_defect,
            "relative prefactor difference below 5e-15",
        ),
        check(
            "independent Bessel-indicator agreement",
            maximum_bessel_defect < 2.0e-7,
            maximum_bessel_defect,
            "relative producer/independent indicator difference below 2e-7",
        ),
        check(
            "formal PNG dimensions and resolution",
            abs(png.width - expected_width) <= 6
            and abs(png.height - expected_height) <= 6
            and abs(float(png_dpi[0]) - 600.0) < 0.1
            and abs(float(png_dpi[1]) - 600.0) < 0.1,
            {"pixels": [png.width, png.height], "dpi": list(png_dpi)},
            "178x86 mm nominal size at 600 dpi within Matplotlib's 0.01-inch quantization",
        ),
        check(
            "PDF has one correctly sized page",
            len(reader.pages) == 1
            and abs(width_mm - 178.0) < 0.30
            and abs(height_mm - 86.0) < 0.30,
            {"pages": len(reader.pages), "millimetres": [width_mm, height_mm]},
            "one nominal 178x86 mm page within Matplotlib's 0.01-inch quantization",
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
            "SVG nontrivial and color/grayscale/PDF QA surfaces share final size",
        ),
        check(
            "claim boundary is explicit",
            all(
                token in contract["claimBoundary"]
                for token in (
                    "not interval arithmetic",
                    "cannot remove pre-burn-in slope mass",
                    "does not construct a normalized lower family",
                )
            ),
            contract["claimBoundary"],
            "interval, burn-in, and lower-construction limits are stated",
        ),
    ]
    all_passed = all(bool(row["passed"]) for row in checks)
    payload = {
        "schemaVersion": "r072b-figure-validation-v1",
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
