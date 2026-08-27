#!/usr/bin/env python3
"""Validate the R0.72O formal figure package and public masters."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat
from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
REPOSITORY = ROOT.parents[2]


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def relerr(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


def check(name: str, passed: bool, value: Any, requirement: str) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def expected_pixels(config: dict[str, Any], dpi: int) -> tuple[int, int]:
    figure = config["figure"]
    return (
        round(float(figure["widthMillimetres"]) / 25.4 * dpi),
        round(float(figure["heightMillimetres"]) / 25.4 * dpi),
    )


def main() -> int:
    config = json.loads((ROOT / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((ROOT / "contract.json").read_text(encoding="utf-8"))
    results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))
    rows = read_csv(ROOT / "data.csv")
    items: list[dict[str, Any]] = []

    required = [
        "README.md",
        "caption.md",
        "figure-contract.md",
        "contract.json",
        "config.json",
        "command.txt",
        "requirements.txt",
        "plot.py",
        "qa_images.py",
        "publish_assets.py",
        "validate.py",
        "build_manifest.py",
        "figure.pdf",
        "figure.svg",
        "figure.png",
        "data.csv",
        "results.json",
        "environment.txt",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "progress.ndjson",
        "resource-log.ndjson",
    ]
    missing = [name for name in required if not (ROOT / name).is_file()]
    items.append(
        check(
            "required_assets",
            not missing,
            missing,
            "all source, master, data, QA, and archive inputs exist",
        )
    )

    width_mm = float(config["figure"]["widthMillimetres"])
    height_mm = float(config["figure"]["heightMillimetres"])
    png_dpi = int(config["figure"]["pngDpi"])
    with Image.open(ROOT / "figure.png") as image:
        png_size = image.size
        png_dpi_meta = image.info.get("dpi", (0.0, 0.0))
    expected_png = expected_pixels(config, png_dpi)
    items.append(
        check(
            "png_600_dpi",
            all(abs(float(value) - png_dpi) < 0.02 for value in png_dpi_meta),
            png_dpi_meta,
            "PNG metadata is 600 dpi",
        )
    )
    items.append(
        check(
            "png_dimensions",
            all(abs(left - right) <= 2 for left, right in zip(png_size, expected_png)),
            {"actual": png_size, "expected": expected_png},
            "PNG pixels match final size at 600 dpi",
        )
    )

    reader = PdfReader(str(ROOT / "figure.pdf"))
    page = reader.pages[0]
    pdf_mm = (
        float(page.mediabox.width) * 25.4 / 72.0,
        float(page.mediabox.height) * 25.4 / 72.0,
    )
    items.append(check("pdf_one_page", len(reader.pages) == 1, len(reader.pages), "PDF has one page"))
    items.append(
        check(
            "pdf_dimensions",
            abs(pdf_mm[0] - width_mm) < 0.08 and abs(pdf_mm[1] - height_mm) < 0.08,
            pdf_mm,
            f"PDF matches {width_mm:g} x {height_mm:g} mm",
        )
    )
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    items.append(
        check(
            "svg_vector_text",
            "<svg" in svg and "<text" in svg and "<image" not in svg,
            {"svg": "<svg" in svg, "text": "<text" in svg, "image": "<image" in svg},
            "SVG is vector-only and keeps editable text",
        )
    )

    qa_dpi = int(config["figure"]["qaDpi"])
    qa_expected = expected_pixels(config, qa_dpi)
    qa_sizes: dict[str, tuple[int, int]] = {}
    for name in ("qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"):
        with Image.open(ROOT / name) as image:
            qa_sizes[name] = image.size
    items.append(
        check(
            "qa_dimensions",
            all(size == qa_expected for size in qa_sizes.values()),
            qa_sizes,
            "QA surfaces match final print size at 180 dpi",
        )
    )
    with Image.open(ROOT / "qa-grayscale.png") as image:
        gray_std = float(ImageStat.Stat(image.convert("L")).stddev[0])
    minimum_gray = float(config["validation"]["minimumGrayscaleStandardDeviation"])
    items.append(
        check(
            "grayscale_contrast",
            gray_std > minimum_gray,
            gray_std,
            f"grayscale standard deviation exceeds {minimum_gray:g}",
        )
    )

    certificate_root = REPOSITORY / config["certificateDirectory"]
    names = config["certificates"]
    windows = {
        "producer audit": read_csv(certificate_root / names["producerWindow"]),
        "independent audit": read_csv(certificate_root / names["independentWindow"]),
    }
    degeneracy = {
        "producer audit": read_csv(certificate_root / names["producerDegeneracy"]),
        "independent audit": read_csv(certificate_root / names["independentDegeneracy"]),
    }
    expected_grid = {
        (r_value, regime, float(level))
        for r_value in config["expectedR"]
        for regime in ("oneCarrier", "worstCommonBand")
        for level in config["expectedLevels"]
    }
    actual_grids = {
        route: {
            (int(row["R"]), row["regime"], float(row["level"]))
            for row in values
        }
        for route, values in windows.items()
    }
    items.append(
        check(
            "certificate_window_grid",
            all(grid == expected_grid for grid in actual_grids.values()),
            {route: len(grid) for route, grid in actual_grids.items()},
            "both routes contain the exact 4 R x 2 regime x 3 level grid",
        )
    )
    degenerate_pass = {
        route: len(values) == len(config["expectedR"])
        and [int(row["R"]) for row in values] == config["expectedR"]
        and all(
            int(row["firstDerivativeAtZero"]) == 0
            and int(row["secondDerivativeAtZero"]) == 0
            and int(row["thirdDerivativeAtZero"])
            == int(row["expectedThirdDerivative"])
            == int(row["R"]) * (2 * int(row["R"]) + 1)
            and truthy(row["passed"])
            for row in values
        )
        for route, values in degeneracy.items()
    }
    items.append(
        check(
            "certificate_exact_degeneracy",
            all(degenerate_pass.values()),
            degenerate_pass,
            "both routes verify U'(0)=U''(0)=0 and U'''(0)=R(2R+1) != 0",
        )
    )
    ledgers = {
        route: json.loads((certificate_root / names[key]).read_text(encoding="utf-8"))
        for route, key in (
            ("producer audit", "producerExponents"),
            ("independent audit", "independentExponents"),
        )
    }
    items.append(
        check(
            "certificate_exact_exponents",
            all(value.get("exactExponentLedgerPassed") is True for value in ledgers.values())
            and all(value["actual"]["UEDOneCarrier"] == {"epsilon": "11/6"} for value in ledgers.values())
            and ledgers["producer audit"] == ledgers["independent audit"],
            {route: value["actual"]["UEDOneCarrier"] for route, value in ledgers.items()},
            "independent exact ledgers agree and give the lifted one-carrier exponent 11/6",
        )
    )
    crosscheck = json.loads((certificate_root / names["crosscheck"]).read_text(encoding="utf-8"))
    tolerance = float(config["validation"]["crossRouteRelativeTolerance"])
    maxima = crosscheck.get("maximumRelativeDifferences", {})
    items.append(
        check(
            "certificate_crosscheck",
            crosscheck.get("status") == "passed"
            and bool(maxima)
            and all(float(value) <= tolerance for value in maxima.values()),
            {"status": crosscheck.get("status"), "maxima": maxima},
            f"crosscheck passes and all route differences are <= {tolerance:g}",
        )
    )

    # Hard endpoint gate requested by the R0.72O mathematical review: ED is
    # equal to the old expression at epsilon=1, never larger thereafter, and
    # strictly smaller at every sampled epsilon>1.
    certificate_endpoint: dict[str, Any] = {}
    for route, values in windows.items():
        equal_rows = [row for row in values if float(row["epsilon"]) == 1.0]
        strict_rows = [row for row in values if float(row["epsilon"]) > 1.0]
        ratios = [
            relerr(float(row["edOverOld"]), float(row["epsilon"]) ** -0.5)
            for row in values
        ]
        certificate_endpoint[route] = {
            "epsilonOneRows": len(equal_rows),
            "epsilonGreaterThanOneRows": len(strict_rows),
            "equalityAtOne": bool(equal_rows)
            and all(relerr(float(row["edDirectNormalized"]), float(row["oldDirectNormalized"])) <= 2.0e-13 for row in equal_rows),
            "strictAfterOne": bool(strict_rows)
            and all(float(row["edDirectNormalized"]) < float(row["oldDirectNormalized"]) for row in strict_rows),
            "noLarger": all(float(row["edDirectNormalized"]) <= float(row["oldDirectNormalized"]) * (1.0 + 2.0e-13) for row in values),
            "maxRatioError": max(ratios),
            "allRowsPassed": all(truthy(row["passed"]) for row in values),
        }
    items.append(
        check(
            "certificate_ed_endpoint_order",
            all(
                value["equalityAtOne"]
                and value["strictAfterOne"]
                and value["noLarger"]
                and value["maxRatioError"] <= 2.0e-13
                and value["allRowsPassed"]
                for value in certificate_endpoint.values()
            ),
            certificate_endpoint,
            "ED equals old at epsilon=1, is strictly smaller for epsilon>1, and has ratio epsilon^(-1/2)",
        )
    )

    minimum_rows = int(config["validation"]["minimumDataRows"])
    panel_counts = {panel: sum(row["panel"] == panel for row in rows) for panel in "ABCD"}
    items.append(
        check(
            "data_completeness",
            len(rows) >= minimum_rows and all(panel_counts[panel] > 0 for panel in "ABCD"),
            {"rows": len(rows), "panels": panel_counts},
            f"data.csv has all four panels and at least {minimum_rows} traceable rows",
        )
    )

    panel_a = [row for row in rows if row["panel"] == "A" and row["route"] == "analytic algebra"]
    panel_a_errors: list[float] = []
    for row in panel_a:
        r_value = float(row["x"])
        expected = (
            r_value ** (2.0 / 3.0) * (1.0 + math.log(r_value))
            if row["series"] == "old one-carrier window"
            else r_value ** (4.0 / 3.0) * (1.0 + math.log(r_value)) ** 2
        )
        panel_a_errors.append(relerr(float(row["y"]), expected))
    expected_a = 2 * int(config["panels"]["A"]["samples"])
    items.append(
        check(
            "panel_a_scale_formulas",
            len(panel_a) == expected_a and max(panel_a_errors) < 2.0e-15,
            {"rows": len(panel_a), "maxRelativeError": max(panel_a_errors)},
            "Panel A directly evaluates the old and ED one-carrier window formulas",
        )
    )

    panel_b = [row for row in rows if row["panel"] == "B" and row["route"] == "analytic algebra"]
    old_b = {float(row["x"]): float(row["y"]) for row in panel_b if row["series"] == "old normalized direct screen"}
    ed_b = {float(row["x"]): float(row["y"]) for row in panel_b if row["series"] == "ED normalized direct screen"}
    b_x = sorted(old_b)
    endpoint_equal = bool(b_x) and b_x[0] == 1.0 and relerr(old_b[1.0], ed_b[1.0]) < 2.0e-15
    strict_after = all(ed_b[value] < old_b[value] for value in b_x if value > 1.0)
    dense_ratio_error = max(relerr(ed_b[value] / old_b[value], value ** -0.5) for value in b_x)
    items.append(
        check(
            "panel_b_ed_endpoint_order",
            len(old_b) == len(ed_b) == int(config["panels"]["B"]["samples"])
            and endpoint_equal
            and strict_after
            and all(ed_b[value] <= old_b[value] for value in b_x)
            and dense_ratio_error < 2.0e-15,
            {
                "samples": len(b_x),
                "epsilonOneEqual": endpoint_equal,
                "strictForAllEpsilonAboveOne": strict_after,
                "maxRatioError": dense_ratio_error,
            },
            "Panel B says no larger, equal at epsilon=1, and strictly smaller for every epsilon>1",
        )
    )
    items.append(
        check(
            "panel_b_fixed_r_boundary",
            bool(b_x) and ed_b[b_x[-1]] > 1.0 and old_b[b_x[-1]] > ed_b[b_x[-1]],
            {"epsilonMaximum": b_x[-1], "old": old_b[b_x[-1]], "ed": ed_b[b_x[-1]]},
            "at fixed R the improved current bound still crosses the scale-one guide",
        )
    )

    conditional_c = [row for row in rows if row["panel"] == "C" and row["series"] == "multi-carrier ED window"]
    unconditional_rows = [row for row in rows if "unconditional" in row["status"].lower()]
    unconditional_c = [row for row in unconditional_rows if row["panel"] == "C"]
    items.append(
        check(
            "panel_c_claim_status",
            len(conditional_c) == int(config["panels"]["C"]["samples"])
            and all(row["status"] == "conditional for N>1" for row in conditional_c)
            and len(unconditional_c) == 1
            and unconditional_c[0]["status"] == "unconditional N=1"
            and float(unconditional_c[0]["p"]) == 1.0,
            {"conditionalRows": len(conditional_c), "unconditionalPanelCRows": len(unconditional_c)},
            "only the declared N=1 point is unconditional; the full multi-carrier curve is conditional",
        )
    )

    panel_d = [row for row in rows if row["panel"] == "D"]
    d_status = {row["series"]: row["status"] for row in panel_d}
    items.append(
        check(
            "panel_d_exact_obstruction",
            len(panel_d) == 2 * int(config["panels"]["D"]["samples"])
            and d_status.get("two-carrier flat critical point") == "unconditional exact identity"
            and d_status.get("Morse quadratic reference") == "reference"
            and all(float(row["y"]) > 0.0 for row in panel_d),
            {"rows": len(panel_d), "statuses": d_status},
            "Panel D encodes the exact flat critical point separately from the Morse reference",
        )
    )

    changed_sources = [
        relative
        for relative, expected in results["sourceHashes"].items()
        if not (REPOSITORY / relative).is_file() or digest(REPOSITORY / relative) != expected
    ]
    changed_package_sources = [
        name
        for name, expected in results["packageSourceHashes"].items()
        if not (ROOT / name).is_file() or digest(ROOT / name) != expected
    ]
    items.append(
        check(
            "source_lineage",
            not changed_sources and not changed_package_sources,
            {"repository": changed_sources, "package": changed_package_sources},
            "analytic, certificate, contract, caption, and plotting sources retain build hashes",
        )
    )

    publication = config["publication"]
    public_root = REPOSITORY / publication["directory"]
    identities = {
        suffix: (public_root / f"{publication['stem']}.{suffix}").is_file()
        and digest(public_root / f"{publication['stem']}.{suffix}") == digest(ROOT / f"figure.{suffix}")
        for suffix in ("pdf", "svg", "png")
    }
    items.append(
        check(
            "public_byte_identity",
            all(identities.values()),
            identities,
            "public masters are byte-identical to archival masters",
        )
    )

    combined = "\n".join(
        [
            (ROOT / "README.md").read_text(encoding="utf-8"),
            (ROOT / "caption.md").read_text(encoding="utf-8"),
            contract["claimBoundary"],
        ]
    ).lower()
    boundary_terms = [
        "no larger",
        "strictly smaller",
        "conditional",
        "fixed-r arbitrary-coupling",
        "general three-dimensional",
        "global navier",
    ]
    items.append(
        check(
            "claim_boundary",
            all(term in combined for term in boundary_terms),
            boundary_terms,
            "caption and contract preserve endpoint, conditionality, fixed-R, and Clay-problem boundaries",
        )
    )
    no_fit = (
        results.get("noPdeEvolution") is True
        and results.get("noFiniteFit") is True
        and results.get("formulaCurvesNotCertificateInterpolation") is True
        and contract["renderPolicy"]["finiteFit"] == "forbidden"
        and not any(" fitted " in f" {row['series'].lower()} " for row in rows)
    )
    items.append(
        check(
            "no_simulation_or_fit",
            no_fit,
            {
                "noPdeEvolution": results.get("noPdeEvolution"),
                "noFiniteFit": results.get("noFiniteFit"),
                "formulaCurvesNotCertificateInterpolation": results.get("formulaCurvesNotCertificateInterpolation"),
            },
            "the figure is exact-algebra extraction with no PDE evolution, regression, fit, or certificate interpolation",
        )
    )

    visual = os.environ.get("R072O_VISUAL_QA_INSPECTED", "").strip().lower() == "true"
    items.append(
        check(
            "visual_inspection_declared",
            visual,
            visual,
            "final-size, grayscale, and PDF-raster surfaces were explicitly inspected",
        )
    )

    all_passed = all(item["passed"] for item in items)
    payload = {
        "schemaVersion": 1,
        "figureId": "R0.72O-1",
        "status": "passed" if all_passed else "failed",
        "allPassed": all_passed,
        "checkCount": len(items),
        "checks": items,
    }
    (ROOT / "validation.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    failed = [item["name"] for item in items if not item["passed"]]
    (ROOT / "qa-report.md").write_text(
        "\n".join(
            [
                "# R0.72O figure QA report",
                "",
                f"- Automatic validation: **{'PASS' if all_passed else 'FAIL'}** ({len(items)} checks).",
                f"- Final print size: {pdf_mm[0]:.3f} x {pdf_mm[1]:.3f} mm; PNG {png_size[0]} x {png_size[1]} px at 600 dpi.",
                f"- QA surfaces: {qa_expected[0]} x {qa_expected[1]} px at 180 dpi; grayscale standard deviation {gray_std:.3f}.",
                (
                    "- Human inspection: final-size, grayscale, and PDF-raster surfaces checked for legibility, collisions, line/marker distinction, and the locked header blossom."
                    if visual
                    else "- Human inspection: not declared."
                ),
                "- Endpoint gate: the enhanced-dissipation screen is equal to the old screen at epsilon=1, no larger throughout, and strictly smaller for epsilon>1.",
                "- Claim boundary: only the filled one-carrier point is unconditional; multi-carrier extension remains conditional and the fixed-R arbitrary-coupling limit remains open.",
                f"- Failed checks: {', '.join(failed) if failed else 'none'}.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"status": payload["status"], "checks": len(items), "failed": failed}, sort_keys=True))
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
