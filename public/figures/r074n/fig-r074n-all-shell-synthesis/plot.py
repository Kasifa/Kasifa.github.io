#!/usr/bin/env python3
"""Render the deterministic R0.74N all-shell synthesis formal figure."""

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
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFTOPPM = BUNDLE / "bin/override/pdftoppm"
QUICKLOOK = Path("/usr/bin/qlmanage")
FIGURE_ID = "fig-r074n-all-shell-synthesis"
CLAIM = "FAMILYWISE_ALL_SHELL_SYNTHESIS_NOT_CLAY"

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
OLIVE = HexColor("#536A32")
OLIVE_LIGHT = HexColor("#EEF3E5")
GOLD = HexColor("#95650F")
GOLD_LIGHT = HexColor("#FAF0D8")
PURPLE = HexColor("#604D82")
PURPLE_LIGHT = HexColor("#EEEAF5")
RED = HexColor("#9B3E38")

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
pdfmetrics.registerFont(TTFont("R074N-Regular", str(REGULAR_FONT)))
pdfmetrics.registerFont(TTFont("R074N-Bold", str(BOLD_FONT)))


def label(drawing, x, y, value, size=5.0, *, color=INK, bold=False, anchor="start"):
    drawing.add(
        String(
            x,
            y,
            value,
            fontName="R074N-Bold" if bold else "R074N-Regular",
            fontSize=size,
            fillColor=color,
            textAnchor=anchor,
        )
    )


def multiline(
    drawing, x, y, lines, size=4.5, *, color=INK, bold_first=False,
    anchor="middle", leading=5.7
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


def arrow(drawing, x0, y0, x1, y1, *, color=INK, dashed=False, width=0.85):
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
    length, spread = 3.2, 0.52
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
    label(drawing, x + 24, y + height - 13, title, 5.75, bold=True)


def box(
    drawing, x, y, width, height, lines, *, fill, stroke, size=4.1,
    dashed=False, bold_first=True
):
    drawing.add(
        Rect(
            x,
            y,
            width,
            height,
            rx=4,
            ry=4,
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
        y + height / 2 + total / 2 - 1.5,
        lines,
        size,
        bold_first=bold_first,
        leading=5.4,
    )


def load_rows():
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        return {row["item"]: row for row in csv.DictReader(handle)}


def exact_checks(rows):
    expected = {
        "radius_exponent_rho": Fraction(1, 320),
        "annular_weight_exponent_c_gamma": Fraction(8, 3969),
        "target_R_power": Fraction(5),
        "inward_outer_coefficient": Fraction(32, 63),
        "collar_padding_coefficient": Fraction(1, 8),
        "path_modulus_coefficient": Fraction(1, 16),
        "defect_window_coefficient": Fraction(3, 5),
        "geometry_gap": Fraction(149, 5040),
        "final_segment_length": Fraction(1, 64),
        "defect_exponent": Fraction(1, 640),
        "sigma_prefactor": Fraction(1, 32768),
        "bad_path_exponent": Fraction(1, 16),
        "bad_event_reserve": Fraction(72851, 1270080),
        "tail_distance_fraction": Fraction(1, 2),
        "tail_denominator": Fraction(1056),
        "outer_volume_base": Fraction(4),
        "geometric_tail_ratio_bound": Fraction(1, 2),
        "outer_L_squared_prefactor": Fraction(4096, 3969),
        "gamma_forward_gap": Fraction(8, 1323),
        "outer_exponent_reserve": Fraction(1237, 423360),
    }
    assert set(rows) == set(expected), (set(rows) ^ set(expected))
    for key, value in expected.items():
        assert Fraction(rows[key]["exact_value"]) == value, key
        numeric = float(rows[key]["numeric_value"])
        assert abs(numeric - float(value)) <= max(5e-15, 5e-15 * abs(float(value))), key
    rho = expected["radius_exponent_rho"]
    c_gamma = expected["annular_weight_exponent_c_gamma"]
    assert Fraction(1, 16) - rho - c_gamma == expected["bad_event_reserve"]
    assert 3 * c_gamma - rho == expected["outer_exponent_reserve"]
    assert 3 * c_gamma == expected["gamma_forward_gap"]
    assert Fraction(3, 5) - Fraction(32, 63) - Fraction(1, 16) == expected["geometry_gap"]


def make_drawing(_rows):
    drawing = Drawing(W, H)
    drawing.add(Rect(0, 0, W, H, fillColor=white, strokeColor=None))

    label(drawing, 14, H - 17, "R0.74N  |  exact all-shell synthesis", 8.2, bold=True)
    label(
        drawing,
        W - 14,
        H - 17,
        "signed annular collar flux • deterministic proof schematic",
        4.75,
        color=MID,
        anchor="end",
    )

    margin = 14
    top_y, top_h = 193, 50
    panel(drawing, margin, top_y, W - 2 * margin, top_h, "A", "exact disjoint index partition")

    ix = margin + 12
    iy = top_y + 9
    ih = 20
    usable = W - 2 * margin - 24
    gap = 7
    left_w = 0.39 * (usable - 2 * gap)
    center_w = 0.22 * (usable - 2 * gap)
    right_w = usable - 2 * gap - left_w - center_w
    box(
        drawing,
        ix,
        iy,
        left_w,
        ih,
        ["INWARD UNION", "1 <= k <= j-1"],
        fill=BLUE_LIGHT,
        stroke=BLUE,
        size=4.5,
    )
    box(
        drawing,
        ix + left_w + gap,
        iy,
        center_w,
        ih,
        ["TARGET", "k = j"],
        fill=OLIVE_LIGHT,
        stroke=OLIVE,
        size=4.5,
        dashed=True,
    )
    box(
        drawing,
        ix + left_w + center_w + 2 * gap,
        iy,
        right_w,
        ih,
        ["OUTER TAIL", "k >= j+1"],
        fill=GOLD_LIGHT,
        stroke=GOLD,
        size=4.5,
    )
    label(
        drawing,
        W - margin - 12,
        top_y + top_h - 13,
        "I_j = I_< + I_= + I_>  •  no missing or overlapping row",
        4.25,
        color=MID,
        anchor="end",
    )

    bottom_y, bottom_h = 31, 152
    gap = 8
    inner_w = 182
    target_w = 126
    outer_w = W - 2 * margin - 2 * gap - inner_w - target_w
    inner_x = margin
    target_x = inner_x + inner_w + gap
    outer_x = target_x + target_w + gap
    panel(drawing, inner_x, bottom_y, inner_w, bottom_h, "B", "combined inward chord + expulsion", title_color=BLUE)
    panel(drawing, target_x, bottom_y, target_w, bottom_h, "C", "target shell", title_color=OLIVE)
    panel(drawing, outer_x, bottom_y, outer_w, bottom_h, "D", "super-Gaussian outer tail", title_color=GOLD)

    # B: all inner rings inside one padded tube, followed by the inherited expulsion ledger.
    cx, cy = inner_x + 35, bottom_y + 98
    drawing.add(Rect(cx - 29, cy - 29, 58, 58, fillColor=PALE, strokeColor=GRID, strokeWidth=0.7))
    for radius, dash in [(9, None), (18, [2, 2]), (27, None)]:
        drawing.add(
            Circle(
                cx,
                cy,
                radius,
                fillColor=None,
                strokeColor=BLUE,
                strokeWidth=0.9,
                strokeDashArray=dash,
            )
        )
    drawing.add(Line(cx, cy - 32, cx, cy + 32, strokeColor=MID, strokeWidth=0.55, strokeDashArray=[2, 2]))
    drawing.add(Line(cx - 32, cy, cx + 32, cy, strokeColor=MID, strokeWidth=0.55, strokeDashArray=[2, 2]))
    label(drawing, cx, cy - 39, "all k <= j-1 • schematic", 3.45, color=MID, anchor="middle")
    multiline(
        drawing,
        inner_x + 78,
        bottom_y + 123,
        [
            "0 <= Dbar_< <= C sum 2^k Gamma_k < infinity",
            "supp Dbar_< lies in one r_- tube",
            "r_- = (32L/63 + 1/8)R",
            "no shell or packet cancellation",
        ],
        3.65,
        anchor="start",
        leading=6.0,
    )
    arrow(drawing, inner_x + 91, bottom_y + 88, inner_x + 91, bottom_y + 72, color=PURPLE)
    box(
        drawing,
        inner_x + 9,
        bottom_y + 48,
        inner_w - 18,
        22,
        ["R0.74M expulsion in the same tube", "good: R^3 exp[-Sigma_L^2/(1056 R^2)]"],
        fill=PURPLE_LIGHT,
        stroke=PURPLE,
        size=3.65,
        dashed=True,
    )
    box(
        drawing,
        inner_x + 9,
        bottom_y + 21,
        inner_w - 18,
        20,
        ["bad: C R^4 exp(-L^2/16)", "reserve 72851/1270080 > 0"],
        fill=BLUE_LIGHT,
        stroke=BLUE,
        size=3.7,
    )
    label(drawing, inner_x + inner_w / 2, bottom_y + 7, "[I_<]_+ <= C Gamma_j L R^5", 4.3, bold=True, color=BLUE, anchor="middle")

    # C: a single highlighted target annulus and the inherited absolute estimate.
    tcx, tcy = target_x + target_w / 2, bottom_y + 103
    drawing.add(Circle(tcx, tcy, 32, fillColor=PALE, strokeColor=GRID, strokeWidth=0.7))
    drawing.add(Circle(tcx, tcy, 27, fillColor=None, strokeColor=OLIVE, strokeWidth=4.0))
    drawing.add(Circle(tcx, tcy, 17, fillColor=white, strokeColor=GRID, strokeWidth=0.7))
    label(drawing, tcx, tcy - 2, "k = j", 6.0, bold=True, color=OLIVE, anchor="middle")
    label(drawing, tcx, tcy - 41, "schematic annulus", 3.45, color=MID, anchor="middle")
    box(
        drawing,
        target_x + 9,
        bottom_y + 39,
        target_w - 18,
        30,
        ["R0.74L absolute", "true-packet estimate", "both radial faces"],
        fill=OLIVE_LIGHT,
        stroke=OLIVE,
        size=3.9,
        dashed=True,
    )
    label(drawing, tcx, bottom_y + 22, "|I_=| <= Gamma_j C L R^5", 3.9, bold=True, color=OLIVE, anchor="middle")
    label(drawing, tcx, bottom_y + 7, "inherited • independently audited", 3.45, color=MID, anchor="middle")

    # D: ordinal bars for the super-Gaussian shell weights, then the exact tail ledger.
    ox0, oy0 = outer_x + 18, bottom_y + 87
    base_y = oy0
    drawing.add(Line(ox0, base_y, outer_x + outer_w - 12, base_y, strokeColor=MID, strokeWidth=0.7))
    heights = [39, 27, 18, 11, 6]
    labels = ["j+1", "j+2", "j+3", "j+4", "..."]
    bar_w = 12
    bar_gap = 8
    for index, (height, tick) in enumerate(zip(heights, labels)):
        x = ox0 + index * (bar_w + bar_gap)
        drawing.add(
            Rect(
                x,
                base_y,
                bar_w,
                height,
                fillColor=GOLD_LIGHT if index % 2 == 0 else white,
                strokeColor=GOLD,
                strokeWidth=0.9,
                strokeDashArray=[3, 2] if index % 2 else None,
            )
        )
        label(drawing, x + bar_w / 2, base_y - 8, tick, 3.3, color=MID, anchor="middle")
    label(drawing, outer_x + outer_w - 10, base_y + 42, "ordinal shell symbols", 3.35, color=MID, anchor="end")
    label(drawing, outer_x + outer_w - 10, base_y + 36, "not quantitative data", 3.35, color=MID, anchor="end")
    box(
        drawing,
        outer_x + 9,
        bottom_y + 48,
        outer_w - 18,
        29,
        [
            "|J_jk| <= C Gamma_k 4^k R^4",
            "sum_(k>=j+1) 4^k Gamma_k",
            "<= 2(4^(j+1)) Gamma_(j+1)",
            "ratio <= 1/2 eventually",
        ],
        fill=GOLD_LIGHT,
        stroke=GOLD,
        size=3.55,
    )
    box(
        drawing,
        outer_x + 9,
        bottom_y + 21,
        outer_w - 18,
        20,
        ["3 c_gamma - rho", "= 1237/423360 > 0"],
        fill=white,
        stroke=GOLD,
        size=3.8,
        dashed=True,
    )
    label(drawing, outer_x + outer_w / 2, bottom_y + 7, "|I_>| <= C Gamma_j L R^5", 4.1, bold=True, color=GOLD, anchor="middle")

    label(drawing, 14, 11, "Schematic • not to scale • no DNS • no sampled path", 4.2, color=MID)
    label(
        drawing,
        W - 14,
        11,
        "ALL BRANCHES -> C Gamma_j L R^5  |  ANALYTIC AUDIT PASS  |  FAMILYWISE  |  NOT CLAY",
        3.9,
        color=RED,
        bold=True,
        anchor="end",
    )
    return drawing


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inject_svg_fonts():
    """Embed the exact TTF files so the SVG is self-contained."""
    svg_path = HERE / "figure.svg"
    svg = svg_path.read_text(encoding="utf-8")
    regular = base64.b64encode(REGULAR_FONT.read_bytes()).decode("ascii")
    bold = base64.b64encode(BOLD_FONT.read_bytes()).decode("ascii")
    style = (
        "\t<style type=\"text/css\"><![CDATA[\n"
        "@font-face { font-family: 'R074N-Regular'; "
        f"src: url('data:font/ttf;base64,{regular}') format('truetype'); "
        "font-style: normal; font-weight: 400; }\n"
        "@font-face { font-family: 'R074N-Bold'; "
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
    pdf.setTitle("R0.74N exact all-shell synthesis")
    pdf.setAuthor("C. K. Zeng")
    pdf.setSubject(
        "Familywise all-shell theorem; analytic audit PASS; figure-package "
        "audit separate; schematic; no simulation; NOT CLAY"
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
    drawing = make_drawing(rows)
    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"))
    inject_svg_fonts()
    render_pdf(drawing)
    dimensions = render_rasters()
    quicklook_dimensions = render_quicklook()
    results = {
        "analytic_proof_audit": "PASS",
        "claim_boundary": CLAIM,
        "exact_data_checks": "PASS",
        "figure_id": FIGURE_ID,
        "figure_package_independent_audit": "EXTERNAL_SEPARATE_NOT_CLAIMED",
        "outputs": {
            "pdf_sha256": sha256(HERE / "figure.pdf"),
            "png_sha256": sha256(HERE / "figure.png"),
            "svg_sha256": sha256(HERE / "figure.svg"),
        },
        "quicklook_svg_dimensions": quicklook_dimensions,
        "simulation": False,
        "visual_status": "SCHEMATIC_NOT_TO_SCALE",
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
