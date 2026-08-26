#!/usr/bin/env python3
"""Render the 178 mm R0.71P journal figure from certificate-backed CSV data."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch


WIDTH_MM = 178.0
HEIGHT_MM = 118.0
MM_PER_INCH = 25.4
FIGSIZE_IN = (7.01, 4.65)  # Matplotlib 3.11 rounds figsize to 0.01 inch.
BLUE = "#355C7D"
OCHRE = "#B8792B"
INK = "#252422"
GRAY = "#77736C"
LIGHT = "#D9D5CC"
PAPER = "#FBF9F4"


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def select(rows: list[dict[str, str]], panel: str, series: str) -> list[dict[str, str]]:
    return [row for row in rows if row["panel"] == panel and row["series"] == series]


def panel_header(ax: plt.Axes, label: str, title: str) -> None:
    ax.text(
        -0.13,
        1.08,
        label,
        transform=ax.transAxes,
        fontsize=10.0,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
    )
    ax.text(
        -0.02,
        1.075,
        title,
        transform=ax.transAxes,
        fontsize=8.2,
        fontweight="bold",
        color=INK,
        ha="left",
        va="top",
    )


def style_axis(ax: plt.Axes) -> None:
    ax.set_facecolor(PAPER)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(INK)
        ax.spines[side].set_linewidth(0.7)
    ax.tick_params(axis="both", labelsize=6.4, width=0.65, length=2.5, colors=INK)
    ax.grid(axis="y", color=LIGHT, linewidth=0.55, alpha=0.75, zorder=0)


def panel_a(ax: plt.Axes, rows: list[dict[str, str]]) -> None:
    style_axis(ax)
    panel_header(ax, "A", "Segmented/soft entry versus hard V+")
    table = {(row["case"], row["component"]): float(row["value"]) for row in rows}
    cases = ("odd crossing m=1", "even touch m=2")
    x = np.arange(2, dtype=float)
    width = 0.32
    segmented = [table[(case, "segmentedSoftEntry")] for case in cases]
    hard = [table[(case, "ordinaryHardPositiveAtom")] for case in cases]
    bars_a = ax.bar(
        x - width / 2,
        segmented,
        width,
        color=BLUE,
        edgecolor=INK,
        linewidth=0.65,
        label=r"segmented/soft $A_+$",
        zorder=3,
    )
    bars_b = ax.bar(
        x + width / 2,
        hard,
        width,
        facecolor=PAPER,
        edgecolor=OCHRE,
        linewidth=1.0,
        hatch="////",
        label=r"hard $(A_+-A_-)^+$",
        zorder=3,
    )
    for bar in (*bars_a, *bars_b):
        value = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.045,
            f"{value:.0f}",
            ha="center",
            va="bottom",
            fontsize=6.5,
            color=INK,
            fontfamily="DejaVu Sans Mono",
        )
    ax.annotate(
        "even-touch gap\n" r"$min(A_+,A_-)=1$",
        xy=(1 + width / 2, 0.02),
        xytext=(0.48, 0.47),
        textcoords="data",
        fontsize=5.8,
        color=INK,
        ha="center",
        bbox=dict(boxstyle="round,pad=0.14", facecolor=PAPER, edgecolor="none", alpha=0.94),
        arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.75),
    )
    ax.set_xticks(x, ("odd crossing", "even touch"))
    ax.set_ylabel("positive atomic mass", fontsize=6.8, color=INK)
    ax.set_ylim(0.0, 1.32)
    ax.set_yticks((0.0, 0.5, 1.0))
    ax.legend(
        loc="upper left",
        frameon=False,
        fontsize=6.1,
        handlelength=1.7,
        borderaxespad=0.2,
    )


def panel_b(ax: plt.Axes, cell_rows: list[dict[str, str]], summary_rows: list[dict[str, str]]) -> None:
    style_axis(ax)
    panel_header(ax, "B", "Simultaneous-cell bounded-overlap batch")
    cell = {(row["case"], row["component"]): float(row["value"]) for row in cell_rows}
    cases = ("cell Q1", "cell Q2", "cell Q3")
    x = np.arange(3, dtype=float)
    width = 0.31
    entries = [cell[(case, "entryAtom")] for case in cases]
    budgets = [cell[(case, "localSupportBudget")] for case in cases]
    bars_a = ax.bar(
        x - width / 2,
        entries,
        width,
        color=BLUE,
        edgecolor=INK,
        linewidth=0.65,
        label=r"entry $A_{Q,+}$",
        zorder=3,
    )
    bars_b = ax.bar(
        x + width / 2,
        budgets,
        width,
        facecolor=PAPER,
        edgecolor=OCHRE,
        linewidth=1.0,
        hatch="....",
        label="local support budget",
        zorder=3,
    )
    for bar in (*bars_a, *bars_b):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 0.12,
            f"{bar.get_height():g}",
            ha="center",
            va="bottom",
            fontsize=5.9,
            color=INK,
            fontfamily="DejaVu Sans Mono",
        )
    summary = {row["component"]: float(row["value"]) for row in summary_rows}
    chain = (
        rf"$\sum A_+={summary['entrySum']:g}$"
        rf" $\leq {summary['localEnergySum']:g}$"
        rf" $\leq M_\chi\|F\|^2/Y={summary['overlapGlobalBudget']:g}$"
    )
    ax.text(
        0.5,
        0.955,
        chain,
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=6.2,
        color=INK,
        bbox=dict(boxstyle="round,pad=0.23", facecolor="#F0EDE5", edgecolor=LIGHT, linewidth=0.7),
    )
    ax.set_xticks(x, ("Q1", "Q2", "Q3"))
    ax.set_ylabel("normalized batch mass", fontsize=6.8, color=INK)
    ax.set_ylim(0.0, 6.8)
    ax.set_yticks((0, 2, 4, 6))
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.0, 0.79),
        frameon=False,
        fontsize=6.0,
        handlelength=1.7,
        borderaxespad=0.2,
    )


def panel_c(ax: plt.Axes, rows: list[dict[str, str]]) -> None:
    style_axis(ax)
    panel_header(ax, "C", "Sequential entries and ordinary time budgets")
    by_series: dict[str, list[tuple[float, float]]] = {}
    for row in rows:
        by_series.setdefault(row["series"], []).append((float(row["x"]), float(row["value"])))
    for values in by_series.values():
        values.sort()
    styles = (
        ("hardEntryMass", BLUE, "-", "o", BLUE, r"entry mass $N$"),
        ("ordinaryTimeBudget", INK, "--", "s", PAPER, r"$\int 1\,dt=2\pi$"),
        ("CtSquareMass", GRAY, ":", "^", PAPER, r"$\int\|C_t\|^2dt=\pi$"),
        ("denominatorMass", OCHRE, "-.", "D", PAPER, r"$\int d\,dt=\pi/N^2$"),
    )
    for series, color, line, marker, fill, label in styles:
        values = by_series[series]
        ax.plot(
            [value[0] for value in values],
            [value[1] for value in values],
            color=color,
            linestyle=line,
            linewidth=1.25,
            marker=marker,
            markersize=3.8,
            markerfacecolor=fill,
            markeredgecolor=color,
            markeredgewidth=0.8,
            label=label,
            zorder=3,
        )
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xlim(0.85, 78)
    ax.set_ylim(4.5e-4, 110)
    ax.set_xticks((1, 2, 4, 8, 16, 32, 64), ("1", "2", "4", "8", "16", "32", "64"))
    ax.set_xlabel("temporal frequency N", fontsize=6.8, color=INK, labelpad=2)
    ax.set_ylabel("exact positive quantity", fontsize=6.8, color=INK)
    ax.grid(which="major", color=LIGHT, linewidth=0.52, alpha=0.72)
    ax.grid(which="minor", visible=False)
    legend = ax.legend(
        loc="upper left",
        frameon=True,
        facecolor=PAPER,
        edgecolor=LIGHT,
        framealpha=0.94,
        title="abstract path on [0,2pi) - not NSE",
        title_fontsize=5.6,
        fontsize=5.7,
        handlelength=2.0,
        labelspacing=0.25,
        borderaxespad=0.2,
    )
    legend.get_title().set_color(OCHRE)


def panel_d(ax: plt.Axes, mode_rows: list[dict[str, str]], metric_rows: list[dict[str, str]]) -> None:
    ax.set_facecolor(PAPER)
    ax.set_axis_off()
    panel_header(ax, "D", "Genuine NSE one-sided initial-jet sharpness")

    # Fourier-mode map in axes coordinates.
    x0, x1 = 0.06, 0.43
    y0, y1 = 0.22, 0.78
    xc, yc = (x0 + x1) / 2, (y0 + y1) / 2
    ax.plot([x0, x1], [yc, yc], transform=ax.transAxes, color=GRAY, lw=0.7, clip_on=False)
    ax.plot([xc, xc], [y0, y1], transform=ax.transAxes, color=GRAY, lw=0.7, clip_on=False)
    ax.text(x1 + 0.01, yc - 0.01, r"$k_1$", transform=ax.transAxes, fontsize=6.0, color=INK)
    ax.text(xc + 0.012, y1 + 0.005, r"$k_2$", transform=ax.transAxes, fontsize=6.0, color=INK)
    for index, row in enumerate(sorted(mode_rows, key=lambda item: (float(item["x"]), float(item["y"])))):
        kx, ky = float(row["x"]), float(row["y"])
        px = x0 + (kx + 1.0) * (x1 - x0) / 2.0
        py = y0 + (ky + 1.0) * (y1 - y0) / 2.0
        open_marker = index in (1, 2)
        ax.plot(
            [px],
            [py],
            transform=ax.transAxes,
            marker="o" if not open_marker else "s",
            markersize=6.0,
            markerfacecolor=PAPER if open_marker else BLUE,
            markeredgecolor=OCHRE if open_marker else INK,
            markeredgewidth=1.0,
            linestyle="none",
        )
        ax.text(
            px,
            py - 0.075 if ky < 0 else py + 0.055,
            f"({int(kx):+d},{int(ky):+d})",
            transform=ax.transAxes,
            fontsize=5.3,
            ha="center",
            va="center",
            color=INK,
            fontfamily="DejaVu Sans Mono",
        )

    metrics = {row["component"]: float(row["value"]) for row in metric_rows}
    box = FancyBboxPatch(
        (0.50, 0.19),
        0.47,
        0.61,
        transform=ax.transAxes,
        boxstyle="round,pad=0.012",
        facecolor="#F0EDE5",
        edgecolor=LIGHT,
        linewidth=0.8,
    )
    ax.add_patch(box)
    ledger = (
        rf"$Y(0)={metrics['Y0']:g}$" "\n"
        rf"$\|F(0)\|_2^2={metrics['F2']:.2f}$" "\n"
        rf"$\|c\|_2^2={metrics['c2']:g}$" "\n"
        rf"$\langle F,c\rangle={metrics['pairing']:.1f}$"
    )
    ax.text(0.535, 0.735, ledger, transform=ax.transAxes, ha="left", va="top", fontsize=6.5, color=INK, linespacing=1.45)
    ax.plot([0.53, 0.94], [0.41, 0.41], transform=ax.transAxes, color=LIGHT, lw=0.8)
    ax.text(
        0.735,
        0.335,
        r"$A_+=\frac{1}{4}=\|F\|_2^2/Y$",
        transform=ax.transAxes,
        ha="center",
        va="center",
        fontsize=8.0,
        fontweight="bold",
        color=BLUE,
    )
    ax.text(0.735, 0.245, "sharpness ratio = 1", transform=ax.transAxes, ha="center", va="center", fontsize=6.0, color=INK, fontfamily="DejaVu Sans Mono")
    ax.text(
        0.735,
        0.045,
        "one-sided initial jet only\nno internal or repeated NSE faces",
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=5.35,
        color=INK,
        bbox=dict(boxstyle="round,pad=0.20", facecolor=PAPER, edgecolor=OCHRE, linewidth=0.75),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    rows = read_rows(args.data)

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.0,
            "axes.unicode_minus": True,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "svg.hashsalt": "r071p-positive-entry-batching",
            "savefig.facecolor": PAPER,
        }
    )
    fig, axes = plt.subplots(
        2,
        2,
        figsize=FIGSIZE_IN,
        facecolor=PAPER,
    )
    fig.subplots_adjust(left=0.078, right=0.982, top=0.935, bottom=0.105, wspace=0.29, hspace=0.42)
    panel_a(axes[0, 0], select(rows, "A", "positiveAtomComparison"))
    panel_b(axes[0, 1], select(rows, "B", "cellLedger"), select(rows, "B", "batchSummary"))
    panel_c(axes[1, 0], [row for row in rows if row["panel"] == "C"])
    panel_d(axes[1, 1], select(rows, "D", "targetMode"), select(rows, "D", "nseMetric"))
    fig.text(
        0.5,
        0.024,
        "Finite R0.71P result: same-time spatial batching closes; distinct entry-time packing remains open.",
        ha="center",
        va="center",
        fontsize=6.1,
        color=INK,
    )

    args.output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_stem.with_suffix(".pdf"), format="pdf")
    fig.savefig(args.output_stem.with_suffix(".svg"), format="svg")
    fig.savefig(args.output_stem.with_suffix(".png"), format="png", dpi=600)
    plt.close(fig)


if __name__ == "__main__":
    main()
