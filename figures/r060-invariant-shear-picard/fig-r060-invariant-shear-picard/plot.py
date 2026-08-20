#!/usr/bin/env python3
"""Render the R0.60 invariant-shear Picard support figure."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyBboxPatch


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
RED = "#8b4d43"
PALE_BLUE = "#dce7ec"
PALE_GOLD = "#efe1c7"
PALE_RED = "#eadbd7"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def add_blossom(figure) -> None:
    center = (0.955, 0.942)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(
            Ellipse(
                (center[0] + 0.0105 * math.cos(theta), center[1] + 0.013 * math.sin(theta)),
                width=0.015,
                height=0.026,
                angle=angle - 90,
                facecolor=PALE_GOLD,
                edgecolor=GOLD,
                linewidth=0.45,
                transform=figure.transFigure,
                zorder=20,
            )
        )
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK, zorder=21)


def chain_panel(axis) -> None:
    axis.set_title("(a) Picard forest collapses to one chain", loc="left", pad=5, fontsize=5.2)
    axis.set_xlim(0, 1)
    axis.set_ylim(0, 1)
    axis.axis("off")
    positions = (0.08, 0.32, 0.56, 0.80)
    labels = ((r"$G_1$", "linear"), (r"$G_2$", "target"), (r"$G_3$", "high return"), (r"$G_4$", "target possible"))
    fills = (PALE_BLUE, PALE_GOLD, PALE_RED, PALE_GOLD)
    edges = (BLUE, GOLD, RED, GOLD)
    for index, (x_value, (symbol, subtitle), fill, edge) in enumerate(zip(positions, labels, fills, edges)):
        box = FancyBboxPatch(
            (x_value - 0.075, 0.52),
            0.15,
            0.20,
            boxstyle="round,pad=0.012,rounding_size=0.018",
            facecolor=fill,
            edgecolor=edge,
            linewidth=0.75,
        )
        axis.add_patch(box)
        axis.text(x_value, 0.64, symbol, ha="center", va="center", fontsize=7.2, color=INK)
        axis.text(x_value, 0.555, subtitle, ha="center", va="center", fontsize=3.45, color=MUTED)
        if index:
            axis.annotate(
                "",
                xy=(x_value - 0.082, 0.62),
                xytext=(positions[index - 1] + 0.082, 0.62),
                arrowprops={"arrowstyle": "->", "color": INK, "linewidth": 0.65},
            )
            axis.text((x_value + positions[index - 1]) / 2, 0.69, r"$-F_1\partial_2$", ha="center", va="bottom", fontsize=3.6, color=MUTED)
    axis.text(
        0.5,
        0.39,
        r"$(\partial_t-\Delta_{12})G_n=-F_1\partial_2G_{n-1}$",
        ha="center",
        va="center",
        fontsize=5.0,
        color=INK,
    )
    axis.text(
        0.5,
        0.23,
        r"$u=(0,F,G)$  ·  $u^{[n]}=G_ne_3$ for $n\geq2$" + "\n" + r"the second frequency $m$ is conserved",
        ha="center",
        va="center",
        fontsize=3.75,
        color=MUTED,
        linespacing=1.55,
    )


def draw() -> None:
    support = rows("support-gaps.csv")
    events = rows("picard-events.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r060-invariant-shear-picard"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.065,
            right=0.965,
            bottom=0.34,
            top=0.825,
            width_ratios=(1.15, 1.05, 1.15),
            wspace=0.36,
        )
        chain_axis = figure.add_subplot(grid[0, 0])
        gap_axis = figure.add_subplot(grid[0, 1])
        event_axis = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Support thresholds in the invariant shear Picard chain",
            x=0.065,
            y=0.945,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        chain_panel(chain_axis)

        gap_axis.set_title("(b) Odd-order distance to $\\xi_1=0$", loc="left", pad=5, fontsize=5.2)
        styles = {
            3: (BLUE, "o", "-"),
            5: (GOLD, "s", (0, (4, 2))),
            7: (RED, "^", (0, (1, 2))),
            9: (INK, "D", (0, (6, 2, 1, 2))),
        }
        for order, (color, marker, linestyle) in styles.items():
            selected = [row for row in support if int(row["order"]) == order]
            gap_axis.semilogx(
                [int(row["N"]) for row in selected],
                [float(row["gapOverH"]) for row in selected],
                base=2,
                color=color,
                marker=marker,
                markerfacecolor="white",
                markeredgewidth=0.5,
                markersize=2.4,
                linewidth=0.9,
                linestyle=linestyle,
                label=rf"order {order}",
            )
        gap_axis.scatter([5], [0], marker="*", s=18, facecolor=GOLD, edgecolor=INK, linewidth=0.35, zorder=5)
        gap_axis.annotate(
            "order 11: zero support path\nfor $N\\geq5$ (coefficient unproved)",
            xy=(5, 0),
            xytext=(9, 0.115),
            fontsize=3.25,
            color=MUTED,
            arrowprops={"arrowstyle": "->", "color": MUTED, "linewidth": 0.45},
        )
        gap_axis.axhline(0.75, color=BLUE, linewidth=0.45, alpha=0.45)
        gap_axis.text(1.1, 0.73, r"cubic gap $>3H/4$", fontsize=3.3, color=BLUE, va="bottom")
        gap_axis.set_xlim(1, 4096)
        gap_axis.set_ylim(-0.035, 1.06)
        gap_axis.set_xlabel(r"carrier count $N=LM$ (log scale)")
        gap_axis.set_ylabel(r"certified distance divided by $H$")
        gap_axis.grid(color=GRID, linewidth=0.32)
        gap_axis.legend(loc="upper right", frameon=False, fontsize=3.35)

        event_axis.set_title("(c) Target return and $A^4$ energy", loc="left", pad=5, fontsize=5.2)
        lane_y = {"A^4 energy": 0, "original V support": 1, "target plane": 2}
        status_style = {
            "initial": (BLUE, "o", PALE_BLUE),
            "reached": (GOLD, "o", PALE_GOLD),
            "returned": (RED, "D", PALE_RED),
            "excluded": (MUTED, "x", "none"),
            "support-admissible": (GOLD, "s", "white"),
            "positive square": (BLUE, "o", "white"),
            "cross term": (RED, "D", "white"),
        }
        for lane, y_value in lane_y.items():
            event_axis.axhline(y_value, color=GRID, linewidth=0.55, zorder=0)
        for row in events:
            order = int(row["order"])
            y_value = lane_y[row["lane"]]
            edge, marker, face = status_style[row["status"]]
            event_axis.scatter(
                [order],
                [y_value],
                marker=marker,
                s=20,
                edgecolor=edge,
                facecolor=face,
                linewidth=0.75,
                zorder=3,
            )
        event_axis.text(2.0, 2.14, "quadratic target", ha="right", fontsize=3.2, color=GOLD)
        event_axis.text(3.0, 1.14, "cubic return", ha="center", fontsize=3.2, color=RED)
        event_axis.text(4.0, 2.14, "first correction", ha="left", fontsize=3.2, color=GOLD)
        event_axis.text(11.0, 2.14, "support only", ha="center", fontsize=3.2, color=GOLD)
        event_axis.text(2.5, -0.27, r"$\|G_2\|^2$  and  $2\langle G_1,G_3\rangle$", ha="center", fontsize=3.45, color=MUTED)
        event_axis.set_xlim(0.5, 11.5)
        event_axis.set_ylim(-0.42, 2.42)
        event_axis.set_xticks([1, 2, 3, 4, 5, 7, 9, 11])
        event_axis.set_yticks([0, 1, 2], [r"$A^4$ energy", "original V support", r"target $\xi_1=0$"])
        event_axis.set_xlabel("Picard order")
        event_axis.tick_params(axis="y", labelsize=4.1)
        event_axis.spines["left"].set_visible(False)
        event_axis.spines["bottom"].set_color(GRID)

        figure.text(
            0.065,
            0.228,
            r"Exact order-four identity: $\frac{d}{dt}(2\langle G_1,G_3\rangle+\|G_2\|_2^2)"
            r"+2(2\langle\nabla G_1,\nabla G_3\rangle+\|\nabla G_2\|_2^2)=0$.",
            ha="left",
            va="top",
            fontsize=4.0,
            color=INK,
        )
        figure.text(
            0.065,
            0.162,
            "Formal scope: 24/24 checks; 32,771,750 exact support transitions through order 11; "
            "323,216 Gaussian-integer convolution pairs for the energy regression.",
            ha="left",
            va="top",
            fontsize=3.75,
            color=MUTED,
        )
        figure.text(
            0.065,
            0.105,
            "Conclusion: cubic target return is impossible, but cubic high-frequency backtracking is essential. "
            "The packet is globally smooth in this shear class; this is not an arbitrary-data regularity proof.",
            ha="left",
            va="top",
            fontsize=3.75,
            color=MUTED,
        )
        add_blossom(figure)

        figure.savefig(HERE / "figure.pdf")
        figure.savefig(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")


if __name__ == "__main__":
    draw()
