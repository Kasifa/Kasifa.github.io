#!/usr/bin/env python3
"""Generate the deterministic R0.74E outer-annulus finite-gate figure package.

The certificate is the sole quantitative input.  The drawing is an analytic
schematic, not DNS and not a packet-survival computation.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import sys
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


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074e_outer_annulus_exponent_certificate.json"
SOURCE_NOTE = REPO / "research/r074e_local_mollified_frame_gate.md"
EXPECTED_CERT_SHA256 = "c6b7f0b9d11a58568c588dd3116e66fbdb9d7d5b5383493c9b492bf6cdba4372"
EXPECTED_SOURCE_NOTE_SHA256 = "3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7"
FIGURE_ID = "fig-r074e-outer-annulus-frame-gate"

WIDTH_MM = 180
HEIGHT_MM = 82
DPI = 600
W = WIDTH_MM * mm
H = HEIGHT_MM * mm

INK = HexColor("#202A34")
MID = HexColor("#5D6873")
LIGHT = HexColor("#E7EBEF")
XLIGHT = HexColor("#F6F8FA")
BLUE = HexColor("#1F5A91")
BLUE_LIGHT = HexColor("#E7F0F7")
GOLD = HexColor("#A87312")
GOLD_LIGHT = HexColor("#FBF3DF")

rl_config.invariant = 1


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def locate_font(filename: str) -> Path:
    candidates = [
        Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype") / filename,
        Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler") / filename,
        Path("/System/Library/Fonts/Supplemental") / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"required font not found: {filename}")


FONT_REGULAR = locate_font("DejaVuSans.ttf")
FONT_BOLD = locate_font("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074E-Regular", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("R074E-Bold", str(FONT_BOLD)))


def frac(value: str) -> Fraction:
    return Fraction(value)


def load_exact() -> tuple[dict, dict[str, Fraction]]:
    if sha256(CERTIFICATE) != EXPECTED_CERT_SHA256:
        raise RuntimeError("certificate hash mismatch; freeze or update the figure contract")
    if sha256(SOURCE_NOTE) != EXPECTED_SOURCE_NOTE_SHA256:
        raise RuntimeError("source-note hash mismatch; freeze or update the figure contract")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate.get("status") != "PASS" or certificate.get("summary") != {"passed": 13, "total": 13}:
        raise RuntimeError("certificate is not the frozen 13/13 PASS object")
    inputs = certificate["inputs"]
    values = {
        "lambda": frac(inputs["lambda"]),
        "c_h": frac(inputs["c_h"]),
        "alpha": frac(inputs["alpha"]),
        "beta_squared": frac(inputs["beta_squared"]),
        "c_R": frac(inputs["c_R"]),
        "kappa": frac(inputs["kappa"]),
        "L_min": frac(inputs["L_min"]),
        "c_gamma": frac(certificate["derived"]["c_gamma"]),
        "window_lower": frac(certificate["derived"]["packet_Gu_lower"]),
        "window_upper": frac(certificate["derived"]["heat_isolation_upper"]),
        "leakage_exponent": frac(certificate["derived"]["local_leakage_exponent"]),
    }
    values.update({
        "window_lower_margin": values["c_R"] - values["window_lower"],
        "window_upper_margin": values["window_upper"] - values["c_R"],
        "leakage_margin": values["leakage_exponent"] - values["c_gamma"],
        "leakage_inverse_R_margin": values["leakage_exponent"] - values["c_R"],
        "buffer_gap": values["c_h"] - values["alpha"],
        "annulus_inner_over_r": 1 / values["lambda"],
        "annulus_outer_over_r": 2 / values["lambda"],
        "outer_edge_gap_over_r": 2 / values["lambda"] - 1,
        "transition_bound_over_r": 2 * values["kappa"] / values["L_min"],
    })
    return certificate, values


def write_source_data(values: dict[str, Fraction]) -> None:
    rows = [
        ("A", "lambda", values["lambda"], "parameter", "PROVED", "target radius lies in the dyadic annulus"),
        ("A", "c_h", values["c_h"], "parameter", "PROVED", "vertical target fraction"),
        ("A", "alpha", values["alpha"], "parameter", "PROVED", "reserved transition separation"),
        ("A", "beta_squared", values["beta_squared"], "parameter", "PROVED", "horizontal fraction squared"),
        ("A", "c_R", values["c_R"], "chosen exponent", "PROVED", "chosen radius exponent"),
        ("A", "window_lower", values["window_lower"], "lower bound", "PROVED", "packet-G_u dominance gate"),
        ("A", "window_upper", values["window_upper"], "upper bound", "PROVED", "65 R^2 caloric-isolation gate"),
        ("A", "window_lower_margin", values["window_lower_margin"], "strict margin", "PROVED", "c_R minus lower gate"),
        ("A", "window_upper_margin", values["window_upper_margin"], "strict margin", "PROVED", "upper gate minus c_R"),
        ("A", "c_gamma", values["c_gamma"], "annular exponent", "PROVED", "1/(128 lambda^2)"),
        ("A", "leakage_exponent", values["leakage_exponent"], "leakage exponent", "PROVED", "c_h^2/264"),
        ("A", "leakage_inverse_R_margin", values["leakage_inverse_R_margin"], "strict margin", "PROVED", "transverse leakage exponent minus c_R"),
        ("A", "leakage_margin", values["leakage_margin"], "strict margin", "PROVED", "transverse leakage exponent minus c_gamma"),
        ("B", "annulus_inner_over_r", values["annulus_inner_over_r"], "normalized radius", "PROVED", "inner annular edge normalized by r_j"),
        ("B", "target_radius_over_r", Fraction(1), "normalized radius", "PROVED", "paired target radius"),
        ("B", "annulus_outer_over_r", values["annulus_outer_over_r"], "normalized radius", "PROVED", "outer annular edge normalized by r_j"),
        ("B", "outer_edge_gap_over_r", values["outer_edge_gap_over_r"], "strict geometric gap", "PROVED", "outer edge minus target radius"),
        ("B", "transition_bound_over_r", values["transition_bound_over_r"], "finite separation", "PROVED", "2 kappa/L_min"),
        ("B", "buffer_gap", values["buffer_gap"], "finite separation", "PROVED", "c_h-alpha"),
        ("B", "mollified_F_at_origin", Fraction(0), "odd-even cancellation", "PROVED", "even mollifier against inversion-odd F"),
        ("B", "mollified_b_at_origin", Fraction(0), "odd-even cancellation", "PROVED", "even mollifier against odd shear"),
        ("B", "frame_speed", Fraction(0), "frame cancellation", "PROVED", "a_R(t)=0"),
        ("B", "frame_acceleration", Fraction(0), "frame cancellation", "PROVED", "a_R'(t)=0"),
    ]
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["panel", "record", "exact_value", "decimal_value", "role", "status", "note"])
        for panel, record, value, role, status, note in rows:
            writer.writerow([panel, record, f"{value.numerator}/{value.denominator}", f"{float(value):.17g}", role, status, note])


LAYOUT: list[dict] = []


def add_text(drawing: Drawing, x: float, y: float, text: str, *, size: float = 6.2,
             color=INK, bold: bool = False, anchor: str = "start",
             container: tuple[float, float, float, float] | None = None,
             layout_id: str = "text") -> None:
    font = "R074E-Bold" if bold else "R074E-Regular"
    width = pdfmetrics.stringWidth(text, font, size)
    left = x if anchor == "start" else x - width / 2 if anchor == "middle" else x - width
    bounds = [left, y - 0.23 * size, left + width, y + 0.86 * size]
    region = list(container or (0, 0, W, H))
    within = bounds[0] >= region[0] - 0.25 and bounds[1] >= region[1] - 0.25 and bounds[2] <= region[2] + 0.25 and bounds[3] <= region[3] + 0.25
    LAYOUT.append({"id": layout_id, "text": text, "fontPt": size, "boundsPt": [round(v, 4) for v in bounds], "containerPt": [round(v, 4) for v in region], "proxyPass": within})
    drawing.add(String(x, y, text, fontName=font, fontSize=size, fillColor=color, textAnchor=anchor))


def add_multiline(drawing: Drawing, x: float, y: float, lines: list[str], *, size: float = 6.0,
                  leading: float = 7.7, color=INK, bold_first: bool = False,
                  anchor: str = "start", container=None, layout_id: str = "multi") -> None:
    for index, line in enumerate(lines):
        add_text(drawing, x, y - index * leading, line, size=size, color=color,
                 bold=bold_first and index == 0, anchor=anchor, container=container,
                 layout_id=f"{layout_id}-{index}")


def add_box(drawing: Drawing, x: float, y: float, width: float, height: float, *,
            stroke=LIGHT, fill=white, radius: float = 3.0, dash=None, line_width: float = 0.7) -> None:
    box = Rect(x, y, width, height, rx=radius, ry=radius, strokeColor=stroke,
               fillColor=fill, strokeWidth=line_width)
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)


def add_badge(drawing: Drawing, x: float, y: float, text: str, *, stroke=BLUE,
              fill=white, text_color=BLUE, width: float | None = None, dash=None,
              container=None, layout_id="badge") -> None:
    size = 5.6
    box_width = width or pdfmetrics.stringWidth(text, "R074E-Bold", size) + 10
    box = Rect(x, y, box_width, 12, rx=4, ry=4, strokeColor=stroke,
               fillColor=fill, strokeWidth=0.7)
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)
    add_text(drawing, x + box_width / 2, y + 3.55, text, size=size, color=text_color,
             bold=True, anchor="middle", container=container,
             layout_id=layout_id)


def add_arrow(drawing: Drawing, x1: float, y1: float, x2: float, y2: float, *,
              color=INK, dash=None, width: float = 0.8) -> None:
    line = Line(x1, y1, x2, y2, strokeColor=color, strokeWidth=width)
    if dash:
        line.strokeDashArray = dash
    drawing.add(line)
    angle = math.atan2(y2 - y1, x2 - x1)
    head = 4.2
    wing = 2.1
    bx = x2 - head * math.cos(angle)
    by = y2 - head * math.sin(angle)
    points = [x2, y2, bx + wing * math.sin(angle), by - wing * math.cos(angle), bx - wing * math.sin(angle), by + wing * math.cos(angle)]
    drawing.add(Polygon(points, fillColor=color, strokeColor=color, strokeWidth=0.3))


def add_blossom(drawing: Drawing, x: float, y: float) -> None:
    radius = 2.0
    for angle in (90, 18, -54, -126, 162):
        radians = math.radians(angle)
        drawing.add(Circle(x + 3.3 * math.cos(radians), y + 3.3 * math.sin(radians), radius,
                           strokeColor=BLUE, fillColor=None, strokeWidth=0.45))
    drawing.add(Circle(x, y, 1.1, strokeColor=BLUE, fillColor=GOLD, strokeWidth=0.35))


def build_drawing(values: dict[str, Fraction]) -> Drawing:
    LAYOUT.clear()
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, strokeColor=None, fillColor=white))

    add_text(d, 14, H - 16, "R0.74E outer-annulus finite frame gate", size=10.2, bold=True,
             layout_id="title")
    add_text(d, 14, H - 28, "Exact rational compatibility + odd-symmetry cancellation; packet survival remains open.",
             size=6.4, color=MID, layout_id="subtitle")
    add_blossom(d, W - 17, H - 17)
    d.add(Line(14, H - 35, W - 14, H - 35, strokeColor=LIGHT, strokeWidth=0.7))
    d.add(Line(W / 2, 25, W / 2, H - 42, strokeColor=LIGHT, strokeWidth=0.7))

    panel_a = (14, 25, W / 2 - 6, H - 39)
    panel_b = (W / 2 + 6, 25, W - 14, H - 39)

    # Panel A: exact rational windows.
    add_text(d, 16, H - 51, "A", size=8.2, bold=True, container=panel_a, layout_id="panel-a")
    add_text(d, 31, H - 51, "Exact exponent compatibility", size=7.4, bold=True,
             container=panel_a, layout_id="panel-a-title")
    add_badge(d, W / 2 - 76, H - 61, "13/13 EXACT", stroke=BLUE, fill=BLUE_LIGHT,
              width=61, container=panel_a, layout_id="badge-exact")

    add_text(d, 22, H - 74, "Nonempty radius-exponent window", size=6.25, bold=True,
             container=panel_a, layout_id="window-label")
    x_start, x_end = 32, W / 2 - 24
    y_axis = H - 99
    xmin, xmax = 0.00290, 0.00345
    map_x = lambda value: x_start + (float(value) - xmin) / (xmax - xmin) * (x_end - x_start)
    lower_x = map_x(values["window_lower"])
    chosen_x = map_x(values["c_R"])
    upper_x = map_x(values["window_upper"])
    d.add(Rect(lower_x, y_axis - 4, upper_x - lower_x, 8, strokeColor=BLUE,
               fillColor=BLUE_LIGHT, strokeWidth=0.65))
    d.add(Line(x_start, y_axis, x_end, y_axis, strokeColor=INK, strokeWidth=0.8))
    for x, label, exact in ((lower_x, "lower", "4/1323"), (upper_x, "upper", "49/14625")):
        line = Line(x, y_axis - 7, x, y_axis + 12, strokeColor=BLUE, strokeWidth=0.8)
        line.strokeDashArray = [2.4, 1.8]
        d.add(line)
        d.add(Circle(x, y_axis, 2.5, strokeColor=BLUE, fillColor=white, strokeWidth=0.9))
        add_text(d, x, y_axis + 17, f"{label}  {exact}", size=5.8, color=BLUE,
                 bold=True, anchor="middle", container=panel_a, layout_id=f"window-{label}")
    d.add(Polygon([chosen_x, y_axis + 4, chosen_x + 4, y_axis, chosen_x, y_axis - 4, chosen_x - 4, y_axis],
                  strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=1.0))
    add_text(d, chosen_x, y_axis - 15, "chosen  1/320", size=6.0, color=GOLD,
             bold=True, anchor="middle", container=panel_a, layout_id="window-chosen")

    box_y = H - 140
    add_box(d, 20, box_y, 105, 26, stroke=BLUE, fill=white)
    add_multiline(d, 72.5, box_y + 16, ["chosen - lower", "= 43/423360 > 0"],
                  size=5.7, leading=8.0, color=INK, bold_first=True, anchor="middle",
                  container=panel_a, layout_id="lower-margin")
    add_box(d, 132, box_y, 105, 26, stroke=BLUE, fill=white)
    add_multiline(d, 184.5, box_y + 16, ["upper - chosen", "= 211/936000 > 0"],
                  size=5.7, leading=8.0, color=INK, bold_first=True, anchor="middle",
                  container=panel_a, layout_id="upper-margin")

    add_text(d, 22, H - 153, "Transverse leakage exponent beats c_R and annular weight", size=6.15,
             bold=True, container=panel_a, layout_id="leakage-label")
    leak_y = H - 171
    lx0, lx1 = 36, W / 2 - 28
    lmin, lmax = 0.0018, 0.0035
    leak_map = lambda value: lx0 + (float(value) - lmin) / (lmax - lmin) * (lx1 - lx0)
    gamma_x = leak_map(values["c_gamma"])
    leak_x = leak_map(values["leakage_exponent"])
    d.add(Line(lx0, leak_y, lx1, leak_y, strokeColor=MID, strokeWidth=0.7))
    c_r_x = leak_map(values["c_R"])
    d.add(Circle(gamma_x, leak_y, 3.0, strokeColor=BLUE, fillColor=white, strokeWidth=1.0))
    d.add(Polygon([c_r_x, leak_y + 3.8, c_r_x + 3.8, leak_y, c_r_x, leak_y - 3.8, c_r_x - 3.8, leak_y],
                  strokeColor=INK, fillColor=white, strokeWidth=0.9))
    d.add(Rect(leak_x - 3, leak_y - 3, 6, 6, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=1.0))
    add_text(d, gamma_x, leak_y + 9, "c_gamma = 8/3969", size=5.65, color=BLUE,
             bold=True, anchor="middle", container=panel_a, layout_id="gamma-point")
    add_text(d, c_r_x - 5, leak_y - 13, "c_R = 1/320", size=5.55, color=INK,
             bold=True, anchor="end", container=panel_a, layout_id="inverse-r-point")
    add_text(d, W / 2 - 27, leak_y + 9, "leak = 75/22528", size=5.55, color=GOLD,
             bold=True, anchor="end", container=panel_a, layout_id="leak-point")
    add_arrow(d, gamma_x + 5, leak_y + 2, c_r_x - 5, leak_y + 2, color=INK, width=0.6)
    add_arrow(d, c_r_x + 5, leak_y + 2, leak_x - 5, leak_y + 2, color=GOLD, width=0.65)
    add_box(d, 20, 24, 105, 20, stroke=GOLD, fill=GOLD_LIGHT)
    add_text(d, 72.5, 31.0, "leak - c_R = 23/112640", size=5.45,
             color=INK, bold=True, anchor="middle", container=panel_a,
             layout_id="leak-inverse-r-margin")
    add_box(d, 132, 24, 105, 20, stroke=GOLD, fill=GOLD_LIGHT)
    add_text(d, 184.5, 31.0, "leak - c_gamma = 117451/89413632", size=5.05,
             color=INK, bold=True, anchor="middle", container=panel_a,
             layout_id="leak-margin")

    # Panel B: normalized annulus and exact odd-even cancellation.
    bx0 = W / 2 + 6
    add_text(d, bx0 + 2, H - 51, "B", size=8.2, bold=True, container=panel_b,
             layout_id="panel-b")
    add_text(d, bx0 + 17, H - 51, "Outer geometry and frame cancellation", size=7.4,
             bold=True, container=panel_b, layout_id="panel-b-title")
    add_badge(d, W - 74, H - 61, "PROVED", stroke=BLUE, fill=BLUE_LIGHT,
              width=48, container=panel_b, layout_id="badge-proved")

    cx, cy, radius = bx0 + 67, H - 126, 55
    inner_radius = radius * float(values["annulus_inner_over_r"])
    outer_radius = radius * float(values["annulus_outer_over_r"])
    d.add(Circle(cx, cy, outer_radius, strokeColor=BLUE, fillColor=BLUE_LIGHT, strokeWidth=0.9))
    d.add(Circle(cx, cy, inner_radius, strokeColor=BLUE, fillColor=white, strokeWidth=0.8))
    inner = Circle(cx, cy, inner_radius, strokeColor=BLUE, fillColor=None, strokeWidth=0.8)
    inner.strokeDashArray = [3, 2]
    d.add(inner)
    d.add(Line(cx - outer_radius - 3, cy, cx + outer_radius + 3, cy,
               strokeColor=LIGHT, strokeWidth=0.8))

    beta = math.sqrt(float(values["beta_squared"]))
    ch = float(values["c_h"])
    px, py = cx + radius * beta, cy + radius * ch
    mx, my = cx - radius * beta, cy - radius * ch
    inversion = Line(mx, my, px, py, strokeColor=MID, strokeWidth=0.75)
    inversion.strokeDashArray = [3, 2]
    d.add(inversion)
    d.add(Circle(px, py, 3.6, strokeColor=BLUE, fillColor=BLUE, strokeWidth=0.8))
    d.add(Circle(mx, my, 3.6, strokeColor=GOLD, fillColor=white, strokeWidth=1.0))
    add_text(d, px - 7, py - 1, "+ (beta r, c_h r)", size=5.55, color=BLUE,
             bold=True, anchor="end", container=panel_b, layout_id="plus-point")
    add_text(d, mx + 7, my - 1, "- (beta r, c_h r)", size=5.55, color=GOLD,
             bold=True, container=panel_b, layout_id="minus-point")

    d.add(Circle(cx, cy, 8, strokeColor=MID, fillColor=XLIGHT, strokeWidth=0.7))
    add_text(d, cx, cy - 2, "even", size=5.0, color=MID, bold=True, anchor="middle",
             container=panel_b, layout_id="even-kernel")
    add_text(d, cx, cy - 10, "phi_R", size=5.0, color=MID, anchor="middle",
             container=panel_b, layout_id="even-kernel-phi")
    add_text(d, cx, cy - outer_radius - 10, "inner=32r/63 · target=r · outer=64r/63", size=5.25,
             color=MID, anchor="middle", container=panel_b, layout_id="annulus-radii")
    add_text(d, cx, cy - outer_radius - 19, "gap=r/63 · beta^2=31/256 · c_h=15/16", size=5.1,
             color=MID, anchor="middle", container=panel_b, layout_id="geometry-values")

    dim_x = px + 13
    d.add(Line(dim_x, cy + radius / 240, dim_x, py, strokeColor=GOLD, strokeWidth=0.8))
    d.add(Polygon([dim_x, py, dim_x - 2, py - 4, dim_x + 2, py - 4], fillColor=GOLD, strokeColor=GOLD))
    d.add(Polygon([dim_x, cy + radius / 240, dim_x - 2, cy + radius / 240 + 4, dim_x + 2, cy + radius / 240 + 4], fillColor=GOLD, strokeColor=GOLD))
    add_text(d, dim_x - 5, cy + 27, ">= alpha r", size=5.45, color=GOLD, bold=True,
             anchor="end", container=panel_b, layout_id="alpha-distance")
    add_text(d, cx - outer_radius + 1, cy + outer_radius + 5, "transition bound <= r/240 at L >= 7680", size=5.35,
             color=MID, container=panel_b, layout_id="transition-bound")

    right_x = bx0 + 132
    add_box(d, right_x, H - 143, 94, 78, stroke=BLUE, fill=white)
    add_multiline(d, right_x + 7, H - 76,
                  ["ODD + EVEN", "F(t,-x) = -F(t,x)", "b(t,-x3) = -b(t,x3)",
                   "phi_R is even", "", "(phi_R * F)(t,0) = 0", "(phi_R * b)(t,0) = 0"],
                  size=5.55, leading=8.2, color=INK, bold_first=True,
                  container=panel_b, layout_id="odd-even")
    add_arrow(d, right_x + 47, H - 145, right_x + 47, H - 153, color=BLUE)
    add_box(d, right_x, H - 191, 94, 36, stroke=BLUE, fill=BLUE_LIGHT)
    add_multiline(d, right_x + 47, H - 164,
                  ["X_R(t) = 0", "a_R(t) = a'_R(t) = 0", "Versions M and F coincide"],
                  size=5.65, leading=8.5, color=INK, bold_first=True, anchor="middle",
                  container=panel_b, layout_id="frame-zero")
    add_badge(d, right_x, 31, "EXACT NSE · ZERO MEAN · p=0", stroke=MID,
              fill=white, text_color=MID, width=101, dash=[3, 2], container=panel_b,
              layout_id="exact-nse-badge")

    # Global boundary band.
    d.add(Rect(14, 5, W - 28, 15, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.75))
    add_text(d, 21, 10, "FINITE GATE ONLY", size=5.8, color=GOLD, bold=True,
             layout_id="finite-boundary")
    add_text(d, 86, 10, "OPEN: two-packet survival · buffered leakage · full ledger · amplitude closure",
             size=5.55, color=INK, layout_id="open-boundary")
    add_text(d, W - 21, 10, "NOT CLAY", size=5.8, color=INK, bold=True, anchor="end",
             layout_id="not-clay")
    return d


def main() -> None:
    certificate, values = load_exact()
    write_source_data(values)
    drawing = build_drawing(values)

    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"), showBoundary=False)
    renderPDF.drawToFile(drawing, str(HERE / "figure.pdf"), showBoundary=False)
    import pypdfium2 as pdfium
    pdf = pdfium.PdfDocument(str(HERE / "figure.pdf"))
    master = pdf[0].render(scale=DPI / 72).to_pil().convert("RGB")
    master.save(HERE / "figure.png", dpi=(DPI, DPI), optimize=False)
    ImageOps.grayscale(master).save(HERE / "qa-grayscale.png", dpi=(DPI, DPI), optimize=False)
    final_width = 1800
    final_height = round(master.height * final_width / master.width)
    master.resize((final_width, final_height), Image.Resampling.LANCZOS).save(
        HERE / "qa-final-size.png", dpi=(254, 254), optimize=False
    )

    bitmap = pdf[0].render(scale=300 / 72)
    bitmap.to_pil().convert("RGB").save(HERE / "qa-pdf.png", dpi=(300, 300), optimize=False)

    (HERE / "layout-bounds.json").write_text(
        json.dumps({
            "canvasPt": [round(W, 4), round(H, 4)],
            "method": "ReportLab pdfmetrics.stringWidth plus font ascent/descent proxy",
            "entries": LAYOUT,
            "summary": {
                "passed": sum(bool(entry["proxyPass"]) for entry in LAYOUT),
                "total": len(LAYOUT),
            },
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (HERE / "environment.json").write_text(
        json.dumps({
            "certificatePath": str(CERTIFICATE.relative_to(REPO)),
            "certificateSha256": sha256(CERTIFICATE),
            "figureId": FIGURE_ID,
            "fontBold": {"path": str(FONT_BOLD), "sha256": sha256(FONT_BOLD)},
            "fontRegular": {"path": str(FONT_REGULAR), "sha256": sha256(FONT_REGULAR)},
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "reportlab": __import__("reportlab").Version,
            "sourceNotePath": str(SOURCE_NOTE.relative_to(REPO)),
            "sourceNoteSha256AtRender": sha256(SOURCE_NOTE),
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"generated {FIGURE_ID}: {len(LAYOUT)} text bounds; certificate 13/13 PASS")


if __name__ == "__main__":
    main()
