#!/usr/bin/env python3
"""Render the four-panel R0.71Q journal figure."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import inset_axes


PAPER = "#FBF9F4"
INK = "#252422"
BLUE = "#355C7D"
OCHRE = "#B8792B"
GRAY = "#77736C"


def load(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(encoding="utf-8")))


def series(rows: list[dict[str, str]], panel: str, name: str) -> tuple[list[float], list[float]]:
    selected = [row for row in rows if row["panel"] == panel and row["series"] == name]
    return [float(row["x"]) for row in selected], [float(row["y"]) for row in selected]


def style() -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.4,
        "axes.titlesize": 8.4,
        "axes.labelsize": 7.4,
        "xtick.labelsize": 6.6,
        "ytick.labelsize": 6.6,
        "legend.fontsize": 6.2,
        "axes.edgecolor": INK,
        "axes.labelcolor": INK,
        "text.color": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "axes.facecolor": PAPER,
        "figure.facecolor": PAPER,
        "savefig.facecolor": PAPER,
        "axes.linewidth": 0.75,
        "lines.linewidth": 1.35,
        "pdf.fonttype": 42,
        "svg.fonttype": "none",
    })


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-stem", type=Path, required=True)
    args = parser.parse_args()
    rows = load(args.data)
    style()

    fig, axes = plt.subplots(2, 2, figsize=(178 / 25.4, 118 / 25.4), constrained_layout=True)
    axa, axb, axc, axd = axes.ravel()

    x, y = series(rows, "A", "Temam lobe")
    axa.plot(x, y, color=BLUE, label=r"Temam lobe $\Delta_R$")
    x, y = series(rows, "A", "certified disk")
    axa.fill(x, y, facecolor=OCHRE, alpha=0.30, edgecolor=OCHRE, linewidth=1.0, label=r"certified $D(T_1/4,T_1/64)$")
    axa.axhline(0, color=GRAY, lw=0.6)
    axa.set_aspect("equal", adjustable="box")
    axa.set_xlim(-0.03, 1.03)
    axa.set_ylim(-0.36, 0.36)
    axa.set_xlabel(r"$\operatorname{Re}(z-\tau)/T_1$")
    axa.set_ylabel(r"$\operatorname{Im}(z-\tau)/T_1$")
    axa.set_title("Complex-time radius is a strong-norm scale", loc="left", fontweight="bold")
    axa.legend(loc="upper right", frameon=False)
    ins = inset_axes(axa, width="40%", height="38%", loc="lower right", borderpad=1.0)
    ix, iy = series(rows, "A", "inverse window scale")
    ins.loglog(ix, iy, color=OCHRE)
    ins.set_xlabel(r"$Y$", labelpad=0)
    ins.set_ylabel(r"$T_1^{-1}$", labelpad=0)
    ins.tick_params(pad=1)
    ins.grid(True, which="both", color="#D8D3C8", lw=0.35)

    for name, color, marker, ls in (
        ("distinct zeros", BLUE, "o", "-"),
        ("Jensen bound", OCHRE, "", "--"),
        ("positive entries of B_N squared", INK, "s", "none"),
    ):
        x, y = series(rows, "B", name)
        axb.plot(x, y, color=color, marker=marker, markevery=8, ms=3.0, linestyle=ls, label=name)
    axb.set_xlim(0, 66)
    axb.set_ylim(0, 68)
    axb.set_xlabel(r"Blaschke degree $N$")
    axb.set_ylabel("count")
    axb.set_title("Anchor logarithm is necessary and sharp", loc="left", fontweight="bold")
    axb.grid(True, color="#D8D3C8", lw=0.45)
    axb.legend(loc="upper left", frameon=False)
    axb.text(0.97, 0.06, r"$\|B_N\|_{H^\infty}=1$" + "\n" + r"$|B_N(0)|\asymp2^{-N}$", transform=axb.transAxes, ha="right", va="bottom", fontsize=6.5)

    for name, color, ls, marker in (
        ("distinct union", BLUE, "-", "o"),
        ("one-component capacity", GRAY, ":", ""),
        ("summed capacity", OCHRE, "--", ""),
    ):
        x, y = series(rows, "C", name)
        axc.loglog(x, y, color=color, linestyle=ls, marker=marker, markevery=8, ms=3.0, label=name)
    axc.set_xlabel(r"number of observables $|\Lambda|$")
    axc.set_ylabel("zero-set count / capacity")
    axc.set_title("A union of zero sets pays truncation tax", loc="left", fontweight="bold")
    axc.grid(True, which="both", color="#D8D3C8", lw=0.45)
    axc.legend(loc="upper left", frameon=False)
    axc.text(0.97, 0.07, "uniform radius, M,\nand center anchor", transform=axc.transAxes, ha="right", va="bottom", fontsize=6.5)

    for name, color, ls, marker in (
        ("owned entries", BLUE, "-", "o"),
        ("owned windows", OCHRE, "--", "s"),
        ("relative complex growth", GRAY, ":", ""),
    ):
        x, y = series(rows, "D", name)
        axd.loglog(x, y, color=color, linestyle=ls, marker=marker, markevery=8, ms=3.0, label=name)
    axd.set_xlabel(r"oscillation parameter $N$")
    axd.set_ylabel("count / relative growth")
    axd.set_title("Local analytic data do not pay the cover", loc="left", fontweight="bold")
    axd.grid(True, which="both", color="#D8D3C8", lw=0.45)
    axd.legend(loc="upper left", frameon=False)
    axd.text(0.97, 0.07, r"$M_m/a_m\leq\cosh^2(3\pi/4)$" + "\n" + r"$R_m,r_m\propto N^{-1}$", transform=axd.transAxes, ha="right", va="bottom", fontsize=6.5)

    for label, axis in zip("ABCD", axes.ravel()):
        axis.text(-0.13, 1.04, label, transform=axis.transAxes, fontsize=10, fontweight="bold", va="top")

    fig.suptitle("R0.71Q  Quantitative analyticity retains radius, anchor, truncation, and cover taxes", fontsize=10.2, fontweight="bold")
    fig.text(0.5, -0.01, "Finite conditional audit. Panels B-D are analytic counterfamilies, not Navier-Stokes trajectories.", ha="center", fontsize=6.4, color=GRAY)

    stem = args.output_stem
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
