#!/usr/bin/env python3
"""Render the deterministic R0.74K single-inward-collar figure.

The figure visualizes exact rational exponent bookkeeping and a conditional
proof dependency.  It contains no DNS, simulation, sampled stochastic path,
or evidence of Navier--Stokes singularity.
"""

from __future__ import annotations

import csv
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
CERTIFICATE = REPO / "research/r074k_single_collar_exponent_certificate.json"
PRODUCER = REPO / "scripts/r074k_single_collar_exponent_certificate.py"
FIGURE_ID = "fig-r074k-single-inward-collar"

BUNDLE = Path("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies")
PDFTOPPM = BUNDLE / "bin/override/pdftoppm"
WIDTH_MM = 178
HEIGHT_MM = 92
DPI = 600
W = WIDTH_MM * mm
H = HEIGHT_MM * mm

INK = HexColor("#202A34")
MID = HexColor("#626D78")
GRID = HexColor("#D9E0E5")
PALE = HexColor("#F5F7F8")
BLUE = HexColor("#1E5A8A")
BLUE_LIGHT = HexColor("#E8F1F7")
RED = HexColor("#A13D35")
RED_LIGHT = HexColor("#F8E9E6")
GOLD = HexColor("#A66E10")
GOLD_LIGHT = HexColor("#FBF1DB")
GREEN = HexColor("#376B55")

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


pdfmetrics.registerFont(TTFont("R074K-Regular", str(locate_font("DejaVuSans.ttf"))))
pdfmetrics.registerFont(TTFont("R074K-Bold", str(locate_font("DejaVuSans-Bold.ttf"))))


def write_text(path: Path, content: str) -> None:
    path.write_text(content.replace("\r\n", "\n").rstrip("\n") + "\n", encoding="utf-8")


def label(d: Drawing, x: float, y: float, text: str, size: float = 5.2, *,
          color=INK, bold: bool = False, anchor: str = "start") -> None:
    d.add(
        String(
            x,
            y,
            text,
            fontName="R074K-Bold" if bold else "R074K-Regular",
            fontSize=size,
            fillColor=color,
            textAnchor=anchor,
        )
    )


def arrow(d: Drawing, x0: float, y0: float, x1: float, y1: float, *, color=INK) -> None:
    d.add(Line(x0, y0, x1, y1, strokeColor=color, strokeWidth=1.05))
    angle = math.atan2(y1 - y0, x1 - x0)
    length = 4.0
    spread = 0.48
    d.add(
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
            strokeWidth=0.2,
        )
    )


def load_exact() -> tuple[dict, dict[str, Fraction]]:
    regenerated = subprocess.run(
        [sys.executable, str(PRODUCER)], check=True, capture_output=True
    ).stdout
    if regenerated != CERTIFICATE.read_bytes():
        raise RuntimeError("producer stdout is not byte-identical to certificate")
    data = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    if data.get("result") != "PASS" or data.get("summary") != {"passed": 41, "total": 41}:
        raise RuntimeError("certificate is not PASS 41/41")
    checks = {item["id"]: item for item in data["checks"]}
    if len(checks) != 41 or not all(item["pass"] for item in checks.values()):
        raise RuntimeError("certificate rows are incomplete")

    def value(check_id: str) -> Fraction:
        return Fraction(checks[check_id]["left"])

    values = {
        "wrong_boundary": value("nearest_boundary_wrong_margin"),
        "wrong_slab": value("nearest_slab_wrong_margin"),
        "sharp_m2": value("sharp_m2_margin"),
        "uniform_deep": value("uniform_deep_margin"),
        "coarse_m2": value("coarse_m2_margin"),
        "coarse_m3": value("coarse_m3_margin"),
        "chord": value("chord_square"),
        "slab_height": value("epsilon_slab_height"),
        "center": Fraction(15, 16),
        "target_inner": Fraction(32, 63),
        "inner_inner": Fraction(16, 63),
        "target_outer": Fraction(64, 63),
    }
    return data, values


def margins() -> list[dict]:
    lam = Fraction(63, 32)
    c_h = Fraction(15, 16)
    c_gamma = Fraction(8, 3969)
    rows = []
    for m in range(1, 7):
        d_m = c_h - Fraction(1, 1) / (lam * 2 ** (m - 1))
        gain = c_gamma * (1 - Fraction(1, 4**m))
        rows.append(
            {
                "m": m,
                "sharp": d_m * d_m / 132 - gain,
                "coarse": d_m * d_m / 262 - gain,
            }
        )
    return rows


def write_support_files(v: dict[str, Fraction], rows: list[dict]) -> None:
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["m", "sharp_margin_exact", "sharp_margin_times_1e3", "coarse_margin_exact", "coarse_margin_times_1e3", "status"])
        for row in rows:
            writer.writerow(
                [
                    row["m"],
                    f'{row["sharp"].numerator}/{row["sharp"].denominator}',
                    f'{1000 * float(row["sharp"]):.12f}',
                    f'{row["coarse"].numerator}/{row["coarse"].denominator}',
                    f'{1000 * float(row["coarse"]):.12f}',
                    "ADVERSE_NEAREST" if row["m"] == 1 else "SHARP_COMPATIBLE",
                ]
            )
        writer.writerow(
            [
                "1-positive-volume",
                f'{(-v["wrong_slab"]).numerator}/{(-v["wrong_slab"]).denominator}',
                f'{-1000 * float(v["wrong_slab"]):.12f}',
                "NA",
                "NA",
                "FREE_TAIL_PROOF_FAILS",
            ]
        )

    write_text(
        HERE / "caption.md",
        r"""# Figure caption

**Figure R0.74K.** Left: exact free squared-Gaussian exponent minus annular
weight gain for inward shells.  Positive values are compatible with
absorption.  The sharp denominator 132 closes every deeper shell
\(j-m\), \(m\ge2\), but the nearest shell remains adverse, including the
positive-volume \(\varepsilon=1/128\) slab.  Right: the true packet includes
a correlated differential-shear displacement in \(x_2\).  A bridge--BV
estimate on the main collar and shear-expulsion estimate at \(j-1\) would
imply the displayed familywise collar upper.  Those true-packet estimates
remain OPEN.  The diagram is exact bookkeeping, not DNS or evidence of a
singularity.  NOT CLAY.
""",
    )
    write_text(
        HERE / "chart-contract-and-source-data.md",
        r"""# Chart contract and source data

- Quantitative panel: exact `Fraction` values from the frozen 41/41 R0.74K
  certificate, independently reproducible from `source-data.csv`.
- Geometry panel: exact ratios \(16/63,32/63,64/63,15/16\) and slab height
  \(4033/8064\).
- Red means the free-tail proof mechanism has the wrong exponent; it does
  not mean the desired observable upper is false.
- Blue/green means finite exponent compatibility or a proved implication;
  it does not certify the missing bridge estimate.
- No stochastic samples, fitted curves, simulations, DNS, or empirical
  observations are plotted.
""",
    )
    write_text(
        HERE / "README.md",
        """# R0.74K formal figure package

This package contains a deterministic vector figure, 600-dpi PNG, exact
source table, plotting source, validation record, grayscale/final-size/PDF
QA surfaces, and SHA-256 seal.  Re-run the render command from the repository
root, inspect all four QA surfaces, replace the PENDING gate in `qa-report.md`
with a signed PASS or FAIL record, and only then run the validator.  The
result is a route-reduction diagram, not a numerical Navier--Stokes
simulation.  NOT CLAY.
""",
    )
    write_text(
        HERE / "command.txt",
        "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/figures/r074k/fig-r074k-single-inward-collar/plot.py\n"
        "# HUMAN GATE: inspect figure.png and all qa-*.png files; record PASS/FAIL in qa-report.md\n"
        "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 research/figures/r074k/fig-r074k-single-inward-collar/validate.py\n",
    )
    write_text(HERE / "requirements.txt", "Pillow==12.3.0\nreportlab==4.4.9\n")
    write_text(
        HERE / "qa-protocol.md",
        """# QA protocol

1. Reproduce the 41/41 exact certificate byte for byte.
2. Render one-page SVG/PDF and 600-dpi RGB PNG from the same vector drawing.
3. Inspect color, grayscale, final-size, and independent PDF raster surfaces.
4. Check zero-line, adverse-shell sign, positive-volume marker, labels,
   arrows, conditional OPEN box, clipping, and minimum text size.
5. Verify inventory, UTF-8/LF policy, manifest hashes, and SHA256SUMS.
""",
    )
    write_text(
        HERE / "qa-report.md",
        """# QA report

Manual status: PENDING

Automated structural validation is separate.  Before sealing, a human
reviewer must inspect color, grayscale, final-size, and PDF-raster surfaces;
verify the two annular regions, all labels and arrows, the exact conditional
hypothesis, clipping, and claim boundaries; and replace PENDING with a signed
PASS or FAIL record.  The validator must not self-certify this gate.
""",
    )
    config = {
        "figure_id": FIGURE_ID,
        "width_mm": WIDTH_MM,
        "height_mm": HEIGHT_MM,
        "dpi": DPI,
        "panels": ["exact inward-shell exponent margins", "correlated shear-lag mechanism and conditional route"],
        "data_class": "FINITE_EXACT_AND_ANALYTIC_DIAGRAM",
        "simulation": False,
    }
    write_text(HERE / "config.json", json.dumps(config, indent=2, sort_keys=True))
    contract = {
        "claim": "nearest inner shell is the unique wrong-sign free-tail exponent row",
        "proved": ["finite rational margins", "positive-volume chord", "reference-packet scale", "conditional algebra"],
        "open": ["time-coupled bridge-BV", "nearest-inner shear expulsion", "matching collar upper"],
        "forbidden": ["desired upper is false", "universal endpoint", "singularity", "global regularity", "Clay"],
    }
    write_text(HERE / "contract.json", json.dumps(contract, indent=2, sort_keys=True))
    environment = {
        "python": platform.python_version(),
        "platform": platform.platform(),
        "pillow": Image.__version__,
        "reportlab": __import__("reportlab").Version,
        "dgx_used": False,
    }
    write_text(HERE / "environment.json", json.dumps(environment, indent=2, sort_keys=True))


def render(v: dict[str, Fraction], rows: list[dict]) -> None:
    d = Drawing(W, H)
    d.add(Rect(0, 0, W, H, fillColor=white, strokeColor=None))

    margin = 10 * mm
    gap = 6 * mm
    panel_w = (W - 2 * margin - gap) / 2
    panel_h = H - 20 * mm
    panel_y = 8 * mm
    left_x = margin
    right_x = margin + panel_w + gap

    label(d, margin, H - 7 * mm, "R0.74K  |  ONE ADVERSE INWARD COLLAR", 8.2, bold=True)
    label(d, W - margin, H - 7 * mm, "FINITE EXACT + CONDITIONAL ROUTE", 5.2, color=MID, anchor="end")

    for x in (left_x, right_x):
        d.add(Rect(x, panel_y, panel_w, panel_h, rx=4, ry=4, fillColor=PALE, strokeColor=GRID, strokeWidth=0.8))

    # Panel A: exact margins.
    label(d, left_x + 5 * mm, panel_y + panel_h - 7 * mm, "A  inward-shell exponent ledger", 6.7, bold=True)
    label(d, left_x + 5 * mm, panel_y + panel_h - 12 * mm, "free F² decay minus annular gain  (×10⁻³)", 5.0, color=MID)

    chart_x0 = left_x + 13 * mm
    chart_x1 = left_x + panel_w - 6 * mm
    chart_y0 = panel_y + 16 * mm
    chart_y1 = panel_y + panel_h - 20 * mm
    ymin, ymax = -1.0, 4.8

    def px(m: int) -> float:
        return chart_x0 + (m - 1) * (chart_x1 - chart_x0) / 5

    def py(value: float) -> float:
        return chart_y0 + (value - ymin) * (chart_y1 - chart_y0) / (ymax - ymin)

    # highlight nearest shell
    d.add(Rect(px(1) - 5 * mm, chart_y0, 10 * mm, chart_y1 - chart_y0, fillColor=RED_LIGHT, strokeColor=None))
    for tick in (-1, 0, 1, 2, 3, 4):
        yy = py(tick)
        d.add(Line(chart_x0, yy, chart_x1, yy, strokeColor=GRID if tick else INK, strokeWidth=0.45 if tick else 0.8))
        label(d, chart_x0 - 2 * mm, yy - 1.5, str(tick), 5.0, color=MID, anchor="end")
    for m in range(1, 7):
        xx = px(m)
        label(d, xx, chart_y0 - 4 * mm, str(m), 5.0, color=MID, anchor="middle")
    label(d, (chart_x0 + chart_x1) / 2, chart_y0 - 8 * mm, "inward depth  m  in  j−m", 5.0, color=MID, anchor="middle")

    sharp_pts = [(px(r["m"]), py(1000 * float(r["sharp"]))) for r in rows]
    coarse_pts = [(px(r["m"]), py(1000 * float(r["coarse"]))) for r in rows]
    for pts, color in ((sharp_pts, BLUE), (coarse_pts, GOLD)):
        for a, b in zip(pts, pts[1:]):
            d.add(Line(a[0], a[1], b[0], b[1], strokeColor=color, strokeWidth=1.2))
        for xx, yy in pts:
            d.add(Circle(xx, yy, 2.2, fillColor=white, strokeColor=color, strokeWidth=1.2))

    slab_y = py(-1000 * float(v["wrong_slab"]))
    slab_x = px(1) + 3.2 * mm
    d.add(Polygon([slab_x, slab_y + 2.8, slab_x + 2.8, slab_y, slab_x, slab_y - 2.8, slab_x - 2.8, slab_y], fillColor=RED, strokeColor=RED))

    legend_y = panel_y + 7 * mm
    d.add(Line(left_x + 8 * mm, legend_y, left_x + 16 * mm, legend_y, strokeColor=BLUE, strokeWidth=1.4))
    label(d, left_x + 18 * mm, legend_y - 1.6, "sharp dₘ² / 132", 5.0, color=BLUE)
    d.add(Line(left_x + 42 * mm, legend_y, left_x + 50 * mm, legend_y, strokeColor=GOLD, strokeWidth=1.4))
    label(d, left_x + 52 * mm, legend_y - 1.6, "inherited dₘ² / 262", 5.0, color=GOLD)
    slab_legend_y = panel_y + 3.2 * mm
    slab_legend_x = left_x + 8 * mm
    d.add(Polygon([slab_legend_x, slab_legend_y + 2.8, slab_legend_x + 2.8, slab_legend_y, slab_legend_x, slab_legend_y - 2.8, slab_legend_x - 2.8, slab_legend_y], fillColor=RED, strokeColor=RED))
    label(d, left_x + 12 * mm, slab_legend_y - 1.6, "positive-volume slab", 5.0, color=RED)
    label(d, px(1), chart_y1 + 2 * mm, "ADVERSE", 5.0, color=RED, bold=True, anchor="middle")
    label(d, px(3.8), chart_y1 + 2 * mm, "sharp-compatible", 5.0, color=GREEN, bold=True, anchor="middle")

    # Panel B: exact geometry and conditional chain.
    label(d, right_x + 5 * mm, panel_y + panel_h - 7 * mm, "B  true packet: correlation cannot be dropped", 6.7, bold=True)

    geom_cx = right_x + 25 * mm
    geom_cy = panel_y + 36 * mm
    scale = 22 * mm
    r_inner = float(v["inner_inner"]) * scale
    r_shared = float(v["target_inner"]) * scale
    r_outer = float(v["target_outer"]) * scale
    d.add(Circle(geom_cx, geom_cy, r_outer, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=0.9))
    d.add(Circle(geom_cx, geom_cy, r_shared, fillColor=RED_LIGHT, strokeColor=BLUE, strokeWidth=0.9))
    d.add(Circle(geom_cx, geom_cy, r_inner, fillColor=PALE, strokeColor=RED, strokeWidth=0.8))
    d.add(Line(geom_cx - 24 * mm, geom_cy, geom_cx + 23 * mm, geom_cy, strokeColor=GRID, strokeWidth=0.5))
    d.add(Line(geom_cx, geom_cy - 17 * mm, geom_cx, geom_cy + 25 * mm, strokeColor=GRID, strokeWidth=0.5))
    label(d, geom_cx + 20.5 * mm, geom_cy + 1.5, "x₂", 5.0, color=MID)
    label(d, geom_cx + 1.5, geom_cy + 24 * mm, "x₃", 5.0, color=MID)

    center_y = geom_cy + float(v["center"]) * scale
    slab_y_geom = geom_cy + float(v["slab_height"]) * scale
    d.add(Circle(geom_cx, center_y, 2.5, fillColor=BLUE, strokeColor=white, strokeWidth=0.4))
    label(d, geom_cx + 3 * mm, center_y + 1, "packet centre  h", 5.0, color=BLUE)
    arrow(d, geom_cx, center_y - 2.5, geom_cx, slab_y_geom + 2.5, color=RED)
    label(d, geom_cx + 2 * mm, (center_y + slab_y_geom) / 2, "free inward tail", 5.0, color=RED)
    chord_half = math.sqrt(float(v["chord"])) * scale
    d.add(Line(geom_cx - chord_half, slab_y_geom, geom_cx + chord_half, slab_y_geom, strokeColor=RED, strokeWidth=2.0))
    label(d, geom_cx, slab_y_geom - 4 * mm, "j−1 slab; nonzero chord", 5.0, color=RED, anchor="middle")
    arrow(d, geom_cx - 1 * mm, slab_y_geom + 2 * mm, geom_cx - 16 * mm, slab_y_geom + 2 * mm, color=GOLD)
    label(d, geom_cx - 8 * mm, slab_y_geom + 5 * mm, "positive shear lag  S", 5.0, color=GOLD, anchor="middle")

    label(d, geom_cx - 19 * mm, geom_cy + 1.5, "Aⱼ", 5.0, color=BLUE, bold=True, anchor="middle")
    label(d, geom_cx - 8.5 * mm, geom_cy + 1.5, "Aⱼ₋₁", 5.0, color=RED, bold=True, anchor="middle")

    route_x = right_x + 50 * mm
    route_w = panel_w - 54 * mm
    route_y = panel_y + 14 * mm
    box_h = 10 * mm
    stages = [
        (("Aⱼ reference scale", "PROVED", "true bridge–BV OPEN"), GOLD_LIGHT, GOLD),
        (("j−1 shear expulsion", "true-packet estimate", "OPEN"), RED_LIGHT, RED),
        (("supτ [Iⱼ(τ)]₊", "≤ C Γⱼ Lⱼ Rⱼ⁵", "OPEN (4.3)"), BLUE_LIGHT, BLUE),
        (("Cⱼ ≲ Bⱼ² Lⱼ Rⱼ²", "familywise implication", "if hypothesis holds"), white, GREEN),
    ]
    for index, (lines, fill, color) in enumerate(stages):
        yy = route_y + (len(stages) - 1 - index) * 13 * mm
        d.add(Rect(route_x, yy, route_w, box_h, rx=3, ry=3, fillColor=fill, strokeColor=color, strokeWidth=0.8))
        label(d, route_x + route_w / 2, yy + 7.0 * mm, lines[0], 5.0, bold=True, color=color, anchor="middle")
        label(d, route_x + route_w / 2, yy + 4.1 * mm, lines[1], 5.0, color=MID, anchor="middle")
        label(d, route_x + route_w / 2, yy + 1.3 * mm, lines[2], 5.0, color=RED if "OPEN" in lines[2] else MID, anchor="middle")
        if index < len(stages) - 1:
            arrow(d, route_x + route_w / 2, yy - 0.5 * mm, route_x + route_w / 2, yy - 3 * mm, color=MID)
    label(d, right_x + panel_w / 2, panel_y + 6.5 * mm, "OPEN ≠ false   |   familywise ≠ universal   |   NOT CLAY", 5.0, color=MID, anchor="middle")

    renderPDF.drawToFile(d, str(HERE / "figure.pdf"))
    renderSVG.drawToFile(d, str(HERE / "figure.svg"))

    subprocess.run(
        [str(PDFTOPPM), "-png", "-r", str(DPI), "-singlefile", str(HERE / "figure.pdf"), str(HERE / "figure-raster")],
        check=True,
        capture_output=True,
    )
    raster = HERE / "figure-raster.png"
    img = Image.open(raster).convert("RGB")
    img.save(HERE / "figure.png", dpi=(DPI, DPI), optimize=True)
    raster.unlink()

    final_size = img.resize((1402, 724), Image.Resampling.LANCZOS)
    final_size.save(HERE / "qa-final-size.png", optimize=True)
    ImageOps.grayscale(final_size).save(HERE / "qa-grayscale.png", optimize=True)

    subprocess.run(
        [str(PDFTOPPM), "-png", "-r", "300", "-singlefile", str(HERE / "figure.pdf"), str(HERE / "qa-pdf-raster")],
        check=True,
        capture_output=True,
    )
    pdf_qa = HERE / "qa-pdf-raster.png"
    Image.open(pdf_qa).convert("RGB").save(HERE / "qa-pdf.png", optimize=True)
    pdf_qa.unlink()

    layout = {
        "canvas_pt": [float(W), float(H)],
        "panels": {
            "A": [float(left_x), float(panel_y), float(panel_w), float(panel_h)],
            "B": [float(right_x), float(panel_y), float(panel_w), float(panel_h)],
        },
        "minimum_declared_font_pt": 5.0,
        "overlap_proxy": "MANUAL_QA_REQUIRED",
    }
    write_text(HERE / "layout-bounds.json", json.dumps(layout, indent=2, sort_keys=True))
    results = {
        "figure_id": FIGURE_ID,
        "status": "RENDERED",
        "certificate": "PASS_41_OF_41",
        "nearest_positive_volume_wrong_margin": f'{v["wrong_slab"].numerator}/{v["wrong_slab"].denominator}',
        "uniform_deeper_margin": f'{v["uniform_deep"].numerator}/{v["uniform_deep"].denominator}',
        "conditional_hypothesis": "OPEN",
        "simulation": False,
        "clay": "NOT_CLAIMED",
    }
    write_text(HERE / "results.json", json.dumps(results, indent=2, sort_keys=True))
    write_text(
        HERE / "progress.ndjson",
        "\n".join(
            json.dumps(item, sort_keys=True)
            for item in [
                {"step": "certificate-rebind", "status": "PASS_41_OF_41"},
                {"step": "vector-render", "status": "PASS"},
                {"step": "600dpi-raster", "status": "PASS"},
                {"step": "qa-surfaces", "status": "READY_FOR_VALIDATION"},
            ]
        ),
    )


def main() -> None:
    _, values = load_exact()
    rows = margins()
    write_support_files(values, rows)
    render(values, rows)
    print("R074K_FIGURE_RENDER=PASS")
    print("R074K_DATA_CLASS=FINITE_EXACT_AND_ANALYTIC_DIAGRAM")
    print("R074K_SIMULATION=false")


if __name__ == "__main__":
    main()
