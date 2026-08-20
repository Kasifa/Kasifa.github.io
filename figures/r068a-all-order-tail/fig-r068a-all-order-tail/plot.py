#!/usr/bin/env python3
"""Render the R0.68A all-order tail reduction figure."""

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
        "\n".join(line.rstrip() for line in path.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )


def rss_mib() -> float:
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value / (1024 * 1024) if platform.system() == "Darwin" else value / 1024


def blossom(figure) -> None:
    center = (0.946, 0.942)
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
    tail = rows("tail-bounds.csv")
    rates = rows("contraction-rates.csv")
    orders = rows("order-status.csv")
    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = "r068a-all-order-tail"
        figure = plt.figure(figsize=(178 / 25.4, 100 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2, 2, left=.10, right=.955, bottom=.17, top=.79,
            width_ratios=(1.25, 1), height_ratios=(.58, .42),
            hspace=.68, wspace=.35,
        )
        tail_axis = figure.add_subplot(grid[:, 0])
        rate_axis = figure.add_subplot(grid[0, 1])
        order_axis = figure.add_subplot(grid[1, 1])
        figure.suptitle(
            "All target orders at least ten form a certified contracting tail",
            x=.068, y=.954, ha="left", fontsize=8.0, color=INK,
        )
        figure.text(
            .068, .895,
            r"quartic-critical amplitude  ·  invariant shear Dyson series  ·  $M_r=16^r$  ·  one finite eighth-order gate remains",
            ha="left", fontsize=3.8, color=MUTED,
        )
        blossom(figure)

        x = [int(row["block"]) for row in tail]
        y = [float(row["certifiedSimpleBound"]) for row in tail]
        y_root = [float(row["rootEnclosureDisplayBound"]) for row in tail]
        tail_axis.set_title("(a) Complete tail relative to the quadratic target", loc="left", pad=5)
        tail_axis.semilogy(x, y, color=BLUE, marker="o", markersize=2.6, linewidth=1.25,
                           label=r"certified  $(1/30000)(43/64)^r$")
        tail_axis.semilogy(x, y_root, color=INK, linestyle="--", linewidth=.75,
                           label=r"root-enclosure display")
        tail_axis.fill_between(x, y, 1e-8, color=PALE_BLUE, alpha=.75, zorder=-2)
        tail_axis.set_xlim(0, 16)
        tail_axis.set_ylim(1e-8, 5e-5)
        tail_axis.set_xlabel("four-bit block r")
        tail_axis.set_ylabel("upper ratio")
        tail_axis.grid(color=GRID, linewidth=.3, which="both")
        tail_axis.legend(loc="upper right", frameon=False, fontsize=3.1)
        tail_axis.text(
            .04, .07, "The infinite tail is closed jointly, not term by term.",
            transform=tail_axis.transAxes, fontsize=3.45, color=BLUE,
        )

        rate_axis.set_title("(b) One-block contraction factors", loc="left", pad=5)
        selected = [row for row in rates if row["quantity"] != "eighth branch probe"]
        short_labels = {
            "simple theorem rate": "theorem 43/64",
            "lambda>25 rate": r"$\lambda>25$ bound",
            "root-enclosure display": r"$\lambda$ enclosure",
            "sixth fixed-order rate": "sixth order",
        }
        labels = [short_labels[row["quantity"]] for row in selected]
        values = [float(row["rate"]) for row in selected]
        for index, (label, value) in enumerate(zip(labels, values)):
            y_pos = len(values) - 1 - index
            color = BLUE if "tail" in label or "theorem" in label or "lambda" in label or "root" in label else RUST
            marker = "o" if color == BLUE else "D"
            rate_axis.hlines(y_pos, 0, value, color=color, linewidth=1.1)
            rate_axis.scatter([value], [y_pos], color=color, marker=marker, s=17)
            rate_axis.text(value + .012, y_pos, f"{value:.4f}", va="center", fontsize=3.1, color=color)
        rate_axis.axvline(1, color=INK, linewidth=.55)
        rate_axis.set_xlim(0, 1.04)
        rate_axis.set_yticks(range(len(values)), list(reversed(labels)))
        rate_axis.set_xlabel("factor per block  (<1 contracts)")
        rate_axis.grid(axis="x", color=GRID, linewidth=.3)

        order_axis.set_title("(c) Reduction of the all-order question", loc="left", pad=5)
        status_style = {
            "exact": (INK, "s", "white"),
            "certified": (BLUE, "o", BLUE),
            "open": (GOLD, "D", "white"),
        }
        order_axis.axhline(0, color=GRID, linewidth=.8)
        for row in orders:
            order = int(row["order"])
            color, marker, face = status_style[row["status"]]
            order_axis.scatter([order], [0], s=30, marker=marker, edgecolor=color,
                               facecolor=face, linewidth=.9, zorder=3)
            label = "8\nopen" if order == 8 else ("≥10\ntail" if order == 10 else str(order))
            order_axis.text(order, -.24, label, ha="center", va="top", fontsize=3.0,
                            color=color if order == 8 else INK)
        order_axis.axvspan(7.45, 8.55, color=PALE_GOLD, zorder=-2)
        order_axis.set_xlim(1.3, 10.7)
        order_axis.set_ylim(-.72, .45)
        order_axis.set_xticks([])
        order_axis.set_yticks([])
        order_axis.spines[["left", "right", "top", "bottom"]].set_visible(False)
        order_axis.text(.02, .76, "closed", transform=order_axis.transAxes, color=BLUE, fontsize=3.2)
        order_axis.text(.55, .76, "only finite gate", transform=order_axis.transAxes, color=GOLD, fontsize=3.2)

        figure.text(
            .068, .055,
            "Claim boundary: complete n≥10 tail only; the eighth-order heat term and general 3D regularity remain open.",
            fontsize=3.35, color=MUTED,
        )
        metadata = {"Creator": "R0.68A all-order tail reduction", "Date": None}
        figure.savefig(HERE / "figure.pdf", metadata=metadata)
        figure.savefig(HERE / "figure.svg", metadata=metadata)
        figure.savefig(HERE / "figure.png", dpi=600, metadata=metadata)
        plt.close(figure)
    normalize_svg(HERE / "figure.svg")
    with (HERE / "plot-resources.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["elapsedSeconds", "maximumRssMiB", "status"], lineterminator="\n")
        writer.writeheader()
        writer.writerow({
            "elapsedSeconds": f"{time.perf_counter() - started:.6f}",
            "maximumRssMiB": f"{rss_mib():.3f}",
            "status": "passed",
        })


if __name__ == "__main__":
    draw()
