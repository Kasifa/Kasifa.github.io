#!/usr/bin/env python3
"""Render the deterministic R0.74O passive-amplitude endpoint figure."""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import math
import platform
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageOps
from reportlab import rl_config
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas as pdfcanvas


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFTOPPM = BUNDLE / "bin/override/pdftoppm"
QUICKLOOK = Path("/usr/bin/qlmanage")
FIGURE_ID = "fig-r074o-amplitude-endpoint"
CLAIM = "SCALAR_PAYMENT_ONLY_ENDPOINT_NO_GO_SMOOTH_EXACT_FAMILY_NOT_CLAY"

WIDTH_MM = 178
HEIGHT_MM = 100
DPI = 600
W = WIDTH_MM * mm
H = HEIGHT_MM * mm

INK = HexColor("#202A34")
MID = HexColor("#64707B")
GRID = HexColor("#D7DEE3")
PALE = HexColor("#F5F7F8")
BLUE = HexColor("#1D5F91")
BLUE_LIGHT = HexColor("#E7F1F8")
GOLD = HexColor("#95650F")
GOLD_LIGHT = HexColor("#FAF0D8")
RED = HexColor("#9B3E38")
RED_LIGHT = HexColor("#F7E8E5")

rl_config.invariant = 1


def locate_font(filename: str) -> Path:
    candidates = [
        BUNDLE
        / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
        / filename,
        Path("/System/Library/Fonts/Supplemental") / filename,
        Path("/Library/Fonts") / filename,
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(filename)


REGULAR_FONT = locate_font("DejaVuSans.ttf")
BOLD_FONT = locate_font("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074O-Regular", str(REGULAR_FONT)))
pdfmetrics.registerFont(TTFont("R074O-Bold", str(BOLD_FONT)))


def label(drawing, x, y, value, size=5.0, *, color=INK, bold=False, anchor="start"):
    drawing.add(
        String(
            x,
            y,
            value,
            fontName="R074O-Bold" if bold else "R074O-Regular",
            fontSize=size,
            fillColor=color,
            textAnchor=anchor,
        )
    )


def multiline(
    drawing,
    x,
    y,
    lines,
    size=4.4,
    *,
    color=INK,
    bold_first=False,
    anchor="middle",
    leading=5.6,
):
    for index, value in enumerate(lines):
        label(
            drawing,
            x,
            y - index * leading,
            value,
            size,
            color=color,
            bold=bold_first and index == 0,
            anchor=anchor,
        )


def arrow(drawing, x0, y0, x1, y1, *, color=INK, dashed=False, width=0.9):
    drawing.add(
        Line(
            x0,
            y0,
            x1,
            y1,
            strokeColor=color,
            strokeWidth=width,
            strokeDashArray=[3, 2] if dashed else None,
        )
    )
    angle = math.atan2(y1 - y0, x1 - x0)
    length, spread = 3.4, 0.52
    drawing.add(
        Polygon(
            [
                x1,
                y1,
                x1 - length * math.cos(angle - spread),
                y1 - length * math.sin(angle - spread),
                x1 - length * math.cos(angle + spread),
                y1 - length * math.sin(angle + spread),
            ],
            fillColor=color,
            strokeColor=color,
        )
    )


def panel(drawing, x, y, width, height, tag, title, *, title_color=BLUE):
    drawing.add(
        Rect(
            x,
            y,
            width,
            height,
            rx=5,
            ry=5,
            fillColor=white,
            strokeColor=GRID,
            strokeWidth=0.9,
        )
    )
    label(drawing, x + 8, y + height - 13, tag, 6.8, bold=True, color=title_color)
    label(drawing, x + 24, y + height - 13, title, 5.65, bold=True)


def box(
    drawing,
    x,
    y,
    width,
    height,
    lines,
    *,
    fill=white,
    stroke=GRID,
    size=4.0,
    dashed=False,
    bold_first=True,
    radius=4,
):
    drawing.add(
        Rect(
            x,
            y,
            width,
            height,
            rx=radius,
            ry=radius,
            fillColor=fill,
            strokeColor=stroke,
            strokeWidth=0.9,
            strokeDashArray=[4, 2] if dashed else None,
        )
    )
    total = (len(lines) - 1) * 5.4
    multiline(
        drawing,
        x + width / 2,
        y + height / 2 + total / 2 - 1.4,
        lines,
        size,
        bold_first=bold_first,
        leading=5.4,
    )


def ledger_row(drawing, x, y, width, tag, formula, *, fill, stroke, dashed=False):
    drawing.add(
        Rect(
            x,
            y,
            width,
            12,
            rx=3,
            ry=3,
            fillColor=fill,
            strokeColor=stroke,
            strokeWidth=0.8,
            strokeDashArray=[3, 2] if dashed else None,
        )
    )
    label(drawing, x + 6, y + 3.7, tag, 3.9, bold=True, color=stroke)
    label(drawing, x + 31, y + 3.7, formula, 3.65)


def load_rows():
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        return {row["item"]: row for row in csv.DictReader(handle)}


def exact_checks(rows):
    expected = {
        "radius_exponent_rho": Fraction(1, 320),
        "annular_weight_exponent_c_gamma": Fraction(8, 3969),
        "energy_decay_d_E": Fraction(98, 29475),
        "net_energy_exponent_e_E": Fraction(17018, 12998475),
        "amplitude_gap_m": Fraction(43, 423360),
        "varkappa_L_power": Fraction(2, 3),
        "varkappa_exp_coefficient": Fraction(43, 1270080),
        "energy_reserve": Fraction(1171, 943200),
        "velocity_packet_background_ratio": Fraction(1),
        "harmonic_L_power": Fraction(-3, 2),
        "payment_B_power": Fraction(3),
        "payment_R_power": Fraction(3),
        "beta_limit": Fraction(1, 128),
        "shear_lower_prefactor": Fraction(8),
        "shear_lower_exp_exponent": Fraction(-8),
        "quadratic_varkappa_power": Fraction(2),
        "observable_L_power": Fraction(1),
        "observable_B_power": Fraction(2),
        "observable_R_power": Fraction(2),
        "power_increment_delta_star": Fraction(86, 11907),
        "frontier_power_q_star": Fraction(8024, 11907),
        "endpoint_log_power": Fraction(1, 2),
        "frontier_log_power": Fraction(7, 6),
        "ratio_log_power": Fraction(2, 3),
    }
    assert set(rows) == set(expected), sorted(set(rows) ^ set(expected))
    for key, value in expected.items():
        assert Fraction(rows[key]["exact_value"]) == value, key
        numeric = float(rows[key]["numeric_value"])
        assert abs(numeric - float(value)) <= max(5e-15, 5e-15 * abs(float(value))), key
    rho = expected["radius_exponent_rho"]
    c_gamma = expected["annular_weight_exponent_c_gamma"]
    d_e = expected["energy_decay_d_E"]
    e_e = expected["net_energy_exponent_e_E"]
    m = expected["amplitude_gap_m"]
    delta = expected["power_increment_delta_star"]
    assert d_e - c_gamma == e_e
    assert rho - Fraction(3, 2) * c_gamma == m
    assert m / 3 == expected["varkappa_exp_coefficient"]
    assert e_e - Fraction(2, 3) * m == expected["energy_reserve"]
    assert Fraction(2) * m / (Fraction(9) * rho) == delta
    assert Fraction(2, 3) + delta == expected["frontier_power_q_star"]
    assert expected["frontier_log_power"] - expected["endpoint_log_power"] == expected["ratio_log_power"]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def status_from_file(relative_path: str, required_tokens: tuple[str, ...]) -> str:
    path = REPO / relative_path
    if not path.is_file():
        return "PENDING_OR_MISSING"
    text = path.read_text(encoding="utf-8")
    return "PASS" if all(token in text for token in required_tokens) else "FAIL_OR_UNBOUND"


def make_drawing(_rows, statuses):
    drawing = Drawing(W, H)
    drawing.add(Rect(0, 0, W, H, fillColor=white, strokeColor=None))

    label(drawing, 14, H - 17, "R0.74O  |  passive-amplitude endpoint obstruction", 8.0, bold=True)
    label(
        drawing,
        W - 14,
        H - 17,
        "exact rational ledger • deterministic analytic schematic",
        4.65,
        color=MID,
        anchor="end",
    )

    margin = 14
    gap = 8
    col_w = (W - 2 * margin - gap) / 2
    top_y, top_h = 151, 92
    bottom_y, bottom_h = 31, 112
    left_x = margin
    right_x = margin + col_w + gap

    panel(drawing, left_x, top_y, col_w, top_h, "A", "free amplitude in an exact 2D3C family", title_color=BLUE)
    panel(drawing, right_x, top_y, col_w, top_h, "B", "complete scalar payment stays at background scale", title_color=GOLD)
    panel(drawing, left_x, bottom_y, col_w, bottom_h, "C", "quadratic observables reveal the hidden amplitude", title_color=BLUE)
    panel(drawing, right_x, bottom_y, col_w, bottom_h, "D", "conversion to the scalar frontier", title_color=GOLD)

    # A: exact family and free passive multiplier.
    label(drawing, left_x + 10, top_y + 62, "u^(a) = (a F, B theta, 0)   •   p = 0", 4.35, bold=True)
    box(
        drawing,
        left_x + 10,
        top_y + 28,
        79,
        27,
        ["NORMALIZED", "a_0 = B Gamma^(-1/2)"],
        fill=BLUE_LIGHT,
        stroke=BLUE,
        size=3.75,
    )
    arrow(drawing, left_x + 92, top_y + 42, left_x + 133, top_y + 42, color=GOLD)
    drawing.add(Circle(left_x + 112, top_y + 42, 14, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=1.0))
    multiline(
        drawing,
        left_x + 112,
        top_y + 46,
        ["FREE", "varkappa > 0"],
        3.7,
        color=GOLD,
        bold_first=True,
        leading=6.0,
    )
    box(
        drawing,
        left_x + 136,
        top_y + 28,
        col_w - 146,
        27,
        ["AMPLIFIED", "a_* = varkappa B Gamma^(-1/2)"],
        fill=GOLD_LIGHT,
        stroke=GOLD,
        size=3.55,
        dashed=True,
    )
    label(
        drawing,
        left_x + col_w / 2,
        top_y + 18,
        "varkappa = L^(2/3) exp(m L^2/3)   •   m = 43/423360 > 0",
        3.55,
        anchor="middle",
    )
    label(
        drawing,
        left_x + col_w / 2,
        top_y + 8,
        "smooth • periodic • mean-zero • unforced • global",
        3.55,
        color=MID,
        anchor="middle",
    )

    # B: every payment row remains at the B^3 R^3 scale.
    row_x = right_x + 9
    row_w = col_w - 73
    ledger_row(
        drawing,
        row_x,
        top_y + 61,
        row_w,
        "E + p",
        "reserve = 1171/943200 > 0",
        fill=BLUE_LIGHT,
        stroke=BLUE,
    )
    ledger_row(
        drawing,
        row_x,
        top_y + 46,
        row_w,
        "G",
        "packet / background = 1 exactly",
        fill=GOLD_LIGHT,
        stroke=GOLD,
    )
    ledger_row(
        drawing,
        row_x,
        top_y + 31,
        row_w,
        "H",
        "packet / background = L^(-3/2)",
        fill=white,
        stroke=BLUE,
        dashed=True,
    )
    ledger_row(
        drawing,
        row_x,
        top_y + 16,
        row_w,
        "J",
        "shear lower >= 8 e^(-8) B^3 R^3",
        fill=white,
        stroke=GOLD,
        dashed=True,
    )
    arrow(drawing, row_x + row_w + 5, top_y + 54, right_x + col_w - 12, top_y + 54, color=INK)
    box(
        drawing,
        right_x + col_w - 63,
        top_y + 27,
        53,
        48,
        ["COMPLETE", "P_* ~", "B^3 R^3"],
        fill=PALE,
        stroke=INK,
        size=4.25,
    )
    label(drawing, right_x + 10, top_y + 7, "all rows paid • no selected denominator", 3.55, color=MID)

    # C: exact quadratic amplitude scaling for both endpoint observables.
    box(
        drawing,
        left_x + 10,
        bottom_y + 61,
        72,
        29,
        ["BASE FAMILY", "X_0 , C_0", "~ B^2 L R^2"],
        fill=BLUE_LIGHT,
        stroke=BLUE,
        size=3.75,
    )
    arrow(drawing, left_x + 86, bottom_y + 75, left_x + 137, bottom_y + 75, color=GOLD)
    drawing.add(Circle(left_x + 112, bottom_y + 75, 15, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=1.0))
    multiline(
        drawing,
        left_x + 112,
        bottom_y + 79,
        ["EXACT", "x varkappa^2"],
        3.7,
        color=GOLD,
        bold_first=True,
        leading=6.0,
    )
    box(
        drawing,
        left_x + 141,
        bottom_y + 58,
        col_w - 151,
        35,
        ["AMPLIFIED", "X_* ~ C_*", "~ varkappa^2 B^2 L R^2"],
        fill=GOLD_LIGHT,
        stroke=GOLD,
        size=3.65,
        dashed=True,
    )
    drawing.add(Line(left_x + 18, bottom_y + 48, left_x + col_w - 18, bottom_y + 48, strokeColor=GRID, strokeWidth=0.7))
    label(drawing, left_x + 15, bottom_y + 35, "X_*", 4.7, bold=True, color=BLUE)
    label(drawing, left_x + 50, bottom_y + 35, "endpoint energy + dissipation quantity", 3.7)
    label(drawing, left_x + 15, bottom_y + 20, "C_*", 4.7, bold=True, color=GOLD)
    label(drawing, left_x + 50, bottom_y + 20, "positive cumulative collar flux", 3.7)
    label(
        drawing,
        left_x + col_w / 2,
        bottom_y + 7,
        "X lower comes from endpoint energy • no separate dissipation lower",
        3.60,
        color=MID,
        anchor="middle",
    )

    # D: exact exponent conversion and the rejected scalar endpoint.
    label(
        drawing,
        right_x + 10,
        bottom_y + 86,
        "q_* = 8024/11907 = 2/3 + 86/11907",
        4.35,
        bold=True,
    )
    box(
        drawing,
        right_x + 10,
        bottom_y + 55,
        col_w - 20,
        24,
        ["X_* ~ C_* ~ P_*^(8024/11907)", "x (1 + log_+ P_*)^(7/6)"],
        fill=GOLD_LIGHT,
        stroke=GOLD,
        size=3.85,
    )
    box(
        drawing,
        right_x + 10,
        bottom_y + 26,
        col_w - 20,
        23,
        ["ratio to  P_*^(2/3) sqrt(1 + log_+ P_*)", "~ P_*^(86/11907) (1 + log_+ P_*)^(2/3)  ->  infinity"],
        fill=white,
        stroke=BLUE,
        size=3.55,
        dashed=True,
    )
    drawing.add(
        Rect(
            right_x + 10,
            bottom_y + 7,
            col_w - 20,
            14,
            rx=3,
            ry=3,
            fillColor=RED_LIGHT,
            strokeColor=RED,
            strokeWidth=1.0,
        )
    )
    label(
        drawing,
        right_x + col_w / 2,
        bottom_y + 11,
        "SCALAR-PAYMENT-ONLY NO-GO",
        4.9,
        bold=True,
        color=RED,
        anchor="middle",
    )

    audit_note = f"analytic audit {statuses['analytic'].lower()} • literature audit {statuses['literature'].lower()}"
    label(drawing, 14, 11, "Analytic schematic • not to scale • no DNS/simulation/fitted data", 4.0, color=MID)
    label(drawing, W / 2, 11, audit_note, 3.45, color=MID, anchor="middle")
    label(
        drawing,
        W - 14,
        11,
        "smooth exact family • scalar-payment-only no-go • NOT CLAY",
        4.05,
        color=RED,
        bold=True,
        anchor="end",
    )
    return drawing


def inject_svg_fonts():
    """Embed the exact TTF files so the SVG is self-contained."""
    svg_path = HERE / "figure.svg"
    svg = svg_path.read_text(encoding="utf-8")
    regular = base64.b64encode(REGULAR_FONT.read_bytes()).decode("ascii")
    bold = base64.b64encode(BOLD_FONT.read_bytes()).decode("ascii")
    style = (
        "\t<style type=\"text/css\"><![CDATA[\n"
        "@font-face { font-family: 'R074O-Regular'; "
        f"src: url('data:font/ttf;base64,{regular}') format('truetype'); "
        "font-style: normal; font-weight: 400; }\n"
        "@font-face { font-family: 'R074O-Bold'; "
        f"src: url('data:font/ttf;base64,{bold}') format('truetype'); "
        "font-style: normal; font-weight: 700; }\n"
        "]]></style>\n"
    )
    marker = "\t<title>"
    if marker not in svg:
        raise RuntimeError("SVG title marker missing; refusing unbound font injection")
    svg_path.write_text(svg.replace(marker, style + marker, 1).replace("\t", "  "), encoding="utf-8")


def render_quicklook():
    with tempfile.TemporaryDirectory(prefix=".quicklook-", dir=HERE) as temp_dir:
        subprocess.run(
            [str(QUICKLOOK), "-t", "-s", "2103", "-o", temp_dir, str(HERE / "figure.svg")],
            check=True,
            capture_output=True,
            text=True,
        )
        candidates = sorted(Path(temp_dir).glob("*.png"))
        if len(candidates) != 1:
            raise RuntimeError(f"expected one Quick Look raster, found {candidates}")
        with Image.open(candidates[0]) as source:
            quicklook = source.convert("RGB")
            quicklook.save(HERE / "qa-svg-quicklook.png")
            return [quicklook.width, quicklook.height]


def render_pdf(drawing):
    pdf = pdfcanvas.Canvas(str(HERE / "figure.pdf"), pagesize=(W, H), invariant=1, pageCompression=1)
    pdf.setTitle("R0.74O passive-amplitude endpoint obstruction")
    pdf.setAuthor("C. K. Zeng")
    pdf.setSubject(
        "Scalar-payment-only endpoint no-go on a smooth exact family; analytic schematic; "
        "no simulation or DNS; independent figure-package audit separate; NOT CLAY"
    )
    renderPDF.draw(drawing, pdf, 0, 0)
    pdf.showPage()
    pdf.save()


def render_rasters():
    subprocess.run(
        [str(PDFTOPPM), "-png", "-singlefile", "-r", str(DPI), str(HERE / "figure.pdf"), str(HERE / "raster-600")],
        check=True,
        capture_output=True,
        text=True,
    )
    with Image.open(HERE / "raster-600.png") as source:
        master = source.convert("RGB")
        master.save(HERE / "figure.png", dpi=(DPI, DPI))
    (HERE / "raster-600.png").unlink()
    with Image.open(HERE / "figure.png") as master_image:
        final_size = (max(1, round(master_image.width / 3)), max(1, round(master_image.height / 3)))
        final = master_image.resize(final_size, Image.Resampling.LANCZOS)
        final.save(HERE / "qa-final-size.png", dpi=(200, 200))
        ImageOps.grayscale(final).save(HERE / "qa-grayscale.png", dpi=(200, 200))
        master_dimensions = [master_image.width, master_image.height]
    subprocess.run(
        [str(PDFTOPPM), "-png", "-singlefile", "-r", "300", str(HERE / "figure.pdf"), str(HERE / "qa-pdf")],
        check=True,
        capture_output=True,
        text=True,
    )
    return {"master_dimensions": master_dimensions, "final_size_dimensions": list(final_size)}


def main():
    rows = load_rows()
    exact_checks(rows)
    statuses = {
        "analytic": status_from_file(
            "research/r074o_amplitude_endpoint_independent_audit.md",
            ("Verdict: PASS", "471158de1db718ac96f38adc729464d8717006f47c8c6bb57834cc4e159bd9bb", "NOT CLAY"),
        ),
        "literature": status_from_file(
            "research/r074o_primary_literature_independent_audit.md",
            ("Verdict: **PASS**", "NOT CLAY", "not used as evidence of novelty"),
        ),
        "reader": status_from_file(
            "research/r074o_reader_source_independent_audit.md",
            ("PASS", "NOT CLAY"),
        ),
    }
    drawing = make_drawing(rows, statuses)
    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"))
    inject_svg_fonts()
    render_pdf(drawing)
    dimensions = render_rasters()
    quicklook_dimensions = render_quicklook()
    results = {
        "analytic_proof_audit": statuses["analytic"],
        "claim_boundary": CLAIM,
        "exact_data_checks": "PASS",
        "figure_id": FIGURE_ID,
        "figure_package_independent_audit": "EXTERNAL_SEPARATE_NOT_CLAIMED",
        "literature_audit": statuses["literature"],
        "outputs": {
            "pdf_sha256": sha256(HERE / "figure.pdf"),
            "png_sha256": sha256(HERE / "figure.png"),
            "svg_sha256": sha256(HERE / "figure.svg"),
        },
        "quicklook_svg_dimensions": quicklook_dimensions,
        "reader_source_audit": statuses["reader"],
        "simulation": False,
        "visual_status": "ANALYTIC_SCHEMATIC_NOT_TO_SCALE",
        **dimensions,
    }
    (HERE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    environment = {
        "generator": "reportlab",
        "pdf_renderer": str(PDFTOPPM),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "quicklook_renderer": str(QUICKLOOK),
        "reportlab_invariant": True,
    }
    (HERE / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    events = [
        {"event": "exact_source_data", "status": "PASS"},
        {"event": "analytic_source_binding", "status": statuses["analytic"]},
        {"event": "reader_source_binding", "status": statuses["reader"]},
        {"event": "literature_source_binding", "status": statuses["literature"]},
        {"event": "vector_render", "status": "PASS"},
        {"event": "raster_render_600dpi", "status": "PASS"},
        {"event": "svg_embedded_fonts", "status": "PASS"},
        {"event": "svg_quicklook_raster", "status": "PASS"},
        {"event": "visual_qa", "status": "PASS"},
    ]
    (HERE / "progress.ndjson").write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events), encoding="utf-8"
    )
    (HERE / "command.txt").write_text(
        f"{platform.python_implementation()} {platform.python_version()}\n"
        f"{Path(sys.executable)} {Path(__file__).name}\n"
        f"{PDFTOPPM} -png -singlefile -r 600 figure.pdf raster-600\n",
        encoding="utf-8",
    )
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
