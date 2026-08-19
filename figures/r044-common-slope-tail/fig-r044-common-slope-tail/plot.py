#!/usr/bin/env python3
"""Render the R0.44 common-slope active-tail journal figure."""

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


def lollipop(
    axis,
    y: float,
    start: float,
    value: float,
    color: str,
    marker: str,
    filled: bool,
) -> None:
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
    envelope = rows("common-slope-envelope.csv")
    bridge = rows("slope-loss-bridge.csv")
    controls = rows("radius-controls.csv")
    gates = rows("proof-gates.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r044-common-slope-tail"
        figure = plt.figure(figsize=(178 / 25.4, 140 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(1.04, 0.96),
            height_ratios=(1.0, 1.0),
            left=0.145,
            right=0.974,
            bottom=0.252,
            top=0.883,
            wspace=0.44,
            hspace=0.61,
        )
        envelope_axis = figure.add_subplot(grid[0, 0])
        bridge_axis = figure.add_subplot(grid[0, 1])
        control_axis = figure.add_subplot(grid[1, 0])
        gate_axis = figure.add_subplot(grid[1, 1])

        envelope_axis.set_title(
            r"(a) Complete common-slope envelope at $r=0.370$",
            loc="left",
            pad=5,
        )
        slopes = [float(Fraction(row["slopeExact"])) for row in envelope]
        bounds = [float(Fraction(row["boundExact"])) for row in envelope]
        envelope_axis.plot(slopes, bounds, color=BLUE, linewidth=1.05)
        envelope_axis.scatter(
            slopes[::25],
            bounds[::25],
            s=6,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=0.42,
            zorder=4,
        )
        endpoint_indices = [
            index for index, row in enumerate(envelope) if row["isEndpoint"] == "true"
        ]
        for index, marker, color in zip(endpoint_indices, ["o", "D"], [GOLD, BLUE]):
            envelope_axis.scatter(
                [slopes[index]],
                [bounds[index]],
                s=34,
                marker=marker,
                facecolor=PALE_GOLD if color == GOLD else PALE_BLUE,
                edgecolor=color,
                linewidth=0.9,
                zorder=6,
            )
        envelope_axis.text(
            0.035,
            bounds[0] + 0.018,
            f"H(0) = {bounds[0]:.6f}",
            fontsize=4.75,
            color=GOLD,
        )
        envelope_axis.text(
            1.965,
            bounds[-1] - 0.030,
            f"H(2) = {bounds[-1]:.6f}",
            ha="right",
            fontsize=4.75,
            color=BLUE,
        )
        envelope_axis.axhline(1, color=INK, linewidth=0.72, linestyle=(0, (4, 2)))
        envelope_axis.text(1.98, 1.012, "threshold 1", ha="right", fontsize=4.45, color=INK)
        envelope_axis.set_xlim(0, 2)
        envelope_axis.set_ylim(0.43, 1.035)
        envelope_axis.set_xticks([0, 0.5, 1, 1.5, 2])
        envelope_axis.set_xlabel(r"shared input slope $x=s/j$")
        envelope_axis.set_ylabel(r"positive column envelope $H_r(x)$")
        envelope_axis.grid(axis="y", color=GRID, linewidth=0.40)

        bridge_axis.set_title("(b) Removed termwise slope loss", loc="left", pad=5)
        old_total = sum(float(row["legacyDecimal"]) for row in bridge)
        reductions = [float(row["reductionDecimal"]) for row in bridge]
        new_total = old_total - sum(reductions)
        labels = ["R0.43", *[row["baseChargeGroup"] for row in bridge], "common x"]
        x_positions = list(range(len(labels)))
        bottom_floor = 0.94
        bottoms = [bottom_floor]
        heights = [old_total - bottom_floor]
        facecolors = ["white"]
        edgecolors = [INK]
        running = old_total
        for reduction in reductions:
            next_value = running - reduction
            bottoms.append(next_value)
            heights.append(reduction)
            facecolors.append(PALE_GOLD)
            edgecolors.append(GOLD)
            running = next_value
        bottoms.append(bottom_floor)
        heights.append(new_total - bottom_floor)
        facecolors.append(PALE_BLUE)
        edgecolors.append(BLUE)
        bridge_axis.bar(
            x_positions,
            heights,
            bottom=bottoms,
            width=0.62,
            color=facecolors,
            edgecolor=edgecolors,
            linewidth=0.85,
        )
        running = old_total
        bridge_axis.text(0, old_total + 0.010, f"{old_total:.6f}", ha="center", fontsize=4.7, color=INK)
        for index, reduction in enumerate(reductions, start=1):
            next_value = running - reduction
            bridge_axis.plot(
                [index - 0.69, index - 0.31],
                [running, running],
                color=MUTED,
                linewidth=0.45,
            )
            if reduction > 0.001:
                bridge_axis.text(
                    index,
                    next_value - 0.009,
                    f"−{reduction:.6f}",
                    ha="center",
                    va="top",
                    fontsize=4.0,
                    color=GOLD,
                )
            else:
                bridge_axis.text(
                    index,
                    running + 0.008,
                    "0" if reduction == 0 else f"−{reduction:.6f}",
                    ha="center",
                    fontsize=3.9,
                    color=MUTED,
                )
            running = next_value
        bridge_axis.text(
            len(labels) - 1,
            new_total - 0.014,
            f"{new_total:.6f}",
            ha="center",
            va="top",
            fontsize=4.7,
            color=BLUE,
        )
        bridge_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        bridge_axis.text(6.35, 1.008, "threshold 1", ha="right", fontsize=4.45, color=INK)
        bridge_axis.set_xlim(-0.55, len(labels) - 0.45)
        bridge_axis.set_ylim(bottom_floor, 1.235)
        bridge_axis.set_xticks(x_positions)
        bridge_axis.set_xticklabels(labels, rotation=28, ha="right", fontsize=4.3)
        bridge_axis.set_ylabel("focused all-order bound")
        bridge_axis.grid(axis="y", color=GRID, linewidth=0.40)

        control_axis.set_title("(c) Three exact radius controls", loc="left", pad=5)
        series_order = [
            "common large sector",
            "finite s=-1 / complete tail",
            "canonical stretch",
        ]
        styles = {
            "common large sector": (BLUE, "o", "common large"),
            "finite s=-1 / complete tail": (GOLD, "D", r"finite $s=-1$ / tail"),
            "canonical stretch": (INK, "s", "canonical stretch"),
        }
        radius_order = [0.331, 0.370, 0.371]
        control_positions = [0, 1, 2]
        for series in series_order:
            selected = [row for row in controls if row["series"] == series]
            values_by_radius = {
                round(float(row["radiusDecimal"]), 3): float(row["boundDecimal"])
                for row in selected
            }
            values = [values_by_radius[round(radius, 3)] for radius in radius_order]
            color, marker, label = styles[series]
            control_axis.plot(
                control_positions,
                values,
                color=color,
                linewidth=0.80,
                linestyle=(0, (4, 2)) if series == "canonical stretch" else "solid",
            )
            control_axis.scatter(
                control_positions,
                values,
                s=27,
                marker=marker,
                facecolor="white" if series == "canonical stretch" else color,
                edgecolor=color,
                linewidth=0.85,
                label=label,
                zorder=5,
            )
            for x_value, y_value in zip(control_positions, values):
                control_axis.text(
                    x_value,
                    y_value + (0.008 if series != "canonical stretch" else -0.014),
                    f"{y_value:.6f}",
                    ha="center",
                    va="bottom" if series != "canonical stretch" else "top",
                    fontsize=3.8,
                    color=color,
                )
        control_axis.axhline(1, color=INK, linewidth=0.75, linestyle=(0, (4, 2)))
        control_axis.text(2.0, 1.008, "threshold 1", ha="right", fontsize=4.45, color=INK)
        control_axis.set_xlim(-0.16, 2.16)
        control_axis.set_ylim(0.74, 1.025)
        control_axis.set_xticks(control_positions)
        control_axis.set_xticklabels(["entry\n0.331", "target\n0.370", "probe\n0.371"])
        control_axis.set_ylabel("all-order bound")
        control_axis.legend(loc="lower right", frameon=False, fontsize=4.15)
        control_axis.grid(axis="y", color=GRID, linewidth=0.40)

        gate_axis.set_title(r"(d) Complete proof gates at $r=0.370$", loc="left", pad=5)
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
        gate_axis.set_xlim(0.90, 1.63)
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
        gate_axis.set_xlabel("focused bound; direct transport is not a gate")
        gate_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (envelope_axis, bridge_axis, control_axis, gate_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.44 common-slope active-tail diagnostics",
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
            r"Exact GMP bounds; one shared $x=s/j$ replaces independent termwise slope maxima in the complete positive sum",
            ha="left",
            fontsize=5.55,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.181,
            r"Theorem: the positive envelope $H_r(x)=\sum c_{iq}d_i\beta_q|ix-q|/3$ is convex on $0\leq x\leq2$.",
            ha="left",
            fontsize=5.0,
            color=INK,
        )
        figure.text(
            0.145,
            0.150,
            r"Target: $r=0.370$ closes at 0.997012; the worst sector is now finite charge $s=-1$, not $s\geq241$.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.119,
            r"Control: at $r=0.371$ the common large sector is 0.971401, while the inherited $s=-1$ column is 1.000856.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.145,
            0.088,
            "Scope: reduced canonical edge generating system; finite breakpoint and column checks validate code, not the theorem.",
            ha="left",
            fontsize=4.75,
            color=MUTED,
        )
        figure.text(
            0.984,
            0.038,
            "R0.44 | exact rational certificate | 2026-08-19",
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
