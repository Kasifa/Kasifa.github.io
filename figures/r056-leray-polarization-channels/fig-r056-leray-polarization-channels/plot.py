#!/usr/bin/env python3
"""Render the R0.56 exact Leray polarization-channel figure."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
RED = "#9a3f36"
PALE_BLUE = "#dbe5ea"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def add_blossom(figure) -> None:
    center = (0.955, 0.942)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(
            Ellipse(
                (
                    center[0] + 0.0105 * math.cos(theta),
                    center[1] + 0.013 * math.sin(theta),
                ),
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
    profile = rows("channel-profile.csv")
    families = rows("channel-families.csv")
    angular = rows("angular-persistence.csv")

    mus = [float(row["muDecimal"]) for row in profile]
    normal_profile = [float(row["normalGainDecimal"]) for row in profile]
    planar_profile = [float(row["planarGainDecimal"]) for row in profile]
    indices = [int(row["N"]) for row in families]
    saturation_normal = [
        float(row["saturationNormalGainDecimal"]) for row in families
    ]
    saturation_planar = [
        float(row["saturationPlanarGainDecimal"]) for row in families
    ]
    half_limit_planar = [
        float(row["halfLimitPlanarGainDecimal"]) for row in families
    ]
    angular_near = [row for row in angular if float(row["deltaDecimal"]) <= 0.25]
    deltas = [float(row["deltaDecimal"]) for row in angular_near]
    measures = [
        float(row["nearSaturationMeasureDecimal"]) for row in angular_near
    ]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r056-leray-polarization-channels"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.075,
            right=0.963,
            bottom=0.345,
            top=0.825,
            width_ratios=(1.05, 1.15, 0.95),
            wspace=0.39,
        )
        profile_axis = figure.add_subplot(grid[0, 0])
        family_axis = figure.add_subplot(grid[0, 1])
        angular_axis = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Exact Leray polarization channels in high–high-to-low triads",
            x=0.075,
            y=0.945,
            ha="left",
            fontsize=8.2,
            color=INK,
        )

        profile_axis.set_title("(a) Channel profile at $|k|/|p|=1/8$", loc="left", pad=5)
        profile_axis.plot(
            mus,
            normal_profile,
            color=BLUE,
            linewidth=1.2,
            label=r"normal $g_N$",
        )
        profile_axis.plot(
            mus,
            planar_profile,
            color=GOLD,
            linewidth=1.0,
            linestyle=(0, (4, 2)),
            label=r"in-plane $g_T$",
        )
        profile_axis.axhline(
            9 / 16,
            color=RED,
            linewidth=0.7,
            linestyle=(0, (1, 2)),
        )
        profile_axis.scatter(
            [0],
            [1],
            marker="D",
            s=21,
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.7,
            zorder=5,
        )
        profile_axis.text(
            0.97,
            0.965,
            r"$g_N=\sqrt{1-\mu^2}$",
            transform=profile_axis.transAxes,
            ha="right",
            va="top",
            fontsize=4.1,
            color=BLUE,
        )
        profile_axis.text(
            0.97,
            0.57,
            r"formal $g_T\leq9/16$",
            transform=profile_axis.transAxes,
            ha="right",
            va="bottom",
            fontsize=3.9,
            color=RED,
        )
        profile_axis.set_xlim(-1, 1)
        profile_axis.set_ylim(0, 1.05)
        profile_axis.set_xlabel(r"output-direction cosine $\mu=\widehat p\cdot\widehat k$")
        profile_axis.set_ylabel("critical channel gain")
        profile_axis.grid(color=GRID, linewidth=0.34)
        profile_axis.legend(loc="lower center", frameon=False, fontsize=3.8, ncol=2)

        family_axis.set_title("(b) Two exact integer families", loc="left", pad=5)
        family_axis.plot(
            indices,
            saturation_normal,
            color=BLUE,
            linewidth=1.2,
            label=r"saturating family: $g_N=1$",
        )
        family_axis.plot(
            indices,
            saturation_planar,
            color=BLUE,
            linewidth=0.85,
            linestyle=(0, (3, 2)),
            label=r"same family: $g_T=(N^2+1)^{-1/2}$",
        )
        family_axis.plot(
            indices,
            half_limit_planar,
            color=GOLD,
            linewidth=1.1,
            label=r"half-limit family: $g_T\to1/2$",
        )
        family_axis.axhline(
            0.5,
            color=INK,
            linewidth=0.55,
            linestyle=(0, (1, 2)),
        )
        family_axis.scatter(
            [1, 8, 64, 512],
            [1, 1, 1, 1],
            marker="D",
            s=12,
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.55,
            zorder=5,
        )
        family_axis.set_xscale("log", base=2)
        family_axis.set_xlim(1, 512)
        family_axis.set_ylim(0, 1.05)
        family_axis.set_xlabel(r"integer family index $N$")
        family_axis.set_ylabel("exact channel gain")
        family_axis.grid(color=GRID, linewidth=0.34)
        family_axis.legend(loc="center right", frameon=False, fontsize=3.6)
        family_axis.text(
            0.04,
            0.95,
            r"$|k|/|p|\to0$",
            transform=family_axis.transAxes,
            va="top",
            fontsize=4.0,
            color=MUTED,
        )

        angular_axis.set_title("(c) Angular persistence", loc="left", pad=5)
        angular_axis.fill_between(
            deltas,
            measures,
            color=PALE_BLUE,
            linewidth=0,
            alpha=0.8,
        )
        angular_axis.plot(deltas, measures, color=BLUE, linewidth=1.2)
        angular_axis.scatter(
            [0.1],
            [math.sqrt(0.19)],
            marker="D",
            s=18,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.65,
            zorder=5,
        )
        angular_axis.annotate(
            r"$\delta=0.1:\ 43.6\%$",
            xy=(0.1, math.sqrt(0.19)),
            xytext=(0.145, 0.33),
            fontsize=3.9,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.5},
        )
        angular_axis.text(
            0.05,
            0.94,
            r"fraction $=\sqrt{2\delta-\delta^2}$"
            "\n"
            r"mean$(g_N)=\pi/4$"
            "\n"
            r"mean$(g_N^2)=2/3$",
            transform=angular_axis.transAxes,
            va="top",
            fontsize=4.0,
            color=INK,
        )
        angular_axis.set_xlim(0, 0.25)
        angular_axis.set_ylim(0, 0.7)
        angular_axis.set_xlabel(r"near-saturation tolerance $\delta$")
        angular_axis.set_ylabel(r"solid-angle fraction with $g_N\geq1-\delta$")
        angular_axis.grid(color=GRID, linewidth=0.34)

        figure.text(
            0.075,
            0.235,
            r"Exact kernel: $\mathcal{K}_{p,q}(a,b)=g_N a_t\,[b_n n+(\widehat{q}\cdot\widehat{k})b_t t_k]$; only the normal channel attains one.",
            ha="left",
            va="top",
            fontsize=4.15,
            color=INK,
        )
        figure.text(
            0.075,
            0.165,
            r"Separated-cell theorem: if $|k|/|p|\leq\rho<1$, then $g_T\leq(1+\rho)/2<1$, whereas positive angular averages of $g_N$ have no shell decay.",
            ha="left",
            va="top",
            fontsize=4.15,
            color=RED,
        )
        figure.text(
            0.075,
            0.095,
            "Exact audit: 1,764,912 integer triads · 400,000 family instances · 21/21 checks · Craya–Herring/Waleffe frame acknowledged as prior art",
            ha="left",
            va="top",
            fontsize=4.05,
            color=INK,
        )
        figure.text(
            0.075,
            0.043,
            "Scope: pointwise triad lemma; no closed large-data norm and no three-dimensional Navier–Stokes regularity claim",
            ha="left",
            fontsize=4.05,
            color=MUTED,
        )
        add_blossom(figure)
        figure.savefig(HERE / "figure.pdf", metadata={"CreationDate": None})
        figure.savefig(HERE / "figure.svg", metadata={"Date": None})
        normalize_svg(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)


if __name__ == "__main__":
    draw()
