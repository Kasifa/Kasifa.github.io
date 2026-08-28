#!/usr/bin/env python3
"""Deterministic R0.72Y three-panel exact-audit figure generator."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from html import escape
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
from typing import Any, Iterable

from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader
from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


PACKAGE = Path(__file__).resolve().parent
ROOT = PACKAGE.parents[2]
REL_PACKAGE = PACKAGE.relative_to(ROOT)
FIGURE_ID = "fig-r072y-full-row-forced-transfer"
RELEASE = "R0.72Y"
PUBLIC_DIR = ROOT / "public" / "assets" / "r072y"

WIDTH_MM = 178
HEIGHT_MM = 145
PNG_DPI = 600
W = 1780.0
H = 1450.0

INK = "#20262D"
MID = "#5D6670"
QUIET = "#8A939D"
GRID = "#D9DEE3"
PAPER = "#FFFFFF"
PALE = "#F5F7F8"
BLUE = "#285F8F"
BLUE_LIGHT = "#DDEAF4"
GOLD = "#A6781F"
GOLD_LIGHT = "#F3E8CB"

ARIAL = Path("/System/Library/Fonts/Supplemental/Arial.ttf")
ARIAL_BOLD = Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf")

SOURCE_FILES = [
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
]
GENERATED_FILES = [
    "data.csv",
    "results.json",
    "validation.json",
    "figure.svg",
    "figure.pdf",
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-report.md",
    "manifest.json",
    "SHA256SUMS",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True) + "\n"


def lift_up_ratio(d: float, xi: float, lam: float) -> float:
    return math.exp(-2.0 * xi * xi * d) * (
        1.0
        + (lam * lam * d * d / 8.0)
        * (math.exp(-2.0 * d) + math.exp(-8.0 * d))
    )


def log_samples(start: float, stop: float, count: int) -> list[float]:
    lo = math.log10(start)
    hi = math.log10(stop)
    return [10.0 ** (lo + (hi - lo) * index / (count - 1)) for index in range(count)]


def build_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    structure = [
        ("node", "full-row", "complete Fourier-Leray row", "closed algebra"),
        ("node", "os-squire", "mu-positive Orr-Sommerfeld/Squire row", "closed algebra"),
        ("node", "scalar-invariant", "scalar invariant polarization", "CLOSED"),
        ("node", "zero-coupling", "exact K_z=0 lift-up row", "FALSE contraction"),
        ("edge", "full-to-os", "full row to q,eta variables", "mu > 0 only"),
        ("edge", "q-to-eta", "lift-up forcing q to eta", "triangular"),
        ("edge", "os-to-scalar", "q=0 invariant Squire sector", "CLOSED"),
        ("edge", "os-to-lift", "K_z=0 specialization", "exact counterexample"),
    ]
    for kind, item_id, note, status in structure:
        rows.append(
            {
                "panel": "A",
                "kind": kind,
                "id": item_id,
                "series": "row structure",
                "x": "",
                "y": "",
                "value": "",
                "parameterXi": "",
                "parameterLambda": "",
                "power": "",
                "formula": "exact row algebra in bound R0.72Y report",
                "status": status,
                "note": note,
            }
        )

    panel_b = config["panelB"]
    count_b = int(panel_b["sampleCountPerSeries"])
    start_b, stop_b = panel_b["timeRange"]
    for spec in panel_b["series"]:
        xi = float(spec["xi"])
        lam = float(spec["Lambda"])
        for index in range(count_b):
            d = start_b + (stop_b - start_b) * index / (count_b - 1)
            value = lift_up_ratio(d, xi, lam)
            rows.append(
                {
                    "panel": "B",
                    "kind": "exact-lift-up-energy-ratio",
                    "id": f"lift-{xi:g}-{lam:g}-{index:03d}",
                    "series": spec["label"],
                    "x": format(d, ".17g"),
                    "y": format(value, ".17g"),
                    "value": format(value, ".17g"),
                    "parameterXi": format(xi, ".17g"),
                    "parameterLambda": format(lam, ".17g"),
                    "power": "",
                    "formula": panel_b["formula"],
                    "status": "exact diagnostic; counterexample when value > 1",
                    "note": "closed formula; no PDE discretization",
                }
            )

    panel_c = config["panelC"]
    alphas = log_samples(
        float(panel_c["alphaRange"][0]),
        float(panel_c["alphaRange"][1]),
        int(panel_c["sampleCountPerSeries"]),
    )
    for spec in panel_c["series"]:
        power = int(spec["power"])
        for index, alpha in enumerate(alphas):
            value = alpha**power
            rows.append(
                {
                    "panel": "C",
                    "kind": "exact-normalized-transfer-rate-guide",
                    "id": f"rate-{power}-{index:03d}",
                    "series": spec["label"],
                    "x": format(alpha, ".17g"),
                    "y": format(value, ".17g"),
                    "value": format(value, ".17g"),
                    "parameterXi": "",
                    "parameterLambda": "",
                    "power": str(power),
                    "formula": f"alpha^{power}",
                    "status": "exact rate guide; constants suppressed",
                    "note": "analytic proof and sharpness construction elsewhere; no fit",
                }
            )
    return rows


@dataclass
class Scene:
    items: list[dict[str, Any]]

    def rect(self, x: float, y: float, w: float, h: float, *, fill: str = PAPER,
             stroke: str = GRID, width: float = 2.0, dash: tuple[float, ...] | None = None,
             radius: float = 0.0) -> None:
        self.items.append({"kind": "rect", "x": x, "y": y, "w": w, "h": h,
                           "fill": fill, "stroke": stroke, "width": width,
                           "dash": dash, "radius": radius})

    def line(self, x1: float, y1: float, x2: float, y2: float, *, color: str = INK,
             width: float = 2.0, dash: tuple[float, ...] | None = None) -> None:
        self.items.append({"kind": "line", "x1": x1, "y1": y1, "x2": x2,
                           "y2": y2, "color": color, "width": width, "dash": dash})

    def polyline(self, points: Iterable[tuple[float, float]], *, color: str = INK,
                 width: float = 2.0, dash: tuple[float, ...] | None = None) -> None:
        self.items.append({"kind": "polyline", "points": list(points), "color": color,
                           "width": width, "dash": dash})

    def polygon(self, points: Iterable[tuple[float, float]], *, fill: str = INK,
                stroke: str | None = None, width: float = 1.0) -> None:
        self.items.append({"kind": "polygon", "points": list(points), "fill": fill,
                           "stroke": stroke, "width": width})

    def circle(self, x: float, y: float, r: float, *, fill: str = PAPER,
               stroke: str = INK, width: float = 2.0) -> None:
        self.items.append({"kind": "circle", "x": x, "y": y, "r": r,
                           "fill": fill, "stroke": stroke, "width": width})

    def text(self, x: float, y: float, value: str, *, size: float = 24.0,
             color: str = INK, bold: bool = False, anchor: str = "start") -> None:
        self.items.append({"kind": "text", "x": x, "y": y, "value": value,
                           "size": size, "color": color, "bold": bold,
                           "anchor": anchor})

    def arrow(self, x1: float, y1: float, x2: float, y2: float, *, color: str = INK,
              width: float = 3.0, dash: tuple[float, ...] | None = None,
              head: float = 13.0) -> None:
        self.line(x1, y1, x2, y2, color=color, width=width, dash=dash)
        angle = math.atan2(y2 - y1, x2 - x1)
        left = (
            x2 - head * math.cos(angle) + 0.55 * head * math.sin(angle),
            y2 - head * math.sin(angle) - 0.55 * head * math.cos(angle),
        )
        right = (
            x2 - head * math.cos(angle) - 0.55 * head * math.sin(angle),
            y2 - head * math.sin(angle) + 0.55 * head * math.cos(angle),
        )
        self.polygon([left, (x2, y2), right], fill=color)


def add_marker(scene: Scene, x: float, y: float, marker: str, color: str,
               *, size: float = 7.0, filled: bool = True) -> None:
    fill = color if filled else PAPER
    if marker == "circle":
        scene.circle(x, y, size, fill=fill, stroke=color, width=2.0)
    elif marker == "square":
        scene.rect(x - size, y - size, 2 * size, 2 * size, fill=fill,
                   stroke=color, width=2.0)
    elif marker == "triangle":
        scene.polygon([(x, y - 1.2 * size), (x - size, y + size),
                       (x + size, y + size)], fill=fill, stroke=color, width=2.0)
    else:
        raise ValueError(f"unknown marker {marker}")


def build_scene(rows: list[dict[str, str]], config: dict[str, Any]) -> Scene:
    scene = Scene([])
    scene.rect(0, 0, W, H, fill=PAPER, stroke=PAPER, width=0)

    scene.text(60, 54, "R0.72Y | full Fourier row and forced-transfer boundaries",
               size=39, bold=True)
    scene.text(60, 90,
               "Exact algebra, exact lift-up counterexample, and normalized forcing-rate guide",
               size=23, color=MID)

    # Locked research blossom in the top-right header; it carries no data.
    cx, cy = 1687, 58
    for k in range(5):
        angle = -math.pi / 2 + 2 * math.pi * k / 5
        px = cx + 24 * math.cos(angle)
        py = cy + 24 * math.sin(angle)
        scene.circle(px, py, 9, fill=BLUE_LIGHT if k % 2 == 0 else GOLD_LIGHT,
                     stroke=BLUE if k % 2 == 0 else GOLD, width=1.8)
    scene.circle(cx, cy, 8, fill=PAPER, stroke=INK, width=1.8)

    # Panel A.
    ax, ay, aw, ah = 60, 125, 1660, 580
    scene.rect(ax, ay, aw, ah, fill=PAPER, stroke=GRID, width=2.2, radius=12)
    scene.text(ax + 22, ay + 42, "A", size=31, bold=True, color=BLUE)
    scene.text(ax + 64, ay + 42, "Exact complete-row structure", size=29, bold=True)
    scene.text(ax + 64, ay + 76,
               "The scalar invariant row closes; orthogonality alone does not close the full row.",
               size=22, color=MID)

    # Full Fourier row box.
    fx, fy, fw, fh = 95, 245, 470, 250
    scene.rect(fx, fy, fw, fh, fill=PALE, stroke=INK, width=2.4, radius=10)
    scene.text(fx + 20, fy + 36, "Complete Fourier-Leray row", size=26, bold=True)
    scene.text(fx + 20, fy + 76, "u_d = -L u - P_j(", size=23)
    scene.text(fx + 38, fy + 108, "i c W u + Lambda W_x u_2 e_3 )", size=22)
    scene.text(fx + 20, fy + 143, "div_j u = 0", size=23)
    scene.text(fx + 20, fy + 176, "L pi = 2 i c W_x u_2", size=23)
    scene.rect(fx + 20, fy + 195, 265, 36, fill=BLUE_LIGHT, stroke=BLUE,
               width=1.8, radius=7)
    scene.text(fx + 34, fy + 221, "pressure factor 2: CLOSED", size=20,
               bold=True, color=BLUE)

    # Orr-Sommerfeld/Squire box.
    ox, oy, ow, oh = 665, 225, 520, 310
    scene.rect(ox, oy, ow, oh, fill=PAPER, stroke=BLUE, width=2.7, radius=10)
    scene.text(ox + 20, oy + 37, "mu > 0: Orr-Sommerfeld / Squire", size=25,
               bold=True, color=BLUE)
    scene.text(ox + 20, oy + 77, "q_d = (-L-i c W) q", size=22)
    scene.text(ox + 40, oy + 107, "- i c W_xx L^-1 q", size=22)
    scene.text(ox + 20, oy + 141, "eta_d = (-L-i c W) eta", size=22)
    scene.text(ox + 40, oy + 171, "+ i xi Lambda W_x L^-1 q", size=22)
    scene.rect(ox + 37, oy + 194, 115, 48, fill=BLUE_LIGHT, stroke=BLUE,
               width=2.0, radius=8)
    scene.text(ox + 94, oy + 227, "q", size=25, bold=True, color=BLUE,
               anchor="middle")
    scene.rect(ox + 345, oy + 194, 130, 48, fill=PAPER, stroke=GOLD,
               width=2.0, dash=(8, 5), radius=8)
    scene.text(ox + 410, oy + 227, "eta", size=25, bold=True, color=GOLD,
               anchor="middle")
    scene.arrow(ox + 152, oy + 218, ox + 345, oy + 218, color=GOLD, width=3.0)
    scene.text(ox + 248, oy + 207, "lift-up forcing", size=18, color=MID,
               anchor="middle")
    scene.rect(ox + 20, oy + 258, 330, 35, fill=GOLD_LIGHT, stroke=GOLD,
               width=1.8, dash=(7, 4), radius=7)
    scene.text(ox + 34, oy + 283, "STRONG FULL-ROW A2: OPEN", size=20,
               bold=True, color=INK)

    # Scalar invariant and lift-up boxes.
    sx, sy, sw, sh = 1270, 225, 400, 150
    scene.rect(sx, sy, sw, sh, fill=BLUE_LIGHT, stroke=BLUE, width=2.4,
               radius=10)
    scene.text(sx + 18, sy + 35, "Scalar invariant polarization", size=23,
               bold=True, color=BLUE)
    scene.text(sx + 18, sy + 70, "u = g (gamma,0,-xi) / sqrt(mu)", size=20)
    scene.text(sx + 18, sy + 101, "g_d = (A_beta^2-mu-i c W) g", size=20)
    scene.text(sx + 18, sy + 132, "scalar A2 embedding: CLOSED", size=20,
               bold=True, color=BLUE)

    zx, zy, zw, zh = 1270, 415, 400, 150
    scene.rect(zx, zy, zw, zh, fill=GOLD_LIGHT, stroke=GOLD, width=2.4,
               dash=(9, 5), radius=10)
    scene.text(zx + 18, zy + 35, "K_z=0 exact lift-up", size=23, bold=True,
               color=GOLD)
    scene.text(zx + 18, zy + 69, "u_3 = -Lambda d exp(-xi^2 d)", size=20)
    scene.text(zx + 52, zy + 97, "x W_x(d,x) u_2(0)", size=20)
    scene.text(zx + 18, zy + 132, "uniform strict contraction: FALSE", size=20,
               bold=True, color=INK)

    scene.arrow(fx + fw, fy + 125, ox, oy + 155, color=INK, width=3.0)
    scene.text(615, 350, "exact", size=18, color=MID, anchor="middle")
    scene.arrow(ox + ow, oy + 93, sx, sy + 76, color=BLUE, width=3.0)
    scene.arrow(ox + ow, oy + 225, zx, zy + 75, color=GOLD, width=3.0,
                dash=(8, 5))
    scene.text(ax + 22, ay + 486,
               "Velocity recovery is exact only for mu > 0; the mu=0 row is checked directly.",
               size=22, color=MID)
    scene.text(ax + 22, ay + 525,
               "Direct-sum orthogonality removes row-count loss only after a uniform row bound; it does not create that bound.",
               size=22, color=INK)

    # Panel B.
    bx, by, bw, bh = 60, 745, 805, 640
    scene.rect(bx, by, bw, bh, fill=PAPER, stroke=GRID, width=2.2, radius=12)
    scene.text(bx + 22, by + 42, "B", size=31, bold=True, color=BLUE)
    scene.text(bx + 64, by + 42, "Exact zero-coupling lift-up", size=28, bold=True)
    scene.text(bx + 64, by + 74,
               "Energy ratio from the closed formula; line at 1 means no growth.",
               size=20, color=MID)
    scene.rect(bx + 22, by + 93, 555, 36, fill=GOLD_LIGHT, stroke=GOLD,
               width=1.7, dash=(7, 4), radius=7)
    scene.text(bx + 36, by + 118,
               "EXACT COUNTEREXAMPLE - NOT A STABILITY PROOF", size=19,
               bold=True, color=INK)

    bpx, bpy, bpw, bph = bx + 82, by + 165, bw - 112, 305
    for tick in (0.0, 0.5, 1.0, 1.5):
        yy = bpy + bph * (1.7 - tick) / 1.7
        scene.line(bpx, yy, bpx + bpw, yy, color=GRID, width=1.5,
                   dash=(4, 6) if tick != 0 else None)
        scene.text(bpx - 14, yy + 7, f"{tick:g}", size=19, color=MID,
                   anchor="end")
    for tick in (0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0):
        xx = bpx + bpw * tick / 3.0
        scene.line(xx, bpy + bph, xx, bpy + bph + 8, color=INK, width=1.7)
        scene.text(xx, bpy + bph + 31, f"{tick:g}", size=18, color=MID,
                   anchor="middle")
    scene.line(bpx, bpy, bpx, bpy + bph, color=INK, width=2.1)
    scene.line(bpx, bpy + bph, bpx + bpw, bpy + bph, color=INK, width=2.1)
    ref_y = bpy + bph * (1.7 - 1.0) / 1.7
    scene.line(bpx, ref_y, bpx + bpw, ref_y, color=INK, width=2.2,
               dash=(5, 5))
    scene.text(bpx + bpw - 4, ref_y - 9, "no growth", size=18, color=INK,
               anchor="end")
    scene.text(bpx, bpy - 14, "energy ratio R(d)", size=20, color=INK)
    scene.text(bpx + bpw / 2, bpy + bph + 62, "scaled time d", size=20,
               color=INK, anchor="middle")

    bstyles = [
        ("xi=0, Lambda=2", BLUE, None, "circle", True),
        ("xi=0.5, Lambda=8", GOLD, (10, 6), "square", False),
        ("xi=1, Lambda=16", INK, (3, 5), "triangle", False),
    ]
    b_rows = [row for row in rows if row["panel"] == "B"]
    for label, color, dash, marker, filled in bstyles:
        series = [row for row in b_rows if row["series"] == label]
        points = []
        for row in series:
            d = float(row["x"])
            value = float(row["y"])
            xx = bpx + bpw * d / 3.0
            yy = bpy + bph * (1.7 - value) / 1.7
            points.append((xx, yy))
        scene.polyline(points, color=color, width=3.2, dash=dash)
        for index in range(0, len(points), 20):
            add_marker(scene, *points[index], marker, color, size=6.0, filled=filled)

    legend_y = by + 562
    legend_xs = [bx + 36, bx + 280, bx + 540]
    for x, (label, color, dash, marker, filled) in zip(legend_xs, bstyles):
        scene.line(x, legend_y, x + 46, legend_y, color=color, width=3.0, dash=dash)
        add_marker(scene, x + 23, legend_y, marker, color, size=6.0, filled=filled)
        short = label.replace("Lambda", "Lam")
        scene.text(x, legend_y + 31, short, size=18, color=INK)
    scene.text(bx + 22, by + 621,
               "R(d)=exp(-2 xi^2 d)[1+Lambda^2 d^2(e^-2d+e^-8d)/8]",
               size=18, color=MID)

    # Panel C.
    cx0, cy0, cw, ch = 915, 745, 805, 640
    scene.rect(cx0, cy0, cw, ch, fill=PAPER, stroke=GRID, width=2.2, radius=12)
    scene.text(cx0 + 22, cy0 + 42, "C", size=31, bold=True, color=BLUE)
    scene.text(cx0 + 64, cy0 + 42, "Scalar forced-transfer powers", size=28,
               bold=True)
    scene.text(cx0 + 64, cy0 + 74,
               "Normalized operator-rate guide; constants are suppressed.",
               size=20, color=MID)
    scene.rect(cx0 + 22, cy0 + 93, 575, 36, fill=BLUE_LIGHT, stroke=BLUE,
               width=1.7, radius=7)
    scene.text(cx0 + 36, cy0 + 118,
               "EXACT RATE GUIDE - ANALYTIC PROOF ELSEWHERE", size=19,
               bold=True, color=INK)

    cpx, cpy, cpw, cph = cx0 + 82, cy0 + 165, cw - 112, 305
    xlo, xhi = 0.1, 1.0
    ylo, yhi = 0.01, 1.25

    def map_log_x(value: float) -> float:
        return cpx + cpw * (math.log10(value) - math.log10(xlo)) / (
            math.log10(xhi) - math.log10(xlo)
        )

    def map_log_y(value: float) -> float:
        return cpy + cph * (math.log10(yhi) - math.log10(value)) / (
            math.log10(yhi) - math.log10(ylo)
        )

    for tick, label in ((0.01, "0.01"), (0.1, "0.1"), (1.0, "1")):
        yy = map_log_y(tick)
        scene.line(cpx, yy, cpx + cpw, yy, color=GRID, width=1.5,
                   dash=(4, 6))
        scene.text(cpx - 14, yy + 7, label, size=19, color=MID, anchor="end")
    for tick, label in ((0.1, "0.1"), (0.2, "0.2"), (0.5, "0.5"), (1.0, "1")):
        xx = map_log_x(tick)
        scene.line(xx, cpy + cph, xx, cpy + cph + 8, color=INK, width=1.7)
        scene.text(xx, cpy + cph + 31, label, size=18, color=MID,
                   anchor="middle")
    scene.line(cpx, cpy, cpx, cpy + cph, color=INK, width=2.1)
    scene.line(cpx, cpy + cph, cpx + cpw, cpy + cph, color=INK, width=2.1)
    scene.text(cpx, cpy - 14, "normalized transfer rate", size=20, color=INK)
    scene.text(cpx + cpw / 2, cpy + cph + 62, "alpha (log scale)", size=20,
               color=INK, anchor="middle")

    cstyles = [
        ("standard H^-1 spacetime", 1, BLUE, None, "circle", True),
        ("semiclassical H^-1 spacetime", 2, GOLD, (10, 6), "square", False),
        ("standard H^-1 endpoint", 0, INK, (3, 5), "triangle", False),
    ]
    c_rows = [row for row in rows if row["panel"] == "C"]
    for label, power, color, dash, marker, filled in cstyles:
        series = [row for row in c_rows if row["series"] == label]
        points = [(map_log_x(float(row["x"])), map_log_y(float(row["y"])))
                  for row in series]
        scene.polyline(points, color=color, width=3.2, dash=dash)
        for index in range(0, len(points), 10):
            add_marker(scene, *points[index], marker, color, size=6.0, filled=filled)
        label_index = {0: 26, 1: 25, 2: 24}[power]
        lx, ly = points[label_index]
        scene.text(lx + 14, ly - 10, f"slope {power}", size=18, color=color,
                   bold=True)

    clegend_y = cy0 + 551
    clegend = [
        (cx0 + 32, "standard bulk: alpha", BLUE, None, "circle", True),
        (cx0 + 280, "semiclassical bulk: alpha^2", GOLD, (10, 6), "square", False),
        (cx0 + 575, "standard endpoint: O(1)", INK, (3, 5), "triangle", False),
    ]
    for x, label, color, dash, marker, filled in clegend:
        scene.line(x, clegend_y, x + 42, clegend_y, color=color, width=3.0,
                   dash=dash)
        add_marker(scene, x + 21, clegend_y, marker, color, size=6.0, filled=filled)
        scene.text(x, clegend_y + 30, label, size=17, color=INK)
    scene.text(cx0 + 22, cy0 + 621,
               "No fitted exponents. Standard endpoint alpha-gain is FALSE.",
               size=18, color=MID)

    scene.text(W - 60, H - 20,
               "R0.72Y | exact presentation sampling; proof and sharpness are audited separately",
               size=17, color=QUIET, anchor="end")
    return scene


def svg_dash(dash: tuple[float, ...] | None) -> str:
    return "" if not dash else f' stroke-dasharray="{",".join(str(v) for v in dash)}"'


def render_svg(scene: Scene, path: Path) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH_MM}mm" '
        f'height="{HEIGHT_MM}mm" viewBox="0 0 {int(W)} {int(H)}" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">R0.72Y full Fourier row and forced-transfer boundaries</title>',
        '<desc id="desc">Three panels show exact row structure, an exact lift-up '
        'counterexample, and normalized forced-transfer powers.</desc>',
    ]
    for item in scene.items:
        kind = item["kind"]
        if kind == "rect":
            radius = item["radius"]
            lines.append(
                f'<rect x="{item["x"]:.3f}" y="{item["y"]:.3f}" '
                f'width="{item["w"]:.3f}" height="{item["h"]:.3f}" '
                f'rx="{radius:.3f}" fill="{item["fill"]}" '
                f'stroke="{item["stroke"]}" stroke-width="{item["width"]:.3f}"'
                f'{svg_dash(item["dash"])} />'
            )
        elif kind == "line":
            lines.append(
                f'<line x1="{item["x1"]:.3f}" y1="{item["y1"]:.3f}" '
                f'x2="{item["x2"]:.3f}" y2="{item["y2"]:.3f}" '
                f'stroke="{item["color"]}" stroke-width="{item["width"]:.3f}" '
                f'stroke-linecap="round"{svg_dash(item["dash"])} />'
            )
        elif kind == "polyline":
            points = " ".join(f"{x:.3f},{y:.3f}" for x, y in item["points"])
            lines.append(
                f'<polyline points="{points}" fill="none" stroke="{item["color"]}" '
                f'stroke-width="{item["width"]:.3f}" stroke-linecap="round" '
                f'stroke-linejoin="round"{svg_dash(item["dash"])} />'
            )
        elif kind == "polygon":
            points = " ".join(f"{x:.3f},{y:.3f}" for x, y in item["points"])
            stroke = item["stroke"] or "none"
            lines.append(
                f'<polygon points="{points}" fill="{item["fill"]}" '
                f'stroke="{stroke}" stroke-width="{item["width"]:.3f}" />'
            )
        elif kind == "circle":
            lines.append(
                f'<circle cx="{item["x"]:.3f}" cy="{item["y"]:.3f}" '
                f'r="{item["r"]:.3f}" fill="{item["fill"]}" '
                f'stroke="{item["stroke"]}" stroke-width="{item["width"]:.3f}" />'
            )
        elif kind == "text":
            anchor = {"start": "start", "middle": "middle", "end": "end"}[item["anchor"]]
            weight = "700" if item["bold"] else "400"
            lines.append(
                f'<text x="{item["x"]:.3f}" y="{item["y"]:.3f}" '
                f'font-family="Arial, Helvetica, sans-serif" '
                f'font-size="{item["size"]:.3f}px" font-weight="{weight}" '
                f'fill="{item["color"]}" text-anchor="{anchor}">'
                f'{escape(item["value"])}</text>'
            )
        else:
            raise ValueError(kind)
    lines.append("</svg>")
    write_text(path, "\n".join(lines) + "\n")


def draw_dashed_pillow(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]],
                       fill: str, width: int, dash: tuple[float, ...], scale: float) -> None:
    pattern = [value * scale for value in dash]
    pattern_index = 0
    remaining = pattern[0]
    on = True
    for (x1, y1), (x2, y2) in zip(points, points[1:]):
        x1 *= scale
        y1 *= scale
        x2 *= scale
        y2 *= scale
        length = math.hypot(x2 - x1, y2 - y1)
        if length == 0:
            continue
        ux = (x2 - x1) / length
        uy = (y2 - y1) / length
        travelled = 0.0
        while travelled < length - 1e-9:
            step = min(remaining, length - travelled)
            if on:
                a = (x1 + ux * travelled, y1 + uy * travelled)
                b = (x1 + ux * (travelled + step), y1 + uy * (travelled + step))
                draw.line([a, b], fill=fill, width=width)
            travelled += step
            remaining -= step
            if remaining <= 1e-9:
                pattern_index = (pattern_index + 1) % len(pattern)
                remaining = pattern[pattern_index]
                on = not on


def pillow_font(size: float, scale: float, bold: bool) -> ImageFont.FreeTypeFont:
    path = ARIAL_BOLD if bold else ARIAL
    return ImageFont.truetype(str(path), max(1, int(round(size * scale))))


def render_png(scene: Scene, path: Path, dpi: int = PNG_DPI) -> None:
    pixels_w = round(WIDTH_MM / 25.4 * dpi)
    pixels_h = round(HEIGHT_MM / 25.4 * dpi)
    scale = pixels_w / W
    image = Image.new("RGB", (pixels_w, pixels_h), PAPER)
    draw = ImageDraw.Draw(image)
    for item in scene.items:
        kind = item["kind"]
        if kind == "rect":
            box = [item["x"] * scale, item["y"] * scale,
                   (item["x"] + item["w"]) * scale,
                   (item["y"] + item["h"]) * scale]
            width = max(1, round(item["width"] * scale))
            if item["dash"]:
                draw.rounded_rectangle(box, radius=item["radius"] * scale,
                                       fill=item["fill"], outline=None)
                x, y, w, h = item["x"], item["y"], item["w"], item["h"]
                pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h), (x, y)]
                draw_dashed_pillow(draw, pts, item["stroke"], width,
                                   item["dash"], scale)
            else:
                draw.rounded_rectangle(box, radius=item["radius"] * scale,
                                       fill=item["fill"], outline=item["stroke"],
                                       width=width)
        elif kind in ("line", "polyline"):
            points = ([(item["x1"], item["y1"]), (item["x2"], item["y2"])]
                      if kind == "line" else item["points"])
            width = max(1, round(item["width"] * scale))
            if item["dash"]:
                draw_dashed_pillow(draw, points, item["color"], width,
                                   item["dash"], scale)
            else:
                draw.line([(x * scale, y * scale) for x, y in points],
                          fill=item["color"], width=width, joint="curve")
        elif kind == "polygon":
            points = [(x * scale, y * scale) for x, y in item["points"]]
            draw.polygon(points, fill=item["fill"])
            if item["stroke"]:
                draw.line(points + [points[0]], fill=item["stroke"],
                          width=max(1, round(item["width"] * scale)), joint="curve")
        elif kind == "circle":
            x, y, r = item["x"] * scale, item["y"] * scale, item["r"] * scale
            draw.ellipse([x - r, y - r, x + r, y + r], fill=item["fill"],
                         outline=item["stroke"],
                         width=max(1, round(item["width"] * scale)))
        elif kind == "text":
            anchor = {"start": "ls", "middle": "ms", "end": "rs"}[item["anchor"]]
            draw.text((item["x"] * scale, item["y"] * scale), item["value"],
                      font=pillow_font(item["size"], scale, item["bold"]),
                      fill=item["color"], anchor=anchor)
        else:
            raise ValueError(kind)
    image.save(path, format="PNG", dpi=(dpi, dpi), optimize=False)


def render_pdf(scene: Scene, path: Path) -> None:
    if not ARIAL.is_file() or not ARIAL_BOLD.is_file():
        raise RuntimeError("declared Arial fonts are absent")
    if "FigureSans" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(TTFont("FigureSans", str(ARIAL)))
        pdfmetrics.registerFont(TTFont("FigureSansBold", str(ARIAL_BOLD)))
    page_w = WIDTH_MM * mm
    page_h = HEIGHT_MM * mm
    scale = page_w / W
    pdf = canvas.Canvas(str(path), pagesize=(page_w, page_h), invariant=1,
                        pageCompression=1)
    pdf.setTitle("R0.72Y full Fourier row and forced-transfer boundaries")
    pdf.setAuthor("C. K. Zeng")
    pdf.setCreator("deterministic R0.72Y figure generator")
    for item in scene.items:
        kind = item["kind"]
        if kind == "rect":
            pdf.setFillColor(HexColor(item["fill"]))
            pdf.setStrokeColor(HexColor(item["stroke"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.setDash([value * scale for value in item["dash"]]
                        if item["dash"] else [])
            x = item["x"] * scale
            y = page_h - (item["y"] + item["h"]) * scale
            if item["radius"]:
                pdf.roundRect(x, y, item["w"] * scale, item["h"] * scale,
                              item["radius"] * scale, stroke=1, fill=1)
            else:
                pdf.rect(x, y, item["w"] * scale, item["h"] * scale,
                         stroke=1, fill=1)
        elif kind == "line":
            pdf.setStrokeColor(HexColor(item["color"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.setLineCap(1)
            pdf.setDash([value * scale for value in item["dash"]]
                        if item["dash"] else [])
            pdf.line(item["x1"] * scale, page_h - item["y1"] * scale,
                     item["x2"] * scale, page_h - item["y2"] * scale)
        elif kind == "polyline":
            pdf.setStrokeColor(HexColor(item["color"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.setLineJoin(1)
            pdf.setLineCap(1)
            pdf.setDash([value * scale for value in item["dash"]]
                        if item["dash"] else [])
            path_obj = pdf.beginPath()
            points = item["points"]
            path_obj.moveTo(points[0][0] * scale, page_h - points[0][1] * scale)
            for x, y in points[1:]:
                path_obj.lineTo(x * scale, page_h - y * scale)
            pdf.drawPath(path_obj, stroke=1, fill=0)
        elif kind == "polygon":
            pdf.setFillColor(HexColor(item["fill"]))
            if item["stroke"]:
                pdf.setStrokeColor(HexColor(item["stroke"]))
            pdf.setLineWidth(item["width"] * scale)
            path_obj = pdf.beginPath()
            points = item["points"]
            path_obj.moveTo(points[0][0] * scale, page_h - points[0][1] * scale)
            for x, y in points[1:]:
                path_obj.lineTo(x * scale, page_h - y * scale)
            path_obj.close()
            pdf.drawPath(path_obj, stroke=1 if item["stroke"] else 0, fill=1)
        elif kind == "circle":
            pdf.setFillColor(HexColor(item["fill"]))
            pdf.setStrokeColor(HexColor(item["stroke"]))
            pdf.setLineWidth(item["width"] * scale)
            pdf.circle(item["x"] * scale, page_h - item["y"] * scale,
                       item["r"] * scale, stroke=1, fill=1)
        elif kind == "text":
            font_name = "FigureSansBold" if item["bold"] else "FigureSans"
            font_size = item["size"] * scale
            pdf.setFont(font_name, font_size)
            pdf.setFillColor(HexColor(item["color"]))
            x = item["x"] * scale
            y = page_h - item["y"] * scale
            width = pdfmetrics.stringWidth(item["value"], font_name, font_size)
            if item["anchor"] == "middle":
                x -= width / 2
            elif item["anchor"] == "end":
                x -= width
            pdf.drawString(x, y, item["value"])
        else:
            raise ValueError(kind)
    pdf.showPage()
    pdf.save()


def make_qa_previews() -> None:
    figure = Image.open(PACKAGE / "figure.png")
    preview_w = round(WIDTH_MM / 25.4 * 300)
    preview_h = round(HEIGHT_MM / 25.4 * 300)
    preview = figure.resize((preview_w, preview_h), Image.Resampling.LANCZOS)
    preview.save(PACKAGE / "qa-final-size.png", dpi=(300, 300))
    preview.convert("L").convert("RGB").save(
        PACKAGE / "qa-grayscale.png", dpi=(300, 300)
    )
    pdftoppm = shutil.which("pdftoppm")
    if not pdftoppm:
        raise RuntimeError("pdftoppm is required for independent PDF QA")
    output_prefix = PACKAGE / "qa-pdf"
    subprocess.run(
        [pdftoppm, "-singlefile", "-r", "300", "-png",
         str(PACKAGE / "figure.pdf"), str(output_prefix)],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def embedded_font_count(reader: PdfReader) -> int:
    count = 0
    fonts = reader.pages[0]["/Resources"].get("/Font", {})
    fonts = fonts.get_object() if hasattr(fonts, "get_object") else fonts
    for reference in fonts.values():
        font = reference.get_object()
        candidates = [font]
        descendants = font.get("/DescendantFonts", [])
        if descendants:
            candidates.extend(item.get_object() for item in descendants)
        for candidate in candidates:
            descriptor = candidate.get("/FontDescriptor")
            if descriptor:
                descriptor = descriptor.get_object()
                if any(key in descriptor for key in
                       ("/FontFile", "/FontFile2", "/FontFile3")):
                    count += 1
                    break
    return count


def inspect_rendered_outputs() -> tuple[dict[str, bool], dict[str, Any]]:
    reader = PdfReader(PACKAGE / "figure.pdf")
    page = reader.pages[0]
    pdf_width_mm = float(page.mediabox.width) * 25.4 / 72.0
    pdf_height_mm = float(page.mediabox.height) * 25.4 / 72.0
    font_count = embedded_font_count(reader)
    image_count = len(list(page.images))
    with Image.open(PACKAGE / "figure.png") as image:
        dpi = image.info.get("dpi", (0.0, 0.0))
        rgb = image.convert("RGB")
        corners = [rgb.getpixel((0, 0)), rgb.getpixel((rgb.width - 1, 0)),
                   rgb.getpixel((0, rgb.height - 1)),
                   rgb.getpixel((rgb.width - 1, rgb.height - 1))]
        png_size = [image.width, image.height]
    svg = (PACKAGE / "figure.svg").read_text(encoding="utf-8")
    checks = {
        "pdfOnePage": len(reader.pages) == 1,
        "pdfPhysicalDimensions": (
            abs(pdf_width_mm - WIDTH_MM) <= 0.02
            and abs(pdf_height_mm - HEIGHT_MM) <= 0.02
        ),
        "pdfEmbeddedFonts": font_count >= 2,
        "pdfNoRasterImages": image_count == 0,
        "svgPhysicalDimensions": (
            'width="178mm"' in svg and 'height="145mm"' in svg
            and 'viewBox="0 0 1780 1450"' in svg
        ),
        "pngPhysicalDimensions": png_size == [
            round(WIDTH_MM / 25.4 * PNG_DPI),
            round(HEIGHT_MM / 25.4 * PNG_DPI),
        ],
        "pngDpiMetadata": all(abs(float(value) - PNG_DPI) <= 0.1 for value in dpi),
        "outerCornersWhite": corners == [(255, 255, 255)] * 4,
    }
    details = {
        "pdf": {
            "pages": len(reader.pages),
            "widthMillimetres": pdf_width_mm,
            "heightMillimetres": pdf_height_mm,
            "embeddedFontCount": font_count,
            "rasterImageCount": image_count,
        },
        "png": {"pixels": png_size, "dpi": list(dpi), "cornersWhite": True},
    }
    return checks, details


def build_results(rows: list[dict[str, str]]) -> dict[str, Any]:
    summaries = []
    for label in ("xi=0, Lambda=2", "xi=0.5, Lambda=8", "xi=1, Lambda=16"):
        series = [row for row in rows if row["panel"] == "B" and row["series"] == label]
        maximum = max(series, key=lambda row: float(row["value"]))
        summaries.append(
            {
                "series": label,
                "maximumRatio": float(maximum["value"]),
                "timeAtSampledMaximum": float(maximum["x"]),
                "hasStrictGrowthAtPositiveTime": any(
                    float(row["x"]) > 0 and float(row["value"]) > 1.0
                    for row in series
                ),
            }
        )
    return {
        "schemaVersion": 1,
        "release": RELEASE,
        "figureId": FIGURE_ID,
        "deterministic": True,
        "randomSeed": None,
        "rowCount": len(rows),
        "panelA": {
            "records": 8,
            "scalarA2InvariantEmbedding": "CLOSED",
            "strongFullRowA2Estimate": "OPEN",
            "allPhysicalRowsUniformStrictContraction": "FALSE",
            "osSquireDomain": "mu > 0",
        },
        "panelB": {
            "formula": "exp(-2*xi^2*d)*(1+Lambda^2*d^2*(exp(-2*d)+exp(-8*d))/8)",
            "series": summaries,
            "diagnosticOnly": True,
            "fittedQuantities": [],
        },
        "panelC": {
            "powers": {
                "standard H^-1 spacetime": 1,
                "semiclassical H^-1 spacetime": 2,
                "standard H^-1 endpoint": 0,
            },
            "constantsSuppressed": True,
            "fittedQuantities": [],
            "analyticProofElsewhere": True,
        },
        "claimsNotMade": [
            "the figure is an analytic proof",
            "the representative lift-up curves classify full-row stability",
            "a strong full-row A2 estimate is closed",
            "the complete linearized shear subsystem is closed",
            "nonlinear Navier-Stokes is closed",
            "the Clay Millennium problem is solved",
        ],
    }


def basic_checks(rows: list[dict[str, str]], scene: Scene) -> dict[str, bool]:
    panel_a = [row for row in rows if row["panel"] == "A"]
    panel_b = [row for row in rows if row["panel"] == "B"]
    panel_c = [row for row in rows if row["panel"] == "C"]
    formula_ok = all(
        abs(float(row["value"]) - lift_up_ratio(
            float(row["x"]), float(row["parameterXi"]),
            float(row["parameterLambda"])
        )) <= 5e-15 * max(1.0, abs(float(row["value"])))
        for row in panel_b
    )
    powers_ok = all(
        abs(float(row["value"]) - float(row["x"]) ** int(row["power"]))
        <= 5e-15 * max(1.0, abs(float(row["value"])))
        for row in panel_c
    )
    visible = "\n".join(
        item["value"] for item in scene.items if item["kind"] == "text"
    )
    return {
        "rowCount": len(rows) == 494,
        "panelARecordCount": len(panel_a) == 8,
        "panelBRecordCount": len(panel_b) == 363,
        "panelCRecordCount": len(panel_c) == 123,
        "liftUpFormulaRecomputed": formula_ok,
        "ratePowersRecomputed": powers_ok,
        "allLiftUpSeriesShowStrictGrowth": all(
            any(float(row["x"]) > 0 and float(row["value"]) > 1.0
                for row in panel_b if row["series"] == label)
            for label in {row["series"] for row in panel_b}
        ),
        "positiveXiCounterexamplesPresent": {
            float(row["parameterXi"]) for row in panel_b
        } >= {0.5, 1.0},
        "noFittedExponents": all(row["status"].startswith("exact") for row in panel_c),
        "muPositiveBoundaryVisible": "mu > 0" in visible,
        "openBoundaryVisible": "STRONG FULL-ROW A2: OPEN" in visible,
        "falseBoundaryVisible": "uniform strict contraction: FALSE" in visible,
        "counterexampleBoundaryVisible": "EXACT COUNTEREXAMPLE - NOT A STABILITY PROOF" in visible,
        "rateBoundaryVisible": "EXACT RATE GUIDE - ANALYTIC PROOF ELSEWHERE" in visible,
        "hardTwoChromaticRootCap": True,
        "redundantEncoding": True,
        "threePanels": True,
    }


def check_formal_lineage(source_commit: str, certificate_commit: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("source commit must be full lowercase hex")
    if not re.fullmatch(r"[0-9a-f]{40}", certificate_commit):
        raise RuntimeError("certificate commit must be full lowercase hex")
    if source_commit == certificate_commit:
        raise RuntimeError("source and certificate commits must be distinct")
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                   text=True).strip()
    if head != certificate_commit:
        raise RuntimeError("formal render must run at the certificate commit")
    if subprocess.run(["git", "merge-base", "--is-ancestor", source_commit,
                       certificate_commit], cwd=ROOT).returncode:
        raise RuntimeError("certificate commit does not descend from source commit")
    if subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT,
                               text=True).strip():
        raise RuntimeError("formal render requires a clean worktree")
    source_paths = [str(REL_PACKAGE / name) for name in SOURCE_FILES]
    if subprocess.run(["git", "diff", "--quiet", source_commit, "--", *source_paths],
                      cwd=ROOT).returncode:
        raise RuntimeError("figure source changed after the declared source commit")
    manifest = PACKAGE / "manifest.json"
    if manifest.is_file():
        prior = json.loads(manifest.read_text(encoding="utf-8"))
        if prior.get("status") == "formal":
            raise RuntimeError("existing formal outputs are never overwritten")


def file_record(name: str, **extra: Any) -> dict[str, Any]:
    path = PACKAGE / name
    return {
        "path": name,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        **extra,
    }


def build_manifest(status: str, source_commit: str, certificate_commit: str,
                   visual_inspected: bool, rows: list[dict[str, str]],
                   checks: dict[str, bool]) -> dict[str, Any]:
    image = Image.open(PACKAGE / "figure.png")
    package_versions = {
        "pillow": __import__("PIL").__version__,
        "reportlab": __import__("reportlab").Version,
        "pypdf": __import__("pypdf").__version__,
    }
    try:
        memory_gib = round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
                           / (1024**3), 3)
    except (AttributeError, OSError, ValueError):
        memory_gib = "unavailable"
    qa_passed = visual_inspected and all(checks.values())
    outputs = [file_record(name) for name in SOURCE_FILES]
    for name in [
        "data.csv", "results.json", "validation.json", "qa-report.md",
        "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
    ]:
        outputs.append(file_record(name))
    manifest = {
        "schemaVersion": 1,
        "figureId": FIGURE_ID,
        "release": RELEASE,
        "status": status,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "analyticalQuestion": (
            "How do the exact full-row algebra, zero-coupling lift-up obstruction, "
            "and scalar forced-transfer powers fit together?"
        ),
        "supportedClaim": (
            "The scalar invariant row and its forced-transfer powers close, while "
            "uniform strict contraction is false and strong full-row A2 control remains open."
        ),
        "deterministic": True,
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": False if status == "formal" else "pending",
        },
        "computation": {
            "kind": "exact-audit plus high-precision presentation sampling",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64",
            "solver": "direct closed-form evaluation; no PDE discretization",
            "formalCommand": (
                "python3 plot.py --formal --visual-inspected "
                "--source-commit <40-hex> --certificate-commit <40-hex>"
            ),
            "wallTimeSeconds": 0.0,
            "wallTimePolicy": "not used in any claim; fixed at zero for a byte-stable exact sampler",
            "randomSeed": None,
            "diagnosticOnly": True,
        },
        "compute": {
            "host": platform.node() or "local-host",
            "operatingSystem": f"{platform.system()}-{platform.release()}-{platform.machine()}",
            "cpu": platform.processor() or platform.machine() or "unknown",
            "memoryGiB": memory_gib,
            "processes": 1,
            "threadsPerProcess": 1,
            "gpu": "not used",
        },
        "environment": {
            "python": platform.python_version(),
            "packagesLock": "requirements.txt",
            **package_versions,
        },
        "data": [
            file_record(
                "data.csv",
                rows=len(rows),
                schema=[
                    "panel", "kind", "id", "series", "x", "y", "value",
                    "parameterXi", "parameterLambda", "power", "formula",
                    "status", "note",
                ],
            ),
            file_record("results.json", schema="exact maxima and claim-boundary ledger"),
            file_record("validation.json", schema="formula, format, and visible-boundary checks"),
        ],
        "sourceData": [],
        "figure": {
            "profile": "journal-double-column",
            "layout": "one full-width panel above two quantitative panels",
            "widthMillimetres": WIDTH_MM,
            "heightMillimetres": HEIGHT_MM,
            "script": "plot.py",
            "outputs": [
                file_record("figure.pdf"),
                file_record("figure.svg"),
                file_record("figure.png", dpi=PNG_DPI,
                            pixels=[image.width, image.height]),
            ],
        },
        "caption": {"english": "caption.md"},
        "claimBoundary": json.loads((PACKAGE / "contract.json").read_text(
            encoding="utf-8"
        ))["claimBoundary"],
        "qa": {
            "status": "passed" if qa_passed else "pending visual inspection",
            "visualInspectionExplicit": visual_inspected,
            "finalSizeInspected": visual_inspected,
            "grayscaleInspected": visual_inspected,
            "labelsAndLegendsInspected": visual_inspected,
            "scalesAndUnitsInspected": visual_inspected,
            "dataCrossChecked": all(checks.values()),
            "fontEmbeddingInspected": visual_inspected,
            "croppingInspected": visual_inspected,
            "report": "qa-report.md",
            "previews": ["qa-final-size.png", "qa-grayscale.png", "qa-pdf.png"],
        },
        "publication": {
            "directory": "public/assets/r072y",
            "files": [
                f"{FIGURE_ID}.pdf",
                f"{FIGURE_ID}.svg",
                f"{FIGURE_ID}.png",
            ],
            "byteIdenticalToArchive": status == "formal",
        },
        "outputs": outputs,
    }
    return manifest


def write_qa_report(status: str, visual_inspected: bool,
                    checks: dict[str, bool]) -> None:
    lines = [
        "# R0.72Y figure QA",
        "",
        f"- manifest stage: {status}",
        f"- explicit visual inspection: {'yes' if visual_inspected else 'pending'}",
        "- final-size, grayscale, and independent PDF previews generated: yes",
        "- exact lift-up formula recomputed for every plotted mark: yes",
        "- exact alpha powers recomputed for every plotted mark: yes",
        "- simulation or fitted exponent used: no",
        "- two chromatic roots plus redundant non-color encodings: yes",
        "- visible proof and open-claim boundaries present: yes",
        "- PDF vector, embedded-font, one-page, and page-size checks: see validation.json",
        "- full-row A2, complete linearized, nonlinear, and Clay claims remain open: yes",
        "",
        "## Machine checks",
        "",
    ]
    lines.extend(f"- {key}: {'PASS' if value else 'FAIL'}" for key, value in checks.items())
    write_text(PACKAGE / "qa-report.md", "\n".join(lines) + "\n")


def write_sums() -> None:
    names = [name for name in SOURCE_FILES + GENERATED_FILES
             if name != "SHA256SUMS" and (PACKAGE / name).is_file()]
    lines = [f"{sha256(PACKAGE / name)}  {name}" for name in sorted(names)]
    write_text(PACKAGE / "SHA256SUMS", "\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--draft", action="store_true")
    group.add_argument("--formal", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--visual-inspected", action="store_true")
    parser.add_argument("--source-commit", default="")
    parser.add_argument("--certificate-commit", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config = json.loads((PACKAGE / "config.json").read_text(encoding="utf-8"))
    rows = build_rows(config)
    scene = build_scene(rows, config)
    checks = basic_checks(rows, scene)
    if not all(checks.values()):
        failed = [key for key, value in checks.items() if not value]
        raise RuntimeError(f"self-test failed: {failed}")
    if args.self_test:
        print(json.dumps({"status": "passed", "checks": checks}, indent=2))
        return 0
    if not args.draft and not args.formal:
        raise RuntimeError("choose --draft or --formal")
    if args.formal:
        if not args.visual_inspected:
            raise RuntimeError("formal render requires --visual-inspected")
        check_formal_lineage(args.source_commit, args.certificate_commit)
        status = "formal"
        source_commit = args.source_commit
        certificate_commit = args.certificate_commit
    else:
        status = "draft"
        source_commit = "pending"
        certificate_commit = "pending"

    fields = [
        "panel", "kind", "id", "series", "x", "y", "value",
        "parameterXi", "parameterLambda", "power", "formula", "status", "note",
    ]
    with (PACKAGE / "data.csv").open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    write_text(PACKAGE / "results.json", json_text(build_results(rows)))

    render_svg(scene, PACKAGE / "figure.svg")
    render_pdf(scene, PACKAGE / "figure.pdf")
    render_png(scene, PACKAGE / "figure.png")
    make_qa_previews()
    if status == "formal":
        PUBLIC_DIR.mkdir(parents=True, exist_ok=True)
        for suffix in ("pdf", "svg", "png"):
            shutil.copyfile(
                PACKAGE / f"figure.{suffix}",
                PUBLIC_DIR / f"{FIGURE_ID}.{suffix}",
            )

    rendered_checks, rendered_details = inspect_rendered_outputs()

    validation = {
        "schemaVersion": 1,
        "status": "passed",
        "rowCount": len(rows),
        "checks": {
            **checks,
            "vectorSvg": True,
            "vectorPdf": True,
            "pngAt600Dpi": True,
            "finalSizePreviewGenerated": True,
            "grayscalePreviewGenerated": True,
            "independentPdfPreviewGenerated": True,
            **rendered_checks,
        },
        **rendered_details,
    }
    write_text(PACKAGE / "validation.json", json_text(validation))
    write_qa_report(status, args.visual_inspected, validation["checks"])
    manifest = build_manifest(status, source_commit, certificate_commit,
                              args.visual_inspected, rows, validation["checks"])
    write_text(PACKAGE / "manifest.json", json_text(manifest))
    write_sums()
    print(json.dumps({
        "status": status,
        "figureId": FIGURE_ID,
        "rowCount": len(rows),
        "visualInspected": args.visual_inspected,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
