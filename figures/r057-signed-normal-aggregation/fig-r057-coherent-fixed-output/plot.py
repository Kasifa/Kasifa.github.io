#!/usr/bin/env python3
"""Render the R0.57 coherent fixed-output packet figure."""

from __future__ import annotations

import csv
import math
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Ellipse, FancyArrowPatch


HERE = Path(__file__).resolve().parent
STYLE = HERE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
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
    figure.text(
        center[0],
        center[1],
        "·",
        ha="center",
        va="center",
        fontsize=8,
        color=INK,
        zorder=21,
    )


def draw() -> None:
    geometry = rows("packet-geometry.csv")
    localization = rows("localization.csv")
    heat = rows("heat-response.csv")

    packet_sizes = [int(row["L"]) for row in localization]
    scale_ratios = [float(row["scaleRatioDecimal"]) for row in localization]
    cap_angles = [float(row["capAngleRadiansDecimal"]) for row in localization]
    norm_ratios = [float(row["fixedOutputNormRatioDecimal"]) for row in localization]
    scaled_times = [float(row["scaledTimeTau"]) for row in heat]
    output_response = [float(row["normalizedOutput"]) for row in heat]
    norm_response = [float(row["normalizedBlockNormProduct"]) for row in heat]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r057-coherent-fixed-output"
        figure = plt.figure(figsize=(178 / 25.4, 105 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.07,
            right=0.963,
            bottom=0.34,
            top=0.825,
            width_ratios=(1.08, 1.0, 1.05),
            wspace=0.39,
        )
        geometry_axis = figure.add_subplot(grid[0, 0])
        localization_axis = figure.add_subplot(grid[0, 1])
        heat_axis = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Coherent fixed-output saturation of the normal Fourier–Leray channel",
            x=0.07,
            y=0.945,
            ha="left",
            fontsize=8.2,
            color=INK,
        )

        geometry_axis.set_title("(a) One-shell packet geometry ($L=8$)", loc="left", pad=5)
        p_x = [int(row["pX"]) for row in geometry]
        p_y = [int(row["pY"]) for row in geometry]
        q_x = [int(row["qX"]) for row in geometry]
        q_y = [int(row["qY"]) for row in geometry]
        geometry_axis.scatter(
            p_x,
            p_y,
            s=15,
            marker="o",
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.65,
            zorder=4,
        )
        geometry_axis.scatter(
            q_x,
            q_y,
            s=15,
            marker="s",
            facecolor=PALE_GOLD,
            edgecolor=GOLD,
            linewidth=0.65,
            zorder=4,
        )
        geometry_axis.scatter(
            [0],
            [1],
            s=24,
            marker="D",
            facecolor="white",
            edgecolor=INK,
            linewidth=0.75,
            zorder=6,
        )
        selected = 12
        geometry_axis.add_patch(
            FancyArrowPatch(
                (0, 0),
                (selected, 0),
                arrowstyle="-|>",
                mutation_scale=5,
                color=BLUE,
                linewidth=0.75,
                zorder=3,
            )
        )
        geometry_axis.add_patch(
            FancyArrowPatch(
                (selected, 0),
                (0, 1),
                arrowstyle="-|>",
                mutation_scale=5,
                color=GOLD,
                linewidth=0.75,
                linestyle=(0, (3, 2)),
                zorder=3,
            )
        )
        geometry_axis.annotate(
            r"$p_{12}$",
            xy=(selected, 0),
            xytext=(10.2, -0.34),
            fontsize=4.1,
            color=BLUE,
        )
        geometry_axis.annotate(
            r"$q_{12}=k-p_{12}$",
            xy=(-selected, 1),
            xytext=(-15.5, 1.32),
            fontsize=4.0,
            color=GOLD,
        )
        geometry_axis.annotate(
            r"$k=e_2$",
            xy=(0, 1),
            xytext=(1.1, 1.24),
            fontsize=4.1,
            color=INK,
        )
        geometry_axis.text(
            0.5,
            0.08,
            r"all outputs $\parallel e_3$  $\odot$",
            transform=geometry_axis.transAxes,
            ha="center",
            va="bottom",
            fontsize=4.0,
            color=BLUE,
        )
        geometry_axis.axhline(0, color=GRID, linewidth=0.35, zorder=0)
        geometry_axis.axhline(1, color=GRID, linewidth=0.35, zorder=0)
        geometry_axis.set_xlim(-16.5, 16.5)
        geometry_axis.set_ylim(-0.55, 1.55)
        geometry_axis.set_xlabel("Fourier $x$ coordinate")
        geometry_axis.set_ylabel("Fourier $y$ coordinate")
        geometry_axis.set_yticks([0, 1])
        geometry_axis.grid(axis="x", color=GRID, linewidth=0.28)
        geometry_axis.legend(
            handles=[
                Line2D(
                    [0],
                    [0],
                    marker="o",
                    markersize=3.6,
                    markerfacecolor=PALE_BLUE,
                    markeredgecolor=BLUE,
                    linewidth=0,
                    label=r"$p_N=(N,0,0)$",
                ),
                Line2D(
                    [0],
                    [0],
                    marker="s",
                    markersize=3.4,
                    markerfacecolor=PALE_GOLD,
                    markeredgecolor=GOLD,
                    linewidth=0,
                    label=r"$q_N=(-N,1,0)$",
                ),
            ],
            loc="lower left",
            frameon=False,
            fontsize=3.7,
        )

        localization_axis.set_title("(b) Localization versus sharp ratio", loc="left", pad=5)
        localization_axis.plot(
            packet_sizes,
            norm_ratios,
            color=BLUE,
            linewidth=1.2,
            label=r"fixed-output ratio $=1$",
        )
        localization_axis.plot(
            packet_sizes,
            scale_ratios,
            color=GOLD,
            linewidth=1.0,
            linestyle=(0, (4, 2)),
            label=r"shell ratio $1/L$",
        )
        localization_axis.plot(
            packet_sizes,
            cap_angles,
            color=INK,
            linewidth=0.8,
            linestyle=(0, (1, 2)),
            label=r"cap aperture $\arctan(1/L)$",
        )
        localization_axis.scatter(
            [200000],
            [1],
            marker="D",
            s=18,
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.65,
            zorder=5,
        )
        localization_axis.annotate(
            "formal audit\n$L=200{,}000$",
            xy=(200000, 1),
            xytext=(12200, 0.11),
            fontsize=3.7,
            color=BLUE,
            arrowprops={"arrowstyle": "-", "color": BLUE, "linewidth": 0.45},
        )
        localization_axis.set_xscale("log", base=2)
        localization_axis.set_yscale("log", base=10)
        localization_axis.set_xlim(1, 2**18)
        localization_axis.set_ylim(2e-6, 1.7)
        localization_axis.set_xlabel(r"packet size $L$")
        localization_axis.set_ylabel("dimensionless value")
        localization_axis.grid(color=GRID, linewidth=0.32, which="both")
        localization_axis.legend(loc="lower left", frameon=False, fontsize=3.65)

        heat_axis.set_title("(c) Instantaneous heat equality ($L=64$)", loc="left", pad=5)
        heat_axis.semilogy(
            scaled_times,
            output_response,
            color=BLUE,
            linewidth=1.15,
            label=r"$|\mathfrak B_k(U(t),V(t))|/|\mathfrak B_k(U,V)|$",
        )
        heat_axis.semilogy(
            scaled_times[::5],
            norm_response[::5],
            color=GOLD,
            linewidth=0,
            marker="o",
            markersize=2.8,
            markerfacecolor="white",
            markeredgewidth=0.65,
            label=r"$\|U(t)\|_2\|V(t)\|_2/(\|U\|_2\|V\|_2)$",
        )
        heat_axis.text(
            0.95,
            0.94,
            r"ratio $=1$ for every $t\geq0$",
            transform=heat_axis.transAxes,
            ha="right",
            va="top",
            fontsize=4.1,
            color=BLUE,
        )
        heat_axis.set_xlim(0, 4)
        heat_axis.set_ylim(2e-6, 1.3)
        heat_axis.set_xlabel(r"scaled time $\tau=\nu L^2t$")
        heat_axis.set_ylabel("normalized instantaneous magnitude")
        heat_axis.grid(color=GRID, linewidth=0.32, which="both")
        heat_axis.legend(loc="lower left", frameon=False, fontsize=3.45)

        figure.text(
            0.07,
            0.225,
            (
                r"Exact packet: $p_N=(N,0,0)$, $q_N=(-N,1,0)$, "
                r"$\widehat U(p_N)=c_Ne_2$, $\widehat V(q_N)=c_Ne_3$; "
                r"every forward term is $c_N^2e_3$ and every exchanged term is zero."
            ),
            ha="left",
            va="top",
            fontsize=4.1,
            color=INK,
        )
        figure.text(
            0.07,
            0.165,
            (
                "Formal scope: 200,000 coherent pairs, 400,000 ordered output pairs, "
                "1,000,000 all-index regressions, 20/20 checks; exact integer audit. "
                "The plotted heat curve is presentation data for an analytic identity."
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
                "Conclusion: signed fixed-output aggregation, exchange symmetrization, "
                "one-shell localization, and instantaneous heat evolution do not force decay. "
                "This is not a Duhamel estimate or a Navier–Stokes regularity proof."
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

