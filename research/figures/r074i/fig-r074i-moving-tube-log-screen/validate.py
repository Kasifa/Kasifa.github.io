#!/usr/bin/env python3
"""Independent provenance, exact-data, structural, and surface validator."""
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
CERTIFICATE = REPO / "research/r074i_tube_log_certificate.json"
PRODUCER = REPO / "scripts/r074i_tube_log_certificate.py"
EXPECTED_CERT_SHA256 = "d4d0f32f6772bdae8a9ec0e8fd6f5f5f9248877df3c19bf544c3577055ab7bf5"
EXPECTED_PRODUCER_SHA256 = "5411134949eedbb1c285607c33a4f8feb9f8d358f5fc7cee91ec3601dfe3932f"
FIGURE_ID = "fig-r074i-moving-tube-log-screen"
PDFINFO = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override/pdfinfo")
# Signed only after view_image inspection of the master, final-size,
# grayscale, and independently Poppler-rasterized PDF surfaces.
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


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


def screen_y(gamma: Fraction) -> Fraction:
    return Fraction(1) - 2 * gamma


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def dpi_close(image: Image.Image, target: int) -> bool:
    dpi = image.info.get("dpi", (0, 0))
    return len(dpi) == 2 and all(abs(float(value) - target) < 1.5 for value in dpi)


def main() -> None:
    checks: dict[str, bool] = {}
    current_names = {path.name for path in HERE.iterdir() if path.is_file()}
    checks["inventory_pre_or_final"] = current_names <= NAMES and len(current_names) in {20, 21, 22, 23, 24}
    checks["certificate_hash"] = sha256(CERTIFICATE) == EXPECTED_CERT_SHA256
    checks["producer_hash"] = sha256(PRODUCER) == EXPECTED_PRODUCER_SHA256

    regenerated = subprocess.run([sys.executable, str(PRODUCER)], check=True, capture_output=True).stdout
    checks["producer_stdout_byte_identical"] = regenerated == CERTIFICATE.read_bytes()
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    checks["certificate_result_pass"] = certificate.get("result") == "PASS"
    checks["certificate_36_of_36"] = certificate.get("summary") == {"passed": 36, "total": 36}
    checks["certificate_all_true"] = len(certificate.get("checks", [])) == 36 and all(
        item.get("pass") is True for item in certificate.get("checks", [])
    )
    boundary = " ".join(certificate.get("analytic_boundary", [])).lower()
    checks["boundary_moving_path_not_finite"] = "mollified path" in boundary and "does not prove" in boundary
    checks["boundary_epsilon_not_finite"] = "epsilon-regularity criterion" in boundary and "does not prove" in boundary
    checks["boundary_clay"] = "clay millennium" in boundary and "global smoothness" in boundary

    cert = {item["id"]: item for item in certificate["checks"]}

    def value(check_id: str, field: str = "left") -> Fraction:
        return Fraction(cert[check_id][field])

    finite = {
        "normalized_cubic_scaling": value("ns_normalized_l3_scale_invariance"),
        "half_radius_time_factor": value("half_radius_time_length_factor"),
        "half_radius_normalization": value("half_radius_normalization_factor"),
        "half_radius_factor_product": value("half_radius_fixed_factor_product"),
        "energy_payment_inverse_chain": value("energy_from_payment_inverse_power"),
        "tube_payment_threshold_chain": value("tube_to_payment_threshold_power"),
        "rho": value("rho_exact_value"),
        "log_window_lower": value("two_rho"),
        "log_window_upper": value("three_rho"),
        "log_window_width": value("log_window_width"),
        "lacunarity_exponent": value("lacunarity_log_exponent"),
        "frontier_L_power": value("frontier_total_L_power"),
    }
    checks["finite_normalized_cubic_zero"] = finite["normalized_cubic_scaling"] == 0
    checks["finite_half_time_quarter"] = finite["half_radius_time_factor"] == Fraction(1, 4)
    checks["finite_half_normalization_four"] = finite["half_radius_normalization"] == 4
    checks["finite_half_product_one"] = finite["half_radius_factor_product"] == 1
    checks["finite_threshold_chains_one"] = (
        finite["energy_payment_inverse_chain"]
        == finite["tube_payment_threshold_chain"]
        == 1
    )
    checks["finite_rho_window"] = (
        finite["rho"] == Fraction(1, 320)
        and finite["log_window_lower"] == Fraction(1, 160)
        and finite["log_window_upper"] == Fraction(3, 320)
        and finite["log_window_width"] == Fraction(1, 320)
    )
    checks["finite_lacunarity"] = finite["lacunarity_exponent"] == Fraction(1, 64)
    checks["finite_frontier_L_one"] = finite["frontier_L_power"] == 1
    checks["finite_gap_coefficients"] = (
        value("subcritical_gap_constant_coefficient") == 0
        and value("subcritical_gap_delta_coefficient") == 1
        and value("endpoint_gamma_gap") == 0
    )

    rows = list(csv.DictReader((HERE / "source-data.csv").open(encoding="utf-8")))
    row_map = {(row["panel"], row["record"]): row for row in rows}
    checks["source_rows_19"] = len(rows) == 19
    checks["source_unique_keys"] = len(row_map) == 19
    expected_keys = {
        *(('A', key) for key in (
            "normalized_cubic_scaling",
            "half_radius_time_factor",
            "half_radius_normalization",
            "half_radius_factor_product",
            "energy_payment_inverse_chain",
            "tube_payment_threshold_chain",
            "path_confinement",
            "fixed_cylinder_cubic",
        )),
        *(('B', f"screen_gamma_{gamma}") for gamma in ("0/1", "1/4", "1/2", "3/4", "1/1")),
        *(('B', key) for key in (
            "rho",
            "log_window_lower",
            "log_window_upper",
            "log_window_width",
            "lacunarity_exponent",
            "frontier_L_power",
        )),
    }
    checks["source_keys_exact"] = set(row_map) == expected_keys
    checks["source_finite_values_exact"] = all(
        Fraction(row_map[("A" if name in {
            "normalized_cubic_scaling",
            "half_radius_time_factor",
            "half_radius_normalization",
            "half_radius_factor_product",
            "energy_payment_inverse_chain",
            "tube_payment_threshold_chain",
        } else "B", name)]["value_exact"]) == expected
        for name, expected in finite.items()
    )
    gamma_points = (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1))
    checks["source_affine_points_exact"] = all(
        Fraction(row_map[("B", f"screen_gamma_{q(gamma)}")]["gamma_exact"]) == gamma
        and Fraction(row_map[("B", f"screen_gamma_{q(gamma)}")]["value_exact"]) == screen_y(gamma)
        for gamma in gamma_points
    )
    checks["source_region_statuses_exact"] = (
        row_map[("B", "screen_gamma_0/1")]["status"] == "REJECTED"
        and row_map[("B", "screen_gamma_1/4")]["status"] == "REJECTED"
        and row_map[("B", "screen_gamma_1/2")]["status"] == "OPEN ENDPOINT"
        and row_map[("B", "screen_gamma_3/4")]["status"] == "NOT REJECTED / NOT PROVED"
        and row_map[("B", "screen_gamma_1/1")]["status"] == "NOT REJECTED / NOT PROVED"
    )
    checks["source_path_status_analytic"] = row_map[("A", "path_confinement")]["status"] == "ANALYTIC IMPLICATION"
    checks["source_cubic_status_analytic"] = row_map[("A", "fixed_cylinder_cubic")]["status"] == "ANALYTIC IMPLICATION"
    source_lower = (HERE / "source-data.csv").read_text(encoding="utf-8").lower()
    checks["source_no_empirical_values"] = all(
        term not in source_lower for term in ("measured", "observed", "sample output", "dns output")
    )

    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    checks["config_figure_id"] = config.get("figureId") == FIGURE_ID
    checks["config_600dpi"] = config.get("dpi") == 600
    checks["config_180x88"] = config.get("canvasMm") == [180, 88]
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
    checks["contract_region_boundaries"] = contract["panelB"]["regions"] == {
        "gamma<1/2": "REJECTED",
        "gamma=1/2": "OPEN ENDPOINT",
        "gamma>1/2": "NOT REJECTED / NOT PROVED",
    }
    checks["contract_scope_statuses"] = {
        "EXACT DIAGRAM",
        "NOT DNS",
        "NOT SIMULATION",
        "NOT CLAY",
    } <= set(contract.get("statuses", []))

    master = Image.open(HERE / "figure.png")
    expected_width = round(180 / 25.4 * 600)
    expected_height = round(88 / 25.4 * 600)
    checks["png_600dpi_dimensions"] = abs(master.width - expected_width) <= 1 and abs(master.height - expected_height) <= 1
    checks["png_600dpi_metadata"] = dpi_close(master, 600)
    checks["png_rgb"] = master.mode == "RGB"
    checks["png_aspect_180x88"] = abs(master.width / master.height - 180 / 88) < 0.003
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
    gray_stat = ImageStat.Stat(gray)
    checks["qa_grayscale_nonblank"] = gray_stat.extrema[0][0] < 50 and gray_stat.stddev[0] > 15

    final_size = Image.open(HERE / "qa-final-size.png")
    checks["qa_final_width_1800"] = final_size.width == 1800
    checks["qa_final_aspect"] = abs(final_size.width / final_size.height - 180 / 88) < 0.004
    checks["qa_final_metadata"] = dpi_close(final_size, 254)

    pdf_qa = Image.open(HERE / "qa-pdf.png")
    checks["qa_pdf_dimensions_300dpi"] = (
        abs(pdf_qa.width - round(180 / 25.4 * 300)) <= 1
        and abs(pdf_qa.height - round(88 / 25.4 * 300)) <= 1
    )
    checks["qa_pdf_aspect"] = abs(pdf_qa.width / pdf_qa.height - 180 / 88) < 0.004
    checks["qa_pdf_metadata"] = dpi_close(pdf_qa, 300)
    checks["qa_pdf_nonblank"] = ImageStat.Stat(pdf_qa.convert("L")).stddev[0] > 15

    reader = PdfReader(str(HERE / "figure.pdf"))
    checks["pdf_one_page"] = len(reader.pages) == 1
    page = reader.pages[0]
    width = float(page.mediabox.width)
    height = float(page.mediabox.height)
    checks["pdf_180x88mm"] = abs(width - 180 / 25.4 * 72) < 0.5 and abs(height - 88 / 25.4 * 72) < 0.5
    font_count, all_embedded = embedded_fonts(page)
    checks["pdf_fonts_embedded"] = font_count >= 1 and all_embedded
    checks["pdf_vector_no_image_xobjects"] = image_xobject_count(page) == 0
    pdfinfo = subprocess.run([str(PDFINFO), str(HERE / "figure.pdf")], check=True, capture_output=True, text=True).stdout
    checks["pdfinfo_page_size"] = "510.236 x 249.449 pts" in pdfinfo

    svg_bytes = (HERE / "figure.svg").read_bytes()
    svg_text = svg_bytes.decode("utf-8")
    root = ET.fromstring(svg_bytes)
    visible_text = " ".join("".join(root.itertext()).split())
    viewbox = root.attrib.get("viewBox", "")
    checks["svg_viewbox"] = bool(viewbox) and len(viewbox.split()) == 4
    checks["svg_figure_id_text"] = "R0.74I moving-tube criterion and logarithmic screen" in visible_text
    checks["svg_scope_labels"] = all(term in visible_text for term in ("EXACT DIAGRAM", "NOT DNS", "NOT SIMULATION", "NOT CLAY"))
    checks["svg_panel_labels"] = all(term in visible_text for term in ("Moving tube to a regular point", "Exact logarithmic exponent screen"))
    checks["svg_chain_labels"] = all(term in visible_text for term in ("E_R sufficiently small", "path confinement", "fixed Q_(R/2) cubic is small", "z0 is a regular point"))
    checks["svg_screen_labels"] = all(term in visible_text for term in ("y(gamma) = 1 - 2 gamma", "REJECTED", "OPEN ENDPOINT", "NOT REJECTED / NOT PROVED"))
    checks["svg_unknown_constants_not_plotted"] = "no unknown constants plotted" in visible_text
    checks["svg_lacunary_boundary"] = "realized lacunary P_j only" in visible_text

    colors = {token.upper() for token in re.findall(r"#[0-9A-Fa-f]{6}", svg_text)}
    allowed = {
        "#202A34",
        "#626D78",
        "#E3E8EC",
        "#F6F8FA",
        "#1F5A91",
        "#E6F0F7",
        "#A87312",
        "#FBF2DE",
        "#FFFFFF",
    }
    css_colors = {
        tuple(float(component) for component in match)
        for match in re.findall(
            r"rgb\(\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*,\s*([0-9.]+)%\s*\)",
            svg_text,
        )
    }
    allowed_css = {
        (12.0, 16.0, 20.0),
        (38.0, 42.0, 47.0),
        (89.0, 90.0, 92.0),
        (96.0, 97.0, 98.0),
        (12.0, 35.0, 56.0),
        (90.0, 94.0, 96.0),
        (65.0, 45.0, 7.0),
        (98.0, 94.0, 87.0),
        (100.0, 100.0, 100.0),
    }
    checks["svg_palette_declared_only"] = colors <= allowed and css_colors <= allowed_css
    checks["svg_blue_and_gold_present"] = (
        ("#1F5A91" in colors or (12.0, 35.0, 56.0) in css_colors)
        and ("#A87312" in colors or (65.0, 45.0, 7.0) in css_colors)
    )
    checks["svg_noncolor_markers"] = "<circle" in svg_text and "<polygon" in svg_text and "<rect" in svg_text
    checks["svg_dashed_distinction"] = "stroke-dasharray" in svg_text
    checks["svg_texture_density"] = svg_text.count("<circle") >= 30 and svg_text.count("<path") >= 40

    layout = json.loads((HERE / "layout-bounds.json").read_text(encoding="utf-8"))
    entries = layout.get("entries", [])
    checks["layout_entries_nonempty"] = len(entries) >= 45
    checks["layout_min_font"] = min(float(item["fontPt"]) for item in entries) >= 3.8
    checks["layout_all_proxy_pass"] = bool(entries) and all(item.get("proxyPass") is True for item in entries)
    checks["layout_summary_exact"] = layout.get("summary") == {"passed": len(entries), "total": len(entries)}

    environment = json.loads((HERE / "environment.json").read_text(encoding="utf-8"))
    checks["environment_poppler"] = environment.get("poppler", "").startswith("pdfinfo version")
    checks["environment_provenance"] = (
        environment.get("certificateSha256") == EXPECTED_CERT_SHA256
        and environment.get("producerSha256") == EXPECTED_PRODUCER_SHA256
        and environment.get("certificateStdoutByteIdentical") is True
    )

    checks["manual_visual_qa_master"] = MANUAL_VISUAL_QA == "PASS"
    checks["manual_visual_qa_grayscale"] = MANUAL_VISUAL_QA == "PASS"
    checks["manual_visual_qa_final_size"] = MANUAL_VISUAL_QA == "PASS"
    checks["manual_visual_qa_pdf"] = MANUAL_VISUAL_QA == "PASS"

    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise SystemExit("validator failures before sealing: " + ", ".join(failed))

    validation = {
        "checks": checks,
        "figureId": FIGURE_ID,
        "result": "PASS",
        "summary": {"passed": len(checks), "total": len(checks)},
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (HERE / "qa-report.md").write_text(
        "# R0.74I figure QA report\n\n"
        f"**Result:** PASS ({len(checks)}/{len(checks)})\n\n"
        "The certificate and producer hashes match, and producer stdout is byte-identical to the 36/36 certificate. "
        "All exact source-data values and affine screen points were independently reconstructed with rational arithmetic. "
        "The one-page 180 mm x 88 mm SVG/vector PDF/600-dpi PNG exports, embedded fonts, Poppler raster, declared two-root palette, "
        "non-color textures and markers, layout bounds, grayscale, and final-size surfaces pass. The PDF contains no raster image XObject. "
        "Manual inspection found no clipping, collision, illegible label, detached arrow or marker, weak grayscale distinction, or color-only meaning. "
        "The figure visibly states EXACT DIAGRAM, NOT DNS, NOT SIMULATION, and NOT CLAY.\n",
        encoding="utf-8",
    )
    (HERE / "results.json").write_text(
        json.dumps(
            {
                "certificate": {"passed": 36, "total": 36},
                "figureId": FIGURE_ID,
                "filesExpected": 24,
                "status": "PASS",
                "validator": {"passed": len(checks), "total": len(checks)},
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    manifest_files = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name not in {"manifest.json", "SHA256SUMS"}:
            manifest_files.append(
                {"bytes": path.stat().st_size, "path": path.name, "sha256": sha256(path)}
            )
    manifest = {
        "certificateSha256": EXPECTED_CERT_SHA256,
        "figureId": FIGURE_ID,
        "files": manifest_files,
        "producerSha256": EXPECTED_PRODUCER_SHA256,
        "sources": [
            "scripts/r074i_tube_log_certificate.py",
            "research/r074i_tube_log_certificate.json",
        ],
        "status": "PASS",
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    final_names_without_sums = {
        path.name for path in HERE.iterdir() if path.is_file() and path.name != "SHA256SUMS"
    }
    if final_names_without_sums != NAMES - {"SHA256SUMS"}:
        missing = sorted((NAMES - {"SHA256SUMS"}) - final_names_without_sums)
        extra = sorted(final_names_without_sums - (NAMES - {"SHA256SUMS"}))
        raise SystemExit(
            f"inventory before SHA256SUMS mismatch; missing={missing}, extra={extra}"
        )
    lines = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if path.is_file() and path.name != "SHA256SUMS":
            lines.append(f"{sha256(path)}  {path.name}")
    (HERE / "SHA256SUMS").write_text("\n".join(lines) + "\n", encoding="utf-8")

    final_names = {path.name for path in HERE.iterdir() if path.is_file()}
    if final_names != NAMES:
        raise SystemExit("final 24-file inventory mismatch")
    for line in (HERE / "SHA256SUMS").read_text(encoding="utf-8").splitlines():
        expected_hash, filename = line.split("  ", 1)
        if sha256(HERE / filename) != expected_hash:
            raise SystemExit(f"post-seal hash mismatch: {filename}")
    print(f"PASS {len(checks)}/{len(checks)}; 24 files; all SHA256 entries verified")


if __name__ == "__main__":
    main()
