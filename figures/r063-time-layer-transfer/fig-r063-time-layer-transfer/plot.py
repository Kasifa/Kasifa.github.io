#!/usr/bin/env python3
"""Render Figure R0.63-1 at double-column journal size."""

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
    axis.text(xy[0] + width / 2, xy[1] + height * 0.62, title, ha="center", va="center", fontsize=5.4, color=INK)
    axis.text(xy[0] + width / 2, xy[1] + height * 0.27, detail, ha="center", va="center", fontsize=3.45, color=MUTED)


def draw() -> None:
    probes = rows("hostile-target-probes.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r063-time-layer-transfer"
        figure = plt.figure(figsize=(178 / 25.4, 96 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.066,
            right=0.957,
            bottom=0.19,
            top=0.79,
            width_ratios=(1.08, 1.0),
            hspace=0.6,
            wspace=0.34,
        )
        transfer_axis = figure.add_subplot(grid[:, 0])
        scale_axis = figure.add_subplot(grid[0, 1])
        condition_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "The quartic transfer closes only after a lifted state system",
            x=0.066,
            y=0.946,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.066,
            0.888,
            "Exact: time-layer factorization + 8-state cubic lift  ·  Open: integrated norm needed for |S4,m| ≤ C L²M",
            ha="left",
            fontsize=3.9,
            color=MUTED,
        )

        transfer_axis.set_title("(a) Exact state closure", loc="left", pad=4)
        transfer_axis.set_xlim(0, 1)
        transfer_axis.set_ylim(0, 1)
        transfer_axis.axis("off")
        state_box(transfer_axis, (0.11, 0.76), 0.78, 0.14, "2 base states", r"$P_n, Q_n$ generate the signs", PALE_BLUE, BLUE)
        state_box(transfer_axis, (0.11, 0.48), 0.78, 0.14, "8 cubic states", r"$P/Q \times P/Q \times \overline{P/Q}$", PALE_BLUE, BLUE)
        state_box(transfer_axis, (0.11, 0.20), 0.78, 0.14, "16 target-signed states + carries", r"target $P/Q$ bit; shifts $-1,0,1,2$", PALE_RUST, RUST)
        for start, end in (((0.5, 0.75), (0.5, 0.63)), ((0.5, 0.47), (0.5, 0.35))):
            transfer_axis.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=8, color=INK, linewidth=0.7))
        transfer_axis.text(0.5, 0.675, "cubic lift", ha="center", va="center", fontsize=3.5, color=MUTED)
        transfer_axis.text(0.5, 0.395, "multiply target sign", ha="center", va="center", fontsize=3.5, color=MUTED)
        transfer_axis.text(
            0.5,
            0.075,
            "Gaussian half-block restrictions change with scale:\nnon-autonomous integrated transfer",
            ha="center",
            va="center",
            fontsize=3.75,
            color=GOLD,
        )

        scales = [int(row["M"]) for row in probes]
        ratios = [float(row["S4OverM"]) for row in probes]
        conditions = [float(row["cancellationConditionNumber"]) for row in probes]

        scale_axis.set_title("(b) Heat-weighted hostile targets", loc="left", pad=4)
        scale_axis.plot(
            scales,
            ratios,
            color=BLUE,
            linewidth=0.9,
            marker="o",
            markerfacecolor="white",
            markeredgewidth=0.55,
            markersize=2.8,
        )
        scale_axis.set_xscale("log", base=2)
        scale_axis.set_ylim(0, 0.022)
        scale_axis.set_ylabel(r"$S_{4,m}/M$")
        scale_axis.set_xlabel(r"output count $M$ (log$_2$ scale)")
        scale_axis.grid(color=GRID, linewidth=0.3)
        scale_axis.text(0.98, 0.08, "six finite probes", transform=scale_axis.transAxes, ha="right", fontsize=3.35, color=MUTED)

        condition_axis.set_title("(c) Numerical cancellation boundary", loc="left", pad=4)
        condition_axis.plot(
            scales,
            conditions,
            color=RUST,
            linewidth=0.9,
            linestyle=(0, (4, 2)),
            marker="s",
            markerfacecolor="white",
            markeredgewidth=0.55,
            markersize=2.8,
        )
        condition_axis.set_xscale("log", base=2)
        condition_axis.set_yscale("log")
        condition_axis.set_ylabel("absolute/signed path sum")
        condition_axis.set_xlabel(r"output count $M$ (log$_2$ scale)")
        condition_axis.grid(color=GRID, linewidth=0.3, which="both")
        condition_axis.text(0.98, 0.08, "not an interval certificate", transform=condition_axis.transAxes, ha="right", fontsize=3.35, color=MUTED)

        figure.text(
            0.066,
            0.06,
            "Interpretation: the finite heat-weighted probes do not show the unweighted growth, but only a common norm or a supercritical carry cycle can decide the all-index O(M) question.",
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
