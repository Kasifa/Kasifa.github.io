#!/usr/bin/env python3
"""Build the R0.73E finite complement-transfer diagnostic figure."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--deps", default="")
    parser.add_argument("--diagnostic", type=Path, required=True)
    parser.add_argument("--independent-validation", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


ARGS = parse_args()
if ARGS.deps:
    sys.path.insert(0, ARGS.deps)

import matplotlib  # noqa: E402

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
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
    "pale_red": "#f3e6e3",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def panel_label(ax, label: str, title: str) -> None:
    ax.text(-0.03, 1.055, label, transform=ax.transAxes, fontsize=9.2,
            fontweight="bold", color=COLORS["ink"], va="bottom")
    ax.text(0.035, 1.055, title, transform=ax.transAxes, fontsize=8.0,
            fontweight="bold", color=COLORS["ink"], va="bottom")


def selected_row(data: dict) -> dict:
    rows = [row for row in data["rows"]
            if int(row["N"]) == 96 and float(row["epsilon"]) == 1e-6]
    if len(rows) != 1:
        raise RuntimeError("expected exactly one N=96, epsilon=1e-6 row")
    return rows[0]


def draw_spectrum(ax, row: dict) -> None:
    panel_label(ax, "A", "Rightmost finite spectrum after one-cluster removal")
    cluster = row["clusterEigenvalue"]
    qvals = row["qSpectrum"]["sixRightmost"]
    q_re = np.asarray([z["real"] for z in qvals])
    q_im = np.asarray([z["imag"] for z in qvals])
    unstable = q_re > 1e-10
    stable = ~unstable
    ax.axvspan(0.0, 0.19, color=COLORS["pale_red"], alpha=0.60, zorder=0)
    ax.axvline(0.0, color=COLORS["muted"], lw=0.75, ls=":")
    ax.scatter(q_re[stable], q_im[stable], marker="x", s=25,
               color=COLORS["muted"], lw=1.0, label=r"rightmost $Q_\varepsilon$ values")
    ax.scatter(q_re[unstable], q_im[unstable], marker="o", s=31,
               facecolor=COLORS["pale_gold"], edgecolor=COLORS["gold"],
               lw=1.0, label="additional positive-real pair")
    ax.scatter([cluster["real"]], [cluster["imag"]], marker="*", s=72,
               color=COLORS["blue"], edgecolor=COLORS["ink"], lw=0.45,
               label=r"removed leading $P_\varepsilon$ cluster")
    ax.annotate(r"$0.04054\pm0.17614i$", xy=(q_re[0], q_im[0]),
                xytext=(0.070, -0.125), fontsize=6.0, color=COLORS["gold"],
                arrowprops=dict(arrowstyle="-", color=COLORS["gold"], lw=0.7))
    ax.annotate(r"$0.17041$", xy=(cluster["real"], cluster["imag"]),
                xytext=(0.125, 0.085), fontsize=6.0, color=COLORS["blue"],
                arrowprops=dict(arrowstyle="-", color=COLORS["blue"], lw=0.7))
    ax.set_xlim(-0.03, 0.19)
    ax.set_ylim(-0.29, 0.29)
    ax.set_xlabel(r"$\operatorname{Re}\lambda$", fontsize=6.8)
    ax.set_ylabel(r"$\operatorname{Im}\lambda$", fontsize=6.8)
    ax.tick_params(labelsize=6.0, length=2.5)
    ax.grid(True, lw=0.42, color=COLORS["grid"], alpha=0.8)
    ax.legend(frameon=False, fontsize=5.65, loc="upper right", handletextpad=0.35)
    ax.text(0.02, 0.035, r"$N=96,\ \varepsilon=10^{-6}$; six rightmost $Q_\varepsilon$ values only",
            transform=ax.transAxes, fontsize=5.75, color=COLORS["red"],
            bbox=dict(boxstyle="round,pad=0.16", facecolor=COLORS["pale_red"], edgecolor="none"))


def draw_resolvent(ax, data: dict) -> None:
    panel_label(ax, "B", "Sampled vertical-line Q-resolvent peaks")
    rows = sorted((row for row in data["rows"] if int(row["N"]) == 96),
                  key=lambda row: float(row["epsilon"]), reverse=True)
    styles = [
        (0.05, COLORS["red"], "o", "-"),
        (0.08, COLORS["gold"], "s", "--"),
        (0.12, COLORS["blue"], "^", "-."),
    ]
    for line_re, color, marker, linestyle in styles:
        eps = []
        peaks = []
        for row in rows:
            line = next(item for item in row["resolventVerticalLines"]
                        if abs(float(item["lineRealPart"]) - line_re) < 1e-14)
            eps.append(float(row["epsilon"]))
            peaks.append(float(line["resolventNormMaximum"]))
        ax.loglog(eps, peaks, marker=marker, ms=2.8, lw=1.0,
                  ls=linestyle, color=color,
                  label=rf"$\operatorname{{Re}}z={line_re:.2f}$")
    ax.invert_xaxis()
    ax.set_xlabel(r"viscosity $\varepsilon$  (toward zero $\rightarrow$)", fontsize=6.8)
    ax.set_ylabel(r"sampled $\max_{|\operatorname{Im}z|\leq0.4}\|(z-B)^{-1}Q\|_2$",
                  fontsize=6.45)
    ax.tick_params(labelsize=6.0, length=2.5)
    ax.grid(True, which="both", lw=0.42, color=COLORS["grid"], alpha=0.8)
    ax.legend(frameon=False, fontsize=6.0, loc="upper left")
    ax.text(0.97, 0.055, "finite grid + scalar peak refinement",
            transform=ax.transAxes, ha="right", fontsize=5.7, color=COLORS["red"])


def draw_intrinsic_semigroup(ax, row: dict) -> None:
    panel_label(ax, "C", "Intrinsic moving-complement semigroup diagnostic")
    semigroup = row["semigroup"]
    alpha = float(semigroup["qSpectralAbscissa"])
    rows = semigroup["rows"]
    time = np.asarray([float(item["time"]) for item in rows])
    norm = np.asarray([float(item["intrinsicMovingQNorm"]) for item in rows])
    normalized = norm * np.exp(-alpha * time)
    ax.semilogy(time, norm, color=COLORS["blue"], lw=1.25,
                label=r"$\|e^{tB_\varepsilon}Q_\varepsilon\|$ (intrinsic basis)")
    ax.semilogy(time, normalized, color=COLORS["gold"], lw=1.05, ls="--",
                label=r"$e^{-\alpha_Qt}\|e^{tB_\varepsilon}Q_\varepsilon\|$")
    ax.axvline(float(semigroup["intrinsicMovingQ"]["tailFitStartsAt"]),
               color=COLORS["muted"], lw=0.7, ls=":")
    ax.text(0.61, 0.10, rf"$\alpha_Q={alpha:.5f}$" + "\nfinite spectral abscissa",
            transform=ax.transAxes, fontsize=5.9, color=COLORS["ink"])
    ax.set_xlabel("time t", fontsize=6.8)
    ax.set_ylabel("operator 2-norm", fontsize=6.8)
    ax.tick_params(labelsize=6.0, length=2.5)
    ax.grid(True, which="both", lw=0.42, color=COLORS["grid"], alpha=0.8)
    ax.legend(frameon=False, fontsize=5.75, loc="upper left")
    ax.text(0.02, 0.035, "stored time grid only; no continuous-time bound",
            transform=ax.transAxes, fontsize=5.7, color=COLORS["red"])


def draw_projection_leakage(ax, row: dict) -> None:
    panel_label(ax, "D", "A fixed inviscid complement leaks into the leading mode")
    rows = row["semigroup"]["rows"]
    time = np.asarray([float(item["time"]) for item in rows])
    fixed = np.asarray([float(item["ambientFixedQ0Norm"]) for item in rows])
    moving = np.asarray([float(item["ambientMovingQNorm"]) for item in rows])
    ax.semilogy(time, fixed, color=COLORS["red"], lw=1.25,
                label=r"fixed $Q_0$: $\|e^{tB_\varepsilon}Q_0\|_2$")
    ax.semilogy(time, moving, color=COLORS["blue"], lw=1.15, ls="--",
                label=r"moving $Q_\varepsilon$: $\|e^{tB_\varepsilon}Q_\varepsilon\|_2$")
    ax.annotate(r"$1.95\times10^{11}$", xy=(time[-1], fixed[-1]),
                xytext=(112, 2.0e9), fontsize=6.0, color=COLORS["red"],
                arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=0.75))
    ax.annotate(r"$1.69\times10^4$", xy=(time[-1], moving[-1]),
                xytext=(115, 2.0e3), fontsize=6.0, color=COLORS["blue"],
                arrowprops=dict(arrowstyle="->", color=COLORS["blue"], lw=0.75))
    ax.set_xlabel("time t", fontsize=6.8)
    ax.set_ylabel("ambient operator 2-norm", fontsize=6.8)
    ax.tick_params(labelsize=6.0, length=2.5)
    ax.grid(True, which="both", lw=0.42, color=COLORS["grid"], alpha=0.8)
    ax.legend(frameon=False, fontsize=5.6, loc="upper left")
    ax.text(0.02, 0.035,
            "finite lesson: project every selected top cluster; do not use fixed Q0 at long times",
            transform=ax.transAxes, fontsize=5.55, color=COLORS["red"],
            bbox=dict(boxstyle="round,pad=0.15", facecolor=COLORS["pale_red"], edgecolor="none"))


def main() -> int:
    diagnostic = json.loads(ARGS.diagnostic.read_text(encoding="utf-8"))
    independent = json.loads(ARGS.independent_validation.read_text(encoding="utf-8"))
    if not diagnostic.get("allChecksPass"):
        raise RuntimeError("primary finite diagnostic did not pass")
    if not independent.get("allChecksPass"):
        raise RuntimeError("independent finite validation did not pass")
    if independent["primary"]["sha256"] != sha256(ARGS.diagnostic):
        raise RuntimeError("independent validation is not bound to the diagnostic")
    row = selected_row(diagnostic)

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
    fig = plt.figure(figsize=(178 / 25.4, 132 / 25.4))
    grid = fig.add_gridspec(2, 2, left=0.068, right=0.975, bottom=0.075,
                            top=0.875, hspace=0.56, wspace=0.38)
    axes = [fig.add_subplot(grid[i, j]) for i in range(2) for j in range(2)]
    draw_spectrum(axes[0], row)
    draw_resolvent(axes[1], diagnostic)
    draw_intrinsic_semigroup(axes[2], row)
    draw_projection_leakage(axes[3], row)
    fig.suptitle("Finite complement diagnostics for spectral projection and transfer",
                 fontsize=10.0, fontweight="bold", color=COLORS["ink"], y=0.963)
    fig.text(0.5, 0.918,
             r"periodic Rayleigh row; $N=96$, $\varepsilon=10^{-6}$ unless stated; IEEE-754 binary64",
             ha="center", fontsize=6.5, color=COLORS["muted"])

    ARGS.output_dir.mkdir(parents=True, exist_ok=True)
    pdf = ARGS.output_dir / "figure.pdf"
    svg = ARGS.output_dir / "figure.svg"
    png = ARGS.output_dir / "figure.png"
    fig.savefig(pdf)
    fig.savefig(svg)
    fig.savefig(png, dpi=600)
    plt.close(fig)

    selected = {
        "N": row["N"],
        "epsilon": row["epsilon"],
        "clusterEigenvalue": row["clusterEigenvalue"],
        "qSpectrum": row["qSpectrum"],
        "resolventVerticalLines": row["resolventVerticalLines"],
        "movingVsFixed": row["movingVsFixed"],
        "semigroupEndpoints": {
            "fixedQ0": row["semigroup"]["ambientFixedQ0"]["endpointNorm"],
            "movingQ": row["semigroup"]["ambientMovingQ"]["endpointNorm"],
            "intrinsicMovingQ": row["semigroup"]["intrinsicMovingQ"]["endpointNorm"],
            "normalizedPeak": row["semigroup"]["intrinsicMovingQ"]["spectralAbscissaNormalizedPeak"],
        },
        "independentMaximumErrors": independent["maximumErrors"],
    }
    result = {
        "schemaVersion": "r073e-figure-results-v1",
        "release": "R0.73E",
        "figureId": "fig-r073e-complement-transfer",
        "inputs": [
            {"path": str(ARGS.diagnostic), "sha256": sha256(ARGS.diagnostic)},
            {"path": str(ARGS.independent_validation),
             "sha256": sha256(ARGS.independent_validation)},
        ],
        "selectedFiniteData": selected,
        "claimBoundary": {
            "formalFiniteDiagnosticFigure": True,
            "independentFiniteRecomputation": True,
            "finiteSpectrumIsContinuumSpectrum": False,
            "finiteResolventPeaksAreUniformHalfPlaneBound": False,
            "sampledSemigroupIsContinuousTimeBound": False,
            "fixedProjectionIsValidAtLongTimes": False,
            "additionalContinuumEigenpairProvedHere": False,
            "continuumComplementDichotomyProvedHere": False,
            "nonautonomousTransferProvedHere": False,
            "nonlinearNavierStokesProvedHere": False,
            "clayProblemSolved": False,
        },
        "outputs": [
            {"path": "figure.pdf", "sha256": sha256(pdf), "bytes": pdf.stat().st_size},
            {"path": "figure.svg", "sha256": sha256(svg), "bytes": svg.stat().st_size},
            {"path": "figure.png", "sha256": sha256(png), "bytes": png.stat().st_size},
        ],
    }
    (ARGS.output_dir / "results.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"event": "figure-built", "outputs": result["outputs"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
