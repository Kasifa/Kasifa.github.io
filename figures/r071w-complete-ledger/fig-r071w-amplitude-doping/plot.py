#!/usr/bin/env python3
"""Render the three-panel R0.71W amplitude-doping journal figure."""

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
    record = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        **payload,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def configure() -> None:
    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.05,
            "axes.titlesize": 7.9,
            "axes.labelsize": 6.9,
            "xtick.labelsize": 6.05,
            "ytick.labelsize": 6.05,
            "legend.fontsize": 5.75,
            "axes.edgecolor": INK,
            "axes.labelcolor": INK,
            "text.color": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "axes.facecolor": PAPER,
            "figure.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "axes.linewidth": 0.72,
            "lines.linewidth": 1.22,
            "pdf.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r071w-amplitude-doping",
        }
    )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def select(
    rows: list[dict[str, str]], panel: str, series: str
) -> list[dict[str, str]]:
    return sorted(
        [
            row
            for row in rows
            if row["panel"] == panel and row["series"] == series
        ],
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
                (
                    center_x + 0.009 * np.cos(angle),
                    center_y + 0.009 * np.sin(angle),
                ),
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


def log_grid(axis: plt.Axes, *, base_two_x: bool = True) -> None:
    if base_two_x:
        axis.set_xscale("log", base=2)
    axis.set_yscale("log")
    axis.grid(True, which="major", color=LIGHT, linewidth=0.38)
    axis.grid(True, which="minor", axis="y", color=LIGHT, linewidth=0.24, alpha=0.45)


def power_guide(
    axis: plt.Axes,
    x_values: np.ndarray,
    y_values: np.ndarray,
    power: float,
    label: str,
    color: str,
    *,
    start: int,
    factor: float = 1.0,
) -> None:
    guide_x = x_values[start:]
    guide_y = y_values[start] * factor * (guide_x / guide_x[0]) ** power
    axis.plot(
        guide_x,
        guide_y,
        color=color,
        linewidth=0.72,
        linestyle=(0, (1.3, 1.5)),
        alpha=0.78,
        zorder=1,
    )
    axis.annotate(
        label,
        xy=(guide_x[-1], guide_y[-1]),
        xytext=(-1, 2),
        textcoords="offset points",
        ha="right",
        va="bottom",
        fontsize=5.35,
        color=color,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-stem", type=Path, required=True)
    arguments = parser.parse_args()
    started = time.perf_counter()
    rows = load_rows(arguments.data)
    results = json.loads(arguments.results.read_text(encoding="utf-8"))
    config = json.loads(arguments.config.read_text(encoding="utf-8"))
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
        bottom=0.157,
        top=0.856,
        wspace=0.30,
        hspace=0.42,
    )
    axa = fig.add_subplot(grid[0, :])
    axb = fig.add_subplot(grid[1, 0])
    axc = fig.add_subplot(grid[1, 1])

    fig.suptitle(
        "Amplitude-doped complete-ledger test",
        x=0.088,
        y=0.963,
        ha="left",
        fontsize=10.15,
        fontweight="bold",
    )
    fig.text(
        0.088,
        0.920,
        r"$A_q=q^{3/2}$  $\cdot$  $\nu=.02$  $\cdot$  target $(1,1)$  $\cdot$  $d=8$  $\cdot$  roots $(.1,.2)/q^2$  $\cdot$  background $B_q=A_qq$",
        ha="left",
        fontsize=6.45,
        color=GRAY,
    )
    blossom(fig)

    # Panel A: certified analytic complete-ledger ratio.
    q_a, ratio = xy(select(rows, "A", "atom over complete-ledger proxy"))
    axa.plot(
        q_a,
        ratio,
        color=BLUE,
        linestyle="-",
        marker="o",
        markersize=3.3,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        label=r"certified $M_{2,q}/\mathcal{L}_q$",
        zorder=3,
    )
    axa.axhline(1.0, color=GRAY, linestyle="--", linewidth=0.65, alpha=0.78)
    power_guide(
        axa,
        q_a,
        ratio,
        1.0,
        r"$q^{+1}$",
        INK,
        start=len(q_a) - 4,
        factor=0.67,
    )
    log_grid(axa)
    axa.set_xticks([2**8, 2**12, 2**16, 2**20, 2**24, 2**28, 2**32])
    axa.set_xticklabels([r"$2^8$", r"$2^{12}$", r"$2^{16}$", r"$2^{20}$", r"$2^{24}$", r"$2^{28}$", r"$2^{32}$"])
    axa.set_xlabel(r"carrier frequency $q$")
    axa.set_ylabel(r"atom / complete-ledger proxy")
    fitted_a = results["derivedFigureFits"]["analyticAtomToCompleteLedger"]["power"]
    axa.text(
        0.012,
        0.93,
        rf"tail-four fit: $q^{{{fitted_a:+.3f}}}$",
        transform=axa.transAxes,
        ha="left",
        va="top",
        fontsize=5.75,
        color=GRAY,
    )
    axa.legend(loc="lower right", frameon=False, handlelength=2.4)
    panel_title(axa, "A", "Certified atom-to-complete-ledger ratio")

    # Panel B: finite nonlinear retained-coset corroboration.
    q_b, atom = xy(select(rows, "B", "nonlinear truncated atom proxy"))
    q_charge, charge = xy(
        select(rows, "B", "full retained H^-1 rotational charge")
    )
    if not np.array_equal(q_b, q_charge):
        raise RuntimeError("Panel B q grids do not agree")
    axb.plot(
        q_b,
        atom,
        color=BLUE,
        linestyle="-",
        marker="o",
        markersize=3.5,
        markerfacecolor=BLUE,
        markeredgecolor=PAPER,
        markeredgewidth=0.45,
        label=r"second-root atom $M_{2,q}^{(R=40)}$",
        zorder=3,
    )
    axb.plot(
        q_b,
        charge,
        color=OCHRE,
        linestyle="--",
        marker="s",
        markersize=3.25,
        markerfacecolor=PAPER,
        markeredgecolor=OCHRE,
        markeredgewidth=0.80,
        label=r"full retained $H^{-1}$ charge",
        zorder=3,
    )
    power_guide(axb, q_b, atom, 1.0, r"$q^{+1}$", BLUE, start=1, factor=0.70)
    power_guide(
        axb, q_b, charge, -1.0, r"$q^{-1}$", OCHRE, start=1, factor=2.8
    )
    log_grid(axb)
    axb.set_xticks(q_b)
    axb.set_xticklabels(["256", "512", "1k", "2k", "4k"])
    axb.set_ylim(float(np.min(charge)) * 0.45, float(np.max(atom)) * 4.0)
    axb.set_xlabel(r"carrier frequency $q$")
    axb.set_ylabel("dimensionless proxy")
    fitted_atom = results["derivedFigureFits"]["nonlinearAtomProxy"]["power"]
    fitted_charge = results["derivedFigureFits"]["nonlinearRotationalCharge"]["power"]
    axb.text(
        0.025,
        0.34,
        rf"fits: ${fitted_atom:+.3f}$, ${fitted_charge:+.3f}$",
        transform=axb.transAxes,
        ha="left",
        va="bottom",
        fontsize=5.25,
        color=GRAY,
    )
    axb.legend(
        loc="center left",
        bbox_to_anchor=(0.015, 0.52),
        frameon=False,
        handlelength=2.5,
    )
    panel_title(axb, "B", "Finite nonlinear coset scaling")

    # Panel C: normalized root slope and the q=1024 radius audit.
    q_c, slopes = xy(select(rows, "C", "normalized second-root slope"))
    axc.plot(
        q_c,
        slopes,
        color=INK,
        linestyle="-",
        marker="D",
        markersize=3.25,
        markerfacecolor=PAPER,
        markeredgecolor=INK,
        markeredgewidth=0.75,
        label=r"$|a_t(t_2)|/A_q^2$",
        zorder=3,
    )
    axc.axhline(
        slopes[-1], color=GRAY, linestyle=(0, (1.3, 1.5)), linewidth=0.72
    )
    axc.set_xscale("log", base=2)
    axc.set_xticks(q_c)
    axc.set_xticklabels(["256", "512", "1k", "2k", "4k"])
    axc.set_ylim(0.16175, 0.16435)
    axc.set_xlabel(r"carrier frequency $q$")
    axc.set_ylabel(r"normalized second-root slope")
    axc.grid(True, color=LIGHT, linewidth=0.38)
    axc.legend(loc="lower right", frameon=False, handlelength=2.4)
    panel_title(axc, "C", "Root transversality and radius audit")

    inset_rows = select(rows, "C-inset", "slope relative difference versus R=40")
    radii, slope_difference = xy(inset_rows)
    inset = inset_axes(
        axc, width="48%", height="36%", loc="upper right", borderpad=0.75
    )
    inset.plot(
        radii,
        slope_difference,
        color=OCHRE,
        linestyle="--",
        marker="^",
        markersize=2.7,
        markerfacecolor=PAPER,
        markeredgecolor=OCHRE,
        markeredgewidth=0.65,
    )
    inset.set_yscale("log")
    inset.set_ylim(1.4e-16, 4.0e-15)
    inset.yaxis.set_major_locator(
        mpl.ticker.FixedLocator([2.0e-16, 1.0e-15, 3.0e-15])
    )
    inset.yaxis.set_major_formatter(
        mpl.ticker.FixedFormatter(["2e-16", "1e-15", "3e-15"])
    )
    inset.yaxis.set_minor_formatter(mpl.ticker.NullFormatter())
    inset.set_xticks(radii)
    inset.set_xticklabels([str(int(value)) for value in radii])
    inset.set_xlabel(r"radius $R$", fontsize=4.8, labelpad=1.1)
    inset.tick_params(labelsize=4.25, pad=1.0, length=2.0)
    inset.grid(True, color=LIGHT, linewidth=0.25)
    inset.text(
        0.035,
        0.95,
        "$q=1024$; relative slope diff.\nref. $R=40$",
        transform=inset.transAxes,
        ha="left",
        va="top",
        fontsize=4.45,
        color=INK,
        bbox={"facecolor": PAPER, "edgecolor": "none", "alpha": 0.90, "pad": 0.20},
    )

    fig.text(
        0.088,
        0.066,
        "Evidence boundary: analytic certificate in A; finite retained-coset ODE corroboration in B-C. Computation corroboration only - not DNS.",
        ha="left",
        fontsize=5.55,
        color=GRAY,
    )
    fig.text(
        0.088,
        0.035,
        "No continuum IFT or spectral-convergence proof is claimed; the initial-data norms are not uniformly bounded; source data are fully archived.",
        ha="left",
        fontsize=5.35,
        color=GRAY,
    )

    stem = arguments.output_stem
    pdf_path = stem.with_suffix(".pdf")
    svg_path = stem.with_suffix(".svg")
    png_path = stem.with_suffix(".png")
    fig.savefig(
        pdf_path,
        metadata={
            "Title": "Amplitude-doped complete-ledger test",
            "Author": "R0.71W research audit",
            "Creator": "Matplotlib",
            "CreationDate": None,
            "ModDate": None,
        },
    )
    fig.savefig(
        svg_path,
        metadata={
            "Title": "Amplitude-doped complete-ledger test",
            "Description": "R0.71W analytic certificate and finite retained-coset corroboration",
            "Date": None,
        },
    )
    fig.savefig(
        png_path,
        dpi=int(config["figure"]["pngDpi"]),
        metadata={"Software": "Matplotlib; R0.71W deterministic figure pipeline"},
    )
    plt.close(fig)

    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(
        ROOT / "progress.ndjson",
        {
            "stage": "plot-complete",
            "elapsedSeconds": elapsed,
            "outputs": [pdf_path.name, svg_path.name, png_path.name],
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
                "outputs": [str(pdf_path), str(svg_path), str(png_path)],
                "elapsedSeconds": elapsed,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
