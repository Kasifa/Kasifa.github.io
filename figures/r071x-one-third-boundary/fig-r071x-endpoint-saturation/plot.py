#!/usr/bin/env python3
"""Render the three-panel R0.71X endpoint-saturation journal figure."""

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
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
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
            "svg.hashsalt": "r071x-endpoint-saturation",
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


def log_grid(axis: plt.Axes, *, x_base_two: bool = True) -> None:
    if x_base_two:
        axis.set_xscale("log", base=2)
    else:
        axis.set_xscale("log")
    axis.set_yscale("log")
    axis.grid(True, which="major", color=LIGHT, linewidth=0.38)
    axis.grid(True, which="minor", axis="y", color=LIGHT, linewidth=0.23, alpha=0.45)


def guide(
    axis: plt.Axes,
    x_values: np.ndarray,
    anchor: float,
    power: float,
    label: str,
    *,
    factor: float,
    text_offset: tuple[float, float] = (-2.0, 1.0),
) -> None:
    y_values = anchor * factor * (x_values / x_values[0]) ** power
    axis.plot(x_values, y_values, color=GRAY, linestyle=(0, (1.2, 1.5)), linewidth=0.68, zorder=1)
    axis.annotate(
        label,
        xy=(x_values[-1], y_values[-1]),
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
        height_ratios=(1.02, 1.0),
        left=0.088,
        right=0.985,
        bottom=0.190,
        top=0.852,
        wspace=0.31,
        hspace=0.43,
    )
    axa = fig.add_subplot(grid[0, :])
    axb = fig.add_subplot(grid[1, 0])
    axc = fig.add_subplot(grid[1, 1])

    fig.suptitle(
        "Fixed-small-coupling endpoint scaling",
        x=0.088,
        y=0.963,
        ha="left",
        fontsize=10.15,
        fontweight="bold",
    )
    fig.text(
        0.088,
        0.919,
        r"$A_q=\delta q^2$  $\cdot$  fixed-$\delta$ panels use $\delta=1/128$  $\cdot$  target $(1,1)$  $\cdot$  roots $(.1,.2)/q^2$  $\cdot$  finite coset $R=40$",
        ha="left",
        fontsize=6.35,
        color=GRAY,
    )
    blossom(fig)

    # Panel A: indexed q scaling preserves the raw values in the data package.
    q_d, d_index = xy(select(rows, "A", "initial-data D indexed to q=256"))
    q_a, atom_index = xy(select(rows, "A", "complete prescribed atomProxy sum indexed to q=256"))
    if not np.array_equal(q_d, q_a):
        raise RuntimeError("Panel A q grids do not agree")
    axa.plot(
        q_d,
        d_index,
        color=BLUE,
        linestyle="-",
        marker="o",
        markersize=3.35,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        label=r"initial-data $D/D_{256}$",
        zorder=3,
    )
    axa.plot(
        q_a,
        atom_index,
        color=OCHRE,
        linestyle="--",
        marker="s",
        markersize=3.25,
        markerfacecolor=PAPER,
        markeredgecolor=OCHRE,
        markeredgewidth=0.8,
        label=r"two-root atomProxy sum / value at $256$",
        zorder=3,
    )
    guide(axa, q_d, d_index[0], 6.0, r"$q^6$", factor=0.55, text_offset=(-2, 2))
    guide(axa, q_a, atom_index[0], 2.0, r"$q^2$", factor=0.52, text_offset=(-2, -7))
    log_grid(axa)
    axa.set_xticks(q_d)
    axa.set_xticklabels(["256", "512", "1k", "2k", "4k"])
    axa.set_xlabel(r"carrier frequency $q$")
    axa.set_ylabel(r"index, $q=256$ equals 1")
    fit_d = results["derivedFigureFits"]["fixedDeltaInitialDataD"]["power"]
    fit_atom = results["derivedFigureFits"]["fixedDeltaCompletePrescribedAtomProxySum"]["power"]
    axa.text(
        0.012,
        0.925,
        rf"finite $R=40$ fits: $D\sim q^{{{fit_d:.4f}}}$; atomProxy sum $\sim q^{{{fit_atom:.4f}}}$",
        transform=axa.transAxes,
        ha="left",
        va="top",
        fontsize=5.65,
        color=GRAY,
    )
    axa.legend(loc="lower right", frameon=False, handlelength=2.5, ncol=2, columnspacing=1.4)
    panel_title(axa, "A", "Fixed-delta q scaling (indexed)")

    # Panel B: evidence layers; same axes, no arithmetic combination.
    series_b = (
        (
            "high-precision endpoint atom-proxy ratio",
            BLUE,
            "-",
            "o",
            BLUE,
            r"HP atomProxy/$D^{1/3}$",
        ),
        (
            "finite-coset endpoint atomProxy ratio",
            BLUE,
            ":",
            "D",
            PAPER,
            r"finite $R=40$ atomProxy/$D^{1/3}$",
        ),
        (
            "high-precision complete-ledger-normalized proxy",
            INK,
            "-.",
            "^",
            PAPER,
            "HP complete-ledger norm.",
        ),
        (
            "full retained rotational-charge upper bound",
            OCHRE,
            "--",
            "s",
            PAPER,
            r"finite full retained charge upper",
        ),
    )
    for series, color, style, marker, face, label in series_b:
        x_values, y_values = xy(select(rows, "B", series))
        axb.plot(
            x_values,
            y_values,
            color=color,
            linestyle=style,
            marker=marker,
            markersize=3.1,
            markerfacecolor=face,
            markeredgecolor=color,
            markeredgewidth=0.72,
            label=label,
            zorder=3,
        )
    log_grid(axb)
    axb.set_xticks([32, 128, 512, 2048])
    axb.set_xticklabels(["32", "128", "512", "2k"])
    axb.set_ylim(8.0e-12, 5.5e-8)
    axb.set_xlabel(r"carrier frequency $q$")
    axb.set_ylabel("dimensionless certificate / corroboration proxy")
    axb.text(
        0.025,
        0.965,
        "Four layers shown separately; no substitution",
        transform=axb.transAxes,
        ha="left",
        va="top",
        fontsize=5.1,
        color=GRAY,
    )
    axb.legend(loc="center left", bbox_to_anchor=(0.012, 0.50), frameon=False, handlelength=2.35)
    panel_title(axb, "B", "Endpoint-normalized evidence layers")

    # Panel C: delta collapse with a radius-audit inset.
    deltas, endpoint = xy(select(rows, "C", "high-precision delta endpoint collapse"))
    axc.plot(
        deltas,
        endpoint,
        color=BLUE,
        linestyle="-",
        marker="o",
        markersize=3.5,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        label=r"HP atomProxy/$D^{1/3}$",
        zorder=3,
    )
    guide(axc, deltas, endpoint[0], 4.0 / 3.0, r"$\delta^{4/3}$", factor=1.28, text_offset=(-1, 2))
    log_grid(axc, x_base_two=True)
    axc.set_xticks(deltas)
    axc.set_xticklabels(["1/1024", "1/512", "1/256", "1/128", "1/64"], rotation=18, ha="right")
    axc.set_xlabel(r"coupling $\delta$ at $q=2048$", labelpad=0.5)
    axc.set_ylabel(r"endpoint atom-proxy ratio")
    delta_fit = results["derivedFigureFits"]["deltaEndpointCollapse"]["power"]
    axc.text(
        0.97,
        0.08,
        rf"fit $\delta^{{{delta_fit:.6f}}}$",
        transform=axc.transAxes,
        ha="right",
        va="bottom",
        fontsize=5.25,
        color=GRAY,
    )
    axc.legend(loc="lower left", frameon=False, handlelength=2.25)
    panel_title(axc, "C", r"High-precision $\delta^{4/3}$ collapse")

    radius, differences = xy(
        select(rows, "C-inset", "maximum retained-observable relative difference versus R=40")
    )
    inset = inset_axes(axc, width="47%", height="42%", loc="upper left", borderpad=0.72)
    inset.plot(
        radius,
        differences,
        color=OCHRE,
        linestyle=(0, (1.3, 1.5)),
        marker="^",
        markersize=3.0,
        markerfacecolor=PAPER,
        markeredgecolor=OCHRE,
        markeredgewidth=0.72,
    )
    inset.set_yscale("log")
    inset.set_ylim(8.0e-15, 7.0e-12)
    inset.yaxis.set_major_locator(mpl.ticker.FixedLocator([1.0e-14, 1.0e-13, 1.0e-12]))
    inset.yaxis.set_major_formatter(mpl.ticker.FixedFormatter(["1e-14", "1e-13", "1e-12"]))
    inset.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    inset.set_xticks(radius)
    inset.set_xticklabels([str(int(value)) for value in radius])
    inset.set_xlabel(r"radius $R$", fontsize=4.7, labelpad=1.0)
    inset.tick_params(labelsize=4.15, pad=1.0, length=2.0)
    inset.grid(True, color=LIGHT, linewidth=0.25)
    inset.text(
        0.04,
        0.96,
        "max retained-observable\nrel. diff. vs $R=40$",
        transform=inset.transAxes,
        ha="left",
        va="top",
        fontsize=4.25,
        color=INK,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.88, "pad": 0.2},
    )

    fig.text(
        0.088,
        0.066,
        "Evidence boundary: high-precision algebra and finite retained-coset corroboration are separate. atomProxy is not multiplier-locked $J_*$; finite coset is not DNS.",
        ha="left",
        fontsize=5.35,
        color=GRAY,
    )
    fig.text(
        0.088,
        0.035,
        r"$\delta=1/128$ is not proved inside the existential continuum IFT radius; no spectral-convergence, universal $D^{1/3}$, or regularity claim is made.",
        ha="left",
        fontsize=5.25,
        color=GRAY,
    )

    stem = args.output_stem
    pdf_path = stem.with_suffix(".pdf")
    svg_path = stem.with_suffix(".svg")
    png_path = stem.with_suffix(".png")
    fig.savefig(
        pdf_path,
        metadata={
            "Title": "Fixed-small-coupling endpoint scaling",
            "Author": "R0.71X research audit",
            "Creator": "Matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(
        svg_path,
        metadata={
            "Title": "Fixed-small-coupling endpoint scaling",
            "Description": "R0.71X high-precision certificate and finite retained-coset corroboration",
            "Date": None,
        },
    )
    fig.savefig(
        png_path,
        dpi=int(config["figure"]["pngDpi"]),
        metadata={"Software": "Matplotlib; R0.71X deterministic figure pipeline"},
    )
    plt.close(fig)

    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(
        ROOT / "progress.ndjson",
        {"stage": "plot-complete", "elapsedSeconds": elapsed, "outputs": [pdf_path.name, svg_path.name, png_path.name]},
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
    print(json.dumps({"status": "passed", "outputs": [str(pdf_path), str(svg_path), str(png_path)], "elapsedSeconds": elapsed}, indent=2))


if __name__ == "__main__":
    main()
