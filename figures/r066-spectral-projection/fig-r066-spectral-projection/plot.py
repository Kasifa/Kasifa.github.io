#!/usr/bin/env python3
"""Render Figure R0.66-1 at double-column journal size."""

from __future__ import annotations

import csv
import platform
import resource
import time
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.ticker import FixedFormatter, FixedLocator


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a16f27"
PALE_BLUE = "#e4edf2"
PALE_RUST = "#f2e5df"
GRID = "#d5cec0"


def csv_rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def blossom(figure) -> None:
    center = (0.946, 0.942)
    for dx, dy, angle in (
        (0.0, 0.010, 0),
        (0.0, -0.010, 0),
        (0.008, 0.0, 90),
        (-0.008, 0.0, 90),
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


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def draw() -> None:
    started = time.perf_counter()
    convergence = csv_rows("cycle-normalized.csv")
    intervals = csv_rows("coefficient-intervals.csv")
    errors = csv_rows("error-budget.csv")

    r_values = [int(row["r"]) for row in convergence]
    normalized = [float(row["normalizedCenter"]) for row in convergence]
    positive_r = [r for r, value in zip(r_values, normalized) if value > 0]
    positive_y = [value for value in normalized if value > 0]
    negative_r = [r for r, value in zip(r_values, normalized) if value < 0]
    negative_y = [value for value in normalized if value < 0]
    coefficient_lower = float(intervals[1]["lower"])
    coefficient_upper = float(intervals[1]["upper"])

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r066-spectral-projection"
        figure = plt.figure(figsize=(178 / 25.4, 108 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.090,
            right=0.955,
            bottom=0.165,
            top=0.790,
            width_ratios=(1.16, 1.0),
            height_ratios=(0.47, 0.53),
            hspace=0.52,
            wspace=0.33,
        )
        convergence_axis = figure.add_subplot(grid[:, 0])
        interval_axis = figure.add_subplot(grid[0, 1])
        error_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "Dominant heat-weighted spectral coefficient is strictly negative",
            x=0.072,
            y=0.954,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.072,
            0.895,
            r"Exact 48-state affine block  ·  degree-48 cycle-100 iterate  ·  $S_r=C_*\lambda^r+O(r16^r)$",
            ha="left",
            fontsize=3.9,
            color=MUTED,
        )
        blossom(figure)

        convergence_axis.set_title(
            r"(a) Complete finite coefficients after division by $\lambda^r$",
            loc="left",
            pad=5,
        )
        convergence_axis.axhspan(
            coefficient_lower,
            coefficient_upper,
            color=PALE_RUST,
            zorder=0,
        )
        convergence_axis.plot(r_values, normalized, color=MUTED, linewidth=0.7, zorder=1)
        convergence_axis.scatter(
            positive_r,
            positive_y,
            s=13,
            facecolors="white",
            edgecolors=BLUE,
            marker="o",
            linewidths=0.7,
            label="certified positive",
            zorder=3,
        )
        convergence_axis.scatter(
            negative_r,
            negative_y,
            s=12,
            facecolors=RUST,
            edgecolors=RUST,
            marker="s",
            linewidths=0.5,
            label="certified negative",
            zorder=3,
        )
        convergence_axis.axhline(0, color=INK, linewidth=0.7)
        convergence_axis.set_yscale("symlog", linthresh=3e-5, linscale=1.15, base=10)
        convergence_axis.set_xlim(0.5, 24.5)
        convergence_axis.set_ylim(-5.2e-5, 1.2e-2)
        convergence_axis.set_xlabel(r"cycle count $r$")
        convergence_axis.set_ylabel(r"$S_r/\lambda^r$ (symmetric-log)")
        convergence_axis.grid(color=GRID, linewidth=0.3, which="major")
        convergence_axis.legend(
            loc="upper right", frameon=False, fontsize=3.35, handletextpad=0.5
        )
        convergence_axis.annotate(
            "sign change\nr = 14",
            xy=(14, normalized[13]),
            xytext=(10.6, -4.1e-5),
            fontsize=3.55,
            color=RUST,
            ha="center",
            arrowprops={"arrowstyle": "-", "color": RUST, "linewidth": 0.55},
        )
        convergence_axis.text(
            23.8,
            (coefficient_lower + coefficient_upper) / 2,
            r"certified asymptotic $C_*$ band",
            ha="right",
            va="bottom",
            fontsize=3.35,
            color=RUST,
        )

        interval_axis.set_title(
            r"(b) Cycle 100 and complete $C_*$ intervals",
            loc="left",
            pad=5,
        )
        interval_axis.axvline(0, color=INK, linewidth=0.75)
        y_positions = [1, 0]
        colors = [BLUE, RUST]
        markers = ["o", "s"]
        for row, y, color, marker in zip(intervals, y_positions, colors, markers):
            low = float(row["lower"]) * 1e5
            high = float(row["upper"]) * 1e5
            center = (low + high) / 2
            interval_axis.hlines(y, low, high, color=color, linewidth=2.2, zorder=2)
            interval_axis.scatter(
                [center],
                [y],
                s=17,
                marker=marker,
                facecolors="white" if marker == "o" else color,
                edgecolors=color,
                linewidths=0.7,
                zorder=3,
            )
        interval_axis.set_xlim(-2.36, 0.12)
        interval_axis.set_ylim(-0.55, 1.55)
        interval_axis.set_yticks(y_positions)
        interval_axis.set_yticklabels(["cycle 100 polynomial", r"complete $C_*$"])
        interval_axis.set_xlabel(r"coefficient ($\times10^{-5}$); zero shown")
        interval_axis.grid(axis="x", color=GRID, linewidth=0.3)
        interval_axis.text(
            -2.34,
            0.34,
            r"$-2.30446<C_*\,10^5<-2.28653$",
            fontsize=3.25,
            color=RUST,
            ha="left",
        )

        error_axis.set_title(
            "(c) Outward errors versus certified zero margin",
            loc="left",
            pad=5,
        )
        error_labels = [
            "simplex tail",
            "spectral convergence",
            "target parameter",
            "total error",
            "distance to zero",
        ]
        error_values = [float(row["bound"]) for row in errors]
        y = list(range(len(errors)))
        error_axis.hlines(y, 1e-22, error_values, color=GRID, linewidth=0.8, zorder=1)
        for index, (row, value) in enumerate(zip(errors, error_values)):
            if row["kind"] == "margin":
                color, marker, face = INK, "D", INK
            elif row["kind"] == "total":
                color, marker, face = RUST, "s", RUST
            else:
                color, marker, face = BLUE, "o", "white"
            error_axis.scatter(
                [value],
                [index],
                s=16,
                color=color,
                marker=marker,
                facecolors=face,
                edgecolors=color,
                linewidths=0.7,
                zorder=3,
            )
        error_axis.set_xscale("log")
        error_axis.set_xlim(1e-22, 1e-4)
        error_axis.set_ylim(-0.6, len(errors) - 0.4)
        error_axis.set_yticks(y)
        error_axis.set_yticklabels(error_labels)
        error_axis.invert_yaxis()
        error_axis.set_xlabel("absolute bound (log scale)")
        error_axis.xaxis.set_major_locator(FixedLocator([1e-20, 1e-16, 1e-12, 1e-8, 1e-4]))
        error_axis.xaxis.set_major_formatter(
            FixedFormatter([r"$10^{-20}$", r"$10^{-16}$", r"$10^{-12}$", r"$10^{-8}$", r"$10^{-4}$"])
        )
        error_axis.grid(axis="x", color=GRID, linewidth=0.3, which="major")
        error_axis.axvspan(
            error_values[3], error_values[4], color=PALE_BLUE, alpha=0.75, linewidth=0
        )
        error_axis.text(
            1.4e-7,
            3.6,
            ">255× separation",
            fontsize=3.25,
            color=INK,
            ha="left",
        )

        figure.text(
            0.072,
            0.060,
            r"Claim boundary: $|S_r|/16^r\to\infty$ for one explicit quartic packet; higher Picard orders and the full mild solution are not controlled.",
            ha="left",
            va="top",
            fontsize=3.7,
            color=MUTED,
        )
        figure.savefig(HERE / "figure.pdf")
        figure.savefig(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    elapsed = time.perf_counter() - started
    with (HERE / "plot-resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["elapsedSeconds", "rssMiB", "status"], lineterminator="\n"
        )
        writer.writeheader()
        writer.writerow(
            {"elapsedSeconds": f"{elapsed:.6f}", "rssMiB": f"{rss_mib():.3f}", "status": "exited:0"}
        )


if __name__ == "__main__":
    draw()
