#!/usr/bin/env python3
"""Deterministic producer for Figure R0.74A-1.

The chart is a rendering of closed analytic formulas.  It performs no DNS,
time stepping, parameter fitting, or random sampling.  SVG and PDF share one
vector drawing routine; the archival PNG is a Poppler render of that PDF.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import os
import platform
import resource
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Sequence

import numpy as np
from PIL import Image, ImageOps, __version__ as PILLOW_VERSION
from reportlab import Version as REPORTLAB_VERSION
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor


PACKAGE = Path(__file__).resolve().parent
CONFIG_PATH = PACKAGE / "config.json"
MM_TO_PT = 72.0 / 25.4
BLUE = "#356A93"
AMBER = "#B66D35"
INK = "#252B30"
MUTED = "#66717C"
GRID = "#D9DDE1"
PAPER = "#FCFBF7"
WHITE = "#FFFFFF"


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


class RunLog:
    def __init__(self) -> None:
        self.started = time.perf_counter()
        self.progress: list[dict[str, object]] = []
        self.resources: list[dict[str, object]] = []

    def event(self, stage: str, status: str, detail: str) -> None:
        elapsed = time.perf_counter() - self.started
        record = {
            "elapsedSeconds": round(elapsed, 6),
            "stage": stage,
            "status": status,
            "timestampUtc": utc_now(),
            "detail": detail,
        }
        self.progress.append(record)
        usage = resource.getrusage(resource.RUSAGE_SELF)
        self.resources.append(
            {
                "elapsedSeconds": round(elapsed, 6),
                "stage": stage,
                "userCpuSeconds": round(usage.ru_utime, 6),
                "systemCpuSeconds": round(usage.ru_stime, 6),
                "maximumResidentSetRaw": int(usage.ru_maxrss),
                "maximumResidentSetUnit": "bytes on macOS; KiB on Linux",
            }
        )
        print(f"[{elapsed:8.3f}s] {stage}: {status} — {detail}", flush=True)

    def write(self) -> None:
        for path, rows in (
            (PACKAGE / "progress.ndjson", self.progress),
            (PACKAGE / "resource-log.ndjson", self.resources),
        ):
            text = "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows)
            path.write_text(text, encoding="utf-8", newline="\n")


def repository_root() -> Path:
    value = subprocess.check_output(
        ["git", "rev-parse", "--show-toplevel"], cwd=PACKAGE, text=True
    ).strip()
    return Path(value).resolve()


def verify_source_binding(config: dict[str, object]) -> tuple[Path, str]:
    root = repository_root()
    binding = config["sourceBinding"]
    assert isinstance(binding, dict)
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
    expected_head = str(binding["commit"])
    if head != expected_head:
        raise RuntimeError(f"source commit mismatch: {head} != {expected_head}")
    files = binding["files"]
    assert isinstance(files, dict)
    for relative, expected_hash in files.items():
        actual = sha256_file(root / relative)
        if actual != expected_hash:
            raise RuntimeError(f"source hash mismatch for {relative}: {actual} != {expected_hash}")
    certificate = json.loads((root / "research/r074a_localized_kd_certificate.json").read_text(encoding="utf-8"))
    if certificate.get("status") != "PASS":
        raise RuntimeError("bound localized K_D certificate is not PASS")
    if certificate.get("summary") != binding["certificateSummary"]:
        raise RuntimeError("certificate 21/21 summary mismatch")
    return root, head


def fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    return format(value, ".17g")


CSV_FIELDS = [
    "panel",
    "sample_index",
    "theta",
    "cc_weight",
    "ec_weight",
    "ce_weight",
    "ee_weight",
    "j",
    "N",
    "epsilon_N",
    "KD_lower_bound_exponent_factor",
    "old_cubic_N_factor",
    "gradient_energy_N_factor",
    "delta",
    "old_cubic_delta_factor",
    "U_ext_infinity_delta_factor",
    "normalization",
    "analytic_formula",
    "claim_qualifier",
]


def build_rows(config: dict[str, object]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    panel_a = config["panelA"]
    panel_b = config["panelB"]
    panel_c = config["panelC"]
    assert isinstance(panel_a, dict) and isinstance(panel_b, dict) and isinstance(panel_c, dict)

    theta_minimum = float(panel_a["thetaMinimum"])
    theta_maximum = float(panel_a["thetaMaximum"])
    theta_points = int(panel_a["points"])
    theta_ratio = theta_maximum / theta_minimum
    for zero_index in range(theta_points):
        theta = theta_minimum * theta_ratio ** (zero_index / (theta_points - 1))
        quarter = theta ** 0.25
        row = {key: "" for key in CSV_FIELDS}
        row.update(
            {
                "panel": "A",
                "sample_index": str(zero_index + 1),
                "theta": fmt(theta),
                "cc_weight": fmt(quarter),
                "ec_weight": fmt(quarter),
                "ce_weight": fmt(theta),
                "ee_weight": fmt(theta),
                "normalization": "A_c=B_c=U_ext=D_ext=1; unknown theorem constant C suppressed",
                "analytic_formula": "w_cc=w_ec=theta^(1/4); w_ce=w_ee=theta",
                "claim_qualifier": "normalized analytic upper-bound weights; C is not plotted; finite rows do not prove quantifiers; NOT CLAY",
            }
        )
        rows.append(row)

    for index, j in enumerate(
        range(int(panel_b["indexMinimum"]), int(panel_b["indexMaximum"]) + 1), start=1
    ):
        n = 2**j
        epsilon = n ** (-2.0 / 3.0)
        kd_factor = n**0
        old_factor = n**-2
        gradient_factor = n ** (2.0 / 3.0)
        row = {key: "" for key in CSV_FIELDS}
        row.update(
            {
                "panel": "B",
                "sample_index": str(index),
                "j": str(j),
                "N": str(n),
                "epsilon_N": fmt(epsilon),
                "KD_lower_bound_exponent_factor": str(kd_factor),
                "old_cubic_N_factor": fmt(old_factor),
                "gradient_energy_N_factor": fmt(gradient_factor),
                "normalization": "N=2^j; epsilon_N=N^(-2/3); unknown positive lower-bound constant c suppressed",
                "analytic_formula": "epsilon^3*N^2=N^0; epsilon^3=N^(-2); epsilon^2*N^2=N^(2/3)",
                "claim_qualifier": "function-level packet, not an unforced NSE trajectory; no simulation/DNS; finite rows do not prove quantifiers; NOT CLAY",
            }
        )
        rows.append(row)

    minimum = float(panel_c["deltaMinimum"])
    maximum = float(panel_c["deltaMaximum"])
    points = int(panel_c["points"])
    ratio = maximum / minimum
    for zero_index in range(points):
        delta = minimum * ratio ** (zero_index / (points - 1))
        old_factor = delta**0
        endpoint_factor = delta ** (-2.0 / 3.0)
        row = {key: "" for key in CSV_FIELDS}
        row.update(
            {
                "panel": "C",
                "sample_index": str(zero_index + 1),
                "delta": fmt(delta),
                "old_cubic_delta_factor": str(old_factor),
                "U_ext_infinity_delta_factor": fmt(endpoint_factor),
                "normalization": "spike length delta; amplitude delta^(-1/3)",
                "analytic_formula": "old cubic=delta*delta^(-1)=delta^0; U_ext^infinity=delta^(-2/3)",
                "claim_qualifier": "separate finite energy-class field for each delta; no uniform global L_t^infinity L_x^2; not an unforced NSE trajectory; no simulation/DNS; finite rows do not prove quantifiers; NOT CLAY",
            }
        )
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str]]) -> None:
    with (PACKAGE / "source-data.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


class SVGBackend:
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.items: list[str] = []

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str = "none", stroke: str = "none", width: float = 0.0) -> None:
        self.items.append(
            f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{width:.3f}"/>'
        )

    def line(self, x1: float, y1: float, x2: float, y2: float, *, color: str = INK, width: float = 0.7, dash: Sequence[float] | None = None) -> None:
        attr = "" if not dash else f' stroke-dasharray="{",".join(f"{v:.2f}" for v in dash)}"'
        self.items.append(
            f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{width:.3f}" stroke-linecap="round"{attr}/>'
        )

    def polyline(self, points: Sequence[tuple[float, float]], *, color: str, width: float, dash: Sequence[float] | None = None) -> None:
        values = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
        attr = "" if not dash else f' stroke-dasharray="{",".join(f"{v:.2f}" for v in dash)}"'
        self.items.append(
            f'<polyline points="{values}" fill="none" stroke="{color}" stroke-width="{width:.3f}" stroke-linecap="round" stroke-linejoin="round"{attr}/>'
        )

    def text(self, x: float, y: float, value: str, *, size: float = 6.0, color: str = INK, anchor: str = "start", bold: bool = False, italic: bool = False) -> None:
        weight = "700" if bold else "400"
        style = "italic" if italic else "normal"
        self.items.append(
            f'<text x="{x:.3f}" y="{y:.3f}" fill="{color}" font-family="Helvetica,Arial,sans-serif" font-size="{size:.3f}" font-weight="{weight}" font-style="{style}" text-anchor="{anchor}">{html.escape(value)}</text>'
        )

    def circle(self, x: float, y: float, radius: float, *, fill: str, stroke: str = "none", width: float = 0.0) -> None:
        self.items.append(
            f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{radius:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{width:.3f}"/>'
        )

    def polygon(self, points: Sequence[tuple[float, float]], *, fill: str, stroke: str = "none", width: float = 0.0) -> None:
        values = " ".join(f"{x:.3f},{y:.3f}" for x, y in points)
        self.items.append(
            f'<polygon points="{values}" fill="{fill}" stroke="{stroke}" stroke-width="{width:.3f}"/>'
        )

    def save(self, path: Path) -> None:
        body = "\n  ".join(self.items)
        document = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            f'<svg xmlns="http://www.w3.org/2000/svg" width="178mm" height="74mm" viewBox="0 0 {self.width:.12f} {self.height:.12f}">\n'
            "  <title>R0.74A localized K_D payments</title>\n"
            "  <desc>Three vector panels of closed exponent factors; function-level packets are not unforced NSE trajectories.</desc>\n"
            f"  {body}\n</svg>\n"
        )
        path.write_text(document, encoding="utf-8", newline="\n")


class PDFBackend:
    def __init__(self, path: Path, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.canvas = canvas.Canvas(
            str(path), pagesize=(width, height), pageCompression=1, invariant=1
        )
        self.canvas.setTitle("R0.74A localized K_D payments")
        self.canvas.setAuthor("C. K. Zeng")
        self.canvas.setCreator("R0.74A deterministic vector producer")
        self.canvas.setSubject("Function-level exponent ledgers; no simulation; NOT CLAY")

    def _y(self, y: float) -> float:
        return self.height - y

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str = "none", stroke: str = "none", width: float = 0.0) -> None:
        self.canvas.saveState()
        self.canvas.setLineWidth(width)
        self.canvas.setFillColor(HexColor(fill if fill != "none" else WHITE))
        self.canvas.setStrokeColor(HexColor(stroke if stroke != "none" else WHITE))
        self.canvas.rect(x, self.height - y - h, w, h, fill=int(fill != "none"), stroke=int(stroke != "none"))
        self.canvas.restoreState()

    def line(self, x1: float, y1: float, x2: float, y2: float, *, color: str = INK, width: float = 0.7, dash: Sequence[float] | None = None) -> None:
        self.canvas.saveState()
        self.canvas.setStrokeColor(HexColor(color))
        self.canvas.setLineWidth(width)
        self.canvas.setLineCap(1)
        self.canvas.setDash(list(dash) if dash else [])
        self.canvas.line(x1, self._y(y1), x2, self._y(y2))
        self.canvas.restoreState()

    def polyline(self, points: Sequence[tuple[float, float]], *, color: str, width: float, dash: Sequence[float] | None = None) -> None:
        self.canvas.saveState()
        self.canvas.setStrokeColor(HexColor(color))
        self.canvas.setLineWidth(width)
        self.canvas.setLineCap(1)
        self.canvas.setLineJoin(1)
        self.canvas.setDash(list(dash) if dash else [])
        path = self.canvas.beginPath()
        x0, y0 = points[0]
        path.moveTo(x0, self._y(y0))
        for x, y in points[1:]:
            path.lineTo(x, self._y(y))
        self.canvas.drawPath(path, fill=0, stroke=1)
        self.canvas.restoreState()

    def text(self, x: float, y: float, value: str, *, size: float = 6.0, color: str = INK, anchor: str = "start", bold: bool = False, italic: bool = False) -> None:
        if bold and italic:
            font = "Helvetica-BoldOblique"
        elif bold:
            font = "Helvetica-Bold"
        elif italic:
            font = "Helvetica-Oblique"
        else:
            font = "Helvetica"
        self.canvas.saveState()
        self.canvas.setFillColor(HexColor(color))
        self.canvas.setFont(font, size)
        draw = {"start": self.canvas.drawString, "middle": self.canvas.drawCentredString, "end": self.canvas.drawRightString}[anchor]
        draw(x, self._y(y), value)
        self.canvas.restoreState()

    def circle(self, x: float, y: float, radius: float, *, fill: str, stroke: str = "none", width: float = 0.0) -> None:
        self.canvas.saveState()
        self.canvas.setFillColor(HexColor(fill))
        self.canvas.setStrokeColor(HexColor(stroke if stroke != "none" else fill))
        self.canvas.setLineWidth(width)
        self.canvas.circle(x, self._y(y), radius, fill=1, stroke=int(stroke != "none"))
        self.canvas.restoreState()

    def polygon(self, points: Sequence[tuple[float, float]], *, fill: str, stroke: str = "none", width: float = 0.0) -> None:
        self.canvas.saveState()
        self.canvas.setFillColor(HexColor(fill))
        self.canvas.setStrokeColor(HexColor(stroke if stroke != "none" else fill))
        self.canvas.setLineWidth(width)
        path = self.canvas.beginPath()
        x0, y0 = points[0]
        path.moveTo(x0, self._y(y0))
        for x, y in points[1:]:
            path.lineTo(x, self._y(y))
        path.close()
        self.canvas.drawPath(path, fill=1, stroke=int(stroke != "none"))
        self.canvas.restoreState()

    def save(self, path: Path) -> None:
        del path
        self.canvas.showPage()
        self.canvas.save()


def marker(backend: SVGBackend | PDFBackend, shape: str, x: float, y: float, color: str, size: float = 1.65) -> None:
    if shape == "circle":
        backend.circle(x, y, size, fill=PAPER, stroke=color, width=0.8)
    elif shape == "square":
        backend.rect(x - size, y - size, 2 * size, 2 * size, fill=PAPER, stroke=color, width=0.8)
    elif shape == "triangle":
        backend.polygon(
            [(x, y - size * 1.2), (x - size * 1.05, y + size * 0.8), (x + size * 1.05, y + size * 0.8)],
            fill=PAPER,
            stroke=color,
            width=0.8,
        )


def map_linear(value: float, low: float, high: float, start: float, end: float) -> float:
    return start + (value - low) * (end - start) / (high - low)


def map_log(value: float, low: float, high: float, start: float, end: float) -> float:
    return map_linear(math.log(value), math.log(low), math.log(high), start, end)


def axes(
    backend: SVGBackend | PDFBackend,
    left: float,
    top: float,
    right: float,
    bottom: float,
    x_ticks: Sequence[tuple[float, str]],
    y_ticks_left: Sequence[tuple[float, str]],
    *,
    y_ticks_right: Sequence[tuple[float, str]] = (),
    x_label: str,
    left_label: str,
    right_label: str = "",
) -> None:
    for y, label in y_ticks_left:
        backend.line(left, y, right, y, color=GRID, width=0.45)
        backend.text(left - 3.2, y + 1.8, label, size=4.55, color=MUTED, anchor="end")
    backend.line(left, top, left, bottom, color=INK, width=0.65)
    backend.line(left, bottom, right, bottom, color=INK, width=0.65)
    if y_ticks_right:
        backend.line(right, top, right, bottom, color=INK, width=0.65)
        for y, label in y_ticks_right:
            backend.text(right + 3.2, y + 1.8, label, size=4.55, color=MUTED, anchor="start")
    for x, label in x_ticks:
        backend.line(x, bottom, x, bottom + 2.3, color=INK, width=0.55)
        backend.text(x, bottom + 8.0, label, size=4.45, color=MUTED, anchor="middle")
    backend.text((left + right) / 2, bottom + 15.0, x_label, size=5.0, color=INK, anchor="middle")
    backend.text(left, top - 4.0, left_label, size=4.7, color=MUTED)
    if right_label:
        backend.text(right, top - 4.0, right_label, size=4.7, color=MUTED, anchor="end")


def draw_blossom(backend: SVGBackend | PDFBackend, x: float, y: float) -> None:
    for index in range(6):
        angle = math.pi * index / 3.0
        px = x + 4.4 * math.cos(angle)
        py = y + 4.4 * math.sin(angle)
        backend.line(x, y, px, py, color=GRID, width=0.55)
        backend.circle(px, py, 1.12, fill=BLUE if index % 2 == 0 else AMBER)
    backend.circle(x, y, 1.3, fill=INK)


def panel_heading(backend: SVGBackend | PDFBackend, x: float, letter: str, title: str, subtitle: str) -> None:
    backend.text(x, 35.0, letter, size=8.4, bold=True)
    backend.text(x + 11.5, 35.0, title, size=6.6, bold=True)
    backend.text(x + 11.5, 45.0, subtitle, size=4.65, color=MUTED)


def draw_figure(backend: SVGBackend | PDFBackend, rows: list[dict[str, str]], width: float, height: float) -> None:
    backend.rect(0, 0, width, height, fill=PAPER)
    backend.text(20, 14.0, "R0.74A | Localized K_D payments and obstruction ledgers", size=9.1, bold=True)
    backend.text(20, 24.3, "Closed exponent factors from the proved size lemma and two function-level examples.", size=5.5, color=MUTED)
    draw_blossom(backend, width - 18.5, 15.0)

    panel_width = 146.0
    panel_x = [20.0, 179.3, 338.6]
    plot_top = 58.0
    plot_bottom = 158.0
    plot_left_offsets = [27.0, 27.0, 27.0]
    plot_right_offsets = [8.0, 8.0, 8.0]

    # Panel A
    x0 = panel_x[0]
    panel_heading(backend, x0, "A", "Four-block scale weights", "A_c=B_c=U_ext=D_ext=1; C suppressed, not plotted")
    left = x0 + plot_left_offsets[0]
    right = x0 + panel_width - plot_right_offsets[0]
    theta_min, theta_max = 1e-4, 1.0
    a_ticks = (1e-4, 1e-3, 1e-2, 1e-1, 1.0)
    x_ticks_a = [(map_log(value, theta_min, theta_max, left, right), f"1e{int(math.log10(value))}" if value < 1 else "1") for value in a_ticks]
    y_ticks_a = [(map_log(value, theta_min, theta_max, plot_bottom, plot_top), f"1e{int(math.log10(value))}" if value < 1 else "1") for value in a_ticks]
    axes(backend, left, plot_top, right, plot_bottom, x_ticks_a, y_ticks_a, x_label="heat fraction theta (log)", left_label="payment weight (log)")
    a_rows = [row for row in rows if row["panel"] == "A"]
    quarter_points = [
        (
            map_log(float(row["theta"]), theta_min, theta_max, left, right),
            map_log(float(row["cc_weight"]), theta_min, theta_max, plot_bottom, plot_top),
        )
        for row in a_rows
    ]
    linear_points = [
        (
            map_log(float(row["theta"]), theta_min, theta_max, left, right),
            map_log(float(row["ce_weight"]), theta_min, theta_max, plot_bottom, plot_top),
        )
        for row in a_rows
    ]
    backend.polyline(quarter_points, color=BLUE, width=1.45)
    backend.polyline(linear_points, color=AMBER, width=1.25, dash=(4.0, 2.4))
    for point_index in (0, 30, 60, 90, 120):
        marker(backend, "circle", *quarter_points[point_index], BLUE)
        marker(backend, "square", *linear_points[point_index], AMBER, size=1.4)
    backend.text(left + 3.0, plot_top + 9.0, "cc/ec: theta^(1/4)", size=4.9, color=BLUE, bold=True)
    backend.text(right - 2, linear_points[73][1] + 8.0, "ce/ee: theta", size=4.9, color=AMBER, anchor="end", bold=True)

    # Panel B
    x0 = panel_x[1]
    panel_heading(backend, x0, "B", "Exterior frequency packet", "N=2^j; epsilon_N=N^(-2/3); c suppressed, not plotted")
    left = x0 + plot_left_offsets[1]
    right = x0 + panel_width - plot_right_offsets[1]
    j_ticks = (1, 4, 8, 12, 16, 20, 24)
    x_ticks_b = [(map_linear(j, 1, 24, left, right), f"2^{j}") for j in j_ticks]
    b_y_min, b_y_max = 1e-15, 1e5
    b_y_ticks = [(map_log(value, b_y_min, b_y_max, plot_bottom, plot_top), label) for value, label in ((1e-15, "1e-15"), (1e-10, "1e-10"), (1e-5, "1e-5"), (1.0, "1"), (1e5, "1e5"))]
    axes(backend, left, plot_top, right, plot_bottom, x_ticks_b, b_y_ticks, x_label="frequency N=2^j (log2)", left_label="exponent factor (log)")
    b_rows = [row for row in rows if row["panel"] == "B"]
    def b_points(field: str) -> list[tuple[float, float]]:
        return [(map_linear(float(row["j"]), 1, 24, left, right), map_log(float(row[field]), b_y_min, b_y_max, plot_bottom, plot_top)) for row in b_rows]

    kd_points = b_points("KD_lower_bound_exponent_factor")
    old_n_points = b_points("old_cubic_N_factor")
    gradient_points = b_points("gradient_energy_N_factor")
    backend.polyline(kd_points, color=BLUE, width=1.45)
    backend.polyline(old_n_points, color=AMBER, width=1.25, dash=(4.0, 2.4))
    backend.polyline(gradient_points, color=INK, width=1.15, dash=(1.2, 2.0))
    for point_index in (0, 5, 11, 17, 23):
        marker(backend, "circle", *kd_points[point_index], BLUE)
        marker(backend, "square", *old_n_points[point_index], AMBER, size=1.25)
        marker(backend, "triangle", *gradient_points[point_index], INK, size=1.25)
    backend.text(left + 3.0, plot_top + 9.0, "gradient: N^(2/3)", size=4.75, color=INK, bold=True)
    backend.text(right - 2.0, kd_points[-1][1] - 4.0, "K_D factor: N^0", size=4.75, color=BLUE, anchor="end", bold=True)
    backend.text(left + 3.0, plot_bottom - 8.0, "old cubic: N^-2", size=4.75, color=AMBER, bold=True)

    # Panel C
    x0 = panel_x[2]
    panel_heading(backend, x0, "C", "Exterior time spike", "each delta is separate; no uniform global Linf_t L2_x")
    left = x0 + plot_left_offsets[2]
    right = x0 + panel_width - plot_right_offsets[2]
    c_min, c_max = 1e-6, 1.0
    c_ticks = (1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1, 1.0)
    x_ticks_c = [(map_log(value, c_min, c_max, left, right), f"1e{int(math.log10(value))}" if value < 1 else "1") for value in c_ticks]
    c_y_min, c_y_max = 1.0, 1e4
    c_y_ticks = [(map_log(value, c_y_min, c_y_max, plot_bottom, plot_top), label) for value, label in ((1.0, "1"), (10.0, "10"), (1e2, "1e2"), (1e3, "1e3"), (1e4, "1e4"))]
    axes(backend, left, plot_top, right, plot_bottom, x_ticks_c, c_y_ticks, x_label="spike length delta (log)", left_label="exponent factor (log)")
    c_rows = [row for row in rows if row["panel"] == "C"]

    def c_points(field: str) -> list[tuple[float, float]]:
        return [(map_log(float(row["delta"]), c_min, c_max, left, right), map_log(float(row[field]), c_y_min, c_y_max, plot_bottom, plot_top)) for row in c_rows]

    endpoint_points = c_points("U_ext_infinity_delta_factor")
    old_delta_points = c_points("old_cubic_delta_factor")
    backend.polyline(endpoint_points, color=BLUE, width=1.45)
    backend.polyline(old_delta_points, color=AMBER, width=1.25, dash=(4.0, 2.4))
    for point_index in (0, 30, 60, 90, 120):
        marker(backend, "circle", *endpoint_points[point_index], BLUE)
        marker(backend, "square", *old_delta_points[point_index], AMBER, size=1.4)
    backend.text(right - 2.0, plot_top + 9.0, "U_ext^infinity: delta^(-2/3)", size=4.75, color=BLUE, anchor="end", bold=True)
    backend.text(left + 3.0, plot_bottom - 8.0, "old cubic: delta^0", size=4.75, color=AMBER, bold=True)

    backend.line(20.0, 184.0, width - 20.0, 184.0, color=GRID, width=0.6)
    backend.text(20.0, 194.0, "Function-level packets, not unforced NSE trajectories • no simulation/DNS • finite rows do not prove quantifiers", size=4.75, color=MUTED)
    backend.text(width - 20.0, 194.0, "NOT CLAY", size=5.2, color=INK, anchor="end", bold=True)
    backend.text(20.0, 203.0, "Source-bound: 391debac9d48158ab4b0f90edf873150849e6e57", size=4.25, color=MUTED)


def render_vector(rows: list[dict[str, str]], config: dict[str, object]) -> None:
    width = float(config["widthMillimetres"]) * MM_TO_PT
    height = float(config["heightMillimetres"]) * MM_TO_PT
    svg = SVGBackend(width, height)
    draw_figure(svg, rows, width, height)
    svg.save(PACKAGE / "figure.svg")
    pdf = PDFBackend(PACKAGE / "figure.pdf", width, height)
    draw_figure(pdf, rows, width, height)
    pdf.save(PACKAGE / "figure.pdf")


def poppler_render(pdf_path: Path, output_path: Path, dpi: int) -> None:
    command = shutil.which("pdftoppm")
    if command is None:
        raise RuntimeError("pdftoppm is required for deterministic PDF raster QA")
    with tempfile.TemporaryDirectory(prefix="r074a-poppler-") as temp_dir:
        prefix = Path(temp_dir) / "page"
        subprocess.run(
            [command, "-f", "1", "-singlefile", "-png", "-r", str(dpi), str(pdf_path), str(prefix)],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        rendered = prefix.with_suffix(".png")
        with Image.open(rendered) as image:
            rgb = image.convert("RGB")
            rgb.save(output_path, format="PNG", dpi=(dpi, dpi), compress_level=9, optimize=False)


def render_rasters(config: dict[str, object]) -> None:
    pdf_path = PACKAGE / "figure.pdf"
    png_dpi = int(config["pngDpi"])
    qa_dpi = int(config["qaDpi"])
    poppler_render(pdf_path, PACKAGE / "figure.png", png_dpi)
    poppler_render(pdf_path, PACKAGE / "qa-pdf.png", qa_dpi)
    with Image.open(PACKAGE / "qa-pdf.png") as qa_image:
        qa_size = qa_image.size
    with Image.open(PACKAGE / "figure.png") as archival:
        final_size = archival.convert("RGB").resize(qa_size, Image.Resampling.LANCZOS)
        final_size.save(PACKAGE / "qa-final-size.png", format="PNG", dpi=(qa_dpi, qa_dpi), compress_level=9, optimize=False)
        grayscale = ImageOps.grayscale(final_size)
        grayscale.save(PACKAGE / "qa-grayscale.png", format="PNG", dpi=(qa_dpi, qa_dpi), compress_level=9, optimize=False)


def write_results(rows: list[dict[str, str]], config: dict[str, object]) -> None:
    a_rows = [row for row in rows if row["panel"] == "A"]
    b_rows = [row for row in rows if row["panel"] == "B"]
    c_rows = [row for row in rows if row["panel"] == "C"]
    results = {
        "claimBoundary": {
            "finiteRowsProveQuantifiers": False,
            "functionLevelPacketsAreUnforcedNseTrajectories": False,
            "normalizedAnalyticConsequences": True,
            "notClay": True,
            "simulation": False,
            "timeSpikeUniformGlobalLinfL2": False,
            "unknownConstantsPlotted": False,
        },
        "figureId": config["figureId"],
        "formulas": {
            "A": "A_c=B_c=U_ext=D_ext=1; cc=ec=theta^(1/4); ce=ee=theta; C suppressed",
            "B": "N=2^j; epsilon=N^(-2/3); K_D factor=N^0; old cubic=N^(-2); gradient energy=N^(2/3); c suppressed",
            "C": "spike amplitude=delta^(-1/3); old cubic=delta^0; U_ext^infinity=delta^(-2/3)",
        },
        "panelA": {
            "quarterWeightMinimumDisplayed": min(float(row["cc_weight"]) for row in a_rows),
            "linearWeightMinimumDisplayed": min(float(row["ce_weight"]) for row in a_rows),
            "rows": len(a_rows),
            "unknownConstantPlotted": False,
        },
        "panelB": {
            "gradientEnergyMaximumDisplayed": max(float(row["gradient_energy_N_factor"]) for row in b_rows),
            "kdExponentFactor": 1,
            "oldCubicMinimumDisplayed": min(float(row["old_cubic_N_factor"]) for row in b_rows),
            "rows": len(b_rows),
            "unknownConstantPlotted": False,
        },
        "panelC": {
            "endpointMaximumDisplayed": max(float(row["U_ext_infinity_delta_factor"]) for row in c_rows),
            "oldCubicExponentFactor": 1,
            "rows": len(c_rows),
            "separateFiniteFieldPerDelta": True,
            "uniformGlobalLinfL2": False,
        },
        "rowCount": len(rows),
        "sourceBinding": config["sourceBinding"],
        "status": "PASS",
    }
    (PACKAGE / "results.json").write_text(canonical_json(results), encoding="utf-8", newline="\n")


def write_environment(config: dict[str, object], head: str) -> None:
    pdftoppm_path = shutil.which("pdftoppm")
    environment = {
        "compute": {
            "dgxUsed": False,
            "execution": "local CPU",
            "networkUsed": False,
            "randomnessUsed": False,
        },
        "machine": platform.machine(),
        "numpy": np.__version__,
        "operatingSystem": platform.platform(),
        "pdfRenderer": pdftoppm_path,
        "pillow": PILLOW_VERSION,
        "python": platform.python_version(),
        "reportlab": REPORTLAB_VERSION,
        "sourceCommit": head,
        "sourceDateEpoch": int(config["sourceDateEpoch"]),
    }
    (PACKAGE / "environment.json").write_text(canonical_json(environment), encoding="utf-8", newline="\n")


def produce() -> None:
    log = RunLog()
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    log.event("configuration", "PASS", "loaded deterministic figure contract")
    root, head = verify_source_binding(config)
    log.event("source-binding", "PASS", f"verified {head}, six frozen source hashes, and certificate 21/21")
    rows = build_rows(config)
    if len(rows) != 266:
        raise RuntimeError(f"unexpected row count: {len(rows)}")
    write_csv(rows)
    log.event("source-data", "PASS", "wrote 266 closed-form rows (121 + 24 + 121)")
    render_vector(rows, config)
    log.event("vector-render", "PASS", "wrote shared-coordinate SVG and one-page PDF")
    render_rasters(config)
    log.event("raster-render", "PASS", "wrote 600 dpi archival PNG and 300 dpi QA renders")
    write_results(rows, config)
    write_environment(config, head)
    log.event("results", "PASS", f"wrote deterministic results and local environment from {root}")
    log.event("complete", "PASS", "figure production completed; validation remains independent")
    log.write()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--render", action="store_true", help="render all formula, vector, raster, and observability outputs")
    args = parser.parse_args()
    if not args.render:
        parser.error("--render is required")
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1788252873")
    os.environ.setdefault("PYTHONHASHSEED", "0")
    produce()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
