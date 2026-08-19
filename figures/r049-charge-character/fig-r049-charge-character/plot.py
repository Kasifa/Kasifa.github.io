#!/usr/bin/env python3
"""Render the R0.49 multiplicative charge-character journal figure."""

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
    roots = rows("root-endpoints.csv")
    contributions = rows("charge-contributions.csv")
    competitors = rows("competitor-gaps.csv")
    geometry = rows("anisotropic-geometry.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r049-charge-character"
        figure = plt.figure(figsize=(178 / 25.4, 142 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(1.04, 0.96),
            height_ratios=(1.0, 1.0),
            left=0.145,
            right=0.974,
            bottom=0.252,
            top=0.876,
            wspace=0.43,
            hspace=0.63,
        )
        crossing_axis = figure.add_subplot(grid[0, 0])
        contribution_axis = figure.add_subplot(grid[0, 1])
        gap_axis = figure.add_subplot(grid[1, 0])
        geometry_axis = figure.add_subplot(grid[1, 1])

        crossing_axis.set_title(
            r"(a) Weighted active-column crossing on $[0.382618,0.382619]$",
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
        window_lower = Fraction(curve[0]["radiusExact"])
        window_upper = Fraction(curve[-1]["radiusExact"])
        root_lower = Fraction(roots[0]["radiusExact"])
        root_upper = Fraction(roots[1]["radiusExact"])
        root_midpoint = (root_lower + root_upper) / 2
        root_position = float((root_midpoint - window_lower) / (window_upper - window_lower))
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
            r"$r_*^{(4/5)}\approx0.3826186423886807785$",
            xy=(root_position, 0),
            xytext=(0.05, 1.65),
            fontsize=4.15,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        crossing_axis.text(
            0.02, -2.82, "81-term Sturm: 40 - 39 = 1 root\n"
            r"$P'(r)>0$ for every $r>0$",
            fontsize=4.15, color=INK, va="bottom"
        )
        crossing_axis.text(
            0.015, crossing_y[0] + 0.18, f"{crossing_y[0]:+.4f} ppm",
            fontsize=4.10, color=BLUE
        )
        crossing_axis.text(
            0.985, crossing_y[-1] - 0.20, f"{crossing_y[-1]:+.4f} ppm",
            fontsize=4.10, color=BLUE, ha="right", va="top"
        )
        crossing_axis.set_xlim(0, 1)
        crossing_axis.set_ylim(-3.45, 2.25)
        crossing_axis.set_xlabel(r"window position $10^6(r-0.382618)$")
        crossing_axis.set_ylabel(r"$10^6[C_{r,4/5}(81,162)-1]$ (ppm)")
        crossing_axis.grid(axis="y", color=GRID, linewidth=0.40)

        contribution_axis.set_title(
            r"(b) Center-charge share of $C_{r,4/5}(81,162)$",
            loc="left",
            pad=5,
        )
        group_order = ["q=-1", "q=+1", "q=+0", "q=+2", "q=+3", "q>=+4"]
        grouped = {label: 0.0 for label in group_order}
        for row in contributions:
            grouped[row["displayGroup"]] += float(row["sharePercentDecimal"])
        y_positions = list(reversed(range(len(group_order))))
        for label, y_value in zip(group_order, y_positions, strict=True):
            value = grouped[label]
            negative_charge = label == "q=-1"
            color = GOLD if negative_charge else BLUE
            fill = PALE_GOLD if negative_charge else PALE_BLUE
            contribution_axis.barh(
                y_value,
                value,
                height=0.56,
                color=fill,
                edgecolor=color,
                linewidth=0.65,
            )
            contribution_axis.text(
                value + 0.8,
                y_value,
                f"{value:.3f}%",
                va="center",
                fontsize=4.10,
                color=color,
            )
        contribution_axis.set_yticks(y_positions)
        contribution_axis.set_yticklabels(
            [r"$q=-1$", r"$q=+1$", r"$q=0$", r"$q=+2$", r"$q=+3$", r"$q\geq+4$"]
        )
        contribution_axis.set_xlim(0, 55)
        contribution_axis.set_ylim(-0.55, 5.55)
        contribution_axis.set_xlabel("share of active column (%)")
        contribution_axis.grid(axis="x", color=GRID, linewidth=0.40)

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
            r"nearest: $s=164$" + "\n" + r"gap $=1.41573\times10^{-4}$",
            xy=(gap_x[0], gap_y[0]),
            xytext=(36, 3.0e-4),
            fontsize=4.15,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.52},
        )
        gap_axis.text(
            238, 0.64, "every exact gap > 0", fontsize=4.20,
            color=INK, ha="right"
        )
        gap_axis.set_xlim(1, 243)
        gap_axis.set_ylim(1.0e-4, 1.1)
        gap_axis.set_xlabel("competitor rank by increasing exact gap")
        gap_axis.set_ylabel("exact sandwich gap")
        gap_axis.grid(axis="y", which="major", color=GRID, linewidth=0.40)

        geometry_axis.set_title(
            "(d) Anisotropic geometry relative to R0.48",
            loc="left",
            pad=5,
        )
        geometry_values = [float(row["percentChangeDecimal"]) for row in geometry]
        geometry_y = list(reversed(range(len(geometry))))
        geometry_axis.axvline(0, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        for index, (row, value, y_value) in enumerate(
            zip(geometry, geometry_values, geometry_y, strict=True)
        ):
            positive = value > 0
            color = GOLD if positive else BLUE
            marker = "D" if index == 2 else "o"
            geometry_axis.hlines(y_value, 0, value, color=color, linewidth=1.0)
            geometry_axis.scatter(
                [value], [y_value], s=34, marker=marker,
                facecolor=PALE_GOLD if positive else "white",
                edgecolor=color, linewidth=0.9, zorder=5
            )
            geometry_axis.text(
                value + 1.1,
                y_value + (0.16 if not positive else 0),
                f"{value:+.2f}%" if index != 2 else f"{value:+.4f}%",
                ha="left",
                va="center",
                fontsize=4.15,
                color=color,
            )
        geometry_axis.text(
            -37.5, -0.40,
            "rho_Z=r/c, rho_W=rc^2, rho_Z^2 rho_W=r^3\n"
            "the old and new polydiscs are not nested",
            fontsize=4.05, color=INK, va="bottom"
        )
        geometry_axis.set_yticks(geometry_y)
        geometry_axis.set_yticklabels(
            [r"$Z$ polyradius", r"$W$ polyradius", r"$R=Z^2W$ disk"]
        )
        geometry_axis.set_xlim(-40, 32)
        geometry_axis.set_ylim(-0.55, 2.55)
        geometry_axis.set_xlabel("exact change versus R0.48 upper threshold (%)")
        geometry_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (crossing_axis, contribution_axis, gap_axis, geometry_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.49 multiplicative charge-character certificate",
            x=0.145,
            y=0.956,
            ha="left",
            fontsize=10.0,
            fontweight="bold",
            color=INK,
        )
        figure.text(
            0.145,
            0.916,
            r"Exact GMP arithmetic; $\omega_s=(4/5)^s$ is multiplicative and conjugates the anisotropic Wiener algebra",
            ha="left",
            fontsize=5.15,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.152,
            "Formal scope: reduced canonical edge generating system.  The figure does not show an isotropic-bidisc gain,\n"
            "optimality of c=4/5, a PDE singularity, or three-dimensional Navier-Stokes regularity.",
            ha="left",
            va="top",
            fontsize=4.45,
            color=INK,
        )
        figure.text(
            0.145,
            0.075,
            "Source: R0.49 exact certificate · 32/32 checks · 243 competitors · monitored 120.58 s · no floating-point decision",
            ha="left",
            fontsize=4.35,
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
