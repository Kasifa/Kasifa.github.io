#!/usr/bin/env python3
"""Render the formal R0.67B journal figure."""

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
PALE_BLUE = "#e4edf2"
PALE_RUST = "#f2e5df"
PALE_GOLD = "#f1eadb"
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
    direct = rows("direct-levels.csv")
    levels = [int(row["level"]) for row in direct]
    masses = [int(row["maximumAbsoluteMass"]) for row in direct]
    normalized_moments = [float(row["normalizedFirstMoment"]) for row in direct]
    scales = {row["name"]: row for row in rows("spectral-scales.csv")}
    mu_lower = float(scales["dominant root mu"]["lower"])
    mu_upper = float(scales["dominant root mu"]["upper"])

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r067b-affine-moment-lift"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=.085,
            right=.955,
            bottom=.155,
            top=.79,
            width_ratios=(1.12, 1),
            height_ratios=(.49, .51),
            hspace=.57,
            wspace=.34,
        )
        direct_axis = figure.add_subplot(grid[:, 0])
        scale_axis = figure.add_subplot(grid[0, 1])
        lift_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            r"An exact affine lift separates the dominant root from the $C^{1,1}$ remainder",
            x=.07,
            y=.954,
            ha="left",
            fontsize=8.1,
            color=INK,
        )
        figure.text(
            .07,
            .895,
            r"320 states  ·  1600 finite moments  ·  $26<256<300<\mu$  ·  all 13 certificate checks pass",
            ha="left",
            fontsize=3.85,
            color=MUTED,
        )
        blossom(figure)

        direct_axis.set_title(
            "(a) Independent direct-convolution checks",
            loc="left",
            pad=5,
        )
        direct_axis.plot(levels, masses, color=BLUE, linewidth=.8)
        direct_axis.scatter(
            levels, masses, s=13, facecolors="white", edgecolors=BLUE, linewidths=.65,
            label=r"maximum state mass $|m|$",
        )
        direct_axis.plot(levels, normalized_moments, color=RUST, linewidth=.8)
        direct_axis.scatter(
            levels, normalized_moments, s=11, marker="s", facecolors=RUST,
            edgecolors=RUST, linewidths=.55,
            label=r"maximum normalized first moment $|\ell|$",
        )
        direct_axis.set_yscale("log")
        direct_axis.set_xlim(.7, 7.3)
        direct_axis.set_xticks(levels)
        direct_axis.set_xlabel("binary level")
        direct_axis.set_ylabel("exact maximum (log scale)")
        direct_axis.grid(color=GRID, linewidth=.3, which="both")
        direct_axis.legend(loc="upper left", frameon=False, fontsize=3.35)
        direct_axis.annotate(
            "all mass and four first moments agree",
            xy=(7, normalized_moments[-1]),
            xytext=(3.75, 13000),
            fontsize=3.35,
            color=RUST,
            arrowprops={"arrowstyle": "-", "linewidth": .5, "color": RUST},
        )

        scale_axis.set_title("(b) Certified scale separation", loc="left", pad=5)
        scale_axis.axvspan(0, 26, color=PALE_BLUE, linewidth=0)
        scale_axis.axvspan(256, 300, color=PALE_GOLD, linewidth=0)
        for y, value, label, color, marker in (
            (.28, 26, r"$\rho(W)/16<26$", BLUE, "o"),
            (.58, 256, r"zero-affine scale $=256$", GOLD, "D"),
            (.88, 300, r"other finite spectrum $<300$", MUTED, "^"),
        ):
            scale_axis.hlines(y, 0, value, color=color, linewidth=1.1)
            scale_axis.scatter([value], [y], s=15, marker=marker, color=color, zorder=3)
            scale_axis.text(value - 4, y + .08, label, ha="right", fontsize=3.15, color=color)
        scale_axis.axvspan(mu_lower, mu_upper, color=PALE_RUST, linewidth=0)
        scale_axis.scatter([(mu_lower + mu_upper) / 2], [1.18], s=18, marker="s", color=RUST)
        scale_axis.text(420, 1.18, r"$\mu\in(402.425429345624,\,402.4254293456256)$",
                        ha="right", va="center", fontsize=3.0, color=RUST)
        scale_axis.set_xlim(0, 425)
        scale_axis.set_ylim(.08, 1.38)
        scale_axis.set_yticks([])
        scale_axis.set_xlabel("four-bit growth factor")
        scale_axis.grid(axis="x", color=GRID, linewidth=.3)

        lift_axis.set_title("(c) Exact block-triangular affine lift", loc="left", pad=5)
        labels = ["m", r"$\ell_A$", r"$\ell_B$", r"$\ell_C$", r"$\ell_D$"]
        lift_axis.set_xlim(-.7, 5.25)
        lift_axis.set_ylim(5.55, -.85)
        lift_axis.axis("off")
        for index, label in enumerate(labels):
            lift_axis.text(index + .5, -.25, label, ha="center", va="center", fontsize=3.5, color=MUTED)
            lift_axis.text(-.25, index + .5, label, ha="center", va="center", fontsize=3.5, color=MUTED)
        for row in range(5):
            for column in range(5):
                active_mass = row == 0 and column == 0
                active_coupling = row > 0 and column == 0
                active_diagonal = row > 0 and row == column
                active = active_mass or active_coupling or active_diagonal
                face = (
                    PALE_RUST if active_mass else
                    PALE_GOLD if active_coupling else
                    PALE_BLUE if active_diagonal else
                    "white"
                )
                lift_axis.add_patch(
                    Rectangle((column, row), 1, 1, facecolor=face, edgecolor=GRID, linewidth=.45)
                )
                if active_mass:
                    text = r"$W$"
                elif active_coupling:
                    text = rf"$E_{{{labels[row][6]}}}/16$"
                elif active_diagonal:
                    text = r"$W/16$"
                else:
                    text = "0"
                lift_axis.text(
                    column + .5, row + .5, text, ha="center", va="center",
                    fontsize=3.3, color=INK if active else GRID,
                )
        lift_axis.text(
            2.5,
            5.32,
            r"$\mathcal{M}\mathcal{P}=L\mathcal{M}$ and "
            r"$\mathcal{M}(\mathcal{P}J-JL)=0$",
            ha="center",
            fontsize=3.3,
            color=RUST,
        )

        figure.text(
            .07,
            .055,
            "Claim boundary: the affine lift and resolvent are certified; the complete heat-kernel projection sign is not.",
            fontsize=3.35,
            color=MUTED,
        )
        metadata = {"Creator": "R0.67B exact-affine-lift audit", "Date": None}
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    with (HERE / "plot-resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(
            stream, fieldnames=["elapsedSeconds", "maximumRssMiB", "status"], lineterminator="\n"
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
