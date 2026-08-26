#!/usr/bin/env python3
"""Render the three-panel R0.71Y operator-sampling journal figure."""

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
            "axes.titlesize": 7.8,
            "axes.labelsize": 6.8,
            "xtick.labelsize": 5.9,
            "ytick.labelsize": 5.9,
            "legend.fontsize": 5.25,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.facecolor": PAPER,
            "figure.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "axes.linewidth": 0.72,
            "lines.linewidth": 1.18,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r071y-operator-sampling",
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
    axis.set_title(f"{letter}   {title}", loc="left", fontweight="bold", pad=4.5)


def log_grid(axis: plt.Axes) -> None:
    axis.set_xscale("log", base=2)
    axis.set_yscale("log")
    axis.grid(True, which="major", color=LIGHT, linewidth=0.38)
    axis.grid(True, which="minor", axis="y", color=LIGHT, linewidth=0.22, alpha=0.42)


def power_guide(
    axis: plt.Axes,
    x_values: np.ndarray,
    *,
    anchor_x: float,
    anchor_y: float,
    power: float,
    label: str,
    span: tuple[float, float],
    text_offset: tuple[float, float],
) -> None:
    mask = (x_values >= span[0]) & (x_values <= span[1])
    guide_x = x_values[mask]
    guide_y = anchor_y * (guide_x / anchor_x) ** power
    axis.plot(guide_x, guide_y, color=GRAY, linestyle=(0, (1.2, 1.5)), linewidth=0.68, zorder=1)
    axis.annotate(
        label,
        xy=(guide_x[-1], guide_y[-1]),
        xytext=text_offset,
        textcoords="offset points",
        ha="right",
        va="bottom",
        fontsize=5.25,
        color=GRAY,
    )


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

    width = round(float(config["figure"]["widthMillimetres"]) / 25.4, 2)
    height = round(float(config["figure"]["heightMillimetres"]) / 25.4, 2)
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    grid = fig.add_gridspec(
        2,
        2,
        height_ratios=(0.96, 1.0),
        left=0.088,
        right=0.985,
        bottom=0.190,
        top=0.842,
        wspace=0.31,
        hspace=0.43,
    )
    axa = fig.add_subplot(grid[0, :])
    axb = fig.add_subplot(grid[1, 0])
    axc = fig.add_subplot(grid[1, 1])

    fig.suptitle(
        "Growing-root operator-sampling bounds",
        x=0.088,
        y=0.963,
        ha="left",
        fontsize=10.15,
        fontweight="bold",
    )
    fig.text(
        0.088,
        0.916,
        r"Analytic/certificate envelopes  $\cdot$  unit phases $M=2N+1$  $\cdot$  fixed target and enstrophy floors  $\cdot$  selected roots",
        ha="left",
        fontsize=6.35,
        color=GRAY,
    )
    blossom(fig)

    # Panel A: exact lattice payment and theorem upper bound.
    n_exact, exact_factor = xy(select(rows, "A", "exact minimum-lattice factor NM/Ks"))
    n_upper, upper_factor = xy(select(rows, "A", "analytic upper bound 3/(4N)"))
    if not np.array_equal(n_exact, n_upper):
        raise RuntimeError("Panel A N grids do not agree")
    axa.plot(
        n_exact,
        exact_factor,
        color=BLUE,
        linestyle="-",
        marker="o",
        markevery=2,
        markersize=3.15,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        label=r"exact $NM/K_s$, $K_s=\sum_{j=1}^{2N+1}j^2$",
        zorder=3,
    )
    axa.plot(
        n_upper,
        upper_factor,
        color=OCHRE,
        linestyle="--",
        marker="s",
        markevery=(1, 2),
        markersize=3.05,
        markerfacecolor=PAPER,
        markeredgecolor=OCHRE,
        markeredgewidth=0.75,
        label=r"analytic upper bound $3/(4N)$",
        zorder=3,
    )
    log_grid(axa)
    ticks = np.asarray([1, 16, 256, 4096, 65536, 1048576], dtype=float)
    axa.set_xticks(ticks)
    axa.set_xticklabels(["1", "16", "256", "4k", "65k", "1m"])
    axa.set_xlabel(r"selected root count $N$")
    axa.set_ylabel("dimensionless lattice factor")
    power = results["derivedFigureFits"]["latticeFactor"]["power"]
    axa.text(
        0.012,
        0.925,
        rf"exact finite-$N$ identity; last-six-point descriptive fit $p={power:.6f}$",
        transform=axa.transAxes,
        ha="left",
        va="top",
        fontsize=5.65,
        color=GRAY,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.88, "pad": 0.7},
    )
    axa.legend(loc="lower left", frameon=False, handlelength=2.6, ncol=2, columnspacing=1.6)
    panel_title(axa, "A", "Integer-lattice payment")

    # Panel B: normalized theorem laws; raw unnormalized values remain in data.csv.
    b_series = (
        (
            "no separation; fixed delta_obs=1/8",
            BLUE,
            "-",
            "o",
            BLUE,
            r"no separation, $\delta_{\rm obs}=1/8$",
            2,
            3,
        ),
        (
            "separated; fixed h=0.05",
            OCHRE,
            "--",
            "s",
            PAPER,
            r"fixed $h=0.05$",
            (1, 2),
            4,
        ),
        (
            "separated; h=N^-1",
            INK,
            ":",
            "D",
            PAPER,
            r"$h=N^{-1}$ (coincident $N$-law)",
            (0, 2),
            5,
        ),
    )
    for series, color, style, marker, face, label, markevery, zorder in b_series:
        x_values, y_values = xy(select(rows, "B", series))
        axb.plot(
            x_values,
            y_values,
            color=color,
            linestyle=style,
            marker=marker,
            markevery=markevery,
            markersize=2.95,
            markerfacecolor=face,
            markeredgecolor=color,
            markeredgewidth=0.72,
            linewidth=1.05 if series == "separated; h=N^-1" else 1.2,
            label=label,
            zorder=zorder,
        )
    log_grid(axb)
    axb.set_xticks(ticks)
    axb.set_xticklabels(["1", "16", "256", "4k", "65k", "1m"])
    axb.set_ylim(5.0e-13, 2.1)
    axb.set_xlabel(r"selected root count $N$")
    axb.set_ylabel(r"upper envelope / value at $N=1$")
    axb.text(
        0.025,
        0.965,
        r"theorem bounds, not simulated values; common constants normalized out",
        transform=axb.transAxes,
        ha="left",
        va="top",
        fontsize=5.1,
        color=GRAY,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.9, "pad": 0.6},
    )
    power_guide(
        axb,
        x_values,
        anchor_x=256.0,
        anchor_y=1.1e-3,
        power=-1.0,
        label=r"$N^{-1}$",
        span=(256, 1048576),
        text_offset=(-2, 2),
    )
    power_guide(
        axb,
        x_values,
        anchor_x=64.0,
        anchor_y=1.2e-3,
        power=-2.0,
        label=r"$N^{-2}$",
        span=(64, 65536),
        text_offset=(-2, -7),
    )
    axb.legend(loc="lower left", frameon=False, handlelength=2.4, borderaxespad=0.3)
    panel_title(axb, "B", "Selected-root envelope laws")

    # Panel C: the exact determinant-based lower bound, already log10 transformed.
    n_inverse, inverse_log = xy(select(rows, "C", "equal-grid inverse lower bound; h=N^-3"))
    axc.plot(
        n_inverse,
        inverse_log,
        color=BLUE,
        linestyle="-",
        marker="o",
        markersize=3.45,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        zorder=3,
    )
    axc.set_xscale("log", base=2)
    axc.grid(True, which="major", color=LIGHT, linewidth=0.38)
    axc.set_xticks(n_inverse)
    axc.set_xticklabels([str(int(value)) for value in n_inverse])
    axc.set_ylim(0.0, 54.0)
    axc.set_yticks([0, 10, 20, 30, 40, 50])
    axc.set_xlabel(r"selected root count $N$")
    axc.set_ylabel(r"$\log_{10}$ inverse lower bound")
    for x_value, y_value in zip(n_inverse, inverse_log, strict=True):
        if x_value in (4, 16, 64):
            axc.annotate(
                f"{y_value:.2f}",
                xy=(x_value, y_value),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=5.15,
                color=INK,
            )
    axc.text(
        0.025,
        0.965,
        r"$r_l=l$, $h=N^{-3}$, $b=2\nu d^2=2.56$",
        transform=axc.transAxes,
        ha="left",
        va="top",
        fontsize=5.1,
        color=GRAY,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.9, "pad": 0.6},
    )
    axc.text(
        0.975,
        0.08,
        "conditioning lower bound\nnot an IFT-radius upper bound",
        transform=axc.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.05,
        color=GRAY,
    )
    panel_title(axc, "C", "Equal-grid conditioning squeeze")

    fig.text(
        0.088,
        0.107,
        "Source: R0.71Y analytic theorem and committed high-precision / independent certificates.",
        ha="left",
        fontsize=5.35,
        color=GRAY,
    )
    fig.text(
        0.088,
        0.069,
        "Analytic/certificate envelopes, not DNS; selected unit-phase roots with full floors only. No growing-root construction, universal endpoint, or regularity claim.",
        ha="left",
        fontsize=5.15,
        color=GRAY,
    )

    output_stem = args.output_stem
    pdf_metadata = {
        "Title": "Growing-root operator-sampling bounds",
        "Author": "Kasifa",
        "Subject": "R0.71Y analytic and certificate envelopes",
        "Keywords": "Navier-Stokes, operator sampling, growing roots, exact bounds, conditioning",
    }
    svg_metadata = {
        "Title": "Growing-root operator-sampling bounds",
        "Creator": "Kasifa",
        "Description": "R0.71Y analytic and certificate envelopes",
    }
    fig.savefig(output_stem.with_suffix(".pdf"), metadata=pdf_metadata)
    fig.savefig(output_stem.with_suffix(".svg"), metadata=svg_metadata)
    fig.savefig(output_stem.with_suffix(".png"), dpi=int(config["figure"]["pngDpi"]), metadata={"Software": "Matplotlib"})
    plt.close(fig)

    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(
        ROOT / "progress.ndjson",
        {
            "stage": "plot-complete",
            "outputs": ["figure.pdf", "figure.svg", "figure.png"],
            "elapsedSeconds": elapsed,
        },
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
