#!/usr/bin/env python3
"""Render the deterministic R0.74J fifth-shell payment figure.

The figure is an exact analytic geometry/payment diagram.  It contains no
DNS, simulation, sampled trajectory, or empirical proxy.  Every quantitative
label is reconstructed from the frozen 38/38 exact certificate after source
hash and byte-identity checks.
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
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074j_matching_payment_certificate.json"
PRODUCER = REPO / "scripts/r074j_matching_payment_certificate.py"
EXPECTED_CERT_SHA256 = "493c9cf6bc1357b36da1b0a13becbc51e62ea26aab95b6af7eaeb085b65be5d5"
EXPECTED_PRODUCER_SHA256 = "6dcc03d283612306dc39669f5b6c8b3cf8569e40205e067c4db0c2b6929879ec"
FIGURE_ID = "fig-r074j-fifth-shell-payment"

BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFTOPPM = BUNDLE / "bin/override/pdftoppm"
PDFINFO = BUNDLE / "bin/override/pdfinfo"

WIDTH_MM = 178
HEIGHT_MM = 88
DPI = 600
W = WIDTH_MM * mm
H = HEIGHT_MM * mm

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
LAYOUT: list[dict] = []


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def write_text(path: Path, content: str) -> None:
    path.write_text(content.replace("\r\n", "\n").rstrip("\n") + "\n", encoding="utf-8")


def assert_text_eof_policy() -> None:
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
        raise RuntimeError("text EOF policy failed: " + ", ".join(failures))


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


FONT_REGULAR = locate_font("DejaVuSans.ttf")
FONT_BOLD = locate_font("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074J-Regular", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("R074J-Bold", str(FONT_BOLD)))


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def load_exact() -> tuple[dict, dict[str, Fraction]]:
    if sha256(CERTIFICATE) != EXPECTED_CERT_SHA256:
        raise RuntimeError("certificate hash mismatch")
    if sha256(PRODUCER) != EXPECTED_PRODUCER_SHA256:
        raise RuntimeError("producer hash mismatch")
    regenerated = subprocess.run(
        [sys.executable, str(PRODUCER)], check=True, capture_output=True
    ).stdout
    if regenerated != CERTIFICATE.read_bytes():
        raise RuntimeError("producer stdout is not byte-identical to certificate")
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate.get("result") != "PASS":
        raise RuntimeError("certificate result is not PASS")
    if certificate.get("summary") != {"passed": 38, "total": 38}:
        raise RuntimeError("certificate is not the frozen 38/38 object")
    checks = {item["id"]: item for item in certificate.get("checks", [])}
    if len(checks) != 38 or not all(item.get("pass") is True for item in checks.values()):
        raise RuntimeError("certificate Boolean gates are incomplete")

    def value(check_id: str, field: str = "left") -> Fraction:
        return Fraction(checks[check_id][field])

    values = {
        "shell_index": value("payment_shell_index"),
        "radius_ratio": value("payment_radius_over_R"),
        "shell_inner": value("shell_inner_over_R"),
        "shell_outer": value("shell_outer_over_R"),
        "box_outer_square": value("box_outer_square_is_inside_shell_outer"),
        "box_outer_square_bound": value("box_outer_square_is_inside_shell_outer", "right"),
        "box_margin": value("box_outer_squared_margin"),
        "box_volume": value("box_volume_coefficient"),
        "gamma_exponent": value("gamma5_exponent"),
        "R_cap": value("R_cap"),
        "plateau_distance": value("left_plateau_distance_over_R"),
        "exit_probability": value("exit_probability_upper"),
        "theta_lower": value("theta_rational_lower"),
        "time_length": value("I_2R_length_coefficient"),
        "normalization": value("payment_normalization_coefficient"),
        "theta_cube": value("theta_cube_floor"),
        "Gu_coefficient": value("Gu_lower_coefficient"),
        "Gu_R_power": value("Gu_R_power"),
        "rho": value("rho_exact_value"),
        "payment_rate": value("log_payment_coefficient"),
        "lacunarity": value("lacunarity_coefficient"),
        "frontier_L": value("frontier_total_L_power"),
    }
    expected = {
        "shell_index": Fraction(5),
        "radius_ratio": Fraction(2),
        "shell_inner": Fraction(64),
        "shell_outer": Fraction(128),
        "box_outer_square": Fraction(9218),
        "box_outer_square_bound": Fraction(16384),
        "box_margin": Fraction(7166),
        "box_volume": Fraction(64),
        "gamma_exponent": Fraction(8),
        "R_cap": Fraction(1, 200),
        "plateau_distance": Fraction(48),
        "exit_probability": Fraction(65, 1152),
        "theta_lower": Fraction(511, 576),
        "time_length": Fraction(4),
        "normalization": Fraction(1, 4),
        "theta_cube": Fraction(1, 8),
        "Gu_coefficient": Fraction(8),
        "Gu_R_power": Fraction(3),
        "rho": Fraction(1, 320),
        "payment_rate": Fraction(3, 320),
        "lacunarity": Fraction(9, 320),
        "frontier_L": Fraction(1),
    }
    if values != expected:
        raise RuntimeError("exact R0.74J value map drift")
    return certificate, values


def write_source_data(v: dict[str, Fraction]) -> None:
    rows = [
        ["A", "payment_radius_over_R", q(v["radius_ratio"]), "payment_radius=2R", "FINITE EXACT", "payment radius"],
        ["A", "shell_index", q(v["shell_index"]), "k=5", "FINITE EXACT", "annular row"],
        ["A", "shell_inner_over_R", q(v["shell_inner"]), "2^5(2R)=64R", "FINITE EXACT", "closed inner boundary"],
        ["A", "shell_outer_over_R", q(v["shell_outer"]), "2^6(2R)=128R", "FINITE EXACT", "open outer boundary"],
        ["A", "proof_box_x3_lower_over_R", "80/1", "80R", "ANALYTIC INPUT", "central lift"],
        ["A", "proof_box_x3_upper_over_R", "96/1", "96R", "ANALYTIC INPUT", "central lift"],
        ["A", "proof_box_volume_over_R3", q(v["box_volume"]), "(2R)(2R)(16R)", "FINITE EXACT", "64R^3"],
        ["A", "outer_square", q(v["box_outer_square"]), "96^2+1+1", "FINITE EXACT", "less than 128^2"],
        ["A", "outer_square_margin", q(v["box_margin"]), "128^2-9218", "FINITE EXACT", "positive containment margin"],
        ["A", "plateau_distance_over_R", q(v["plateau_distance"]), "80R-32R", "PROVED ANALYTIC CONSEQUENCE", "circle distance floor"],
        ["A", "exit_probability_upper", q(v["exit_probability"]), "130/2304", "FINITE EXACT", "Chebyshev arithmetic"],
        ["A", "theta_lower", q(v["theta_lower"]), "1-65/576", "PROVED ANALYTIC CONSEQUENCE", "strictly above 1/2"],
        ["B", "time_length_over_R2", q(v["time_length"]), "|I_(2R)|=4R^2", "FINITE EXACT", "time ledger"],
        ["B", "payment_normalization", q(v["normalization"]), "(2R)^-2=(1/4)R^-2", "FINITE EXACT", "normalization ledger"],
        ["B", "theta_cube_floor", q(v["theta_cube"]), "(1/2)^3", "FINITE EXACT", "profile floor"],
        ["B", "Gu_lower_coefficient", q(v["Gu_coefficient"]), "(1/4)*4*64*(1/8)", "FINITE EXACT", "finite coefficient inside the analytic lower bound"],
        ["B", "Gu_R_power", q(v["Gu_R_power"]), "-2+2+3", "FINITE EXACT", "R exponent"],
        ["B", "log_payment_rate", q(v["payment_rate"]), "3/320", "PROVED", "limit of log(P_j)/L_j^2"],
        ["B", "old_log_window_lower", "1/160", "2/320", "INHERITED", "R0.74I liminf lower bound"],
        ["B", "old_log_window_upper", q(v["payment_rate"]), "3/320", "INHERITED", "R0.74I limsup upper bound"],
        ["B", "lacunarity_rate", q(v["lacunarity"]), "9/320", "PROVED", "log(P_(j+1)/P_j)/L_j^2"],
        ["B", "frontier_L_power", q(v["frontier_L"]), "P^(2/3)sqrt(log P)", "PROVED FOR FAMILY", "endpoint compatibility only"],
    ]
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["panel", "record", "value_exact", "formula", "status", "note"])
        writer.writerows(rows)


def add_text(
    drawing: Drawing,
    x: float,
    y: float,
    text: str,
    *,
    size: float = 5.3,
    color=INK,
    bold: bool = False,
    anchor: str = "start",
    container: tuple[float, float, float, float] | None = None,
    layout_id: str = "text",
) -> None:
    font = "R074J-Bold" if bold else "R074J-Regular"
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
            "boundsPt": [round(item, 4) for item in bounds],
            "containerPt": [round(item, 4) for item in region],
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
) -> None:
    line = Line(x0, y0, x1, y1, strokeColor=color, strokeWidth=0.85)
    if dash:
        line.strokeDashArray = dash
    drawing.add(line)
    angle = math.atan2(y1 - y0, x1 - x0)
    length = 3.2
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
            strokeWidth=0.3,
        )
    )


def hatch(drawing: Drawing, x: float, y: float, width: float, height: float) -> None:
    for offset in range(-int(height), int(width) + int(height), 8):
        x0 = max(x, x + offset)
        y0 = max(y, y - offset)
        x1 = min(x + width, x + offset + height)
        y1 = min(y + height, y + width - offset)
        if x0 <= x1 and y0 <= y1:
            drawing.add(Line(x0, y0, x1, y1, strokeColor=GOLD, strokeWidth=0.3))


def blossom(drawing: Drawing, x: float, y: float) -> None:
    for angle in (90, 18, -54, -126, 162):
        r = math.radians(angle)
        drawing.add(Circle(x + 3.2 * math.cos(r), y + 3.2 * math.sin(r), 1.9, strokeColor=BLUE, fillColor=None, strokeWidth=0.45))
    drawing.add(Circle(x, y, 1.05, strokeColor=BLUE, fillColor=GOLD, strokeWidth=0.35))


def build_drawing(v: dict[str, Fraction]) -> Drawing:
    LAYOUT.clear()
    drawing = Drawing(W, H)
    drawing.add(Rect(0, 0, W, H, strokeColor=None, fillColor=white))
    add_text(drawing, 14, H - 16, "R0.74J exact fifth-shell payment law", size=9.6, bold=True, layout_id="title")
    add_text(
        drawing,
        14,
        H - 28,
        "38/38 finite gates; analytic heat lower bound plus a nonnegative-row payment ledger.",
        size=5.65,
        color=MID,
        layout_id="subtitle",
    )
    blossom(drawing, W - 17, H - 17)
    drawing.add(Line(14, H - 36, W - 14, H - 36, strokeColor=LIGHT, strokeWidth=0.7))
    divider = W / 2 + 2
    drawing.add(Line(divider, 25, divider, H - 42, strokeColor=LIGHT, strokeWidth=0.7))
    panel_a = (14, 25, divider - 6, H - 40)
    panel_b = (divider + 8, 18, W - 14, H - 40)

    ax0, ax1 = 16, divider - 9
    add_text(drawing, ax0, H - 51, "A", size=8.2, bold=True, container=panel_a, layout_id="panel-a")
    add_text(drawing, ax0 + 15, H - 51, "Exact fifth-shell geometry", size=6.6, bold=True, container=panel_a, layout_id="panel-a-title")
    add_box(drawing, ax1 - 68, H - 63, 63, 12, stroke=BLUE, fill=BLUE_LIGHT)
    add_text(drawing, ax1 - 36.5, H - 59.2, "ANALYTIC + FINITE", size=4.45, color=BLUE, bold=True, anchor="middle", container=panel_a, layout_id="panel-a-badge")

    gx0, gx1 = ax0 + 12, ax1 - 8
    gy0, gy1 = H - 118, H - 78
    add_box(drawing, gx0, gy0, gx1 - gx0, gy1 - gy0, stroke=LIGHT, fill=XLIGHT)

    def xmap(value: float) -> float:
        return gx0 + 9 + (value - 56) / (132 - 56) * (gx1 - gx0 - 18)

    shell_x0, shell_x1 = xmap(64), xmap(128)
    drawing.add(Rect(shell_x0, gy0 + 13, shell_x1 - shell_x0, 14, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.8))
    hatch(drawing, shell_x0, gy0 + 13, shell_x1 - shell_x0, 14)
    box_x0, box_x1 = xmap(80), xmap(96)
    drawing.add(Rect(box_x0, gy0 + 10, box_x1 - box_x0, 20, strokeColor=BLUE, fillColor=BLUE_LIGHT, strokeWidth=1.05))
    for value in (64, 80, 96, 128):
        x = xmap(value)
        drawing.add(Line(x, gy0 + 7, x, gy0 + 10, strokeColor=INK, strokeWidth=0.55))
        add_text(drawing, x, gy0 + 2, str(value), size=3.8, color=MID, bold=True, anchor="middle", container=panel_a, layout_id=f"x3-{value}")
    add_text(drawing, (shell_x0 + shell_x1) / 2, gy0 + 32, "A_5(2R): 64R <= |x| < 128R", size=4.25, color=GOLD, bold=True, anchor="middle", container=panel_a, layout_id="shell-label")
    add_text(drawing, (box_x0 + box_x1) / 2, gy0 + 18, "Q_R", size=4.4, color=BLUE, bold=True, anchor="middle", container=panel_a, layout_id="box-label")
    add_text(drawing, gx1 - 6, gy0 - 6, "coordinate: x3/R", size=3.75, color=MID, bold=True, anchor="end", container=panel_a, layout_id="axis-label")

    add_box(drawing, ax0 + 4, H - 159, 103, 30, stroke=BLUE, fill=white)
    add_text(drawing, ax0 + 10, H - 140, "|x1|, |x2| < R  (schematic thickness)", size=4.05, color=MID, container=panel_a, layout_id="transverse")
    add_text(drawing, ax0 + 10, H - 150, "|Q_R| = 64 R^3", size=4.7, color=BLUE, bold=True, container=panel_a, layout_id="box-volume")
    add_text(drawing, ax0 + 10, H - 157, "9218 < 128^2; margin = 7166", size=3.8, color=MID, container=panel_a, layout_id="outer-margin")

    add_box(drawing, ax0 + 115, H - 159, ax1 - (ax0 + 115), 30, stroke=GOLD, fill=GOLD_LIGHT)
    add_text(drawing, ax0 + 121, H - 140, "dist_T(x3, P_R^c) >= 48R", size=4.0, color=GOLD, bold=True, container=panel_a, layout_id="distance-floor")
    add_text(drawing, ax0 + 121, H - 150, "P(exit) <= 65/1152", size=4.0, color=INK, container=panel_a, layout_id="exit-floor")
    add_text(drawing, ax0 + 121, H - 157, "theta >= 511/576 > 1/2", size=4.0, color=BLUE, bold=True, container=panel_a, layout_id="theta-floor")

    add_arrow(drawing, ax0 + 54, H - 166, ax0 + 54, H - 176, color=BLUE)
    add_arrow(drawing, ax0 + 164, H - 166, ax0 + 164, H - 176, color=GOLD)
    add_box(drawing, ax0 + 4, 31, ax1 - ax0 - 8, 39, stroke=LIGHT, fill=white)
    add_text(drawing, ax0 + 11, 57, "ledger: (2R)^-2 · |I_(2R)| · |Q_R| · (1/2)^3", size=4.35, color=INK, bold=True, container=panel_a, layout_id="ledger")
    add_text(drawing, ax0 + 11, 47, "       = (1/4) · 4 · 64 · (1/8) · R^3 = 8 R^3", size=4.2, color=BLUE, bold=True, container=panel_a, layout_id="ledger-product")
    add_text(drawing, ax0 + 11, 37, "annular weight: Gamma_5 = e^-8", size=4.15, color=GOLD, bold=True, container=panel_a, layout_id="gamma-five")

    bx0, bx1 = divider + 10, W - 16
    add_text(drawing, bx0, H - 51, "B", size=8.2, bold=True, container=panel_b, layout_id="panel-b")
    add_text(drawing, bx0 + 15, H - 51, "Matching complete payment", size=6.6, bold=True, container=panel_b, layout_id="panel-b-title")
    add_box(drawing, bx1 - 63, H - 63, 58, 12, stroke=GOLD, fill=GOLD_LIGHT)
    add_text(drawing, bx1 - 34, H - 59.2, "PROVED FOR FAMILY", size=4.15, color=GOLD, bold=True, anchor="middle", container=panel_b, layout_id="panel-b-badge")

    chain_x = bx0 + 15
    chain_w = bx1 - chain_x - 4
    stages = [
        (H - 91, "1  positive heat platform", "theta >= 1/2 on I_(2R) x Q_R", BLUE, BLUE_LIGHT),
        (H - 123, "2  cubic payment row", "G_u >= 8 e^-8 B^3 R^3", GOLD, GOLD_LIGHT),
        (H - 155, "3  complete nonnegative payment", "8 e^-8 B_j^3 R_j^3 <= P_j <= C B_j^3 R_j^3", BLUE, white),
        (H - 187, "4  exact family rate", "log(P_j)/L_j^2 -> 3/320", INK, white),
    ]
    for index, (y, head, body, color, fill) in enumerate(stages):
        add_box(drawing, chain_x, y, chain_w, 23, stroke=color, fill=fill, dash=[4, 2] if index == 2 else None)
        add_text(drawing, chain_x + 7, y + 13, head, size=4.35, color=color, bold=True, container=panel_b, layout_id=f"chain-{index+1}-head")
        add_text(drawing, chain_x + 7, y + 5, body, size=3.9, color=MID if index != 1 else GOLD, bold=index == 1, container=panel_b, layout_id=f"chain-{index+1}-body")
        if index < 3:
            add_arrow(drawing, chain_x + chain_w / 2, y, chain_x + chain_w / 2, stages[index + 1][0] + 23, color=INK)

    chart_x0, chart_x1 = bx0 + 24, bx1 - 10
    chart_y = 43
    drawing.add(Line(chart_x0, chart_y, chart_x1, chart_y, strokeColor=INK, strokeWidth=0.7))
    x_two = chart_x0
    x_three = chart_x1
    drawing.add(Rect(x_two, chart_y + 7, x_three - x_two, 8, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.7))
    hatch(drawing, x_two, chart_y + 7, x_three - x_two, 8)
    drawing.add(Line(x_three, chart_y - 4, x_three, chart_y + 20, strokeColor=BLUE, strokeWidth=1.5))
    drawing.add(Circle(x_three, chart_y + 11, 2.2, strokeColor=BLUE, fillColor=white, strokeWidth=1.0))
    add_text(drawing, x_two, chart_y - 9, "2/320", size=3.85, color=MID, bold=True, anchor="middle", container=panel_b, layout_id="two-rho")
    add_text(drawing, x_three - 3, chart_y - 9, "3/320", size=3.85, color=BLUE, bold=True, anchor="middle", container=panel_b, layout_id="three-rho")
    add_text(drawing, (x_two + x_three) / 2, chart_y + 16, "R0.74I liminf/limsup window", size=3.8, color=GOLD, bold=True, anchor="middle", container=panel_b, layout_id="old-window")
    add_text(drawing, x_three - 4, chart_y + 27, "R0.74J exact rate", size=3.85, color=BLUE, bold=True, anchor="end", container=panel_b, layout_id="new-rate")
    add_text(drawing, bx0 + 4, 28, "also: log(P_(j+1)/P_j) = (9/320)L_j^2 + O(1)", size=4.0, color=MID, container=panel_b, layout_id="lacunarity")
    add_text(drawing, bx0 + 4, 20.5, "sqrt-log endpoint upper remains OPEN", size=4.0, color=GOLD, bold=True, container=panel_b, layout_id="endpoint-open")

    drawing.add(Rect(14, 5, W - 28, 12, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.75))
    add_text(drawing, 21, 8.7, "EXACT FAMILY", size=4.9, color=GOLD, bold=True, layout_id="footer-exact")
    add_text(drawing, W / 2, 8.7, "NOT DNS  ·  NOT SIMULATION", size=4.7, color=INK, bold=True, anchor="middle", layout_id="footer-simulation")
    add_text(drawing, W - 21, 8.7, "NOT CLAY", size=5.1, color=INK, bold=True, anchor="end", layout_id="footer-clay")
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
    final_width = 1780
    final_height = round(master.height * final_width / master.width)
    master.resize((final_width, final_height), Image.Resampling.LANCZOS).save(
        HERE / "qa-final-size.png", dpi=(254, 254), optimize=False
    )
    qa_tmp = rasterize_pdf(HERE / "figure.pdf", HERE / "qa-pdf", 300)
    qa_pdf = Image.open(qa_tmp).convert("RGB")
    qa_pdf.save(HERE / "qa-pdf.png", dpi=(300, 300), optimize=False)

    write_text(
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
        ),
    )
    write_text(
        HERE / "environment.json",
        json.dumps(
            {
                "certificateChecks": "38/38",
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
        ),
    )
    write_text(
        HERE / "results.json",
        json.dumps(
            {
                "certificate": certificate["summary"],
                "figureId": FIGURE_ID,
                "layout": {
                    "passed": sum(bool(item["proxyPass"]) for item in LAYOUT),
                    "total": len(LAYOUT),
                },
                "panelA": "exact fifth-shell geometry and heat-platform lower bound",
                "panelB": "matching complete-payment and logarithmic-rate chain",
                "status": "GENERATED",
            },
            indent=2,
            sort_keys=True,
        ),
    )
    assert_text_eof_policy()
    print(
        f"generated {FIGURE_ID}: {len(LAYOUT)} text bounds; "
        f"certificate {certificate['summary']['passed']}/{certificate['summary']['total']} PASS"
    )


if __name__ == "__main__":
    main()
