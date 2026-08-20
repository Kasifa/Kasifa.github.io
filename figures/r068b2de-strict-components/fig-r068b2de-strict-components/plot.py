#!/usr/bin/env python3
"""Render the R0.68B-2d/e strict-components figure."""

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
PALE_BLUE = "#e6edf1"
PALE_GOLD = "#f1e6cb"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def blossom(figure) -> None:
    center = (0.946, 0.942)
    for dx, dy, angle in (
        (0, 0.010, 0),
        (0, -0.010, 0),
        (0.008, 0, 90),
        (-0.008, 0, 90),
    ):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy),
                0.010,
                0.018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=0.35,
            )
        )


def draw() -> None:
    started = time.perf_counter()
    derivative = rows("derivative-bounds.csv")
    margins = rows("interval-margins.csv")
    budget = rows("pilot-budget.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r068b2de-strict-components"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.08,
            right=0.955,
            bottom=0.17,
            top=0.79,
            width_ratios=(1.08, 0.92),
            height_ratios=(0.52, 0.48),
            hspace=0.68,
            wspace=0.34,
        )
        derivative_axis = figure.add_subplot(grid[0, 0])
        interval_axis = figure.add_subplot(grid[0, 1])
        budget_axis = figure.add_subplot(grid[1, :])
        figure.suptitle(
            "Strict derivative and dominant-mass components of the eighth-order heat sign budget",
            x=0.055,
            y=0.954,
            ha="left",
            fontsize=7.35,
            color=INK,
        )
        figure.text(
            0.055,
            0.894,
            "35 shuffles  ·  all 4,368 eleventh-order multiindices  ·  1,792 exact mass intervals  ·  combined sign still open",
            ha="left",
            fontsize=3.65,
            color=MUTED,
        )
        blossom(figure)

        coordinates = [int(row["coordinate"]) for row in derivative]
        derivative_values = [float(row["upperTimes1e6"]) for row in derivative]
        colors = [BLUE if coordinate == 4 else PALE_BLUE for coordinate in coordinates]
        bars = derivative_axis.bar(
            coordinates,
            derivative_values,
            color=colors,
            edgecolor=BLUE,
            linewidth=0.55,
        )
        bars[3].set_hatch("///")
        derivative_axis.axhline(
            2.567,
            color=RUST,
            linewidth=0.8,
            linestyle="--",
            label=r"exact benchmark $2.567$",
        )
        derivative_axis.set_title(
            "(a) Exact eleventh-derivative upper bounds",
            loc="left",
            pad=5,
        )
        derivative_axis.set_xlabel("pure coordinate i")
        derivative_axis.set_ylabel(r"$10^6\|\partial_i^{11}K\|_\infty$")
        derivative_axis.set_xticks(coordinates)
        derivative_axis.set_ylim(0, 2.9)
        derivative_axis.grid(axis="y", color=GRID, linewidth=0.3)
        derivative_axis.legend(frameon=False, fontsize=2.8, loc="upper left")
        derivative_axis.text(
            0.04,
            0.08,
            r"all-index maximum: $\alpha=(0,0,0,11,0,0)$",
            transform=derivative_axis.transAxes,
            fontsize=2.9,
            color=INK,
        )

        margin_values = [
            float(row["decimalOrdersBeyondGate"]) for row in margins
        ]
        labels = ["root interval", "mass intervals"]
        margin_bars = interval_axis.barh(
            labels,
            margin_values,
            color=[PALE_GOLD, PALE_BLUE],
            edgecolor=[GOLD, BLUE],
            linewidth=0.65,
        )
        margin_bars[0].set_hatch("..")
        margin_bars[1].set_hatch("//")
        interval_axis.axvline(0, color=INK, linewidth=0.55)
        interval_axis.set_title(
            "(b) Certified precision beyond declared gates",
            loc="left",
            pad=5,
        )
        interval_axis.set_xlabel("additional decimal orders")
        interval_axis.grid(axis="x", color=GRID, linewidth=0.3)
        for index, value in enumerate(margin_values):
            interval_axis.text(
                value + 0.35,
                index,
                f"+{value:.2f}",
                va="center",
                fontsize=3.0,
                color=INK,
            )
        interval_axis.text(
            0.03,
            0.06,
            r"gates: root $10^{-60}$; mass $10^{-50}$",
            transform=interval_axis.transAxes,
            fontsize=2.85,
            color=MUTED,
        )

        components = [row["component"] for row in budget]
        budget_values = [float(row["valueTimes1e8"]) for row in budget]
        budget_bars = budget_axis.bar(
            range(3),
            budget_values,
            color=[PALE_BLUE, PALE_GOLD, "white"],
            edgecolor=[BLUE, GOLD, RUST],
            linewidth=0.75,
        )
        budget_bars[1].set_hatch("///")
        budget_bars[2].set_hatch("xx")
        budget_axis.set_title(
            "(c) Degree-ten sign budget remains a mixed-evidence pilot",
            loc="left",
            pad=5,
        )
        budget_axis.set_xticks(range(3), components)
        budget_axis.set_ylabel(r"$10^8$ times magnitude")
        budget_axis.set_ylim(0, 1.7)
        budget_axis.grid(axis="y", color=GRID, linewidth=0.3)
        for index, value in enumerate(budget_values):
            budget_axis.text(
                index,
                value + 0.06,
                f"{value:.3f}",
                ha="center",
                fontsize=3.0,
                color=INK,
            )
        budget_axis.text(
            0.51,
            0.79,
            "derivative factor strict",
            transform=budget_axis.transAxes,
            fontsize=2.9,
            color=BLUE,
        )
        budget_axis.text(
            0.51,
            0.65,
            "moment, heat, defect and resolvent enclosures open",
            transform=budget_axis.transAxes,
            fontsize=2.9,
            color=RUST,
        )

        figure.text(
            0.055,
            0.055,
            "Claim boundary: panels (a) and (b) are exact rational certificates. Panel (c) is diagnostic; its positive gap is not yet a strict sign theorem.",
            fontsize=3.25,
            color=MUTED,
        )
        metadata = {
            "Creator": "R0.68B-2d/e strict component certificates",
            "Date": None,
        }
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    with (HERE / "plot-resources.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["elapsedSeconds", "maximumRssMiB", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow(
            {
                "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
                "maximumRssMiB": f"{rss_mib():.3f}",
                "status": "passed",
            }
        )


if __name__ == "__main__":
    draw()
