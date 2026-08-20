#!/usr/bin/env python3
"""Render Figure R0.65-1 at double-column journal size."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.ticker import FixedFormatter, FixedLocator


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
PALE_RUST = "#f2e5df"
GRID = "#d5cec0"


def rows() -> list[dict[str, str]]:
    with (HERE / "cycle-enclosures.csv").open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def blossom(figure) -> None:
    center = (0.946, 0.934)
    for dx, dy, angle in ((0.0, 0.010, 0), (0.0, -0.010, 0), (0.008, 0.0, 90), (-0.008, 0.0, 90)):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy),
                0.010,
                0.018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=0.35,
            )
        )


def draw() -> None:
    data = rows()
    r_values = [int(row["r"]) for row in data]
    normalized = [float(row["S4OverMCenter"]) for row in data]
    ratio_r = r_values[1:]
    ratios = [float(row["absoluteBlockRatioCenter"]) for row in data[1:]]
    ratio_low = [float(row["absoluteBlockRatioLower"]) for row in data[1:]]
    ratio_high = [float(row["absoluteBlockRatioUpper"]) for row in data[1:]]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r065-weighted-cycle"
        figure = plt.figure(figsize=(178 / 25.4, 96 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            2,
            left=0.070,
            right=0.955,
            bottom=0.205,
            top=0.765,
            width_ratios=(1.08, 1.0),
            wspace=0.31,
        )
        signed_axis = figure.add_subplot(grid[0, 0])
        ratio_axis = figure.add_subplot(grid[0, 1])

        figure.suptitle(
            "Heat-weighted periodic target through 24 four-bit cycles",
            x=0.070,
            y=0.947,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.070,
            0.885,
            r"Exact bivariate moments to degree 96  ·  order-48 rational simplex enclosure  ·  $L=1$, $M=16^r$",
            ha="left",
            fontsize=3.9,
            color=MUTED,
        )
        blossom(figure)

        signed_axis.set_title("(a) Signed normalized quartic coefficient", loc="left", pad=5)
        signed_axis.plot(r_values, normalized, color=MUTED, linewidth=0.65, zorder=1)
        positive_r = [r for r, value in zip(r_values, normalized) if value > 0]
        positive_y = [value for value in normalized if value > 0]
        negative_r = [r for r, value in zip(r_values, normalized) if value < 0]
        negative_y = [value for value in normalized if value < 0]
        signed_axis.scatter(
            positive_r,
            positive_y,
            s=13,
            facecolors="white",
            edgecolors=BLUE,
            marker="o",
            linewidths=0.7,
            label="certified positive",
            zorder=3,
        )
        signed_axis.scatter(
            negative_r,
            negative_y,
            s=12,
            facecolors=RUST,
            edgecolors=RUST,
            marker="s",
            linewidths=0.5,
            label="certified negative",
            zorder=3,
        )
        signed_axis.axhline(0, color=INK, linewidth=0.65)
        signed_axis.set_yscale("symlog", linthresh=0.004, linscale=0.7, base=10)
        signed_axis.set_xlim(0.5, 24.5)
        signed_axis.set_ylim(-1.6, 0.035)
        signed_axis.set_xlabel(r"cycle count $r$")
        signed_axis.set_ylabel(r"$S_r/M_r$ (symmetric-log scale)")
        signed_axis.grid(color=GRID, linewidth=0.3)
        signed_axis.legend(loc="lower left", frameon=False, fontsize=3.35, handletextpad=0.5)
        signed_axis.annotate(
            "first sign change\nr = 14",
            xy=(14, normalized[13]),
            xytext=(10.8, -0.055),
            fontsize=3.55,
            color=RUST,
            ha="center",
            arrowprops={"arrowstyle": "-", "color": RUST, "linewidth": 0.55},
        )
        signed_axis.text(
            23.8,
            normalized[-1],
            r"$|S_{24}|/M_{24}=1.1786\ldots$",
            ha="right",
            va="bottom",
            fontsize=3.45,
            color=RUST,
        )

        ratio_axis.set_title("(b) Absolute growth per four-level block", loc="left", pad=5)
        ratio_axis.axvspan(14.5, 24.5, color=PALE_RUST, alpha=0.8, linewidth=0)
        ratio_axis.plot(ratio_r, ratios, color=BLUE, linewidth=0.75, zorder=2)
        ratio_axis.vlines(ratio_r, ratio_low, ratio_high, color=BLUE, linewidth=0.55, zorder=2)
        ratio_axis.scatter(
            ratio_r,
            ratios,
            s=12,
            facecolors="white",
            edgecolors=BLUE,
            marker="o",
            linewidths=0.65,
            zorder=3,
        )
        ratio_axis.axhline(16, color=INK, linewidth=0.7, linestyle=(0, (3, 2)))
        ratio_axis.axhline(25.151589334101537, color=RUST, linewidth=0.7, linestyle=(0, (5, 2)))
        ratio_axis.set_yscale("log")
        ratio_axis.set_xlim(1.5, 24.5)
        ratio_axis.set_ylim(5, 110)
        ratio_axis.set_xlabel(r"destination cycle $r$")
        ratio_axis.set_ylabel(r"$|S_r|/|S_{r-1}|$ (log scale)")
        ratio_axis.yaxis.set_major_locator(FixedLocator([8, 16, 25.151589334101537, 50, 100]))
        ratio_axis.yaxis.set_major_formatter(FixedFormatter(["8", "16", "25.15", "50", "100"]))
        ratio_axis.grid(color=GRID, linewidth=0.3, which="major")
        ratio_axis.text(2.0, 16.7, "extensive threshold 16", fontsize=3.25, color=INK)
        ratio_axis.text(2.0, 26.4, r"zero-time $\lambda=25.151589\ldots$", fontsize=3.25, color=RUST)
        ratio_axis.text(
            19.5,
            73,
            "10 consecutive certified\nblocks above 16",
            ha="center",
            va="center",
            fontsize=3.55,
            color=RUST,
        )
        ratio_axis.text(
            24.0,
            ratios[-1] * 0.92,
            "25.2923…",
            ha="right",
            va="top",
            fontsize=3.45,
            color=BLUE,
        )

        figure.text(
            0.070,
            0.066,
            r"Finite inference boundary: every point is rigorously enclosed, but 24 scales do not prove an asymptotic limit or unbounded $|S_r|/M_r$.",
            ha="left",
            va="top",
            fontsize=3.7,
            color=MUTED,
        )
        figure.savefig(HERE / "figure.pdf")
        figure.savefig(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")


if __name__ == "__main__":
    draw()
