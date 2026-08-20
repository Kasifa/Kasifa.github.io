#!/usr/bin/env python3
"""Render the R0.69A complete target Picard closure figure."""

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
PALE_GOLD = "#f4ead6"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()
        ) + "\n",
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
    limits = rows("limit-interval.csv")
    rates = rows("decay-rates.csv")
    envelopes = rows("rate-envelopes.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r069a-full-picard-closure"
        figure = plt.figure(figsize=(178 / 25.4, 103 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2, 2, left=.095, right=.955, bottom=.17, top=.79,
            width_ratios=(.92, 1.25), height_ratios=(.48, .52),
            hspace=.62, wspace=.35,
        )
        interval_axis = figure.add_subplot(grid[0, 0])
        rate_axis = figure.add_subplot(grid[1, 0])
        envelope_axis = figure.add_subplot(grid[:, 1])
        figure.suptitle(
            "Every Picard order closes on one periodic target coefficient",
            x=.068, y=.954, ha="left", fontsize=8.0, color=INK,
        )
        figure.text(
            .068, .895,
            r"quartic-critical amplitude  ·  complete invariant-shear series  ·  $M_r=16^r$  ·  source-locked R0.69A certificate",
            ha="left", fontsize=3.8, color=MUTED,
        )
        blossom(figure)

        correction = limits[0]
        lower = float(correction["lowerTimes1e8"])
        upper = float(correction["upperTimes1e8"])
        centre = (lower + upper) / 2
        interval_axis.set_title("(a) Surviving nonlinear correction", loc="left", pad=5)
        interval_axis.hlines(0, lower, upper, color=BLUE, linewidth=4.0)
        interval_axis.scatter([lower, upper], [0, 0], color=BLUE, marker="|", s=65)
        interval_axis.scatter([centre], [0], color=INK, marker="o", s=18, zorder=3)
        interval_axis.axvline(0, color=RUST, linewidth=.6, linestyle="--")
        interval_axis.set_xlim(0, 2.85)
        interval_axis.set_ylim(-.55, .55)
        interval_axis.set_yticks([])
        interval_axis.set_xlabel(r"$10^8\,(R_\infty-1)$")
        interval_axis.grid(axis="x", color=GRID, linewidth=.3)
        interval_axis.text(
            centre, .23, f"[{lower:.4f}, {upper:.4f}]",
            ha="center", va="bottom", fontsize=3.25, color=BLUE,
        )
        interval_axis.text(
            .03, .08, "strictly positive",
            transform=interval_axis.transAxes, fontsize=3.25, color=BLUE,
        )

        labels = ["sixth", "eighth", r"$n\geq10$"]
        values = [float(row["rate"]) for row in rates]
        colors = [RUST, GOLD, BLUE]
        markers = ["D", "s", "o"]
        rate_axis.set_title("(b) Certified one-block decay", loc="left", pad=5)
        for index, (label, value, color, marker) in enumerate(
            zip(labels, values, colors, markers)
        ):
            y = len(values) - index - 1
            rate_axis.hlines(y, 0, value, color=color, linewidth=1.2)
            rate_axis.scatter([value], [y], color=color, marker=marker, s=18)
            rate_axis.text(value + .018, y, f"{value:.4f}", va="center", fontsize=3.1, color=color)
        rate_axis.axvline(1, color=INK, linewidth=.55)
        rate_axis.set_xlim(0, 1.04)
        rate_axis.set_yticks(range(3), list(reversed(labels)))
        rate_axis.set_xlabel("factor per four-bit block")
        rate_axis.grid(axis="x", color=GRID, linewidth=.3)

        blocks = [int(row["block"]) for row in envelopes]
        series = [
            ("sixth_order", "sixth", RUST, "D", "-"),
            ("eighth_order", "eighth", GOLD, "s", "--"),
            ("orders_at_least_ten", r"$n\geq10$ tail rate", BLUE, "o", "-."),
        ]
        envelope_axis.set_title("(c) Rate envelopes vanish after amplitude scaling", loc="left", pad=5)
        for key, label, color, marker, linestyle in series:
            values_y = [float(row[key]) for row in envelopes]
            envelope_axis.semilogy(
                blocks, values_y, color=color, marker=marker, markevery=4,
                markersize=2.5, linewidth=1.05, linestyle=linestyle, label=label,
            )
        envelope_axis.fill_between(
            blocks,
            [float(row["orders_at_least_ten"]) for row in envelopes],
            1e-9,
            color=PALE_BLUE,
            alpha=.55,
            zorder=-2,
        )
        envelope_axis.set_xlim(0, 20)
        envelope_axis.set_ylim(1e-8, 1.2)
        envelope_axis.set_xlabel("four-bit block r")
        envelope_axis.set_ylabel(r"rate factor $\rho^r$  (unit prefactor)")
        envelope_axis.grid(color=GRID, linewidth=.3, which="both")
        envelope_axis.legend(loc="upper right", frameon=False, fontsize=3.2)
        envelope_axis.text(
            .035, .055,
            "The quartic contribution tends to a nonzero constant;\nall remaining orders vanish.",
            transform=envelope_axis.transAxes, fontsize=3.35, color=INK,
            bbox={"facecolor": PALE_GOLD, "edgecolor": "none", "pad": 2.0},
        )

        figure.text(
            .068, .054,
            "Claim boundary: one target coefficient in a globally smooth invariant-shear class; arbitrary 3D transverse perturbations and singularity criteria remain open.",
            fontsize=3.25, color=MUTED,
        )
        metadata = {"Creator": "R0.69A complete Picard closure", "Date": None}
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
