#!/usr/bin/env python3
"""Render the R0.54 complete product-affine family enclosure figure."""

from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Patch, Rectangle


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_BLUE = "#dbe5ea"
PALE_GOLD = "#efe1c7"
PALE_GRAY = "#e7e3dc"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def add_blossom(figure) -> None:
    center = (0.951, 0.944)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(
            Ellipse(
                (center[0] + 0.011 * math.cos(theta), center[1] + 0.014 * math.sin(theta)),
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
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK, zorder=21)


def draw() -> None:
    domain = rows("invariant-domain.csv")
    leaves = rows("cover-leaves.csv")
    enclosure = rows("global-enclosure.csv")
    metadata = json.loads((HERE / "figure-data-metadata.json").read_text(encoding="utf-8"))

    scaled_a = [float(row["scaledADecimal"]) for row in domain]
    lower = [float(row["scaledBLowerDecimal"]) for row in domain]
    upper = [float(row["scaledBUpperDecimal"]) for row in domain]
    candidate_a = float(metadata["candidate"]["scaledA"])
    candidate_b = float(metadata["candidate"]["scaledB"])
    candidate_c = float(metadata["candidate"]["character"])
    gains = [float(row["gainPpmDecimal"]) for row in enclosure]

    cover_style = {
        "H": (PALE_BLUE, BLUE, "///"),
        "P": (PALE_GOLD, GOLD, "\\\\"),
        "Q": (PALE_GRAY, INK, ".."),
    }

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r054-product-affine-global"
        figure = plt.figure(figsize=(178 / 25.4, 112 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.102,
            right=0.974,
            bottom=0.292,
            top=0.858,
            width_ratios=(0.9, 1.1),
            wspace=0.39,
            hspace=0.69,
        )
        domain_axis = figure.add_subplot(grid[:, 0])
        gain_axis = figure.add_subplot(grid[0, 1])
        cover_axis = figure.add_subplot(grid[1, 1])
        figure.suptitle(
            "A global exact enclosure for the complete product-affine family",
            x=0.102,
            y=0.946,
            ha="left",
            fontsize=8.1,
            color=INK,
        )

        domain_axis.set_title("(a) Exact compactified invariant domain", loc="left", pad=5)
        domain_axis.fill_between(scaled_a, lower, upper, color=PALE_BLUE, alpha=0.78, linewidth=0)
        domain_axis.plot(scaled_a, upper, color=BLUE, linewidth=1.0, label=r"$S^2B=(SA)^2/4$")
        domain_axis.plot(scaled_a, lower, color=INK, linewidth=0.8, linestyle=(0, (4, 2)), label=r"$S^2B=\max(0,SA-1)$")
        domain_axis.scatter(
            [candidate_a],
            [candidate_b],
            marker="D",
            s=31,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=6,
        )
        domain_axis.annotate(
            "100-digit symmetric\ndiagnostic (not proof)",
            xy=(candidate_a, candidate_b),
            xytext=(1.02, 0.73),
            fontsize=4.0,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.48},
        )
        domain_axis.text(
            0.05,
            0.96,
            r"$0\leq SA\leq2$" + "\n" + r"$\max(0,SA-1)\leq S^2B\leq(SA)^2/4$",
            transform=domain_axis.transAxes,
            va="top",
            fontsize=4.25,
            color=INK,
        )
        domain_axis.set_xlim(0, 2.02)
        domain_axis.set_ylim(0, 1.02)
        domain_axis.set_xlabel(r"scaled sum $SA=S(\alpha+\beta)$")
        domain_axis.set_ylabel(r"scaled product $S^2B=S^2\alpha\beta$")
        domain_axis.legend(loc="lower right", frameon=False, fontsize=4.0)
        domain_axis.grid(color=GRID, linewidth=0.36)

        gain_axis.set_title("(b) Certified gain interval for the whole family", loc="left", pad=5)
        lower_gain, candidate_gain, upper_gain = gains
        gain_axis.hlines(1, lower_gain, upper_gain, color=BLUE, linewidth=5.0, alpha=0.26)
        gain_axis.hlines(1, lower_gain, upper_gain, color=BLUE, linewidth=0.9)
        gain_axis.scatter([lower_gain, upper_gain], [1, 1], marker="|", s=84, color=BLUE, linewidth=1.1, zorder=5)
        gain_axis.scatter(
            [candidate_gain],
            [1],
            marker="D",
            s=34,
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.85,
            zorder=6,
        )
        gain_axis.text(lower_gain, 1.18, f"> {lower_gain:.4f}", ha="left", fontsize=4.1, color=BLUE)
        gain_axis.text(upper_gain, 0.76, f"< {upper_gain:.4f}", ha="right", fontsize=4.1, color=BLUE)
        gain_axis.annotate(
            f"diagnostic {candidate_gain:.4f} ppm\nnot used by the theorem",
            xy=(candidate_gain, 1),
            xytext=(candidate_gain - 0.17, 1.47),
            ha="center",
            fontsize=3.95,
            color=GOLD,
            arrowprops={"arrowstyle": "-", "color": GOLD, "linewidth": 0.45},
        )
        gain_axis.text(
            0.02,
            0.03,
            r"remaining factor above R0.53 $<1.0000010396$",
            transform=gain_axis.transAxes,
            fontsize=4.1,
            color=MUTED,
        )
        gain_axis.set_xlim(lower_gain - 0.12, upper_gain + 0.12)
        gain_axis.set_ylim(0.62, 1.72)
        gain_axis.set_yticks([])
        gain_axis.set_xlabel("radius gain over the complete affine upper [ppm]")
        gain_axis.grid(axis="x", color=GRID, linewidth=0.36)

        cover_axis.set_title("(c) Exact 14-leaf cover at r = 0.382629", loc="left", pad=5)
        for leaf in leaves:
            x_left = float(leaf["scaledALowerDecimal"])
            x_right = float(leaf["scaledAUpperDecimal"])
            y_lower = float(leaf["characterLowerDecimal"])
            y_upper = float(leaf["characterUpperDecimal"])
            face, edge, hatch = cover_style[leaf["excludedBy"]]
            cover_axis.add_patch(
                Rectangle(
                    (x_left, y_lower),
                    x_right - x_left,
                    y_upper - y_lower,
                    facecolor=face,
                    edgecolor=edge,
                    hatch=hatch,
                    linewidth=0.55,
                    alpha=0.9,
                )
            )
        cover_axis.scatter(
            [candidate_a],
            [candidate_c],
            marker="D",
            s=24,
            facecolor="white",
            edgecolor=GOLD,
            linewidth=0.8,
            zorder=7,
        )
        cover_axis.text(0.02, 0.04, "adaptive tensor-Bernstein cover\nno parameter grid", transform=cover_axis.transAxes, fontsize=4.0, color=MUTED)
        cover_axis.set_xlim(0, 2)
        cover_axis.set_ylim(0.1337, 0.803)
        cover_axis.set_xlabel(r"scaled invariant $SA$")
        cover_axis.set_ylabel(r"character $c$")
        legend_handles = [
            Patch(facecolor=cover_style[key][0], edgecolor=cover_style[key][1], hatch=cover_style[key][2], label=f"{key}: {metadata['coverExclusionCounts'][key]} leaves")
            for key in ("H", "P", "Q")
        ]
        cover_axis.legend(handles=legend_handles, loc="lower right", frameon=False, fontsize=3.8, ncol=3, columnspacing=0.8, handlelength=1.6)
        cover_axis.grid(color=GRID, linewidth=0.3, zorder=0)

        figure.text(
            0.102,
            0.171,
            r"Theorem: $0.382628602237879637<r_{\rm prod}^{\rm opt}<0.382629$ in the complete compactified product-affine family of the degree-80 reduced edge model.",
            ha="left",
            va="top",
            fontsize=4.25,
            color=INK,
        )
        figure.text(
            0.102,
            0.123,
            r"Proof: exact invariant reduction, character-tail exclusion, and a complete dyadic tensor-Bernstein cover. The plotted boundary samples and optimizer point are not proof data.",
            ha="left",
            va="top",
            fontsize=4.25,
            color=INK,
        )
        figure.text(
            0.102,
            0.075,
            "Scope: reduced algebraic model only · 16/16 exact checks · 14 leaves · GMP rational signs · no three-dimensional Navier--Stokes regularity claim",
            ha="left",
            fontsize=4.25,
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
