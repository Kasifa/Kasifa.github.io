#!/usr/bin/env python3
"""Validate and seal the R0.74L formal figure package."""

from __future__ import annotations

import csv
import hashlib
import json
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFINFO = BUNDLE / "bin/override/pdfinfo"
PYTHON = BUNDLE / "python/bin/python3"

EXTERNAL_BINDINGS = [
    REPO / "research/r074l_forward_bridge_bv_reduction.md",
    REPO / "research/r074l_main_collar_certificate.json",
    REPO / "research/r074l_main_collar_independent_audit.md",
    REPO / "scripts/r074l_main_collar_certificate.py",
    REPO / "scripts/r074l_main_collar_certificate_independent.rb",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check(check_id: str, passed: bool, note: str) -> dict:
    return {"id": check_id, "note": note, "pass": bool(passed)}


def image_info(path: Path) -> dict:
    with Image.open(path) as image:
        return {
            "dpi": list(image.info.get("dpi", (0, 0))),
            "mode": image.mode,
            "size": [image.width, image.height],
        }


def main() -> None:
    checks: list[dict] = []
    required = [
        "README.md",
        "caption.md",
        "command.txt",
        "config.json",
        "environment.json",
        "figure.pdf",
        "figure.png",
        "figure.svg",
        "plot.py",
        "progress.ndjson",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
        "qa-protocol.md",
        "qa-report.md",
        "requirements.txt",
        "results.json",
        "source-data.csv",
        "validate.py",
    ]
    for name in required:
        checks.append(check(f"exists_{name}", (HERE / name).is_file(), name))

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    checks.append(
        check(
            "claim_boundary",
            config["claim_boundary"] == "PROVED_MAIN_TARGET_COLLAR_ONLY_NOT_CLAY"
            and results["claim_boundary"] == config["claim_boundary"],
            "conservative figure boundary",
        )
    )
    checks.append(check("simulation_false", config["simulation"] is False, "not simulation"))
    checks.append(
        check(
            "output_hashes",
            results["outputs"]["pdf_sha256"] == sha256(HERE / "figure.pdf")
            and results["outputs"]["png_sha256"] == sha256(HERE / "figure.png")
            and results["outputs"]["svg_sha256"] == sha256(HERE / "figure.svg"),
            "results bind all three masters",
        )
    )

    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        rows = {row["item"]: row for row in csv.DictReader(handle)}
    numeric_mismatches = []
    for key, row in rows.items():
        exact = float(Fraction(row["exact_value"]))
        numeric = float(row["numeric_value"])
        tolerance = max(5e-15, 5e-15 * abs(exact))
        if abs(numeric - exact) > tolerance:
            numeric_mismatches.append(
                {
                    "item": key,
                    "exact": exact,
                    "numeric": numeric,
                    "tolerance": tolerance,
                }
            )
    checks.extend(
        [
            check(
                "numeric_columns_match_exact",
                not numeric_mismatches,
                f"all CSV numeric values agree with exact values: {numeric_mismatches}",
            ),
            check(
                "exact_A",
                Fraction(rows["bad_path_exponent_A"]["exact_value"])
                == Fraction(4876875, 1476395008),
                "bad exponent",
            ),
            check(
                "exact_A_minus_rho",
                Fraction(rows["bad_path_reserve_A_minus_rho"]["exact_value"])
                == Fraction(1315703, 7381975040),
                "strict bad-path reserve",
            ),
            check(
                "exact_clock_length",
                Fraction(rows["clock_length_upper"]["exact_value"])
                == Fraction(65, 64),
                "clock interval",
            ),
            check(
                "exact_duration",
                Fraction(rows["component_duration_coefficient"]["exact_value"])
                == Fraction(66560, 189),
                "component physical duration",
            ),
        ]
    )

    good_sum = sum(
        int(rows[key]["exact_value"])
        for key in [
            "good_packet_prefactor",
            "good_inverse_B",
            "good_endpoint_kernel",
            "good_derivative_kernel",
            "good_clock_slice",
        ]
    )
    bad_sum = sum(
        int(rows[key]["exact_value"])
        for key in [
            "bad_packet_prefactor",
            "bad_endpoint_kernel",
            "bad_derivative_kernel",
            "bad_time_window",
            "bad_probability",
        ]
    )
    checks.append(check("good_power_sum", good_sum == 5, "good row R exponent"))
    checks.append(check("bad_power_sum", bad_sum == 5, "bad row R exponent"))

    pdf = subprocess.run(
        [str(PDFINFO), str(HERE / "figure.pdf")],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    checks.extend(
        [
            check("pdf_one_page", "Pages:           1" in pdf, "one vector page"),
            check("pdf_unencrypted", "Encrypted:       no" in pdf, "PDF is open"),
            check("pdf_size", "504.567 x 260.787 pts" in pdf, "178 mm by 92 mm"),
        ]
    )

    master = image_info(HERE / "figure.png")
    final = image_info(HERE / "qa-final-size.png")
    gray = image_info(HERE / "qa-grayscale.png")
    pdf_raster = image_info(HERE / "qa-pdf.png")
    checks.extend(
        [
            check("png_dimensions", master["size"] == [4205, 2174], "600-dpi master"),
            check("png_rgb", master["mode"] == "RGB", "publication color mode"),
            check(
                "png_dpi",
                min(master["dpi"]) >= 599,
                f"metadata dpi={master['dpi']}",
            ),
            check("final_dimensions", final["size"] == [1402, 725], "200-dpi QA"),
            check("gray_mode", gray["mode"] == "L", "grayscale QA"),
            check("pdf_raster_dimensions", pdf_raster["size"] == [2103, 1087], "300-dpi PDF QA"),
        ]
    )

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    plot_source = (HERE / "plot.py").read_text(encoding="utf-8")
    checks.extend(
        [
            check("svg_root", "<svg" in svg and "</svg>" in svg, "valid SVG wrapper"),
            check("svg_vectors", svg.count("<path") + svg.count("<rect") > 10, "vector geometry"),
            check("svg_text", "common forward law" in svg, "semantic title retained"),
            check(
                "displayed_math_contract",
                all(
                    token in svg
                    for token in [
                        "X0 ~ K_T,  T = R^2",
                        "ℬ_j(tau)",
                        "∫ H_R du",
                        "L × R^6 × R^-1 × R^-3 × R^2 × R = L R^5",
                    ]
                )
                and "X0 ~ K_R^2" not in plot_source
                and '"B_j(tau) <= C L R^5"' not in plot_source
                and '"dK_T"' not in plot_source,
                "rendered labels bind the exact proof objects and ledgers",
            ),
        ]
    )

    qa_protocol = (HERE / "qa-protocol.md").read_text(encoding="utf-8")
    qa_report = (HERE / "qa-report.md").read_text(encoding="utf-8")
    checks.append(
        check(
            "manual_visual_gate",
            "Manual status: PASS" in qa_protocol
            and "Manual status: PASS" in qa_report,
            "explicit human visual QA",
        )
    )

    certificate_run = subprocess.run(
        [str(PYTHON), str(REPO / "scripts/r074l_main_collar_certificate.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    certificate = json.loads(certificate_run.stdout)
    checks.append(
        check(
            "finite_certificate",
            certificate["result"] == "PASS"
            and certificate["summary"] == {"passed": 24, "total": 24},
            "24/24 finite checks",
        )
    )

    text_files = [
        path
        for path in HERE.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".md", ".py", ".json", ".csv", ".txt", ".svg"}
    ]
    forbidden = []
    for path in text_files:
        data = path.read_bytes()
        for byte in data:
            if byte < 32 and byte not in (9, 10, 13):
                forbidden.append((path.name, byte))
    checks.append(check("no_forbidden_controls", not forbidden, str(forbidden)))

    passed = sum(1 for item in checks if item["pass"])
    validation = {
        "checks": checks,
        "claim_boundary": "PROVED_MAIN_TARGET_COLLAR_ONLY_NOT_CLAY",
        "figure_id": "fig-r074l-forward-clock-bv",
        "result": "PASS" if passed == len(checks) else "FAIL",
        "summary": {"passed": passed, "total": len(checks)},
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    layout = {
        "final_size_dimensions": final["size"],
        "master_dimensions": master["size"],
        "page_mm": [178, 92],
        "pdf_raster_dimensions": pdf_raster["size"],
        "visual_qa": "PASS",
    }
    (HERE / "layout-bounds.json").write_text(
        json.dumps(layout, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    external = []
    for path in EXTERNAL_BINDINGS:
        external.append(
            {
                "path": str(path.relative_to(REPO)),
                "sha256": sha256(path),
            }
        )
    package_entries = []
    excluded = {"manifest.json", "SHA256SUMS"}
    for path in sorted(HERE.iterdir()):
        if path.is_file() and path.name not in excluded:
            package_entries.append(
                {
                    "bytes": path.stat().st_size,
                    "path": path.name,
                    "sha256": sha256(path),
                }
            )
    manifest = {
        "claim_boundary": "PROVED_MAIN_TARGET_COLLAR_ONLY_NOT_CLAY",
        "entries": package_entries,
        "external_bindings": external,
        "figure_id": "fig-r074l-forward-clock-bv",
        "schema": "r074l-formal-figure-manifest-v1",
        "simulation": False,
        "validation": validation["result"],
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    seal_paths = [
        path
        for path in sorted(HERE.iterdir())
        if path.is_file() and path.name != "SHA256SUMS"
    ]
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in seal_paths),
        encoding="utf-8",
    )

    print(
        f"verify-only {validation['result']} "
        f"{passed}/{len(checks)}; {len(package_entries)} package entries"
    )
    if validation["result"] != "PASS":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
