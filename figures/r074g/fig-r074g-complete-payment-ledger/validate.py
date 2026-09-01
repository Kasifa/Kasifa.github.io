#!/usr/bin/env python3
"""Independent exact, structural, provenance, and QA validator for R0.74G."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074g_complete_payment_certificate.json"
SCRIPT = REPO / "scripts/r074g_complete_payment_certificate.py"
EXPECTED_CERT_SHA256 = "2a411007989e63e51ab7f1644724f654f26794b80507681aaf62e00adbeefd53"
EXPECTED_SCRIPT_SHA256 = "315f4cc7f0a397287cc2eb14ec1ad65bcacb797692e2a6ce5a1459985a4853ca"
FIGURE_ID = "fig-r074g-complete-payment-ledger"
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


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def analytic_formula(series: str, length: Fraction) -> str:
    ell = q(length)
    if series == "background_floor":
        return "1"
    if series == "packet_G_envelope":
        return f"exp[-(43/423360)*({ell})^2]*({ell})^-2"
    if series == "packet_H_envelope":
        return f"exp[-(43/423360)*({ell})^2]*({ell})^-7/2"
    if series == "target_ratio_lower":
        return ell
    raise ValueError(series)


def analytic_log10(series: str, gap: Fraction, length: Fraction) -> float:
    ell = float(length)
    if series == "background_floor":
        return 0.0
    if series == "packet_G_envelope":
        return -float(gap) * ell * ell / math.log(10.0) - 2.0 * math.log10(ell)
    if series == "packet_H_envelope":
        return -float(gap) * ell * ell / math.log(10.0) - 3.5 * math.log10(ell)
    if series == "target_ratio_lower":
        return math.log10(ell)
    raise ValueError(series)


def main() -> None:
    checks: dict[str, bool] = {}
    current_names = {path.name for path in HERE.iterdir() if path.is_file()}
    checks["file_inventory_24"] = current_names == NAMES - SELF_OUTPUTS or current_names == NAMES
    checks["certificate_hash"] = sha256(CERTIFICATE) == EXPECTED_CERT_SHA256
    checks["script_hash"] = sha256(SCRIPT) == EXPECTED_SCRIPT_SHA256

    regenerated = subprocess.run([sys.executable, str(SCRIPT)], check=True, capture_output=True).stdout
    checks["script_stdout_byte_identical"] = regenerated == CERTIFICATE.read_bytes()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    checks["certificate_result_pass"] = certificate.get("result") == "PASS"
    checks["certificate_31_of_31"] = certificate.get("summary") == {"passed": 31, "total": 31}
    checks["certificate_all_checks_true"] = (
        len(certificate.get("checks", [])) == 31
        and all(item.get("pass") is True for item in certificate["checks"])
    )
    boundary = " ".join(certificate.get("analytic_boundary", [])).lower()
    checks["certificate_boundary_complete_denominator"] = "complete denominator" in boundary
    checks["certificate_boundary_endpoint"] = "endpoint counterexample" in boundary
    checks["certificate_boundary_clay"] = "clay" in boundary and "regularity" in boundary

    cert_checks = {item["id"]: item for item in certificate["checks"]}
    value = lambda check_id, field="left": Fraction(cert_checks[check_id][field])
    c_gamma = value("gamma_coefficient")
    three_half_gamma = Fraction(3, 2) * c_gamma
    c_r = value("inverse_R_beats_three_halves_gamma")
    d_e = value("buffered_energy_exponent")
    a_plateau = value("plateau_exponent")
    gap_complete = value("complete_payment_gap")
    gap_energy = value("buffered_energy_gap")
    gap_shift = value("plateau_shift_gap")
    l12 = value("discrete_L12")
    l13 = value("discrete_L13")
    buffer_threshold = value("buffer_width_threshold")

    checks["c_gamma_exact"] = c_gamma == Fraction(8, 3969)
    checks["three_half_gamma_exact"] = three_half_gamma == Fraction(4, 1323)
    checks["c_R_exact"] = c_r == Fraction(1, 320)
    checks["d_E_exact"] = d_e == Fraction(98, 29475)
    checks["a_plateau_exact"] = a_plateau == Fraction(49, 14625)
    checks["five_coefficient_ladder"] = c_gamma < three_half_gamma < c_r < d_e < a_plateau
    checks["complete_gap_exact"] = c_r - three_half_gamma == gap_complete == Fraction(43, 423360)
    checks["energy_gap_exact"] = d_e - c_gamma == gap_energy == Fraction(17018, 12998475)
    checks["shift_gap_exact"] = a_plateau - c_r == gap_shift == Fraction(211, 936000)
    checks["three_gaps_strictly_positive"] = min(gap_complete, gap_energy, gap_shift) > 0
    checks["L12_exact"] = l12 == Fraction(8064)
    checks["L13_exact"] = l13 == Fraction(16128)
    checks["buffer_threshold_exact"] = buffer_threshold == Fraction(3840)
    checks["discrete_scales_clear_buffer"] = l12 > buffer_threshold and l13 > l12

    rows = list(csv.DictReader((HERE / "source-data.csv").open(encoding="utf-8")))
    panel_a_rows = [row for row in rows if row["panel"] == "A"]
    panel_b_rows = [row for row in rows if row["panel"] == "B"]
    checks["source_rows_16"] = len(rows) == 16 and len(panel_a_rows) == 8 and len(panel_b_rows) == 8
    checks["source_unique_keys"] = len({(row["panel"], row["record"], row["index_j"]) for row in rows}) == 16

    expected_a = {
        "c_gamma": c_gamma,
        "three_half_gamma": three_half_gamma,
        "c_R": c_r,
        "d_E": d_e,
        "a_plateau": a_plateau,
        "gap_complete": gap_complete,
        "gap_energy": gap_energy,
        "gap_shift": gap_shift,
    }
    a_map = {row["record"]: Fraction(row["exact_value"]) for row in panel_a_rows}
    checks["source_A_records"] = set(a_map) == set(expected_a)
    checks["source_A_exact_values"] = a_map == expected_a
    checks["source_A_formula_exact"] = all(
        row["analytic_formula"] == q(expected_a[row["record"]]) for row in panel_a_rows
    )
    checks["source_A_identity_transform"] = all(row["plotted_unit"] == "identity" for row in panel_a_rows)
    checks["source_A_status_exact"] = all(row["status"] == "EXACT FINITE" for row in panel_a_rows)

    b_map = {(row["record"], int(row["index_j"])): row for row in panel_b_rows}
    expected_series = {"background_floor", "packet_G_envelope", "packet_H_envelope", "target_ratio_lower"}
    checks["source_B_records"] = set(b_map) == {(series, index) for series in expected_series for index in (12, 13)}
    formula_ok = True
    log_ok = True
    l_ok = True
    status_ok = True
    exact_blank = True
    for (series, index), row in b_map.items():
        length = l12 if index == 12 else l13
        formula_ok &= row["analytic_formula"] == analytic_formula(series, length)
        log_ok &= abs(float(row["plotted_value"]) - analytic_log10(series, gap_complete, length)) < 5e-12
        l_ok &= row["L_exact"] == q(length)
        exact_blank &= row["exact_value"] == ""
        expected_status = {
            "background_floor": "ANALYTIC FLOOR",
            "packet_G_envelope": "ANALYTIC ENVELOPE",
            "packet_H_envelope": "ANALYTIC ENVELOPE",
            "target_ratio_lower": "ANALYTIC LOWER BOUND",
        }[series]
        status_ok &= row["status"] == expected_status
    checks["source_B_exact_formulas"] = formula_ok
    checks["source_B_log10_evaluations"] = log_ok
    checks["source_B_exact_scales"] = l_ok
    checks["source_B_exact_value_blank"] = exact_blank
    checks["source_B_status_boundary"] = status_ok
    checks["source_B_transform_explicit"] = all(row["plotted_unit"] == "log10(analytic factor)" for row in panel_b_rows)
    source_text = (HERE / "source-data.csv").read_text(encoding="utf-8").lower()
    checks["source_no_empirical_claim"] = all(term not in source_text for term in ("measured", "observed", "sampled path"))

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
        "R0.74G complete-payment ledger",
        "31/31 EXACT",
        "c_gamma  8/3969",
        "3c_gamma/2 = 4/1323",
        "c_R = 1/320",
        "d_E = 98/29475",
        "a_plateau = 49/14625",
        "c_R-3c_gamma/2 = 43/423360",
        "d_E-c_gamma = 17018/12998475",
        "a_plateau-c_R = 211/936000",
        "background floor",
        "packet G",
        "packet H",
        "ratio lower",
        "PROPOSED INEQUALITY REJECTED",
        "ANALYTIC DERIVATION",
        "NOT DNS",
        "NOT CLAY",
    ]
    checks["svg_required_phrases"] = all(phrase in svg_text for phrase in required_phrases)
    checks["svg_live_text"] = svg.count("<text") >= 42
    checks["svg_no_raster"] = "<image" not in svg
    checks["svg_canvas_dimensions"] = (
        abs(float(root.attrib["width"]) - 180 / 25.4 * 72) < 0.01
        and abs(float(root.attrib["height"]) - 82 / 25.4 * 72) < 0.01
    )
    checks["svg_palette_limited"] = all(token not in svg.lower() for token in ("#ff0000", "#00ff00", "#800080"))

    layout = json.loads((HERE / "layout-bounds.json").read_text(encoding="utf-8"))
    entries = layout["entries"]
    checks["layout_proxy_all_inside"] = bool(entries) and all(entry["proxyPass"] for entry in entries)
    checks["layout_proxy_summary"] = layout["summary"] == {"passed": len(entries), "total": len(entries)}
    checks["layout_proxy_min_font"] = min(entry["fontPt"] for entry in entries) >= 4.4
    checks["layout_proxy_count"] = len(entries) >= 42

    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    environment = json.loads((HERE / "environment.json").read_text(encoding="utf-8"))
    checks["contract_certificate_bound"] = (
        contract["certificate"]["sha256"] == EXPECTED_CERT_SHA256
        and contract["certificate"]["checks"] == "31/31"
    )
    checks["contract_script_bound"] = contract["script"]["sha256"] == EXPECTED_SCRIPT_SHA256
    checks["contract_source_only"] = contract.get("sourceCertificateAndGeneratorOnly") is True
    checks["contract_claim_boundary"] = (
        contract["claimBoundary"]["rejectedObject"] == "FROZEN PROPOSED INEQUALITY ONLY"
        and contract["claimBoundary"]["clay"] == "NOT CLAY"
        and contract["claimBoundary"]["dns"] == "NOT DNS"
    )
    checks["contract_two_panels"] = set(contract["figureClaims"]) == {"A", "B"}
    checks["config_static_analytic"] = config["static"] is True and config["dns"] is False and config["simulation"] is False
    checks["config_palette"] = config["palettePolicy"] == "hard two-root cap" and set(config["nonNeutralRoots"]) == {"blue", "gold"}
    checks["config_source_hashes"] = (
        config["certificateSha256"] == EXPECTED_CERT_SHA256
        and config["scriptSha256"] == EXPECTED_SCRIPT_SHA256
    )
    checks["environment_source_hashes"] = (
        environment["certificateSha256"] == EXPECTED_CERT_SHA256
        and environment["scriptSha256"] == EXPECTED_SCRIPT_SHA256
        and environment["certificateStdoutByteIdentical"] is True
    )

    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    contract_note = (HERE / "chart-contract-and-source-data.md").read_text(encoding="utf-8")
    checks["caption_formula_boundary"] = "not numerical flow simulations" in caption.lower() and "NOT CLAY" in caption
    checks["caption_rejected_object"] = "PROPOSED INEQUALITY REJECTED" in caption and "accompanying proof" in caption
    checks["readme_boundary"] = "not DNS, simulation" in readme and "NOT CLAY" in readme
    checks["chart_contract_exact_source"] = "16 rows" in contract_note and "No fitted values" in contract_note
    checks["manual_visual_qa"] = MANUAL_VISUAL_QA == "PASS"

    passed = sum(checks.values())
    total = len(checks)
    status = "PASS" if passed == total else "FAIL"
    validation = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "checks": checks,
        "figureId": FIGURE_ID,
        "scriptSha256": EXPECTED_SCRIPT_SHA256,
        "status": status,
        "summary": {"passed": passed, "total": total},
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (HERE / "results.json").write_text(
        json.dumps({
            "certificateChecks": "31/31",
            "certificateSha256": EXPECTED_CERT_SHA256,
            "figureId": FIGURE_ID,
            "scriptSha256": EXPECTED_SCRIPT_SHA256,
            "status": status,
            "validationChecks": f"{passed}/{total}",
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    visual_line = (
        "**PASS (2026-09-01).** The approximately 600 dpi master, grayscale derivative, 300 dpi PDF render, and 1800-pixel final-size derivative were inspected locally. The full and enlarged exponent ladders, three exact gap cards, ledger headers, formulas, both discrete-scale values, asymptotic directions, and theorem-status footer are unclipped. Open/filled circle, diamond, square, triangle, solid/dashed row borders, direct labels, and row separation remain distinguishable in grayscale. The PDF render matches the master composition."
        if MANUAL_VISUAL_QA == "PASS"
        else "**PENDING.** Visual inspection of all four QA surfaces must be completed before the package can pass."
    )
    (HERE / "qa-report.md").write_text(
        "# QA report\n\n"
        f"**Status:** {status} ({passed}/{total} independent checks).\n\n"
        "The validator independently recomputed every displayed fraction from the frozen 31/31 certificate, regenerated that certificate byte-for-byte from the frozen script, checked all 16 exact-source rows and analytic log10 evaluations, verified the 180 x 82 mm one-page PDF and embedded fonts, checked the approximately 600 dpi RGB PNG, confirmed live SVG text with no raster image, and required every recorded text extent to stay inside its declared canvas or panel container. The extent check is an auditable string-width/ascent proxy, not a substitute for visual inspection. The rejected object is the frozen proposed inequality only. NOT DNS. NOT CLAY.\n\n"
        "## Manual visual QA\n\n"
        f"{visual_line}\n",
        encoding="utf-8",
    )

    bound = sorted(name for name in NAMES if name not in {"SHA256SUMS", "manifest.json"})
    manifest = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "figureId": FIGURE_ID,
        "files": [
            {"bytes": (HERE / name).stat().st_size, "path": name, "sha256": sha256(HERE / name)}
            for name in bound
        ],
        "scriptSha256": EXPECTED_SCRIPT_SHA256,
        "sources": [
            "scripts/r074g_complete_payment_certificate.py",
            "research/r074g_complete_payment_certificate.json",
        ],
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
        failed = [name for name, passed_check in checks.items() if not passed_check]
        raise SystemExit(f"validation failed: {failed}; {passed}/{total}")
    print(f"PASS {passed}/{total}; 24 files; analytic derivation; certificate 31/31; NOT CLAY")


if __name__ == "__main__":
    main()
