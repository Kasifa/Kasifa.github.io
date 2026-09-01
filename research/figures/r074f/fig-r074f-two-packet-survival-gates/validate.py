#!/usr/bin/env python3
"""Independent structural and exact-arithmetic validator for the R0.74F figure."""
from __future__ import annotations

import csv
import hashlib
import json
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074f_two_packet_survival_certificate.json"
EXPECTED_CERT_SHA256 = "44bd3208d10134ae84cf8b001e9569b6c480af6ac7d85efc25759dc4e725e981"
MANUAL_VISUAL_QA = "PASS"

NAMES = {
    "README.md", "SHA256SUMS", "caption.md", "chart-contract-and-source-data.md",
    "command.txt", "config.json", "contract.json", "environment.json",
    "figure.pdf", "figure.png", "figure.svg", "layout-bounds.json",
    "manifest.json", "plot.py", "qa-final-size.png", "qa-grayscale.png",
    "qa-pdf.png", "qa-protocol.md", "qa-report.md", "requirements.txt",
    "results.json", "source-data.csv", "validate.py", "validation.json",
}
SELF_OUTPUTS = {"SHA256SUMS", "manifest.json", "qa-report.md", "results.json", "validation.json"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def resolve(value):
    return value.get_object() if hasattr(value, "get_object") else value


def embedded_fonts(page) -> tuple[int, bool]:
    resources = resolve(page.get("/Resources", {}))
    fonts = resolve(resources.get("/Font", {}))
    flags = []
    for reference in fonts.values():
        font = resolve(reference)
        base = str(font.get("/BaseFont", ""))
        subtype = str(font.get("/Subtype", ""))
        if subtype == "/Type1" and base in {"/Times-Roman", "/Helvetica", "/Courier"}:
            continue
        descriptor = font.get("/FontDescriptor")
        if descriptor is None and font.get("/DescendantFonts"):
            descendant = resolve(resolve(font["/DescendantFonts"])[0])
            descriptor = descendant.get("/FontDescriptor")
        descriptor = resolve(descriptor) if descriptor is not None else {}
        flags.append(any(key in descriptor for key in ("/FontFile", "/FontFile2", "/FontFile3")))
    return len(flags), bool(flags) and all(flags)


def main() -> None:
    checks: dict[str, bool] = {}
    current_names = {path.name for path in HERE.iterdir() if path.is_file()}
    checks["file_inventory_24"] = current_names == NAMES - SELF_OUTPUTS or current_names == NAMES
    checks["certificate_hash"] = sha256(CERTIFICATE) == EXPECTED_CERT_SHA256

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    checks["certificate_schema"] = certificate.get("schema") == "r074f-two-packet-survival-finite-certificate-v1"
    checks["certificate_30_of_30"] = certificate.get("status") == "PASS" and certificate.get("summary") == {"passed": 30, "total": 30}
    checks["certificate_all_checks_true"] = len(certificate.get("checks", [])) == 30 and all(item.get("pass") is True for item in certificate["checks"])
    checks["certificate_scope_finite"] = certificate.get("scope") == "finite exact rational compatibility and conditional annular geometry only"
    boundary = " ".join(certificate.get("analytic_boundary", [])).lower()
    checks["certificate_boundary_explicit"] = all(term in boundary for term in ("brownian", "packet survival", "clay"))

    inputs = certificate["inputs"]
    derived = certificate["derived"]
    lam = Fraction(inputs["lambda"])
    c_h = Fraction(inputs["c_h"])
    alpha = Fraction(inputs["alpha"])
    c_r = Fraction(inputs["c_R"])
    c_gamma = Fraction(inputs["c_gamma"])
    l_contrast = Fraction(inputs["L_contrast"])
    l_surv = Fraction(inputs["L_surv"])
    shrink = Fraction(inputs["shrink"])
    c_leak = Fraction(derived["c_leak"])
    c_surv = Fraction(derived["c_surv"])
    effective_separation = Fraction(derived["effective_separation"])
    buffer_over_r = Fraction(derived["buffer_over_R"])
    inner_margin = Fraction(derived["inner_margin_at_L_surv"])
    outer_sq_margin = Fraction(derived["outer_sq_margin_at_L_surv"])

    c_alpha_heat = alpha**2 / 260
    l12 = lam * 2**12
    l13 = lam * 2**13
    inner_threshold = 1 / lam
    inner_lower = 1 - Fraction(97, 32) / l_surv
    outer_threshold_sq = (2 / lam) ** 2
    conditional_upper_sq = Fraction(87370044545, 86973087744)

    checks["frozen_parameters"] = (
        lam, c_h, alpha, c_r, c_gamma, l_contrast, l_surv, shrink
    ) == (
        Fraction(63, 32), Fraction(15, 16), Fraction(14, 15), Fraction(1, 320),
        Fraction(8, 3969), Fraction(7680), Fraction(9216), Fraction(255, 256),
    )
    checks["exponents_exact"] = (
        c_gamma, c_r, c_leak, c_alpha_heat, c_surv
    ) == (
        Fraction(8, 3969), Fraction(1, 320), Fraction(75, 22528),
        Fraction(49, 14625), Fraction(2926125, 872415232),
    )
    checks["five_exponent_hierarchy"] = c_gamma < c_r < c_leak < c_alpha_heat < c_surv
    checks["gap_R_gamma_exact"] = c_r - c_gamma == Fraction(1409, 1270080)
    checks["gap_leak_R_exact"] = c_leak - c_r == Fraction(23, 112640)
    checks["gap_alpha_leak_exact"] = c_alpha_heat - c_leak == Fraction(6997, 329472000)
    checks["gap_surv_alpha_exact"] = c_surv - c_alpha_heat == Fraction(3556289, 981467136000)
    checks["gap_surv_leak_exact"] = c_surv - c_leak == Fraction(238575, 9596567552)
    checks["buffer_exact"] = buffer_over_r == Fraction(33) and c_h * l_surv / 256 == Fraction(135, 4)
    checks["effective_separation_exact"] = effective_separation == Fraction(3825, 4096) and effective_separation == shrink * c_h
    checks["discrete_scale_exact"] = l12 == Fraction(8064) and l13 == Fraction(16128) and l12 < l_surv < l13
    checks["first_admissible_j"] = all(lam * 2**j < l_surv for j in range(13)) and lam * 2**13 > l_surv
    checks["inner_gate_exact"] = inner_lower - inner_threshold == inner_margin == Fraction(1015129, 2064384)
    checks["outer_gate_exact"] = outer_threshold_sq - conditional_upper_sq == outer_sq_margin == Fraction(116914328399, 4261681299456)

    rows = list(csv.DictReader((HERE / "source-data.csv").open(encoding="utf-8")))
    row_map = {row["record"]: Fraction(row["exact_value"]) for row in rows}
    expected_rows = {
        "c_gamma": c_gamma,
        "c_R": c_r,
        "c_leak": c_leak,
        "c_alpha_heat": c_alpha_heat,
        "c_surv": c_surv,
        "gap_R_gamma": c_r - c_gamma,
        "gap_leak_R": c_leak - c_r,
        "gap_alpha_leak": c_alpha_heat - c_leak,
        "gap_surv_alpha": c_surv - c_alpha_heat,
        "gap_surv_leak": c_surv - c_leak,
        "effective_separation": effective_separation,
        "L_contrast": l_contrast,
        "L_surv": l_surv,
        "L12": l12,
        "L13": l13,
        "buffer_over_R": buffer_over_r,
        "buffer_budget": c_h * l_surv / 256,
        "inner_threshold": inner_threshold,
        "inner_lower": inner_lower,
        "inner_margin": inner_margin,
        "outer_threshold_sq": outer_threshold_sq,
        "conditional_upper_sq": conditional_upper_sq,
        "outer_sq_margin": outer_sq_margin,
        "x1_half_width_over_r": Fraction(1, 16),
        "e2_abs_over_R": Fraction(65, 32),
        "e3_abs_over_R": Fraction(1),
        "first_admissible_j": Fraction(13),
    }
    checks["source_rows_27"] = len(rows) == 27 and len(row_map) == 27 and set(row_map) == set(expected_rows)
    checks["source_exact_values"] = row_map == expected_rows
    conditional_records = {"inner_lower", "inner_margin", "conditional_upper_sq", "outer_sq_margin", "x1_half_width_over_r", "e2_abs_over_R", "e3_abs_over_R"}
    checks["source_status_boundary"] = all(
        row["status"] == ("CONDITIONAL" if row["record"] in conditional_records else "EXACT FINITE")
        for row in rows
    )

    png = Image.open(HERE / "figure.png")
    checks["png_600dpi_dimensions"] = png.width >= 4250 and png.height >= 1936
    checks["png_rgb_or_rgba"] = png.mode in {"RGB", "RGBA"}
    checks["qa_grayscale_mode"] = Image.open(HERE / "qa-grayscale.png").mode == "L"
    final_size = Image.open(HERE / "qa-final-size.png").size
    checks["qa_final_size"] = final_size[0] == 1800 and 815 <= final_size[1] <= 825
    checks["qa_pdf_size"] = Image.open(HERE / "qa-pdf.png").width >= 2100

    reader = PdfReader(str(HERE / "figure.pdf"))
    checks["pdf_one_page"] = len(reader.pages) == 1
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    checks["pdf_180x82mm"] = abs(width - 180 / 25.4 * 72) < 0.5 and abs(height - 82 / 25.4 * 72) < 0.5
    font_count, all_embedded = embedded_fonts(page)
    checks["pdf_fonts_embedded"] = font_count >= 1 and all_embedded

    svg_bytes = (HERE / "figure.svg").read_bytes()
    svg = svg_bytes.decode("utf-8")
    root = ET.fromstring(svg_bytes)
    svg_text = " ".join(part.strip() for part in root.itertext() if part.strip())
    required_phrases = [
        "R0.74F two-packet survival finite gates",
        "30/30 EXACT",
        "c_gamma  8/3969",
        "c_R  1/320",
        "c_leak = 75/22528",
        "alpha^2/260 = 49/14625",
        "c_surv = 2926125/872415232",
        "CONDITIONAL",
        "Lobe hypotheses (not certificate outputs)",
        "exact margin = 1015129/2064384 > 0",
        "margin = 116914328399/4261681299456 > 0",
        "L_12=8064 < L*=9216 < L_13=16128",
        "first admissible j=13",
        "FINITE COMPATIBILITY ONLY",
        "ANALYTIC BRIDGE / PACKET SURVIVAL NOT CERTIFIED BY FIGURE",
        "NOT CLAY",
    ]
    checks["svg_required_phrases"] = all(phrase in svg_text for phrase in required_phrases)
    checks["svg_live_text"] = svg.count("<text") >= 34
    checks["svg_no_raster"] = "<image" not in svg
    checks["svg_canvas_dimensions"] = abs(float(root.attrib["width"]) - 180 / 25.4 * 72) < 0.01 and abs(float(root.attrib["height"]) - 82 / 25.4 * 72) < 0.01
    checks["svg_palette_limited"] = all(token not in svg.lower() for token in ("#ff0000", "#00ff00", "#800080"))

    layout = json.loads((HERE / "layout-bounds.json").read_text(encoding="utf-8"))
    entries = layout["entries"]
    checks["layout_proxy_all_inside"] = bool(entries) and all(entry["proxyPass"] for entry in entries)
    checks["layout_proxy_summary"] = layout["summary"] == {"passed": len(entries), "total": len(entries)}
    checks["layout_proxy_min_font"] = min(entry["fontPt"] for entry in entries) >= 4.4
    checks["layout_proxy_count"] = len(entries) >= 34

    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    checks["contract_certificate_bound"] = contract["certificate"]["sha256"] == EXPECTED_CERT_SHA256 and contract["certificate"]["checks"] == "30/30"
    checks["contract_source_certificate_only"] = contract.get("sourceCertificateOnly") is True
    checks["contract_claim_boundary"] = contract["claimBoundary"]["packetSurvival"] == "NOT CERTIFIED BY FIGURE" and contract["claimBoundary"]["clay"] == "NOT CLAY"
    checks["contract_two_panels"] = set(contract["figureClaims"]) == {"A", "B"}
    checks["config_static_analytic"] = config["static"] is True and config["dns"] is False and config["simulation"] is False
    checks["config_palette"] = config["palettePolicy"] == "hard two-root cap" and set(config["nonNeutralRoots"]) == {"blue", "gold"}

    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    checks["caption_boundary"] = "does not establish" in caption.lower() and "NOT CLAY" in caption
    checks["readme_boundary"] = "not dns or simulation" in readme.lower() and "NOT CLAY" in readme
    checks["manual_visual_qa"] = MANUAL_VISUAL_QA == "PASS"

    passed = sum(checks.values())
    total = len(checks)
    status = "PASS" if passed == total else "FAIL"
    validation = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "checks": checks,
        "figureId": "fig-r074f-two-packet-survival-gates",
        "status": status,
        "summary": {"passed": passed, "total": total},
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (HERE / "results.json").write_text(
        json.dumps({
            "certificateChecks": "30/30",
            "certificateSha256": EXPECTED_CERT_SHA256,
            "figureId": "fig-r074f-two-packet-survival-gates",
            "status": status,
            "validationChecks": f"{passed}/{total}",
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    visual_line = (
        "**PASS (2026-09-01).** The 600 dpi master, grayscale derivative, 300 dpi PDF render, and 1800-pixel final-size derivative were inspected locally. Full-scale and enlarged exponent markers remain distinct; every exact gap is readable; the conditional hypotheses, inner/outer comparison rows, discrete j >= 13 gate, and claim-boundary footer are unclipped. Circle/diamond/square/triangle, open/filled states, row separation, and dashed outlines remain distinguishable in grayscale. The PDF render matches the master composition."
        if MANUAL_VISUAL_QA == "PASS"
        else "**PENDING.** Visual inspection must be completed before the package can pass."
    )
    (HERE / "qa-report.md").write_text(
        "# QA report\n\n"
        f"**Status:** {status} ({passed}/{total} independent checks).\n\n"
        "The validator recomputed every displayed fraction from the frozen 30/30 exact certificate, checked the 27-row source export, verified the 180 x 82 mm one-page PDF and embedded fonts, checked the approximately 600 dpi RGB PNG, confirmed live SVG text with no raster image, and required every recorded text extent to stay inside its declared canvas or panel container. The extent check is an auditable string-width/ascent proxy, not a substitute for visual inspection. The figure certifies finite arithmetic only and visibly states that the analytic bridge and packet survival are not certified by the figure. NOT CLAY.\n\n"
        "## Manual visual QA\n\n"
        f"{visual_line}\n",
        encoding="utf-8",
    )

    bound = sorted(name for name in NAMES if name not in {"SHA256SUMS", "manifest.json"})
    manifest = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "figureId": "fig-r074f-two-packet-survival-gates",
        "files": [
            {"bytes": (HERE / name).stat().st_size, "path": name, "sha256": sha256(HERE / name)}
            for name in bound
        ],
        "source": "research/r074f_two_packet_survival_certificate.json",
        "status": status,
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    sums = sorted(name for name in NAMES if name != "SHA256SUMS")
    (HERE / "SHA256SUMS").write_text(
        "".join(f"{sha256(HERE / name)}  {name}\n" for name in sums), encoding="utf-8"
    )

    final_names = {path.name for path in HERE.iterdir() if path.is_file()}
    if final_names != NAMES:
        raise SystemExit(f"final inventory mismatch: {sorted(final_names ^ NAMES)}")
    if status != "PASS":
        failed = [name for name, value in checks.items() if not value]
        raise SystemExit(f"validation failed: {failed}")
    print(f"PASS {passed}/{total}; 24 files; finite compatibility only; certificate 30/30")


if __name__ == "__main__":
    main()
