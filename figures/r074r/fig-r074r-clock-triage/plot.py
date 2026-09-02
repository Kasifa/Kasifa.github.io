#!/usr/bin/env python3
"""Render the deterministic R0.74R clock-triage figure."""

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
REPO = HERE.parents[3]
INK = HexColor("#202A34")
MID = HexColor("#67727B")
GRID = HexColor("#D2D9DE")
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
    override = os.environ.get("R074R_DEPENDENCIES_ROOT")
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
    candidates = []
    if BUNDLE:
        candidates.append(BUNDLE / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype" / name)
    candidates += [
        Path("/System/Library/Fonts/Supplemental") / name,
        Path("/Library/Fonts") / name,
        Path("/usr/share/fonts/truetype/dejavu") / name,
    ]
    for path in candidates:
        if path.is_file():
            return path
    raise FileNotFoundError(name)


REGULAR = font_path("DejaVuSans.ttf")
BOLD = font_path("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074R-Regular", str(REGULAR)))
pdfmetrics.registerFont(TTFont("R074R-Bold", str(BOLD)))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label(d: Drawing, x: float, y: float, value: str, size: float = 5.0, *, color=INK, bold=False, anchor="start") -> None:
    d.add(String(x, y, value, fontName="R074R-Bold" if bold else "R074R-Regular", fontSize=size, fillColor=color, textAnchor=anchor))


def multiline(d: Drawing, x: float, y: float, lines: list[str], size: float = 5.0, *, color=INK, bold_first=False, leading=7.0, anchor="start") -> None:
    for i, line in enumerate(lines):
        label(d, x, y - i * leading, line, size, color=color, bold=bold_first and i == 0, anchor=anchor)


def panel(d: Drawing, x: float, y: float, w: float, h: float, tag: str, title: str) -> None:
    d.add(Rect(x, y, w, h, rx=4, ry=4, fillColor=white, strokeColor=GRID, strokeWidth=0.8))
    label(d, x + 8, y + h - 14, tag, 6.6, color=BLUE, bold=True)
    label(d, x + 25, y + h - 14, title, 6.0, bold=True)


def box(d: Drawing, x: float, y: float, w: float, h: float, lines: list[str], *, fill, stroke, status: str | None = None) -> None:
    d.add(Rect(x, y, w, h, rx=3, ry=3, fillColor=fill, strokeColor=stroke, strokeWidth=0.8))
    multiline(d, x + w / 2, y + h / 2 + (3 if len(lines) == 2 else 0), lines, 5.0, color=stroke, bold_first=True, leading=6.8, anchor="middle")
    if status:
        label(d, x + w - 5, y + 5, status, 4.5, color=stroke, bold=True, anchor="end")


def arrow(d: Drawing, x1: float, y1: float, x2: float, y2: float, *, color=MID) -> None:
    d.add(Line(x1, y1, x2 - 6, y2, strokeColor=color, strokeWidth=1.0))
    d.add(Polygon([x2 - 6, y2 + 3, x2, y2, x2 - 6, y2 - 3], fillColor=color, strokeColor=color))


def write_source_data(config: dict) -> None:
    fields = ["panel", "id", "statement", "status"]
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(config["rows"])


def finalize_svg(config: dict) -> None:
    path = HERE / "figure.svg"
    svg = path.read_text(encoding="utf-8")
    svg, count = re.subn(r'<svg width="[^"]+" height="[^"]+"', f'<svg width="{config["width_mm"]}mm" height="{config["height_mm"]}mm"', svg, count=1)
    assert count == 1
    regular = base64.b64encode(REGULAR.read_bytes()).decode("ascii")
    bold = base64.b64encode(BOLD.read_bytes()).decode("ascii")
    css = (
        "\n\t<defs><style type=\"text/css\"><![CDATA[\n"
        "@font-face { font-family: 'R074R-Regular'; src: url(data:font/ttf;base64," + regular + ") format('truetype'); }\n"
        "@font-face { font-family: 'R074R-Bold'; src: url(data:font/ttf;base64," + bold + ") format('truetype'); }\n"
        "]]></style></defs>"
    )
    svg, count = re.subn(r"(\s*</desc>)", r"\1" + css, svg, count=1)
    assert count == 1
    path.write_text(svg, encoding="utf-8")


def render(config: dict) -> None:
    width, height = config["width_mm"] * mm, config["height_mm"] * mm
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=white, strokeColor=None))
    label(d, 14, height - 16, "Terminal-window contraction and the arbitrary-clock gate", 8.4, bold=True)
    label(d, 14, height - 27, "R0.74R analytic route  |  no simulation or DNS  |  NOT CLAY", 5.2, color=MID)
    for dx, dy in [(0, 4.5), (4.5, 0), (0, -4.5), (-4.5, 0)]:
        d.add(Circle(width - 19 + dx, height - 18 + dy, 2.3, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=0.5))
    d.add(Circle(width - 19, height - 18, 1.8, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=0.5))

    y, h = 22, height - 58
    ax, aw = 14, 154
    bx, bw = 175, 160
    cx, cw = 342, width - 356
    panel(d, ax, y, aw, h, "A", "Terminal window")
    panel(d, bx, y, bw, h, "B", "Arbitrary completed clock")
    panel(d, cx, y, cw, h, "C", "Exact remaining gate")

    box(d, ax + 10, y + h - 62, 58, 28, ["mass in", "target lobes"], fill=BLUE_LIGHT, stroke=BLUE, status="PROVED")
    box(d, ax + 86, y + h - 62, 58, 28, ["bounded", "cubic payment"], fill=GOLD_LIGHT, stroke=GOLD)
    box(d, ax + 31, y + h - 119, 92, 34, ["mass contracts to", "the first target shell"], fill=PLUM_LIGHT, stroke=PLUM, status="PROVED")
    d.add(Line(ax + 39, y + h - 62, ax + 58, y + h - 85, strokeColor=MID, strokeWidth=1.0))
    d.add(Line(ax + 115, y + h - 62, ax + 96, y + h - 85, strokeColor=MID, strokeWidth=1.0))
    multiline(d, ax + 10, y + 42, ["Bounded payment forbids broad", "terminal-window target mass."], 4.8, color=MID, leading=6.5)

    box(d, bx + 49, y + h - 57, 62, 25, ["large K(tau)"], fill=PALE, stroke=INK, status="PROVED TRIAGE")
    branch_y = y + h - 112
    boxes = [
        (bx + 7, ["D(tau)", ">= K/2"], BLUE_LIGHT, BLUE),
        (bx + 56, ["avg E", ">= K/4"], GOLD_LIGHT, GOLD),
        (bx + 105, ["recent Var+", ">= K/4"], PLUM_LIGHT, PLUM),
    ]
    for x0, lines, fill, stroke in boxes:
        d.add(Line(bx + 80, y + h - 57, x0 + 23, branch_y + 30, strokeColor=MID, strokeWidth=0.85))
        box(d, x0, branch_y, 46, 30, lines, fill=fill, stroke=stroke)
    multiline(d, bx + 9, y + 44, ["At least one branch occurs.", "Only the kinetic branch directly", "supplies the needed time window."], 4.8, color=MID, leading=6.4)

    box(d, cx + 10, y + h - 64, cw - 20, 31, ["universal extraction +", "persistence packing"], fill=RED_LIGHT, stroke=RED, status="OPEN")
    arrow(d, cx + cw / 2, y + h - 70, cx + cw / 2, y + h - 93, color=RED)
    box(d, cx + 10, y + h - 126, cw - 20, 34, ["best-terminal tail", "and Q.1 follow"], fill=BLUE_LIGHT, stroke=BLUE, status="PROVED CONDITIONAL")
    multiline(d, cx + 10, y + 48, ["NO-GO: scalar positivity,", "thin-time, and pure functional", "shortcuts are excluded."], 4.8, color=RED, bold_first=True, leading=6.3)
    label(d, cx + 10, y + 22, "Witnesses are NOT NSE solutions.", 4.8, color=MID, bold=True)

    renderPDF.drawToFile(d, str(HERE / "figure.pdf"), title="R0.74R clock triage")
    renderSVG.drawToFile(d, str(HERE / "figure.svg"))
    finalize_svg(config)

    with tempfile.TemporaryDirectory(prefix="r074r-png-") as temp:
        prefix = Path(temp) / "figure"
        subprocess.run([str(PDFTOPPM), "-png", "-singlefile", "-r", str(config["dpi"]), str(HERE / "figure.pdf"), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Image.open(prefix.with_suffix(".png")).save(HERE / "figure.png", dpi=(config["dpi"], config["dpi"]))


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    assert config["schema"] == "r074r-clock-triage-config-v1"
    assert len(config["rows"]) == 9
    (HERE / "progress.ndjson").write_text("", encoding="utf-8")
    write_source_data(config)
    render(config)
    image = Image.open(HERE / "figure.png")
    environment = {
        "schema": "r074r-clock-triage-environment-v1",
        "python": sys.version.split()[0], "platform": platform.platform(),
        "pillow": PIL.__version__, "pypdf": pypdf.__version__, "reportlab": REPORTLAB_VERSION,
        "pdftoppm": str(PDFTOPPM), "regular_font_sha256": sha(REGULAR), "bold_font_sha256": sha(BOLD),
    }
    results = {
        "schema": "r074r-clock-triage-results-v1", "rows": 9,
        "pixel_size": list(image.size),
        "terminal_certificate_sha256": sha(REPO / "research/r074r_persistent_lobe_certificate.json"),
        "arbitrary_clock_certificate_sha256": sha(REPO / "research/r074r_arbitrary_clock_gate_certificate.json"),
        "independent_certificate_sha256": sha(REPO / "research/r074r_arbitrary_clock_independent_certificate.json"),
        "claim_boundary": "PROVED window theorem; PROVED CONDITIONAL arbitrary-clock implication; universal inputs OPEN; NOT CLAY",
    }
    (HERE / "environment.json").write_text(json.dumps(environment, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "results.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (HERE / "progress.ndjson").write_text(
        "{\"stage\":\"source-data\",\"status\":\"complete\"}\n{\"stage\":\"vector-raster\",\"status\":\"complete\"}\n",
        encoding="utf-8",
    )
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
