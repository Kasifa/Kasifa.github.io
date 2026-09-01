#!/usr/bin/env python3
"""Build the deterministic R0.74H collar-flux journal figure.

Every plotted exponent is read from the frozen 25/25 exact certificate.
Panel A is an exact implication diagram and Panel B is an exponent diagram;
neither panel is DNS, simulation, sampled-path output, or empirical data.
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
CERTIFICATE = REPO / "research/r074h_collar_flux_certificate.json"
PRODUCER = REPO / "scripts/r074h_collar_flux_certificate.py"
EXPECTED_CERT_SHA256 = "783591f3da880ec9182be89c585eb732e35d5842b7d196dc2ae4e35b6c0d2ba4"
EXPECTED_PRODUCER_SHA256 = "acce024b8dd78ba727e3ec8176a308dc53ecc34b7bdaf57b6c48e5d1e1a5c6e4"
FIGURE_ID = "fig-r074h-collar-flux-repair"

WIDTH_MM = 180
HEIGHT_MM = 82
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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def locate_font(filename: str) -> Path:
    candidates = [
        Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype") / filename,
        Path("/System/Library/Fonts/Supplemental") / filename,
        Path("/Library/Fonts") / filename,
    ]
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"required font not found: {filename}")


FONT_REGULAR = locate_font("DejaVuSans.ttf")
FONT_BOLD = locate_font("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074H-Regular", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("R074H-Bold", str(FONT_BOLD)))


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
    if certificate.get("summary") != {"passed": 25, "total": 25}:
        raise RuntimeError("certificate is not the frozen 25/25 object")
    items = certificate.get("checks", [])
    if len(items) != 25 or not all(item.get("pass") is True for item in items):
        raise RuntimeError("certificate Boolean gates are incomplete")
    checks = {item["id"]: item for item in items}

    def value(check_id: str, field: str = "left") -> Fraction:
        return Fraction(checks[check_id][field])

    values = {
        "cutoff_power": value("small_payment_absorption_exponents"),
        "linear_power": value("small_payment_absorption_exponents", "right"),
        "energy_outer_power": value("energy_payment_outer_power"),
        "acceleration_outer_power": value("acceleration_payment_outer_power"),
        "collar_outer_power": value("collar_payment_outer_power"),
        "old_L_power": value("old_payment_23_L_power"),
        "missing_L_power": value("target_over_old_23_L_power"),
        "flux_inside_L_power": value("cubic_flux_L_power"),
        "flux_outside_L_power": value("collar_payment_outer_power"),
        "old_B_power": value("old_payment_23_B_power"),
        "old_R_power": value("old_payment_23_R_power"),
        "flux_B_power": value("cubic_flux_B_power"),
        "flux_R_power": value("cubic_flux_R_power"),
        "sum_constant": value("flux_repair_sum_constant"),
    }
    if values["cutoff_power"] != Fraction(2, 3):
        raise RuntimeError("cutoff exponent drift")
    if values["linear_power"] != 1:
        raise RuntimeError("linear exponent drift")
    if values["old_L_power"] != 0 or values["missing_L_power"] != 1:
        raise RuntimeError("explicit-family L-exponent drift")
    if values["flux_inside_L_power"] != Fraction(3, 2):
        raise RuntimeError("cubicized collar exponent drift")
    if values["flux_outside_L_power"] != 1:
        raise RuntimeError("outer collar exponent drift")
    return certificate, values


def write_source_data(values: dict[str, Fraction]) -> None:
    rows = [
        ["A", "quadratic_cutoff", q(values["cutoff_power"]), "P_0^(2/3)", "EXACT EXPONENT", "quadratic cutoff row"],
        ["A", "energy_after_outer_power", q(values["energy_outer_power"]), "(E^(3/2))^(2/3)=E", "EXACT IDENTITY", "buffered energy becomes linear"],
        ["A", "acceleration_after_outer_power", q(values["acceleration_outer_power"]), "(J_acc^(3/2))^(2/3)=J_acc", "EXACT IDENTITY", "Version-F acceleration is already paid"],
        ["A", "collar_after_outer_power", q(values["collar_outer_power"]), "(C_R^(3/2))^(2/3)=C_R", "EXACT IDENTITY", "positive collar flux becomes linear"],
        ["A", "small_regime_reference", q(values["cutoff_power"]), "0<=P<=1: P<=P^(2/3)", "EXACT IMPLICATION", "small-payment closure"],
        ["A", "large_regime_reference", q(values["linear_power"]), "P>=1: P^(2/3)<=P", "EXACT IMPLICATION", "linear ledger dominates at large payment"],
        ["A", "repair_sum_constant", q(values["sum_constant"]), "P^(2/3)+C<=2(P+C^(3/2))^(2/3)", "EXACT IMPLICATION", "non-sharp algebraic factor"],
        ["B", "old_payment", q(values["old_L_power"]), "P^(2/3)/(B^2 R^2) ~ L^0", "CERTIFIED EXPONENT", "old payment misses L"],
        ["B", "endpoint", q(values["missing_L_power"]), "X/(B^2 R^2) >= c L^1", "ANALYTIC LOWER SCALE", "R0.74F-G terminal target"],
        ["B", "positive_collar_flux", q(values["flux_outside_L_power"]), "C_R/(B^2 R^2) >= c L^1", "ANALYTIC LOWER SCALE", "R0.74H positive flux lower bound"],
        ["B", "cubicized_collar_inside_payment", q(values["flux_inside_L_power"]), "C_R^(3/2)/(B^3 R^3) >= c L^(3/2)", "CERTIFIED EXPONENT", "inside repaired payment"],
    ]
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["panel", "record", "L_exponent_exact", "formula", "status", "note"])
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
    font = "R074H-Bold" if bold else "R074H-Regular"
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
    LAYOUT.append({
        "id": layout_id,
        "text": text,
        "fontPt": size,
        "boundsPt": [round(v, 4) for v in bounds],
        "containerPt": [round(v, 4) for v in region],
        "proxyPass": within,
    })
    drawing.add(String(x, y, text, fontName=font, fontSize=size, fillColor=color, textAnchor=anchor))


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
    box = Rect(x, y, width, height, rx=radius, ry=radius, strokeColor=stroke, fillColor=fill, strokeWidth=line_width)
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)


def add_marker(drawing: Drawing, x: float, y: float, kind: str, *, color, fill, size: float = 2.6) -> None:
    if kind == "circle":
        drawing.add(Circle(x, y, size, strokeColor=color, fillColor=fill, strokeWidth=0.95))
    elif kind == "square":
        drawing.add(Rect(x - size, y - size, 2 * size, 2 * size, strokeColor=color, fillColor=fill, strokeWidth=0.95))
    elif kind == "diamond":
        drawing.add(Polygon([x, y + size, x + size, y, x, y - size, x - size, y], strokeColor=color, fillColor=fill, strokeWidth=0.95))
    else:
        raise ValueError(kind)


def add_arrow(drawing: Drawing, x0: float, y0: float, x1: float, y1: float, *, color=INK, dash=None) -> None:
    line = Line(x0, y0, x1, y1, strokeColor=color, strokeWidth=0.85)
    if dash:
        line.strokeDashArray = dash
    drawing.add(line)
    angle = math.atan2(y1 - y0, x1 - x0)
    length = 3.4
    spread = 0.48
    drawing.add(Polygon([
        x1,
        y1,
        x1 - length * math.cos(angle - spread),
        y1 - length * math.sin(angle - spread),
        x1 - length * math.cos(angle + spread),
        y1 - length * math.sin(angle + spread),
    ], strokeColor=color, fillColor=color, strokeWidth=0.4))


def add_blossom(drawing: Drawing, x: float, y: float) -> None:
    for angle in (90, 18, -54, -126, 162):
        radians = math.radians(angle)
        drawing.add(Circle(
            x + 3.2 * math.cos(radians), y + 3.2 * math.sin(radians), 1.9,
            strokeColor=BLUE, fillColor=None, strokeWidth=0.45,
        ))
    drawing.add(Circle(x, y, 1.05, strokeColor=BLUE, fillColor=GOLD, strokeWidth=0.35))


def build_drawing(values: dict[str, Fraction]) -> Drawing:
    LAYOUT.clear()
    drawing = Drawing(W, H)
    drawing.add(Rect(0, 0, W, H, strokeColor=None, fillColor=white))

    add_text(drawing, 14, H - 16, "R0.74H collar-flux repair", size=10.2, bold=True, layout_id="title")
    add_text(
        drawing, 14, H - 28,
        "25/25 exact compatibility gates + analytic lower-scale diagram; no unknown constants plotted.",
        size=6.05, color=MID, layout_id="subtitle",
    )
    add_blossom(drawing, W - 17, H - 17)
    drawing.add(Line(14, H - 35, W - 14, H - 35, strokeColor=LIGHT, strokeWidth=0.7))
    drawing.add(Line(W / 2 + 2, 25, W / 2 + 2, H - 42, strokeColor=LIGHT, strokeWidth=0.7))

    panel_a = (14, 25, W / 2 - 5, H - 39)
    panel_b = (W / 2 + 8, 25, W - 14, H - 39)

    # Panel A: exact identity-level ledger and two regimes.
    ax = 16
    add_text(drawing, ax, H - 51, "A", size=8.2, bold=True, container=panel_a, layout_id="panel-a")
    add_text(drawing, ax + 15, H - 51, "Energy ledger and two-regime closure", size=6.75, bold=True, container=panel_a, layout_id="panel-a-title")
    add_box(drawing, W / 2 - 76, H - 63, 59, 12, stroke=BLUE, fill=BLUE_LIGHT)
    add_text(drawing, W / 2 - 46.5, H - 59.3, "25/25 EXACT", size=5.15, color=BLUE, bold=True, anchor="middle", container=panel_a, layout_id="exact-badge")

    left_x, right_x = 22, 132
    box_y, box_w, box_h = H - 92, 94, 24
    add_box(drawing, left_x, box_y, box_w, box_h, stroke=BLUE, fill=BLUE_LIGHT)
    add_text(drawing, left_x + 7, box_y + 14, "quadratic cutoff", size=4.9, color=BLUE, bold=True, container=panel_a, layout_id="cutoff-label")
    add_text(drawing, left_x + 7, box_y + 5.8, "Q_R <= C P_0^(2/3)", size=4.75, color=INK, container=panel_a, layout_id="cutoff-formula")

    add_box(drawing, right_x, box_y, box_w, box_h, stroke=GOLD, fill=GOLD_LIGHT, dash=[4, 2])
    add_text(drawing, right_x + 7, box_y + 14, "positive collar flux", size=4.9, color=GOLD, bold=True, container=panel_a, layout_id="flux-label")
    add_text(drawing, right_x + 7, box_y + 5.8, "C_R = sup [F_R(t)]_+", size=4.75, color=INK, container=panel_a, layout_id="flux-formula")

    merge_y = H - 115
    add_arrow(drawing, left_x + box_w / 2, box_y, 101, merge_y + 15, color=BLUE)
    add_arrow(drawing, right_x + box_w / 2, box_y, 147, merge_y + 15, color=GOLD, dash=[4, 2])
    add_box(drawing, 52, merge_y, 146, 25, stroke=INK, fill=XLIGHT)
    add_text(drawing, 125, merge_y + 14.5, "signed-flux closure", size=4.55, color=MID, bold=True, anchor="middle", container=panel_a, layout_id="signed-label")
    add_text(drawing, 125, merge_y + 6.0, "X_R^alpha <= C [ P_R^(2/3) + C_R^alpha ]", size=5.05, color=INK, bold=True, anchor="middle", container=panel_a, layout_id="signed-formula")

    repaired_y = H - 145
    add_arrow(drawing, 125, merge_y, 125, repaired_y + 21, color=INK)
    add_box(drawing, 42, repaired_y, 166, 22, stroke=GOLD, fill=GOLD_LIGHT)
    add_text(drawing, 125, repaired_y + 12.4, "P_hat = P + C_R^(3/2)", size=4.8, color=GOLD, bold=True, anchor="middle", container=panel_a, layout_id="repair-payment")
    add_text(drawing, 125, repaired_y + 4.6, "X_R^alpha <= C P_hat^(2/3)", size=5.0, color=INK, bold=True, anchor="middle", container=panel_a, layout_id="repair-result")

    regime_y = H - 179
    add_box(drawing, 20, regime_y, 105, 25, stroke=BLUE, fill=white)
    add_text(drawing, 27, regime_y + 15, "SMALL  0 <= P <= 1", size=4.55, color=BLUE, bold=True, container=panel_a, layout_id="small-head")
    add_text(drawing, 27, regime_y + 6, "P <= P^(2/3)  ->  X <= C P^(2/3)", size=4.3, color=INK, container=panel_a, layout_id="small-body")
    add_box(drawing, 132, regime_y, 105, 25, stroke=GOLD, fill=white, dash=[4, 2])
    add_text(drawing, 139, regime_y + 15, "LARGE  P >= 1", size=4.55, color=GOLD, bold=True, container=panel_a, layout_id="large-head")
    add_text(drawing, 139, regime_y + 6, "X <= C [ P^(2/3) + P ]", size=4.3, color=INK, container=panel_a, layout_id="large-body")

    add_text(drawing, 22, 30, "Version F:  (J_acc^(3/2))^(2/3) = J_acc; no second enlargement.", size=4.15, color=MID, container=panel_a, layout_id="acc-note")

    # Panel B: exact L-exponent comparison, normalized by B^2 R^2.
    bx0 = W / 2 + 10
    add_text(drawing, bx0, H - 51, "B", size=8.2, bold=True, container=panel_b, layout_id="panel-b")
    add_text(drawing, bx0 + 15, H - 51, "Explicit-family L-exponent comparison", size=6.75, bold=True, container=panel_b, layout_id="panel-b-title")
    add_box(drawing, W - 119, H - 63, 102, 12, stroke=GOLD, fill=GOLD_LIGHT)
    add_text(drawing, W - 68, H - 59.3, "EXACT EXPONENT DIAGRAM", size=4.9, color=GOLD, bold=True, anchor="middle", container=panel_b, layout_id="diagram-badge")
    add_text(drawing, bx0 + 3, H - 75, "Rows divided by B^2 R^2; coefficients suppressed; lower-bound directions retained.", size=4.35, color=MID, container=panel_b, layout_id="panel-b-subtitle")

    axis_x0, axis_x1 = bx0 + 89, W - 65
    axis_y = H - 104
    drawing.add(Line(axis_x0, axis_y, axis_x1, axis_y, strokeColor=INK, strokeWidth=0.85))
    for exponent in (0, Fraction(1, 2), 1):
        xpos = axis_x0 + float(exponent) * (axis_x1 - axis_x0) / 1.15
        drawing.add(Line(xpos, axis_y - 2.5, xpos, axis_y + 2.5, strokeColor=INK, strokeWidth=0.65))
        label = q(exponent) if isinstance(exponent, Fraction) and exponent.denominator != 1 else str(int(exponent))
        add_text(drawing, xpos, axis_y + 6, label, size=4.2, color=MID, bold=True, anchor="middle", container=panel_b, layout_id=f"tick-{label}")
    add_text(drawing, W - 20, axis_y + 14, "power of L", size=4.2, color=MID, bold=True, anchor="end", container=panel_b, layout_id="axis-title")

    rows = [
        ("old payment  P^(2/3)", 0.0, "circle", INK, white, [4, 2], "L^0", "FINITE EXPONENT"),
        ("endpoint  X", 1.0, "square", BLUE, BLUE, None, "L^1", "ANALYTIC LOWER"),
        ("positive flux  C_R", 1.0, "diamond", GOLD, GOLD, [5, 2], "L^1", "ANALYTIC LOWER"),
    ]
    row_ys = [H - 126, H - 149, H - 172]
    for index, (name, exponent, marker, color, fill, dash, power, status) in enumerate(rows):
        y = row_ys[index]
        add_text(drawing, bx0 + 4, y - 1.7, name, size=4.75, color=color, bold=True, container=panel_b, layout_id=f"series-{index}")
        xpos = axis_x0 + exponent * (axis_x1 - axis_x0) / 1.15
        connector = Line(axis_x0, y, xpos, y, strokeColor=color, strokeWidth=1.0)
        if dash:
            connector.strokeDashArray = dash
        drawing.add(connector)
        add_marker(drawing, xpos, y, marker, color=color, fill=fill, size=2.8)
        add_text(drawing, xpos + 7, y - 1.7, power, size=4.9, color=color, bold=True, container=panel_b, layout_id=f"power-{index}")
        add_text(drawing, W - 18, y - 1.7, status, size=3.55, color=MID, bold=True, anchor="end", container=panel_b, layout_id=f"status-{index}")

    # Exact missing/repair annotations use shape and stroke, not color alone.
    y_bracket = H - 138
    x_zero = axis_x0
    x_one = axis_x0 + (axis_x1 - axis_x0) / 1.15
    drawing.add(Line(x_zero, y_bracket, x_one, y_bracket, strokeColor=INK, strokeWidth=0.75))
    drawing.add(Line(x_zero, y_bracket - 2, x_zero, y_bracket + 2, strokeColor=INK, strokeWidth=0.75))
    drawing.add(Line(x_one, y_bracket - 2, x_one, y_bracket + 2, strokeColor=INK, strokeWidth=0.75))
    add_text(drawing, (x_zero + x_one) / 2, y_bracket + 4, "missing exponent  +1", size=4.0, color=INK, bold=True, anchor="middle", container=panel_b, layout_id="missing-bracket")

    card_y = 28
    add_box(drawing, bx0 + 6, card_y, W / 2 - 32, 22, stroke=GOLD, fill=GOLD_LIGHT, dash=[4, 2])
    add_text(drawing, bx0 + 13, card_y + 12.6, "cubicized repair inside P_hat", size=4.35, color=GOLD, bold=True, container=panel_b, layout_id="cubic-head")
    add_text(drawing, bx0 + 13, card_y + 4.8, "C_R^(3/2): L^(3/2)  --outer 2/3-->  L^1", size=4.6, color=INK, bold=True, container=panel_b, layout_id="cubic-body")

    drawing.add(Rect(14, 5, W - 28, 15, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.75))
    add_text(drawing, 21, 10, "TWO-REGIME SIZE CLOSURE", size=5.35, color=GOLD, bold=True, layout_id="footer-result")
    add_text(drawing, W / 2, 10, "EXACT EXPONENT DIAGRAM · NOT DNS · NOT SIMULATION", size=4.85, color=INK, bold=True, anchor="middle", layout_id="footer-boundary")
    add_text(drawing, W - 21, 10, "NOT CLAY", size=5.7, color=INK, bold=True, anchor="end", layout_id="footer-clay")
    return drawing


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
            "method": "ReportLab stringWidth plus ascent/descent proxy",
            "entries": LAYOUT,
            "summary": {
                "passed": sum(bool(item["proxyPass"]) for item in LAYOUT),
                "total": len(LAYOUT),
            },
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (HERE / "environment.json").write_text(
        json.dumps({
            "certificateChecks": "25/25",
            "certificatePath": str(CERTIFICATE.relative_to(REPO)),
            "certificateSha256": sha256(CERTIFICATE),
            "certificateStdoutByteIdentical": True,
            "figureId": FIGURE_ID,
            "fontBold": {"path": str(FONT_BOLD), "sha256": sha256(FONT_BOLD)},
            "fontRegular": {"path": str(FONT_REGULAR), "sha256": sha256(FONT_REGULAR)},
            "platform": platform.platform(),
            "producerPath": str(PRODUCER.relative_to(REPO)),
            "producerSha256": sha256(PRODUCER),
            "python": sys.version.split()[0],
            "reportlab": __import__("reportlab").Version,
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (HERE / "results.json").write_text(
        json.dumps({
            "certificate": certificate["summary"],
            "figureId": FIGURE_ID,
            "layout": {
                "passed": sum(bool(item["proxyPass"]) for item in LAYOUT),
                "total": len(LAYOUT),
            },
            "panelA": "exact energy-ledger and two-regime implication diagram",
            "panelB": "B^2 R^2-normalized exact L-exponent diagram",
            "status": "GENERATED",
        }, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(
        f"generated {FIGURE_ID}: {len(LAYOUT)} text bounds; "
        f"certificate {certificate['summary']['passed']}/{certificate['summary']['total']} PASS"
    )


if __name__ == "__main__":
    main()
