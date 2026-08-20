#!/usr/bin/env python3
"""Render the formal R0.67C-2 journal figure."""

from __future__ import annotations

import csv
import platform
import resource
import time
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
PALE_RUST = "#f2e5df"
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
                (center[0] + dx, center[1] + dy),
                .010,
                .018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=.35,
            )
        )


def draw() -> None:
    started = time.perf_counter()
    intervals = rows("projection-intervals.csv")
    derivative = rows("derivative-budget.csv")
    scales = rows("spectral-scales.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r067c2-dominant-heat"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2, 2, left=.125, right=.955, bottom=.16, top=.79,
            width_ratios=(1.14, 1), height_ratios=(.57, .43),
            hspace=.64, wspace=.34,
        )
        interval_axis = figure.add_subplot(grid[:, 0])
        derivative_axis = figure.add_subplot(grid[0, 1])
        spectral_axis = figure.add_subplot(grid[1, 1])
        figure.suptitle(
            "The dominant complete sixth-order heat projection is strictly negative",
            x=.068, y=.954, ha="left", fontsize=8.0, color=INK,
        )
        figure.text(
            .068, .895,
            r"degree-six centred jet  ·  67,200 finite coordinates  ·  ten heat shuffles  ·  $C^{6,1}$ resolvent",
            ha="left", fontsize=3.8, color=MUTED,
        )
        blossom(figure)

        interval_axis.set_title("(a) Guarded coefficient decomposition", loc="left", pad=5)
        colors = [RUST, BLUE, GOLD]
        markers = ["D", "o", "s"]
        for y, row, color, marker in zip((2, 1, 0), intervals, colors, markers):
            lower = float(row["lower"]) * 1e6
            upper = float(row["upper"]) * 1e6
            center = (lower + upper) / 2
            interval_axis.hlines(y, lower, upper, color=color, linewidth=2.0)
            interval_axis.scatter([lower, upper], [y, y], marker="|", s=55, color=color)
            interval_axis.scatter([center], [y], marker=marker, s=20, facecolor="white", edgecolor=color, linewidth=.7)
        interval_axis.axvline(0, color=INK, linewidth=.55)
        interval_axis.axvspan(-1.71549, -.202514, color=PALE_RUST, zorder=-2)
        interval_axis.set_yticks([0, 1, 2], ["complete", "correction", "degree-six jet"])
        interval_axis.set_xlabel(r"coefficient  ($\times10^{-6}$)")
        interval_axis.set_xlim(-1.82, .86)
        interval_axis.grid(axis="x", color=GRID, linewidth=.3)
        interval_axis.text(
            .04, .07,
            r"$-1.71549<C_{6,\mathrm{heat}}\times10^6<-0.202514$",
            transform=interval_axis.transAxes, fontsize=3.55, color=RUST,
        )

        derivative_axis.set_title("(b) Seventh-derivative budget", loc="left", pad=5)
        names = [row["quantity"] for row in derivative]
        values = [float(row["value"]) * 1e5 for row in derivative]
        for y, value, color, marker in zip((2, 1, 0), values, (BLUE, RUST, GOLD), ("o", "D", "|")):
            derivative_axis.hlines(y, 0, value, color=color, linewidth=1.4)
            derivative_axis.scatter([value], [y], s=18, marker=marker, color=color)
            derivative_axis.text(value + .08, y, f"{value:.3f}", va="center", fontsize=3.2, color=color)
        derivative_axis.set_yticks([0, 1, 2], list(reversed(names)))
        derivative_axis.set_xlim(0, max(values) * 1.16)
        derivative_axis.set_xlabel(r"derivative scale  ($\times10^{-5}$)")
        derivative_axis.grid(axis="x", color=GRID, linewidth=.3)

        spectral_axis.set_title("(c) Spectral and remainder scales", loc="left", pad=5)
        labels = [row["quantity"] for row in scales]
        values = [float(row["value"]) for row in scales]
        for y, value, color, marker in zip(range(4), values, (BLUE, RUST, GOLD, INK), ("o", "^", "s", "D")):
            spectral_axis.scatter([value], [y], s=19, marker=marker, color=color)
            spectral_axis.hlines(y, 1e-5, value, color=color, linewidth=.75)
        spectral_axis.set_xscale("log")
        spectral_axis.set_xlim(1e-5, 900)
        spectral_axis.set_ylim(-.6, 3.6)
        spectral_axis.set_yticks(range(4), labels)
        spectral_axis.set_xlabel("one-block scale (log axis)")
        spectral_axis.grid(axis="x", color=GRID, linewidth=.3, which="both")

        figure.text(
            .068, .055,
            "Claim boundary: one fixed sixth-order periodic projection; all-order control and 3D regularity remain open.",
            fontsize=3.35, color=MUTED,
        )
        metadata = {"Creator": "R0.67C-2 dominant heat audit", "Date": None}
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    with (HERE / "plot-resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["elapsedSeconds", "maximumRssMiB", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerow({
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        })


if __name__ == "__main__":
    draw()
