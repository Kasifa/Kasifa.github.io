#!/usr/bin/env python3
"""Render the R0.33 exact Hankel and Turan sign audit."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Rectangle
import numpy as np


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_BLUE = "#dce6ec"
PALE_GOLD = "#eadcc5"
GRID = "#d5cec0"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def draw() -> None:
    turan = rows("turan.csv")
    hankel = rows("hankel-signs.csv")
    witnesses = rows("witnesses.csv")
    sequence_order = ("B_U", "B_V", "H_U", "H_V")
    row_keys = [
        (sequence, kind)
        for sequence in sequence_order
        for kind in ("ordinary", "shifted")
    ]
    labels = [
        rf"${sequence.replace('_', '_{') + '}' if '_' in sequence else sequence}$ "
        + (r"$\mathcal{H}^{(0)}$" if kind == "ordinary" else r"$\mathcal{H}^{(1)}$")
        for sequence, kind in row_keys
    ]
    sign_lookup = {
        (record["sequence"], record["matrix_kind"], int(record["order"])):
        int(record["sign"])
        for record in hankel
    }
    sign_matrix = np.array(
        [
            [sign_lookup[(sequence, kind, order)] for order in range(1, 13)]
            for sequence, kind in row_keys
        ],
        dtype=int,
    )
    witness_cells = {
        (record["sequence"], record["matrix_kind"], int(record["order"]))
        for record in witnesses
    }

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 86 / 25.4),
            gridspec_kw={"width_ratios": (.88, 1.32)},
            layout="none",
        )

        left.set_title("(a) Local transport moment condition", loc="left", pad=5)
        for y, sequence, marker in ((1, "B_U", "o"), (0, "B_V", "s")):
            selected = [record for record in turan if record["sequence"] == sequence]
            positive = [record for record in selected if int(record["sign"]) >= 0]
            negative = [record for record in selected if int(record["sign"]) < 0]
            left.scatter(
                [int(record["index"]) for record in positive],
                [y] * len(positive),
                marker=marker,
                s=12,
                facecolors="white",
                edgecolors=BLUE,
                linewidths=.65,
                label="nonnegative" if sequence == "B_U" else None,
                zorder=2,
            )
            left.scatter(
                [int(record["index"]) for record in negative],
                [y] * len(negative),
                marker="x",
                s=15,
                color=GOLD,
                linewidths=.85,
                label="negative: condition fails" if sequence == "B_U" else None,
                zorder=3,
            )
        left.axvline(1, color=MUTED, linewidth=.55, linestyle=(0, (2, 2)))
        left.axvline(2, color=MUTED, linewidth=.55, linestyle=(0, (2, 2)))
        left.text(
            2.8,
            1.20,
            r"$B_U$: first exact witness at $n=1$",
            fontsize=5.7,
            color=INK,
            va="center",
        )
        left.text(
            3.8,
            -.20,
            r"$B_V$: first exact witness at $n=2$",
            fontsize=5.7,
            color=INK,
            va="center",
        )
        left.set_xlim(.1, 48.9)
        left.set_ylim(-.45, 1.45)
        left.set_xticks([1, 8, 16, 24, 32, 40, 48])
        left.set_yticks([0, 1], [r"$B_V$", r"$B_U$"])
        left.set_xlabel(r"coefficient index $n$ in $b_{n-1}b_{n+1}-b_n^2$")
        left.grid(axis="x", color=GRID, linewidth=.4)
        left.spines["left"].set_visible(False)
        left.tick_params(axis="y", length=0)
        left.legend(
            loc="center right",
            frameon=False,
            fontsize=5.7,
            handletextpad=.45,
            borderaxespad=.15,
        )
        left.text(
            48.7,
            1.38,
            "Finite exact table: 13/48 U failures; 20/48 V failures",
            fontsize=5.6,
            color=MUTED,
            ha="right",
            va="top",
        )

        right.set_title("(b) Leading Hankel determinant signs", loc="left", pad=5)
        cmap = ListedColormap([PALE_GOLD, "#eeeeeb", PALE_BLUE])
        right.imshow(
            sign_matrix,
            cmap=cmap,
            vmin=-1,
            vmax=1,
            interpolation="nearest",
            aspect="auto",
            extent=(.5, 12.5, 7.5, -.5),
        )
        for row_index, (sequence, kind) in enumerate(row_keys):
            for order in range(1, 13):
                value = sign_lookup[(sequence, kind, order)]
                right.text(
                    order,
                    row_index,
                    "+" if value > 0 else ("-" if value < 0 else "0"),
                    ha="center",
                    va="center",
                    fontsize=6.2,
                    color=BLUE if value > 0 else (GOLD if value < 0 else MUTED),
                    fontweight="bold" if value < 0 else "normal",
                )
                if (sequence, kind, order) in witness_cells:
                    right.add_patch(
                        Rectangle(
                            (order - .48, row_index - .46),
                            .96,
                            .92,
                            fill=False,
                            edgecolor=INK,
                            linewidth=1.0,
                        )
                    )
        right.set_xlim(.5, 12.5)
        right.set_ylim(7.5, -.5)
        right.set_xticks(range(1, 13))
        right.set_yticks(range(8), labels)
        right.set_xlabel("leading principal determinant order")
        right.set_xticks(np.arange(.5, 12.5, 1), minor=True)
        right.set_yticks(np.arange(-.5, 8, 1), minor=True)
        right.grid(which="minor", color="white", linewidth=.7)
        right.tick_params(which="minor", bottom=False, left=False)
        for spine in right.spines.values():
            spine.set_visible(False)
        figure.text(
            .012,
            .986,
            "R0.33 exact moment-condition audit · signs through Hankel order 12",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(.985, .986, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        figure.text(
            .985,
            .025,
            "Outlined cells are the four theorem witnesses; any '-' excludes "
            "the direct nonnegative-measure moment representation.",
            fontsize=5.6,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.subplots_adjust(left=.072, right=.985, bottom=.22, top=.82, wspace=.31)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-33-hankel-obstruction.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
