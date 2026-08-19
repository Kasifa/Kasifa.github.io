#!/usr/bin/env python3
"""Render the R0.30 kernel estimate and certified analytic domains."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
RED = "#8a302c"
PALE = "#e9e1d1"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def load_kernel() -> tuple[list[int], list[float]]:
    with (PACKAGE / "kernel.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 118:
        raise AssertionError("unexpected R0.30 kernel table")
    return [int(row["degree"]) for row in rows], [float(row["decimal"]) for row in rows]


def arrow(axis, start, end, *, color=INK) -> None:
    axis.add_patch(
        FancyArrowPatch(
            start,
            end,
            arrowstyle="-|>",
            mutation_scale=8,
            linewidth=.8,
            color=color,
            shrinkA=2,
            shrinkB=2,
        )
    )


def draw() -> None:
    degrees, kernel = load_kernel()
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 72 / 25.4),
            gridspec_kw={"width_ratios": (1.08, .92)},
            layout="none",
        )

        left.set_title("(a) Exact finite kernel diagnostic", loc="left", pad=5)
        left.plot(degrees, kernel, color=BLUE, linewidth=1.25, label=r"$H_L$")
        left.scatter([2], [8], s=15, color=RED, zorder=3)
        left.axhline(8, color=RED, linewidth=.7, linestyle="--")
        left.axhline(32, color=GOLD, linewidth=.8, linestyle=(0, (4, 3)))
        left.text(118, 31.0, "all-order proof ceiling 32", ha="right", va="top", color=GOLD, fontsize=6.2)
        left.text(5, 8.8, r"finite maximum $H_2=8$", color=RED, fontsize=6.2)
        left.set_xlim(2, 119)
        left.set_ylim(2.8, 34)
        left.set_xlabel(r"total degree $L$")
        left.set_ylabel(r"$H_L$")
        left.set_yticks([4, 8, 16, 24, 32])
        left.spines[["top", "right"]].set_visible(False)
        left.grid(axis="y", color="#d5cec0", linewidth=.45)

        right.set_title("(b) What the all-order estimate proves", loc="left", pad=5)
        right.set_xlim(0, 1)
        right.set_ylim(0, 1)
        right.axis("off")
        right.add_patch(
            Rectangle((.08, .12), .84, .70, facecolor=PALE, edgecolor=BLUE, linewidth=1.0)
        )
        right.text(
            .50,
            .73,
            r"$\max(|Z|,|W|)<1/96$",
            ha="center",
            va="center",
            color=BLUE,
            fontsize=7.4,
        )
        right.text(
            .50,
            .63,
            r"$a,\ U,\ V$ converge absolutely",
            ha="center",
            va="center",
            color=INK,
            fontsize=6.8,
        )
        right.add_patch(
            Rectangle((.25, .25), .50, .27, facecolor="white", edgecolor=RED, linewidth=1.0)
        )
        right.text(
            .50,
            .43,
            r"$\max(|Z|,|W|)<1/192$",
            ha="center",
            va="center",
            color=RED,
            fontsize=7.2,
        )
        right.text(
            .50,
            .33,
            r"$\log(U/Z),\ \log(V/W)$"
            + "\n"
            + r"$\phi$ and factorization analytic",
            ha="center",
            va="center",
            color=INK,
            fontsize=5.8,
            linespacing=1.35,
        )
        arrow(right, (.50, .60), (.50, .53), color=RED)
        right.text(
            .50,
            .06,
            "nearest singularity not located",
            ha="center",
            va="center",
            color=MUTED,
            fontsize=6.6,
        )

        figure.text(
            .01,
            .985,
            "R0.30 analytic-majorant theorem · all-order proof and finite regression separated",
            ha="left",
            va="top",
            fontsize=7.2,
            color=INK,
        )
        figure.subplots_adjust(left=.065, right=.99, bottom=.18, top=.82, wspace=.23)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-30-analytic-domain.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
