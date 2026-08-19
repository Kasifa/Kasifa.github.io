#!/usr/bin/env python3
"""Render the R0.34 bounded-degree polynomial-background obstruction."""

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
PALE_GRAY = "#efefec"
GRID = "#d5cec0"
SEQUENCE_ORDER = ("B_U", "B_V", "H_U", "H_V")


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def math_label(sequence: str) -> str:
    base, subscript = sequence.split("_")
    return rf"${base}_{{{subscript}}}$"


def draw() -> None:
    thresholds = rows("thresholds.csv")
    tail = rows("tail-search.csv")
    threshold_by_sequence = {record["sequence"]: record for record in thresholds}
    tail_lookup = {
        (record["sequence"], int(record["shift"])): record for record in tail
    }

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 86 / 25.4),
            gridspec_kw={"width_ratios": (0.88, 1.22)},
            layout="none",
        )

        left.set_title("(a) Polynomial degree excluded", loc="left", pad=5)
        y_positions = np.arange(len(SEQUENCE_ORDER))[::-1]
        degrees = [
            int(threshold_by_sequence[sequence]["maximum_excluded_degree"])
            for sequence in SEQUENCE_ORDER
        ]
        colors = [BLUE, BLUE, GOLD, GOLD]
        hatches = ["", "//", "", "//"]
        for y, sequence, degree, color, hatch in zip(
            y_positions, SEQUENCE_ORDER, degrees, colors, hatches
        ):
            left.barh(
                y,
                degree,
                height=0.56,
                color=color,
                alpha=0.86 if not hatch else 0.48,
                edgecolor=INK,
                linewidth=0.55,
                hatch=hatch,
            )
            witness = threshold_by_sequence[sequence]
            left.text(
                degree - 0.8,
                y,
                rf"$d\leq {degree}$" + "\n" +
                rf"$s={witness['witness_shift']},\ r={witness['witness_order']}$",
                va="center",
                ha="right",
                fontsize=5.45,
                color=INK if hatch else "white",
                linespacing=0.92,
            )
        left.set_yticks(y_positions, [math_label(value) for value in SEQUENCE_ORDER])
        left.set_xlim(0, 50)
        left.set_xticks([0, 10, 20, 30, 40, 50])
        left.set_xlabel("maximum universally excluded degree")
        left.grid(axis="x", color=GRID, linewidth=0.4)
        left.spines["left"].set_visible(False)
        left.tick_params(axis="y", length=0)

        right.set_title("(b) Exact tail principal-minor scan", loc="left", pad=5)
        state = np.zeros((4, 10), dtype=int)
        # State -1: a negative principal minor exists; 0: none among tested;
        # state 1: unavailable because the exact coefficient window ends.
        for row_index, sequence in enumerate(SEQUENCE_ORDER):
            for column, shift in enumerate(range(40, 50)):
                record = tail_lookup[(sequence, shift)]
                if not int(record["available"]):
                    state[row_index, column] = 1
                elif int(record["negative_count"]) > 0:
                    state[row_index, column] = -1
        cmap = ListedColormap([PALE_GOLD, PALE_BLUE, PALE_GRAY])
        right.imshow(
            state,
            cmap=cmap,
            vmin=-1,
            vmax=1,
            interpolation="nearest",
            aspect="auto",
            extent=(39.5, 49.5, 3.5, -0.5),
        )
        for row_index, sequence in enumerate(SEQUENCE_ORDER):
            for shift in range(40, 50):
                record = tail_lookup[(sequence, shift)]
                available = bool(int(record["available"]))
                negative_count = int(record["negative_count"])
                if not available:
                    label, color = "n/a", MUTED
                elif negative_count:
                    label, color = rf"$\times${negative_count}", GOLD
                else:
                    label, color = "0", BLUE
                right.text(
                    shift,
                    row_index,
                    label,
                    ha="center",
                    va="center",
                    fontsize=5.8,
                    color=color,
                    fontweight="bold" if negative_count else "normal",
                )
                if int(record["is_maximal_witness_shift"]):
                    right.add_patch(
                        Rectangle(
                            (shift - 0.48, row_index - 0.46),
                            0.96,
                            0.92,
                            fill=False,
                            edgecolor=INK,
                            linewidth=1.05,
                        )
                    )
        right.set_xlim(39.5, 49.5)
        right.set_ylim(3.5, -0.5)
        right.set_xticks(range(40, 50))
        right.set_yticks(range(4), [math_label(value) for value in SEQUENCE_ORDER])
        right.set_xlabel("tail start $s$")
        right.set_xticks(np.arange(39.5, 50, 1), minor=True)
        right.set_yticks(np.arange(-0.5, 4, 1), minor=True)
        right.grid(which="minor", color="white", linewidth=0.75)
        right.tick_params(which="minor", bottom=False, left=False)
        for spine in right.spines.values():
            spine.set_visible(False)
        figure.text(
            0.012,
            0.986,
            "R0.34 bounded-degree polynomial-background obstruction",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(0.985, 0.986, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        figure.text(
            0.985,
            0.066,
            r"Cells: $\times k$ = $k$ negative minors; 0 = none tested negative; n/a = unavailable; box = theorem witness.",
            fontsize=5.45,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.text(
            0.985,
            0.023,
            "Negative tail Gram determinants exclude every polynomial coefficient choice "
            "through the stated degree; later blue cells are finite-window diagnostics only.",
            fontsize=5.55,
            color=MUTED,
            ha="right",
            va="bottom",
        )
        figure.subplots_adjust(left=0.065, right=0.985, bottom=0.235, top=0.82, wspace=0.24)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-34-tail-background-obstruction.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
