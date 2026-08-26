#!/usr/bin/env python3
"""Render the four-panel R0.71R journal figure."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt


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

    for name, color, marker in (
        ("Lamb Sobolev order", BLUE, "o"),
        ("vorticity Sobolev order", OCHRE, "s"),
    ):
        x, y = series(rows, "A", name)
        axa.plot(x, y, color=color, marker=marker, markevery=20, ms=3.0, label=name)
    axa.axvline(0.0, color=GRAY, ls=":", lw=0.8)
    axa.axvline(2.0, color=GRAY, ls="--", lw=0.8)
    axa.set_xlim(-0.08, 2.08)
    axa.set_ylim(-1.12, 1.12)
    axa.set_xlabel(r"incidence exponent $\rho$")
    axa.set_ylabel("required Sobolev order")
    axa.set_title("Critical scaling and Leray payment miss by two", loc="left", fontweight="bold")
    axa.grid(True, color="#D8D3C8", lw=0.45)
    axa.legend(loc="upper right", frameon=False)
    axa.text(0.03, 0.06, r"critical $\rho=0$", transform=axa.transAxes, fontsize=6.4)
    axa.text(0.97, 0.06, r"minimal Leray $\rho=2$", transform=axa.transAxes, ha="right", fontsize=6.4)

    for name, color, ls, marker in (
        ("Gamma_2 jet surrogate", BLUE, "-", "o"),
        ("K squared law", OCHRE, "--", ""),
    ):
        x, y = series(rows, "B", name)
        label = r"$\Gamma_{2,\mathrm{jet}}$" if name == "Gamma_2 jet surrogate" else r"$K^2$ law"
        axb.loglog(x, y, color=color, linestyle=ls, marker=marker, ms=3.0, label=label)
    axb.set_xlabel(r"initial frequency $K$")
    axb.set_ylabel(r"Taylor-jet ratio")
    axb.set_title("A genuine NSE initial jet shows K² jet pressure", loc="left", fontweight="bold")
    axb.grid(True, which="both", color="#D8D3C8", lw=0.45)
    axb.legend(loc="upper left", frameon=False)
    axb.text(0.97, 0.07, r"$A_+=a^2/4$" + "\n" + r"$\|u_{0,K}\|_2^2=a^2$", transform=axb.transAxes, ha="right", va="bottom", fontsize=6.5)

    for name, color, ls, marker in (
        ("positive entry", BLUE, "-", "o"),
        ("source-square energy", OCHRE, "--", "s"),
    ):
        x, y = series(rows, "C", name)
        axc.loglog(x, y, color=color, linestyle=ls, marker=marker, ms=3.0, label=name)
    axc.invert_xaxis()
    axc.set_xlabel(r"observable amplitude $\varepsilon$")
    axc.set_ylabel("entry / source mass")
    axc.set_title("Degree-zero entry; quadratic source charge", loc="left", fontweight="bold")
    axc.grid(True, which="both", color="#D8D3C8", lw=0.45)
    axc.legend(loc="lower right", frameon=False)
    axc.text(0.03, 0.06, "forced scalar even touch\nnot an NSE trajectory", transform=axc.transAxes, fontsize=6.3, color=GRAY)

    for name, color, ls, marker in (
        ("sequential entries", BLUE, "-", "o"),
        ("sequential source", GRAY, ":", ""),
        ("component-union entries", OCHRE, "--", "s"),
        ("component source", INK, "-.", ""),
    ):
        x, y = series(rows, "D", name)
        axd.loglog(x, y, color=color, linestyle=ls, marker=marker, ms=3.0, label=name)
    axd.set_xlabel("event / component count")
    axd.set_ylabel("entry / source mass")
    axd.set_title("Bounded source does not count events", loc="left", fontweight="bold")
    axd.grid(True, which="both", color="#D8D3C8", lw=0.45)
    axd.legend(loc="upper left", frameon=False, ncol=2)
    axd.text(0.97, 0.06, "exact forced-parabolic families", transform=axd.transAxes, ha="right", fontsize=6.3, color=GRAY)

    for label, axis in zip("ABCD", axes.ravel()):
        axis.text(-0.13, 1.04, label, transform=axis.transAxes, fontsize=10, fontweight="bold", va="top")
    fig.suptitle("R0.71R  Parabolic incidence has a scale-versus-energy mismatch", fontsize=10.2, fontweight="bold")
    fig.text(0.5, -0.01, "Finite conditional theorem. Panel B stops at an exact NSE initial jet; panels C-D are not NSE trajectories.", ha="center", fontsize=6.4, color=GRAY)
    stem = args.output_stem
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
