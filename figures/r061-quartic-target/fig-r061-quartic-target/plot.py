#!/usr/bin/env python3
"""Render the paper-ready R0.61 complete quartic-target scan figure."""

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
RUST = "#8b4d43"
OLIVE = "#707241"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def add_blossom(figure) -> None:
    center = (0.955, 0.943)
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
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK, zorder=21)


def draw() -> None:
    profiles = rows("target-profiles.csv")
    edges = rows("edge-scaling.csv")
    profile_styles = {
        (1, 256): (BLUE, "-", "o"),
        (4, 64): (GOLD, (0, (5, 2)), "s"),
        (8, 64): (RUST, (0, (1.5, 1.5)), "^"),
        (16, 32): (OLIVE, (0, (5, 2, 1, 2)), "D"),
    }
    edge_styles = {
        1: (BLUE, "-", "o"),
        2: (GOLD, (0, (5, 2)), "s"),
        4: (RUST, (0, (1.5, 1.5)), "^"),
        8: (OLIVE, (0, (5, 2, 1, 2)), "D"),
        16: (INK, (0, (2.5, 1.5)), "P"),
    }

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r061-quartic-target"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            2,
            left=0.075,
            right=0.965,
            bottom=0.29,
            top=0.79,
            width_ratios=(1.08, 1.0),
            wspace=0.32,
        )
        profile_axis = figure.add_subplot(grid[0, 0])
        edge_axis = figure.add_subplot(grid[0, 1])

        figure.suptitle(
            "Finite quartic target scan in the invariant shear chain",
            x=0.075,
            y=0.945,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.075,
            0.885,
            r"$A^4\widehat G_4/(A^2\widehat G_2)=-(\varepsilon^2/L^2)R_{L,M,m}$  ·  "
            "461 distinct triples  ·  7.495 billion ordered paths  ·  finite evidence only",
            ha="left",
            va="center",
            fontsize=3.9,
            color=MUTED,
        )

        profile_axis.set_title("(a) Complete target profiles", loc="left", pad=5, fontsize=5.2)
        for family, (color, linestyle, marker) in profile_styles.items():
            selected = sorted(
                (row for row in profiles if (int(row["L"]), int(row["M"])) == family),
                key=lambda row: int(row["target"]),
            )
            mark_every = max(1, len(selected) // 12)
            profile_axis.semilogy(
                [float(row["targetFraction"]) for row in selected],
                [float(row["normalizedSignedRatio"]) for row in selected],
                color=color,
                linestyle=linestyle,
                linewidth=0.85,
                marker=marker,
                markerfacecolor="white",
                markeredgewidth=0.45,
                markersize=2.1,
                markevery=mark_every,
                label=rf"$L={family[0]},\ M={family[1]}$",
            )
        profile_axis.set_xlim(0, 1.02)
        profile_axis.set_ylim(5e-9, 2e-3)
        profile_axis.set_xlabel(r"target position $m/M$")
        profile_axis.set_ylabel(r"normalized ratio $R_{L,M,m}$ (log scale)")
        profile_axis.grid(color=GRID, linewidth=0.32, which="major")
        profile_axis.grid(color=GRID, linewidth=0.22, which="minor", alpha=0.45)
        profile_axis.legend(loc="upper left", frameon=False, fontsize=3.45, ncol=2)
        profile_axis.text(
            0.98,
            1.1e-8,
            "416/416 displayed values are positive",
            ha="right",
            va="bottom",
            fontsize=3.45,
            color=MUTED,
        )

        edge_axis.set_title("(b) Edge target over dyadic output count", loc="left", pad=5, fontsize=5.2)
        for length, (color, linestyle, marker) in edge_styles.items():
            selected = sorted(
                (
                    row
                    for row in edges
                    if int(row["L"]) == length and int(row["M"]) >= 16
                ),
                key=lambda row: int(row["M"]),
            )
            if len(selected) < 2:
                continue
            edge_axis.plot(
                [int(row["M"]) for row in selected],
                [1e3 * float(row["normalizedSignedRatio"]) for row in selected],
                color=color,
                linestyle=linestyle,
                linewidth=0.85,
                marker=marker,
                markerfacecolor="white",
                markeredgewidth=0.45,
                markersize=2.3,
                label=rf"$L={length}$",
            )
        edge_axis.set_xscale("log", base=2)
        edge_axis.set_xlim(14, 10000)
        edge_axis.set_ylim(0, 1.52)
        edge_axis.set_xlabel(r"number of outputs $M$ (log$_2$ scale)")
        edge_axis.set_ylabel(r"edge ratio $10^3R_{L,M,M}$")
        edge_axis.grid(color=GRID, linewidth=0.32)
        edge_axis.legend(loc="lower left", frameon=False, fontsize=3.45, ncol=2)
        edge_axis.scatter(
            [64],
            [1.3286562612066827],
            marker="*",
            s=24,
            facecolor=GOLD,
            edgecolor=INK,
            linewidth=0.45,
            zorder=6,
        )
        edge_axis.annotate(
            r"observed max $1.328656\times10^{-3}$" + "\n" + r"$(L,M,m)=(4,64,64)$",
            xy=(64, 1.3286562612066827),
            xytext=(118, 1.43),
            fontsize=3.35,
            color=MUTED,
            arrowprops={"arrowstyle": "->", "color": MUTED, "linewidth": 0.45},
        )

        figure.text(
            0.075,
            0.195,
            "Numerical reliability: maximum cancellation condition 3,860.6; the observed maximum was recomputed at 60 decimal digits; "
            "relative long-double discrepancy < 5.6e-15.",
            ha="left",
            va="top",
            fontsize=3.75,
            color=INK,
        )
        figure.text(
            0.075,
            0.128,
            "Interpretation: positive R means the quartic target opposes the quadratic target. No M-growth appears in the archived range, "
            "but positivity and a uniform bound outside this finite set remain unproved.",
            ha="left",
            va="top",
            fontsize=3.75,
            color=MUTED,
        )
        figure.text(
            0.075,
            0.071,
            "Next theorem: a smooth weighted four-point Rudin–Shapiro correlation estimate uniform in L, M, and m.",
            ha="left",
            va="top",
            fontsize=3.75,
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
