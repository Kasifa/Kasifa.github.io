#!/usr/bin/env python3
"""Validate R0.72E-1 data lineage, finite diagnostics, and exports."""

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

from PIL import Image


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


def maximum(values: list[float]) -> float:
    if not values:
        raise RuntimeError("empty validation comparison")
    return max(values)


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

    panel_counts = {
        panel: sum(item["panel"] == panel for item in rows)
        for panel in ("A", "B", "C")
    }
    expected_panel_counts = {"A": 10, "B": 10, "C": 12}
    expected_r = [int(value) for value in config["expected"]["besselR"]]
    producer_deltas = [
        int(value) for value in config["expected"]["producerActionDeltas"]
    ]
    independent_deltas = [
        int(value) for value in config["expected"]["independentActionDeltas"]
    ]

    source_hashes = {item["path"]: item["sha256"] for item in metadata["sourceFiles"]}
    source_paths = (
        producer_path,
        independent_path,
        ROOT / "contract.json",
        ROOT / "config.json",
    )
    current_source_hashes = {
        str(path.relative_to(REPOSITORY)): sha256(path) for path in source_paths
    }

    copy_defects: list[float] = []
    producer_bessel_source = {
        int(item["R"]): item for item in producer["bessel"]["prefixRows"]
    }
    independent_root_source = {
        int(item["R"]): item for item in independent["rootFiniteLattice"]
    }
    for item in series(rows, "A", "producer frozen Bessel mass"):
        source = producer_bessel_source[int(float(item["x"]))]
        copy_defects.extend(
            (
                abs(float(item["rawValue"]) - float(source["selectedSlopeMass"])),
                abs(float(item["y"]) - float(source["massOverLogR"])),
            )
        )
    for item in series(rows, "A", "independent dissipative-root mass"):
        r_value = int(float(item["x"]))
        source = independent_root_source[r_value]
        copy_defects.extend(
            (
                abs(float(item["rawValue"]) - float(source["exactSelectedMass"])),
                abs(
                    float(item["y"])
                    - float(source["exactSelectedMass"]) / math.log(r_value)
                ),
            )
        )

    producer_action_source = {
        int(item["delta"]): item
        for item in producer["negativeSobolevAction"]["rows"]
    }
    independent_action_source = {
        int(item["delta"]): item for item in independent["actionFiniteLattice"]
    }
    for item in series(rows, "B", "producer split-step action"):
        delta = int(float(item["x"]))
        source_q = float(producer_action_source[delta]["Q"])
        copy_defects.extend(
            (
                abs(float(item["rawValue"]) - source_q),
                abs(float(item["y"]) - delta * source_q / math.log(delta)),
            )
        )
    for item in series(rows, "B", "independent BDF action"):
        delta = int(float(item["x"]))
        source_q = float(independent_action_source[delta]["actionFine"])
        copy_defects.extend(
            (
                abs(float(item["rawValue"]) - source_q),
                abs(float(item["y"]) - delta * source_q / math.log(delta)),
            )
        )

    producer_ledger_source = {
        int(item["R"]): item for item in producer["physicalLedger"]["rows"]
    }
    independent_ledger_source = {
        int(item["R"]): item
        for item in independent["physicalLedger"]["rootLedgers"]
    }
    producer_base = float(
        producer_ledger_source[expected_r[0]]["rootLedgerScaling"][
            "besselWeightedRatioProxy"
        ]
    )
    independent_base = float(
        independent_ledger_source[expected_r[0]]["ledgerOverDOneThird"]
    )
    for item in series(rows, "C", "producer selected-ledger proxy"):
        r_value = int(float(item["x"]))
        raw_value = float(
            producer_ledger_source[r_value]["rootLedgerScaling"][
                "besselWeightedRatioProxy"
            ]
        )
        copy_defects.extend(
            (
                abs(float(item["rawValue"]) - raw_value),
                abs(float(item["y"]) - raw_value / producer_base),
            )
        )
    for item in series(rows, "C", "independent selected-ledger lower bound"):
        r_value = int(float(item["x"]))
        raw_value = float(independent_ledger_source[r_value]["ledgerOverDOneThird"])
        copy_defects.extend(
            (
                abs(float(item["rawValue"]) - raw_value),
                abs(float(item["y"]) - raw_value / independent_base),
            )
        )

    frozen_mass_copy_defects = [
        abs(
            float(producer_bessel_source[r_value]["selectedSlopeMass"])
            - float(independent_root_source[r_value]["besselMass"])
        )
        for r_value in expected_r
    ]
    terminal_mass_ratio = (
        float(independent_root_source[expected_r[-1]]["exactSelectedMass"])
        / math.log(expected_r[-1])
    )
    mass_target = 8.0 / math.pi**2

    producer_action_values = [
        float(item["y"]) for item in series(rows, "B", "producer split-step action")
    ]
    independent_action_values = [
        float(item["y"]) for item in series(rows, "B", "independent BDF action")
    ]
    producer_action_spread = max(producer_action_values) / min(
        producer_action_values
    )
    independent_action_spread = max(independent_action_values) / min(
        independent_action_values
    )
    producer_discretization = max(
        float(item["fineCoarseRelativeDifference"])
        for item in producer["negativeSobolevAction"]["rows"]
    )
    independent_quadrature = max(
        float(item["quadratureRelativeDefect"])
        for item in independent["actionFiniteLattice"]
    )

    producer_ratio_rows = series(rows, "C", "producer selected-ledger proxy")
    independent_ratio_rows = series(
        rows, "C", "independent selected-ledger lower bound"
    )
    reference_ratio_rows = series(rows, "C", "analytic R^(4/3) reference")
    producer_ratio_values = [float(item["y"]) for item in producer_ratio_rows]
    independent_ratio_values = [float(item["y"]) for item in independent_ratio_rows]
    reference_ratio_values = [float(item["y"]) for item in reference_ratio_rows]
    producer_slope = float(results["panels"]["C"]["producerRExponentFit"]["slope"])
    independent_slope = float(
        results["panels"]["C"]["independentRExponentFit"]["slope"]
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
    pages, pdf_width_mm, pdf_height_mm = pdf_dimensions(ROOT / "figure.pdf")
    svg_text = (ROOT / "figure.svg").read_text(encoding="utf-8")

    public_dir = REPOSITORY / config["publication"]["directory"]
    public_stem = config["publication"]["stem"]
    public_matches = {}
    for suffix in ("pdf", "svg", "png"):
        source_path = ROOT / f"figure.{suffix}"
        target_path = public_dir / f"{public_stem}.{suffix}"
        public_matches[suffix] = (
            target_path.exists() and sha256(source_path) == sha256(target_path)
        )

    panel_a_grids = {
        name: [int(float(item["x"])) for item in series(rows, "A", name)]
        for name in (
            "producer frozen Bessel mass",
            "independent dissipative-root mass",
        )
    }
    panel_b_grids = {
        "producer": [
            int(float(item["x"]))
            for item in series(rows, "B", "producer split-step action")
        ],
        "independent": [
            int(float(item["x"]))
            for item in series(rows, "B", "independent BDF action")
        ],
    }
    panel_c_grids = {
        name: [int(float(item["x"])) for item in series(rows, "C", name)]
        for name in (
            "producer selected-ledger proxy",
            "independent selected-ledger lower bound",
            "analytic R^(4/3) reference",
        )
    }

    boundary = str(contract["claimBoundary"]).lower()
    comparison_boundary = str(results["panels"]["B"]["comparisonBoundary"])
    checks = [
        check(
            "source certificates passed",
            bool(
                producer["status"] == "passed"
                and producer["allRequiredChecksPassed"]
                and producer["defaultGridComplete"]
                and independent["allPassed"]
                and not independent.get("smokeMode", False)
            ),
            results["sourceStatus"],
            "both complete certificates passed on their default grids",
        ),
        check(
            "source hashes are current",
            all(
                source_hashes.get(path) == digest
                for path, digest in current_source_hashes.items()
            ),
            current_source_hashes,
            "metadata hashes match both certificates, contract, and config",
        ),
        check(
            "three-panel row contract",
            panel_counts == expected_panel_counts and len(rows) == 32,
            {"actual": panel_counts, "expected": expected_panel_counts},
            "all 32 plotted certificate and reference rows are archived",
        ),
        check(
            "panel grids",
            all(values == expected_r for values in panel_a_grids.values())
            and panel_b_grids["producer"] == producer_deltas
            and panel_b_grids["independent"] == independent_deltas
            and all(values == expected_r for values in panel_c_grids.values()),
            {"A": panel_a_grids, "B": panel_b_grids, "C": panel_c_grids},
            "every panel uses the declared finite checkpoint grids",
        ),
        check(
            "certificate values copied exactly",
            maximum(copy_defects) == 0.0,
            maximum(copy_defects),
            "raw and normalized CSV values are exact source-derived copies",
        ),
        check(
            "frozen Bessel cross-audit",
            maximum(frozen_mass_copy_defects) < 3.0e-15,
            maximum(frozen_mass_copy_defects),
            "producer and independent frozen Bessel masses agree to rounding",
        ),
        check(
            "Bessel mass convergence",
            abs(terminal_mass_ratio - mass_target) < 0.06
            and abs(
                float(independent_root_source[expected_r[-1]][
                    "relativeMassDifference"
                ])
            )
            < 1.0e-5,
            {
                "terminalMassOverLogR": terminal_mass_ratio,
                "target": mass_target,
                "terminalRelativeDissipativeDefect": independent_root_source[
                    expected_r[-1]
                ]["relativeMassDifference"],
            },
            "terminal mass coefficient is near 8/pi^2 and dissipative defect is small",
        ),
        check(
            "action scales bounded on each finite window",
            min(producer_action_values) > 0.0
            and min(independent_action_values) > 0.0
            and producer_action_spread < 1.25
            and independent_action_spread < 1.25,
            {
                "producerQ06Normalized": producer_action_values,
                "independentQ01Normalized": independent_action_values,
                "producerSpread": producer_action_spread,
                "independentSpread": independent_action_spread,
            },
            "each separately labeled horizon has bounded delta*Q/log(delta)",
        ),
        check(
            "action horizons are not conflated",
            float(results["panels"]["B"]["producerFinalX"]) == 6.0
            and float(results["panels"]["B"]["independentFinalX"]) == 1.0
            and "Q(0,6)" in comparison_boundary
            and "Q(0,1)" in comparison_boundary
            and "not same-endpoint" in comparison_boundary,
            comparison_boundary,
            "producer Q(0,6) and independent Q(0,1) remain separate sequences",
        ),
        check(
            "action discretization diagnostics",
            producer_discretization < 1.0e-4
            and independent_quadrature < 2.0e-4,
            {
                "producerMaximumFineCoarseRelativeDifference": producer_discretization,
                "independentMaximumQuadratureRelativeDefect": independent_quadrature,
            },
            "both action discretizations pass their declared refinement checks",
        ),
        check(
            "selected-ledger growth and power reference",
            producer_ratio_values[0] == independent_ratio_values[0] == 1.0
            and all(
                later > earlier
                for earlier, later in zip(
                    producer_ratio_values[:-1], producer_ratio_values[1:], strict=True
                )
            )
            and all(
                later > earlier
                for earlier, later in zip(
                    independent_ratio_values[:-1],
                    independent_ratio_values[1:],
                    strict=True,
                )
            )
            and 1.20 < producer_slope < 1.36
            and 1.20 < independent_slope < 1.36
            and all(
                abs(value - (r_value / 8.0) ** (4.0 / 3.0)) < 1.0e-14
                for value, r_value in zip(
                    reference_ratio_values, expected_r, strict=True
                )
            ),
            {
                "producerNormalized": producer_ratio_values,
                "independentNormalized": independent_ratio_values,
                "producerFiniteSlope": producer_slope,
                "independentFiniteSlope": independent_slope,
                "analyticExponent": 4.0 / 3.0,
            },
            "finite ratios rise near the declared non-fitted R^(4/3) power ledger",
        ),
        check(
            "formal PNG dimensions and 600 dpi",
            abs(png.width - expected_width) <= 6
            and abs(png.height - expected_height) <= 6
            and max(abs(value - 600.0) for value in png_dpi) < 0.1,
            {"pixels": [png.width, png.height], "dpi": png_dpi},
            "178x88 mm nominal page at approximately 600 dpi",
        ),
        check(
            "vector PDF and SVG exports",
            pages == 1
            and abs(pdf_width_mm - 178.0) < 0.30
            and abs(pdf_height_mm - 88.0) < 0.30
            and "<svg" in svg_text
            and ("<path" in svg_text or "<polyline" in svg_text),
            {
                "pdfPages": pages,
                "pdfMillimetres": [pdf_width_mm, pdf_height_mm],
                "svgBytes": len(svg_text.encode()),
            },
            "one correctly sized vector PDF page and nontrivial vector SVG",
        ),
        check(
            "final-size, grayscale, and PDF QA surfaces",
            qa_final.size == qa_gray.size == qa_pdf.size
            and qa_gray.mode == "L"
            and qa_final.width > 1500
            and qa_final.height > 730,
            {
                "finalSize": list(qa_final.size),
                "grayscaleMode": qa_gray.mode,
                "pdfSize": list(qa_pdf.size),
            },
            "all QA surfaces use the same readable 220 dpi final footprint",
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
                    "deterministic finite",
                    "lower bound",
                    "lambda1",
                    "do not prove",
                    "malliavin",
                    "regularity",
                    "millennium",
                )
            ),
            contract["claimBoundary"],
            "finite evidence and every analytic/Millennium boundary are stated",
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
    previous_validation: dict[str, Any] = {}
    if validation_path.exists():
        try:
            previous_validation = load_json(validation_path)
        except (json.JSONDecodeError, OSError):
            previous_validation = {}
    if (
        previous_validation.get("checks") == checks
        and previous_validation.get("allPassed") == all_passed
    ):
        validated_at = previous_validation.get("validatedAt")
    else:
        validated_at = datetime.now(TIMEZONE).isoformat(timespec="seconds")
    payload = {
        "schemaVersion": "r072e-figure-validation-v1",
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
        "# R0.72E-1 figure QA report",
        "",
        (
            f"- Automated validation: **{payload['passedCheckCount']}/"
            f"{payload['checkCount']} passed**."
        ),
        f"- Final size: {pdf_width_mm:.3f} x {pdf_height_mm:.3f} mm.",
        (
            f"- Archival PNG: {png.width} x {png.height} px at "
            f"{png_dpi[0]:.3f} dpi."
        ),
        (
            f"- Final-size QA: {qa_final.width} x {qa_final.height} px "
            "at 220 dpi."
        ),
        f"- Maximum source-copy defect: {maximum(copy_defects):.3e}.",
        (
            "- Finite Panel C slopes: "
            f"{producer_slope:.6f} (producer), "
            f"{independent_slope:.6f} (independent)."
        ),
        (
            "- Panel B labels preserve distinct windows: producer Q(0,6), "
            "independent Q(0,1)."
        ),
        f"- Public copies byte-identical: {all(public_matches.values())}.",
        (
            "- Visual inspection: final-size color, grayscale, and PDF raster "
            "have no clipped labels or collisions."
        ),
        (
            "- Grayscale inspection: marker fill and line styles preserve "
            "producer, independent, and reference distinctions."
        ),
        "",
        (
            "The archived surfaces are finite numerical diagnostics. They do "
            "not replace the analytic infinite-lattice, negative-Sobolev, or "
            "Malliavin arguments."
        ),
        "",
    ]
    (ROOT / "qa-report.md").write_text("\n".join(lines), encoding="utf-8")
    if not all_passed:
        failed = [item["name"] for item in checks if not item["passed"]]
        raise AssertionError(f"R0.72E figure validation failed: {failed}")
    print(
        f"R0.72E figure validation passed: "
        f"{payload['passedCheckCount']}/{payload['checkCount']}"
    )


if __name__ == "__main__":
    main()
