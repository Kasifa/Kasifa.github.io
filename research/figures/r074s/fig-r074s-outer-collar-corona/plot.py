#!/usr/bin/env python3
"""Render the R0.74S Step 14 outer-collar and jump-corona schematic."""

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
pdfmetrics.registerFont(TTFont("R074S14-Regular", str(REGULAR)))
pdfmetrics.registerFont(TTFont("R074S14-Bold", str(BOLD)))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label(d: Drawing, x: float, y: float, value: str, size: float = 5.0, *, color=INK, bold=False, anchor="start") -> None:
    d.add(String(x, y, value, fontName="R074S14-Bold" if bold else "R074S14-Regular", fontSize=size, fillColor=color, textAnchor=anchor))


def multiline(d: Drawing, x: float, y: float, lines: list[str], size: float = 5.0, *, color=INK, bold_first=False, leading=7.0, anchor="start") -> None:
    for index, line in enumerate(lines):
        label(d, x, y - index * leading, line, size, color=color, bold=bold_first and index == 0, anchor=anchor)


def panel(d: Drawing, x: float, y: float, w: float, h: float, tag: str, title: str) -> None:
    d.add(Rect(x, y, w, h, rx=4, ry=4, fillColor=white, strokeColor=GRID, strokeWidth=0.8))
    label(d, x + 8, y + h - 14, tag, 6.6, color=BLUE, bold=True)
    label(d, x + 25, y + h - 14, title, 5.45, bold=True)


def box(d: Drawing, x: float, y: float, w: float, h: float, lines: list[str], *, fill, stroke, status: str) -> None:
    d.add(Rect(x, y, w, h, rx=3, ry=3, fillColor=fill, strokeColor=stroke, strokeWidth=0.8))
    multiline(d, x + 6, y + h - 10, lines, 4.15, color=stroke, bold_first=True, leading=5.9)
    label(d, x + w - 5, y + 5, status, 3.55, color=stroke, bold=True, anchor="end")


def arrow(d: Drawing, x1: float, y1: float, x2: float, y2: float, *, color=MID, dashed=False) -> None:
    d.add(Line(x1, y1, x2 - 5, y2, strokeColor=color, strokeWidth=1.0, strokeDashArray=[3, 2] if dashed else None))
    d.add(Polygon([x2 - 5, y2 + 2.6, x2, y2, x2 - 5, y2 - 2.6], fillColor=color, strokeColor=color))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for k in (3, 4, 5, 6):
        rows.append({"panel": "A", "parameter": f"shell_k={k}:inner", "value_exact": f"exp(-15*4^{k-3}/32)", "status": "PROVED_INNER_GAIN"})
        rows.append({"panel": "A", "parameter": f"shell_k={k}:outer", "value_exact": "1", "status": "PROVED_OUTER_ALIGNMENT"})
    for lam in (Fraction(1, 4), Fraction(1), Fraction(4)):
        rows.append({"panel": "B", "parameter": f"lambda={lam}", "value_exact": "2^(1/3)*M_R", "status": "PROVED_THRESHOLD_NO_GAIN"})
    for alpha in (1, 3, 5):
        denominator = 2 ** (alpha - 1)
        rows.append({"panel": "C", "parameter": f"alpha={alpha}", "value_exact": f"1/({denominator}*kappa)", "status": "PROVED_JUMP_DINI"})
    for depth in range(0, 6):
        rows.append({"panel": "C", "parameter": f"critical_corona_depth={depth}", "value_exact": "1", "status": "ABSTRACT_CRITICAL_CUBE"})
    rows.append({"panel": "C", "parameter": "open_lemma", "value_exact": "S.375=>S.376", "status": "CONDITIONAL_ARROW_OPEN_ANTECEDENT"})
    return rows


def write_source_data(rows: list[dict[str, str]]) -> None:
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["panel", "parameter", "value_exact", "status"], lineterminator="\n")
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
        "@font-face { font-family: 'R074S14-Regular'; src: url(data:font/ttf;base64," + regular + ") format('truetype'); }\n"
        "@font-face { font-family: 'R074S14-Bold'; src: url(data:font/ttf;base64," + bold + ") format('truetype'); }\n"
        "]]></style></defs>"
    )
    svg, count = re.subn(r"(\s*</desc>)", r"\1" + css, svg, count=1)
    assert count == 1
    path.write_text(svg, encoding="utf-8")


def draw_collar_panel(d: Drawing, x: float, y: float, w: float, h: float) -> None:
    panel(d, x, y, w, h, "A", "Outer-collar coefficient alignment")
    axis_y = y + h - 78
    left, right = x + 14, x + w - 10
    d.add(Line(left, axis_y, right, axis_y, strokeColor=INK, strokeWidth=0.9))
    points = [left + 12, left + 45, left + 82, left + 119]
    names = ["rho_k", "2rho_k", "2rho_k+R/8", "4rho_k"]
    for px, name in zip(points, names):
        d.add(Line(px, axis_y - 4, px, axis_y + 4, strokeColor=INK, strokeWidth=0.7))
        label(d, px, axis_y - 13, name, 3.45, color=MID, anchor="middle")
    d.add(Rect(points[1], axis_y + 9, points[2] - points[1], 15, fillColor=RED_LIGHT, strokeColor=RED, strokeWidth=0.8))
    label(d, (points[1] + points[2]) / 2, axis_y + 14, "C_k,R^+", 4.0, color=RED, bold=True, anchor="middle")
    d.add(Line(points[1], axis_y + 28, points[3], axis_y + 28, strokeColor=RED, strokeWidth=1.0))
    label(d, (points[1] + points[3]) / 2, axis_y + 32, "A_k(2R) carries gamma_k", 3.85, color=RED, bold=True, anchor="middle")
    box(d, x + 8, y + h - 144, w - 16, 36, ["Outer face", "target gamma_k / payment gamma_k = 1", "finite deletion leaves infinitely many"], fill=RED_LIGHT, stroke=RED, status="PROVED GEOMETRIC")
    box(d, x + 8, y + 52, w - 16, 36, ["Inner face (k >= 3)", "gamma_k/gamma_(k-2) -> 0", "super-Gaussian gain only here"], fill=BLUE_LIGHT, stroke=BLUE, status="PROVED")
    box(d, x + 8, y + 9, w - 16, 31, ["Smooth aligned spikes", "weighted L1 cannot imply Lp, p>1"], fill=PLUM_LIGHT, stroke=PLUM, status="ABSTRACT ONLY")


def draw_threshold_panel(d: Drawing, x: float, y: float, w: float, h: float) -> None:
    panel(d, x, y, w, h, "B", "Critical density threshold")
    top_y = y + h - 48
    box(d, x + 8, top_y - 39, w - 16, 39, ["First lambda-roots", "sum rho_Q <= M_R/lambda", "sum p_Q <= (2lambda)^(1/2) M_R"], fill=BLUE_LIGHT, stroke=BLUE, status="PROVED")
    arrow(d, x + w / 2, top_y - 43, x + w / 2, top_y - 59, color=BLUE)
    box(d, x + 8, top_y - 104, w - 16, 41, ["Critical factorization", "m_Q = rho_Q^(1/3) p_Q^(2/3)", "lambda cancels exactly"], fill=GOLD_LIGHT, stroke=GOLD, status="NO GAIN")
    label(d, x + w / 2, y + 76, "(M_R/lambda)^(1/3)", 4.0, color=INK, bold=True, anchor="middle")
    label(d, x + w / 2, y + 65, "x ((2lambda)^(1/2) M_R)^(2/3)", 3.75, color=INK, anchor="middle")
    label(d, x + w / 2, y + 51, "= 2^(1/3) M_R", 4.8, color=RED, bold=True, anchor="middle")
    box(d, x + 8, y + 9, w - 16, 29, ["Changing lambda cannot improve", "a linear total-measure payment"], fill=RED_LIGHT, stroke=RED, status="PROVED THRESHOLD")


def draw_corona_panel(d: Drawing, x: float, y: float, w: float, h: float) -> None:
    panel(d, x, y, w, h, "C", "Jump skeleton versus unpaid corona")
    root_x, root_y = x + w / 2, y + h - 48
    d.add(Circle(root_x, root_y, 6, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=1.0))
    label(d, root_x, root_y - 1.8, "S", 4.8, color=BLUE, bold=True, anchor="middle")
    level1 = [(x + 27, y + h - 90), (x + w / 2, y + h - 90), (x + w - 27, y + h - 90)]
    for idx, (cx, cy) in enumerate(level1):
        color = GOLD if idx == 1 else BLUE
        fill = GOLD_LIGHT if idx == 1 else BLUE_LIGHT
        d.add(Line(root_x, root_y - 6, cx, cy + 6, strokeColor=color, strokeWidth=1.2, strokeDashArray=[3, 2] if idx == 1 else None))
        d.add(Circle(cx, cy, 5.3, fillColor=fill, strokeColor=color, strokeWidth=0.9))
        label(d, cx, cy - 1.5, "C" if idx == 1 else "J", 4.2, color=color, bold=True, anchor="middle")
    label(d, root_x, y + h - 112, "jump: sum c_child^3 <= theta c_S^3", 3.55, color=BLUE, bold=True, anchor="middle")
    label(d, root_x, y + h - 123, "theta = 2^(1-alpha)/kappa < 1", 3.75, color=BLUE, anchor="middle")
    d.add(Rect(x + 10, y + 77, w - 20, 38, rx=3, ry=3, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=0.9, strokeDashArray=[3, 2]))
    multiline(d, x + w / 2, y + 102, ["LOW-TRANSITION CORONA", "moving drift + unreached nodes", "no quadratic q-budget yet"], 4.0, color=GOLD, bold_first=True, leading=6.0, anchor="middle")
    box(d, x + 8, y + 38, w - 16, 29, ["Critical eight-child corona", "8(1/2)^3 = 1 repeats"], fill=PLUM_LIGHT, stroke=PLUM, status="ABSTRACT")
    box(d, x + 8, y + 8, w - 16, 22, ["S.375 => S.376", "PDE antecedent remains open"], fill=RED_LIGHT, stroke=RED, status="CONDITIONAL")


def render(config: dict) -> None:
    width, height = config["width_mm"] * mm, config["height_mm"] * mm
    drawing = Drawing(width, height)
    drawing.add(Rect(0, 0, width, height, fillColor=white, strokeColor=None))
    label(drawing, 14, height - 16, "R0.74S Step 14: outer-collar and jump-corona method boundary", 8.0, bold=True)
    label(drawing, 14, height - 27, "ANALYTIC SCHEMATIC | EXACT FORMULAS | NOT SIMULATION OR DNS | OPEN PDE LEMMA | NOT CLAY", 4.9, color=MID)
    for dx, dy in [(0, 4.5), (4.5, 0), (0, -4.5), (-4.5, 0)]:
        drawing.add(Circle(width - 19 + dx, height - 18 + dy, 2.3, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=0.5))
    drawing.add(Circle(width - 19, height - 18, 1.8, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=0.5))
    content_y = 20
    content_h = height - 57
    gap = 8
    panel_w = (width - 28 - 2 * gap) / 3
    draw_collar_panel(drawing, 14, content_y, panel_w, content_h)
    draw_threshold_panel(drawing, 14 + panel_w + gap, content_y, panel_w, content_h)
    draw_corona_panel(drawing, 14 + 2 * (panel_w + gap), content_y, panel_w, content_h)
    renderPDF.drawToFile(drawing, str(HERE / "figure.pdf"), title="R0.74S Step 14 outer-collar and jump-corona analytic schematic")
    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"))
    finalize_svg(config)
    with tempfile.TemporaryDirectory(prefix="r074s14-png-") as temp:
        prefix = Path(temp) / "figure"
        subprocess.run([str(PDFTOPPM), "-png", "-singlefile", "-r", str(config["dpi"]), str(HERE / "figure.pdf"), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Image.open(prefix.with_suffix(".png")).save(HERE / "figure.png", dpi=(config["dpi"], config["dpi"]))


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    assert config["schema"] == "r074s-step14-outer-collar-corona-figure-config-v1"
    rows = source_rows()
    write_source_data(rows)
    render(config)
    image = Image.open(HERE / "figure.png")
    environment = {
        "schema": "r074s-step14-outer-collar-corona-environment-v1",
        "python": sys.version.split()[0], "platform": platform.platform(),
        "pillow": PIL.__version__, "pypdf": pypdf.__version__, "reportlab": REPORTLAB_VERSION,
        "pdftoppm": str(PDFTOPPM), "regularFontSha256": sha(REGULAR), "boldFontSha256": sha(BOLD),
    }
    results = {
        "schema": "r074s-step14-outer-collar-corona-results-v1",
        "sourceRows": len(rows), "pixelSize": list(image.size),
        "frozenResearchCommit": "468f8cba70c9281cb00e97a40135a2224cc1e4cd",
        "mainNoteSha256": sha(REPO / "research/r074s_outer_collar_corona_obstruction.md"),
        "certificateSha256": sha(REPO / "research/r074s_outer_collar_corona_certificate.json"),
        "claimBoundary": "ANALYTIC SCHEMATIC; PROVED OUTER ALIGNMENT AND THRESHOLD NO-GAIN; ABSTRACT SPIKE AND CRITICAL CORONA; S.358/S.376 CONDITIONAL; S.342/S.375/S.288/S.303 OPEN; NOT CLAY",
    }
    (HERE / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "progress.ndjson").write_text("{\"stage\":\"exact-formula-rows\",\"status\":\"complete\"}\n{\"stage\":\"vector-raster\",\"status\":\"complete\"}\n", encoding="utf-8")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
