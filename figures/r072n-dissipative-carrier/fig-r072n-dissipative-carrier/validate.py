#!/usr/bin/env python3
"""Validate the R0.72N formal figure package and public masters."""

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


def check(
    name: str, passed: bool, value: Any, requirement: str
) -> dict[str, Any]:
    return {
        "name": name,
        "passed": bool(passed),
        "value": value,
        "requirement": requirement,
    }


def relerr(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-300)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def truthy(value: str) -> bool:
    return value.strip().lower() in {"true", "1", "yes"}


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
        dpi_meta = image.info.get("dpi", (0.0, 0.0))
    expected_png = (
        round(width_mm / 25.4 * png_dpi),
        round(height_mm / 25.4 * png_dpi),
    )
    items.append(
        check(
            "png_600_dpi",
            all(abs(float(value) - png_dpi) < 0.02 for value in dpi_meta),
            dpi_meta,
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
    items.append(
        check(
            "pdf_one_page",
            len(reader.pages) == 1,
            len(reader.pages),
            "PDF has one page",
        )
    )
    items.append(
        check(
            "pdf_dimensions",
            abs(pdf_mm[0] - width_mm) < 0.08
            and abs(pdf_mm[1] - height_mm) < 0.08,
            pdf_mm,
            "PDF matches 177.8 x 124.0 mm",
        )
    )
    svg = (ROOT / "figure.svg").read_text(encoding="utf-8")
    items.append(
        check(
            "svg_vector_text",
            "<svg" in svg and "<text" in svg and "<image" not in svg,
            {
                "svg": "<svg" in svg,
                "text": "<text" in svg,
                "image": "<image" in svg,
            },
            "SVG is vector and keeps editable text",
        )
    )

    qa_dpi = int(config["figure"]["qaDpi"])
    qa_expected = (
        round(width_mm / 25.4 * qa_dpi),
        round(height_mm / 25.4 * qa_dpi),
    )
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
    minimum_gray = float(
        config["validation"]["minimumGrayscaleStandardDeviation"]
    )
    items.append(
        check(
            "grayscale_contrast",
            gray_std > minimum_gray,
            gray_std,
            f"grayscale standard deviation exceeds {minimum_gray:g}",
        )
    )

    expected_sigmas = [float(value) for value in config["expectedSigmas"]]
    certificate_root = REPOSITORY / config["certificateDirectory"]
    certificate_names = config["certificates"]
    certificates = {
        route: read_csv(certificate_root / certificate_names[route])
        for route in ("producer", "independent")
    }
    certificate_grids = {
        route: [float(row["sigma"]) for row in values]
        for route, values in certificates.items()
    }
    items.append(
        check(
            "certificate_sigma_grid",
            all(grid == expected_sigmas for grid in certificate_grids.values()),
            certificate_grids,
            "both finite routes use the exact declared ten-case sigma grid",
        )
    )
    crosscheck_path = certificate_root / certificate_names["crosscheck"]
    crosscheck = json.loads(crosscheck_path.read_text(encoding="utf-8"))
    tolerance = float(config["validation"]["crossRouteRelativeTolerance"])
    maxima = crosscheck.get("maximumRelativeDifferences", {})
    items.append(
        check(
            "certificate_crosscheck",
            crosscheck.get("status") == "passed"
            and bool(maxima)
            and all(float(value) <= tolerance for value in maxima.values()),
            {"status": crosscheck.get("status"), "maxima": maxima},
            f"crosscheck passes and all declared route differences are <= {tolerance:g}",
        )
    )

    theorem_a = [
        row
        for row in rows
        if row["panel"] == "A" and row["kind"] == "theorem"
    ]
    errors_a = [
        relerr(
            float(row["y"]),
            max(1.0, (2.0 * float(row["x"])) ** (2.0 / 3.0)),
        )
        for row in theorem_a
    ]
    items.append(
        check(
            "panel_a_theorem_formula",
            len(theorem_a) == int(config["panels"]["A"]["analyticSamples"])
            and max(errors_a) < 2.0e-15,
            {"rows": len(theorem_a), "maxRelativeError": max(errors_a)},
            "Panel A samples exactly the strict full-chain moment barrier",
        )
    )

    slack = float(config["validation"]["momentBarrierRelativeSlack"])
    moment_checks: list[bool] = []
    certificate_passes: list[bool] = []
    tail_values: list[float] = []
    for route, values in certificates.items():
        tail_field = (
            "maxHighModeMass" if route == "producer" else "boundaryMass"
        )
        for value in values:
            sigma = float(value["sigma"])
            exact_barrier = max(1.0, (2.0 * sigma) ** (2.0 / 3.0))
            moment_checks.append(
                relerr(float(value["momentBarrier"]), exact_barrier) < 2.0e-15
                and float(value["maxMoment"]) <= exact_barrier * (1.0 + slack)
            )
            certificate_passes.append(truthy(value["passed"]))
            tail_values.append(float(value[tail_field]))
    items.append(
        check(
            "finite_moment_barrier",
            all(moment_checks),
            {"cases": len(moment_checks), "relativeSlack": slack},
            "every finite point respects the exact barrier with declared audit slack",
        )
    )
    tail_maximum = float(config["validation"]["finiteTailMaximum"])
    items.append(
        check(
            "finite_certificate_gates",
            all(certificate_passes) and max(tail_values) < tail_maximum,
            {
                "allRowsPassed": all(certificate_passes),
                "maxTail": max(tail_values),
            },
            f"all finite rows pass and spatial tail is below {tail_maximum:g}",
        )
    )

    mapping = {
        ("A", "D max"): "maxMoment",
        ("B", "scaled action"): "scaledAction",
        ("B", "action-poor proxy"): "actionPoorRatio",
        ("C", "T_proxy/V_proxy"): "tOverV",
        ("D", "C/log sigma"): "cubicOverLogSigma",
        ("D", "C/sqrt sigma"): "cubicOverSqrtSigma",
    }
    mapping_errors: list[float] = []
    route_row_counts: dict[str, int] = {}
    for route, values in certificates.items():
        by_sigma = {float(value["sigma"]): value for value in values}
        route_rows = [
            row
            for row in rows
            if row["route"] == route and row["kind"] == "finite diagnostic"
        ]
        route_row_counts[route] = len(route_rows)
        for row in route_rows:
            field = mapping[(row["panel"], row["series"])]
            mapping_errors.append(
                relerr(
                    float(row["y"]),
                    float(by_sigma[float(row["x"])][field]),
                )
            )
    expected_route_rows = len(expected_sigmas) * len(mapping)
    items.append(
        check(
            "certificate_data_mapping",
            all(count == expected_route_rows for count in route_row_counts.values())
            and max(mapping_errors) < 2.0e-15,
            {
                "rows": route_row_counts,
                "maxRelativeError": max(mapping_errors),
            },
            "all six plotted finite observables per case are exact CSV mappings",
        )
    )

    panel_b = [
        row
        for row in rows
        if row["panel"] == "B" and row["kind"] == "finite diagnostic"
    ]
    action_growth: dict[str, bool] = {}
    for route in ("producer", "independent"):
        ratio_rows = sorted(
            (
                row
                for row in panel_b
                if row["route"] == route
                and row["series"] == "action-poor proxy"
            ),
            key=lambda row: float(row["x"]),
        )
        action_growth[route] = (
            len(ratio_rows) == len(expected_sigmas)
            and float(ratio_rows[-1]["y"]) > float(ratio_rows[0]["y"])
        )
    items.append(
        check(
            "panel_b_action_diagnostics",
            len(panel_b) == 4 * len(expected_sigmas)
            and all(float(row["y"]) > 0.0 for row in panel_b)
            and all(action_growth.values()),
            {"rows": len(panel_b), "ratioGrows": action_growth},
            "Panel B has positive two-route proxy values and the screened proxy grows",
        )
    )

    theorem_c = [
        row
        for row in rows
        if row["panel"] == "C" and row["kind"] == "theorem"
    ]
    finite_c = [
        row
        for row in rows
        if row["panel"] == "C" and row["kind"] == "finite diagnostic"
    ]
    c_last = {
        route: float(
            sorted(
                (row for row in finite_c if row["route"] == route),
                key=lambda row: float(row["x"]),
            )[-1]["y"]
        )
        for route in ("producer", "independent")
    }
    items.append(
        check(
            "panel_c_scalar_ceiling",
            len(theorem_c) == 2
            and all(float(row["y"]) == 1.0 for row in theorem_c)
            and len(finite_c) == 2 * len(expected_sigmas)
            and all(0.0 < float(row["y"]) <= 1.0 + 1.0e-12 for row in finite_c)
            and all(value > 0.9 for value in c_last.values()),
            {"theoremRows": len(theorem_c), "lastFinite": c_last},
            "Panel C uses the exact ceiling and both finite routes enter the order-one screen",
        )
    )

    finite_d = [
        row
        for row in rows
        if row["panel"] == "D" and row["kind"] == "finite diagnostic"
    ]
    sqrt_decreases: dict[str, bool] = {}
    for route in ("producer", "independent"):
        sqrt_rows = sorted(
            (
                row
                for row in finite_d
                if row["route"] == route and row["series"] == "C/sqrt sigma"
            ),
            key=lambda row: float(row["x"]),
        )
        sqrt_decreases[route] = (
            len(sqrt_rows) == len(expected_sigmas)
            and float(sqrt_rows[-1]["y"]) < float(sqrt_rows[0]["y"])
        )
    items.append(
        check(
            "panel_d_cubic_diagnostics",
            len(finite_d) == 4 * len(expected_sigmas)
            and all(float(row["y"]) > 0.0 for row in finite_d)
            and all(sqrt_decreases.values()),
            {"rows": len(finite_d), "sqrtNormalizationDecreases": sqrt_decreases},
            "Panel D contains both positive finite normalizations and the square-root ratio decreases",
        )
    )

    role_counts = {
        kind: sum(row["kind"] == kind for row in rows)
        for kind in ("theorem", "finite diagnostic")
    }
    no_fit = (
        results.get("finiteFitsPlotted") is False
        and contract["renderPolicy"]["finiteFit"] == "forbidden"
        and not any("fit" in row["series"].lower() for row in rows)
    )
    items.append(
        check(
            "claim_role_encoding",
            role_counts["theorem"] > 0
            and role_counts["finite diagnostic"] > 0
            and no_fit,
            {"roleCounts": role_counts, "noFiniteFit": no_fit},
            "theorem and finite roles are explicit and no finite fit is plotted",
        )
    )

    changed_sources = [
        relative
        for relative, expected in results["sourceSha256"].items()
        if not (REPOSITORY / relative).is_file()
        or digest(REPOSITORY / relative) != expected
    ]
    changed_outputs = [
        name
        for name, expected in results["outputSha256"].items()
        if not (ROOT / name).is_file() or digest(ROOT / name) != expected
    ]
    items.append(
        check(
            "source_lineage",
            not changed_sources,
            changed_sources,
            "all analytic, certificate, contract, and plotting source hashes retain build lineage",
        )
    )
    items.append(
        check(
            "output_lineage",
            not changed_outputs,
            changed_outputs,
            "all figure outputs retain build hashes",
        )
    )

    publication = config["publication"]
    public_dir = REPOSITORY / publication["directory"]
    identity = {
        suffix: (
            public_dir / f"{publication['stem']}.{suffix}"
        ).is_file()
        and digest(public_dir / f"{publication['stem']}.{suffix}")
        == digest(ROOT / f"figure.{suffix}")
        for suffix in ("pdf", "svg", "png")
    }
    items.append(
        check(
            "public_byte_identity",
            all(identity.values()),
            identity,
            "public masters are byte-identical to archival masters",
        )
    )

    combined = (
        (ROOT / "caption.md").read_text(encoding="utf-8")
        + "\n"
        + str(contract["claimBoundary"])
    ).lower()
    boundary_terms = [
        "finite binary64",
        "do not prove a logarithmic",
        "multi-carrier",
        "general three-dimensional",
    ]
    items.append(
        check(
            "claim_boundary",
            all(term in combined for term in boundary_terms),
            boundary_terms,
            "caption and contract separate theorem, diagnostics, logarithmic conjecture, and Clay problem",
        )
    )

    visual = (
        os.environ.get("R072N_VISUAL_QA_INSPECTED", "").strip().lower()
        == "true"
    )
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
        "figureId": "R0.72N-1",
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
                "# R0.72N figure QA report",
                "",
                f"- Automatic validation: **{'PASS' if all_passed else 'FAIL'}** ({len(items)} checks).",
                f"- Final print size: {pdf_mm[0]:.3f} x {pdf_mm[1]:.3f} mm; PNG {png_size[0]} x {png_size[1]} px at 600 dpi.",
                f"- QA surfaces: {qa_expected[0]} x {qa_expected[1]} px at 180 dpi; grayscale standard deviation {gray_std:.3f}.",
                "- Human inspection: final-size, grayscale, and PDF-raster surfaces checked for legibility, collisions, marker/line distinction, and the locked header blossom."
                if visual
                else "- Human inspection: not declared.",
                "- Claim boundary: rigorous barrier and ceiling are visually distinct from finite routes; the logarithmic cubic normalization remains diagnostic only.",
                f"- Failed checks: {', '.join(failed) if failed else 'none'}.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"status": payload["status"], "checks": len(items), "failed": failed},
            sort_keys=True,
        )
    )
    return 0 if all_passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
