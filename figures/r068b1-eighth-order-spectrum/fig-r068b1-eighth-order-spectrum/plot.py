#!/usr/bin/env python3
"""Render the R0.68B-1 exact eighth-order cycle-spectrum figure."""

from __future__ import annotations

import csv
import platform
import resource
import time
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
GREEN = "#4f6a57"
PALE_BLUE = "#e6edf1"
PALE_GOLD = "#f4ead6"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def blossom(figure) -> None:
    center = (0.946, 0.942)
    for dx, dy, angle in ((0, .010, 0), (0, -.010, 0), (.008, 0, 90), (-.008, 0, 90)):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy), .010, .018,
                angle=angle, transform=figure.transFigure,
                facecolor="#ead9b8", edgecolor=GOLD, linewidth=.35,
            )
        )


def draw() -> None:
    started = time.perf_counter()
    ranks = rows("rank-collapse.csv")
    blocks = rows("spectral-blocks.csv")
    sequence = rows("reachable-sequence.csv")
    scales = {row["quantity"]: row for row in rows("certified-scales.csv")}
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r068b1-eighth-order-spectrum"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2, 2, left=.085, right=.955, bottom=.17, top=.79,
            width_ratios=(.78, 1.22), height_ratios=(.50, .50),
            hspace=.62, wspace=.34,
        )
        rank_axis = figure.add_subplot(grid[0, 0])
        factor_axis = figure.add_subplot(grid[0, 1])
        sequence_axis = figure.add_subplot(grid[1, :])
        figure.suptitle(
            "The eighth-order zero-time cycle has a 148-dimensional stable image and one reachable dominant root",
            x=.056, y=.954, ha="left", fontsize=7.65, color=INK,
        )
        figure.text(
            .056, .894,
            r"exact 1792-state transfer  ·  four-bit cycle $0100$  ·  $Y_{8,r}=C_{8,0}\nu^r+O(4800^r)$  ·  heat simplex still open",
            ha="left", fontsize=3.75, color=MUTED,
        )
        blossom(figure)

        labels = [row["stage"] for row in ranks]
        values = [int(row["exactRank"]) for row in ranks]
        x = range(len(values))
        rank_axis.set_title("(a) Exact rank collapse", loc="left", pad=5)
        rank_axis.plot(x, values, color=BLUE, linewidth=1.15, marker="o", markersize=3.2)
        rank_axis.fill_between(x, values, color=PALE_BLUE, alpha=.82)
        for index, value in enumerate(values):
            rank_axis.text(index, value + 70, f"{value:,}", ha="center", fontsize=3.2, color=BLUE if index else INK)
        rank_axis.axhline(148, color=INK, linestyle="--", linewidth=.55)
        rank_axis.set_xticks(list(x), ["ambient", r"$W_8$", r"$W_8^2$", r"$W_8^3$"])
        rank_axis.set_ylabel("exact rank")
        rank_axis.set_ylim(0, 2000)
        rank_axis.grid(axis="y", color=GRID, linewidth=.3)
        rank_axis.text(1.82, 330, "rank stabilizes at 148", fontsize=3.05, color=INK)

        factor_axis.set_title("(b) Exact characteristic factorization on im($W_8$)", loc="left", pad=5)
        colors = [MUTED, RUST, BLUE, GREEN, GOLD]
        hatches = ["//", "..", "", "xx", "\\\\"]
        left = 0
        factor_labels = {
            "x": r"$x$",
            "x-4096": r"$x-4096$",
            "q4_256": r"$q_{4,256}$",
            "q10_16": r"$q_{10,16}$",
            "q18": r"$q_{18}$",
        }
        for row, color, hatch in zip(blocks, colors, hatches):
            width = int(row["imageDimension"])
            factor_axis.add_patch(Rectangle((left, .46), width, .30, facecolor=color, edgecolor=INK, linewidth=.35, hatch=hatch, alpha=.88))
            factor_axis.text(left + width / 2, .61, factor_labels[row["factor"]], ha="center", va="center", fontsize=3.0, color="white" if color in (RUST, BLUE, GREEN) else INK)
            factor_axis.text(left + width / 2, .34, str(width), ha="center", fontsize=2.9, color=INK)
            left += width
        factor_axis.set_xlim(0, 204)
        factor_axis.set_ylim(0, 1)
        factor_axis.set_xticks([0, 56, 70, 126, 186, 204])
        factor_axis.set_xlabel("algebraic dimension (total 204)")
        factor_axis.set_yticks([])
        factor_axis.spines[["left", "right", "top"]].set_visible(False)
        nu_lower = float(scales["dominant root nu"]["lower"])
        factor_axis.text(.02, .92, r"$\chi_{\rm im}=x^{56}(x-4096)^{14}q_{4,256}^{14}q_{10,16}^{6}q_{18}$", transform=factor_axis.transAxes, fontsize=3.15, color=INK)
        factor_axis.text(.02, .04, rf"reachable $\nu>{nu_lower:.3f}$; every other reachable root $<4800$", transform=factor_axis.transAxes, fontsize=3.05, color=BLUE)

        displayed_sequence = [row for row in sequence if int(row["block"]) >= 7]
        blocks_x = [int(row["block"]) for row in displayed_sequence]
        normalized = [float(row["normalizedByDominantRootMidpoint"]) for row in displayed_sequence]
        coefficient_lower = float(scales["dominant coefficient C8,0"]["lower"])
        coefficient_upper = float(scales["dominant coefficient C8,0"]["upper"])
        sequence_axis.set_title("(c) The reachable scalar crosses sign and converges to a strictly negative projection", loc="left", pad=5)
        sequence_axis.plot(blocks_x, normalized, color=BLUE, linewidth=1.0, marker="o", markevery=[0, 3, 13, 33, 53, 74], markersize=2.8)
        sequence_axis.axhline(0, color=INK, linewidth=.55)
        sequence_axis.axhspan(coefficient_lower, coefficient_upper, color=RUST, alpha=.55, label=r"certified $C_{8,0}$ interval")
        sequence_axis.axvline(10, color=GOLD, linewidth=.65, linestyle="--")
        sequence_axis.text(10.8, .80, "strictly negative from r=10", transform=sequence_axis.get_xaxis_transform(), fontsize=3.0, color=GOLD)
        sequence_axis.set_xlim(7, 81)
        sequence_axis.set_ylim(-.04, .08)
        sequence_axis.set_xlabel("four-bit block r")
        sequence_axis.set_ylabel(r"$Y_{8,r}/\nu^r$")
        sequence_axis.grid(color=GRID, linewidth=.3)
        sequence_axis.legend(loc="upper right", frameon=False, fontsize=3.05)
        sequence_axis.text(.52, .35, r"$-0.0261267936341<C_{8,0}<-0.0261267936271$", transform=sequence_axis.transAxes, fontsize=3.2, color=RUST)
        sequence_axis.text(.52, .23, r"zero-time quartic-critical probe: $256/\lambda^2<256/625=0.4096$", transform=sequence_axis.transAxes, fontsize=3.1, color=BLUE)

        figure.text(
            .056, .055,
            "Claim boundary: exact zero-time fixed-order spectrum only; the complete seven-simplex heat projection and general 3D regularity remain open.",
            fontsize=3.35, color=MUTED,
        )
        metadata = {"Creator": "R0.68B-1 exact eighth-order cycle spectrum", "Date": None}
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    with (HERE / "plot-resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["elapsedSeconds", "maximumRssMiB", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerow({"elapsedSeconds": f"{time.perf_counter() - started:.6f}", "maximumRssMiB": f"{rss_mib():.3f}", "status": "passed"})


if __name__ == "__main__":
    draw()
