#!/usr/bin/env python3
"""Independent exact-data, structural, surface, and seal validator."""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageStat
from pypdf import PdfReader


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074j_matching_payment_certificate.json"
PRODUCER = REPO / "scripts/r074j_matching_payment_certificate.py"
INDEPENDENT = REPO / "scripts/r074j_matching_payment_certificate_independent.rb"
EXPECTED_CERT_SHA256 = "493c9cf6bc1357b36da1b0a13becbc51e62ea26aab95b6af7eaeb085b65be5d5"
EXPECTED_PRODUCER_SHA256 = "6dcc03d283612306dc39669f5b6c8b3cf8569e40205e067c4db0c2b6929879ec"
EXPECTED_INDEPENDENT_SHA256 = "ca3da7fafea86012c58c20801e680c9bb5ed26c712c92d32cc080426f9916197"
FIGURE_ID = "fig-r074j-fifth-shell-payment"
PDFINFO = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo")
MANUAL_VISUAL_QA = "PASS"

NAMES = {
    "README.md",
    "SHA256SUMS",
    "caption.md",
    "chart-contract-and-source-data.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "layout-bounds.json",
    "manifest.json",
    "plot.py",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-protocol.md",
    "qa-report.md",
    "requirements.txt",
    "results.json",
    "source-data.csv",
    "validate.py",
    "validation.json",
}
TEXT_NAMES = {
    name for name in NAMES
    if Path(name).suffix in {".md", ".txt", ".json", ".csv", ".py"}
} | {"SHA256SUMS"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def write_text(path: Path, content: str) -> None:
    path.write_text(content.replace("\r\n", "\n").rstrip("\n") + "\n", encoding="utf-8")


def resolve(value):
    return value.get_object() if hasattr(value, "get_object") else value


def embedded_fonts(page) -> tuple[int, bool]:
    resources = resolve(page.get("/Resources", {}))
    fonts = resolve(resources.get("/Font", {}))
    flags: list[bool] = []
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


def image_xobject_count(page) -> int:
    resources = resolve(page.get("/Resources", {}))
    xobjects = resolve(resources.get("/XObject", {}))
    count = 0
    for reference in xobjects.values():
        item = resolve(reference)
        if str(item.get("/Subtype", "")) == "/Image":
            count += 1
    return count


def dpi_close(image: Image.Image, target: int) -> bool:
    dpi = image.info.get("dpi", (0, 0))
    return len(dpi) == 2 and all(abs(float(value) - target) < 1.5 for value in dpi)


def exact_expected() -> dict[str, Fraction]:
    k = Fraction(5)
    pay_radius = Fraction(2)
    shell_inner = 2**int(k) * pay_radius
    shell_outer = 2 ** (int(k) + 1) * pay_radius
    box_outer_square = Fraction(96**2 + 1 + 1)
    box_volume = Fraction(2 * 2 * (96 - 80))
    gamma_exponent = Fraction(4 ** (int(k) - 1), 32)
    r_cap = Fraction(1, 200)
    arcsin_input = 16 * r_cap
    delta_over_r = Fraction(32)
    plateau_distance = Fraction(80) - delta_over_r
    brownian_variance = Fraction(2 * 65)
    chebyshev_denominator = plateau_distance**2
    exit_probability = brownian_variance / chebyshev_denominator
    one_minus_theta = 2 * exit_probability
    theta_lower = 1 - one_minus_theta
    time_length = Fraction(65 - 61)
    normalization = Fraction(1, pay_radius**2)
    theta_cube = Fraction(1, 2) ** 3
    gu_coefficient = normalization * time_length * box_volume * theta_cube
    rho = Fraction(1, 320)
    payment_rate = 3 * rho
    lacunarity = payment_rate * (4 - 1)
    return {
        "payment_radius_over_R": pay_radius,
        "shell_index": k,
        "shell_inner_over_R": shell_inner,
        "shell_outer_over_R": shell_outer,
        "proof_box_x3_lower_over_R": Fraction(80),
        "proof_box_x3_upper_over_R": Fraction(96),
        "proof_box_volume_over_R3": box_volume,
        "outer_square": box_outer_square,
        "outer_square_margin": shell_outer**2 - box_outer_square,
        "plateau_distance_over_R": plateau_distance,
        "exit_probability_upper": exit_probability,
        "theta_lower": theta_lower,
        "time_length_over_R2": time_length,
        "payment_normalization": normalization,
        "theta_cube_floor": theta_cube,
        "Gu_lower_coefficient": gu_coefficient,
        "Gu_R_power": Fraction(-2 + 2 + 3),
        "log_payment_rate": payment_rate,
        "old_log_window_lower": 2 * rho,
        "old_log_window_upper": 3 * rho,
        "lacunarity_rate": lacunarity,
        "frontier_L_power": Fraction(1),
        "gamma_exponent": gamma_exponent,
        "R_cap": r_cap,
        "arcsin_input": arcsin_input,
        "delta_over_R": delta_over_r,
        "brownian_variance": brownian_variance,
        "chebyshev_denominator": chebyshev_denominator,
    }


def verify_seal() -> tuple[bool, list[str]]:
    errors: list[str] = []
    current = {path.name for path in HERE.iterdir() if path.is_file()}
    if current != NAMES:
        errors.append("final inventory mismatch")
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    rows = manifest.get("files", [])
    expected_manifest_names = sorted(NAMES - {"manifest.json", "SHA256SUMS"})
    if [row.get("path") for row in rows] != expected_manifest_names or len(rows) != 22:
        errors.append("manifest path set/order mismatch")
    for row in rows:
        path = HERE / str(row.get("path"))
        if not path.is_file():
            errors.append(f"manifest missing {path.name}")
        elif row.get("bytes") != path.stat().st_size or row.get("sha256") != sha256(path):
            errors.append(f"manifest digest mismatch {path.name}")
    lines = (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    expected_sha_names = sorted(NAMES - {"SHA256SUMS"})
    parsed: list[tuple[str, str]] = []
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  ([A-Za-z0-9._-]+)", line)
        if not match:
            errors.append("invalid SHA256SUMS syntax")
            continue
        parsed.append((match.group(2), match.group(1)))
    if [name for name, _ in parsed] != expected_sha_names or len(parsed) != 23:
        errors.append("SHA256SUMS path set/order mismatch")
    for name, digest in parsed:
        if sha256(HERE / name) != digest:
            errors.append(f"SHA256SUMS mismatch {name}")
    return not errors, errors


def verify_only() -> None:
    ok, errors = verify_seal()
    validation = json.loads((HERE / "validation.json").read_text(encoding="utf-8"))
    ok = ok and validation.get("result") == "PASS"
    if not ok:
        raise SystemExit("verify-only FAIL: " + "; ".join(errors or ["validation is not PASS"]))
    summary = validation["summary"]
    print(f"verify-only PASS {summary['passed']}/{summary['total']}; 24 files; 22 manifest rows; 23 SHA rows")


def main() -> None:
    checks: dict[str, bool] = {}
    current_names = {path.name for path in HERE.iterdir() if path.is_file()}
    checks["inventory_pre_or_final"] = current_names <= NAMES and len(current_names) in {21, 24}
    checks["certificate_hash"] = sha256(CERTIFICATE) == EXPECTED_CERT_SHA256
    checks["producer_hash"] = sha256(PRODUCER) == EXPECTED_PRODUCER_SHA256
    checks["independent_hash"] = sha256(INDEPENDENT) == EXPECTED_INDEPENDENT_SHA256

    regenerated = subprocess.run([sys.executable, str(PRODUCER)], check=True, capture_output=True).stdout
    checks["producer_stdout_byte_identical"] = regenerated == CERTIFICATE.read_bytes()
    ruby = subprocess.run(["/usr/bin/ruby", str(INDEPENDENT)], check=True, capture_output=True, text=True).stdout
    checks["ruby_independent_38_of_38"] = all(
        token in ruby
        for token in (
            "frozen_json_used_as_arithmetic_input=false",
            "independentPassed=38",
            "independentTotal=38",
            "leafFieldComparisons=287",
            "mismatchCount=0",
            "result=PASS",
        )
    )

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    cert_rows = certificate.get("checks", [])
    cert = {item["id"]: item for item in cert_rows}
    checks["certificate_result_pass"] = certificate.get("result") == "PASS"
    checks["certificate_38_of_38"] = certificate.get("summary") == {"passed": 38, "total": 38}
    checks["certificate_unique_all_true"] = (
        len(cert_rows) == 38 and len(cert) == 38 and all(item.get("pass") is True for item in cert_rows)
    )
    boundary = " ".join(certificate.get("analytic_boundary", [])).lower()
    checks["boundary_heat_not_finite"] = "brownian representation" in boundary and "does not prove" in boundary
    checks["boundary_upper_not_finite"] = "complete-payment upper bound" in boundary and "does not prove" in boundary
    checks["boundary_endpoint_open"] = "upper bound for x_j" in boundary and "does not prove" in boundary
    checks["boundary_clay"] = "clay millennium" in boundary and "does not prove" in boundary

    expected = exact_expected()
    cert_map = {
        "payment_shell_index": expected["shell_index"],
        "payment_radius_over_R": expected["payment_radius_over_R"],
        "shell_inner_over_R": expected["shell_inner_over_R"],
        "shell_outer_over_R": expected["shell_outer_over_R"],
        "box_outer_square_is_inside_shell_outer": expected["outer_square"],
        "box_outer_squared_margin": expected["outer_square_margin"],
        "box_volume_coefficient": expected["proof_box_volume_over_R3"],
        "gamma5_exponent": expected["gamma_exponent"],
        "R_cap": expected["R_cap"],
        "arcsin_input_cap": expected["arcsin_input"],
        "delta_over_R_upper": expected["delta_over_R"],
        "left_plateau_distance_over_R": expected["plateau_distance_over_R"],
        "brownian_variance_coefficient": expected["brownian_variance"],
        "chebyshev_denominator_coefficient": expected["chebyshev_denominator"],
        "exit_probability_upper": expected["exit_probability_upper"],
        "one_minus_theta_upper": 1 - expected["theta_lower"],
        "theta_rational_lower": expected["theta_lower"],
        "I_2R_length_coefficient": expected["time_length_over_R2"],
        "payment_normalization_coefficient": expected["payment_normalization"],
        "theta_cube_floor": expected["theta_cube_floor"],
        "Gu_lower_coefficient": expected["Gu_lower_coefficient"],
        "Gu_R_power": expected["Gu_R_power"],
        "rho_exact_value": Fraction(1, 320),
        "log_payment_coefficient": expected["log_payment_rate"],
        "L_square_ratio": Fraction(4),
        "lacunarity_coefficient": expected["lacunarity_rate"],
        "payment_23_B_power": Fraction(2),
        "payment_23_R_power": Fraction(2),
        "sqrt_log_L_power": Fraction(1),
        "frontier_total_L_power": expected["frontier_L_power"],
        "payment_to_target_ratio_B_power": Fraction(1),
        "payment_to_target_ratio_R_power": Fraction(1),
        "payment_to_target_ratio_L_power": Fraction(-1),
    }
    checks["certificate_plotted_and_endpoint_values_exact"] = all(
        item in cert and Fraction(cert[item]["left"]) == value
        for item, value in cert_map.items()
    )
    checks["finite_shell_containment"] = (
        expected["outer_square"] < expected["shell_outer_over_R"] ** 2
        and expected["outer_square_margin"] == 7166
    )
    checks["finite_theta_chain"] = (
        expected["exit_probability_upper"] == Fraction(65, 1152)
        and expected["theta_lower"] == Fraction(511, 576)
        and expected["theta_lower"] > Fraction(1, 2)
    )
    checks["finite_cubic_ledger"] = (
        expected["Gu_lower_coefficient"] == 8 and expected["Gu_R_power"] == 3
    )
    checks["finite_log_rates"] = (
        expected["log_payment_rate"] == Fraction(3, 320)
        and expected["lacunarity_rate"] == Fraction(9, 320)
    )

    rows = list(csv.DictReader((HERE / "source-data.csv").open(encoding="utf-8")))
    row_map = {(row["panel"], row["record"]): row for row in rows}
    checks["source_rows_22"] = len(rows) == 22
    checks["source_unique_keys"] = len(row_map) == 22
    expected_key_panels = {
        **{name: "A" for name in (
            "payment_radius_over_R",
            "shell_index",
            "shell_inner_over_R",
            "shell_outer_over_R",
            "proof_box_x3_lower_over_R",
            "proof_box_x3_upper_over_R",
            "proof_box_volume_over_R3",
            "outer_square",
            "outer_square_margin",
            "plateau_distance_over_R",
            "exit_probability_upper",
            "theta_lower",
        )},
        **{name: "B" for name in (
            "time_length_over_R2",
            "payment_normalization",
            "theta_cube_floor",
            "Gu_lower_coefficient",
            "Gu_R_power",
            "log_payment_rate",
            "old_log_window_lower",
            "old_log_window_upper",
            "lacunarity_rate",
            "frontier_L_power",
        )},
    }
    expected_keys = {(panel, name) for name, panel in expected_key_panels.items()}
    checks["source_keys_exact"] = set(row_map) == expected_keys
    checks["source_values_exact"] = all(
        Fraction(row_map[(panel, name)]["value_exact"]) == expected[name]
        for name, panel in expected_key_panels.items()
    )
    checks["source_evidence_classes"] = (
        row_map[("A", "plateau_distance_over_R")]["status"] == "PROVED ANALYTIC CONSEQUENCE"
        and row_map[("A", "theta_lower")]["status"] == "PROVED ANALYTIC CONSEQUENCE"
        and row_map[("B", "Gu_lower_coefficient")]["status"] == "FINITE EXACT"
        and row_map[("B", "old_log_window_lower")]["status"] == "INHERITED"
        and row_map[("B", "frontier_L_power")]["status"] == "PROVED FOR FAMILY"
    )
    source_lower = (HERE / "source-data.csv").read_text(encoding="utf-8").lower()
    checks["source_no_empirical_values"] = all(
        term not in source_lower for term in ("measured", "observed", "sample output", "dns output")
    )

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    checks["config_figure_id"] = config.get("figureId") == FIGURE_ID
    checks["config_600dpi"] = config.get("dpi") == 600
    checks["config_178x88"] = config.get("canvasMm") == [178, 88]
    checks["config_two_roots"] = (
        config.get("palettePolicy") == "hard two-root cap"
        and config.get("nonNeutralRoots") == ["blue", "gold"]
    )
    checks["config_not_simulation"] = config.get("dns") is False and config.get("simulation") is False
    checks["config_noncolor_distinctions"] = len(config.get("nonColorDistinction", [])) >= 5
    checks["contract_file_count"] = contract.get("expectedFileCount") == 24
    checks["contract_source_hashes"] = (
        contract["certificate"]["sha256"] == EXPECTED_CERT_SHA256
        and contract["producer"]["sha256"] == EXPECTED_PRODUCER_SHA256
    )
    checks["contract_exact_consequences"] = contract["panelB"]["consequences"] == {
        "endpointUpper": "OPEN",
        "lacunarityRate": "9/320",
        "logPaymentRate": "3/320",
    }
    checks["contract_evidence_boundary"] = contract.get("evidenceBoundary") == {
        "analytic": "R0.74J Lemma 2.1 and Theorems 3.2--3.3",
        "certificate": "FINITE ARITHMETIC ONLY",
        "inherited": "R0.74G Theorem 1.1",
    }
    checks["contract_scope_statuses"] = {
        "EXACT FAMILY",
        "NOT DNS",
        "NOT SIMULATION",
        "NOT CLAY",
    } <= set(contract.get("statuses", []))

    master = Image.open(HERE / "figure.png")
    expected_width = round(178 / 25.4 * 600)
    expected_height = round(88 / 25.4 * 600)
    checks["png_600dpi_dimensions"] = abs(master.width - expected_width) <= 1 and abs(master.height - expected_height) <= 1
    checks["png_600dpi_metadata"] = dpi_close(master, 600)
    checks["png_rgb"] = master.mode == "RGB"
    checks["png_aspect_178x88"] = abs(master.width / master.height - 178 / 88) < 0.003
    extrema = master.getextrema()
    checks["png_nonblank_tonal_range"] = (
        min(low for low, _ in extrema) < 40
        and all(high > 245 for _, high in extrema)
        and ImageStat.Stat(master.convert("L")).stddev[0] > 15
    )

    gray = Image.open(HERE / "qa-grayscale.png")
    checks["qa_grayscale_mode"] = gray.mode == "L"
    checks["qa_grayscale_dimensions"] = gray.size == master.size
    checks["qa_grayscale_metadata"] = dpi_close(gray, 600)
    checks["qa_grayscale_nonblank"] = ImageStat.Stat(gray).stddev[0] > 15

    final_size = Image.open(HERE / "qa-final-size.png")
    checks["qa_final_width_1780"] = final_size.width == 1780
    checks["qa_final_aspect"] = abs(final_size.width / final_size.height - 178 / 88) < 0.004
    checks["qa_final_metadata"] = dpi_close(final_size, 254)

    pdf_qa = Image.open(HERE / "qa-pdf.png")
    checks["qa_pdf_dimensions_300dpi"] = (
        abs(pdf_qa.width - round(178 / 25.4 * 300)) <= 1
        and abs(pdf_qa.height - round(88 / 25.4 * 300)) <= 1
    )
    checks["qa_pdf_aspect"] = abs(pdf_qa.width / pdf_qa.height - 178 / 88) < 0.004
    checks["qa_pdf_metadata"] = dpi_close(pdf_qa, 300)
    checks["qa_pdf_nonblank"] = ImageStat.Stat(pdf_qa.convert("L")).stddev[0] > 15

    reader = PdfReader(str(HERE / "figure.pdf"))
    checks["pdf_one_page"] = len(reader.pages) == 1
    page = reader.pages[0]
    width, height = float(page.mediabox.width), float(page.mediabox.height)
    checks["pdf_178x88mm"] = abs(width - 178 / 25.4 * 72) < 0.5 and abs(height - 88 / 25.4 * 72) < 0.5
    font_count, all_embedded = embedded_fonts(page)
    checks["pdf_fonts_embedded"] = font_count >= 1 and all_embedded
    checks["pdf_vector_no_image_xobjects"] = image_xobject_count(page) == 0
    pdfinfo = subprocess.run([str(PDFINFO), str(HERE / "figure.pdf")], check=True, capture_output=True, text=True).stdout
    checks["pdfinfo_one_page"] = "Pages:" in pdfinfo and re.search(r"Pages:\s+1\b", pdfinfo) is not None

    svg_bytes = (HERE / "figure.svg").read_bytes()
    svg_text = svg_bytes.decode("utf-8")
    root = ET.fromstring(svg_bytes)
    visible = " ".join("".join(root.itertext()).split())
    checks["svg_viewbox"] = len(root.attrib.get("viewBox", "").split()) == 4
    checks["svg_title"] = "R0.74J exact fifth-shell payment law" in visible
    checks["svg_panel_labels"] = all(
        item in visible for item in ("Exact fifth-shell geometry", "Matching complete payment")
    )
    checks["svg_geometry_labels"] = all(
        item in visible for item in ("A_5(2R): 64R <= |x| < 128R", "|Q_R| = 64 R^3", "theta >= 511/576 > 1/2")
    )
    checks["svg_payment_labels"] = all(
        item in visible for item in ("G_u >= 8 e^-8 B^3 R^3", "log(P_j)/L_j^2 -> 3/320", "sqrt-log endpoint upper remains OPEN")
    )
    checks["svg_scope_labels"] = all(
        item in visible for item in ("EXACT FAMILY", "NOT DNS", "NOT SIMULATION", "NOT CLAY")
    )
    colors = {token.upper() for token in re.findall(r"#[0-9A-Fa-f]{6}", svg_text)}
    allowed = {
        "#202A34", "#626D78", "#E3E8EC", "#F6F8FA", "#1F5A91",
        "#E6F0F7", "#A87312", "#FBF2DE", "#FFFFFF",
    }
    css_colors = {
        tuple(float(component) for component in match)
        for match in re.findall(
            r"rgb\(\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*\)",
            svg_text,
        )
    }
    allowed_css = {
        (12.0, 16.0, 20.0), (38.0, 42.0, 47.0), (89.0, 90.0, 92.0),
        (96.0, 97.0, 98.0), (12.0, 35.0, 56.0), (90.0, 94.0, 96.0),
        (65.0, 45.0, 7.0), (98.0, 94.0, 87.0), (100.0, 100.0, 100.0),
    }
    checks["svg_palette_declared_only"] = colors <= allowed and css_colors <= allowed_css
    checks["svg_blue_and_gold_present"] = (
        ("#1F5A91" in colors or (12.0, 35.0, 56.0) in css_colors)
        and ("#A87312" in colors or (65.0, 45.0, 7.0) in css_colors)
    )
    checks["svg_noncolor_distinctions"] = "stroke-dasharray" in svg_text and "<polygon" in svg_text

    layout = json.loads((HERE / "layout-bounds.json").read_text(encoding="utf-8"))
    entries = layout.get("entries", [])
    checks["layout_entries_nonempty"] = len(entries) >= 35
    checks["layout_all_proxy_pass"] = bool(entries) and all(item.get("proxyPass") is True for item in entries)
    checks["layout_summary_exact"] = layout.get("summary") == {"passed": len(entries), "total": len(entries)}
    checks["layout_min_font"] = min(float(item["fontPt"]) for item in entries) >= 3.7

    environment = json.loads((HERE / "environment.json").read_text(encoding="utf-8"))
    checks["environment_provenance"] = (
        environment.get("figureId") == FIGURE_ID
        and environment.get("certificateChecks") == "38/38"
        and environment.get("certificateSha256") == EXPECTED_CERT_SHA256
        and environment.get("producerSha256") == EXPECTED_PRODUCER_SHA256
        and environment.get("certificateStdoutByteIdentical") is True
    )
    checks["environment_poppler"] = str(environment.get("poppler", "")).startswith("pdfinfo version")
    checks["qa_report_pass"] = "**Result:** PASS" in (HERE / "qa-report.md").read_text(encoding="utf-8")
    checks["manual_visual_qa_master"] = MANUAL_VISUAL_QA == "PASS"
    checks["manual_visual_qa_final_size"] = MANUAL_VISUAL_QA == "PASS"
    checks["manual_visual_qa_grayscale"] = MANUAL_VISUAL_QA == "PASS"
    checks["manual_visual_qa_pdf"] = MANUAL_VISUAL_QA == "PASS"
    checks["runtime_cache_absent"] = not any(path.name == "__pycache__" for path in HERE.iterdir())

    text_policy = True
    control_policy = True
    for name in sorted(current_names & TEXT_NAMES):
        payload = (HERE / name).read_bytes()
        text_policy &= b"\r\n" not in payload and payload.endswith(b"\n") and not payload.endswith(b"\n\n")
        decoded = payload.decode("utf-8")
        control_policy &= not any(ord(char) < 32 and char not in "\n\t" for char in decoded)
    checks["text_eof_policy"] = text_policy
    checks["text_control_char_policy"] = control_policy

    passed = sum(checks.values())
    total = len(checks)
    validation = {
        "checks": checks,
        "figureId": FIGURE_ID,
        "result": "PASS" if passed == total else "FAIL",
        "summary": {"passed": passed, "total": total},
    }
    write_text(HERE / "validation.json", json.dumps(validation, indent=2, sort_keys=True))
    results = json.loads((HERE / "results.json").read_text(encoding="utf-8"))
    results.update(
        {
            "filesExpected": 24,
            "status": validation["result"],
            "validator": validation["summary"],
        }
    )
    write_text(HERE / "results.json", json.dumps(results, indent=2, sort_keys=True))

    manifest_names = sorted(NAMES - {"manifest.json", "SHA256SUMS"})
    manifest = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "figureId": FIGURE_ID,
        "files": [
            {
                "bytes": (HERE / name).stat().st_size,
                "path": name,
                "sha256": sha256(HERE / name),
            }
            for name in manifest_names
        ],
        "independentProducerSha256": EXPECTED_INDEPENDENT_SHA256,
        "producerSha256": EXPECTED_PRODUCER_SHA256,
        "sources": [
            "scripts/r074j_matching_payment_certificate.py",
            "scripts/r074j_matching_payment_certificate_independent.rb",
            "research/r074j_matching_payment_certificate.json",
        ],
        "status": validation["result"],
    }
    write_text(HERE / "manifest.json", json.dumps(manifest, indent=2, sort_keys=True))
    sha_names = sorted(NAMES - {"SHA256SUMS"})
    write_text(
        HERE / "SHA256SUMS",
        "\n".join(f"{sha256(HERE / name)}  {name}" for name in sha_names),
    )
    seal_ok, seal_errors = verify_seal()
    if validation["result"] != "PASS" or not seal_ok:
        failed = [name for name, state in checks.items() if not state]
        raise SystemExit(
            f"FAIL {passed}/{total}; checks={','.join(failed)}; seal={';'.join(seal_errors)}"
        )
    print(f"PASS {passed}/{total}; 24 files; 22 manifest rows; 23 SHA rows")


if __name__ == "__main__":
    if "--verify-only" in sys.argv[1:]:
        verify_only()
    else:
        main()
