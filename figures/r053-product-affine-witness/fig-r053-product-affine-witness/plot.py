#!/usr/bin/env python3
"""Render the R0.53 product-affine witness journal figure."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    path.write_text("\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")


def add_blossom(figure) -> None:
    center = (0.951, 0.944)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(Ellipse((center[0] + 0.011 * math.cos(theta), center[1] + 0.014 * math.sin(theta)), width=0.016, height=0.028, angle=angle - 90, facecolor=PALE_GOLD, edgecolor=GOLD, linewidth=0.45, transform=figure.transFigure, zorder=20))
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK, zorder=21)


def draw() -> None:
    profile = rows("threshold-profile.csv")
    gains = rows("strict-gains.csv")
    competitors = rows("competitor-gaps.csv")
    x = [float(row["radiusDecimal"]) for row in profile]
    zero = [float(row["zeroDeficitPpmDecimal"]) for row in profile]
    active = [float(row["active162DeficitPpmDecimal"]) for row in profile]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r053-product-affine-witness"
        figure = plt.figure(figsize=(178 / 25.4, 112 / 25.4), layout="none")
        grid = figure.add_gridspec(2, 2, left=0.105, right=0.974, bottom=0.295, top=0.858, wspace=0.38, hspace=0.69)
        threshold_axis = figure.add_subplot(grid[0, 0])
        gain_axis = figure.add_subplot(grid[0, 1])
        gap_axis = figure.add_subplot(grid[1, :])
        figure.suptitle(r"A rational product-affine weight beyond the complete affine family", x=0.105, y=0.946, ha="left", fontsize=8.1, color=INK)

        threshold_axis.set_title("(a) Which column reaches one first?", loc="left", pad=5)
        threshold_axis.plot(x, zero, color=GOLD, linewidth=1.0, marker="D", markersize=2.2, markevery=12, label=r"zero charge $s=0$")
        threshold_axis.plot(x, active, color=BLUE, linewidth=0.9, linestyle=(0, (4, 2)), marker="o", markerfacecolor="white", markeredgewidth=0.45, markersize=2.2, markevery=12, label=r"old active $(j,s)=(81,162)$")
        threshold_axis.axhline(0, color=INK, linewidth=0.58)
        threshold_axis.axvspan(0.382628602237879637, 0.382628602237879638, color=PALE_GOLD, alpha=0.95, linewidth=0)
        threshold_axis.axvline(0.38262447184859883148, color=MUTED, linewidth=0.62, linestyle=(0, (2, 2)))
        threshold_axis.annotate("R0.52 global upper", xy=(0.3826244718485988, zero[10]), xytext=(0.38262505, max(zero) * 0.72), fontsize=4.0, color=MUTED, arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.45})
        threshold_axis.annotate(r"$r_*\in[\,0.382628602237879637,$" + "\n" + r"$0.382628602237879638\,]$", xy=(0.3826286022378796375, 0), xytext=(0.3826262, min(zero) * 0.72), fontsize=3.9, color=GOLD, arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.48})
        threshold_axis.set_xlim(min(x), max(x))
        threshold_axis.set_xlabel(r"radius $r$")
        threshold_axis.set_ylabel(r"$10^6(1-\mathrm{column})$ [ppm]")
        threshold_axis.ticklabel_format(axis="x", style="plain", useOffset=True)
        threshold_axis.legend(loc="upper right", frameon=False, fontsize=4.0)
        threshold_axis.grid(axis="y", color=GRID, linewidth=0.36)

        gain_axis.set_title("(b) Strict gains over the affine optimum", loc="left", pad=5)
        positions = [1, 2]
        values = [float(row["gainPpmDecimal"]) for row in gains]
        gain_axis.vlines(positions, 0, values, color=[BLUE, GOLD], linewidth=1.25)
        gain_axis.scatter([1], [values[0]], s=31, marker="o", facecolor="white", edgecolor=BLUE, linewidth=0.8, zorder=5)
        gain_axis.scatter([2], [values[1]], s=34, marker="D", facecolor=PALE_GOLD, edgecolor=GOLD, linewidth=0.85, zorder=5)
        for position, value in zip(positions, values, strict=True):
            gain_axis.text(position, value + 0.20, f"> {value:.4f}", ha="center", va="bottom", fontsize=4.4, color=INK)
        gain_axis.set_xlim(0.5, 2.5)
        gain_axis.set_ylim(0, 12)
        gain_axis.set_xticks(positions, ["fixed\nrestart", "sharp\nthreshold"])
        gain_axis.set_ylabel("strict radius gain [ppm]")
        gain_axis.text(0.04, 0.94, r"baseline: complete $c^s(1+\lambda|s|)$ family", transform=gain_axis.transAxes, va="top", fontsize=4.0, color=MUTED)
        gain_axis.grid(axis="y", color=GRID, linewidth=0.36)

        ranks = [int(row["rankByGap"]) for row in competitors]
        gaps = [float(row["gapDecimal"]) for row in competitors]
        gap_axis.set_title("(c) Every one of the 281 inactive all-order records remains strict", loc="left", pad=5)
        gap_axis.semilogy(ranks, gaps, color=BLUE, linewidth=0.85)
        gap_axis.scatter(ranks[::5], gaps[::5], s=6, facecolor="white", edgecolor=BLUE, linewidth=0.4, zorder=4)
        gap_axis.scatter([ranks[0]], [gaps[0]], marker="D", s=31, facecolor=PALE_GOLD, edgecolor=GOLD, linewidth=0.85, zorder=6)
        tail_index = next(i for i, row in enumerate(competitors) if row["label"] == "s>=280")
        gap_axis.scatter([ranks[tail_index]], [gaps[tail_index]], marker="s", s=22, facecolor="white", edgecolor=INK, linewidth=0.75, zorder=6)
        gap_axis.annotate(r"nearest: $(j,s)=(81,162)$" + "\n" + r"gap $>1.488345\times10^{-6}$", xy=(ranks[0], gaps[0]), xytext=(38, 7.0e-6), fontsize=4.1, color=GOLD, arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.5})
        gap_axis.annotate(r"all $s\geq280$", xy=(ranks[tail_index], gaps[tail_index]), xytext=(ranks[tail_index] - 55, gaps[tail_index] * 4), fontsize=4.0, color=INK, arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 0.45})
        gap_axis.set_xlim(1, 281)
        gap_axis.set_ylim(1e-6, 1.0)
        gap_axis.set_xlabel("competitor rank")
        gap_axis.set_ylabel("gap below zero equality (log)")
        gap_axis.grid(axis="y", which="both", color=GRID, linewidth=0.38)

        figure.text(0.105, 0.171, r"Display: 121 exact rational threshold samples, two exact gain factors, and all 281 certified competitor gaps.  Proof: GMP Sturm isolation, fixed-charge endpoints, special-sector arguments, and parity/Bernstein tail bounds.", ha="left", va="top", fontsize=4.25, color=INK)
        figure.text(0.105, 0.123, r"Scope: one fixed rational product-affine weight in the reduced degree-80 edge system.  This disproves degeneration to the complete single-affine boundary; it does not globally optimize the product-affine family or settle three-dimensional Navier--Stokes regularity.", ha="left", va="top", fontsize=4.25, color=INK)
        figure.text(0.105, 0.075, "Source: R0.53 exact certificate · 28/28 checks · 281 inactive records · monitored 143.4 s · no floating-point sign decision", ha="left", fontsize=4.25, color=MUTED)
        add_blossom(figure)
        figure.savefig(HERE / "figure.pdf", metadata={"CreationDate": None})
        figure.savefig(HERE / "figure.svg", metadata={"Date": None})
        normalize_svg(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)


if __name__ == "__main__":
    draw()
