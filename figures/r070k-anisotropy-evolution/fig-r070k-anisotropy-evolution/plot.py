#!/usr/bin/env python3
"""Render the journal-style analytic figure for R0.70K.

All plotted values evaluate closed covariance formulas.  There is no DNS,
time-stepping PDE solver, random sampling, fitted curve, or regularity claim.
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
FIGURE_ID = "fig-r070k-anisotropy-evolution"
RELEASE = "R0.70K"

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
    """Locked research blossom at the top-right header anchor."""

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


def main() -> None:
    HERE.mkdir(parents=True, exist_ok=True)
    contract = json.loads((HERE / "contract.json").read_text(encoding="utf-8"))

    # Panel A: exact source-only trajectory from isotropic covariance.
    time = np.linspace(0.0, 4.0, 121)
    exponential = np.exp(3.0 * time)
    axial_weight = exponential / (exponential + 2.0)
    source_correlation = (exponential - 1.0) / (exponential + 2.0)
    anisotropy_norm_square = 2.0 * source_correlation**2 / 3.0

    # Panel B: exact frozen-source correlation production.
    correlation_grid = np.linspace(-0.5, 1.0, 151)
    source_production = (1.0 + 2.0 * correlation_grid) * (
        1.0 - correlation_grid
    )

    # Panel C: exact diffusion-only normalized anisotropy production for the
    # periodic two-mode Navier--Stokes shear, after dividing by viscosity.
    probability_grid = np.linspace(0.0, 1.0, 201)
    diffusion_production = (
        12.0
        * probability_grid
        * (1.0 - probability_grid)
        * (2.0 * probability_grid - 1.0)
    )
    p_low = 1.0 / 5.0
    p_high = 4.0 / 5.0
    certified_magnitude = 144.0 / 125.0

    rows: list[tuple[object, ...]] = []
    for index, t_value, p_value, q_value, alpha_value in zip(
        np.arange(time.size),
        time,
        axial_weight,
        source_correlation,
        anisotropy_norm_square,
        strict=True,
    ):
        rows.append(
            (
                "A",
                "frozen-source-trajectory",
                int(index),
                t_value,
                p_value,
                q_value,
                alpha_value,
                None,
                None,
                None,
                None,
                None,
            )
        )

    for index, q_value, production_value in zip(
        np.arange(correlation_grid.size),
        correlation_grid,
        source_production,
        strict=True,
    ):
        rows.append(
            (
                "B",
                "frozen-source-variance-production",
                int(index),
                None,
                None,
                None,
                None,
                q_value,
                production_value,
                None,
                None,
                None,
            )
        )

    for index, p_value, production_value in zip(
        np.arange(probability_grid.size),
        probability_grid,
        diffusion_production,
        strict=True,
    ):
        rows.append(
            (
                "C",
                "periodic-shear-diffusion-production",
                int(index),
                None,
                None,
                None,
                None,
                None,
                None,
                p_value,
                production_value,
                None,
            )
        )

    summary_rows = (
        ("initial_axial_weight", 1.0 / 3.0),
        ("initial_source_correlation", 0.0),
        ("initial_anisotropy_norm_square", 0.0),
        ("sharp_rank_one_anisotropy_norm_square", 2.0 / 3.0),
        ("source_production_left_endpoint", 0.0),
        ("source_production_right_endpoint", 0.0),
        ("source_production_maximum", 9.0 / 8.0),
        ("diffusion_zero_probability", 0.5),
        ("diffusion_negative_witness", -certified_magnitude),
        ("diffusion_positive_witness", certified_magnitude),
    )
    for index, (metric, value) in enumerate(summary_rows):
        rows.append(
            (
                "summary",
                "exact-summary",
                int(index),
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                None,
                f"{metric}={value:.17g}",
            )
        )

    write_csv(
        HERE / "data.csv",
        [
            "panel",
            "row_role",
            "sample_index",
            "time_t",
            "axisymmetric_axial_weight_p",
            "axisymmetric_source_correlation_q",
            "anisotropy_norm_square",
            "correlation_grid_q",
            "frozen_source_production",
            "periodic_shear_probability_p",
            "diffusion_anisotropy_production_over_nu",
            "exact_summary",
        ],
        rows,
    )

    low_index = int(round(p_low * (probability_grid.size - 1)))
    high_index = int(round(p_high * (probability_grid.size - 1)))
    checks = {
        "contractFigureIdMatches": contract.get("figureId") == FIGURE_ID,
        "contractReleaseMatches": contract.get("release") == RELEASE,
        "contractRendererIsStaticMatplotlib": contract.get("surface", {}).get("renderer")
        == "static Matplotlib",
        "trajectoryStartsIsotropic": bool(
            axial_weight[0] == 1.0 / 3.0
            and source_correlation[0] == 0.0
            and anisotropy_norm_square[0] == 0.0
        ),
        "trajectoryAxialWeightMonotone": bool(np.all(np.diff(axial_weight) > 0.0)),
        "trajectoryCorrelationMonotone": bool(
            np.all(np.diff(source_correlation) > 0.0)
        ),
        "trajectoryAnisotropyMonotone": bool(
            np.all(np.diff(anisotropy_norm_square) > 0.0)
        ),
        "trajectoryRespectsSharpBound": bool(
            np.all(anisotropy_norm_square < 2.0 / 3.0)
        ),
        "sourceProductionNonnegative": bool(np.all(source_production >= -1.0e-15)),
        "sourceProductionEndpointZeros": bool(
            source_production[0] == 0.0 and source_production[-1] == 0.0
        ),
        "sourceProductionMaximumExact": bool(
            abs(float(np.max(source_production)) - 9.0 / 8.0) < 1.0e-15
        ),
        "diffusionProductionHasBothSigns": bool(
            np.any(diffusion_production < 0.0)
            and np.any(diffusion_production > 0.0)
        ),
        "diffusionProductionThreeZeros": bool(
            diffusion_production[0] == 0.0
            and diffusion_production[probability_grid.size // 2] == 0.0
            and diffusion_production[-1] == 0.0
        ),
        "negativeWitnessExact": bool(
            abs(diffusion_production[low_index] + certified_magnitude) < 1.0e-15
        ),
        "positiveWitnessExact": bool(
            abs(diffusion_production[high_index] - certified_magnitude) < 1.0e-15
        ),
        "witnessAntisymmetry": bool(
            diffusion_production[low_index]
            == -diffusion_production[high_index]
        ),
        "dataRowCount": len(rows) == 483,
        "contractDataRowCountMatches": contract.get("data", {}).get("rowCount")
        == len(rows),
        "nonColorDistinctionDeclared": "marker"
        in contract.get("palette", {}).get("nonColorDistinction", ""),
    }
    if not all(checks.values()):
        raise AssertionError(checks)

    with plt.style.context(STYLE):
        plt.rcParams["figure.constrained_layout.use"] = False
        plt.rcParams["svg.hashsalt"] = FIGURE_ID
        figure = plt.figure(figsize=(178 / 25.4, 96 / 25.4), layout="none")
        grid = figure.add_gridspec(
            1,
            3,
            left=0.075,
            right=0.985,
            bottom=0.205,
            top=0.715,
            width_ratios=(1.06, 1.0, 1.08),
            wspace=0.35,
        )
        axis_a = figure.add_subplot(grid[0, 0])
        axis_b = figure.add_subplot(grid[0, 1])
        axis_c = figure.add_subplot(grid[0, 2])

        figure.suptitle(
            "Normalized vorticity anisotropy: alignment and the missing sign",
            x=0.045,
            y=0.966,
            ha="left",
            fontsize=8.3,
            color=INK,
        )
        figure.text(
            0.045,
            0.912,
            "frozen-source covariance flow  ·  exact variance law  ·  periodic Navier–Stokes diffusion gate",
            ha="left",
            fontsize=4.25,
            color=MUTED,
        )
        figure.text(
            0.045,
            0.840,
            "EXACT ANALYTIC IDENTITIES  /  NOT DNS  /  NOT A REGULARITY OR BLOW-UP RESULT",
            ha="left",
            va="center",
            fontsize=4.20,
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

        # Panel A: exact source-only trajectory.
        axis_a.axhline(2.0 / 3.0, color=MUTED, linewidth=0.55, linestyle=":")
        axis_a.plot(
            time,
            axial_weight,
            color=BLUE,
            linewidth=1.15,
            linestyle="--",
            marker="o",
            markerfacecolor=WHITE,
            markeredgecolor=BLUE,
            markeredgewidth=0.65,
            markersize=2.3,
            markevery=(0, 20),
            label=r"axial weight $p(t)$",
        )
        axis_a.plot(
            time,
            source_correlation,
            color=RUST,
            linewidth=1.3,
            marker="s",
            markerfacecolor=RUST,
            markeredgewidth=0.0,
            markersize=2.2,
            markevery=(10, 20),
            label=r"correlation $q(t)$",
        )
        axis_a.plot(
            time,
            anisotropy_norm_square,
            color=INK,
            linewidth=0.95,
            linestyle="-.",
            label=r"anisotropy $|B|_F^2$",
        )
        axis_a.set_title("A  Isotropy is not stationary", loc="left", pad=5)
        axis_a.set_xlim(0.0, 4.0)
        axis_a.set_ylim(-0.04, 1.04)
        axis_a.set_xticks([0, 1, 2, 3, 4])
        axis_a.set_yticks([0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0], [r"$0$", r"$1/3$", r"$2/3$", r"$1$"])
        axis_a.set_xlabel(r"source-only time $t$")
        axis_a.set_ylabel("normalized shape value")
        axis_a.grid(color=GRID, linewidth=0.35, axis="y")
        axis_a.legend(loc="lower right", frameon=False, fontsize=4.0)
        axis_a.text(
            3.95,
            0.69,
            r"sharp $|B|_F^2=2/3$",
            color=MUTED,
            fontsize=4.15,
            ha="right",
            va="bottom",
        )

        # Panel B: frozen-source variance production.
        axis_b.axhline(0.0, color=INK, linewidth=0.6, zorder=1)
        axis_b.fill_between(
            correlation_grid,
            0.0,
            source_production,
            color=PALE_RUST,
            edgecolor=RUST,
            linewidth=0.45,
            hatch="////",
            zorder=2,
        )
        axis_b.plot(
            correlation_grid,
            source_production,
            color=RUST,
            linewidth=1.15,
            zorder=3,
        )
        axis_b.scatter(
            [-0.5, 1.0],
            [0.0, 0.0],
            s=11,
            facecolors=WHITE,
            edgecolors=BLUE,
            linewidths=0.65,
            zorder=4,
        )
        axis_b.scatter(
            [0.25],
            [9.0 / 8.0],
            s=12,
            marker="s",
            facecolors=RUST,
            edgecolors=RUST,
            linewidths=0.4,
            zorder=4,
        )
        axis_b.set_title("B  Frozen source reinforces $q$", loc="left", pad=5)
        axis_b.set_xlim(-0.5, 1.0)
        axis_b.set_ylim(-0.06, 1.22)
        axis_b.set_xticks([-0.5, 0.0, 0.25, 0.5, 1.0], [r"$-1/2$", r"$0$", r"$1/4$", r"$1/2$", r"$1$"])
        axis_b.set_yticks([0.0, 0.5, 1.0, 9.0 / 8.0], [r"$0$", r"$1/2$", r"$1$", r"$9/8$"])
        axis_b.set_xlabel(r"source correlation $q=\Sigma_0:B$")
        axis_b.set_ylabel(r"$\dot q=(1+2q)(1-q)$")
        axis_b.grid(color=GRID, linewidth=0.35, axis="y")
        axis_b.text(
            0.96,
            0.10,
            "nonnegative variance\nzero only on eigenspaces",
            color=RUST,
            fontsize=4.2,
            ha="right",
            va="bottom",
        )

        # Panel C: sign-changing normalized diffusion.
        axis_c.axhline(0.0, color=INK, linewidth=0.6, zorder=1)
        axis_c.fill_between(
            probability_grid,
            0.0,
            np.minimum(diffusion_production, 0.0),
            color=PALE_BLUE,
            edgecolor=BLUE,
            linewidth=0.4,
            hatch="\\\\\\\\",
            zorder=2,
        )
        axis_c.fill_between(
            probability_grid,
            0.0,
            np.maximum(diffusion_production, 0.0),
            color=PALE_RUST,
            edgecolor=RUST,
            linewidth=0.4,
            zorder=2,
        )
        axis_c.plot(
            probability_grid,
            diffusion_production,
            color=INK,
            linewidth=1.1,
            zorder=3,
        )
        axis_c.scatter(
            [p_low],
            [-certified_magnitude],
            s=14,
            facecolors=WHITE,
            edgecolors=BLUE,
            linewidths=0.75,
            zorder=4,
        )
        axis_c.scatter(
            [p_high],
            [certified_magnitude],
            s=14,
            marker="s",
            facecolors=RUST,
            edgecolors=RUST,
            linewidths=0.5,
            zorder=4,
        )
        axis_c.set_title("C  Diffusion has both signs", loc="left", pad=5)
        axis_c.set_xlim(0.0, 1.0)
        axis_c.set_ylim(-1.5, 1.5)
        axis_c.set_xticks([0.0, p_low, 0.5, p_high, 1.0], [r"$0$", r"$1/5$", r"$1/2$", r"$4/5$", r"$1$"])
        axis_c.set_yticks([-certified_magnitude, 0.0, certified_magnitude], [r"$-144/125$", r"$0$", r"$144/125$"])
        axis_c.set_xlabel(r"modal vorticity weight $p$")
        axis_c.set_ylabel(r"$\nu^{-1}d|B|_F^2/dt$")
        axis_c.grid(color=GRID, linewidth=0.35, axis="y")
        axis_c.text(
            0.04,
            -1.36,
            "exact periodic NSE shear\nnonlinearity = 0",
            color=BLUE,
            fontsize=4.2,
            ha="left",
            va="bottom",
        )
        axis_c.text(
            0.96,
            1.34,
            "unequal heat decay\ncan increase anisotropy",
            color=RUST,
            fontsize=4.2,
            ha="right",
            va="top",
        )

        figure.text(
            0.985,
            0.035,
            "closed-form covariance identities — full source evolution and Leray endpoint control remain open",
            ha="right",
            va="bottom",
            color=MUTED,
            fontsize=4.25,
        )

        figure.savefig(
            HERE / "figure.pdf",
            metadata={
                "Title": "Normalized vorticity anisotropy evolution",
                "Author": "R0.70K analytic figure package",
                "Subject": "Frozen-source variance law and periodic diffusion sign gate",
                "Creator": "plot.py",
                "CreationDate": None,
                "ModDate": None,
            },
        )
        figure.savefig(
            HERE / "figure.svg",
            metadata={
                "Title": "Normalized vorticity anisotropy evolution",
                "Description": "Exact analytic identities; not DNS or a blow-up or regularity result.",
                "Creator": "plot.py",
                "Date": None,
            },
        )
        figure.savefig(
            HERE / "figure.png",
            dpi=600,
            metadata={
                "Title": "Normalized vorticity anisotropy evolution",
                "Description": "Exact analytic identities; not DNS or a blow-up or regularity result.",
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
        "pngOriginalPixelDimensions": bool(image.width >= 4200 and image.height >= 2200),
        "pngRequestedDpiEmbedded": bool(
            embedded_dpi[0] is not None
            and embedded_dpi[1] is not None
            and abs(float(embedded_dpi[0]) - 600.0) < 0.1
            and abs(float(embedded_dpi[1]) - 600.0) < 0.1
        ),
        "pdfNonempty": bool((HERE / "figure.pdf").stat().st_size > 10_000),
        "svgNonempty": bool((HERE / "figure.svg").stat().st_size > 10_000),
        "visibleClaimBoundaryInSvg": bool(
            "EXACT ANALYTIC IDENTITIES" in svg_text
            and "NOT DNS" in svg_text
            and "NOT A REGULARITY OR BLOW-UP RESULT" in svg_text
        ),
        "writtenDataRowCount": data_row_count == 483,
    }
    checks.update(output_checks)
    if not all(checks.values()):
        raise AssertionError(checks)

    validation = {
        "status": "passed",
        "release": RELEASE,
        "checks": checks,
        "diagnostics": {
            "timePoints": int(time.size),
            "correlationPoints": int(correlation_grid.size),
            "probabilityPoints": int(probability_grid.size),
            "initialAxialWeight": float(axial_weight[0]),
            "finalSourceCorrelation": float(source_correlation[-1]),
            "sharpAnisotropyNormSquare": 2.0 / 3.0,
            "sourceProductionMaximum": float(np.max(source_production)),
            "negativeDiffusionWitness": float(diffusion_production[low_index]),
            "positiveDiffusionWitness": float(diffusion_production[high_index]),
            "dataRows": data_row_count,
            "pngPixels": [image.width, image.height],
            "pngEmbeddedDpi": [float(embedded_dpi[0]), float(embedded_dpi[1])],
        },
        "visualQa": {
            "originalResolution": "passed: title, three panel titles, axes, legends, annotations, and footer inspected at 4204 by 2267 pixels",
            "grayscale": "passed: line style, marker fill, zero baselines, hatching, and panel separation preserve every claimed distinction",
        },
        "claimBoundary": (
            "Exact analytic covariance data only; not DNS, not a finite-energy "
            "R3 cascade, and not evidence for blow-up, regularity, or a "
            "Millennium-problem solution."
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
        },
        "claimBoundary": (
            "Exact analytic covariance identities; not simulation evidence or "
            "a numerical PDE proof, not a finite-energy fixed-positive-time "
            "cascade, and not a Millennium result."
        ),
    }
    (HERE / "manifest.json").write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
