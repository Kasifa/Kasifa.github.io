#!/usr/bin/env python3
"""Validate and seal the R0.74M nearest-inward formal figure package."""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import re
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFINFO = BUNDLE / "bin/override/pdfinfo"
PYTHON = BUNDLE / "python/bin/python3"
CLAIM = "PROVED_IN_SOURCE_ANALYTIC_AUDIT_PASS_NOT_CLAY"
FIGURE_ID = "fig-r074m-nearest-inward-expulsion"

EXTERNAL_BINDINGS = [
    REPO / "research/r074m_problem_freeze.md",
    REPO / "research/r074m_final_segment_expulsion.md",
    REPO / "research/r074m_nearest_inward_certificate.json",
    REPO / "research/r074m_nearest_inward_independent_audit.md",
    REPO / "scripts/r074m_nearest_inward_certificate.py",
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
        "README.md", "caption.md", "command.txt", "config.json", "environment.json",
        "figure.pdf", "figure.png", "figure.svg", "plot.py", "progress.ndjson",
        "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-svg-quicklook.png", "qa-protocol.md",
        "qa-report.md", "requirements.txt", "results.json", "source-data.csv", "validate.py",
    ]
    for name in required:
        checks.append(check(f"exists_{name}", (HERE / name).is_file(), name))

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    checks.extend([
        check("claim_boundary", config["claim_boundary"] == CLAIM
              and results["claim_boundary"] == CLAIM
              and config["analytic_proof_audit"] == "PASS"
              and results["analytic_proof_audit"] == "PASS"
              and config["figure_package_independent_audit"] == "EXTERNAL_SEPARATE_NOT_CLAIMED"
              and results["figure_package_independent_audit"] == "EXTERNAL_SEPARATE_NOT_CLAIMED",
              "analytic proof audit PASS; independent figure-package audit separate; not Clay"),
        check("simulation_false", config["simulation"] is False
              and results["simulation"] is False, "deterministic analytic schematic"),
        check("output_hashes", results["outputs"]["pdf_sha256"] == sha256(HERE / "figure.pdf")
              and results["outputs"]["png_sha256"] == sha256(HERE / "figure.png")
              and results["outputs"]["svg_sha256"] == sha256(HERE / "figure.svg"),
              "results bind all publication masters"),
    ])

    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        rows = {row["item"]: row for row in csv.DictReader(handle)}
    mismatches = []
    for key, row in rows.items():
        exact = float(Fraction(row["exact_value"]))
        numeric = float(row["numeric_value"])
        tolerance = max(5e-15, 5e-15 * abs(exact))
        if abs(exact - numeric) > tolerance:
            mismatches.append({"item": key, "exact": exact, "numeric": numeric})
    checks.extend([
        check("numeric_columns_match_exact", not mismatches, str(mismatches)),
        check("geometry_identity",
              Fraction(3, 5) - Fraction(32, 63) - Fraction(1, 16) == Fraction(149, 5040)
              == Fraction(rows["geometry_gap"]["exact_value"]), "exact vertical room"),
        check("bad_event_reserve",
              Fraction(1, 16) - Fraction(1, 320) - Fraction(2, 1323)
              == Fraction(24497, 423360)
              == Fraction(rows["bad_event_reserve"]["exact_value"]),
              "fast-return exponent pays R and Gamma ratio"),
        check("expulsion_gap",
              Fraction(rows["radius_exponent_rho"]["exact_value"])
              - Fraction(rows["defect_exponent"]["exact_value"]) == Fraction(1, 640),
              "Sigma is asymptotically larger than LR"),
        check("scale_ledgers",
              Fraction(rows["raw_bad_R_power"]["exact_value"]) == 4
              and Fraction(rows["raw_good_R_power"]["exact_value"]) == 3
              and Fraction(rows["target_R_power"]["exact_value"]) == 5,
              "raw bad/good and target R powers"),
    ])

    pdf_text = subprocess.run([str(PDFINFO), str(HERE / "figure.pdf")], check=True,
                              capture_output=True, text=True).stdout
    checks.extend([
        check("pdf_metadata",
              "Title:           R0.74M nearest-inward final-segment expulsion" in pdf_text
              and "Author:          C. K. Zeng" in pdf_text
              and "Subject:         Analytic proof audit PASS; figure-package independent audit reported separately; not simulation; NOT CLAY" in pdf_text,
              "PDF metadata preserves analytic-audit and separate figure-audit boundary"),
        check("pdf_one_page", "Pages:           1" in pdf_text, "one vector page"),
        check("pdf_unencrypted", "Encrypted:       no" in pdf_text, "PDF is open"),
        check("pdf_size", "504.567 x 283.465 pts" in pdf_text, "178 mm by 100 mm"),
    ])

    master = image_info(HERE / "figure.png")
    final = image_info(HERE / "qa-final-size.png")
    gray = image_info(HERE / "qa-grayscale.png")
    pdf_raster = image_info(HERE / "qa-pdf.png")
    svg_quicklook = image_info(HERE / "qa-svg-quicklook.png")
    checks.extend([
        check("png_dimensions", master["size"] == [4205, 2363], "600-dpi master"),
        check("png_rgb", master["mode"] == "RGB", "publication color mode"),
        check("png_dpi", min(master["dpi"]) >= 599, f"metadata dpi={master['dpi']}"),
        check("final_dimensions", final["size"] == [1402, 788], "200-dpi QA"),
        check("gray_mode", gray["mode"] == "L", "grayscale QA"),
        check("pdf_raster_dimensions", pdf_raster["size"] == [2103, 1182],
              "300-dpi PDF QA"),
        check("svg_quicklook_raster", svg_quicklook["mode"] == "RGB"
              and svg_quicklook["size"] == [2103, 2103],
              f"macOS Quick Look SVG QA size={svg_quicklook['size']}"),
    ])

    svg = (HERE / "figure.svg").read_text(encoding="utf-8")
    plot_source = (HERE / "plot.py").read_text(encoding="utf-8")
    semantic_tokens = [
        "endpoint in A_{j-1}", "t - R^2/64", "LR/16", "exp(-L^2/640) / 32768",
        "dist_T(u,0) &gt;= Sigma_L/2", "4 exp(-L^2/16)",
        "+32LR/63 + R/8", "PROVED IN SOURCE", "ANALYTIC AUDIT PASS", "NOT CLAY",
    ]
    font_payloads = re.findall(r"data:font/ttf;base64,([A-Za-z0-9+/=]+)", svg)
    font_payload_sizes = []
    for payload in font_payloads:
        try:
            font_payload_sizes.append(len(base64.b64decode(payload, validate=True)))
        except ValueError:
            font_payload_sizes.append(0)
    checks.extend([
        check("svg_root", "<svg" in svg and "</svg>" in svg, "valid SVG wrapper"),
        check("svg_vectors", svg.count("<path") + svg.count("<rect") > 20,
              "sufficient vector geometry"),
        check("svg_semantics", all(token in svg for token in semantic_tokens),
              "rendered labels retain the exact mechanism and status"),
        check("svg_embedded_fonts", svg.count("@font-face") == 2
              and svg.count("data:font/ttf;base64,") == 2
              and "font-family: 'R074M-Regular'" in svg
              and "font-family: 'R074M-Bold'" in svg
              and "font-weight: 400" in svg and "font-weight: 700" in svg
              and len(font_payload_sizes) == 2 and min(font_payload_sizes) > 600000
              and len(svg.encode("utf-8")) > 1800000,
              f"two embedded DejaVu TTF payloads, decoded bytes={font_payload_sizes}"),
        check("schematic_not_simulated", "analytic event; curve is schematic" in svg
              and "random" not in plot_source.lower() and "numpy" not in plot_source.lower(),
              "no sampled stochastic path"),
    ])

    qa_protocol = (HERE / "qa-protocol.md").read_text(encoding="utf-8")
    qa_report = (HERE / "qa-report.md").read_text(encoding="utf-8")
    checks.append(check("manual_visual_gate", "Manual status: PASS" in qa_protocol
                        and "Manual status: PASS" in qa_report
                        and "Quick Look" in qa_protocol and "Quick Look" in qa_report
                        and "not an independent figure-package audit" in qa_protocol
                        and "not an independent figure-package audit" in qa_report,
                        "explicit internal visual QA including Quick Look; no independent-audit claim"))

    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    caption_tokens = [r"\to\infty", r"\ge", r"\mathbb P", r"\le",
                      "1/(8L)", "149/5040", "independent analytic audit with result PASS"]
    checks.append(check("caption_latex_and_padding",
                        all(token in caption for token in caption_tokens)
                        and "\t" not in caption,
                        "LaTeX commands intact and R/8 padding stated"))

    certificate_run = subprocess.run(
        [str(PYTHON), str(REPO / "scripts/r074m_nearest_inward_certificate.py")],
        check=True, capture_output=True, text=True)
    certificate = json.loads(certificate_run.stdout)
    checks.append(check("finite_certificate", certificate["result"] == "PASS"
                        and certificate["summary"] == {"passed": 38, "total": 38},
                        "38/38 finite certificate; analytic audit bound separately"))

    external_exist = all(path.is_file() for path in EXTERNAL_BINDINGS)
    checks.append(check("external_bindings_exist", external_exist,
                        "problem freeze, proof source, certificate, independent analytic audit, and generator"))

    text_files = [path for path in HERE.iterdir() if path.is_file()
                  and path.suffix.lower() in {".md", ".py", ".json", ".csv", ".txt", ".svg"}]
    forbidden = []
    for path in text_files:
        for byte in path.read_bytes():
            if byte < 32 and byte not in (10, 13):
                forbidden.append((path.name, byte))
    checks.append(check("no_forbidden_controls", not forbidden, str(forbidden)))

    passed = sum(1 for item in checks if item["pass"])
    validation = {
        "analytic_proof_audit": "PASS",
        "checks": checks,
        "claim_boundary": CLAIM,
        "figure_id": FIGURE_ID,
        "figure_package_independent_audit": "EXTERNAL_SEPARATE_NOT_CLAIMED",
        "result": "PASS" if passed == len(checks) else "FAIL",
        "summary": {"passed": passed, "total": len(checks)},
    }
    (HERE / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n",
                                           encoding="utf-8")
    layout = {
        "final_size_dimensions": final["size"],
        "master_dimensions": master["size"],
        "page_mm": [178, 100],
        "pdf_raster_dimensions": pdf_raster["size"],
        "visual_qa": "PASS" if next(item for item in checks
                                      if item["id"] == "manual_visual_gate")["pass"]
        else "PENDING_OR_FAIL",
    }
    (HERE / "layout-bounds.json").write_text(json.dumps(layout, indent=2, sort_keys=True) + "\n",
                                              encoding="utf-8")

    external = [{"path": str(path.relative_to(REPO)), "sha256": sha256(path)}
                for path in EXTERNAL_BINDINGS if path.is_file()]
    excluded = {"manifest.json", "SHA256SUMS"}
    entries = [{"bytes": path.stat().st_size, "path": path.name, "sha256": sha256(path)}
               for path in sorted(HERE.iterdir()) if path.is_file() and path.name not in excluded]
    manifest = {
        "analytic_proof_audit": "PASS",
        "claim_boundary": CLAIM,
        "entries": entries,
        "external_bindings": external,
        "figure_id": FIGURE_ID,
        "figure_package_independent_audit": "EXTERNAL_SEPARATE_NOT_CLAIMED",
        "schema": "r074m-formal-figure-manifest-v1",
        "simulation": False,
        "validation": validation["result"],
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                         encoding="utf-8")

    seal_paths = [path for path in sorted(HERE.iterdir())
                  if path.is_file() and path.name != "SHA256SUMS"]
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(path)}  {path.name}\n" for path in seal_paths), encoding="utf-8")

    print(f"verify-only {validation['result']} {passed}/{len(checks)}; {len(entries)} package entries")
    if validation["result"] != "PASS":
        failed = [item["id"] for item in checks if not item["pass"]]
        print("failed:", ", ".join(failed))
        raise SystemExit(1)


if __name__ == "__main__":
    main()
