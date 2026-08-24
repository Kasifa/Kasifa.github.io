#!/usr/bin/env python3
"""Render the journal-style analytic figure for R0.70H.

Every plotted value evaluates an exact closed recurrence or scale weight.
The Lambda=2 choice is an algebraic diagnostic only: it is not an NSE
trajectory and does not validate the R0.70F support geometry.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
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
FIGURE_ID = "fig-r070h-core-moment-gap"
RELEASE = "R0.70H"

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


def write_csv(
    path: Path,
    header: list[str],
    rows: list[tuple[object, ...]],
) -> None:
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(header)
        for row in rows:
            rendered: list[object] = []
            for value in row:
                if value is None:
                    rendered.append("")
                elif isinstance(value, (float, np.floating)):
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
    center = (0.968, 0.945)
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


def g_value(index: np.ndarray | int, q: float) -> np.ndarray:
    values = np.asarray(index, dtype=float)
    return ((1.0 - q**values) / (1.0 - q)) ** 2


def ordinary_increment(index: np.ndarray, q: float) -> np.ndarray:
    q_power = q**index
    return (2.0 * q_power - (1.0 + q) * q_power**2) / (1.0 - q)


def pairing_increment(
    index: np.ndarray,
    q: float,
    transport: float,
) -> np.ndarray:
    q_power = q**index
    return (
        (1.0 - transport)
        - 2.0 * (1.0 - transport * q) * q_power
        + (1.0 - transport * q**2) * q_power**2
    ) / (1.0 - q) ** 2


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))

    lambda_base = 2.0
    rho = lambda_base**-2
    q = lambda_base**-4
    transport_zero = rho**2
    transport_one = rho**3

    # One wide analytic table supports all panels.
    scale_index = np.arange(0, 41, dtype=int)
    positive_index = scale_index[1:]
    b_all = (1.0 - q**scale_index) / (1.0 - q)
    g_all = b_all**2
    ordinary_steps = ordinary_increment(positive_index, q)
    pairing_zero_steps = pairing_increment(positive_index, q, transport_zero)
    pairing_one_steps = pairing_increment(positive_index, q, transport_one)

    number_of_scales = np.arange(1, 41, dtype=int)
    ordinary_total_variation = g_all[1:] - 1.0
    pairing_l1_mass = np.concatenate(
        ([0.0], np.cumsum(pairing_zero_steps[:-1]))
    )
    pairing_square_mass = np.concatenate(
        ([0.0], np.cumsum(pairing_zero_steps[:-1] ** 2))
    )

    radius = rho**scale_index
    spacetime_coordinate_weight = radius**-2
    spacetime_dual_weight = radius**-3

    rows: list[tuple[object, ...]] = []
    for index in scale_index:
        if index == 0:
            panels = "C"
        elif index <= 8:
            panels = "A;B;C"
        elif index <= 12:
            panels = "A;B"
        else:
            panels = "B"
        rows.append(
            (
                int(index),
                int(index) if index >= 1 else None,
                lambda_base,
                rho,
                q,
                b_all[index] if index >= 1 else None,
                g_all[index] if index >= 1 else None,
                ordinary_steps[index - 1] if index >= 1 else None,
                pairing_zero_steps[index - 1] if index >= 1 else None,
                pairing_one_steps[index - 1] if index >= 1 else None,
                ordinary_total_variation[index - 1] if index >= 1 else None,
                pairing_l1_mass[index - 1] if index >= 1 else None,
                pairing_square_mass[index - 1] if index >= 1 else None,
                radius[index],
                spacetime_coordinate_weight[index],
                spacetime_dual_weight[index],
                panels,
            )
        )

    write_csv(
        HERE / "data.csv",
        [
            "scale_index_k",
            "number_of_active_scales_N",
            "Lambda",
            "rho_Lambda_minus_2",
            "q_Lambda_minus_4",
            "b_k",
            "g_k_b_k_squared",
            "ordinary_increment_g_k_plus_1_minus_g_k",
            "pairing_covariant_increment_degree_0",
            "pairing_covariant_increment_degree_1",
            "ordinary_total_variation_through_N",
            "pairing_l1_mass_degree_0_through_N",
            "pairing_square_mass_degree_0_through_N",
            "r_k_with_r_0_equal_1",
            "spacetime_coordinate_weight_r_k_minus_2",
            "spacetime_dual_weight_r_k_minus_3",
            "panels_using_row",
        ],
        rows,
    )

    ordinary_limit = (1.0 - q) ** -2 - 1.0
    pairing_zero_limit = (1.0 - transport_zero) / (1.0 - q) ** 2
    pairing_one_limit = (1.0 - transport_one) / (1.0 - q) ** 2
    pairing_zero_lower = 1.0 - transport_zero / (1.0 - q) ** 2
    pairing_one_lower = 1.0 - transport_one / (1.0 - q) ** 2

    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "lambdaTwoParametersExact": bool(
            rho == 0.25
            and q == 0.0625
            and transport_zero == 0.0625
            and transport_one == 0.015625
        ),
        "ordinaryIncrementClosedForm": bool(
            np.allclose(
                ordinary_steps[:12],
                g_value(np.arange(2, 14), q) - g_value(np.arange(1, 13), q),
                rtol=1.0e-12,
                atol=1.0e-15,
            )
        ),
        "ordinaryIncrementPositiveAndDecaying": bool(
            np.all(ordinary_steps > 0.0) and np.all(np.diff(ordinary_steps) < 0.0)
        ),
        "pairingIncrementsStayPositive": bool(
            np.all(pairing_zero_steps >= pairing_zero_lower)
            and np.all(pairing_one_steps >= pairing_one_lower)
            and pairing_zero_lower > 0.0
            and pairing_one_lower > 0.0
        ),
        "ordinaryVariationSaturates": bool(
            np.all(ordinary_total_variation >= 0.0)
            and np.all(ordinary_total_variation <= ordinary_limit + 2.0e-15)
            and abs(ordinary_total_variation[-1] - ordinary_limit) < 2.0e-15
        ),
        "pairingL1MassHasLinearLowerBound": bool(
            np.all(
                pairing_l1_mass
                >= (number_of_scales - 1) * pairing_zero_lower - 2.0e-14
            )
        ),
        "pairingSquareMassHasLinearLowerBound": bool(
            np.all(
                pairing_square_mass
                >= (number_of_scales - 1) * pairing_zero_lower**2 - 2.0e-14
            )
        ),
        "spacetimeWeightsExact": bool(
            np.array_equal(spacetime_coordinate_weight[1:9] / spacetime_coordinate_weight[:8], np.full(8, 16.0))
            and np.array_equal(spacetime_dual_weight[1:9] / spacetime_dual_weight[:8], np.full(8, 64.0))
            and np.all(spacetime_dual_weight[1:9] > spacetime_coordinate_weight[1:9])
        ),
        "dataRowCount": len(rows) == 41,
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    panel_a_index = np.arange(1, 13, dtype=int)
    panel_b_count = number_of_scales
    panel_c_index = np.arange(0, 9, dtype=int)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 94 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.083,
            right=0.985,
            bottom=0.205,
            top=0.715,
            width_ratios=(1.03, 1.15, 1.00),
            wspace=0.34,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Core-moment variation and the spacetime dual gap",
            x=0.045,
            y=0.966,
            ha="left",
            fontsize=8.3,
            color=INK,
        )
        figure.text(
            0.045,
            0.912,
            r"closed recurrence $b_k=(1-16^{-k})/(1-16^{-1})$  ·  instantaneous pairing  ·  actual spacetime weight",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        figure.text(
            0.045,
            0.840,
            "ALGEBRAIC DIAGNOSTIC  /  NOT AN NSE TRAJECTORY  /  Λ=2 DOES NOT VALIDATE R0.70F GEOMETRY",
            ha="left",
            va="center",
            fontsize=4.65,
            color=RUST,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.28",
                "facecolor": PALE_RUST,
                "edgecolor": RUST,
                "linewidth": 0.45,
            },
        )
        blossom(figure)

        # Panel A: ordinary versus pairing-covariant adjacent increments.
        axis_a.semilogy(
            panel_a_index,
            ordinary_steps[:12],
            color=BLUE,
            linewidth=1.15,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.7,
            markersize=2.7,
            label=r"ordinary $g_{k+1}-g_k$",
        )
        axis_a.semilogy(
            panel_a_index,
            pairing_zero_steps[:12],
            color=RUST,
            linewidth=1.2,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.5,
            label=r"pairing $n=0$: $g_k-\rho^2g_{k+1}$",
        )
        axis_a.semilogy(
            panel_a_index,
            pairing_one_steps[:12],
            color=RUST,
            linewidth=1.0,
            linestyle=":",
            marker="^",
            markerfacecolor=WHITE,
            markeredgecolor=RUST,
            markeredgewidth=0.65,
            markersize=2.7,
            label=r"pairing $n=1$: $g_k-\rho^3g_{k+1}$",
        )
        axis_a.set_title("A  Adjacent increments", loc="left", pad=5)
        axis_a.set_xlim(1, 12)
        axis_a.set_ylim(1.0e-15, 2.1)
        axis_a.set_xticks([1, 4, 8, 12])
        axis_a.set_yticks(
            [1.0e-15, 1.0e-10, 1.0e-5, 1.0],
            [r"$10^{-15}$", r"$10^{-10}$", r"$10^{-5}$", r"$1$"],
        )
        axis_a.set_xlabel(r"active-scale index $k$")
        axis_a.set_ylabel("increment magnitude (log)", labelpad=1.0)
        axis_a.grid(color=GRID, linewidth=0.35, which="major")
        axis_a.legend(loc="lower left", frameon=False, fontsize=4.25)
        axis_a.text(
            11.65,
            3.5e-13,
            "ordinary → 0",
            ha="right",
            va="bottom",
            fontsize=4.6,
            color=BLUE,
        )
        axis_a.text(
            11.65,
            1.43,
            "pairing baseline persists",
            ha="right",
            va="bottom",
            fontsize=4.55,
            color=RUST,
        )

        # Panel B: cumulative pairing mass and the bounded ordinary inset.
        axis_b.plot(
            panel_b_count,
            pairing_l1_mass,
            color=RUST,
            linewidth=1.2,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.4,
            markevery=7,
            label=r"pairing $\ell^1$: $\sum|D_k|$",
        )
        axis_b.plot(
            panel_b_count,
            pairing_square_mass,
            color=RUST,
            linewidth=1.05,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=RUST,
            markeredgewidth=0.65,
            markersize=2.5,
            markevery=7,
            label=r"pairing square: $\sum|D_k|^2$",
        )
        axis_b.set_title("B  Cumulative scale mass", loc="left", pad=5)
        axis_b.set_xlim(1, 40)
        axis_b.set_ylim(0.0, max(pairing_square_mass[-1], pairing_l1_mass[-1]) * 1.12)
        axis_b.set_xticks([1, 10, 20, 30, 40])
        axis_b.set_xlabel(r"number of active scales $N$")
        axis_b.set_ylabel("pairing-covariant mass")
        axis_b.grid(color=GRID, linewidth=0.35)
        axis_b.legend(loc="lower right", frameon=False, fontsize=4.45)
        axis_b.text(
            39.0,
            pairing_square_mass[-1] + 1.1,
            "linear growth",
            ha="right",
            va="bottom",
            fontsize=4.7,
            color=RUST,
        )

        inset = axis_b.inset_axes([0.10, 0.55, 0.43, 0.35])
        inset.plot(
            panel_b_count[:16],
            ordinary_total_variation[:16],
            color=BLUE,
            linewidth=1.0,
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.55,
            markersize=2.0,
        )
        inset.axhline(
            ordinary_limit,
            color=BLUE,
            linewidth=0.65,
            linestyle=":",
        )
        inset.set_xlim(1, 16)
        inset.set_ylim(0.0, 0.15)
        inset.set_xticks([1, 8, 16])
        inset.set_yticks([0.0, ordinary_limit], ["0", r"$31/225$"])
        inset.set_title("ordinary total variation saturates", fontsize=4.1, pad=2)
        inset.tick_params(labelsize=3.5, pad=1)
        inset.grid(color=GRID, linewidth=0.25)

        # Panel C: the actual spacetime coordinate and dual weight.
        axis_c.set_yscale("log", base=2)
        axis_c.plot(
            panel_c_index,
            spacetime_coordinate_weight[:9],
            color=BLUE,
            linewidth=1.05,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.7,
            markersize=2.7,
            label=r"coordinate $r_k^{-2}=2^{4k}$",
        )
        axis_c.plot(
            panel_c_index,
            spacetime_dual_weight[:9],
            color=RUST,
            linewidth=1.25,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.6,
            label=r"dual weight $r_k^{-3}=2^{6k}$",
        )
        axis_c.set_title("C  Spacetime dual weight", loc="left", pad=5)
        axis_c.set_xlim(0, 8)
        axis_c.set_ylim(1.0, 2.0**50)
        axis_c.set_xticks([0, 2, 4, 6, 8])
        weight_exponents = np.array([0, 12, 24, 36, 48], dtype=int)
        axis_c.set_yticks(
            2.0**weight_exponents,
            [rf"$2^{{{exponent}}}$" for exponent in weight_exponents],
        )
        axis_c.set_xlabel(r"fine-scale index $k$ ($r_k=4^{-k}$)")
        axis_c.set_ylabel("scale weight (base-2 log)")
        axis_c.grid(color=GRID, linewidth=0.35, which="major")
        axis_c.legend(loc="lower right", frameon=False, fontsize=4.45)
        axis_c.text(
            0.04,
            0.95,
            r"$r_k^{-3}=r_k^{-2}\times r_k^{-1}$",
            transform=axis_c.transAxes,
            ha="left",
            va="top",
            color=RUST,
            fontsize=4.8,
        )
        axis_c.annotate(
            "extra dual amplification",
            xy=(6, spacetime_dual_weight[6]),
            xytext=(3.0, 2.0**41),
            color=RUST,
            fontsize=4.45,
            arrowprops={
                "arrowstyle": "->",
                "color": RUST,
                "linewidth": 0.55,
                "shrinkA": 1,
                "shrinkB": 2,
            },
        )

        figure.text(
            0.985,
            0.035,
            "closed-form R0.70H comparators — not simulation, nonlinear persistence, or a numerical PDE result",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.35,
        )

        figure.savefig(
            HERE / "figure.pdf",
            metadata={
                "Title": "Core-moment variation and the spacetime dual gap",
                "Author": "R0.70H analytic figure package",
                "Subject": "Ordinary variation, pairing covariance, and spacetime weights",
                "Creator": "plot.py",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": "Core-moment variation and the spacetime dual gap",
                "Description": "Algebraic diagnostic at Lambda=2; not an NSE trajectory.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": "Core-moment variation and the spacetime dual gap",
                "Description": "Algebraic diagnostic at Lambda=2; not an NSE trajectory.",
                "Software": "Matplotlib",
            },
        )
        plt.close(figure)

    normalize_svg(HERE / "figure.svg")

    image = Image.open(HERE / "figure.png")
    embedded_dpi = image.info.get("dpi", (None, None))
    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    with (HERE / "data.csv").open(newline="", encoding="utf-8") as stream:
        data_row_count = sum(1 for _ in csv.DictReader(stream))

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
        "visibleClaimBoundaryInSvg": bool(
            "ALGEBRAIC DIAGNOSTIC" in svg_text
            and "NOT AN NSE TRAJECTORY" in svg_text
            and "DOES NOT VALIDATE R0.70F GEOMETRY" in svg_text
        ),
        "writtenDataRowCount": data_row_count == 41,
    }
    checks.update(output_checks)
    if not all(checks.values()):
        raise AssertionError(checks)

    validation = {
        "status": "passed",
        "release": RELEASE,
        "checks": checks,
        "diagnostics": {
            "Lambda": lambda_base,
            "rho": rho,
            "q": q,
            "ordinaryIncrementAtK1": float(ordinary_steps[0]),
            "ordinaryIncrementAtK12": float(ordinary_steps[11]),
            "pairingDegree0Limit": pairing_zero_limit,
            "pairingDegree1Limit": pairing_one_limit,
            "ordinaryVariationAtN40": float(ordinary_total_variation[-1]),
            "ordinaryVariationLimit": ordinary_limit,
            "pairingL1MassAtN40": float(pairing_l1_mass[-1]),
            "pairingSquareMassAtN40": float(pairing_square_mass[-1]),
            "spacetimeCoordinateWeightAtK8": float(spacetime_coordinate_weight[8]),
            "spacetimeDualWeightAtK8": float(spacetime_dual_weight[8]),
            "dataRows": data_row_count,
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [
                float(embedded_dpi[0]),
                float(embedded_dpi[1]),
            ],
        },
        "claimBoundary": (
            "Closed-form algebraic diagnostics only; not simulation evidence or a "
            "numerical PDE proof.  Lambda=2 is not an NSE trajectory and does not "
            "validate the R0.70F compact support geometry."
        ),
    }
    (HERE / "validation.json").write_text(
        json.dumps(validation, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    payloads = [
        "contract.json",
        "figure-contract.md",
        "caption.md",
        "data.csv",
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
        },
        "claimBoundary": (
            "Algebraic R0.70H recurrence and spacetime-weight diagnostics; "
            "not simulation evidence or a numerical PDE proof; not an NSE "
            "trajectory or a geometry certificate."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
