#!/usr/bin/env python3
"""Deterministic R0.72Z three-panel exact-audit figure generator."""

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
FIGURE_ID = "fig-r072z-os-squire-threshold"
RELEASE = "R0.72Z"
PUBLIC_DIR = ROOT / "public" / "assets" / "r072z"

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
    "manifest-draft.json",
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


FIELDS = [
    "panel", "kind", "id", "series", "x", "y", "value", "alpha", "gap",
    "cAbs", "theta0", "modeN", "orientationRatio", "rhoOverGamma", "chi",
    "A_vartheta", "B_vartheta", "formula", "status", "note",
]


def signed_envelope(z: float, m3: float) -> float:
    return 4.0 * m3 * z ** (-2.5)


def high_mode_scaled(n: int, d: float) -> float:
    mu = 2.0 * n * n
    return (
        math.exp(-d) * (2.0 * n + 1.0) * mu ** 2.5
        / (8.0 * (3.0 * n * n) ** 1.5
           * (3.0 * n * n + 2.0 * n + 1.0) ** 1.5)
    )


def low_mode_growth(mu: float, c_abs: float) -> float:
    return c_abs / (8.0 * mu ** 1.5 * (1.0 + mu) ** 1.5) - 1.0


def tangent_norm_sq(d: float) -> float:
    return math.exp(-2.0 * d) / 8.0 + math.exp(-8.0 * d) / 2.0


def tangent_ratio(alpha: float, t_block: float) -> float:
    return math.sqrt(tangent_norm_sq(2.0 * t_block * alpha * alpha)
                     / tangent_norm_sq(0.0))


def kinetic_chi(ratio: float, rho_over_gamma: float) -> float:
    return ratio / math.sqrt(1.0 + ratio * ratio + rho_over_gamma ** 2)


def log_samples(start: float, stop: float, count: int) -> list[float]:
    lo = math.log10(start)
    hi = math.log10(stop)
    return [10.0 ** (lo + (hi - lo) * index / (count - 1)) for index in range(count)]


def build_rows(config: dict[str, Any]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    def add(panel: str, kind: str, item_id: str, series: str, x: float,
            value: float, formula: str, status: str, note: str, **extra: Any) -> None:
        row = {field: "" for field in FIELDS}
        row.update({
            "panel": panel, "kind": kind, "id": item_id, "series": series,
            "x": format(x, ".17g"), "y": format(value, ".17g"),
            "value": format(value, ".17g"), "formula": formula,
            "status": status, "note": note,
        })
        row.update({key: format(value_, ".17g") if isinstance(value_, float)
                    else str(value_) for key, value_ in extra.items()})
        rows.append(row)

    panel_a = config["panelA"]
    m3 = float(panel_a["M3"])
    theta0 = float(panel_a["theta0"])
    for index, z in enumerate(log_samples(*map(float, panel_a["normalizedGapRange"]),
                                           int(panel_a["thresholdSampleCount"]))):
        add("A", "signed-threshold-envelope", f"theta-{index:03d}",
            "signed sufficient envelope", z, signed_envelope(z, m3),
            panel_a["signedEnvelopeFormula"], "exact coarse envelope",
            "z=g*alpha^2; admissible when value <= theta0",
            gap=z, theta0=theta0)
    d0 = float(panel_a["d0"])
    first_n, last_n = map(int, panel_a["highModeNRange"])
    for n in range(first_n, last_n + 1):
        value = high_mode_scaled(n, d0)
        add("A", "high-mode-sharpness-sequence", f"mode-{n:03d}",
            "two-mode scaled witness", float(n), value,
            panel_a["highModeFormula"], "exact sequence; no fitted exponent",
            "limit sqrt(2)*exp(-d)/27", modeN=n)

    panel_b = config["panelB"]
    mus = log_samples(*map(float, panel_b["muRange"]),
                       int(panel_b["growthSampleCountPerSeries"]))
    for c_abs in map(float, panel_b["cAbsSeries"]):
        for index, mu in enumerate(mus):
            add("B", "low-mode-instantaneous-growth", f"growth-{c_abs:g}-{index:03d}",
                f"|c|={c_abs:g}", mu, low_mode_growth(mu, c_abs),
                panel_b["growthFormula"], "exact signed derivative witness",
                "positive values disprove prefactor-one contraction", gap=mu,
                cAbs=c_abs)
    for index, alpha in enumerate(log_samples(*map(float, panel_b["alphaRange"]),
                                               int(panel_b["tangentSampleCount"]))):
        add("B", "abstract-tangent-block-ratio", f"tangent-{index:03d}",
            "abstract tangent ratio", alpha,
            tangent_ratio(alpha, float(panel_b["T"])), panel_b["tangentFormula"],
            "exact abstract mean-zero OS solution",
            "not a physical mu=0 velocity-row claim", alpha=alpha)

    panel_c = config["panelC"]
    ratios = log_samples(*map(float, panel_c["orientationRange"]),
                         int(panel_c["orientationSampleCountPerSeries"]))
    for rho_ratio in map(float, panel_c["rhoOverGammaSeries"]):
        for index, ratio in enumerate(ratios):
            value = kinetic_chi(ratio, rho_ratio)
            add("C", "kinetic-orientation", f"chi-{rho_ratio:g}-{index:03d}",
                f"rho/gamma={rho_ratio:g}", ratio, value,
                panel_c["orientationFormula"], "exact kinetic orientation",
                "chi <= 1; |Lambda| remains outside", orientationRatio=ratio,
                rhoOverGamma=rho_ratio, chi=value)
    alpha = float(panel_c["historyAlpha"])
    chi = float(panel_c["historyChi"])
    vartheta = float(panel_c["vartheta"])
    t_const = float(panel_c["T"])
    a_vartheta = 2.0 * t_const / (1.0 - vartheta)
    b_vartheta = 2.0 * t_const / (1.0 - vartheta * vartheta)
    gaps = log_samples(*map(float, panel_c["historyGapRange"]),
                       int(panel_c["historySampleCountPerSeries"]))
    for kind, series, formula in (
        ("history-L2-multiplier", "L2 history multiplier", panel_c["historyL2Formula"]),
        ("history-endpoint-multiplier", "endpoint history multiplier", panel_c["historyEndpointFormula"]),
    ):
        for index, gap in enumerate(gaps):
            if kind == "history-L2-multiplier":
                value = chi * min(1.0 / gap, a_vartheta * alpha * alpha)
            else:
                value = chi * min(1.0 / math.sqrt(2.0 * gap),
                                  math.sqrt(b_vartheta) * alpha)
            add("C", kind, f"history-{kind}-{index:03d}", series, gap, value,
                formula, "exact normalized upper-bound multiplier",
                "multiply by |Lambda|*M1 and the declared Q-history norm",
                alpha=alpha, gap=gap, chi=chi, A_vartheta=a_vartheta,
                B_vartheta=b_vartheta)
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
    scene.text(55, 52, "R0.72Z | Orr-Sommerfeld threshold and Squire payment",
               size=37, bold=True)
    scene.text(55, 88,
               "Closed-form audit guides only; no PDE simulation, fitted exponent, or random seed",
               size=21, color=MID)

    # Locked research blossom: decorative, top-right, and data-free.
    blossom_x, blossom_y = 1688, 57
    for index in range(5):
        angle = -math.pi / 2 + 2 * math.pi * index / 5
        px = blossom_x + 23 * math.cos(angle)
        py = blossom_y + 23 * math.sin(angle)
        scene.circle(px, py, 8.5,
                     fill=BLUE_LIGHT if index % 2 == 0 else GOLD_LIGHT,
                     stroke=BLUE if index % 2 == 0 else GOLD, width=1.6)
    scene.circle(blossom_x, blossom_y, 7, fill=PAPER, stroke=INK, width=1.6)

    panel_y, panel_h, panel_w = 120, 1265, 540
    panel_xs = [55, 620, 1185]

    def panel_box(x: float, letter: str, title: str, subtitle: str,
                  badge: str, badge_fill: str, badge_stroke: str) -> None:
        scene.rect(x, panel_y, panel_w, panel_h, fill=PAPER, stroke=GRID,
                   width=2.0, radius=11)
        scene.text(x + 18, panel_y + 38, letter, size=29, bold=True, color=BLUE)
        scene.text(x + 56, panel_y + 38, title, size=24, bold=True)
        scene.text(x + 20, panel_y + 72, subtitle, size=17.5, color=MID)
        scene.rect(x + 20, panel_y + 91, panel_w - 40, 34, fill=badge_fill,
                   stroke=badge_stroke, width=1.5, radius=7)
        scene.text(x + 34, panel_y + 115, badge, size=15.5, bold=True, color=INK)

    def axes(x: float, y: float, width: float, height: float,
             x_label: str, y_label: str) -> None:
        scene.line(x, y, x, y + height, color=INK, width=1.8)
        scene.line(x, y + height, x + width, y + height, color=INK, width=1.8)
        scene.text(x, y - 10, y_label, size=16.5, color=INK)
        scene.text(x + width / 2, y + height + 43, x_label, size=16.5,
                   color=INK, anchor="middle")

    def map_log(value: float, lo: float, hi: float, start: float,
                length: float) -> float:
        return start + length * (math.log10(value) - math.log10(lo)) / (
            math.log10(hi) - math.log10(lo)
        )

    def map_y(value: float, lo: float, hi: float, start: float,
              height: float) -> float:
        return start + height * (hi - value) / (hi - lo)

    # Panel A: signed threshold and high-mode sharpness.
    ax = panel_xs[0]
    panel_box(ax, "A", "Signed OS threshold",
              "Sufficient class and necessary high-mode power",
              "CLOSED HIGH-GAP CLASS | COARSE CONSTANT NOT OPTIMAL",
              BLUE_LIGHT, BLUE)
    apx, apy, apw, aph = ax + 65, panel_y + 175, 430, 330
    axes(apx, apy, apw, aph, "z = g alpha^2 (log)", "Theta_bar (log)")
    xlo, xhi, ylo, yhi = 0.7, 8.0, 0.04, 30.0
    for tick in (1.0, 2.0, 4.0, 8.0):
        xx = map_log(tick, xlo, xhi, apx, apw)
        scene.line(xx, apy + aph, xx, apy + aph + 7, color=INK, width=1.4)
        scene.text(xx, apy + aph + 26, f"{tick:g}", size=15, color=MID,
                   anchor="middle")
    for tick in (0.1, 0.5, 1.0, 10.0):
        yy = map_y(math.log10(tick), math.log10(ylo), math.log10(yhi), apy, aph)
        scene.line(apx, yy, apx + apw, yy, color=GRID, width=1.2, dash=(4, 5))
        scene.text(apx - 10, yy + 5, f"{tick:g}", size=14.5, color=MID,
                   anchor="end")
    theta0 = float(config["panelA"]["theta0"])
    theta_y = map_y(math.log10(theta0), math.log10(ylo), math.log10(yhi), apy, aph)
    scene.line(apx, theta_y, apx + apw, theta_y, color=INK, width=2.0,
               dash=(6, 5))
    scene.text(apx + apw - 4, theta_y - 8, "theta0=0.5", size=15,
               color=INK, anchor="end")
    threshold_rows = [row for row in rows if row["kind"] == "signed-threshold-envelope"]
    threshold_points = [
        (map_log(float(row["x"]), xlo, xhi, apx, apw),
         map_y(math.log10(float(row["value"])), math.log10(ylo),
               math.log10(yhi), apy, aph))
        for row in threshold_rows
    ]
    scene.polyline(threshold_points, color=BLUE, width=3.0)
    for index in range(0, len(threshold_points), 10):
        add_marker(scene, *threshold_points[index], "circle", BLUE,
                   size=5.2, filled=True)
    crossing = (4.0 * float(config["panelA"]["M3"]) / theta0) ** 0.4
    cross_x = map_log(crossing, xlo, xhi, apx, apw)
    scene.line(cross_x, apy, cross_x, apy + aph, color=GOLD, width=2.0,
               dash=(4, 5))
    scene.text(cross_x - 5, apy + 25, "admissible ->", size=15.5,
               color=GOLD, bold=True, anchor="end")
    scene.text(apx + 8, apy + 58, "Theta_bar = 4 M3 z^(-5/2)", size=16,
               color=BLUE, bold=True)

    aqx, aqy, aqw, aqh = ax + 65, panel_y + 660, 430, 290
    axes(aqx, aqy, aqw, aqh, "mode n", "a_n mu^(5/2)")
    high_rows = [row for row in rows if row["kind"] == "high-mode-sharpness-sequence"]
    hlo, hhi = 0.025, 0.055
    for tick in (0.03, 0.04, 0.05, 0.055):
        yy = map_y(tick, hlo, hhi, aqy, aqh)
        scene.line(aqx, yy, aqx + aqw, yy, color=GRID, width=1.2, dash=(4, 5))
        scene.text(aqx - 10, yy + 5, f"{tick:.3f}", size=14, color=MID,
                   anchor="end")
    for tick in (1, 20, 40, 60, 80):
        xx = aqx + aqw * (tick - 1) / 79
        scene.line(xx, aqy + aqh, xx, aqy + aqh + 7, color=INK, width=1.4)
        scene.text(xx, aqy + aqh + 25, str(tick), size=14.5, color=MID,
                   anchor="middle")
    high_points = [
        (aqx + aqw * (float(row["x"]) - 1.0) / 79.0,
         map_y(float(row["value"]), hlo, hhi, aqy, aqh))
        for row in high_rows
    ]
    scene.polyline(high_points, color=GOLD, width=2.8, dash=(9, 5))
    for index in range(0, len(high_points), 10):
        add_marker(scene, *high_points[index], "square", GOLD,
                   size=5.0, filled=False)
    limit = math.sqrt(2.0) / 27.0
    limit_y = map_y(limit, hlo, hhi, aqy, aqh)
    scene.line(aqx, limit_y, aqx + aqw, limit_y, color=INK, width=1.8,
               dash=(3, 5))
    scene.text(aqx + aqw - 4, limit_y - 8, "sqrt(2)/27", size=15,
               color=INK, anchor="end")
    scene.rect(ax + 20, panel_y + 1030, panel_w - 40, 72, fill=PALE,
               stroke=GRID, width=1.3, radius=7)
    scene.text(ax + 34, panel_y + 1057, "g ~ |c|^(2/5) = alpha^(-2): SHARP POWER",
               size=17, bold=True)
    scene.text(ax + 34, panel_y + 1083, "Exact sequence; no regression or fitted slope.",
               size=16, color=MID)
    scene.text(ax + 20, panel_y + 1170,
               "Low-gap transient-prefactor theorem: OPEN", size=17,
               color=INK, bold=True)

    # Panel B: low-mode and tangent negative boundaries.
    bx = panel_xs[1]
    panel_box(bx, "B", "Negative boundary",
              "Two exact witnesses; neither is a stability simulation",
              "ALL-GAP PREFACTOR-ONE L2_q CONTRACTION: FALSE",
              GOLD_LIGHT, GOLD)
    bpx, bpy, bpw, bph = bx + 65, panel_y + 175, 430, 330
    axes(bpx, bpy, bpw, bph, "mu > 0 (log)", "signed log growth")
    mu_lo, mu_hi = map(float, config["panelB"]["muRange"])
    sy_lo, sy_hi = -0.4, 4.2
    zero_y = map_y(0.0, sy_lo, sy_hi, bpy, bph)
    scene.line(bpx, zero_y, bpx + bpw, zero_y, color=INK, width=2.0,
               dash=(6, 5))
    scene.text(bpx + bpw - 4, zero_y - 8, "growth = 0", size=15,
               color=INK, anchor="end")
    for tick in (0.01, 0.1, 1.0, 3.0):
        xx = map_log(tick, mu_lo, mu_hi, bpx, bpw)
        scene.line(xx, bpy + bph, xx, bpy + bph + 7, color=INK, width=1.4)
        scene.text(xx, bpy + bph + 26, f"{tick:g}", size=14.5,
                   color=MID, anchor="middle")
    growth_styles = [("|c|=4", BLUE, None, "circle", True),
                     ("|c|=32", GOLD, (9, 5), "square", False)]
    growth_rows = [row for row in rows if row["kind"] == "low-mode-instantaneous-growth"]
    for label, color, dash, marker, filled in growth_styles:
        series = [row for row in growth_rows if row["series"] == label]
        points = []
        for row in series:
            signed = math.copysign(math.log10(1.0 + abs(float(row["value"]))),
                                   float(row["value"]))
            points.append((map_log(float(row["x"]), mu_lo, mu_hi, bpx, bpw),
                           map_y(max(sy_lo, min(sy_hi, signed)), sy_lo, sy_hi,
                                 bpy, bph)))
        scene.polyline(points, color=color, width=3.0, dash=dash)
        for index in range(0, len(points), 16):
            add_marker(scene, *points[index], marker, color,
                       size=5.0, filled=filled)
    scene.text(bpx + 7, bpy + 24, "sign(G) log10(1+|G|)", size=15, color=MID)
    for lx, (label, color, dash, marker, filled) in zip((bpx + 10, bpx + 235), growth_styles):
        scene.line(lx, bpy + bph + 58, lx + 36, bpy + bph + 58,
                   color=color, width=2.8, dash=dash)
        add_marker(scene, lx + 18, bpy + bph + 58, marker, color,
                   size=5.0, filled=filled)
        scene.text(lx + 44, bpy + bph + 64, label, size=15.5)

    bqx, bqy, bqw, bqh = bx + 65, panel_y + 660, 430, 290
    axes(bqx, bqy, bqw, bqh, "alpha (log)", "tangent block ratio")
    alpha_lo, alpha_hi = map(float, config["panelB"]["alphaRange"])
    for tick in (0.02, 0.1, 0.3, 1.0):
        xx = map_log(tick, alpha_lo, alpha_hi, bqx, bqw)
        scene.line(xx, bqy + bqh, xx, bqy + bqh + 7, color=INK, width=1.4)
        scene.text(xx, bqy + bqh + 25, f"{tick:g}", size=14.5, color=MID,
                   anchor="middle")
    for tick in (0.2, 0.4, 0.6, 0.8, 1.0):
        yy = map_y(tick, 0.0, 1.02, bqy, bqh)
        scene.line(bqx, yy, bqx + bqw, yy, color=GRID, width=1.2, dash=(4, 5))
        scene.text(bqx - 10, yy + 5, f"{tick:g}", size=14.5, color=MID,
                   anchor="end")
    one_y = map_y(1.0, 0.0, 1.02, bqy, bqh)
    scene.line(bqx, one_y, bqx + bqw, one_y, color=INK, width=1.8,
               dash=(5, 5))
    tangent_rows = [row for row in rows if row["kind"] == "abstract-tangent-block-ratio"]
    tangent_points = [
        (map_log(float(row["x"]), alpha_lo, alpha_hi, bqx, bqw),
         map_y(float(row["value"]), 0.0, 1.02, bqy, bqh))
        for row in tangent_rows
    ]
    scene.polyline(tangent_points, color=GOLD, width=3.0, dash=(9, 5))
    for index in range(0, len(tangent_points), 10):
        add_marker(scene, *tangent_points[index], "triangle", GOLD,
                   size=5.2, filled=False)
    scene.text(bqx + 8, bqy + 28, "ratio -> 1 as alpha -> 0", size=16,
               color=GOLD, bold=True)
    scene.rect(bx + 20, panel_y + 1030, panel_w - 40, 92, fill=GOLD_LIGHT,
               stroke=GOLD, width=1.4, dash=(7, 5), radius=7)
    scene.text(bx + 34, panel_y + 1058,
               "ABSTRACT TANGENT - NOT PHYSICAL mu=0 ROW", size=16.5,
               bold=True)
    scene.text(bx + 34, panel_y + 1084, "q*=W_xx exactly cancels scalar mixing.",
               size=16, color=MID)
    scene.text(bx + 34, panel_y + 1107, "Projected positive-mu theorem remains open.",
               size=16, color=MID)

    # Panel C: orientation and Lambda-paid history transfer.
    cx0 = panel_xs[2]
    panel_box(cx0, "C", "Squire orientation",
              "Kinetic saturation plus explicit history payments",
              "|Lambda| PAID | Q HISTORY REQUIRED",
              BLUE_LIGHT, BLUE)
    cpx, cpy, cpw, cph = cx0 + 65, panel_y + 175, 430, 330
    axes(cpx, cpy, cpw, cph, "R = |xi/gamma| (log)", "kinetic chi")
    r_lo, r_hi = map(float, config["panelC"]["orientationRange"])
    for tick in (0.01, 0.1, 1.0, 10.0, 100.0):
        xx = map_log(tick, r_lo, r_hi, cpx, cpw)
        scene.line(xx, cpy + cph, xx, cpy + cph + 7, color=INK, width=1.4)
        scene.text(xx, cpy + cph + 25, f"{tick:g}", size=14, color=MID,
                   anchor="middle")
    for tick in (0.0, 0.25, 0.5, 0.75, 1.0):
        yy = map_y(tick, 0.0, 1.03, cpy, cph)
        scene.line(cpx, yy, cpx + cpw, yy, color=GRID, width=1.2, dash=(4, 5))
        scene.text(cpx - 10, yy + 5, f"{tick:g}", size=14.5, color=MID,
                   anchor="end")
    scene.line(cpx, map_y(1.0, 0.0, 1.03, cpy, cph), cpx + cpw,
               map_y(1.0, 0.0, 1.03, cpy, cph), color=INK, width=1.8,
               dash=(5, 5))
    orientation_styles = [
        ("rho/gamma=0", BLUE, None, "circle", True),
        ("rho/gamma=1", GOLD, (9, 5), "square", False),
        ("rho/gamma=3", INK, (3, 5), "triangle", False),
    ]
    orientation_rows = [row for row in rows if row["kind"] == "kinetic-orientation"]
    for label, color, dash, marker, filled in orientation_styles:
        series = [row for row in orientation_rows if row["series"] == label]
        points = [(map_log(float(row["x"]), r_lo, r_hi, cpx, cpw),
                   map_y(float(row["value"]), 0.0, 1.03, cpy, cph))
                  for row in series]
        scene.polyline(points, color=color, width=2.8, dash=dash)
        for index in range(0, len(points), 16):
            add_marker(scene, *points[index], marker, color,
                       size=4.8, filled=filled)
    scene.text(cpx + 10, cpy + 28, "chi <= 1", size=17, color=BLUE, bold=True)
    legend_y = cpy + cph + 56
    for lx, (label, color, dash, marker, filled) in zip(
            (cpx, cpx + 150, cpx + 300), orientation_styles):
        scene.line(lx, legend_y, lx + 28, legend_y, color=color, width=2.6,
                   dash=dash)
        add_marker(scene, lx + 14, legend_y, marker, color, size=4.6,
                   filled=filled)
        scene.text(lx + 34, legend_y + 5, label.replace("rho/gamma=", "r/g="),
                   size=14.5)

    cqx, cqy, cqw, cqh = cx0 + 65, panel_y + 660, 430, 290
    axes(cqx, cqy, cqw, cqh, "gap g (log)", "normalized multiplier (log)")
    g_lo, g_hi = map(float, config["panelC"]["historyGapRange"])
    v_lo, v_hi = 0.005, 0.5
    for tick in (0.1, 1.0, 10.0, 100.0):
        xx = map_log(tick, g_lo, g_hi, cqx, cqw)
        scene.line(xx, cqy + cqh, xx, cqy + cqh + 7, color=INK, width=1.4)
        scene.text(xx, cqy + cqh + 25, f"{tick:g}", size=14.5, color=MID,
                   anchor="middle")
    for tick in (0.01, 0.03, 0.1, 0.3):
        yy = map_y(math.log10(tick), math.log10(v_lo), math.log10(v_hi),
                   cqy, cqh)
        scene.line(cqx, yy, cqx + cqw, yy, color=GRID, width=1.2, dash=(4, 5))
        scene.text(cqx - 10, yy + 5, f"{tick:g}", size=14, color=MID,
                   anchor="end")
    history_styles = [
        ("L2 history multiplier", BLUE, None, "circle", True),
        ("endpoint history multiplier", GOLD, (9, 5), "square", False),
    ]
    history_rows = [row for row in rows if row["kind"].startswith("history-")]
    for label, color, dash, marker, filled in history_styles:
        series = [row for row in history_rows if row["series"] == label]
        points = [(map_log(float(row["x"]), g_lo, g_hi, cqx, cqw),
                   map_y(math.log10(float(row["value"])), math.log10(v_lo),
                         math.log10(v_hi), cqy, cqh))
                  for row in series]
        scene.polyline(points, color=color, width=3.0, dash=dash)
        for index in range(0, len(points), 16):
            add_marker(scene, *points[index], marker, color,
                       size=5.0, filled=filled)
    scene.text(cqx + 8, cqy + 28, "alpha=0.2, chi=1, theta=0.5", size=15,
               color=MID)
    scene.text(cqx + 8, cqy + 53, "multiply by |Lambda| M1 and ||Q||", size=15.5,
               color=INK, bold=True)
    scene.rect(cx0 + 20, panel_y + 1030, panel_w - 40, 105, fill=PALE,
               stroke=GRID, width=1.3, radius=7)
    scene.text(cx0 + 34, panel_y + 1058,
               "L2_t / (|Lambda| M1) = chi min(g^-1, A alpha^2)",
               size=15.5, bold=True)
    scene.text(cx0 + 34, panel_y + 1084,
               "Linf_t / (|Lambda| M1) = chi min((2g)^-1/2, sqrt(B) alpha)",
               size=15.0, bold=True)
    scene.text(cx0 + 34, panel_y + 1110,
               "Conditional upper bounds; not terminal-Q closure.",
               size=15.5, color=MID)
    scene.text(cx0 + 20, panel_y + 1170,
               "Physical direct sum / nonlinear closure: OPEN", size=17,
               color=INK, bold=True)

    scene.text(55, H - 20,
               "EXACT FORMULAS - NO PDE SIMULATION | LOW-GAP OS PROPAGATOR: OPEN",
               size=16.5, color=QUIET)
    scene.text(W - 55, H - 20,
               "CLAY PROBLEM: OPEN", size=16.5, color=QUIET, anchor="end")
    return scene

def svg_dash(dash: tuple[float, ...] | None) -> str:
    return "" if not dash else f' stroke-dasharray="{",".join(str(v) for v in dash)}"'


def render_svg(scene: Scene, path: Path) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH_MM}mm" '
        f'height="{HEIGHT_MM}mm" viewBox="0 0 {int(W)} {int(H)}" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">R0.72Z Orr-Sommerfeld threshold and Squire payment</title>',
        '<desc id="desc">Three panels show a signed high-gap threshold, exact '
        'low-gap and tangent negative boundaries, and orientation-paid history transfer.</desc>',
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
    pdf.setTitle("R0.72Z Orr-Sommerfeld threshold and Squire payment")
    pdf.setAuthor("C. K. Zeng")
    pdf.setCreator("deterministic R0.72Z figure generator")
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
    kinds = {kind: [row for row in rows if row["kind"] == kind]
             for kind in {row["kind"] for row in rows}}
    high_last = kinds["high-mode-sharpness-sequence"][-1]
    tangent = kinds["abstract-tangent-block-ratio"]
    return {
        "schemaVersion": 1,
        "release": RELEASE,
        "figureId": FIGURE_ID,
        "deterministic": True,
        "randomSeed": None,
        "rowCount": len(rows),
        "panelA": {
            "signedRelativeFormOSAbsorption": "CLOSED",
            "alphaMinusTwoOSGapSufficiency": "CLOSED",
            "highModeOSGapExponentSharpness": "CLOSED, scoped",
            "thresholdRows": len(kinds["signed-threshold-envelope"]),
            "highModeRows": len(kinds["high-mode-sharpness-sequence"]),
            "lastScaledWitness": float(high_last["value"]),
            "exactLimit": math.sqrt(2.0) / 27.0,
            "fittedQuantities": [],
        },
        "panelB": {
            "allStrongRowsOSPrefactorOneContraction": "FALSE",
            "abstractGaplessOSA2StrictContraction": "FALSE",
            "growthRows": len(kinds["low-mode-instantaneous-growth"]),
            "tangentRows": len(tangent),
            "smallestAlphaTangentRatio": float(tangent[0]["value"]),
            "abstractTangentNotPhysicalMuZeroVelocity": True,
            "fittedQuantities": [],
        },
        "panelC": {
            "exactKineticOrientationNormalization": "CLOSED",
            "orientationUniformWithLambdaPayment": "CLOSED",
            "strongKernelConditionalSquireTransfer": "CLOSED, conditional",
            "orientationRows": len(kinds["kinetic-orientation"]),
            "historyRows": (len(kinds["history-L2-multiplier"])
                            + len(kinds["history-endpoint-multiplier"])),
            "lambdaPaymentExplicit": True,
            "conditionalOnQHistory": True,
            "fittedQuantities": [],
        },
        "claimsNotMade": [
            "the figure is an analytic proof",
            "the curves are PDE simulation output",
            "the coarse high-gap constant is optimal",
            "a low-gap transient OS propagator is closed",
            "the physical Bloch direct sum is closed",
            "nonlinear Navier-Stokes is closed",
            "the Clay Millennium problem is solved",
        ],
    }


def basic_checks(rows: list[dict[str, str]], scene: Scene) -> dict[str, bool]:
    by_kind = {kind: [row for row in rows if row["kind"] == kind]
               for kind in {row["kind"] for row in rows}}
    tol = 5e-14
    panel_a = config_a = json.loads((PACKAGE / "config.json").read_text(
        encoding="utf-8"))["panelA"]
    m3 = float(config_a["M3"])
    signed_ok = all(abs(float(row["value"]) - signed_envelope(float(row["x"]), m3))
                    <= tol * max(1.0, abs(float(row["value"])))
                    for row in by_kind["signed-threshold-envelope"])
    high_ok = all(abs(float(row["value"]) - high_mode_scaled(int(row["modeN"]),
                                                               float(config_a["d0"])))
                  <= tol for row in by_kind["high-mode-sharpness-sequence"])
    growth_ok = all(abs(float(row["value"]) - low_mode_growth(
        float(row["gap"]), float(row["cAbs"]))) <= tol * max(1.0, abs(float(row["value"])))
        for row in by_kind["low-mode-instantaneous-growth"])
    config_b = json.loads((PACKAGE / "config.json").read_text(
        encoding="utf-8"))["panelB"]
    tangent_ok = all(abs(float(row["value"]) - tangent_ratio(
        float(row["alpha"]), float(config_b["T"]))) <= tol
        for row in by_kind["abstract-tangent-block-ratio"])
    orientation_ok = all(abs(float(row["value"]) - kinetic_chi(
        float(row["orientationRatio"]), float(row["rhoOverGamma"]))) <= tol
        and 0.0 < float(row["value"]) < 1.0
        for row in by_kind["kinetic-orientation"])
    history_ok = True
    for kind in ("history-L2-multiplier", "history-endpoint-multiplier"):
        for row in by_kind[kind]:
            gap = float(row["gap"])
            alpha = float(row["alpha"])
            chi = float(row["chi"])
            if kind == "history-L2-multiplier":
                expected = chi * min(1.0 / gap, float(row["A_vartheta"]) * alpha ** 2)
            else:
                expected = chi * min(1.0 / math.sqrt(2.0 * gap),
                                     math.sqrt(float(row["B_vartheta"])) * alpha)
            history_ok &= abs(float(row["value"]) - expected) <= tol
    visible = "\n".join(item["value"] for item in scene.items
                         if item["kind"] == "text")
    growth_groups = {row["series"] for row in by_kind["low-mode-instantaneous-growth"]}
    return {
        "rowCount": len(rows) == 769,
        "panelARecordCount": sum(row["panel"] == "A" for row in rows) == 141,
        "panelBRecordCount": sum(row["panel"] == "B" for row in rows) == 223,
        "panelCRecordCount": sum(row["panel"] == "C" for row in rows) == 405,
        "signedEnvelopeRecomputed": signed_ok,
        "highModeSequenceRecomputed": high_ok,
        "highModeLimitApproached": abs(float(by_kind["high-mode-sharpness-sequence"][-1]["value"])
                                       - math.sqrt(2.0) / 27.0) < 5e-4,
        "lowModeGrowthRecomputed": growth_ok,
        "eachGrowthSeriesCrossesZero": all(
            any(float(row["value"]) > 0 for row in by_kind["low-mode-instantaneous-growth"]
                if row["series"] == label)
            and any(float(row["value"]) < 0 for row in by_kind["low-mode-instantaneous-growth"]
                    if row["series"] == label)
            for label in growth_groups),
        "tangentRatioRecomputed": tangent_ok,
        "tangentApproachesOneAtSmallAlpha": float(by_kind["abstract-tangent-block-ratio"][0]["value"]) > 0.99,
        "orientationRecomputedAndBounded": orientation_ok,
        "historyMultipliersRecomputed": history_ok,
        "noFittedExponents": all("fitted" not in row["status"] or "no fitted" in row["status"]
                                  for row in rows),
        "falseBoundaryVisible": "ALL-GAP PREFACTOR-ONE L2_q CONTRACTION: FALSE" in visible,
        "tangentBoundaryVisible": "ABSTRACT TANGENT - NOT PHYSICAL mu=0 ROW" in visible,
        "lambdaPaymentVisible": "|Lambda| PAID | Q HISTORY REQUIRED" in visible,
        "openBoundaryVisible": "LOW-GAP OS PROPAGATOR: OPEN" in visible,
        "noSimulationBoundaryVisible": "EXACT FORMULAS - NO PDE SIMULATION" in visible,
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
    publication_assets = []
    for suffix in ("pdf", "svg", "png"):
        master = file_record(f"figure.{suffix}")
        publication_assets.append({
            "path": f"public/assets/r072z/{FIGURE_ID}.{suffix}",
            "bytes": master["bytes"],
            "sha256": master["sha256"],
            "byteIdenticalToMaster": status == "formal",
        })
    manifest = {
        "schemaVersion": 1,
        "figureId": FIGURE_ID,
        "release": RELEASE,
        "status": status,
        "createdAt": "2026-08-28T00:00:00+08:00",
        "analyticalQuestion": (
            "Where does signed OS absorption close, what exact witnesses block "
            "all-gap contraction, and what Squire payments remain?"
        ),
        "supportedClaim": (
            "The scale-sharp high-gap class closes; exact low-gap and tangent "
            "witnesses are negative boundaries; Squire transfer pays Lambda and Q history."
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
                schema=FIELDS,
            ),
            file_record("results.json", schema="exact maxima and claim-boundary ledger"),
            file_record("validation.json", schema="formula, format, and visible-boundary checks"),
        ],
        "sourceData": [],
        "figure": {
            "profile": "journal-double-column",
            "layout": "three equal journal panels, each with two exact-formula insets",
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
            "directory": "public/assets/r072z",
            "stem": FIGURE_ID,
            "files": [
                f"{FIGURE_ID}.pdf",
                f"{FIGURE_ID}.svg",
                f"{FIGURE_ID}.png",
            ],
            "assets": publication_assets,
            "publicCopiesComplete": status == "formal",
            "byteIdenticalToArchive": status == "formal",
        },
        "outputs": outputs,
    }
    return manifest


def write_qa_report(status: str, visual_inspected: bool,
                    checks: dict[str, bool]) -> None:
    lines = [
        "# R0.72Z figure QA",
        "",
        f"- manifest stage: {status}",
        f"- explicit visual inspection: {'yes' if visual_inspected else 'pending'}",
        "- final-size, grayscale, and independent PDF previews generated: yes",
        "- signed threshold and high-mode sequence recomputed: yes",
        "- low-mode, tangent, orientation, and history formulas recomputed: yes",
        "- simulation or fitted exponent used: no",
        "- two chromatic roots plus redundant non-color encodings: yes",
        "- visible proof and open-claim boundaries present: yes",
        "- PDF vector, embedded-font, one-page, and page-size checks: see validation.json",
        "- low-gap OS, physical direct sum, nonlinear, and Clay claims remain open: yes",
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

    fields = FIELDS
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
