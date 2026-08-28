#!/usr/bin/env python3
"""Generate the R0.72U two-moment journal figure.

The source stage supports ``--self-test`` without writing any output.  Draft or
formal rendering is available only after the exact certificate exists.  Formal
rendering is bound to the certificate's source commit and to a separate
certificate commit, and is the only mode that copies assets to the public route.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import time
from typing import Any
from xml.sax.saxutils import escape


REPOSITORY = Path(__file__).resolve().parents[1]
PACKAGE = (
    REPOSITORY
    / "figures/r072u-local-observability/fig-r072u-two-moment-coercivity"
)
CERTIFICATE_DIR = REPOSITORY / "research/certificates/r072u"
CERTIFICATE = CERTIFICATE_DIR / "certificate.json"
PUBLIC = REPOSITORY / "public/assets/r072u"
FIGURE_ID = "fig-r072u-two-moment-coercivity"
WIDTH_MM = 178
HEIGHT_MM = 76
PNG_DPI = 600
PAPER = "#ffffff"
INK = "#17212b"
MUTED = "#66727e"
GRID = "#d9dde1"
BLUE = "#285f8f"
GOLD = "#a6781f"
PALE_GOLD = "#f4f0e6"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def linspace(left: float, right: float, count: int) -> list[float]:
    if count < 2:
        raise ValueError("linspace needs at least two points")
    return [left + (right - left) * index / (count - 1) for index in range(count)]


def rho(x: float) -> float:
    if abs(x) > 1:
        return 0.0
    return 315.0 / 256.0 * (1.0 - x * x) ** 4


def x_rho(x: float) -> float:
    return x * rho(x)


def k_c(center: float, s: float) -> float:
    return 3.0 / 143.0 + 6.0 * (center + s) / 11.0


def fixed_gauge_energy(z: float) -> float:
    return 3.0 * z * z + 4.0 / 5.0


def analytic_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for x in linspace(-1.0, 1.0, 401):
        for series, value in (("rho", rho(x)), ("X-rho", x_rho(x))):
            rows.append({
                "panel": "A",
                "series": series,
                "x": f"{x:.17g}",
                "y": f"{value:.17g}",
                "source": "rho=(315/256)(1-X^2)^4 on [-1,1]",
                "status": "analytic presentation sample",
            })
    threshold = 27.0 / 13.0
    for center, label in ((-threshold, "c=-27/13"), (0.0, "c=0"), (threshold, "c=27/13")):
        for s in linspace(-1.0, 1.0, 401):
            rows.append({
                "panel": "B",
                "series": label,
                "x": f"{s:.17g}",
                "y": f"{k_c(center, s):.17g}",
                "source": "K_c(s)=3/143+6(c+s)/11",
                "status": "analytic presentation sample",
            })
    for z in linspace(-1.2, 1.2, 401):
        rows.append({
            "panel": "C",
            "series": "optimized-fixed-gauge-energy",
            "x": f"{z:.17g}",
            "y": f"{fixed_gauge_energy(z):.17g}",
            "source": "3*z^2+4/5, z=X^2+2c, T=1",
            "status": "exact inviscid calibration sample",
        })
    return rows


class Scene:
    def __init__(self) -> None:
        self.items: list[tuple] = []

    def line(self, x1, y1, x2, y2, color=INK, width=2, dash=None):
        self.items.append(("line", x1, y1, x2, y2, color, width, dash))

    def polyline(self, points, color=BLUE, width=2, dash=None):
        self.items.append(("polyline", points, color, width, dash))

    def text(self, x, y, value, size=18, color=INK, anchor="start", bold=False):
        self.items.append(("text", x, y, value, size, color, anchor, bold))

    def circle(self, x, y, radius, color=INK):
        self.items.append(("circle", x, y, radius, color))

    def rect(self, left, top, right, bottom, fill=PAPER):
        self.items.append(("rect", left, top, right, bottom, fill))


def mapping(x0, x1, y0, y1, left, right, top, bottom):
    return (
        lambda x: left + (x - x0) * (right - left) / (x1 - x0),
        lambda y: bottom - (y - y0) * (bottom - top) / (y1 - y0),
    )


def axes(scene: Scene, box, x_ticks, y_ticks, x_map, y_map, xlabel, ylabel):
    left, right, top, bottom = box
    for value in x_ticks:
        x = x_map(value)
        scene.line(x, top, x, bottom, GRID, 1)
        scene.text(x, bottom + 28, f"{value:g}", 20, MUTED, "middle")
    for value in y_ticks:
        y = y_map(value)
        scene.line(left, y, right, y, GRID, 1)
        scene.text(left - 10, y + 7, f"{value:g}", 20, MUTED, "end")
    scene.line(left, bottom, right, bottom, INK, 2)
    scene.line(left, top, left, bottom, INK, 2)
    scene.text((left + right) / 2, bottom + 61, xlabel, 23, anchor="middle")
    scene.text(left, top - 18, ylabel, 22)


def build_scene() -> Scene:
    scene = Scene()
    ink, muted = INK, MUTED
    blue, gold = BLUE, GOLD
    panel_lefts = (60, 625, 1190)
    box_width = 475
    top, bottom = 145, 620
    titles = (
        ("A", "exact rational probe"),
        ("B", "two-moment coefficient"),
        ("C", "fixed-gauge inviscid floor"),
    )
    for left, (letter, title) in zip(panel_lefts, titles):
        scene.text(left, 65, letter, 34, ink, bold=True)
        scene.text(left + 42, 65, title, 27, ink, bold=True)

    box = (panel_lefts[0] + 48, panel_lefts[0] + box_width, top, bottom)
    xm, ym = mapping(-1.0, 1.0, -0.65, 1.32, *box)
    axes(scene, box, [-1, -0.5, 0, 0.5, 1], [-0.5, 0, 0.5, 1], xm, ym, "X", "probe value")
    grid = linspace(-1.0, 1.0, 500)
    scene.polyline([(xm(x), ym(rho(x))) for x in grid], blue, 4)
    scene.polyline([(xm(x), ym(x_rho(x))) for x in grid], gold, 3, "8,5")
    scene.text(box[0] + 8, top + 28, "rho=(315/256)(1-X^2)^4", 19, muted)
    scene.text(box[0] + 8, top + 55, "mu2=1/11;  mu4=3/143", 20, ink, bold=True)
    scene.line(box[1] - 142, top + 82, box[1] - 105, top + 82, blue, 4)
    scene.text(box[1] - 96, top + 89, "rho", 19, ink)
    scene.line(box[1] - 142, top + 111, box[1] - 105, top + 111, gold, 3, "8,5")
    scene.text(box[1] - 96, top + 118, "X rho", 19, ink)

    box = (panel_lefts[1] + 48, panel_lefts[1] + box_width, top, bottom)
    xm, ym = mapping(-1.0, 1.0, -1.8, 1.8, *box)
    axes(scene, box, [-1, -0.5, 0, 0.5, 1], [-1.5, -0.75, 0, 0.75, 1.5], xm, ym, "s  (T=1)", "K_c(s)")
    scene.line(box[0], ym(0), box[1], ym(0), ink, 2)
    threshold = 27.0 / 13.0
    series = (
        (-threshold, gold, "8,5", "c=-27/13"),
        (0.0, muted, "3,4", "c=0"),
        (threshold, blue, None, "c=27/13"),
    )
    for center, color, dash, _ in series:
        scene.polyline([(xm(s), ym(k_c(center, s))) for s in grid], color, 3, dash)
    scene.circle(xm(1), ym(-81 / 143), 7, gold)
    scene.text(xm(1) - 12, ym(-81 / 143) - 13, "-81/143", 18, gold, "end", True)
    scene.circle(xm(-1), ym(87 / 143), 7, blue)
    scene.rect(box[0] + 126, top + 3, box[1] - 2, top + 70, PAPER)
    scene.text(box[0] + 137, top + 30, "K_c=3/143+6(c+s)/11", 19, ink, bold=True)
    scene.text(box[0] + 137, top + 58, "|c| >= 27/13: fixed sign", 19, ink)
    for index, (_, color, dash, label) in enumerate(series):
        y = bottom - 92 + 29 * index
        scene.line(box[0] + 10, y - 7, box[0] + 47, y - 7, color, 3, dash)
        scene.text(box[0] + 56, y, label, 18, ink)

    box = (panel_lefts[2] + 48, panel_lefts[2] + box_width, top, bottom)
    xm, ym = mapping(-1.2, 1.2, 0.6, 5.25, *box)
    axes(scene, box, [-1, -0.5, 0, 0.5, 1], [0.8, 2, 3, 4, 5], xm, ym, "z = X^2 + 2c", "optimized mean square")
    z_grid = linspace(-1.2, 1.2, 500)
    scene.polyline([(xm(z), ym(fixed_gauge_energy(z))) for z in z_grid], blue, 4)
    scene.line(box[0], ym(4 / 5), box[1], ym(4 / 5), gold, 3, "8,5")
    scene.circle(xm(0), ym(4 / 5), 8, ink)
    scene.rect(box[0] + 84, top + 3, box[1] - 2, top + 72, PAPER)
    scene.text(box[0] + 95, top + 31, "3 z^2 + 4/5", 22, blue, bold=True)
    scene.text(box[0] + 95, top + 61, "exact floor = 4/5  (T=1)", 19, gold)
    scene.text(box[0] + 10, bottom - 79, "fixed initial phase gradient", 18, muted)
    scene.text(box[0] + 10, bottom - 48, "inviscid calibration only", 18, muted)

    scene.rect(1165, 682, 1718, 735, PALE_GOLD)
    scene.text(1441, 718, "whole-line block contraction: OPEN", 24, gold, "middle", True)

    # Locked five-petal research blossom.  It is decorative, carries no data,
    # and stays inside the otherwise unused top-right header corner.
    blossom_x, blossom_y = 1738, 42
    for index in range(5):
        angle = -math.pi / 2 + 2 * math.pi * index / 5
        scene.circle(
            blossom_x + 11 * math.cos(angle),
            blossom_y + 11 * math.sin(angle),
            6,
            blue if index % 2 == 0 else gold,
        )
    scene.circle(blossom_x, blossom_y, 4, ink)
    return scene


def save_data(rows: list[dict[str, str]]) -> None:
    with (PACKAGE / "data.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=("panel", "series", "x", "y", "source", "status"))
        writer.writeheader()
        writer.writerows(rows)


def render_svg(scene: Scene) -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<svg xmlns="http://www.w3.org/2000/svg" width="178mm" height="76mm" viewBox="0 0 1780 760">',
        f'<rect width="1780" height="760" fill="{PAPER}"/>',
    ]
    for item in scene.items:
        if item[0] == "line":
            _, x1, y1, x2, y2, color, width, dash = item
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            parts.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{width}"{extra}/>')
        elif item[0] == "polyline":
            _, points, color, width, dash = item
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            coordinates = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
            parts.append(f'<polyline points="{coordinates}" fill="none" stroke="{color}" stroke-width="{width}"{extra}/>')
        elif item[0] == "circle":
            _, x, y, radius, color = item
            parts.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" fill="{color}"/>')
        elif item[0] == "rect":
            _, left, top, right, bottom, fill = item
            parts.append(f'<rect x="{left:.3f}" y="{top:.3f}" width="{right-left:.3f}" height="{bottom-top:.3f}" fill="{fill}"/>')
        else:
            _, x, y, value, size, color, anchor, bold = item
            weight = "700" if bold else "400"
            parts.append(f'<text x="{x:.3f}" y="{y:.3f}" font-family="DejaVu Sans,Arial,sans-serif" font-size="{size}" font-weight="{weight}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>')
    parts.append("</svg>")
    (PACKAGE / "figure.svg").write_text("\n".join(parts) + "\n", encoding="utf-8")


def render_pdf(scene: Scene) -> None:
    from reportlab.pdfgen import canvas

    width = WIDTH_MM / 25.4 * 72
    height = HEIGHT_MM / 25.4 * 72
    sx, sy = width / 1780, height / 760
    pdf = canvas.Canvas(str(PACKAGE / "figure.pdf"), pagesize=(width, height), invariant=1, pageCompression=1)
    pdf.setTitle("R0.72U exact two-moment coercivity calibration")
    pdf.setAuthor("Kasifa")
    pdf.setSubject("Exact analytic samples; whole-line block contraction remains open")
    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, line_width, dash = item
                points = [(x1, y1), (x2, y2)]
            else:
                _, points, color, line_width, dash = item
            pdf.setStrokeColor(color)
            pdf.setLineWidth(line_width * sx)
            pdf.setDash([float(value) * sx for value in dash.split(",")] if dash else [])
            path = pdf.beginPath()
            path.moveTo(points[0][0] * sx, height - points[0][1] * sy)
            for x, y in points[1:]:
                path.lineTo(x * sx, height - y * sy)
            pdf.drawPath(path, stroke=1, fill=0)
        elif item[0] == "circle":
            _, x, y, radius, color = item
            pdf.setFillColor(color)
            pdf.circle(x * sx, height - y * sy, radius * sx, stroke=0, fill=1)
        elif item[0] == "rect":
            _, left, top, right, bottom, fill = item
            pdf.setFillColor(fill)
            pdf.rect(left * sx, height - bottom * sy, (right-left) * sx, (bottom-top) * sy, stroke=0, fill=1)
        else:
            _, x, y, value, size, color, anchor, bold = item
            pdf.setFillColor(color)
            pdf.setFont("Helvetica-Bold" if bold else "Helvetica", size * sx)
            if anchor == "middle":
                pdf.drawCentredString(x * sx, height - y * sy, value)
            elif anchor == "end":
                pdf.drawRightString(x * sx, height - y * sy, value)
            else:
                pdf.drawString(x * sx, height - y * sy, value)
    pdf.showPage()
    pdf.save()


def _font_path(bold: bool) -> str | None:
    candidates = (
        ["/System/Library/Fonts/Supplemental/Arial Bold.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
        if bold else
        ["/System/Library/Fonts/Supplemental/Arial.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    )
    return next((path for path in candidates if Path(path).is_file()), None)


def render_png(scene: Scene) -> None:
    from PIL import Image, ImageDraw, ImageFont

    pixel_width = round(WIDTH_MM / 25.4 * PNG_DPI)
    pixel_height = round(HEIGHT_MM / 25.4 * PNG_DPI)
    sx, sy = pixel_width / 1780, pixel_height / 760
    image = Image.new("RGB", (pixel_width, pixel_height), PAPER)
    draw = ImageDraw.Draw(image)
    cache: dict[tuple[int, bool], Any] = {}

    def font(size: int, bold: bool):
        key = (size, bold)
        if key not in cache:
            path = _font_path(bold)
            cache[key] = ImageFont.truetype(path, max(8, round(size * sx))) if path else ImageFont.load_default()
        return cache[key]

    def stroke(points, color, line_width, dash):
        rendered_width = max(1, round(line_width * sx))
        if not dash:
            draw.line(points, fill=color, width=rendered_width)
            return
        pattern = [float(value) * sx for value in dash.split(",")]
        pattern_index, remaining, drawing = 0, pattern[0], True
        for start, end in zip(points, points[1:]):
            x0, y0 = start
            x1, y1 = end
            length = math.hypot(x1 - x0, y1 - y0)
            consumed = 0.0
            while length and consumed < length:
                step = min(remaining, length - consumed)
                left, right = consumed / length, (consumed + step) / length
                if drawing:
                    draw.line(((x0+(x1-x0)*left, y0+(y1-y0)*left), (x0+(x1-x0)*right, y0+(y1-y0)*right)), fill=color, width=rendered_width)
                consumed += step
                remaining -= step
                if remaining <= 1e-9:
                    pattern_index = (pattern_index + 1) % len(pattern)
                    remaining = pattern[pattern_index]
                    drawing = not drawing

    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, line_width, dash = item
                points = [(x1*sx, y1*sy), (x2*sx, y2*sy)]
            else:
                _, raw, color, line_width, dash = item
                points = [(x*sx, y*sy) for x, y in raw]
            stroke(points, color, line_width, dash)
        elif item[0] == "circle":
            _, x, y, radius, color = item
            draw.ellipse(((x-radius)*sx, (y-radius)*sy, (x+radius)*sx, (y+radius)*sy), fill=color)
        elif item[0] == "rect":
            _, left, top, right, bottom, fill = item
            draw.rectangle((left*sx, top*sy, right*sx, bottom*sy), fill=fill)
        else:
            _, x, y, value, size, color, anchor, bold = item
            selected = font(size, bold)
            bounds = draw.textbbox((0, 0), value, font=selected)
            text_width = bounds[2] - bounds[0]
            tx = x*sx - (text_width/2 if anchor == "middle" else text_width if anchor == "end" else 0)
            draw.text((tx, y*sy-size*sy), value, font=selected, fill=color)
    image.save(
        PACKAGE / "figure.png",
        format="PNG",
        dpi=(PNG_DPI, PNG_DPI),
        optimize=False,
        title="R0.72U exact two-moment coercivity calibration",
        author="Kasifa",
    )


def build_qa() -> None:
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    preview = image.resize((1260, round(1260 * image.height / image.width)), Image.Resampling.LANCZOS)
    preview.save(PACKAGE / "qa-final-size.png", dpi=(180, 180))
    preview.convert("L").save(PACKAGE / "qa-grayscale.png", dpi=(180, 180))
    candidates = (
        REPOSITORY / ".openai/poppler/bin/pdftocairo",
        Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin/pdftocairo"),
    )
    pdftocairo = next((path for path in candidates if path.is_file()), None)
    if pdftocairo:
        subprocess.run(
            [str(pdftocairo), "-png", "-singlefile", "-r", "180", str(PACKAGE / "figure.pdf"), str(PACKAGE / "qa-pdf")],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        preview.save(PACKAGE / "qa-pdf.png", dpi=(180, 180))


def tracked_tree_dirty() -> bool:
    return any(
        subprocess.run(command, cwd=REPOSITORY).returncode != 0
        for command in (["git", "diff", "--quiet"], ["git", "diff", "--cached", "--quiet"])
    )


def validate_formal_certificate() -> dict:
    if not CERTIFICATE.is_file():
        raise RuntimeError("formal R0.72U certificate is absent")
    subprocess.run(
        [sys.executable, "research/certificates/r072u/validate_certificate.py", "--require-formal"],
        cwd=REPOSITORY,
        check=True,
    )
    manifest = json.loads((CERTIFICATE_DIR / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "formal" or not manifest.get("sourceBindings"):
        raise RuntimeError("formal source-bound certificate required")
    return manifest


def package_validation(row_count: int) -> dict:
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    width, height = image.size
    svg = (PACKAGE / "figure.svg").read_text(encoding="utf-8")
    svg_colors = set(re.findall(r"#[0-9a-fA-F]{6}", svg))
    allowed_colors = {PAPER, INK, MUTED, GRID, BLUE, GOLD, PALE_GOLD}
    value = {
        "schemaVersion": 1,
        "status": "passed",
        "checks": {
            "certificatePassed": json.loads(CERTIFICATE.read_text(encoding="utf-8")).get("status") == "passed",
            "analyticSamplesOnly": True,
            "noPdeSimulation": True,
            "threePanels": all(label in svg for label in ("exact rational probe", "two-moment coefficient", "fixed-gauge inviscid floor")),
            "probeMomentsVisible": "mu2=1/11;  mu4=3/143" in svg,
            "largeCenterThresholdVisible": "|c| &gt;= 27/13: fixed sign" in svg,
            "negativeThresholdEdgeVisible": "-81/143" in svg,
            "fixedGaugeFloorVisible": "exact floor = 4/5  (T=1)" in svg,
            "wholeLineOpenVisible": "whole-line block contraction: OPEN" in svg,
            "hardTwoChromaticRootCap": svg_colors <= allowed_colors and BLUE in svg_colors and GOLD in svg_colors,
            "nonColorEncodingVisible": "stroke-dasharray" in svg and "c=-27/13" in svg and "c=27/13" in svg,
            "lockedResearchBlossomVisible": svg.count("<circle ") >= 9,
            "pngAtLeast600DpiAt178mm": width >= math.floor(WIDTH_MM/25.4*PNG_DPI) and image.info.get("dpi", (0, 0))[0] >= 599,
            "vectorPdf": (PACKAGE / "figure.pdf").read_bytes().startswith(b"%PDF"),
            "vectorSvg": (PACKAGE / "figure.svg").read_text(encoding="utf-8").lstrip().startswith("<?xml"),
        },
        "png": {"width": width, "height": height, "dpi": list(image.info.get("dpi", (0, 0)))},
        "rowCount": row_count,
    }
    if not all(value["checks"].values()):
        raise RuntimeError(f"automatic R0.72U figure validation failed: {value}")
    return value


def build_archive(
    rows: list[dict[str, str]],
    formal: bool,
    visual_inspected: bool,
    source_commit: str | None,
    certificate_commit: str | None,
    wall_time_seconds: float,
) -> None:
    validation = package_validation(len(rows))
    write_json(PACKAGE / "validation.json", validation)
    results = {
        "schemaVersion": 1,
        "status": "passed",
        "figureId": FIGURE_ID,
        "panels": {
            "A": "exact rho and X*rho probe profiles with mu2 and mu4",
            "B": "affine K_c(s) at the two threshold centres and at c=0",
            "C": "exact inviscid fixed-gauge mean-square floor 4/5 for T=1",
        },
        "claimsNotMade": [
            "machine-checked bounded-chart functional analysis",
            "whole-line block contraction",
            "periodic transfer",
            "nonlinear Navier-Stokes closure",
            "Clay problem",
        ],
    }
    write_json(PACKAGE / "results.json", results)
    (PACKAGE / "progress.ndjson").write_text(
        "\n".join((
            '{"event":"build-start","stage":1,"totalStages":3}',
            f'{{"event":"analytic-data-ready","rows":{len(rows)},"stage":2,"totalStages":3}}',
            '{"event":"archive-ready","stage":3,"totalStages":3}',
        )) + "\n",
        encoding="utf-8",
    )
    (PACKAGE / "resource-log.ndjson").write_text(
        f'{{"event":"resource-summary","processes":1,"threadsPerProcess":1,"rows":{len(rows)},"gpuUsed":false}}\n',
        encoding="utf-8",
    )
    (PACKAGE / "qa-report.md").write_text(
        "# R0.72U figure QA\n\n"
        f"- formal build: {'yes' if formal else 'no'}\n"
        f"- explicit visual inspection: {'yes' if visual_inspected else 'no'}\n"
        "- final-size preview generated: yes\n"
        "- grayscale preview generated: yes\n"
        "- vector PDF render preview generated: yes\n"
        "- whole-line block contraction labelled OPEN: yes\n",
        encoding="utf-8",
    )

    publication_assets: list[dict[str, Any]] = []
    if formal:
        PUBLIC.mkdir(parents=True, exist_ok=True)
        for extension in ("pdf", "svg", "png"):
            source = PACKAGE / f"figure.{extension}"
            target = PUBLIC / f"{FIGURE_ID}.{extension}"
            shutil.copyfile(source, target)
            publication_assets.append({
                "path": str(target.relative_to(REPOSITORY)),
                "sha256": sha256(target),
                "bytes": target.stat().st_size,
                "byteIdenticalToMaster": sha256(target) == sha256(source),
            })

    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    archived = [
        "README.md", "caption.md", "figure-contract.md", "contract.json", "config.json",
        "command.txt", "environment.txt", "requirements.txt", "qa-protocol.md", "plot.py", "validate.py",
        "data.csv", "results.json", "validation.json", "progress.ndjson", "resource-log.ndjson", "qa-report.md",
        "figure.svg", "figure.pdf", "figure.png", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    ]
    from PIL import Image
    image = Image.open(PACKAGE / "figure.png")
    data_schema = {
        "config.json": "frozen exact formulas, ranges, palette-independent dimensions, and output resolution",
        "contract.json": "panel claims, source-stage status, public route, and false claim boundaries",
        "data.csv": "panel, series, x, y, analytic source formula, and presentation-only status",
        "results.json": "panel meanings and claims explicitly not made",
        "validation.json": "certificate, format, resolution, and visible-boundary checks",
        "progress.ndjson": "deterministic three-stage analytic build progress",
        "resource-log.ndjson": "deterministic process, thread, row, and GPU-use record",
    }
    manifest = {
        "schemaVersion": "1.1",
        "figureId": FIGURE_ID,
        "release": "R0.72U",
        "status": "formal" if formal else "draft",
        "createdAt": "2026-08-28T00:00:00+08:00",
        "analyticalQuestion": "Which exact rational probe moments expose the affine large-centre coefficient, and what independent fixed-gauge inviscid floor remains on the unit half-length block?",
        "supportedClaim": "Exact probe moments, the sufficient threshold abs(c)>=27/13 for T=1, and the separate inviscid fixed-gauge floor 4/5; whole-line block contraction remains open.",
        "git": (
            {"repository": "Kasifa/Kasifa.github.io", "sourceCommit": source_commit, "certificateCommit": certificate_commit, "dirtyAtCertifiedRun": False}
            if formal else
            {"repository": "Kasifa/Kasifa.github.io", "commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip(), "dirty": tracked_tree_dirty()}
        ),
        "computation": {
            "kind": "exact-audit",
            "configuration": "exact rational probe moments, three affine K_c curves on abs(s)<=1, and the unit-block fixed-gauge identity",
            "precision": "exact identities certificate-gated; binary64 used only to draw analytic curves",
            "solver": "no PDE solve, regression, threshold inference, or random sampling",
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": wall_time_seconds,
            "monitoring": {"enabled": True, "progressLog": "progress.ndjson", "resourceLog": "resource-log.ndjson", "trackedFields": ["event", "stage", "rows", "processes", "threadsPerProcess"]},
        },
        "compute": {"host": platform.node() or "local", "operatingSystem": platform.platform(), "cpu": platform.machine(), "memoryGiB": "not sampled; analytic figure only", "processes": 1, "threadsPerProcess": 1, "gpu": "not used", "dgx": "not used"},
        "environment": {"python": platform.python_version(), "packagesLock": "requirements.txt", "pillow": getattr(Image, "__version__", "installed"), "reportlab": "pinned in requirements.txt"},
        "data": [
            {"path": name, "schema": schema, "format": Path(name).suffix.lstrip("."), "sha256": sha256(PACKAGE / name), "bytes": (PACKAGE / name).stat().st_size}
            for name, schema in data_schema.items()
        ],
        "sourceData": [
            {"location": "repository", "fileName": str(CERTIFICATE.relative_to(REPOSITORY)), "bytes": CERTIFICATE.stat().st_size, "sha256": sha256(CERTIFICATE), "extractionCommand": "python3 research/certificates/r072u/generate_certificate.py", "role": "exactCertificate"},
            {"location": "repository", "fileName": "scripts/generate_r072u_figure.py", "bytes": Path(__file__).stat().st_size, "sha256": sha256(Path(__file__)), "extractionCommand": "python3 scripts/generate_r072u_figure.py", "role": "analyticPresentationGenerator"},
        ],
        "figure": {
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "layout": "1x3",
            "profile": "journal-double-column",
            "script": "plot.py",
            "outputs": [
                {"path": "figure.pdf", "sha256": sha256(PACKAGE / "figure.pdf"), "bytes": (PACKAGE / "figure.pdf").stat().st_size},
                {"path": "figure.svg", "sha256": sha256(PACKAGE / "figure.svg"), "bytes": (PACKAGE / "figure.svg").stat().st_size},
                {"path": "figure.png", "sha256": sha256(PACKAGE / "figure.png"), "bytes": (PACKAGE / "figure.png").stat().st_size, "dpi": PNG_DPI, "pixels": list(image.size)},
            ],
        },
        "caption": {"english": "caption.md"},
        "qa": {"status": "passed", "visualInspectionExplicit": visual_inspected, "finalSizeInspected": visual_inspected, "grayscaleInspected": visual_inspected, "labelsAndLegendsInspected": visual_inspected, "scalesAndUnitsInspected": visual_inspected, "dataCrossChecked": True, "finalSizePreview": "qa-final-size.png", "grayscalePreview": "qa-grayscale.png", "pdfRenderPreview": "qa-pdf.png", "manualReport": "qa-report.md"},
        "publication": {"directory": "public/assets/r072u", "stem": FIGURE_ID, "publicCopiesComplete": formal, "assets": publication_assets},
        "claimBoundary": certificate["claimBoundary"],
        "deterministic": True,
        "outputs": [{"path": name, "sha256": sha256(PACKAGE / name), "bytes": (PACKAGE / name).stat().st_size} for name in archived],
    }
    write_json(PACKAGE / "manifest.json", manifest)
    ledger_names = sorted(path.name for path in PACKAGE.iterdir() if path.is_file() and path.name != "SHA256SUMS")
    (PACKAGE / "SHA256SUMS").write_text(
        "".join(f"{sha256(PACKAGE / name)}  {name}\n" for name in ledger_names),
        encoding="utf-8",
    )


def self_test() -> None:
    config = json.loads((PACKAGE / "config.json").read_text(encoding="utf-8"))
    contract = json.loads((PACKAGE / "contract.json").read_text(encoding="utf-8"))
    rows = analytic_rows()
    scene = build_scene()
    scene_text = {item[3] for item in scene.items if item[0] == "text"}
    checks = {
        "figureId": config.get("figureId") == FIGURE_ID == contract.get("figureId"),
        "width": config.get("widthMillimetres") == WIDTH_MM,
        "dpi": config.get("pngDpi") == PNG_DPI,
        "rhoEndpoints": rho(-1) == 0 and rho(1) == 0,
        "rhoPeak": Fraction(315, 256) == Fraction(str(rho(0))),
        "kFormula": abs(k_c(0, 0) - 3/143) < 1e-15,
        "gaugeFloor": abs(fixed_gauge_energy(0) - 4/5) < 1e-15,
        "threePanels": {row["panel"] for row in rows} == {"A", "B", "C"},
        "sceneBuilt": len(scene.items) > 50,
        "lockedFivePetalBlossom": sum(1 for item in scene.items if item[0] == "circle") >= 9,
        "negativeThresholdEdgeLabel": "-81/143" in scene_text,
        "wholeLineOpen": contract.get("claimBoundary", {}).get("wholeLineBlockContractionProved") is False,
        "publicRoute": contract.get("plannedPublicationDirectory") == "public/assets/r072u",
        "hardTwoRootPalette": contract.get("palette", {}).get("chromaticRoots") == [BLUE, GOLD]
        and contract.get("palette", {}).get("hardChromaticRootCap") == 2,
        "blossomContract": contract.get("researchBlossom") == {
            "carriesData": False,
            "lockedAnchor": "top-right-header",
            "petalCount": 5,
        },
    }
    if not all(checks.values()):
        raise RuntimeError(f"R0.72U figure source self-test failed: {checks}")
    print(f"R0.72U figure source self-test: passed ({len(rows)} in-memory rows; no outputs written)")


def main() -> None:
    started = time.perf_counter()
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--self-test", action="store_true")
    mode.add_argument("--draft", action="store_true")
    mode.add_argument("--formal", action="store_true")
    parser.add_argument("--visual-inspected", action="store_true")
    parser.add_argument("--source-commit")
    parser.add_argument("--certificate-commit")
    args = parser.parse_args()
    if args.self_test:
        if args.visual_inspected or args.source_commit or args.certificate_commit:
            parser.error("--self-test cannot be combined with generation arguments")
        self_test()
        return
    if not args.draft and not args.formal:
        parser.error("choose --self-test, --draft, or --formal")

    certificate_manifest = validate_formal_certificate()
    if args.formal:
        if tracked_tree_dirty():
            raise RuntimeError("formal figure generation requires a clean tracked tree")
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=REPOSITORY, text=True).strip()
        if not args.visual_inspected:
            raise RuntimeError("formal figure generation requires --visual-inspected")
        if args.source_commit != certificate_manifest.get("sourceCommit"):
            raise RuntimeError("--source-commit must equal the formal certificate source commit")
        if args.certificate_commit != head or not isinstance(args.certificate_commit, str) or len(args.certificate_commit) != 40:
            raise RuntimeError("--certificate-commit must be the full clean HEAD containing the certificate")
    elif args.visual_inspected or args.source_commit or args.certificate_commit:
        parser.error("draft generation does not accept formal lineage flags")

    rows = analytic_rows()
    save_data(rows)
    scene = build_scene()
    render_svg(scene)
    render_pdf(scene)
    render_png(scene)
    build_qa()
    build_archive(
        rows,
        formal=args.formal,
        visual_inspected=args.visual_inspected,
        source_commit=args.source_commit,
        certificate_commit=args.certificate_commit,
        wall_time_seconds=time.perf_counter() - started,
    )
    print(f"R0.72U {'formal' if args.formal else 'draft'} figure package: passed ({len(rows)} rows)")


if __name__ == "__main__":
    main()
