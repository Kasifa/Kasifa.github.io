#!/usr/bin/env python3
"""Render the R0.74S Step 13 analytic threshold schematic."""

from __future__ import annotations

import base64
import csv
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

import PIL
import pypdf
from PIL import Image
from reportlab import Version as REPORTLAB_VERSION, rl_config
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Circle, Drawing, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
INK = HexColor("#202A34")
MID = HexColor("#66717B")
GRID = HexColor("#D4DADF")
PALE = HexColor("#F6F7F5")
BLUE = HexColor("#2E607E")
BLUE_LIGHT = HexColor("#E7F0F4")
GOLD = HexColor("#936617")
GOLD_LIGHT = HexColor("#F6EDD8")
PLUM = HexColor("#6C526C")
PLUM_LIGHT = HexColor("#F1E9F1")
RED = HexColor("#8A3E34")
RED_LIGHT = HexColor("#F7E9E6")
rl_config.invariant = 1


def dependency_root() -> Path | None:
    override = os.environ.get("R074S_DEPENDENCIES_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    for parent in Path(sys.executable).resolve().parents:
        if (parent / "bin/override/pdftoppm").is_file():
            return parent
    return None


BUNDLE = dependency_root()
bundled = BUNDLE / "bin/override/pdftoppm" if BUNDLE else None
fallback = shutil.which("pdftoppm")
PDFTOPPM = bundled if bundled and bundled.is_file() else (Path(fallback).resolve() if fallback else None)
if PDFTOPPM is None:
    raise FileNotFoundError("pdftoppm")


def font_path(name: str) -> Path:
    candidates: list[Path] = []
    if BUNDLE:
        candidates.append(BUNDLE / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype" / name)
    candidates += [
        Path("/System/Library/Fonts/Supplemental") / name,
        Path("/Library/Fonts") / name,
        Path("/usr/share/fonts/truetype/dejavu") / name,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(name)


REGULAR = font_path("DejaVuSans.ttf")
BOLD = font_path("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074S13-Regular", str(REGULAR)))
pdfmetrics.registerFont(TTFont("R074S13-Bold", str(BOLD)))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label(d: Drawing, x: float, y: float, value: str, size: float = 5.0, *, color=INK, bold=False, anchor="start") -> None:
    d.add(String(x, y, value, fontName="R074S13-Bold" if bold else "R074S13-Regular", fontSize=size, fillColor=color, textAnchor=anchor))


def multiline(d: Drawing, x: float, y: float, lines: list[str], size: float = 5.0, *, color=INK, bold_first=False, leading=7.0, anchor="start") -> None:
    for index, line in enumerate(lines):
        label(d, x, y - index * leading, line, size, color=color, bold=bold_first and index == 0, anchor=anchor)


def panel(d: Drawing, x: float, y: float, w: float, h: float, tag: str, title: str) -> None:
    d.add(Rect(x, y, w, h, rx=4, ry=4, fillColor=white, strokeColor=GRID, strokeWidth=0.8))
    label(d, x + 8, y + h - 14, tag, 6.6, color=BLUE, bold=True)
    label(d, x + 25, y + h - 14, title, 6.0, bold=True)


def box(d: Drawing, x: float, y: float, w: float, h: float, lines: list[str], *, fill, stroke, status: str) -> None:
    d.add(Rect(x, y, w, h, rx=3, ry=3, fillColor=fill, strokeColor=stroke, strokeWidth=0.8))
    multiline(d, x + 7, y + h - 11, lines, 4.8, color=stroke, bold_first=True, leading=6.4)
    label(d, x + w - 5, y + 5, status, 4.25, color=stroke, bold=True, anchor="end")


def arrow(d: Drawing, x1: float, y1: float, x2: float, y2: float, *, color=MID) -> None:
    d.add(Line(x1, y1, x2 - 6, y2, strokeColor=color, strokeWidth=1.0))
    d.add(Polygon([x2 - 6, y2 + 3, x2, y2, x2 - 6, y2 - 3], fillColor=color, strokeColor=color))


def temporal_exponent(inverse_p: Fraction) -> Fraction:
    return Fraction(2) * (Fraction(2) - inverse_p) / (Fraction(5) - 3 * inverse_p)


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for numerator in range(0, 21):
        inverse_p = Fraction(numerator, 20)
        exponent = temporal_exponent(inverse_p)
        rows.append({
            "panel": "A",
            "parameter": "inverse_p",
            "x_exact": f"{inverse_p.numerator}/{inverse_p.denominator}",
            "value_exact": f"{exponent.numerator}/{exponent.denominator}",
            "status": "METHOD_CEILING",
        })
    for theta in (Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(3, 4), Fraction(1)):
        gap = min(Fraction(1), theta) - Fraction(2, 3)
        rows.append({
            "panel": "B",
            "parameter": "morrey_theta",
            "x_exact": f"{theta.numerator}/{theta.denominator}",
            "value_exact": f"{gap.numerator}/{gap.denominator}",
            "status": "CLOSES" if gap <= 0 else "ABSTRACT_TWO_CAP_FAILURE",
        })
    for q in (Fraction(2), Fraction(5, 2), Fraction(3), Fraction(7, 2), Fraction(4)):
        factor = Fraction(8, 1) / Fraction(2, 1) ** q if q.denominator == 1 else None
        rows.append({
            "panel": "C",
            "parameter": "coefficient_power_q",
            "x_exact": f"{q.numerator}/{q.denominator}",
            "value_exact": f"{factor.numerator}/{factor.denominator}" if factor is not None else "8*2^(-q)",
            "status": "CRITICAL" if q == 3 else ("SUBCRITICAL" if q > 3 else "SUPERCRITICAL"),
        })
    return rows


def write_source_data(rows: list[dict[str, str]]) -> None:
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["panel", "parameter", "x_exact", "value_exact", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def finalize_svg(config: dict) -> None:
    path = HERE / "figure.svg"
    svg = path.read_text(encoding="utf-8")
    svg, count = re.subn(r'<svg width="[^"]+" height="[^"]+"', f'<svg width="{config["width_mm"]}mm" height="{config["height_mm"]}mm"', svg, count=1)
    assert count == 1
    regular = base64.b64encode(REGULAR.read_bytes()).decode("ascii")
    bold = base64.b64encode(BOLD.read_bytes()).decode("ascii")
    css = (
        "\n\t<defs><style type=\"text/css\"><![CDATA[\n"
        "@font-face { font-family: 'R074S13-Regular'; src: url(data:font/ttf;base64," + regular + ") format('truetype'); }\n"
        "@font-face { font-family: 'R074S13-Bold'; src: url(data:font/ttf;base64," + bold + ") format('truetype'); }\n"
        "]]></style></defs>"
    )
    svg, count = re.subn(r"(\s*</desc>)", r"\1" + css, svg, count=1)
    assert count == 1
    path.write_text(svg, encoding="utf-8")


def draw_temporal_panel(d: Drawing, x: float, y: float, w: float, h: float) -> None:
    panel(d, x, y, w, h, "A", "Temporal-integrability ceiling")
    left, right = x + 34, x + w - 12
    bottom, top = y + 34, y + h - 32
    target = Fraction(2, 3)
    y_min, y_max = 0.62, 1.02
    scale_x = lambda value: left + float(value) * (right - left)
    scale_y = lambda value: bottom + (float(value) - y_min) / (y_max - y_min) * (top - bottom)
    for tick, text in [(Fraction(0), "0 (p=infinity)"), (Fraction(1, 4), "1/4"), (Fraction(1, 2), "1/2"), (Fraction(3, 4), "3/4 (p=4/3)"), (Fraction(1), "1 (p=1)")]:
        px = scale_x(tick)
        d.add(Line(px, bottom, px, top, strokeColor=PALE, strokeWidth=0.6))
        label(d, px, bottom - 10, text, 3.9, color=MID, anchor="middle")
    for tick, text in [(target, "2/3 target"), (Fraction(4, 5), "4/5 limit"), (Fraction(10, 11), "10/11"), (Fraction(1), "1")]:
        py = scale_y(tick)
        d.add(Line(left, py, right, py, strokeColor=GRID, strokeWidth=0.55))
        label(d, left - 5, py - 1.5, text, 4.0, color=MID, anchor="end")
    d.add(Line(left, bottom, left, top, strokeColor=INK, strokeWidth=0.8))
    d.add(Line(left, bottom, right, bottom, strokeColor=INK, strokeWidth=0.8))
    d.add(Line(left, scale_y(target), right, scale_y(target), strokeColor=RED, strokeWidth=1.0, strokeDashArray=[4, 3]))
    points = []
    for numerator in range(0, 41):
        inverse_p = Fraction(numerator, 40)
        points.append((scale_x(inverse_p), scale_y(temporal_exponent(inverse_p))))
    for first, second in zip(points, points[1:]):
        d.add(Line(first[0], first[1], second[0], second[1], strokeColor=BLUE, strokeWidth=1.6))
    for inverse_p, value, text in [
        (Fraction(0), Fraction(4, 5), "p=infinity: 4/5"),
        (Fraction(3, 4), Fraction(10, 11), "p=4/3: 10/11"),
        (Fraction(1), Fraction(1), "p=1: 1"),
    ]:
        px, py = scale_x(inverse_p), scale_y(value)
        d.add(Circle(px, py, 2.6, fillColor=white, strokeColor=BLUE, strokeWidth=1.2))
        label(d, px + (-4 if inverse_p == 1 else 4), py + (5 if inverse_p != Fraction(3, 4) else -10), text, 4.0, color=BLUE, bold=True, anchor="end" if inverse_p == 1 else "start")
    label(d, (left + right) / 2, y + 10, "inverse time exponent 1/p", 4.4, color=MID, anchor="middle")
    label(d, x + 8, (bottom + top) / 2, "E_p", 4.4, color=MID, bold=True)
    label(d, right, top + 8, "E_p = 2(2p-1)/(5p-3)", 4.3, color=BLUE, bold=True, anchor="end")


def draw_threshold_panel(d: Drawing, x: float, y: float, w: float, h: float) -> None:
    panel(d, x, y, w, h, "B", "Two exact packing thresholds")
    half = (w - 26) / 2
    box(d, x + 8, y + h - 70, half, 36, ["Moving-Morrey cap", "theta <= 2/3", "closes S.329"], fill=BLUE_LIGHT, stroke=BLUE, status="CONDITIONAL")
    box(d, x + 16 + half, y + h - 70, half, 36, ["theta > 2/3", "equal-coordinate tail", "outgrows P^(2/3)"], fill=RED_LIGHT, stroke=RED, status="ABSTRACT")
    arrow(d, x + 8 + half, y + h - 52, x + 16 + half, y + h - 52)
    label(d, x + w / 2, y + h - 87, "threshold = 2/3 for the two-scalar-cap inference", 4.6, color=MID, bold=True, anchor="middle")
    box(d, x + 8, y + 42, half, 36, ["Child coefficient cube", "sum c_child^3", "<= theta_d c_parent^3"], fill=GOLD_LIGHT, stroke=GOLD, status="INTERFACE")
    box(d, x + 16 + half, y + 42, half, 36, ["Eight children x 1/2", "8(1/2)^3 = 1", "Dini constant grows"], fill=PLUM_LIGHT, stroke=PLUM, status="CRITICAL TREE")
    arrow(d, x + 8 + half, y + 60, x + 16 + half, y + 60)
    label(d, x + w / 2, y + 25, "uniform Dini: sup_d0 sum_n product_j theta_(d0+j) < infinity", 4.15, color=MID, anchor="middle")
    label(d, x + w / 2, y + 11, "strict cubic decay is sufficient; critical equality is not", 4.5, color=PLUM, bold=True, anchor="middle")


def render(config: dict) -> None:
    width, height = config["width_mm"] * mm, config["height_mm"] * mm
    drawing = Drawing(width, height)
    drawing.add(Rect(0, 0, width, height, fillColor=white, strokeColor=None))
    label(drawing, 14, height - 16, "R0.74S Step 13: temporal and packing thresholds", 8.2, bold=True)
    label(drawing, 14, height - 27, "ANALYTIC SCHEMATIC | EXACT FORMULAS | NOT SIMULATION OR DNS | OPEN GATES RETAINED | NOT CLAY", 5.0, color=MID)
    for dx, dy in [(0, 4.5), (4.5, 0), (0, -4.5), (-4.5, 0)]:
        drawing.add(Circle(width - 19 + dx, height - 18 + dy, 2.3, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=0.5))
    drawing.add(Circle(width - 19, height - 18, 1.8, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=0.5))
    content_y = 22
    content_h = height - 58
    gap = 10
    left_w = 255
    draw_temporal_panel(drawing, 14, content_y, left_w, content_h)
    draw_threshold_panel(drawing, 14 + left_w + gap, content_y, width - 28 - left_w - gap, content_h)
    renderPDF.drawToFile(drawing, str(HERE / "figure.pdf"), title="R0.74S Step 13 analytic threshold schematic")
    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"))
    finalize_svg(config)
    with tempfile.TemporaryDirectory(prefix="r074s13-png-") as temp:
        prefix = Path(temp) / "figure"
        subprocess.run([str(PDFTOPPM), "-png", "-singlefile", "-r", str(config["dpi"]), str(HERE / "figure.pdf"), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Image.open(prefix.with_suffix(".png")).save(HERE / "figure.png", dpi=(config["dpi"], config["dpi"]))


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    assert config["schema"] == "r074s-step13-temporal-morrey-figure-config-v1"
    rows = source_rows()
    write_source_data(rows)
    render(config)
    image = Image.open(HERE / "figure.png")
    environment = {
        "schema": "r074s-step13-temporal-morrey-environment-v1",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "pillow": PIL.__version__,
        "pypdf": pypdf.__version__,
        "reportlab": REPORTLAB_VERSION,
        "pdftoppm": str(PDFTOPPM),
        "regularFontSha256": sha(REGULAR),
        "boldFontSha256": sha(BOLD),
    }
    results = {
        "schema": "r074s-step13-temporal-morrey-results-v1",
        "sourceRows": len(rows),
        "pixelSize": list(image.size),
        "frozenResearchCommit": "533d9e70949da1ad19007fd741581a8c7e165e7c",
        "mainNoteSha256": sha(REPO / "research/r074s_temporal_integrability_morrey_threshold.md"),
        "certificateSha256": sha(REPO / "research/r074s_temporal_integrability_morrey_certificate.json"),
        "claimBoundary": "ANALYTIC SCHEMATIC; TEMPORAL METHOD CEILING ABOVE 2/3; MORREY 2/3 TWO-CAP THRESHOLD; CRITICAL CUBIC TREE OBSTRUCTION; S.280/S.288/S.303/S.342 OPEN; NOT CLAY",
    }
    (HERE / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "progress.ndjson").write_text("{\"stage\":\"exact-formula-rows\",\"status\":\"complete\"}\n{\"stage\":\"vector-raster\",\"status\":\"complete\"}\n", encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
