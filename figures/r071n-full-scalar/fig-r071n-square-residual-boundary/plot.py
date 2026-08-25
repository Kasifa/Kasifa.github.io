#!/usr/bin/env python3
"""Plot the R0.71N square-residual boundary at double-column journal size."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle


BLUE = "#355C7D"
ORANGE = "#C76B3C"
INK = "#252422"
GRAY = "#77736C"
LIGHT_GRAY = "#D9D5CD"
PALE_BLUE = "#DDE7EF"
PALE_ORANGE = "#F4E1D5"
PAPER = "#FBF9F4"


def load(path: Path):
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    grouped = {}
    for row in rows:
        grouped.setdefault((row["panel"], row["series"]), []).append(row)
    return rows, grouped


def witness_value(grouped, panel, series):
    return {
        row["witness"]: float(row["value"])
        for row in grouped[(panel, series)]
    }


def add_blossom(fig):
    center_x, center_y = 0.955, 0.946
    radius = 0.0058
    offsets = ((-0.006, 0), (0.006, 0), (0, -0.007), (0, 0.007))
    colors = (BLUE, ORANGE, BLUE, ORANGE)
    for (dx, dy), color in zip(offsets, colors, strict=True):
        fig.add_artist(
            Circle(
                (center_x + dx, center_y + dy),
                radius,
                transform=fig.transFigure,
                facecolor="none",
                edgecolor=color,
                linewidth=0.7,
            )
        )


def fmt_raw(value):
    return f"{value / 1000:+.2f}k"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data.csv"))
    parser.add_argument("--output-stem", type=Path, default=Path("figure"))
    args = parser.parse_args()
    _, grouped = load(args.data)

    mpl.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 7.1,
            "axes.titlesize": 7.8,
            "axes.labelsize": 6.8,
            "legend.fontsize": 6.0,
            "xtick.labelsize": 6.0,
            "ytick.labelsize": 6.0,
            "axes.edgecolor": GRAY,
            "axes.labelcolor": INK,
            "xtick.color": INK,
            "ytick.color": INK,
            "text.color": INK,
            "axes.facecolor": PAPER,
            "figure.facecolor": PAPER,
            "savefig.facecolor": PAPER,
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
        }
    )

    fig = plt.figure(figsize=(178 / 25.4, 118 / 25.4))
    fig.set_size_inches(178 / 25.4, 118 / 25.4, forward=False)
    grid = fig.add_gridspec(
        2,
        2,
        left=0.085,
        right=0.975,
        bottom=0.145,
        top=0.865,
        wspace=0.34,
        hspace=0.55,
    )
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[1, 0])
    ax_d = fig.add_subplot(grid[1, 1])

    fig.text(
        0.07,
        0.955,
        "R0.71N  /  full scalar, square cancellation, and the signed second jet",
        fontsize=9.7,
        fontweight="bold",
        color=INK,
    )
    fig.text(
        0.07,
        0.922,
        "Exact fixed-cell algebra - deterministic initial-jet diagnostics - critical co-scaling - no DNS",
        fontsize=6.5,
        color=GRAY,
    )
    add_blossom(fig)

    # Panel A: exact structural flow.
    ax_a.set_axis_off()
    ax_a.set_title(
        "A   Complete scalar: exact cancellation route",
        loc="left",
        fontweight="bold",
        pad=4,
    )
    stages = sorted(
        grouped[("A", "structureFlow")], key=lambda row: float(row["x"])
    )
    labels = (
        ("complete derivative", r"retain $B_t$, $d_t$, and $Y_t$ together"),
        ("square + residual", r"$\mathcal{J}=(\mathcal{P}^{\mathrm{sq}}+\mathfrak{R})/\sqrt{Yd}$"),
        ("local enstrophy", r"$\mathfrak{R}=-\mathcal{P}^{\mathrm{sq}}+\mathcal{K}$: square cancels"),
        ("signed second jet", r"$\mathcal{J}=\mathcal{K}/\sqrt{Yd}$"),
    )
    y_positions = (0.84, 0.62, 0.37, 0.14)
    for index, ((short, formula), row, y_value) in enumerate(
        zip(labels, stages, y_positions, strict=True)
    ):
        edge = BLUE if index in (0, 3) else ORANGE
        face = PALE_BLUE if index in (0, 3) else PALE_ORANGE
        hatch = "///" if index == 2 else None
        ax_a.text(
            0.50,
            y_value,
            f"{short}\n{formula}",
            transform=ax_a.transAxes,
            ha="center",
            va="center",
            fontsize=5.8,
            linespacing=1.22,
            bbox=dict(
                boxstyle="round,pad=0.23",
                facecolor=face,
                edgecolor=edge,
                linewidth=0.85,
                hatch=hatch,
            ),
        )
        if index < 3:
            ax_a.annotate(
                "",
                xy=(0.50, y_positions[index + 1] + 0.075),
                xytext=(0.50, y_value - 0.075),
                xycoords="axes fraction",
                arrowprops=dict(arrowstyle="->", color=INK, lw=0.85),
            )

    # Panel B: raw numerator components.
    p_values = witness_value(grouped, "B", "positiveSquare")
    r_values = witness_value(grouped, "B", "signedResidual")
    totals = witness_value(grouped, "B", "numeratorTotal")
    witnesses = ("seed 49", "seed 5")
    y_centers = np.array([1.0, 0.0])
    height = 0.26
    p_bars = ax_b.barh(
        y_centers + height / 1.7,
        [p_values[name] for name in witnesses],
        height=height,
        color=BLUE,
        edgecolor=INK,
        linewidth=0.45,
        label=r"$\mathcal{P}_Q^{\mathrm{sq}}$",
    )
    r_bars = ax_b.barh(
        y_centers - height / 1.7,
        [r_values[name] for name in witnesses],
        height=height,
        color=PALE_ORANGE,
        edgecolor=ORANGE,
        linewidth=0.8,
        hatch="///",
        label=r"$\mathfrak{R}_Q$",
    )
    for index, name in enumerate(witnesses):
        ax_b.plot(
            totals[name],
            y_centers[index],
            marker="D",
            markersize=4.0,
            markerfacecolor=PAPER,
            markeredgecolor=INK,
            markeredgewidth=0.8,
            zorder=5,
        )
        ax_b.text(
            totals[name],
            y_centers[index] + 0.20,
            f"sum {fmt_raw(totals[name])}",
            va="bottom",
            ha="center",
            fontsize=5.4,
            color=INK,
        )
    for bars, values in (
        (p_bars, [p_values[name] for name in witnesses]),
        (r_bars, [r_values[name] for name in witnesses]),
    ):
        for bar, value in zip(bars, values, strict=True):
            ax_b.text(
                value + (380 if value >= 0 else -380),
                bar.get_y() + bar.get_height() / 2,
                fmt_raw(value),
                va="center",
                ha="left" if value >= 0 else "right",
                fontsize=5.3,
                color=INK,
            )
    ax_b.axvline(0, color=INK, linewidth=0.65)
    ax_b.set_xlim(-28500, 12500)
    ax_b.set_yticks(y_centers, witnesses)
    ax_b.set_xlabel("raw numerator contribution")
    ax_b.grid(axis="x", color=LIGHT_GRAY, linewidth=0.5)
    ax_b.set_title(
        "B   Initial-jet numerator components",
        loc="left",
        fontweight="bold",
    )
    ax_b.legend(frameon=False, loc="lower right", ncol=2, handlelength=1.5)
    ax_b.text(
        0.01,
        0.02,
        "diagnostic, not an interval theorem",
        transform=ax_b.transAxes,
        fontsize=5.6,
        color=GRAY,
    )

    # Panel C: separate z and J scales.
    ax_c.set_axis_off()
    ax_c.set_title(
        "C   Positive z, opposite signs of J",
        loc="left",
        fontweight="bold",
        pad=4,
    )
    ax_z = ax_c.inset_axes([0.05, 0.27, 0.39, 0.55])
    ax_j = ax_c.inset_axes([0.57, 0.27, 0.39, 0.55])
    z_values = witness_value(grouped, "C", "z")
    j_values = witness_value(grouped, "C", "J")
    colors = (BLUE, PALE_ORANGE)
    edges = (INK, ORANGE)
    hatches = (None, "///")
    for axis, values, scale, title, xlim in (
        (ax_z, z_values, 1000.0, r"$10^3 z_Q$", (0, 4.4)),
        (ax_j, j_values, 1.0, r"$\mathcal{J}_Q$", (-8.5, 2.4)),
    ):
        bars = []
        for index, name in enumerate(witnesses):
            bar = axis.barh(
                y_centers[index],
                values[name] * scale,
                height=0.42,
                color=colors[index],
                edgecolor=edges[index],
                linewidth=0.75,
                hatch=hatches[index],
            )[0]
            bars.append(bar)
            plotted = values[name] * scale
            axis.text(
                plotted + (0.12 if title != r"$\mathcal{J}_Q$" else 0.22) * (1 if plotted >= 0 else -1),
                y_centers[index],
                f"{plotted:+.3f}" if title == r"$\mathcal{J}_Q$" else f"{plotted:.3f}",
                va="center",
                ha="left" if plotted >= 0 else "right",
                fontsize=5.6,
            )
        axis.axvline(0, color=INK, linewidth=0.6)
        axis.set_xlim(*xlim)
        axis.set_title(title, fontsize=6.5, fontweight="bold")
        axis.grid(axis="x", color=LIGHT_GRAY, linewidth=0.45)
        axis.tick_params(axis="y", length=0)
    ax_z.set_yticks(y_centers, witnesses)
    ax_j.set_yticks(y_centers, [])
    ax_c.text(
        0.50,
        0.055,
        "deterministic binary64 initial jets; no time stepping",
        transform=ax_c.transAxes,
        ha="center",
        fontsize=5.6,
        color=GRAY,
    )

    # Panel D: scaling exponents and next gate.
    scaling_rows = sorted(
        grouped[("D", "scalingExponent")], key=lambda row: float(row["x"])
    )
    x_values = np.arange(4)
    exponents = np.array([float(row["value"]) for row in scaling_rows])
    labels_d = ("numerator", r"$\sqrt{Yd}$", r"$\mathcal{J}$", "weighted\ncreation")
    colors_d = (BLUE, GRAY, BLUE, INK)
    markers_d = ("o", "s", "o", "D")
    for x_value, exponent, color, marker in zip(
        x_values, exponents, colors_d, markers_d, strict=True
    ):
        ax_d.vlines(x_value, 0, exponent, color=color, linewidth=1.3)
        ax_d.plot(
            x_value,
            exponent,
            marker=marker,
            markersize=5.0,
            markerfacecolor=PAPER if x_value in (1, 3) else color,
            markeredgecolor=color,
            markeredgewidth=0.9,
        )
        ax_d.text(
            x_value,
            exponent + 0.25,
            f"{exponent:.0f}",
            ha="center",
            va="bottom",
            fontsize=6.2,
            fontweight="bold",
        )
    ax_d.axhline(0, color=INK, linewidth=0.6)
    ax_d.set_ylim(-0.55, 6.0)
    ax_d.set_xlim(-0.55, 5.60)
    ax_d.set_xticks(x_values, labels_d)
    ax_d.set_ylabel("NSE scaling exponent")
    ax_d.grid(axis="y", color=LIGHT_GRAY, linewidth=0.5)
    ax_d.set_title(
        "D   Critical exponents; R0.71O face gate",
        loc="left",
        fontweight="bold",
    )
    ax_d.text(1.25, 4.45, r"$5-2=3$", fontsize=6.4, color=BLUE, ha="center")
    ax_d.text(
        0.95,
        3.60,
        r"$-2+1+3-2=0$",
        fontsize=5.8,
        color=INK,
        ha="center",
    )
    ax_d.annotate(
        "R0.71O face gate\nhard vs soft at $d_Q=0$",
        xy=(3.05, 0.05),
        xytext=(4.45, 1.85),
        textcoords="data",
        ha="center",
        va="center",
        fontsize=5.8,
        bbox=dict(
            boxstyle="round,pad=0.28",
            facecolor=PALE_ORANGE,
            edgecolor=ORANGE,
            linewidth=0.8,
            hatch="///",
        ),
        arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9),
    )

    fig.text(
        0.07,
        0.028,
        "Scope: fixed chi_Q and Y,d_Q>0. Witness signs are diagnostic, not interval theorems. No no-go, continuation, regularity, or singularity claim.",
        fontsize=5.9,
        color=GRAY,
    )

    for extension in ("pdf", "svg", "png"):
        fig.savefig(
            args.output_stem.with_suffix(f".{extension}"),
            dpi=600 if extension == "png" else None,
        )
    svg_path = args.output_stem.with_suffix(".svg")
    svg_text = svg_path.read_text(encoding="utf-8")
    svg_text = re.sub(r'width="[^"]+"', 'width="178mm"', svg_text, count=1)
    svg_text = re.sub(r'height="[^"]+"', 'height="118mm"', svg_text, count=1)
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
