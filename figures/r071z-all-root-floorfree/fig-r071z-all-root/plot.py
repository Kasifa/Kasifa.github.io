#!/usr/bin/env python3
"""Render the four-panel R0.71Z all-root journal figure."""

from __future__ import annotations

import argparse
import csv
from datetime import datetime
import json
import os
from pathlib import Path
import resource
import time
from zoneinfo import ZoneInfo

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import numpy as np


ROOT = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo("Asia/Shanghai")
PAPER = "#FBF9F4"
INK = "#252422"
BLUE = "#355C7D"
OCHRE = "#B8792B"
GRAY = "#77736C"
LIGHT = "#D8D3C8"


def append_log(path: Path, payload: dict[str, object]) -> None:
    record = {"timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"), **payload}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.titlesize": 7.65,
            "axes.labelsize": 6.7,
            "xtick.labelsize": 5.75,
            "ytick.labelsize": 5.75,
            "legend.fontsize": 5.15,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.facecolor": PAPER,
            "figure.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "axes.linewidth": 0.72,
            "lines.linewidth": 1.15,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r071z-all-root",
        }
    )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def select(rows: list[dict[str, str]], panel: str, series: str) -> list[dict[str, str]]:
    return sorted(
        [row for row in rows if row["panel"] == panel and row["series"] == series],
        key=lambda row: float(row["x"]),
    )


def xy(rows: list[dict[str, str]]) -> tuple[np.ndarray, np.ndarray]:
    return (
        np.asarray([float(row["x"]) for row in rows], dtype=float),
        np.asarray([float(row["y"]) for row in rows], dtype=float),
    )


def blossom(fig: plt.Figure) -> None:
    center_x, center_y = 0.979, 0.963
    for index, color in enumerate((BLUE, OCHRE, BLUE, OCHRE, BLUE)):
        angle = 2.0 * np.pi * index / 5.0 + np.pi / 2.0
        fig.add_artist(
            Circle(
                (center_x + 0.009 * np.cos(angle), center_y + 0.009 * np.sin(angle)),
                0.0062,
                transform=fig.transFigure,
                facecolor=color,
                edgecolor=PAPER,
                linewidth=0.35,
                alpha=0.82,
                zorder=20,
            )
        )
    fig.add_artist(
        Circle(
            (center_x, center_y),
            0.0048,
            transform=fig.transFigure,
            facecolor=INK,
            edgecolor=PAPER,
            linewidth=0.35,
            zorder=21,
        )
    )


def panel_title(axis: plt.Axes, letter: str, title: str) -> None:
    axis.set_title(f"{letter}   {title}", loc="left", fontweight="bold", pad=4.2)


def log_grid(axis: plt.Axes, *, xbase2: bool = True) -> None:
    if xbase2:
        axis.set_xscale("log", base=2)
    axis.set_yscale("log")
    axis.grid(True, which="major", color=LIGHT, linewidth=0.38)
    axis.grid(True, which="minor", axis="y", color=LIGHT, linewidth=0.22, alpha=0.42)


def power_guide(
    axis: plt.Axes,
    *,
    anchor_x: float,
    anchor_y: float,
    power: float,
    label: str,
    span: tuple[float, float],
    text_offset: tuple[float, float] = (-1.0, 2.0),
) -> None:
    guide_x = np.geomspace(span[0], span[1], 64)
    guide_y = anchor_y * (guide_x / anchor_x) ** power
    axis.plot(guide_x, guide_y, color=GRAY, linestyle=(0, (1.2, 1.5)), linewidth=0.68, zorder=1)
    axis.annotate(
        label,
        xy=(guide_x[-1], guide_y[-1]),
        xytext=text_offset,
        textcoords="offset points",
        ha="right",
        va="bottom",
        fontsize=5.15,
        color=GRAY,
    )


def set_m_ticks(axis: plt.Axes) -> None:
    ticks = np.asarray([3, 129, 8193, 524289, 33554433, 1073741825], dtype=float)
    axis.set_xticks(ticks)
    axis.set_xticklabels(["3", "129", "8k", "524k", "34m", "1.1b"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-stem", type=Path, required=True)
    args = parser.parse_args()
    started = time.perf_counter()
    rows = load_rows(args.data)
    results = json.loads(args.results.read_text(encoding="utf-8"))
    config = json.loads(args.config.read_text(encoding="utf-8"))
    configure()
    append_log(ROOT / "progress.ndjson", {"stage": "plot-start"})

    # Matplotlib's raster canvas is integer-valued at its default 100 dpi.
    # Two-decimal inch dimensions keep PDF, SVG, and 600 dpi raster exports
    # on one stable physical footprint, as in the adjacent formal packages.
    width = round(float(config["figure"]["widthMillimetres"]) / 25.4, 2)
    height = round(float(config["figure"]["heightMillimetres"]) / 25.4, 2)
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        2,
        2,
        left=0.086,
        right=0.985,
        bottom=0.186,
        top=0.846,
        wspace=0.32,
        hspace=0.46,
    )
    axa = fig.add_subplot(grid[0, 0])
    axb = fig.add_subplot(grid[0, 1])
    axc = fig.add_subplot(grid[1, 0])
    axd = fig.add_subplot(grid[1, 1])

    fig.suptitle(
        "All-root suppression and launch retention",
        x=0.086,
        y=0.965,
        ha="left",
        fontsize=10.2,
        fontweight="bold",
    )
    fig.text(
        0.086,
        0.922,
        r"Analytic/certificate envelopes  $\cdot$  real shear and unit phases  $\cdot$  fixed target  $\cdot$  no DNS",
        ha="left",
        fontsize=6.3,
        color=GRAY,
    )
    blossom(fig)

    # Panel A: exact complete-root lattice payment.
    m_exact, exact_factor = xy(select(rows, "A", "exact minimum-lattice factor M/Ks"))
    m_upper, upper_factor = xy(select(rows, "A", "analytic upper bound 3/M^2"))
    if not np.array_equal(m_exact, m_upper):
        raise RuntimeError("Panel A M grids do not agree")
    axa.plot(
        m_exact,
        exact_factor,
        color=BLUE,
        linestyle="-",
        marker="o",
        markevery=3,
        markersize=3.0,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        label=r"exact $M/K_s$",
        zorder=3,
    )
    axa.plot(
        m_upper,
        upper_factor,
        color=GRAY,
        linestyle="--",
        marker="s",
        markevery=(1, 4),
        markersize=2.8,
        markerfacecolor=PAPER,
        markeredgecolor=GRAY,
        markeredgewidth=0.7,
        label=r"analytic $3/M^2$ bound",
        zorder=2,
    )
    log_grid(axa)
    set_m_ticks(axa)
    axa.set_ylim(8.0e-19, 6.0e-1)
    axa.set_xlabel(r"carrier count $M$")
    axa.set_ylabel("dimensionless lattice factor")
    lattice_power = results["derivedFigureFits"]["latticeMOverKs"]["power"]
    axa.text(
        0.025,
        0.965,
        rf"$K_s=\sum_{{j=1}}^M j^2$; exact tail fit $p={lattice_power:.6f}$",
        transform=axa.transAxes,
        ha="left",
        va="top",
        fontsize=5.2,
        color=GRAY,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.9, "pad": 0.55},
    )
    axa.legend(loc="lower left", frameon=False, handlelength=2.4, borderaxespad=0.3)
    panel_title(axa, "A", "Exact integer-lattice factor")

    # Panel B: new complete-root envelope versus the neutral prior comparator.
    b_complete = "complete-root BV envelope; eta=1"
    b_selected = "prior selected-root envelope; N=(M-1)/2"
    m_complete, y_complete = xy(select(rows, "B", b_complete))
    m_selected, y_selected = xy(select(rows, "B", b_selected))
    axb.plot(
        m_complete,
        y_complete,
        color=BLUE,
        linestyle="-",
        marker="o",
        markevery=3,
        markersize=3.0,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        label=r"complete roots: $M/K_s$",
        zorder=3,
    )
    axb.plot(
        m_selected,
        y_selected,
        color=GRAY,
        linestyle="--",
        marker="s",
        markevery=(1, 4),
        markersize=2.8,
        markerfacecolor=PAPER,
        markeredgecolor=GRAY,
        markeredgewidth=0.7,
        label=r"prior selected roots: $NM/K_s$",
        zorder=2,
    )
    log_grid(axb)
    set_m_ticks(axb)
    axb.set_ylim(2.0e-19, 3.5)
    axb.set_xlabel(r"carrier count $M=2N+1$")
    axb.set_ylabel(r"upper envelope / common $M=3$ value")
    power_guide(axb, anchor_x=8193, anchor_y=1.3e-6, power=-1.0, label=r"$M^{-1}$", span=(8193, 1073741825))
    power_guide(axb, anchor_x=8193, anchor_y=2.0e-7, power=-2.0, label=r"$M^{-2}$", span=(8193, 33554433), text_offset=(-1.0, -6.0))
    axb.text(
        0.025,
        0.965,
        r"bounded $\eta=1$; same constants and common normalizer",
        transform=axb.transAxes,
        ha="left",
        va="top",
        fontsize=5.15,
        color=GRAY,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.9, "pad": 0.55},
    )
    axb.legend(loc="lower left", frameon=False, handlelength=2.45, borderaxespad=0.3)
    panel_title(axb, "B", "Complete versus selected roots")

    # Panel C: exact envelope under three coupling laws.
    c_styles = (
        ("bounded eta=1", BLUE, "-", "o", BLUE, r"$\eta=1$: $M^{-2}$", 3, 4),
        ("eta=M^(1/2)", INK, "-.", "^", PAPER, r"$\eta=M^{1/2}$: $M^{-5/6}$", (1, 4), 3),
        ("eta=M^(6/7)", OCHRE, ":", "D", PAPER, r"$\eta=M^{6/7}$: $M^0$ diagnostic", (2, 4), 5),
    )
    for series, color, style, marker, face, label, markevery, zorder in c_styles:
        x_values, y_values = xy(select(rows, "C", series))
        axc.plot(
            x_values,
            y_values,
            color=color,
            linestyle=style,
            marker=marker,
            markevery=markevery,
            markersize=2.9,
            markerfacecolor=face,
            markeredgecolor=color,
            markeredgewidth=0.72,
            linewidth=1.15,
            label=label,
            zorder=zorder,
        )
    log_grid(axc)
    set_m_ticks(axc)
    axc.set_ylim(2.0e-19, 3.5)
    axc.set_xlabel(r"carrier count $M$")
    axc.set_ylabel(r"upper envelope / own $M=3$ value")
    axc.text(
        0.025,
        0.965,
        r"exact $C_{\rm BV}=e^{2\lambda_0L}(4+C_\kappa\eta)$ retained",
        transform=axc.transAxes,
        ha="left",
        va="top",
        fontsize=5.1,
        color=GRAY,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.9, "pad": 0.55},
    )
    axc.legend(loc="lower left", frameon=False, handlelength=2.45, borderaxespad=0.3)
    panel_title(axc, "C", "Observation-coupling laws")

    # Panel D: exact heat retention and the launch-inclusive identity.
    r_fixed, retention = xy(select(rows, "D", "fixed-window exact heat retention"))
    r_launch, retention_launch = xy(select(rows, "D", "launch-inclusive retention"))
    axd.plot(
        r_fixed,
        retention,
        color=OCHRE,
        linestyle="-",
        marker="D",
        markevery=[0, 1, 3, 7, 15, 31],
        markersize=3.0,
        markerfacecolor=PAPER,
        markeredgecolor=OCHRE,
        markeredgewidth=0.72,
        label=r"fixed window: $e^{-2\nu d^2A_0R^2}$",
        zorder=4,
    )
    axd.plot(
        r_launch,
        retention_launch,
        color=GRAY,
        linestyle="--",
        marker="s",
        markevery=[0, 7, 15, 23, 31],
        markersize=2.8,
        markerfacecolor=PAPER,
        markeredgecolor=GRAY,
        markeredgewidth=0.7,
        label="launch-inclusive: retention = 1",
        zorder=3,
    )
    axd.set_yscale("log")
    axd.grid(True, which="major", color=LIGHT, linewidth=0.38)
    axd.grid(True, which="minor", axis="y", color=LIGHT, linewidth=0.22, alpha=0.42)
    axd.set_xlim(0.5, 32.5)
    axd.set_ylim(1.0e-60, 3.0)
    axd.set_xticks([1, 4, 8, 16, 24, 32])
    axd.set_xlabel(r"heat-shear multiplier $R$")
    axd.set_ylabel(r"enstrophy retention $\theta$")
    heat_coefficient = results["parameters"]["heatCoefficient"]
    axd.text(
        0.025,
        0.965,
        rf"$\nu=0.02$, $d=8$, $A_0=0.05$; $-\log\theta={heat_coefficient:.3f}R^2$",
        transform=axd.transAxes,
        ha="left",
        va="top",
        fontsize=5.1,
        color=GRAY,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.9, "pad": 0.55},
    )
    axd.text(
        0.975,
        0.09,
        "exact heat shear\nretention boundary only",
        transform=axd.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.0,
        color=GRAY,
    )
    axd.legend(loc="lower left", frameon=False, handlelength=2.35, borderaxespad=0.3)
    panel_title(axd, "D", "Fixed-window retention boundary")

    fig.text(
        0.086,
        0.111,
        "Source: R0.71Z analytic theorem, high-precision certificate, and independent finite-matrix audit.",
        ha="left",
        fontsize=5.25,
        color=GRAY,
    )
    fig.text(
        0.086,
        0.075,
        "Analytic/certificate values, not DNS. Complete squared-slope mass, not raw root count; strong-coupling curve is diagnostic only.",
        ha="left",
        fontsize=5.05,
        color=GRAY,
    )
    fig.text(
        0.086,
        0.043,
        "Real-shear, fixed-target, unit-phase triangular class; launch-inclusive payment with roots on the later window. No universal endpoint or regularity claim.",
        ha="left",
        fontsize=5.0,
        color=GRAY,
    )

    output_stem = args.output_stem
    pdf_metadata = {
        "Title": "All-root suppression and launch retention",
        "Author": "Kasifa",
        "Subject": "R0.71Z analytic and certificate envelopes",
        "Keywords": "Navier-Stokes, all-root sampling, lattice suppression, launch retention",
    }
    svg_metadata = {
        "Title": "All-root suppression and launch retention",
        "Creator": "Kasifa",
        "Description": "R0.71Z analytic and certificate envelopes",
    }
    fig.savefig(output_stem.with_suffix(".pdf"), metadata=pdf_metadata)
    fig.savefig(output_stem.with_suffix(".svg"), metadata=svg_metadata)
    fig.savefig(
        output_stem.with_suffix(".png"),
        dpi=int(config["figure"]["pngDpi"]),
        metadata={"Software": "Matplotlib"},
    )
    plt.close(fig)

    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(
        ROOT / "progress.ndjson",
        {"stage": "plot-complete", "outputs": ["figure.pdf", "figure.svg", "figure.png"], "elapsedSeconds": elapsed},
    )
    append_log(
        ROOT / "resource-log.ndjson",
        {
            "stage": "plot-complete",
            "elapsedSeconds": elapsed,
            "pid": os.getpid(),
            "processUserCpuSeconds": usage.ru_utime,
            "processSystemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "figureInches": [width, height],
                "outputs": [str(output_stem.with_suffix(suffix)) for suffix in (".pdf", ".svg", ".png")],
                "elapsedSeconds": elapsed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
