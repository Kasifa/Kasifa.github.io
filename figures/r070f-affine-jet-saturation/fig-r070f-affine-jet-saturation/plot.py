#!/usr/bin/env python3
"""Render the journal-style analytic figure for R0.70F.

The numerical arrays are evaluations of exact closed formulas: Taylor gap
powers, triangular dyadic sums, and the finite-chain recurrence factor. The
right panel is a construction diagram. Nothing in this figure is DNS,
trajectory evidence, or a numerical Navier--Stokes proof.
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
from matplotlib.patches import Circle, FancyArrowPatch, Wedge
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070f-affine-jet-saturation"

INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a27a3f"
GREEN = "#55705b"
GRID = "#d5cec0"
PAPER = "#f8f4eb"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, header: list[str], rows: list[tuple[float, ...]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            writer.writerow([f"{value:.17g}" for value in row])


def triangular_sum(beta: int, count: np.ndarray) -> np.ndarray:
    denominator = 2.0**beta - 1.0
    return (
        count / denominator
        - (1.0 - 2.0 ** (-beta * count)) / denominator**2
    )


def main() -> None:
    started = time.perf_counter()
    HERE.mkdir(parents=True, exist_ok=True)

    gap = np.arange(1.0, 13.0)
    theta = 2.0 ** (-gap)
    constant = theta
    linear = theta**2
    affine_remainder = theta**3
    quadratic_remainder = theta**4

    count = np.arange(1.0, 81.0)
    sums = {beta: triangular_sum(beta, count) for beta in range(1, 5)}
    slopes = {beta: 1.0 / (2.0**beta - 1.0) for beta in range(1, 5)}

    lam = 16.0
    layer = np.arange(1.0, 31.0)
    recurrence = (
        (1.0 - lam ** (-4.0 * layer)) / (1.0 - lam**-4.0)
    ) ** 2

    checks = {
        "taylorFactorsStrictlyDecrease": bool(
            np.all(np.diff(constant) < 0.0)
            and np.all(np.diff(linear) < 0.0)
            and np.all(np.diff(affine_remainder) < 0.0)
            and np.all(np.diff(quadratic_remainder) < 0.0)
        ),
        "powerOrdering": bool(
            np.all(constant > linear)
            and np.all(linear > affine_remainder)
            and np.all(affine_remainder > quadratic_remainder)
        ),
        "triangularSumsIncrease": bool(
            all(np.all(np.diff(values) > 0.0) for values in sums.values())
        ),
        "betaThreeSlopeApproach": bool(
            abs((sums[3][-1] - sums[3][-2]) - slopes[3]) < 1.0e-12
        ),
        "recurrencePositiveAndBounded": bool(
            np.all(recurrence >= 1.0)
            and np.all(recurrence <= (1.0 - lam**-4.0) ** -2 + 1.0e-14)
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    write_csv(
        HERE / "taylor-gap-data.csv",
        [
            "gap_k_minus_j",
            "constant_theta",
            "linear_theta2",
            "affine_remainder_theta3",
            "quadratic_remainder_theta4",
        ],
        list(
            zip(
                gap,
                constant,
                linear,
                affine_remainder,
                quadratic_remainder,
            )
        ),
    )
    write_csv(
        HERE / "triangular-sum-data.csv",
        [
            "number_of_scales_N",
            "beta1_sum",
            "beta2_sum",
            "beta3_sum",
            "beta4_sum",
        ],
        list(zip(count, sums[1], sums[2], sums[3], sums[4])),
    )
    write_csv(
        HERE / "recurrence-factor-data.csv",
        ["active_layer_n", "b_n_squared", "Lambda"],
        [(n_value, b_value, lam) for n_value, b_value in zip(layer, recurrence)],
    )

    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig = plt.figure(figsize=(180 / 25.4, 78 / 25.4))
    grid = fig.add_gridspec(1, 3, width_ratios=[1.00, 1.06, 0.94], wspace=0.32)
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[0, 2])

    ax_a.semilogy(gap, constant, marker="o", ms=2.3, color=RUST, lw=1.15, label=r"constant $\theta$")
    ax_a.semilogy(gap, linear, marker="s", ms=2.1, color=GOLD, lw=1.10, label=r"linear $\theta^2$")
    ax_a.semilogy(gap, affine_remainder, marker="^", ms=2.2, color=BLUE, lw=1.15, label=r"affine rem. $\theta^3$")
    ax_a.semilogy(gap, quadratic_remainder, color=GREEN, lw=0.9, ls=(0, (3, 2)), label=r"quadratic rem. $\theta^4$")
    ax_a.set_xlim(1, 12)
    ax_a.set_xticks([1, 3, 6, 9, 12])
    ax_a.set_xlabel(r"scale gap $m=k-j$")
    ax_a.set_ylabel("normalized work factor")
    ax_a.set_title("A  Taylor gain is exact", loc="left", fontweight="bold")
    ax_a.grid(True, which="major", color=GRID, lw=0.4)
    ax_a.legend(loc="lower left", frameon=False, fontsize=5.3)

    colors = {1: RUST, 2: GOLD, 3: BLUE, 4: GREEN}
    labels = {
        1: r"$\beta=1$  slope $1$",
        2: r"$\beta=2$  slope $1/3$",
        3: r"$\beta=3$  slope $1/7$",
        4: r"$\beta=4$  slope $1/15$",
    }
    for beta in range(1, 5):
        ax_b.plot(count, sums[beta], color=colors[beta], lw=1.15, label=labels[beta])
    ax_b.set_xlim(1, 80)
    ax_b.set_ylim(bottom=0.0)
    ax_b.set_xlabel(r"number of nested scales $N$")
    ax_b.set_ylabel(r"$D_{\beta,N}$")
    ax_b.set_title("B  Every fixed power still grows", loc="left", fontweight="bold")
    ax_b.grid(True, color=GRID, lw=0.4)
    ax_b.legend(loc="upper left", frameon=False, fontsize=5.3)
    ax_b.text(
        0.97,
        0.05,
        r"after affine subtraction: $D_{3,N}=N/7+O(1)$",
        transform=ax_b.transAxes,
        ha="right",
        color=MUTED,
        fontsize=5.7,
    )

    ax_c.set_aspect("equal")
    ax_c.set_xlim(-1.14, 1.14)
    ax_c.set_ylim(-1.12, 1.16)
    ax_c.axis("off")
    ax_c.set_title("C  Initial-face witness", loc="left", fontweight="bold")

    source_annulus = Wedge(
        (0.0, 0.0),
        1.0,
        0.0,
        360.0,
        width=0.18,
        facecolor=RUST,
        alpha=0.23,
        edgecolor=RUST,
        lw=0.8,
    )
    ax_c.add_patch(source_annulus)
    ax_c.add_patch(Circle((0.0, 0.0), 0.81, facecolor=PAPER, edgecolor=GRID, lw=0.6))
    ax_c.add_patch(Circle((0.0, 0.0), 0.34, facecolor=BLUE, alpha=0.08, edgecolor=BLUE, lw=0.8))
    ax_c.add_patch(Circle((0.17, 0.0), 0.075, facecolor=GOLD, alpha=0.55, edgecolor=GOLD, lw=0.8))
    ax_c.add_patch(
        FancyArrowPatch(
            (-0.40, -0.13),
            (0.08, -0.02),
            arrowstyle="-|>",
            mutation_scale=7,
            lw=0.8,
            color=BLUE,
        )
    )
    ax_c.text(0.0, 0.93, r"fixed source $\psi_j\Omega$", ha="center", va="center", color=RUST, fontsize=5.8)
    ax_c.text(-0.02, 0.51, "harmonic core", ha="center", color=MUTED, fontsize=5.7)
    ax_c.text(0.17, 0.11, r"$\chi_n$: off-centre", ha="center", color=INK, fontsize=5.5)
    ax_c.text(0.17, -0.01, r"$\Omega\parallel e_1$", ha="center", va="center", color=INK, fontsize=5.5)
    ax_c.text(-0.46, -0.24, r"$A$ or $Lx$", color=BLUE, fontsize=5.7)
    ax_c.text(
        0.0,
        -0.76,
        r"$J_n^{(0)}\sim\Lambda^{-2}$" "\n"
        r"$J_n^{(1)}\sim\Lambda^{-3}$",
        ha="center",
        va="center",
        color=INK,
        fontsize=6.0,
        linespacing=1.35,
    )
    ax_c.text(
        0.0,
        -1.04,
        "t=0 exact  •  common-top case open",
        ha="center",
        color=MUTED,
        fontsize=5.4,
    )

    fig.text(
        0.99,
        0.012,
        "closed-form comparators and construction geometry — not DNS or cascade evidence",
        ha="right",
        va="bottom",
        color=MUTED,
        fontsize=5.6,
    )
    fig.subplots_adjust(left=0.074, right=0.991, bottom=0.205, top=0.89)
    fig.savefig(HERE / "figure.pdf")
    fig.savefig(HERE / "figure.svg")
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)

    svg_path = HERE / "figure.svg"
    svg_path.write_text(
        "\n".join(
            line.rstrip()
            for line in svg_path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )

    validation = {
        "status": "passed",
        "release": "R0.70F",
        "checks": checks,
        "diagnostics": {
            "Lambda": lam,
            "betaThreeAsymptoticSlope": slopes[3],
            "maximumRecurrenceFactor": float(np.max(recurrence)),
        },
        "claimBoundary": (
            "Exact formula evaluations and analytic construction geometry; "
            "not DNS, trajectory evidence, or a numerical proof of "
            "common-top-time Navier--Stokes recurrence."
        ),
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    image = Image.open(HERE / "figure.png")
    payloads = [
        "taylor-gap-data.csv",
        "triangular-sum-data.csv",
        "recurrence-factor-data.csv",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "explanatory",
        "release": "R0.70F",
        "source": "plot.py",
        "sourceSha256": sha256(Path(__file__)),
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
            "Analytic Taylor factors, exact dyadic sums, and construction "
            "geometry; not simulation evidence or a numerical PDE proof."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
