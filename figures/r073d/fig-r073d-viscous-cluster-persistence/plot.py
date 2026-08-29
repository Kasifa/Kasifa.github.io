#!/usr/bin/env python3
"""Build the R0.73D journal figure from sealed analytic and finite inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--experiment", type=Path, required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402
import numpy as np  # noqa: E402


COLORS = {
    "ink": "#1c1b19",
    "muted": "#6b665e",
    "blue": "#315f84",
    "blue2": "#6f9db9",
    "gold": "#a87224",
    "green": "#3d6d57",
    "red": "#9b4a42",
    "paper": "#fbfaf6",
    "grid": "#d9d4ca",
    "pale_blue": "#e7eff3",
    "pale_gold": "#f3ead9",
    "pale_green": "#e5eee8",
    "pale_red": "#f3e6e3",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def panel_label(ax, label: str, title: str) -> None:
    ax.text(
        -0.035, 1.045, label, transform=ax.transAxes,
        fontsize=9.4, fontweight="bold", color=COLORS["ink"], va="bottom"
    )
    ax.text(
        0.02, 1.045, title, transform=ax.transAxes,
        fontsize=8.3, fontweight="bold", color=COLORS["ink"], va="bottom"
    )


def box(ax, xy, width, height, text, face, edge, fontsize=7.2) -> None:
    patch = FancyBboxPatch(
        xy, width, height,
        boxstyle="round,pad=0.012,rounding_size=0.02",
        transform=ax.transAxes,
        facecolor=face, edgecolor=edge, linewidth=0.8,
    )
    ax.add_patch(patch)
    ax.text(
        xy[0] + width / 2, xy[1] + height / 2, text,
        transform=ax.transAxes, ha="center", va="center",
        fontsize=fontsize, color=COLORS["ink"], linespacing=1.25,
    )


def draw_operator_panel(ax) -> None:
    ax.set_axis_off()
    panel_label(ax, "A", "Exact kinetic-space reduction")
    box(ax, (0.02, 0.68), 0.28, 0.19,
        r"$X_{1/4}$" + "\nphysical kinetic space",
        COLORS["pale_gold"], COLORS["gold"])
    box(ax, (0.37, 0.68), 0.24, 0.19,
        r"$U=2L^{-1/2}$" + "\nonto isometry",
        COLORS["pale_blue"], COLORS["blue"])
    box(ax, (0.68, 0.68), 0.29, 0.19,
        r"$L^2(\mathbb{T})$" + "\nstandard norm",
        COLORS["pale_green"], COLORS["green"])
    for x0, x1 in ((0.30, 0.37), (0.61, 0.68)):
        ax.annotate(
            "", xy=(x1, 0.775), xytext=(x0, 0.775),
            xycoords=ax.transAxes, textcoords=ax.transAxes,
            arrowprops=dict(arrowstyle="->", lw=1.0, color=COLORS["ink"]),
        )

    box(ax, (0.10, 0.33), 0.80, 0.20,
        r"$UB_\varepsilon U^{-1}=M+K-\varepsilon L$" + "\n"
        + r"$M=-\frac{i}{2}M_{W_0}$ skew,   $K$ compact",
        "#f1f0eb", COLORS["muted"], fontsize=8.0)
    ax.annotate(
        "", xy=(0.50, 0.54), xytext=(0.50, 0.66),
        xycoords=ax.transAxes, textcoords=ax.transAxes,
        arrowprops=dict(arrowstyle="->", lw=1.0, color=COLORS["ink"]),
    )
    box(ax, (0.08, 0.05), 0.38, 0.15,
        r"$D(H_0)=L^2$" + "\nzero-viscosity domain",
        COLORS["pale_blue"], COLORS["blue"])
    box(ax, (0.54, 0.05), 0.38, 0.15,
        r"$D(H_\varepsilon)=H^2$" + "\n" + r"$\varepsilon>0$",
        COLORS["pale_red"], COLORS["red"])
    ax.text(
        0.50, 0.255, "singular domain jump retained",
        transform=ax.transAxes, ha="center", va="center",
        fontsize=7.0, color=COLORS["muted"], fontstyle="italic",
    )


def draw_eigenvalue_panel(ax, rows) -> None:
    panel_label(ax, "B", "Finite eigenvalue diagnostic as viscosity vanishes")
    cutoffs = sorted({int(row["N"]) for row in rows})
    palette = ["#a87224", "#6f9db9", "#315f84", "#1c1b19"]
    for N, color in zip(cutoffs, palette):
        selected = sorted(
            (row for row in rows if int(row["N"]) == N and row["epsilon"] > 0),
            key=lambda row: row["epsilon"], reverse=True,
        )
        eps = [row["epsilon"] for row in selected]
        vals = [row["lambdaReal"] for row in selected]
        ax.plot(eps, vals, marker="o", ms=2.6, lw=1.0, color=color, label=f"N={N}")
    ax.axhspan(0.17035, 0.17050, color=COLORS["pale_green"], zorder=0)
    ax.axhline(0.170407976920433, color=COLORS["green"], lw=0.9, ls="--")
    ax.text(
        0.60, 0.96, "R0.73C inviscid bracket",
        transform=ax.transAxes, fontsize=6.3, color=COLORS["green"],
        ha="left", va="top",
    )
    ax.set_xscale("log")
    ax.invert_xaxis()
    ax.set_xlabel(r"viscosity $\varepsilon$  (toward zero $\rightarrow$)", fontsize=7.0)
    ax.set_ylabel(r"$\operatorname{Re}\lambda_{\varepsilon,N}$", fontsize=7.0)
    ax.grid(True, which="both", lw=0.45, color=COLORS["grid"], alpha=0.8)
    ax.tick_params(labelsize=6.3, length=2.5)
    ax.legend(frameon=False, fontsize=6.1, ncol=2, loc="lower right")
    ax.text(
        0.02, 0.04, "finite compression only",
        transform=ax.transAxes, fontsize=6.3, color=COLORS["red"],
        bbox=dict(boxstyle="round,pad=0.18", facecolor=COLORS["pale_red"], edgecolor="none"),
    )


def draw_projection_panel(ax, rows) -> None:
    panel_label(ax, "C", "Finite projector diagnostic in the kinetic norm")
    selected = sorted(
        (row for row in rows if int(row["N"]) == 128 and row["epsilon"] > 0),
        key=lambda row: row["epsilon"], reverse=True,
    )
    eps = np.asarray([row["epsilon"] for row in selected])
    diff = np.asarray([row["projectorDifferenceFromEpsilonZero"] for row in selected])
    pnorm = np.asarray([row["projectorNorm"] for row in selected])
    line1 = ax.loglog(
        eps, diff, marker="o", ms=3.0, lw=1.2, color=COLORS["blue"],
        label=r"$\|P_{\varepsilon,128}-P_{0,128}\|$",
    )[0]
    reference = diff[-3] * (eps / eps[-3])
    ax.loglog(eps, reference, lw=0.8, ls=":", color=COLORS["muted"], label=r"reference $C\varepsilon$")
    ax.invert_xaxis()
    ax.set_xlabel(r"viscosity $\varepsilon$  (toward zero $\rightarrow$)", fontsize=7.0)
    ax.set_ylabel("finite projector difference", fontsize=7.0, color=COLORS["blue"])
    ax.tick_params(axis="both", labelsize=6.3, length=2.5)
    ax.tick_params(axis="y", colors=COLORS["blue"])
    ax.grid(True, which="both", lw=0.45, color=COLORS["grid"], alpha=0.8)

    twin = ax.twinx()
    line2 = twin.semilogx(
        eps, pnorm, marker="s", ms=2.8, lw=1.0, color=COLORS["gold"],
        label=r"$\|P_{\varepsilon,128}\|$",
    )[0]
    twin.set_ylabel("finite projector norm", fontsize=7.0, color=COLORS["gold"])
    twin.tick_params(axis="y", labelsize=6.3, colors=COLORS["gold"], length=2.5)
    twin.set_ylim(1.44, 1.71)
    ax.legend(
        [line1, line2],
        [line1.get_label(), line2.get_label()],
        frameon=False, fontsize=6.2, loc="center right",
    )
    ax.text(
        0.02, 0.04, "diagnostic, not the continuum proof",
        transform=ax.transAxes, fontsize=6.2, color=COLORS["red"],
        bbox=dict(boxstyle="round,pad=0.18", facecolor=COLORS["pale_red"], edgecolor="none"),
    )


def draw_boundary_panel(ax) -> None:
    ax.set_axis_off()
    panel_label(ax, "D", "Closed theorem and exact remaining boundary")
    closed = [
        "fixed contour / resolvent",
        "Riesz norm convergence",
        "cluster multiplicity",
        "cluster eigenvalues",
    ]
    open_items = [
        "simplicity / explicit rate",
        "complement dichotomy",
        "fast-time transfer",
        "nonlinear NSE / Clay",
    ]
    ax.text(
        0.03, 0.92, "CLOSED\nfixed-cluster theorem",
        transform=ax.transAxes, fontsize=7.0, fontweight="bold",
        color=COLORS["green"], va="top", linespacing=1.2,
    )
    for index, item in enumerate(closed):
        y = 0.70 - 0.11 * index
        ax.text(0.04, y, "[x]", transform=ax.transAxes, fontsize=7.0, color=COLORS["green"], va="center")
        ax.text(0.13, y, item, transform=ax.transAxes, fontsize=6.45, color=COLORS["ink"], va="center")
    ax.text(
        0.57, 0.92, "OPEN\nnext proof gates",
        transform=ax.transAxes, fontsize=7.0, fontweight="bold",
        color=COLORS["red"], va="top", linespacing=1.2,
    )
    for index, item in enumerate(open_items):
        y = 0.70 - 0.11 * index
        ax.text(0.58, y, "[ ]", transform=ax.transAxes, fontsize=7.0, color=COLORS["red"], va="center")
        ax.text(0.67, y, item, transform=ax.transAxes, fontsize=6.45, color=COLORS["ink"], va="center")
    box(ax, (0.06, 0.10), 0.88, 0.16,
        "General persistence precedent: Shvydkoy-Friedlander (2008)\n"
        "This release gives a self-contained fixed-row norm proof; no priority claim.",
        "#f1f0eb", COLORS["muted"], fontsize=6.7)


def main() -> int:
    experiment = json.loads(ARGS.experiment.read_text())
    certificate = json.loads(ARGS.certificate.read_text())
    if not all(experiment["checks"].values()):
        raise RuntimeError("finite diagnostic checks are not all true")
    if not all(certificate["checks"].values()):
        raise RuntimeError("analytic certificate checks are not all true")
    if certificate["claimBoundary"]["logFastTimeTransfer"] is not False:
        raise RuntimeError("fast-time boundary is not fail-closed")

    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["STIX Two Text", "Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "axes.edgecolor": COLORS["ink"],
        "axes.linewidth": 0.7,
        "figure.facecolor": COLORS["paper"],
        "axes.facecolor": COLORS["paper"],
        "savefig.facecolor": COLORS["paper"],
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })

    fig = plt.figure(figsize=(7.0079, 5.1969))
    # Reserve a dedicated title band. Panel labels intentionally sit just
    # above the axes, so constrained layout alone can let them collide with
    # the figure title after the physical page size is fixed.
    grid = fig.add_gridspec(
        2, 2,
        left=0.065, right=0.975, bottom=0.075, top=0.875,
        hspace=0.58, wspace=0.48,
    )
    axes = [fig.add_subplot(grid[i, j]) for i in range(2) for j in range(2)]
    draw_operator_panel(axes[0])
    draw_eigenvalue_panel(axes[1], experiment["rows"])
    draw_projection_panel(axes[2], experiment["rows"])
    draw_boundary_panel(axes[3])
    fig.suptitle(
        "Static viscous persistence of the certified periodic Rayleigh cluster",
        fontsize=10.2, fontweight="bold", color=COLORS["ink"], y=0.965,
    )

    ARGS.output_dir.mkdir(parents=True, exist_ok=True)
    pdf = ARGS.output_dir / "figure.pdf"
    svg = ARGS.output_dir / "figure.svg"
    png = ARGS.output_dir / "figure.png"
    fig.savefig(pdf)
    fig.savefig(svg)
    fig.savefig(png, dpi=600)
    plt.close(fig)

    selected = [
        {
            key: row[key]
            for key in (
                "N", "epsilon", "lambdaReal", "lambdaImag",
                "projectorNorm", "projectorDifferenceFromEpsilonZero",
                "embeddedResidual",
            )
        }
        for row in experiment["rows"]
        if row["N"] == 128 and row["epsilon"] in (0.0, 1e-2, 1e-4, 1e-6, 1e-8)
    ]
    result = {
        "schemaVersion": "r073d-figure-results-v1",
        "figureId": "fig-r073d-viscous-cluster-persistence",
        "release": "R0.73D",
        "inputs": [
            {"path": str(ARGS.experiment), "sha256": sha256(ARGS.experiment)},
            {"path": str(ARGS.certificate), "sha256": sha256(ARGS.certificate)},
        ],
        "selectedFiniteRows": selected,
        "claimBoundary": {
            "staticVanishingViscosityPersistence": True,
            "fixedClusterRieszProjectionNormConvergence": True,
            "finiteCurvesAreContinuumProof": False,
            "inviscidEigenvalueSimple": False,
            "explicitContourRadius": False,
            "logFastTimeTransfer": False,
            "nonlinearNavierStokes": False,
            "clayProblemSolved": False,
        },
        "outputs": [
            {"path": "figure.pdf", "sha256": sha256(pdf), "bytes": len(pdf.read_bytes())},
            {"path": "figure.svg", "sha256": sha256(svg), "bytes": len(svg.read_bytes())},
            {"path": "figure.png", "sha256": sha256(png), "bytes": len(png.read_bytes())},
        ],
    }
    (ARGS.output_dir / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n"
    )
    print(json.dumps({"event": "figure-built", "outputs": result["outputs"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
