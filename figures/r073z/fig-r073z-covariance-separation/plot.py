#!/usr/bin/env python3
"""Deterministic producer for Figure R0.73Z-1.

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
from fractions import Fraction
from pathlib import Path
from typing import Iterable, Sequence

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
TOLERANCE = 5e-13


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
    certificate = json.loads((root / "research/r073z_covariance_certificate.json").read_text(encoding="utf-8"))
    if certificate.get("status") != "PASS":
        raise RuntimeError("bound covariance certificate is not PASS")
    if certificate.get("payload_sha256") != binding["certificatePayloadSha256"]:
        raise RuntimeError("certificate payload SHA-256 mismatch")
    return root, head


def fmt(value: float) -> str:
    if value == 0.0:
        return "0"
    return format(value, ".17g")


CSV_FIELDS = [
    "panel",
    "sample_index",
    "n",
    "J",
    "s",
    "r_exp_minus_s",
    "energy_over_pi_cubed",
    "D32_lower_bound_frequency_factor",
    "l2_partial_sum",
    "l2_partial_sum_exact",
    "l2_limit_exact",
    "lacunary_unit_term",
    "lacunary_partial_lower_sum",
    "Pi_s",
    "centered_S_s",
    "D_s",
    "Q_s_magnitude",
    "div_Q_s",
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

    for index, n in enumerate(
        range(int(panel_a["frequencyMinimum"]), int(panel_a["frequencyMaximum"]) + 1), start=1
    ):
        row = {key: "" for key in CSV_FIELDS}
        row.update(
            {
                "panel": "A",
                "sample_index": str(index),
                "n": str(n),
                "energy_over_pi_cubed": "6",
                "D32_lower_bound_frequency_factor": str(n),
                "normalization": "energy divided by pi^3; fixed geometry constant c suppressed",
                "analytic_formula": "E_n/pi^3=6; lower-bound factor in c*n equals n",
                "claim_qualifier": "normalized analytic consequence; finite rows do not prove the quantified bound; NOT CLAY",
            }
        )
        rows.append(row)

    for index, j in enumerate(
        range(int(panel_b["indexMinimum"]), int(panel_b["indexMaximum"]) + 1), start=1
    ):
        exact = Fraction(1, 3) * (1 - Fraction(1, 4**j))
        row = {key: "" for key in CSV_FIELDS}
        row.update(
            {
                "panel": "B",
                "sample_index": str(index),
                "J": str(j),
                "l2_partial_sum": fmt(float(exact)),
                "l2_partial_sum_exact": f"{exact.numerator}/{exact.denominator}",
                "l2_limit_exact": "1/3",
                "lacunary_unit_term": "1",
                "lacunary_partial_lower_sum": str(j),
                "normalization": "N_j=8^j; a_j=2^(-j)=N_j^(-1/3)",
                "analytic_formula": "S_J=(1-4^(-J))/3; a_j^3*N_j=1; sum_{j<=J}1=J",
                "claim_qualifier": "exact rational evaluation; finite display is not the divergence proof; NOT CLAY",
            }
        )
        rows.append(row)

    minimum = float(panel_c["heatScaleMinimum"])
    maximum = float(panel_c["heatScaleMaximum"])
    points = int(panel_c["points"])
    ratio = maximum / minimum
    for index in range(points):
        s = minimum * ratio ** (index / (points - 1))
        r = math.exp(-s)
        d_s = (1.0 - r * r) * (1.0 + 0.5 * r * r)
        q_base = r**3 - r**5
        q_magnitude = math.sqrt(6.0) * q_base / 8.0
        div_q = 3.0 * q_base / 4.0
        row = {key: "" for key in CSV_FIELDS}
        row.update(
            {
                "panel": "C",
                "sample_index": str(index + 1),
                "s": fmt(s),
                "r_exp_minus_s": fmt(r),
                "Pi_s": "0",
                "centered_S_s": "0",
                "D_s": fmt(d_s),
                "Q_s_magnitude": fmt(q_magnitude),
                "div_Q_s": fmt(div_q),
                "normalization": "A=B=n=1; t=t_*; x1=x2=pi/3; r=exp(-s)",
                "analytic_formula": "D=(1-r^2)*(1+r^2/2); |Q|=sqrt(6)*(r^3-r^5)/8; divQ=3*(r^3-r^5)/4",
                "claim_qualifier": "normalized analytic consequence; positivity is proved by formula, not finite sampling; NOT CLAY",
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
            "  <title>R0.73Z covariance separation</title>\n"
            "  <desc>Three vector panels of normalized analytic consequences; finite rows are not proof.</desc>\n"
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
        self.canvas.setTitle("R0.73Z covariance separation")
        self.canvas.setAuthor("C. K. Zeng")
        self.canvas.setCreator("R0.73Z deterministic vector producer")
        self.canvas.setSubject("Normalized analytic consequences; NOT CLAY")

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
    backend.text(20, 14.0, "R0.73Z | Covariance separation and endpoint obstruction", size=9.1, bold=True)
    backend.text(20, 24.3, "Closed-form normalized consequences; finite plotted rows are not proofs.", size=5.5, color=MUTED)
    draw_blossom(backend, width - 18.5, 15.0)

    panel_width = 146.0
    panel_x = [20.0, 179.3, 338.6]
    plot_top = 58.0
    plot_bottom = 158.0
    plot_left_offsets = [27.0, 27.0, 27.0]
    plot_right_offsets = [8.0, 14.0, 14.0]

    # Panel A
    x0 = panel_x[0]
    panel_heading(backend, x0, "A", "Initial-endpoint frequency", "E/pi^3 = 6; plotted bound factor = n in c n")
    left = x0 + plot_left_offsets[0]
    right = x0 + panel_width - plot_right_offsets[0]
    x_ticks_a = [(map_log(n, 1, 64, left, right), str(n)) for n in (1, 2, 4, 8, 16, 32, 64)]
    y_ticks_a = [(map_linear(v, 0, 64, plot_bottom, plot_top), str(v)) for v in (0, 16, 32, 48, 64)]
    axes(backend, left, plot_top, right, plot_bottom, x_ticks_a, y_ticks_a, x_label="frequency n (log2)", left_label="normalized units")
    a_rows = [row for row in rows if row["panel"] == "A"]
    frequency_points = [
        (
            map_log(float(row["n"]), 1, 64, left, right),
            map_linear(float(row["D32_lower_bound_frequency_factor"]), 0, 64, plot_bottom, plot_top),
        )
        for row in a_rows
    ]
    energy_points = [
        (
            map_log(float(row["n"]), 1, 64, left, right),
            map_linear(6.0, 0, 64, plot_bottom, plot_top),
        )
        for row in a_rows
    ]
    backend.polyline(frequency_points, color=BLUE, width=1.45)
    backend.polyline(energy_points, color=AMBER, width=1.25, dash=(4.0, 2.4))
    for point_index in (0, 7, 15, 31, 63):
        marker(backend, "circle", *frequency_points[point_index], BLUE)
        marker(backend, "square", *energy_points[point_index], AMBER, size=1.4)
    backend.text(right - 2, plot_top + 5.5, "factor n", size=5.1, color=BLUE, anchor="end", bold=True)
    backend.text(right - 2, energy_points[-1][1] - 4.0, "fixed energy = 6", size=4.9, color=AMBER, anchor="end", bold=True)
    backend.text(left + 2, plot_bottom - 4.2, "c is suppressed, not estimated", size=4.25, color=MUTED, italic=True)

    # Panel B
    x0 = panel_x[1]
    panel_heading(backend, x0, "B", "Lacunary exact arithmetic", "S_J -> 1/3, while each lower-bound unit equals 1")
    left = x0 + plot_left_offsets[1]
    right = x0 + panel_width - plot_right_offsets[1]
    x_ticks_b = [(map_linear(j, 1, 16, left, right), str(j)) for j in (1, 4, 8, 12, 16)]
    y_ticks_b_left = [(map_linear(v, 0, 0.36, plot_bottom, plot_top), label) for v, label in ((0, "0"), (0.1, ".1"), (0.2, ".2"), (0.3, ".3"))]
    y_ticks_b_right = [(map_linear(v, 0, 16, plot_bottom, plot_top), str(v)) for v in (0, 4, 8, 12, 16)]
    axes(
        backend,
        left,
        plot_top,
        right,
        plot_bottom,
        x_ticks_b,
        y_ticks_b_left,
        y_ticks_right=y_ticks_b_right,
        x_label="partial index J",
        left_label="S_J",
        right_label="unit sum",
    )
    b_rows = [row for row in rows if row["panel"] == "B"]
    l2_points = [
        (
            map_linear(float(row["J"]), 1, 16, left, right),
            map_linear(float(row["l2_partial_sum"]), 0, 0.36, plot_bottom, plot_top),
        )
        for row in b_rows
    ]
    j_points = [
        (
            map_linear(float(row["J"]), 1, 16, left, right),
            map_linear(float(row["lacunary_partial_lower_sum"]), 0, 16, plot_bottom, plot_top),
        )
        for row in b_rows
    ]
    limit_y = map_linear(1.0 / 3.0, 0, 0.36, plot_bottom, plot_top)
    backend.line(left, limit_y, right, limit_y, color=MUTED, width=0.8, dash=(1.2, 2.0))
    backend.polyline(l2_points, color=BLUE, width=1.45)
    backend.polyline(j_points, color=AMBER, width=1.25, dash=(4.0, 2.4))
    for point_index in (0, 3, 7, 11, 15):
        marker(backend, "circle", *l2_points[point_index], BLUE)
        marker(backend, "square", *j_points[point_index], AMBER, size=1.4)
    backend.text(left + 4.0, limit_y - 3.7, "limit 1/3", size=4.75, color=MUTED)
    backend.text(right - 2.0, j_points[-1][1] + 7.0, "sum = J", size=4.9, color=AMBER, anchor="end", bold=True)
    backend.text(right - 2.0, l2_points[-1][1] + 8.0, "S_J", size=4.9, color=BLUE, anchor="end", bold=True)

    # Panel C
    x0 = panel_x[2]
    panel_heading(backend, x0, "C", "Crossed production kernel", "A=B=n=1; x1=x2=pi/3; r=exp(-s)")
    left = x0 + plot_left_offsets[2]
    right = x0 + panel_width - plot_right_offsets[2]
    c_min, c_max = 0.005, 3.0
    c_ticks = (0.005, 0.01, 0.03, 0.1, 0.3, 1.0, 3.0)
    x_ticks_c = [(map_log(v, c_min, c_max, left, right), f"{v:g}") for v in c_ticks]
    y_ticks_c_left = [(map_linear(v, 0, 1.05, plot_bottom, plot_top), label) for v, label in ((0, "0"), (0.25, ".25"), (0.5, ".5"), (0.75, ".75"), (1.0, "1"))]
    y_ticks_c_right = [(map_linear(v, 0, 0.15, plot_bottom, plot_top), label) for v, label in ((0, "0"), (0.05, ".05"), (0.1, ".10"), (0.15, ".15"))]
    axes(
        backend,
        left,
        plot_top,
        right,
        plot_bottom,
        x_ticks_c,
        y_ticks_c_left,
        y_ticks_right=y_ticks_c_right,
        x_label="heat scale s (log)",
        left_label="D_s",
        right_label="|Q_s|, div Q_s",
    )
    c_rows = [row for row in rows if row["panel"] == "C"]

    def c_points(field: str, maximum: float) -> list[tuple[float, float]]:
        return [
            (
                map_log(float(row["s"]), c_min, c_max, left, right),
                map_linear(float(row[field]), 0, maximum, plot_bottom, plot_top),
            )
            for row in c_rows
        ]

    d_points = c_points("D_s", 1.05)
    q_points = c_points("Q_s_magnitude", 0.15)
    div_points = c_points("div_Q_s", 0.15)
    backend.polyline(d_points, color=BLUE, width=1.45)
    backend.polyline(q_points, color=AMBER, width=1.25, dash=(4.0, 2.4))
    backend.polyline(div_points, color=AMBER, width=1.15, dash=(1.2, 2.0))
    for point_index in (0, 30, 60, 90, 120):
        marker(backend, "circle", *d_points[point_index], BLUE)
        marker(backend, "square", *q_points[point_index], AMBER, size=1.25)
        marker(backend, "triangle", *div_points[point_index], AMBER, size=1.25)
    # Compact in-panel line key, intentionally redundant with color.
    legend_x = left + 3.0
    legend_y = plot_top + 9.0
    for offset, label, color, dash, shape in (
        (0.0, "D_s", BLUE, None, "circle"),
        (8.0, "|Q_s|", AMBER, (4.0, 2.4), "square"),
        (16.0, "div Q_s", AMBER, (1.2, 2.0), "triangle"),
    ):
        backend.line(legend_x, legend_y + offset, legend_x + 10.0, legend_y + offset, color=color, width=1.15, dash=dash)
        marker(backend, shape, legend_x + 5.0, legend_y + offset, color, size=1.05)
        backend.text(legend_x + 13.0, legend_y + offset + 1.7, label, size=4.6, color=color, bold=True)
    backend.text(right - 2.0, plot_bottom - 4.0, "Pi_s = S_s = 0", size=4.7, color=INK, anchor="end", bold=True)

    backend.line(20.0, 184.0, width - 20.0, 184.0, color=GRID, width=0.6)
    backend.text(20.0, 194.0, "Exact formulas • normalized analytic consequences • no DNS • finite rows do not prove quantifiers", size=5.0, color=MUTED)
    backend.text(width - 20.0, 194.0, "NOT CLAY", size=5.2, color=INK, anchor="end", bold=True)
    backend.text(20.0, 203.0, "Source-bound: 7321e8a2c50817b58edd6e3bf1dd35bb3a24576b", size=4.25, color=MUTED)


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
    with tempfile.TemporaryDirectory(prefix="r073z-poppler-") as temp_dir:
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
    c_rows = [row for row in rows if row["panel"] == "C"]
    results = {
        "claimBoundary": {
            "finiteRowsProveQuantifiers": False,
            "normalizedAnalyticConsequences": True,
            "notClay": True,
            "simulation": False,
        },
        "figureId": config["figureId"],
        "formulas": {
            "A": "E_n/pi^3=6 and displayed lower-bound frequency factor=n in c*n",
            "B": "S_J=(1-4^(-J))/3; a_j^3*N_j=1; partial lower sum=J",
            "C": "r=exp(-s); D=(1-r^2)(1+r^2/2); |Q|=sqrt(6)(r^3-r^5)/8; divQ=3(r^3-r^5)/4; Pi=S=0",
        },
        "panelA": {
            "energyOverPiCubed": 6,
            "frequencyFactorMaximum": int(config["panelA"]["frequencyMaximum"]),
            "rows": sum(row["panel"] == "A" for row in rows),
        },
        "panelB": {
            "displayedExactLimit": "1/3",
            "lastExactPartialSum": next(row["l2_partial_sum_exact"] for row in reversed(rows) if row["panel"] == "B"),
            "partialLowerSumMaximum": int(config["panelB"]["indexMaximum"]),
            "rows": sum(row["panel"] == "B" for row in rows),
        },
        "panelC": {
            "DMinimumDisplayed": min(float(row["D_s"]) for row in c_rows),
            "QMagnitudeMaximumDisplayed": max(float(row["Q_s_magnitude"]) for row in c_rows),
            "divQMaximumDisplayed": max(float(row["div_Q_s"]) for row in c_rows),
            "productionChannels": {"Pi_s": 0, "centered_S_s": 0},
            "rows": len(c_rows),
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
    log.event("source-binding", "PASS", f"verified {head} and nine frozen source hashes")
    rows = build_rows(config)
    if len(rows) != 201:
        raise RuntimeError(f"unexpected row count: {len(rows)}")
    write_csv(rows)
    log.event("source-data", "PASS", "wrote 201 closed-form rows (64 + 16 + 121)")
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
    os.environ.setdefault("SOURCE_DATE_EPOCH", "1788250565")
    os.environ.setdefault("PYTHONHASHSEED", "0")
    produce()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
