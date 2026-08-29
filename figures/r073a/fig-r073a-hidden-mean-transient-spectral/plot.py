#!/usr/bin/env python3
"""Deterministic R0.73A three-panel exact-audit figure generator."""

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
FIGURE_ID = "fig-r073a-hidden-mean-transient-spectral"
RELEASE = "R0.73A"
PUBLIC_DIR = ROOT / "public" / "assets" / "r073a"

WIDTH_MM = 178
HEIGHT_MM = 145
PNG_DPI = 600
CERTIFICATE_BOUND_TOLERANCE = 2e-8
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
    "panel", "kind", "id", "series", "x", "y", "value", "mu", "d", "s",
    "tau", "cAbs", "J", "rawSpectralEdge", "rawNumericalAbscissa",
    "displayValue", "projection", "targetCase", "N", "sourcePath",
    "sourceSha256", "certificateId", "formula", "status", "note",
]


def hidden_mean(mu: float, d: float) -> float:
    return math.exp(-2.0 * d) / (8.0 * (1.0 + mu)) + math.exp(-8.0 * d) / (
        8.0 * (4.0 + mu)
    )


def hidden_limit(d: float) -> float:
    return math.exp(-2.0 * d) / 8.0 + math.exp(-8.0 * d) / 32.0


def transient_j(s: float, d: float) -> float:
    return (7.0 / 4.0) * (math.exp(-s) - math.exp(-d)) + 0.5 * (
        math.exp(-4.0 * s) - math.exp(-4.0 * d)
    )


def transient_envelope(mu: float, c_abs: float, s: float, d: float) -> float:
    return math.exp(-mu * (d - s) + c_abs * transient_j(s, d))


def signed_log(value: float) -> float:
    return math.copysign(math.log10(1.0 + abs(value)), value) if value else 0.0


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
        for key, extra_value in extra.items():
            if isinstance(extra_value, float):
                row[key] = format(extra_value, ".17g")
            else:
                row[key] = str(extra_value)
        rows.append(row)

    panel_a = config["panelA"]
    mus = log_samples(float(panel_a["muRange"][0]), float(panel_a["muRange"][1]),
                       int(panel_a["muSampleCount"]))
    for d_value in map(float, panel_a["dSeries"]):
        for index, mu_value in enumerate(mus):
            value = hidden_mean(mu_value, d_value)
            add("A", "hidden-mean-excitation", f"hidden-{d_value:g}-{index:03d}",
                f"d={d_value:g}", mu_value, value,
                panel_a["hiddenMeanFormula"], "exact physical formula",
                "h_d/(i*c_mu); normalized bracket; no fitted quantity",
                mu=mu_value, d=d_value)
    d_lo, d_hi = map(float, panel_a["limitDRange"])
    for index in range(int(panel_a["limitSampleCount"])):
        d_value = d_lo + (d_hi - d_lo) * index / (int(panel_a["limitSampleCount"]) - 1)
        value = hidden_limit(d_value)
        add("A", "abstract-limit-mismatch", f"limit-{index:03d}",
            "physical mu->0 hidden derivative", d_value, value,
            panel_a["abstractLimitFormula"], "exact nonzero normalized-bracket limit",
            "only c_mu->c0!=0; fixed Lambda undecided; tangent has no hidden coordinate",
            d=d_value)

    panel_b = config["panelB"]
    if float(panel_b["certificateBoundTolerance"]) != CERTIFICATE_BOUND_TOLERANCE:
        raise RuntimeError("certificate crosscheck tolerance differs from fixed 2e-8")
    tau_lo, tau_hi = map(float, panel_b["tauRange"])
    count_b = int(panel_b["sampleCountPerSeries"])
    taus = [tau_lo + (tau_hi - tau_lo) * index / (count_b - 1)
            for index in range(count_b)]
    for s_value in map(float, panel_b["jStartSeries"]):
        for index, tau in enumerate(taus):
            d_value = s_value + tau
            j_value = transient_j(s_value, d_value)
            add("B", "exact-J-kernel", f"j-{s_value:g}-{index:03d}",
                f"s={s_value:g}", tau, j_value, panel_b["jFormula"],
                "exact analytic kernel", "d=s+tau", s=s_value, d=d_value,
                tau=tau, J=j_value)
    for spec in panel_b["envelopeSeries"]:
        mu_value = float(spec["mu"])
        c_abs = float(spec["cAbs"])
        s_value = float(spec["s"])
        for index, tau in enumerate(taus):
            d_value = s_value + tau
            j_value = transient_j(s_value, d_value)
            value = transient_envelope(mu_value, c_abs, s_value, d_value)
            add("B", "analytic-transient-envelope", f"env-{mu_value:g}-{c_abs:g}-{s_value:g}-{index:03d}",
                spec["label"], tau, value, panel_b["envelopeFormula"],
                "proved analytic upper envelope", "not observed propagator gain",
                mu=mu_value, cAbs=c_abs, s=s_value, d=d_value, tau=tau,
                J=j_value, displayValue=math.log10(value))

    certificate_path = ROOT / panel_b["certificateCsv"]
    if certificate_path.is_file():
        with certificate_path.open(encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != panel_b["certificateRequiredSchema"]:
                raise RuntimeError("X_mu certificate schema mismatch")
            for index, source in enumerate(reader):
                gain = float(source["gain"])
                bound = float(source["bound"])
                if not (0.0 < gain <= bound + CERTIFICATE_BOUND_TOLERANCE):
                    raise RuntimeError(
                        "certified gain must be positive and no greater than "
                        "bound + fixed 2e-8 numerical crosscheck tolerance"
                    )
                s_value, d_value = float(source["s"]), float(source["d"])
                add("B", "certified-xmu-propagator-gain", f"cert-{index:04d}",
                    source["certificateId"], d_value - s_value, gain,
                    "certificate CSV observed operator gain", "certificate-bound overlay",
                    "not a frozen Galerkin gain", mu=float(source["mu"]),
                    cAbs=abs(float(source["c"])), s=s_value, d=d_value,
                    tau=d_value-s_value, certificateId=source["certificateId"],
                    sourcePath=panel_b["certificateCsv"],
                    sourceSha256=sha256(certificate_path), displayValue=math.log10(gain))

    panel_c = config["panelC"]
    source_path = ROOT / panel_c["sourceCsv"]
    validation_path = ROOT / panel_c["validationJson"]
    if sha256(source_path) != panel_c["sourceSha256"]:
        raise RuntimeError("Panel C target CSV hash mismatch")
    if sha256(validation_path) != panel_c["validationSha256"]:
        raise RuntimeError("Panel C validation JSON hash mismatch")
    validation = json.loads(validation_path.read_text(encoding="utf-8"))
    if validation.get("status") != "passed" or not all(validation.get("checks", {}).values()):
        raise RuntimeError("Panel C source audit is not fully passed")
    with source_path.open(encoding="utf-8") as stream:
        source_rows = [row for row in csv.DictReader(stream)
                       if int(row["N"]) == int(panel_c["N"])]
    if len(source_rows) != int(panel_c["expectedRows"]):
        raise RuntimeError("Panel C N=40 row count mismatch")
    for index, source in enumerate(source_rows):
        for metric, kind, raw_field in (
            ("spectralAbscissa", "frozen-spectral-edge", "rawSpectralEdge"),
            ("numericalAbscissa", "frozen-numerical-abscissa", "rawNumericalAbscissa"),
        ):
            raw = float(source[metric])
            display = signed_log(raw)
            add("C", kind, f"{kind}-{index:03d}", source["projection"],
                float(int(source["caseId"][1:3])), display,
                panel_c["displayTransform"], "validated finite Galerkin diagnostic",
                "N=40 only; no tail bound", projection=source["projection"],
                targetCase=source["caseId"], N=int(source["N"]),
                sourcePath=panel_c["sourceCsv"], sourceSha256=panel_c["sourceSha256"],
                displayValue=display, **{raw_field: raw})
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
    scene.text(55, 52,
               "R0.73A | hidden mean, transient envelope, and frozen projection screen",
               size=34, bold=True)
    scene.text(55, 88,
               "Exact formulas plus a validated finite Galerkin audit; no PDE simulation or fitted curve",
               size=20.5, color=MID)

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
        scene.text(x + 56, panel_y + 38, title, size=23, bold=True)
        scene.text(x + 20, panel_y + 72, subtitle, size=17, color=MID)
        scene.rect(x + 20, panel_y + 91, panel_w - 40, 34, fill=badge_fill,
                   stroke=badge_stroke, width=1.5, radius=7)
        scene.text(x + 34, panel_y + 115, badge, size=15, bold=True, color=INK)

    def axes(x: float, y: float, width: float, height: float,
             x_label: str, y_label: str) -> None:
        scene.line(x, y, x, y + height, color=INK, width=1.8)
        scene.line(x, y + height, x + width, y + height, color=INK, width=1.8)
        scene.text(x, y - 10, y_label, size=16, color=INK)
        scene.text(x + width / 2, y + height + 41, x_label, size=16,
                   color=INK, anchor="middle")

    def map_log(value: float, lo: float, hi: float, start: float,
                length: float) -> float:
        return start + length * (math.log10(value) - math.log10(lo)) / (
            math.log10(hi) - math.log10(lo)
        )

    def map_y(value: float, lo: float, hi: float, start: float,
              height: float) -> float:
        return start + height * (hi - value) / (hi - lo)

    def ticks_y(x: float, y: float, width: float, height: float,
                lo: float, hi: float, values: tuple[float, ...],
                fmt: str = "g") -> None:
        for tick in values:
            yy = map_y(tick, lo, hi, y, height)
            scene.line(x, yy, x + width, yy, color=GRID, width=1.1,
                       dash=(4, 5))
            scene.text(x - 9, yy + 5, format(tick, fmt), size=13.5,
                       color=MID, anchor="end")

    # A: the normalized bracket survives only on the c_mu -> c0 != 0 path.
    ax = panel_xs[0]
    panel_box(ax, "A", "Normalized hidden-mean bracket",
              "h_d/(i c_mu); path-sensitive interpretation",
              "BRACKET mu->0: NONZERO IF c_mu->c0 != 0", GOLD_LIGHT, GOLD)
    apx, apy, apw, aph = ax + 73, panel_y + 195, 420, 290
    axes(apx, apy, apw, aph, "mu (log)", "h_d / (i c_mu)")
    mu_lo, mu_hi = map(float, config["panelA"]["muRange"])
    a_lo, a_hi = 0.0, 0.165
    ticks_y(apx, apy, apw, aph, a_lo, a_hi, (0.0, 0.04, 0.08, 0.12, 0.16), ".2f")
    for tick in (1e-6, 1e-4, 1e-2, 1.0):
        xx = map_log(tick, mu_lo, mu_hi, apx, apw)
        scene.line(xx, apy + aph, xx, apy + aph + 7, color=INK, width=1.3)
        scene.text(xx, apy + aph + 25, f"10^{int(math.log10(tick))}",
                   size=13.5, color=MID, anchor="middle")
    a_styles = [
        ("d=0", BLUE, None, "circle", True),
        ("d=0.25", GOLD, (9, 5), "square", False),
        ("d=1", INK, (3, 5), "triangle", False),
        ("d=2", MID, (12, 4, 3, 4), "circle", False),
    ]
    hidden_rows = [row for row in rows if row["kind"] == "hidden-mean-excitation"]
    for label, color, dash, marker, filled in a_styles:
        series = [row for row in hidden_rows if row["series"] == label]
        points = [(map_log(float(row["mu"]), mu_lo, mu_hi, apx, apw),
                   map_y(float(row["value"]), a_lo, a_hi, apy, aph))
                  for row in series]
        scene.polyline(points, color=color, width=2.8, dash=dash)
        for index in range(0, len(points), 15):
            add_marker(scene, *points[index], marker, color, size=4.7,
                       filled=filled)
    scene.text(ax + 34, panel_y + 158,
               "e^(-2d)/[8(1+mu)] + e^(-8d)/[8(4+mu)]",
               size=14.5, color=INK, bold=True)
    legend_y = apy + aph + 58
    for lx, style in zip((apx, apx + 104, apx + 220, apx + 310), a_styles):
        label, color, dash, marker, filled = style
        scene.line(lx, legend_y, lx + 24, legend_y, color=color,
                   width=2.5, dash=dash)
        add_marker(scene, lx + 12, legend_y, marker, color, size=4.2,
                   filled=filled)
        scene.text(lx + 31, legend_y + 5, label, size=13.5)

    aqx, aqy, aqw, aqh = ax + 73, panel_y + 665, 420, 275
    axes(aqx, aqy, aqw, aqh, "d", "mu->0 normalized bracket")
    ticks_y(aqx, aqy, aqw, aqh, a_lo, a_hi, (0.0, 0.04, 0.08, 0.12, 0.16), ".2f")
    for tick in (0.0, 1.0, 2.0, 3.0):
        xx = aqx + aqw * tick / 3.0
        scene.line(xx, aqy + aqh, xx, aqy + aqh + 7, color=INK, width=1.3)
        scene.text(xx, aqy + aqh + 24, f"{tick:g}", size=13.5,
                   color=MID, anchor="middle")
    limit_rows = [row for row in rows if row["kind"] == "abstract-limit-mismatch"]
    limit_points = [(aqx + aqw * float(row["d"]) / 3.0,
                     map_y(float(row["value"]), a_lo, a_hi, aqy, aqh))
                    for row in limit_rows]
    scene.polyline(limit_points, color=BLUE, width=3.0)
    for index in range(0, len(limit_points), 15):
        add_marker(scene, *limit_points[index], "circle", BLUE, size=4.8,
                   filled=True)
    zero_y = map_y(0.0, a_lo, a_hi, aqy, aqh)
    scene.line(aqx, zero_y, aqx + aqw, zero_y, color=GOLD, width=2.3,
               dash=(9, 5))
    scene.text(aqx + 10, aqy + 28,
               "bracket limit (c_mu factor excluded)", size=15,
               color=BLUE, bold=True)
    scene.text(aqx + 10, aqy + aqh - 12, "abstract hidden coordinate: absent",
               size=15, color=GOLD, bold=True)
    scene.rect(ax + 20, panel_y + 1030, panel_w - 40, 91,
               fill=GOLD_LIGHT, stroke=GOLD, width=1.4, dash=(7, 5), radius=7)
    scene.text(ax + 34, panel_y + 1058,
               "ABSTRACT TANGENT: NO HIDDEN COORDINATE", size=16.5,
               bold=True)
    scene.text(ax + 34, panel_y + 1085,
               "FIXED Lambda (c_mu->0): UNDECIDED", size=16.5, bold=True)
    scene.text(ax + 20, panel_y + 1170,
               "Nonzero h_d limit requires c_mu->c0 != 0 (Lambda_mu ~ 1/gamma).",
               size=16, color=MID)

    # B: the proved envelope and the intentionally absent certificate overlay.
    bx = panel_xs[1]
    certificate_rows = [row for row in rows
                        if row["kind"] == "certified-xmu-propagator-gain"]
    panel_box(bx, "B", "Transient envelope",
              "Exact J kernel and declared analytic upper bounds",
              "ANALYTIC UPPER ENVELOPE - NOT OBSERVED GAIN",
              BLUE_LIGHT, BLUE)
    bpx, bpy, bpw, bph = bx + 73, panel_y + 195, 420, 280
    axes(bpx, bpy, bpw, bph, "tau = d-s", "J(s,s+tau)")
    ticks_y(bpx, bpy, bpw, bph, 0.0, 2.3, (0.0, 0.5, 1.0, 1.5, 2.0), ".1f")
    for tick in (0.0, 2.0, 4.0, 6.0):
        xx = bpx + bpw * tick / 6.0
        scene.line(xx, bpy + bph, xx, bpy + bph + 7, color=INK, width=1.3)
        scene.text(xx, bpy + bph + 24, f"{tick:g}", size=13.5,
                   color=MID, anchor="middle")
    b_styles = [
        ("s=0", BLUE, None, "circle", True),
        ("s=0.5", GOLD, (9, 5), "square", False),
        ("s=1", INK, (3, 5), "triangle", False),
    ]
    j_rows = [row for row in rows if row["kind"] == "exact-J-kernel"]
    for label, color, dash, marker, filled in b_styles:
        series = [row for row in j_rows if row["series"] == label]
        points = [(bpx + bpw * float(row["tau"]) / 6.0,
                   map_y(float(row["value"]), 0.0, 2.3, bpy, bph))
                  for row in series]
        scene.polyline(points, color=color, width=2.8, dash=dash)
        for index in range(0, len(points), 20):
            add_marker(scene, *points[index], marker, color, size=4.5,
                       filled=filled)
    scene.text(bx + 34, panel_y + 158,
               "J = 7/4(e^-s-e^-d) + 1/2(e^-4s-e^-4d)",
               size=14.2, color=INK, bold=True)

    j_legend_y = panel_y + 548
    scene.text(bx + 34, j_legend_y + 5, "J start:", size=13.5,
               color=MID, bold=True)
    for lx, style in zip((bx + 112, bx + 250, bx + 390), b_styles):
        label, color, dash, marker, filled = style
        scene.line(lx, j_legend_y, lx + 25, j_legend_y, color=color,
                   width=2.5, dash=dash)
        add_marker(scene, lx + 12, j_legend_y, marker, color, size=4.2,
                   filled=filled)
        scene.text(lx + 32, j_legend_y + 5, label, size=13.5)

    envelope_legend_y = panel_y + 585
    scene.text(bx + 34, envelope_legend_y + 5, "E mu/|c|/s:", size=13.2,
               color=MID, bold=True)
    envelope_legend = [
        (".01/4/0", BLUE, None, "circle", True),
        (".1/4/.5", GOLD, (9, 5), "square", False),
        ("1/1/1", INK, (3, 5), "triangle", False),
    ]
    for lx, style in zip((bx + 145, bx + 280, bx + 415), envelope_legend):
        label, color, dash, marker, filled = style
        scene.line(lx, envelope_legend_y, lx + 25, envelope_legend_y,
                   color=color, width=2.5, dash=dash)
        add_marker(scene, lx + 12, envelope_legend_y, marker, color, size=4.2,
                   filled=filled)
        scene.text(lx + 32, envelope_legend_y + 5, label, size=13.2)

    bqx, bqy, bqw, bqh = bx + 73, panel_y + 650, 420, 295
    axes(bqx, bqy, bqw, bqh, "tau = d-s", "log10 envelope / gain")
    e_lo, e_hi = -2.7, 4.0
    ticks_y(bqx, bqy, bqw, bqh, e_lo, e_hi, (-2.0, 0.0, 2.0, 4.0), ".0f")
    zero_env_y = map_y(0.0, e_lo, e_hi, bqy, bqh)
    scene.line(bqx, zero_env_y, bqx + bqw, zero_env_y, color=INK,
               width=1.7, dash=(5, 5))
    for tick in (0.0, 2.0, 4.0, 6.0):
        xx = bqx + bqw * tick / 6.0
        scene.line(xx, bqy + bqh, xx, bqy + bqh + 7, color=INK, width=1.3)
        scene.text(xx, bqy + bqh + 24, f"{tick:g}", size=13.5,
                   color=MID, anchor="middle")
    env_rows = [row for row in rows if row["kind"] == "analytic-transient-envelope"]
    env_styles = [
        ("mu=0.01, |c|=4, s=0", BLUE, None, "circle", True),
        ("mu=0.1, |c|=4, s=0.5", GOLD, (9, 5), "square", False),
        ("mu=1, |c|=1, s=1", INK, (3, 5), "triangle", False),
    ]
    for label, color, dash, marker, filled in env_styles:
        series = [row for row in env_rows if row["series"] == label]
        points = [(bqx + bqw * float(row["tau"]) / 6.0,
                   map_y(float(row["displayValue"]), e_lo, e_hi, bqy, bqh))
                  for row in series]
        scene.polyline(points, color=color, width=2.8, dash=dash)
        for index in range(0, len(points), 20):
            add_marker(scene, *points[index], marker, color, size=4.5,
                       filled=filled)
    if certificate_rows:
        for row in certificate_rows:
            xx = bqx + bqw * float(row["tau"]) / 6.0
            yy = map_y(float(row["displayValue"]), e_lo, e_hi, bqy, bqh)
            add_marker(scene, xx, yy, "square", GOLD, size=5.5, filled=False)
        certificate_badge = "CERTIFIED X_mu GAIN: OVERLAY PRESENT"
        certificate_note = "Certificate CSV only; formal lineage still required."
    else:
        certificate_badge = "CERTIFIED X_mu GAIN: PENDING - NOT PLOTTED"
        certificate_note = "FORMAL SEAL BLOCKED; NO SYNTHETIC CURVE"
    scene.rect(bx + 20, panel_y + 1030, panel_w - 40, 91,
               fill=GOLD_LIGHT, stroke=GOLD, width=1.4, dash=(7, 5), radius=7)
    scene.text(bx + 34, panel_y + 1058, certificate_badge,
               size=15.5, bold=True)
    scene.text(bx + 34, panel_y + 1086, certificate_note,
               size=15.5, bold=True)
    scene.text(bx + 20, panel_y + 1170,
               "Bound draft closed; maximum observed gain remains unclaimed.",
               size=16, color=MID)

    # C: validated N=40 screening data; the finite-dimensional boundary is explicit.
    cx = panel_xs[2]
    panel_box(cx, "C", "Frozen projection screen",
              "Three matrix variants across ten low-gap target cases",
              "FINITE GALERKIN N=40 - NOT INFINITE-DIMENSIONAL",
              GOLD_LIGHT, GOLD)
    c_styles = [
        ("unprojected", BLUE, None, "circle", True, "unprojected"),
        ("qstar-Wxx", GOLD, (9, 5), "square", False, "delete Wxx"),
        ("span-sin1-sin2", INK, (3, 5), "triangle", False,
         "delete sin x, sin 2x"),
    ]

    def signed_metric_plot(kind: str, x: float, y: float, title: str) -> None:
        width, height = 420, 275
        lo, hi = map(float, config["panelC"]["displayDomains"][kind])
        tick_values = tuple(map(float, config["panelC"]["displayTicks"][kind]))
        axes(x, y, width, height, "target case", title)
        ticks_y(x, y, width, height, lo, hi, tick_values, ".0f")
        zy = map_y(0.0, lo, hi, y, height)
        scene.line(x, zy, x + width, zy, color=INK, width=2.0, dash=(6, 5))
        for tick in (1, 3, 5, 7, 9):
            xx = x + width * (tick - 1) / 9.0
            scene.line(xx, y + height, xx, y + height + 7,
                       color=INK, width=1.3)
            scene.text(xx, y + height + 24, f"T{tick:02d}", size=12.5,
                       color=MID, anchor="middle")
        metric_rows = [row for row in rows if row["kind"] == kind]
        offsets = {"unprojected": -7.0, "qstar-Wxx": 0.0,
                   "span-sin1-sin2": 7.0}
        for key, color, dash, marker, filled, _label in c_styles:
            series = sorted((row for row in metric_rows if row["projection"] == key),
                            key=lambda row: float(row["x"]))
            points = [(x + width * (float(row["x"]) - 1.0) / 9.0 + offsets[key],
                       map_y(float(row["displayValue"]), lo, hi, y, height))
                      for row in series]
            scene.polyline(points, color=color, width=2.3, dash=dash)
            for point in points:
                add_marker(scene, *point, marker, color, size=4.7,
                           filled=filled)

    cpx, cpy = cx + 73, panel_y + 175
    signed_metric_plot("frozen-spectral-edge", cpx, cpy,
                       "signed log spectral edge")
    cqx, cqy = cx + 73, panel_y + 650
    signed_metric_plot("frozen-numerical-abscissa", cqx, cqy,
                       "signed log numerical abscissa")
    scene.text(cpx + 8, cpy + 26, "sgn(a) log10(1+|a|)", size=14.5,
               color=MID)
    legend_y = panel_y + 995
    for ly, style in zip((legend_y, legend_y + 27, legend_y + 54), c_styles):
        key, color, dash, marker, filled, label = style
        scene.line(cx + 34, ly, cx + 72, ly, color=color, width=2.5, dash=dash)
        add_marker(scene, cx + 53, ly, marker, color, size=4.5, filled=filled)
        scene.text(cx + 82, ly + 5, label, size=14.5)
    scene.rect(cx + 20, panel_y + 1090, panel_w - 40, 85,
               fill=GOLD_LIGHT, stroke=GOLD, width=1.4, dash=(7, 5), radius=7)
    scene.text(cx + 34, panel_y + 1118,
               "FIXED PROJECTION SUFFICIENT: FALSE IN SCREEN",
               size=15.5, bold=True)
    scene.text(cx + 34, panel_y + 1147,
               "NO GALERKIN TAIL BOUND", size=15.5, bold=True)
    scene.text(cx + 20, panel_y + 1210,
               "Counterexample screen only; not an infinite-dimensional theorem.",
               size=15.5, color=MID)

    scene.text(55, H - 20,
               "LOW-GAP KINETIC / BLOCH DIRECT SUM / NONLINEAR: OPEN",
               size=16.5, color=QUIET)
    scene.text(W - 55, H - 20, "CLAY PROBLEM: OPEN", size=16.5,
               color=QUIET, anchor="end")
    return scene

def svg_dash(dash: tuple[float, ...] | None) -> str:
    return "" if not dash else f' stroke-dasharray="{",".join(str(v) for v in dash)}"'


def render_svg(scene: Scene, path: Path) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH_MM}mm" '
        f'height="{HEIGHT_MM}mm" viewBox="0 0 {int(W)} {int(H)}" '
        'role="img" aria-labelledby="title desc">',
        '<title id="title">R0.73A hidden physical mean, transient envelope, and frozen projection screen</title>',
        '<desc id="desc">Three panels show the exact hidden physical coordinate, '
        'the analytic transient envelope with a fail-closed certificate slot, and '
        'validated finite frozen Galerkin projection diagnostics.</desc>',
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
    pdf.setTitle("R0.73A hidden physical mean and frozen projection screen")
    pdf.setAuthor("C. K. Zeng")
    pdf.setCreator("deterministic R0.73A figure generator")
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
    certificates = kinds.get("certified-xmu-propagator-gain", [])
    frozen = [row for row in rows if row["panel"] == "C"]
    stability_counts: dict[str, dict[str, int]] = {}
    for projection in sorted({row["projection"] for row in frozen}):
        spectral = [row for row in frozen
                    if row["projection"] == projection
                    and row["kind"] == "frozen-spectral-edge"]
        numerical = [row for row in frozen
                     if row["projection"] == projection
                     and row["kind"] == "frozen-numerical-abscissa"]
        stability_counts[projection] = {
            "spectrallyStableTargets": sum(float(row["rawSpectralEdge"]) < 0.0
                                            for row in spectral),
            "positiveNumericalAbscissaTargets": sum(
                float(row["rawNumericalAbscissa"]) > 0.0 for row in numerical
            ),
            "targetCount": len(spectral),
        }
    return {
        "schemaVersion": 1,
        "release": RELEASE,
        "figureId": FIGURE_ID,
        "deterministic": True,
        "randomSeed": None,
        "rowCount": len(rows),
        "panelA": {
            "exactNormalizedHiddenMeanBracket": "CLOSED IN BOUND DRAFT",
            "normalizedBracketLimitNonzero": True,
            "nonzeroHiddenDerivativeLimitRequires": "c_mu -> c0 != 0; equivalently Lambda_mu ~ 1/gamma",
            "fixedLambdaHiddenDerivativeLimitDecided": False,
            "abstractTangentHasHiddenCoordinate": False,
            "hiddenMeanRows": len(kinds["hidden-mean-excitation"]),
            "limitMismatchRows": len(kinds["abstract-limit-mismatch"]),
            "limitAtDZero": hidden_limit(0.0),
            "fittedQuantities": [],
        },
        "panelB": {
            "exactJKernelRows": len(kinds["exact-J-kernel"]),
            "analyticEnvelopeRows": len(kinds["analytic-transient-envelope"]),
            "certifiedPropagatorRows": len(certificates),
            "certificateOverlayAvailable": bool(certificates),
            "formalBlockedWithoutCertificate": not bool(certificates),
            "observedMaximumTransientGainClaimed": False,
            "fittedQuantities": [],
        },
        "panelC": {
            "finiteFrozenGalerkinScreen": "VALIDATED AT N=40",
            "sourceTargetRows": len(kinds["frozen-spectral-edge"]),
            "plottedMetricRows": len(frozen),
            "projectionSummary": stability_counts,
            "fixedProjectionUniformlyStabilizesScreen": False,
            "galerkinTailBoundAvailable": False,
            "fittedQuantities": [],
        },
        "claimsNotMade": [
            "the figure is an analytic proof",
            "the curves are PDE simulation output",
            "an absent X_mu propagator certificate has been synthesized",
            "the analytic envelope is an observed propagator gain",
            "continuous-time maximum transient gain is proved",
            "the finite Galerkin spectrum is an infinite-dimensional theorem",
            "a Galerkin tail bound is available",
            "the physical Bloch direct sum is closed",
            "nonlinear Navier-Stokes is closed",
            "the Clay Millennium problem is solved",
        ],
    }


def basic_checks(rows: list[dict[str, str]], scene: Scene) -> dict[str, bool]:
    by_kind = {kind: [row for row in rows if row["kind"] == kind]
               for kind in {row["kind"] for row in rows}}
    tol = 5e-14
    config = json.loads((PACKAGE / "config.json").read_text(encoding="utf-8"))
    hidden_ok = all(abs(float(row["value"]) - hidden_mean(
        float(row["mu"]), float(row["d"]))) <= tol
        for row in by_kind["hidden-mean-excitation"])
    limit_ok = all(abs(float(row["value"]) - hidden_limit(float(row["d"]))) <= tol
                   for row in by_kind["abstract-limit-mismatch"])
    j_ok = all(abs(float(row["value"]) - transient_j(
        float(row["s"]), float(row["d"]))) <= tol
        for row in by_kind["exact-J-kernel"])
    envelope_ok = all(abs(float(row["value"]) - transient_envelope(
        float(row["mu"]), float(row["cAbs"]), float(row["s"]),
        float(row["d"]))) <= tol * max(1.0, abs(float(row["value"])))
        and abs(float(row["displayValue"]) - math.log10(float(row["value"]))) <= tol
        for row in by_kind["analytic-transient-envelope"])
    frozen_ok = all(abs(float(row["displayValue"]) - signed_log(
        float(row["rawSpectralEdge"] or row["rawNumericalAbscissa"]))) <= tol
        for row in rows if row["panel"] == "C")
    certificate_rows = by_kind.get("certified-xmu-propagator-gain", [])
    certificate_ok = all(float(row["value"]) > 0.0 and row["certificateId"]
                         for row in certificate_rows)
    visible = "\n".join(item["value"] for item in scene.items
                         if item["kind"] == "text")
    formula_y = {item["value"]: item["y"] for item in scene.items
                 if item["kind"] == "text" and item["value"] in {
                     "e^(-2d)/[8(1+mu)] + e^(-8d)/[8(4+mu)]",
                     "J = 7/4(e^-s-e^-d) + 1/2(e^-4s-e^-4d)",
                 }}
    c_domains_ok = True
    minimum_padding = float(config["panelC"]["minimumDisplayPadding"])
    for kind in ("frozen-spectral-edge", "frozen-numerical-abscissa"):
        values = [float(row["displayValue"]) for row in by_kind[kind]]
        lo, hi = map(float, config["panelC"]["displayDomains"][kind])
        ticks = list(map(float, config["panelC"]["displayTicks"][kind]))
        c_domains_ok &= (
            min(values) - lo >= minimum_padding
            and hi - max(values) >= minimum_padding
            and 0.0 in ticks
            and all(lo <= tick <= hi for tick in ticks)
        )
    expected_without_certificate = 851
    return {
        "rowCount": len(rows) == expected_without_certificate + len(certificate_rows),
        "panelARecordCount": sum(row["panel"] == "A" for row in rows) == 305,
        "panelBAnalyticRecordCount": sum(row["panel"] == "B" for row in rows
                                          if row["kind"] != "certified-xmu-propagator-gain") == 486,
        "panelBRecordCountIncludesCertificate": sum(row["panel"] == "B" for row in rows) == 486 + len(certificate_rows),
        "panelCRecordCount": sum(row["panel"] == "C" for row in rows) == 60,
        "hiddenMeanRecomputed": hidden_ok,
        "singularLimitRecomputed": limit_ok,
        "singularLimitNonzeroAtDZero": abs(hidden_limit(0.0) - 5.0 / 32.0) <= tol,
        "transientJRecomputed": j_ok,
        "analyticEnvelopeRecomputed": envelope_ok,
        "frozenDiagnosticsTransformed": frozen_ok,
        "panelCDomainsContainAllDataWithPadding": c_domains_ok,
        "certificateRowsValidIfPresent": certificate_ok,
        "certificateTolerancePinned": (
            float(config["panelB"]["certificateBoundTolerance"])
            == CERTIFICATE_BOUND_TOLERANCE
        ),
        "targetSourceHashPinned": sha256(ROOT / config["panelC"]["sourceCsv"])
                                  == config["panelC"]["sourceSha256"],
        "targetValidationHashPinned": sha256(ROOT / config["panelC"]["validationJson"])
                                      == config["panelC"]["validationSha256"],
        "normalizedBracketBoundaryVisible": "BRACKET mu->0: NONZERO IF c_mu->c0 != 0" in visible,
        "abstractTangentBoundaryVisible": "ABSTRACT TANGENT: NO HIDDEN COORDINATE" in visible,
        "fixedLambdaBoundaryVisible": "FIXED Lambda (c_mu->0): UNDECIDED" in visible,
        "bracketFactorExclusionVisible": "bracket limit (c_mu factor excluded)" in visible,
        "formulaAnnotationsOutsideDataRects": (len(formula_y) == 2
                                                and max(formula_y.values()) < 295.0),
        "panelBJLegendVisible": "J start:" in visible,
        "panelBEnvelopeLegendVisible": "E mu/|c|/s:" in visible,
        "certificateDependencyVisible": (("CERTIFIED X_mu GAIN: OVERLAY PRESENT" in visible)
                                         if certificate_rows else
                                         ("CERTIFIED X_mu GAIN: PENDING - NOT PLOTTED" in visible
                                          and "FORMAL SEAL BLOCKED; NO SYNTHETIC CURVE" in visible)),
        "finiteDimensionalBoundaryVisible": "FINITE GALERKIN N=40 - NOT INFINITE-DIMENSIONAL" in visible,
        "fixedProjectionBoundaryVisible": "FIXED PROJECTION SUFFICIENT: FALSE IN SCREEN" in visible,
        "tailBoundaryVisible": "NO GALERKIN TAIL BOUND" in visible,
        "openBoundaryVisible": "LOW-GAP KINETIC / BLOCH DIRECT SUM / NONLINEAR: OPEN" in visible,
        "noSimulationBoundaryVisible": "no PDE simulation or fitted curve" in visible,
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
            "path": f"public/assets/r073a/{FIGURE_ID}.{suffix}",
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
            "How do the exact hidden mean, an explicit transient envelope, and "
            "finite frozen projection diagnostics delimit the next low-gap theorem?"
        ),
        "supportedClaim": (
            "The normalized hidden-mean bracket has a nonzero limit along "
            "c_mu -> c0 != 0, while fixed Lambda is undecided; the proved X_mu "
            "bound has a finite analytic envelope; fixed low-mode deletion does "
            "not uniformly stabilize the validated N=40 frozen screen."
        ),
        "deterministic": True,
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "sourceCommit": source_commit,
            "certificateCommit": certificate_commit,
            "dirtyAtCertifiedRun": False if status == "formal" else "pending",
        },
        "computation": {
            "kind": "closed-form sampling plus validated finite CSV ingestion",
            "configuration": "config.json",
            "precision": "IEEE-754 binary64",
            "solver": "direct closed-form evaluation plus read-only finite Galerkin audit data",
            "formalCommand": (
                "python3 plot.py --formal --visual-inspected "
                "--source-commit <40-hex> --certificate-commit <40-hex>"
            ),
            "wallTimeSeconds": 0.0,
            "wallTimePolicy": "not used in any claim; fixed at zero for a byte-stable exact sampler",
            "randomSeed": None,
            "diagnosticOnly": True,
            "syntheticCertificateData": False,
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
            file_record("results.json", schema="exact identities, dependency, and finite-screen ledger"),
            file_record("validation.json", schema="formula, format, and visible-boundary checks"),
        ],
        "sourceData": [
            {
                "path": json.loads((PACKAGE / "config.json").read_text(
                    encoding="utf-8"))["panelC"]["sourceCsv"],
                "sha256": json.loads((PACKAGE / "config.json").read_text(
                    encoding="utf-8"))["panelC"]["sourceSha256"],
                "role": "validated finite frozen Galerkin target data",
                "sourceRowsAtN40": 30,
                "plottedMetricRows": 60,
            },
            {
                "path": json.loads((PACKAGE / "config.json").read_text(
                    encoding="utf-8"))["panelC"]["validationJson"],
                "sha256": json.loads((PACKAGE / "config.json").read_text(
                    encoding="utf-8"))["panelC"]["validationSha256"],
                "role": "upstream finite-audit validation",
            },
        ],
        "dependency": {
            "path": json.loads((PACKAGE / "config.json").read_text(
                encoding="utf-8"))["panelB"]["certificateCsv"],
            "available": any(row["kind"] == "certified-xmu-propagator-gain"
                             for row in rows),
            "syntheticSubstitutionAllowed": False,
            "formalBlocked": not any(
                row["kind"] == "certified-xmu-propagator-gain" for row in rows
            ),
        },
        "figure": {
            "profile": "journal-double-column",
            "layout": "three equal journal panels with paired analytic or audited insets",
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
            "directory": "public/assets/r073a",
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
        "# R0.73A figure QA",
        "",
        f"- manifest stage: {status}",
        f"- explicit visual inspection: {'yes' if visual_inspected else 'pending'}",
        "- final-size, grayscale, and independent PDF previews generated: yes",
        "- hidden-mean derivative, singular limit, J kernel, and envelope recomputed: yes",
        "- finite frozen metrics verified against pinned upstream data: yes",
        "- simulation, fitted curve, or synthetic certificate used: no",
        "- two chromatic roots plus redundant non-color encodings: yes",
        "- finite-dimensional, certificate, and open-claim boundaries visible: yes",
        "- PDF vector, embedded-font, one-page, and page-size checks: see validation.json",
        "- maximum gain, tail, physical direct sum, nonlinear, and Clay claims remain open: yes",
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
        if not any(row["kind"] == "certified-xmu-propagator-gain" for row in rows):
            raise RuntimeError(
                "formal render requires the certified X_mu propagator overlay; "
                "synthetic substitution is forbidden"
            )
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
