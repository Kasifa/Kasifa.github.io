#!/usr/bin/env python3
"""Render Figure R0.64-1 at double-column journal size."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
PALE_BLUE = "#dce8ef"
PALE_RUST = "#eddeda"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def state_box(axis, xy, width, height, title, detail, facecolor, edgecolor) -> None:
    box = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.025",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=0.8,
    )
    axis.add_patch(box)
    axis.text(xy[0] + width / 2, xy[1] + height * 0.63, title, ha="center", va="center", fontsize=5.35, color=INK)
    axis.text(xy[0] + width / 2, xy[1] + height * 0.27, detail, ha="center", va="center", fontsize=3.45, color=MUTED)


def draw() -> None:
    spectrum = rows("cycle-spectrum.csv")
    reachable = rows("reachable-cycle.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r064-supercritical-cycle"
        figure = plt.figure(figsize=(178 / 25.4, 96 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.066,
            right=0.957,
            bottom=0.19,
            top=0.79,
            width_ratios=(1.08, 1.0),
            hspace=0.62,
            wspace=0.34,
        )
        transfer_axis = figure.add_subplot(grid[:, 0])
        spectrum_axis = figure.add_subplot(grid[0, 1])
        growth_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "A zero-time digit cycle exceeds the factor-two threshold",
            x=0.066,
            y=0.946,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.066,
            0.888,
            "Exact integer transfer  ·  word 0100 (least-significant bit first)  ·  integrated heat-weighted estimate remains open",
            ha="left",
            fontsize=3.9,
            color=MUTED,
        )

        transfer_axis.set_title("(a) Exact cycle reduction", loc="left", pad=4)
        transfer_axis.set_xlim(0, 1)
        transfer_axis.set_ylim(0, 1)
        transfer_axis.axis("off")
        state_box(transfer_axis, (0.10, 0.75), 0.80, 0.14, "48 exact states", r"2 target $\times$ 8 cubic $\times$ 3 carries", PALE_BLUE, BLUE)
        state_box(transfer_axis, (0.10, 0.47), 0.80, 0.14, r"$W=T_0T_0T_1T_0$", "four binary levels; exact rank 6", PALE_BLUE, BLUE)
        state_box(transfer_axis, (0.10, 0.19), 0.80, 0.14, r"$\lambda\in(25,26)$", r"$\lambda=25.151589\ldots>16=2^4$", PALE_RUST, RUST)
        for start, end in (((0.5, 0.74), (0.5, 0.62)), ((0.5, 0.46), (0.5, 0.34))):
            transfer_axis.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=8, color=INK, linewidth=0.7))
        transfer_axis.text(0.5, 0.675, "select word 0100", ha="center", va="center", fontsize=3.5, color=MUTED)
        transfer_axis.text(0.5, 0.395, "exact image characteristic polynomial", ha="center", va="center", fontsize=3.5, color=MUTED)
        transfer_axis.text(
            0.5,
            0.065,
            "Consequence: no common full-state norm with\n$\|T_0\|,\|T_1\|\leq2$ at zero heat time",
            ha="center",
            va="center",
            fontsize=3.75,
            color=GOLD,
        )

        eigenvalues = [float(row["eigenvalueDisplayOnly"]) for row in spectrum]
        multiplicities = [int(row["multiplicity"]) for row in spectrum]
        expanded = []
        for eigenvalue, multiplicity in zip(eigenvalues, multiplicities):
            expanded.extend([eigenvalue] * multiplicity)
        y_positions = list(range(1, len(expanded) + 1))
        colors = [RUST if value > 16 else BLUE for value in expanded]
        spectrum_axis.set_title("(b) Nonzero spectrum of the 4-step product", loc="left", pad=4)
        spectrum_axis.axvline(16, color=INK, linewidth=0.7, linestyle=(0, (3, 2)))
        spectrum_axis.scatter(expanded, y_positions, s=13, facecolors="white", edgecolors=colors, linewidths=0.8, zorder=3)
        spectrum_axis.set_xlim(-15, 28)
        spectrum_axis.set_ylim(0.3, 6.7)
        spectrum_axis.set_yticks([])
        spectrum_axis.set_xlabel("real eigenvalue")
        spectrum_axis.grid(axis="x", color=GRID, linewidth=0.3)
        spectrum_axis.text(16, 6.38, r"$2^4=16$", ha="center", va="bottom", fontsize=3.4, color=INK)
        spectrum_axis.annotate(
            r"$25.151589\ldots$",
            xy=(max(expanded), y_positions[expanded.index(max(expanded))]),
            xytext=(20.4, 5.9),
            fontsize=3.55,
            color=RUST,
            arrowprops={"arrowstyle": "-", "color": RUST, "linewidth": 0.55},
        )

        r_values = [int(row["r"]) for row in reachable if int(row["r"]) >= 1]
        growth = [float(row["observedBlockGrowth"]) for row in reachable if int(row["r"]) >= 1]
        dominant = 25.151589334101537
        growth_axis.set_title("(c) Reachable target-cycle growth", loc="left", pad=4)
        growth_axis.plot(
            r_values,
            growth,
            color=BLUE,
            linewidth=0.85,
            marker="o",
            markerfacecolor="white",
            markeredgewidth=0.5,
            markersize=2.25,
        )
        growth_axis.axhline(16, color=INK, linewidth=0.7, linestyle=(0, (3, 2)), label=r"threshold $16$")
        growth_axis.axhline(dominant, color=RUST, linewidth=0.7, linestyle=(0, (5, 2)), label=r"$\lambda$")
        growth_axis.set_xlim(1, 30)
        growth_axis.set_ylim(0, 29)
        growth_axis.set_xlabel(r"cycle count $r$ ($M=16^r$)")
        growth_axis.set_ylabel(r"$|y_r|^{1/r}$")
        growth_axis.grid(color=GRID, linewidth=0.3)
        growth_axis.legend(loc="lower right", frameon=False, fontsize=3.3, handlelength=2.2)

        figure.text(
            0.066,
            0.06,
            "Interpretation: the supercritical mode is exact and reachable, so pointwise full-state contraction is impossible. Heat weighting and simplex integration must be retained before taking a norm.",
            ha="left",
            va="top",
            fontsize=3.65,
            color=MUTED,
        )
        figure.savefig(HERE / "figure.pdf")
        figure.savefig(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")


if __name__ == "__main__":
    draw()

