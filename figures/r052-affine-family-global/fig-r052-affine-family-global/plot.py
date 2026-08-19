#!/usr/bin/env python3
"""Render the R0.52 affine-family global-bound journal figure."""

from __future__ import annotations

import csv
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
    feasibility = rows("feasibility-profile.csv")
    contraction = rows("krawczyk-contraction.csv")
    competitors = rows("inactive-gaps.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r052-affine-family-global"
        figure = plt.figure(figsize=(178 / 25.4, 112 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            height_ratios=(1.00, 1.00),
            left=0.105,
            right=0.974,
            bottom=0.295,
            top=0.858,
            wspace=0.38,
            hspace=0.69,
        )
        feasibility_axis = figure.add_subplot(grid[0, 0])
        contraction_axis = figure.add_subplot(grid[0, 1])
        gap_axis = figure.add_subplot(grid[1, :])

        figure.suptitle(
            r"Global certification of the affine family $c^s(1+\lambda|s|)$",
            x=0.105,
            y=0.946,
            ha="left",
            fontsize=8.1,
            color=INK,
        )

        feasibility_axis.set_title(
            r"(a) Eliminated margin around the global candidate",
            loc="left",
            pad=5,
        )
        for side, color, marker, linestyle in (
            ("left", BLUE, "o", (0, (4, 2))),
            ("right", GOLD, "s", "-"),
        ):
            selected = [row for row in feasibility if row["side"] == side]
            distance = [float(row["distanceDecimal"]) for row in selected]
            margin = [
                float(row["negativeClearedFeasibilityDecimal"])
                for row in selected
            ]
            feasibility_axis.loglog(
                distance,
                margin,
                color=color,
                linewidth=0.9,
                linestyle=linestyle,
                marker=marker,
                markersize=2.2,
                markerfacecolor="white",
                markeredgewidth=0.45,
                markevery=4,
                label=rf"$c_2$ {side}",
            )
        bernstein_margin = 6.806827772536233e-39
        feasibility_axis.axhline(
            bernstein_margin,
            color=INK,
            linewidth=0.65,
            linestyle=(0, (4, 2)),
        )
        feasibility_axis.annotate(
            "317/317 Bernstein\ncoefficients negative",
            xy=(2.0e-35, bernstein_margin),
            xytext=(1.0e-23, 2.4e-34),
            fontsize=4.1,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 0.48},
        )
        feasibility_axis.set_xlim(2e-41, 2e-1)
        feasibility_axis.set_ylim(2e-39, 2e2)
        feasibility_axis.set_xlabel(r"distance $|c-c_2|$")
        feasibility_axis.set_ylabel(r"$-c^2E(r_U,c)$")
        feasibility_axis.legend(loc="upper left", frameon=False, fontsize=4.1)
        feasibility_axis.grid(which="both", color=GRID, linewidth=0.36)

        contraction_axis.set_title(
            "(b) Exact Krawczyk contraction",
            loc="left",
            pad=5,
        )
        x_positions = list(range(1, len(contraction) + 1))
        box_widths = [float(row["boxWidthDecimal"]) for row in contraction]
        image_radii = [
            float(row["krawczykImageRadiusDecimal"]) for row in contraction
        ]
        contraction_axis.vlines(
            x_positions,
            image_radii,
            box_widths,
            color=BLUE,
            linewidth=1.0,
        )
        contraction_axis.scatter(
            x_positions,
            box_widths,
            s=27,
            marker="s",
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.75,
            label="root-box width",
            zorder=5,
        )
        contraction_axis.scatter(
            x_positions,
            image_radii,
            s=31,
            marker="D",
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            label="Krawczyk radius",
            zorder=6,
        )
        for x, radius in zip(x_positions, image_radii, strict=True):
            contraction_axis.text(
                x,
                radius / 5,
                f"{radius:.1e}",
                ha="center",
                va="top",
                fontsize=4.0,
                color=GOLD,
            )
        contraction_axis.set_yscale("log")
        contraction_axis.set_xlim(0.5, 3.5)
        contraction_axis.set_ylim(1e-82, 2e-38)
        contraction_axis.set_xticks(x_positions, [r"$r$", r"$c$", r"$\alpha$"])
        contraction_axis.set_ylabel("interval scale")
        contraction_axis.text(
            0.03,
            0.94,
            r"open square: box width $=10^{-40}$",
            transform=contraction_axis.transAxes,
            ha="left",
            va="top",
            fontsize=4.0,
            color=BLUE,
        )
        contraction_axis.text(
            0.03,
            0.86,
            "filled diamond: Krawczyk radius",
            transform=contraction_axis.transAxes,
            ha="left",
            va="top",
            fontsize=4.0,
            color=GOLD,
        )
        contraction_axis.grid(axis="y", which="both", color=GRID, linewidth=0.36)

        gap_x = [int(row["rankByGap"]) for row in competitors]
        gap_y = [float(row["gapDecimal"]) for row in competitors]
        gap_axis.set_title(
            "(c) All 242 inactive all-order sector gaps on the root box",
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
            r"nearest: $s=164,j=82$" + "\n" + r"gap $>1.45276\times10^{-4}$",
            xy=(gap_x[0], gap_y[0]),
            xytext=(37, 7.5e-4),
            fontsize=4.2,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        gap_axis.set_xlim(1, 242)
        gap_axis.set_ylim(1e-4, 1.0)
        gap_axis.set_xlabel("inactive-sector rank")
        gap_axis.set_ylabel("gap below one (log)")
        gap_axis.grid(axis="y", which="both", color=GRID, linewidth=0.40)

        figure.text(
            0.105,
            0.171,
            "Display: 80 exact rational feasibility samples, three exact Krawczyk inclusions, and all 242 inactive gaps.  "
            "Proof: GMP Krawczyk/KKT, Descartes 3/3 roots, and 317 negative Bernstein coefficients.",
            ha="left",
            va="top",
            fontsize=4.25,
            color=INK,
        )
        figure.text(
            0.105,
            0.123,
            r"Scope: complete $c>0,\lambda\geq0$ affine family in the reduced degree-80 edge system; global radius gap $10^{-40}$.  "
            "No exact-real maximizer uniqueness and no three-dimensional Navier--Stokes regularity claim.",
            ha="left",
            va="top",
            fontsize=4.25,
            color=INK,
        )
        figure.text(
            0.105,
            0.075,
            "Source: R0.52 exact certificate · 22/22 checks · 242 inactive sectors · monitored 242.4 s · no floating-point sign decision",
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
