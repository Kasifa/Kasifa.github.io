#!/usr/bin/env python3
"""Render the R0.55 critical Fourier bridge and scalar-charge figure."""

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
    scaling = rows("critical-scaling.csv")
    triads = rows("triad-saturation.csv")
    sigmas = [float(row["sigmaDecimal"]) for row in scaling]
    exponents = [float(row["spatialScalingExponentDecimal"]) for row in scaling]
    indices = [int(row["N"]) for row in triads]
    ratios = [float(row["criticalSymbolRatioDecimal"]) for row in triads]
    separations = [
        float(row["minimumInputOutputSeparationDecimal"]) for row in triads
    ]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r055-critical-fourier-bridge"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.075,
            right=0.963,
            bottom=0.315,
            top=0.835,
            width_ratios=(0.95, 1.05, 1.2),
            wspace=0.42,
        )
        scaling_axis = figure.add_subplot(grid[0, 0])
        geometry_axis = figure.add_subplot(grid[0, 1])
        ratio_axis = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Critical Fourier control and the scalar-charge obstruction",
            x=0.075,
            y=0.945,
            ha="left",
            fontsize=8.2,
            color=INK,
        )

        scaling_axis.set_title("(a) Exact scaling exponent", loc="left", pad=5)
        scaling_axis.axhline(0, color=INK, linewidth=0.55, linestyle=(0, (3, 2)))
        scaling_axis.axvline(-1, color=GRID, linewidth=0.5)
        scaling_axis.plot(sigmas, exponents, color=BLUE, linewidth=1.2)
        scaling_axis.scatter(
            [-1],
            [0],
            marker="D",
            s=32,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=5,
        )
        scaling_axis.annotate(
            r"$\mathcal X^{-1}$ is critical",
            xy=(-1, 0),
            xytext=(-1.7, 1.0),
            fontsize=4.3,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.5},
        )
        scaling_axis.text(
            0.05,
            0.94,
            r"$\|u_\lambda\|_{\mathcal X^\sigma}"
            "\n"
            r"=\lambda^{\sigma+1}\|u\|_{\mathcal X^\sigma}$",
            transform=scaling_axis.transAxes,
            va="top",
            fontsize=4.2,
            color=INK,
        )
        scaling_axis.set_xlim(-2.05, 2.05)
        scaling_axis.set_ylim(-1.15, 3.15)
        scaling_axis.set_xlabel(r"Fourier weight exponent $\sigma$")
        scaling_axis.set_ylabel(r"scaling exponent $\sigma+1$")
        scaling_axis.grid(color=GRID, linewidth=0.34)

        geometry_axis.set_title("(b) One exact near-cancelling triad", loc="left", pad=5)
        origin = (0.0, 0.0)
        left_tip = (4.0, 0.0)
        output_tip = (0.0, 1.0)
        arrow = {"arrowstyle": "-|>", "mutation_scale": 8, "shrinkA": 0, "shrinkB": 0}
        geometry_axis.annotate(
            "",
            xy=left_tip,
            xytext=origin,
            arrowprops={**arrow, "color": BLUE, "linewidth": 1.1},
        )
        geometry_axis.annotate(
            "",
            xy=output_tip,
            xytext=left_tip,
            arrowprops={**arrow, "color": GOLD, "linewidth": 1.1},
        )
        geometry_axis.annotate(
            "",
            xy=output_tip,
            xytext=origin,
            arrowprops={**arrow, "color": INK, "linewidth": 0.9},
        )
        geometry_axis.scatter(
            [origin[0], left_tip[0], output_tip[0]],
            [origin[1], left_tip[1], output_tip[1]],
            s=9,
            color=INK,
            zorder=5,
        )
        geometry_axis.text(2.0, -0.22, r"$p_4=(4,0,0)$", ha="center", fontsize=4.2, color=BLUE)
        geometry_axis.text(2.25, 0.63, r"$q_4=(-4,1,0)$", ha="center", fontsize=4.2, color=GOLD, rotation=-8)
        geometry_axis.text(-0.16, 0.5, r"$k=(0,1,0)$", ha="right", va="center", fontsize=4.2, color=INK, rotation=90)
        geometry_axis.text(
            0.05,
            0.94,
            r"$a=e_2,\ b=e_3$"
            "\n"
            r"$P_k[(q_N\!\cdot a)b]=b$",
            transform=geometry_axis.transAxes,
            va="top",
            fontsize=4.2,
            color=INK,
        )
        geometry_axis.text(
            0.05,
            0.06,
            "Representative N = 4\nidentity holds for every N >= 1",
            transform=geometry_axis.transAxes,
            fontsize=3.9,
            color=MUTED,
        )
        geometry_axis.set_xlim(-0.62, 4.55)
        geometry_axis.set_ylim(-0.48, 1.58)
        geometry_axis.set_aspect("equal", adjustable="box")
        geometry_axis.set_xlabel(r"frequency coordinate $\xi_1$")
        geometry_axis.set_ylabel(r"frequency coordinate $\xi_2$")
        geometry_axis.grid(color=GRID, linewidth=0.34)

        ratio_axis.set_title("(c) Exact all-index saturation", loc="left", pad=5)
        ratio_axis.plot(
            indices,
            ratios,
            color=BLUE,
            linewidth=1.2,
            label=r"critical symbol ratio $=1$",
        )
        ratio_axis.scatter(
            [1, 4, 16, 64, 256],
            [1, 1, 1, 1, 1],
            marker="D",
            s=13,
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.65,
            zorder=5,
        )
        separation_axis = ratio_axis.twinx()
        separation_axis.plot(
            indices,
            separations,
            color=GOLD,
            linewidth=0.9,
            linestyle=(0, (4, 2)),
            label=r"input/output separation $=N$",
        )
        ratio_axis.set_xscale("log", base=2)
        separation_axis.set_yscale("log", base=2)
        ratio_axis.set_xlim(1, 256)
        ratio_axis.set_ylim(0.955, 1.045)
        separation_axis.set_ylim(1, 256)
        ratio_axis.set_xlabel(r"integer family index $N$")
        ratio_axis.set_ylabel(r"$|k|^{-1}|\mathscr B_k|/(|a||b|)$", color=BLUE)
        separation_axis.set_ylabel("minimum input/output separation", color=GOLD)
        ratio_axis.tick_params(axis="y", colors=BLUE)
        separation_axis.tick_params(axis="y", colors=GOLD)
        ratio_axis.grid(color=GRID, linewidth=0.34)
        legend_handles = [
            Line2D([0], [0], color=BLUE, linewidth=1.2, label="critical ratio = 1"),
            Line2D(
                [0],
                [0],
                color=GOLD,
                linewidth=0.9,
                linestyle=(0, (4, 2)),
                label="separation = N",
            ),
        ]
        ratio_axis.legend(
            handles=legend_handles,
            loc="lower right",
            frameon=False,
            fontsize=3.8,
        )
        ratio_axis.text(
            0.04,
            0.94,
            "200,000 exact triads checked\nall displayed rows are presentation data",
            transform=ratio_axis.transAxes,
            va="top",
            fontsize=3.9,
            color=MUTED,
        )

        figure.text(
            0.075,
            0.235,
            "Bridge decision:  scalar degree majorant = finite   |   nontrivial scalar charge = impossible under additivity + rotation   |   shell–angle–polarization state = open",
            ha="left",
            va="top",
            fontsize=4.15,
            color=INK,
        )
        figure.text(
            0.075,
            0.168,
            r"Critical bound: $\|\mathcal T(u,v)\|_{\mathcal E_\nu}\leq\nu^{-1}\|u\|_{\mathcal E_\nu}\|v\|_{\mathcal E_\nu}$."
            "  The exact high–high-to-low family shows that scale separation supplies no extra small factor.",
            ha="left",
            va="top",
            fontsize=4.15,
            color=INK,
        )
        figure.text(
            0.075,
            0.103,
            r"Charge no-go: $\chi(\xi+\eta)=\chi(\xi)+\chi(\eta)$ and $\chi(R\xi)=\chi(\xi)$ for every $R\in SO(3)$ imply $\chi\equiv0$.",
            ha="left",
            va="top",
            fontsize=4.15,
            color=RED,
        )
        figure.text(
            0.075,
            0.043,
            "Scope: classical critical small-data baseline plus one direct-interface obstruction · 17/17 checks · no three-dimensional Navier–Stokes regularity claim",
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
