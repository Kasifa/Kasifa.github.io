#!/usr/bin/env python3
"""Render the R0.59 multi-output critical-saturation figure."""

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


def draw() -> None:
    profiles = rows("target-profiles.csv")
    witnesses = rows("multi-output-witness.csv")
    flattening = rows("tensor-flattening.csv")

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r059-multi-output-critical-saturation"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.07,
            right=0.963,
            bottom=0.34,
            top=0.825,
            width_ratios=(1.08, 1.02, 1.0),
            wspace=0.40,
        )
        profile_axis = figure.add_subplot(grid[0, 0])
        witness_axis = figure.add_subplot(grid[0, 1])
        flattening_axis = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "One flattened high shell sustains a growing coherent output set",
            x=0.07,
            y=0.945,
            ha="left",
            fontsize=8.2,
            color=INK,
        )

        profile_axis.set_title("(a) All target coefficients remain positive", loc="left", pad=5)
        colors = (GOLD, GREEN, RED, BLUE)
        for color, length in zip(colors, (4, 16, 64, 256)):
            selected = [row for row in profiles if int(row["L"]) == length]
            profile_axis.plot(
                [float(row["mOverM"]) for row in selected],
                [float(row["scaledCoefficient"]) for row in selected],
                color=color,
                linewidth=0.95,
                label=rf"$L={length}$",
            )
        first_profile = [row for row in profiles if int(row["L"]) == 4]
        profile_axis.fill_between(
            [float(row["mOverM"]) for row in first_profile],
            [float(row["scaledLower"]) for row in first_profile],
            [float(row["scaledUpper"]) for row in first_profile],
            color=PALE_GOLD,
            alpha=0.42,
            linewidth=0,
            label="certified envelope",
        )
        profile_axis.text(
            0.05,
            0.91,
            r"$K_M=\{(0,m,0):1\leq m\leq M\}$" + "\n" + r"$M=256,\ H=4LM$",
            transform=profile_axis.transAxes,
            ha="left",
            va="top",
            fontsize=3.85,
            color=INK,
        )
        profile_axis.set_xlim(0, 1.02)
        profile_axis.set_ylim(0, 0.11)
        profile_axis.set_xlabel(r"relative output frequency $m/M$")
        profile_axis.set_ylabel(r"scaled coefficient $H d_m(t_H)$")
        profile_axis.grid(color=GRID, linewidth=0.32)
        profile_axis.legend(loc="lower right", frameon=False, fontsize=3.35)

        witness_axis.set_title("(b) Total heat witness scales as $H^{-1}$", loc="left", pad=5)
        witness_lengths = (1, 4, 16, 64)
        for index, (color, length) in enumerate(zip(colors, witness_lengths)):
            selected = [row for row in witnesses if int(row["L"]) == length]
            witness_axis.semilogx(
                [int(row["M"]) for row in selected],
                [float(row["scaledHeatWitness"]) for row in selected],
                base=2,
                color=color,
                marker="o",
                markersize=2.2,
                markerfacecolor="white",
                markeredgewidth=0.5,
                linewidth=0.9,
                label=(r"$L=1,4,16,64$ (collapse)" if index == len(witness_lengths) - 1 else "_nolegend_"),
            )
        heat_lower = float(witnesses[0]["certifiedScaledHeatLower"])
        bmo_lower = float(witnesses[0]["certifiedScaledBmoLower"])
        witness_axis.axhline(
            heat_lower,
            color=INK,
            linestyle=(0, (4, 2)),
            linewidth=0.8,
            label=r"certified heat lower bound",
        )
        witness_axis.axhline(
            bmo_lower,
            color=MUTED,
            linestyle=(0, (1, 2)),
            linewidth=0.8,
            label=r"certified $BMO^{-1}$ lower bound",
        )
        witness_axis.set_xscale("log", base=2)
        witness_axis.set_yscale("log")
        witness_axis.set_xlim(1, 2**10)
        witness_axis.set_ylim(2e-4, 2e-2)
        witness_axis.set_xlabel(r"number of coherent outputs $M$")
        witness_axis.set_ylabel(r"scaled output witness $H\,W$")
        witness_axis.grid(color=GRID, linewidth=0.32, which="both")
        witness_axis.legend(
            loc="upper right",
            frameon=True,
            facecolor="white",
            edgecolor="none",
            framealpha=0.88,
            fontsize=3.05,
        )

        flattening_axis.set_title("(c) Tensor phase flattening", loc="left", pad=5)
        phases = [int(row["totalPhases"]) for row in flattening]
        rs_values = [float(row["sampledTensorOverSqrtLM"]) for row in flattening]
        positive_values = [float(row["allPositiveMaximumOverSqrtLM"]) for row in flattening]
        flattening_axis.loglog(
            phases,
            rs_values,
            color=BLUE,
            marker="o",
            markersize=2.8,
            markerfacecolor="white",
            markeredgewidth=0.55,
            linewidth=1.0,
            label="tensor Rudin–Shapiro (sampled)",
        )
        flattening_axis.axhline(2, color=INK, linestyle=(0, (1, 2)), linewidth=0.8, label="exact full-tensor bound")
        flattening_axis.loglog(
            phases,
            positive_values,
            color=GOLD,
            linestyle=(0, (4, 2)),
            linewidth=0.95,
            label="all-positive phases",
        )
        flattening_axis.text(
            0.95,
            0.61,
            r"input: $O(\sqrt{LM})$" + "\n" + r"all $M$ matches: $c_{r,n}^2=1$",
            transform=flattening_axis.transAxes,
            ha="right",
            va="center",
            fontsize=3.85,
            color=INK,
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.84, "pad": 1.2},
        )
        flattening_axis.set_xlim(1, 2**20)
        flattening_axis.set_ylim(0.8, 2e3)
        flattening_axis.set_xlabel(r"number of high-frequency phases $LM$")
        flattening_axis.set_ylabel(r"spatial maximum divided by $\sqrt{LM}$")
        flattening_axis.grid(color=GRID, linewidth=0.32, which="both")
        flattening_axis.legend(
            loc="upper left",
            frameon=True,
            facecolor="white",
            edgecolor="none",
            framealpha=0.88,
            fontsize=3.15,
        )

        figure.text(
            0.07,
            0.225,
            (
                r"Exact target output: $d_m(t_H)=m e^{-m^2t_H}\sum_{n=0}^{L-1}"
                r"(1-e^{-2R_{m-1,n}^2t_H})/(2R_{m-1,n}^2)$, with $H=4LM$."
            ),
            ha="left",
            va="top",
            fontsize=4.0,
            color=INK,
        )
        figure.text(
            0.07,
            0.165,
            (
                "Formal scope: 4,190,209 packet modes, 29,822,521 interaction pairs, "
                "16,760,836 tensor prefixes, and 24/24 exact checks. Display curves use floating point only for presentation."
            ),
            ha="left",
            va="top",
            fontsize=3.75,
            color=MUTED,
        )
        figure.text(
            0.07,
            0.105,
            (
                "Conclusion: output multiplicity and isotropic square functions do not force an extra shell factor in the first "
                "critical Picard iterate. This is not norm inflation, nonlinear remainder control, or a regularity proof."
            ),
            ha="left",
            va="top",
            fontsize=3.75,
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
