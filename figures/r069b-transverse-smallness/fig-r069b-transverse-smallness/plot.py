#!/usr/bin/env python3
"""Render the R0.69B critical transverse-smallness figure."""

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
    center = (0.946, 0.925)
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
    scales = rows("scale-separation.csv")
    decisions = rows("decision-depth.csv")
    crossings = rows("certified-crossings.csv")
    depths = [int(row["r"]) for row in scales]
    amplitude = [float(row["physicalAmplitudeLower"]) for row in scales]
    critical = [float(row["criticalNormUpper"]) for row in scales]
    budgets = [float(row["budget"]) for row in decisions]
    required = [int(row["firstDepthStrictlyBelow"]) for row in decisions]

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r069b-transverse-smallness"
        figure = plt.figure(figsize=(178 / 25.4, 92 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1, 2, left=.082, right=.958, bottom=.20, top=.76,
            width_ratios=(1.18, .92), wspace=.30,
        )
        scale_axis = figure.add_subplot(grid[0, 0])
        decision_axis = figure.add_subplot(grid[0, 1])
        figure.suptitle(
            "Critical smallness excludes infinitesimal transverse singularity routes",
            x=.055, y=.947, ha="left", fontsize=8.0, color=INK,
        )
        figure.text(
            .055, .884,
            r"periodic invariant-shear packet  ·  $M_r=16^r$  ·  source-locked R0.69B certificate",
            ha="left", fontsize=3.8, color=MUTED,
        )
        blossom(figure)

        scale_axis.set_title("(a) Opposite scale behavior", loc="left", pad=5)
        scale_axis.semilogy(
            depths, amplitude, color=RUST, linewidth=1.15, linestyle="-",
            marker="D", markevery=5, markersize=2.6,
            label=r"Fourier amplitude $A_r$  (certified lower bound)",
        )
        scale_axis.semilogy(
            depths, critical, color=BLUE, linewidth=1.2, linestyle="--",
            marker="o", markerfacecolor="white", markevery=5, markersize=2.7,
            label=r"$BMO^{-1}_{\rm per}$ bound $(6+4\sqrt{2})\rho^r$",
        )
        scale_axis.fill_between(depths, critical, 1e-5, color=PALE_BLUE, alpha=.45)
        scale_axis.axhline(1, color=INK, linewidth=.5, linestyle=":")
        scale_axis.set_xlim(0, 50)
        scale_axis.set_ylim(1e-5, 1e26)
        scale_axis.set_xlabel("packet depth r")
        scale_axis.set_ylabel("certified envelope  (log scale)")
        scale_axis.grid(color=GRID, linewidth=.3, which="both")
        scale_axis.legend(loc="upper left", frameon=False, fontsize=3.15)
        scale_axis.text(
            .045, .08,
            r"$A_r$ grows while the scale-critical bound decays" + "\n" +
            r"at rate $\rho<0.797586$.",
            transform=scale_axis.transAxes, fontsize=3.25, color=INK,
            bbox={"facecolor": PALE_GOLD, "edgecolor": "none", "pad": 2.0},
        )

        decision_axis.set_title("(b) Depth needed for a target budget", loc="left", pad=5)
        decision_axis.semilogx(
            list(reversed(budgets)), list(reversed(required)),
            color=BLUE, linewidth=1.2, drawstyle="steps-post",
        )
        marker_map = {"1": "o", "1e-1": "s", "1e-2": "D", "1e-3": "^", "1e-6": "v"}
        for row in crossings:
            budget = float(row["budget"])
            depth = int(row["firstDepthStrictlyBelow"])
            decision_axis.scatter(
                [budget], [depth], color=RUST, marker=marker_map[row["budget"]],
                s=18, zorder=3,
            )
            decision_axis.text(
                budget * (1.18 if budget < 1 else .82), depth + 1.7,
                f"r={depth}", ha="left" if budget < 1 else "right",
                fontsize=3.0, color=RUST,
            )
        decision_axis.set_xlim(7e-7, 1.45)
        decision_axis.set_ylim(0, 78)
        decision_axis.set_xlabel(r"target base budget $\tau$")
        decision_axis.set_ylabel(r"first r with $(6+4\sqrt{2})\rho^r<\tau$")
        decision_axis.grid(color=GRID, linewidth=.3, which="both")
        decision_axis.text(
            .06, .78,
            r"Transverse gate:" + "\n" +
            r"$(6+4\sqrt{2})\rho^r+\|w_{0,r}\|_{BMO^{-1}_{\rm per}}$" + "\n" +
            r"$<\eta^{\rm per}_{\rm KT}$",
            transform=decision_axis.transAxes, fontsize=3.45, color=INK,
            bbox={"facecolor": PALE_GOLD, "edgecolor": GOLD, "linewidth": .35, "pad": 2.2},
        )
        decision_axis.text(
            .06, .62,
            r"$eta^{\rm per}_{\rm KT}$ is existential; no numerical value is used.",
            transform=decision_axis.transAxes, fontsize=3.05, color=MUTED,
        )

        figure.text(
            .055, .065,
            "Claim boundary: the fixed critical ball follows from a standard small-data theorem; order-one transverse data, instability, and singularity remain open.",
            fontsize=3.25, color=MUTED,
        )
        metadata = {"Creator": "R0.69B transverse critical smallness", "Date": None}
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
