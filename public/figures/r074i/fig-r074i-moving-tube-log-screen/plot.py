#!/usr/bin/env python3
"""Render the deterministic R0.74I moving-tube/log-screen journal figure.

The figure contains an exact analytic implication diagram and an exact affine
exponent screen.  It contains no DNS, simulation, sampled trajectory, or
empirical proxy.  Every quantitative finite label is reconstructed from the
frozen R0.74I certificate after provenance and byte-identity checks.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import subprocess
import sys
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageOps
from reportlab import rl_config
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import (
    Circle,
    Drawing,
    Ellipse,
    Line,
    Path as ShapePath,
    Polygon,
    Rect,
    String,
)
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074i_tube_log_certificate.json"
PRODUCER = REPO / "scripts/r074i_tube_log_certificate.py"
EXPECTED_CERT_SHA256 = "d4d0f32f6772bdae8a9ec0e8fd6f5f5f9248877df3c19bf544c3577055ab7bf5"
EXPECTED_PRODUCER_SHA256 = "5411134949eedbb1c285607c33a4f8feb9f8d358f5fc7cee91ec3601dfe3932f"
FIGURE_ID = "fig-r074i-moving-tube-log-screen"

BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFTOPPM = BUNDLE / "bin/override/pdftoppm"
PDFINFO = BUNDLE / "bin/override/pdfinfo"

WIDTH_MM = 180
HEIGHT_MM = 88
DPI = 600
W = WIDTH_MM * mm
H = HEIGHT_MM * mm

# Hard two-root palette: blue + gold, with neutral ink and paper shades.
INK = HexColor("#202A34")
MID = HexColor("#626D78")
LIGHT = HexColor("#E3E8EC")
XLIGHT = HexColor("#F6F8FA")
BLUE = HexColor("#1F5A91")
BLUE_LIGHT = HexColor("#E6F0F7")
GOLD = HexColor("#A87312")
GOLD_LIGHT = HexColor("#FBF2DE")

rl_config.invariant = 1

TEXT_SUFFIXES = {".md", ".txt", ".json", ".csv", ".py"}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def write_canonical_text(path: Path, content: str) -> None:
    """Write UTF-8 text with exactly one terminal LF and no CRLF drift."""

    normalized = content.replace("\r\n", "\n").rstrip("\n") + "\n"
    path.write_text(normalized, encoding="utf-8")


def assert_text_eof_policy() -> None:
    """Reject any package text file with a blank line at EOF."""

    failures = []
    for path in sorted(HERE.iterdir(), key=lambda item: item.name):
        if not path.is_file() or (
            path.suffix not in TEXT_SUFFIXES and path.name != "SHA256SUMS"
        ):
            continue
        payload = path.read_bytes()
        if b"\r\n" in payload or not payload.endswith(b"\n") or payload.endswith(b"\n\n"):
            failures.append(path.name)
    if failures:
        raise RuntimeError(
            "package text EOF policy failed (require exactly one LF): "
            + ", ".join(failures)
        )


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
    raise FileNotFoundError(f"required font not found: {filename}")


FONT_REGULAR = locate_font("DejaVuSans.ttf")
FONT_BOLD = locate_font("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074I-Regular", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("R074I-Bold", str(FONT_BOLD)))


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def load_exact() -> tuple[dict, dict[str, Fraction]]:
    if sha256(CERTIFICATE) != EXPECTED_CERT_SHA256:
        raise RuntimeError("certificate hash mismatch; refusing source drift")
    if sha256(PRODUCER) != EXPECTED_PRODUCER_SHA256:
        raise RuntimeError("producer hash mismatch; refusing source drift")
    regenerated = subprocess.run(
        [sys.executable, str(PRODUCER)], check=True, capture_output=True
    ).stdout
    if regenerated != CERTIFICATE.read_bytes():
        raise RuntimeError("producer stdout is not byte-identical to certificate JSON")

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate.get("result") != "PASS":
        raise RuntimeError("certificate result is not PASS")
    if certificate.get("summary") != {"passed": 36, "total": 36}:
        raise RuntimeError("certificate is not the frozen 36/36 object")
    items = certificate.get("checks", [])
    if len(items) != 36 or not all(item.get("pass") is True for item in items):
        raise RuntimeError("certificate Boolean gates are incomplete")
    checks = {item["id"]: item for item in items}

    def value(check_id: str, field: str = "left") -> Fraction:
        return Fraction(checks[check_id][field])

    values = {
        "scaled_l3_power": value("ns_scaled_l3_total_power"),
        "normalized_l3_power": value("ns_normalized_l3_scale_invariance"),
        "half_time": value("half_radius_time_length_factor"),
        "half_normalization": value("half_radius_normalization_factor"),
        "half_product": value("half_radius_fixed_factor_product"),
        "energy_inverse": value("energy_from_payment_inverse_power"),
        "threshold_chain": value("tube_to_payment_threshold_power"),
        "l3_payment_chain": value("l3_to_payment_threshold_chain"),
        "rho": value("rho_exact_value"),
        "two_rho": value("two_rho"),
        "three_rho": value("three_rho"),
        "window_width": value("log_window_width"),
        "lacunarity": value("lacunarity_log_exponent"),
        "frontier_l": value("frontier_total_L_power"),
        "gap_constant": value("subcritical_gap_constant_coefficient"),
        "gap_delta": value("subcritical_gap_delta_coefficient"),
        "endpoint_gap": value("endpoint_gamma_gap"),
        "endpoint_l": value("endpoint_L_cancellation"),
    }
    expected = {
        "scaled_l3_power": Fraction(-2),
        "normalized_l3_power": Fraction(0),
        "half_time": Fraction(1, 4),
        "half_normalization": Fraction(4),
        "half_product": Fraction(1),
        "energy_inverse": Fraction(1),
        "threshold_chain": Fraction(1),
        "l3_payment_chain": Fraction(1),
        "rho": Fraction(1, 320),
        "two_rho": Fraction(1, 160),
        "three_rho": Fraction(3, 320),
        "window_width": Fraction(1, 320),
        "lacunarity": Fraction(1, 64),
        "frontier_l": Fraction(1),
        "gap_constant": Fraction(0),
        "gap_delta": Fraction(1),
        "endpoint_gap": Fraction(0),
        "endpoint_l": Fraction(0),
    }
    if values != expected:
        raise RuntimeError("exact R0.74I value map drift")
    return certificate, values


def screen_y(gamma: Fraction) -> Fraction:
    """Exact residual L exponent y(gamma)=1-2 gamma."""

    return Fraction(1) - 2 * gamma


def write_source_data(values: dict[str, Fraction]) -> None:
    rows = [
        ["A", "normalized_cubic_scaling", "", q(values["normalized_l3_power"]), "r^-2 integral_Qr |u|^3", "FINITE EXACT", "scale-invariant normalized cubic quantity"],
        ["A", "half_radius_time_factor", "1/2", q(values["half_time"]), "|I_(R/2)|/|I_R|", "FINITE EXACT", "parabolic time factor"],
        ["A", "half_radius_normalization", "1/2", q(values["half_normalization"]), "(R/2)^-2 / R^-2", "FINITE EXACT", "normalization factor"],
        ["A", "half_radius_factor_product", "1/2", q(values["half_product"]), "(1/4)*4", "FINITE EXACT", "exact cancellation"],
        ["A", "energy_payment_inverse_chain", "", q(values["energy_inverse"]), "(3/2)*(2/3)", "FINITE EXACT", "payment-to-energy exponent recovery"],
        ["A", "tube_payment_threshold_chain", "", q(values["threshold_chain"]), "(3/2)*(2/3)", "FINITE EXACT", "tube threshold exponent compatibility"],
        ["A", "path_confinement", "1/2", "1/2", "sup_t |X_R(t)-x0| <= R/2", "ANALYTIC IMPLICATION", "symbolic threshold; no epsilon value plotted"],
        ["A", "fixed_cylinder_cubic", "1/2", "3/2", "(R/2)^-2 int_Q(R/2)|u|^3 <= C E_R^(3/2)", "ANALYTIC IMPLICATION", "unknown C is symbolic and not plotted"],
    ]
    for gamma in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
        y = screen_y(gamma)
        status = "REJECTED" if y > 0 else "OPEN ENDPOINT" if y == 0 else "NOT REJECTED / NOT PROVED"
        rows.append(["B", f"screen_gamma_{q(gamma)}", q(gamma), q(y), "y(gamma)=1-2 gamma", status, "exact affine residual exponent"])
    rows.extend([
        ["B", "rho", "", q(values["rho"]), "rho", "FINITE EXACT", "frozen packet parameter"],
        ["B", "log_window_lower", "", q(values["two_rho"]), "2 rho", "FINITE EXACT", "lower coefficient of log P_j / L_j^2"],
        ["B", "log_window_upper", "", q(values["three_rho"]), "3 rho", "FINITE EXACT", "upper coefficient of log P_j / L_j^2"],
        ["B", "log_window_width", "", q(values["window_width"]), "3 rho - 2 rho", "FINITE EXACT", "window width"],
        ["B", "lacunarity_exponent", "", q(values["lacunarity"]), "8 rho - 3 rho", "FINITE EXACT", "consecutive-index lower-minus-upper exponent"],
        ["B", "frontier_L_power", "1/2", q(values["frontier_l"]), "P^(2/3) sqrt(log P) supplies L^1", "FINITE EXACT", "endpoint-compatible power only"],
    ])
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["panel", "record", "gamma_exact", "value_exact", "formula", "status", "note"])
        writer.writerows(rows)


LAYOUT: list[dict] = []


def add_text(
    drawing: Drawing,
    x: float,
    y: float,
    text: str,
    *,
    size: float = 5.5,
    color=INK,
    bold: bool = False,
    anchor: str = "start",
    container: tuple[float, float, float, float] | None = None,
    layout_id: str = "text",
) -> None:
    font = "R074I-Bold" if bold else "R074I-Regular"
    width = pdfmetrics.stringWidth(text, font, size)
    left = x if anchor == "start" else x - width / 2 if anchor == "middle" else x - width
    bounds = [left, y - 0.25 * size, left + width, y + 0.86 * size]
    region = list(container or (0, 0, W, H))
    within = (
        bounds[0] >= region[0] - 0.25
        and bounds[1] >= region[1] - 0.25
        and bounds[2] <= region[2] + 0.25
        and bounds[3] <= region[3] + 0.25
    )
    LAYOUT.append(
        {
            "id": layout_id,
            "text": text,
            "fontPt": size,
            "boundsPt": [round(v, 4) for v in bounds],
            "containerPt": [round(v, 4) for v in region],
            "proxyPass": within,
        }
    )
    drawing.add(
        String(
            x,
            y,
            text,
            fontName=font,
            fontSize=size,
            fillColor=color,
            textAnchor=anchor,
        )
    )


def add_box(
    drawing: Drawing,
    x: float,
    y: float,
    width: float,
    height: float,
    *,
    stroke=LIGHT,
    fill=white,
    dash=None,
    line_width: float = 0.75,
    radius: float = 3,
) -> None:
    box = Rect(
        x,
        y,
        width,
        height,
        rx=radius,
        ry=radius,
        strokeColor=stroke,
        fillColor=fill,
        strokeWidth=line_width,
    )
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)


def add_arrow(
    drawing: Drawing,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    color=INK,
    dash=None,
    line_width: float = 0.9,
) -> None:
    line = Line(x0, y0, x1, y1, strokeColor=color, strokeWidth=line_width)
    if dash:
        line.strokeDashArray = dash
    drawing.add(line)
    angle = math.atan2(y1 - y0, x1 - x0)
    length = 3.4
    spread = 0.48
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
            strokeColor=color,
            fillColor=color,
            strokeWidth=0.35,
        )
    )


def add_blossom(drawing: Drawing, x: float, y: float) -> None:
    for angle in (90, 18, -54, -126, 162):
        radians = math.radians(angle)
        drawing.add(
            Circle(
                x + 3.2 * math.cos(radians),
                y + 3.2 * math.sin(radians),
                1.9,
                strokeColor=BLUE,
                fillColor=None,
                strokeWidth=0.45,
            )
        )
    drawing.add(Circle(x, y, 1.05, strokeColor=BLUE, fillColor=GOLD, strokeWidth=0.35))


def hatch_rect(drawing: Drawing, x: float, y: float, width: float, height: float) -> None:
    """Gold diagonal hatch, clipped geometrically by endpoint calculations."""

    step = 9
    for offset in range(-int(height), int(width) + int(height), step):
        x0 = max(x, x + offset)
        y0 = max(y, y - offset)
        x1 = min(x + width, x + offset + height)
        y1 = min(y + height, y + width - offset)
        if x0 <= x1 and y0 <= y1:
            drawing.add(Line(x0, y0, x1, y1, strokeColor=GOLD, strokeWidth=0.32))


def stipple_rect(drawing: Drawing, x: float, y: float, width: float, height: float) -> None:
    """Blue stipple texture for non-color separation of the right region."""

    for ix in range(int(x) + 6, int(x + width) - 2, 13):
        for iy in range(int(y) + 6, int(y + height) - 2, 13):
            drawing.add(Circle(ix, iy, 0.42, strokeColor=BLUE, fillColor=BLUE, strokeWidth=0.2))


def build_drawing(values: dict[str, Fraction]) -> Drawing:
    LAYOUT.clear()
    drawing = Drawing(W, H)
    drawing.add(Rect(0, 0, W, H, strokeColor=None, fillColor=white))

    add_text(drawing, 14, H - 16, "R0.74I moving-tube criterion and logarithmic screen", size=9.6, bold=True, layout_id="title")
    add_text(
        drawing,
        14,
        H - 28,
        "36/36 exact finite gates; analytic implications and affine exponents only; no unknown constants plotted.",
        size=5.75,
        color=MID,
        layout_id="subtitle",
    )
    add_blossom(drawing, W - 17, H - 17)
    drawing.add(Line(14, H - 36, W - 14, H - 36, strokeColor=LIGHT, strokeWidth=0.7))
    divider_x = W / 2 + 2
    drawing.add(Line(divider_x, 25, divider_x, H - 42, strokeColor=LIGHT, strokeWidth=0.7))

    panel_a = (14, 25, divider_x - 6, H - 40)
    panel_b = (divider_x + 8, 25, W - 14, H - 40)

    # Panel A: geometry is schematic; the arrows and inequalities are analytic.
    ax0, ax1 = 16, divider_x - 9
    add_text(drawing, ax0, H - 51, "A", size=8.2, bold=True, container=panel_a, layout_id="panel-a")
    add_text(drawing, ax0 + 15, H - 51, "Moving tube to a regular point", size=6.6, bold=True, container=panel_a, layout_id="panel-a-title")
    add_box(drawing, ax1 - 67, H - 63, 62, 12, stroke=BLUE, fill=BLUE_LIGHT)
    add_text(drawing, ax1 - 36, H - 59.2, "ANALYTIC CHAIN", size=4.65, color=BLUE, bold=True, anchor="middle", container=panel_a, layout_id="analytic-badge")

    # Moving-tube geometry at a representative time slice.
    gx, gy, gw, gh = ax0 + 2, H - 150, 100, 78
    add_box(drawing, gx, gy, gw, gh, stroke=LIGHT, fill=XLIGHT)
    add_text(drawing, gx + 7, gy + gh - 12, "moving-tube geometry", size=4.8, color=MID, bold=True, container=panel_a, layout_id="geometry-title")
    outer_cx, outer_cy, outer_rx, outer_ry = gx + 51.5, gy + 35, 39.5, 23
    drawing.add(Ellipse(outer_cx, outer_cy, outer_rx, outer_ry, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.8, strokeDashArray=[5, 2]))
    # Inner fixed ball, with vertical hatch to remain distinct in grayscale.
    inner_cx, inner_cy, inner_rx, inner_ry = gx + 53, gy + 35.5, 22, 15.5
    drawing.add(Ellipse(inner_cx, inner_cy, inner_rx, inner_ry, strokeColor=BLUE, fillColor=BLUE_LIGHT, strokeWidth=0.9))
    for hx in range(int(inner_cx - inner_rx + 4), int(inner_cx + inner_rx), 7):
        normalized = (hx - inner_cx) / inner_rx
        dy = inner_ry * math.sqrt(max(0.0, 1.0 - normalized * normalized))
        drawing.add(Line(hx, inner_cy - dy, hx, inner_cy + dy, strokeColor=BLUE, strokeWidth=0.3))
    # A single schematic curve: no points or numeric samples.
    path = ShapePath()
    path.moveTo(gx + 25, gy + 33)
    path.curveTo(gx + 38, gy + 47, gx + 51, gy + 24, gx + 67, gy + 37)
    path.curveTo(gx + 76, gy + 44, gx + 79, gy + 42, gx + 82, gy + 40)
    path.strokeColor = INK
    path.strokeWidth = 1.0
    path.strokeDashArray = [2, 1.5]
    path.fillColor = None
    drawing.add(path)
    drawing.add(Circle(gx + 67, gy + 37, 2.2, strokeColor=INK, fillColor=white, strokeWidth=0.8))
    drawing.add(Circle(gx + 67, gy + 37, 0.8, strokeColor=INK, fillColor=INK, strokeWidth=0.3))
    add_text(drawing, gx + 7, gy + 6, "schematic path; no samples", size=4.05, color=MID, container=panel_a, layout_id="geometry-boundary")
    add_text(drawing, gx + 59, gy + 51, "B_R(X_R(t))", size=4.0, color=GOLD, bold=True, anchor="middle", container=panel_a, layout_id="outer-ball")
    add_text(drawing, gx + 54, gy + 24, "B_(R/2)(x0)", size=3.9, color=BLUE, bold=True, anchor="middle", container=panel_a, layout_id="inner-ball")

    # Four-stage strict implication chain.
    cx, cw, ch = ax0 + 111, ax1 - (ax0 + 111), 24
    stage_ys = [H - 86, H - 119, H - 152, H - 185]
    stage = [
        ("1  E_R sufficiently small", "hypothesis; epsilon not plotted", BLUE, BLUE_LIGHT, None),
        ("2  sup |X_R(t)-x0| <= R/2", "path confinement", BLUE, white, None),
        ("3  fixed Q_(R/2) cubic is small", "<= C E_R^(3/2)", GOLD, GOLD_LIGHT, [4, 2]),
        ("4  z0 is a regular point", "velocity-only one-scale criterion", INK, white, None),
    ]
    for index, (head, body, color, fill, dash) in enumerate(stage):
        y = stage_ys[index]
        add_box(drawing, cx, y, cw, ch, stroke=color, fill=fill, dash=dash)
        add_text(drawing, cx + 6, y + 13.2, head, size=4.25, color=color, bold=True, container=panel_a, layout_id=f"stage-{index + 1}-head")
        add_text(drawing, cx + 6, y + 5.0, body, size=3.85, color=MID, container=panel_a, layout_id=f"stage-{index + 1}-body")
        if index < len(stage) - 1:
            add_arrow(drawing, cx + cw / 2, y, cx + cw / 2, stage_ys[index + 1] + ch, color=INK, dash=[3, 2] if index == 1 else None)
    add_arrow(drawing, gx + gw, gy + gh / 2, cx - 3, stage_ys[1] + ch / 2, color=GOLD, dash=[4, 2])
    add_text(drawing, ax0 + 3, 31, "Scope: no claim that E_R is small at every point or scale.", size=4.25, color=MID, container=panel_a, layout_id="panel-a-scope")

    # Panel B: exact affine screen y(gamma)=1-2 gamma.
    bx0, bx1 = divider_x + 10, W - 16
    add_text(drawing, bx0, H - 51, "B", size=8.2, bold=True, container=panel_b, layout_id="panel-b")
    add_text(drawing, bx0 + 15, H - 51, "Exact logarithmic exponent screen", size=6.55, bold=True, container=panel_b, layout_id="panel-b-title")
    add_box(drawing, bx1 - 75, H - 63, 70, 12, stroke=GOLD, fill=GOLD_LIGHT, dash=[4, 2])
    add_text(drawing, bx1 - 40, H - 59.2, "EXACT AFFINE SCREEN", size=4.45, color=GOLD, bold=True, anchor="middle", container=panel_b, layout_id="screen-badge")
    add_text(drawing, bx0 + 2, H - 72, "candidate residual power:  y(gamma) = 1 - 2 gamma", size=4.75, color=MID, bold=True, container=panel_b, layout_id="screen-formula")

    plot_x0, plot_x1 = bx0 + 38, bx1 - 8
    plot_y0, plot_y1 = 78, H - 88
    x_mid = (plot_x0 + plot_x1) / 2
    y_mid = (plot_y0 + plot_y1) / 2
    # Region fills and textures. Endpoint is a zero-width boundary line.
    drawing.add(Rect(plot_x0, plot_y0, x_mid - plot_x0, plot_y1 - plot_y0, strokeColor=None, fillColor=GOLD_LIGHT))
    hatch_rect(drawing, plot_x0, plot_y0, x_mid - plot_x0, plot_y1 - plot_y0)
    drawing.add(Rect(x_mid, plot_y0, plot_x1 - x_mid, plot_y1 - plot_y0, strokeColor=None, fillColor=BLUE_LIGHT))
    stipple_rect(drawing, x_mid, plot_y0, plot_x1 - x_mid, plot_y1 - plot_y0)
    drawing.add(Rect(plot_x0, plot_y0, plot_x1 - plot_x0, plot_y1 - plot_y0, strokeColor=LIGHT, fillColor=None, strokeWidth=0.75))

    # Axis map: gamma in [0,1], y in [-1,1].
    def xp(gamma: Fraction) -> float:
        return plot_x0 + float(gamma) * (plot_x1 - plot_x0)

    def yp(value: Fraction) -> float:
        return plot_y0 + (float(value) + 1.0) * (plot_y1 - plot_y0) / 2.0

    drawing.add(Line(plot_x0, y_mid, plot_x1, y_mid, strokeColor=INK, strokeWidth=0.75))
    drawing.add(Line(plot_x0, plot_y0, plot_x0, plot_y1, strokeColor=INK, strokeWidth=0.75))
    drawing.add(Line(x_mid, plot_y0, x_mid, plot_y1, strokeColor=INK, strokeWidth=0.85, strokeDashArray=[4, 2]))
    for gamma in (Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), Fraction(1)):
        x = xp(gamma)
        drawing.add(Line(x, plot_y0, x, plot_y0 - 3, strokeColor=INK, strokeWidth=0.6))
        label = {Fraction(0): "0", Fraction(1, 4): "1/4", Fraction(1, 2): "1/2", Fraction(3, 4): "3/4", Fraction(1): "1"}[gamma]
        add_text(drawing, x, plot_y0 - 10, label, size=4.15, color=MID, bold=True, anchor="middle", container=panel_b, layout_id=f"gamma-{label}")
    for value in (Fraction(-1), Fraction(-1, 2), Fraction(0), Fraction(1, 2), Fraction(1)):
        y = yp(value)
        drawing.add(Line(plot_x0 - 3, y, plot_x0, y, strokeColor=INK, strokeWidth=0.6))
        label = {Fraction(-1): "-1", Fraction(-1, 2): "-1/2", Fraction(0): "0", Fraction(1, 2): "1/2", Fraction(1): "1"}[value]
        add_text(drawing, plot_x0 - 6, y - 1.6, label, size=3.85, color=MID, bold=True, anchor="end", container=panel_b, layout_id=f"y-{label}")

    # Exact affine line and non-color-distinct point markers.
    drawing.add(Line(xp(Fraction(0)), yp(Fraction(1)), xp(Fraction(1)), yp(Fraction(-1)), strokeColor=INK, strokeWidth=1.45))
    for gamma, kind in ((Fraction(0), "circle"), (Fraction(1, 4), "square"), (Fraction(1, 2), "diamond"), (Fraction(3, 4), "square"), (Fraction(1), "circle")):
        x, y = xp(gamma), yp(screen_y(gamma))
        if kind == "circle":
            drawing.add(Circle(x, y, 2.35, strokeColor=INK, fillColor=white, strokeWidth=0.9))
        elif kind == "square":
            drawing.add(Rect(x - 2.2, y - 2.2, 4.4, 4.4, strokeColor=INK, fillColor=white, strokeWidth=0.9))
        else:
            drawing.add(Polygon([x, y + 3.0, x + 3.0, y, x, y - 3.0, x - 3.0, y], strokeColor=GOLD, fillColor=white, strokeWidth=1.0))

    add_text(drawing, plot_x0 - 18, plot_y1 + 3, "y", size=4.8, color=INK, bold=True, anchor="middle", container=panel_b, layout_id="y-axis-title")
    add_text(drawing, (plot_x0 + plot_x1) / 2, plot_y0 - 20, "gamma", size=4.3, color=INK, bold=True, anchor="middle", container=panel_b, layout_id="x-axis-title")
    add_text(drawing, (plot_x0 + x_mid) / 2, plot_y0 + 25, "gamma < 1/2", size=4.35, color=GOLD, bold=True, anchor="middle", container=panel_b, layout_id="rejected-range")
    add_text(drawing, (plot_x0 + x_mid) / 2, plot_y0 + 15, "REJECTED", size=5.15, color=GOLD, bold=True, anchor="middle", container=panel_b, layout_id="rejected-label")
    add_text(drawing, (x_mid + plot_x1) / 2, plot_y1 - 17, "gamma > 1/2", size=4.35, color=BLUE, bold=True, anchor="middle", container=panel_b, layout_id="not-rejected-range")
    add_text(drawing, (x_mid + plot_x1) / 2, plot_y1 - 47, "NOT REJECTED / NOT PROVED", size=4.15, color=BLUE, bold=True, anchor="middle", container=panel_b, layout_id="not-rejected-label")
    add_box(drawing, x_mid + 5, y_mid + 5, 68, 13, stroke=GOLD, fill=white)
    add_text(drawing, x_mid + 39, y_mid + 9.2, "OPEN ENDPOINT", size=4.15, color=INK, bold=True, anchor="middle", container=panel_b, layout_id="endpoint-label")
    add_text(drawing, x_mid + 6, y_mid - 9, "y=0", size=3.8, color=INK, bold=True, container=panel_b, layout_id="endpoint-zero")

    add_box(drawing, bx0 + 2, 25, bx1 - bx0 - 4, 31, stroke=LIGHT, fill=white)
    add_text(drawing, bx0 + 9, 44, "log window:  2rho <= lim log(P_j)/L_j^2 <= 3rho", size=4.25, color=INK, bold=True, container=panel_b, layout_id="log-window")
    add_text(drawing, bx0 + 9, 35, "rho=1/320; width=1/320; lacunarity exponent=1/64", size=4.05, color=MID, container=panel_b, layout_id="log-constants")
    add_text(drawing, bx0 + 9, 27.5, "Screen applies along realized lacunary P_j only.", size=3.95, color=MID, container=panel_b, layout_id="lacunary-boundary")

    # Full-width status footer.
    drawing.add(Rect(14, 5, W - 28, 15, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.75))
    add_text(drawing, 21, 10, "EXACT DIAGRAM", size=5.2, color=GOLD, bold=True, layout_id="footer-exact")
    add_text(drawing, W / 2, 10, "NOT DNS  ·  NOT SIMULATION", size=4.9, color=INK, bold=True, anchor="middle", layout_id="footer-simulation")
    add_text(drawing, W - 21, 10, "NOT CLAY", size=5.5, color=INK, bold=True, anchor="end", layout_id="footer-clay")
    return drawing


def poppler_version() -> str:
    completed = subprocess.run([str(PDFINFO), "-v"], capture_output=True, text=True)
    return (completed.stderr or completed.stdout).splitlines()[0].strip()


def rasterize_pdf(pdf_path: Path, prefix: Path, dpi: int) -> Path:
    subprocess.run(
        [str(PDFTOPPM), "-png", "-r", str(dpi), "-singlefile", str(pdf_path), str(prefix)],
        check=True,
        capture_output=True,
    )
    output = prefix.with_suffix(".png")
    if not output.exists():
        raise RuntimeError(f"Poppler did not create {output.name}")
    return output


def main() -> None:
    assert_text_eof_policy()
    certificate, values = load_exact()
    write_source_data(values)
    drawing = build_drawing(values)

    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"), showBoundary=False)
    renderPDF.drawToFile(drawing, str(HERE / "figure.pdf"), showBoundary=False)

    master_tmp = rasterize_pdf(HERE / "figure.pdf", HERE / "_figure-600", DPI)
    master = Image.open(master_tmp).convert("RGB")
    master.save(HERE / "figure.png", dpi=(DPI, DPI), optimize=False)
    master_tmp.unlink()
    ImageOps.grayscale(master).save(HERE / "qa-grayscale.png", dpi=(DPI, DPI), optimize=False)
    final_width = 1800
    final_height = round(master.height * final_width / master.width)
    master.resize((final_width, final_height), Image.Resampling.LANCZOS).save(
        HERE / "qa-final-size.png", dpi=(254, 254), optimize=False
    )
    pdf_qa_tmp = rasterize_pdf(HERE / "figure.pdf", HERE / "qa-pdf", 300)
    pdf_qa = Image.open(pdf_qa_tmp).convert("RGB")
    pdf_qa.save(HERE / "qa-pdf.png", dpi=(300, 300), optimize=False)

    write_canonical_text(
        HERE / "layout-bounds.json",
        json.dumps(
            {
                "canvasPt": [round(W, 4), round(H, 4)],
                "method": "ReportLab stringWidth plus ascent/descent proxy",
                "entries": LAYOUT,
                "summary": {
                    "passed": sum(bool(item["proxyPass"]) for item in LAYOUT),
                    "total": len(LAYOUT),
                },
            },
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
    )
    write_canonical_text(
        HERE / "environment.json",
        json.dumps(
            {
                "certificateChecks": "36/36",
                "certificatePath": str(CERTIFICATE.relative_to(REPO)),
                "certificateSha256": sha256(CERTIFICATE),
                "certificateStdoutByteIdentical": True,
                "figureId": FIGURE_ID,
                "fontBold": {"path": str(FONT_BOLD), "sha256": sha256(FONT_BOLD)},
                "fontRegular": {"path": str(FONT_REGULAR), "sha256": sha256(FONT_REGULAR)},
                "pdfinfo": str(PDFINFO),
                "pdftoppm": str(PDFTOPPM),
                "platform": platform.platform(),
                "poppler": poppler_version(),
                "producerPath": str(PRODUCER.relative_to(REPO)),
                "producerSha256": sha256(PRODUCER),
                "python": sys.version.split()[0],
                "reportlab": __import__("reportlab").Version,
            },
            indent=2,
            sort_keys=True,
            ensure_ascii=False,
        )
        + "\n",
    )
    write_canonical_text(
        HERE / "results.json",
        json.dumps(
            {
                "certificate": certificate["summary"],
                "figureId": FIGURE_ID,
                "layout": {
                    "passed": sum(bool(item["proxyPass"]) for item in LAYOUT),
                    "total": len(LAYOUT),
                },
                "panelA": "moving-tube geometry and strict analytic implication chain",
                "panelB": "exact affine exponent screen y(gamma)=1-2 gamma",
                "status": "GENERATED",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )
    assert_text_eof_policy()
    print(
        f"generated {FIGURE_ID}: {len(LAYOUT)} text bounds; "
        f"certificate {certificate['summary']['passed']}/{certificate['summary']['total']} PASS"
    )


if __name__ == "__main__":
    main()
