#!/usr/bin/env python3
"""Render the R0.50 charge-character optimization journal figure."""

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
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def add_blossom(figure) -> None:
    center = (0.951, 0.944)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(
            Ellipse(
                (
                    center[0] + 0.011 * math.cos(theta),
                    center[1] + 0.014 * math.sin(theta),
                ),
                width=0.016,
                height=0.028,
                angle=angle - 90,
                facecolor=PALE_GOLD,
                edgecolor=GOLD,
                linewidth=0.45,
                transform=figure.transFigure,
                zorder=20,
            )
        )
    figure.text(
        center[0],
        center[1],
        "·",
        ha="center",
        va="center",
        fontsize=8,
        color=INK,
        zorder=21,
    )


def draw() -> None:
    global_profile = rows("global-threshold-profile.csv")
    local_profile = rows("local-threshold-profile.csv")
    competitors = rows("competitor-gaps.csv")

    c_mid = (0.8024563827 + 0.8024563828) / 2
    r_mid = (0.382619813709565 + 0.382619813709566) / 2

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r050-charge-character-optimization"
        figure = plt.figure(figsize=(178 / 25.4, 112 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            height_ratios=(1.03, 0.97),
            left=0.105,
            right=0.974,
            bottom=0.245,
            top=0.862,
            wspace=0.38,
            hspace=0.66,
        )
        global_axis = figure.add_subplot(grid[0, :])
        local_axis = figure.add_subplot(grid[1, 0])
        gap_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "Threshold radius across the multiplicative charge-character family",
            x=0.105,
            y=0.946,
            ha="left",
            fontsize=8.1,
            color=INK,
        )

        global_x = [float(row["characterDecimal"]) for row in global_profile]
        global_y = [
            float(row["thresholdRadiusDecimal"]) for row in global_profile
        ]
        global_axis.set_title(
            r"(a) Global profile of the active-column threshold $r_*(c)$",
            loc="left",
            pad=5,
        )
        global_axis.plot(global_x, global_y, color=BLUE, linewidth=1.0)
        global_axis.scatter(
            global_x[::5],
            global_y[::5],
            s=7,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.42,
            zorder=4,
        )
        reference_index = min(
            range(len(global_x)),
            key=lambda index: abs(global_x[index] - 0.8),
        )
        global_axis.axvline(
            0.8,
            color=INK,
            linewidth=0.72,
            linestyle=(0, (4, 2)),
        )
        global_axis.scatter(
            [0.8],
            [global_y[reference_index]],
            s=27,
            marker="o",
            facecolor="white",
            edgecolor=INK,
            linewidth=0.78,
            zorder=6,
        )
        global_axis.scatter(
            [c_mid],
            [r_mid],
            s=31,
            marker="D",
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=7,
        )
        global_axis.annotate(
            r"certified $c_*$ interval" + "\n" + r"$0.8024563827<c_*<0.8024563828$",
            xy=(c_mid, r_mid),
            xytext=(0.91, max(global_y) - 0.0065),
            fontsize=4.2,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        global_axis.text(
            0.8,
            min(global_y) + 0.008,
            r"$c=4/5$",
            fontsize=4.2,
            color=INK,
            ha="center",
        )
        global_axis.set_xlim(min(global_x), max(global_x))
        span = max(global_y) - min(global_y)
        global_axis.set_ylim(min(global_y) - 0.06 * span, max(global_y) + 0.10 * span)
        global_axis.set_xlabel(r"charge character $c$")
        global_axis.set_ylabel(r"threshold radius $r_*(c)$")
        global_axis.grid(axis="y", color=GRID, linewidth=0.40)

        local_x = [float(row["characterDecimal"]) for row in local_profile]
        local_y = [
            float(row["gainRelativeToFourFifthsPpmDecimal"])
            for row in local_profile
        ]
        local_axis.set_title(
            r"(b) Local gain relative to $c=4/5$",
            loc="left",
            pad=5,
        )
        local_axis.plot(local_x, local_y, color=BLUE, linewidth=0.95)
        local_axis.scatter(
            local_x[::5],
            local_y[::5],
            s=7,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.42,
            zorder=4,
        )
        local_axis.axhline(0, color=INK, linewidth=0.70, linestyle=(0, (4, 2)))
        local_axis.axvline(0.8, color=INK, linewidth=0.65, linestyle=(0, (4, 2)))
        local_max_index = max(range(len(local_y)), key=local_y.__getitem__)
        local_axis.scatter(
            [c_mid],
            [local_y[local_max_index]],
            s=31,
            marker="D",
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=6,
        )
        local_axis.annotate(
            "> 3.061 ppm",
            xy=(c_mid, local_y[local_max_index]),
            xytext=(0.8053, 1.3),
            fontsize=4.2,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        local_axis.set_xlim(min(local_x), max(local_x))
        local_axis.set_ylim(min(local_y) - 1.5, max(local_y) + 1.25)
        local_axis.set_xlabel(r"charge character $c$")
        local_axis.set_ylabel("threshold-radius gain (ppm)")
        local_axis.text(
            0.79525,
            min(local_y) + 0.25,
            r"ppm $=10^6[r_*(c)/r_*(4/5)-1]$",
            fontsize=4.0,
            color=MUTED,
            va="bottom",
        )
        local_axis.grid(axis="y", color=GRID, linewidth=0.40)

        gap_x = [int(row["rankByGap"]) for row in competitors]
        gap_y = [float(Fraction(row["gapExact"])) for row in competitors]
        gap_axis.set_title(
            "(c) All 243 rectangle competitor gaps",
            loc="left",
            pad=5,
        )
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
            linewidth=0.85,
            zorder=6,
        )
        gap_axis.annotate(
            r"nearest: $s=164$" + "\n" + r"gap $=1.45803\times10^{-4}$",
            xy=(gap_x[0], gap_y[0]),
            xytext=(37, 3.2e-4),
            fontsize=4.2,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        gap_axis.text(
            238,
            0.59,
            "every exact gap > 0",
            fontsize=4.2,
            color=INK,
            ha="right",
        )
        gap_axis.set_xlim(1, 243)
        gap_axis.set_ylim(1e-4, 0.9)
        gap_axis.set_xlabel("competitor rank")
        gap_axis.set_ylabel("exact competitor gap")
        gap_axis.grid(axis="y", which="both", color=GRID, linewidth=0.40)

        figure.text(
            0.105,
            0.171,
            "Display curves: 90-digit evaluation of the exact degree-80 Laurent polynomial.  "
            "Proof: four complete-face Bernstein signs and a 243-competitor exact rectangle sandwich.",
            ha="left",
            va="top",
            fontsize=4.35,
            color=INK,
        )
        figure.text(
            0.105,
            0.123,
            "Scope: reduced canonical edge generating system; optimization only within the multiplicative family "
            r"$\omega_s=c^s$.  No three-dimensional Navier--Stokes regularity claim.",
            ha="left",
            va="top",
            fontsize=4.35,
            color=INK,
        )
        figure.text(
            0.105,
            0.075,
            "Source: R0.50 exact certificate · 33/33 checks · 243 competitors · monitored 138.1 s · no floating-point sign decision",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        add_blossom(figure)

        figure.savefig(PACKAGE / "figure.pdf", metadata={"CreationDate": None})
        figure.savefig(PACKAGE / "figure.svg", metadata={"Date": None})
        normalize_svg(PACKAGE / "figure.svg")
        figure.savefig(PACKAGE / "figure.png", dpi=600)
        plt.close(figure)


if __name__ == "__main__":
    draw()
