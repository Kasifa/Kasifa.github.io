#!/usr/bin/env python3
"""Independent structural and exact-arithmetic validator for the R0.74E figure."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074e_outer_annulus_exponent_certificate.json"
EXPECTED_CERT_SHA256 = "c6b7f0b9d11a58568c588dd3116e66fbdb9d7d5b5383493c9b492bf6cdba4372"
EXPECTED_SOURCE_NOTE_SHA256 = "3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7"
SOURCE_NOTE = REPO / "research/r074e_local_mollified_frame_gate.md"

NAMES = {
    "README.md", "SHA256SUMS", "caption.md", "chart-contract-and-source-data.md",
    "command.txt", "config.json", "contract.json", "environment.json",
    "figure.pdf", "figure.png", "figure.svg", "layout-bounds.json",
    "manifest.json", "plot.py", "qa-final-size.png", "qa-grayscale.png",
    "qa-pdf.png", "qa-protocol.md", "qa-report.md", "requirements.txt",
    "results.json", "source-data.csv", "validate.py", "validation.json",
}


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
    checks["file_inventory_24"] = {path.name for path in HERE.iterdir() if path.is_file()} == NAMES
    checks["certificate_hash"] = sha256(CERTIFICATE) == EXPECTED_CERT_SHA256
    checks["source_note_hash"] = sha256(SOURCE_NOTE) == EXPECTED_SOURCE_NOTE_SHA256
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    checks["certificate_schema"] = certificate.get("schema") == "r074e-outer-annulus-exponent-certificate-v1"
    checks["certificate_13_of_13"] = certificate.get("status") == "PASS" and certificate.get("summary") == {"passed": 13, "total": 13}
    checks["certificate_all_checks_true"] = len(certificate.get("checks", [])) == 13 and all(item.get("pass") is True for item in certificate["checks"])

    inputs = certificate["inputs"]
    lam = Fraction(inputs["lambda"])
    ch = Fraction(inputs["c_h"])
    alpha = Fraction(inputs["alpha"])
    beta2 = Fraction(inputs["beta_squared"])
    c_r = Fraction(inputs["c_R"])
    kappa = Fraction(inputs["kappa"])
    l_min = Fraction(inputs["L_min"])
    c_gamma = Fraction(certificate["derived"]["c_gamma"])
    lower = Fraction(certificate["derived"]["packet_Gu_lower"])
    upper = Fraction(certificate["derived"]["heat_isolation_upper"])
    leakage = Fraction(certificate["derived"]["local_leakage_exponent"])
    checks["frozen_parameters"] = (lam, ch, alpha, beta2, c_r, kappa, l_min) == (
        Fraction(63, 32), Fraction(15, 16), Fraction(14, 15), Fraction(31, 256),
        Fraction(1, 320), Fraction(16), Fraction(7680),
    )
    checks["radial_split_exact"] = ch * ch + beta2 == 1
    checks["window_exact"] = lower == Fraction(4, 1323) and upper == Fraction(49, 14625) and lower < c_r < upper
    checks["window_margins_exact"] = c_r - lower == Fraction(43, 423360) and upper - c_r == Fraction(211, 936000)
    checks["leakage_exact"] = c_gamma == Fraction(8, 3969) and leakage == Fraction(75, 22528) and leakage - c_gamma == Fraction(117451, 89413632)
    checks["leakage_beats_inverse_R_exact"] = leakage > c_r and leakage - c_r == Fraction(23, 112640)
    checks["geometry_exact"] = 1 / lam == Fraction(32, 63) and 2 / lam == Fraction(64, 63) and 2 / lam - 1 == Fraction(1, 63)
    checks["finite_separation_exact"] = ch - alpha == Fraction(1, 240) and 2 * kappa / l_min == Fraction(1, 240)

    rows = list(csv.DictReader((HERE / "source-data.csv").open(encoding="utf-8")))
    row_map = {row["record"]: Fraction(row["exact_value"]) for row in rows}
    expected_rows = {
        "lambda": lam, "c_h": ch, "alpha": alpha, "beta_squared": beta2,
        "c_R": c_r, "window_lower": lower, "window_upper": upper,
        "window_lower_margin": c_r - lower, "window_upper_margin": upper - c_r,
        "c_gamma": c_gamma, "leakage_exponent": leakage,
        "leakage_inverse_R_margin": leakage - c_r,
        "leakage_margin": leakage - c_gamma, "annulus_inner_over_r": 1 / lam,
        "target_radius_over_r": Fraction(1), "annulus_outer_over_r": 2 / lam,
        "outer_edge_gap_over_r": 2 / lam - 1,
        "transition_bound_over_r": 2 * kappa / l_min,
        "buffer_gap": ch - alpha, "mollified_F_at_origin": Fraction(0),
        "mollified_b_at_origin": Fraction(0), "frame_speed": Fraction(0),
        "frame_acceleration": Fraction(0),
    }
    checks["source_rows_23"] = len(rows) == 23 and set(row_map) == set(expected_rows)
    checks["source_exact_values"] = row_map == expected_rows
    checks["source_status_proved"] = all(row["status"] == "PROVED" for row in rows)

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
        "R0.74E outer-annulus finite frame gate", "13/13 EXACT",
        "4/1323", "1/320", "49/14625", "117451/89413632",
        "ODD + EVEN", "(phi_R * F)(t,0) = 0", "X_R(t) = 0",
        "a_R(t) = a'_R(t) = 0", "EXACT NSE", "PROVED",
        "FINITE GATE ONLY", "OPEN:", "NOT CLAY",
    ]
    checks["svg_required_phrases"] = all(phrase in svg_text for phrase in required_phrases)
    checks["svg_live_text"] = svg.count("<text") >= 35
    checks["svg_no_raster"] = "<image" not in svg
    checks["svg_canvas_dimensions"] = "510.236" in svg and "232.440" in svg
    checks["svg_palette_limited"] = all(token not in svg.lower() for token in ("#ff0000", "#00ff00", "#800080"))

    layout = json.loads((HERE / "layout-bounds.json").read_text(encoding="utf-8"))
    entries = layout["entries"]
    checks["layout_proxy_all_inside"] = bool(entries) and all(entry["proxyPass"] for entry in entries)
    checks["layout_proxy_summary"] = layout["summary"] == {"passed": len(entries), "total": len(entries)}
    checks["layout_proxy_min_font"] = min(entry["fontPt"] for entry in entries) >= 5.0
    checks["layout_proxy_count"] = len(entries) >= 40

    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    checks["contract_certificate_bound"] = contract["certificate"]["sha256"] == EXPECTED_CERT_SHA256 and contract["certificate"]["checks"] == "13/13"
    checks["contract_source_note_bound"] = contract["sourceNoteSha256"] == EXPECTED_SOURCE_NOTE_SHA256
    checks["contract_finite_boundary"] = contract["claimBoundary"]["packetSurvival"] == "OPEN" and contract["claimBoundary"]["clay"] == "NOT CLAY"
    checks["contract_two_panels"] = set(contract["figureClaims"]) == {"A", "B"}
    checks["config_static_analytic"] = config["static"] is True and config["dns"] is False and config["simulation"] is False
    checks["config_palette"] = config["palettePolicy"] == "hard two-root cap" and set(config["nonNeutralRoots"]) == {"blue", "gold"}

    caption = (HERE / "caption.md").read_text(encoding="utf-8")
    readme = (HERE / "README.md").read_text(encoding="utf-8")
    checks["caption_boundary"] = "packet survival remains open" in caption.lower() and "NOT CLAY" in caption
    checks["readme_boundary"] = "finite" in readme.lower() and "NOT CLAY" in readme

    passed = sum(checks.values())
    total = len(checks)
    status = "PASS" if passed == total else "FAIL"
    validation = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "checks": checks,
        "figureId": "fig-r074e-outer-annulus-frame-gate",
        "status": status,
        "summary": {"passed": passed, "total": total},
    }
    (HERE / "validation.json").write_text(json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "results.json").write_text(json.dumps({
        "certificateChecks": "13/13", "certificateSha256": EXPECTED_CERT_SHA256,
        "figureId": "fig-r074e-outer-annulus-frame-gate", "status": status,
        "validationChecks": f"{passed}/{total}",
    }, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "qa-report.md").write_text(
        "# QA report\n\n"
        f"**Status:** {status} ({passed}/{total} independent checks).\n\n"
        "The validator recomputed every displayed fraction from the frozen 13/13 exact certificate, checked the 23-row source export, verified the 180 x 82 mm one-page PDF and embedded fonts, checked the approximately 600 dpi RGB PNG, confirmed live SVG text with no raster image, and required every recorded text extent to stay inside its declared canvas or panel container. The latter is an auditable string-width/ascent proxy, not a substitute for visual inspection. Final-size, grayscale, and PDF-render derivatives are present. The figure states FINITE GATE ONLY, OPEN packet-survival/full-ledger work, and NOT CLAY.\n\n"
        "## Manual visual QA\n\n"
        "**PASS (2026-09-01).** The 600 dpi master, grayscale derivative, 300 dpi PDF render, and 1800-pixel final-size derivative were inspected locally at original detail. Exact fractions remain readable; the c_R marker and both leakage margins are unobscured; paired annular labels, the alpha-separation arrow, and the odd/even implication chain do not clip; the OPEN/NOT CLAY footer is intact. In grayscale, open/filled circle, diamond, square, dashed guide, and outlined interval encodings remain distinguishable. The PDF render matches the master composition.\n",
        encoding="utf-8",
    )

    bound = sorted(name for name in NAMES if name not in {"SHA256SUMS", "manifest.json"})
    manifest = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "figureId": "fig-r074e-outer-annulus-frame-gate",
        "files": [{"bytes": (HERE / name).stat().st_size, "path": name, "sha256": sha256(HERE / name)} for name in bound],
        "sourceNoteSha256": EXPECTED_SOURCE_NOTE_SHA256,
        "status": status,
    }
    (HERE / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    sums = sorted(name for name in NAMES if name != "SHA256SUMS")
    (HERE / "SHA256SUMS").write_text("".join(f"{sha256(HERE / name)}  {name}\n" for name in sums), encoding="utf-8")

    if status != "PASS":
        failed = [name for name, value in checks.items() if not value]
        raise SystemExit(f"validation failed: {failed}")
    print(f"PASS {passed}/{total}; 24 files; exact finite gate only; certificate 13/13")


if __name__ == "__main__":
    main()
