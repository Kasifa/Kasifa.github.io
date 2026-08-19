#!/usr/bin/env python3
"""Render the R0.31 kernel certificate and analytic-domain improvement."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
RED = "#8a302c"
PALE = "#d8d0c2"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def read_curve(name: str) -> tuple[list[int], list[float]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    return [int(row["degree"]) for row in rows], [float(row["decimal"]) for row in rows]


def draw() -> None:
    degrees, kernel = read_curve("kernel.csv")
    tail_degrees, tail = read_curve("tail-bound.csv")
    with (PACKAGE / "domains.csv").open(newline="", encoding="utf-8") as stream:
        domain_rows = list(csv.DictReader(stream))

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 72 / 25.4),
            gridspec_kw={"width_ratios": (1.15, .85)},
            layout="none",
        )

        left.set_title("(a) Exact finite range and analytic tail", loc="left", pad=5)
        left.plot(degrees, kernel, color=BLUE, linewidth=1.2)
        left.plot(
            tail_degrees,
            tail,
            color=RED,
            linewidth=1.0,
            linestyle=(0, (4, 2)),
        )
        left.axhline(27 / 4, color=GOLD, linewidth=.8, linestyle="--")
        left.scatter([2], [8], s=17, color=RED, zorder=4)
        left.scatter([3], [27 / 4], s=17, color=GOLD, zorder=4)
        left.axvline(297, color=MUTED, linewidth=.65, linestyle=":")
        left.text(45, 3.82, r"exact $H_L$", color=BLUE, fontsize=6.0)
        left.text(450, 5.72, "analytic tail bound", color=RED, fontsize=6.0, rotation=-18)
        left.text(4.4, 8.05, r"$H_2=8$", color=RED, fontsize=6.2, va="center")
        left.text(9, 6.86, r"$H_3=27/4$", color=GOLD, fontsize=6.2)
        left.text(225, 6.70, r"new ceiling $27/4$", color=GOLD, fontsize=6.0, ha="right", va="top")
        left.text(790, 3.18, "R0.30 ceiling 32 is off scale", color=MUTED, fontsize=5.8, ha="right")
        left.set_xscale("log")
        left.set_xlim(2, 820)
        left.set_ylim(3.0, 8.35)
        left.set_xlabel(r"total degree $L$ (log scale)")
        left.set_ylabel(r"kernel bound")
        left.set_xticks([2, 3, 10, 30, 100, 297, 800])
        left.set_xticklabels(["2", "3", "10", "30", "100", "297", "800"])
        left.spines[["top", "right"]].set_visible(False)
        left.grid(axis="y", color="#d5cec0", linewidth=.45)

        labels = [r"$a,U,V$", "logs, $\\phi$,\nfactorization"]
        old = [float(Fraction(row["r030_exact"])) for row in domain_rows]
        new = [float(Fraction(row["r031_exact"])) for row in domain_rows]
        gains = [float(Fraction(row["improvement_exact"])) for row in domain_rows]
        positions = [1, 0]
        height = .27
        right.set_title("(b) Guaranteed polydisc radius", loc="left", pad=5)
        right.barh(
            [position - height / 2 for position in positions],
            old,
            height=height,
            color=PALE,
            edgecolor=MUTED,
            linewidth=.5,
            label="R0.30",
        )
        right.barh(
            [position + height / 2 for position in positions],
            new,
            height=height,
            color=BLUE,
            edgecolor=BLUE,
            linewidth=.5,
            label="R0.31",
        )
        for position, value, gain in zip(positions, new, gains):
            right.text(
                value + .0012,
                position + height / 2,
                f"{gain:.2f}×",
                va="center",
                color=RED,
                fontsize=6.2,
            )
        right.axvline(4 / 81, color=BLUE, linewidth=.6, linestyle=":")
        right.set_yticks(positions, labels)
        right.set_xlim(0, .057)
        right.set_xlabel(r"certified radius $r$")
        right.set_xticks([0, 1 / 192, 1 / 96, .02, .03, .04, 4 / 81])
        right.set_xticklabels(["0", "1/192", "1/96", ".02", ".03", ".04", "4/81"], rotation=32, ha="right")
        right.spines[["top", "right", "left"]].set_visible(False)
        right.tick_params(axis="y", length=0, labelsize=6.1, pad=3)
        right.grid(axis="x", color="#d5cec0", linewidth=.45)
        right.legend(loc="lower right", frameon=False, fontsize=6.0)

        figure.text(
            .01,
            .985,
            "R0.31 optimized analytic majorant · finite exact range and all-order tail separated",
            ha="left",
            va="top",
            fontsize=7.2,
            color=INK,
        )
        figure.subplots_adjust(left=.065, right=.985, bottom=.24, top=.82, wspace=.28)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-31-improved-domain.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
