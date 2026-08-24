#!/usr/bin/env python3
"""Render the journal-style analytic figure for R0.70E.

The panels display exact trigonometric coefficient functions, the exact
reflection-parameter cubic for one normalized coefficient ratio, and the
closed-form hard-annulus Fourier multiplier.  They are explanatory analytic
plots, not DNS or numerical proof of the localization/IFT steps.
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
HERE = (
    ROOT
    / "figures"
    / "r070e-yu-parity-transversality"
    / "fig-r070e-yu-parity-transversality"
)
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070e-yu-parity-transversality"
INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a27a3f"
GREEN = "#55705b"
GRID = "#d5cec0"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def j1_over_x(value: np.ndarray) -> np.ndarray:
    result = np.empty_like(value)
    small = np.abs(value) < 2.0e-3
    squared = value[small] ** 2
    result[small] = (
        1.0 / 3.0
        - squared / 30.0
        + squared**2 / 840.0
        - squared**3 / 45360.0
    )
    regular = value[~small]
    result[~small] = (
        np.sin(regular) / regular**3 - np.cos(regular) / regular**2
    )
    return result


def shell_multiplier(kappa: np.ndarray, gamma: float) -> np.ndarray:
    return 3.0 * (
        j1_over_x(gamma * kappa) - j1_over_x(2.0 * gamma * kappa)
    )


def write_csv(path: Path, header: list[str], rows: list[tuple[float, ...]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            writer.writerow([f"{value:.17g}" for value in row])


def main() -> None:
    started = time.perf_counter()
    HERE.mkdir(parents=True, exist_ok=True)

    phase = np.linspace(-0.72, 0.72, 1201)
    base = -3.0 * np.sin(phase) ** 3
    mixed = 9.0 / 4.0 * (np.cos(phase) - np.cos(3.0 * phase))

    lam = np.linspace(0.25, 1.75, 1001)
    ratio_a3_a1 = 1.0 / 3.0
    cubic = (
        (1.0 + lam) ** 2 * (1.0 - lam)
        + ratio_a3_a1 * (1.0 - lam) ** 3
    ) / 8.0
    tangent = -0.5 * (lam - 1.0)

    gamma = 2.0
    kappa = np.linspace(0.0, 0.62, 1001)
    alpha = shell_multiplier(kappa, gamma)
    alpha_asymptotic = 3.0 * gamma**2 * kappa**2 / 10.0

    checks = {
        "baseOdd": bool(np.max(np.abs(base + base[::-1])) < 2.0e-14),
        "mixedEven": bool(np.max(np.abs(mixed - mixed[::-1])) < 2.0e-14),
        "mixedPositiveAtPositiveLobe": bool(mixed[np.argmin(np.abs(phase - 0.4))] > 0.0),
        "cubicRootAtOne": bool(abs(cubic[np.argmin(np.abs(lam - 1.0))]) < 2.0e-15),
        "cubicSimpleRoot": bool(abs((cubic[501] - cubic[499]) / (lam[501] - lam[499]) + 0.5) < 3.0e-5),
        "shellMultiplierPositive": bool(np.all(alpha[1:] > 0.0)),
        "shellSmallFrequencyCoefficient": bool(
            abs(alpha[2] / (kappa[2] ** 2) - 3.0 * gamma**2 / 10.0) < 2.0e-4
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    write_csv(
        HERE / "coefficient-data.csv",
        ["equal_phase_delta", "base_C0", "mixed_C1"],
        list(zip(phase, base, mixed)),
    )
    write_csv(
        HERE / "reflection-cubic-data.csv",
        ["lambda", "H_over_A1", "tangent_at_lambda_1"],
        list(zip(lam, cubic, tangent)),
    )
    write_csv(
        HERE / "shell-multiplier-data.csv",
        ["kappa_q_rj", "exact_alpha", "quadratic_asymptotic"],
        list(zip(kappa, alpha, alpha_asymptotic)),
    )

    plt.style.use(STYLE)
    plt.rcParams["figure.constrained_layout.use"] = False
    plt.rcParams["svg.hashsalt"] = FIGURE_ID
    fig = plt.figure(figsize=(180 / 25.4, 74 / 25.4))
    grid = fig.add_gridspec(1, 3, width_ratios=[1.14, 0.92, 1.0], wspace=0.36)
    ax_a = fig.add_subplot(grid[0, 0])
    ax_b = fig.add_subplot(grid[0, 1])
    ax_c = fig.add_subplot(grid[0, 2])

    ax_a.axhline(0.0, color=INK, lw=0.55)
    ax_a.plot(phase, base, color=RUST, lw=1.25, label=r"base $C_0=-3\sin^3\delta$")
    ax_a.plot(
        phase,
        mixed,
        color=BLUE,
        lw=1.25,
        label=r"mixed $C_1=\frac{9}{4}(\cos\delta-\cos3\delta)$",
    )
    for center in (-0.4, 0.4):
        ax_a.axvspan(center - 0.045, center + 0.045, color=GOLD, alpha=0.16, lw=0)
    ax_a.set_xlim(phase[0], phase[-1])
    ax_a.set_xlabel(r"equal phase $\delta$")
    ax_a.set_ylabel("cubic coefficient density")
    ax_a.set_title("A  Two-lobe transversality", loc="left", fontweight="bold")
    ax_a.grid(True, axis="y", color=GRID, lw=0.4)
    ax_a.legend(loc="upper left", frameon=False, fontsize=5.6)
    ax_a.text(
        0.03,
        0.04,
        r"$C_0$ cancels at $\pm\delta$; $C_1$ adds",
        transform=ax_a.transAxes,
        color=MUTED,
        fontsize=6.0,
    )

    ax_b.axhline(0.0, color=INK, lw=0.55)
    ax_b.axvline(1.0, color=GOLD, lw=0.7, ls=(0, (3, 2)))
    ax_b.plot(lam, cubic, color=INK, lw=1.45, label=r"$H(\lambda)/A_1$")
    ax_b.plot(lam, tangent, color=GREEN, lw=0.9, ls=(0, (4, 2)), label="root tangent")
    ax_b.scatter([1.0], [0.0], s=17, color=RUST, zorder=4)
    ax_b.set_xlim(lam[0], lam[-1])
    ax_b.set_xlabel(r"reflection amplitude $\lambda$")
    ax_b.set_ylabel(r"normalized signed work")
    ax_b.set_title("B  Exact simple parity root", loc="left", fontweight="bold")
    ax_b.grid(True, axis="y", color=GRID, lw=0.4)
    ax_b.legend(loc="lower left", frameon=False, fontsize=5.8)
    ax_b.text(
        0.96,
        0.94,
        r"$H'(1)/A_1=-1/2$",
        transform=ax_b.transAxes,
        ha="right",
        va="top",
        color=MUTED,
        fontsize=6.1,
    )

    ax_c.plot(kappa, alpha, color=BLUE, lw=1.45, label="exact Bessel multiplier")
    ax_c.plot(
        kappa,
        alpha_asymptotic,
        color=RUST,
        lw=0.95,
        ls=(0, (4, 2)),
        label=r"$3\Gamma^2\kappa^2/10$",
    )
    ax_c.set_xlim(kappa[0], kappa[-1])
    ax_c.set_ylim(bottom=0.0)
    ax_c.set_xlabel(r"shell frequency $\kappa=q r_j$")
    ax_c.set_ylabel(r"relative strain multiplier $\alpha$")
    ax_c.set_title("C  Hard shell remains active", loc="left", fontweight="bold")
    ax_c.grid(True, color=GRID, lw=0.4)
    ax_c.legend(loc="upper left", frameon=False, fontsize=5.7)
    ax_c.text(
        0.96,
        0.06,
        r"$\Gamma=2$; $\alpha>0$ on plotted interval",
        transform=ax_c.transAxes,
        ha="right",
        color=MUTED,
        fontsize=5.9,
    )

    fig.text(
        0.99,
        0.012,
        "exact analytic comparators — not DNS and not a numerical proof of localization",
        ha="right",
        va="bottom",
        color=MUTED,
        fontsize=5.8,
    )
    fig.subplots_adjust(left=0.066, right=0.989, bottom=0.205, top=0.89)
    fig.savefig(HERE / "figure.pdf")
    fig.savefig(HERE / "figure.svg")
    fig.savefig(HERE / "figure.png", dpi=600)
    plt.close(fig)

    svg_path = HERE / "figure.svg"
    svg_path.write_text(
        "\n".join(line.rstrip() for line in svg_path.read_text(encoding="utf-8").splitlines())
        + "\n",
        encoding="utf-8",
    )

    validation = {
        "status": "passed",
        "release": "R0.70E",
        "checks": checks,
        "diagnostics": {
            "gamma": gamma,
            "normalizedA3OverA1": ratio_a3_a1,
            "minimumPositiveShellMultiplier": float(np.min(alpha[1:])),
            "maximumShellMultiplier": float(np.max(alpha)),
        },
        "claimBoundary": (
            "Exact formula plots only; not DNS, not trajectory evidence, and "
            "not a numerical proof of compact localization, heat tails, or IFT."
        ),
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    image = Image.open(HERE / "figure.png")
    payloads = [
        "coefficient-data.csv",
        "reflection-cubic-data.csv",
        "shell-multiplier-data.csv",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "explanatory",
        "release": "R0.70E",
        "source": "research/r070e_parity_transversality_figure.py",
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
            "Analytic coefficient, cubic, and Fourier-multiplier comparators; "
            "not simulation evidence or a numerical PDE proof."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
