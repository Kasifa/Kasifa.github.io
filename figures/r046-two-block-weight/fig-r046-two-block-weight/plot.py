#!/usr/bin/env python3
"""Render the R0.46 correlated two-block journal figure."""

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
                (center[0] + 0.012 * math.cos(theta), center[1] + 0.015 * math.sin(theta)),
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
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK, zorder=21)


def lollipop(axis, y, start, value, color, marker, filled=True):
    axis.hlines(y, start, value, color=color, linewidth=0.88)
    if marker == "x":
        axis.scatter([value], [y], s=29, marker=marker, color=color, linewidth=0.9, zorder=5)
        return
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
    envelope = rows("weight-envelope.csv")
    controls = rows("radius-controls.csv")
    sectors = rows("sector-bounds.csv")
    gates = rows("proof-gates.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r046-two-block-weight"
        figure = plt.figure(figsize=(178 / 25.4, 140 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(1.08, 0.92),
            height_ratios=(1.0, 1.0),
            left=0.145,
            right=0.974,
            bottom=0.252,
            top=0.883,
            wspace=0.43,
            hspace=0.61,
        )
        weight_axis = figure.add_subplot(grid[0, 0])
        radius_axis = figure.add_subplot(grid[0, 1])
        sector_axis = figure.add_subplot(grid[1, 0])
        gate_axis = figure.add_subplot(grid[1, 1])

        weight_axis.set_title(r"(a) Exact weight envelope at $r=0.376$", loc="left", pad=5)
        styles = {
            "s=0 endpoint": (BLUE, (0, (4, 2)), r"$s=0$ endpoint"),
            "s=-1 endpoint": (GOLD, (0, (6, 2, 1, 2)), r"$s=-1$ endpoint"),
            "large s>=241": (MUTED, (0, (1, 2)), r"large $s\geq241$"),
            "complete envelope": (INK, "solid", "complete envelope"),
        }
        for series, (color, line_style, label) in styles.items():
            selected = [row for row in envelope if row["series"] == series]
            xs = [float(Fraction(row["zeroChargeWeightExact"])) for row in selected]
            ys = [float(Fraction(row["boundExact"])) for row in selected]
            weight_axis.plot(xs, ys, color=color, linestyle=line_style, linewidth=1.0, label=label)
        target_row = next(
            row
            for row in envelope
            if row["series"] == "complete envelope" and row["isCertifiedWeight"] == "true"
        )
        target_weight = float(Fraction(target_row["zeroChargeWeightExact"]))
        target_value = float(Fraction(target_row["boundExact"]))
        weight_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        weight_axis.axvline(target_weight, color=GOLD, linewidth=0.75, linestyle=(0, (4, 2)))
        weight_axis.scatter([target_weight], [target_value], marker="D", s=34, facecolor=PALE_GOLD, edgecolor=GOLD, linewidth=0.9, zorder=7)
        weight_axis.text(target_weight + 0.012, 0.9982, r"$\kappa=3/4$", fontsize=4.45, color=GOLD)
        weight_axis.text(0.505, 1.0011, "threshold 1", fontsize=4.35, color=INK)
        weight_axis.set_xlim(0.50, 1.00)
        weight_axis.set_ylim(0.74, 1.04)
        weight_axis.set_xlabel(r"charge-zero block weight $\kappa$")
        weight_axis.set_ylabel("weighted column bound")
        weight_axis.legend(loc="lower right", frameon=False, fontsize=3.95)
        weight_axis.grid(axis="y", color=GRID, linewidth=0.40)

        radius_axis.set_title(r"(b) Radius controls at $\kappa=3/4$", loc="left", pad=5)
        control_order = ["entry", "rescued", "target", "probe"]
        x_positions = list(range(4))
        radius_styles = {
            "two-block tail": (GOLD, "D", "solid", "two-block tail"),
            "unweighted R0.45": (INK, "x", (0, (4, 2)), "unweighted"),
            "canonical stretch": (BLUE, "o", "solid", "stretch"),
        }
        for series, (color, marker, line_style, label) in radius_styles.items():
            selected = {row["control"]: float(row["boundDecimal"]) for row in controls if row["series"] == series}
            values = [selected[item] for item in control_order]
            radius_axis.plot(x_positions, values, color=color, linewidth=0.85, linestyle=line_style)
            scatter_style = {
                "s": 27,
                "marker": marker,
                "linewidth": 0.85,
                "label": label,
                "zorder": 5,
            }
            if marker == "x":
                radius_axis.scatter(x_positions, values, color=color, **scatter_style)
            else:
                radius_axis.scatter(
                    x_positions,
                    values,
                    facecolor="white" if series == "canonical stretch" else color,
                    edgecolor=color,
                    **scatter_style,
                )
        radius_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        radius_axis.text(3.0, 1.0011, "threshold 1", ha="right", fontsize=4.35, color=INK)
        radius_axis.set_xlim(-0.18, 3.18)
        radius_axis.set_ylim(0.953, 1.024)
        radius_axis.set_xticks(x_positions)
        radius_axis.set_xticklabels(["entry\n0.371", "rescued\n0.372", "target\n0.376", "probe\n0.377"])
        radius_axis.set_ylabel("focused all-order bound")
        radius_axis.legend(loc="lower right", frameon=False, fontsize=3.9)
        radius_axis.grid(axis="y", color=GRID, linewidth=0.40)

        sector_axis.set_title(r"(c) Exhaustive sectors at $r=0.376$", loc="left", pad=5)
        y_positions = list(reversed(range(len(sectors))))
        for row, y in zip(sectors, y_positions):
            value = float(row["boundDecimal"])
            active = row["sector"] == "s>=241"
            color = GOLD if active else BLUE
            marker = "D" if active else "o"
            lollipop(sector_axis, y, 0, value, color, marker, active)
            sector_axis.text(value + 0.012, y, f"{value:.6f}", va="center", fontsize=4.45, color=color)
        sector_axis.axvline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        sector_axis.text(1.012, 4.25, "threshold 1", fontsize=4.45, color=INK)
        sector_axis.set_xlim(0, 1.08)
        sector_axis.set_ylim(-0.45, 4.45)
        sector_axis.set_yticks(y_positions)
        sector_axis.set_yticklabels([row["sector"] for row in sectors])
        sector_axis.set_xlabel("all-order weighted-column bound")
        sector_axis.grid(axis="x", color=GRID, linewidth=0.40)

        gate_axis.set_title("(d) Correlation and construction gates", loc="left", pad=5)
        y_positions = list(reversed(range(len(gates))))
        for row, y in zip(gates, y_positions):
            value = float(row["valueDecimal"])
            formal = row["classification"] == "formal gate"
            color = BLUE if row["gate"] == "canonical stretch" else (GOLD if formal else INK)
            marker = "o" if formal else "s"
            if row["gate"] == "coarse block Perron":
                marker = "x"
            lollipop(gate_axis, y, 0.95, value, color, marker, formal)
            gate_axis.text(
                value + 0.003 if value < 1.06 else value - 0.003,
                y,
                f"{value:.6f}",
                ha="left" if value < 1.06 else "right",
                va="center",
                fontsize=4.2,
                color=color,
            )
        gate_axis.axvline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        gate_axis.text(1.002, 5.25, "threshold 1", fontsize=4.4, color=INK)
        gate_axis.set_xlim(0.95, 1.09)
        gate_axis.set_ylim(-0.45, 5.45)
        gate_axis.set_yticks(y_positions)
        gate_axis.set_yticklabels([row["gate"] for row in gates])
        gate_axis.set_xlabel("focused bound; Perron value is display-only")
        gate_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (weight_axis, radius_axis, sector_axis, gate_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.46 two-block weighted-column diagnostics",
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
            r"Exact GMP bounds; same-column zero/nonzero output correlation moves the certified radius from $0.371$ to $0.376$",
            ha="left",
            fontsize=5.35,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.181,
            r"Norm: $\|f\|_{r,\kappa}=\kappa\|P_0f\|_{B_r}+\|P_{\ne0}f\|_{B_r}$ with $\kappa=3/4$; all five charge sectors are covered analytically.",
            ha="left",
            fontsize=4.85,
            color=INK,
        )
        figure.text(
            0.145,
            0.150,
            r"Target: at $r=0.376$, the correlated tail is 0.997706, while the unweighted $s=-1$ column is 1.016502.",
            ha="left",
            fontsize=4.75,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.119,
            r"Control: at $r=0.377$, the inherited common-slope large sector is 1.003041; this is a sufficient-bound failure only.",
            ha="left",
            fontsize=4.75,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.088,
            "Scope: reduced canonical edge generating system; sampled weights validate presentation, not the all-order theorem.",
            ha="left",
            fontsize=4.65,
            color=MUTED,
        )
        figure.text(
            0.984,
            0.038,
            "R0.46 | exact rational certificate | 2026-08-19",
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
