#!/usr/bin/env python3
"""Render the R0.42 canonical-stretch journal figure."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt


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


def lollipop(axis, y: float, value: float, color: str, marker: str, filled: bool) -> None:
    axis.hlines(y, 0, value, color=color, linewidth=0.86)
    axis.scatter(
        [value],
        [y],
        s=28,
        marker=marker,
        facecolor=color if filled else "white",
        edgecolor=color,
        linewidth=0.9,
        zorder=5,
    )


def draw() -> None:
    radius_data = rows("radius-gain.csv")
    gate_data = rows("proof-gates.csv")
    endpoint_data = rows("endpoint-decomposition.csv")
    normalized = {
        (row["quantity"], row["version"]): float(
            Fraction(row["normalized_to_r031"])
        )
        for row in radius_data
    }

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r042-canonical-stretch"
        figure = plt.figure(figsize=(178 / 25.4, 140 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            width_ratios=(0.96, 1.04),
            height_ratios=(1.0, 1.0),
            left=0.150,
            right=0.974,
            bottom=0.252,
            top=0.883,
            wspace=0.40,
            hspace=0.61,
        )
        radius_axis = figure.add_subplot(grid[0, 0])
        acceptance_axis = figure.add_subplot(grid[0, 1])
        target_axis = figure.add_subplot(grid[1, 0])
        boundary_axis = figure.add_subplot(grid[1, 1])

        radius_axis.set_title("(a) Certified radius ladder", loc="left", pad=5)
        versions = ["R0.31", "R0.37", "R0.38", "R0.39", "R0.40", "R0.41", "R0.42"]
        markers = ["o", "s", "D", "P", "X", "^", "*"]
        colors = [MUTED, BLUE, GOLD, MUTED, BLUE, INK, GOLD]
        fills = ["white", PALE_BLUE, PALE_GOLD, "white", PALE_BLUE, INK, PALE_GOLD]
        offsets = [0.42, 0.28, 0.14, 0.0, -0.14, -0.28, -0.42]
        for quantity, y_base, label in (
            ("common_radius", 1.0, r"common $r$"),
            ("fixed_charge_radius", 0.0, r"fixed-charge $r^3$"),
        ):
            for version, marker, color, fill, offset in zip(
                versions, markers, colors, fills, offsets
            ):
                value = normalized[(quantity, version)]
                y = y_base + offset
                radius_axis.hlines(y, 0.93, value, color=color, linewidth=0.76)
                radius_axis.scatter(
                    [value],
                    [y],
                    s=25 if version != "R0.42" else 34,
                    marker=marker,
                    facecolor=fill,
                    edgecolor=color,
                    linewidth=0.86,
                    zorder=5,
                )
                radius_axis.text(
                    value * 1.075,
                    y,
                    f"{version} {value:.2f}",
                    va="center",
                    fontsize=4.45,
                    color=color,
                )
        radius_axis.axvline(1, color=INK, linewidth=0.72, linestyle=(0, (4, 2)))
        radius_axis.set_xscale("log")
        radius_axis.set_xlim(0.88, 360)
        radius_axis.set_ylim(-0.52, 1.52)
        radius_axis.set_yticks([0, 1])
        radius_axis.set_yticklabels([r"fixed-charge $r^3$", r"common $r$"])
        radius_axis.set_xlabel("normalized to R0.31")
        radius_axis.set_xticks([1, 4, 16, 64, 256])
        radius_axis.set_xticklabels(["1", "4", "16", "64", "256"])
        radius_axis.grid(axis="x", which="major", color=GRID, linewidth=0.40)

        acceptance_axis.set_title(
            r"(b) Preassigned acceptance at $r=0.282$",
            loc="left",
            pad=5,
        )
        acceptance = [row for row in endpoint_data if row["stage"] == "acceptance"]
        positions = {
            ("direct transport", "polynomial"): 3.0,
            ("direct transport", "total"): 2.4,
            ("canonical stretch", "polynomial"): 1.2,
            ("canonical stretch", "total"): 0.6,
        }
        labels = {
            ("direct transport", "polynomial"): "direct polynomial",
            ("direct transport", "total"): "direct + tail",
            ("canonical stretch", "polynomial"): "stretch polynomial",
            ("canonical stretch", "total"): "stretch + tail",
        }
        for row in acceptance:
            key = (row["operator"], row["component"])
            if key not in positions:
                continue
            value = float(row["decimal"])
            direct = key[0] == "direct transport"
            total = key[1] == "total"
            color = INK if direct else BLUE
            marker = "s" if direct else "o"
            y = positions[key]
            acceptance_axis.hlines(y, 0.55, value, color=color, linewidth=0.84)
            acceptance_axis.scatter(
                [value],
                [y],
                s=28,
                marker=marker,
                facecolor=color if total else "white",
                edgecolor=color,
                linewidth=0.9,
                zorder=5,
            )
            acceptance_axis.text(
                value - 0.009 if direct else value + 0.009,
                y,
                f"{value:.9f}",
                ha="right" if direct else "left",
                va="center",
                fontsize=4.65,
                color=color,
            )
        acceptance_axis.axvline(1, color=GOLD, linewidth=0.78, linestyle=(0, (4, 2)))
        acceptance_axis.text(
            0.997,
            3.37,
            "threshold 1",
            ha="right",
            fontsize=4.75,
            color=GOLD,
        )
        acceptance_axis.set_xlim(0.55, 1.022)
        acceptance_axis.set_ylim(0.28, 3.55)
        acceptance_axis.set_yticks(list(positions.values()))
        acceptance_axis.set_yticklabels([labels[key] for key in positions])
        acceptance_axis.set_xlabel("focused operator norm scale")
        acceptance_axis.grid(axis="x", color=GRID, linewidth=0.40)
        acceptance_axis.text(
            0.55,
            0.34,
            r"direct tail adds only $1.48\times10^{-7}$",
            fontsize=4.65,
            color=MUTED,
        )

        target_axis.set_title(r"(c) Target gates at $r=0.329$", loc="left", pad=5)
        target_rows = [row for row in gate_data if row["stage"] == "target"]
        target_positions = {"active tail": 2, "direct transport": 1, "canonical stretch": 0}
        gate_style = {
            "active tail": (GOLD, "D", True),
            "direct transport": (INK, "s", False),
            "canonical stretch": (BLUE, "o", True),
        }
        for row in target_rows:
            gate = row["gate"]
            value = float(row["decimal"])
            color, marker, filled = gate_style[gate]
            y = target_positions[gate]
            lollipop(target_axis, y, value, color, marker, filled)
            target_axis.text(
                value + 0.025,
                y,
                f"{value:.6f}",
                va="center",
                fontsize=4.85,
                color=color,
            )
        target_axis.axvline(1, color=INK, linewidth=0.76, linestyle=(0, (4, 2)))
        target_axis.text(1.012, 2.30, "threshold 1", fontsize=4.75)
        target_axis.set_xlim(0, 1.39)
        target_axis.set_ylim(-0.45, 2.45)
        target_axis.set_yticks([0, 1, 2])
        target_axis.set_yticklabels(["canonical stretch", "direct transport", "active tail"])
        target_axis.tick_params(axis="y", labelsize=5.35, pad=2)
        target_axis.set_xlabel("all-order bound")
        target_axis.grid(axis="x", color=GRID, linewidth=0.40)

        boundary_axis.set_title(
            "(d) Millesimal active-tail bracket",
            loc="left",
            pad=5,
        )
        boundary_rows = [
            row
            for row in gate_data
            if row["stage"] in ("target", "failure")
            and row["gate"] in ("active tail", "canonical stretch")
        ]
        boundary_positions = {
            ("target", "active tail"): 3,
            ("failure", "active tail"): 2,
            ("target", "canonical stretch"): 1,
            ("failure", "canonical stretch"): 0,
        }
        boundary_labels = {
            ("target", "active tail"): r"tail, $0.329$",
            ("failure", "active tail"): r"tail, $0.330$",
            ("target", "canonical stretch"): r"stretch, $0.329$",
            ("failure", "canonical stretch"): r"stretch $p_{80}$, $0.330$",
        }
        for row in boundary_rows:
            key = (row["stage"], row["gate"])
            value = float(row["decimal"])
            active = row["gate"] == "active tail"
            color = GOLD if active else BLUE
            marker = "D" if active else "o"
            filled = row["status"] == "passes"
            y = boundary_positions[key]
            lollipop(boundary_axis, y, value, color, marker, filled)
            near_threshold = value > 0.95
            boundary_axis.text(
                value - 0.013 if near_threshold else value + 0.011,
                y,
                f"{value:.6f}",
                ha="right" if near_threshold else "left",
                va="center",
                fontsize=4.7,
                color=color,
            )
        boundary_axis.axvline(1, color=INK, linewidth=0.76, linestyle=(0, (4, 2)))
        boundary_axis.text(
            0.996,
            3.34,
            "threshold 1",
            ha="right",
            fontsize=4.75,
        )
        boundary_axis.set_xlim(0, 1.055)
        boundary_axis.set_ylim(-0.45, 3.48)
        boundary_axis.set_yticks(list(boundary_positions.values()))
        boundary_axis.set_yticklabels([boundary_labels[key] for key in boundary_positions])
        boundary_axis.set_xlabel("bound (failure stretch is polynomial only)")
        boundary_axis.grid(axis="x", color=GRID, linewidth=0.40)

        for axis in (radius_axis, acceptance_axis, target_axis, boundary_axis):
            axis.spines["top"].set_visible(False)
            axis.spines["right"].set_visible(False)

        figure.suptitle(
            "R0.42 canonical-stretch restart diagnostics",
            x=0.150,
            y=0.956,
            ha="left",
            fontsize=10.0,
            fontweight="bold",
            color=INK,
        )
        figure.text(
            0.150,
            0.918,
            r"Exact GMP bounds; full degree and charge closure at $r_*=329/1000$",
            ha="left",
            fontsize=5.7,
            color=MUTED,
        )
        figure.text(
            0.150,
            0.181,
            r"Theorem: $S_a=\mathcal{L}^{-1}\{a,\cdot\}$ has exact convex endpoint columns and no input-degree prefactor.",
            ha="left",
            fontsize=5.05,
            color=INK,
        )
        figure.text(
            0.150,
            0.150,
            r"Finite checks: 3055 monomial pairs; five complete columns; 990 canonical-factorization checks.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.150,
            0.119,
            r"Boundary: $r=0.330$ fails the present active-tail inequality only; no singularity is inferred.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.150,
            0.088,
            "Scope: reduced canonical edge generating system, not the full three-dimensional Navier-Stokes equation.",
            ha="left",
            fontsize=4.85,
            color=MUTED,
        )
        figure.text(
            0.984,
            0.038,
            "R0.42 | exact rational certificate | 2026-08-19",
            ha="right",
            fontsize=4.65,
            color=LIGHT,
        )

        figure.savefig(PACKAGE / "figure.pdf")
        figure.savefig(PACKAGE / "figure.svg")
        figure.savefig(PACKAGE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(PACKAGE / "figure.svg")


if __name__ == "__main__":
    draw()
