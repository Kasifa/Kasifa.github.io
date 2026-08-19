#!/usr/bin/env python3
"""Render the R0.43 charge-implied degree-floor journal figure."""

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
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def add_blossom(figure) -> None:
    center = (0.948, 0.947)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        petal = Ellipse(
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
        figure.add_artist(petal)
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


def lollipop(axis, y: float, start: float, value: float, color: str, marker: str, filled: bool) -> None:
    axis.hlines(y, start, value, color=color, linewidth=0.86)
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
    support = rows("support-geometry.csv")
    bridge = rows("large-sector-bridge.csv")
    gates = rows("proof-gates.csv")
    boundary = rows("boundary-bracket.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r043-charge-degree-floor"
        figure = plt.figure(figsize=(178 / 25.4, 140 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(1.02, 0.98),
            height_ratios=(1.0, 1.0),
            left=0.145,
            right=0.974,
            bottom=0.252,
            top=0.883,
            wspace=0.39,
            hspace=0.61,
        )
        support_axis = figure.add_subplot(grid[0, 0])
        bridge_axis = figure.add_subplot(grid[0, 1])
        gate_axis = figure.add_subplot(grid[1, 0])
        boundary_axis = figure.add_subplot(grid[1, 1])

        support_axis.set_title("(a) Support-implied input degree", loc="left", pad=5)
        charges = [int(row["input_charge"]) for row in support]
        cone = [int(row["cone_degree_floor"]) for row in support]
        lattice = [int(row["minimum_bivariate_degree"]) for row in support]
        support_axis.axhline(
            81,
            color=MUTED,
            linewidth=0.70,
            linestyle=(0, (2, 2)),
        )
        support_axis.text(235.2, 82.2, "generic tail floor 81", fontsize=4.55, color=MUTED)
        support_axis.plot(
            charges,
            cone,
            color=GOLD,
            linewidth=0.90,
            linestyle=(0, (4, 2)),
            label=r"cone floor $\lceil s/2\rceil$",
        )
        support_axis.step(
            charges,
            lattice,
            where="mid",
            color=BLUE,
            linewidth=1.08,
            label="exact bivariate lattice minimum",
        )
        support_axis.scatter(
            charges,
            lattice,
            s=8,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.55,
            zorder=5,
        )
        support_axis.axvline(241, color=INK, linewidth=0.72, linestyle=(0, (4, 2)))
        support_axis.scatter(
            [241],
            [121],
            s=31,
            marker="D",
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.9,
            zorder=6,
        )
        support_axis.text(241.6, 116.0, r"$S=241\Rightarrow J_S=121$", fontsize=4.75, color=INK)
        support_axis.set_xlim(235, 255)
        support_axis.set_ylim(78, 132)
        support_axis.set_xticks([235, 241, 245, 250, 255])
        support_axis.set_yticks([81, 100, 121, 130])
        support_axis.set_xlabel(r"positive input charge $s$")
        support_axis.set_ylabel(r"minimum input degree $j$")
        support_axis.legend(loc="upper left", frameon=False, fontsize=4.45)
        support_axis.grid(axis="y", color=GRID, linewidth=0.40)

        bridge_axis.set_title("(b) Large-sector bound bridge", loc="left", pad=5)
        values = [float(Fraction(row["exact"])) for row in bridge]
        labels = [row["component"] for row in bridge]
        cumulative = values[0]
        bottoms = [0.9975]
        heights = [values[0] - bottoms[0]]
        colors = [INK]
        for delta in values[1:-1]:
            next_value = cumulative + delta
            bottoms.append(min(cumulative, next_value))
            heights.append(abs(delta))
            colors.append(GOLD)
            cumulative = next_value
        bottoms.append(0.9975)
        heights.append(values[-1] - 0.9975)
        colors.append(BLUE)
        x_positions = list(range(len(values)))
        bridge_axis.bar(
            x_positions,
            heights,
            bottom=bottoms,
            width=0.62,
            color=[PALE_GOLD if color == GOLD else (PALE_BLUE if color == BLUE else "white") for color in colors],
            edgecolor=colors,
            linewidth=0.85,
        )
        running = values[0]
        bridge_axis.hlines(running, 0.31, 0.69, color=INK, linewidth=0.65)
        for index, delta in enumerate(values[1:-1], start=1):
            next_value = running + delta
            bridge_axis.plot(
                [index - 0.69, index - 0.31],
                [running, running],
                color=MUTED,
                linewidth=0.45,
            )
            bridge_axis.text(
                index,
                min(running, next_value) - 0.00010,
                f"{delta:.6f}",
                ha="center",
                va="top",
                fontsize=4.0,
                color=GOLD,
            )
            running = next_value
        bridge_axis.text(0, values[0] + 0.00014, f"{values[0]:.6f}", ha="center", fontsize=4.7, color=INK)
        bridge_axis.text(
            len(values) - 1,
            values[-1] - 0.00016,
            f"{values[-1]:.6f}",
            ha="center",
            va="top",
            fontsize=4.7,
            color=BLUE,
        )
        bridge_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        bridge_axis.text(6.38, 1.00010, "threshold 1", ha="right", fontsize=4.45, color=INK)
        bridge_axis.set_xlim(-0.55, len(values) - 0.45)
        bridge_axis.set_ylim(0.9975, 1.00345)
        bridge_axis.set_xticks(x_positions)
        bridge_axis.set_xticklabels(labels, rotation=28, ha="right", fontsize=4.45)
        bridge_axis.set_ylabel("focused all-order bound")
        bridge_axis.grid(axis="y", color=GRID, linewidth=0.40)

        gate_axis.set_title(r"(c) Complete gates at $r=0.330$", loc="left", pad=5)
        target_rows = [row for row in gates if row["stage"] == "target"]
        positions = {"active tail": 2, "direct transport": 1, "canonical stretch": 0}
        styles = {
            "active tail": (GOLD, "D", True),
            "direct transport": (INK, "s", False),
            "canonical stretch": (BLUE, "o", True),
        }
        for row in target_rows:
            gate = row["gate"]
            value = float(row["decimal"])
            color, marker, filled = styles[gate]
            y = positions[gate]
            lollipop(gate_axis, y, 0, value, color, marker, filled)
            gate_axis.text(value + 0.025, y, f"{value:.6f}", va="center", fontsize=4.85, color=color)
        gate_axis.axvline(1, color=INK, linewidth=0.76, linestyle=(0, (4, 2)))
        gate_axis.text(1.012, 2.30, "threshold 1", fontsize=4.75, color=INK)
        gate_axis.set_xlim(0, 1.39)
        gate_axis.set_ylim(-0.45, 2.45)
        gate_axis.set_yticks([0, 1, 2])
        gate_axis.set_yticklabels(["canonical stretch", "direct transport", "active tail"])
        gate_axis.set_xlabel("all-order bound")
        gate_axis.grid(axis="x", color=GRID, linewidth=0.40)

        boundary_axis.set_title("(d) Adjacent tail-bound bracket", loc="left", pad=5)
        boundary_labels = [
            r"improved, $r=0.329$",
            r"legacy, $r=0.330$",
            r"improved, $r=0.330$",
            r"improved, $r=0.331$",
        ]
        y_positions = [3, 2, 1, 0]
        for row, label, y in zip(boundary, boundary_labels, y_positions):
            value = float(row["decimal"])
            improved = row["method"] == "improved"
            passes = row["status"] == "passes"
            color = BLUE if improved else GOLD
            marker = "o" if improved else "s"
            lollipop(boundary_axis, y, 0.992, value, color, marker, passes)
            boundary_axis.text(
                value - 0.00020 if value > 1 else value + 0.00018,
                y,
                f"{value:.6f}",
                ha="right" if value > 1 else "left",
                va="center",
                fontsize=4.55,
                color=color,
            )
        boundary_axis.axvline(1, color=INK, linewidth=0.76, linestyle=(0, (4, 2)))
        boundary_axis.text(0.99984, 3.34, "threshold 1", ha="right", fontsize=4.6, color=INK)
        boundary_axis.set_xlim(0.992, 1.0054)
        boundary_axis.set_ylim(-0.45, 3.48)
        boundary_axis.set_yticks(y_positions)
        boundary_axis.set_yticklabels(boundary_labels)
        boundary_axis.set_xlabel("focused active-tail bound")
        boundary_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (support_axis, bridge_axis, gate_axis, boundary_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.43 charge-implied degree-floor diagnostics",
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
            r"Exact GMP bounds; $s\geq241$ and $s\leq2j$ sharpen the uniform input floor from 81 to 121",
            ha="left",
            fontsize=5.7,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.181,
            r"Theorem: $j\geq\max\{N+1,\lceil S/2\rceil\}$ lowers only the positive large-charge degree prefactor.",
            ha="left",
            fontsize=5.05,
            color=INK,
        )
        figure.text(
            0.145,
            0.150,
            r"Target: legacy 1.002872 becomes 0.998881 at $r=0.330$; all active and canonical-stretch gates close.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.119,
            r"Regression: 21 finite exact large-charge columns lie below the analytic sector bound; they do not prove it.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.088,
            "Scope: reduced canonical edge generating system, not the full three-dimensional Navier-Stokes equation.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.984,
            0.038,
            "R0.43 | exact rational certificate | 2026-08-19",
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
