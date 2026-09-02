#!/usr/bin/env python3
"""Render the deterministic R0.74S ball-clock debt figure."""

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
pdfmetrics.registerFont(TTFont("R074S-Regular", str(REGULAR)))
pdfmetrics.registerFont(TTFont("R074S-Bold", str(BOLD)))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def label(d: Drawing, x: float, y: float, value: str, size: float = 5.0, *, color=INK, bold=False, anchor="start") -> None:
    d.add(String(x, y, value, fontName="R074S-Bold" if bold else "R074S-Regular", fontSize=size, fillColor=color, textAnchor=anchor))


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
        "@font-face { font-family: 'R074S-Regular'; src: url(data:font/ttf;base64," + regular + ") format('truetype'); }\n"
        "@font-face { font-family: 'R074S-Bold'; src: url(data:font/ttf;base64," + bold + ") format('truetype'); }\n"
        "]]></style></defs>"
    )
    svg, count = re.subn(r"(\s*</desc>)", r"\1" + css, svg, count=1)
    assert count == 1
    path.write_text(svg, encoding="utf-8")


def render(config: dict) -> None:
    width, height = config["width_mm"] * mm, config["height_mm"] * mm
    d = Drawing(width, height)
    d.add(Rect(0, 0, width, height, fillColor=white, strokeColor=None))
    label(d, 14, height - 16, "Canonical best-N last exits: exact representations, no new compression", 8.2, bold=True)
    label(d, 14, height - 27, "R0.74S STEP 9  |  SHARP B_Q ERROR  |  NO-GAIN / NO-GO  |  NOT CLAY", 5.2, color=MID)
    for dx, dy in [(0, 4.5), (4.5, 0), (0, -4.5), (-4.5, 0)]:
        d.add(Circle(width - 19 + dx, height - 18 + dy, 2.3, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=0.5))
    d.add(Circle(width - 19, height - 18, 1.8, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=0.5))

    y, h = 22, height - 58
    ax, aw = 14, 154
    bx, bw = 175, 160
    cx, cw = 342, width - 356
    panel(d, ax, y, aw, h, "A", "Signed F half-exit")
    panel(d, bx, y, bw, h, "B", "K-theta last exit")
    panel(d, cx, y, cw, h, "C", "No-gain boundary")

    box(d, ax + 10, y + h - 64, 134, 30, ["W_half^F = (1/2) S_N^F", "forced signed full tail"], fill=BLUE_LIGHT, stroke=BLUE, status="EXACT")
    box(d, ax + 10, y + h - 106, 134, 29, ["sup_tau inf_{S_tau}", "exceptions depend on terminal"], fill=GOLD_LIGHT, stroke=GOLD, status="ORDER")
    box(d, ax + 10, y + h - 148, 134, 29, ["F half-exit may fail S.25", "closure is not admissibility"], fill=RED_LIGHT, stroke=RED, status="FALSE")
    multiline(d, ax + 10, y + 29, ["Cancellation remains inside the", "complete nonexceptional tail."], 4.8, color=MID, leading=6.5)

    box(d, bx + 12, y + h - 65, 136, 31, ["L_theta = (1-theta)T", "minus Delta Q"], fill=BLUE_LIGHT, stroke=BLUE, status="EXACT")
    box(d, bx + 12, y + h - 108, 136, 30, ["| W_theta^K", "- (1-theta) S_N^K | <= B_Q"], fill=GOLD_LIGHT, stroke=GOLD, status="SHARP")
    box(d, bx + 12, y + h - 150, 136, 29, ["theta < 3/4", "finite good-stop closure"], fill=PLUM_LIGHT, stroke=PLUM, status="SCOPED")
    multiline(d, bx + 10, y + 29, ["No continuity of the selector;", "no infinite cutoff test."], 4.8, color=MID, leading=6.3)

    box(d, cx + 10, y + h - 69, cw - 20, 35, ["canonical last-exit bounds", "equivalent to open best-N tails"], fill=RED_LIGHT, stroke=RED, status="NO-GAIN")
    box(d, cx + 10, y + h - 112, cw - 20, 28, ["full domain = Q.12", "plateau domain is weaker"], fill=GOLD_LIGHT, stroke=GOLD, status="DISTINCT")
    box(d, cx + 10, y + h - 155, cw - 20, 29, ["NEXT: paid-branch", "forced PDE residual tail"], fill=BLUE_LIGHT, stroke=BLUE, status="OPEN")
    multiline(d, cx + 10, y + 29, ["No new quadratic compression.", "Step 8 no-go and S.38 retained.", "No regularity conclusion."], 4.7, color=MID, leading=6.1)
    label(d, cx + 10, y + 12, "NOT CLAY.", 4.9, color=RED, bold=True)

    renderPDF.drawToFile(d, str(HERE / "figure.pdf"), title="R0.74S canonical best-N last-exit no-gain")
    renderSVG.drawToFile(d, str(HERE / "figure.svg"))
    finalize_svg(config)

    with tempfile.TemporaryDirectory(prefix="r074s-png-") as temp:
        prefix = Path(temp) / "figure"
        subprocess.run([str(PDFTOPPM), "-png", "-singlefile", "-r", str(config["dpi"]), str(HERE / "figure.pdf"), str(prefix)], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Image.open(prefix.with_suffix(".png")).save(HERE / "figure.png", dpi=(config["dpi"], config["dpi"]))


def main() -> None:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    assert config["schema"] == "r074s-ball-clock-debt-config-v1"
    assert len(config["rows"]) == 9
    (HERE / "progress.ndjson").write_text("", encoding="utf-8")
    write_source_data(config)
    render(config)
    image = Image.open(HERE / "figure.png")
    environment = {
        "schema": "r074s-ball-clock-debt-environment-v1",
        "python": sys.version.split()[0], "platform": platform.platform(),
        "pillow": PIL.__version__, "pypdf": pypdf.__version__, "reportlab": REPORTLAB_VERSION,
        "pdftoppm": str(PDFTOPPM), "regular_font_sha256": sha(REGULAR), "bold_font_sha256": sha(BOLD),
    }
    results = {
        "schema": "r074s-ball-clock-debt-results-v1", "rows": 9,
        "pixel_size": list(image.size),
        "one_sided_certificate_sha256": sha(REPO / "research/r074s_one_sided_ball_clock_certificate.json"),
        "cross_channel_certificate_sha256": sha(REPO / "research/r074s_cross_channel_recombination_certificate.json"),
        "dissipation_rayleigh_certificate_sha256": sha(REPO / "research/r074s_dissipation_rayleigh_certificate.json"),
        "step8_certificate_sha256": sha(REPO / "research/r074s_defect_relaxed_total_rayleigh_certificate.json"),
        "step9_certificate_sha256": sha(REPO / "research/r074s_best_n_last_exit_certificate.json"),
        "analytic_note_sha256": sha(REPO / "research/r074s_best_n_last_exit_equivalence.md"),
        "claim_boundary": "CANONICAL BEST-N LAST EXITS ARE EXACT TERMINAL-TAIL REPRESENTATIONS; NO NEW QUADRATIC COMPRESSION; PDE RESIDUAL TAIL OPEN; NOT CLAY",
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
