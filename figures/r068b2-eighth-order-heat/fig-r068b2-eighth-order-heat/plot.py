#!/usr/bin/env python3
"""Render the R0.68B-2 first-cycle and degree-eight heat-jet figure."""

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
GREEN = "#4f6a57"
PALE_BLUE = "#e6edf1"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
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
    compression = rows("state-compression.csv")
    convergence = rows("jet-convergence.csv")
    residuals = rows("moment-residuals.csv")
    summary = rows("certified-summary.csv")[0]
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r068b2-eighth-order-heat"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2, 2, left=.08, right=.955, bottom=.17, top=.79,
            width_ratios=(.9, 1.1), height_ratios=(.50, .50),
            hspace=.66, wspace=.34,
        )
        compression_axis = figure.add_subplot(grid[0, 0])
        interval_axis = figure.add_subplot(grid[0, 1])
        jet_axis = figure.add_subplot(grid[1, :])
        figure.suptitle(
            "The complete first eighth-order heat block is positive, while the dominant degree-eight jet is numerically negative",
            x=.055, y=.954, ha="left", fontsize=7.35, color=INK,
        )
        figure.text(
            .055, .894,
            r"exact $M=16$ seven-simplex sum  ·  35 shuffles  ·  six-variable 1792-state affine lift  ·  final defect bounds still open",
            ha="left", fontsize=3.65, color=MUTED,
        )
        blossom(figure)

        depth = [int(row["depth"]) for row in compression]
        states = [int(row["stateCount"]) for row in compression]
        transitions = [int(row["transitionCount"]) for row in compression]
        compression_axis.set_title("(a) Exact suffix-state compression", loc="left", pad=5)
        compression_axis.plot(depth, states, color=BLUE, marker="o", markersize=2.8, linewidth=1.0, label="retained states")
        compression_axis.plot(depth, transitions, color=GOLD, marker="s", markersize=2.4, linewidth=.75, linestyle="--", label="transitions")
        compression_axis.fill_between(depth, states, color=PALE_BLUE, alpha=.75)
        compression_axis.set_yscale("log")
        compression_axis.set_xlabel("suffix depth")
        compression_axis.set_ylabel("exact count")
        compression_axis.set_xticks(depth)
        compression_axis.grid(color=GRID, linewidth=.3)
        compression_axis.legend(frameon=False, fontsize=2.8, loc="upper left")
        compression_axis.text(.04, .08, "273,823,760 raw paths", transform=compression_axis.transAxes, fontsize=2.9, color=RUST)
        compression_axis.text(.58, .08, "max 105,499 states", transform=compression_axis.transAxes, fontsize=2.9, color=BLUE)

        lower = float(summary["oneCycleLower"])
        upper = float(summary["oneCycleUpper"])
        midpoint = (lower + upper) / 2
        half_width = (upper - lower) / 2
        tail = float(summary["oneCycleTail"])
        interval_axis.set_title("(b) Exact first-cycle heat enclosure", loc="left", pad=5)
        scaled_half_width = half_width * 1e11
        interval_axis.errorbar(
            [0], [0], xerr=[scaled_half_width], fmt="o", color=RUST,
            ecolor=RUST, capsize=4, markersize=4, linewidth=1.0,
        )
        interval_axis.set_xlim(-8, 8)
        interval_axis.set_yticks([])
        interval_axis.set_xlabel(r"$[S_{8,q}^{(M=16)}-0.0074150893806]\times10^{11}$")
        interval_axis.grid(axis="x", color=GRID, linewidth=.3)
        interval_axis.text(.04, .82, r"strictly positive rational interval", transform=interval_axis.transAxes, fontsize=3.1, color=RUST)
        interval_axis.text(.04, .66, rf"midpoint {midpoint:.13f}", transform=interval_axis.transAxes, fontsize=3.0, color=INK)
        interval_axis.text(.04, .50, rf"Taylor tail $<{tail:.3e}$", transform=interval_axis.transAxes, fontsize=3.0, color=BLUE)
        interval_axis.text(.04, .20, "finite block only; no asymptotic sign inference", transform=interval_axis.transAxes, fontsize=2.9, color=MUTED)

        degree = [int(row["degree"]) for row in convergence]
        scaled = [float(row["scaledValueTimes1e8"]) for row in convergence]
        jet_axis.set_title("(c) The complete dominant heat-jet pairing stabilizes by degree eight", loc="left", pad=5)
        jet_axis.plot(degree, scaled, color=BLUE, marker="o", linewidth=1.05, markersize=3.0, label=r"cumulative pairing $10^8 B_d$")
        jet_axis.axhline(0, color=INK, linewidth=.6)
        jet_axis.axhline(scaled[-1], color=RUST, linewidth=.7, linestyle="--")
        jet_axis.set_xlim(-.2, 8.2)
        jet_axis.set_xticks(degree)
        jet_axis.set_xlabel("centred jet degree d")
        jet_axis.set_ylabel(r"$10^8 B_d$")
        jet_axis.grid(color=GRID, linewidth=.3)
        jet_axis.text(.48, .78, rf"$B_8={float(summary['degreeEightJetPilot']):.16e}$", transform=jet_axis.transAxes, fontsize=3.15, color=RUST)
        jet_axis.text(.48, .64, r"$|B_8-B_7|=4.27\times10^{-17}$", transform=jet_axis.transAxes, fontsize=3.05, color=BLUE)
        maximum_residual = max(float(row["relativeLinearResidual"]) for row in residuals)
        jet_axis.text(.48, .50, rf"max relative moment residual ${maximum_residual:.2e}$", transform=jet_axis.transAxes, fontsize=3.0, color=GREEN)
        jet_axis.legend(frameon=False, fontsize=2.9, loc="upper right")

        figure.text(
            .055, .055,
            "Claim boundary: panel (b) is exact; panel (c) is a binary64 convergence pilot. A strict dominant sign still needs defect-resolvent and ninth-derivative bounds.",
            fontsize=3.25, color=MUTED,
        )
        metadata = {"Creator": "R0.68B-2 eighth-order heat gates", "Date": None}
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
