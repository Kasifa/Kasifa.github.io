#!/usr/bin/env python3
"""Render the formal R0.67C-1 journal figure."""

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
    enumeration = rows("enumeration-by-a.csv")
    partial = rows("partial-sums.csv")
    scales = {row["name"]: float(row["value"]) for row in rows("certificate-scales.csv")}
    offsets = [int(row["a"]) for row in enumeration]
    valid = [int(row["validTuples"]) for row in enumeration]
    signed = [int(row["signedMass"]) for row in enumeration]
    degrees = [int(row["degree"]) for row in partial]
    sums = [float(row["partialSum"]) for row in partial]
    final_center = (scales["coefficient lower"] + scales["coefficient upper"]) / 2

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r067c1-one-cycle-heat"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=.083,
            right=.955,
            bottom=.16,
            top=.79,
            width_ratios=(1.03, 1.12),
            height_ratios=(.61, .39),
            hspace=.62,
            wspace=.34,
        )
        geometry_axis = figure.add_subplot(grid[:, 0])
        convergence_axis = figure.add_subplot(grid[0, 1])
        scale_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            "The complete first-cycle sixth-order heat coefficient is strictly positive",
            x=.068,
            y=.954,
            ha="left",
            fontsize=8.0,
            color=INK,
        )
        figure.text(
            .068,
            .895,
            r"$M=16$  ·  34,690 valid carrier tuples  ·  10 time orders  ·  degree-32 exact Taylor enclosure",
            ha="left",
            fontsize=3.8,
            color=MUTED,
        )
        blossom(figure)

        geometry_axis.set_title("(a) Exact carrier-constraint enumeration", loc="left", pad=5)
        geometry_axis.bar(
            offsets,
            valid,
            width=.74,
            color="#e4edf2",
            edgecolor=BLUE,
            linewidth=.45,
            label="valid tuples at fixed $a$",
        )
        geometry_axis.set_xlabel("positive-carrier offset $a$")
        geometry_axis.set_ylabel("valid $(b,c,d,e)$ tuples")
        geometry_axis.set_xticks(range(0, 16, 2))
        geometry_axis.grid(axis="y", color=GRID, linewidth=.3)
        signed_axis = geometry_axis.twinx()
        signed_axis.plot(offsets, signed, color=RUST, linewidth=.8)
        signed_axis.scatter(
            offsets,
            signed,
            s=10,
            marker="D",
            facecolor="white",
            edgecolor=RUST,
            linewidth=.55,
            label="signed mass contribution",
        )
        signed_axis.axhline(0, color=GRID, linewidth=.4)
        signed_axis.tick_params(axis="y", colors=RUST, pad=1)
        handles_a, labels_a = geometry_axis.get_legend_handles_labels()
        handles_b, labels_b = signed_axis.get_legend_handles_labels()
        geometry_axis.legend(handles_a + handles_b, labels_a + labels_b, loc="upper left", frameon=False, fontsize=3.25)
        geometry_axis.text(
            .04,
            .06,
            r"$sum_a N_a=34{,}690$" "\n" r"$\sum_a Y_a=500$",
            transform=geometry_axis.transAxes,
            fontsize=3.5,
            color=INK,
        )

        convergence_axis.set_title("(b) Five-simplex Taylor convergence", loc="left", pad=5)
        convergence_axis.axhspan(
            scales["coefficient lower"],
            scales["coefficient upper"],
            color=PALE_RUST,
            linewidth=0,
        )
        convergence_axis.axhline(final_center, color=RUST, linewidth=.55)
        convergence_axis.plot(degrees, sums, color=BLUE, linewidth=.8)
        convergence_axis.scatter(
            degrees,
            sums,
            s=9,
            facecolor="white",
            edgecolor=BLUE,
            linewidth=.5,
        )
        convergence_axis.set_xlim(-.5, 32.7)
        convergence_axis.set_xticks([0, 4, 8, 12, 16, 20, 24, 28, 32])
        convergence_axis.set_xlabel("Taylor degree $N$")
        convergence_axis.text(
            .015,
            .93,
            "partial coefficient",
            transform=convergence_axis.transAxes,
            fontsize=3.15,
            color=MUTED,
            va="top",
        )
        convergence_axis.grid(color=GRID, linewidth=.3)
        convergence_axis.annotate(
            r"$S_{6,q}=0.051669755156\ldots$",
            xy=(32, sums[-1]),
            xytext=(16.2, .105),
            fontsize=3.35,
            color=RUST,
            arrowprops={"arrowstyle": "-", "linewidth": .45, "color": RUST},
        )

        scale_axis.set_title("(c) Certified separation from the omitted tail", loc="left", pad=5)
        names = ["coefficient lower", "absolute Taylor tail"]
        values = [scales[name] for name in names]
        colors = [RUST, GOLD]
        markers = ["s", "o"]
        for y, value, color, marker in zip((1, 0), values, colors, markers):
            scale_axis.hlines(y, 1e-13, value, color=color, linewidth=1.25)
            scale_axis.scatter([value], [y], s=17, marker=marker, color=color, zorder=3)
        scale_axis.set_xscale("log")
        scale_axis.set_xlim(1e-13, .2)
        scale_axis.set_ylim(-.6, 1.6)
        scale_axis.set_yticks([0, 1], ["tail upper bound", "coefficient lower bound"])
        scale_axis.set_xlabel("absolute magnitude (log scale)")
        scale_axis.grid(axis="x", color=GRID, linewidth=.3, which="both")
        scale_axis.text(
            .98,
            .88,
            r"signal/tail $>2.65\times10^{10}$",
            transform=scale_axis.transAxes,
            ha="right",
            fontsize=3.4,
            color=INK,
        )

        figure.text(
            .068,
            .055,
            "Claim boundary: this is an exact M=16 calibration point; the dominant asymptotic heat projection is still open.",
            fontsize=3.35,
            color=MUTED,
        )
        metadata = {"Creator": "R0.67C-1 exact heat audit", "Date": None}
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
        writer.writerow(
            {
                "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
                "maximumRssMiB": f"{rss_mib():.3f}",
                "status": "passed",
            }
        )


if __name__ == "__main__":
    draw()
