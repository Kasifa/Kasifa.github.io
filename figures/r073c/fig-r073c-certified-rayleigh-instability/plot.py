#!/usr/bin/env python3
"""Render the R0.73C certified Rayleigh-instability journal figure."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
INTERVAL = ROOT / "experiments/r073c/interval_run_b.json"
FOURIER = ROOT / "experiments/r073c/fourier_screen.json"
VALIDATION = ROOT / "experiments/r073c/independent_fourier_validation.json"
FIGURE_ID = "fig-r073c-certified-rayleigh-instability"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def trace_residual(eta: float) -> float:
    def rhs(x: float, values: np.ndarray) -> np.ndarray:
        w = -0.5 * np.sin(x) + 0.25 * np.sin(2.0 * x)
        wxx = 0.5 * np.sin(x) - np.sin(2.0 * x)
        coefficient = 0.25 + wxx / (w - 1j * eta)
        y = values.reshape(2, 2)
        return np.array([[y[1, 0], y[1, 1]],
                         [coefficient * y[0, 0],
                          coefficient * y[0, 1]]]).reshape(-1)

    initial = np.eye(2, dtype=np.complex128).reshape(-1)
    solution = solve_ivp(
        rhs, (0.0, 2.0 * np.pi), initial,
        method="DOP853", rtol=2e-13, atol=2e-15,
    )
    if not solution.success:
        raise RuntimeError(solution.message)
    matrix = solution.y[:, -1].reshape(2, 2)
    return float((np.trace(matrix) - 2.0).real)


def main() -> None:
    interval = json.loads(INTERVAL.read_text(encoding="utf-8"))
    fourier = json.loads(FOURIER.read_text(encoding="utf-8"))
    validation = json.loads(VALIDATION.read_text(encoding="utf-8"))
    if interval.get("status") != "passed":
        raise RuntimeError("formal interval input is not passed")
    signs = [row["sign"] for row in interval["results"]]
    if signs != ["negative", "positive"]:
        raise RuntimeError("formal interval endpoints are not opposite-sign")
    if validation.get("status") != "passed":
        raise RuntimeError("finite diagnostic validation is not passed")

    mpl.rcParams.update({
        "font.family": "serif",
        "font.serif": ["STIX Two Text", "Times New Roman", "DejaVu Serif"],
        "mathtext.fontset": "stix",
        "font.size": 7.4,
        "axes.titlesize": 8.3,
        "axes.labelsize": 7.5,
        "xtick.labelsize": 6.7,
        "ytick.labelsize": 6.7,
        "legend.fontsize": 6.4,
        "axes.linewidth": 0.65,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })
    gold = "#a86f17"
    red = "#9d3f32"
    blue = "#355f77"
    green = "#3f6b54"
    ink = "#1c1b19"
    grid = "#d8d1c4"

    width = 178 / 25.4
    height = 132 / 25.4
    fig = plt.figure(figsize=(width, height), constrained_layout=False)
    gs = fig.add_gridspec(2, 2, left=0.075, right=0.985, bottom=0.09,
                          top=0.955, wspace=0.34, hspace=0.42)
    ax_a = fig.add_subplot(gs[0, 0])
    ax_b = fig.add_subplot(gs[0, 1])
    ax_c = fig.add_subplot(gs[1, 0])
    ax_d = fig.add_subplot(gs[1, 1])

    x = np.linspace(0.0, 2.0 * np.pi, 700)
    w = -0.5 * np.sin(x) + 0.25 * np.sin(2.0 * x)
    phi = np.sin(x / 2.0) ** 3
    ax_a.axhline(0.0, color=grid, lw=0.7)
    ax_a.plot(x / np.pi, w, color=ink, lw=1.3, label=r"$W_0(x)$")
    ax_a.plot(x / np.pi, phi, color=gold, lw=1.25,
              label=r"$\phi_0=|\sin(x/2)|^3$")
    ax_a.set(xlabel=r"$x/\pi$", ylabel="amplitude",
             xlim=(0, 2), ylim=(-0.8, 1.1))
    ax_a.set_xticks([0, 0.5, 1, 1.5, 2])
    ax_a.legend(frameon=False, loc="lower right")
    ax_a.set_title(r"exact cubic neutral level: $\gamma_0^2=7/4$", pad=5)

    etas = np.linspace(0.336, 0.346, 61)
    traces = np.array([trace_residual(float(eta)) for eta in etas])
    ax_b.axhline(0.0, color=ink, lw=0.75)
    ax_b.plot(etas, traces, color=blue, lw=1.25,
              label="high-accuracy ODE diagnostic")
    endpoint_eta = [float(row["eta"]) for row in interval["results"]]
    endpoint_f = [trace_residual(value) for value in endpoint_eta]
    ax_b.scatter(endpoint_eta, endpoint_f, s=26, color=[red, green],
                 edgecolor="white", linewidth=0.55, zorder=4,
                 label="certified endpoint signs")
    ax_b.axvspan(endpoint_eta[0], endpoint_eta[1], color=gold, alpha=0.11,
                 label=r"existence bracket for $\eta_*$")
    ax_b.set(xlabel=r"imaginary phase speed $\eta$",
             ylabel=r"$F(\eta)=\mathrm{tr}\,M(\eta)-2$",
             xlim=(etas[0], etas[-1]))
    ax_b.ticklabel_format(axis="y", style="sci", scilimits=(-2, 2))
    ax_b.legend(frameon=False, loc="upper left")
    ax_b.set_title(r"infinite-dimensional periodic-ODE certificate", pad=5)

    rows = [row for row in fourier["leadingGalerkinRows"]
            if abs(float(row["gamma"]) - 0.5) < 1e-14]
    rows.sort(key=lambda row: int(row["N"]))
    cutoffs = np.array([int(row["N"]) for row in rows])
    eigenvalues = np.array([float(row["leadingReal"]) for row in rows])
    residuals = np.array([float(row["embeddedResidual"]) for row in rows])
    ax_c.axhspan(0.17035, 0.17050, color=gold, alpha=0.15,
                 label="certified sigma bracket")
    ax_c.plot(cutoffs, eigenvalues, "o-", ms=3.2, lw=1.0, color=blue,
              label=r"finite $P_N A P_N$")
    ax_c.set_xscale("log", base=2)
    ax_c.set(xlabel="Fourier cutoff N", ylabel=r"leading $\Re\,\sigma_N$",
             ylim=(0.17034, 0.17051))
    ax_c.set_xticks([8, 16, 32, 64, 128], labels=["8", "16", "32", "64", "128"])
    ax_c.ticklabel_format(axis="y", style="plain", useOffset=False)
    ax_c_res = ax_c.twinx()
    ax_c_res.semilogy(cutoffs, residuals, "s--", ms=2.8, lw=0.9,
                      color=red, label="embedded residual")
    ax_c_res.set_ylabel("finite embedded residual", color=red)
    ax_c_res.tick_params(axis="y", colors=red)
    handles, labels = ax_c.get_legend_handles_labels()
    h2, l2 = ax_c_res.get_legend_handles_labels()
    ax_c.legend(handles + h2, labels + l2, frameon=False, loc="center right")
    ax_c.set_title("finite diagnostic agrees with the certified bracket", pad=5)

    ax_d.axis("off")
    boxes = [
        (0.82, green, "C3", "CLOSED",
         "exact singular spectrum\nneutral threshold gamma-squared = 7/4"),
        (0.62, green, "C4", "CLOSED",
         "certified periodic mode\nsigma in (0.17035, 0.17050)"),
        (0.42, red, "C5", "OPEN",
         "viscous Riesz + dichotomy\nand domain control missing"),
        (0.22, gold, "C6", "CONDITIONAL",
         "super-polynomial no-go\nrequires C5"),
    ]
    for yc, color, claim, status, body in boxes:
        patch = mpl.patches.FancyBboxPatch(
            (0.02, yc - 0.072), 0.96, 0.144,
            boxstyle="round,pad=0.008,rounding_size=0.012",
            transform=ax_d.transAxes, facecolor=mpl.colors.to_rgba(color, 0.10),
            edgecolor=color, linewidth=0.9,
        )
        ax_d.add_patch(patch)
        ax_d.text(0.055, yc, claim, transform=ax_d.transAxes,
                  color=color, weight="bold", fontsize=8.0,
                  va="center", ha="left")
        ax_d.text(0.18, yc, status, transform=ax_d.transAxes,
                  color=color, weight="bold", fontsize=7.0,
                  va="center", ha="left")
        ax_d.text(0.46, yc, body, transform=ax_d.transAxes,
                  color=ink, fontsize=5.75, va="center", ha="left",
                  linespacing=1.20)
    for upper, lower in ((0.748, 0.692), (0.548, 0.492), (0.348, 0.292)):
        ax_d.annotate("", xy=(0.50, lower), xytext=(0.50, upper),
                      xycoords="axes fraction",
                      arrowprops=dict(arrowstyle="->", color=ink, lw=0.7))
    ax_d.text(0.02, 0.055,
              "Not proved: root uniqueness, OS-Squire A2, nonlinear NSE, Clay.",
              transform=ax_d.transAxes, fontsize=6.4, color=ink)
    ax_d.set_title("claim boundary and the next theorem gate", pad=5)

    for label, axis in zip("ABCD", [ax_a, ax_b, ax_c, ax_d]):
        axis.text(-0.13, 1.08, label, transform=axis.transAxes,
                  fontsize=9.2, weight="bold", va="top", ha="left")
    for axis in (ax_a, ax_b, ax_c):
        axis.grid(True, color=grid, lw=0.45, alpha=0.7)
        axis.spines[["top", "right"]].set_visible(False)

    outputs = {
        "pdf": HERE / "figure.pdf",
        "svg": HERE / "figure.svg",
        "png": HERE / "figure.png",
    }
    fig.savefig(outputs["pdf"], metadata={
        "Title": "R0.73C certified frozen Rayleigh instability",
        "Author": "ChuiKuan Zeng",
        "Subject": "Validated periodic Rayleigh monodromy certificate",
    })
    fig.savefig(outputs["svg"])
    fig.savefig(outputs["png"], dpi=600)
    plt.close(fig)

    results = {
        "schemaVersion": "r073c-figure-results-v1",
        "figureId": FIGURE_ID,
        "intervalInput": {"path": str(INTERVAL.relative_to(ROOT)),
                          "sha256": sha256(INTERVAL)},
        "fourierInput": {"path": str(FOURIER.relative_to(ROOT)),
                         "sha256": sha256(FOURIER)},
        "finiteValidation": {"path": str(VALIDATION.relative_to(ROOT)),
                             "sha256": sha256(VALIDATION)},
        "etaBracket": endpoint_eta,
        "endpointTraceDiagnostic": endpoint_f,
        "sigmaBracket": [0.17035, 0.17050],
        "finiteLimitDiagnostic": float(eigenvalues[-1]),
        "claimBoundary": {
            "smoothTraceCurveCertified": False,
            "endpointSignsCertifiedByInput": True,
            "finiteFourierRowsAreTheorem": False,
            "viscousTransferProved": False,
            "nonlinearNavierStokesProved": False,
            "clayProblemSolved": False,
        },
    }
    (HERE / "results.json").write_text(
        json.dumps(results, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
