#!/usr/bin/env python3
"""Render the R0.68B-2f/g/h corrected dominant-heat figure."""

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
        ) + "\n",
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
    moments = rows("moment-radius-by-degree.csv")
    heat = rows("heat-partial-by-degree.csv")
    budget = rows("sign-budget.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r068b2fgh-corrected-heat"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.08,
            right=0.955,
            bottom=0.17,
            top=0.79,
            width_ratios=(1.04, 0.96),
            height_ratios=(0.52, 0.48),
            hspace=0.68,
            wspace=0.34,
        )
        radius_axis = figure.add_subplot(grid[0, 0])
        heat_axis = figure.add_subplot(grid[0, 1])
        budget_axis = figure.add_subplot(grid[1, :])
        figure.suptitle(
            "Certification chain for one fixed eighth-order dominant heat coefficient",
            x=0.055,
            y=0.954,
            ha="left",
            fontsize=7.35,
            color=INK,
        )
        figure.text(
            0.055,
            0.894,
            "14,350,336 moment intervals  ·  8,008 heat channels  ·  44,514 signature classes  ·  corrected upper endpoint < 0",
            ha="left",
            fontsize=3.65,
            color=MUTED,
        )
        blossom(figure)

        degrees = [int(row["degree"]) for row in moments]
        radii = [float(row["maximumRadius"]) for row in moments]
        centred_maximum = float(moments[0]["centredGlobalMaximumRadius"])
        radius_axis.semilogy(
            degrees,
            radii,
            color=BLUE,
            marker="o",
            markerfacecolor=PALE_BLUE,
            markeredgecolor=BLUE,
            markersize=2.8,
            linewidth=0.9,
        )
        radius_axis.axhline(
            centred_maximum,
            color=RUST,
            linestyle="--",
            linewidth=0.75,
            label="global centred maximum",
        )
        radius_axis.set_title("(a) Raw moment interval radius by degree", loc="left", pad=5)
        radius_axis.set_xlabel("total spatial degree d")
        radius_axis.set_ylabel("maximum radius")
        radius_axis.set_xticks(degrees)
        radius_axis.set_ylim(1e-34, 8e-20)
        radius_axis.grid(axis="y", which="major", color=GRID, linewidth=0.3)
        radius_axis.legend(frameon=False, fontsize=2.75, loc="lower right")
        radius_axis.text(
            0.04,
            0.87,
            r"degree 10: $7.912\times10^{-22}$",
            transform=radius_axis.transAxes,
            fontsize=2.85,
            color=INK,
        )

        heat_values = [float(row["centreTimes1e8"]) for row in heat]
        heat_axis.plot(
            degrees,
            heat_values,
            color=RUST,
            marker="s",
            markerfacecolor=PALE_GOLD,
            markeredgecolor=RUST,
            markersize=2.8,
            linewidth=0.9,
        )
        heat_axis.axhline(0, color=INK, linewidth=0.5)
        heat_axis.set_title("(b) Certified heat Taylor partial value", loc="left", pad=5)
        heat_axis.set_xlabel("maximum spatial degree d")
        heat_axis.set_ylabel(r"$10^8 B_{\leq d}$")
        heat_axis.set_xticks(degrees)
        heat_axis.set_ylim(-1.59, -1.35)
        heat_axis.grid(axis="y", color=GRID, linewidth=0.3)
        heat_axis.text(
            0.04,
            0.10,
            r"$B_{\leq10}=-1.49238243185\times10^{-8}$",
            transform=heat_axis.transAxes,
            fontsize=2.85,
            color=INK,
        )

        components = [row["component"] for row in budget]
        values = [float(row["valueTimes1e8"]) for row in budget]
        bars = budget_axis.bar(
            range(3),
            values,
            width=0.56,
            color=[PALE_BLUE, PALE_GOLD, "white"],
            edgecolor=[BLUE, GOLD, RUST],
            linewidth=0.75,
        )
        bars[0].set_hatch("//")
        bars[1].set_hatch("..")
        bars[2].set_hatch("xx")
        budget_axis.set_title("(c) Guarded sign budget after the complete defect correction", loc="left", pad=5)
        budget_axis.set_xticks(range(3), components)
        budget_axis.set_ylabel(r"$10^8$ times magnitude")
        budget_axis.set_ylim(0, 1.72)
        budget_axis.grid(axis="y", color=GRID, linewidth=0.3)
        for index, value in enumerate(values):
            budget_axis.text(
                index,
                value + 0.055,
                f"{value:.4f}",
                ha="center",
                fontsize=3.0,
                color=INK,
            )
        budget_axis.text(
            0.61,
            0.79,
            r"$|B_{10}|_{\rm lower}-\Delta_{\rm upper}\geq 0.2873\times10^{-8}$",
            transform=budget_axis.transAxes,
            fontsize=3.0,
            color=RUST,
        )
        budget_axis.text(
            0.61,
            0.64,
            r"corrected interval: $[-2.6974,-0.2873]\times10^{-8}$",
            transform=budget_axis.transAxes,
            fontsize=2.9,
            color=MUTED,
        )

        figure.text(
            0.055,
            0.055,
            "Claim boundary: a strict sign for one fixed eighth-order coefficient. All Picard orders, singularity formation, and general 3D regularity remain open.",
            fontsize=3.25,
            color=MUTED,
        )
        metadata = {
            "Creator": "R0.68B-2f/g/h guarded certificates",
            "Date": None,
        }
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    with (HERE / "plot-resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream,
            fieldnames=["elapsedSeconds", "maximumRssMiB", "status"],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerow({
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        })


if __name__ == "__main__":
    draw()
