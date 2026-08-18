#!/usr/bin/env python3
"""Render the R0.29 canonical reduction and charge-ladder schematic."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


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


def load_contract() -> dict[str, str]:
    with (PACKAGE / "identities.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 4 or any(row["status"] != "all-order identity" for row in rows):
        raise AssertionError("unexpected R0.29 identity contract")
    return {row["id"]: row["statement"] for row in rows}


def box(axis, xy, width, height, text, *, edge=INK, face="white", fontsize=7.0):
    patch = FancyBboxPatch(
        xy,
        width,
        height,
        boxstyle="round,pad=0.018,rounding_size=0.018",
        linewidth=.75,
        edgecolor=edge,
        facecolor=face,
    )
    axis.add_patch(patch)
    axis.text(
        xy[0] + width / 2,
        xy[1] + height / 2,
        text,
        ha="center",
        va="center",
        fontsize=fontsize,
        color=INK,
        linespacing=1.25,
    )


def arrow(axis, start, end, *, color=INK, dashed=False, mutation=9):
    patch = FancyArrowPatch(
        start,
        end,
        arrowstyle="-|>",
        mutation_scale=mutation,
        linewidth=.85,
        linestyle="--" if dashed else "-",
        color=color,
        shrinkA=2,
        shrinkB=2,
    )
    axis.add_patch(patch)


def draw() -> None:
    load_contract()
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 72 / 25.4),
            gridspec_kw={"width_ratios": (0.78, 1.22)},
            layout="none",
        )
        for axis in (left, right):
            axis.set_xlim(0, 1)
            axis.set_ylim(0, 1)
            axis.axis("off")

        left.set_title("(a) No finite charge cutoff closes", loc="left", pad=5)
        left.add_patch(
            Rectangle((.08, .10), .72, .42, facecolor=PALE, edgecolor="none", alpha=.78)
        )
        left.text(
            .58,
            .18,
            r"finite cone  $q\leq Q$",
            va="center",
            fontsize=5.8,
            color=MUTED,
        )
        levels = [(.20, r"$q=Q-1$"), (.40, r"$q=Q$"), (.60, r"$q=Q+1$")]
        for y, label in levels:
            outside = y > .5
            box(
                left,
                (.25, y - .055),
                .30,
                .11,
                label,
                edge=RED if outside else BLUE,
                face="white",
                fontsize=7.2,
            )
        left.text(.60, .60, "outside", va="center", fontsize=6.6, color=RED)
        arrow(left, (.40, .545), (.40, .455), color=RED)
        left.text(.58, .50, r"$k\,f_{k,Q+1}$", va="center", fontsize=7.2, color=RED)
        arrow(left, (.40, .345), (.40, .255), color=BLUE)
        left.text(.43, .30, "next equation", va="center", fontsize=6.5, color=MUTED)
        left.text(
            .08,
            .02,
            r"$a_{0,-1}=1$ forces the upward-charge dependency",
            fontsize=6.8,
            color=INK,
        )

        right.set_title("(b) Exact log-canonical reduction", loc="left", pad=5)
        box(
            right,
            (.02, .68),
            .21,
            .17,
            "transport arrays\n" + r"$u,\ v$",
            edge=BLUE,
        )
        box(
            right,
            (.31, .68),
            .25,
            .17,
            r"$U=-12u$" + "\n" + r"$V=-3v$",
            edge=BLUE,
        )
        box(
            right,
            (.64, .64),
            .34,
            .25,
            r"$\{U,V\}=UV$" + "\n" + r"$\dfrac{U}{V}=\dfrac{Z}{W}e^{-a}$",
            edge=GOLD,
            face="#fbf8f0",
            fontsize=7.3,
        )
        arrow(right, (.23, .765), (.31, .765), color=BLUE)
        arrow(right, (.56, .765), (.64, .765), color=GOLD)

        box(
            right,
            (.15, .20),
            .31,
            .22,
            r"$\phi=\frac{1}{2}\log(UV/ZW)$"
            + "\n"
            + r"$U=Ze^{\phi-a/2}$"
            + "\n"
            + r"$V=We^{\phi+a/2}$",
            edge=GOLD,
            face="#fbf8f0",
            fontsize=5.8,
        )
        box(
            right,
            (.57, .18),
            .41,
            .26,
            r"$d=-e^\phi\left[\frac{pZ}{12}e^{-a/2}+\frac{qW}{3}e^{a/2}\right]$",
            edge=RED,
            face="#fbf8f0",
            fontsize=6.2,
        )
        arrow(right, (.78, .64), (.45, .42), color=GOLD, dashed=True)
        arrow(right, (.46, .31), (.57, .31), color=RED)
        right.text(
            .02,
            .02,
            "all-order formal identities · finite audit is a regression only",
            fontsize=6.7,
            color=MUTED,
        )

        figure.text(
            .01,
            .985,
            "R0.29 canonical transport theorem · exact rational formal series",
            ha="left",
            va="top",
            fontsize=7.2,
            color=INK,
        )
        figure.subplots_adjust(left=.025, right=.99, bottom=.10, top=.82, wspace=.12)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-29-canonical-reduction.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
