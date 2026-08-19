#!/usr/bin/env python3
"""Render the R0.32 exact finite D-log Padé candidate diagnostic."""

from __future__ import annotations

import csv
from fractions import Fraction
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


PACKAGE = Path(__file__).resolve().parent
REPOSITORY = PACKAGE.parents[2]
STYLE = PACKAGE.parents[1] / "journal.mplstyle"
INK = "#27221d"
MUTED = "#6b675f"
BLUE = "#315a76"
GOLD = "#a16f27"
PALE_BLUE = "#dce6ec"
GRID = "#d5cec0"


def normalize_svg(path: Path) -> None:
    lines = path.read_text(encoding="utf-8").splitlines()
    path.write_text(
        "\n".join(line.rstrip() for line in lines) + "\n",
        encoding="utf-8",
    )


def read_rows(name: str) -> list[dict[str, str]]:
    with (PACKAGE / name).open(newline="", encoding="utf-8") as source:
        return list(csv.DictReader(source))


def series(data: list[dict[str, str]], field: str, quantity: str) -> tuple[list[int], list[float]]:
    selected = [row for row in data if row["field"] == field]
    return (
        [int(row["coefficient_cut"]) for row in selected],
        [float(row[quantity]) for row in selected],
    )


def draw() -> None:
    data = read_rows("candidate-poles.csv")
    summary = {row["quantity"]: row for row in read_rows("summary.csv")}
    u_cut, u_root = series(data, "U", "root_mid")
    v_cut, v_root = series(data, "V", "root_mid")
    _, u_residue = series(data, "U", "residue_mid")
    _, v_residue = series(data, "V", "residue_mid")
    d_cut, d_residue = series(data, "D center", "residue_mid")
    _, d_root = series(data, "D center", "root_mid")
    tail = summary["transport cluster, cuts 42-50"]
    tail_lower = float(Fraction(tail["lower"]))
    tail_upper = float(Fraction(tail["upper"]))

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        figure, (left, right) = plt.subplots(
            1,
            2,
            figsize=(178 / 25.4, 74 / 25.4),
            gridspec_kw={"width_ratios": (1.05, .95)},
            layout="none",
        )

        left.set_title("(a) Transport candidate cluster (zoomed)", loc="left", pad=5)
        left.axhspan(tail_lower, tail_upper, color=PALE_BLUE, alpha=.72, zorder=0)
        left.axhline(-.75, color=MUTED, linewidth=.7, linestyle=(0, (2, 2)))
        left.plot(
            u_cut,
            u_root,
            color=BLUE,
            marker="o",
            markerfacecolor=BLUE,
            markeredgecolor=BLUE,
            linewidth=1.0,
            label=r"$U_1$: exact $[m/m]$ pole",
        )
        left.plot(
            v_cut,
            v_root,
            color=GOLD,
            marker="s",
            markerfacecolor="white",
            markeredgecolor=GOLD,
            linestyle=(0, (4, 2)),
            linewidth=1.0,
            label=r"$V_1$: exact $[m/m]$ pole",
        )
        left.text(
            30.2,
            -.749975,
            r"reference $-3/4$ (not a proved limit)",
            color=MUTED,
            fontsize=5.7,
            va="bottom",
        )
        left.text(
            49.7,
            -.749385,
            "cuts 42-50 hull < 1e-4",
            color=BLUE,
            fontsize=5.7,
            ha="right",
            va="center",
        )
        left.set_xlim(29.3, 50.7)
        left.set_ylim(-.75002, -.74934)
        left.set_xticks([30, 34, 38, 42, 46, 50])
        left.yaxis.set_major_formatter(FormatStrFormatter("%.4f"))
        left.set_xlabel(r"coefficient cut $c$; order $m=(c-2)/2$")
        left.set_ylabel(r"isolated approximant pole in $R$")
        left.grid(axis="y", color=GRID, linewidth=.45)
        left.legend(loc="upper left", frameon=False, fontsize=5.8, handlelength=2.4)

        right.set_title("(b) D-log residue classifies the object", loc="left", pad=5)
        right.axhline(0, color=INK, linewidth=.65)
        right.axhline(-.5, color=MUTED, linewidth=.65, linestyle=(0, (2, 2)))
        right.axhline(1, color=MUTED, linewidth=.65, linestyle=(0, (1, 2)))
        right.plot(
            u_cut,
            u_residue,
            color=BLUE,
            marker="o",
            markerfacecolor=BLUE,
            linewidth=1.0,
            label=r"$U_1$ branch candidate",
        )
        right.plot(
            v_cut,
            v_residue,
            color=GOLD,
            marker="s",
            markerfacecolor="white",
            markeredgecolor=GOLD,
            linestyle=(0, (4, 2)),
            linewidth=1.0,
            label=r"$V_1$ branch candidate",
        )
        right.plot(
            d_cut,
            d_residue,
            color=MUTED,
            marker="^",
            markerfacecolor="white",
            markeredgecolor=INK,
            linestyle=(0, (1, 2)),
            linewidth=.9,
            label=r"$D_1$ zero candidate",
        )
        right.text(31, -.47, r"branch test: residue $<-1/2$", color=MUTED, fontsize=5.7)
        right.text(
            49.8,
            1.035,
            "$D_1$: residue $\\to+1$\n"
            + rf"$R\approx {d_root[-1]:.6f}$",
            color=INK,
            fontsize=5.8,
            ha="right",
            va="bottom",
        )
        right.set_xlim(29.3, 50.7)
        right.set_ylim(-.65, 1.14)
        right.set_xticks([30, 34, 38, 42, 46, 50])
        right.set_yticks([-.5, 0, .5, 1])
        right.set_xlabel(r"coefficient cut $c$")
        right.set_ylabel(r"exactly enclosed Padé residue")
        right.grid(axis="y", color=GRID, linewidth=.45)
        right.legend(loc="center right", frameon=False, fontsize=5.7, handlelength=2.4)

        figure.text(
            .012,
            .985,
            "R0.32 finite exact D-log Padé audit · approximant poles, not certified singularities",
            ha="left",
            va="top",
            fontsize=7.1,
            color=INK,
        )
        figure.text(.985, .985, r"$\nu$", ha="right", va="top", fontsize=8.0, color=MUTED)
        figure.subplots_adjust(left=.075, right=.985, bottom=.22, top=.82, wspace=.28)

        for suffix in ("pdf", "svg", "png"):
            output = PACKAGE / f"figure.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        public_figures = REPOSITORY / "public/figures"
        public_figures.mkdir(parents=True, exist_ok=True)
        for suffix in ("svg", "png"):
            output = public_figures / f"r0-32-candidate-cluster.{suffix}"
            figure.savefig(output)
            if suffix == "svg":
                normalize_svg(output)
        plt.close(figure)


if __name__ == "__main__":
    draw()
