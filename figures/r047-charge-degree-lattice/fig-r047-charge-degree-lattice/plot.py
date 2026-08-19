#!/usr/bin/env python3
"""Render the R0.47 charge--degree lattice journal figure."""

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


def lollipop(axis, y, start, value, color, marker, filled=True):
    axis.hlines(y, start, value, color=color, linewidth=0.88)
    axis.scatter(
        [value],
        [y],
        s=29,
        marker=marker,
        facecolor=color if filled else "white",
        edgecolor=color,
        linewidth=0.9,
        zorder=5,
    )


def draw() -> None:
    fixed = rows("fixed-charge-bounds.csv")
    parity = rows("parity-endpoints.csv")
    controls = rows("radius-controls.csv")
    sectors = rows("sector-bounds.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r047-charge-degree-lattice"
        figure = plt.figure(figsize=(178 / 25.4, 142 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(1.06, 0.94),
            height_ratios=(1.0, 1.0),
            left=0.145,
            right=0.974,
            bottom=0.262,
            top=0.883,
            wspace=0.43,
            hspace=0.62,
        )
        fixed_axis = figure.add_subplot(grid[0, 0])
        parity_axis = figure.add_subplot(grid[0, 1])
        radius_axis = figure.add_subplot(grid[1, 0])
        sector_axis = figure.add_subplot(grid[1, 1])

        fixed_axis.set_title(
            r"(a) Fixed-charge all-degree endpoints at $r=0.376932$",
            loc="left",
            pad=5,
        )
        fixed_x = [int(row["inputCharge"]) for row in fixed]
        fixed_y = [float(Fraction(row["boundExact"])) for row in fixed]
        fixed_axis.plot(fixed_x, fixed_y, color=BLUE, linewidth=0.78)
        fixed_axis.scatter(
            fixed_x,
            fixed_y,
            s=3.2,
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.25,
            zorder=4,
        )
        maximum = next(row for row in fixed if row["isMaximum"] == "true")
        maximum_x = int(maximum["inputCharge"])
        maximum_y = float(Fraction(maximum["boundExact"]))
        fixed_axis.scatter(
            [maximum_x],
            [maximum_y],
            marker="D",
            s=34,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.9,
            zorder=7,
        )
        fixed_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        fixed_axis.annotate(
            r"$s=162,\ j=81$" + "\n0.9999973491",
            xy=(maximum_x, maximum_y),
            xytext=(124, 0.925),
            fontsize=4.45,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.55},
        )
        fixed_axis.text(3, 1.0024, "threshold 1", fontsize=4.35, color=INK)
        fixed_axis.set_xlim(2, 240)
        fixed_axis.set_ylim(0.40, 1.025)
        fixed_axis.set_xlabel(r"fixed positive input charge $s$")
        fixed_axis.set_ylabel("exact endpoint bound")
        fixed_axis.grid(axis="y", color=GRID, linewidth=0.40)

        parity_axis.set_title(
            r"(b) Large-charge lattice branches in $y=1/s$",
            loc="left",
            pad=5,
        )
        parity_styles = {
            "even": (GOLD, "D", "solid", r"even: $E_{\rm e}(y)$"),
            "odd": (BLUE, "o", (0, (5, 2)), r"odd: $E_{\rm o}(y)$"),
        }
        for branch, (color, marker, line_style, label) in parity_styles.items():
            selected = [row for row in parity if row["branch"] == branch]
            xs = [1000 * float(Fraction(row["yExact"])) for row in selected]
            ys = [float(Fraction(row["boundExact"])) for row in selected]
            parity_axis.plot(
                xs,
                ys,
                color=color,
                linewidth=0.95,
                linestyle=line_style,
                label=label,
            )
            parity_axis.scatter(
                [xs[0], xs[-1]],
                [ys[0], ys[-1]],
                s=26,
                marker=marker,
                facecolor=color if branch == "even" else "white",
                edgecolor=color,
                linewidth=0.8,
                zorder=5,
            )
        parity_axis.text(
            0.10,
            0.9979,
            "319/319 signed Bernstein\ncoefficients positive per branch",
            fontsize=4.2,
            color=INK,
            va="top",
        )
        parity_axis.text(4.095, 0.9968, r"$s=242$", fontsize=4.25, color=GOLD)
        parity_axis.text(4.105, 0.9872, r"$s=241$", fontsize=4.25, color=BLUE)
        parity_axis.set_xlim(0, 4.25)
        parity_axis.set_ylim(0.9858, 0.9985)
        parity_axis.set_xlabel(r"$10^3y=10^3/s$")
        parity_axis.set_ylabel("exact rational endpoint")
        parity_axis.legend(loc="lower left", frameon=False, fontsize=4.05)
        parity_axis.grid(axis="y", color=GRID, linewidth=0.40)

        radius_axis.set_title(
            r"(c) Radius controls at $\kappa=3/4$",
            loc="left",
            pad=5,
        )
        control_order = ["entry", "target", "probe"]
        x_positions = list(range(3))
        control_styles = {
            "lattice-sharp tail": (GOLD, "D", "solid", "lattice-sharp tail"),
            "R0.46 separated tail": (
                INK,
                "s",
                (0, (4, 2)),
                "old separated tail",
            ),
            "canonical stretch": (BLUE, "o", (0, (1, 1.5)), "stretch"),
        }
        for series, (color, marker, line_style, label) in control_styles.items():
            selected = {
                row["control"]: float(Fraction(row["boundExact"]))
                for row in controls
                if row["series"] == series
            }
            values = [selected[item] for item in control_order]
            radius_axis.plot(
                x_positions,
                values,
                color=color,
                linewidth=0.9,
                linestyle=line_style,
            )
            radius_axis.scatter(
                x_positions,
                values,
                s=29,
                marker=marker,
                facecolor=(
                    "white" if series in {"canonical stretch", "R0.46 separated tail"}
                    else color
                ),
                edgecolor=color,
                linewidth=0.85,
                label=label,
                zorder=5,
            )
        radius_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        radius_axis.text(-0.12, 1.00020, "threshold 1", ha="left", fontsize=4.35)
        radius_axis.text(
            1.50,
            1.00072,
            "target: -2.651e-6\nprobe: +2.658e-6",
            ha="center",
            va="bottom",
            fontsize=4.15,
            color=GOLD,
        )
        radius_axis.set_xlim(-0.16, 2.16)
        radius_axis.set_ylim(0.985, 1.0042)
        radius_axis.set_xticks(x_positions)
        radius_axis.set_xticklabels(
            ["entry\n0.376", "target\n0.376932", "probe\n0.376933"]
        )
        radius_axis.set_ylabel("focused exact bound")
        radius_axis.legend(loc="lower right", frameon=False, fontsize=3.85)
        radius_axis.grid(axis="y", color=GRID, linewidth=0.40)

        sector_axis.set_title(
            r"(d) Exhaustive sectors at $r=0.376932$",
            loc="left",
            pad=5,
        )
        y_positions = list(reversed(range(len(sectors))))
        for row, y in zip(sectors, y_positions):
            value = float(Fraction(row["boundExact"]))
            active = row["isMaximum"] == "true"
            color = GOLD if active else BLUE
            marker = "D" if active else "o"
            lollipop(sector_axis, y, 0, value, color, marker, active)
            sector_axis.text(
                value + 0.012,
                y,
                f"{value:.6f}",
                va="center",
                fontsize=4.35,
                color=color,
            )
        sector_axis.axvline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        sector_axis.text(1.012, 4.25, "threshold 1", fontsize=4.35, color=INK)
        sector_axis.set_xlim(0, 1.08)
        sector_axis.set_ylim(-0.45, 4.45)
        sector_axis.set_yticks(y_positions)
        sector_labels = {
            "s=0": r"$s=0$",
            "s=-1": r"$s=-1$",
            "s=1": r"$s=1$",
            "s=162": r"$s=162$",
            "s>=241": r"$s\geq241$",
        }
        sector_axis.set_yticklabels([sector_labels[row["sector"]] for row in sectors])
        sector_axis.set_xlabel("all-order weighted-column bound")
        sector_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (fixed_axis, parity_axis, radius_axis, sector_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.47 exact charge–degree lattice diagnostics",
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
            r"Exact GMP bounds; preserving lattice correlation moves the certified radius from $0.376$ to $0.376932$",
            ha="left",
            fontsize=5.30,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.194,
            r"Theorem: each fixed $2\leq s<241$ covers all $j\geq J_s$; the even/odd rational branches cover every $s\geq241$.",
            ha="left",
            fontsize=4.80,
            color=INK,
        )
        figure.text(
            0.145,
            0.161,
            r"Target: the exact $s=162,j=81$ column is 0.9999973491 at $r=0.376932$; the fixed-point and stretch gates close.",
            ha="left",
            fontsize=4.72,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.128,
            r"Control: the same true column is 1.0000026585 at $r=0.376933$; this is a failure of this sufficient norm inequality only.",
            ha="left",
            fontsize=4.72,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.095,
            "Scope: reduced canonical edge generating system; rational-curve samples are presentation aids, not the continuous sign proof.",
            ha="left",
            fontsize=4.62,
            color=MUTED,
        )
        figure.text(
            0.984,
            0.038,
            "R0.47 | exact rational certificate | 2026-08-19",
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
