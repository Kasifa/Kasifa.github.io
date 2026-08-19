#!/usr/bin/env python3
"""Render the R0.58 Duhamel critical-saturation figure."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
RED = "#8b4d43"
GREEN = "#466b5a"
PALE_BLUE = "#dbe5ea"
PALE_GOLD = "#efe1c7"
GRID = "#d5cec0"


def rows(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def normalize_svg(path: Path) -> None:
    content = path.read_text(encoding="utf-8").splitlines()
    path.write_text("\n".join(line.rstrip() for line in content) + "\n", encoding="utf-8")


def add_blossom(figure) -> None:
    center = (0.955, 0.942)
    for angle in range(0, 360, 72):
        theta = math.radians(angle)
        figure.add_artist(
            Ellipse(
                (
                    center[0] + 0.0105 * math.cos(theta),
                    center[1] + 0.013 * math.sin(theta),
                ),
                width=0.015,
                height=0.026,
                angle=angle - 90,
                facecolor=PALE_GOLD,
                edgecolor=GOLD,
                linewidth=0.45,
                transform=figure.transFigure,
                zorder=20,
            )
        )
    figure.text(center[0], center[1], "·", ha="center", va="center", fontsize=8, color=INK, zorder=21)


def geometric_midpoint(lower: list[float], upper: list[float]) -> list[float]:
    return [math.sqrt(left * right) for left, right in zip(lower, upper)]


def draw() -> None:
    coefficient = rows("duhamel-coefficient.csv")
    norms = rows("norm-envelopes.csv")
    flattening = rows("phase-flattening.csv")

    shells = [int(row["L"]) for row in coefficient]
    scaled_coefficients = [float(row["scaledCoefficient"]) for row in coefficient]
    block_lower = [float(row["blockLower"]) for row in norms]
    block_upper = [float(row["blockUpper"]) for row in norms]
    x_lower = [float(row["xMinusOneLower"]) for row in norms]
    x_upper = [float(row["xMinusOneUpper"]) for row in norms]
    h_lower = [float(row["hOneHalfLower"]) for row in norms]
    h_upper = [float(row["hOneHalfUpper"]) for row in norms]
    heat_lower = [float(row["heatBesovUniformLower"]) for row in norms]
    bmo_lower = [float(row["periodicBmoUniformLower"]) for row in norms]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r058-duhamel-critical-saturation"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.07,
            right=0.963,
            bottom=0.34,
            top=0.825,
            width_ratios=(1.0, 1.12, 1.0),
            wspace=0.39,
        )
        coefficient_axis = figure.add_subplot(grid[0, 0])
        norm_axis = figure.add_subplot(grid[0, 1])
        flattening_axis = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Exact Duhamel denominator: shell gain versus critical saturation",
            x=0.07,
            y=0.945,
            ha="left",
            fontsize=8.2,
            color=INK,
        )

        coefficient_axis.set_title("(a) Scaled exact coefficient", loc="left", pad=5)
        coefficient_axis.plot(
            shells,
            scaled_coefficients,
            color=BLUE,
            marker="o",
            markersize=2.8,
            markerfacecolor="white",
            markeredgewidth=0.55,
            linewidth=1.0,
            label=r"$L d_L(t_L)$",
        )
        limit_value = scaled_coefficients[-1]
        coefficient_axis.axhline(limit_value, color=GOLD, linestyle=(0, (4, 2)), linewidth=0.85, label="Riemann limit")
        coefficient_axis.fill_between(shells, [1 / 32] * len(shells), [1 / 2] * len(shells), color=PALE_BLUE, alpha=0.55, linewidth=0, label="certified envelope")
        coefficient_axis.text(
            0.96,
            0.20,
            r"$t_L=(\log 2)/(2L^2)$" + "\n" + r"$d_L\asymp L^{-1}$",
            transform=coefficient_axis.transAxes,
            ha="right",
            va="bottom",
            fontsize=4.0,
            color=INK,
        )
        coefficient_axis.set_xscale("log", base=2)
        coefficient_axis.set_xlim(1, 2**16)
        coefficient_axis.set_ylim(0, 0.54)
        coefficient_axis.set_xlabel(r"shell size $L$")
        coefficient_axis.set_ylabel(r"scaled coefficient $L d_L$")
        coefficient_axis.grid(color=GRID, linewidth=0.32, which="both")
        coefficient_axis.legend(loc="upper right", frameon=False, fontsize=3.55)

        norm_axis.set_title("(b) Certified bilinear scaling", loc="left", pad=5)
        norm_axis.loglog(shells, geometric_midpoint(block_lower, block_upper), color=GOLD, linewidth=1.0, label=r"block: $\Theta(L^{-2})$")
        norm_axis.fill_between(shells, block_lower, block_upper, color=PALE_GOLD, alpha=0.35, linewidth=0)
        norm_axis.loglog(shells, geometric_midpoint(x_lower, x_upper), color=BLUE, linewidth=1.05, label=r"$\mathcal X^{-1}$: $\Theta(L^{-1})$")
        norm_axis.fill_between(shells, x_lower, x_upper, color=PALE_BLUE, alpha=0.32, linewidth=0)
        norm_axis.loglog(shells, geometric_midpoint(h_lower, h_upper), color=RED, linewidth=0.9, linestyle=(0, (4, 2)), label=r"$\dot H^{1/2}$: $\Theta(L^{-3})$")
        norm_axis.loglog(shells, heat_lower, color=GREEN, linewidth=1.0, label=r"heat $B^{-1}$: $\Omega(1)$")
        norm_axis.loglog(shells, bmo_lower, color=INK, linewidth=0.9, linestyle=(0, (1, 2)), label=r"periodic $BMO^{-1}$: $\Omega(1)$")
        norm_axis.set_xlim(1, 2**16)
        norm_axis.set_ylim(1e-17, 2)
        norm_axis.set_xlabel(r"shell size $L$")
        norm_axis.set_ylabel("normalized bilinear quotient")
        norm_axis.grid(color=GRID, linewidth=0.32, which="both")
        norm_axis.legend(loc="lower left", frameon=False, fontsize=3.25)

        flattening_axis.set_title("(c) Deterministic phase flattening", loc="left", pad=5)
        flattening_shells = [int(row["L"]) for row in flattening]
        rs_values = [float(row["sampledRudinShapiroOverSqrtL"]) for row in flattening]
        positive_values = [float(row["allPositiveMaximumOverSqrtL"]) for row in flattening]
        flattening_axis.loglog(
            flattening_shells,
            rs_values,
            color=BLUE,
            marker="o",
            markersize=2.8,
            markerfacecolor="white",
            markeredgewidth=0.55,
            linewidth=1.0,
            label="Rudin–Shapiro (sampled)",
        )
        flattening_axis.axhline(math.sqrt(2), color=INK, linestyle=(0, (1, 2)), linewidth=0.8, label=r"exact bound $\sqrt2$")
        flattening_axis.loglog(flattening_shells, positive_values, color=GOLD, linestyle=(0, (4, 2)), linewidth=0.95, label="all-positive phases")
        flattening_axis.text(
            0.05,
            0.08,
            r"input: $O(\sqrt L)$" + "\n" + r"matched output: $a_n^2=1$",
            transform=flattening_axis.transAxes,
            ha="left",
            va="bottom",
            fontsize=4.0,
            color=INK,
        )
        flattening_axis.set_xlim(1, 2**16)
        flattening_axis.set_ylim(0.8, 400)
        flattening_axis.set_xlabel(r"number of phases $L=2^m$")
        flattening_axis.set_ylabel(r"$\sup_{|z|=1}|P_m(z)|/\sqrt L$")
        flattening_axis.grid(color=GRID, linewidth=0.32, which="both")
        flattening_axis.legend(loc="upper left", frameon=False, fontsize=3.45)

        figure.text(
            0.07,
            0.225,
            (
                r"Exact output: $d_L(t)=e^{-t}\sum_{N=L}^{2L-1}(1-e^{-2N^2t})/(2N^2)$. "
                r"At $t_L=(\log2)/(2L^2)$, $1/(32L)\leq d_L(t_L)\leq1/(2L)$ for every $L$."
            ),
            ha="left",
            va="top",
            fontsize=4.05,
            color=INK,
        )
        figure.text(
            0.07,
            0.165,
            (
                "Formal scope: 8,390,656 packet modes, Rudin–Shapiro length 4,194,304, "
                "24/24 checks; exact integer and Q(sqrt(2)) audit. Curves and sampled maxima are presentation data."
            ),
            ha="left",
            va="top",
            fontsize=3.8,
            color=MUTED,
        )
        figure.text(
            0.07,
            0.105,
            (
                "Conclusion: the time integral gives a genuine heat denominator, but critical negative regularity and "
                "phase flattening can consume its shell gain. This is not norm inflation or a Navier–Stokes regularity proof."
            ),
            ha="left",
            va="top",
            fontsize=3.8,
            color=MUTED,
        )
        add_blossom(figure)

        figure.savefig(HERE / "figure.pdf")
        figure.savefig(HERE / "figure.svg")
        figure.savefig(HERE / "figure.png", dpi=600)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")


if __name__ == "__main__":
    draw()
