#!/usr/bin/env python3
"""Generate the deterministic R0.74G complete-payment journal figure.

The frozen finite-certificate script and its byte-identical 31/31 JSON are the
only quantitative inputs.  Panel B evaluates stated analytic formulas; it is
not DNS, simulation, sampled-path output, or empirical data.
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
CERTIFICATE = REPO / "research/r074g_complete_payment_certificate.json"
SCRIPT = REPO / "scripts/r074g_complete_payment_certificate.py"
EXPECTED_CERT_SHA256 = "2a411007989e63e51ab7f1644724f654f26794b80507681aaf62e00adbeefd53"
EXPECTED_SCRIPT_SHA256 = "315f4cc7f0a397287cc2eb14ec1ad65bcacb797692e2a6ce5a1459985a4853ca"
FIGURE_ID = "fig-r074g-complete-payment-ledger"

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
pdfmetrics.registerFont(TTFont("R074G-Regular", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("R074G-Bold", str(FONT_BOLD)))


def frac(value: str) -> Fraction:
    return Fraction(value)


def check_value(checks: dict[str, dict], check_id: str, field: str = "left") -> Fraction:
    try:
        return frac(checks[check_id][field])
    except (KeyError, ValueError) as exc:
        raise RuntimeError(f"missing exact certificate field: {check_id}.{field}") from exc


def load_exact() -> tuple[dict, dict[str, Fraction]]:
    if sha256(CERTIFICATE) != EXPECTED_CERT_SHA256:
        raise RuntimeError("certificate hash mismatch; figure contract refuses source drift")
    if sha256(SCRIPT) != EXPECTED_SCRIPT_SHA256:
        raise RuntimeError("certificate-script hash mismatch; figure contract refuses source drift")
    regenerated = subprocess.run(
        [sys.executable, str(SCRIPT)], check=True, capture_output=True
    ).stdout
    if regenerated != CERTIFICATE.read_bytes():
        raise RuntimeError("certificate script stdout is not byte-identical to the frozen JSON")

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if certificate.get("result") != "PASS" or certificate.get("summary") != {"passed": 31, "total": 31}:
        raise RuntimeError("certificate is not the frozen 31/31 PASS object")
    if len(certificate.get("checks", [])) != 31 or not all(item.get("pass") is True for item in certificate["checks"]):
        raise RuntimeError("certificate Boolean checks are incomplete")

    checks = {item["id"]: item for item in certificate["checks"]}
    c_gamma = check_value(checks, "gamma_coefficient")
    values = {
        "c_gamma": c_gamma,
        "three_half_gamma": Fraction(3, 2) * c_gamma,
        "c_R": check_value(checks, "inverse_R_beats_three_halves_gamma"),
        "d_E": check_value(checks, "buffered_energy_exponent"),
        "a_plateau": check_value(checks, "plateau_exponent"),
        "gap_complete": check_value(checks, "complete_payment_gap"),
        "gap_energy": check_value(checks, "buffered_energy_gap"),
        "gap_shift": check_value(checks, "plateau_shift_gap"),
        "L12": check_value(checks, "discrete_L12"),
        "L13": check_value(checks, "discrete_L13"),
        "buffer_threshold": check_value(checks, "buffer_width_threshold"),
    }
    if not values["c_gamma"] < values["three_half_gamma"] < values["c_R"] < values["d_E"] < values["a_plateau"]:
        raise RuntimeError("five-coefficient order drift")
    if values["c_R"] - values["three_half_gamma"] != values["gap_complete"]:
        raise RuntimeError("complete-payment gap drift")
    if values["d_E"] - values["c_gamma"] != values["gap_energy"]:
        raise RuntimeError("energy gap drift")
    if values["a_plateau"] - values["c_R"] != values["gap_shift"]:
        raise RuntimeError("plateau-shift gap drift")
    return certificate, values


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def analytic_log10(series: str, gap: Fraction, length: Fraction) -> float:
    ell = float(length)
    if series == "background_floor":
        return 0.0
    if series == "packet_G_envelope":
        return -float(gap) * ell * ell / math.log(10.0) - 2.0 * math.log10(ell)
    if series == "packet_H_envelope":
        return -float(gap) * ell * ell / math.log(10.0) - 3.5 * math.log10(ell)
    if series == "target_ratio_lower":
        return math.log10(ell)
    raise ValueError(series)


def formula_for(series: str, length: Fraction) -> str:
    ell = q(length)
    if series == "background_floor":
        return "1"
    if series == "packet_G_envelope":
        return f"exp[-(43/423360)*({ell})^2]*({ell})^-2"
    if series == "packet_H_envelope":
        return f"exp[-(43/423360)*({ell})^2]*({ell})^-7/2"
    if series == "target_ratio_lower":
        return ell
    raise ValueError(series)


def write_source_data(values: dict[str, Fraction]) -> None:
    rows: list[list[str]] = []
    panel_a = [
        ("c_gamma", values["c_gamma"], "coefficient", "annular-weight exponent"),
        ("three_half_gamma", values["three_half_gamma"], "coefficient", "three halves of c_gamma"),
        ("c_R", values["c_R"], "coefficient", "inverse-radius exponent"),
        ("d_E", values["d_E"], "coefficient", "buffered transverse-energy exponent"),
        ("a_plateau", values["a_plateau"], "coefficient", "plateau heat-leakage exponent"),
        ("gap_complete", values["gap_complete"], "strict gap", "c_R minus three halves c_gamma"),
        ("gap_energy", values["gap_energy"], "strict gap", "d_E minus c_gamma"),
        ("gap_shift", values["gap_shift"], "strict gap", "a_plateau minus c_R"),
    ]
    for record, value, role, note in panel_a:
        rows.append([
            "A", record, "", "", q(value), q(value), f"{float(value):.17g}",
            "identity", role, "EXACT FINITE", note,
        ])

    roles = {
        "background_floor": ("normalized floor", "ANALYTIC FLOOR", "unit shear/background payment floor"),
        "packet_G_envelope": ("normalized upper envelope", "ANALYTIC ENVELOPE", "packet cubic row relative to the floor"),
        "packet_H_envelope": ("normalized upper envelope", "ANALYTIC ENVELOPE", "packet harmonic row relative to the floor"),
        "target_ratio_lower": ("normalized lower bound", "ANALYTIC LOWER BOUND", "rejected-ratio lower bound"),
    }
    for index, length in ((12, values["L12"]), (13, values["L13"])):
        for series in ("background_floor", "packet_G_envelope", "packet_H_envelope", "target_ratio_lower"):
            role, status, note = roles[series]
            rows.append([
                "B", series, str(index), q(length), "", formula_for(series, length),
                f"{analytic_log10(series, values['gap_complete'], length):.17g}",
                "log10(analytic factor)", role, status, note,
            ])

    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow([
            "panel", "record", "index_j", "L_exact", "exact_value", "analytic_formula",
            "plotted_value", "plotted_unit", "role", "status", "note",
        ])
        writer.writerows(rows)


LAYOUT: list[dict] = []


def add_text(
    drawing: Drawing,
    x: float,
    y: float,
    text: str,
    *,
    size: float = 6.0,
    color=INK,
    bold: bool = False,
    anchor: str = "start",
    container: tuple[float, float, float, float] | None = None,
    layout_id: str = "text",
) -> None:
    font = "R074G-Bold" if bold else "R074G-Regular"
    width = pdfmetrics.stringWidth(text, font, size)
    left = x if anchor == "start" else x - width / 2 if anchor == "middle" else x - width
    bounds = [left, y - 0.23 * size, left + width, y + 0.86 * size]
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
        "boundsPt": [round(value, 4) for value in bounds],
        "containerPt": [round(value, 4) for value in region],
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
    line_width: float = 0.7,
) -> None:
    box = Rect(x, y, width, height, rx=3, ry=3, strokeColor=stroke, fillColor=fill, strokeWidth=line_width)
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)


def add_badge(
    drawing: Drawing,
    x: float,
    y: float,
    text: str,
    *,
    stroke=BLUE,
    fill=white,
    text_color=BLUE,
    width: float | None = None,
    dash=None,
    container=None,
    layout_id: str = "badge",
) -> None:
    size = 5.25
    box_width = width or pdfmetrics.stringWidth(text, "R074G-Bold", size) + 10
    box = Rect(x, y, box_width, 12, rx=4, ry=4, strokeColor=stroke, fillColor=fill, strokeWidth=0.7)
    if dash:
        box.strokeDashArray = dash
    drawing.add(box)
    add_text(
        drawing, x + box_width / 2, y + 3.55, text, size=size, color=text_color,
        bold=True, anchor="middle", container=container, layout_id=layout_id,
    )


def add_blossom(drawing: Drawing, x: float, y: float) -> None:
    for angle in (90, 18, -54, -126, 162):
        radians = math.radians(angle)
        drawing.add(Circle(
            x + 3.3 * math.cos(radians), y + 3.3 * math.sin(radians), 2.0,
            strokeColor=BLUE, fillColor=None, strokeWidth=0.45,
        ))
    drawing.add(Circle(x, y, 1.1, strokeColor=BLUE, fillColor=GOLD, strokeWidth=0.35))


def add_marker(
    drawing: Drawing,
    x: float,
    y: float,
    kind: str,
    *,
    color=BLUE,
    fill=white,
    size: float = 3.0,
) -> None:
    if kind == "circle":
        drawing.add(Circle(x, y, size, strokeColor=color, fillColor=fill, strokeWidth=0.95))
    elif kind == "diamond":
        drawing.add(Polygon(
            [x, y + size, x + size, y, x, y - size, x - size, y],
            strokeColor=color, fillColor=fill, strokeWidth=0.95,
        ))
    elif kind == "square":
        drawing.add(Rect(
            x - size, y - size, 2 * size, 2 * size,
            strokeColor=color, fillColor=fill, strokeWidth=0.95,
        ))
    elif kind == "triangle":
        drawing.add(Polygon(
            [x, y + size, x + size, y - size, x - size, y - size],
            strokeColor=color, fillColor=fill, strokeWidth=0.95,
        ))
    else:
        raise ValueError(kind)


def add_gap_card(
    drawing: Drawing,
    x: float,
    y: float,
    width: float,
    label: str,
    *,
    stroke,
    fill,
    container,
    layout_id: str,
) -> None:
    add_box(drawing, x, y, width, 17, stroke=stroke, fill=fill)
    add_text(
        drawing, x + width / 2, y + 5.7, label, size=4.65, color=INK,
        bold=True, anchor="middle", container=container, layout_id=layout_id,
    )


def build_drawing(values: dict[str, Fraction]) -> Drawing:
    LAYOUT.clear()
    drawing = Drawing(W, H)
    drawing.add(Rect(0, 0, W, H, strokeColor=None, fillColor=white))

    add_text(drawing, 14, H - 16, "R0.74G complete-payment ledger", size=10.2, bold=True, layout_id="title")
    add_text(
        drawing, 14, H - 28,
        "31/31 exact gates + normalized analytic envelopes; formula evaluation, not flow simulation.",
        size=6.15, color=MID, layout_id="subtitle",
    )
    add_blossom(drawing, W - 17, H - 17)
    drawing.add(Line(14, H - 35, W - 14, H - 35, strokeColor=LIGHT, strokeWidth=0.7))
    drawing.add(Line(W / 2, 25, W / 2, H - 42, strokeColor=LIGHT, strokeWidth=0.7))

    panel_a = (14, 25, W / 2 - 6, H - 39)
    panel_b = (W / 2 + 6, 25, W - 14, H - 39)

    # Panel A: proportional full ladder, enlarged close range, exact gap cards.
    add_text(drawing, 16, H - 51, "A", size=8.2, bold=True, container=panel_a, layout_id="panel-a")
    add_text(
        drawing, 31, H - 51, "Exact payment exponent ladder", size=7.15, bold=True,
        container=panel_a, layout_id="panel-a-title",
    )
    add_badge(
        drawing, W / 2 - 83, H - 62, "31/31 EXACT", stroke=BLUE, fill=BLUE_LIGHT,
        width=67, container=panel_a, layout_id="badge-exact",
    )

    add_text(drawing, 22, H - 74, "Full scale", size=5.7, bold=True, color=MID, container=panel_a, layout_id="full-title")
    x0, x1, y = 31, W / 2 - 19, H - 91
    full_min, full_max = 0.0019, 0.00337
    full_x = lambda value: x0 + (float(value) - full_min) / (full_max - full_min) * (x1 - x0)
    drawing.add(Line(x0, y, x1, y, strokeColor=INK, strokeWidth=0.8))
    marks = [
        ("c_gamma", "circle", BLUE, white),
        ("three_half_gamma", "diamond", INK, white),
        ("c_R", "square", BLUE, BLUE_LIGHT),
        ("d_E", "triangle", GOLD, GOLD_LIGHT),
        ("a_plateau", "circle", GOLD, GOLD),
    ]
    for key, kind, color, fill in marks:
        add_marker(drawing, full_x(values[key]), y, kind, color=color, fill=fill, size=2.65)
    add_text(
        drawing, full_x(values["c_gamma"]), y + 10, "c_gamma  8/3969", size=4.85,
        color=BLUE, bold=True, anchor="middle", container=panel_a, layout_id="full-gamma",
    )
    add_text(
        drawing, full_x(values["three_half_gamma"]), y - 14, "3c_gamma/2", size=4.7,
        color=INK, bold=True, anchor="end", container=panel_a, layout_id="full-three-half",
    )
    add_text(
        drawing, full_x(values["c_R"]) + 3, y + 10, "c_R", size=4.7,
        color=BLUE, bold=True, anchor="start", container=panel_a, layout_id="full-c-r",
    )
    add_text(
        drawing, x1, y - 14, "d_E < a_plateau", size=4.7, color=GOLD,
        bold=True, anchor="end", container=panel_a, layout_id="full-cluster",
    )

    add_text(
        drawing, 22, H - 122, "Enlarged close range", size=5.7, bold=True,
        color=MID, container=panel_a, layout_id="zoom-title",
    )
    zx0, zx1, zy = 31, W / 2 - 19, H - 139
    zoom_min, zoom_max = 0.00298, 0.00336
    zoom_x = lambda value: zx0 + (float(value) - zoom_min) / (zoom_max - zoom_min) * (zx1 - zx0)
    drawing.add(Line(zx0, zy, zx1, zy, strokeColor=INK, strokeWidth=0.8))
    close_marks = [
        ("three_half_gamma", "3c_gamma/2 = 4/1323", "diamond", INK, white, 10, "middle"),
        ("c_R", "c_R = 1/320", "square", BLUE, BLUE_LIGHT, -14, "middle"),
        ("d_E", "d_E = 98/29475", "triangle", GOLD, GOLD_LIGHT, 10, "end"),
        ("a_plateau", "a_plateau = 49/14625", "circle", GOLD, GOLD, -14, "end"),
    ]
    for key, label, kind, color, fill, offset, anchor in close_marks:
        xpos = zoom_x(values[key])
        add_marker(drawing, xpos, zy, kind, color=color, fill=fill, size=2.75)
        tx = xpos if anchor != "end" else zx1
        add_text(
            drawing, tx, zy + offset, label, size=4.45, color=color, bold=True,
            anchor=anchor, container=panel_a, layout_id=f"zoom-{key}",
        )

    add_gap_card(
        drawing, 20, 61, 105, "c_R-3c_gamma/2 = 43/423360", stroke=BLUE,
        fill=BLUE_LIGHT, container=panel_a, layout_id="gap-complete",
    )
    add_gap_card(
        drawing, 132, 61, 105, "d_E-c_gamma = 17018/12998475", stroke=GOLD,
        fill=GOLD_LIGHT, container=panel_a, layout_id="gap-energy",
    )
    add_gap_card(
        drawing, 70, 39, 120, "a_plateau-c_R = 211/936000", stroke=INK,
        fill=XLIGHT, container=panel_a, layout_id="gap-shift",
    )

    # Panel B: direct formula ledger.  Printed values are log10 evaluations.
    bx0 = W / 2 + 6
    add_text(drawing, bx0 + 2, H - 51, "B", size=8.2, bold=True, container=panel_b, layout_id="panel-b")
    add_text(
        drawing, bx0 + 17, H - 51, "Normalized analytic ledger", size=7.15,
        bold=True, container=panel_b, layout_id="panel-b-title",
    )
    add_badge(
        drawing, W - 119, H - 62, "ANALYTIC DERIVATION", stroke=GOLD,
        fill=GOLD_LIGHT, text_color=GOLD, width=102, container=panel_b,
        layout_id="badge-analytic",
    )
    add_text(
        drawing, bx0 + 9, H - 75,
        "g=43/423360 > 0; L_12=8064; L_13=16128; cells report log10(factor)",
        size=4.55, color=MID, container=panel_b, layout_id="ledger-subtitle",
    )

    col_series = bx0 + 12
    col_formula = bx0 + 66
    col_j12 = bx0 + 160
    col_j13 = bx0 + 199
    col_limit = W - 25
    header_y = H - 88
    add_text(drawing, col_series, header_y, "quantity", size=4.4, color=MID, bold=True, container=panel_b, layout_id="head-series")
    add_text(drawing, col_formula, header_y, "exact analytic formula", size=4.4, color=MID, bold=True, container=panel_b, layout_id="head-formula")
    add_text(drawing, col_j12, header_y, "j=12", size=4.4, color=MID, bold=True, anchor="middle", container=panel_b, layout_id="head-j12")
    add_text(drawing, col_j13, header_y, "j=13", size=4.4, color=MID, bold=True, anchor="middle", container=panel_b, layout_id="head-j13")
    add_text(drawing, col_limit, header_y, "limit", size=4.4, color=MID, bold=True, anchor="middle", container=panel_b, layout_id="head-limit")

    ledger = [
        ("background floor", "1", "0.000", "0.000", "-> 1", "circle", INK, white, XLIGHT, None),
        ("packet G", "exp(-g L^2) L^-2", "-2876.24", "-11482.13", "-> 0", "circle", BLUE, BLUE, BLUE_LIGHT, None),
        ("packet H", "exp(-g L^2) L^-7/2", "-2882.10", "-11488.44", "-> 0", "square", GOLD, white, GOLD_LIGHT, [3, 2]),
        ("ratio lower", "L", "+3.9066", "+4.2076", "-> +inf", "diamond", GOLD, GOLD, white, None),
    ]
    centers = [H - 105, H - 131, H - 157, H - 183]
    for row_index, (name, formula, j12, j13, limit, marker, color, fill, row_fill, dash) in enumerate(ledger):
        cy = centers[row_index]
        add_box(
            drawing, bx0 + 8, cy - 10.5, W / 2 - 28, 21,
            stroke=color if row_index else LIGHT, fill=row_fill, dash=dash,
        )
        add_text(
            drawing, col_series, cy - 1.8, name, size=4.75, color=color,
            bold=True, container=panel_b, layout_id=f"ledger-name-{row_index}",
        )
        marker_x = col_formula + 9 if row_index == 0 else col_formula - 8
        formula_x = col_formula + 17 if row_index == 0 else col_formula
        add_marker(drawing, marker_x, cy, marker, color=color, fill=fill, size=2.35)
        add_text(
            drawing, formula_x, cy - 1.8, formula, size=4.4, color=INK,
            container=panel_b, layout_id=f"ledger-formula-{row_index}",
        )
        add_text(
            drawing, col_j12, cy - 1.8, j12, size=4.45, color=color,
            bold=True, anchor="middle", container=panel_b, layout_id=f"ledger-j12-{row_index}",
        )
        add_text(
            drawing, col_j13, cy - 1.8, j13, size=4.45, color=color,
            bold=True, anchor="middle", container=panel_b, layout_id=f"ledger-j13-{row_index}",
        )
        add_text(
            drawing, col_limit, cy - 1.8, limit, size=4.4, color=color,
            bold=True, anchor="middle", container=panel_b, layout_id=f"ledger-limit-{row_index}",
        )

    add_text(
        drawing, bx0 + 9, 32,
        "Exact formulas, deterministic evaluation; envelope/lower-bound directions are not DNS.",
        size=4.4, color=MID, container=panel_b, layout_id="ledger-note",
    )

    # Global theorem-status and scope boundary.
    drawing.add(Rect(14, 5, W - 28, 15, strokeColor=GOLD, fillColor=GOLD_LIGHT, strokeWidth=0.75))
    add_text(
        drawing, 21, 10, "PROPOSED INEQUALITY REJECTED", size=5.4, color=GOLD,
        bold=True, layout_id="rejected-boundary",
    )
    add_text(
        drawing, W / 2, 10, "ANALYTIC DERIVATION · NOT DNS", size=5.15,
        color=INK, bold=True, anchor="middle", layout_id="analytic-boundary",
    )
    add_text(
        drawing, W - 21, 10, "NOT CLAY", size=5.75, color=INK,
        bold=True, anchor="end", layout_id="not-clay",
    )
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
            "certificateChecks": "31/31",
            "certificatePath": str(CERTIFICATE.relative_to(REPO)),
            "certificateSha256": sha256(CERTIFICATE),
            "certificateStdoutByteIdentical": True,
            "figureId": FIGURE_ID,
            "fontBold": {"path": str(FONT_BOLD), "sha256": sha256(FONT_BOLD)},
            "fontRegular": {"path": str(FONT_REGULAR), "sha256": sha256(FONT_REGULAR)},
            "platform": platform.platform(),
            "python": sys.version.split()[0],
            "reportlab": __import__("reportlab").Version,
            "scriptPath": str(SCRIPT.relative_to(REPO)),
            "scriptSha256": sha256(SCRIPT),
        }, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"generated {FIGURE_ID}: {len(LAYOUT)} text bounds; "
        f"certificate {certificate['summary']['passed']}/{certificate['summary']['total']} PASS"
    )


if __name__ == "__main__":
    main()
