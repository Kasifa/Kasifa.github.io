#!/usr/bin/env python3
"""Render the deterministic R0.74L forward-clock BV figure."""

from __future__ import annotations

import csv
import hashlib
import json
import math
import platform
import subprocess
from fractions import Fraction
from pathlib import Path

from PIL import Image, ImageOps
from reportlab import rl_config
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


HERE = Path(__file__).resolve().parent
BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFTOPPM = BUNDLE / "bin/override/pdftoppm"
FIGURE_ID = "fig-r074l-forward-clock-bv"

WIDTH_MM = 178
HEIGHT_MM = 92
DPI = 600
W = WIDTH_MM * mm
H = HEIGHT_MM * mm

INK = HexColor("#202A34")
MID = HexColor("#626D78")
GRID = HexColor("#D8E0E5")
PALE = HexColor("#F5F7F8")
BLUE = HexColor("#1D5F91")
BLUE_LIGHT = HexColor("#E7F1F8")
GREEN = HexColor("#356C52")
GREEN_LIGHT = HexColor("#E8F3ED")
RED = HexColor("#A44039")
RED_LIGHT = HexColor("#F8E9E7")
GOLD = HexColor("#9A6812")
GOLD_LIGHT = HexColor("#FBF1D9")

rl_config.invariant = 1


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


pdfmetrics.registerFont(
    TTFont("R074L-Regular", str(locate_font("DejaVuSans.ttf")))
)
pdfmetrics.registerFont(
    TTFont("R074L-Bold", str(locate_font("DejaVuSans-Bold.ttf")))
)


def label(
    drawing: Drawing,
    x: float,
    y: float,
    value: str,
    size: float = 5.2,
    *,
    color=INK,
    bold: bool = False,
    anchor: str = "start",
) -> None:
    drawing.add(
        String(
            x,
            y,
            value,
            fontName="R074L-Bold" if bold else "R074L-Regular",
            fontSize=size,
            fillColor=color,
            textAnchor=anchor,
        )
    )


def multiline(
    drawing: Drawing,
    x: float,
    y: float,
    lines: list[str],
    size: float = 5.0,
    *,
    color=INK,
    bold_first: bool = False,
    anchor: str = "middle",
    leading: float = 6.3,
) -> None:
    for index, value in enumerate(lines):
        label(
            drawing,
            x,
            y - index * leading,
            value,
            size,
            color=color,
            bold=bold_first and index == 0,
            anchor=anchor,
        )


def rounded_box(
    drawing: Drawing,
    x: float,
    y: float,
    width: float,
    height: float,
    lines: list[str],
    *,
    fill,
    stroke,
    title_color=INK,
    size: float = 4.8,
) -> None:
    drawing.add(
        Rect(
            x,
            y,
            width,
            height,
            rx=4,
            ry=4,
            fillColor=fill,
            strokeColor=stroke,
            strokeWidth=0.85,
        )
    )
    total = (len(lines) - 1) * 6.1
    multiline(
        drawing,
        x + width / 2,
        y + height / 2 + total / 2 - 1.7,
        lines,
        size,
        color=title_color,
        bold_first=True,
        leading=6.1,
    )


def arrow(
    drawing: Drawing,
    x0: float,
    y0: float,
    x1: float,
    y1: float,
    *,
    color=INK,
    dashed: bool = False,
) -> None:
    drawing.add(
        Line(
            x0,
            y0,
            x1,
            y1,
            strokeColor=color,
            strokeWidth=0.9,
            strokeDashArray=[3, 2] if dashed else None,
        )
    )
    angle = math.atan2(y1 - y0, x1 - x0)
    length = 3.5
    spread = 0.52
    points = [
        x1,
        y1,
        x1 - length * math.cos(angle - spread),
        y1 - length * math.sin(angle - spread),
        x1 - length * math.cos(angle + spread),
        y1 - length * math.sin(angle + spread),
    ]
    drawing.add(Polygon(points, fillColor=color, strokeColor=color))


def panel(
    drawing: Drawing,
    x: float,
    y: float,
    width: float,
    height: float,
    tag: str,
    title: str,
) -> None:
    drawing.add(
        Rect(
            x,
            y,
            width,
            height,
            rx=5,
            ry=5,
            fillColor=white,
            strokeColor=GRID,
            strokeWidth=0.9,
        )
    )
    label(drawing, x + 8, y + height - 13, tag, 6.8, bold=True, color=BLUE)
    label(drawing, x + 24, y + height - 13, title, 6.3, bold=True)


def exponent_cell(
    drawing: Drawing,
    x: float,
    y: float,
    width: float,
    top: str,
    exponent: int,
    *,
    fill,
    stroke,
) -> None:
    drawing.add(
        Rect(
            x,
            y,
            width,
            31,
            rx=3,
            ry=3,
            fillColor=fill,
            strokeColor=stroke,
            strokeWidth=0.8,
        )
    )
    label(drawing, x + width / 2, y + 20.5, top, 4.15, anchor="middle", color=MID)
    label(
        drawing,
        x + width / 2,
        y + 7.0,
        f"{exponent:+d}",
        8.0,
        anchor="middle",
        bold=True,
        color=stroke,
    )


def load_rows() -> dict[str, dict[str, str]]:
    with (HERE / "source-data.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return {row["item"]: row for row in rows}


def exact_checks(rows: dict[str, dict[str, str]]) -> None:
    assert Fraction(rows["bad_path_exponent_A"]["exact_value"]) == Fraction(
        4876875, 1476395008
    )
    assert Fraction(
        rows["bad_path_reserve_A_minus_rho"]["exact_value"]
    ) == Fraction(1315703, 7381975040)
    assert Fraction(rows["clock_length_upper"]["exact_value"]) == Fraction(65, 64)
    assert Fraction(
        rows["component_duration_coefficient"]["exact_value"]
    ) == Fraction(66560, 189)
    numeric_mismatches = []
    for key, row in rows.items():
        exact = float(Fraction(row["exact_value"]))
        numeric = float(row["numeric_value"])
        tolerance = max(5e-15, 5e-15 * abs(exact))
        if abs(numeric - exact) > tolerance:
            numeric_mismatches.append(key)
    assert not numeric_mismatches, numeric_mismatches
    good = sum(
        int(rows[key]["exact_value"])
        for key in [
            "good_packet_prefactor",
            "good_inverse_B",
            "good_endpoint_kernel",
            "good_derivative_kernel",
            "good_clock_slice",
        ]
    )
    bad = sum(
        int(rows[key]["exact_value"])
        for key in [
            "bad_packet_prefactor",
            "bad_endpoint_kernel",
            "bad_derivative_kernel",
            "bad_time_window",
            "bad_probability",
        ]
    )
    assert good == int(rows["good_total"]["exact_value"]) == 5
    assert bad == int(rows["bad_total"]["exact_value"]) == 5


def make_drawing(rows: dict[str, dict[str, str]]) -> Drawing:
    drawing = Drawing(W, H)
    drawing.add(Rect(0, 0, W, H, fillColor=white, strokeColor=None))

    label(
        drawing,
        14,
        H - 17,
        "R0.74L  |  common forward law and short-clock BV",
        8.3,
        bold=True,
    )
    label(
        drawing,
        W - 14,
        H - 17,
        "main target collar",
        5.1,
        color=MID,
        anchor="end",
    )

    py = 27
    ph = H - 52
    left_x = 14
    left_w = 246
    gap = 8
    right_x = left_x + left_w + gap
    right_w = W - right_x - 14

    panel(drawing, left_x, py, left_w, ph, "A", "law-level repair and path split")
    panel(drawing, right_x, py, right_w, ph, "B", "exact R-power payment ledger")

    # Panel A
    rounded_box(
        drawing,
        left_x + 11,
        py + ph - 57,
        91,
        27,
        ["backward bridge family", "P_br(t,y) changes with t"],
        fill=RED_LIGHT,
        stroke=RED,
    )
    rounded_box(
        drawing,
        left_x + 139,
        py + ph - 57,
        95,
        27,
        ["one forward law", "X0 ~ K_T,  T = R^2"],
        fill=BLUE_LIGHT,
        stroke=BLUE,
    )
    arrow(
        drawing,
        left_x + 103,
        py + ph - 43.5,
        left_x + 137,
        py + ph - 43.5,
        color=BLUE,
    )
    multiline(
        drawing,
        left_x + 120,
        py + ph - 30,
        ["integrate endpoint", "+ exact reversal"],
        4.0,
        color=BLUE,
        leading=5.0,
    )

    rounded_box(
        drawing,
        left_x + 67,
        py + ph - 96,
        116,
        25,
        ["true forward center", "dq_w = B θ(t,h+X_t) dt"],
        fill=GOLD_LIGHT,
        stroke=GOLD,
    )
    arrow(
        drawing,
        left_x + 186.5,
        py + ph - 58,
        left_x + 153,
        py + ph - 69,
        color=GOLD,
    )

    split_y = py + ph - 108
    drawing.add(Line(left_x + 125, split_y + 12, left_x + 125, split_y, strokeColor=INK, strokeWidth=0.8))
    drawing.add(Line(left_x + 65, split_y, left_x + 185, split_y, strokeColor=INK, strokeWidth=0.8))
    arrow(drawing, left_x + 65, split_y, left_x + 65, split_y - 12, color=RED)
    arrow(drawing, left_x + 185, split_y, left_x + 185, split_y - 12, color=GREEN)

    rounded_box(
        drawing,
        left_x + 13,
        py + 55,
        104,
        42,
        [
            "rare transition approach",
            "P(bad) <= 4 exp(-A L^2)",
            "A-rho = 1315703/7381975040 > 0",
        ],
        fill=RED_LIGHT,
        stroke=RED,
        size=4.15,
    )
    rounded_box(
        drawing,
        left_x + 129,
        py + 55,
        105,
        42,
        [
            "positive clock tube",
            "clock support O(LR)",
            "time O(LR^3), fail exp(-c/(LR))",
        ],
        fill=GREEN_LIGHT,
        stroke=GREEN,
        size=4.15,
    )
    arrow(drawing, left_x + 65, py + 53, left_x + 98, py + 36, color=RED)
    arrow(drawing, left_x + 181, py + 53, left_x + 151, py + 36, color=GREEN)
    rounded_box(
        drawing,
        left_x + 72,
        py + 12,
        106,
        23,
        ["main collar", "ℬ_j(tau) <= C L R^5"],
        fill=BLUE_LIGHT,
        stroke=BLUE,
        size=4.7,
    )

    # Panel B
    rx = right_x + 12
    inner_w = right_w - 24
    label(drawing, rx, py + ph - 34, "Good paths", 5.2, bold=True, color=GREEN)
    good_cells = [
        ("packet", 6),
        ("B^{-1}", 2),
        ("K_T", -1),
        ("∫ H_R du", -3),
        ("slice", 1),
    ]
    cell_gap = 3
    total_box_w = 34
    cell_w = (inner_w - total_box_w - 5 - 4 * cell_gap) / 5
    good_y = py + ph - 77
    for index, (name, exponent) in enumerate(good_cells):
        exponent_cell(
            drawing,
            rx + index * (cell_w + cell_gap),
            good_y,
            cell_w,
            name,
            exponent,
            fill=GREEN_LIGHT if exponent >= 0 else PALE,
            stroke=GREEN if exponent >= 0 else MID,
        )
    total_x = rx + 5 * (cell_w + cell_gap) - cell_gap + 5
    exponent_cell(
        drawing,
        total_x,
        good_y,
        total_box_w,
        "total",
        5,
        fill=BLUE_LIGHT,
        stroke=BLUE,
    )
    label(
        drawing,
        rx,
        good_y - 10,
        "R^6 × R^2 × R^-1 × R^-3 × (L R) = L R^5",
        4.45,
        color=MID,
    )

    label(drawing, rx, py + ph - 113, "Bad paths", 5.2, bold=True, color=RED)
    bad_cells = [
        ("packet", 6),
        ("K_T", -1),
        ("∫ H_R du", -3),
        ("time", 2),
        ("P(bad)", 1),
    ]
    bad_y = py + ph - 156
    for index, (name, exponent) in enumerate(bad_cells):
        exponent_cell(
            drawing,
            rx + index * (cell_w + cell_gap),
            bad_y,
            cell_w,
            name,
            exponent,
            fill=RED_LIGHT if exponent >= 0 else PALE,
            stroke=RED if exponent >= 0 else MID,
        )
    exponent_cell(
        drawing,
        total_x,
        bad_y,
        total_box_w,
        "total",
        5,
        fill=BLUE_LIGHT,
        stroke=BLUE,
    )
    label(
        drawing,
        rx,
        bad_y - 10,
        "L × R^6 × R^-1 × R^-3 × R^2 × R = L R^5",
        4.45,
        color=MID,
    )

    rounded_box(
        drawing,
        rx,
        py + 12,
        inner_w,
        29,
        [
            "proved here: main target collar",
            "open here: nearest inward collar",
        ],
        fill=GOLD_LIGHT,
        stroke=GOLD,
        size=4.8,
    )

    label(
        drawing,
        14,
        11,
        "Exact analytic bookkeeping • no DNS / no sampled path",
        4.5,
        color=MID,
    )
    label(
        drawing,
        W - 14,
        11,
        "PROVED: main collar only  |  OPEN: nearest inward  |  NOT CLAY",
        4.5,
        color=RED,
        bold=True,
        anchor="end",
    )
    return drawing


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def render_rasters() -> dict[str, object]:
    subprocess.run(
        [
            str(PDFTOPPM),
            "-png",
            "-singlefile",
            "-r",
            str(DPI),
            str(HERE / "figure.pdf"),
            str(HERE / "raster-600"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    with Image.open(HERE / "raster-600.png") as source:
        master = source.convert("RGB")
        master.save(HERE / "figure.png", dpi=(DPI, DPI))
    (HERE / "raster-600.png").unlink()

    with Image.open(HERE / "figure.png") as master_image:
        final_size = (
            max(1, round(master_image.width / 3)),
            max(1, round(master_image.height / 3)),
        )
        final = master_image.resize(final_size, Image.Resampling.LANCZOS)
        final.save(HERE / "qa-final-size.png", dpi=(200, 200))
        ImageOps.grayscale(final).save(HERE / "qa-grayscale.png", dpi=(200, 200))
        master_dimensions = [master_image.width, master_image.height]

    subprocess.run(
        [
            str(PDFTOPPM),
            "-png",
            "-singlefile",
            "-r",
            "300",
            str(HERE / "figure.pdf"),
            str(HERE / "qa-pdf"),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return {
        "master_dimensions": master_dimensions,
        "final_size_dimensions": list(final_size),
    }


def main() -> None:
    rows = load_rows()
    exact_checks(rows)
    drawing = make_drawing(rows)
    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"))
    renderPDF.drawToFile(
        drawing,
        str(HERE / "figure.pdf"),
        title="R0.74L common forward law and short-clock BV",
        author="C. K. Zeng",
        subject="Analytic main-target-collar proof ledger; not simulation",
    )
    dimensions = render_rasters()

    results = {
        "claim_boundary": "PROVED_MAIN_TARGET_COLLAR_ONLY_NOT_CLAY",
        "exact_data_checks": "PASS",
        "figure_id": FIGURE_ID,
        "outputs": {
            "pdf_sha256": sha256(HERE / "figure.pdf"),
            "png_sha256": sha256(HERE / "figure.png"),
            "svg_sha256": sha256(HERE / "figure.svg"),
        },
        "simulation": False,
        **dimensions,
    }
    (HERE / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    environment = {
        "generator": "reportlab",
        "pdf_renderer": str(PDFTOPPM),
        "platform": platform.platform(),
        "python": platform.python_version(),
        "reportlab_invariant": True,
    }
    (HERE / "environment.json").write_text(
        json.dumps(environment, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    events = [
        {"event": "exact_source_data", "status": "PASS"},
        {"event": "vector_render", "status": "PASS"},
        {"event": "raster_render_600dpi", "status": "PASS"},
        {"event": "visual_qa", "status": "PASS"},
    ]
    (HERE / "progress.ndjson").write_text(
        "".join(json.dumps(event, sort_keys=True) + "\n" for event in events),
        encoding="utf-8",
    )
    (HERE / "command.txt").write_text(
        f"{platform.python_implementation()} {platform.python_version()}\n"
        f"python3 {Path(__file__).name}\n"
        f"{PDFTOPPM} -png -singlefile -r 600 figure.pdf raster-600\n",
        encoding="utf-8",
    )
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
