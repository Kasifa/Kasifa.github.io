#!/usr/bin/env python3
"""Render the formal R0.73J continuum-branch certificate figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, getcontext, localcontext
from fractions import Fraction
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import re
import resource
import socket
import subprocess
import sys
import time


def _bootstrap_dependencies() -> None:
    for index, argument in enumerate(sys.argv):
        if argument == "--deps" and index + 1 < len(sys.argv):
            sys.path.insert(0, str(Path(sys.argv[index + 1]).resolve()))
            return
        if argument.startswith("--deps="):
            sys.path.insert(0, str(Path(argument.split("=", 1)[1]).resolve()))
            return


_bootstrap_dependencies()

import matplotlib as mpl

mpl.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.lines import Line2D
from matplotlib.patches import Circle, Ellipse, Rectangle
import numpy as np


HERE = Path(__file__).resolve().parent
REPOSITORY = HERE.parents[2]
FIGURE_ID = "fig-r073j-continuum-branch-certificate"
CONTOUR_PATH = REPOSITORY / "experiments/r073j/contour_certificate.json"
OVERLAP_PATH = REPOSITORY / "experiments/r073j/overlap_certificate.json"
CONTOUR_CONFIG_PATH = REPOSITORY / "experiments/r073j/config.json"
OVERLAP_CONFIG_PATH = REPOSITORY / "experiments/r073j/overlap_config.json"
GENERATED = (
    "source-data.csv",
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "results.json",
    "environment.json",
    "progress.ndjson",
    "resource-log.ndjson",
    "qa-report.md",
)
BALL_RE = re.compile(
    r"^\[?\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
    r"(?:\s*\+/-\s*([+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?))?"
    r"\s*\]?$"
)


def canonical(value: object) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"JSON root must be an object: {path}")
    return value


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def ball_parts(text: str) -> tuple[Decimal, Decimal, Decimal]:
    match = BALL_RE.fullmatch(text.strip())
    if not match:
        raise RuntimeError(f"unsupported interval string: {text!r}")
    midpoint = Decimal(match.group(1))
    radius = Decimal(match.group(2) or "0")
    require(radius >= 0, f"negative interval radius: {text}")
    return midpoint, radius, midpoint - radius


def decimal_text(value: Decimal) -> str:
    return format(value, "f")


def fraction_decimal(value: Fraction, digits: int = 70) -> str:
    with localcontext() as context:
        context.prec = digits
        return decimal_text(Decimal(value.numerator) / Decimal(value.denominator))


def fraction_from_text(value: str) -> Fraction:
    return Fraction(value)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def process_rss_mib() -> float:
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        return float(rss) / (1024.0 * 1024.0)
    return float(rss) / 1024.0


class Monitor:
    def __init__(self) -> None:
        self.started = time.perf_counter()
        self.progress = HERE / "progress.ndjson"
        self.resources = HERE / "resource-log.ndjson"
        self.progress.write_text("", encoding="utf-8")
        self.resources.write_text("", encoding="utf-8")

    def event(self, stage: str, **fields: object) -> None:
        record = {
            "timestamp": utc_now(),
            "elapsedSeconds": round(time.perf_counter() - self.started, 6),
            "stage": stage,
            **fields,
        }
        with self.progress.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(record, sort_keys=True) + "\n")
        resource_record = {
            "timestamp": record["timestamp"],
            "elapsedSeconds": record["elapsedSeconds"],
            "stage": stage,
            "pid": os.getpid(),
            "processes": 1,
            "threadsPerProcess": 1,
            "maximumResidentSetMiB": round(process_rss_mib(), 3),
            "gpu": "not used",
        }
        with self.resources.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(resource_record, sort_keys=True) + "\n")


def validate_inputs(
    figure_config: dict,
    contract: dict,
    contour: dict,
    overlap: dict,
    contour_config: dict,
    overlap_config: dict,
) -> None:
    require(figure_config.get("figureId") == FIGURE_ID, "figure config identity drift")
    require(contract.get("figureId") == FIGURE_ID, "figure contract identity drift")
    require(contour.get("status") == "passed", "contour certificate is not passed")
    require(overlap.get("status") == "passed", "overlap certificate is not passed")
    require(len(contour.get("panels", [])) == 64, "expected 64 contour panels")
    require(len(overlap.get("cells", [])) == 128, "expected 128 overlap cells")
    families = [row.get("family") for row in contour["panels"]]
    require(families.count("global") == 56, "expected 56 global contour panels")
    require(families.count("local") == 8, "expected 8 local contour panels")
    require(len({row.get("id") for row in contour["panels"]}) == 64,
            "contour panel identifiers are not unique")
    require(
        contour["decisions"].get("globalBoundaryNonzeroForAllD") is True
        and contour["decisions"].get("localBoundaryNonzeroForAllD") is True,
        "contour nonzero decisions are not both true",
    )
    require(
        contour["decisions"].get("globalBasePositiveOrientationWinding") == 1
        and contour["decisions"].get("localBasePositiveOrientationWinding") == 1,
        "base winding decisions are not both one",
    )
    require(
        overlap["decisions"].get(
            "auxiliaryRectangleKineticQuotientAtLeastOneHalf"
        ) is True,
        "overlap threshold decision is not true",
    )
    require(
        overlap["decisions"].get("auxiliaryRectanglePhaseAnchorNonzero") is True,
        "overlap phase-anchor decision is not true",
    )
    grid = {(int(row["dIndex"]), int(row["lambdaIndex"])) for row in overlap["cells"]}
    require(grid == {(j, k) for j in range(8) for k in range(16)},
            "overlap grid is not the complete 8 by 16 dyadic grid")
    require(contour.get("configuration") == contour_config,
            "contour configuration does not match its certificate")
    require(overlap.get("configuration") == overlap_config,
            "overlap configuration does not match its certificate")

    geometry = figure_config["geometry"]
    require(Fraction(contour_config["global"]["boundary"]["left"]) == Fraction(11, 100),
            "global left boundary drift")
    require(Fraction(contour_config["global"]["boundary"]["outer"]) == Fraction(19, 50),
            "global outer boundary drift")
    require(Fraction(overlap_config["lambdaCenter"]) == Fraction(17, 100),
            "local center drift")
    require(Fraction(overlap_config["lambdaRadius"]) == Fraction(3, 1000),
            "local radius drift")
    require(math.isclose(float(geometry["dUpper"]), 1.0 / 450.0,
                         rel_tol=0.0, abs_tol=1e-18), "d upper endpoint drift")
    require(math.isclose(float(geometry["overlapThreshold"]), 0.5,
                         rel_tol=0.0, abs_tol=0.0), "overlap threshold drift")

    boundary = contract.get("claimBoundary", {})
    required_true = {
        "formalValidatedCertificateFigure",
        "continuumSpectralBranchCountCertified",
        "kineticOverlapThresholdCertified",
    }
    required_false = {
        "viscousBranchCertified",
        "adiabaticRemainderCertified",
        "transverseThreeDimensionalClosureCertified",
        "finiteTimeSingularityCertified",
        "clayProblemSolved",
    }
    require(all(boundary.get(key) is True for key in required_true),
            "required certified claim boundary is missing")
    require(all(boundary.get(key) is False for key in required_false),
            "an excluded claim escaped the figure contract")


def build_source_rows(contour: dict, overlap: dict) -> list[dict[str, str]]:
    contour_relative = str(CONTOUR_PATH.relative_to(REPOSITORY))
    overlap_relative = str(OVERLAP_PATH.relative_to(REPOSITORY))
    contour_hash = sha256(CONTOUR_PATH)
    overlap_hash = sha256(OVERLAP_PATH)
    rows: list[dict[str, str]] = []
    d_upper = Fraction(1, 450)

    for order, panel in enumerate(contour["panels"], start=1):
        definition = panel["definition"]
        midpoint, radius, lower = ball_parts(panel["minimumAbsoluteLower"])
        rows.append({
            "figure_panel": "B",
            "record_type": "contour_panel",
            "record_id": str(panel["id"]),
            "order_index": str(order),
            "family": str(panel["family"]),
            "edge": str(definition.get("edge", "circle")),
            "contour_kind": str(definition["kind"]),
            "center_real": str(definition.get("centerReal", "")),
            "center_imag": str(definition.get("centerImag", "")),
            "half_real": str(definition.get("halfReal", "")),
            "half_imag": str(definition.get("halfImag", "")),
            "theta_center_pi": str(definition.get("thetaCenterPi", "")),
            "theta_half_pi": str(definition.get("thetaHalfPi", "")),
            "d_depth": "",
            "d_index": "",
            "d_lower": "0",
            "d_upper": fraction_decimal(d_upper),
            "lambda_depth": "",
            "lambda_index": "",
            "lambda_lower": "",
            "lambda_upper": "",
            "certified_bound_name": "minimumAbsoluteLower",
            "bound_raw": panel["minimumAbsoluteLower"],
            "bound_midpoint": decimal_text(midpoint),
            "bound_radius": decimal_text(radius),
            "bound_lower_endpoint": decimal_text(lower),
            "threshold": "0",
            "strict_margin": decimal_text(lower),
            "upstream_path": contour_relative,
            "upstream_sha256": contour_hash,
        })

    center = Fraction(overlap["configuration"]["lambdaCenter"])
    radius = Fraction(overlap["configuration"]["lambdaRadius"])
    d_depth = int(overlap["configuration"]["subdivision"]["dDepth"])
    lambda_depth = int(overlap["configuration"]["subdivision"]["lambdaDepth"])
    threshold = Decimal("0.5")
    for cell in sorted(overlap["cells"], key=lambda row: (row["dIndex"], row["lambdaIndex"])):
        d_index = int(cell["dIndex"])
        lambda_index = int(cell["lambdaIndex"])
        d_lo = d_upper * d_index / (2 ** d_depth)
        d_hi = d_upper * (d_index + 1) / (2 ** d_depth)
        lam_left = center - radius
        lam_width = 2 * radius / (2 ** lambda_depth)
        lam_lo = lam_left + lambda_index * lam_width
        lam_hi = lam_left + (lambda_index + 1) * lam_width
        midpoint, value_radius, lower = ball_parts(cell["overlapLower"])
        rows.append({
            "figure_panel": "C",
            "record_type": "overlap_cell",
            "record_id": f"O-d{d_index:02d}-lambda{lambda_index:02d}",
            "order_index": str(len(rows) + 1),
            "family": "overlap",
            "edge": "",
            "contour_kind": "dyadic_rectangle",
            "center_real": "",
            "center_imag": "",
            "half_real": "",
            "half_imag": "",
            "theta_center_pi": "",
            "theta_half_pi": "",
            "d_depth": str(d_depth),
            "d_index": str(d_index),
            "d_lower": fraction_decimal(d_lo),
            "d_upper": fraction_decimal(d_hi),
            "lambda_depth": str(lambda_depth),
            "lambda_index": str(lambda_index),
            "lambda_lower": fraction_decimal(lam_lo),
            "lambda_upper": fraction_decimal(lam_hi),
            "certified_bound_name": "overlapLower",
            "bound_raw": cell["overlapLower"],
            "bound_midpoint": decimal_text(midpoint),
            "bound_radius": decimal_text(value_radius),
            "bound_lower_endpoint": decimal_text(lower),
            "threshold": decimal_text(threshold),
            "strict_margin": decimal_text(lower - threshold),
            "upstream_path": overlap_relative,
            "upstream_sha256": overlap_hash,
        })
    require(len(rows) == 192, "source row count drift")
    return rows


def write_source_data(rows: list[dict[str, str]]) -> None:
    path = HERE / "source-data.csv"
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def add_research_blossom(fig: mpl.figure.Figure, blue: str, orange: str) -> None:
    center_x, center_y = 0.966, 0.957
    for index in range(5):
        angle = 90.0 + 72.0 * index
        radians = math.radians(angle)
        petal = Ellipse(
            (center_x + 0.0095 * math.cos(radians),
             center_y + 0.016 * math.sin(radians)),
            width=0.014,
            height=0.028,
            angle=angle - 90.0,
            transform=fig.transFigure,
            facecolor=mpl.colors.to_rgba(blue, 0.18),
            edgecolor=blue,
            linewidth=0.55,
            zorder=20,
        )
        petal.set_gid(f"research-blossom-petal-{index + 1}")
        fig.add_artist(petal)
    center = Circle(
        (center_x, center_y), 0.0039, transform=fig.transFigure,
        facecolor=orange, edgecolor="white", linewidth=0.4, zorder=21,
    )
    center.set_gid("research-blossom-center")
    fig.add_artist(center)


def render_figure(config: dict, rows: list[dict[str, str]]) -> dict[str, object]:
    palette = config["palette"]
    blue = palette["blue"]
    blue_light = palette["blueLight"]
    orange = palette["orange"]
    orange_light = palette["orangeLight"]
    ink = palette["ink"]
    muted = palette["muted"]
    grid = palette["grid"]
    paper = palette["paper"]

    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["DejaVu Sans", "Arial", "Liberation Sans"],
        "mathtext.fontset": "stixsans",
        "font.size": 6.6,
        "axes.titlesize": 7.7,
        "axes.labelsize": 6.8,
        "xtick.labelsize": 5.9,
        "ytick.labelsize": 5.9,
        "legend.fontsize": 5.6,
        "axes.linewidth": 0.6,
        "axes.edgecolor": ink,
        "text.color": ink,
        "axes.labelcolor": ink,
        "xtick.color": ink,
        "ytick.color": ink,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
        "savefig.facecolor": paper,
    })

    width_mm = float(config["widthMillimetres"])
    height_mm = float(config["heightMillimetres"])
    figure = plt.figure(
        figsize=(width_mm / 25.4, height_mm / 25.4),
        facecolor=paper,
        constrained_layout=False,
    )
    gridspec = figure.add_gridspec(
        2, 2,
        left=0.075, right=0.915, bottom=0.145, top=0.875,
        width_ratios=(0.88, 1.12), height_ratios=(1.04, 0.96),
        wspace=0.30, hspace=0.58,
    )
    ax_a = figure.add_subplot(gridspec[0, 0])
    ax_b = figure.add_subplot(gridspec[0, 1])
    ax_c = figure.add_subplot(gridspec[1, :])

    figure.suptitle(
        "Validated periodic Rayleigh–Evans branch certificate",
        x=0.50, y=0.972, fontsize=9.0, fontweight="semibold", color=ink,
    )
    figure.text(
        0.50, 0.935,
        r"$0\leq d\leq 1/450$; interval lower bounds and exact base windings",
        ha="center", va="center", fontsize=6.2, color=muted,
    )
    add_research_blossom(figure, blue, orange)

    geometry = config["geometry"]
    global_left = float(geometry["globalLeft"])
    global_outer = float(geometry["globalOuter"])
    local_center = float(geometry["localCenter"])
    local_radius = float(geometry["localRadius"])
    howard_radius = 3.0 * math.sqrt(3.0) / 16.0
    root_lower = float(geometry["rootLower"])
    root_upper = float(geometry["rootUpper"])

    ax_a.axvline(0.0, color=muted, lw=0.8, ls=(0, (1.5, 2.0)), zorder=1)
    howard = Circle(
        (0.0, 0.0), howard_radius, fill=False, edgecolor=muted,
        linewidth=0.85, linestyle=(0, (4.0, 2.2)), zorder=2,
    )
    ax_a.add_patch(howard)
    global_rectangle = Rectangle(
        (global_left, -global_outer), global_outer - global_left, 2 * global_outer,
        fill=False, edgecolor=blue, linewidth=1.15, linestyle="solid", zorder=3,
    )
    ax_a.add_patch(global_rectangle)
    local_circle = Circle(
        (local_center, 0.0), local_radius, fill=False, edgecolor=orange,
        linewidth=1.0, linestyle=(0, (3.0, 2.0)), zorder=5,
    )
    ax_a.add_patch(local_circle)
    ax_a.plot([root_lower, root_upper], [0.0, 0.0], color=ink, lw=2.0,
              solid_capstyle="butt", zorder=6)
    ax_a.set_xlim(-0.37, 0.42)
    ax_a.set_ylim(-0.42, 0.42)
    ax_a.set_aspect("equal", adjustable="box")
    ax_a.set_xlabel(r"$\operatorname{Re}\lambda$")
    ax_a.set_ylabel(r"$\operatorname{Im}\lambda$")
    ax_a.set_xticks([-0.3, 0.0, 0.11, 0.38])
    ax_a.set_xticklabels([r"$-0.3$", r"$0$", r"$0.11$", r"$0.38$"])
    ax_a.set_yticks([-0.38, 0.0, 0.38])
    ax_a.set_title("A   Spectral-domain geometry", loc="left", pad=4,
                   fontweight="semibold")
    ax_a.grid(False)
    ax_a.spines[["top", "right"]].set_visible(False)
    legend_handles = [
        Line2D([0], [0], color=blue, lw=1.15, label="global contour"),
        Line2D([0], [0], color=orange, lw=1.0, ls=(0, (3.0, 2.0)),
               marker="s", markerfacecolor="none", markersize=3.1,
               label="local contour"),
        Line2D([0], [0], color=muted, lw=0.85, ls=(0, (4.0, 2.2)),
               label="Howard disk"),
    ]
    ax_a.legend(handles=legend_handles, loc="upper left", frameon=False,
                borderaxespad=0.1, handlelength=2.1, labelspacing=0.25)
    ax_a.text(
        0.011, 0.50, "essential-spectrum axis", color=muted, rotation=90,
        ha="left", va="center", transform=ax_a.transAxes, fontsize=5.1,
    )

    inset = ax_a.inset_axes([0.54, 0.06, 0.43, 0.34])
    inset.add_patch(Circle(
        (local_center, 0.0), local_radius, fill=False, edgecolor=orange,
        linewidth=0.9, linestyle=(0, (3.0, 2.0)),
    ))
    inset.plot([root_lower, root_upper], [0.0, 0.0], color=ink, lw=1.5,
               solid_capstyle="butt")
    inset.plot([root_lower, root_upper], [0.0, 0.0], linestyle="none",
               marker="|", markersize=5.5, markeredgewidth=0.8, color=ink)
    inset.set_xlim(local_center - 1.48 * local_radius,
                   local_center + 1.48 * local_radius)
    inset.set_ylim(-1.35 * local_radius, 1.35 * local_radius)
    inset.set_xticks([root_lower, root_upper])
    inset.set_yticks([0.0])
    inset.tick_params(labelsize=4.5, length=1.7, pad=1.0)
    inset.set_title("root interval, not point", fontsize=4.8, pad=2)
    for spine in inset.spines.values():
        spine.set_linewidth(0.45)

    contour_rows = [row for row in rows if row["record_type"] == "contour_panel"]
    global_rows = [row for row in contour_rows if row["family"] == "global"]
    local_rows = [row for row in contour_rows if row["family"] == "local"]
    x_global = np.array([int(row["order_index"]) for row in global_rows])
    y_global = np.array([float(row["bound_lower_endpoint"]) for row in global_rows])
    x_local = np.array([int(row["order_index"]) for row in local_rows])
    y_local = np.array([float(row["bound_lower_endpoint"]) for row in local_rows])
    ax_b.semilogy(
        x_global, y_global, color=blue, marker="o", markersize=2.5,
        markerfacecolor=blue, markeredgecolor=paper, markeredgewidth=0.35,
        linewidth=0.9, linestyle="solid", label="global: 56 panels",
    )
    ax_b.semilogy(
        x_local, y_local, color=orange, marker="s", markersize=3.0,
        markerfacecolor=paper, markeredgecolor=orange, markeredgewidth=0.75,
        linewidth=0.9, linestyle=(0, (3.0, 2.0)), label="local: 8 panels",
    )
    ax_b.axvline(56.5, color=muted, lw=0.55, ls=(0, (1.5, 2.0)))
    global_min_index = int(np.argmin(y_global))
    local_min_index = int(np.argmin(y_local))
    ax_b.annotate(
        f"global min {y_global[global_min_index]:.6f}",
        xy=(x_global[global_min_index], y_global[global_min_index]),
        xytext=(31, 2.7), textcoords="data", fontsize=5.25, color=blue,
        arrowprops={"arrowstyle": "-", "color": blue, "lw": 0.55},
    )
    ax_b.annotate(
        f"local min {y_local[local_min_index]:.6f}",
        xy=(x_local[local_min_index], y_local[local_min_index]),
        xytext=(45, 0.28), textcoords="data", fontsize=5.25, color=orange,
        arrowprops={"arrowstyle": "-", "color": orange, "lw": 0.55},
    )
    ax_b.set_xlim(0.0, 65.0)
    ax_b.set_ylim(0.12, 60.0)
    ax_b.set_xticks([1, 9, 28, 37, 56, 64])
    ax_b.set_xlabel("ordered contour panel")
    ax_b.set_ylabel(r"certified lower bound on $|E|$")
    ax_b.set_title("B   Uniform contour-panel bounds", loc="left", pad=4,
                   fontweight="semibold")
    ax_b.legend(loc="upper right", frameon=False, handlelength=2.4,
                borderaxespad=0.2, labelspacing=0.25)
    ax_b.grid(True, which="major", axis="y", color=grid, linewidth=0.45)
    ax_b.grid(True, which="minor", axis="y", color=grid, linewidth=0.25,
              alpha=0.45)
    ax_b.spines[["top", "right"]].set_visible(False)

    overlap_rows = [row for row in rows if row["record_type"] == "overlap_cell"]
    values = np.empty((8, 16), dtype=float)
    for row in overlap_rows:
        values[int(row["d_index"]), int(row["lambda_index"])] = float(
            row["bound_lower_endpoint"]
        )
    value_min = float(values.min())
    value_max = float(values.max())
    color_map = LinearSegmentedColormap.from_list(
        "r073j-blue", [paper, blue_light, blue], N=256,
    )
    normalization = Normalize(vmin=value_min, vmax=value_max)
    d_upper_float = float(Fraction(1, 450)) * 1000.0
    lambda_left = local_center - local_radius
    lambda_width = 2.0 * local_radius / 16.0
    d_height = d_upper_float / 8.0
    for d_index in range(8):
        for lambda_index in range(16):
            patch = Rectangle(
                (lambda_left + lambda_index * lambda_width, d_index * d_height),
                lambda_width, d_height,
                facecolor=color_map(normalization(values[d_index, lambda_index])),
                edgecolor=paper, linewidth=0.28,
            )
            ax_c.add_patch(patch)
    minimum_location = np.unravel_index(int(np.argmin(values)), values.shape)
    d_min, lambda_min = int(minimum_location[0]), int(minimum_location[1])
    minimum_outline = Rectangle(
        (lambda_left + lambda_min * lambda_width, d_min * d_height),
        lambda_width, d_height, facecolor="none", edgecolor=orange,
        linewidth=1.05, zorder=5,
    )
    ax_c.add_patch(minimum_outline)
    ax_c.plot(
        lambda_left + (lambda_min + 0.5) * lambda_width,
        (d_min + 0.5) * d_height,
        marker="x", color=orange, markersize=4.0, markeredgewidth=0.9,
        linestyle="none", zorder=6,
    )
    ax_c.annotate(
        f"minimum {value_min:.6f}",
        xy=(lambda_left + (lambda_min + 0.5) * lambda_width,
            (d_min + 0.5) * d_height),
        xytext=(0.17155, 1.45), textcoords="data", fontsize=5.6,
        color=orange, ha="left",
        bbox={"boxstyle": "square,pad=0.16", "facecolor": paper,
              "edgecolor": "none", "alpha": 0.88},
        arrowprops={"arrowstyle": "-", "color": orange, "lw": 0.65},
        zorder=7,
    )
    ax_c.set_xlim(lambda_left, local_center + local_radius)
    ax_c.set_ylim(0.0, d_upper_float)
    ax_c.set_xlabel(r"real $\lambda$")
    ax_c.set_ylabel(r"$d\;(\times 10^{-3})$")
    ax_c.set_xticks([0.167, 0.169, 0.171, 0.173])
    ax_c.set_yticks([0.0, 0.556, 1.111, 1.667, 2.222])
    ax_c.set_title("C   Kinetic left–right overlap lower bounds", loc="left",
                   pad=14, fontweight="semibold")
    ax_c.text(
        0.0, 1.025,
        r"128 dyadic cells; focused color scale; declared threshold $1/2$",
        transform=ax_c.transAxes, ha="left", va="bottom", color=muted,
        fontsize=5.6,
    )
    # A finite stack of rectangles keeps both archival vector formats free of
    # embedded raster images (Matplotlib's standard colorbar may rasterize its
    # gradient even when every data cell is a vector patch).
    colorbar_axis = ax_c.inset_axes([1.018, 0.0, 0.020, 1.0])
    strip_count = 48
    strip_height = (value_max - value_min) / strip_count
    for strip in range(strip_count):
        lower = value_min + strip * strip_height
        middle = lower + 0.5 * strip_height
        colorbar_axis.add_patch(Rectangle(
            (0.0, lower), 1.0, strip_height * 1.002,
            facecolor=color_map(normalization(middle)), edgecolor="none",
        ))
    colorbar_axis.set_xlim(0.0, 1.0)
    colorbar_axis.set_ylim(value_min, value_max)
    colorbar_axis.set_xticks([])
    colorbar_axis.set_yticks([
        value_min, 0.5 * (value_min + value_max), value_max
    ])
    colorbar_axis.yaxis.tick_right()
    colorbar_axis.yaxis.set_label_position("right")
    colorbar_axis.set_ylabel("certified lower bound (focused)", fontsize=5.7)
    colorbar_axis.tick_params(axis="y", labelsize=5.2, length=2.0, pad=1.2)
    for spine in colorbar_axis.spines.values():
        spine.set_linewidth(0.45)
    for spine in ax_c.spines.values():
        spine.set_linewidth(0.55)

    figure.text(
        0.50, 0.040,
        "Scope: one planar periodic linearized certificate; no viscous, 3D, "
        "finite-time-singularity, or Clay conclusion.",
        ha="center", va="center", fontsize=5.5, color=muted,
    )

    outputs = {
        "pdf": HERE / "figure.pdf",
        "svg": HERE / "figure.svg",
        "png": HERE / "figure.png",
    }
    figure.savefig(outputs["pdf"], metadata={
        "Title": "R0.73J continuum spectral-branch certificate",
        "Author": "ChuiKuan Zeng",
        "Subject": "Validated periodic Rayleigh-Evans contour and overlap margins",
        "Keywords": "Rayleigh Evans interval certificate kinetic overlap",
    })
    figure.savefig(outputs["svg"])
    figure.savefig(outputs["png"], dpi=int(config["pngDpi"]))
    plt.close(figure)
    return {
        "globalMinimum": float(y_global.min()),
        "globalMinimumId": global_rows[global_min_index]["record_id"],
        "localMinimum": float(y_local.min()),
        "localMinimumId": local_rows[local_min_index]["record_id"],
        "overlapMinimum": value_min,
        "overlapMinimumCell": {"dIndex": d_min, "lambdaIndex": lambda_min},
        "overlapMaximum": value_max,
    }


def command_version(command: list[str]) -> str:
    try:
        result = subprocess.run(command, text=True, capture_output=True, check=False)
    except OSError:
        return "unavailable"
    line = (result.stdout or result.stderr).splitlines()
    return line[0].strip() if line else "unavailable"


def write_environment(deps: Path | None) -> None:
    memory_bytes = None
    try:
        memory_bytes = int(subprocess.check_output(
            ["sysctl", "-n", "hw.memsize"], text=True
        ).strip())
    except (OSError, ValueError, subprocess.CalledProcessError):
        pass
    environment = {
        "schemaVersion": "r073j-figure-environment-v1",
        "python": platform.python_version(),
        "pythonExecutable": sys.executable,
        "platform": platform.platform(),
        "operatingSystem": command_version(["sw_vers", "-productVersion"]),
        "host": socket.gethostname(),
        "architecture": platform.machine(),
        "processor": platform.processor() or command_version(
            ["sysctl", "-n", "machdep.cpu.brand_string"]
        ),
        "memoryGiB": None if memory_bytes is None else round(memory_bytes / 2**30, 3),
        "processes": 1,
        "threadsPerProcess": 1,
        "gpu": "not used",
        "dependencyDirectory": None if deps is None else str(deps),
        "packages": {
            "matplotlib": mpl.__version__,
            "numpy": np.__version__,
        },
        "threadLimits": {
            "OPENBLAS_NUM_THREADS": os.environ.get("OPENBLAS_NUM_THREADS"),
            "OMP_NUM_THREADS": os.environ.get("OMP_NUM_THREADS"),
            "VECLIB_MAXIMUM_THREADS": os.environ.get("VECLIB_MAXIMUM_THREADS"),
        },
    }
    (HERE / "environment.json").write_text(canonical(environment), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", type=Path)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()
    if not args.overwrite:
        present = [name for name in GENERATED if (HERE / name).exists()]
        if present:
            parser.error("generated outputs already exist; use --overwrite")

    getcontext().prec = 120
    monitor = Monitor()
    monitor.event("started", figureId=FIGURE_ID)
    started = time.perf_counter()

    figure_config = load_json(HERE / "config.json")
    contract = load_json(HERE / "contract.json")
    contour = load_json(CONTOUR_PATH)
    overlap = load_json(OVERLAP_PATH)
    contour_config = load_json(CONTOUR_CONFIG_PATH)
    overlap_config = load_json(OVERLAP_CONFIG_PATH)
    validate_inputs(
        figure_config, contract, contour, overlap, contour_config, overlap_config
    )
    monitor.event("inputs-validated", contourPanels=64, overlapCells=128)

    rows = build_source_rows(contour, overlap)
    write_source_data(rows)
    monitor.event("source-data-written", rows=len(rows))

    plotted = render_figure(figure_config, rows)
    monitor.event("masters-rendered", formats=["pdf", "svg", "png"])
    wall_time = time.perf_counter() - started
    input_paths = (
        CONTOUR_PATH, OVERLAP_PATH, CONTOUR_CONFIG_PATH, OVERLAP_CONFIG_PATH
    )
    results = {
        "schemaVersion": "r073j-continuum-branch-figure-results-v1",
        "figureId": FIGURE_ID,
        "status": "passed",
        "renderedAt": utc_now(),
        "wallTimeSeconds": wall_time,
        "inputBindings": [
            {
                "path": str(path.relative_to(REPOSITORY)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
            for path in input_paths
        ],
        "rowCounts": {
            "sourceData": len(rows),
            "globalContourPanels": 56,
            "localContourPanels": 8,
            "overlapCells": 128,
        },
        "decisions": {
            "globalBasePositiveOrientationWinding": contour["decisions"][
                "globalBasePositiveOrientationWinding"
            ],
            "localBasePositiveOrientationWinding": contour["decisions"][
                "localBasePositiveOrientationWinding"
            ],
            "globalMinimumAbsoluteLowerRaw": contour["decisions"][
                "globalMinimumAbsoluteLower"
            ],
            "localMinimumAbsoluteLowerRaw": contour["decisions"][
                "localMinimumAbsoluteLower"
            ],
            "minimumKineticOverlapLowerRaw": overlap["decisions"][
                "minimumKineticOverlapLower"
            ],
            **plotted,
        },
        "certificateStatus": {
            "contour": contour["status"],
            "overlap": overlap["status"],
        },
        "claimBoundary": contract["claimBoundary"],
        "conditionalStatement": overlap["decisions"]["conditionalBranchImplications"],
    }
    (HERE / "results.json").write_text(canonical(results), encoding="utf-8")
    write_environment(args.deps.resolve() if args.deps else None)
    (HERE / "qa-report.md").write_text(
        "# R0.73J figure QA report\n\n"
        "**Status:** pending manual visual inspection.\n\n"
        "The master figure was regenerated from the sealed certificate JSON files. "
        "Run `validate.py` once to prepare the final-size, grayscale, and PDF-raster "
        "surfaces, inspect all three, record any corrections here, and then rerun "
        "the validator with `--require-formal`.\n",
        encoding="utf-8",
    )
    monitor.event("completed", rows=len(rows), wallTimeSeconds=round(wall_time, 6))
    print(canonical({
        "status": "passed",
        "figureId": FIGURE_ID,
        "rows": len(rows),
        "globalMinimum": plotted["globalMinimum"],
        "localMinimum": plotted["localMinimum"],
        "overlapMinimum": plotted["overlapMinimum"],
        "wallTimeSeconds": wall_time,
    }), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
