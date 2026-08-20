#!/usr/bin/env python3
"""Render Figure R0.62-1 at double-column journal size."""

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
RUST = "#8b4d43"
GOLD = "#a16f27"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def add_blossom(figure) -> None:
    center = (0.955, 0.946)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(
            Ellipse(
                (center[0] + 0.0105 * math.cos(theta), center[1] + 0.013 * math.sin(theta)),
                width=0.015,
                height=0.026,
                angle=angle - 90,
                facecolor=PALE_GOLD,
                edgecolor=GOLD,
                linewidth=0.45,
                transform=figure.transFigure,
                zorder=20,
            )
        )
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK)


def draw() -> None:
    profiles = rows("weighted-target-profiles.csv")
    scales = rows("scale-comparison.csv")
    styles = {
        256: (BLUE, "-", "o", 0.42),
        512: (BLUE, (0, (5, 2)), "s", 0.58),
        1024: (BLUE, (0, (1.5, 1.5)), "^", 0.76),
        2048: (BLUE, (0, (5, 2, 1, 2)), "D", 1.0),
    }

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r062-quartic-correlation"
        figure = plt.figure(figsize=(178 / 25.4, 112 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.078,
            right=0.963,
            bottom=0.235,
            top=0.79,
            height_ratios=(1.2, 0.82),
            hspace=0.62,
            wspace=0.31,
        )
        profile_axis = figure.add_subplot(grid[0, :])
        weighted_axis = figure.add_subplot(grid[1, 0])
        unweighted_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "Heat-weighted quartic profiles and the unweighted correlation gap",
            x=0.078,
            y=0.948,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.078,
            0.892,
            r"All-index theorem: $|R_{L,M,m}|\leq 7.8343\,(m/M)^2\sqrt{M}$  ·  "
            "finite extension: 4,042 triples and 27.082 billion ordered paths",
            ha="left",
            va="center",
            fontsize=3.9,
            color=MUTED,
        )

        profile_axis.set_title("(a) Complete heat-weighted target profiles, L = 1", loc="left", pad=4)
        for outputs, (color, linestyle, marker, alpha) in styles.items():
            selected = [row for row in profiles if int(row["M"]) == outputs]
            mark_every = max(1, outputs // 14)
            profile_axis.semilogy(
                [float(row["targetFraction"]) for row in selected],
                [float(row["normalizedSignedRatio"]) for row in selected],
                color=color,
                alpha=alpha,
                linestyle=linestyle,
                linewidth=0.75,
                marker=marker,
                markerfacecolor="white",
                markeredgewidth=0.4,
                markersize=1.9,
                markevery=mark_every,
                label=rf"$M={outputs}$",
            )
        profile_axis.set_xlim(0, 1.01)
        profile_axis.set_ylim(1e-10, 2e-3)
        profile_axis.set_xlabel(r"target position $m/M$")
        profile_axis.set_ylabel(r"normalized ratio $R_{1,M,m}$ (log scale)")
        profile_axis.grid(color=GRID, linewidth=0.3, which="major")
        profile_axis.grid(color=GRID, linewidth=0.2, which="minor", alpha=0.42)
        profile_axis.legend(loc="upper left", ncol=4, frameon=False, fontsize=3.55)
        profile_axis.text(
            0.995,
            1.8e-10,
            "3,840/3,840 displayed values are positive (finite evidence)",
            ha="right",
            va="bottom",
            fontsize=3.45,
            color=MUTED,
        )

        weighted = [row for row in scales if row["weightedMaximumRatio"]]
        weighted_axis.set_title("(b) Maximum heat-weighted ratio", loc="left", pad=4)
        weighted_axis.plot(
            [int(row["M"]) for row in weighted],
            [1e3 * float(row["weightedMaximumRatio"]) for row in weighted],
            color=BLUE,
            linewidth=0.9,
            marker="o",
            markerfacecolor="white",
            markeredgewidth=0.55,
            markersize=2.8,
        )
        weighted_axis.axhline(1.3286562612066827, color=GOLD, linestyle=(0, (4, 2)), linewidth=0.7)
        weighted_axis.text(270, 1.36, "overall finite max", fontsize=3.25, color=GOLD)
        weighted_axis.set_xscale("log", base=2)
        weighted_axis.set_xlim(220, 2400)
        weighted_axis.set_ylim(0.85, 1.42)
        weighted_axis.set_xlabel(r"output count $M$ (log$_2$ scale)")
        weighted_axis.set_ylabel(r"$10^3\max_m R_{1,M,m}$")
        weighted_axis.grid(color=GRID, linewidth=0.3)

        unweighted_axis.set_title("(c) Ordinary outer correlation", loc="left", pad=4)
        unweighted_axis.plot(
            [int(row["M"]) for row in scales],
            [float(row["unweightedOuterMaximumOverM"]) for row in scales],
            color=RUST,
            linewidth=0.9,
            linestyle="-",
            marker="s",
            markerfacecolor="white",
            markeredgewidth=0.55,
            markersize=2.5,
        )
        unweighted_axis.set_xscale("log", base=2)
        unweighted_axis.set_xlim(190, 1.5e6)
        unweighted_axis.set_ylim(0, 6.6)
        unweighted_axis.set_xlabel(r"output count $M$ (log$_2$ scale)")
        unweighted_axis.set_ylabel(r"$M^{-1}\max_{r,k}|O_{M,r,k}|$")
        unweighted_axis.grid(color=GRID, linewidth=0.3)
        unweighted_axis.text(
            0.98,
            0.07,
            "unweighted diagnostic; not the heat-kernel sum",
            transform=unweighted_axis.transAxes,
            ha="right",
            fontsize=3.25,
            color=MUTED,
        )

        figure.text(
            0.078,
            0.072,
            "Interpretation: the proved ceiling removes all L-growth but leaves sqrt(M). Panel (c) shows why a supremum bound on the heat kernel is too crude; "
            "the next lemma must retain smooth heat weights and time ordering.",
            ha="left",
            va="top",
            fontsize=3.65,
            color=MUTED,
        )
        add_blossom(figure)
        figure.savefig(HERE / "figure.pdf")
        figure.savefig(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")


if __name__ == "__main__":
    draw()
