#!/usr/bin/env python3
"""Render the deterministic R0.74P temporal-observable triage figure."""

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
from reportlab import Version as REPORTLAB_VERSION
from reportlab import rl_config
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Circle, Drawing, Line, Path as ShapePath, Rect, String
from reportlab.lib.colors import HexColor, white
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
CERTIFICATE = REPO / "research/r074p_temporal_clock_certificate.json"

INK = HexColor("#202A34")
MID = HexColor("#68747E")
GRID = HexColor("#D6DDE2")
PALE = HexColor("#F6F8F9")
BLUE = HexColor("#285F82")
BLUE_LIGHT = HexColor("#E8F1F6")
GOLD = HexColor("#986817")
GOLD_LIGHT = HexColor("#F7EEDC")
PLUM = HexColor("#6F536F")
PLUM_LIGHT = HexColor("#F1EAF1")

rl_config.invariant = 1


def locate_dependency_root() -> Path | None:
    override = os.environ.get("R074P_DEPENDENCIES_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    for parent in Path(sys.executable).resolve().parents:
        if (parent / "bin/override/pdftoppm").is_file():
            return parent
    return None


BUNDLE = locate_dependency_root()
bundled_pdftoppm = BUNDLE / "bin/override/pdftoppm" if BUNDLE else None
path_pdftoppm = shutil.which("pdftoppm")
PDFTOPPM = bundled_pdftoppm if bundled_pdftoppm and bundled_pdftoppm.is_file() else (
    Path(path_pdftoppm).resolve() if path_pdftoppm else None
)
if PDFTOPPM is None:
    raise FileNotFoundError("pdftoppm; set R074P_DEPENDENCIES_ROOT or add pdftoppm to PATH")


def locate_font(filename: str) -> Path:
    candidates = []
    if BUNDLE:
        candidates.append(
            BUNDLE
            / "native/libreoffice-headless/libreoffice/LibreOfficeDev.app/Contents/Resources/fonts/truetype"
            / filename
        )
    candidates.extend([
        Path("/System/Library/Fonts/Supplemental") / filename,
        Path("/Library/Fonts") / filename,
        Path("/usr/share/fonts/truetype/dejavu") / filename,
    ])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(filename)


def dependency_label(path: Path) -> str:
    if BUNDLE:
        try:
            return f"R074P_DEPENDENCIES_ROOT/{path.relative_to(BUNDLE)}"
        except ValueError:
            pass
    return path.name


REGULAR_FONT = locate_font("DejaVuSans.ttf")
BOLD_FONT = locate_font("DejaVuSans-Bold.ttf")
pdfmetrics.registerFont(TTFont("R074P-Regular", str(REGULAR_FONT)))
pdfmetrics.registerFont(TTFont("R074P-Bold", str(BOLD_FONT)))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def progress(stage: str, status: str, detail: str) -> None:
    with (HERE / "progress.ndjson").open("a", encoding="utf-8") as handle:
        handle.write(
            json.dumps(
                {"stage": stage, "status": status, "detail": detail},
                sort_keys=True,
            )
            + "\n"
        )


def label(
    drawing: Drawing,
    x: float,
    y: float,
    value: str,
    size: float = 5.0,
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
            fontName="R074P-Bold" if bold else "R074P-Regular",
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
    size: float = 4.2,
    *,
    color=INK,
    bold_first: bool = False,
    anchor: str = "start",
    leading: float = 5.3,
) -> None:
    for index, line in enumerate(lines):
        label(
            drawing,
            x,
            y - index * leading,
            line,
            size,
            color=color,
            bold=bold_first and index == 0,
            anchor=anchor,
        )


def panel(drawing: Drawing, x: float, y: float, width: float, height: float, tag: str, title: str) -> None:
    drawing.add(
        Rect(
            x,
            y,
            width,
            height,
            rx=4,
            ry=4,
            fillColor=white,
            strokeColor=GRID,
            strokeWidth=0.8,
        )
    )
    label(drawing, x + 8, y + height - 14, tag, 6.7, color=BLUE, bold=True)
    label(drawing, x + 24, y + height - 14, title, 6.1, bold=True)


def blossom(drawing: Drawing, x: float, y: float) -> None:
    petals = [(0, 4.5), (4.5, 0), (0, -4.5), (-4.5, 0)]
    for dx, dy in petals:
        drawing.add(Circle(x + dx, y + dy, 2.35, fillColor=BLUE_LIGHT, strokeColor=BLUE, strokeWidth=0.55))
    drawing.add(Circle(x, y, 1.8, fillColor=GOLD_LIGHT, strokeColor=GOLD, strokeWidth=0.55))


def load_config() -> dict:
    config = json.loads((HERE / "config.json").read_text(encoding="utf-8"))
    assert config["schema"] == "r074p-observable-triage-config-v1"
    assert config["figure_id"] == "fig-r074p-observable-triage"
    assert config["width_mm"] == 178 and config["height_mm"] == 100
    assert config["dpi"] == 600
    return config


def certificate_values() -> dict[str, Fraction]:
    payload = json.loads(CERTIFICATE.read_text(encoding="utf-8"))
    checks = {row["id"]: row for row in payload["checks"]}
    assert len(checks) == 52
    assert all(row["pass"] for row in payload["checks"])
    expected = {
        "m_exact": Fraction(43, 423360),
        "K_exponential_rate": Fraction(43, 635040),
        "strong_exponential_penalty": Fraction(4, 3969),
    }
    for key, value in expected.items():
        assert Fraction(checks[key]["left"]) == value, key
    assert expected["strong_exponential_penalty"] / expected["K_exponential_rate"] == Fraction(640, 43)
    return expected


def generate_source_data(config: dict) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    x_min = Fraction(str(config["log10_K_min"]))
    x_max = Fraction(str(config["log10_K_max"]))
    step = Fraction(str(config["log10_K_step"]))
    count = int((x_max - x_min) / step) + 1
    assert count == 49

    panel_a: list[dict[str, str]] = []
    for series in config["carleson_series"]:
        beta = Fraction(series["beta_numerator"], series["beta_denominator"])
        for index in range(count):
            x_value = x_min + index * step
            y_value = -beta * x_value
            panel_a.append(
                {
                    "panel": "A",
                    "item_id": f"{series['id']}_{index:02d}",
                    "series_id": series["id"],
                    "label": series["label"],
                    "sigma_or_beta_exact": f"{beta.numerator}/{beta.denominator}",
                    "log10_K": f"{float(x_value):.2f}",
                    "log10_decay_term": f"{float(y_value):.6f}",
                    "observable": "",
                    "relation": "<=",
                    "rate_exact": "",
                    "rate_decimal": "",
                    "classification": "proved decay-rate term; additive log10 C suppressed",
                    "claim_type": "PROVED_RATE_ONLY",
                }
            )

    panel_b: list[dict[str, str]] = []
    for row in config["rate_ledger"]:
        rate = Fraction(row["rate_numerator"], row["rate_denominator"])
        panel_b.append(
            {
                "panel": "B",
                "item_id": row["id"],
                "series_id": "",
                "label": "",
                "sigma_or_beta_exact": "",
                "log10_K": "",
                "log10_decay_term": "",
                "observable": row["observable"],
                "relation": row["relation"],
                "rate_exact": f"{rate.numerator}/{rate.denominator}",
                "rate_decimal": f"{float(rate):.12f}",
                "classification": row["classification"],
                "claim_type": "PROVED",
            }
        )

    fields = [
        "panel",
        "item_id",
        "series_id",
        "label",
        "sigma_or_beta_exact",
        "log10_K",
        "log10_decay_term",
        "observable",
        "relation",
        "rate_exact",
        "rate_decimal",
        "classification",
        "claim_type",
    ]
    with (HERE / "source-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(panel_a + panel_b)
    return panel_a, panel_b


def render_figure(config: dict, panel_a: list[dict[str, str]], panel_b: list[dict[str, str]]) -> None:
    width = config["width_mm"] * mm
    height = config["height_mm"] * mm
    drawing = Drawing(width, height)
    drawing.add(Rect(0, 0, width, height, fillColor=white, strokeColor=None))

    label(drawing, 14, height - 16, "Temporal observables: miss, detect, or overpay?", 8.5, bold=True)
    label(
        drawing,
        14,
        height - 27,
        "R0.74P exact-family comparison  |  analytic bounds, not simulation  |  NOT CLAY",
        5.2,
        color=MID,
    )
    blossom(drawing, width - 19, height - 18)

    ax, ay, aw, ah = 14, 22, 292, height - 58
    bx, by, bw, bh = 313, 22, width - 327, height - 58
    panel(drawing, ax, ay, aw, ah, "A", "Positive-order window masses lose the target")
    panel(drawing, bx, by, bw, bh, "B", "Exact exponential-rate ledger")

    plot_x = ax + 38
    plot_y = ay + 60
    plot_w = aw - 54
    plot_h = ah - 103
    x_min, x_max = 0.0, 12.0
    y_min, y_max = -12.0, 0.0

    def sx(value: float) -> float:
        return plot_x + (value - x_min) / (x_max - x_min) * plot_w

    def sy(value: float) -> float:
        return plot_y + (value - y_min) / (y_max - y_min) * plot_h

    drawing.add(Rect(plot_x, plot_y, plot_w, plot_h, fillColor=PALE, strokeColor=GRID, strokeWidth=0.65))
    for tick in range(0, 13, 2):
        x = sx(float(tick))
        drawing.add(Line(x, plot_y, x, plot_y + plot_h, strokeColor=GRID, strokeWidth=0.45))
        label(drawing, x, plot_y - 10, str(tick), 5.2, color=MID, anchor="middle")
    for tick in [-12, -9, -6, -3, 0]:
        y = sy(float(tick))
        drawing.add(Line(plot_x, y, plot_x + plot_w, y, strokeColor=GRID, strokeWidth=0.45))
        label(drawing, plot_x - 5, y - 1.8, str(tick), 5.2, color=MID, anchor="end")

    styles = {
        "sigma_1_4": (BLUE, None),
        "sigma_1_2": (GOLD, [5, 2.5]),
        "sigma_ge_1": (PLUM, [1.2, 2.0]),
    }
    direct_labels = {
        "sigma_1_4": "sigma=1/4  [solid]",
        "sigma_1_2": "sigma=1/2  [dash]",
        "sigma_ge_1": "sigma>=1  [dot]",
    }
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in panel_a:
        grouped.setdefault(row["series_id"], []).append(row)
    for series_id in ["sigma_1_4", "sigma_1_2", "sigma_ge_1"]:
        rows = grouped[series_id]
        color, dash = styles[series_id]
        path = ShapePath()
        for index, row in enumerate(rows):
            x = sx(float(row["log10_K"]))
            y = sy(float(row["log10_decay_term"]))
            if index == 0:
                path.moveTo(x, y)
            else:
                path.lineTo(x, y)
        path.strokeColor = color
        path.strokeWidth = 1.35
        path.fillColor = None
        path.strokeDashArray = dash
        drawing.add(path)
        end_y = sy(float(rows[-1]["log10_decay_term"]))
        drawing.add(Rect(plot_x + plot_w - 76, end_y - 5.3, 73, 10.5, fillColor=white, strokeColor=None))
        label(drawing, plot_x + plot_w - 4, end_y - 1.8, direct_labels[series_id], 5.2, color=color, bold=True, anchor="end")

    label(drawing, plot_x + plot_w / 2, plot_y - 21, "log10 K*", 5.5, bold=True, anchor="middle")
    label(drawing, plot_x - 29, plot_y + plot_h + 8, "decay term -beta log10 K*  (additive log10 C suppressed)", 5.2, bold=True)
    label(
        drawing,
        plot_x,
        ay + 25,
        "PROVED:  log10(C_sigma/T*) <= log10 C - beta log10 K*",
        5.2,
        color=BLUE,
        bold=True,
    )
    label(
        drawing,
        plot_x,
        ay + 14,
        "Rate-only curves omit log10 C; fixed sigma>0, nonuniform as sigma -> 0.",
        5.0,
        color=MID,
    )

    inner_x = bx + 8
    table_w = bw - 16
    label(drawing, inner_x, by + bh - 29, "Rate relative to T*, in units a=2m/3", 5.2, color=MID)
    table_top = by + bh - 39
    header_h = 15
    row_h = 25
    col1 = table_w * 0.53
    col2 = table_w * 0.22
    col3 = table_w - col1 - col2
    drawing.add(Rect(inner_x, table_top - header_h, table_w, header_h, fillColor=INK, strokeColor=INK, strokeWidth=0.6))
    label(drawing, inner_x + 5, table_top - 10.2, "observable", 5.2, color=white, bold=True)
    label(drawing, inner_x + col1 + col2 / 2, table_top - 10.2, "rate", 5.2, color=white, bold=True, anchor="middle")
    label(drawing, inner_x + col1 + col2 + col3 / 2, table_top - 10.2, "verdict", 5.2, color=white, bold=True, anchor="middle")

    display_rows = [
        (["window", "sigma=1/4"], "<= -1/4", "misses", BLUE_LIGHT, BLUE),
        (["window", "sigma=1/2"], "<= -1/2", "misses", BLUE_LIGHT, BLUE),
        (["window", "sigma>=1"], "<= -1", "misses", BLUE_LIGHT, BLUE),
        (["matched target", "component v_j"], "= 0", "detects", GOLD_LIGHT, GOLD),
        (["over-weighted", "target lower"], ">= 640/43", "overpays", PLUM_LIGHT, PLUM),
    ]
    assert len(panel_b) == len(display_rows)
    for index, (observable, rate, verdict, fill, accent) in enumerate(display_rows):
        top = table_top - header_h - index * row_h
        bottom = top - row_h
        drawing.add(Rect(inner_x, bottom, table_w, row_h, fillColor=fill, strokeColor=GRID, strokeWidth=0.6))
        drawing.add(Line(inner_x + col1, bottom, inner_x + col1, top, strokeColor=GRID, strokeWidth=0.55))
        drawing.add(Line(inner_x + col1 + col2, bottom, inner_x + col1 + col2, top, strokeColor=GRID, strokeWidth=0.55))
        multiline(drawing, inner_x + 5, top - 8.5, observable, 5.0, leading=6.3)
        label(drawing, inner_x + col1 + col2 / 2, bottom + 8.9, rate, 5.2, color=accent, bold=True, anchor="middle")
        label(drawing, inner_x + col1 + col2 + col3 / 2, bottom + 8.9, verdict, 5.0, color=accent, bold=True, anchor="middle")

    footer_y = table_top - header_h - len(display_rows) * row_h - 12
    multiline(
        drawing,
        inner_x,
        footer_y,
        [
            "Target component only:  v_j ~ T*.",
            "OPEN: no full upper bound for Y2(sf).",
            "The over-weighted lower bound pays Gamma^{-1/2}.",
        ],
        5.0,
        color=MID,
        bold_first=True,
        leading=6.8,
    )

    renderPDF.drawToFile(drawing, str(HERE / "figure.pdf"), title="R0.74P temporal observable triage")
    renderSVG.drawToFile(drawing, str(HERE / "figure.svg"))
    finalize_svg(config)


def finalize_svg(config: dict) -> None:
    """Add physical units and embed the two archived font faces."""
    path = HERE / "figure.svg"
    svg = path.read_text(encoding="utf-8")
    svg, replacements = re.subn(
        r'<svg width="[^"]+" height="[^"]+"',
        f'<svg width="{config["width_mm"]}mm" height="{config["height_mm"]}mm"',
        svg,
        count=1,
    )
    assert replacements == 1
    regular_data = base64.b64encode(REGULAR_FONT.read_bytes()).decode("ascii")
    bold_data = base64.b64encode(BOLD_FONT.read_bytes()).decode("ascii")
    embedded_css = (
        "\n\t<defs><style type=\"text/css\"><![CDATA[\n"
        "@font-face { font-family: 'R074P-Regular'; "
        f"src: url(data:font/ttf;base64,{regular_data}) format('truetype'); }}\n"
        "@font-face { font-family: 'R074P-Bold'; "
        f"src: url(data:font/ttf;base64,{bold_data}) format('truetype'); }}\n"
        "]]></style></defs>"
    )
    svg, replacements = re.subn(r"(\s*</desc>)", r"\1" + embedded_css, svg, count=1)
    assert replacements == 1
    path.write_text(svg, encoding="utf-8")


def render_png(config: dict) -> None:
    if not PDFTOPPM.exists():
        raise FileNotFoundError(PDFTOPPM)
    with tempfile.TemporaryDirectory(prefix="r074p-render-") as temp_dir:
        prefix = Path(temp_dir) / "figure"
        subprocess.run(
            [
                str(PDFTOPPM),
                "-png",
                "-singlefile",
                "-r",
                str(config["dpi"]),
                str(HERE / "figure.pdf"),
                str(prefix),
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        image = Image.open(prefix.with_suffix(".png"))
        image.save(HERE / "figure.png", dpi=(config["dpi"], config["dpi"]))


def main() -> None:
    (HERE / "progress.ndjson").write_text("", encoding="utf-8")
    progress("inputs", "started", "load frozen config and finite certificate")
    config = load_config()
    exact = certificate_values()
    progress("inputs", "complete", "certificate exact-rate bindings verified")

    panel_a, panel_b = generate_source_data(config)
    assert len(panel_a) == 147 and len(panel_b) == 5
    progress("source-data", "complete", "wrote 147 envelope rows and 5 exact ledger rows")

    render_figure(config, panel_a, panel_b)
    progress("vector", "complete", "wrote PDF and SVG vector masters")
    render_png(config)
    progress("raster", "complete", "wrote 600 dpi PNG from PDF master")

    with Image.open(HERE / "figure.png") as image:
        pixel_size = list(image.size)
    version_result = subprocess.run(
        [str(PDFTOPPM), "-v"],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    pdftoppm_version = (version_result.stderr or version_result.stdout).splitlines()[0]
    environment = {
        "schema": "r074p-observable-triage-environment-v1",
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "pillow": PIL.__version__,
        "pypdf": pypdf.__version__,
        "reportlab": REPORTLAB_VERSION,
        "pdftoppm": dependency_label(PDFTOPPM),
        "pdftoppm_version": pdftoppm_version,
        "regular_font": dependency_label(REGULAR_FONT),
        "regular_font_sha256": sha256(REGULAR_FONT),
        "bold_font": dependency_label(BOLD_FONT),
        "bold_font_sha256": sha256(BOLD_FONT),
    }
    write_json(HERE / "environment.json", environment)
    results = {
        "schema": "r074p-observable-triage-results-v1",
        "claim_status": "PROVED analytic comparison; finite rendering only; NOT CLAY",
        "panel_a_rows": len(panel_a),
        "panel_b_rows": len(panel_b),
        "panel_a_formula": "log10(C_sigma/T*) <= log10 C - min(sigma,1) log10 K; plotted decay term suppresses additive log10 C",
        "strong_rate_exact": "640/43",
        "m_exact": str(exact["m_exact"]),
        "K_exponential_rate": str(exact["K_exponential_rate"]),
        "strong_exponential_penalty": str(exact["strong_exponential_penalty"]),
        "pixel_size": pixel_size,
        "certificate_sha256": sha256(CERTIFICATE),
        "source_data_sha256": sha256(HERE / "source-data.csv"),
    }
    write_json(HERE / "results.json", results)
    progress("outputs", "complete", "environment and deterministic result ledger written")
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
