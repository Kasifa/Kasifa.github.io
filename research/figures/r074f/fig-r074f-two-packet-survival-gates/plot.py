#!/usr/bin/env python3
"""Generate the deterministic R0.74F finite-gates journal figure package.

The frozen exact certificate is the sole quantitative input.  The drawing is
finite analytic bookkeeping, not DNS, not a stochastic simulation, and not a
certificate of the periodic bridge or packet-survival argument.
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
CERTIFICATE = REPO / "research/r074f_two_packet_survival_certificate.json"
EXPECTED_CERT_SHA256 = "44bd3208d10134ae84cf8b001e9569b6c480af6ac7d85efc25759dc4e725e981"
FIGURE_ID = "fig-r074f-two-packet-survival-gates"

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
pdfmetrics.registerFont(TTFont("R074F-Regular", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("R074F-Bold", str(FONT_BOLD)))


def frac(value: str) -> Fraction:
    return Fraction(value)


def load_exact() -> tuple[dict, dict[str, Fraction]]:
    if sha256(CERTIFICATE) != EXPECTED_CERT_SHA256:
        raise RuntimeError("certificate hash mismatch; freeze or update the figure contract")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate.get("schema") != "r074f-two-packet-survival-finite-certificate-v1":
        raise RuntimeError("unexpected R0.74F certificate schema")
    if certificate.get("status") != "PASS" or certificate.get("summary") != {"passed": 30, "total": 30}:
        raise RuntimeError("certificate is not the frozen 30/30 PASS object")
    if len(certificate.get("checks", [])) != 30 or not all(item.get("pass") is True for item in certificate["checks"]):
        raise RuntimeError("certificate Boolean checks are incomplete")

    inputs = certificate["inputs"]
    derived = certificate["derived"]
    values = {
        "lambda": frac(inputs["lambda"]),
        "c_h": frac(inputs["c_h"]),
        "alpha": frac(inputs["alpha"]),
        "c_R": frac(inputs["c_R"]),
        "c_gamma": frac(inputs["c_gamma"]),
        "L_contrast": frac(inputs["L_contrast"]),
        "L_surv": frac(inputs["L_surv"]),
        "shrink": frac(inputs["shrink"]),
        "c_leak": frac(derived["c_leak"]),
        "c_surv": frac(derived["c_surv"]),
        "effective_separation": frac(derived["effective_separation"]),
        "buffer_over_R": frac(derived["buffer_over_R"]),
        "inner_margin": frac(derived["inner_margin_at_L_surv"]),
        "outer_sq_margin": frac(derived["outer_sq_margin_at_L_surv"]),
    }
    values.update({
        "c_alpha_heat": values["alpha"] ** 2 / 260,
        "gap_R_gamma": values["c_R"] - values["c_gamma"],
        "gap_leak_R": values["c_leak"] - values["c_R"],
        "gap_alpha_leak": values["alpha"] ** 2 / 260 - values["c_leak"],
        "gap_surv_alpha": values["c_surv"] - values["alpha"] ** 2 / 260,
        "gap_surv_leak": values["c_surv"] - values["c_leak"],
        "L12": values["lambda"] * 2**12,
        "L13": values["lambda"] * 2**13,
        "buffer_budget": values["c_h"] * values["L_surv"] / 256,
        "inner_threshold": 1 / values["lambda"],
        "inner_lower": 1 - Fraction(97, 32) / values["L_surv"],
        "outer_threshold_sq": (2 / values["lambda"]) ** 2,
        "conditional_upper_sq": Fraction(87370044545, 86973087744),
        "x1_half_width": Fraction(1, 16),
        "e2_abs": Fraction(65, 32),
        "e3_abs": Fraction(1),
        "first_admissible_j": Fraction(13),
    })
    checks = {item["id"]: item for item in certificate["checks"]}
    if frac(checks["survival_exponent_beats_alpha_heat"]["margin"]) != values["gap_surv_alpha"]:
        raise RuntimeError("survival/alpha-heat margin drift")
    if frac(checks["conditional_outer_annulus_margin"]["margin"]) != values["outer_sq_margin"]:
        raise RuntimeError("conditional outer margin drift")
    if values["inner_lower"] - values["inner_threshold"] != values["inner_margin"]:
        raise RuntimeError("conditional inner margin drift")
    return certificate, values


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def write_source_data(values: dict[str, Fraction]) -> None:
    rows = [
        ("A", "c_gamma", values["c_gamma"], "exponent", "EXACT FINITE", "annular weight exponent"),
        ("A", "c_R", values["c_R"], "exponent", "EXACT FINITE", "inverse-radius exponent"),
        ("A", "c_leak", values["c_leak"], "conditional exponent", "EXACT FINITE", "proposed local-leakage exponent"),
        ("A", "c_alpha_heat", values["c_alpha_heat"], "conditional exponent", "EXACT FINITE", "alpha squared over 260"),
        ("A", "c_surv", values["c_surv"], "conditional exponent", "EXACT FINITE", "proposed buffered-survival exponent"),
        ("A", "gap_R_gamma", values["gap_R_gamma"], "strict gap", "EXACT FINITE", "c_R minus c_gamma"),
        ("A", "gap_leak_R", values["gap_leak_R"], "strict gap", "EXACT FINITE", "c_leak minus c_R"),
        ("A", "gap_alpha_leak", values["gap_alpha_leak"], "strict gap", "EXACT FINITE", "alpha heat minus c_leak"),
        ("A", "gap_surv_alpha", values["gap_surv_alpha"], "strict gap", "EXACT FINITE", "c_surv minus alpha heat"),
        ("A", "gap_surv_leak", values["gap_surv_leak"], "strict gap", "EXACT FINITE", "c_surv minus c_leak"),
        ("A", "effective_separation", values["effective_separation"], "coefficient", "EXACT FINITE", "255 c_h over 256"),
        ("B", "L_contrast", values["L_contrast"], "threshold", "EXACT FINITE", "inherited contrast threshold"),
        ("B", "L_surv", values["L_surv"], "threshold", "EXACT FINITE", "finite survival-bookkeeping threshold"),
        ("B", "L12", values["L12"], "discrete scale", "EXACT FINITE", "lambda times 2 to the 12"),
        ("B", "L13", values["L13"], "discrete scale", "EXACT FINITE", "lambda times 2 to the 13"),
        ("B", "buffer_over_R", values["buffer_over_R"], "buffer", "EXACT FINITE", "2 kappa plus terminal vertical unit"),
        ("B", "buffer_budget", values["buffer_budget"], "buffer", "EXACT FINITE", "c_h L_surv over 256"),
        ("B", "inner_threshold", values["inner_threshold"], "normalized radius", "EXACT FINITE", "dyadic inner annular threshold"),
        ("B", "inner_lower", values["inner_lower"], "conditional normalized radius", "CONDITIONAL", "terminal-lobe lower radius bound at L_surv"),
        ("B", "inner_margin", values["inner_margin"], "conditional strict margin", "CONDITIONAL", "inner lower bound minus threshold"),
        ("B", "outer_threshold_sq", values["outer_threshold_sq"], "normalized radius squared", "EXACT FINITE", "dyadic outer squared-radius threshold"),
        ("B", "conditional_upper_sq", values["conditional_upper_sq"], "conditional normalized radius squared", "CONDITIONAL", "terminal-lobe upper squared-radius bound at L_surv"),
        ("B", "outer_sq_margin", values["outer_sq_margin"], "conditional strict margin", "CONDITIONAL", "outer squared threshold minus upper bound"),
        ("B", "x1_half_width_over_r", values["x1_half_width"], "hypothesis", "CONDITIONAL", "absolute x1 half-width over r"),
        ("B", "e2_abs_over_R", values["e2_abs"], "hypothesis", "CONDITIONAL", "absolute second-component error over R"),
        ("B", "e3_abs_over_R", values["e3_abs"], "hypothesis", "CONDITIONAL", "absolute third-component error over R"),
        ("B", "first_admissible_j", values["first_admissible_j"], "discrete index", "EXACT FINITE", "first j with L_j at least L_surv"),
    ]
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["panel", "record", "exact_value", "decimal_value", "role", "status", "note"])
        for panel, record, value, role, status, note in rows:
            writer.writerow([panel, record, q(value), f"{float(value):.17g}", role, status, note])


LAYOUT: list[dict] = []


def add_text(drawing: Drawing, x: float, y: float, text: str, *, size: float = 6.0,
             color=INK, bold: bool = False, anchor: str = "start",
             container: tuple[float, float, float, float] | None = None,
             layout_id: str = "text") -> None:
    font = "R074F-Bold" if bold else "R074F-Regular"
    width = pdfmetrics.stringWidth(text, font, size)
    left = x if anchor == "start" else x - width / 2 if anchor == "middle" else x - width
    bounds = [left, y - 0.23 * size, left + width, y + 0.86 * size]
    region = list(container or (0, 0, W, H))
    within = bounds[0] >= region[0] - 0.25 and bounds[1] >= region[1] - 0.25 and bounds[2] <= region[2] + 0.25 and bounds[3] <= region[3] + 0.25
    LAYOUT.append({
        "id": layout_id,
        "text": text,
        "fontPt": size,
        "boundsPt": [round(value, 4) for value in bounds],
        "containerPt": [round(value, 4) for value in region],
        "proxyPass": within,
    })
    drawing.add(String(x, y, text, fontName=font, fontSize=size, fillColor=color, textAnchor=anchor))


def add_multiline(drawing: Drawing, x: float, y: float, lines: list[str], *, size: float = 5.5,
                  leading: float = 7.4, color=INK, bold_first: bool = False,
                  anchor: str = "start", container=None, layout_id: str = "multi") -> None:
    for index, line in enumerate(lines):
        add_text(drawing, x, y - index * leading, line, size=size, color=color,
                 bold=bold_first and index == 0, anchor=anchor, container=container,
                 layout_id=f"{layout_id}-{index}")


def add_box(drawing: Drawing, x: float, y: float, width: float, height: float, *,
            stroke=LIGHT, fill=white, dash=None, line_width: float = 0.7) -> None:
    box = Rect(x, y, width, height, rx=3, ry=3, strokeColor=stroke,
               fillColor=fill, strokeWidth=line_width)
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)


def add_badge(drawing: Drawing, x: float, y: float, text: str, *, stroke=BLUE,
              fill=white, text_color=BLUE, width: float | None = None,
              dash=None, container=None, layout_id: str = "badge") -> None:
    size = 5.4
    box_width = width or pdfmetrics.stringWidth(text, "R074F-Bold", size) + 10
    box = Rect(x, y, box_width, 12, rx=4, ry=4, strokeColor=stroke,
               fillColor=fill, strokeWidth=0.7)
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)
    add_text(drawing, x + box_width / 2, y + 3.55, text, size=size, color=text_color,
             bold=True, anchor="middle", container=container, layout_id=layout_id)


def add_blossom(drawing: Drawing, x: float, y: float) -> None:
    for angle in (90, 18, -54, -126, 162):
        radians = math.radians(angle)
        drawing.add(Circle(x + 3.3 * math.cos(radians), y + 3.3 * math.sin(radians), 2.0,
                           strokeColor=BLUE, fillColor=None, strokeWidth=0.45))
    drawing.add(Circle(x, y, 1.1, strokeColor=BLUE, fillColor=GOLD, strokeWidth=0.35))


def add_marker(drawing: Drawing, x: float, y: float, kind: str, *, color=BLUE,
               fill=white, size: float = 3.2) -> None:
    if kind == "circle":
        drawing.add(Circle(x, y, size, strokeColor=color, fillColor=fill, strokeWidth=1.0))
    elif kind == "diamond":
        drawing.add(Polygon([x, y + size, x + size, y, x, y - size, x - size, y],
                            strokeColor=color, fillColor=fill, strokeWidth=1.0))
    elif kind == "square":
        drawing.add(Rect(x - size, y - size, 2 * size, 2 * size,
                         strokeColor=color, fillColor=fill, strokeWidth=1.0))
    elif kind == "triangle":
        drawing.add(Polygon([x, y + size, x + size, y - size, x - size, y - size],
                            strokeColor=color, fillColor=fill, strokeWidth=1.0))
    else:
        raise ValueError(kind)


def add_double_arrow(drawing: Drawing, x1: float, x2: float, y: float, *, color=INK) -> None:
    drawing.add(Line(x1, y, x2, y, strokeColor=color, strokeWidth=0.65))
    for x, direction in ((x1, 1), (x2, -1)):
        drawing.add(Polygon([x, y, x + direction * 4, y + 1.8, x + direction * 4, y - 1.8],
                            fillColor=color, strokeColor=color, strokeWidth=0.2))


def build_drawing(values: dict[str, Fraction]) -> Drawing:
    LAYOUT.clear()
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, strokeColor=None, fillColor=white))

    add_text(d, 14, H - 16, "R0.74F two-packet survival finite gates", size=10.2,
             bold=True, layout_id="title")
    add_text(d, 14, H - 28,
             "Exact certificate compatibility + conditional lobe geometry; analytic bridge not certified by this figure.",
             size=6.25, color=MID, layout_id="subtitle")
    add_blossom(d, W - 17, H - 17)
    d.add(Line(14, H - 35, W - 14, H - 35, strokeColor=LIGHT, strokeWidth=0.7))
    d.add(Line(W / 2, 25, W / 2, H - 42, strokeColor=LIGHT, strokeWidth=0.7))

    panel_a = (14, 25, W / 2 - 6, H - 39)
    panel_b = (W / 2 + 6, 25, W - 14, H - 39)

    # Panel A: exact hierarchy plus a close-range inset.
    add_text(d, 16, H - 51, "A", size=8.2, bold=True, container=panel_a, layout_id="panel-a")
    add_text(d, 31, H - 51, "Exact exponent hierarchy", size=7.4, bold=True,
             container=panel_a, layout_id="panel-a-title")
    add_badge(d, W / 2 - 78, H - 61, "30/30 EXACT", stroke=BLUE, fill=BLUE_LIGHT,
              width=63, container=panel_a, layout_id="badge-exact")

    add_text(d, 22, H - 74, "Full scale", size=5.9, bold=True, color=MID,
             container=panel_a, layout_id="full-scale-title")
    x0, x1, y = 31, W / 2 - 23, H - 97
    full_min, full_max = 0.00195, 0.00338
    full_x = lambda value: x0 + (float(value) - full_min) / (full_max - full_min) * (x1 - x0)
    d.add(Line(x0, y, x1, y, strokeColor=INK, strokeWidth=0.8))
    marks = [
        ("c_gamma", "circle", BLUE, white),
        ("c_R", "diamond", INK, white),
        ("c_leak", "square", GOLD, GOLD_LIGHT),
        ("c_alpha_heat", "triangle", BLUE, BLUE_LIGHT),
        ("c_surv", "circle", GOLD, GOLD),
    ]
    for key, kind, color, fill in marks:
        xpos = full_x(values[key])
        add_marker(d, xpos, y, kind, color=color, fill=fill, size=3.0)
    add_text(d, full_x(values["c_gamma"]), y + 11, "c_gamma  8/3969", size=5.15,
             color=BLUE, bold=True, anchor="middle", container=panel_a,
             layout_id="full-c_gamma")
    add_text(d, full_x(values["c_R"]), y - 15, "c_R  1/320", size=5.15,
             color=INK, bold=True, anchor="middle", container=panel_a,
             layout_id="full-c_R")
    add_text(d, x1, y + 11, "c_leak < alpha heat < c_surv", size=4.75,
             color=GOLD, bold=True, anchor="end", container=panel_a,
             layout_id="full-close-cluster")
    cluster_x = full_x(values["c_alpha_heat"])
    guide = Line(cluster_x, y - 4, cluster_x, H - 123, strokeColor=MID, strokeWidth=0.55)
    guide.strokeDashArray = [2, 2]
    d.add(guide)

    box_y = H - 130
    add_box(d, 20, box_y, 105, 18, stroke=BLUE, fill=white)
    add_text(d, 72.5, box_y + 6.2, "c_R-c_gamma = 1409/1270080", size=5.15,
             bold=True, anchor="middle", container=panel_a, layout_id="gap-r-gamma")
    add_box(d, 132, box_y, 105, 18, stroke=GOLD, fill=GOLD_LIGHT)
    add_text(d, 184.5, box_y + 6.2, "c_leak-c_R = 23/112640", size=5.15,
             bold=True, anchor="middle", container=panel_a, layout_id="gap-leak-r")

    add_text(d, 22, H - 145, "Enlarged close range", size=5.9, bold=True, color=MID,
             container=panel_a, layout_id="zoom-title")
    zx0, zx1, zy = 31, W / 2 - 23, H - 169
    zoom_min, zoom_max = 0.003326, 0.003357
    zoom_x = lambda value: zx0 + (float(value) - zoom_min) / (zoom_max - zoom_min) * (zx1 - zx0)
    d.add(Line(zx0, zy, zx1, zy, strokeColor=INK, strokeWidth=0.8))
    close_marks = [
        ("c_leak", "c_leak = 75/22528", "square", GOLD, GOLD_LIGHT, 11, "middle"),
        ("c_alpha_heat", "alpha^2/260 = 49/14625", "triangle", BLUE, BLUE_LIGHT, -14, "middle"),
        ("c_surv", "c_surv = 2926125/872415232", "circle", GOLD, GOLD, 11, "end"),
    ]
    for key, label, kind, color, fill, offset, anchor in close_marks:
        xpos = zoom_x(values[key])
        add_marker(d, xpos, zy, kind, color=color, fill=fill, size=3.1)
        tx = xpos if anchor != "end" else zx1
        add_text(d, tx, zy + offset, label, size=4.95, color=color, bold=True,
                 anchor=anchor, container=panel_a, layout_id=f"zoom-{key}")
    add_double_arrow(d, zoom_x(values["c_leak"]) + 5, zoom_x(values["c_alpha_heat"]) - 5,
                     zy - 25, color=BLUE)
    add_text(d, (zoom_x(values["c_leak"]) + zoom_x(values["c_alpha_heat"])) / 2,
             zy - 33, "6997/329472000", size=4.85, color=INK, bold=True,
             anchor="middle", container=panel_a, layout_id="gap-alpha-leak")
    add_double_arrow(d, zoom_x(values["c_alpha_heat"]) + 4, zoom_x(values["c_surv"]) - 4,
                     zy - 25, color=GOLD)
    add_text(d, zx1, zy - 33, "3556289/981467136000", size=4.45, color=INK,
             bold=True, anchor="end", container=panel_a, layout_id="gap-surv-alpha")

    # Panel B: conditional annular gates and discrete threshold.
    bx0 = W / 2 + 6
    add_text(d, bx0 + 2, H - 51, "B", size=8.2, bold=True, container=panel_b,
             layout_id="panel-b")
    add_text(d, bx0 + 17, H - 51, "Conditional annular lobe gate", size=7.4, bold=True,
             container=panel_b, layout_id="panel-b-title")
    add_badge(d, W - 89, H - 61, "CONDITIONAL", stroke=GOLD, fill=GOLD_LIGHT,
              text_color=GOLD, width=63, container=panel_b, layout_id="badge-conditional")

    add_box(d, bx0 + 8, H - 91, W / 2 - 28, 24, stroke=GOLD, fill=GOLD_LIGHT, dash=[3, 2])
    add_multiline(d, bx0 + 15, H - 75,
                  ["Lobe hypotheses (not certificate outputs)",
                   "|x1| <= r/16   |e2| <= 65R/32   |e3| <= R"],
                  size=5.25, leading=8.0, color=INK, bold_first=True,
                  container=panel_b, layout_id="hypotheses")

    # Inner-radius comparison, shown on its honest shared scale.
    add_text(d, bx0 + 10, H - 100, "Inner check · normalized radius", size=5.75,
             bold=True, container=panel_b, layout_id="inner-title")
    ix0, ix1, iy = bx0 + 20, W - 26, H - 119
    inner_min, inner_max = 0.48, 1.01
    inner_x = lambda value: ix0 + (float(value) - inner_min) / (inner_max - inner_min) * (ix1 - ix0)
    d.add(Line(ix0, iy, ix1, iy, strokeColor=MID, strokeWidth=0.75))
    it = inner_x(values["inner_threshold"])
    il = inner_x(values["inner_lower"])
    d.add(Rect(it, iy - 3.5, il - it, 7, strokeColor=BLUE, fillColor=BLUE_LIGHT, strokeWidth=0.65))
    add_marker(d, it, iy, "circle", color=BLUE, fill=white, size=3.1)
    add_marker(d, il, iy, "triangle", color=GOLD, fill=GOLD_LIGHT, size=3.2)
    add_text(d, it, iy + 9, "inner = 32/63", size=5.05, color=BLUE, bold=True,
             anchor="middle", container=panel_b, layout_id="inner-threshold")
    add_text(d, il, iy - 13, "lower = 1-97/(32*9216)", size=4.85, color=GOLD,
             bold=True, anchor="end", container=panel_b, layout_id="inner-lower")
    add_text(d, bx0 + 12, iy - 23, "exact margin = 1015129/2064384 > 0", size=5.0,
             color=INK, bold=True, container=panel_b, layout_id="inner-margin")

    # Outer squared-radius comparison, again on a shared scale.
    add_text(d, bx0 + 10, H - 154, "Outer check · normalized radius squared", size=5.75,
             bold=True, container=panel_b, layout_id="outer-title")
    ox0, ox1, oy = bx0 + 20, W - 26, H - 174
    outer_min, outer_max = 0.998, 1.036
    outer_x = lambda value: ox0 + (float(value) - outer_min) / (outer_max - outer_min) * (ox1 - ox0)
    d.add(Line(ox0, oy, ox1, oy, strokeColor=MID, strokeWidth=0.75))
    ou = outer_x(values["conditional_upper_sq"])
    ot = outer_x(values["outer_threshold_sq"])
    d.add(Rect(ou, oy - 3.5, ot - ou, 7, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.65))
    add_marker(d, ou, oy, "square", color=GOLD, fill=GOLD_LIGHT, size=3.1)
    add_marker(d, ot, oy, "diamond", color=BLUE, fill=white, size=3.1)
    add_text(d, bx0 + 12, oy + 10, "upper^2 = 87370044545/86973087744", size=4.4,
             color=GOLD, bold=True, anchor="start", container=panel_b,
             layout_id="outer-upper")
    add_text(d, W - 26, oy + 10, "outer^2 = (64/63)^2", size=4.55, color=BLUE,
             bold=True, anchor="end", container=panel_b, layout_id="outer-threshold")
    add_text(d, bx0 + 12, oy - 13, "margin = 116914328399/4261681299456 > 0", size=4.45,
             color=INK, bold=True, container=panel_b, layout_id="outer-margin")

    # Discrete scale threshold, compressed to preserve the annular rows.
    add_box(d, bx0 + 8, 24, W / 2 - 28, 14, stroke=BLUE, fill=BLUE_LIGHT)
    add_text(d, bx0 + 15, 28.8,
             "L_12=8064 < L*=9216 < L_13=16128  =>  first admissible j=13",
             size=4.55, color=INK, bold=True, container=panel_b,
             layout_id="discrete-gate")

    # Global claim boundary.
    d.add(Rect(14, 5, W - 28, 15, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.75))
    add_text(d, 21, 10, "FINITE COMPATIBILITY ONLY", size=5.7, color=GOLD,
             bold=True, layout_id="finite-boundary")
    add_text(d, 118, 10, "ANALYTIC BRIDGE / PACKET SURVIVAL NOT CERTIFIED BY FIGURE",
             size=5.25, color=INK, layout_id="analytic-boundary")
    add_text(d, W - 21, 10, "NOT CLAY", size=5.8, color=INK, bold=True,
             anchor="end", layout_id="not-clay")
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
    pdf[0].render(scale=300 / 72).to_pil().convert("RGB").save(
        HERE / "qa-pdf.png", dpi=(300, 300), optimize=False
    )

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
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"generated {FIGURE_ID}: {len(LAYOUT)} text bounds; certificate 30/30 PASS")


if __name__ == "__main__":
    main()
