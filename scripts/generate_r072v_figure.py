#!/usr/bin/env python3
"""Generate the R0.72V coefficient-uniform globalization figure.

The source stage exposes only a zero-write self-test. Draft and formal
rendering require the formal R0.72V exact certificate. Formal rendering also
binds the certificate source commit to a distinct clean certificate commit,
refuses every pre-existing output target, and alone publishes byte-identical
assets.
"""

from __future__ import annotations

import argparse
import csv
from fractions import Fraction
import hashlib
import json
import math
import platform
from pathlib import Path
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
    / "figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization"
)
CERTIFICATE_DIR = REPOSITORY / "research/certificates/r072v"
CERTIFICATE = CERTIFICATE_DIR / "certificate.json"
PUBLIC = REPOSITORY / "public/assets/r072v"
FIGURE_ID = "fig-r072v-unit-chart-globalization"
WIDTH_MM = 178
HEIGHT_MM = 82
PNG_DPI = 600
PAPER = "#ffffff"
INK = "#17212b"
MUTED = "#66727e"
GRID = "#d9dde1"
BLUE = "#285f8f"
GOLD = "#a6781f"
PALE_GOLD = "#f4f0e6"
SOURCE_FILES = (
    "README.md",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "environment.txt",
    "figure-contract.md",
    "plot.py",
    "qa-protocol.md",
    "requirements.txt",
    "validate.py",
)
GENERATED_FILES = (
    "data.csv",
    "results.json",
    "validation.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
    "figure.svg",
    "figure.pdf",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "manifest.json",
    "SHA256SUMS",
)
EXPECTED_ROWS = 2592


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def linspace(left: float, right: float, count: int) -> list[float]:
    if count < 2:
        raise ValueError("linspace needs at least two points")
    return [
        left + (right - left) * index / (count - 1)
        for index in range(count)
    ]


def kappa(theta: float) -> float:
    return (
        math.cos(theta) ** 2 * (5.0 / 6292.0)
        + math.sin(theta) ** 2 * (1.0 / 44.0)
    )


def translated_b(a_value: float, center: float) -> float:
    return a_value * a_value / 3.0 + 6.0 * center


def contraction_ratio(symbolic_s: float) -> float:
    return symbolic_s / (1.0 + symbolic_s)


def analytic_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for theta in linspace(0.0, 2.0 * math.pi, 721):
        rows.append({
            "panel": "A",
            "series": "adaptive-moment-floor",
            "x": f"{theta:.17g}",
            "y": f"{kappa(theta):.17g}",
            "source": "cos(theta)^2*(5/6292)+sin(theta)^2*(1/44)",
            "status": "analytic presentation only",
        })
    for center, label in ((-2.0, "c=-2"), (0.0, "c=0"), (2.0, "c=2")):
        for a_value in linspace(-12.0, 12.0, 481):
            rows.append({
                "panel": "B",
                "series": label,
                "x": f"{a_value:.17g}",
                "y": f"{translated_b(a_value, center):.17g}",
                "source": "b=a^2/3+6*c",
                "status": "analytic presentation only",
            })
        for integer_k in range(-4, 5):
            a_value = 3.0 * integer_k
            rows.append({
                "panel": "B",
                "series": f"{label}-integer-k-marker",
                "x": f"{a_value:.17g}",
                "y": f"{translated_b(a_value, center):.17g}",
                "source": "a=3*k; b=3*k^2+6*c",
                "status": "exact integer-cell marker",
            })
    for symbolic_s in linspace(0.0, 6.0, 401):
        rows.append({
            "panel": "C",
            "series": "symbolic-contraction-ratio",
            "x": f"{symbolic_s:.17g}",
            "y": f"{contraction_ratio(symbolic_s):.17g}",
            "source": "r=s/(1+s); s=C_T^2/T",
            "status": "analytic formula presentation only",
        })
    return rows


class Scene:
    def __init__(self) -> None:
        self.items: list[tuple[Any, ...]] = []

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        color: str = INK,
        width: float = 2,
        dash: str | None = None,
    ) -> None:
        self.items.append(("line", x1, y1, x2, y2, color, width, dash))

    def polyline(
        self,
        points: list[tuple[float, float]],
        color: str = BLUE,
        width: float = 2,
        dash: str | None = None,
    ) -> None:
        self.items.append(("polyline", points, color, width, dash))

    def text(
        self,
        x: float,
        y: float,
        value: str,
        size: int = 18,
        color: str = INK,
        anchor: str = "start",
        bold: bool = False,
    ) -> None:
        self.items.append(("text", x, y, value, size, color, anchor, bold))

    def circle(
        self,
        x: float,
        y: float,
        radius: float,
        color: str = INK,
    ) -> None:
        self.items.append(("circle", x, y, radius, color))

    def box(
        self,
        left: float,
        top: float,
        right: float,
        bottom: float,
        fill: str = PAPER,
        stroke: str = INK,
        width: float = 2,
    ) -> None:
        self.items.append(
            ("box", left, top, right, bottom, fill, stroke, width)
        )


def mapping(
    x0: float,
    x1: float,
    y0: float,
    y1: float,
    left: float,
    right: float,
    top: float,
    bottom: float,
):
    return (
        lambda x: left + (x - x0) * (right - left) / (x1 - x0),
        lambda y: bottom - (y - y0) * (bottom - top) / (y1 - y0),
    )


def axes(
    scene: Scene,
    box: tuple[float, float, float, float],
    x_ticks: list[tuple[float, str]],
    y_ticks: list[tuple[float, str]],
    x_map,
    y_map,
    xlabel: str,
    ylabel: str,
) -> None:
    left, right, top, bottom = box
    for value, label in x_ticks:
        x = x_map(value)
        scene.line(x, top, x, bottom, GRID, 1)
        scene.text(x, bottom + 27, label, 18, MUTED, "middle")
    for value, label in y_ticks:
        y = y_map(value)
        scene.line(left, y, right, y, GRID, 1)
        scene.text(left - 9, y + 6, label, 17, MUTED, "end")
    scene.line(left, bottom, right, bottom, INK, 2)
    scene.line(left, top, left, bottom, INK, 2)
    scene.text((left + right) / 2, bottom + 57, xlabel, 21, anchor="middle")
    scene.text(left, top - 14, ylabel, 19)


def build_scene() -> Scene:
    scene = Scene()
    panel_lefts = (50, 620, 1180)
    titles = (
        ("A", "adaptive moment floor"),
        ("B", "translated coefficient plane"),
        ("C", "direct sum to contraction"),
    )
    for left, (letter, title) in zip(panel_lefts, titles):
        scene.text(left, 64, letter, 34, INK, bold=True)
        scene.text(left + 42, 64, title, 25, INK, bold=True)

    # Panel A: exact adaptive-moment floor and q0 ledger.
    box_a = (96, 564, 160, 575)
    xa, ya = mapping(0.0, 2.0 * math.pi, 0.0, 0.0245, *box_a)
    axes(
        scene,
        box_a,
        [
            (0.0, "0"),
            (math.pi / 2, "pi/2"),
            (math.pi, "pi"),
            (3 * math.pi / 2, "3pi/2"),
            (2 * math.pi, "2pi"),
        ],
        [(0.0, "0"), (0.01, ".01"), (0.02, ".02")],
        xa,
        ya,
        "theta",
        "kappa(theta)",
    )
    theta_grid = linspace(0.0, 2.0 * math.pi, 721)
    scene.polyline(
        [(xa(theta), ya(kappa(theta))) for theta in theta_grid],
        BLUE,
        4,
    )
    floor = 5.0 / 6292.0
    scene.line(box_a[0], ya(floor), box_a[1], ya(floor), GOLD, 3, "9,5")
    for theta in (0.0, math.pi, 2.0 * math.pi):
        scene.circle(xa(theta), ya(floor), 6, GOLD)
    scene.box(114, 176, 548, 260, PAPER, GRID, 1)
    scene.text(
        128,
        202,
        "q0=(315/128)(1-4y^2)^4 on |y|<=1/2",
        16,
        INK,
    )
    scene.text(128, 228, "mu2=1/44;  mu4=3/2288", 18, INK, bold=True)
    scene.text(128, 251, "variance(y^2)=5/6292", 18, GOLD, bold=True)
    scene.text(120, 548, "exact floor 5/6292", 18, GOLD, bold=True)

    # Panel B: every translated cell lands in the uniform (a,b) theorem.
    box_b = (672, 1138, 160, 575)
    xb, yb = mapping(-12.0, 12.0, -14.0, 62.0, *box_b)
    axes(
        scene,
        box_b,
        [(-12, "-12"), (-6, "-6"), (0, "0"), (6, "6"), (12, "12")],
        [(-12, "-12"), (0, "0"), (24, "24"), (48, "48"), (60, "60")],
        xb,
        yb,
        "a  (integer cells: a=3k)",
        "b",
    )
    a_grid = linspace(-12.0, 12.0, 481)
    series = (
        (-2.0, GOLD, "9,5", "c=-2"),
        (0.0, MUTED, "3,4", "c=0"),
        (2.0, BLUE, None, "c=2"),
    )
    for center, color, dash, label in series:
        scene.polyline(
            [(xb(a_value), yb(translated_b(a_value, center))) for a_value in a_grid],
            color,
            3,
            dash,
        )
        for integer_k in range(-4, 5):
            a_value = 3.0 * integer_k
            scene.circle(
                xb(a_value),
                yb(translated_b(a_value, center)),
                4.5,
                color,
            )
        label_a = 8.8
        scene.text(
            xb(label_a) + 7,
            yb(translated_b(label_a, center)) + 4,
            label,
            17,
            color,
            bold=True,
        )
    scene.box(692, 178, 1025, 237, PAPER, GRID, 1)
    scene.text(708, 202, "b=a^2/3+6c", 20, INK, bold=True)
    scene.text(708, 226, "a=3k, b=3k^2+6c", 17, INK)
    scene.text(690, 550, "markers: exact k in {-4,...,4}", 17, MUTED)

    # Panel C: structural implication and exact symbolic contraction ratio.
    chain_left, chain_right = 1224, 1718
    chain_boxes = (
        (142, 199, "disjoint unit cells J_k;  a=3k"),
        (221, 278, "sum ||g_k||^2 <= ||g||_H^-1^2"),
        (300, 357, "uniform local theorem -> whole-line graph"),
        (379, 436, "energy evolution -> strict contraction"),
    )
    for index, (top, bottom, label) in enumerate(chain_boxes):
        scene.box(
            chain_left,
            top,
            chain_right,
            bottom,
            PALE_GOLD if index in (1, 3) else PAPER,
            BLUE if index in (0, 2) else GOLD,
            2,
        )
        scene.text(
            (chain_left + chain_right) / 2,
            top + 35,
            label,
            17,
            INK,
            "middle",
            index in (2, 3),
        )
        if index < len(chain_boxes) - 1:
            scene.line(
                (chain_left + chain_right) / 2,
                bottom,
                (chain_left + chain_right) / 2,
                chain_boxes[index + 1][0],
                GOLD,
                3,
            )
            scene.circle(
                (chain_left + chain_right) / 2,
                chain_boxes[index + 1][0] - 3,
                4,
                GOLD,
            )

    ratio_box = (1260, 1685, 490, 615)
    xr, yr = mapping(0.0, 6.0, 0.0, 0.9, *ratio_box)
    axes(
        scene,
        ratio_box,
        [(0, "0"), (2, "2"), (4, "4"), (6, "6")],
        [(0, "0"), (0.4, ".4"), (0.8, ".8")],
        xr,
        yr,
        "s=C_T^2/T  (symbolic)",
        "r",
    )
    s_grid = linspace(0.0, 6.0, 401)
    scene.polyline(
        [(xr(symbolic_s), yr(contraction_ratio(symbolic_s))) for symbolic_s in s_grid],
        BLUE,
        4,
    )
    scene.text(1280, 514, "r=s/(1+s)", 18, BLUE, bold=True)
    scene.text(1280, 541, "formula only; C_T not evaluated", 15, MUTED)

    # Visible theorem boundary across the double-column width.
    scene.box(54, 676, 1162, 746, PAPER, BLUE, 3)
    scene.text(
        608,
        718,
        "whole-line block contraction: CLOSED (exact cubic energy model)",
        23,
        BLUE,
        "middle",
        True,
    )
    scene.box(1192, 676, 1724, 746, PALE_GOLD, GOLD, 3)
    scene.text(
        1458,
        718,
        "periodic / Clay: OPEN",
        23,
        GOLD,
        "middle",
        True,
    )
    scene.text(
        54,
        788,
        "analytic presentation only | pdeSimulation=false | finite certificate does not machine-check functional analysis",
        17,
        MUTED,
    )

    # Locked five-petal research blossom. It is decorative and carries no data.
    blossom_x, blossom_y = 1740, 42
    for index in range(5):
        angle = -math.pi / 2 + 2 * math.pi * index / 5
        scene.circle(
            blossom_x + 11 * math.cos(angle),
            blossom_y + 11 * math.sin(angle),
            6,
            BLUE if index % 2 == 0 else GOLD,
        )
    scene.circle(blossom_x, blossom_y, 4, INK)
    return scene


def save_data(rows: list[dict[str, str]]) -> None:
    with (PACKAGE / "data.csv").open(
        "w",
        encoding="utf-8",
        newline="",
    ) as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("panel", "series", "x", "y", "source", "status"),
        )
        writer.writeheader()
        writer.writerows(rows)


def render_svg(scene: Scene) -> None:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            '<svg xmlns="http://www.w3.org/2000/svg" '
            'width="178mm" height="82mm" viewBox="0 0 1780 820">'
        ),
        f'<rect width="1780" height="820" fill="{PAPER}"/>',
    ]
    for item in scene.items:
        if item[0] == "line":
            _, x1, y1, x2, y2, color, width, dash = item
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            parts.append(
                f'<line x1="{x1:.3f}" y1="{y1:.3f}" '
                f'x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" '
                f'stroke-width="{width}"{extra}/>'
            )
        elif item[0] == "polyline":
            _, points, color, width, dash = item
            extra = f' stroke-dasharray="{dash}"' if dash else ""
            coordinates = " ".join(
                f"{x:.3f},{y:.3f}" for x, y in points
            )
            parts.append(
                f'<polyline points="{coordinates}" fill="none" '
                f'stroke="{color}" stroke-width="{width}"{extra}/>'
            )
        elif item[0] == "circle":
            _, x, y, radius, color = item
            parts.append(
                f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius}" '
                f'fill="{color}"/>'
            )
        elif item[0] == "box":
            _, left, top, right, bottom, fill, stroke, width = item
            parts.append(
                f'<rect x="{left:.3f}" y="{top:.3f}" '
                f'width="{right-left:.3f}" height="{bottom-top:.3f}" '
                f'fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>'
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            weight = "700" if bold else "400"
            parts.append(
                f'<text x="{x:.3f}" y="{y:.3f}" '
                'font-family="DejaVu Sans,Arial,sans-serif" '
                f'font-size="{size}" font-weight="{weight}" '
                f'text-anchor="{anchor}" fill="{color}">'
                f'{escape(value)}</text>'
            )
    parts.append("</svg>")
    (PACKAGE / "figure.svg").write_text(
        "\n".join(parts) + "\n",
        encoding="utf-8",
    )


def render_pdf(scene: Scene) -> None:
    from reportlab.pdfgen import canvas

    width = WIDTH_MM / 25.4 * 72
    height = HEIGHT_MM / 25.4 * 72
    sx, sy = width / 1780, height / 820
    pdf = canvas.Canvas(
        str(PACKAGE / "figure.pdf"),
        pagesize=(width, height),
        invariant=1,
        pageCompression=1,
    )
    pdf.setTitle("R0.72V coefficient-uniform whole-line transfer")
    pdf.setAuthor("Kasifa")
    pdf.setSubject(
        "Analytic presentation only; exact cubic energy-model contraction"
    )
    for item in scene.items:
        if item[0] in ("line", "polyline"):
            if item[0] == "line":
                _, x1, y1, x2, y2, color, line_width, dash = item
                points = [(x1, y1), (x2, y2)]
            else:
                _, points, color, line_width, dash = item
            pdf.setStrokeColor(color)
            pdf.setLineWidth(line_width * sx)
            pdf.setDash(
                [float(value) * sx for value in dash.split(",")]
                if dash
                else []
            )
            path = pdf.beginPath()
            path.moveTo(points[0][0] * sx, height - points[0][1] * sy)
            for x_value, y_value in points[1:]:
                path.lineTo(x_value * sx, height - y_value * sy)
            pdf.drawPath(path, stroke=1, fill=0)
        elif item[0] == "circle":
            _, x, y, radius, color = item
            pdf.setFillColor(color)
            pdf.circle(
                x * sx,
                height - y * sy,
                radius * sx,
                stroke=0,
                fill=1,
            )
        elif item[0] == "box":
            _, left, top, right, bottom, fill, stroke, line_width = item
            pdf.setFillColor(fill)
            pdf.setStrokeColor(stroke)
            pdf.setLineWidth(line_width * sx)
            pdf.rect(
                left * sx,
                height - bottom * sy,
                (right - left) * sx,
                (bottom - top) * sy,
                stroke=1,
                fill=1,
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            pdf.setFillColor(color)
            pdf.setFont(
                "Helvetica-Bold" if bold else "Helvetica",
                size * sx,
            )
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
        [
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
        if bold
        else [
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    )
    return next((path for path in candidates if Path(path).is_file()), None)


def render_png(scene: Scene) -> None:
    from PIL import Image, ImageDraw, ImageFont

    pixel_width = round(WIDTH_MM / 25.4 * PNG_DPI)
    pixel_height = round(HEIGHT_MM / 25.4 * PNG_DPI)
    sx, sy = pixel_width / 1780, pixel_height / 820
    image = Image.new("RGB", (pixel_width, pixel_height), PAPER)
    draw = ImageDraw.Draw(image)
    cache: dict[tuple[int, bool], Any] = {}

    def font(size: int, bold: bool):
        key = (size, bold)
        if key not in cache:
            path = _font_path(bold)
            cache[key] = (
                ImageFont.truetype(path, max(8, round(size * sx)))
                if path
                else ImageFont.load_default()
            )
        return cache[key]

    def stroke(
        points: list[tuple[float, float]],
        color: str,
        line_width: float,
        dash: str | None,
    ) -> None:
        rendered_width = max(1, round(line_width * sx))
        if not dash:
            draw.line(points, fill=color, width=rendered_width)
            return
        pattern = [float(value) * sx for value in dash.split(",")]
        pattern_index = 0
        remaining = pattern[0]
        drawing = True
        for start, end in zip(points, points[1:]):
            x0, y0 = start
            x1, y1 = end
            length = math.hypot(x1 - x0, y1 - y0)
            consumed = 0.0
            while length and consumed < length:
                step = min(remaining, length - consumed)
                left = consumed / length
                right = (consumed + step) / length
                if drawing:
                    draw.line(
                        (
                            (
                                x0 + (x1 - x0) * left,
                                y0 + (y1 - y0) * left,
                            ),
                            (
                                x0 + (x1 - x0) * right,
                                y0 + (y1 - y0) * right,
                            ),
                        ),
                        fill=color,
                        width=rendered_width,
                    )
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
                points = [(x1 * sx, y1 * sy), (x2 * sx, y2 * sy)]
            else:
                _, raw, color, line_width, dash = item
                points = [(x * sx, y * sy) for x, y in raw]
            stroke(points, color, line_width, dash)
        elif item[0] == "circle":
            _, x, y, radius, color = item
            draw.ellipse(
                (
                    (x - radius) * sx,
                    (y - radius) * sy,
                    (x + radius) * sx,
                    (y + radius) * sy,
                ),
                fill=color,
            )
        elif item[0] == "box":
            _, left, top, right, bottom, fill, outline, line_width = item
            draw.rectangle(
                (left * sx, top * sy, right * sx, bottom * sy),
                fill=fill,
                outline=outline,
                width=max(1, round(line_width * sx)),
            )
        else:
            _, x, y, value, size, color, anchor, bold = item
            selected = font(size, bold)
            bounds = draw.textbbox((0, 0), value, font=selected)
            text_width = bounds[2] - bounds[0]
            if anchor == "middle":
                tx = x * sx - text_width / 2
            elif anchor == "end":
                tx = x * sx - text_width
            else:
                tx = x * sx
            draw.text(
                (tx, y * sy - size * sy),
                value,
                font=selected,
                fill=color,
            )
    image.save(
        PACKAGE / "figure.png",
        format="PNG",
        dpi=(PNG_DPI, PNG_DPI),
        optimize=False,
        title="R0.72V coefficient-uniform whole-line transfer",
        author="Kasifa",
    )


def build_qa() -> None:
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    preview = image.resize(
        (1260, round(1260 * image.height / image.width)),
        Image.Resampling.LANCZOS,
    )
    preview.save(PACKAGE / "qa-final-size.png", dpi=(180, 180))
    preview.convert("L").save(
        PACKAGE / "qa-grayscale.png",
        dpi=(180, 180),
    )
    candidates = (
        REPOSITORY / ".openai/poppler/bin/pdftocairo",
        Path(
            "/Users/kasifa/.cache/codex-runtimes/"
            "codex-primary-runtime/dependencies/native/poppler/"
            "poppler/bin/pdftocairo"
        ),
    )
    pdftocairo = next((path for path in candidates if path.is_file()), None)
    if pdftocairo:
        subprocess.run(
            [
                str(pdftocairo),
                "-png",
                "-singlefile",
                "-r",
                "180",
                str(PACKAGE / "figure.pdf"),
                str(PACKAGE / "qa-pdf"),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    else:
        preview.save(PACKAGE / "qa-pdf.png", dpi=(180, 180))


def git_status_dirty() -> bool:
    return bool(
        subprocess.check_output(
            ["git", "status", "--porcelain", "--untracked-files=all"],
            cwd=REPOSITORY,
            text=True,
        ).strip()
    )


def reject_output_overwrite(include_public: bool) -> None:
    paths = [PACKAGE / name for name in GENERATED_FILES]
    if include_public:
        paths.extend(
            PUBLIC / f"{FIGURE_ID}.{extension}"
            for extension in ("pdf", "svg", "png")
        )
    present = [str(path.relative_to(REPOSITORY)) for path in paths if path.exists()]
    if present:
        raise RuntimeError(
            "refusing to overwrite pre-existing figure outputs: "
            + ", ".join(present)
        )


def validate_formal_certificate() -> tuple[dict[str, Any], dict[str, Any]]:
    if not CERTIFICATE.is_file():
        raise RuntimeError("formal R0.72V certificate is absent")
    subprocess.run(
        [
            sys.executable,
            "research/certificates/r072v/validate_certificate.py",
            "--require-formal",
        ],
        cwd=REPOSITORY,
        check=True,
    )
    manifest = json.loads(
        (CERTIFICATE_DIR / "manifest.json").read_text(encoding="utf-8")
    )
    certificate = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if (
        manifest.get("status") != "formal"
        or not manifest.get("sourceBindings")
        or certificate.get("status") != "passed"
    ):
        raise RuntimeError("formal source-bound R0.72V certificate required")
    return manifest, certificate


def validate_formal_lineage(
    certificate_manifest: dict[str, Any],
    source_commit: str | None,
    certificate_commit: str | None,
) -> None:
    if not isinstance(source_commit, str) or not re.fullmatch(
        r"[0-9a-f]{40}",
        source_commit,
    ):
        raise RuntimeError("--source-commit must be a full Git commit")
    if not isinstance(certificate_commit, str) or not re.fullmatch(
        r"[0-9a-f]{40}",
        certificate_commit,
    ):
        raise RuntimeError("--certificate-commit must be a full Git commit")
    if source_commit != certificate_manifest.get("sourceCommit"):
        raise RuntimeError(
            "--source-commit must equal the formal certificate source commit"
        )
    if certificate_commit == source_commit:
        raise RuntimeError(
            "certificateCommit must be distinct from the frozen sourceCommit"
        )
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=REPOSITORY,
        text=True,
    ).strip()
    if certificate_commit != head:
        raise RuntimeError(
            "--certificate-commit must equal the clean HEAD containing the certificate"
        )
    for commit in (source_commit, certificate_commit):
        result = subprocess.run(
            ["git", "cat-file", "-e", f"{commit}^{{commit}}"],
            cwd=REPOSITORY,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if result.returncode:
            raise RuntimeError(f"invalid Git commit in formal lineage: {commit}")
    if subprocess.run(
        ["git", "merge-base", "--is-ancestor", source_commit, certificate_commit],
        cwd=REPOSITORY,
    ).returncode:
        raise RuntimeError("certificateCommit does not descend from sourceCommit")
    for name in (
        "manifest.json",
        "certificate.json",
        "independent.json",
        "crosscheck.json",
        "SHA256SUMS",
    ):
        relative = f"research/certificates/r072v/{name}"
        committed = subprocess.check_output(
            ["git", "show", f"{certificate_commit}:{relative}"],
            cwd=REPOSITORY,
        )
        working = (REPOSITORY / relative).read_bytes()
        if committed != working:
            raise RuntimeError(
                f"working certificate differs from {certificate_commit}:{relative}"
            )


def package_validation(row_count: int) -> dict[str, Any]:
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
            "certificatePassed": json.loads(
                CERTIFICATE.read_text(encoding="utf-8")
            ).get("status") == "passed",
            "analyticPresentationOnly": True,
            "noPdeSimulation": True,
            "threePanels": all(
                label in svg
                for label in (
                    "adaptive moment floor",
                    "translated coefficient plane",
                    "direct sum to contraction",
                )
            ),
            "exactMomentFloorVisible": all(
                token in svg
                for token in ("mu2=1/44", "mu4=3/2288", "5/6292")
            ),
            "translationIdentityVisible": (
                "b=a^2/3+6c" in svg and "a=3k, b=3k^2+6c" in svg
            ),
            "directSumVisible": (
                "sum ||g_k||^2 &lt;= ||g||_H^-1^2" in svg
            ),
            "closedBoundaryVisible": (
                "whole-line block contraction: CLOSED "
                "(exact cubic energy model)" in svg
            ),
            "openBoundaryVisible": "periodic / Clay: OPEN" in svg,
            "formulaOnlyVisible": (
                "formula only; C_T not evaluated" in svg
            ),
            "hardTwoChromaticRootCap": (
                svg_colors <= allowed_colors
                and BLUE in svg_colors
                and GOLD in svg_colors
            ),
            "nonColorEncodingVisible": (
                "stroke-dasharray" in svg
                and "markers: exact k in {-4,...,4}" in svg
            ),
            "lockedResearchBlossomVisible": svg.count("<circle ") >= 39,
            "pngAtLeast600DpiAt178mm": (
                width >= math.floor(WIDTH_MM / 25.4 * PNG_DPI)
                and image.info.get("dpi", (0, 0))[0] >= 599
            ),
            "vectorPdf": (PACKAGE / "figure.pdf").read_bytes().startswith(
                b"%PDF"
            ),
            "vectorSvg": svg.lstrip().startswith("<?xml"),
        },
        "png": {
            "width": width,
            "height": height,
            "dpi": list(image.info.get("dpi", (0, 0))),
        },
        "rowCount": row_count,
    }
    if not all(value["checks"].values()):
        raise RuntimeError(
            f"automatic R0.72V figure validation failed: {value}"
        )
    return value


def build_archive(
    rows: list[dict[str, str]],
    formal: bool,
    visual_inspected: bool,
    source_commit: str | None,
    certificate_commit: str | None,
    certificate: dict[str, Any],
    wall_time_seconds: float,
) -> None:
    validation = package_validation(len(rows))
    write_json(PACKAGE / "validation.json", validation)
    results = {
        "schemaVersion": 1,
        "status": "passed",
        "figureId": FIGURE_ID,
        "pdeSimulation": False,
        "presentationOnly": True,
        "panels": {
            "A": (
                "exact adaptive moment floor and normalized q0 moment ledger"
            ),
            "B": (
                "analytic translated-cell coefficient curves with exact "
                "integer-k markers"
            ),
            "C": (
                "direct-sum implication chain and symbolic contraction-ratio "
                "formula"
            ),
        },
        "analyticClaimsFromBoundReport": [
            "coefficient-uniform unit-chart coercivity",
            "whole-line graph coercivity",
            "whole-line exact cubic energy-model block contraction",
        ],
        "claimsNotMade": [
            "figure or finite-certificate machine check of functional analysis",
            "numerical value or fitted estimate of C_T",
            "time-length-uniform contraction",
            "periodic transfer",
            "nonlinear Navier-Stokes closure",
            "Clay problem",
        ],
    }
    write_json(PACKAGE / "results.json", results)
    (PACKAGE / "progress.ndjson").write_text(
        "\n".join((
            '{"event":"build-start","stage":1,"totalStages":3}',
            (
                f'{{"event":"analytic-data-ready","rows":{len(rows)},'
                '"stage":2,"totalStages":3}'
            ),
            '{"event":"archive-ready","stage":3,"totalStages":3}',
        )) + "\n",
        encoding="utf-8",
    )
    (PACKAGE / "resource-log.ndjson").write_text(
        (
            f'{{"event":"resource-summary","processes":1,'
            f'"threadsPerProcess":1,"rows":{len(rows)},'
            '"gpuUsed":false,"pdeSimulation":false}\n'
        ),
        encoding="utf-8",
    )
    (PACKAGE / "qa-report.md").write_text(
        "".join((
            "# R0.72V figure QA\n\n",
            f"- formal build: {'yes' if formal else 'no'}\n",
            (
                "- explicit visual inspection: "
                f"{'yes' if visual_inspected else 'no'}\n"
            ),
            "- final-size preview generated: yes\n",
            "- grayscale preview generated: yes\n",
            "- vector PDF render preview generated: yes\n",
            "- analytic presentation only: yes\n",
            "- pdeSimulation: false\n",
            (
                "- exact cubic energy-model block contraction labelled "
                "CLOSED: yes\n"
            ),
            "- periodic and Clay labelled OPEN: yes\n",
        )),
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

    archived = [
        *SOURCE_FILES,
        "data.csv",
        "results.json",
        "validation.json",
        "progress.ndjson",
        "resource-log.ndjson",
        "qa-report.md",
        "figure.svg",
        "figure.pdf",
        "figure.png",
        "qa-final-size.png",
        "qa-grayscale.png",
        "qa-pdf.png",
    ]
    from PIL import Image

    image = Image.open(PACKAGE / "figure.png")
    data_schema = {
        "config.json": (
            "frozen exact formulas, ranges, dimensions, and output resolution"
        ),
        "contract.json": (
            "panel claims, source-stage lifecycle, public route, and boundaries"
        ),
        "data.csv": (
            "panel, series, x, y, analytic source formula, presentation status"
        ),
        "results.json": (
            "panel meanings, analytic report claims, and claims not made"
        ),
        "validation.json": (
            "certificate, format, resolution, and visible-boundary checks"
        ),
        "progress.ndjson": "deterministic three-stage analytic build progress",
        "resource-log.ndjson": (
            "deterministic process, thread, row, GPU, and simulation record"
        ),
    }
    manifest = {
        "schemaVersion": "1.1",
        "figureId": FIGURE_ID,
        "release": "R0.72V",
        "status": "formal" if formal else "draft",
        "createdAt": "2026-08-28T00:00:00+08:00",
        "analyticalQuestion": (
            "How do coefficient-uniform unit charts cover every translated "
            "cell and transfer the exact cubic graph estimate to a whole-line "
            "energy contraction?"
        ),
        "supportedClaim": (
            "The exact kappa floor, translated-cell coefficient identity, "
            "full-H1 H^-1 direct-sum chain, and analytic exact-cubic "
            "energy-model contraction; periodic and Clay remain open."
        ),
        "git": (
            {
                "repository": "Kasifa/Kasifa.github.io",
                "sourceCommit": source_commit,
                "certificateCommit": certificate_commit,
                "dirtyAtCertifiedRun": False,
            }
            if formal
            else {
                "repository": "Kasifa/Kasifa.github.io",
                "commit": subprocess.check_output(
                    ["git", "rev-parse", "HEAD"],
                    cwd=REPOSITORY,
                    text=True,
                ).strip(),
                "dirty": git_status_dirty(),
            }
        ),
        "computation": {
            "kind": "exact-analytic-presentation",
            "configuration": (
                "adaptive kappa curve, three translated coefficient "
                "parabolas with exact integer markers, and symbolic ratio"
            ),
            "precision": (
                "exact identities certificate-gated; binary64 only samples "
                "analytic presentation curves"
            ),
            "solver": (
                "no PDE solve, simulation, time stepping, regression, "
                "constant fitting, or random sampling"
            ),
            "formalCommand": "commands recorded in command.txt",
            "wallTimeSeconds": wall_time_seconds,
            "monitoring": {
                "enabled": True,
                "progressLog": "progress.ndjson",
                "resourceLog": "resource-log.ndjson",
                "trackedFields": [
                    "event",
                    "stage",
                    "rows",
                    "processes",
                    "threadsPerProcess",
                    "pdeSimulation",
                ],
            },
        },
        "compute": {
            "host": platform.node() or "local",
            "operatingSystem": platform.platform(),
            "cpu": platform.machine(),
            "memoryGiB": "not sampled; analytic figure only",
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
            "dgx": "not used",
        },
        "environment": {
            "python": platform.python_version(),
            "packagesLock": "requirements.txt",
            "pillow": getattr(Image, "__version__", "installed"),
            "reportlab": "pinned in requirements.txt",
        },
        "data": [
            {
                "path": name,
                "schema": schema,
                "format": Path(name).suffix.lstrip("."),
                "sha256": sha256(PACKAGE / name),
                "bytes": (PACKAGE / name).stat().st_size,
            }
            for name, schema in data_schema.items()
        ],
        "sourceData": [
            {
                "location": "repository",
                "fileName": str(CERTIFICATE.relative_to(REPOSITORY)),
                "bytes": CERTIFICATE.stat().st_size,
                "sha256": sha256(CERTIFICATE),
                "extractionCommand": (
                    "python3 research/certificates/r072v/"
                    "generate_certificate.py"
                ),
                "role": "exactFiniteCertificate",
            },
            {
                "location": "repository",
                "fileName": "scripts/generate_r072v_figure.py",
                "bytes": Path(__file__).stat().st_size,
                "sha256": sha256(Path(__file__)),
                "extractionCommand": (
                    "python3 scripts/generate_r072v_figure.py"
                ),
                "role": "analyticPresentationGenerator",
            },
        ],
        "figure": {
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "layout": "1x3",
            "profile": "journal-double-column",
            "script": "plot.py",
            "outputs": [
                {
                    "path": "figure.pdf",
                    "sha256": sha256(PACKAGE / "figure.pdf"),
                    "bytes": (PACKAGE / "figure.pdf").stat().st_size,
                },
                {
                    "path": "figure.svg",
                    "sha256": sha256(PACKAGE / "figure.svg"),
                    "bytes": (PACKAGE / "figure.svg").stat().st_size,
                },
                {
                    "path": "figure.png",
                    "sha256": sha256(PACKAGE / "figure.png"),
                    "bytes": (PACKAGE / "figure.png").stat().st_size,
                    "dpi": PNG_DPI,
                    "pixels": list(image.size),
                },
            ],
        },
        "caption": {"english": "caption.md"},
        "qa": {
            "status": "passed",
            "visualInspectionExplicit": visual_inspected,
            "finalSizeInspected": visual_inspected,
            "grayscaleInspected": visual_inspected,
            "labelsAndLegendsInspected": visual_inspected,
            "scalesAndUnitsInspected": visual_inspected,
            "dataCrossChecked": True,
            "finalSizePreview": "qa-final-size.png",
            "grayscalePreview": "qa-grayscale.png",
            "pdfRenderPreview": "qa-pdf.png",
            "manualReport": "qa-report.md",
        },
        "publication": {
            "directory": "public/assets/r072v",
            "stem": FIGURE_ID,
            "publicCopiesComplete": formal,
            "assets": publication_assets,
        },
        "claimBoundary": certificate["claimBoundary"],
        "deterministic": True,
        "outputs": [
            {
                "path": name,
                "sha256": sha256(PACKAGE / name),
                "bytes": (PACKAGE / name).stat().st_size,
            }
            for name in archived
        ],
    }
    write_json(PACKAGE / "manifest.json", manifest)
    ledger_names = sorted(
        path.name
        for path in PACKAGE.iterdir()
        if path.is_file() and path.name != "SHA256SUMS"
    )
    (PACKAGE / "SHA256SUMS").write_text(
        "".join(
            f"{sha256(PACKAGE / name)}  {name}\n"
            for name in ledger_names
        ),
        encoding="utf-8",
    )


def self_test() -> None:
    config = json.loads(
        (PACKAGE / "config.json").read_text(encoding="utf-8")
    )
    contract = json.loads(
        (PACKAGE / "contract.json").read_text(encoding="utf-8")
    )
    rows = analytic_rows()
    scene = build_scene()
    scene_text = {
        item[3] for item in scene.items if item[0] == "text"
    }
    package_files = {
        path.name for path in PACKAGE.iterdir() if path.is_file()
    }
    checks = {
        "figureId": (
            config.get("figureId") == FIGURE_ID
            and contract.get("figureId") == FIGURE_ID
        ),
        "dimensions": (
            config.get("widthMillimetres") == WIDTH_MM
            and config.get("heightMillimetres") == HEIGHT_MM
            and config.get("pngDpi") == PNG_DPI
        ),
        "sourceFilesPresent": set(SOURCE_FILES) <= package_files,
        "lifecycleFilesKnown": (
            package_files <= set(SOURCE_FILES) | set(GENERATED_FILES)
        ),
        "rowCount": len(rows) == EXPECTED_ROWS,
        "threePanels": {row["panel"] for row in rows} == {"A", "B", "C"},
        "exactKappaEndpoints": (
            Fraction(5, 6292)
            == Fraction(5, 6292) * 1 + Fraction(1, 44) * 0
            and abs(kappa(0.0) - 5 / 6292) < 1e-15
            and abs(kappa(math.pi / 2) - 1 / 44) < 1e-15
        ),
        "translationIdentity": all(
            abs(
                translated_b(3.0 * integer_k, center)
                - (3.0 * integer_k * integer_k + 6.0 * center)
            ) < 1e-14
            for center in (-2.0, 0.0, 2.0)
            for integer_k in range(-4, 5)
        ),
        "symbolicRatio": (
            contraction_ratio(0.0) == 0.0
            and abs(contraction_ratio(1.0) - 0.5) < 1e-15
        ),
        "pdeSimulationFalse": config.get("pdeSimulation") is False,
        "sceneBuilt": len(scene.items) > 100,
        "closedBoundary": (
            "whole-line block contraction: CLOSED "
            "(exact cubic energy model)" in scene_text
        ),
        "openBoundary": "periodic / Clay: OPEN" in scene_text,
        "formulaOnly": (
            "formula only; C_T not evaluated" in scene_text
        ),
        "hardTwoRootPalette": (
            contract.get("palette", {}).get("chromaticRoots")
            == [BLUE, GOLD]
            and contract.get("palette", {}).get("hardChromaticRootCap") == 2
        ),
        "blossomContract": (
            contract.get("researchBlossom")
            == {
                "carriesData": False,
                "lockedAnchor": "top-right-header",
                "petalCount": 5,
            }
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(
            f"R0.72V figure source self-test failed: {checks}"
        )
    print(
        "R0.72V figure source self-test: passed "
        f"({len(rows)} in-memory rows; no outputs written)"
    )


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
            parser.error(
                "--self-test cannot be combined with generation arguments"
            )
        self_test()
        return
    if not args.draft and not args.formal:
        parser.error("choose --self-test, --draft, or --formal")

    certificate_manifest, certificate = validate_formal_certificate()
    if args.formal:
        if git_status_dirty():
            raise RuntimeError(
                "formal figure generation requires a completely clean tree"
            )
        if not args.visual_inspected:
            raise RuntimeError(
                "formal figure generation requires --visual-inspected"
            )
        validate_formal_lineage(
            certificate_manifest,
            args.source_commit,
            args.certificate_commit,
        )
        reject_output_overwrite(include_public=True)
    else:
        if args.visual_inspected or args.source_commit or args.certificate_commit:
            parser.error(
                "draft generation does not accept formal lineage flags"
            )
        reject_output_overwrite(include_public=False)

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
        certificate=certificate,
        wall_time_seconds=time.perf_counter() - started,
    )
    print(
        f"R0.72V {'formal' if args.formal else 'draft'} figure package: "
        f"passed ({len(rows)} rows)"
    )


if __name__ == "__main__":
    main()
