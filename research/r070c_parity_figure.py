#!/usr/bin/env python3
"""Render the journal-style explanatory figure for R0.70C.

The left panel evaluates an exact analytic vortex-stretching witness.  The
right panel displays the proved amplitude orders with normalized coefficients.
Neither panel is a direct numerical simulation of Navier--Stokes.
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
from matplotlib.colors import TwoSlopeNorm
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
HERE = (
    ROOT
    / "figures"
    / "r070c-parity-obstruction"
    / "fig-r070c-parity-obstruction"
)
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070c-parity-obstruction"
INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GRID = "#d5cec0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_data(
    coordinates: np.ndarray,
    stretching: np.ndarray,
    epsilon: np.ndarray,
    absolute_order: np.ndarray,
    signed_order: np.ndarray,
) -> None:
    with (HERE / "slice-data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["x", "y", "z", "normalized_stretching"])
        for row, y_value in enumerate(coordinates):
            for column, x_value in enumerate(coordinates):
                writer.writerow(
                    [
                        f"{x_value:.17g}",
                        f"{y_value:.17g}",
                        f"{y_value:.17g}",
                        f"{stretching[row, column]:.17g}",
                    ]
                )

    with (HERE / "amplitude-data.csv").open(
        "w", newline="", encoding="utf-8"
    ) as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            ["epsilon", "normalized_absolute_activity", "signed_upper_order", "ratio"]
        )
        for eps, absolute, signed in zip(epsilon, absolute_order, signed_order):
            writer.writerow(
                [f"{eps:.17g}", f"{absolute:.17g}", f"{signed:.17g}", f"{signed / absolute:.17g}"]
            )


def render(
    coordinates: np.ndarray,
    stretching: np.ndarray,
    epsilon: np.ndarray,
    absolute_order: np.ndarray,
    signed_order: np.ndarray,
) -> None:
    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID

    fig = plt.figure(figsize=(178 / 25.4, 86 / 25.4))
    grid = fig.add_gridspec(1, 2, width_ratios=[1.18, 1.0], wspace=0.34)
    left = fig.add_subplot(grid[0, 0])
    right = fig.add_subplot(grid[0, 1])

    x_grid, y_grid = np.meshgrid(coordinates, coordinates)
    levels = np.linspace(-3.0, 3.0, 17)
    image = left.contourf(
        x_grid,
        y_grid,
        stretching,
        levels=levels,
        cmap="RdBu_r",
        norm=TwoSlopeNorm(vmin=-3.0, vcenter=0.0, vmax=3.0),
        extend="both",
    )
    left.contour(x_grid, y_grid, stretching, levels=[0.0], colors=INK, linewidths=0.55)
    left.set_aspect("equal")
    left.set_xlim(-np.pi, np.pi)
    left.set_ylim(-np.pi, np.pi)
    left.set_xticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
    left.set_yticks([-np.pi, 0, np.pi], [r"$-\pi$", "0", r"$\pi$"])
    left.set_xlabel(r"$x$")
    left.set_ylabel(r"$y$ on the plane $z=y$")
    left.set_title("A  Exact odd stretching witness", loc="left", fontweight="bold")
    left.text(
        0.97,
        0.96,
        r"$(x,y)\mapsto(-x,-y)$ flips sign",
        transform=left.transAxes,
        ha="right",
        va="top",
        fontsize=6.6,
        color=MUTED,
    )
    left.text(
        0.03,
        0.04,
        r"$e^{3\nu t}\,\omega\!\cdot\!S\omega=-3\sin x\,\sin^2 y$",
        transform=left.transAxes,
        ha="left",
        va="bottom",
        fontsize=6.9,
        color=INK,
        bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.84, "pad": 1.8},
    )
    colorbar = fig.colorbar(image, ax=left, orientation="horizontal", pad=0.19, fraction=0.055)
    colorbar.set_label("normalized vortex stretching", fontsize=7)
    colorbar.set_ticks([-3, 0, 3])

    right.loglog(
        epsilon,
        absolute_order,
        color=BLUE,
        lw=1.45,
        label=r"absolute activity $A_I\varepsilon^3$",
    )
    right.loglog(
        epsilon,
        signed_order,
        color=RUST,
        lw=1.25,
        ls=(0, (4, 2)),
        label=r"signed remainder order $C_I\varepsilon^4$",
    )
    right.fill_between(epsilon, signed_order, absolute_order, color=BLUE, alpha=0.08)
    right.set_xlim(epsilon[0], epsilon[-1])
    right.set_ylim(signed_order[0] / 2, absolute_order[-1] * 2)
    right.set_xlabel(r"small-data amplitude $\varepsilon$")
    right.set_ylabel("normalized magnitude")
    right.set_title("B  One-order cancellation gap", loc="left", fontweight="bold")
    right.grid(True, which="major", color=GRID, lw=0.45)
    right.legend(loc="upper left", bbox_to_anchor=(0.02, 0.84), frameon=False)
    right.text(
        0.04,
        0.95,
        r"$|W_I|/P_I=O(\varepsilon)\to0$",
        transform=right.transAxes,
        ha="left",
        va="top",
        color=INK,
        fontsize=7.2,
    )
    right.text(
        0.98,
        0.04,
        "order diagram; coefficients normalized to one",
        transform=right.transAxes,
        ha="right",
        va="bottom",
        color=MUTED,
        fontsize=6.4,
    )

    fig.text(
        0.99,
        0.012,
        "analytic witness and asymptotic orders — not DNS",
        ha="right",
        va="bottom",
        color=MUTED,
        fontsize=6.2,
    )
    fig.subplots_adjust(left=0.075, right=0.985, bottom=0.20, top=0.89)
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
    coordinates = np.linspace(-np.pi, np.pi, 129)
    x_grid, y_grid = np.meshgrid(coordinates, coordinates)
    stretching = -3.0 * np.sin(x_grid) * np.sin(y_grid) ** 2
    epsilon = np.logspace(-4, -1, 61)
    absolute_order = epsilon**3
    signed_order = epsilon**4

    parity_residual = float(np.max(np.abs(stretching[::-1, ::-1] + stretching)))
    mean_residual = float(abs(np.mean(stretching)))
    absolute_slope = float(np.polyfit(np.log(epsilon), np.log(absolute_order), 1)[0])
    signed_slope = float(np.polyfit(np.log(epsilon), np.log(signed_order), 1)[0])
    checks = {
        "finiteSlice": bool(np.all(np.isfinite(stretching))),
        "oddUnderPlaneInversion": parity_residual < 1e-13,
        "discreteMeanZero": mean_residual < 1e-14,
        "absoluteSlopeThree": abs(absolute_slope - 3.0) < 1e-12,
        "signedSlopeFour": abs(signed_slope - 4.0) < 1e-12,
        "ratioEqualsEpsilon": bool(np.allclose(signed_order / absolute_order, epsilon)),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    write_data(coordinates, stretching, epsilon, absolute_order, signed_order)
    render(coordinates, stretching, epsilon, absolute_order, signed_order)
    validation = {
        "status": "passed",
        "release": "R0.70C",
        "checks": checks,
        "diagnostics": {
            "maximumParityResidual": parity_residual,
            "discreteMeanResidual": mean_residual,
            "fittedAbsoluteSlope": absolute_slope,
            "fittedSignedSlope": signed_slope,
        },
        "claimBoundary": "analytic witness and normalized asymptotic orders; not DNS",
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    image = Image.open(HERE / "figure.png")
    payloads = [
        "slice-data.csv",
        "amplitude-data.csv",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "explanatory",
        "release": "R0.70C",
        "source": "research/r070c_parity_figure.py",
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
        "claimBoundary": "The figure explains exact parity and proved orders; it is not simulation evidence.",
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
