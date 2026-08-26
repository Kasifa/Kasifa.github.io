#!/usr/bin/env python3
"""Render the four-panel R0.71S signed-packet journal figure."""

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
GRID = "#D8D3C8"


def load(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(encoding="utf-8")))


def series(
    rows: list[dict[str, str]],
    panel: str,
    name: str,
) -> tuple[list[float], list[float]]:
    selected = [
        row for row in rows
        if row["panel"] == panel and row["series"] == name
    ]
    selected.sort(key=lambda row: float(row["x"]))
    return (
        [float(row["x"]) for row in selected],
        [float(row["y"]) for row in selected],
    )


def style() -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.4,
        "axes.titlesize": 8.2,
        "axes.labelsize": 7.4,
        "xtick.labelsize": 6.6,
        "ytick.labelsize": 6.6,
        "legend.fontsize": 6.15,
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
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(178 / 25.4, 118 / 25.4),
        constrained_layout=True,
    )
    axa, axb, axc, axd = axes.ravel()

    for name, color, linestyle, marker, label in (
        (
            "critical H^-1 packet cost",
            BLUE,
            "-",
            "o",
            r"critical $H^{-1}$ normalization",
        ),
        (
            "strong L2 coefficient",
            OCHRE,
            "--",
            "s",
            r"strong $L^2$ ledger",
        ),
    ):
        x, y = series(rows, "A", name)
        axa.loglog(
            x,
            y,
            color=color,
            linestyle=linestyle,
            marker=marker,
            ms=3.1,
            label=label,
        )
    axa.set_xlabel(r"packet frequency $K$")
    axa.set_ylabel("sampling coefficient")
    axa.set_title(
        "Box mean: critical K² cost or strong ledger",
        loc="left",
        fontweight="bold",
    )
    axa.grid(True, which="both", color=GRID, lw=0.45)
    axa.legend(loc="upper left", frameon=False)
    axa.text(
        0.97,
        0.08,
        r"$h=\theta K^{-2}$" + "\n" + r"$\theta=1/8$",
        transform=axa.transAxes,
        ha="right",
        fontsize=6.4,
    )

    for name, color, linestyle, marker in (
        ("largest eigenvalue", BLUE, "-", "o"),
        ("exact Rayleigh lower", OCHRE, "--", "^"),
        ("exact row-sum upper", GRAY, ":", ""),
    ):
        x, y = series(rows, "B", name)
        axb.loglog(
            x,
            y,
            base=2,
            color=color,
            linestyle=linestyle,
            marker=marker,
            ms=3.1,
            label=name,
        )
    axb.set_xlabel(r"integer overlap $p=Nh/T$")
    axb.set_ylabel("Gram constant")
    axb.set_title(
        "Same-direction packet Gram grows with overlap",
        loc="left",
        fontweight="bold",
    )
    axb.grid(True, which="both", color=GRID, lw=0.45)
    axb.legend(loc="upper left", frameon=False)
    axb.text(
        0.97,
        0.08,
        r"$N=64$"
        + "\n"
        + r"$p-(p^2-1)/(3N)\leq\lambda_{\max}\leq p$",
        transform=axb.transAxes,
        ha="right",
        fontsize=6.05,
    )

    for name, color, linestyle, marker, label in (
        (
            "critical H^-1 heat cost",
            BLUE,
            "-",
            "o",
            r"critical $H^{-1}$ normalization",
        ),
        (
            "strong L2 heat coefficient",
            OCHRE,
            "--",
            "s",
            r"strong $L^2$ ledger",
        ),
    ):
        x, y = series(rows, "C", name)
        axc.loglog(
            x,
            y,
            color=color,
            linestyle=linestyle,
            marker=marker,
            ms=3.1,
            label=label,
        )
    axc.set_xlabel(r"heat frequency $K$")
    axc.set_ylabel("inverse mean-square")
    axc.set_title(
        "Adjoint heat mean has the same K² cost",
        loc="left",
        fontweight="bold",
    )
    axc.grid(True, which="both", color=GRID, lw=0.45)
    axc.legend(loc="upper left", frameon=False)
    axc.text(
        0.97,
        0.08,
        r"$\frac{\nu K^2}{2}\coth(\nu\theta/2)$"
        + "\n"
        + r"$\nu=1,\ \theta=1/8$",
        transform=axc.transAxes,
        ha="right",
        fontsize=6.2,
    )

    for name, color, linestyle, marker, markerface, label in (
        ("positive face response", BLUE, "-", "o", BLUE, "positive face"),
        ("Jordan response", OCHRE, "--", "s", OCHRE, "Jordan face"),
        ("signed precursor response", GRAY, "-.", "x", GRAY, "signed precursor"),
        ("zero-mean detector response", INK, ":", "D", "none", "zero-mean detector"),
    ):
        x, y = series(rows, "D", name)
        axd.plot(
            x,
            y,
            color=color,
            linestyle=linestyle,
            marker=marker,
            ms=3.3,
            markerfacecolor=markerface,
            markeredgecolor=color,
            label=label,
            zorder=3 if "zero-mean" in name else 2,
        )
    axd.set_xlim(-0.25, 8.25)
    axd.set_ylim(-0.15, 2.15)
    axd.set_xlabel(r"soft-layer index $n$  ($\eta=2^{-8n}$)")
    axd.set_ylabel("normalized response")
    axd.set_title(
        "Even touch: Jordan survives; signed response cancels",
        loc="left",
        fontweight="bold",
    )
    axd.grid(True, color=GRID, lw=0.45)
    axd.legend(
        loc="center",
        bbox_to_anchor=(0.64, 0.66),
        frameon=False,
        ncol=2,
        columnspacing=0.9,
        handlelength=2.0,
    )

    for label, axis in zip("ABCD", axes.ravel()):
        axis.text(
            -0.13,
            1.04,
            label,
            transform=axis.transAxes,
            fontsize=10,
            fontweight="bold",
            va="top",
        )
    fig.suptitle(
        "R0.71S  Signed packets trade cancellation for inverse-height and Gram costs",
        fontsize=10.1,
        fontweight="bold",
    )
    fig.text(
        0.5,
        -0.01,
        "Panels A–C: exact packet or linear models. Panel D: forced-parabolic, not an NSE trajectory.",
        ha="center",
        fontsize=6.35,
        color=GRAY,
    )
    stem = args.output_stem
    stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight")
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight")
    svg = stem.with_suffix(".svg")
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
