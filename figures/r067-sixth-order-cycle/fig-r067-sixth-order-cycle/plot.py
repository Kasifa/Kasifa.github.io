#!/usr/bin/env python3
"""Render Figure R0.67A-1 at double-column journal size."""

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
    sequence = csv_rows("reachable-sequence.csv")
    spectrum = csv_rows("spectral-enclosures.csv")
    thresholds = csv_rows("thresholds.csv")
    r_values = [int(row["r"]) for row in sequence]
    normalized = [float(row["normalizedByMu"]) for row in sequence]
    ratios = [float(row["absoluteOverM2"]) for row in sequence]
    guides = [float(row["asymptoticGuideOverM2"]) for row in sequence]
    c_lower = -0.013063396815424176
    c_upper = -0.013063396815144788
    mu_lower = float(thresholds[1]["lower"])
    mu_upper = float(thresholds[1]["upper"])

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r067-sixth-order-cycle"
        figure = plt.figure(figsize=(178 / 25.4, 108 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.090,
            right=0.955,
            bottom=0.165,
            top=0.790,
            width_ratios=(1.16, 1.0),
            height_ratios=(0.48, 0.52),
            hspace=0.55,
            wspace=0.34,
        )
        convergence_axis = figure.add_subplot(grid[:, 0])
        spectrum_axis = figure.add_subplot(grid[0, 1])
        growth_axis = figure.add_subplot(grid[1, 1])

        figure.suptitle(
            r"A reachable zero-time sixth-order mode exceeds the conditional $C^{1,1}$ scale",
            x=0.072,
            y=0.954,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.072,
            0.895,
            r"Exact 320-state transfer  ·  $Y_r=C_{6,0}\mu^r+O(300^r)$  ·  $\mu>400>300>256$",
            ha="left",
            fontsize=3.9,
            color=MUTED,
        )
        blossom(figure)

        convergence_axis.set_title(
            r"(a) Exact reachable target after division by $\mu^r$",
            loc="left",
            pad=5,
        )
        convergence_axis.axhspan(c_lower, c_upper, color=PALE_RUST, zorder=0)
        convergence_axis.plot(r_values, normalized, color=MUTED, linewidth=0.7, zorder=1)
        positive_r = [r for r, value in zip(r_values, normalized) if value > 0]
        positive_y = [value for value in normalized if value > 0]
        negative_r = [r for r, value in zip(r_values, normalized) if value < 0]
        negative_y = [value for value in normalized if value < 0]
        convergence_axis.scatter(
            positive_r,
            positive_y,
            s=11,
            marker="o",
            facecolors="white",
            edgecolors=BLUE,
            linewidths=0.6,
            label="positive exact value",
            zorder=3,
        )
        convergence_axis.scatter(
            negative_r,
            negative_y,
            s=10,
            marker="s",
            facecolors=RUST,
            edgecolors=RUST,
            linewidths=0.5,
            label="negative exact value",
            zorder=3,
        )
        convergence_axis.axhline(0, color=INK, linewidth=0.7)
        convergence_axis.set_yscale("symlog", linthresh=0.003, linscale=1.1, base=10)
        convergence_axis.set_xlim(-0.5, 39.5)
        convergence_axis.set_ylim(-0.017, 1.65)
        convergence_axis.set_xlabel(r"cycle count $r$")
        convergence_axis.set_ylabel(r"$Y_r/\mu^r$ (symmetric-log)")
        convergence_axis.grid(color=GRID, linewidth=0.3, which="major")
        convergence_axis.legend(
            loc="upper right", frameon=False, fontsize=3.3, handletextpad=0.45
        )
        convergence_axis.annotate(
            "first negative\nr = 11",
            xy=(11, normalized[11]),
            xytext=(6.4, -0.012),
            fontsize=3.45,
            color=RUST,
            ha="center",
            arrowprops={"arrowstyle": "-", "color": RUST, "linewidth": 0.5},
        )
        convergence_axis.text(
            38.8,
            (c_lower + c_upper) / 2,
            r"strict $C_{6,0}<0$ band",
            ha="right",
            va="bottom",
            fontsize=3.35,
            color=RUST,
        )

        spectrum_axis.set_title(
            "(b) Exact spectral separation",
            loc="left",
            pad=5,
        )
        spectrum_axis.axvspan(-300, 300, color=PALE_BLUE, alpha=0.9, linewidth=0)
        spectrum_axis.text(
            -294,
            0.15,
            r"all $q_{10}$ roots: $|z|<300$",
            fontsize=3.15,
            color=BLUE,
            ha="left",
        )
        for row in spectrum[:4]:
            lower = float(row["lower"])
            upper = float(row["upper"])
            center = (lower + upper) / 2
            dominant = row["kind"] == "dominant"
            color = RUST if dominant else BLUE
            marker = "s" if dominant else "o"
            spectrum_axis.hlines(0.82, lower, upper, color=color, linewidth=2.0, zorder=2)
            spectrum_axis.scatter(
                [center],
                [0.82],
                s=14,
                marker=marker,
                facecolors=color if dominant else "white",
                edgecolors=color,
                linewidths=0.65,
                zorder=3,
            )
        spectrum_axis.axvline(256, color=INK, linestyle="--", linewidth=0.7)
        spectrum_axis.axvspan(mu_lower, mu_upper, color=RUST, alpha=0.7, linewidth=0)
        spectrum_axis.text(256, 1.24, "256 zero-affine scale", ha="center", fontsize=3.1, color=INK)
        spectrum_axis.text(405, 1.24, r"$\mu\approx402.425$", ha="center", fontsize=3.1, color=RUST)
        spectrum_axis.set_xlim(-315, 430)
        spectrum_axis.set_ylim(-0.05, 1.48)
        spectrum_axis.set_yticks([])
        spectrum_axis.set_xlabel("cycle eigenvalue / enclosure")
        spectrum_axis.grid(axis="x", color=GRID, linewidth=0.3)

        growth_axis.set_title(
            r"(c) Exact growth relative to $M_r^2=256^r$",
            loc="left",
            pad=5,
        )
        growth_axis.plot(
            r_values,
            ratios,
            color=BLUE,
            linewidth=0.8,
            marker="o",
            markersize=2.1,
            markerfacecolor="white",
            markeredgewidth=0.55,
            label=r"exact $|Y_r|/256^r$",
        )
        growth_axis.plot(
            r_values[16:],
            guides[16:],
            color=RUST,
            linewidth=0.8,
            linestyle="--",
            label=r"$|C_{6,0}|(\mu/256)^r$",
        )
        growth_axis.axhline(1, color=INK, linewidth=0.65)
        growth_axis.set_yscale("log")
        growth_axis.set_xlim(-0.5, 39.5)
        growth_axis.set_ylim(3e-2, 2e6)
        growth_axis.set_xlabel(r"cycle count $r$")
        growth_axis.set_ylabel(r"absolute ratio (log scale)")
        growth_axis.grid(color=GRID, linewidth=0.3, which="major")
        growth_axis.legend(
            loc="upper left", frameon=False, fontsize=3.15, handletextpad=0.45
        )
        growth_axis.text(
            39,
            ratios[-1] / 1.7,
            r"base ratio $\mu/256\approx1.572$",
            ha="right",
            va="top",
            fontsize=3.15,
            color=RUST,
        )

        figure.text(
            0.072,
            0.060,
            "Claim boundary: zero-time fixed-order correlation only; the complete five-simplex heat projection and full mild solution are not certified.",
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
            {
                "elapsedSeconds": f"{elapsed:.6f}",
                "rssMiB": f"{rss_mib():.3f}",
                "status": "exited:0",
            }
        )


if __name__ == "__main__":
    draw()
