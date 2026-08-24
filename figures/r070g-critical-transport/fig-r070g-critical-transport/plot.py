#!/usr/bin/env python3
"""Render the journal-style analytic figure for R0.70G.

Every array evaluates a closed formula for critical jet transport, an
ordinary-difference recurrence, or a source/core square-function comparator.
Nothing in this package is DNS, trajectory evidence, or a numerical
Navier--Stokes proof.
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
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070g-critical-transport"
RELEASE = "R0.70G"

INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#8b4d43"
GOLD = "#a27a3f"
PALE_BLUE = "#e6edf1"
PALE_RUST = "#f1e4df"
GRID = "#d5cec0"
WHITE = "#ffffff"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_csv(path: Path, header: list[str], rows: list[tuple[object, ...]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            rendered: list[object] = []
            for value in row:
                if isinstance(value, (float, np.floating)):
                    rendered.append(f"{float(value):.17g}")
                else:
                    rendered.append(value)
            writer.writerow(rendered)


def normalize_svg(path: Path) -> None:
    path.write_text(
        "\n".join(
            line.rstrip()
            for line in path.read_text(encoding="utf-8").splitlines()
        )
        + "\n",
        encoding="utf-8",
    )


def blossom(figure: plt.Figure) -> None:
    center = (0.968, 0.938)
    for dx, dy, angle in (
        (0.0, 0.010, 0.0),
        (0.0, -0.010, 0.0),
        (0.008, 0.0, 90.0),
        (-0.008, 0.0, 90.0),
    ):
        figure.add_artist(
            Ellipse(
                (center[0] + dx, center[1] + dy),
                0.010,
                0.018,
                angle=angle,
                transform=figure.transFigure,
                facecolor="#ead9b8",
                edgecolor=GOLD,
                linewidth=0.35,
            )
        )


def main() -> None:
    started = time.perf_counter()
    HERE.mkdir(parents=True, exist_ok=True)

    # Panel A: exact critical transport coefficients.
    order = np.arange(3, dtype=int)
    transport = 2.0 ** (-(order + 2))
    dual_dilation = 1.0 / transport
    unmatched_defect = 1.0 - transport
    order_labels = ["constant", "linear", "quadratic"]

    # Panel B: exact constant recurrence comparator.
    count = np.arange(1, 41, dtype=int)
    p_value = 1.0 - 2.0 ** (-count)
    raw_mass = count.astype(float) - 1.0 + 2.0 ** (-count)
    ordinary_increment = 2.0 ** (-count)
    difference_mass = p_value.copy()

    # Panel C: exact source/core square-function comparator.
    square_count = np.arange(1, 33, dtype=int)
    source_increment = 2.0 ** (-square_count)
    source_weighted_sum = 1.0 - 2.0 ** (-square_count)
    source_factor = np.sqrt(source_weighted_sum)
    core_dual_increment = np.ones_like(square_count, dtype=float)
    core_dual_sum = square_count.astype(float)
    core_dual_factor = np.sqrt(core_dual_sum)

    checks = {
        "criticalTransportExact": bool(
            np.array_equal(transport, np.array([0.25, 0.125, 0.0625]))
        ),
        "dualDilationReciprocal": bool(
            np.array_equal(dual_dilation, np.array([4.0, 8.0, 16.0]))
            and np.allclose(transport * dual_dilation, 1.0, rtol=0.0, atol=0.0)
        ),
        "constantRecurrenceClosedForm": bool(
            np.allclose(
                np.cumsum(1.0 - 2.0 ** (-count)),
                raw_mass,
                rtol=0.0,
                atol=2.0e-15,
            )
        ),
        "ordinaryDifferenceGeometric": bool(
            np.allclose(
                np.diff(np.concatenate(([0.0], p_value))),
                ordinary_increment,
                rtol=0.0,
                atol=2.0e-15,
            )
            and np.allclose(
                ordinary_increment[1:] / ordinary_increment[:-1],
                0.5,
                rtol=0.0,
                atol=0.0,
            )
        ),
        "ordinaryDifferenceMassBounded": bool(
            np.all(difference_mass > 0.0)
            and np.all(difference_mass < 1.0)
            and np.all(np.diff(difference_mass) > 0.0)
        ),
        "sourceSquareFunctionBounded": bool(
            np.allclose(
                np.cumsum(source_increment),
                source_weighted_sum,
                rtol=0.0,
                atol=2.0e-15,
            )
            and np.all(source_weighted_sum < 1.0)
        ),
        "coreDualComparatorLinear": bool(
            np.array_equal(np.cumsum(core_dual_increment), core_dual_sum)
            and np.allclose(core_dual_factor**2, core_dual_sum)
        ),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    write_csv(
        HERE / "critical-transport-data.csv",
        [
            "jet_order_n",
            "jet_label",
            "transport_coefficient_2_pow_minus_n_plus_2",
            "reciprocal_dual_dilation",
            "unmatched_defect_if_dual_held_fixed",
        ],
        [
            (
                int(n_value),
                label,
                coefficient,
                reciprocal,
                defect,
            )
            for n_value, label, coefficient, reciprocal, defect in zip(
                order,
                order_labels,
                transport,
                dual_dilation,
                unmatched_defect,
            )
        ],
    )
    write_csv(
        HERE / "constant-recurrence-data.csv",
        [
            "number_of_scales_N",
            "cumulative_coefficient_p_N",
            "raw_cumulative_mass",
            "ordinary_difference_increment",
            "ordinary_difference_cumulative_mass",
        ],
        [
            (
                int(n_value),
                p_current,
                raw_current,
                increment,
                difference_current,
            )
            for n_value, p_current, raw_current, increment, difference_current in zip(
                count,
                p_value,
                raw_mass,
                ordinary_increment,
                difference_mass,
            )
        ],
    )
    write_csv(
        HERE / "square-function-data.csv",
        [
            "number_of_scales_N",
            "source_weighted_increment",
            "source_weighted_sum",
            "source_cauchy_factor",
            "core_dual_increment_comparator",
            "core_dual_sum_comparator",
            "core_dual_cauchy_factor_comparator",
        ],
        [
            (
                int(n_value),
                source_step,
                source_sum,
                source_root,
                core_step,
                core_sum,
                core_root,
            )
            for (
                n_value,
                source_step,
                source_sum,
                source_root,
                core_step,
                core_sum,
                core_root,
            ) in zip(
                square_count,
                source_increment,
                source_weighted_sum,
                source_factor,
                core_dual_increment,
                core_dual_sum,
                core_dual_factor,
            )
        ],
    )

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 86 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.068,
            right=0.985,
            bottom=0.205,
            top=0.755,
            width_ratios=(0.88, 1.13, 1.08),
            wspace=0.35,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Adjacent-scale transport of fixed-annulus jets",
            x=0.045,
            y=0.955,
            ha="left",
            fontsize=8.2,
            color=INK,
        )
        figure.text(
            0.045,
            0.887,
            "exact dyadic coefficients  ·  signed recurrence comparator  ·  source/core square-function split",
            ha="left",
            fontsize=4.2,
            color=MUTED,
        )
        blossom(figure)

        # Panel A: lollipop comparison.
        axis_a.vlines(order, 0.0, transport, color=BLUE, linewidth=1.2)
        axis_a.scatter(
            order,
            transport,
            s=25,
            marker="o",
            facecolor=WHITE,
            edgecolor=BLUE,
            linewidth=0.9,
            zorder=3,
        )
        fractions = [r"$1/4$", r"$1/8$", r"$1/16$"]
        for x_value, y_value, fraction, reciprocal in zip(
            order, transport, fractions, dual_dilation
        ):
            axis_a.text(
                x_value,
                y_value + 0.014,
                fraction,
                ha="center",
                va="bottom",
                color=INK,
                fontsize=5.7,
            )
            axis_a.text(
                x_value,
                0.018,
                f"dual ×{int(reciprocal)}",
                ha="center",
                va="bottom",
                color=MUTED,
                fontsize=4.3,
            )
        axis_a.set_title("A  Critical dilation coefficients", loc="left", pad=5)
        axis_a.set_xlim(-0.45, 2.45)
        axis_a.set_ylim(0.0, 0.34)
        axis_a.set_xticks(order, ["0\nconstant", "1\nlinear", "2\nquadratic"])
        axis_a.set_yticks([0.0, 0.125, 0.25], ["0", "1/8", "1/4"])
        axis_a.set_xlabel(r"jet order $n$")
        axis_a.set_ylabel(r"transport coefficient $2^{-(n+2)}$")
        axis_a.grid(axis="y", color=GRID, linewidth=0.35)
        axis_a.text(
            0.02,
            0.95,
            r"$\widehat{J}_j^{(n)}=\widehat{P}_j^{(n)}$"
            "\n"
            r"$\qquad-\lambda_n\widehat{P}_{j-1}^{(n)}$",
            transform=axis_a.transAxes,
            ha="left",
            va="top",
            fontsize=4.8,
            color=MUTED,
        )

        # Panel B: raw recurrence versus ordinary differences.
        axis_b.axhspan(0.0, 1.0, color=PALE_BLUE, alpha=0.72, linewidth=0.0)
        axis_b.plot(
            count,
            raw_mass,
            color=RUST,
            linewidth=1.2,
            marker="D",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.4,
            markevery=7,
            label=r"raw $\sum_{j\leq N}p_j$",
        )
        axis_b.plot(
            count,
            difference_mass,
            color=BLUE,
            linewidth=1.15,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.7,
            markersize=2.6,
            markevery=7,
            label=r"$\sum_{j\leq N}\Delta p_j=p_N$",
        )
        axis_b.set_title("B  Constant coefficient recurrence", loc="left", pad=5)
        axis_b.set_xlim(1, 40)
        axis_b.set_ylim(0.0, 41.0)
        axis_b.set_xticks([1, 10, 20, 30, 40])
        axis_b.set_yticks([0, 10, 20, 30, 40])
        axis_b.set_xlabel(r"number of scales $N$")
        axis_b.set_ylabel("cumulative comparator")
        axis_b.grid(color=GRID, linewidth=0.35)
        axis_b.legend(loc="upper left", frameon=False, fontsize=4.7)
        axis_b.text(
            39.1,
            raw_mass[-1] - 1.2,
            r"$N-1+2^{-N}$",
            ha="right",
            va="top",
            color=RUST,
            fontsize=5.0,
        )
        axis_b.text(
            23.0,
            2.4,
            r"signed endpoint $p_N<1$",
            ha="left",
            va="bottom",
            color=BLUE,
            fontsize=4.7,
        )
        inset = axis_b.inset_axes([0.55, 0.34, 0.40, 0.31])
        inset.semilogy(
            count[:12],
            ordinary_increment[:12],
            color=BLUE,
            linewidth=0.9,
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.5,
            markersize=1.8,
        )
        inset.set_facecolor(WHITE)
        inset.set_xlim(1, 12)
        inset.set_xticks([1, 6, 12])
        inset.set_yticks([2.0**-1, 2.0**-6, 2.0**-12])
        inset.set_yticklabels([r"$2^{-1}$", r"$2^{-6}$", r"$2^{-12}$"])
        inset.minorticks_off()
        inset.set_title(r"$\Delta p_j=2^{-j}$", fontsize=4.2, pad=2)
        inset.tick_params(labelsize=3.5, pad=1)
        inset.grid(color=GRID, linewidth=0.25)

        # Panel C: source coefficient control versus the dual requirement.
        axis_c.axhspan(0.0, 1.0, color=PALE_BLUE, alpha=0.72, linewidth=0.0)
        axis_c.plot(
            square_count,
            source_factor,
            color=BLUE,
            linewidth=1.2,
            marker="o",
            markerfacecolor=BLUE,
            markeredgewidth=0.0,
            markersize=2.4,
            markevery=5,
            label=r"source factor $\sqrt{1-2^{-N}}$",
        )
        axis_c.plot(
            square_count,
            core_dual_factor,
            color=RUST,
            linewidth=1.15,
            linestyle="--",
            marker="s",
            markerfacecolor=WHITE,
            markeredgecolor=RUST,
            markeredgewidth=0.7,
            markersize=2.5,
            markevery=5,
            label=r"dual comparator $\sqrt{N}$",
        )
        axis_c.set_title("C  Square-function factors", loc="left", pad=5)
        axis_c.set_xlim(1, 32)
        axis_c.set_ylim(0.0, 6.2)
        axis_c.set_xticks([1, 8, 16, 24, 32])
        axis_c.set_yticks([0, 1, 2, 3, 4, 5, 6])
        axis_c.set_xlabel(r"number of scales $N$")
        axis_c.set_ylabel("Cauchy factor")
        axis_c.grid(color=GRID, linewidth=0.35)
        axis_c.legend(loc="upper left", frameon=False, fontsize=4.65)
        axis_c.text(
            31.3,
            source_factor[-1] + 0.18,
            "source side bounded",
            ha="right",
            va="bottom",
            color=BLUE,
            fontsize=4.7,
        )
        axis_c.text(
            31.3,
            4.95,
            "extra core input required",
            ha="right",
            va="top",
            color=RUST,
            fontsize=4.7,
        )

        figure.text(
            0.985,
            0.035,
            "closed-form analytic comparators — not simulation or a positive-part packing theorem",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.4,
        )

        figure.savefig(
            HERE / "figure.pdf",
            metadata={
                "Title": "Adjacent-scale transport of fixed-annulus jets",
                "Author": "R0.70G analytic figure package",
                "Subject": "Critical dilation, signed differences, and square-function inputs",
                "Creator": "plot.py",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": "Adjacent-scale transport of fixed-annulus jets",
                "Description": "Exact analytic comparators; not simulation evidence.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": "Adjacent-scale transport of fixed-annulus jets",
                "Description": "Exact analytic comparators; not simulation evidence.",
                "Software": "Matplotlib",
            },
        )
        plt.close(figure)

    normalize_svg(HERE / "figure.svg")

    image = Image.open(HERE / "figure.png")
    embedded_dpi = image.info.get("dpi", (None, None))
    output_checks = {
        "pngPixelDimensionsPositive": bool(image.width > 0 and image.height > 0),
        "pngRequestedDpiEmbedded": bool(
            embedded_dpi[0] is not None
            and embedded_dpi[1] is not None
            and abs(float(embedded_dpi[0]) - 600.0) < 0.1
            and abs(float(embedded_dpi[1]) - 600.0) < 0.1
        ),
        "pdfNonempty": bool((HERE / "figure.pdf").stat().st_size > 10_000),
        "svgNonempty": bool((HERE / "figure.svg").stat().st_size > 10_000),
    }
    checks.update(output_checks)
    if not all(checks.values()):
        raise AssertionError(checks)

    validation = {
        "status": "passed",
        "release": RELEASE,
        "checks": checks,
        "diagnostics": {
            "transportCoefficients": transport.tolist(),
            "dualDilationFactors": dual_dilation.tolist(),
            "rawMassAtN40": float(raw_mass[-1]),
            "differenceMassAtN40": float(difference_mass[-1]),
            "sourceFactorAtN32": float(source_factor[-1]),
            "coreDualComparatorAtN32": float(core_dual_factor[-1]),
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [
                float(embedded_dpi[0]),
                float(embedded_dpi[1]),
            ],
        },
        "claimBoundary": (
            "Closed-form critical-transport and square-function comparators; "
            "not simulation, a physical core-moment model, or a positive-part "
            "Navier--Stokes packing theorem."
        ),
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    payloads = [
        "critical-transport-data.csv",
        "constant-recurrence-data.csv",
        "square-function-data.csv",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "explanatory",
        "release": RELEASE,
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
        "png": {
            "pixels": [image.width, image.height],
            "requestedDpi": 600,
            "embeddedDpi": [
                float(embedded_dpi[0]),
                float(embedded_dpi[1]),
            ],
        },
        "runtime": {
            "python": platform.python_version(),
            "numpy": np.__version__,
            "matplotlib": matplotlib.__version__,
            "elapsedSeconds": time.perf_counter() - started,
        },
        "claimBoundary": (
            "Analytic critical transport, recurrence, and square-function "
            "comparators; not simulation evidence or a numerical PDE proof."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
