#!/usr/bin/env python3
"""Render the R0.51 affine charge-weight journal figure."""

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
    switch = rows("constraint-switch.csv")
    gains = rows("incremental-gains.csv")
    competitors = rows("competitor-gaps.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r051-affine-charge-weight"
        figure = plt.figure(figsize=(178 / 25.4, 112 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            height_ratios=(1.03, 0.97),
            left=0.105,
            right=0.974,
            bottom=0.245,
            top=0.862,
            wspace=0.40,
            hspace=0.68,
        )
        switch_axis = figure.add_subplot(grid[0, :])
        gain_axis = figure.add_subplot(grid[1, 0])
        gap_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "Threshold and constraint geometry for one affine charge weight",
            x=0.105,
            y=0.946,
            ha="left",
            fontsize=8.1,
            color=INK,
        )

        switch_x = [float(row["lambdaDecimal"]) for row in switch]
        switch_y = [float(row["activeMinusZeroPpmDecimal"]) for row in switch]
        switch_axis.set_title(
            r"(a) Conservative $s=162$ minus $s=0$ root-box gap",
            loc="left",
            pad=5,
        )
        switch_axis.plot(switch_x, switch_y, color=BLUE, linewidth=1.0)
        switch_axis.scatter(
            switch_x[::5],
            switch_y[::5],
            s=7,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.42,
            zorder=4,
        )
        switch_axis.axhline(0, color=INK, linewidth=0.72, linestyle=(0, (4, 2)))
        selected_index = next(
            index
            for index, row in enumerate(switch)
            if row["isCertifiedChoice"] == "true"
        )
        switch_axis.scatter(
            [switch_x[selected_index]],
            [switch_y[selected_index]],
            marker="D",
            s=31,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=6,
        )
        crossing_index = next(
            index
            for index in range(len(switch_y) - 1)
            if switch_y[index] > 0 > switch_y[index + 1]
        )
        x0, x1 = switch_x[crossing_index : crossing_index + 2]
        y0, y1 = switch_y[crossing_index : crossing_index + 2]
        crossing = x0 - y0 * (x1 - x0) / (y1 - y0)
        switch_axis.scatter(
            [crossing],
            [0],
            s=25,
            facecolor="white",
            edgecolor=INK,
            linewidth=0.75,
            zorder=6,
        )
        switch_axis.annotate(
            r"certified $lambda=0.7653$" + "\n" + "gap = 17.808 ppm",
            xy=(switch_x[selected_index], switch_y[selected_index]),
            xytext=(0.765225, 54),
            fontsize=4.2,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        switch_axis.annotate(
            r"sampled switch $lambda\approx$" + f"{crossing:.7f}",
            xy=(crossing, 0),
            xytext=(0.76536, -49),
            fontsize=4.2,
            color=INK,
            ha="center",
            arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 0.48},
        )
        switch_axis.set_xlim(min(switch_x), max(switch_x))
        switch_axis.set_ylim(-90, 90)
        switch_axis.set_xlabel(r"affine parameter $\lambda$ at fixed $c=0.79756$")
        switch_axis.set_ylabel(r"$10^6(B_{162}^{L}-Z_0^{U})$")
        switch_axis.grid(axis="y", color=GRID, linewidth=0.40)

        gain_labels = [row["label"].replace(" / ", "/") for row in gains]
        gain_y = [float(row["strictGainPpmDecimal"]) for row in gains]
        gain_x = list(range(1, len(gains) + 1))
        gain_axis.set_title(
            "(b) Strict incremental threshold gains",
            loc="left",
            pad=5,
        )
        gain_axis.vlines(gain_x, 1, gain_y, color=BLUE, linewidth=1.0)
        gain_axis.scatter(
            gain_x,
            gain_y,
            s=27,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.75,
            zorder=5,
        )
        gain_axis.scatter(
            [gain_x[-1]],
            [gain_y[-1]],
            marker="D",
            s=31,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=6,
        )
        for x, y in zip(gain_x, gain_y, strict=True):
            gain_axis.text(
                x,
                y * 1.28,
                f"{y:.3f}",
                fontsize=4.0,
                color=GOLD if x == gain_x[-1] else INK,
                ha="center",
                va="bottom",
            )
        gain_axis.set_yscale("log")
        gain_axis.set_xlim(0.55, 3.45)
        gain_axis.set_ylim(1, max(gain_y) * 2.3)
        gain_axis.set_xticks(gain_x, gain_labels)
        gain_axis.set_ylabel("strict radius gain (ppm, log scale)")
        gain_axis.grid(axis="y", which="both", color=GRID, linewidth=0.40)

        gap_x = [int(row["rankByGap"]) for row in competitors]
        gap_y = [float(Fraction(row["gapExact"])) for row in competitors]
        gap_axis.set_title(
            "(c) All 243 root-box competitor gaps",
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
            r"nearest: $s=0$" + "\n" + r"gap $=1.78082\times10^{-5}$",
            xy=(gap_x[0], gap_y[0]),
            xytext=(37, 7.0e-5),
            fontsize=4.2,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        gap_axis.text(
            238,
            0.53,
            "every exact gap > 0",
            fontsize=4.2,
            color=INK,
            ha="right",
        )
        gap_axis.set_xlim(1, 243)
        gap_axis.set_ylim(1e-5, 0.9)
        gap_axis.set_xlabel("competitor rank")
        gap_axis.set_ylabel("exact competitor gap")
        gap_axis.grid(axis="y", which="both", color=GRID, linewidth=0.40)

        figure.text(
            0.105,
            0.171,
            "Display: 126 exact rational switch samples, three exact inter-stage lower gains, and all 243 exact competitor gaps.  "
            "Proof: GMP Sturm, convex endpoints, affine envelope, and parity/Bernstein signs.",
            ha="left",
            va="top",
            fontsize=4.25,
            color=INK,
        )
        figure.text(
            0.105,
            0.123,
            r"Scope: fixed $\omega_s=c^s(1+\lambda|s|)$ in the reduced canonical edge system.  "
            "No global affine-family optimum and no three-dimensional Navier--Stokes regularity claim.",
            ha="left",
            va="top",
            fontsize=4.25,
            color=INK,
        )
        figure.text(
            0.105,
            0.075,
            "Source: R0.51 exact certificate · 26/26 checks · 243 competitors · monitored 127.2 s · no floating-point sign decision",
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
