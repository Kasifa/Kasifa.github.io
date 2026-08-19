#!/usr/bin/env python3
"""Render the R0.48 exact threshold-root journal figure."""

from __future__ import annotations

import csv
from fractions import Fraction
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


PACKAGE = Path(__file__).resolve().parent
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
LIGHT = "#aaa398"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_BLUE = "#dce6ec"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def add_blossom(figure) -> None:
    center = (0.948, 0.947)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(
            Ellipse(
                (
                    center[0] + 0.012 * math.cos(theta),
                    center[1] + 0.015 * math.sin(theta),
                ),
                width=0.017,
                height=0.030,
                angle=angle - 90,
                facecolor=PALE_GOLD,
                edgecolor=GOLD,
                linewidth=0.45,
                transform=figure.transFigure,
                zorder=20,
            )
        )
    figure.text(
        center[0], center[1], "·", ha="center", va="center", fontsize=8,
        color=INK, zorder=21
    )


def draw() -> None:
    curve = rows("threshold-curve.csv")
    root = rows("root-endpoints.csv")
    competitors = rows("competitor-gaps.csv")
    leaders = rows("sandwich-leaders.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r048-threshold-root"
        figure = plt.figure(figsize=(178 / 25.4, 142 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(1.04, 0.96),
            height_ratios=(1.0, 1.0),
            left=0.145,
            right=0.974,
            bottom=0.262,
            top=0.883,
            wspace=0.43,
            hspace=0.62,
        )
        crossing_axis = figure.add_subplot(grid[0, 0])
        root_axis = figure.add_subplot(grid[0, 1])
        gap_axis = figure.add_subplot(grid[1, 0])
        leader_axis = figure.add_subplot(grid[1, 1])

        crossing_axis.set_title(
            r"(a) Active-column crossing on $[0.376932,0.376933]$",
            loc="left",
            pad=5,
        )
        crossing_x = [float(Fraction(row["windowPositionExact"])) for row in curve]
        crossing_y = [float(row["activeMarginPpmDecimal"]) for row in curve]
        crossing_axis.plot(crossing_x, crossing_y, color=BLUE, linewidth=1.05)
        crossing_axis.scatter(
            crossing_x[::5],
            crossing_y[::5],
            s=7,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.45,
            zorder=4,
        )
        root_position = 0.4992905273405
        crossing_axis.axhline(0, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        crossing_axis.axvline(
            root_position, color=GOLD, linewidth=0.8, linestyle=(0, (2, 1.8))
        )
        crossing_axis.scatter(
            [root_position],
            [0],
            marker="D",
            s=31,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=6,
        )
        crossing_axis.annotate(
            r"$r_*\approx0.3769324992905273405$",
            xy=(root_position, 0),
            xytext=(0.08, 2.08),
            fontsize=4.25,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        crossing_axis.text(
            0.015, crossing_y[0] + 0.20, f"{crossing_y[0]:+.4f} ppm",
            fontsize=4.20, color=BLUE
        )
        crossing_axis.text(
            0.985, crossing_y[-1] - 0.22, f"{crossing_y[-1]:+.4f} ppm",
            fontsize=4.20, color=BLUE, ha="right", va="top"
        )
        crossing_axis.set_xlim(0, 1)
        crossing_axis.set_ylim(-3.2, 3.2)
        crossing_axis.set_xlabel(r"window position $10^6(r-0.376932)$")
        crossing_axis.set_ylabel(r"$10^6[C_r(81,162)-1]$ (ppm)")
        crossing_axis.grid(axis="y", color=GRID, linewidth=0.40)

        root_axis.set_title(
            r"(b) Exact width-$10^{-18}$ root bracket",
            loc="left",
            pad=5,
        )
        root_x = [int(row["normalizedBracketPosition"]) for row in root]
        root_y = [float(row["polynomialValueAttoDecimal"]) for row in root]
        root_axis.axhline(0, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        for index, (x_value, y_value) in enumerate(zip(root_x, root_y, strict=True)):
            color = BLUE if y_value < 0 else GOLD
            marker = "o" if y_value < 0 else "D"
            root_axis.vlines(x_value, 0, y_value, color=color, linewidth=0.9)
            root_axis.scatter(
                [x_value],
                [y_value],
                s=34,
                marker=marker,
                facecolor="white" if index == 0 else PALE_GOLD,
                edgecolor=color,
                linewidth=0.9,
                zorder=5,
            )
            root_axis.text(
                x_value,
                y_value + (0.28 if y_value >= 0 else -0.32),
                f"{y_value:+.4f}",
                fontsize=4.35,
                ha="center",
                va="bottom" if y_value >= 0 else "top",
                color=color,
            )
            root_axis.text(
                x_value,
                2.12,
                f"V={root[index]['sturmVariations']}",
                fontsize=4.45,
                ha="center",
                color=INK,
            )
        root_axis.text(
            0.50,
            1.38,
            "40 - 39 = 1 root\n81 exact Sturm polynomials; 0 endpoint zeros",
            ha="center",
            va="center",
            fontsize=4.25,
            color=INK,
        )
        root_axis.set_xlim(-0.30, 1.30)
        root_axis.set_ylim(-5.65, 2.55)
        root_axis.set_xticks([0, 1])
        root_axis.set_xticklabels(
            [
                r"$r_L$" + "\n...527340",
                r"$r_U$" + "\n...527341",
            ]
        )
        root_axis.set_ylabel(r"$10^{18}P(r)$")
        root_axis.grid(axis="y", color=GRID, linewidth=0.40)

        gap_axis.set_title(
            "(c) All 243 full-window competitor gaps",
            loc="left",
            pad=5,
        )
        gap_x = [int(row["rankByGap"]) for row in competitors]
        gap_y = [float(Fraction(row["gapBelowActiveAtWindowLeftExact"])) for row in competitors]
        gap_axis.semilogy(gap_x, gap_y, color=BLUE, linewidth=0.85)
        gap_axis.scatter(
            gap_x[::4],
            gap_y[::4],
            s=6,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.40,
            zorder=4,
        )
        gap_axis.scatter(
            [gap_x[0]],
            [gap_y[0]],
            marker="D",
            s=31,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.9,
            zorder=6,
        )
        gap_axis.annotate(
            r"nearest: $s=164$" + "\n" + r"gap $=9.99338\times10^{-5}$",
            xy=(gap_x[0], gap_y[0]),
            xytext=(37, 2.1e-4),
            fontsize=4.25,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        gap_axis.text(
            238,
            0.64,
            "every exact gap > 0",
            fontsize=4.30,
            color=INK,
            ha="right",
        )
        gap_axis.set_xlim(1, 243)
        gap_axis.set_ylim(7e-5, 1.1)
        gap_axis.set_xlabel("competitor rank by increasing exact gap")
        gap_axis.set_ylabel("exact sandwich gap")
        gap_axis.grid(axis="y", which="major", color=GRID, linewidth=0.40)

        leader_axis.set_title(
            "(d) Nearest monotone-sandwich bounds",
            loc="left",
            pad=5,
        )
        y_positions = list(reversed(range(len(leaders))))
        for row, y_value in zip(leaders, y_positions, strict=True):
            distance = float(row["distanceBelowOnePpmDecimal"])
            active = row["isActive"] == "true"
            color = GOLD if active else BLUE
            marker = "D" if active else "o"
            leader_axis.hlines(y_value, 0, distance, color=color, linewidth=0.88)
            leader_axis.scatter(
                [distance],
                [y_value],
                s=28,
                marker=marker,
                facecolor=PALE_GOLD if active else "white",
                edgecolor=color,
                linewidth=0.85,
                zorder=5,
            )
            leader_axis.text(
                distance + 15,
                y_value,
                f"{distance:.1f}",
                fontsize=4.05,
                va="center",
                color=color,
            )
        leader_axis.axvline(0, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        leader_axis.text(8, 7.35, "threshold 1", fontsize=4.15, color=INK)
        leader_axis.set_xlim(0, 790)
        leader_axis.set_ylim(-0.45, 7.55)
        leader_axis.set_yticks(y_positions)
        leader_axis.set_yticklabels(
            [
                r"active $s=162$ · L",
                r"$s=164$ · R",
                r"$s=166$ · R",
                r"$s=168$ · R",
                r"$s=170$ · R",
                r"$s=172$ · R",
                r"$s=174$ · R",
                r"$s=176$ · R",
            ]
        )
        leader_axis.set_xlabel(r"distance below one, $10^6(1-B)$ (ppm)")
        leader_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (crossing_axis, root_axis, gap_axis, leader_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.48 exact threshold-root diagnostics",
            x=0.145,
            y=0.956,
            ha="left",
            fontsize=10.0,
            fontweight="bold",
            color=INK,
        )
        figure.text(
            0.145,
            0.918,
            r"Exact GMP arithmetic; unique root of $P(r)=C_r(81,162)-1$ and full-window dominance in the current norm",
            ha="left",
            fontsize=5.15,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.184,
            r"Root: $0.376932499290527340<r_*<0.376932499290527341$; $P'(r)>0$ for every $r>0$.",
            ha="left",
            fontsize=4.80,
            color=INK,
        )
        figure.text(
            0.145,
            0.151,
            r"Dominance: 238 other fixed charges + 1 inactive endpoint + 4 remaining sectors = 243 exact competitors.",
            ha="left",
            fontsize=4.72,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.118,
            r"Threshold: the induced norm is $<1$, $=1$, and $>1$ below, at, and above $r_*$ within the displayed window.",
            ha="left",
            fontsize=4.72,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.085,
            "Scope: reduced canonical edge system and one weighted-l1 norm; this is not a PDE regularity or singularity theorem.",
            ha="left",
            fontsize=4.62,
            color=MUTED,
        )
        figure.text(
            0.984,
            0.038,
            "R0.48 | exact rational certificate | 2026-08-19",
            ha="right",
            fontsize=4.65,
            color=LIGHT,
        )
        add_blossom(figure)

        figure.savefig(PACKAGE / "figure.pdf")
        figure.savefig(PACKAGE / "figure.svg")
        figure.savefig(PACKAGE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(PACKAGE / "figure.svg")


if __name__ == "__main__":
    draw()
