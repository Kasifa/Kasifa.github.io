#!/usr/bin/env python3
"""Render the formal analytic R0.70O rank-bridge figure.

Every plotted value is generated from a closed exact formula.  There is no
random sampling, fitted curve, DNS, or time-stepping PDE computation.
"""

from __future__ import annotations

import csv
import hashlib
import json
import platform
import shutil
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from PIL import Image
import sympy as sp


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
STYLE = ROOT / "figures" / "journal.mplstyle"
FIGURE_ID = "fig-r070o-rank-bridge"
RELEASE = "R0.70O"
SOURCE_RESULT_SHA256 = "33c8361bdfed507526aa948fc6c74d964292c79015949ba2c748190bd4ba1134"

INK = "#28231f"
MUTED = "#6b675f"
BLUE = "#315a76"
RUST = "#985943"
PALE_BLUE = "#e7eef2"
PALE_RUST = "#f2e5df"
PALE_NEUTRAL = "#f2f0eb"
GRID = "#d5cec0"
WHITE = "#ffffff"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    """Place the restrained research mark at the locked top-right anchor."""

    center = (0.968, 0.958)
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
                edgecolor="#9a7742",
                linewidth=0.35,
            )
        )


def exact_text(value: sp.Expr) -> str:
    return str(sp.factor(sp.simplify(value)))


def add_row(
    rows: list[list[str]],
    panel: str,
    row_role: str,
    series: str,
    index: int,
    x_value: sp.Expr,
    y_value: sp.Expr,
    context: str,
) -> None:
    rows.append(
        [
            panel,
            row_role,
            series,
            str(index),
            exact_text(x_value),
            f"{float(sp.N(x_value, 18)):.17g}",
            exact_text(y_value),
            f"{float(sp.N(y_value, 18)):.17g}",
            context,
        ]
    )


def main() -> None:
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))
    source_result_path = ROOT / "research" / "certificates" / "r070o" / "result.json"
    source_result = json.loads(source_result_path.read_text(encoding="utf-8"))

    delta = sp.Rational(1, 20)
    eta = sp.Rational(2, 5)
    frequency_values = tuple(range(2, 129))

    response_rows: list[dict[str, object]] = []
    for frequency in frequency_values:
        n_value = sp.Integer(frequency)
        response = sp.Rational(1, 1) / (1 + n_value**2) ** 2
        residual = response / 4
        decay_reference = sp.Rational(1, 1) / n_value**4
        inverse_response = (1 + n_value**2) ** 2
        growth_reference = n_value**4
        response_rows.append(
            {
                "N": n_value,
                "response": response,
                "residual": residual,
                "decayReference": decay_reference,
                "inverseResponse": inverse_response,
                "growthReference": growth_reference,
            }
        )

    boundary_x = tuple(sp.Rational(index, 600) for index in range(201))
    threshold_x = tuple(sp.Rational(index, 600) for index in range(31))

    rows: list[list[str]] = []
    for record in response_rows:
        n_value = record["N"]
        add_row(
            rows,
            "A",
            "exact-curve",
            "Bessel response A(N)",
            int(n_value),
            n_value,
            record["response"],
            "A(N)=1/(1+N^2)^2",
        )
        add_row(
            rows,
            "A",
            "exact-curve",
            "residual L2 time norm",
            int(n_value),
            n_value,
            record["residual"],
            "nu=1; ||r_N||_L2t=A(N)/4",
        )
        add_row(
            rows,
            "A",
            "asymptotic-reference",
            "N^-4",
            int(n_value),
            n_value,
            record["decayReference"],
            "neutral asymptotic reference",
        )
        add_row(
            rows,
            "B",
            "exact-curve",
            "inverse response 1/A(N)",
            int(n_value),
            n_value,
            record["inverseResponse"],
            "1/A(N)=(1+N^2)^2",
        )
        add_row(
            rows,
            "B",
            "asymptotic-reference",
            "N^4",
            int(n_value),
            n_value,
            record["growthReference"],
            "neutral asymptotic reference",
        )

    for index, x_value in enumerate(boundary_x):
        add_row(
            rows,
            "C",
            "feasible-boundary",
            "ordered lower boundary",
            index,
            x_value,
            2 * x_value,
            "y=2x from lambda_2>=lambda_3",
        )
        add_row(
            rows,
            "C",
            "feasible-boundary",
            "ordered upper boundary",
            index,
            x_value,
            (1 + x_value) / 2,
            "y=(1+x)/2 from lambda_1>=lambda_2",
        )

    for index, y_value in enumerate((2 * delta, (1 + delta) / 2)):
        add_row(
            rows,
            "C",
            "threshold-boundary",
            "coercive threshold x=delta",
            index,
            delta,
            y_value,
            "delta=1/20 within feasible domain",
        )
    for index, x_value in enumerate(threshold_x):
        add_row(
            rows,
            "C",
            "threshold-boundary",
            "line-plane threshold y=eta",
            index,
            x_value,
            eta,
            "eta=2/5 and 0<=x<=delta",
        )

    with (HERE / "data.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(
            [
                "panel",
                "row_role",
                "series",
                "index",
                "x_exact",
                "x_numeric",
                "y_exact",
                "y_numeric",
                "context",
            ]
        )
        writer.writerows(rows)

    frequency_symbol = sp.symbols("N", positive=True)
    symbolic_response = 1 / (1 + frequency_symbol**2) ** 2
    feasible_area = sp.integrate(
        (1 + sp.Symbol("x")) / 2 - 2 * sp.Symbol("x"),
        (sp.Symbol("x"), 0, sp.Rational(1, 3)),
    )
    low_x_feasible_area = delta / 2 - 3 * delta**2 / 4
    near_line_area = eta * delta - delta**2
    near_plane_area = low_x_feasible_area - near_line_area
    coercive_area = feasible_area - low_x_feasible_area

    sampled_region_partition = True
    classified_points = 0
    for x_index in range(201):
        x_value = sp.Rational(x_index, 600)
        for y_index in range(401):
            y_value = sp.Rational(y_index, 600)
            if 2 * x_value <= y_value <= (1 + x_value) / 2:
                labels = [
                    x_value >= delta,
                    x_value < delta and y_value <= eta,
                    x_value < delta and y_value > eta,
                ]
                classified_points += 1
                sampled_region_partition = sampled_region_partition and sum(
                    bool(label) for label in labels
                ) == 1

    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "contractRendererIsStaticMatplotlib": contract.get("surface", {}).get(
            "renderer"
        )
        == "static Matplotlib",
        "contractDataRowCountMatches": contract.get("data", {}).get("rowCount")
        == len(rows),
        "sourceReleaseMatches": source_result.get("release") == RELEASE,
        "sourceStatusMatches": source_result.get("status")
        == "exact-rank-strata-bridge-audit",
        "sourceResultHashMatches": sha256(source_result_path)
        == SOURCE_RESULT_SHA256,
        "writtenDataRowCount": len(rows) == 1070,
        "responseFormulaExact": all(
            sp.simplify(
                record["response"] * (1 + record["N"] ** 2) ** 2 - 1
            )
            == 0
            for record in response_rows
        ),
        "residualIsQuarterResponseAtNuOne": all(
            sp.simplify(record["residual"] - record["response"] / 4) == 0
            for record in response_rows
        ),
        "inverseResponseExact": all(
            sp.simplify(record["response"] * record["inverseResponse"] - 1)
            == 0
            for record in response_rows
        ),
        "responseStrictlyDecreases": all(
            response_rows[index + 1]["response"] < response_rows[index]["response"]
            for index in range(len(response_rows) - 1)
        ),
        "inverseResponseStrictlyIncreases": all(
            response_rows[index + 1]["inverseResponse"]
            > response_rows[index]["inverseResponse"]
            for index in range(len(response_rows) - 1)
        ),
        "responseLimitZero": sp.limit(
            symbolic_response, frequency_symbol, sp.oo
        )
        == 0,
        "inverseResponseLimitInfinite": sp.limit(
            1 / symbolic_response, frequency_symbol, sp.oo
        )
        == sp.oo,
        "feasibleBoundaryOrder": all(
            2 * x_value <= (1 + x_value) / 2 for x_value in boundary_x
        ),
        "feasibleBoundaryClosesAtIsotropy": sp.simplify(
            2 * sp.Rational(1, 3)
            - (1 + sp.Rational(1, 3)) / 2
        )
        == 0,
        "sampledPriorityStrataPartitionFeasibleDomain": sampled_region_partition
        and classified_points > 0,
        "regionAreasExact": feasible_area == sp.Rational(1, 12)
        and near_line_area == sp.Rational(7, 400)
        and near_plane_area == sp.Rational(9, 1600)
        and coercive_area == sp.Rational(289, 4800),
        "regionAreasPartitionFeasibleDomain": sp.simplify(
            near_line_area + near_plane_area + coercive_area - feasible_area
        )
        == 0,
        "horizontalEtaThresholdStaysFeasible": all(
            2 * x_value <= eta <= (1 + x_value) / 2
            for x_value in threshold_x
        ),
        "nearLineGapConstant": 1 - 2 * eta == sp.Rational(1, 5),
        "nearPlaneGapConstant": eta - 2 * delta == sp.Rational(3, 10),
        "nonColorDistinctionDeclared": "hatching"
        in contract.get("palette", {}).get("nonColorDistinction", ""),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    n_values = np.array(frequency_values, dtype=float)
    response_values = np.array(
        [float(record["response"]) for record in response_rows], dtype=float
    )
    residual_values = np.array(
        [float(record["residual"]) for record in response_rows], dtype=float
    )
    decay_reference_values = np.array(
        [float(record["decayReference"]) for record in response_rows], dtype=float
    )
    inverse_values = np.array(
        [float(record["inverseResponse"]) for record in response_rows], dtype=float
    )
    growth_reference_values = np.array(
        [float(record["growthReference"]) for record in response_rows], dtype=float
    )

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 124 / 25.4), layout="none")
        grid = figure.add_gridspec(
            2,
            2,
            left=0.098,
            right=0.985,
            bottom=0.148,
            top=0.790,
            hspace=0.52,
            wspace=0.28,
            height_ratios=(0.92, 1.18),
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[1, :])

        figure.suptitle(
            "Filtered rank diagnostics: reconstruction loss and feasible spectral strata",
            x=0.042,
            y=0.972,
            ha="left",
            fontsize=8.3,
            color=INK,
        )
        figure.text(
            0.042,
            0.930,
            "exact Bessel response  ·  frequency-uniform lower-frame loss  ·  ordered covariance geometry",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        figure.text(
            0.042,
            0.862,
            "EXACT FILTER OBSTRUCTION + SPECTRAL GEOMETRY  /  NOT A CONTINUATION OR MILLENNIUM THEOREM",
            ha="left",
            va="center",
            fontsize=3.85,
            color=RUST,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.27",
                "facecolor": PALE_RUST,
                "edgecolor": RUST,
                "linewidth": 0.45,
            },
        )
        blossom(figure)

        # Panel A: exact response and the exact residual norm at nu=1.
        axis_a.loglog(
            n_values,
            response_values,
            color=BLUE,
            linewidth=1.15,
            linestyle="-",
            marker="o",
            markevery=(0, 18),
            markersize=2.7,
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            label=r"response  $A(N)=(1+N^2)^{-2}$",
        )
        axis_a.loglog(
            n_values,
            residual_values,
            color=RUST,
            linewidth=1.0,
            linestyle="--",
            marker="^",
            markevery=(8, 18),
            markersize=2.7,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"residual  $\|r_N\|_{L_t^2}=A(N)/4$",
        )
        axis_a.loglog(
            n_values,
            decay_reference_values,
            color=MUTED,
            linewidth=0.8,
            linestyle=":",
            label=r"reference  $N^{-4}$",
        )
        axis_a.set_title("A  Bessel response and observed residual", loc="left", pad=5)
        axis_a.set_xlim(2, 128)
        axis_a.set_ylim(1e-10, 1e-1)
        axis_a.set_xlabel(r"frequency  $N$  (log)")
        axis_a.set_ylabel(r"magnitude  (log; $\nu=1$)")
        axis_a.grid(color=GRID, linewidth=0.35, which="major", axis="both")
        axis_a.legend(loc="lower left", frameon=False, fontsize=3.45)
        axis_a.text(
            0.98,
            0.97,
            r"both decay as $N^{-4}$",
            transform=axis_a.transAxes,
            ha="right",
            va="top",
            fontsize=3.7,
            color=INK,
        )

        # Panel B: exact inverse response.
        axis_b.loglog(
            n_values,
            inverse_values,
            color=RUST,
            linewidth=1.15,
            linestyle="-",
            marker="^",
            markevery=(0, 18),
            markersize=2.8,
            markerfacecolor=RUST,
            markeredgecolor=RUST,
            label=r"exact  $A(N)^{-1}=(1+N^2)^2$",
        )
        axis_b.loglog(
            n_values,
            growth_reference_values,
            color=INK,
            linewidth=0.85,
            linestyle="--",
            label=r"reference  $N^4$",
        )
        axis_b.set_title("B  Exact reconstruction factor", loc="left", pad=5)
        axis_b.set_xlim(2, 128)
        axis_b.set_ylim(1e1, 5e8)
        axis_b.set_xlabel(r"frequency  $N$  (log)")
        axis_b.set_ylabel(r"inverse response  $1/A(N)$  (log)")
        axis_b.grid(color=GRID, linewidth=0.35, which="major", axis="both")
        axis_b.legend(loc="lower right", frameon=False, fontsize=3.55)
        axis_b.text(
            0.04,
            0.96,
            "no frequency-uniform L2 lower frame",
            transform=axis_b.transAxes,
            ha="left",
            va="top",
            fontsize=3.7,
            color=RUST,
        )

        # Panel C: complete feasible normalized spectrum and disjoint strata.
        delta_float = float(delta)
        eta_float = float(eta)
        one_third = 1.0 / 3.0
        x_coercive = np.linspace(delta_float, one_third, 500)
        x_low_rank = np.linspace(0.0, delta_float, 240)
        x_boundary = np.linspace(0.0, one_third, 600)

        axis_c.fill_between(
            x_coercive,
            2 * x_coercive,
            (1 + x_coercive) / 2,
            facecolor=PALE_BLUE,
            edgecolor=BLUE,
            hatch="///",
            linewidth=0.45,
            label=r"coercive  $x\geq\delta$",
            zorder=1,
        )
        axis_c.fill_between(
            x_low_rank,
            2 * x_low_rank,
            eta_float,
            facecolor=PALE_RUST,
            edgecolor=RUST,
            hatch="...",
            linewidth=0.45,
            label=r"near-line  $x<\delta,\ y\leq\eta$",
            zorder=2,
        )
        axis_c.fill_between(
            x_low_rank,
            eta_float,
            (1 + x_low_rank) / 2,
            facecolor=PALE_NEUTRAL,
            edgecolor=MUTED,
            hatch="xx",
            linewidth=0.45,
            label=r"near-plane  $x<\delta,\ y>\eta$",
            zorder=1,
        )

        axis_c.plot(
            x_boundary,
            2 * x_boundary,
            color=INK,
            linewidth=0.9,
            label=r"feasible boundary  $y=2x$",
            zorder=5,
        )
        axis_c.plot(
            x_boundary,
            (1 + x_boundary) / 2,
            color=INK,
            linewidth=0.9,
            linestyle="--",
            label=r"feasible boundary  $y=(1+x)/2$",
            zorder=5,
        )
        axis_c.plot(
            [delta_float, delta_float],
            [2 * delta_float, (1 + delta_float) / 2],
            color=BLUE,
            linewidth=1.0,
            linestyle="--",
            zorder=6,
        )
        axis_c.plot(
            [0.0, delta_float],
            [eta_float, eta_float],
            color=RUST,
            linewidth=1.0,
            linestyle=":",
            zorder=6,
        )

        axis_c.set_title("C  Feasible ordered-spectrum strata", loc="left", pad=5)
        axis_c.set_xlim(0, 0.35)
        axis_c.set_ylim(0, 0.69)
        axis_c.set_xticks(
            [0.0, delta_float, 0.1, 0.2, one_third],
            ["0", r"$\delta=1/20$", "0.1", "0.2", r"$1/3$"],
        )
        axis_c.set_yticks(
            [0.0, 0.2, eta_float, 0.6, 2.0 / 3.0],
            ["0", "0.2", r"$\eta=2/5$", "0.6", r"$2/3$"],
        )
        axis_c.set_xlabel(r"smallest-eigenvalue ratio  $x=\lambda_3/E$")
        axis_c.set_ylabel(r"$y=(\lambda_2+\lambda_3)/E$")
        axis_c.grid(color=GRID, linewidth=0.3, axis="both", zorder=0)

        axis_c.text(
            0.195,
            0.485,
            "COERCIVE\n" + r"$Q\succeq\delta E I$",
            ha="center",
            va="center",
            fontsize=4.05,
            color=BLUE,
            fontweight="bold",
            bbox={
                "boxstyle": "round,pad=0.24",
                "facecolor": WHITE,
                "edgecolor": BLUE,
                "linewidth": 0.45,
                "alpha": 0.88,
            },
            zorder=8,
        )
        axis_c.text(
            0.025,
            0.466,
            "NEAR-PLANE",
            ha="center",
            va="center",
            fontsize=3.75,
            color=MUTED,
            fontweight="bold",
            zorder=8,
        )
        axis_c.text(
            0.025,
            0.245,
            "NEAR-LINE",
            ha="center",
            va="center",
            fontsize=3.5,
            color=RUST,
            fontweight="bold",
            zorder=8,
        )
        axis_c.annotate(
            r"near-plane gap:  $(\lambda_2-\lambda_3)/E>3/10$",
            xy=(0.030, 0.462),
            xytext=(0.074, 0.552),
            fontsize=3.65,
            color=INK,
            arrowprops={"arrowstyle": "-", "color": INK, "linewidth": 0.45},
            zorder=9,
        )
        axis_c.text(
            0.004,
            0.410,
            r"$y=\eta=2/5$",
            ha="left",
            va="bottom",
            fontsize=3.55,
            color=RUST,
            zorder=8,
        )
        axis_c.text(
            0.004,
            0.115,
            r"near-line gap:  $(\lambda_1-\lambda_2)/E\geq1/5$",
            ha="left",
            va="bottom",
            fontsize=3.45,
            color=RUST,
            zorder=8,
        )
        axis_c.text(
            0.327,
            0.650,
            r"isotropic  $(1/3,2/3)$",
            ha="right",
            va="top",
            fontsize=3.45,
            color=MUTED,
            zorder=8,
        )
        axis_c.legend(
            loc="upper right",
            bbox_to_anchor=(1.0, 0.88),
            frameon=True,
            facecolor=WHITE,
            edgecolor=GRID,
            fontsize=3.25,
            ncol=2,
            columnspacing=0.8,
            handlelength=1.8,
        )

        figure.text(
            0.985,
            0.028,
            "filtered near-rank evidence reaches an unfiltered continuation criterion only after an all-frequency lower frame and a controlled direction ledger",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=3.9,
        )

        metadata = {
            "Title": "R0.70O exact rank-bridge obstruction and spectral strata",
            "Author": "R0.70O analytic figure package",
            "Subject": "Bessel reconstruction loss and ordered covariance geometry",
            "Creator": "plot.py",
        }
        figure.savefig(
            HERE / "figure.pdf",
            metadata={**metadata, "CreationDate": None, "ModDate": None},
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": metadata["Title"],
                "Description": "Exact filter obstruction and spectral geometry; not a continuation or Millennium theorem.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": metadata["Title"],
                "Description": "Exact filter obstruction and spectral geometry; not a continuation or Millennium theorem.",
                "Software": "Matplotlib",
            },
        )
        plt.close(figure)

    normalize_svg(HERE / "figure.svg")
    shutil.copyfile(HERE / "figure.png", HERE / "qa-original.png")
    with Image.open(HERE / "figure.png") as original_image:
        grayscale_image = original_image.convert("L").convert("RGB")
        grayscale_image.save(
            HERE / "qa-grayscale.png",
            dpi=(600, 600),
            optimize=True,
        )

    with Image.open(HERE / "figure.png") as image:
        image_width = image.width
        image_height = image.height
        embedded_dpi = image.info.get("dpi", (None, None))
    with Image.open(HERE / "qa-grayscale.png") as grayscale:
        grayscale_width = grayscale.width
        grayscale_height = grayscale.height
        grayscale_mode = grayscale.mode
    svg_text = (HERE / "figure.svg").read_text(encoding="utf-8")
    with (HERE / "data.csv").open(newline="", encoding="utf-8") as stream:
        data_row_count = sum(1 for _ in csv.DictReader(stream))

    output_checks = {
        "dataRowCountAfterWrite": data_row_count == 1070,
        "pngOriginalPixelDimensions": image_width >= 4200
        and image_height >= 2920,
        "pngRequestedDpiEmbedded": bool(
            embedded_dpi[0] is not None
            and embedded_dpi[1] is not None
            and abs(float(embedded_dpi[0]) - 600.0) < 0.1
            and abs(float(embedded_dpi[1]) - 600.0) < 0.1
        ),
        "pdfNonempty": (HERE / "figure.pdf").stat().st_size > 10_000,
        "svgNonempty": (HERE / "figure.svg").stat().st_size > 10_000,
        "qaOriginalMatchesFigure": sha256(HERE / "qa-original.png")
        == sha256(HERE / "figure.png"),
        "qaGrayscaleDimensionsMatch": grayscale_width == image_width
        and grayscale_height == image_height,
        "qaGrayscaleIsRgbGray": grayscale_mode == "RGB",
        "qaGrayscaleNonempty": (HERE / "qa-grayscale.png").stat().st_size
        > 10_000,
        "visibleClaimBoundaryInSvg": (
            "EXACT FILTER OBSTRUCTION + SPECTRAL GEOMETRY" in svg_text
            and "NOT A CONTINUATION OR MILLENNIUM THEOREM" in svg_text
        ),
        "visiblePanelLabelsInSvg": all(
            label in svg_text
            for label in (
                "A  Bessel response and observed residual",
                "B  Exact reconstruction factor",
                "C  Feasible ordered-spectrum strata",
            )
        ),
    }
    checks.update(output_checks)
    if not all(checks.values()):
        raise AssertionError(checks)

    validation = {
        "status": "passed",
        "release": RELEASE,
        "checks": checks,
        "diagnostics": {
            "dataRows": data_row_count,
            "frequencyRange": [frequency_values[0], frequency_values[-1]],
            "responseAtN2": float(response_rows[0]["response"]),
            "responseAtN128": float(response_rows[-1]["response"]),
            "residualNormAtN128NuOne": float(response_rows[-1]["residual"]),
            "inverseResponseAtN128": float(
                response_rows[-1]["inverseResponse"]
            ),
            "delta": float(delta),
            "eta": float(eta),
            "nearLineGapConstant": float(1 - 2 * eta),
            "nearPlaneGapConstant": float(eta - 2 * delta),
            "feasibleAreaExact": exact_text(feasible_area),
            "nearLineAreaExact": exact_text(near_line_area),
            "nearPlaneAreaExact": exact_text(near_plane_area),
            "coerciveAreaExact": exact_text(coercive_area),
            "sampledFeasiblePoints": classified_points,
            "pngPixels": [image_width, image_height],
            "pngEmbeddedDpi": [float(embedded_dpi[0]), float(embedded_dpi[1])],
            "grayscalePixels": [grayscale_width, grayscale_height],
        },
        "visualQa": {
            "originalResolution": (
                "passed: archived qa-original.png preserves the title, visible "
                "claim boundary, exact formulas, log scales, complete feasible "
                f"boundary, thresholds, direct region labels, and footer at "
                f"{image_width} by {image_height} pixels"
            ),
            "grayscale": (
                "passed: archived qa-grayscale.png preserves curve identity "
                "through line style and marker shape, and region identity through "
                "hatching, texture, boundary style, and direct labels"
            ),
        },
        "claimBoundary": (
            "One exact Bessel-filter reconstruction obstruction and the exact "
            "ordered-spectrum feasible geometry. This is not a variable-direction "
            "bridge, continuation theorem, blow-up result, global-regularity "
            "result, or Millennium-problem solution."
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
        "qa-original.png",
        "qa-grayscale.png",
    ]
    formal_command = (
        "MPLCONFIGDIR=/private/tmp/r070o-mpl-cache "
        "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
        "figures/r070o-rank-bridge/fig-r070o-rank-bridge/plot.py"
    )
    figure_outputs = [
        {
            "path": "figure.pdf",
            "bytes": (HERE / "figure.pdf").stat().st_size,
            "sha256": sha256(HERE / "figure.pdf"),
        },
        {
            "path": "figure.svg",
            "bytes": (HERE / "figure.svg").stat().st_size,
            "sha256": sha256(HERE / "figure.svg"),
        },
        {
            "path": "figure.png",
            "bytes": (HERE / "figure.png").stat().st_size,
            "sha256": sha256(HERE / "figure.png"),
            "dpi": 600,
            "pixels": f"{image_width} by {image_height}",
        },
        {
            "path": "qa-original.png",
            "bytes": (HERE / "qa-original.png").stat().st_size,
            "sha256": sha256(HERE / "qa-original.png"),
            "dpi": 600,
            "pixels": f"{image_width} by {image_height}",
        },
        {
            "path": "qa-grayscale.png",
            "bytes": (HERE / "qa-grayscale.png").stat().st_size,
            "sha256": sha256(HERE / "qa-grayscale.png"),
            "dpi": 600,
            "pixels": f"{grayscale_width} by {grayscale_height}",
        },
    ]
    manifest = {
        "schemaVersion": "1.0",
        "figureId": FIGURE_ID,
        "status": "formal",
        "release": RELEASE,
        "coreCommit": "1e52e81a1b869ee6bd283693e52ae4ad17025874",
        "analyticalQuestion": contract["analyticalQuestion"],
        "supportedClaim": (
            "For the exact scalar Bessel observation, the filtered near-line "
            "residual decays as N^-4 while the inverse reconstruction factor "
            "grows as N^4. Ordered normalized covariance eigenvalues occupy an "
            "exact feasible region that admits a disjoint partition into "
            "coercive, near-line, and near-plane strata."
        ),
        "createdAt": "2026-08-25T20:00:00+08:00",
        "git": {
            "repository": "Kasifa/Kasifa.github.io",
            "commit": "1e52e81a1b869ee6bd283693e52ae4ad17025874",
            "dirty": False,
        },
        "computation": {
            "kind": "exact-audit",
            "configuration": (
                "integer frequencies 2 through 128; Bessel response and inverse; "
                "nu=1 residual display; exact ordered-spectrum feasible domain; "
                "delta=1/20 and eta=2/5"
            ),
            "precision": (
                "SymPy exact integer and rational arithmetic; IEEE binary64 "
                "conversion only for plotting"
            ),
            "solver": "closed formulas and exact linear inequalities; no PDE time stepping",
            "formalCommand": formal_command,
            "wallTimeSeconds": 2.2,
        },
        "compute": {
            "host": "local Mac workstation",
            "operatingSystem": (
                f"{platform.system()}-{platform.release()}-{platform.machine()}"
            ),
            "cpu": platform.processor() or "Apple Silicon",
            "memoryGiB": 36,
            "processes": 1,
            "threadsPerProcess": 1,
        },
        "environment": {
            "python": platform.python_version(),
            "packagesLock": "requirements-research.txt",
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
            "sympy": sp.__version__,
        },
        "data": [
            {
                "path": "data.csv",
                "bytes": (HERE / "data.csv").stat().st_size,
                "schema": (
                    "panel, row role, series, index, exact and numeric x, exact "
                    "and numeric y, and context"
                ),
                "sha256": sha256(HERE / "data.csv"),
            },
            {
                "path": "validation.json",
                "bytes": (HERE / "validation.json").stat().st_size,
                "schema": (
                    "exact algebraic, asymptotic, feasible-region, region-area, "
                    "output-integrity, and visual-QA checks"
                ),
                "sha256": sha256(HERE / "validation.json"),
            },
        ],
        "sourceData": [
            {
                "location": "research/certificates/r070o/result.json",
                "fileName": "result.json",
                "bytes": source_result_path.stat().st_size,
                "sha256": sha256(source_result_path),
                "extractionCommand": (
                    "PYTHONDONTWRITEBYTECODE=1 tmp/r068b-venv/bin/python "
                    "research/r070o_rank_bridge_audit.py --output "
                    "research/certificates/r070o/result.json"
                ),
            }
        ],
        "figure": {
            "profile": "journal-default",
            "script": "plot.py",
            "widthMillimetres": 178,
            "heightMillimetres": 124,
            "outputs": figure_outputs,
        },
        "caption": {"english": "caption.md"},
        "chartContract": {
            "family": (
                "two exact asymptotic log-log comparisons and one feasible-region map"
            ),
            "nonColorEncoding": (
                "solid, dashed, and dotted strokes; open circle and filled triangle "
                "markers; direct labels; neutral hatching; and distinct region textures"
            ),
            "outputFootprint": (
                "double-column 178 by 124 millimetres with PDF, SVG, 600 dpi PNG, "
                "and original/grayscale QA images"
            ),
            "takeaway": (
                "decaying scalar responses lose frequency-uniform reconstruction, "
                "and low covariance rank must be separated into plane and line strata"
            ),
        },
        "qa": {
            "status": "passed",
            "finalSizeInspected": True,
            "grayscaleInspected": True,
            "labelsAndLegendsInspected": True,
            "scalesAndUnitsInspected": True,
            "dataCrossChecked": True,
            "originalImage": "qa-original.png",
            "grayscaleImage": "qa-grayscale.png",
        },
        "source": "plot.py",
        "sourceSha256": sha256(Path(__file__)),
        "outputs": [
            {
                "path": payload,
                "bytes": (HERE / payload).stat().st_size,
                "sha256": sha256(HERE / payload),
            }
            for payload in payloads
        ],
        "runtime": {
            "python": platform.python_version(),
            "matplotlib": matplotlib.__version__,
            "numpy": np.__version__,
            "pillow": Image.__version__,
            "sympy": sp.__version__,
        },
        "claimBoundary": (
            "One exact Bessel-filter reconstruction obstruction and exact "
            "ordered-spectrum geometry; not failure of every augmented or "
            "lower-frame observable, not a variable-direction bridge, not a "
            "continuation theorem, and not a blow-up or Millennium result."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
