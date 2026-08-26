#!/usr/bin/env python3
"""Render the four-panel R0.71T finite-Galerkin journal figure."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter


PAPER = "#FBF9F4"
INK = "#252422"
BLUE = "#355C7D"
OCHRE = "#B8792B"
GRAY = "#77736C"
GRID = "#D8D3C8"


def load(path: Path) -> list[dict[str, str]]:
    return list(csv.DictReader(path.open(encoding="utf-8")))


def series(
    rows: list[dict[str, str]], panel: str, name: str
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


def configure_style() -> None:
    mpl.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 7.25,
        "axes.titlesize": 8.05,
        "axes.labelsize": 7.2,
        "xtick.labelsize": 6.5,
        "ytick.labelsize": 6.5,
        "legend.fontsize": 6.0,
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
        "svg.hashsalt": "r071t-internal-entry",
    })


def combined_legend(axis: plt.Axes, other: plt.Axes, **kwargs: object) -> None:
    handles, labels = axis.get_legend_handles_labels()
    other_handles, other_labels = other.get_legend_handles_labels()
    axis.legend(handles + other_handles, labels + other_labels, **kwargs)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, required=True)
    parser.add_argument("--output-stem", type=Path, required=True)
    args = parser.parse_args()
    rows = load(args.data)
    configure_style()
    fig, axes = plt.subplots(
        2,
        2,
        figsize=(178 / 25.4, 124 / 25.4),
        constrained_layout=True,
    )
    axa, axb, axc, axd = axes.ravel()

    x, y = series(rows, "A", "primary precompensation ratio")
    axa.semilogx(
        x,
        y,
        base=2,
        color=BLUE,
        marker="o",
        ms=3.3,
        label=r"primary $N=10, K_{\rm cut}=2$",
    )
    xi, yi = series(rows, "A", "independent refined check")
    axa.scatter(
        xi,
        yi,
        s=27,
        facecolors="none",
        edgecolors=OCHRE,
        marker="s",
        linewidths=1.2,
        zorder=4,
        label=r"direct convolution $N=12, K_{\rm cut}=3$",
    )
    axa.axhline(1.0, color=GRAY, linestyle=":", lw=1.0, label="leading IFT coefficient")
    axa.set_xlabel(r"internal time $\tau$")
    axa.set_ylabel(r"$\|z_\tau\|/(\tau\|P_*F(u_*)\|_2)$")
    axa.set_ylim(0.99988, 1.00164)
    axa.yaxis.set_major_formatter(FormatStrFormatter("%.4f"))
    axa.set_title("Precompensation approaches its linear coefficient", loc="left", fontweight="bold")
    axa.grid(True, color=GRID, lw=0.45)
    axa.legend(loc="upper left", frameon=False)
    axa.text(
        0.98,
        0.08,
        "focused vertical scale\nexact values in data.csv",
        transform=axa.transAxes,
        ha="right",
        fontsize=5.95,
        color=GRAY,
    )

    xb, principal = series(rows, "B", "signed principal coefficient")
    _, transverse = series(rows, "B", "transverse target norm")
    axb.plot(
        xb,
        principal,
        color=BLUE,
        marker="o",
        markevery=20,
        ms=2.8,
        label="signed principal coefficient",
    )
    axb.axhline(0.0, color=INK, lw=0.75)
    axb.axvline(1.0, color=GRAY, linestyle=":", lw=1.0, label=r"entry $t=\tau$")
    axb.set_xlabel(r"scaled time $t/\tau$  ($\tau=0.04$)")
    axb.set_ylabel("principal coefficient", color=BLUE)
    axb.tick_params(axis="y", colors=BLUE)
    axb.set_ylim(-1.12, 1.02)
    axb_right = axb.twinx()
    axb_right.semilogy(
        xb,
        transverse,
        color=OCHRE,
        linestyle="--",
        marker="s",
        markevery=20,
        ms=2.5,
        markerfacecolor="none",
        label="transverse shell norm",
    )
    axb_right.set_ylabel("transverse norm", color=OCHRE)
    axb_right.tick_params(axis="y", colors=OCHRE)
    axb_right.set_ylim(8e-17, 2e-14)
    axb.set_title("The target shell crosses zero at an internal time", loc="left", fontweight="bold")
    axb.grid(True, color=GRID, lw=0.45)
    combined_legend(axb, axb_right, loc="upper left", frameon=False)
    axb.text(
        0.98,
        0.08,
        r"$\|P_*u(\tau)\|_2<5.0\times10^{-17}$",
        transform=axb.transAxes,
        ha="right",
        fontsize=6.05,
    )

    for name, color, linestyle, marker, markerface, label, zorder in (
        ("entry atom A+", BLUE, "-", "o", BLUE, r"entry atom $A_+$", 3),
        (
            "slope-charge reconstruction",
            OCHRE,
            "--",
            "s",
            "none",
            "slope-charge reconstruction",
            4,
        ),
        (
            "small-time limit 1/4",
            GRAY,
            ":",
            "",
            GRAY,
            r"seed limit $1/4$",
            1,
        ),
    ):
        xc, yc = series(rows, "C", name)
        axc.semilogx(
            xc,
            yc,
            base=2,
            color=color,
            linestyle=linestyle,
            marker=marker,
            ms=4.2 if markerface == "none" else 3.1,
            markerfacecolor=markerface,
            markeredgecolor=color,
            zorder=zorder,
            label=label,
        )
    xci, yci = series(rows, "C", "independent refined A+")
    axc.scatter(
        xci,
        yci,
        s=34,
        facecolors="none",
        edgecolors=INK,
        marker="D",
        linewidths=1.0,
        zorder=5,
        label="refined direct-convolution check",
    )
    axc.set_xlabel(r"internal time $\tau$")
    axc.set_ylabel("normalized entry atom")
    axc.set_ylim(0.208, 0.255)
    axc.set_title("Entry atom equals its scale-zero slope charge", loc="left", fontweight="bold")
    axc.grid(True, color=GRID, lw=0.45)
    axc.legend(loc="lower left", frameon=False)
    axc.text(
        0.98,
        0.08,
        r"$A_+=\|P_*F\|_2^2/Y$" + "\n" + r"$=\|C_t\|_2^2/(\rho^4Y)$",
        transform=axc.transAxes,
        ha="right",
        fontsize=6.1,
    )

    xd, atom = series(rows, "D", "leading internal atom")
    _, budget = series(rows, "D", "leading bare budget")
    _, ratio = series(rows, "D", "atom-to-budget ratio")
    axd.loglog(
        xd,
        atom,
        base=2,
        color=BLUE,
        marker="o",
        ms=3.1,
        label=r"entry atom  $\lambda^{-4}$",
    )
    axd.loglog(
        xd,
        budget,
        base=2,
        color=OCHRE,
        linestyle="--",
        marker="s",
        markerfacecolor="none",
        ms=3.2,
        label=r"bare time budget  $\lambda^{-6}$",
    )
    axd.set_xlabel(r"integer NSE dilation $\lambda$")
    axd.set_ylabel("leading atom or budget")
    axd_right = axd.twinx()
    axd_right.loglog(
        xd,
        ratio,
        base=2,
        color=INK,
        linestyle="-.",
        marker="D",
        markerfacecolor="none",
        ms=3.0,
        label=r"ratio  $\lambda^2$",
    )
    axd_right.set_ylabel("atom / bare budget", color=INK)
    axd.set_title("Double scaling separates the atom from bare payment", loc="left", fontweight="bold")
    axd.grid(True, which="both", color=GRID, lw=0.45)
    combined_legend(axd, axd_right, loc="lower left", frameon=False)
    axd.text(
        0.98,
        0.92,
        r"$a_\lambda=\lambda^{-2},\ \nu=1,\ \tau=0.04$",
        transform=axd.transAxes,
        ha="right",
        va="top",
        fontsize=6.1,
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
        "R0.71T  Finite Galerkin audit of a positive-time target-shell entry",
        fontsize=10.0,
        fontweight="bold",
    )
    fig.text(
        0.5,
        -0.012,
        "Panels A–C: finite Fourier–Galerkin corroboration (time stepping; not DNS). Panel D: exact leading scaling ledger. No continuum PDE error bound.",
        ha="center",
        fontsize=6.15,
        color=GRAY,
    )
    stem = args.output_stem
    stem.parent.mkdir(parents=True, exist_ok=True)
    metadata = {"Creator": "R0.71T finite Galerkin internal-entry audit", "Date": None}
    fig.savefig(stem.with_suffix(".pdf"), bbox_inches="tight", metadata=metadata)
    fig.savefig(stem.with_suffix(".svg"), bbox_inches="tight", metadata=metadata)
    fig.savefig(stem.with_suffix(".png"), dpi=600, bbox_inches="tight", metadata={"Software": metadata["Creator"]})
    svg = stem.with_suffix(".svg")
    svg.write_text(
        "\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n",
        encoding="utf-8",
    )
    plt.close(fig)


if __name__ == "__main__":
    main()
