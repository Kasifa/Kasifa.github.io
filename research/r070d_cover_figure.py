#!/usr/bin/env python3
"""Render the journal-style explanatory figure for R0.70D.

Panel A shows one analytic high-frequency scalar witness and one translated
fixed-resolution observer.  Panel B plots the exact negative-to-signed ratio.
The figure is not DNS and the scalar witness is not asserted to be an NSE flux.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import time
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HERE = ROOT / "figures" / "r070d-cover-blindness" / "fig-r070d-cover-blindness"
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070d-cover-blindness"
INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a27a3f"
GRID = "#d5cec0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def negative_mass(delta: np.ndarray) -> np.ndarray:
    return (
        2.0 * np.sqrt(1.0 - delta**2)
        - delta * (np.pi - 2.0 * np.arcsin(delta))
    ) / (2.0 * np.pi)


def write_data(
    x: np.ndarray,
    signal: np.ndarray,
    observed: np.ndarray,
    delta_grid: np.ndarray,
    mass: np.ndarray,
    ratio: np.ndarray,
) -> None:
    with (HERE / "witness-data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["x1", "scalar_density", "translated_coarse_average"])
        for values in zip(x, signal, observed):
            writer.writerow([f"{value:.17g}" for value in values])

    with (HERE / "ratio-data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "delta",
                "normalized_negative_mass",
                "negative_to_signed_ratio",
                "leading_asymptote",
            ]
        )
        for delta_value, mass_value, ratio_value in zip(delta_grid, mass, ratio):
            writer.writerow(
                [
                    f"{delta_value:.17g}",
                    f"{mass_value:.17g}",
                    f"{ratio_value:.17g}",
                    f"{1.0 / (np.pi * delta_value):.17g}",
                ]
            )


def render(
    x: np.ndarray,
    signal: np.ndarray,
    observed: np.ndarray,
    delta_value: float,
    frequency: int,
    sigma: float,
    delta_grid: np.ndarray,
    mass: np.ndarray,
    ratio: np.ndarray,
) -> None:
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID

    fig = plt.figure(figsize=(178 / 25.4, 86 / 25.4))
    grid = fig.add_gridspec(1, 2, width_ratios=[1.22, 1.0], wspace=0.31)
    left = fig.add_subplot(grid[0, 0])
    right = fig.add_subplot(grid[0, 1])

    left.axhline(0.0, color=INK, lw=0.55)
    left.fill_between(
        x,
        signal,
        0.0,
        where=signal < 0.0,
        color=RUST,
        alpha=0.23,
        interpolate=True,
        label=r"unresolved negative part",
    )
    left.plot(x, signal, color=INK, lw=0.72, label=rf"$f_{{\delta,N}}$, $N={frequency}$")
    left.plot(
        x,
        observed,
        color=BLUE,
        lw=1.5,
        label=rf"fixed-scale average, $\sigma={sigma:g}$",
    )
    left.axhline(delta_value, color=GOLD, lw=0.7, ls=(0, (4, 2)))
    left.set_xlim(0.0, 2.0 * np.pi)
    left.set_ylim(-1.02, 1.28)
    left.set_xticks([0.0, np.pi, 2.0 * np.pi], ["0", r"$\pi$", r"$2\pi$"])
    left.set_xlabel(r"$x_1$")
    left.set_ylabel("signed scalar density")
    left.set_title("A  Positive coarse view, negative fine mass", loc="left", fontweight="bold")
    left.grid(True, axis="y", color=GRID, lw=0.4)
    left.legend(loc="upper right", frameon=False, fontsize=6.3)
    left.text(
        0.02,
        0.04,
        rf"$\delta={delta_value:g}$; shaded mass is order one",
        transform=left.transAxes,
        ha="left",
        va="bottom",
        color=MUTED,
        fontsize=6.5,
    )

    asymptote = 1.0 / (np.pi * delta_grid)
    right.loglog(delta_grid, ratio, color=RUST, lw=1.55, label="exact ratio")
    right.loglog(
        delta_grid,
        asymptote,
        color=BLUE,
        lw=1.0,
        ls=(0, (4, 2)),
        label=r"$1/(\pi\delta)$",
    )
    right.set_xlim(delta_grid[0], delta_grid[-1])
    right.set_ylim(0.12, asymptote[0] * 1.35)
    right.set_xlabel(r"positive signed mean $\delta$")
    right.set_ylabel(r"$\|f_-\|_1\,/\,\int f$")
    right.set_title("B  Exact sign-defect separation", loc="left", fontweight="bold")
    right.grid(True, which="major", color=GRID, lw=0.45)
    right.legend(loc="upper right", frameon=False)
    right.text(
        0.04,
        0.05,
        r"$\|f_-\|_1\to1/\pi$ while $\int f=\delta\to0$",
        transform=right.transAxes,
        ha="left",
        va="bottom",
        color=INK,
        fontsize=6.7,
    )

    fig.text(
        0.99,
        0.012,
        "analytic scalar witness — not DNS and not an NSE-flux realization",
        ha="right",
        va="bottom",
        color=MUTED,
        fontsize=6.1,
    )
    fig.subplots_adjust(left=0.073, right=0.985, bottom=0.19, top=0.89)
    fig.savefig(HERE / "figure.pdf")
    svg_path = HERE / "figure.svg"
    fig.savefig(svg_path)
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)

    svg_text = svg_path.read_text(encoding="utf-8")
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_text.splitlines()) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    started = time.perf_counter()
    HERE.mkdir(parents=True, exist_ok=True)

    delta_value = 0.12
    frequency = 18
    sigma = 0.20
    x = np.linspace(0.0, 2.0 * np.pi, 2401)
    signal = delta_value + np.sin(frequency * x)

    # Convolution with a translated wrapped Gaussian (heat kernel) multiplies
    # the N-th Fourier mode by exp(-sigma^2*N^2/2).
    attenuation = float(np.exp(-0.5 * sigma**2 * frequency**2))
    observed = delta_value + attenuation * np.sin(frequency * x)

    delta_grid = np.logspace(-3.0, np.log10(0.5), 181)
    mass = negative_mass(delta_grid)
    ratio = mass / delta_grid
    half_lower_bound = (np.sqrt(3.0) - np.pi / 3.0) / (2.0 * np.pi)

    checks = {
        "signalHasNegativeSet": bool(np.min(signal) < 0.0),
        "coarseAverageStrictlyPositive": bool(np.min(observed) > 0.0),
        "negativeMassMonotone": bool(np.all(np.diff(mass) < 0.0)),
        "uniformHalfIntervalLowerBound": bool(np.min(mass) >= half_lower_bound - 1e-14),
        "smallDeltaMassNearOneOverPi": bool(abs(mass[0] - 1.0 / np.pi) < 1.1e-3),
        "ratioMatchesDefinition": bool(np.allclose(ratio, mass / delta_grid)),
        "ratioApproachesAsymptote": bool(abs(ratio[0] * np.pi * delta_grid[0] - 1.0) < 0.002),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    write_data(x, signal, observed, delta_grid, mass, ratio)
    render(
        x,
        signal,
        observed,
        delta_value,
        frequency,
        sigma,
        delta_grid,
        mass,
        ratio,
    )

    validation = {
        "status": "passed",
        "release": "R0.70D",
        "checks": checks,
        "diagnostics": {
            "delta": delta_value,
            "frequency": frequency,
            "observerSigma": sigma,
            "fourierAttenuation": attenuation,
            "minimumObservedAverage": float(np.min(observed)),
            "minimumNegativeMassOnLockedInterval": float(np.min(mass)),
            "exactLowerBoundFloat": float(half_lower_bound),
        },
        "claimBoundary": (
            "analytic scalar witness and exact formula; not DNS, not an NSE "
            "flux sample, and not a numerical proof of the uniform theorem"
        ),
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    image = Image.open(HERE / "figure.png")
    payloads = [
        "witness-data.csv",
        "ratio-data.csv",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "explanatory",
        "release": "R0.70D",
        "source": "research/r070d_cover_figure.py",
        "outputs": [
            {
                "path": name,
                "bytes": (HERE / name).stat().st_size,
                "sha256": sha256(HERE / name),
            }
            for name in payloads
        ],
        "png": {"pixels": [image.width, image.height], "dpi": 600},
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "elapsedSeconds": time.perf_counter() - started,
        },
        "claimBoundary": (
            "The figure explains a scalar fixed-resolution obstruction; it "
            "is not simulation evidence or an NSE-flux realization."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
