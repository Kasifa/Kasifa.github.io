#!/usr/bin/env python3
"""Render the R0.45 fixed-negative-charge journal figure."""

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
        petal = Ellipse(
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
        figure.add_artist(petal)
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK, zorder=21)


def lollipop(axis, y: float, start: float, value: float, color: str, marker: str, filled: bool) -> None:
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
    curve = rows("negative-charge-curve.csv")
    derivative = rows("derivative-certificate.csv")
    controls = rows("radius-controls.csv")
    gates = rows("proof-gates.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r045-fixed-negative-charge"
        figure = plt.figure(figsize=(178 / 25.4, 140 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(1.05, 0.95),
            height_ratios=(1.0, 1.0),
            left=0.145,
            right=0.974,
            bottom=0.252,
            top=0.883,
            wspace=0.44,
            hspace=0.61,
        )
        curve_axis = figure.add_subplot(grid[0, 0])
        derivative_axis = figure.add_subplot(grid[0, 1])
        control_axis = figure.add_subplot(grid[1, 0])
        gate_axis = figure.add_subplot(grid[1, 1])

        curve_axis.set_title(r"(a) Exact $s=-1$ column on $0\leq t\leq1/82$", loc="left", pad=5)
        curve_styles = {
            "target 0.371": (BLUE, "o", r"target $r=0.371$"),
            "probe 0.372": (GOLD, "D", r"probe $r=0.372$"),
        }
        for label, (color, marker, legend) in curve_styles.items():
            selected = [row for row in curve if row["radiusLabel"] == label]
            x_values = [float(Fraction(row["inverseDegreeExact"])) for row in selected]
            y_values = [float(Fraction(row["columnExact"])) for row in selected]
            curve_axis.plot(x_values, y_values, color=color, linewidth=1.0, label=legend)
            curve_axis.scatter(
                [x_values[-1]],
                [y_values[-1]],
                s=34,
                marker=marker,
                facecolor=PALE_BLUE if color == BLUE else PALE_GOLD,
                edgecolor=color,
                linewidth=0.9,
                zorder=6,
            )
            curve_axis.text(
                x_values[-1] - 0.00015,
                y_values[-1] + (0.00065 if color == BLUE else 0.00050),
                f"{y_values[-1]:.6f}",
                ha="right",
                fontsize=4.45,
                color=color,
            )
        curve_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        curve_axis.text(0.0003, 1.00045, "threshold 1", fontsize=4.45, color=INK)
        curve_axis.set_xlim(0, 1 / 82 + 0.00015)
        curve_axis.set_ylim(0.976, 1.0032)
        curve_axis.set_xticks([0, 0.004, 0.008, 1 / 82])
        curve_axis.set_xticklabels(["0", "0.004", "0.008", "1/82"])
        curve_axis.set_xlabel(r"inverse tail degree $t=1/j$")
        curve_axis.set_ylabel(r"exact weighted column $F_r(t)$")
        curve_axis.legend(loc="lower right", frameon=False, fontsize=4.2)
        curve_axis.grid(axis="y", color=GRID, linewidth=0.40)

        derivative_axis.set_title(r"(b) Derivative lower bound at $r=0.371$", loc="left", pad=5)
        selected = {
            row["component"]: float(Fraction(row["valueExact"]))
            for row in derivative
            if row["control"] == "target 0.371"
        }
        components = ["q=1 obstruction", "q=2 seed", "certified margin"]
        labels = [r"$\widehat Q_r(1/82)$", r"seed lower $3r$", r"margin $3r-\widehat Q_r$"]
        colors = [GOLD, BLUE, INK]
        markers = ["o", "D", "s"]
        fills = [False, True, False]
        y_positions = [2, 1, 0]
        for component, y, color, marker, filled in zip(components, y_positions, colors, markers, fills):
            value = selected[component]
            lollipop(derivative_axis, y, 0, value, color, marker, filled)
            derivative_axis.text(value + 0.035, y, f"{value:.6f}", va="center", fontsize=4.6, color=color)
        derivative_axis.set_xlim(0, 1.25)
        derivative_axis.set_ylim(-0.55, 2.55)
        derivative_axis.set_yticks(y_positions)
        derivative_axis.set_yticklabels(labels)
        derivative_axis.set_xlabel("exact derivative bound")
        derivative_axis.text(
            0.02,
            -0.36,
            r"$F'_r(t)\geq 0.944352>0$ for every $0\leq t\leq1/82$",
            fontsize=4.45,
            color=INK,
        )
        derivative_axis.grid(axis="x", color=GRID, linewidth=0.40)

        control_axis.set_title("(c) Consecutive exact radius controls", loc="left", pad=5)
        radius_order = [0.370, 0.371, 0.372]
        x_positions = [0, 1, 2]
        styles = {
            "exact s=-1": (GOLD, "D", "solid", r"exact $s=-1$"),
            "common large sector": (BLUE, "o", "solid", "common large"),
            "canonical stretch": (INK, "s", (0, (4, 2)), "canonical stretch"),
        }
        for series, (color, marker, line_style, label) in styles.items():
            selected_rows = [row for row in controls if row["series"] == series]
            values_by_radius = {
                round(float(row["radiusDecimal"]), 3): float(row["boundDecimal"])
                for row in selected_rows
            }
            values = [values_by_radius[radius] for radius in radius_order]
            control_axis.plot(x_positions, values, color=color, linewidth=0.82, linestyle=line_style)
            control_axis.scatter(
                x_positions,
                values,
                s=27,
                marker=marker,
                facecolor="white" if series == "canonical stretch" else color,
                edgecolor=color,
                linewidth=0.85,
                label=label,
                zorder=5,
            )
        old = next(row for row in controls if row["series"] == "R0.44 inherited s=-1")
        old_value = float(old["boundDecimal"])
        control_axis.scatter([1], [old_value], s=36, marker="x", color=INK, linewidth=1.0, zorder=7)
        control_axis.annotate(
            "R0.44 old 1.000856",
            xy=(1, old_value),
            xytext=(0.36, 1.012),
            fontsize=3.9,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": MUTED, "linewidth": 0.45},
        )
        exact_target = next(
            float(row["boundDecimal"])
            for row in controls
            if row["series"] == "exact s=-1" and row["control"] == "target"
        )
        control_axis.text(1.03, exact_target - 0.0020, f"exact {exact_target:.6f}", fontsize=3.9, color=GOLD)
        control_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        control_axis.text(2.0, 1.0017, "threshold 1", ha="right", fontsize=4.35, color=INK)
        control_axis.set_xlim(-0.16, 2.16)
        control_axis.set_ylim(0.955, 1.019)
        control_axis.set_xticks(x_positions)
        control_axis.set_xticklabels(["entry\n0.370", "target\n0.371", "probe\n0.372"])
        control_axis.set_ylabel("focused all-order bound")
        control_axis.legend(loc="lower right", frameon=False, fontsize=4.0)
        control_axis.grid(axis="y", color=GRID, linewidth=0.40)

        gate_axis.set_title(r"(d) Complete proof gates at $r=0.371$", loc="left", pad=5)
        y_positions = list(reversed(range(len(gates))))
        for row, y in zip(gates, y_positions):
            value = float(row["boundDecimal"])
            formal = row["classification"] == "formal gate"
            color = BLUE if formal and row["gate"] == "canonical stretch" else (GOLD if formal else INK)
            marker = "o" if formal else "s"
            lollipop(gate_axis, y, 0.90, value, color, marker, formal)
            gate_axis.text(
                value + 0.012 if value < 1.3 else value - 0.018,
                y,
                f"{value:.6f}",
                ha="left" if value < 1.3 else "right",
                va="center",
                fontsize=4.45,
                color=color,
            )
        gate_axis.axvline(1, color=INK, linewidth=0.76, linestyle=(0, (4, 2)))
        gate_axis.text(1.012, 4.32, "threshold 1", fontsize=4.55, color=INK)
        gate_axis.set_xlim(0.90, 1.65)
        gate_axis.set_ylim(-0.45, 4.48)
        gate_axis.set_yticks(y_positions)
        gate_labels = {
            "active tail": "active tail",
            "ball mapping / radius": "mapping / ball",
            "Lipschitz": "Lipschitz",
            "canonical stretch": "canonical stretch",
            "old direct transport": "direct transport (old)",
        }
        gate_axis.set_yticklabels([gate_labels[row["gate"]] for row in gates])
        gate_axis.set_xlabel("focused bound; direct transport is diagnostic")
        gate_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (curve_axis, derivative_axis, control_axis, gate_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.45 fixed negative-charge tail diagnostics",
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
            r"Exact GMP bounds; a derivative theorem replaces the inherited separated estimate for the complete $s=-1$ column",
            ha="left",
            fontsize=5.45,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.181,
            r"Theorem: $F'_r(t)\geq3r-\widehat Q_r(1/82)>0$ on $0\leq t\leq1/82$; therefore the exact maximum is $j=82$.",
            ha="left",
            fontsize=4.95,
            color=INK,
        )
        figure.text(
            0.145,
            0.150,
            r"Target: $r=0.371$ closes at 0.997228; the inherited R0.44 estimate 1.000856 was not the exact induced column.",
            ha="left",
            fontsize=4.80,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.119,
            r"Control: at $r=0.372$ the exact $j=82,s=-1$ column is 1.001062, while the common large sector remains 0.976614.",
            ha="left",
            fontsize=4.80,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.088,
            "Scope: reduced canonical edge generating system; sampled curves validate presentation, not the all-order theorem.",
            ha="left",
            fontsize=4.70,
            color=MUTED,
        )
        figure.text(
            0.984,
            0.038,
            "R0.45 | exact rational certificate | 2026-08-19",
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
